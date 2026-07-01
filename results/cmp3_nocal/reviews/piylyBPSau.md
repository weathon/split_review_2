## Summary

This paper proposes GenCoGS, a unified 3DGS-based few-shot novel view synthesis method that addresses the overdependence on observed regions through two generative completion strategies: (1) GCGI — a point cloud completion pipeline (DGCNN + Transformer + FoldingNet with kd-tree filtering) that produces a more complete point cloud for 3D Gaussian initialization, and (2) GCGO — a pseudo-view completion strategy using an I2V diffusion model with perturbed camera trajectories and a generative consistency loss to mitigate hallucination during optimization. The method achieves consistent improvements across LLFF, DTU, and Shiny datasets under 3/6/9-view settings, with gains of up to 2.40 dB PSNR over 3DGS-based methods.

## Strengths

1. **Well-motivated problem framing.** The paper clearly identifies a genuine limitation of existing 3DGS-based few-shot NVS methods — their overdependence on observed regions leads to incomplete scene representations, floating artifacts, and missing details (Section 1, Figure 1). The two-pronged response (initialization + optimization) is a principled architectural response to this problem.

2. **Coherent two-pronged architecture with complementary contributions.** Addressing both initialization (GCGI) and optimization (GCGO) is structurally sound. The ablation study (Table 4) confirms each strategy contributes positively and the combination yields the best results, demonstrating that the design is not redundant.

3. **Practical outlier filtering via kd-tree.** The CPF module (Section 3.1.2) is a lightweight, parameter-free solution: using the SfM point cloud as a high-confidence reference and kd-tree nearest-neighbor queries to filter hallucinated points. This is well-illustrated in Figure 3 and directly addresses a genuine problem with generated points.

4. **Consistent quantitative improvements across settings.** Across three datasets (LLFF, DTU, Shiny) and multiple few-shot settings (3/6/9 views), GenCoGS consistently outperforms baselines. On DTU (Table 2), the improvement over the best 3DGS-based method (BinoGS) is +2.40 dB PSNR; on Shiny (Table 3), +1.47 dB PSNR, +0.080 SSIM, −0.125 LPIPS over FSGS.

5. **Informative ablation studies.** Tables 4, 5, and 6 decompose contributions of GCGI/GCGO, the perturbed trajectory vs. random sampling, and the CPG/CPF sub-components. The acknowledgment of the see-saw effect between hallucination and coverage (Figure 8) demonstrates honest engagement with the method's limitations.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Missing specification of how the CPG module is trained.** The CPG module (Section 3.1.1) consists of learned networks (DGCNN, Transformer encoder-decoder, FoldingNet), but the paper provides no information about its training: what dataset it is trained on, what loss function is used, whether it is pretrained on external 3D data or trained per-scene, or any optimization details. The reproducibility statement (lines 347–349) claims comprehensive details, but this information is absent from the main text. While the appendix may contain some of this (it is stripped by the parser), the main body should at minimum indicate where these details reside. The architecture is described, so reimplementation is possible but would require guessing the training protocol. This is the most significant missing piece.

2. **"Generative" terminology is imprecise for the GCGI pipeline.** The paper calls GCGI a "generative point cloud completion-based" strategy (title, abstract, line 30, Section 3.1). However, the pipeline (DGCNN → Transformer → FoldingNet) is a deterministic feed-forward completion network, not a probabilistic generative model (it does not sample from a learned distribution). The I2V-based GCGO genuinely uses a generative model, but applying the same label to both conflates two different mechanisms. This does not undermine the technical contribution (applying learned point cloud completion to 3DGS initialization is valid), but it inflates the framing. The contribution should be characterized as a learned completion pipeline, not a generative one.

3. **ViewCrafter is used internally but absent from quantitative comparisons.** ViewCrafter (Yu et al., 2024a) serves as the I2V diffusion model within GCGO and is shown qualitatively in Figure 6, yet it does not appear in any quantitative table (Tables 1, 2, 3). Including ViewCrafter as a baseline would help isolate whether GenCoGS's improvements come from the GCGI initialization, the perturbed trajectory plus consistency loss, or simply from a different usage of the same I2V model. This is the most natural control experiment for the GCGO contribution.

