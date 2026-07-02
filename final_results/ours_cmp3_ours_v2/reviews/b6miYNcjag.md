## Summary

This paper introduces a formal framework for evaluating dataset reliability without access to ground truth, using auxiliary observations from an unknown statistical experiment. It proposes the **Gram determinant score** — the determinant of a Gram matrix built from reported labels and observations — and proves that this score preserves several reliability orderings (exact-match, Blackwell, approximate Hamming/dist) under linearly independent experiments. A key theoretical result (Proposition 4.3) shows the score is, up to scaling, the unique experiment-agnostic reliability measure. Experiments on synthetic data, CIFAR-10 embeddings, and employment data provide initial validation.

## Strengths

1. **Clean theoretical framework for a genuinely hard problem.** The paper formalizes a well-motivated problem — assessing dataset reliability without ground truth — using partial orderings (Exact Match, Blackwell, Hamming/dist). The impossibility results in Section 3 create a clear characterization of what can and cannot be achieved, which is more informative than most work in this area.

2. **Experiment agnosticism and uniqueness (Proposition 4.3).** Showing that the Gram determinant score yields the same dataset ranking regardless of the experiment (up to scaling) is a genuinely novel and interesting property. The factorization Γ(PQ) = det(P^T P) det(Q)^2 elegantly decouples the experiment from the misreport matrix.

3. **Honest limitation analysis.** Section 3 clearly delineates the boundaries of what is possible, showing that the restrictions to P_indep and constrained misreport classes are necessary, not arbitrary. The paper does not overclaim.

4. **Geometric interpretation.** The volume-of-parallelepiped intuition (Figure 1) makes the mathematical construction accessible and helps build intuition.

## Weaknesses

### Major

1. **CIFAR-10 experiment likely violates the core theoretical condition (P_indep).** Theorem 4.2 and all ordering-preservation guarantees require P ∈ P_indep — linearly independent columns of the experiment matrix. In the CIFAR-10 experiment, observations are 8-dimensional embeddings (via SimCLR projection head, line 256) and there are d=10 classes. The columns of the effective experiment matrix P (an 8×10 matrix) are necessarily linearly dependent, so P_indep cannot hold. The paper defers the kernelized version's theoretical guarantees to Appendix F (not available in the review text), but as presented, the main real-image experiment uses conditions where the theory's preconditions are violated, and this gap is not acknowledged in the main text.

2. **No baselines compared against.** Every experiment evaluates the Gram determinant score in isolation. Without any comparison to alternative scoring methods — e.g., correlation between x̂ and y, mutual information, trace of Ĝ, Frobenius norm of Ĝ, or simpler heuristics — it is impossible to tell whether the Gram determinant captures something distinctive or merely reproduces trivial correlations. The paper proposes a new framework and a specific score; baselines are essential to contextualize the contribution.

3. **The α-dist ordering result (Theorem 4.2, part 3) is practically very restrictive.** The guarantee preserves (1/(4LΔ))-dist ordering under Q_{L, 1/64L²d²}. The constraint δ = 1/(64L²d²) means the Hamming distance must be ≤ N/(64L²d²). For d=5, L=1, this allows at most N/1600 misreports (≈2.5 errors per 4000 samples). For d=10, it drops to N/6400 (≈0.6 errors per 4000 samples). The guarantee thus applies only to extremely clean datasets. The γ = 1/(4LΔ) factor is also small (e.g., 0.25 for Hamming with L=1), preserving only a very weak notion of ordering. The paper presents this alongside the exact-match and Blackwell guarantees without adequately highlighting how restrictive the preconditions are.

### Minor

4. **Employment data experiment is too thin to carry weight.** N=209 samples, d=4 discretized buckets, no error bars, no confidence intervals, no statistical tests, no sensitivity analysis for the discretization choice (line 270). The score increases across vintages, but this is expected from data provenance and the experiment contributes limited evidence beyond what is already known.

5. **"Strategic" framing is not tested.** The title and abstract emphasize "potentially strategic sources," but all experiments test random corruption models (uniform random, asymmetric neighbor, etc.). No adversarial misreport model is tested where the agent knows the experiment P and the scoring mechanism and tries to manipulate reports to appear reliable. The framing thus overstates what the experiments demonstrate.

6. **Merge 0/1→0 manipulation produces a theoretically singular Q.** This manipulation maps two true classes to one report class, making Q non-invertible. Theoretically det(Q)=0 and Γ=0. The empirical score still varies in Figure 2 (likely due to finite-sample estimation), which warrants discussion but is not provided.

