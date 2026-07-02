## Summary

This paper identifies two coupled limitations of Logit Adjustment (LA) for Long-Tailed Semi-Supervised Learning (LTSSL): (1) naive frequency counting inflates head-class prevalence by ignoring sample redundancy, and (2) the overall adjustment strength τ is treated as a fixed hyperparameter despite being sensitive to the estimated distribution. The authors propose CoLA, which co-designs the class-wise and overall LA components — DDDE uses effective rank of feature representations for de-duplicated distribution estimation, and LMC meta-learns τ on a proxy validation set. The paper includes a generalization bound and experiments on 4 benchmarks across 6 distribution types.

## Strengths

1. **Problem diagnosis is insightful and empirically motivated.** The paper correctly identifies that existing LA methods suffer from a coupled two-fold problem — redundancy-inflated frequency estimates and fixed τ — and argues they are interdependent. Figure 1b directly shows the optimal τ varies unpredictably with distribution characteristics, motivating the co-design framing.

2. **DDDE is a well-motivated and validated solution.** Using effective rank of feature representations to estimate de-duplicated class frequencies is a sensible adaptation of the effective-number concept (Cui et al., 2019). Table 5 shows DDDE achieves lower L₂ distance to the true distribution than MCA and NWGMA across all 10 configurations on CIFAR-10/100-LT, providing clean evidence of improved distribution estimation.

3. **Strong empirical results on most benchmarks.** CoLA achieves the highest reported accuracy on CIFAR-100-LT (all 5 distributions), STL-10-LT (all 4 settings), and SIN-127 (both image sizes), with margins typically >1 percentage point on the more challenging CIFAR-100-LT (e.g., 59.04 vs 57.58 for CON). The ablation study (Table 4) shows both DDDE and LMC contribute positively, and the full model outperforms either alone.

4. **Broad and systematic distribution coverage.** Evaluation spans 6 distribution types (consistent, uniform, reversed, middle, head-tail, and unknown on STL-10) across 4 benchmarks, which is more thorough than prior work relying on a small set of pre-defined anchor distributions.

## Weaknesses

### Fatal
None.

### Major

1. **Claim about SOTA on CIFAR-10-LT CON is contradicted by the paper's own data.** Section 6.2.1 states: "Our proposed CoLA achieves the highest accuracy across all five distributions on both the CIFAR-10-LT and CIFAR-100-LT datasets." However, Table 1 shows that on CIFAR-10-LT with the consistent (CON) distribution, ADSH (83.35±3.86) and CPE (82.59±3.18) both outperform CoLA (81.87±2.70). The paper also incorrectly bolds CoLA as the sole top performer in this column. The abstract, introduction, and conclusion all assert "new state-of-the-art performance" without qualification. This is a factual inaccuracy in a central claim that affects the paper's headline finding and requires correction.

2. **Unexamined change from logarithmic to linear LA adjustment.** The paper replaces the standard post-hoc LA formulation `-τ·log P̂(y)` (Eq. 1) with `-τ·p` (Eq. 2, lines 97–99), where **p** is the linear class-frequency vector. These have fundamentally different scaling behavior: for a tail class with P̂(y)=0.001, the log penalty gives +6.9τ while the linear penalty gives -0.001τ; for a head class with P̂(y)=0.5, the log penalty gives +0.69τ while the linear penalty gives -0.5τ. The paper provides a brief rationale citing (Mor & Carmon, 2025) but conducts no ablation or empirical comparison of the two formulations. Since the paper's central thesis is about "co-designing the class-wise and overall LA components," the functional form of the class-wise adjustment is a core design choice. Without isolating this change, the reader cannot attribute gains to the claimed innovation versus a simple change in functional form.

### Minor

3. **SIN-127 results lack variance estimates.** Table 3 reports only point estimates (no standard deviations or confidence intervals), unlike the CIFAR and STL-10 tables. The margins over the runner-up are modest (24.18 vs ABC's 23.66 for 32×32; 37.49 vs ACR's 36.28 for 64×64), making it impossible to assess whether these differences are meaningful.

4. **Meta-learning optimization details are underspecified.** The main text does not specify the optimization procedure for τ: number of gradient steps, learning rate, update frequency (every epoch or once after warm-up). These are deferred to the appendix, which is stripped. Similarly, the criterion for when DDDE becomes active (how many confident samples per class are needed before computing erank) is not specified.

5. **Figure 2 lacks quantitative before/after comparison.** The visualization shows pseudo-label accuracy over epochs and mentions improvements are "most pronounced" on some distributions and "modest" on others, but provides no numerical comparison of accuracy before and after the τ-switch.

### Trivial
None.

## Nice-to-Haves
- Ablate the linear vs. logarithmic adjustment formulation to isolate the contribution of this design choice.
- Add a brief limitations discussion: the method relies on confident pseudo-labels for tail classes early in training, and STL-10 contains OOD samples — how does CoLA handle these scenarios?
- Provide per-setting breakdowns for CIFAR-10-LT CON to clarify where CoLA wins and where it does not within the aggregated average.

## Removed Points
These were flagged in the input review but removed per the filtering rules:
- **"Theoretical contribution is standard"**: The paper explicitly acknowledges "its form is general to many domain adaptation scenarios" (line 135). For an empirical methods paper, a modest theoretical grounding is not a weakness.
- **"Assumption 4 is circular"**: The paper acknowledges this limitation (line 125). The bound is framed as motivation, not proof.
- **"Convexity analysis and DDDE warm-up details deferred to appendix"**: These refer to the stripped appendix. Per instructions, weaknesses about missing appendix content are removed.
- **"K^{(K+1) mod 2} notation issue"**: Parser artifact, removed per instructions.
- **"No failure cases or limitations discussed"**: Generic expectation, not a specific weakness.
- **Generic or sycophantic strengths from the input review** were dropped (e.g., "the paper addressed an important problem").

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Correct the CIFAR-10-LT CON claim in Section 6.2.1 to accurately reflect that CoLA achieves top performance on CIFAR-100-LT across all distributions and on 4 of 5 CIFAR-10-LT distributions, noting the CON exception. Fix the bold marking in Table 1 for the CON column.
- Add an ablation comparing linear LA (`-τ·p`) against the standard logarithmic formulation (`-τ·log P̂(y)`) with all other components fixed.
- Include standard deviations for SIN-127 results in Table 3.
- Specify meta-learning hyperparameters (τ learning rate, gradient steps, update frequency) in the main text or a dedicated table.

## Score and Decision

The paper makes a genuine contribution by identifying and addressing the interaction between class-wise and overall LA components, and the empirical results are strong across most settings. However, two substantive issues — a factual overclaim in the main experimental result and an unexamined change to the core LA formulation — prevent a clean acceptance. Both are fixable with corrections and additional experiments.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>