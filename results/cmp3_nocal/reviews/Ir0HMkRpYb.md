## Summary

This paper presents *Stylos*, a feedforward 3D Gaussian framework for single-pass stylization from unposed multi-view images. It uses a frozen VGGT backbone for geometry prediction, injects style via cross-attention (CrossBlock modules), and introduces a voxel-level 3D style loss that extends 2D AdaIN statistics matching to 3D feature space. The method achieves stylization in ~0.05s per scene without per-scene optimization, with competitive quantitative results on CO3D and Tanks & Temples benchmarks.

## Strengths

- **Genuinely feedforward 3D stylization with practical speed.** The paper demonstrates a system that produces stylized 3D Gaussians in a single forward pass (0.05s per scene), against 14.7–165 minutes for per-scene optimization methods (StyleGaussian, G-Style, SGSST). The speed gap is real and meaningful—this is the paper's primary contribution, and it is well-supported by Tables 3 and 4.

- **Global CrossBlock ablation is well-executed and informative.** Table 1 shows Global CrossBlock consistently outperforms both Frame and Hybrid variants on all three scenes across PSNR, SSIM, and LPIPS. This cleanly justifies the design choice and provides a clear signal that multi-view cross-attention is beneficial.

- **Handles unposed input across a wide range of view counts.** The system operates without precomputed camera parameters and the scaling experiment (1–64 views, Fig. 4) demonstrates flexibility that is genuinely useful. This is a practical advantage over methods requiring calibrated input.

- **The voxel-level 3D style loss is conceptually clean.** Extending AdaIN statistics matching from 2D to voxel-space (Eq. 5 / Algorithm 1) is a natural idea for enforcing cross-view consistency and is well-motivated by the failure modes of per-frame style matching.

## Weaknesses

### Major

