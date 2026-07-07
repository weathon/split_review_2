Now let me finalize the review with all the calibration context.

## Summary

This paper provides the first theoretical analysis of the training dynamics of a one-layer Mamba model for in-context learning (ICL), including convergence bounds and generalization guarantees in the presence of additive outliers. The authors compare Mamba to a one-layer linear Transformer, showing that while Mamba requires more training iterations and larger batch sizes to converge, it can tolerate a much higher fraction of outlier-containing context examples (approaching 1 vs. at most 1/2 for linear Transformers). The mechanistic analysis decomposes this robustness into two components: the linear attention layer selects context examples sharing the same relevant pattern as the query, while the nonlinear gating layer suppresses outliers and induces an exponential recency bias. Synthetic experiments support the theoretical predictions.

## Strengths

1. **First theoretical analysis of Mamba training dynamics for ICL.** The paper fills a clear gap: existing ICL theory focuses almost entirely on Transformers, while Mamba's empirical ICL success has lacked formal treatment. Theorems 1 and 2 represent a non-trivial extension beyond the Transformer case, precisely because the gating mechanism introduces nonlinearities that break the techniques available for linear attention. The paper transparently works with the one-layer setting, which is standard practice in the theoretical ICL literature (Zhang et al., 2023; Li et al., 2024a;b; 2025b).

2. **Clean architectural comparison that isolates the gating mechanism.** By defining the linear Transformer as Mamba with G=1 (Section 2, equation 3), the paper creates a controlled comparison where differences in theoretical results between Theorems 1–2 and Theorems 3–4 can be attributed specifically to the nonlinear gating layer. This is a principled design for a theoretical study.

3. **Concretely testable predictions with experimental support.** The theory makes specific quantitative predictions: Mamba tolerates outlier fraction α < min(1, p_a·l_tr/l_ts) while linear Transformers fail at α > 1/2. These are tested directly in Figure 2 with three different outlier-labeling functions (flipped, targeted, random), and the results are consistent with the theory. The mechanistic predictions (exponential decay of gating values) are verified in Figure 4.

4. **Mechanistic decomposition via Corollaries 1 and 2.** The paper separately characterizes the role of linear attention (pattern-matching, Corollary 1) and nonlinear gating (outlier suppression + exponential recency bias, Corollary 2), providing interpretable insight beyond aggregate convergence bounds. This decomposition clarifies why Mamba's gating — the key structural difference from Transformers — creates a trade-off between harder optimization and superior robustness.

## Weaknesses

### Major

None.

### Minor

1. **The "with a high probability" qualifier in Corollaries 1 and 2 is not quantified.** The paper states these results hold "with a high probability" (lines 215, 225, 229) but does not specify the confidence level (whether it is 1−δ with δ ≪ 1 or something weaker, or how the probability scales with problem parameters such as M₁ or d). For the paper's most novel mechanistic claims, the lack of explicit confidence bounds prevents the reader from assessing the tightness of these guarantees. This is addressable but as written it weakens what would otherwise be the paper's strongest qualitative insights.

2. **Experimental results lack variance reporting.** Figure 2, the main empirical support for the theoretical comparison, reports results for a single parameter configuration (d=30, M₁=6, M₂=10, V=3, p_a=0.6) without error bars, confidence intervals, or information about the number of runs or random seeds. The paper mentions "additional synthetic and real-world data experiments" in the appendix (stripped by the parser), but the main paper's key figure should at minimum indicate statistical reliability. For a theory paper the experiments are illustrative rather than central, so this is a presentation weakness rather than a fundamental flaw.

3. **The robustness guarantee's scope is narrower than the narrative sometimes suggests.** Theorem 2, Condition (a) requires that test-time outliers be positive linear combinations of training-time outliers (v = Σ λ_i v_i^* with Σ λ_i ≥ L > 0). Completely novel outlier types outside the span of training outliers are *not* covered. While the paper states this condition explicitly (Section 3.1, line 93), it does not discuss the significance of this restriction — for example, data poisoning attacks that introduce entirely new trigger patterns would fall outside the guarantee. Additionally, the bound α < min(1, p_a·l_tr/l_ts) requires a moderately high training outlier fraction p_a for α to approach 1 in practice, which is clear from the theorem but could be highlighted more prominently.

4. **The notation in Theorem 1 condition (iii) is ambiguous.** The expression "p_a^{-1} poly(M_1^{κ_a}) ≳ l_{tr}" (line 149) uses κ_a in the exponent of a polynomial argument, which is unusual — it is unclear whether this means poly(M_1)^{κ_a} or poly(M_1^{κ_a}) or something else. Without the appendix, the reader cannot verify whether this is a natural condition or an artifact of the proof technique.

### Trivial

1. The claim in Remark 4 (line 195) that linear Transformers "need a smaller batch size, a smaller number of training iterations" is stated as an empirical finding, but the comparison is between *sufficient* conditions from different proof techniques, not between *necessary* conditions. The wording could clarify that this follows from the sufficient conditions derived, not from a matching lower bound.

## Nice-to-Haves

