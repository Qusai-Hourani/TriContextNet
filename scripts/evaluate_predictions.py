"""Evaluate explicitly supplied predictions; never discovers project subjects or splits."""
import argparse
import csv
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairs", type=Path, required=True, help="Private CSV with prediction,target paths; paths resolve relative to the CSV.")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Output exists; choose a new filename.")
    import nibabel as nib
    import numpy as np
    from src.evaluation.metrics import subject_metrics
    def volume(image):
        raw = np.asanyarray(image.dataobj)
        if not np.isin(raw, [0, 1, 2, 4]).all():
            raise ValueError("Expected raw labels 0, 1, 2, 4.")
        out = raw.astype(np.uint8, copy=True)
        out[out == 4] = 3
        return out
    with args.pairs.open(newline="") as stream:
        pairs = list(csv.DictReader(stream))
    if not pairs:
        raise ValueError("Empty pair manifest.")
    results = []
    seen = set()
    for pair in pairs:
        prediction = (args.pairs.parent / pair["prediction"]).resolve()
        target = (args.pairs.parent / pair["target"]).resolve()
        if prediction in seen or target in seen:
            raise ValueError("Duplicate prediction or target path.")
        seen.update([prediction, target])
        pred_image, target_image = nib.load(prediction), nib.load(target)
        if not np.allclose(pred_image.affine, target_image.affine):
            raise ValueError("Prediction and target voxel grids differ.")
        if any(not np.allclose(x.header.get_zooms()[:3], (1, 1, 1)) for x in (pred_image, target_image)):
            raise ValueError("Frozen metric convention requires 1 mm isotropic spacing.")
        results.append(subject_metrics(volume(pred_image), volume(target_image)))
    metrics = [k for k in results[0] if k.endswith(("_dice", "_hd95_mm"))]
    summary = {k: {"mean": float(np.mean([r[k] for r in results])), "std_population": float(np.std([r[k] for r in results], ddof=0)), "median": float(np.median([r[k] for r in results]))} for k in metrics}
    summary["overall_mean_dice"] = float(np.mean([summary[r + "_dice"]["mean"] for r in ("wt", "tc", "et")]))
    summary["subject_count"] = len(results)
    summary["scope"] = "User-supplied evaluation; not a rerun or replacement of the frozen paper results."
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        json.dump(summary, stream, indent=2)
    print("Evaluation complete; aggregate results written without subject identities.")


if __name__ == "__main__":
    main()
