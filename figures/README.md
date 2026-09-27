# Research figures

| File | Description |
|---|---|
| [tricontextnet_architecture.jpg](tricontextnet_architecture.jpg) | Canonical architecture: three adjacent four-modality slices, pooled encoder skips and centre-slice output. |
| [02_accuracy_efficiency.png](02_accuracy_efficiency.png) | Frozen aggregate comparison of 11 models; GFLOPs measure architecture-level work, not hardware latency. |
| [03_context_ablation.png](03_context_ablation.png) | Frozen validation-only single-slice, repeated-centre and neighbouring-slice comparison; no statistical significance claim. |

The architecture JPEG is 4375×3666 pixels and 1,730,518 bytes. SHA256: `7B81290CEB02B006D07D74DBEF79B02C4D2B04200BA2E86EF4E13DC31780FF3A`.

Architecture skips carry t1=16×128×128 to AG4, t2=32×64×64 to AG3, t3=64×32×32 to AG2 and t4=96×16×16 to AG1. Encoder 5's label includes its final pooling step; the separately drawn bottleneck denotes that same 160×8×8 tensor. Decoder dimensions are after upsampling.

Attention insets are simplified schematics. Channel attention combines global average/max pooling through shared transformations before sigmoid weighting. Spatial attention uses channel-wise average/max aggregation before a 7×7 convolution. Each gate is conditioned on the corresponding upsampled decoder feature. The four-class logits are argmax-decoded before unpadding to a 240×240 centre-slice segmentation. MRI thumbnails are illustrative, with no subject identity mapping.

The aggregate figures are unchanged frozen artifacts. No scientific figure was regenerated.