4. **No sensitivity analysis for key hyperparameters.** Several critical hyperparameters are set to specific values without ablation: δ₁ = 1.0 (filtering threshold in CPF), δ₂ = 20 (variance coefficient in the adaptive threshold, Eq. 13), α = 10.0 (loss weight in Eq. 18), the perturbation amplitude A, and the phase-switch iteration m = 4000. Only A receives any qualitative discussion (Figure 8, comparing A=2.0 vs A=3.0). A quantitative sensitivity sweep would substantiate the choices and help assess robustness.

5. **Anomalous ReconX result on DTU is not discussed.** ReconX achieves an SSIM of 0.476 on DTU (Table 2), dramatically lower than every other baseline (next worst: FSGS at 0.818). The paper does not remark on this. If correctly evaluated, the result needs explanation; if not, including it inflates GenCoGS's lead. Either way, the silence is a gap.

6. **No runtime or computational cost comparison.** Adding an I2V diffusion model to 3DGS implies a substantial increase in per-scene optimization time and GPU memory. The paper motivates 3DGS for "rendering efficiency and quality" (line 35) but never reports training time, peak memory, or inference speed for GenCoGS or any baseline. This is standard for a method that adds a computationally expensive component.

### Trivial
- **Table 3 caption error.** The caption reads "Shiny (Jensen et al., 2014)" but Shiny is from Wizadwongsa et al. (2021); Jensen et al. (2014) is the DTU dataset. The introduction correctly cites Shiny, so this is a caption-level error only.
- **Inconsistent bold highlighting in Table 2 (DTU).** The caption states "best, second-best, and third-best scores are highlighted," but the SSIM column has four bold entries (MuRF 0.885, CAT3D 0.844, BinoGS 0.862, GenCoGS 0.910), exceeding the stated three. This is a formatting inconsistency.

## Nice-to-Haves
- A quantitative sweep of the perturbation amplitude A (e.g., 0.5, 1.0, 2.0, 3.0, 5.0) with corresponding PSNR/SSIM/LPIPS would turn the qualitative see-saw observation (Figure 8) into a principled justification.
- Including ViewCrafter quantitatively on at least one dataset (e.g., LLFF 3-view) would cleanly isolate GCGO's added value.
- A runtime/memory comparison table with the top two baselines would honestly characterize the efficiency trade-off introduced by the I2V diffusion model.

## Removed Points
- **Speculation about CPG training on external data leading to unfair comparison (from Issue 1).** The reviewer speculated that "if the CPG module is pretrained on large-scale 3D datasets... the comparison against baselines that do not use such external training data would be fundamentally unfair." This is speculative — the paper does not state this and the appendix is stripped. Per the filtering rules, speculation about missing information is demoted. The core observation (training details are absent) is retained in Minor Weakness #1.
- **Factually incorrect claims about bold highlighting (from Issue 4).** The reviewer claimed the AVGE column had four bold entries including IPSM (0.077) — IPSM is not bold. The reviewer also claimed CAT3D was not bold in SSIM — it is bold. The underlying inconsistency point (4 bolds in SSIM vs. the stated 3) is real and is retained in Trivial.
- **Strength about "well-motivated problem framing"** — this is generic and non-specific. Removed per filtering rules. The more specific Architecture and CPF strengths are kept.
- **Critique about δ₂ = 20 being "very high."** This is a subjective judgment without quantitative backing in the review itself. The broader point about lack of sensitivity analysis is kept in Minor Weakness #4.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Specify the training protocol for the CPG module — training dataset, loss function, optimization procedure — either in the main text or by explicitly directing readers to an appendix section.
2. Add ViewCrafter to the quantitative comparison on at least one dataset to isolate the contribution of the GCGI initialization and the consistency loss beyond the I2V model itself.
3. Provide a sensitivity table for key hyperparameters (δ₁, δ₂, A, α) to demonstrate robustness and justify the chosen values.
4. Report training time, peak GPU memory, and inference speed for GenCoGS and at least the top two baselines.
5. Either explain the anomalously low ReconX result on DTU or remove it from the table if evaluation conditions were not comparable.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>