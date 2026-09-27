"""Validated BraTS interface for the pinned, unmodified MSMamba source."""

from __future__ import annotations

import importlib
import inspect
import subprocess
import sys
from pathlib import Path
from typing import Any


UPSTREAM_REPOSITORY = "https://github.com/30Liu/MSMamba"
UPSTREAM_COMMIT = "295f6a318dd18fd19c66b16c179f28c1e9ac2033"

BRATS_IN_CHANNELS = 4
BRATS_OUT_CHANNELS = 4
FEATURE_SIZES = (48, 96, 192, 384, 768)
HIDDEN_SIZE = 768
SPATIAL_DIMS = 2
DEEP_SUPERVISION = False
EXPECTED_PARAMETER_COUNT = 59_890_624

PROJECT_ROOT = Path(__file__).resolve().parents[2]
UPSTREAM_ROOT = PROJECT_ROOT / "external" / "MSMamba"
UPSTREAM_PACKAGE_ROOT = UPSTREAM_ROOT / "msmamba"
UPSTREAM_MODEL_FILE = (
    UPSTREAM_PACKAGE_ROOT / "nnunetv2" / "nets" / "MSMamba.py"
)


class MSMambaConfigurationError(RuntimeError):
    """Raised when the vendored source or instantiated architecture has drifted."""


def _run_upstream_git(*arguments: str) -> str:
    """Run a read-only Git query without changing global safe-directory config."""
    command = [
        "git",
        "-c",
        f"safe.directory={UPSTREAM_ROOT.resolve()}",
        "-C",
        str(UPSTREAM_ROOT),
        *arguments,
    ]
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        details = getattr(error, "stderr", "") or str(error)
        raise MSMambaConfigurationError(
            "Could not verify the external/MSMamba checkout with Git. "
            f"Details: {details.strip()}"
        ) from error
    return result.stdout.strip()


def validate_upstream_checkout() -> str:
    """Require the pinned commit and no substantive tracked modifications."""
    if not UPSTREAM_MODEL_FILE.is_file():
        raise FileNotFoundError(
            f"Pinned MSMamba source not found at {UPSTREAM_MODEL_FILE}. "
            "Initialize the external/MSMamba Git submodule first."
        )

    checked_out_commit = _run_upstream_git("rev-parse", "HEAD").lower()
    if checked_out_commit != UPSTREAM_COMMIT:
        raise MSMambaConfigurationError(
            "external/MSMamba is not at the pinned commit: "
            f"expected {UPSTREAM_COMMIT}, found {checked_out_commit}."
        )

    # A submodule checked out on NTFS can appear wholly modified from WSL only
    # because Git compares CRLF worktree files with LF blobs. Ignore CR at EOL,
    # but reject every substantive tracked difference.
    for staged_arguments in ([], ["--cached"]):
        diff_command = [
            "git",
            "-c",
            f"safe.directory={UPSTREAM_ROOT.resolve()}",
            "-C",
            str(UPSTREAM_ROOT),
            "diff",
            *staged_arguments,
            "--quiet",
            "--ignore-cr-at-eol",
            "--no-ext-diff",
            "--",
        ]
        try:
            diff_result = subprocess.run(
                diff_command,
                check=False,
                capture_output=True,
                text=True,
            )
        except OSError as error:
            raise MSMambaConfigurationError(
                f"Could not audit tracked MSMamba changes: {error}"
            ) from error
        if diff_result.returncode == 1:
            location = "index" if staged_arguments else "worktree"
            raise MSMambaConfigurationError(
                f"external/MSMamba contains substantive tracked {location} "
                "modifications. The benchmark requires the unmodified pinned "
                "upstream architecture."
            )
        if diff_result.returncode != 0:
            raise MSMambaConfigurationError(
                "Git could not audit the MSMamba checkout. Details: "
                f"{diff_result.stderr.strip()}"
            )
    return checked_out_commit


def architecture_configuration() -> dict[str, Any]:
    """Return the exact immutable constructor configuration."""
    return {
        "in_chans": BRATS_IN_CHANNELS,
        "out_chans": BRATS_OUT_CHANNELS,
        "feat_size": list(FEATURE_SIZES),
        "hidden_size": HIDDEN_SIZE,
        "spatial_dims": SPATIAL_DIMS,
        "deep_supervision": DEEP_SUPERVISION,
    }


def _load_upstream_class():
    validate_upstream_checkout()
    package_text = str(UPSTREAM_PACKAGE_ROOT)
    if package_text not in sys.path:
        sys.path.insert(0, package_text)

    module = importlib.import_module("nnunetv2.nets.MSMamba")
    msmamba_class = getattr(module, "MSMamba", None)
    if msmamba_class is None:
        raise ImportError("Pinned upstream module does not expose MSMamba.")

    loaded_source = Path(inspect.getfile(msmamba_class)).resolve()
    if loaded_source != UPSTREAM_MODEL_FILE.resolve():
        raise MSMambaConfigurationError(
            "Imported MSMamba from an unexpected location: "
            f"expected {UPSTREAM_MODEL_FILE.resolve()}, found {loaded_source}."
        )
    return msmamba_class


def validate_model_configuration(model: Any) -> None:
    """Validate constructor-visible attributes and the known parameter invariant."""
    observed = {
        "in_chans": getattr(model, "in_chans", None),
        "out_chans": getattr(model, "out_chans", None),
        "feat_size": list(getattr(model, "feat_size", [])),
        "hidden_size": getattr(model, "hidden_size", None),
        "spatial_dims": getattr(model, "spatial_dims", None),
        "deep_supervision": getattr(model, "deep_supervision", None),
    }
    expected = architecture_configuration()
    if observed != expected:
        raise MSMambaConfigurationError(
            "Instantiated MSMamba does not match the pinned configuration: "
            f"expected {expected}, found {observed}."
        )

    total_parameters = sum(parameter.numel() for parameter in model.parameters())
    trainable_parameters = sum(
        parameter.numel() for parameter in model.parameters() if parameter.requires_grad
    )
    if (
        total_parameters != EXPECTED_PARAMETER_COUNT
        or trainable_parameters != EXPECTED_PARAMETER_COUNT
    ):
        raise MSMambaConfigurationError(
            "MSMamba parameter invariant failed: expected "
            f"{EXPECTED_PARAMETER_COUNT:,} total/trainable, found "
            f"{total_parameters:,}/{trainable_parameters:,}."
        )


def create_brats_msmamba():
    """Instantiate the exact frozen MSMamba architecture."""
    msmamba_class = _load_upstream_class()
    model = msmamba_class(**architecture_configuration())
    validate_model_configuration(model)
    return model
