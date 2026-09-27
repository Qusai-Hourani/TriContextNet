# Publication figure catalog

This collection contains 23 scientific concepts: 5 core, 10 brain-image/qualitative, 4 benchmark/performance and 4 supplementary/optional. PNG and SVG versions represent the same concept. Figure 01 uses the single corrected architecture JPEG one directory above this collection.

[Contact sheet](00_all_figures_contact_sheet.png) · [Captions](figure_captions.md) · [SHA256 checksums](SHA256SUMS.txt)

All 22 non-architecture PNGs and 21 SVGs are byte-identical to the verified frozen exports. Figure 05 SVG differs only in its non-rendered accessibility description, where an internal reference was removed; all drawing elements and embedded image bytes are unchanged. No scientific panel was regenerated or modified.

## 01. TriContextNet architecture and ordered context

- Category: Core
- JPG: [tricontextnet_architecture.jpg](../tricontextnet_architecture.jpg)
- Raster SHA256: `7B81290CEB02B006D07D74DBEF79B02C4D2B04200BA2E86EF4E13DC31780FF3A`
- Dimensions: 4375 × 3666 pixels
- Purpose: How does the ordered three-slice, four-modality input reach the centre-slice output?
- Scope: Method description; illustrative MRI thumbnails, not an evaluation result.
- Limitation: Architecture and attention insets summarize the implementation; the diagram is not empirical performance evidence.

## 02. Accuracy–efficiency comparison

- Category: Core
- PNG: [02_accuracy_efficiency.png](01_core/02_accuracy_efficiency.png)
- Raster SHA256: `175F57F2DCE4DDA6F6FE86FD7C756CFCF56D8584C3809E51BBC52579019D6D79`
- Dimensions: 2100 × 1350 pixels
- SVG: [02_accuracy_efficiency.svg](01_core/vector/02_accuracy_efficiency.svg)
- SVG SHA256: `D7337C1242E1D5F6C0B56D3726BE108E28096AA8B5FD516C99CF0C363691CF5D`
- SVG size: 1400 × 900; viewBox `0 0 1400 900`
- Purpose: Where does TriContextNet sit in observed held-out Dice versus architecture-level computation?
- Scope: Frozen held-out aggregate reporting; 11-model publication roster
- Limitation: Different input workloads are retained; GFLOPs are not latency, energy, or controlled hardware measurements.

## 03. Controlled A0/A1/A2 context ablation

- Category: Core
- PNG: [03_context_ablation.png](01_core/03_context_ablation.png)
- Raster SHA256: `B07F3515D7F477CA6A4971440080F2986DB633A3CD8FD1E05769E5627C53E12B`
- Dimensions: 1900 × 1150 pixels
- SVG: [03_context_ablation.svg](01_core/vector/03_context_ablation.svg)
- SVG SHA256: `4EB7F8D891D404D5CA1C39C23FBC01BBEF68C5CFF8EF2DE620D9671B29AB4443`
- SVG size: 1900 × 1150; viewBox `0 0 1900 1150`
- Purpose: Does real neighbouring-slice input differ descriptively from repeated centre-slice input?
- Scope: Frozen validation-only aggregate ablation
- Limitation: One training trajectory per condition; no confidence interval or significance test was performed.

## 04. Subject-level validation distributions

- Category: Core
- PNG: [04_subject_distributions.png](01_core/04_subject_distributions.png)
- Raster SHA256: `87E614945F29CB442EA18DE947C0FA629EB07D5377D1074D31C8CEEEC2D1BD1A`
- Dimensions: 1900 × 1220 pixels
- SVG: [04_subject_distributions.svg](01_core/vector/04_subject_distributions.svg)
- SVG SHA256: `2F6D65C9526F5398BE0D4CBF262667A7E4D8E827F587FE1510FBCFA9CFCEFA4A`
- SVG size: 1900 × 1220; viewBox `0 0 1900 1220`
- Purpose: How variable are validation Dice values across subjects and regions for the active qualitative roster?
- Scope: Frozen validation-only subject-level reporting
- Limitation: Descriptive distributions only; no ranking or statistical test is shown.

## 05. Main fixed-case qualitative comparison

