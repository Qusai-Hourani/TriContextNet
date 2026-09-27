"""Simple 2.5D BraTS interface for pinned MK-UNet."""

from __future__ import annotations

from mkunet_brats import (
    BRATS_NUM_CLASSES,
    PUBLISHED_CHANNELS,
    _load_upstream_module,
)


CONTEXT_SLICES = 3
MODALITIES_PER_SLICE = 4
BRATS_2P5D_IN_CHANNELS = CONTEXT_SLICES * MODALITIES_PER_SLICE
CONTEXT_ORDER = ("previous", "centre", "next")
MODALITY_ORDER = ("T1", "T1ce", "T2", "FLAIR")


def create_brats_mkunet_2p5d():
    """Instantiate pinned MK-UNet with only encoder1 adapted to 12 inputs.

    Input channels are slice-major: previous T1/T1ce/T2/FLAIR, then centre,
    then next. The pinned upstream model otherwise remains unchanged, including
    its one-element output list and eager computation of discarded heads.
    """

    upstream = _load_upstream_module()
    return upstream.MK_UNet(
        in_channels=BRATS_2P5D_IN_CHANNELS,
        num_classes=BRATS_NUM_CLASSES,
        channels=list(PUBLISHED_CHANNELS),
    )
