Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper presents CausalNovo, a model-agnostic framework for de novo peptide sequencing that uses a causality-inspired approach to learn representations invariant to noise peaks. The method identifies noise peaks by comparing against a theoretical spectrum derived from the ground-truth peptide, replaces some of those peaks to simulate causal interventions, then uses contrastive and cross-entropy objectives to encourage the model to focus on signal-related features. Experiments across three datasets and three baseline architectures (CasaNovo, AdaNovo, π-HelixNovo) show consistent improvements at amino acid, peptide, and PTM levels.

## Strengths

1. **Well-motivated problem with empirical grounding.** The vulnerability analysis (Figure 1) demonstrates that existing models degrade when noise peaks are perturbed, providing concrete evidence — not speculation — that models rely on spurious correlations.

2. **Model-agnostic framework with extensive integration.** CausalNovo is integrated with three distinct baseline architectures and shows consistent improvements across all of them, demonstrating generality rather than overfitting to a single model.

3. **Comprehensive evaluation.** Experiments span three datasets (Nine-species, Seven-species, HC-PT), three metric families (amino acid, peptide, PTM-level), cross-species validation, NSR generalization, and attention analysis — more thorough than most papers in this space.

4. **Informative ablation studies.** Tables 4 and 5 isolate each component (independence, purification, symmetric training, replace-based perturbation, causality enhancement), including a useful negative control (random drop that did not help, Section 4.4).

5. **Honest about limitations.** The paper acknowledges the 2.3× training time overhead and the gap between the NovoBench evaluation protocol and the more realistic protocol used by recent methods (Section 5).

## Weaknesses

### Fatal
None.

### Major

1. **Causal framing is inflated relative to what is implemented.** The paper presents an SCM (Figure 2A, Equation 2: X = f(C,S), C ⟂ S, Y = g(C)) and uses causal language throughout — "causal intervention," "do(S)," "causal factors." However, the actual method works as follows: (a) identify "noise" peaks by comparing against a theoretical spectrum derived from the *ground-truth label Y* (Equation 4), (b) replace some of those peaks to create a perturbed spectrum, (c) train representations to be invariant to this perturbation via contrastive learning conditioned on Y (Equation 5), (d) train on the label prediction task. There is no causal identification, do-calculus, or estimation of causal effects. The "do(S)" operation is simulated by noise-peak replacement that depends on knowing Y to identify which peaks are noise in the first place — creating a circularity: the label is needed to identify noise, and the method trains to predict the label. The SCM is used as inspiration to derive reasonable principles (independence, sufficiency), but calling the result a "causality-informed framework" overstates what is technically achieved. The method would be more accurately described as *invariant representation learning with noise-aware data augmentation for de novo peptide sequencing* — a legitimate contribution, but smaller than claimed. This gap between framing and substance is the paper's most significant weakness.

2. **No statistical significance or variance reporting.** Every reported number across all tables and figures is a single point estimate with no error bars, standard deviations, or indication of multiple runs. Given that several improvements are modest (e.g., +2.2% amino acid precision for π-HelixNovo on Nine-species in Table 1; +2.6% average peptide precision in cross-species validation in Table 3), it is impossible to assess whether these improvements are reliable or within training noise. This is a field-standard expectation that the paper does not meet.

### Minor

3. **RI metric in Table 6 is not clearly defined and values do not match standard relative improvement.** The paper defines RI as "the relative performance reduction of CausalNovo compared to the baseline models," but the values in Table 6 do not correspond to any standard definition of relative improvement. For example, at threshold=1 on HC-PT, CasaNovo peptide precision is 0.156 and CausalNovo is 0.352 — a raw improvement of 0.196 (125.6% relative to baseline), yet the reported RI is 28.5%. A precise formula is not provided, making this headline quantitative claim unverifiable.

4. **The independence objective's reliance on Y as a proxy for C is a significant unexamined assumption.** The paper states the objective as max I(z_c; z_c' | C) and then replaces unobserved C with Y (line 181), justified by Y = g(C) from the SCM. This substitution is weaker than claimed: Y provides information about an equivalence class of C values, not full conditioning on C. The contrastive approximation (Equation 5) conditions on Y by treating examples with the same Y as positives, which conflates "same label" with "same causal factors." Different peptides (different Y) could share causal factors, and the same Y could arise from different spectral patterns. While this type of proxy assumption appears in the causal representation learning literature (Chen et al., 2022), the paper should discuss its limitations explicitly rather than treating the substitution as straightforward.

5. **The purification objective (max I(z_s; Y)) is confusingly explained.** The paper states that maximizing I(z_c; Y) could reduce I(z_s; Y), and therefore adds an auxiliary objective that maximizes I(z_s; Y) to "indirectly lead to the purification of z_c" (lines 97-98). The causal mechanism by which maximizing mutual information between the *non-causal* representation z_s and the label Y purifies the *causal* representation z_c is not clearly articulated and appears counterintuitive. This section needs a more careful explanation or justification.

### Trivial
None.

## Nice-to-Haves

- Adding variance estimates (error bars or standard deviations) for at least the main results (Table 1) would substantially strengthen the paper's claims.
- The paper mentions several recent 2025 methods (ContraNovo, RankNovo, π-PrimeNovo, RefineNovo, ReNovo) in related work but does not compare against them in the main tables. While differences in evaluation protocol partly explain this, a brief acknowledgment for each excluded method would be helpful.
- Hyperparameter sensitivity for key parameters (tolerance threshold γ, replacement fraction α, temperature τ) is not analyzed beyond the threshold variation in Table 6.
- Retrained baselines (marked †) sometimes underperform published numbers; reporting CausalNovo's improvement over the *published* numbers in addition would strengthen the comparison.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **Criticism that the RCCP is misapplied because "C causes X, not C being a common cause of X and Y."** — REMOVED. Factually incorrect. Equation 2 states Y = g(C) and X = f(C,S), so C is a common cause of both X and Y, consistent with RCCP.

2. **Criticism that the "statistical nature" framing (line 15) is overstated.** — REMOVED. This is a stylistic complaint about standard ML rhetoric. All papers contrasting statistical vs. causal approaches use this kind of language.

3. **Criticism that retrained baselines underperform published numbers.** — REMOVED. Moved to Nice-to-Haves. The paper transparently reports both published and retrained results; this is a suggestion for additional analysis, not a weakness.

4. **Criticism about missing comparison with 2025 methods.** — REMOVED. Moved to Nice-to-Haves. The paper acknowledges the protocol difference (Section 5) and includes SearchNovo. The reviewer's concern has merit but the paper partially addresses it.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a useful perspective: the strongest evidence for CausalNovo's approach is the *pattern* of improvements across thresholds in Table 6 and Figures 1/3 — the method shines where the baseline degrades most (tight thresholds, high noise). However, without variance estimates or a clear RI formula, even this pattern is hard to interpret precisely.

## Suggestions

1. Reframe the contribution as invariant representation learning with noise-aware data augmentation for de novo sequencing, rather than "causal" discovery. This would align the paper's claims with its technical content.
2. Add multiple-run variance estimates (at least 3 runs with mean and std) for all main results (Table 1, Table 3, Table 6).
3. Provide a precise formula for the RI metric and verify the reported values are auditable from the table data.
4. Clarify the purification objective: explain the mechanism by which maximizing I(z_s; Y) purifies z_c, or remove this framing.
5. Explicitly discuss the Y-as-proxy-for-C assumption and when it might fail.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>