"""Project-owned 2D DeepLabV3+ frozen.

The encoder topology is TorchVision ResNet-50 V1.5.  The segmentation model
uses no pretrained weights and deliberately excludes the classification
average-pooling and fully connected layers.
"""

from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F
from torchvision.models import resnet50


BRATS_IN_CHANNELS = 4
BRATS_NUM_CLASSES = 4
ASPP_CHANNELS = 256
ASPP_RATES = (6, 12, 18)
LOW_LEVEL_CHANNELS = 256
LOW_LEVEL_PROJECTION_CHANNELS = 48
FUSED_DECODER_CHANNELS = ASPP_CHANNELS + LOW_LEVEL_PROJECTION_CHANNELS
TORCHVISION_RELEASE = "v0.28.0"
TORCHVISION_REVISION = "8fb87713a24951e639c494b0f2a8a81b5f8e33a6"
DEEPLAB_REFERENCE_REVISION = "bdcfdd30306a7df694fb281cd24884769009d03e"


class ResNet50V15Encoder(nn.Module):
    """ResNet-50 V1.5 feature encoder with a four-modality input stem."""

    def __init__(self) -> None:
        super().__init__()
        backbone = resnet50(
            weights=None,
            progress=False,
            zero_init_residual=False,
            replace_stride_with_dilation=[False, False, True],
        )
        self.conv1 = nn.Conv2d(
            BRATS_IN_CHANNELS,
            64,
            kernel_size=7,
            stride=2,
            padding=3,
            bias=False,
        )
        self.bn1 = backbone.bn1
        self.relu = backbone.relu
        self.maxpool = backbone.maxpool
        self.layer1 = backbone.layer1
        self.layer2 = backbone.layer2
        self.layer3 = backbone.layer3
        self.layer4 = backbone.layer4

    def forward(self, inputs: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        features = self.conv1(inputs)
        features = self.bn1(features)
        features = self.relu(features)
        features = self.maxpool(features)

        low_level = self.layer1(features)
        features = self.layer2(low_level)
        features = self.layer3(features)
        high_level = self.layer4(features)
        return low_level, high_level


class ConvBNReLU(nn.Sequential):
    """Convolution followed by ordinary trainable BatchNorm and ReLU."""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        *,
        kernel_size: int,
        padding: int = 0,
    ) -> None:
        super().__init__(
            nn.Conv2d(
                in_channels,
                out_channels,
                kernel_size=kernel_size,
                padding=padding,
                bias=False,
            ),
            nn.BatchNorm2d(
                out_channels,
                eps=1e-5,
                momentum=0.1,
                affine=True,
                track_running_stats=True,
            ),
            nn.ReLU(inplace=True),
        )


class SeparableConvBNReLU(nn.Module):
    """Depthwise 3x3 then pointwise 1x1, each with BatchNorm and ReLU."""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        *,
        dilation: int = 1,
    ) -> None:
        super().__init__()
        self.depthwise = nn.Conv2d(
            in_channels,
            in_channels,
            kernel_size=3,
            stride=1,
            padding=dilation,
            dilation=dilation,
            groups=in_channels,
            bias=False,
        )
        self.depthwise_bn = nn.BatchNorm2d(
            in_channels,
            eps=1e-5,
            momentum=0.1,
            affine=True,
            track_running_stats=True,
        )
        self.depthwise_relu = nn.ReLU(inplace=True)
        self.pointwise = nn.Conv2d(
            in_channels,
            out_channels,
            kernel_size=1,
            bias=False,
        )
        self.pointwise_bn = nn.BatchNorm2d(
            out_channels,
            eps=1e-5,
            momentum=0.1,
            affine=True,
            track_running_stats=True,
        )
        self.pointwise_relu = nn.ReLU(inplace=True)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        features = self.depthwise(inputs)
        features = self.depthwise_bn(features)
        features = self.depthwise_relu(features)
        features = self.pointwise(features)
        features = self.pointwise_bn(features)
        return self.pointwise_relu(features)


