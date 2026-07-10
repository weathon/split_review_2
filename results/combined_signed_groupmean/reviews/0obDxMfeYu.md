Now I have a thorough understanding. Let me write the final consolidated review.

## Calibration Summary

**All anchors retrieved across rounds:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|-----------|
| SAL (Du et al. 2024a) | jlEjB8MVGa.md | 6.50 | 1 | Yes | Direct predecessor. My paper has stronger empirical results but more theory-algorithm exposition gaps. |
| ProMix | voVjW1PT2c.md | 6.00 | 1 | Yes | OOD detection with auxiliary data. My paper has stronger novelty but similar clarity issues. |
| MixDiff | sZZ3R0lV9f.md | 5.25 | 1 | Yes | Perturbation-based OOD. My paper has clearer motivation and stronger baselines. |
| CP-OOD Link | GQhlM0Mavg.md | 5.00 | 2 | Yes | CP+OOD link. My paper has much stronger empirical novelty. |
| NOD | imuVEKaU3b.md | 3.67 | 1 | Yes | Unsupervised OOD. My paper has far stronger results but similar theory-clarity concerns. |
| GM Matching | e2F0mJJeN0.md | 3.00 | 1 | Yes | Median-based data pruning. My paper is more novel for its domain. |

**Round-1 bracket:** 5.0 – 6.5. My paper sits between ProMix (6.00, rejected) and MixDiff (5.25, rejected). The direct predecessor SAL (6.50, accepted) sets the upper bound — my paper lacks SAL's clean theory-algorithm connection but has stronger empirical results.

**Comparison via scored items:** My paper shares SAL's decisive strengths (theory ≈ +10, empirical ≈ +10). However, my paper also carries three -10-magnitude weaknesses (theory-algorithm gap, stopping criterion inconsistency, hyperparameter opacity) that SAL did not have. These are presentation/rigor gaps, not fatal errors, but they are more structural than MixDiff's motivation concern. **Final score: 5.5** — borderline, with real contributions that are partially undermined by exposition and rigor issues that require substantive revision.

---

## Summary

This paper introduces Medix, a framework that uses the element-wise median (EWM) of gradients to filter outliers from unlabeled "in-the-wild" data for OOD detection. The method is novel in its use of median-based filtering for this setting. Empirically, Medix achieves state-of-the-art results across CIFAR-10 and CIFAR-100 benchmarks (e.g., 0.80% average FPR95 on CIFAR-10 vs. 3.40% for WOODS), and the paper provides theoretical bounds on inlier/outlier misclassification rates.

## Strengths

- **Novel algorithmic idea.** Using the element-wise median of gradients as a filtering criterion for OOD detection in wild data is a fresh perspective that differs from prior thresholding (Du et al., 2024a) and constrained-optimization (Katz-Samuels et al., 2022a) approaches. The median's inherent robustness to outliers is well-motivated as the core mechanism, especially when the OOD proportion is under 50%.

- **Remarkably strong empirical results.** On CIFAR-10, Medix achieves an average FPR95 of 0.80% and AUROC of 99.74%, substantially outperforming WOODS (3.40%, 98.92%) across all 5 OOD datasets. On CIFAR-100, the average FPR95 of 5.42% is a meaningful improvement over WOODS's 6.74%. Results are reported with standard deviations across five runs.

- **Valuable theoretical formalism.** Few prior works provide theoretical foundations for the wild-data OOD setting. The paper identifies contamination, concentration, and separation effects governing median-based filtering and shows why the method should be robust when π < 0.5. This provides useful insight even if the connection to the specific algorithm needs clarification.

## Weaknesses

### Fatal

None.

### Major

1. **Theory-algorithm gap.** Theorems 4.1 and 4.2 bound misclassification rates of "the EWM filtering rule," which is never formally defined in the paper. The actual method (Algorithm 1) is an iterative greedy leave-one-out procedure, but the theorems contain no dependence on algorithmic parameters (k, ε, T) and no analysis of how errors compound over iterations. While the theorems provide useful motivation for why median-based filtering should work in principle, the paper claims (C2, Sections 1 and 7) that they provide guarantees for Medix specifically, without clarifying the mapping between the analyzed rule and Algorithm 1. This gap needs to be addressed by either formally defining the analyzed rule and showing how Algorithm 1 implements it, or by stating explicitly that the theorems bound the fundamental limits of EWM-based filtering rather than Algorithm 1's convergence behavior.

