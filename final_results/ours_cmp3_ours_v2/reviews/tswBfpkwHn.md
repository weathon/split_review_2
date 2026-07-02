## Summary

This paper provides the first theoretical analysis of training dynamics and in-context learning (ICL) generalization for one-layer Mamba models on binary classification tasks with additive outliers. The authors derive a closed-form expression for one-layer Mamba (linear attention + nonlinear gating), prove convergence and generalization bounds, and compare with linear Transformers. Key results: Mamba's gating enables robustness to outlier fractions approaching 1 (vs. 1/2 for linear Transformers); the linear attention selectively weights same-pattern examples; the gating suppresses outliers and imposes exponential locality bias. Synthetic experiments validate the predictions.

## Strengths

- **First theoretical analysis of Mamba's training dynamics for ICL.** Prior work (Li et al., 2024b; 2025b) analyzed global minima or simplified architectures (H3, gated linear attention), not training dynamics. This fills a clear gap in the literature.

- **Clean apples-to-apples comparison isolating gating effects.** By noting that setting the gating function \(G=1\) in Equation (3) recovers a linear Transformer, the paper attributes behavioral differences to the nonlinear gating mechanism alone — a methodologically sound design.

- **Concrete mechanistic characterization.** Corollaries 1 and 2 go beyond existence guarantees to describe *how* the model works: attention selects same-pattern examples (Corollary 1), gating suppresses outliers and imposes exponential locality bias (Corollary 2). The synthetic experiments in Figures 3 and 4 directly verify these predictions.

- **Sharp qualitative distinction (\(\alpha<1/2\) vs. \(\alpha\to 1\)).** Theorems 2 and 4 establish a nontrivial theoretical result: the analyzed linear Transformer provably fails when outlier fraction exceeds 1/2, while Mamba can tolerate fractions approaching 1 under appropriate conditions.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **The analyzed model is a simplified gated linear RNN, not full Mamba.** The paper derives Equation (3) from the one-layer Mamba recurrence with \(A=-I\) and uses only the last row of the gating matrix (\(\mathbf{w} = \mathbf{w}_{d_0}\)). This collapses the multi-dimensional selective gating of full Mamba (where each hidden dimension \(d_0\) has its own input-dependent gating vector) to a single scalar gating vector shared across all dimensions. While the derivation is mathematically valid and simplification is necessary for tractability, the paper's persistent framing as analyzing "Mamba" throughout (title, abstract, conclusion) oversells the connection. A more precise framing — e.g., "a one-layer gated linear RNN derived from Mamba" — would better match the evidence without diminishing the contribution. The paper acknowledges this briefly in the conclusion ("Although based on a one-layer Mamba structure") but does not discuss what architectural features are lost in the simplification.

2. **Test-time outlier condition is restrictive.** Theorem 2(a) requires test outliers to be positive linear combinations of training outliers (\(\sum_i \lambda_i \ge L > 0\)). This means completely novel outlier types orthogonal to *all* training outliers fall outside the guarantee. The paper mentions this condition (P1 in Section 3.1, Theorem 2(a)) but does not discuss how restrictive it is or compare it to alternative distribution-shift models (e.g., bounded-norm perturbations, adversarial examples). For a paper whose title prominently features "outliers" and "robustness," this limitation deserves a dedicated discussion.

3. **No statistical reporting in experiments.** Section 4 presents results (Figure 2, Table 1) without error bars, confidence intervals, or the number of independent trials. For comparisons involving classification accuracy on a log scale (\(10^{-4}\) to \(10^0\)) and a 6-percentage-point gap (Table 1: 99.73% vs. 93.68%), variance information is needed to assess whether reported differences are statistically meaningful.

4. **Ambiguous notation in Theorem 1.** Condition (iii) uses the notation \(\text{poly}(M_1^{\kappa_a})\). If \(\kappa_a\) is a scalar (outlier magnitude), then \(M_1^{\kappa_a}\) is not a polynomial in the usual sense (the degree would depend on a continuous parameter). The authors should clarify what is intended.

### Trivial
None.

## Nice-to-Haves

