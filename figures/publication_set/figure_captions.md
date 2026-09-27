# Figure captions

Numbers identify the 23 concepts in this collection. Interpretations are descriptive; no statistical-superiority claim is made. Qualitative images use fixed validation cases selected using ground truth only. Held-out figures report frozen aggregate results only. TriContextNet validation HD95 remains NA.

## Figure 01 — TriContextNet architecture and ordered context

TriContextNet ordered tri-slice multimodal context. Four MRI modalities from each of three ordered adjacent axial slices (z−1, z, and z+1) form a 12-channel input. An MK-UNet-derived encoder–decoder predicts the four-class segmentation of the centre slice. Skips are taken after pooling: t1=16×128×128, t2=32×64×64, t3=64×32×32 and t4=96×16×16 (channels×height×width). Decoder dimensions are after upsampling. Attention insets are simplified schematics: channel attention combines global average/max pooling through shared transformations; spatial attention uses channel-wise average/max aggregation before a 7×7 convolution; each gate is conditioned on the upsampled decoder feature. Encoder 5's 8×8 label includes its pooling operation and denotes the same tensor shown as the bottleneck. The four-class logits are argmax-decoded before the eight-pixel border is removed. MRI thumbnails are illustrative.

## Figure 02 — Accuracy–efficiency comparison

Accuracy–efficiency overview. Frozen held-out overall mean Dice is plotted against architecture-level GFLOPs per prediction on a logarithmic horizontal axis for the 11-model publication comparison. Marker area represents total parameter count and TriContextNet is highlighted. The figure is descriptive; different input workloads are retained and no statistical-superiority or hardware-latency claim is implied.

## Figure 03 — Controlled A0/A1/A2 context ablation

Frozen validation-only A0/A1/A2 evidence. The left panel shows exact frozen aggregate Dice for WT, TC, ET, and overall Dice. A0 is the historical single-slice reference, A1 is the repeated-centre control, and A2 is TriContextNet with real neighbouring slices. The right panel shows the frozen displayed A2-minus-A1 differences in percentage points. Differences are descriptive and no significance test was performed.

## Figure 04 — Subject-level validation distributions

Frozen subject-level validation distributions. Per-subject validation Dice is shown for TriContextNet, Rolling-Unet-S, and base CMUNeXt across WT, TC, ET, and per-subject overall Dice. Overall is the mean of WT, TC, and ET. The scientific plot regions are pixel-preserved from the frozen source; the display is descriptive and contains no statistical test.

## Figure 05 — Main fixed-case qualitative comparison

Compact fixed-case validation qualitative comparison. P10, P40, P75, and P90 are shown as full-image FLAIR rows and identically cropped ground-truth-defined ROI rows. Columns show FLAIR, ground truth, TriContextNet, Rolling-Unet-S, and base CMUNeXt. Tumour colours are NCR/NET in gold, oedema in cyan, and enhancing tumour in magenta. Selection used ground truth only; predictions, metrics, and visual preference played no role.

## Figure 06 — Multimodal MRI anatomy atlas

Multimodal validation anatomy atlas. T1, T1ce, T2, FLAIR, and ground truth are shown for the fixed P10, P50, and P90 lesion-burden cases. Public percentile labels derive only from validation ground-truth whole-tumour burden; no prediction or model score influenced selection. Colours denote NCR/NET in gold, oedema in cyan, and enhancing tumour in magenta.

## Figure 07 — Visual tri-slice multimodal input context

TriContextNet tri-slice multimodal input context. T1, T1ce, T2, and FLAIR are shown at z−1, z, and z+1 for the fixed validation P50 case; the ground-truth mask belongs only to the centre slice. Display scaling is for visualization and did not enter inference or selection.

## Figure 08 — Ground-truth and FLAIR slice progression

Ground-truth and FLAIR slice progression. FLAIR and corresponding ground-truth overlays are shown from z−4 through z+4 around the fixed validation P50 centre slice. The panel illustrates through-plane anatomical continuity only and does not contain model predictions or imply performance.

## Figure 09 — Seven-case shared qualitative comparison

Seven-case validation qualitative comparison. FLAIR, ground truth, TriContextNet, Rolling-Unet-S, and base CMUNeXt are shown for the fixed P10, P25, P40, P50, P60, P75, and P90 cases. Cases and slices were selected only from ground-truth burden and area rules; model predictions, scores, and visual preference did not influence selection.

## Figure 10 — WT/TC/ET overlay atlas

