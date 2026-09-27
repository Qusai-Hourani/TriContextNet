"""BraTS interface for the pinned TinyU-Net source."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
import types
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import torch
from torch import nn


PROJECT_ROOT = Path(__file__).resolve().parents[2]
UPSTREAM_SOURCE = PROJECT_ROOT / "external" / "TinyU-Net" / "TinyU-Net.py"
UPSTREAM_COMMIT = "73147721edf36dcb0101f1ec383cb97fe42e36df"
UPSTREAM_SOURCE_SHA256 = (
    "0ed32903d206bb419d4ec2be843981874a1c69f792401fa10f15d39d561d611a"
)

BRATS_IN_CHANNELS = 4
BRATS_NUM_CLASSES = 4
BRATS_IMAGE_SIZE = 256


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _unavailable_optional_tool(*_args: object, **_kwargs: object) -> None:
    raise RuntimeError(
        "This optional upstream reporting helper is intentionally unavailable "
        "through the model wrapper."
    )


@contextmanager
def _optional_import_shims() -> Iterator[None]:
    """Satisfy upstream imports used only by its ``__main__`` report.

    TinyU-Net imports thop and torchsummary at module scope, although neither
    dependency participates in construction or forward execution. When either
    package is absent, a temporary nonfunctional module is exposed only while
    the pinned source is imported. Existing modules are never replaced.
    """

    inserted: list[str] = []
    definitions = {
        "thop": {
            "clever_format": _unavailable_optional_tool,
            "profile": _unavailable_optional_tool,
        },
        "torchsummary": {"summary": _unavailable_optional_tool},
    }
    for module_name, attributes in definitions.items():
        if importlib.util.find_spec(module_name) is None:
            module = types.ModuleType(module_name)
            for attribute_name, value in attributes.items():
                setattr(module, attribute_name, value)
            sys.modules[module_name] = module
            inserted.append(module_name)
    try:
        yield
    finally:
        for module_name in inserted:
            sys.modules.pop(module_name, None)


def _load_upstream_module() -> types.ModuleType:
    if not UPSTREAM_SOURCE.is_file():
        raise FileNotFoundError(f"Pinned TinyU-Net source not found: {UPSTREAM_SOURCE}")
    observed_hash = _sha256(UPSTREAM_SOURCE)
    if observed_hash != UPSTREAM_SOURCE_SHA256:
        raise RuntimeError(
            "TinyU-Net source identity mismatch: "
            f"expected {UPSTREAM_SOURCE_SHA256}, observed {observed_hash}"
        )
    spec = importlib.util.spec_from_file_location(
        "_pinned_tiny_unet_upstream", UPSTREAM_SOURCE
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load pinned TinyU-Net source: {UPSTREAM_SOURCE}")
    module = importlib.util.module_from_spec(spec)
    with _optional_import_shims():
        spec.loader.exec_module(module)
    return module


class BraTSTinyUNet(nn.Module):
    """Thin invariant-checking wrapper around the exact upstream model."""

    def __init__(self) -> None:
        super().__init__()
        upstream = _load_upstream_module()
        self.upstream = upstream.TinyUNet(
            in_channels=BRATS_IN_CHANNELS,
            num_classes=BRATS_NUM_CLASSES,
        )

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        if inputs.ndim != 4 or tuple(inputs.shape[1:]) != (
            BRATS_IN_CHANNELS,
            BRATS_IMAGE_SIZE,
            BRATS_IMAGE_SIZE,
        ):
            raise ValueError(
                "TinyU-Net requires [batch, 4, 256, 256], got "
                f"{tuple(inputs.shape)}"
            )
        logits = self.upstream(inputs)
        if not torch.is_tensor(logits):
            raise TypeError(
                "Pinned TinyU-Net returned an unexpected auxiliary/container output."
            )
        expected_shape = (
            inputs.shape[0],
            BRATS_NUM_CLASSES,
            BRATS_IMAGE_SIZE,
            BRATS_IMAGE_SIZE,
        )
        if tuple(logits.shape) != expected_shape:
            raise RuntimeError(
                f"TinyU-Net logits shape {tuple(logits.shape)} != {expected_shape}"
            )
        return logits


def create_brats_tiny_unet() -> BraTSTinyUNet:
    """Construct TinyU-Net from scratch with the frozen interface."""

    return BraTSTinyUNet()