- **Section 4.2 text misattributes results to Styl3R instead of Stylos.** The quantitative evaluation paragraph (lines 232–233) reads: *"As shown in Table 3, Styl3R achieves strong and stable consistency scores, ranking the first across all consistency metrics and all four scenes… Furthermore, Table 4 shows that Styl3R attains either the best or second-best artistic metric values."* This is false per the paper's own tables: Stylos (ours) wins virtually every row. Styl3R records dashes ("–") for the Train scene, ranks last or near-last on most consistency metrics (e.g., short-range LPIPS 0.061 on Truck vs. Stylos's 0.028), and scores poorly on ArtScore (2.94 on Truck vs. Stylos's 9.70). This is not a trivial typo—a coherent paragraph repeatedly swaps the method and the competitor, making the main results section uninterpretable as written. While the underlying data in the tables is correct, this error undermines confidence in the paper's quality control.

- **The Styl3R comparison is underspecified regarding number of input views.** The paper states Styl3R is "primarily designed for 2–8 input views" (line 40) but does not report how many views were used when evaluating Styl3R on Tanks & Temples. If Styl3R was evaluated with more views than its design target, poor consistency results would be expected and uninformative. This variable must be reported for the comparison to be interpretable.

- **StylizedGS is excluded from the main quantitative comparison with a vague justification.** The paper states (line 254): *"StylizedGS… is not included in quantitative comparisons due to its multiple failure cases observed on our test styles. Nevertheless, its quantitative results are reported in A.4 Table 5 and Table 6 for readers' reference."* Excluding a baseline from the main table because it "failed," then relegating its results to an appendix, prevents readers from directly assessing the competitive landscape. "Multiple failure cases" is not quantified. (Note: SGSST is correctly included in the main tables—the reviewer erred in grouping it with StylizedGS.)

### Minor

- **The 3D style loss's quantitative advantage over the simpler scene-level loss is marginal.** In Table 2, the 3D loss achieves ArtScore 9.15 vs. Scene loss's 9.12 (Δ=0.03); short-range LPIPS is tied at 0.047–0.048; long-range RMSE is tied at 0.142 between 3D loss and image loss. The paper claims the 3D loss "enforces view-consistent stylization while maintaining geometric coherence," but the numerical evidence for this advantage over the scene-level baseline is weak. The qualitative examples (Fig. 3) provide more support than the metrics.

- **CrossBlock ablation measures reconstruction quality only, not stylization quality.** Table 1 evaluates PSNR/SSIM/LPIPS, which reflect geometric fidelity in a style-free setting. This is informative but does not show how different CrossBlock designs affect style transfer quality or cross-view stylization consistency—the aspects most relevant to the paper's core claim.

- **Cross-category generalization claim lacks explicit category-level results.** The paper states it trains on 17 CO3D categories and tests on 3 held-out ones (line 170), but no table breaks down results by held-out category. The ablation studies use CO3D scenes (skateboard, pizza, donut) but it is unclear whether these are drawn from the held-out set. The cross-scene generalization to Tanks & Temples is well-documented, but the cross-category claim is less substantiated.

- **No discussion of failure cases or limitations.** The conclusion is entirely forward-looking, with no acknowledgment of scenarios where Stylos might struggle (extreme camera motion, thin structures, large view gaps, etc.). A limitations section would strengthen credibility.

- **Several implementation details are missing.** The paper does not specify how many CrossBlocks are used, where in the backbone they are inserted, the number of Gaussians predicted (M), or the voxel resolution used for the 3D style loss. The distillation loss in Stage 1 (line 114) is also confusing: if the backbone is initialized from VGGT and a frozen VGGT teacher provides supervision, what exactly is being distilled beyond what the initialization already captures?

### Trivial

- None beyond the above.

## Nice-to-Haves

- **A human perceptual evaluation** (even a small-scale study) would strengthen the paper's claims about stylization quality, which is inherently subjective. The paper relies on ArtScore and ArtFID—automated metrics whose validity for this specific task is not independently verified. However, this is above the standard expectation for the field and should not be treated as a required weakness.

- **The multi-style blending experiment** (Fig. 6) is interesting but only qualitatively demonstrated. Quantitative evaluation or comparison to interpolation behavior of other methods would strengthen this section.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"StylizedGS and SGSST are partially excluded"** — SGSST is fully included in Tables 3 and 4 (lines 244, 250, 263). Only StylizedGS is excluded. The criticism as stated conflates two baselines and is factually incorrect about SGSST.

- **"No user study is conducted for a fundamentally subjective task"** — Demoted to Nice-to-Have. While a user study would strengthen the paper, it is not standard practice for 3D stylization papers to include one; the use of ArtScore and ArtFID is consistent with the literature.

- **"Section 2.2 characterization of Styl3R is odd"** — This is a subjective opinion about positioning, not a verifiable weakness.

- **"The paper does not specify how many CrossBlocks are used"** — Merged into the Minor weakness about missing implementation details.

- **"Abstract claims generalization to unseen categories lacks dedicated quantitative evaluation"** — The paper does evaluate on 3 held-out CO3D categories (stated in line 170), and the ablation results are on CO3D. The concern is that no dedicated category-level table is shown, which is now covered under the Minor weakness about cross-category results.

- **"TV regularizer weight not justified"** — A hyperparameter detail that is not unusual to leave unjustified; removed as a nitpick.

## Novel Insights

None beyond the paper's own contributions. The core insight—feedforward 3D stylization via a frozen geometry backbone with style injected through cross-attention—is the paper's own contribution. The reviewers' main value-add was flagging presentation errors and comparison fairness concerns, not surfacing additional novel observations about the method itself.

## Suggestions

1. **Fix the Section 4.2 attribution error.** Replace every instance of "Styl3R" with "Stylos" in the quantitative evaluation paragraph. This is the single most important correction.

2. **Report the number of views used for Styl3R** in the Tanks & Temples evaluation, and clarify whether it falls within Styl3R's designed operating range (2–8 views).

3. **Either include StylizedGS in the main tables or provide a clearly quantified explanation** (e.g., "StylizedGS failed on X out of Y style-scene pairs, producing NaN/truncated outputs").

4. **Add a brief limitations section** discussing failure modes (extreme camera gaps, thin structures, large view counts beyond training distribution) and any observed artifacts.

5. **Clarify the Stage 1 distillation loss.** If the backbone is initialized from VGGT and the teacher is also VGGT, explain what the distillation loss contributes that the initialization does not already provide.

6. **Provide cross-category results** as a dedicated table or explicitly state which CO3D categories were held out and confirm that the ablation scenes are drawn from them.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>