WT, TC, and ET validation overlay atlas. Ground truth and predictions from TriContextNet, Rolling-Unet-S, and base CMUNeXt are displayed for fixed P25, P50, and P75 cases. WT is gold, TC is cyan, and ET is magenta. The cases were selected from ground truth only; the panel is descriptive.

## Figure 11 — Ground-truth-defined boundary detail crops

Ground-truth-defined validation boundary/detail crops. FLAIR, ground truth, TriContextNet, Rolling-Unet-S, and base CMUNeXt are shown inside identical crops defined by the ground-truth WT bounding box plus 16 pixels. Crop definition is independent of predictions; visual differences are descriptive and are not a boundary-distance test.

## Figure 12 — TriContextNet prediction progression

TriContextNet validation prediction progression. FLAIR, ground truth, and TriContextNet predictions are shown from z−2 through z+2 around the fixed P50 centre slice. The panel is a descriptive visualization of one predeclared case and is not a quantitative consistency analysis.

## Figure 13 — Regional TP/FP/FN detail atlas

Regional TP/FP/FN validation detail atlas. Within identical ground-truth-defined crops for P10, P40, P75, and P90, rows show TriContextNet, Rolling-Unet-S, and base CMUNeXt, while columns separate WT, TC, and ET. True positives, false positives, and false negatives are colour-coded. The cases are fixed by ground truth and the display is descriptive.

## Figure 14 — Boundary contour disagreement

Ground-truth-defined validation boundary and contour disagreement. Exact undilated ground-truth and predicted contours for WT, TC, and ET are overlaid within identical GT-defined crops for P10, P40, P75, and P90. Rows show TriContextNet, Rolling-Unet-S, and base CMUNeXt. No mask smoothing or postprocessing was introduced.

## Figure 15 — Cross-slice anatomical and prediction consistency

P50 cross-slice anatomical and prediction consistency. FLAIR, T1ce, ground truth, TriContextNet prediction, and binary WT TP/FP/FN are shown from z−2 through z+2 around the fixed validation centre slice. The neighbourhood was fixed before rendering and is descriptive rather than a cohort-level consistency metric.

## Figure 16 — Regional held-out Dice comparison

Regional held-out Dice comparison. WT, TC, and ET cohort-mean Dice are shown for six selected completed systems, including TriContextNet. Values come from the frozen 37-subject held-out evaluation. The display is descriptive, omits uncertainty, and does not establish statistical superiority.

## Figure 17 — Held-out regional Dice matrix

Held-out regional Dice matrix. Frozen cohort-mean WT, TC, ET, and overall Dice values are shown for the complete 11-model publication comparison on the protected 37-subject held-out cohort. Colour uses a fixed 0–1 scale. The matrix is descriptive and does not include uncertainty or significance testing.

## Figure 18 — Held-out Dice–HD95 trade-offs

Held-out Dice–HD95 trade-offs. Frozen cohort-mean Dice and mean HD95 are shown for WT, TC, and ET across the 11-model publication comparison. Higher Dice and lower HD95 are preferable. The visibly declared magnified Dice range aids comparison; the panels are descriptive and do not define a composite optimum or statistical ordering.

## Figure 19 — Regional profiles of the top four held-out systems

Regional profiles of the top four held-out systems. The four systems with the highest observed held-out overall mean Dice are shown across WT, TC, and ET. The subset and values are deterministic consequences of the frozen comparison. The profile is descriptive and is not a new balance metric or significance analysis.

## Figure 20 — Validation versus held-out overall Dice

Validation and held-out overall Dice. Frozen overall mean Dice is paired for each model across the validation and protected held-out cohorts. The magnified vertical scale is explicitly declared. The figure is descriptive, contains no uncertainty estimate, and should not be interpreted as a causal analysis of generalization.

## Figure 21 — Validation regional Dice matrix

Validation regional Dice matrix. Frozen cohort-mean WT, TC, ET, and overall Dice values are shown for the complete 11-model publication comparison on the 37-subject validation cohort. Colour uses a fixed 0–1 scale. The matrix is descriptive and should remain secondary to held-out reporting.

## Figure 22 — Held-out regional HD95 matrix

Held-out regional HD95 matrix. Frozen mean WT, TC, and ET HD95 values in millimetres are shown for the complete 11-model publication comparison on the protected held-out cohort. Lower values are preferable. The matrix is descriptive and mean HD95 does not show subject-level variation or uncertainty.

## Figure 23 — Validation regional HD95 matrix

Validation regional HD95 matrix. Available frozen mean WT, TC, and ET HD95 values in millimetres are shown for the 11-model publication comparison. Lower values are preferable. TriContextNet validation HD95 was not present in the frozen record and remains visibly NA; no value is reconstructed or imputed.
