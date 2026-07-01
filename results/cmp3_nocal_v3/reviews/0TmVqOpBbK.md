## Summary

This paper extends Chinchilla-style scaling laws to incorporate architectural factors—hidden size and the mlp-to-attention ratio—and introduces a two-step conditional framework for identifying architectures that balance inference efficiency with accuracy. The authors train over 200 models from 80M to 3B parameters (5× Chinchilla token budget), fit the proposed conditional scaling law, and show that the resulting models outperform LLaMA-3.2 architectural configurations under the same training budget, with up to 2.1% higher average accuracy and 42% greater inference throughput via a combined architecture + GQA search.

## Strengths

- **Systematic multi-scale empirical study.** Training over 200 models across 80M, 145M, 297M, 1B, and 3B with controlled variations of hidden size and mlp-to-attention ratio represents a substantial experimental effort. The progressive validation strategy (fit on smaller → predict larger) is a principled test of extrapolation.

- **Clean conceptual framing.** The two-step conditional approach—referencing the Chinchilla-optimal loss and calibrating architecture effects relative to it—avoids the difficulty of fitting a single unified law across architectural and scaling dimensions simultaneously. The multiplicative and additive forms in Eq. (3) are transparent and straightforward to fit.

- **Practical and reproducible comparison.** All models including LLaMA-3.2 architecture baselines are trained from scratch on Dolma-v1.7 under the same training budget (100B tokens, 5× Chinchilla). This eliminates the data-distribution confound that would arise from using official released checkpoints. The paper explicitly states in Section 4: *"We train decoder-only LLaMA-3.2 style transformers with N_non-embed in {80M, 145M, 297M, 1B, 3B}"* — confirming the baselines are retrained by the authors.

- **U-shaped relationships are empirically grounded.** Figures 4 and 5 document a genuine interior optimum for both hidden size (normalized by √N) and mlp-to-attention ratio, with consistent patterns across scales. This is a useful finding for practitioners.

## Weaknesses

### Fatal
None.

### Major
None. All issues are addressable in revision and do not threaten the paper's core empirical contributions.

### Minor

- **The 42% throughput gain conflates architecture changes with GQA increases, and this is not decomposed.** The "Surefire" models (which achieve the headline throughput numbers) increase GQA from 4→9 (1B) and 3→7 (3B) relative to LLaMA-3.2. Higher GQA is known to improve throughput nearly cost-free in accuracy (Ainslie et al., 2023). The paper's throughput comparison compares Surefire (high GQA + optimized d_model/r) vs. LLaMA-3.2 (low GQA + LLaMA architecture). The "Panda" models have the same GQA as LLaMA-3.2 but their throughput is not reported, so the reader cannot determine how much of the 42% gain comes from the scaling-law-guided architectural changes versus the GQA increase. The paper frames the throughput gains as a product of the complete search framework (Algorithm 1), which is technically accurate, but the lack of decomposition makes it easy to over-attribute the gains to the scaling law. **Fix:** Report throughput for at least one scale under four conditions: (1) LLaMA arch + LLaMA GQA, (2) LLaMA arch + high GQA, (3) Panda arch + LLaMA GQA, (4) Panda arch + high GQA.

- **The fitted coefficients shift with model scale, weakening the "scaling law" framing.** The paper transparently documents this (Section 5.1): a₁ shifts from 0.0974 (fitted on 80M–1B) to 0.238 (fitted on 1B-only) when predicting 3B; the predicted optimal r shifts from 1.055 to 1.229; and the Spearman correlation for 80M–1B→3B prediction is only 0.50. The paper acknowledges that *"the law's coefficients shift with model size."* This means the proposed functional form does not capture scale-invariant behavior in the way Chinchilla-style power laws do—it is more accurately described as an interpolation procedure that works best when fitting data at scales close to the target. The paper should either reframe the contribution as "architecture-aware loss prediction at nearby scales" rather than "scaling laws," or present evidence that the coefficient drift follows a predictable pattern that could itself be modeled.

- **The separability assumption (d_model and r effects factorize) is stated but not validated in the main text.** Equation (3) assumes the effects of d_model and r on loss are separable, meaning the optimal d_model does not depend on r and vice versa. The paper acknowledges this assumption (line 148) and references Appendix J for non-separable formulations that *"do not provide superior predictive performance."* However, the visual evidence in Figures 4 and 5—showing loss curves for different values of r (Figure 4) and different values of d_model (Figure 5)—raises the question of whether the optima shift interactively. Without seeing the actual plots or the appendix results, the reader cannot evaluate whether the interaction is truly negligible. At minimum, the main text should report quantitative evidence (e.g., variance explained by interaction terms) rather than deferring entirely to a stripped appendix.

