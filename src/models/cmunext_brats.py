"""BraTS interface for the pinned base CMUNeXt source."""

from __future__ import annotations

import hashlib
import importlib.util
import types
from pathlib import Path

import torch
from torch import nn


PROJECT_ROOT = Path(__file__).resolve().parents[2]
UPSTREAM_SOURCE = PROJECT_ROOT / "external" / "CMUNeXt" / "network" / "CMUNeXt.py"
UPSTREAM_COMMIT = "affbf03ef631bb318d87b73ef97b2eacd0a5de85"
UPSTREAM_SOURCE_SHA256 = (
    "453c602bb4b8d334c79112aded3ccdb145816b370cf0eb0b0b9fa01934b4d020"
)

BRATS_IN_CHANNELS = 4
BRATS_NUM_CLASSES = 4
BRATS_IMAGE_SIZE = 256
DIMS = [16, 32, 128, 160, 256]
DEPTHS = [1, 1, 1, 3, 1]
KERNELS = [3, 3, 7, 7, 7]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _load_upstream_module() -> types.ModuleType:
    if not UPSTREAM_SOURCE.is_file():
        raise FileNotFoundError(f"Pinned CMUNeXt source not found: {UPSTREAM_SOURCE}")
    observed_hash = _sha256(UPSTREAM_SOURCE)
    if observed_hash != UPSTREAM_SOURCE_SHA256:
        raise RuntimeError(
            "CMUNeXt source identity mismatch: "
            f"expected {UPSTREAM_SOURCE_SHA256}, observed {observed_hash}"
        )
    spec = importlib.util.spec_from_file_location(
        "_pinned_cmunext_upstream", UPSTREAM_SOURCE
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load pinned CMUNeXt source: {UPSTREAM_SOURCE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BraTSCMUNeXt(nn.Module):
    """Thin invariant-checking wrapper around exact base CMUNeXt."""

    def __init__(self) -> None:
        super().__init__()
        upstream = _load_upstream_module()
        self.upstream = upstream.CMUNeXt(
            input_channel=BRATS_IN_CHANNELS,
            num_classes=BRATS_NUM_CLASSES,
            dims=list(DIMS),
            depths=list(DEPTHS),
            kernels=list(KERNELS),
        )

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        if inputs.ndim != 4 or tuple(inputs.shape[1:]) != (
            BRATS_IN_CHANNELS,
            BRATS_IMAGE_SIZE,
            BRATS_IMAGE_SIZE,
        ):
            raise ValueError(
                f"CMUNeXt requires [batch, 4, 256, 256], got {tuple(inputs.shape)}"
            )
        logits = self.upstream(inputs)
        if not torch.is_tensor(logits):
            raise TypeError("Pinned CMUNeXt returned an unexpected container output.")
        expected_shape = (
            inputs.shape[0],
            BRATS_NUM_CLASSES,
            BRATS_IMAGE_SIZE,
            BRATS_IMAGE_SIZE,
        )
        if tuple(logits.shape) != expected_shape:
            raise RuntimeError(
                f"CMUNeXt logits shape {tuple(logits.shape)} != {expected_shape}"
            )
        return logits


def create_brats_cmunext() -> BraTSCMUNeXt:
    """Construct base CMUNeXt from scratch at the frozen configuration."""

    return BraTSCMUNeXt()
