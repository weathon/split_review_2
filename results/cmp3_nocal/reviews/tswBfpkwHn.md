## Summary

This paper provides the first theoretical analysis of training dynamics and ICL generalization for a one-layer Mamba model on binary classification tasks with additive outliers. The authors derive a closed-form expression for Mamba as linear attention followed by nonlinear gating, prove SGD convergence guarantees, and establish generalization bounds under distribution shift. They compare against one-layer linear Transformers (a special case of their formulation with gating removed), showing that while Mamba requires more training iterations, it can tolerate a higher fraction of outliers (α approaching 1, versus α < 1/2 for linear Transformers). The theoretical findings are supported by synthetic experiments and the mechanism is validated through attention-score and gating-value measurements.

## Strengths

1. **First theoretical analysis of Mamba's ICL training dynamics with convergence guarantees.** Prior work (Li et al., 2024b, 2025b) studied Mamba-like models at the loss-landscape level; this paper goes further by characterizing SGD convergence and providing explicit ICL generalization bounds for a one-layer Mamba, including the case with additive outliers.

2. **Clean closed-form decomposition of Mamba into interpretable components.** Equation (3) — deriving the output as linear attention (parameterized by W_B, W_C) followed by a nonlinear gating function G_{i,l+1}(w) — is an elegant analytical simplification. It cleanly isolates the two mechanisms that are then independently characterized: Corollary 1 (attention selects same-pattern examples) and Corollary 2 (gating suppresses outliers and induces recency bias).

3. **Honest reporting of Mamba's limitations.** The CQ (closest-to-query outliers) experiment in Table 1 shows Mamba dropping to 82.73% while the linear Transformer stays at 93.96%. The paper does not hide this result and offers a plausible explanation (exponential gating decay interacting badly with nearby outliers). This candor strengthens credibility.

4. **Well-structured comparison framework.** Setting the linear Transformer as a special case of the same formulation (G=1) makes the comparison clean and apples-to-apples at the architectural level, isolating the gating mechanism as the only structural difference.

## Weaknesses

### Fatal
None.

### Major

1. **The "generalization to unseen outliers" claim is restricted by a strong linear-combination condition.** Theorem 2, Condition (a) requires every test-time outlier to be a linear combination of the V training outlier patterns whose coefficients sum to at least L > 0. This means test outliers must lie in a cone of the training outlier subspace — they cannot be entirely novel directions. The paper's motivating example (Example 1: a "James Bond" poisoning attack) involves a completely new poisoning vector, not a combination of previously seen ones. The paper states this condition (line 93, Remark 3), but the abstract and contribution list (line 31) emphasize that "unseen outliers" are handled without adequately contextualizing that "unseen" here means "unseen coefficients in seen directions." This gap between the motivating narrative and the actual scope of the guarantee should be acknowledged more prominently.

2. **The "approaches 1" robustness claim depends on specific conditions not highlighted in the abstract.** The bound is α < min(1, p_a·l_tr/l_ts). For α to approach 1, one either needs p_a very close to 1 or l_tr significantly larger than l_ts. With equal prompt lengths (as in the experiments), α is bounded by p_a, which is at most technically less than 1. The abstract (line 31) states "Mamba can maintain accurate ICL generalization even when the fraction of outlier-containing context examples approaches 1" without noting this dependency. The experiments test only up to α = 0.8 (with p_a = 0.6, where the theoretical bound gives α < 0.6), so the empirical demonstration of the "approaches 1" claim is partial.

### Minor

3. **No error bars, variance, or seed information reported.** The experimental section (Section 4) does not report standard deviations, confidence intervals, or the number of random seeds used. Given the stochasticity in data generation and training, the results could vary across runs. This is a basic experimental hygiene gap.