- Category: Core
- PNG: [05_main_qualitative.png](01_core/05_main_qualitative.png)
- Raster SHA256: `65891E6DE8911D88FBD3EA5821FE1A32CD5774ED8F4AFB1316B52733199D8ECC`
- Dimensions: 1540 × 2200 pixels
- SVG: [05_main_qualitative.svg](01_core/vector/05_main_qualitative.svg)
- SVG SHA256: `7D35845A0F64D564E2AE8B97D0830BA2154DB81F642BAD012BF0AB57D6A24114`
- SVG size: 1540 × 2200; viewBox `0 0 1540 2200`
- Purpose: What do the three active models predict on four fixed lesion-burden cases at full-image and ROI scales?
- Scope: Frozen validation-only GT-burden-selected qualitative reporting
- Limitation: Four selected slices are illustrative and cannot establish population-level or universal visual superiority.

## 06. Multimodal MRI anatomy atlas

- Category: Brain-image / qualitative
- PNG: [06_multimodal_mri_atlas.png](02_brain_image_qualitative/06_multimodal_mri_atlas.png)
- Raster SHA256: `63AD867E66C0117580CA7BBA9FC843DF9C38C50F79C09C2A75E14FAFC9536945`
- Dimensions: 1310 × 814 pixels
- SVG: [06_multimodal_mri_atlas.svg](02_brain_image_qualitative/vector/06_multimodal_mri_atlas.svg)
- SVG SHA256: `CA0C5FBB6FCBB1E4D96292862199D4DC49C6779A1304DC265A9BA7546CF5C0B7`
- SVG size: 1310 × 814; viewBox `0 0 1310 814`
- Purpose: How do T1, T1ce, T2, FLAIR, and ground truth complement one another across lesion burdens?
- Scope: Validation-only GT-burden-selected display
- Limitation: Three cases illustrate modality contrast but do not represent the full cohort.

## 07. Visual tri-slice multimodal input context

- Category: Brain-image / qualitative
- PNG: [07_trislice_multimodal_context.png](02_brain_image_qualitative/07_trislice_multimodal_context.png)
- Raster SHA256: `E6FC18D961C3C47A3727FAF25A400CD522651938481DEAD8E7CB146B4D875D68`
- Dimensions: 1310 × 814 pixels
- SVG: [07_trislice_multimodal_context.svg](02_brain_image_qualitative/vector/07_trislice_multimodal_context.svg)
- SVG SHA256: `70870CFA52171A6D164E157BE69A4274E8B29E9A38516BAB4AD527114DF4EC69`
- SVG size: 1310 × 814; viewBox `0 0 1310 814`
- Purpose: What anatomical information is available across z−1, z, and z+1 for all four modalities?
- Scope: Validation-only input-context display
- Limitation: One fixed case illustrates the input interface rather than population variability.

## 08. Ground-truth and FLAIR slice progression

- Category: Brain-image / qualitative
- PNG: [08_gt_flair_slice_progression.png](02_brain_image_qualitative/08_gt_flair_slice_progression.png)
- Raster SHA256: `1EC835E9AA817A3B8369DB76CCACA7753651735CDF33EF75B1A54878828F1B8A`
- Dimensions: 590 × 2254 pixels
- SVG: [08_gt_flair_slice_progression.svg](02_brain_image_qualitative/vector/08_gt_flair_slice_progression.svg)
- SVG SHA256: `1EFBBE382648F044BC2C127A4C5C55015492201AAB09421CD68050A74B081608`
- SVG size: 590 × 2254; viewBox `0 0 590 2254`
- Purpose: How does tumour anatomy evolve through adjacent axial slices around a fixed centre?
- Scope: Validation-only GT/FLAIR display
- Limitation: A single case and FLAIR view cannot represent all anatomical patterns.

## 09. Seven-case shared qualitative comparison

- Category: Brain-image / qualitative
- PNG: [09_seven_case_comparison.png](02_brain_image_qualitative/09_seven_case_comparison.png)
- Raster SHA256: `1F5DC9E363B880194501EB275BFCBDC105663DC74F97565A9CAC0C7C421AC019`
- Dimensions: 1310 × 1774 pixels
- SVG: [09_seven_case_comparison.svg](02_brain_image_qualitative/vector/09_seven_case_comparison.svg)
- SVG SHA256: `C59F44D36EA1C0783C8FFAEFE413924DF92AA45FB41CB414EFC6327C4B7425E0`
- SVG size: 1310 × 1774; viewBox `0 0 1310 1774`
- Purpose: How do the active models compare over seven predeclared burden-percentile cases?
- Scope: Validation-only GT-burden-selected qualitative reporting
- Limitation: Seven slices remain illustrative and do not establish statistical or universal visual superiority.

## 10. WT/TC/ET overlay atlas

