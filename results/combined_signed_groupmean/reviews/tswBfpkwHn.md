Here is the consolidated final review.

## Summary
This paper provides the first theoretical analysis of the training dynamics of a one-layer Mamba model for in-context learning (ICL) with outliers. The key analytical contribution is Equation (3), which decomposes one-layer Mamba into a linear attention term and a nonlinear gating term with a product-of-sigmoids structure. Using this decomposition, the paper proves convergence guarantees (Theorem 1), characterizes how outlier fraction enters the bounds, and derives a sharp comparative prediction: Mamba can tolerate outlier fractions up to min(1, p_a l_tr/l_ts) while linear Transformers are bounded by α < 1/2. Corollaries 1 and 2 explain mechanistically how the linear attention selects pattern-matching examples and the gating suppresses outliers while imposing an exponential locality bias. Synthetic experiments support the qualitative predictions.

## Strengths
- **First theoretical training-dynamics analysis of Mamba for ICL.** The paper correctly identifies a genuine gap: existing theoretical ICL work (Zhang et al., 2023; Huang et al., 2023; Li et al., 2024a,b) focuses on Transformers, while existing Mamba theory (Li et al., 2024b; 2025b; Bondaschi et al., 2025) studies global minima or expressivity, not training dynamics. This paper is the first to provide convergence guarantees (Theorem 1) and sample complexity for a trained Mamba model, including an explicit characterization of how outlier fraction p_a enters the bounds.
- **Clean architectural decomposition.** Equation (3) is a genuine analytical contribution: showing that one-layer Mamba decomposes into a linear attention term (p_i^T W_B^T W_C p_query) and a nonlinear gating term G_{i,l+1}(w) with a clear product-of-sigmoids structure. This decomposition enables the subsequent mechanistic analysis and the ablation-style comparison with linear Transformers.
- **Specific, falsifiable comparative prediction.** The theory makes a sharp quantitative prediction: Mamba can tolerate α up to min(1, p_a l_tr/l_ts) while linear Transformers are bounded by α < 1/2 (Theorem 4 vs. Theorem 2). Unlike many theory papers where bounds are too loose to be informative, this is a concrete, testable contrast. The experiments in Figure 2 are consistent with this prediction.
- **Mechanistic decomposition via Corollaries 1 and 2.** The corollaries provide a coherent story about how Mamba achieves robustness: the linear attention selects examples sharing the query's relevant pattern, the gating suppresses outliers and imposes an exponential locality bias. This goes beyond "Mamba is robust" to explain why in architectural terms.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- **The CQ failure case is underexposed.** Table 1 shows Mamba at 82.73% vs. the linear Transformer at 93.96% when outliers are placed closest to the query (CQ) — an 11+ point deficit. The paper discusses this in Section 4.2 and correctly traces it to the exponential locality bias of the gating (Corollary 2(ii)), which becomes a liability when outliers sit near the query. However, this finding is absent from the abstract and conclusion, giving an incomplete picture of the robustness claim. The gating mechanism's locality bias is a double-edged sword: beneficial when outliers are far/random but harmful when they are positioned adversarially near the query. This should be surfaced in the paper's central claims, not buried in a single sentence.
- **Experiments lack basic statistical reporting.** No variance, standard deviation, confidence intervals, or number of random seeds are reported for any result (Figure 2, Table 1). With a single run of a synthetic data process, it is impossible to assess whether observed differences (e.g., the 99.73% vs. 93.68% gap in the FQ row) are statistically significant or within run-to-run noise. For a paper whose abstract claims the theory is "supported by empirical experiments," some measure of variability is needed.
- **The comparison baseline is a linear-attention Transformer (G=1), not a full softmax-attention Transformer.** The paper is consistently transparent about this — the abstract, contributions, theorem statements, and experiments all specify "linear Transformers" — and Remark 6 explicitly acknowledges the limitation, referencing softmax-attention experiments in the appendix. However, the broader narrative framing (introduction discussion of Mamba vs. Transformers generally) and the title could be read as claiming a more general result. The paper's core technical contribution (the gating mechanism analysis and its mechanistic consequences) does not depend on this comparison, so this is a presentation issue rather than a methodological flaw.
- **The test-time outlier condition restricts generality.** Theorem 2 Condition (a) requires test outliers to be positive linear combinations of training outlier patterns. While the paper is transparent about this (Remark 3 states it explicitly), the term "unseen" in the contribution summary (P1) could overstate the generality — an entirely novel outlier direction orthogonal to all training outlier patterns is not covered. The practical scope of the robustness guarantee is narrower than the word "unseen" suggests.