4. **The gating mechanism analysis does not discuss a tension between the two roles of σ.** The gating function G_{i,l+1}(w) = σ(w^T p_i) Π_{j=i+1}^{l+1} (1 - σ(w^T p_j)). For outlier suppression (Corollary 2(i)), the gating value must be near zero, which requires σ(w^T p_i) ≈ 0 for outlier-containing inputs. For the exponential decay in Corollary 2(ii), clean examples need σ(w^T p_j) at some intermediate value (so that (1-σ) ≈ 1/2 for each intermediate example). The paper does not discuss whether a single learned w can simultaneously achieve both regimes given the orthogonal data structure. While the orthogonality between outlier patterns and clean patterns makes this plausible, explicitly reasoning about this would strengthen the mechanism story.

5. **The limitations section is too brief for the strength of assumptions made.** Section 5 is only three sentences and does not discuss the implications of the strong simplifying assumptions: orthogonal patterns, one-layer architecture, A = -I_m (removing the state space model's ability to learn per-dimension memory), and the linear-combination restriction on test outliers. A paper that makes such assumptions should dedicate more space to discussing their scope and implications.

### Trivial
None.

## Nice-to-Haves

- A within-architecture ablation that freezes or removes the gating weights in Mamba (setting G=1) and compares against the full Mamba model would more directly isolate gating as the causal factor in robustness, rather than the cross-architecture comparison.
- A discussion of when the sufficient conditions are tight (e.g., examples of data distributions satisfying the conditions where Mamba cannot learn to suppress outliers) would help calibrate the scope of the theory.
- Reporting the training cost comparison for the synthetic experiments, since the paper motivates Mamba by its efficiency advantages.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

1. **"Comparison is between sufficient conditions, not necessary conditions"** — The paper explicitly acknowledges this (line 187, Remark 6) and validates the predicted thresholds with experiments (Figure 2). The comparison being between sufficient conditions is standard practice in this literature (Fu et al., 2023b; Jiang et al., 2024). This is not a weakness; it is a correctly scoped contribution.

2. **"The derivation in Appendix E.1 is stripped, cannot verify"** — The appendix is stripped by the PDF parser for all papers. This is a parsing artifact, not an author omission.

3. **"The analysis in the stripped appendix may address this"** — Same as above; cannot penalize for content stripped by the system.

4. **"Missing related works"** — Not verifiable without external sources; the instruction explicitly prohibits flagging missing related works.

5. **Criticisms about formatting, garbled characters, broken symbols** — These are parser artifacts, not paper errors.

6. **"Random labeling outlier type is consistent with Theorem 2"** — The critic acknowledges this; not a genuine weakness.

7. **"Condition (b) requires κ'_a ≥ κ_a, paper does not discuss violation"** — The paper states the condition as a requirement; this is how sufficient conditions work. Not a weakness.

8. **"Computational requirements not discussed"** — This is a nice-to-have, not a substantive weakness.

## Novel Insights

None beyond the paper's own contributions. The reviews raise a useful subtle point about the gating-function tension (σ must simultaneously produce near-zero outputs for outliers and intermediate values for clean examples) that the paper does not explicitly address, but this is a granular technical observation rather than a conceptually novel insight.

## Suggestions

1. Add error bars or at minimum report the number of random seeds used across experiments.
2. Expand the limitations section (Section 5) to explicitly discuss the key assumptions: orthogonal patterns, linear-combination test-outlier condition, one-layer architecture, and A = -I_m simplification, and what would be needed to relax them.
3. Add a sentence in the abstract or introduction clarifying that the "α approaches 1" bound depends on the relationship between p_a, l_tr, and l_ts.
4. Briefly discuss in the text (alongside Corollary 2) whether the trained w simultaneously achieves σ-near-zero for outliers and intermediate σ for clean examples given the orthogonal structure, or note why this follows from the optimization.

## Score and Decision

This is a solid theoretical contribution that, within its stated scope, delivers the first analysis of Mamba's training dynamics for ICL with a clear mechanism story and a fair comparison to linear Transformers. The core findings — that the gating mechanism enables outlier suppression and that this comes at the cost of harder optimization and sensitivity to outlier position — are well-supported by the theory and consistent with the experiments. The weaknesses are about scope communication (how the conditions are presented in the abstract vs. the theorem statements) and experimental rigor (missing error bars), none of which invalidate the core claims. With transparent revision to the presentation of limitations and addition of basic experimental reporting, the paper is publishable at a top-tier venue.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>