2. **Stopping criterion inconsistency.** The prose describes the stopping criterion in two places as terminating when "the L₂-norm deviation between consecutive iterations drops below ε" (lines 85, 95–96), i.e., |d_t − d_{t−1}| < ε. However, Algorithm 1 (line 110) uses the condition |δ_max| > ε in the while loop, where δ_max is the maximum single-sample drop in distance — a different quantity. This ambiguity makes the algorithm's exact behavior unclear and undermines reproducibility.

3. **Hyperparameter selection ambiguity.** The paper states (line 178) that ε and k are selected "with the objective of maximizing OOD performance." In the wild-data setting, the algorithm does not have access to OOD labels. It is critical to specify: was a held-out validation set with known labels used, or was some label-free heuristic employed, or were test OOD sets used for tuning? Without this clarification, the validity of the reported results cannot be fully assessed.

### Minor

4. **Misleading "40.98%" claim.** The abstract (line 27) and conclusion (line 262) state that Medix outperforms KNN+ "by an average of 40.98% in terms of FPR95." The absolute FPR95 difference is 40.98 percentage points (KNN+ 46.40% vs. Medix 5.42% on CIFAR-100). However, standard ML usage reads "reduced by 40.98%" as a relative reduction, which would be 88.3%. This should be clarified to avoid misleading interpretation.

5. **Trivial synthetic experiment.** The synthetic data (Figure 2) places OOD at approximately 36σ from the nearest InD cluster center ([20, 2√3] with covariance 0.25·I vs. InD centers within [−2, 3.5]). This separation is trivially separable by any reasonable method, so a 12.5% error rate on this setup does not provide meaningful evidence of robustness. A more informative experiment would vary the separation distance to demonstrate when the method starts to break down.

### Trivial

None.

## Nice-to-Haves

- The synthetic experiment could be made more informative by varying the separation Δ between InD and OOD distributions and reporting filtering accuracy as a function of Δ.
- An analysis of the single-sample signal-to-noise ratio for δ_i (the drop in distance when removing one point) would help understand why the leave-one-out greedy procedure works despite the median's robustness to outliers.
- It would be helpful to report whether the "40.98% improvement" framing (and similar claims of 52.31% and 38.24% on individual datasets) refers to absolute percentage-point differences or relative reductions.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Fundamental tension about median signal-to-noise ratio:** Removed — this is speculative reasoning questioning signal strength without evidence. The empirical results show the method works.
- **Bound looseness (π/(2(1-π)) = 0.5 at π=0.5):** Removed — the paper does not claim tightness, and loose bounds are not a weakness.
- **Missing CONJ/DRL baselines from main tables / runtime not reported:** Removed — these likely appear in the appendix, which was stripped by the parser.
- **Table formatting issue (ReaT row alignment):** Removed — parser artifact.
- **Missing related works:** Removed — as an area chair, I cannot independently verify whether cited works exist or relevant works were omitted.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Resolve the theory-algorithm gap by (a) formally defining the "EWM filtering rule" that the theorems analyze, and (b) explaining how Algorithm 1's iterative greedy procedure relates to this rule. If the theorems analyze a simpler single-pass decision rule, state this explicitly.
2. Fix the stopping criterion inconsistency: ensure the prose description and the pseudocode (Algorithm 1) describe the same condition.
3. Clarify the hyperparameter selection protocol. Specify whether a held-out validation set with known OOD labels was used, or describe a label-free selection heuristic.
4. Clarify whether "40.98% improvement" (and similar claims) refers to absolute percentage-point reduction or relative reduction.
5. Replace or supplement the synthetic experiment with settings where InD and OOD are closer together, varying the separation Δ to demonstrate where the method's filtering accuracy degrades.

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>