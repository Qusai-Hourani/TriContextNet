"""Minimal BraTS interface for the pinned official MK-UNet implementation."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

UPSTREAM_REPOSITORY = "https://github.com/SLDGroup/MK-UNet"
UPSTREAM_COMMIT = "2fa8b230a057602539af7655203ad434bf56a5b6"

BRATS_IN_CHANNELS = 4
BRATS_NUM_CLASSES = 4
PUBLISHED_CHANNELS = (16, 32, 64, 96, 160)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
UPSTREAM_NETWORK_FILE = PROJECT_ROOT / "external" / "MK-UNet" / "mkunet_network.py"


def _load_upstream_module() -> ModuleType:
    if not UPSTREAM_NETWORK_FILE.is_file():
        raise FileNotFoundError(
            f"Official MK-UNet source not found at {UPSTREAM_NETWORK_FILE}. "
            "Initialize the external/MK-UNet Git submodule first."
        )

    spec = importlib.util.spec_from_file_location(
        "mkunet_upstream_network", UPSTREAM_NETWORK_FILE
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load MK-UNet from {UPSTREAM_NETWORK_FILE}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def create_brats_mkunet():
    """Instantiate published MK-UNet with only its BraTS I/O interface configured."""

    upstream = _load_upstream_module()
    return upstream.MK_UNet(
        in_channels=BRATS_IN_CHANNELS,
        num_classes=BRATS_NUM_CLASSES,
        channels=list(PUBLISHED_CHANNELS),
    )
