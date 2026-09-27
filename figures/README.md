# TriContextNet publication figures

This directory contains the verified figure set associated with TriContextNet: **23 scientific concepts** grouped as follows. PNG and SVG versions are two formats of one concept.

| Category | Figure numbers | Concepts |
|---|---|---:|
| Core | 01–05 | 5 |
| Brain-image / qualitative | 06–15 | 10 |
| Benchmark / performance | 16–19 | 4 |
| Supplementary / optional | 20–23 | 4 |

[Full collection](publication_set/) · [Contact sheet](publication_set/00_all_figures_contact_sheet.png) · [Catalog and hashes](publication_set/figure_catalog.md) · [Captions](publication_set/figure_captions.md) · [Checksums](publication_set/SHA256SUMS.txt)

All scientific figures come from frozen project outputs. **No figure uses generative AI.** Qualitative cases are validation-only and selected using ground truth where applicable; predictions and scores did not drive selection. Held-out panels contain frozen aggregate results. Displays are descriptive, with no statistical-superiority claim; TriContextNet validation HD95 remains NA.

[Figure 01: corrected architecture](tricontextnet_architecture.jpg) is the implementation-faithful JPEG and the only architecture artwork supplied. It is 4375×3666 pixels, 1,730,518 bytes; SHA256 `7B81290CEB02B006D07D74DBEF79B02C4D2B04200BA2E86EF4E13DC31780FF3A`. Figures 02–23 each include PNG and SVG. The contact sheet is a thumbnail index of these existing figures, including the corrected JPEG.

Architecture skips carry t1=16×128×128 to AG4, t2=32×64×64 to AG3, t3=64×32×32 to AG2 and t4=96×16×16 to AG1. Encoder 5's label includes its final pooling step; the separately drawn bottleneck denotes that same 160×8×8 tensor. Decoder dimensions are after upsampling.

Attention insets are simplified schematics. Channel attention combines global average/max pooling through shared transformations before sigmoid weighting. Spatial attention uses channel-wise average/max aggregation before a 7×7 convolution. Each gate is conditioned on the corresponding upsampled decoder feature. The four-class logits are argmax-decoded before unpadding to a 240×240 centre-slice segmentation. MRI thumbnails are illustrative, with no subject identity mapping.

The non-architecture PNGs are unchanged frozen exports. Figure 05 SVG has only a non-rendered description cleanup; its drawing elements and embedded image bytes are unchanged. See the catalog for details. Checksum paths are relative to `publication_set/`, including `../tricontextnet_architecture.jpg` for Figure 01.