- Category: Brain-image / qualitative
- PNG: [10_regional_overlay_atlas.png](02_brain_image_qualitative/10_regional_overlay_atlas.png)
- Raster SHA256: `8ABE15E32DAAC6E30FD7B4FC31A779CE04906F494F7D34CA60CFA9D9573FED0D`
- Dimensions: 1070 × 2254 pixels
- SVG: [10_regional_overlay_atlas.svg](02_brain_image_qualitative/vector/10_regional_overlay_atlas.svg)
- SVG SHA256: `0D38308242085523A7EB410396E38742F14F9DA1714B5585C93A08C822733A9C`
- SVG size: 1070 × 2254; viewBox `0 0 1070 2254`
- Purpose: How do WT, TC, and ET overlays differ among models on fixed cases?
- Scope: Validation-only regional overlay display
- Limitation: Region overlays are illustrative and do not quantify error frequency or significance.

## 11. Ground-truth-defined boundary detail crops

- Category: Brain-image / qualitative
- PNG: [11_boundary_detail_crops.png](02_brain_image_qualitative/11_boundary_detail_crops.png)
- Raster SHA256: `B22F86D7BBD00C5FA55049F810026E617A359344F7EF8A7712F4B780B9659C31`
- Dimensions: 1310 × 814 pixels
- SVG: [11_boundary_detail_crops.svg](02_brain_image_qualitative/vector/11_boundary_detail_crops.svg)
- SVG SHA256: `F281EC87CD56B0D3FF814FD5CB21F5C346FBA90588ACABCB2D8929007D506466`
- SVG size: 1310 × 814; viewBox `0 0 1310 814`
- Purpose: What boundary and subregion detail is visible when every model is shown in the same GT-defined crop?
- Scope: Validation-only GT-defined ROI display
- Limitation: Three crops cannot establish population-level boundary superiority and are not HD95 measurements.

## 12. TriContextNet prediction progression

- Category: Brain-image / qualitative
- PNG: [12_prediction_progression.png](02_brain_image_qualitative/12_prediction_progression.png)
- Raster SHA256: `7A622EBB15323F929CAA43D4292CF61FD71348E27E8DFCFF962A9E76D1266866`
- Dimensions: 830 × 1294 pixels
- SVG: [12_prediction_progression.svg](02_brain_image_qualitative/vector/12_prediction_progression.svg)
- SVG SHA256: `885A02F741E1C52350D8DDCB10D9511C46EDC681E949CFC1EC2C8CBAAC8DF4E9`
- SVG size: 830 × 1294; viewBox `0 0 830 1294`
- Purpose: How does TriContextNet's segmentation evolve from z−2 to z+2 around one fixed centre?
- Scope: Validation-only cross-slice qualitative display
- Limitation: One case illustrates continuity but cannot quantify consistency across the cohort.

## 13. Regional TP/FP/FN detail atlas

- Category: Brain-image / qualitative
- PNG: [13_regional_error_atlas.png](02_brain_image_qualitative/13_regional_error_atlas.png)
- Raster SHA256: `2B52DE3231E3F74B1B47E5DDAC04EFD739E5FCA623000E89269F776153B3440B`
- Dimensions: 1872 × 2055 pixels
- SVG: [13_regional_error_atlas.svg](02_brain_image_qualitative/vector/13_regional_error_atlas.svg)
- SVG SHA256: `013B76C0511E7B75B837DFCF02A3BFE98E56E47CC29A2928B8711BE4E79FD00D`
- SVG size: 1872 × 2055; viewBox `0 0 1872 2055`
- Purpose: Where do true-positive, false-positive, and false-negative regions occur for WT, TC, and ET?
- Scope: Frozen validation-only regional error display
- Limitation: Illustrative fixed cases only; area appearance is not an error-rate estimate or significance result.

## 14. Boundary contour disagreement

- Category: Brain-image / qualitative
- PNG: [14_boundary_contour_disagreement.png](02_brain_image_qualitative/14_boundary_contour_disagreement.png)
- Raster SHA256: `E0B5D4B22B0994104D1C8125B2B78A3543AEBC98E8BE474A542DC042A261EE77`
- Dimensions: 1872 × 2055 pixels
- SVG: [14_boundary_contour_disagreement.svg](02_brain_image_qualitative/vector/14_boundary_contour_disagreement.svg)
- SVG SHA256: `055FD9B5B7043551C0B9A760C3D601A63C137A9E4B719EBA767417BF9A7AD9A1`
- SVG size: 1872 × 2055; viewBox `0 0 1872 2055`
- Purpose: Where do exact GT and predicted contours disagree for WT, TC, and ET?
- Scope: Frozen validation-only boundary display
- Limitation: Contour appearance is illustrative and is not a substitute for HD95 or statistical boundary analysis.