class ASPPImagePooling(nn.Module):
    """The image-level fifth ASPP branch."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.pool = nn.AdaptiveAvgPool2d(output_size=1)
        self.projection = ConvBNReLU(
            in_channels,
            out_channels,
            kernel_size=1,
        )

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        spatial_size = inputs.shape[-2:]
        features = self.pool(inputs)
        features = self.projection(features)
        return F.interpolate(
            features,
            size=spatial_size,
            mode="bilinear",
            align_corners=False,
        )


class AtrousSpatialPyramidPooling(nn.Module):
    """Five-branch ASPP and its 1280-to-256 projection."""

    def __init__(self, in_channels: int = 2048) -> None:
        super().__init__()
        self.branches = nn.ModuleList(
            [
                ConvBNReLU(in_channels, ASPP_CHANNELS, kernel_size=1),
                *[
                    SeparableConvBNReLU(
                        in_channels,
                        ASPP_CHANNELS,
                        dilation=rate,
                    )
                    for rate in ASPP_RATES
                ],
                ASPPImagePooling(in_channels, ASPP_CHANNELS),
            ]
        )
        self.project = nn.Sequential(
            nn.Conv2d(
                5 * ASPP_CHANNELS,
                ASPP_CHANNELS,
                kernel_size=1,
                bias=False,
            ),
            nn.BatchNorm2d(
                ASPP_CHANNELS,
                eps=1e-5,
                momentum=0.1,
                affine=True,
                track_running_stats=True,
            ),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.1),
        )

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        branch_features = [branch(inputs) for branch in self.branches]
        return self.project(torch.cat(branch_features, dim=1))


class DeepLabV3PlusBraTS(nn.Module):
    """Exact four-input/four-logit DeepLabV3+."""

    def __init__(self) -> None:
        super().__init__()
        self.encoder = ResNet50V15Encoder()
        self.aspp = AtrousSpatialPyramidPooling(in_channels=2048)
        self.low_level_projection = ConvBNReLU(
            LOW_LEVEL_CHANNELS,
            LOW_LEVEL_PROJECTION_CHANNELS,
            kernel_size=1,
        )
        self.refinement_blocks = nn.Sequential(
            SeparableConvBNReLU(FUSED_DECODER_CHANNELS, ASPP_CHANNELS),
            SeparableConvBNReLU(ASPP_CHANNELS, ASPP_CHANNELS),
        )
        self.classifier = nn.Conv2d(
            ASPP_CHANNELS,
            BRATS_NUM_CLASSES,
            kernel_size=1,
            bias=True,
        )
        self._initialize_weights()

    def _initialize_weights(self) -> None:
        for module in self.modules():
            if isinstance(module, nn.Conv2d):
                nn.init.kaiming_normal_(
                    module.weight,
                    mode="fan_out",
                    nonlinearity="relu",
                )
            elif isinstance(module, nn.BatchNorm2d):
                nn.init.ones_(module.weight)
                nn.init.zeros_(module.bias)

        nn.init.normal_(self.classifier.weight, mean=0.0, std=0.01)
        nn.init.zeros_(self.classifier.bias)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        input_spatial_size = inputs.shape[-2:]
        low_level, high_level = self.encoder(inputs)
        high_level = self.aspp(high_level)
        high_level = F.interpolate(
            high_level,
            size=low_level.shape[-2:],
            mode="bilinear",
            align_corners=False,
        )
        low_level = self.low_level_projection(low_level)
        features = torch.cat((high_level, low_level), dim=1)
        features = self.refinement_blocks(features)
        logits = self.classifier(features)
        return F.interpolate(
            logits,
            size=input_spatial_size,
            mode="bilinear",
            align_corners=False,
        )


def create_brats_deeplabv3plus() -> DeepLabV3PlusBraTS:
    """Instantiate the project-owned DeepLabV3+ frozen."""

    return DeepLabV3PlusBraTS()


__all__ = [
    "ASPP_CHANNELS",
    "ASPP_RATES",
    "AtrousSpatialPyramidPooling",
    "BRATS_IN_CHANNELS",
    "BRATS_NUM_CLASSES",
    "DEEPLAB_REFERENCE_REVISION",
    "DeepLabV3PlusBraTS",
    "FUSED_DECODER_CHANNELS",
    "LOW_LEVEL_CHANNELS",
    "LOW_LEVEL_PROJECTION_CHANNELS",
    "ResNet50V15Encoder",
    "SeparableConvBNReLU",
    "TORCHVISION_RELEASE",
    "TORCHVISION_REVISION",
    "create_brats_deeplabv3plus",
]
