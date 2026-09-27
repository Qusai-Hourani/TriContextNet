"""Exact frozen metric functions extracted without dataset bindings."""
from __future__ import annotations
import math
from typing import Any, Sequence
VOXEL_SPACING_MM=(1.0,1.0,1.0)
ONE_EMPTY_HD95_MM=373.13
ORIGINAL_VOLUME_SHAPE=(240,240,155)

def load_metric_runtime():
    """Import only NumPy/SciPy; safe for the dataset-free self-test path."""
    try:
        import numpy as np
        from scipy import ndimage
    except ImportError as exc:
        raise RuntimeError(
            "NumPy and SciPy are required for metric evaluation. Run this script "
            "with the project .venv."
        ) from exc
    return np, ndimage

def _as_matching_boolean_arrays(
    prediction: Any, target: Any
) -> tuple[Any, Any]:
    np, _ = load_metric_runtime()
    prediction_bool = np.asarray(prediction, dtype=bool)
    target_bool = np.asarray(target, dtype=bool)
    if prediction_bool.shape != target_bool.shape:
        raise ValueError(
            f"Metric mask shapes differ: {prediction_bool.shape} vs "
            f"{target_bool.shape}."
        )
    if prediction_bool.ndim != 3:
        raise ValueError(
            f"Metrics require complete 3D masks, found {prediction_bool.ndim}D."
        )
    return prediction_bool, target_bool

def binary_dice(prediction: Any, target: Any) -> float:
    """Binary Dice with the finalized project empty-region convention."""
    np, _ = load_metric_runtime()
    prediction_bool, target_bool = _as_matching_boolean_arrays(prediction, target)
    prediction_count = int(np.count_nonzero(prediction_bool))
    target_count = int(np.count_nonzero(target_bool))
    if prediction_count == 0 and target_count == 0:
        return 1.0
    if prediction_count == 0 or target_count == 0:
        return 0.0
    intersection = int(np.count_nonzero(prediction_bool & target_bool))
    return (2.0 * intersection) / (prediction_count + target_count)

def binary_hd95(
    prediction: Any,
    target: Any,
    voxel_spacing: Sequence[float] = VOXEL_SPACING_MM,
) -> float:
    """MedPy/CBICA-compatible symmetric surface HD95 for complete 3D masks."""
    np, ndimage = load_metric_runtime()
    prediction_bool, target_bool = _as_matching_boolean_arrays(prediction, target)
    spacing = tuple(float(value) for value in voxel_spacing)
    if len(spacing) != prediction_bool.ndim:
        raise ValueError(
            f"Expected {prediction_bool.ndim} spacing values, found {len(spacing)}."
        )
    if any(not math.isfinite(value) or value <= 0 for value in spacing):
        raise ValueError(f"Voxel spacing must be finite and positive: {spacing}")

    prediction_empty = not bool(np.any(prediction_bool))
    target_empty = not bool(np.any(target_bool))
    if prediction_empty and target_empty:
        return 0.0
    if prediction_empty or target_empty:
        return ONE_EMPTY_HD95_MM

    connectivity_one = ndimage.generate_binary_structure(3, 1)
    prediction_surface = prediction_bool ^ ndimage.binary_erosion(
        prediction_bool,
        structure=connectivity_one,
        iterations=1,
    )
    target_surface = target_bool ^ ndimage.binary_erosion(
        target_bool,
        structure=connectivity_one,
        iterations=1,
    )

    distance_to_target_surface = ndimage.distance_transform_edt(
        ~target_surface,
        sampling=spacing,
    )
    distance_to_prediction_surface = ndimage.distance_transform_edt(
        ~prediction_surface,
        sampling=spacing,
    )
    prediction_to_target = distance_to_target_surface[prediction_surface]
    target_to_prediction = distance_to_prediction_surface[target_surface]
    symmetric_surface_distances = np.concatenate(
        (prediction_to_target, target_to_prediction)
    )
    if symmetric_surface_distances.size == 0:
        raise RuntimeError("Non-empty masks unexpectedly produced no surface voxels.")
    return float(np.percentile(symmetric_surface_distances, 95))

def brats_region_masks(multiclass_volume: Any) -> dict[str, Any]:
    np, _ = load_metric_runtime()
    volume = np.asarray(multiclass_volume)
    if volume.shape != ORIGINAL_VOLUME_SHAPE:
        raise ValueError(
            f"Expected reconstructed volume {ORIGINAL_VOLUME_SHAPE}, found "
            f"{volume.shape}."
        )
    observed = {int(value) for value in np.unique(volume)}
    if not observed.issubset({0, 1, 2, 3}):
        raise ValueError(f"Unexpected internal segmentation classes: {sorted(observed)}")
    return {
        "wt": volume != 0,
        "tc": (volume == 1) | (volume == 3),
        "et": volume == 3,
    }

def subject_metrics(prediction: Any, target: Any) -> dict[str, Any]:
    np, _ = load_metric_runtime()
    prediction_regions = brats_region_masks(prediction)
    target_regions = brats_region_masks(target)
    metrics: dict[str, Any] = {}
    for region in ("wt", "tc", "et"):
        predicted = prediction_regions[region]
        ground_truth = target_regions[region]
        metrics[f"{region}_dice"] = binary_dice(predicted, ground_truth)
        metrics[f"{region}_hd95_mm"] = binary_hd95(
            predicted, ground_truth, VOXEL_SPACING_MM
        )
        metrics[f"{region}_gt_empty"] = not bool(np.any(ground_truth))
        metrics[f"{region}_prediction_empty"] = not bool(np.any(predicted))
    return metrics
