"""Portable implementation of the frozen preprocessing for user-supplied volumes.

No project dataset paths, subject identities, or split discovery are embedded.
"""
from __future__ import annotations
from pathlib import Path

VOLUME_SHAPE = (240, 240, 155)
MODALITIES = ("t1", "t1ce", "t2", "flair")


def inspect_headers(paths):
    import nibabel as nib
    import numpy as np
    images = [nib.load(str(p), mmap="r") for p in paths]
    if len(images) != 4:
        raise ValueError("Supply T1, T1ce, T2, FLAIR in that order.")
    for image in images:
        if tuple(image.shape) != VOLUME_SHAPE:
            raise ValueError("Requires preprocessed BraTS 2020 volumes of shape 240 x 240 x 155.")
        if not np.allclose(image.header.get_zooms()[:3], (1, 1, 1)):
            raise ValueError("Requires 1 mm isotropic BraTS data; no resampling is performed.")
        if not np.allclose(image.affine, images[0].affine):
            raise ValueError("The four modalities must share the same voxel grid.")
    return images


def normalized_modalities(paths):
    import numpy as np
    images = inspect_headers(paths)
    normalized = []
    for image in images:
        volume = np.asanyarray(image.dataobj).astype(np.float32, copy=True)
        if not np.isfinite(volume).all():
            raise ValueError("Non-finite MRI intensities.")
        mask = volume != 0
        values = volume[mask]
        if not values.size:
            raise ValueError("Empty modality.")
        mean = float(np.mean(values, dtype=np.float64))
        std = float(np.std(values, dtype=np.float64, ddof=0))
        if not np.isfinite(std) or std <= 0:
            raise ValueError("Invalid nonzero population standard deviation.")
        output = np.zeros(VOLUME_SHAPE, dtype=np.float32)
        output[mask] = ((values.astype(np.float64) - mean) / std).astype(np.float32)
        normalized.append(output)
    return normalized, images[0]


def context_batch(volumes, centers):
    import numpy as np
    batches = []
    for center in centers:
        if not 0 <= center < 155:
            raise ValueError("Center slice must be in 0..154.")
        slices = (max(center - 1, 0), center, min(center + 1, 154))
        channels = np.stack([volume[:, :, z] for z in slices for volume in volumes])
        batches.append(np.pad(channels, ((0, 0), (8, 8), (8, 8)), mode="constant"))
    return np.stack(batches).astype(np.float32, copy=False)