## 15. Cross-slice anatomical and prediction consistency

- Category: Brain-image / qualitative
- PNG: [15_cross_slice_consistency.png](02_brain_image_qualitative/15_cross_slice_consistency.png)
- Raster SHA256: `CD09D9906926CB50D97C0E903E76981D8F8F033566F0CFAD1CDD13DB57AA7477`
- Dimensions: 1345 × 1408 pixels
- SVG: [15_cross_slice_consistency.svg](02_brain_image_qualitative/vector/15_cross_slice_consistency.svg)
- SVG SHA256: `B1269D9EC43AA20075FC6E9BCC396C9535408E51F6CB9CD77505DF40E61307CF`
- SVG size: 1345 × 1408; viewBox `0 0 1345 1408`
- Purpose: How do anatomy, GT, TriContextNet prediction, and binary error evolve across z−2 to z+2?
- Scope: Frozen validation-only cross-slice display
- Limitation: One fixed P50 neighbourhood is illustrative and does not quantify cohort-wide consistency.

## 16. Regional held-out Dice comparison

- Category: Benchmark / performance
- PNG: [16_regional_heldout_dice.png](03_benchmark_performance/16_regional_heldout_dice.png)
- Raster SHA256: `E4C0B4A199B2B9751ED2BF4C3F0937B1044BC9109AF19BE96B5C6FAD1546E011`
- Dimensions: 2100 × 1350 pixels
- SVG: [16_regional_heldout_dice.svg](03_benchmark_performance/vector/16_regional_heldout_dice.svg)
- SVG SHA256: `4693D1CD5A2EFD8AEEA547467A6E50801B2974808552EE9126CC1149FE274A66`
- SVG size: 1400 × 900; viewBox `0 0 1400 900`
- Purpose: How do selected systems differ across held-out WT, TC, and ET Dice?
- Scope: Frozen held-out aggregate reporting; selected six-model display
- Limitation: The six-model view is selective, descriptive, and contains no significance test.

## 17. Held-out regional Dice matrix

- Category: Benchmark / performance
- PNG: [17_heldout_regional_dice_matrix.png](03_benchmark_performance/17_heldout_regional_dice_matrix.png)
- Raster SHA256: `3B00EE6AB85671A30785AC371A034F380EC4D6A9648072D44DEDA6DDC1BD0F34`
- Dimensions: 2100 × 1600 pixels
- SVG: [17_heldout_regional_dice_matrix.svg](03_benchmark_performance/vector/17_heldout_regional_dice_matrix.svg)
- SVG SHA256: `0D330E40032AD6F3DF5FD3EFE24E5610255AE874C2633BCC3C43D6EF64BC224D`
- SVG size: 2100 × 1600; viewBox `0 0 2100 1600`
- Purpose: Which systems lead or trail by held-out region and overall Dice?
- Scope: Frozen held-out aggregate reporting; complete 11-model publication roster
- Limitation: Cohort means conceal subject-level variability; colour encodes a fixed 0–1 Dice scale.

## 18. Held-out Dice–HD95 trade-offs

- Category: Benchmark / performance
- PNG: [18_heldout_dice_hd95_tradeoffs.png](03_benchmark_performance/18_heldout_dice_hd95_tradeoffs.png)
- Raster SHA256: `DB0D4B472EC63B2CC232E890B6DC4DC840AF5B4483FBA639986205CF7F28B1E3`
- Dimensions: 2100 × 1400 pixels
- SVG: [18_heldout_dice_hd95_tradeoffs.svg](03_benchmark_performance/vector/18_heldout_dice_hd95_tradeoffs.svg)
- SVG SHA256: `85296838DC6238F0F106665E20014492FC4910E4F6C9BE79ED25E89A446F9630`
- SVG size: 2100 × 1400; viewBox `0 0 2100 1400`
- Purpose: Do overlap and boundary-distance ordering tell the same story across regions?
- Scope: Frozen held-out aggregate Dice and HD95 reporting
- Limitation: Descriptive aggregate trade-offs only; the magnified Dice axis does not estimate correlation or an optimum.

## 19. Regional profiles of the top four held-out systems