- Add variance reporting (error bars or confidence intervals) to all experiments.
- Test Mamba's ICL on completely novel outlier patterns (orthogonal to all training outliers) to probe how restrictive Theorem 2(a)'s condition actually is.
- Explicitly reframe the CQ failure mode (Table 1: Mamba 82.73% when outliers are closest to the query) as a *predicted limitation* of the exponential locality bias (Corollary 2(ii)), which would strengthen the narrative by showing the theory predicts both successes and failure modes.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Gating is not multiplicative across positions in actual Mamba"** — This is factually incorrect. Mamba's recurrence \(\mathbf{h}_i = \mathbf{h}_{i-1} \odot \hat{\mathbf{A}}_i + \ldots\) with \(\hat{\mathbf{A}}_i = \exp(\Delta_i A)\) creates multiplicative gating across positions through the hidden state. The product structure in Equation (3) follows directly from unrolling this recurrence. Removed as a misunderstanding of the architecture.
- **"Additional batch-size term for Mamba could be an artifact of the proof technique"** — Speculative claim about whether the difference in sufficient conditions reflects a genuine property or a proof artifact. The paper transparently compares sufficient conditions, which is standard practice. Removed as unsupported speculation.
- **"No comparison with softmax attention"** — Remark 6 explains the design choice (isolating gating effects requires comparing architectures that differ only by gating) and Appendix B.1 (cut by the parser) includes additional experiments with softmax attention. Removed as outside the paper's stated scope.
- **"Three-layer experiments not integrated with the theory"** — Section 4.2 explicitly uses 3-layer models to test whether the 1-layer theory's mechanistic predictions (Corollaries 1, 2) hold in deeper models. The paper's claim that the results "verify" the theory is a reasonable extrapolation. Removed as a misunderstanding.
- Generic strengths about "addressing an important problem" — removed as insufficiently specific.

## Novel Insights

The review surfaces a tension implicit but not fully articulated in the paper: the gating mechanism that enables Mamba's superior robustness to outlier *fraction* simultaneously creates a structural sensitivity to outlier *position* (the exponential locality bias of Corollary 2(ii)). This trade-off — robustness to the quantity of outliers vs. vulnerability to their proximity — is a genuinely interesting observation. The CQ result in Table 1 (Mamba 82.73% vs. Linear Transformer 93.96% when outliers are closest to the query) is not an unexplained failure but a direct consequence of Corollary 2(ii). Reframing it as such would strengthen rather than weaken the paper's narrative.

## Suggestions

1. Reframe the contribution around the analyzed model: "a one-layer gated linear RNN derived from Mamba" rather than simply "Mamba." Acknowledge what architectural features are simplified (multi-dimensional gating → single gating vector) and discuss whether the core results depend on the specific product structure of the gating.
2. Add error bars or confidence intervals to all experimental results.
3. Clarify the notation \(\text{poly}(M_1^{\kappa_a})\) in Theorem 1 condition (iii).
4. Discuss the restrictiveness of the test-time outlier condition (Theorem 2(a)) explicitly, including a comparison with alternative distribution-shift models.
5. Reframe the CQ failure mode in Table 1 as a predicted limitation of Corollary 2(ii) rather than a standalone empirical observation.

## Calibration

**Round 1 bracket:** [5.5, 7.0]

**Anchor papers considered:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/52XG8eexal.md` (State-space models can learn in-context by gradient descent) | 4.00 | R1 | Weaker: that paper's construction-based approach was criticized for limited novelty and poor connection to practice; the current paper provides training dynamics (harder) and a cleaner architectural comparison. Current paper is stronger. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/QFgbJOYJSE.md` (State Space Models are Provably Comparable to Transformers in Dynamic Token Selection) | 5.75 | R1 | Comparable: similar level of theoretical contribution and similar gap between analyzed model and practice. The current paper's experiments are more directly validating but lack variance reporting. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ikwEDva1JZ.md` (How Do Transformers Learn In-Context Beyond Simple Functions?) | 6.50 | R2 | Slightly stronger: more comprehensive experiments and probing analysis, cleaner connection from theory to mechanism. The current paper's comparison between architectures is cleaner but experiments are thinner. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/aKJr5NnN8U.md` (Toward Understanding In-context vs. In-weight Learning) | 6.50 | R2 | Slightly stronger: includes experiments on real LLMs and more comprehensive validation. The current paper's theoretical comparison is more architecturally precise. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/STUGfUz8ob.md` (When can transformers reason with abstract symbols?) | 7.60 | R1 | Stronger: more general theoretical result, cleaner experiments, stronger novelty signal. |

**Narrowing:** The current paper is clearly above the 4.00 (SSM-ICL-GD) paper but below top-tier theoretical works scoring 7.5+. It sits comfortably alongside other accepted SSM theory papers in the 5.75–6.5 range. The framing overreach and missing error bars are the main factors preventing a higher score, but the core theoretical contribution (first training dynamics analysis, clean architectural comparison, mechanistic characterization) is solid and novel.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>