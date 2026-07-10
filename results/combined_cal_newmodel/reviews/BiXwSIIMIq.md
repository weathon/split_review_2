Here is my final consolidated review:

## Summary

This paper proposes AC-DC, a three-stage score-based denoiser (Auto-Correction via additive Gaussian noise, Directional Correction via conditional Langevin dynamics, then Tweedie/ODE denoising) designed to mitigate the manifold mismatch between ADMM optimization iterates and the noisy manifolds score functions are trained on. The paper provides convergence guarantees for ADMM-PnP with the AC-DC denoiser under both fixed and adaptive step-size schedules, extending prior PnP convergence theory to score-based settings. Experiments on 6 inverse problems across two datasets show the method generally achieves best or second-best results.

## Strengths

- **The manifold mismatch problem is well-motivated and genuine.** Sections 1–2 clearly articulate why ADMM iterates—especially with dual variables—do not naturally lie on the Gaussian-perturbed manifolds that score functions are trained on. This is a real obstacle that prior noise-injection strategies only partially address.

- **The three-stage AC-DC denoiser is logically principled.** The AC step adds structured noise, the DC step refines manifold alignment via conditional Langevin dynamics targeting p(z_{σ^{(k)}}|z_ac^{(k)}) (line 129), and the final Tweedie/ODE step performs denoising on the corrected iterate. The conditional score decomposition in Eq. (10) and the Gaussian likelihood approximation (line 135) are technically reasoned.

- **The convergence analysis extends existing ADMM-PnP theory to score-based denoisers.** Theorem 1 generalizes fixed-point convergence (Ryu et al., 2019) to allow weakly contractive (rather than strictly contractive) residuals. Theorems 2–3 instantiate this for the AC-DC denoiser specifically. Extending these results from classical denoisers to diffusion score-based denoisers is a nontrivial theoretical contribution, given the limited convergence theory for score-based PnP methods.

- **Broad experimental evaluation.** The method is evaluated on 6 inverse problems (super-resolution, Gaussian deblur, motion deblur, random inpainting, box inpainting, phase retrieval) across two datasets (FFHQ 256×256, ImageNet 256×256), with 6–9 baselines per task. This coverage exceeds that of typical PnP papers.

## Weaknesses

### Fatal
None.

### Major

1. **Theory–practice gap in the convergence guarantees.** Theorem 2(b) and Theorem 3(b) require σ^{(k)}→0 as k→∞ for convergence of ADMM-PnP with the AC-DC denoiser. However, the practical schedule caps σ^{(k)} = max(0.1, 10 − (10−0.1)·k/W) (line 297), which plateaus at 0.1 and never approaches zero. This means the conditions of the convergence theorems are not satisfied by the actual algorithm run in experiments. The paper's title claims "Convergent" and the abstract presents convergence as a core contribution, but the proof and the implementation operate in different regimes. (Evidence: lines 197, 215 [theory requires σ→0] vs. line 297 [σ capped at 0.1].)

2. **Theorems 2 and 3 assume the Langevin DC step reaches the stationary distribution at each iteration** (line 183: "assume that the DC step reaches the stationary distribution for each k"). The practical algorithm uses only J=10 Langevin steps with step size η^{(k)}=5×10⁻⁴σ^{(k)} (line 297). No evidence or argument is provided that 10 steps mix to stationarity in 256×256×3 image space. The footnote (line 207) defers to Appendix E.2 for counterparts removing this assumption, but the main theorems rest on it, and the appendix removal does not appear in the submitted text. (Evidence: line 183, line 297.)

3. **No computational cost metrics reported.** The AC-DC denoiser is expensive: each ADMM iteration solves the x-subproblem with up to 1000 Adam iterations (line 297), runs J=10 Langevin steps (each requiring a score evaluation), plus a final Tweedie or 10-step ODE denoising. The paper provides no NFE count, wall-clock time, or any cost metric. Given that the gains over the strongest competitor (DAPS) are typically 0.3–0.9 dB PSNR, and the paper's own limitation section (line 379) acknowledges high NFE cost, the omission of cost reporting makes it impossible to assess the practical tradeoff. (Evidence: lines 297, 379.)

### Minor

4. **No statistical significance or variance reporting.** All results are averages over 100 images without standard deviations, error bars, or confidence intervals (lines 269, 303). Since margins over DAPS are often <1 dB and sometimes <0.5 dB, it is unclear whether the reported improvements are significant or within sampling noise.

5. **Baseline inconsistencies in Table 1.** DPIR is listed as a baseline (line 295) but never appears in any table. DDPM appears in the Gaussian blur table (line 352) but is not listed as a baseline. Several baselines (DDRM, DiffPIR, RED-diff, DCDP) are absent from the motion deblur section, making cross-task method rankings difficult to compare.

6. **The decay window W is never specified.** The σ schedule σ^{(k)} = max(0.1, 10 − (10−0.1)·k/W) depends on W, and K = W+10 depends on it too (line 297). Without W, the exact σ trajectory and total iterations cannot be reproduced.