- Category: Benchmark / performance
- PNG: [19_top_model_regional_profiles.png](03_benchmark_performance/19_top_model_regional_profiles.png)
- Raster SHA256: `40F616B48B884EE28C81F4143D262D0FD03BB2306F80361457C2EF9947D79DB4`
- Dimensions: 2100 × 1400 pixels
- SVG: [19_top_model_regional_profiles.svg](03_benchmark_performance/vector/19_top_model_regional_profiles.svg)
- SVG SHA256: `0BC99EB551AC93B72D21F0485FDD0463350689F0B9BFCEA0630FC115762761FE`
- SVG size: 2100 × 1400; viewBox `0 0 2100 1400`
- Purpose: How do the leading overall systems' regional Dice profiles differ?
- Scope: Frozen held-out aggregate reporting; deterministic top-four subset
- Limitation: The subset is selected by observed held-out overall Dice and the profile is not a new balance metric.

## 20. Validation versus held-out overall Dice

- Category: Supplementary / optional
- PNG: [20_validation_heldout_overall.png](04_supplementary_optional/20_validation_heldout_overall.png)
- Raster SHA256: `CB779243FEAB86D970F3142AB90D9840F52CB576087125DEF13A4803FD8CD718`
- Dimensions: 2100 × 1500 pixels
- SVG: [20_validation_heldout_overall.svg](04_supplementary_optional/vector/20_validation_heldout_overall.svg)
- SVG SHA256: `7B2363104A6DEBE6E188B1C20268173D87521D6D44C77C8EE3DCFB36E94C67E0`
- SVG size: 2100 × 1500; viewBox `0 0 2100 1500`
- Purpose: How does observed overall Dice change from validation to held-out evaluation for each displayed model?
- Scope: Frozen validation and held-out aggregate reporting
- Limitation: Not a causal generalization analysis; the magnified vertical scale and lack of uncertainty require caution.

## 21. Validation regional Dice matrix

- Category: Supplementary / optional
- PNG: [21_validation_regional_dice_matrix.png](04_supplementary_optional/21_validation_regional_dice_matrix.png)
- Raster SHA256: `F172111A8927389853531D0A941F131A73EC4F915A707655F984D8E220F4A779`
- Dimensions: 2100 × 1600 pixels
- SVG: [21_validation_regional_dice_matrix.svg](04_supplementary_optional/vector/21_validation_regional_dice_matrix.svg)
- SVG SHA256: `272D3BF6C505F90567F3E05FB57D2AA6F80280F496361DED1A9D3EB9C748BA8B`
- SVG size: 2100 × 1600; viewBox `0 0 2100 1600`
- Purpose: What are the complete regional validation Dice values used in the comparison?
- Scope: Frozen validation aggregate reporting; complete 11-model publication roster
- Limitation: Secondary to held-out evidence; cohort means conceal subject-level variation.

## 22. Held-out regional HD95 matrix

- Category: Supplementary / optional
- PNG: [22_heldout_regional_hd95_matrix.png](04_supplementary_optional/22_heldout_regional_hd95_matrix.png)
- Raster SHA256: `C9CE1103EE41D6A7347ECBDE54A213DBCBBE94E4B05C296E6FB474607083DC06`
- Dimensions: 2100 × 1600 pixels
- SVG: [22_heldout_regional_hd95_matrix.svg](04_supplementary_optional/vector/22_heldout_regional_hd95_matrix.svg)
- SVG SHA256: `FA9B85485E6C5E3F241070BE3117FC50DB96CFC49EE4CED44587ACF9FCEA7681`
- SVG size: 2100 × 1600; viewBox `0 0 2100 1600`
- Purpose: How does held-out boundary-distance performance vary by model and region?
- Scope: Frozen held-out aggregate HD95 reporting
- Limitation: Mean HD95 hides the underlying distribution; lower is better and no uncertainty is available.

## 23. Validation regional HD95 matrix

- Category: Supplementary / optional
- PNG: [23_validation_regional_hd95_matrix.png](04_supplementary_optional/23_validation_regional_hd95_matrix.png)
- Raster SHA256: `C323E2E3A8C521C2D912F856F14E03CADE17264FDAC80F8461306F48D6241AEF`
- Dimensions: 2100 × 1600 pixels
- SVG: [23_validation_regional_hd95_matrix.svg](04_supplementary_optional/vector/23_validation_regional_hd95_matrix.svg)
- SVG SHA256: `04AC077935F136437F238A33A05BB628BFBCE9EA7A35270E428252E6D9D8DB68`
- SVG size: 2100 × 1600; viewBox `0 0 2100 1600`
- Purpose: Which validation HD95 values are available across models and regions?
- Scope: Frozen validation aggregate HD95 reporting
- Limitation: TriContextNet validation HD95 is unavailable and remains visibly NA; it must not be imputed or reconstructed.