- An ablation experiment that replaces the cascading-product gating with a simpler per-token sigmoid would help distinguish which properties (outlier suppression vs. recency bias) come from the sigmoid activation and which from the product structure.
- A discussion of the CQ setting where Mamba underperforms (Table 1: 82.73% vs 93.96% for linear Transformer when outliers are closest to the query). The paper acknowledges this but does not discuss whether an adversary could exploit this recency-bias vulnerability.
- Quantifying the "high probability" bounds in the corollaries would substantially strengthen the mechanistic claims.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Concern that simplified Mamba model departs substantially from actual Mamba (Harsh Critic Issue 1):** Removed because the paper explicitly states the assumption A = −I_m, following Theorem 1 of Gu & Dao (2023), which is a standard analytical choice in the SSM literature. The cascading gating structure G_{i,l+1} = σ(w^T p_i) ∏ (1−σ(w^T p_j)) is a faithful consequence of Mamba's selective scan recurrence under this assumption — the recency bias is intrinsic to any gated RNN/SSM with multiplicative state updates, not an artifact of the derivation. The one-layer simplification is standard practice in theoretical work on both Transformers (Zhang et al., 2023; Li et al., 2024a) and SSMs.
- **Concern that the abstract's robustness claim is stated without preconditions (Harsh Critic Issue 2):** Removed because Theorem 2 and Remark 3 (lines 173, 181) transparently state the condition α < min(1, p_a·l_tr/l_ts) and explicitly note that α can approach 1 "if the prompt length is selected in a way such that p_a l_tr/l_ts ≥ 1." No misrepresentation.
- **Concern about "Transformers broadly vs linear Transformers" in abstract:** Removed because the abstract specifically says "linear Transformer" throughout. Remark 6 (line 209) additionally clarifies that large Transformers with softmax attention can achieve robustness.
- **Criticism about cascading product underflow for long sequences:** Though the paper does not explicitly discuss this, Theorem 2 condition (d) bounds l_ts, indirectly addressing sequence length concerns.

## Novel Insights

None beyond the paper's own contributions. The review confirmed the paper's core claims and identified mostly presentational weaknesses (unquantified probabilities, missing error bars, notation ambiguity).

## Suggestions

1. Quantify the "with a high probability" bounds in Corollaries 1 and 2, at least indicating the dependency on key problem parameters (M₁, d).
2. Add error bars or report the number of independent runs for Figure 2.
3. Clarify the ambiguous notation "poly(M_1^{κ_a})" in Theorem 1 condition (iii).
4. Add a brief discussion of the CQ setting limitation and the condition that test outliers must be in the span of training outliers.
5. Clarify in Remark 4 that the comparison is between sufficient conditions, not necessary ones.

## Calibration Anchors

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| qtTIP5Gjc5.md (Demystifying Token Dynamics of Deep SSMs) | 7.50 | 1 | Yes | Similar theoretical Mamba paper, accepted. Both share simplifying assumptions and limited experimental scope. Our paper's theoretical scope is broader (ICL with outliers vs. 1D dynamics). |
| 52XG8eexal.md (SSMs can learn ICL by gradient descent) | 4.00 | 1 | Yes | Much weaker paper — novelty concerns, no insight into practical SSMs. Our paper provides stronger theoretical grounding. |
| 97rOQDPmk2.md (Two-layer Transformers with SignGD) | 7.33 | 1 | Yes | Similar pattern of strong assumptions for analysis. Our paper's contribution is comparable in technical depth. |
| ikwEDva1JZ.md (Transformers Learn ICL with Representations) | 6.50 | 1 | Yes | Accepted ICL theory paper. Our paper's training dynamics analysis goes beyond their representational results. |
| 8p3fu56lKc.md (One Step of GD is Optimal ICL) | 6.00 | 2 | Yes | Similar one-layer linear attention ICL, but our paper handles nonlinear gating and training dynamics, making it technically more substantial. |
| aKJr5NnN8U.md (In-context vs. In-weight Learning) | 6.50 | 2 | No | Accepted ICL theory with simplified gating model. Comparable in structure but our nonlinear analysis is harder. |
| gK1rl98VRp.md (Auto-Regressive Next-Token ICL) | 6.00 | 2 | No | Accepted ICL theory. Our paper provides more granular training dynamics and robustness characterization. |
| VtP7CamOR5.md (Mamba Neural Operator PDEs) | 3.00 | 2 | No | Applied Mamba paper — not comparable. |
| cagNCwQEEN.md (Multimodal Instruction Tuning) | 3.40 | 2 | No | Applied Mamba paper — not comparable. |

**Bracket (Round 1):** The closest comparable anchors are qtTIP5Gjc5 (7.50) and 97rOQDPmk2 (7.33) on the high end, and ikwEDva1JZ (6.50) and 8p3fu56lKc (6.00) on the lower end. The paper is clearly above 6.0 because it handles nonlinear gating (not just linear attention) and provides both convergence and generalization guarantees. It belongs in the 7.0–8.0 range.

**Narrowing:** Compared to qtTIP5Gjc5 (7.50), our paper shares the "simplifying assumptions" weakness and "limited experiments" weakness, but is broader in theoretical scope. Compared to 97rOQDPmk2 (7.33), our paper makes a stronger originality claim (first Mamba ICL training dynamics) while sharing similar assumption-strength concerns. The unquantified "high probability" and missing error bars are presentational issues that prevent scoring at the 8.0 level but do not undermine the core theoretical contribution.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>