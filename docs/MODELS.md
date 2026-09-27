# Model and checkpoint catalog

All configs specify the exact factory and the pinned source version. Model wrappers retain the frozen constructor constants. All outputs represent four-class center-slice logits; TriContextNet inputs have 12 channels and benchmark inputs have 4. See [preprocessing](PREPROCESSING.md) for normalization, padding and class mapping.

| Model | Bytes | Included | SHA256 |
|---|---:|---|---|
| MK-UNet | 4213954 | No — private metadata | `28029CA9D2D16662C112C244B29D7018F6EB2DCFD820337BD0D7449D0FD0A46E` |
| MSMamba | 719030886 | No — private metadata | `5C2CD2F0173AC5DC5F4E3609651ECFB4F6EDD5A29501446937BE3D8F3A069EA6` |
| standard 2D U-Net | 124151641 | No — private metadata | `5E1CAB138642745EB4A87E1B34518640866854FAD1E29F715C6111C3055E5BCC` |
| Mobile U-ViT | 5727671 | No — private metadata | `EC8E23FC11524C402E1A28215DBA7A50E484C87B32ADB532E63E12619DE13CA1` |
| U-KAN | 25655395 | No — private metadata | `4D4F53922DDCC7968EC99B6618D8170ECF8355F9040B60607EAFC323161F2B88` |
| Attention U-Net | 139443363 | No — private metadata | `53A31B93C805AC9B068A46F9D2D68045759BE16F593A6A0F1AEF8C4EF16DC4DC` |
| DeepLabV3+ | 107210007 | No — private metadata | `486AAC7CAA6532468FE89D2A1ACA643DB653216D57EF57352CED50E71CB3AF0A` |
| TriContextNet | 1475367 | Yes | `725928D75D3B852D5096564E3B1DE63EB8E52912C8284B8D680490022CEEFF2A` |
| TinyU-Net | 2123995 | Yes | `6152856DEF5F8A793F1B11A56B9E3E6EF37138F09FCA253E7C8D72FC0CADD380` |
| Rolling-Unet-S | 7234379 | Yes | `FF7B6B46A09EFB4489736D141F0868FC2D8E87EC0CB4DD315F99294721D8CC5E` |
| base CMUNeXt | 12789425 | Yes | `936CA8FF790F3F2118B18D14F302757C761114BE8F76A1BCE6D4D9A6AE4DC04C` |

## TriContextNet
Source: `src/models/tricontextnet.py`, exact research adapter `mkunet_2p5d_brats.py`, and bundled MK-UNet source. Config: `configs/tricontextnet.json`. Checkpoint: `checkpoints/tricontextnet/best_model.pth`. The README provides complete loading and CLI inference examples. Hash and architecture checks run before loading; the exact checkpoint records selected epoch 37.

## Included benchmark loading and inference
Use this example with your own appropriately acquired data. Use a correctly normalized and padded `[B,4,256,256]` FP32 center-slice tensor `x`. There is no neighboring-slice input for these benchmarks. The model itself returns logits `[B,4,256,256]`.
```python
import hashlib, importlib, json, sys
from pathlib import Path
import torch
from torch.torch_version import TorchVersion

root = Path.cwd()  # run at the repository root
sys.path.insert(0, str(root / "src/models"))
name = "rolling_unet_s"  # or "base_cmunext", "tiny_unet"
cfg = json.loads((root / f"configs/{name}.json").read_text())
path = root / f"checkpoints/benchmarks/{name}/best_model.pth"
with path.open("rb") as stream:
    assert hashlib.file_digest(stream, "sha256").hexdigest().upper() == cfg["checkpoint_sha256"]
module, factory = cfg["factory"].split(":")
model = getattr(importlib.import_module(module), factory)()
with torch.serialization.safe_globals([TorchVersion]):
    checkpoint = torch.load(path, map_location="cpu", weights_only=True)
model.load_state_dict(checkpoint["model_state_dict"], strict=True)
model.eval().float()
# Once you supply x from your own authorized data:
# with torch.inference_mode():
#     labels = model(x).argmax(1)[:, 8:-8, 8:-8]
# labels[labels == 3] = 4
```
These are FP32 CPU inspection examples, not a numerical replication of every benchmark training/inference precision policy. The exact frozen policies and batch sizes appear in the configs/table. Obtain the corresponding original runtime for claims of numerical reproduction.

## Withheld checkpoints and externally referenced source
All remaining factories/configurations and original checkpoint SHA256 values are recorded in `checkpoints/MODEL_MANIFEST.json`; aggregate frozen evaluation values are in `tables/frozen_model_comparison.csv`. The manifest explains why each original weight file is withheld. U-KAN and MSMamba need the separately acquired pinned source as described in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).
