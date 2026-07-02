Here is the final consolidated review.

## Summary
This paper proposes PI-CCA, a replay-free continual learning method for vision-language models that preserves the spectral and subspace structure of canonical correlation analysis (CCA) between images and text, augmented with a prompt-invariance mechanism via projector averaging. The key idea is to treat forgetting as alignment-geometry drift rather than degradation of proxy quantities (logits, similarities). Across four benchmarks (MTIL, X-TAIL, VLCL, ConStruct-VL), the method achieves state-of-the-art performance among replay-free approaches and even surpasses a synthetic-replay method on VLCL.

## Strengths

1. **Principled reframing of forgetting.** The paper's core conceptual move — treating forgetting as alignment-geometry drift rather than matching proxy quantities (logits, similarities, parameters) — is genuinely insightful and well-articulated in Sections 1 and 3.2. If the method holds, this reframing has lasting value beyond the specific implementation.

2. **Comprehensive evaluation across four benchmarks.** The paper evaluates on MTIL (11-domain classification), X-TAIL (task-agnostic classification), VLCL (image-text retrieval), and ConStruct-VL (structured concept matching) — covering multiple task formats. The inclusion of task-order sensitivity (20 random orders, Fig. 5) and a scale/efficiency Pareto analysis (Fig. 2) goes beyond what most VL-CL papers provide.

3. **Empirical SOTA among replay-free methods.** The results in Tables 1 and 2 show consistent improvements over strong contemporary baselines (C-CLIP, MG-CLIP, Proxy-FDA, LADA, DIKI, RAIL, etc.). On VLCL, Pi-CCA even surpasses GIFT, a method that uses diffusion-generated synthetic replay, without storing or generating any data.

4. **Clean ablations supporting the design.** Table 3 isolates each component (spectral term, subspace term, prompt invariance, EMA rates, sketch type) and the performance drops are consistent with the method's motivation. The two largest drops come from disabling the spectral or subspace terms, which is exactly what the geometry-first thesis predicts.

5. **Prompt invariance mechanism.** The projector-averaging approach (Eq. 5-6, 11) is a natural extension of the CCA certificate idea, and the stress test (Fig. 4) shows it provides measurable robustness under both in-distribution and out-of-distribution prompt perturbations.

## Weaknesses

### Fatal
None.

### Major

1. **Figure 3 reports implausible correlation coefficients.** The caption reports Pearson r=1.00 and Spearman ρ=1.00 for two of four subplots, and ρ=1.00 for all four, while simultaneously describing "realistic scatter." A correlation of exactly 1.00 is mathematically impossible in the presence of scatter. Even if these values are rounded (e.g., 0.9998→1.00), reporting them to only two decimal places without disclosure of the number of data points is misleading. The paper uses this figure as central evidence that "preserving CCA geometry predicts retention rather than being a coincidental regularizer" (Fig. 3 caption). The authors must (a) report correlations to at least three decimal places, (b) disclose the number of data points in each scatter plot, and (c) include confidence intervals (e.g., bootstrap). As presented, the correlation evidence is not credible and undermines the paper's supporting argument for its conceptual claim.

### Minor

1. **No variance estimates for the primary classification results (Table 1).** Table 1 reports MTIL and X-TAIL results as point estimates, while Table 2 reports ± intervals for VLCL and ConStruct-VL. This inconsistency is notable. Without variance estimates, readers cannot assess whether Pi-CCA's margins over the second-best method (e.g., 76.8 vs. 75.2 Avg on MTIL) are statistically reliable. The task-order sensitivity analysis (Fig. 5) uses 3 seeds, suggesting seed-level variation exists. The authors should report mean ± std for Table 1 as well.

2. **Potential circularity in the geometry→performance correlation.** The sweep in Figure 3 varies settings that directly change the optimization objective (certificate size k/h, disabling spectral/subspace losses, etc.). In these cases, geometry drift and performance drop are consequences of the same intervention rather than the former causing the latter. This weakens the causal interpretation the paper draws ("predicts retention rather than being a coincidental regularizer"). A cleaner test would induce geometry drift through external means (e.g., data order, noise injection) while holding the optimization fixed. The correlation itself may be real, but its causal interpretation is overstated.