7. **No discussion of computational complexity.** The plug-in estimator requires O(N² + d³) operations for a d×d Gram matrix determinant. The kernelized version involves O(d²N²) inner product computations. For large d (e.g., 1000 classes), this is expensive and should be noted.

### Trivial

- The framework requires identical finite spaces for true and reported data (𝒳=[d]), which excludes continuous label spaces and settings where the report space differs from the true space. The conclusion mentions this as future work, but earlier acknowledgment would help.
- The Kendall-tau experiment (Fig 2d) shows ranking recovery plateaus around 0.7–0.8 even at N=4000. This is not a flaw but merits brief discussion.

## Nice-to-Haves

- Add at least simple baselines (trace or Frobenius norm of Ĝ, correlation between x̂ and y) to the synthetic experiment to contextualize the determinant's value.
- Acknowledge the P_indep violation in the CIFAR-10 experiment explicitly and clarify whether the kernelized version (Appendix F) provides different theoretical conditions.
- Add error bars or confidence intervals to the employment experiment.
- Test the method in a setting where ground truth is deliberately withheld and the score is used to make a decision, then evaluate that decision.

## Removed Points

- *"No experiment tests the method in its intended use case (assessing reliability without ground truth)."* — This was a framing in the harsh critic. Evaluating a proposed method by correlating its output with known ground-truth error is standard validation practice. The employment experiment also demonstrates the method without using ground-truth reliability as a comparison target. Demoted to Nice-to-Have.
- *"Kendall-tau ranking recovery plateaus below 1.0."* — This reflects normal finite-sample behavior of any estimator and is not a weakness.
- *"The paper should test with adversarial misreport models."* — Already covered by Minor weakness #5 (strategic framing).
- *"No guidance on choosing the observation y."* — A valid observation but more of a limitation for future work than a weakness of the presented method.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add baselines (trace, Frobenius norm, mutual information) to all three experiments.
2. Explicitly discuss the P_indep condition in CIFAR-10 and clarify whether the kernelized version rescues the guarantees.
3. Discuss the restrictiveness of the α-dist ordering precondition (δ = 1/(64L²d²)) quantitatively in the main text.
4. Add error bars and a brief sensitivity analysis to the employment experiment.
5. Soften the "strategic" framing or add an experiment with an adversarial misreport model.

## Score and Decision

**Score calibration anchors:** All anchors from the deepreview_13k_calibration corpus.

| Anchor path | Avg score | Round | Comparison |
|---|---|---|---|
| Mitigating Input Noise in Binary Classification (pTsP30MoBq) | 4.20 | Round 2 | Weaker theory, similarly limited empirics; this paper's theory is stronger |
| Just Select Twice (dugoA2gfhs) | 5.00 | Round 2 | Empirically strong but no theory; this paper has stronger theory |
| Identifiability Matters in ULTR (LUcdXA8hAa) | 4.75 | Round 1 | Similar profile (good theory + missing baselines); this paper's theory is more substantial |
| Unmasking Data Credibility (6bcAD6g688) | 5.75 | Round 1 | Strong systematic empirics, accepted; this paper has stronger theory but weaker empirics |
| Class-wise Autoencoders (RW37MMrNAi) | 5.60 | Round 1 | Strong empirics but weak theory claims; rejected; this paper has stronger theory |
| Universal metric of dataset similarity (LVFoynuAQn) | 4.33 | Round 1 | Similar scope (data quality metric); this paper has cleaner theory |

**Round 1 bracket:** 4.0–5.5  
**Round 2 narrowing:** Compared to Identifiability Matters (4.75, rejected) and Just Select Twice (5.00, rejected), this paper has a stronger theoretical core but worse empirical coverage. Compared to Unmasking Data Credibility (5.75, accepted), the empirics are substantially thinner. The final score reflects a paper with a genuine theoretical contribution held back by an evaluation that does not adequately support its practical claims.

**Final score: 5.0** — Borderline. The theoretical contribution (formalization, impossibility results, Gram determinant score with ordering preservation and experiment agnosticism) is solid and novel. However, the empirical evaluation has significant gaps: no baselines, the CIFAR-10 experiment operates under conditions that likely violate the theoretical preconditions, and the α-dist ordering guarantee is practically very restrictive. The paper as presented sits between a theoretical contribution (which is strong) and an empirical validation (which is too weak for the claims made).

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>