7. **The x-subproblem convergence criterion is heuristic.** The inner loop solves (7a) with up to 1000 Adam iterations and stops when "loss increases more than Δ_tol consecutively for 3 iterations" (line 297). This conflates a loss increase with convergence and may terminate prematurely during oscillation.

### Trivial
None.

## Nice-to-Haves

- Provide evidence (even on a simplified distribution) that J=10 Langevin steps approximately mix, or present the relaxed analysis (Appendix E.2) in the main text.
- Align the practical σ schedule with the theory (e.g., run an experiment where σ decays to 0) or explicitly discuss why the σ→0 condition is not practically necessary.
- Quantify the total NFE per image and wall-clock time for Ours-tweedie, Ours-ode, and baselines.
- Add standard deviations or confidence intervals to Table 1.
- Specify W numerically.
- Add a quantitative ablation plot of PSNR vs. number of DC steps J (the current ablation in Fig. 5 is qualitative only).

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Table inconsistencies - PMC appears twice":** The PMC duplication in the raw text (lines 324–325, 339–340, 355–356, 363–365) is likely a PDF-extraction parser artifact (empty rows following entries). Not a paper error.
- **"Section 4 is dense and hard to follow":** A stylistic presentation concern, not a substantive weakness.
- **"DiffPIR formulation is garbled":** Parser artifact, not a paper error.
- **"Phase retrieval results poor across all methods":** The reviewer acknowledges this is not a weakness of the proposed method.
- **"Adaptive step-size less practical":** The authors already acknowledge this in their limitations section (line 379).
- **"Convergence holds under idealized conditions" (overlap with Major 1 and 2):** Already captured above.
- **"Inner subproblem convergence criterion suspect":** Merged into Minor 7 above.

## Novel Insights

None beyond the paper's own contributions. The review confirms that the AC-DC denoiser is a principled solution to a genuine problem, but reveals a non-trivial gap between the theoretical convergence conditions (σ→0, stationary Langevin distribution) and the practical algorithm (σ capped at 0.1, J=10 steps). This gap is common in PnP papers that extend theory from idealized settings to practical heuristics, but it is more consequential here because "convergent" features in the title.

## Suggestions

1. Report NFE count and wall-clock time per image for all methods.
2. Add standard deviations or confidence intervals to Table 1.
3. Either run experiments with σ decaying to 0 (to match the theory) or explicitly discuss the gap and argue why σ=0.1 is effectively negligible for the ball-convergence result.
4. Add a quantitative ablation showing PSNR/LPIPS as a function of DC steps J.
5. Specify W; add DPIR results; ensure consistent baseline coverage across all tasks.

## Score and Decision

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/HXjXPQU3yJ.md (PnP-ADMM Prior Mismatch) | 6.25 | R1, R2 | Yes | Closest topical match: PnP-ADMM + convergence. Was rejected due to presentation/scope issues; this paper has more substantive theory-practice gap but broader experiments. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/x7d1qXEn1e.md (Restoration Network as Implicit Prior) | 6.25 | R2 | Yes | Similar structure (method + theory + experiments). Accepted with concerns about unfair comparisons; this paper has a more principled method but a more central theory-practice gap. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/66arKkGiFy.md (PnP-ULA Posterior Sampling) | 5.75 | R1, R2 | Yes | PnP theory with mismatched models. Weaknesses about incremental contributions and unclear practical implications; this paper's weaknesses are more central. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Z9Odi09Rv9.md (Fast Diffusion Solvers) | 4.75 | R1 | Yes | Diffusion inverse solver with methodological concerns about Tweedie formula usage. Lower score reflects methodology issues. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/dAavOuxZvo.md (VIPaint) | 3.00 | R1 | No | Lower-scored diffusion inverse solver. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/W4djmqKZC6.md (Pixel-Aware Diffusion) | 3.00 | R1 | No | Lower-scored diffusion method. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/6EUtjXAvmj.md (Variational Diffusion Posterior Sampling) | 8.00 | R1 | No | Higher-scored diffusion inverse solver; accepted. |

**Round 1 bracket:** 4.5–6.5. The paper has genuine contributions (principled AC-DC denoiser, first convergence theory for score-based ADMM-PnP) but a substantive gap between what the theory proves and what the algorithm does.

**Round 2 narrowing:** Against the PnP-ADMM anchor (6.25), this paper's most negative weakness (σ schedule gap, favorability -0.34) is less severe than the anchor's worst (-4.08, shallow related work), and its experiments are broader. But the σ schedule gap is *substantively* more central to the paper's core claim. Against the Restoration Network anchor (6.25, Accept), the reviewed paper has a more novel methodological contribution but a more concerning theory-practice gap. The PnP-ULA anchor (5.75, Accept) has similar-quality weaknesses but less central to its claims.

**Final placement:** The paper's strengths (favorability 12–13) are on par with anchor papers scoring 5.75–6.25. Its most damaging weakness (σ schedule gap, favorability -0.34) is less negative than the anchors' worst items but strikes closer to the paper's core claim. Balancing these, the paper sits near the low end of the 5.5–6.25 band. The paper would benefit from addressing the theory-practice gap and reporting computational costs.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>