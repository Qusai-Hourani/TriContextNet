# Data and preprocessing

Use legitimately acquired BraTS 2020 preprocessed MRI from the [official provider](https://www.med.upenn.edu/cbica/brats2020/data.html). The source data are co-registered, skull-stripped and resampled to 1 mm isotropic spacing. This repository neither downloads restricted data nor redistributes it. No clinical raw DICOM ingestion or registration pipeline is provided.

1. Require four aligned volumes of shape `[240,240,155]`, ordered T1, T1ce, T2, FLAIR. Retain array axes; do not reorient or resample.
2. Convert each complete volume to float32. Select its nonzero voxels. Calculate its own mean and population standard deviation (`ddof=0`) in float64. Normalize nonzero voxels with float64 subtraction/division and cast back to float32; preserve exact zero background. There is no cohort-fitted mean, clipping, percentile normalization or slice-wise normalization. Reject empty or constant nonzero volumes.
3. For center index z in 0..154, use `[max(z-1,0),z,min(z+1,154)]`. Thus the first and last neighbors repeat the boundary slice.
4. Stack channels in slice-major order: previous T1/T1ce/T2/FLAIR, center T1/T1ce/T2/FLAIR, next T1/T1ce/T2/FLAIR. Zero-pad 8 pixels on each spatial side to obtain `[B,12,256,256]`.
5. The raw network output is a one-element list containing `[B,4,256,256]` center-slice logits. Use FP32, eval mode, no autocast, no TTA, no threshold adjustment and no postprocessing. Take argmax across classes, remove the 8-pixel padding, and reconstruct every center slice in original order.
6. Internal labels 0/1/2/3 correspond to raw BraTS labels 0/1/2/4. Save raw label 4 for enhancing tumor. Internal evaluation regions are WT={1,2,3}, TC={1,3}, ET={3}.

The historical pipeline used precomputed full-volume per-subject statistics; the portable entrypoint computes the identical statistic definition from the explicitly supplied volumes. Historical statistics and identity files are private and are not copied here.

Training alone applied a horizontal flip with probability 0.5 and, independently with probability 0.5, a random rotation uniformly in [-10,10] degrees. The same geometry was applied jointly to all 12 channels and the center label map (bilinear image interpolation, nearest-neighbor label interpolation, zero fill). No augmentation is used in inference.

## Dataset citations

The [official BraTS 2020 data page](https://www.med.upenn.edu/cbica/brats2020/data.html) requests the following dataset references:

- Menze et al., The Multimodal Brain Tumor Image Segmentation Benchmark (BRATS), 2015. [DOI: 10.1109/TMI.2014.2377694](https://doi.org/10.1109/TMI.2014.2377694).
- Bakas et al., Advancing The Cancer Genome Atlas glioma MRI collections with expert segmentation labels and radiomic features, 2017. [DOI: 10.1038/sdata.2017.117](https://doi.org/10.1038/sdata.2017.117).
- Bakas et al., Identifying the Best Machine Learning Algorithms for Brain Tumor Segmentation, Progression Assessment, and Overall Survival Prediction in the BRATS Challenge, 2018. [arXiv:1811.02629](https://arxiv.org/abs/1811.02629).

Follow the provider's additional data-citation guidance and the terms accepted when obtaining the dataset. Repository access does not grant rights to redistribute MRI data.
