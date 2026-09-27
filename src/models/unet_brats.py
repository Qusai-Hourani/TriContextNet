"""Project-owned standard 2D U-Net finalized."""

from __future__ import annotations

import torch
from torch import nn


BRATS_IN_CHANNELS = 4
BRATS_NUM_CLASSES = 4
FEATURE_CHANNELS = (64, 128, 256, 512, 1024)


class DoubleConv(nn.Sequential):
    """Two padded 3 x 3 convolutions, each followed by ReLU."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__(
            nn.Conv2d(
                in_channels,
                out_channels,
                kernel_size=3,
                stride=1,
                padding=1,
                bias=True,
            ),
            nn.ReLU(inplace=False),
            nn.Conv2d(
                out_channels,
                out_channels,
                kernel_size=3,
                stride=1,
                padding=1,
                bias=True,
            ),
            nn.ReLU(inplace=False),
        )


class UNetBraTS(nn.Module):
    """Standard 2D U-Net with the fixed four-channel BraTS interface."""

    def __init__(self) -> None:
        super().__init__()
        c1, c2, c3, c4, bottleneck_channels = FEATURE_CHANNELS

        self.encoder1 = DoubleConv(BRATS_IN_CHANNELS, c1)
        self.encoder2 = DoubleConv(c1, c2)
        self.encoder3 = DoubleConv(c2, c3)
        self.encoder4 = DoubleConv(c3, c4)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.bottleneck = DoubleConv(c4, bottleneck_channels)

        self.upconv4 = nn.ConvTranspose2d(
            bottleneck_channels, c4, kernel_size=2, stride=2, bias=True
        )
        self.decoder4 = DoubleConv(c4 + c4, c4)
        self.upconv3 = nn.ConvTranspose2d(
            c4, c3, kernel_size=2, stride=2, bias=True
        )
        self.decoder3 = DoubleConv(c3 + c3, c3)
        self.upconv2 = nn.ConvTranspose2d(
            c3, c2, kernel_size=2, stride=2, bias=True
        )
        self.decoder2 = DoubleConv(c2 + c2, c2)
        self.upconv1 = nn.ConvTranspose2d(
            c2, c1, kernel_size=2, stride=2, bias=True
        )
        self.decoder1 = DoubleConv(c1 + c1, c1)

        self.output_conv = nn.Conv2d(
            c1, BRATS_NUM_CLASSES, kernel_size=1, stride=1, padding=0, bias=True
        )

        self._initialize_weights()

    def _initialize_weights(self) -> None:
        for module in self.modules():
            if isinstance(module, (nn.Conv2d, nn.ConvTranspose2d)):
                nn.init.kaiming_normal_(
                    module.weight,
                    mode="fan_in",
                    nonlinearity="relu",
                )
                if module.bias is not None:
                    nn.init.zeros_(module.bias)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        encoder1 = self.encoder1(inputs)
        encoder2 = self.encoder2(self.pool(encoder1))
        encoder3 = self.encoder3(self.pool(encoder2))
        encoder4 = self.encoder4(self.pool(encoder3))
        bottleneck = self.bottleneck(self.pool(encoder4))

        decoder4 = self.upconv4(bottleneck)
        decoder4 = self.decoder4(torch.cat((encoder4, decoder4), dim=1))
        decoder3 = self.upconv3(decoder4)
        decoder3 = self.decoder3(torch.cat((encoder3, decoder3), dim=1))
        decoder2 = self.upconv2(decoder3)
        decoder2 = self.decoder2(torch.cat((encoder2, decoder2), dim=1))
        decoder1 = self.upconv1(decoder2)
        decoder1 = self.decoder1(torch.cat((encoder1, decoder1), dim=1))

        return self.output_conv(decoder1)


def create_brats_unet() -> UNetBraTS:
    """Instantiate the exact project-owned U-Net finalized."""

    return UNetBraTS()