3. **Zero-shot PD metric mentioned but missing from main results tables.** The evaluation protocol (Section 4.1) states the paper reports "performance drop (PD) on a held-out zero-shot suite," but PD does not appear in Tables 1 or 2. It appears only in the prompt invariance stress test (Fig. 4). While the Transfer metric in Table 1 already captures zero-shot accuracy on unseen domains, reporting PD as claimed would strengthen the zero-shot retention narrative.

4. **No discussion of limitations.** The conclusion (Section 5) does not discuss limitations. The paper would benefit from acknowledging settings where the method might struggle (e.g., very long task streams where EMA-based certificate refresh blurs old knowledge, or scenarios where the linear CCA assumption is a poor fit).

### Trivial

1. The scale/efficiency Pareto analysis (Fig. 2) sweeps k and h while keeping other settings fixed. Optimal k/h likely interact with EMA rates, λ weights, and LoRA rank, so the "robust Pareto ridge" conclusion may not generalize to all configurations. A brief caveat would be helpful.

## Nice-to-Haves

- A bootstrap confidence interval for each correlation in Figure 3 would be far more informative than the current point estimates.
- Reporting zero-shot PD alongside the main metrics in Tables 1 and 2 would make the zero-shot retention claim more tangible.
- Mentioning limitations in the conclusion, even briefly, would strengthen the paper.

## Removed Points

These points are flagged to be removed; treat them with caution:

1. **Concern about code not being released due to "ongoing commercial use."** Removed because penalizing a paper for not releasing code under anonymous review is against ICLR norms; the paper commits to open-sourcing upon acceptance.

2. **Claim that the Introduction asserts prior methods "permit slow drift of alignment geometry" without evidence.** Removed because this is a thesis statement and motivation for the paper's approach, not an empirical claim that requires evidence at that point.

3. **Criticism that Eq. (12)/line 129 formula for M^{(t)} is garbled/incoherent.** Removed per hard rules: the apparent character corruption (e.g., Σ→S) and structural distortion are formatting artifacts from PDF extraction, not author errors. The original submission does not have these issues.

4. **General speculation about missing appendix content.** Removed because the appendix was stripped by the PDF parser.

5. **Formatting/style nitpicks.** Removed as parser artifacts.

## Novel Insights

The harsh reviewer's observation about the potential circularity in the correlation analysis is genuinely insightful. The sweep varies settings that directly change the optimization objective (certificate size, disabling spectral/subspace losses), meaning both drift and performance drop are consequences of the same intervention. This highlights that Figure 3 is better interpreted as a sanity check (the method behaves as expected under controlled perturbations) rather than causal evidence that geometry drift drives forgetting. This distinction sharpens what the paper can legitimately claim from this analysis and suggests a cleaner experimental design for future work.

## Suggestions

1. **Fix Figure 3.** Report correlations to three decimal places, disclose the number of data points, add bootstrap confidence intervals, and temper the causal language in the caption.
2. **Add variance estimates to Table 1.** Run 3+ seeds and report mean ± std, consistent with Table 2.
3. **Include PD in main tables** or clarify where zero-shot retention is evaluated beyond the stress test.
4. **Add a limitations paragraph** to the conclusion.

## Score and Decision

The paper makes a genuine conceptual contribution by reframing forgetting as alignment-geometry drift and provides a well-designed method that achieves SOTA results across four benchmarks with clean ablations. The main weakness is the implausible correlation coefficients reported in Figure 3, which undermine the supporting analysis for the conceptual claim. However, this issue does not invalidate the primary empirical results (Tables 1 and 2), which are comprehensive and independently demonstrate the method's effectiveness. The paper's core contributions are solid, and the problematic figure is fixable with proper reporting. The other issues (missing variance estimates, missing PD metric, no limitations) are addressable.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>