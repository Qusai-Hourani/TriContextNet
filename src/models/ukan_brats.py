from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SEG_UKAN_DIR = PROJECT_ROOT / "external" / "U-KAN" / "Seg_UKAN"

if not SEG_UKAN_DIR.is_dir():
    raise FileNotFoundError(
        f"Expected pinned U-KAN source at: {SEG_UKAN_DIR}"
    )

seg_ukan_str = str(SEG_UKAN_DIR)
if seg_ukan_str not in sys.path:
    sys.path.insert(0, seg_ukan_str)

from archs import ConvLayer, UKAN  # noqa: E402


UKAN_UPSTREAM_COMMIT = "b20bf63490f01ba45cc2c18834bc0c4975c12715"

BRATS_INPUT_CHANNELS = 4
BRATS_NUM_CLASSES = 4
BRATS_IMAGE_SIZE = 256

# Authors' released segmentation-training configuration.
UKAN_EMBED_DIMS = [128, 160, 256]


class BraTSUKAN(UKAN):
    """
    Project-owned BraTS interface for the pinned official 2D Seg_UKAN model.

    The upstream architecture is retained except for the strictly necessary
    first-layer input adaptation from the hard-coded 3 channels to the
    project's 4 MRI channels.
    """

    def __init__(self):
        super().__init__(
            num_classes=BRATS_NUM_CLASSES,
            input_channels=BRATS_INPUT_CHANNELS,
            deep_supervision=False,
            img_size=BRATS_IMAGE_SIZE,
            embed_dims=UKAN_EMBED_DIMS,
            no_kan=False,
        )

        # Upstream UKAN currently hard-codes:
        # self.encoder1 = ConvLayer(3, kan_input_dim // 8)
        #
        # Replace only that input stem so it accepts the canonical
        # T1/T1ce/T2/FLAIR four-channel BraTS input.
        self.encoder1 = ConvLayer(
            BRATS_INPUT_CHANNELS,
            UKAN_EMBED_DIMS[0] // 8,
        )


def create_brats_ukan():
    return BraTSUKAN()