## Summary

This paper introduces Neon, a post-hoc parameter merge method for improving generative models. Given a base model trained on real data, Neon (i) briefly fine-tunes it on its own synthetic samples (inducing degradation), then (ii) extrapolates *away* from the degraded weights via \(\theta_{\text{Neon}} = (1+w)\theta_r - w\theta_s\). The paper proves that mode-seeking inference samplers create anti-alignment between synthetic and real-data gradients, which this negative extrapolation exploits to reduce true data risk. The method is evaluated across diffusion, flow matching, autoregressive, and few-step models on ImageNet, CIFAR-10, and FFHQ, consistently improving FID with less than 1% additional compute.

## Strengths

1. **A genuinely counterintuitive and elegant insight.** The idea that self-training degradation is not random noise but a structured signal whose *reversal* improves the model is well-motivated and clearly illustrated with the 2D Gaussian toy example (Figure 2) before the theory formalizes it. This conceptual contribution is striking and novel.

2. **Remarkable simplicity with strong empirical results.** The method is a single parameter merge with no auxiliary models, inference modifications, or iterative training. Headline results are genuinely impressive: xAR-L on ImageNet-256 from FID 1.28 → 1.02 (0.36% extra compute); near-optimal results with only 1k synthetic samples (xAR-L: 1.05 FID); and 4-step IMM + Neon nearly matching 8-step base quality (FID 1.69 vs. 1.98). These results are verified in the paper text (lines 185, 209, 233).

3. **Comprehensive theoretical grounding.** The paper proves two theorems establishing that mode-seeking samplers (temperature < 1, top-k, CFG) induce anti-alignment between synthetic and real data gradients (Theorem 2), and that this anti-alignment guarantees Neon reduces risk under stated assumptions (Theorem 1). The connection between a specific inference property (monotone reweighting of log \(p_\theta\)) and the method's success is clean and falsifiable.

4. **Thorough ablation studies.** The paper systematically checks: does the base model need to be near-optimal? (Figure 9 — no, works across quality spectrum); does the synthetic data need to be high-quality? (Figure 10 — robust to CFG scale 1–3); is the signal transferable across architectures? (Figure 8 — yes). The CIFAR-10C null result (no improvement from corrupted real images) is a well-designed negative control that strengthens the causal claim.

5. **Universality across diverse model families.** Results on diffusion (EDM), flow matching, autoregressive (xAR, VAR), and few-step (IMM) models with consistent improvements provide strong evidence the mechanism is general and not an artifact of a specific architecture or training procedure.

## Weaknesses

### Fatal

None.

### Major

None. The paper's core contributions (the method, its theoretical grounding, and its broad empirical validation) are sound and well-supported.

### Minor

1. **No uncertainty quantification for FID results.** All FID, Precision, and Recall values are reported as point estimates with no standard deviations, confidence intervals, or multi-seed averaging. This is most consequential for the SOTA claim (xAR-L + Neon: FID 1.02 vs. UCGM's 1.06 — a margin of 0.04 FID units). While single-run FID evaluation is standard practice in this field, a SOTA claim with this narrow a margin would be strengthened by variance estimates or multiple seeds. The non-monotonic behavior in some curves (e.g., FID improving then degrading with budget) would also benefit from error bars to distinguish genuine trends from noise. This does not invalidate the paper's broader claims but is worth addressing.

2. **Precision-recall trade-off identified but its practical significance not fully characterized.** The paper transparently shows that Neon trades precision for recall (precision monotonically decreases with \(w\); recall follows an inverted-U). However, the paper does not provide human evaluation or side-by-side comparison (beyond the single Figure 1 example) to assess whether the precision drop is perceptually acceptable at the FID-optimal point. Since FID is sensitive to both precision and recall, the net improvement is genuine by the metric, but the practical implications of the trade-off could be discussed more thoroughly. This is a minor omission in an otherwise thorough empirical characterization.

3. **Robustness to base model quality tested only on CIFAR-10, not ImageNet.** The test of whether Neon works when the base model is not near-optimal (Figure 9) is conducted on CIFAR-10 EDM models with varying training set sizes. While this is a reasonable test, replicating it on ImageNet (where the headline SOTA result lives) would strengthen the claim that the small-error condition is robust in the settings that matter most for the paper's strongest results. The CIFAR-10 experiment supports the claim but is a limited proxy.

### Trivial

None.

## Nice-to-Haves

- **Add variance reporting or multiple seeds for the xAR-L SOTA result** (FID 1.02). Even 2–3 seeds reporting mean ± range would substantially solidify the claim.
- **Replicate the base-model-quality robustness test (Figure 9) on ImageNet** with xAR models trained on varying-size subsets.

## Removed Points

These points were raised in the input review but are excluded per the filtering rules (see justification for each):

- *"The SOTA claim is under-supported in the main text because the comprehensive comparison is deferred to the appendix."* **Removed.** The paper explicitly states "For a comprehensive comparison... please see Table A.1" (line 179). The appendix exists in the original submission; deferring full comparisons to the appendix is standard practice. The main text provides the specific SOTA baseline it surpasses (UCGM's 1.06).
- *"No ablation on the choice of fine-tuning learning rate."* **Removed.** Details are deferred to Appendix C, which exists in the original submission. The paper states "the original training recipe at reduced learning rate (see Appendix C for details)" (line 179).
- *"No discussion of potential failures or regimes where Neon might not work."* **Removed.** The paper already discusses the complementary regime where interpolation (not extrapolation) is indicated (diversity-seeking samplers, line 171), the U-shaped performance curves with budget, and the conditions under which the theory's assumptions may not hold. More exhaustive failure-mode discussion is a nice-to-have, not a missing element.
- *"The theory's small-error assumption test shows only modest improvements."* **Weakened from the reviewer's framing.** The claim being tested in Figure 9 is that Neon works across model quality levels, not that the absolute improvement is large. The paper demonstrates that Neon compensates for a 40% reduction in training data, which supports the robustness claim. The legitimate residual concern (test not replicated on ImageNet) is retained as Minor weakness #3 above.

## Novel Insights

The reviewer's observation that the paper's mechanism trading precision for recall could be perceived differently by practitioners is worth noting, but the paper itself already identifies this dynamic clearly. The broader insight that stands out across the reviews is that Neon's success depends on the specific interaction between *inference-time sampling choices* (mode-seeking via temperature, CFG, top-k) and *training dynamics* — a coupling that the paper's theoretical framework (Theorems 1–2) formalizes cleanly. The reviewer's framing of the SOTA-claim-evidence gap raises a valid methodological point about the field's norms for uncertainty reporting, but this is a community-wide issue rather than a paper-specific flaw.

## Suggestions

1. For camera-ready, add a sentence or a small table in the main text reporting the absolute GPU-hours for the base training runs (to contextualize the "0.36% additional compute" claim with concrete numbers).
2. Add a brief discussion of the precision drop's practical significance — e.g., whether a human preference study would align with the FID improvement at the optimal \(w\).
3. Consider including multi-seed results for the xAR-L + Neon experiment to address the SOTA-claim-evidence concern non-specifically.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>