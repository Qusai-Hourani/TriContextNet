"""BraTS interface for pinned Rolling-Unet-S."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
import types
from pathlib import Path

import torch
from torch import nn


PROJECT_ROOT = Path(__file__).resolve().parents[2]
UPSTREAM_DIR = PROJECT_ROOT / "external" / "Rolling-Unet"
UPSTREAM_SOURCE = UPSTREAM_DIR / "archs.py"
UPSTREAM_UTILS = UPSTREAM_DIR / "utils.py"
UPSTREAM_COMMIT = "8a43d40c218917e454c0584a853757e3a2cf9c80"
UPSTREAM_SOURCE_SHA256 = (
    "4e9523fa045d70fe8c1dc68acef428c463b736971a4b085fe9c294034ea023b3"
)
UPSTREAM_UTILS_SHA256 = (
    "bb76bcf004e5832c291aa3bdd9372e2283b4e8463873295f3f629cd8d5911995"
)

BRATS_IN_CHANNELS = 4
BRATS_NUM_CLASSES = 4
BRATS_IMAGE_SIZE = 256
EMBED_DIMS = [16, 32, 64, 128, 256]
NUM_HEADS = [1, 2, 4, 8]
DEPTHS = [1, 1, 1]
SR_RATIOS = [8, 4, 2, 1]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _load_file(module_name: str, path: Path) -> types.ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load pinned Rolling-Unet file: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_upstream_module() -> types.ModuleType:
    for path, expected_hash in (
        (UPSTREAM_SOURCE, UPSTREAM_SOURCE_SHA256),
        (UPSTREAM_UTILS, UPSTREAM_UTILS_SHA256),
    ):
        if not path.is_file():
            raise FileNotFoundError(f"Pinned Rolling-Unet source not found: {path}")
        observed_hash = _sha256(path)
        if observed_hash != expected_hash:
            raise RuntimeError(
                f"Rolling-Unet source identity mismatch for {path.name}: "
                f"expected {expected_hash}, observed {observed_hash}"
            )

    # archs.py uses ``from utils import *``. Preload exactly the adjacent pinned
    # utils.py under that name, then restore the caller's import state. This
    # avoids any persistent sys.path mutation or collision with another utils.
    previous_utils = sys.modules.get("utils")
    pinned_utils = _load_file("_pinned_rolling_utils", UPSTREAM_UTILS)
    sys.modules["utils"] = pinned_utils
    try:
        return _load_file("_pinned_rolling_unet_upstream", UPSTREAM_SOURCE)
    except ImportError as error:
        if error.name and error.name.startswith("timm"):
            raise RuntimeError(
                "Rolling-Unet-S requires the upstream timm dependency."
            ) from error
        raise
    finally:
        if previous_utils is None:
            sys.modules.pop("utils", None)
        else:
            sys.modules["utils"] = previous_utils


class BraTSRollingUNetS(nn.Module):
    """Thin invariant-checking wrapper around exact Rolling-Unet-S."""

    def __init__(self) -> None:
        super().__init__()
        upstream = _load_upstream_module()
        self.upstream = upstream.Rolling_Unet_S(
            num_classes=BRATS_NUM_CLASSES,
            input_channels=BRATS_IN_CHANNELS,
            deep_supervision=False,
            img_size=BRATS_IMAGE_SIZE,
            embed_dims=list(EMBED_DIMS),
            num_heads=list(NUM_HEADS),
            qkv_bias=False,
            qk_scale=None,
            drop_rate=0.0,
            attn_drop_rate=0.0,
            drop_path_rate=0.0,
            depths=list(DEPTHS),
            sr_ratios=list(SR_RATIOS),
        )

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        if inputs.ndim != 4 or tuple(inputs.shape[1:]) != (
            BRATS_IN_CHANNELS,
            BRATS_IMAGE_SIZE,
            BRATS_IMAGE_SIZE,
        ):
            raise ValueError(
                "Rolling-Unet-S requires [batch, 4, 256, 256], got "
                f"{tuple(inputs.shape)}"
            )
        logits = self.upstream(inputs)
        if not torch.is_tensor(logits):
            raise TypeError(
                "Pinned Rolling-Unet-S returned an unexpected deep-supervision "
                "or container output."
            )
        expected_shape = (
            inputs.shape[0],
            BRATS_NUM_CLASSES,
            BRATS_IMAGE_SIZE,
            BRATS_IMAGE_SIZE,
        )
        if tuple(logits.shape) != expected_shape:
            raise RuntimeError(
                f"Rolling-Unet-S logits shape {tuple(logits.shape)} != "
                f"{expected_shape}"
            )
        return logits


def create_brats_rolling_unet_s() -> BraTSRollingUNetS:
    """Construct Rolling-Unet-S from scratch at the frozen configuration."""

    return BraTSRollingUNetS()
