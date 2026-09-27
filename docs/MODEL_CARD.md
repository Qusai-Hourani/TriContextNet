# TriContextNet model card

**Task:** centre-slice four-class brain-tumour segmentation from three neighbouring axial slices with four MRI modalities each.

**Architecture:** MK-UNet-derived backbone with 12 input channels and widths 16/32/64/96/160; 317,438 parameters and 0.413568384 MAC-style GFLOPs per prediction. No separate cross-slice fusion block or auxiliary deep-supervision loss is introduced. The upstream implementation computes intermediate heads but returns only the final output.

**Training data and selection:** 369 labelled BraTS 2020 training cases partitioned into 295/37/37 train/validation/held-out subjects. Split identities are not distributed. The highest overall validation Dice selected epoch 37, with exact ties retaining the earlier checkpoint. Held-out observations did not select the checkpoint.

**Intended use:** research into multimodal MRI segmentation and reproducible model inspection. Clinical diagnosis, treatment planning and clinical deployment are outside the validated scope.

**Input/output:** [PREPROCESSING.md](PREPROCESSING.md). **Checkpoint and configuration:** [MODEL_MANIFEST.json](../checkpoints/MODEL_MANIFEST.json), [tricontextnet.json](../configs/tricontextnet.json). **Source and attribution:** [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).

**Evidence:** frozen aggregate comparison and controlled validation-only context ablation. The observed held-out difference from MK-UNet is small and does not establish statistical superiority. TriContextNet validation HD95 is unavailable.

**Limitations:** single-dataset evidence; no external dataset validation, prospective study, calibration assessment, demographic subgroup evaluation or clinical safety validation. Exact replication depends on data, split, runtime and hardware. Portable inference/evaluation entrypoints have static validation only; they were not exercised on scientific data during release preparation.
