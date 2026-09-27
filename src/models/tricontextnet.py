"""Publication API for the exact frozen tri-slice MK-UNet interface.

The underlying upstream network and the research adapters are byte-exact.
No model is constructed on import.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "configs/tricontextnet.json"
CHECKPOINT_SHA256 = "725928D75D3B852D5096564E3B1DE63EB8E52912C8284B8D680490022CEEFF2A"


def verify_checkpoint(checkpoint: str | Path) -> None:
    with Path(checkpoint).open("rb") as stream:
        observed = hashlib.file_digest(stream, "sha256").hexdigest().upper()
    if observed != CHECKPOINT_SHA256:
        raise ValueError("Checkpoint is not the frozen TriContextNet artifact.")


def create_tricontextnet(config_path: str | Path = CONFIG_PATH):
    config = json.loads(Path(config_path).read_text())
    expected = {"in_channels": 12, "num_classes": 4, "channels": [16, 32, 64, 96, 160]}
    if any(config.get(k) != v for k, v in expected.items()):
        raise ValueError("Configuration does not match the frozen architecture.")
    upstream = ROOT / "external/MK-UNet/mkunet_network.py"
    if hashlib.sha256(upstream.read_bytes()).hexdigest().upper() != config["upstream_source_sha256"]:
        raise ValueError("Pinned upstream source identity mismatch.")
    models_dir = str(Path(__file__).parent)
    if models_dir not in sys.path:
        sys.path.insert(0, models_dir)
    from mkunet_2p5d_brats import create_brats_mkunet_2p5d
    return create_brats_mkunet_2p5d()


def load_tricontextnet(checkpoint: str | Path, device: str = "cpu"):
    """Verify exact bytes, load safely on CPU, then move the FP32 model."""
    verify_checkpoint(checkpoint)
    import torch
    from torch.torch_version import TorchVersion
    # The frozen file records a TorchVersion value in its runtime metadata.
    # No unrestricted pickle fallback is allowed.
    with torch.serialization.safe_globals([TorchVersion]):
        payload = torch.load(checkpoint, map_location="cpu", weights_only=True)
    if payload.get("selected_epoch") != 37:
        raise ValueError("Unexpected selected epoch.")
    if payload.get("compatibility_signature", {}).get("finalist", {}).get("identity") != "A_simple_2p5d_mkunet":
        raise ValueError("Unexpected frozen model identity.")
    model = create_tricontextnet()
    model.load_state_dict(payload["model_state_dict"], strict=True)
    if sum(p.numel() for p in model.parameters()) != 317438:
        raise ValueError("Unexpected parameter count.")
    return model.float().to(device).eval()