### Trivial
None.

## Nice-to-Haves
- A brief experimental validation of one quantitative scaling prediction from the theory (e.g., the (1-p_a)^{-1} dependence in required context length or iterations) would demonstrate that the bounds track empirical behavior, beyond the qualitative agreement shown.
- A discussion of which data-model assumptions (orthogonality, equal norm, hinge loss) are essential and which are for analytical convenience would help readers assess the scope of the results.

## Removed Points
These points are flagged to be removed, treat them with caution:
- **"Strawman Transformer" as a fatal issue**: The paper consistently and explicitly states "linear Transformers" throughout. The comparison target is clearly defined; Remark 6 further clarifies the scope. The framing concern is a minor presentation issue, not a fatal flaw.
- **Hinge loss "unusual" observation**: This is a standard design choice in theoretical analysis, not a weakness of the paper.
- **Only one experimental configuration**: Standard for a theory paper where supporting experiments are secondary to the theoretical contribution.
- **Data model assumptions not probed (orthogonality, etc.)**: These assumptions are standard in this line of theoretical work (Li et al., 2024a; Huang et al., 2023). Discussing assumption relaxation would strengthen the paper but its absence is not a flaw.
- **Proliferation of constants**: Standard for this type of theoretical analysis; Remark 1 provides helpful interpretation.
- **Speculative concerns about arbitrary labeling functions**: The paper explicitly allows arbitrary labeling (Definition 2), which is a strength, not a weakness.
- **Missing softmax-attention comparison in main text**: The paper states in Remark 6 that such experiments are in Appendix B.1. Per review policy, content stripped by the parser is assumed to exist in the original submission.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add the CQ failure case to the abstract and conclusion to give readers a complete picture of when Mamba's gating advantage holds and when it reverses.
2. Report experiments with at least 5 random seeds and include standard deviations or error bars.
3. Consider adding one figure testing a quantitative scaling prediction from the theory (e.g., required context length scaling with (1-p_a)^{-1}) to demonstrate that the bounds track empirical trends.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| 52XG8eexal (SSMs learn ICL by GD) | 4.00 | R1 | Yes | Weaker: novelty concerns, unclear connection to practice. Our paper is stronger on both. |
| XZhpS5Imzx (Transformers ICL LDS) | 4.00 | R1 | No | Similar topic, lower score. |
| HuBFimORiz (Global Optimality Markov Chains) | 4.33 | R1 | Yes | Weaker: trivial bounds, limited scope. Our paper has sharper predictions. |
| TdgAtxP6G2 (Transformers learn VOMC) | 4.00 | R1 | No | Similar methodology, lower score. |
| QFgbJOYJSE (SSMs comparable to Transformers) | 5.75 | R1 | Yes | Similar: theory paper with comparable experiment quality. Accept decision. |
| ikwEDva1JZ (ICL Beyond Simple Functions) | 6.50 | R2 | Yes | Stronger empirical validation but weaker theoretical novelty (construction-based). |
| aKJr5NnN8U (In-context vs In-weight Learning) | 6.50 | R2 | Yes | Stronger experiments but theory-experiment mismatch criticized. |
| gK1rl98VRp (Auto-Regressive NTP ICL) | 6.00 | R1 | No | Similar level of contribution. |
| u1cQYxRI1H (Unrelated: diffusion) | 0.50 | R1 | No | Unrelated. |
| Others in low bands | 1.00 | R1 | No | Unrelated or clearly weaker. |

**Round 1 bracket:** 5.5–7.0. The paper is clearly above the 4.00 SSM+ICL paper (fundamental novelty concerns) and comparable to the 5.75 and 6.00–6.50 anchors.

**Narrowing:** Comparing against the 5.75 anchor (SSMs comparable to Transformers) — both papers provide theoretical analysis with supporting synthetic experiments. Our paper has stronger theoretical novelty (first training dynamics analysis of Mamba vs. expressive-power results) and makes sharper falsifiable predictions. The 6.50 anchors have stronger experiments but their theoretical contributions are either construction-based (representational, not training dynamics) or had theory-experiment alignment issues. Our paper sits between these: genuine and novel theory, adequate but not strong experiments.

**Final score: 6.0.** The paper makes a genuine theoretical contribution — the first training-dynamics analysis of Mamba for ICL — with a clean architectural decomposition and specific, testable predictions. The weaknesses (CQ failure underexposed, no statistical reporting in experiments, comparison baseline scope, test-outlier condition transparency) are real but do not invalidate the core theoretical contribution. The paper would be strengthened by surfacing the CQ limitation in the abstract and adding basic statistical reporting to the experiments.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>