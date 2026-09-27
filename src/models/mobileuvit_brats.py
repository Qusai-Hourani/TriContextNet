"""BraTS 2020 interface for the pinned Mobile U-ViT architecture.

The upstream architecture remains unchanged under:
    external/Mobile-U-ViT

The constructor below specifies the frozen base benchmark configuration.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import torch.nn as nn


PROJECT_ROOT = Path(__file__).resolve().parents[2]
UPSTREAM_MODEL_FILE = (
    PROJECT_ROOT
    / "external"
    / "Mobile-U-ViT"
    / "network"
    / "MobileUViT.py"
)

EXPECTED_UPSTREAM_MODEL_FILE = UPSTREAM_MODEL_FILE.resolve()


def _load_upstream_module():
    if not UPSTREAM_MODEL_FILE.is_file():
        raise FileNotFoundError(
            f"Pinned Mobile U-ViT source not found: {UPSTREAM_MODEL_FILE}"
        )

    spec = importlib.util.spec_from_file_location(
        "_mobileuvit_pinned_upstream",
        UPSTREAM_MODEL_FILE,
    )

    if spec is None or spec.loader is None:
        raise ImportError(
            f"Could not create import specification for {UPSTREAM_MODEL_FILE}"
        )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def create_brats_mobileuvit() -> nn.Module:
    """Create the frozen base 2D Mobile U-ViT.

    Only the BraTS input/output interfaces differ from the upstream
    default:
        inch: 3 -> 4
        out_channel: 1 -> 4
    """

    upstream = _load_upstream_module()

    model = upstream.mobileuvit(
        inch=4,
        dims=[16, 32, 64, 128],
        depths=[1, 1, 3, 3, 3],
        kernels=[3, 3, 7],
        embed_dim=256,
        out_channel=4,
    )

    return model
