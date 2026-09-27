# Third-party notices

The following pinned upstream files are redistributed under their original terms. Bundled sources and license texts are unchanged. This repository makes no new project-wide license grant; public availability does not replace the rights and conditions stated in these upstream licenses.

| Model | Upstream revision | License | What is included |
|---|---|---|---|
| MK-UNet | [2fa8b230a057602539af7655203ad434bf56a5b6](https://github.com/SLDGroup/MK-UNet/tree/2fa8b230a057602539af7655203ad434bf56a5b6) | BSD-3-Clause | Exact minimal upstream model source + original license; project adapter/config |
| Rolling-Unet | [8a43d40c218917e454c0584a853757e3a2cf9c80](https://github.com/Jiaoyang45/Rolling-Unet/tree/8a43d40c218917e454c0584a853757e3a2cf9c80) | MIT | Exact minimal upstream model source + original license; project adapter/config |
| CMUNeXt | [affbf03ef631bb318d87b73ef97b2eacd0a5de85](https://github.com/FengheTan9/CMUNeXt/tree/affbf03ef631bb318d87b73ef97b2eacd0a5de85) | MIT | Exact minimal upstream model source + original license; project adapter/config |
| TinyU-Net | [73147721edf36dcb0101f1ec383cb97fe42e36df](https://github.com/ChenJunren-Lab/TinyU-Net/tree/73147721edf36dcb0101f1ec383cb97fe42e36df) | MIT | Exact minimal upstream model source + original license; project adapter/config |
| Mobile-U-ViT | [ce35b0864f51c66c20ee5315050ba445351c8891](https://github.com/FengheTan9/Mobile-U-ViT/tree/ce35b0864f51c66c20ee5315050ba445351c8891) | Apache-2.0 | Exact minimal upstream model source + original license; project adapter/config |
| U-KAN | [b20bf63490f01ba45cc2c18834bc0c4975c12715](https://github.com/CUHK-AIM-Group/U-KAN/tree/b20bf63490f01ba45cc2c18834bc0c4975c12715) | MIT (Seg_UKAN subtree) | Project adapter/config only; upstream source referenced externally |
| MSMamba | [295f6a318dd18fd19c66b16c179f28c1e9ac2033](https://github.com/30Liu/MSMamba/tree/295f6a318dd18fd19c66b16c179f28c1e9ac2033) | Apache-2.0 (msmamba subtree) | Project adapter/config only; upstream source referenced externally |

## Bundle boundaries
- MK-UNet: BSD-3-Clause, System Level Design Group (2025). Its exact `mkunet_network.py` supplies the backbone for both standalone MK-UNet and TriContextNet. TriContextNet changes the input interface to twelve channels and retains the published widths and output behavior. No claim of an independently invented backbone is made.
- Rolling-Unet: MIT, Jiaoyang45 (2024); exact `archs.py` and `utils.py` are bundled with LICENSE.
- CMUNeXt: MIT, Fenghe Tang (2023); exact base model source and LICENSE are bundled.
- TinyU-Net: MIT, Chen Junren (2024); exact model source and LICENSE are bundled. The project wrapper temporarily shims optional report-only imports and does not alter the forward graph.
- Mobile U-ViT: Apache-2.0; exact model file and original LICENSE are bundled. No NOTICE file was present at the pinned checkout root; the source remains unmodified.
- U-KAN: the `Seg_UKAN` subtree has an MIT license, but the bundled KAN implementation has an additional upstream lineage whose complete attribution chain was not established for redistribution. Its external source is not recopied. Obtain the exact pinned official repository and retain its license and dependency notices. The project input adapter/config is included.
- MSMamba: Apache-2.0 license is present in the `msmamba` subtree; the upstream package combines nnU-Net/Mamba and compiled dependencies with separate provenance. The complete transitive redistribution audit is unresolved, so only the project adapter/config and pinned acquisition instructions are included. No upstream model source is recopied.
- Standard 2D U-Net: project-owned implementation, without bundled third-party source.
- Attention U-Net: project-owned implementation, citing the MIT architectural reference [Attention-Gated-Networks](https://github.com/ozan-oktay/Attention-Gated-Networks/tree/eee4881fdc31920efd873773e0b744df8dacbfb6). No upstream implementation is bundled. The base U-Net layers are project-owned.
- DeepLabV3+: project-owned decoder with TorchVision ResNet-50 V1.5 as a package dependency. Source identifies TorchVision revision `8fb87713a24951e639c494b0f2a8a81b5f8e33a6` and the DeepLab architectural reference revision `bdcfdd30306a7df694fb281cd24884769009d03e`. TorchVision is not vendored; it is distributed under its own BSD-3-Clause license. No pretrained third-party weights are bundled.


## Project-trained checkpoints

TriContextNet, Rolling-Unet-S, base CMUNeXt and TinyU-Net weights were trained by this project and are hosted with the repository owner's authorization. They are not upstream pretrained weight downloads. Their architecture sources permit source/binary redistribution under BSD-3-Clause (MK-UNet) or MIT (the three benchmark architectures), with the required notices retained here and under `external/`. No separate general reuse license for project-owned code or project-trained weights is asserted.

Names, exact byte sizes, SHA256 values and associated configs are recorded in [MODEL_MANIFEST.json](checkpoints/MODEL_MANIFEST.json). Seven other original checkpoints are not distributed because their serialized metadata contains personal paths. Source licensing does not imply that those private metadata fields may be published. No replacement or rewritten checkpoint is represented as a frozen original.

## External acquisition

U-KAN and MSMamba source is not bundled because its complete transitive attribution chain has not been verified. Obtain their exact revisions separately and retain all upstream and dependency notices:

```bash
git clone https://github.com/CUHK-AIM-Group/U-KAN.git external/U-KAN
git -C external/U-KAN checkout b20bf63490f01ba45cc2c18834bc0c4975c12715
git clone https://github.com/30Liu/MSMamba.git external/MSMamba
git -C external/MSMamba checkout 295f6a318dd18fd19c66b16c179f28c1e9ac2033
```

The project adapters/configs preserve constructor settings. For a new independently conducted training experiment, use the pinned upstream training documentation together with the input/output adapters, the [preprocessing specification](docs/PREPROCESSING.md) and [training methodology](docs/REPRODUCIBILITY.md). New weights will not match the original checkpoint hash. The withheld original files have no public download in this release.

## Package dependencies and data

PyTorch, TorchVision, timm, NumPy, SciPy and NiBabel are installed dependencies, not bundled source distributions; their own package notices apply. The public upstream sources above may use these libraries. No pretrained third-party weight download is enabled by the project adapters.

BraTS data are not bundled. The [official data terms and required citations](https://www.med.upenn.edu/cbica/brats2020/data.html) remain applicable. Follow them for dataset acquisition and research use; no MRI redistribution rights are granted here. Dataset references are listed in [PREPROCESSING.md](docs/PREPROCESSING.md#dataset-citations).
