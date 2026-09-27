# Reproducibility

## Artifact identity

The TriContextNet checkpoint is the exact selected epoch-37 file. Its SHA256 is `725928D75D3B852D5096564E3B1DE63EB8E52912C8284B8D680490022CEEFF2A`; no tensor or serialized metadata was rewritten. [configs/tricontextnet.json](../configs/tricontextnet.json) specifies the exact constructor, input ordering, precision and output conventions. The original checkpoint retains its historical configuration metadata, including generic hosted-runtime paths. These are not portable dataset locations.

The [file provenance manifest](../reproducibility/FILE_PROVENANCE.json) records source identities and released hashes. Bundled upstream sources are unchanged at their pinned revisions. Project model wrappers preserve their constructors and computation; comments, documentation and private import aliases were normalized for this release. Checkpoint compatibility fields retain the original serialization identifiers where needed by the loader. The complete release checksum roster is [SHA256SUMS.txt](../reproducibility/SHA256SUMS.txt).

## Training methodology

The reported training used seed 42, batch size 16, accumulation 1, FP32 without autocast or GradScaler, AdamW (learning rate 0.0005; weight decay 0.0001), and CosineAnnealingLR (T_max 200; eta_min 0.000001). The objective was equal-weight multiclass cross entropy plus foreground soft Dice over internal classes 1/2/3. Joint geometric augmentation is described in [PREPROCESSING.md](PREPROCESSING.md).

The trajectory continued from its epoch-40 boundary with a 200-epoch limit and early-stopping patience 30; training ended at epoch 67. Selection used overall subject-level validation Dice, with strictly higher values replacing the incumbent and ties retaining the earlier epoch. The selected checkpoint remained epoch 37. No held-out result was used for checkpoint selection. Historical restart logic does not establish bitwise persistent-worker augmentation RNG continuity.

Private split identities, cached normalization records and continuation state are not distributed. Consequently this release supports artifact inspection, inference and independently supplied evaluation data, but it does not provide one-command recreation of the original training trajectory. A new experiment with independently acquired data/splits should be reported as a reproduction attempt, not as the frozen original run.

## Evaluation semantics

Full 3D reconstruction uses all 155 centre slices after unpadding. WT/TC/ET Dice are computed per subject and averaged by region; overall mean Dice is the mean of the three regional cohort means. Both-empty region: Dice=1 and HD95=0. Exactly one empty region: Dice=0 and HD95=373.13 mm. HD95 uses connectivity-1 eroded surfaces, 1 mm spacing, concatenated directed surface distances and NumPy's 95th percentile. Population standard deviation uses ddof=0.

The metric function bodies in [src/evaluation/metrics.py](../src/evaluation/metrics.py) are preserved from the frozen evaluator; dataset discovery and split bindings are absent. [scripts/evaluate_predictions.py](../scripts/evaluate_predictions.py) is a portable interface for explicitly supplied label volumes. Its output does not replace the paper's frozen results. TriContextNet validation HD95 was not available and remains NA.

## Validation scope

Release checks cover byte hashes/sizes, inert checkpoint archive/metadata inspection, Python syntax and safe imports, configuration/factory references, documentation links, upstream source identity and privacy scanning. No checkpoint was deserialized, model constructed, scientific data accessed, inference executed, training performed or metric recomputed during release preparation. Runtime execution of the portable commands remains unverified on scientific data.
