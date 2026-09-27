"""Project-owned 2D Attention U-Net frozen.

The ordinary encoder, bottleneck, decoder, and prediction layers are inherited
unchanged from the ``UNetBraTS`` implementation.  Only the three
deeper skip paths receive the attention modules.

Architectural reference (MIT), pinned revision:
https://github.com/ozan-oktay/Attention-Gated-Networks/tree/eee4881fdc31920efd873773e0b744df8dacbfb6
"""

from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F

from unet_brats import (
    BRATS_IN_CHANNELS,
    BRATS_NUM_CLASSES,
    FEATURE_CHANNELS,
    UNetBraTS,
)


UPSTREAM_REFERENCE_REVISION = "eee4881fdc31920efd873773e0b744df8dacbfb6"


class GridAttentionBlock2D(nn.Module):
    """Oktay-style grid-attention ``concatenation`` operation in 2D."""

    def __init__(
        self,
        skip_channels: int,
        gating_channels: int,
        intermediate_channels: int,
    ) -> None:
        super().__init__()
        self.skip_channels = skip_channels
        self.gating_channels = gating_channels
        self.intermediate_channels = intermediate_channels

        self.theta = nn.Conv2d(
            skip_channels,
            intermediate_channels,
            kernel_size=2,
            stride=2,
            padding=0,
            bias=False,
        )
        self.phi = nn.Conv2d(
            gating_channels,
            intermediate_channels,
            kernel_size=1,
            stride=1,
            padding=0,
            bias=True,
        )
        self.psi = nn.Conv2d(
            intermediate_channels,
            1,
            kernel_size=1,
            stride=1,
            padding=0,
            bias=True,
        )
        self.output_transform = nn.Sequential(
            nn.Conv2d(
                skip_channels,
                skip_channels,
                kernel_size=1,
                stride=1,
                padding=0,
                bias=True,
            ),
            nn.BatchNorm2d(skip_channels),
        )

    def forward(
        self,
        skip_feature: torch.Tensor,
        gating_feature: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        skip_spatial_size = skip_feature.shape[2:]
        theta_skip = self.theta(skip_feature)
        phi_gating = F.interpolate(
            self.phi(gating_feature),
            size=theta_skip.shape[2:],
            mode="bilinear",
            align_corners=False,
        )
        compatibility = F.relu(theta_skip + phi_gating, inplace=True)
        coefficients = torch.sigmoid(self.psi(compatibility))
        coefficients = F.interpolate(
            coefficients,
            size=skip_spatial_size,
            mode="bilinear",
            align_corners=False,
        )
        attended_skip = coefficients.expand_as(skip_feature) * skip_feature
        transformed_skip = self.output_transform(attended_skip)
        return transformed_skip, coefficients


class AttentionGate2D(nn.Module):
    """One released single-attention block and its gate-combination transform."""

    def __init__(
        self,
        skip_channels: int,
        gating_channels: int,
        intermediate_channels: int,
    ) -> None:
        super().__init__()
        self.grid_attention = GridAttentionBlock2D(
            skip_channels=skip_channels,
            gating_channels=gating_channels,
            intermediate_channels=intermediate_channels,
        )
        self.combine_gate = nn.Sequential(
            nn.Conv2d(
                skip_channels,
                skip_channels,
                kernel_size=1,
                stride=1,
                padding=0,
                bias=True,
            ),
            nn.BatchNorm2d(skip_channels),
            nn.ReLU(inplace=True),
        )

    def forward(
        self,
        skip_feature: torch.Tensor,
        gating_feature: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        gated_skip, coefficients = self.grid_attention(
            skip_feature,
            gating_feature,
        )
        return self.combine_gate(gated_skip), coefficients


class InitialGatingSignal2D(nn.Sequential):
    """Two-dimensional analogue of the released grid-gating signal."""

    def __init__(self, channels: int) -> None:
        super().__init__(
            nn.Conv2d(
                channels,
                channels,
                kernel_size=1,
                stride=1,
                padding=0,
                bias=True,
            ),
            nn.BatchNorm2d(channels),
            nn.ReLU(inplace=True),
        )


class AttentionUNetBraTS(UNetBraTS):
    """U-Net with attention-gated deep skips."""

    def __init__(self) -> None:
        super().__init__()
        _, c2, c3, c4, bottleneck_channels = FEATURE_CHANNELS

        self.initial_gating = InitialGatingSignal2D(bottleneck_channels)
        self.attention4 = AttentionGate2D(
            skip_channels=c4,
            gating_channels=bottleneck_channels,
            intermediate_channels=c4,
        )
        self.attention3 = AttentionGate2D(
            skip_channels=c3,
            gating_channels=c4,
            intermediate_channels=c3,
        )
        self.attention2 = AttentionGate2D(
            skip_channels=c2,
            gating_channels=c3,
            intermediate_channels=c2,
        )

        self._initialize_attention_weights()

    def _initialize_attention_weights(self) -> None:
        attention_roots = (
            self.initial_gating,
            self.attention4,
            self.attention3,
            self.attention2,
        )
        for root in attention_roots:
            for module in root.modules():
                if isinstance(module, nn.Conv2d):
                    nn.init.kaiming_normal_(
                        module.weight,
                        a=0,
                        mode="fan_in",
                        nonlinearity="relu",
                    )
                    # The pinned helper leaves convolution biases at their
                    # framework defaults; preserve that reference behavior.
                elif isinstance(module, nn.BatchNorm2d):
                    nn.init.normal_(module.weight, mean=1.0, std=0.02)
                    nn.init.zeros_(module.bias)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        encoder1 = self.encoder1(inputs)
        encoder2 = self.encoder2(self.pool(encoder1))
        encoder3 = self.encoder3(self.pool(encoder2))
        encoder4 = self.encoder4(self.pool(encoder3))
        bottleneck = self.bottleneck(self.pool(encoder4))

        gating = self.initial_gating(bottleneck)
        gated_encoder4, _ = self.attention4(encoder4, gating)
        decoder4 = self.upconv4(bottleneck)
        decoder4 = self.decoder4(
            torch.cat((gated_encoder4, decoder4), dim=1)
        )

        gated_encoder3, _ = self.attention3(encoder3, decoder4)
        decoder3 = self.upconv3(decoder4)
        decoder3 = self.decoder3(
            torch.cat((gated_encoder3, decoder3), dim=1)
        )

        gated_encoder2, _ = self.attention2(encoder2, decoder3)
        decoder2 = self.upconv2(decoder3)
        decoder2 = self.decoder2(
            torch.cat((gated_encoder2, decoder2), dim=1)
        )

        decoder1 = self.upconv1(decoder2)
        decoder1 = self.decoder1(torch.cat((encoder1, decoder1), dim=1))
        return self.output_conv(decoder1)


def create_brats_attention_unet() -> AttentionUNetBraTS:
    """Instantiate the exact project-owned Attention U-Net."""

    return AttentionUNetBraTS()


__all__ = [
    "AttentionGate2D",
    "AttentionUNetBraTS",
    "BRATS_IN_CHANNELS",
    "BRATS_NUM_CLASSES",
    "FEATURE_CHANNELS",
    "GridAttentionBlock2D",
    "InitialGatingSignal2D",
    "UPSTREAM_REFERENCE_REVISION",
    "create_brats_attention_unet",
]