- **All experiments use a 100B-token (5× Chinchilla) training budget, which is far smaller than the 2T+ tokens used for models like LLaMA-3.2.** The paper's central finding—that r≈1 (balanced MLP/attention) outperforms r≈4.8 (LLaMA-style)—may be specific to this token budget. The optimal architecture for training at 2T+ tokens could shift toward more MLP parameters as the model has more data to memorize in the MLP layers. The paper acknowledges the restriction to pre-training and models ≤3B in its Limitations section but does not discuss how the token budget might interact with the optimal r. A brief discussion of this confound would help readers gauge the generality of the findings.

- **No throughput decomposition for same-GQA models (Panda vs. LLaMA).** As noted above, the accuracy comparison uses Panda (which has the same GQA as LLaMA-3.2), but the throughput comparison uses only Surefire (which has higher GQA). Reporting Panda throughput would help isolate the scaling law's contribution to efficiency.

### Trivial
- "Underexplored" in the introduction overstates the gap, given existing work on architecture-aware scaling (Sardana et al., 2023; Bian et al., 2025). Minor wording issue.

## Nice-to-Haves
- Report accuracy with confidence intervals or standard deviations over multiple runs, since the reported gains are small (0.6–2.1%).
- Release the full loss-architecture dataset from the 200+ models to enable community follow-up work.
- Include a discussion of how the optimal r might vary with the token budget, since the experiments use a fixed 5× Chinchilla schedule.

## Removed Points
- **"Unfair comparison to LLaMA-3.2 baselines"** — Removed because the paper clearly states (Section 4): "We train decoder-only LLaMA-3.2 style transformers with N_non-embed in {80M, 145M, 297M, 1B, 3B}." All models including LLaMA-3.2 baselines were trained by the authors on Dolma-v1.7 under identical conditions. The abstract's "under the same training budget" and the loss values in Table 1 (which would differ if using official checkpoints) confirm this. The phrase "open-weight LLaMA-3.2-1B baseline configs" (Section 5.1) refers to the architecture configuration, not the released weights. This criticism is factually incorrect when checked against the paper.
- **"Scaling law is just an empirical fit, not a true scaling law"** — Removed as a terminological nitpick. The paper's functional forms are empirically motivated, consistent with how Chinchilla-style scaling laws are fitted. The contribution is clear regardless of the label.
- **"Derivation is ad hoc"** — Removed. The functional forms (a₀ + a₁ log x + a₂/x) are explicitly chosen to model U-shaped curves, and the authors test both multiplicative and additive calibrations. This is a standard empirical modeling approach.
- **"No confidence intervals"** — Removed. Single-run evaluation on large-scale pre-training benchmarks is standard practice in this setting; requesting error bars for 200+ models across 5 scales is not a reasonable expectation.
- **"Raw data not released"** — Removed. The paper may release the dataset post-publication; this is not a valid criticism of the submitted work itself.
- **Criticisms about missing appendix content or incomplete formatting** — Removed per parser-stripping rules.

## Novel Insights

The harsh critic correctly identifies that the throughput gains are not decomposed between architecture effects and GQA effects, and that the coefficient instability weakens the "scaling law" framing. However, the critic's main structural concern—that the LLaMA-3.2 comparison is unfair—is refuted by the paper's clear statement that all models (including baselines) were retrained under identical conditions. The paper's most interesting tension is between its genuine empirical contribution (the U-shaped relationships and the practical method for finding good architectures at nearby scales) and the somewhat inflated "scaling law" terminology for what is more accurately an interpolation procedure. Separating the throughput decomposition cleanly would significantly strengthen the paper.

## Suggestions

1. Report throughput for Panda (same GQA as LLaMA) vs. LLaMA to isolate the architecture-only contribution to efficiency.
2. In the main text, provide quantitative evidence about the separability assumption (e.g., variance explained by interaction terms in the non-separable fits from Appendix J).
3. Reframe the contribution more precisely: "architecture-aware loss prediction" rather than "scaling laws," or explicitly address why coefficient drift across scales is acceptable given the practical goal.
4. Add a paragraph discussing how the optimal mlp-to-attention ratio might depend on the token budget, since all experiments use 100B tokens.

## Score and Decision

This is a solid empirical paper with a practical contribution. The experimental effort (200+ models across 5 scales) is substantial, the conditional framework is well-motivated, and the finding that balanced MLP/attention ratios (r≈1) outperform heavily MLP-dominated architectures (r≈4.8) at 100B-token budgets is genuinely useful. The weaknesses are all addressable: the throughput decomposition can be added, the separability assumption can be better validated in the main text, and the "scaling law" framing can be calibrated. No criticism threatens the paper's core claims.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>