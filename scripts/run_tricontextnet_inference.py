"""Run the frozen model on four explicitly supplied, independently authorized MRIs."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, default=ROOT / "checkpoints/tricontextnet/best_model.pth")
    for modality in ("t1", "t1ce", "t2", "flair"):
        parser.add_argument("--" + modality, type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cpu", choices=("cpu", "cuda:0"))
    parser.add_argument("--batch-size", type=int, default=16)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Output already exists; choose a new output filename.")
    if args.batch_size < 1 or args.batch_size > 155:
        parser.error("Batch size must be in 1..155.")
    if not str(args.output).endswith((".nii", ".nii.gz")):
        parser.error("Output must end in .nii or .nii.gz.")
    import numpy as np
    import nibabel as nib
    import torch
    from src.models.tricontextnet import load_tricontextnet
    from src.data.preprocessing import normalized_modalities, context_batch
    torch.manual_seed(42)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    model = load_tricontextnet(args.checkpoint, args.device)
    volumes, reference = normalized_modalities([getattr(args, m) for m in ("t1", "t1ce", "t2", "flair")])
    prediction = np.zeros((240, 240, 155), dtype=np.uint8)
    with torch.inference_mode():
        for start in range(0, 155, args.batch_size):
            centers = list(range(start, min(start + args.batch_size, 155)))
            tensor = torch.from_numpy(context_batch(volumes, centers)).to(args.device)
            output = model(tensor)
            if not isinstance(output, (list, tuple)) or len(output) != 1:
                raise TypeError("Expected the frozen one-element output container.")
            logits = output[0]
            if tuple(logits.shape) != (len(centers), 4, 256, 256) or logits.dtype != torch.float32:
                raise ValueError("Unexpected model output shape or precision.")
            if not torch.isfinite(logits).all():
                raise ValueError("Non-finite logits.")
            labels = logits.argmax(dim=1)[:, 8:-8, 8:-8].cpu().numpy().astype(np.uint8)
            for i, center in enumerate(centers):
                prediction[:, :, center] = labels[i]
    prediction[prediction == 3] = 4
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # A fresh header avoids copying identifying free-text metadata into predictions.
    nib.save(nib.Nifti1Image(prediction, reference.affine), str(args.output))
    print("Inference complete; output labels are 0, 1, 2, 4.")


if __name__ == "__main__":
    main()
