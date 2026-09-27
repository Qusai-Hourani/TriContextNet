# Runtime evidence and installation scope

The original TriContextNet checkpoint's static pickle opcode metadata records:

| Component | Historical value |
|---|---|
| Python | 3.12.13 |
| PyTorch | 2.10.0+cu128 |
| TorchVision | 0.25.0+cu128 |
| NumPy | 2.0.2 |
| NiBabel | 5.4.2 |
| CUDA runtime | 12.8 |
| GPU | Tesla T4, capability 7.5 |
| Precision | FP32 parameters, forward and backward; no autocast/GradScaler |
| Physical/effective batch | 16/16 |

The frozen held-out evaluator specifies SciPy 1.17.1. Project source documentation specifies timm 0.6.13 for the unchanged MK-UNet helper imports; timm's version is not stored in the selected checkpoint's runtime block. This distinction is retained rather than inventing a fully pinned historical environment lock.

`requirements.txt` targets these versions. Choose the appropriate official PyTorch wheel index for CPU or CUDA 12.8. Model execution was not attempted during release validation, so runtime compatibility of the new portable commands remains unverified. Historical environment records for different benchmarks are not interchangeable with the T4 environment. MSMamba additionally requires its pinned upstream stack, MONAI and compiled Mamba/selective-scan dependencies; consult that upstream revision. U-KAN requires its external segmentation dependency tree.

The exact checkpoint contains the historical TorchVersion metadata type. The loading helper hash-checks the file and uses `weights_only=True` with only that type additionally allowlisted. There is no unrestricted loading fallback. If your PyTorch version rejects other metadata types, stop and review compatibility rather than disabling safe loading.
