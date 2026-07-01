## Summary

This paper introduces Medix, a two-stage framework for OOD detection using unlabeled "in-the-wild" data. Stage 1 filters outliers from a mixed unlabeled dataset via a median-based greedy algorithm that computes gradient deviations from an InD reference gradient. Stage 2 trains a binary OOD detector on the extracted outliers plus labeled InD data. The paper provides theoretical error bounds for the filtering stage (contamination, concentration, and separation effects) and reports strong empirical results on CIFAR-10 and CIFAR-100 against 20 baselines.

## Strengths

1. **Novel and well-motivated median-based filtering approach.** The connection between the median's 50% breakdown point and the theoretical requirement that π < 0.5 is clean and principled. The preliminary experiment (Figure 1) showing monotonic increase in gradient deviation as OOD samples are added provides clear empirical motivation for why the median is a natural choice for this problem. This kind of sanity-check is valuable and helps the reader understand the method's rationale.

2. **Theoretical bounds are a genuine contribution to a theory-sparse subfield.** As the paper correctly notes (Section 1, lines 17-18), Du et al. (2024a) is the only other work providing theoretical guarantees for the in-the-wild OOD setting. The decomposition into contamination, concentration, and separation effects (Theorems 4.1 and 4.2) is interpretable, and the sub-Gaussian verification in the appendix grounds the assumptions empirically. Even loose bounds advance a literature with very little theory.

3. **Strong empirical results, especially on CIFAR-10.** The average FPR95 of 0.80% on CIFAR-10 (Table 1) with standard deviations of 0.01–0.29 across OOD datasets is genuinely impressive. Medix matches or exceeds WOODS on every individual OOD dataset, with substantial gaps on PLACES365 (2.98% vs 10.19%), LSUN-C (0.01% vs 0.51%), and TEXTURES (0.96% vs 6.21%). The CIFAR-100 results (Table 2) are less dramatic but still show consistent improvement over strong baselines.

## Weaknesses

### Fatal
None.

### Major

1. **Framing-evaluation mismatch on "open-world" claims.** The abstract states Medix "outperforms existing methods across the board in open-world settings," and Section 3 frames the method as "particularly well-suited for applications in open-world environments." However, the main experimental setup (Section 5.1) follows the standard protocol where the wild mixture and the test OOD set draw from the **same distribution** (e.g., when testing on PLACES365, the wild mixture also uses PLACES365 as the OOD component). This is a well-defined setting (the wild-data OOD problem of Katz-Samuels et al., 2022a) but it is not an "open-world" evaluation — the test OOD distribution was already seen during training (in the wild mixture). The paper does include an experiment where P_out^test ≠ P_out (Appendix A.4) and claims it "demonstrates that Medix outperforms baselines by a significant margin," but this belongs in the main text given the centrality of the open-world claim. As it stands, the framing significantly overstates what the main experiments evaluate.

### Minor

1. **Theoretical bound at the operating π=0.5 is not informatively tight.** Theorem 4.1 gives ERR_in ≤ 0.5 + concentration terms at π=0.5. This guarantees no more than 50% of InD samples are misclassified — which is mathematically sound but does not distinguish Medix from a random filter. The paper's rhetoric ("provably low error rate," "guarantees minimal error") overstates the practical informativeness of this bound. The bound is a legitimate first theoretical step but does not explain Medix's strong empirical performance, which is substantially better (e.g., 12.5% error in the 2D experiment). Similarly, Theorem 4.2's separation condition ||μ_out − ∇̄_in||₂ ≥ Δ√d scales with the square root of the gradient dimension d (which is large for neural network features), making the bound useful only when OOD is very distinct from InD — precisely when the problem is easiest.

2. **Computational cost of the greedy algorithm is a practical concern not addressed in the main text.** Algorithm 1 requires, at each iteration, computing the element-wise median of gradients for all remaining samples and then for each leave-one-out subset. Since the EWM is not a linear function, EWM(G_{S\{i}}) cannot be derived from EWM(G_S) efficiently — it requires recomputation. The per-iteration complexity is O(|S|²·d) where |S| starts at 50,000. The paper defers efficiency analysis to Appendix A.6 but claims "efficiency" of the algorithm in the introduction (line 25). This computational profile should be acknowledged in the main text and contextualized against simpler alternatives like WOODS (which uses a single training run).

3. **Greedy algorithm's optimality gap is uncharacterized.** The paper formulates an optimization problem (Equation 4: find the subset S that minimizes distance between its EWM and the InD reference gradient) and then replaces it with a greedy leave-one-out heuristic (Algorithm 1) without any analysis of approximation guarantees. For a paper that provides theoretical bounds on the filtering *outcome*, the absence of any analysis connecting the algorithm's output to the optimal solution of Equation 4 is a gap between the theory and the actual method.

4. **2D synthetic experiment is not a meaningful corroboration of the theory.** The synthetic experiment (Figure 2) places the OOD cluster at mean [20, 2√3] while InD clusters are centered at [-2,0], [2,0], [0, 2√3] with covariance 0.25·I — the OOD points are ~18 standard deviations from the nearest InD cluster. This is a trivially separable setting. The paper frames this as "corroborating our theoretical findings" (C3, line 33), but the theory concerns gradient-based filtering on high-dimensional neural network features, not 2D coordinates. The experiment is explicitly described as a "simple" visualization, so the overclaim is modest, but it should be removed or recalibrated.

5. **Missing reporting of extracted set size.** The paper does not report how many samples Algorithm 1 typically flags as outliers. At π=0.5, the true OOD count is ~25,000, but the extracted set could be substantially different. This affects whether Stage 2 training is balanced or imbalanced, which is relevant for interpreting the OOD detector's performance.

### Trivial

- The "40.98% improvement" over KNN+ (line 27) is an absolute percentage-point difference (46.40 − 5.42 = 40.98), not a relative improvement. Standard ML convention would use "40.98 percentage points" to avoid ambiguity. The CIFAR-10 relative improvement over WOODS (76.5%) is actually far more impressive than the "2.60%" absolute difference typically reported.

- The sigmoid surrogate loss for Equation 5 is mentioned in prose (line 128) but never formalized. Providing the exact surrogate loss function would improve reproducibility.

## Nice-to-Haves

- Present the unseen-OOD experiment (P_out^test ≠ P_out) in the main text, not just in the appendix. This directly addresses the open-world framing gap.
- Provide wall-clock time or FLOPs comparison against WOODS and DRL to contextualize the computational cost.
- Analyze failure cases: when does the greedy algorithm extract the wrong samples? This would deepen the contribution more than adding another benchmark.
- Ablate sensitivity to the k hyperparameter in the main text rather than the appendix.

## Removed Points

These points were flagged in the input review but are removed for the following reasons:

- **"KNN+ baseline not a fair comparison on CIFAR-100"** — The paper includes KNN+ as one of 20 baselines, consistently with the literature. KNN+ is a standard reference; showing improvement over it is standard practice. The relevant comparison (against wild-data methods like WOODS) is also reported. Not a weakness.
- **"The 2D synthetic experiment does not provide strong evidence for the method's effectiveness on high-dimensional image data"** — The paper explicitly says "This simulation is designed to be simple to facilitate better understanding." The criticism is technically correct but misinterprets the experiment's purpose. I have retained a softer version of this point (Minor #4) about the overclaim that it "corroborates our theoretical findings."
- **General speculation about what the appendix may or may not contain** — E.g., "the appendix *may* specify X but…" These are not anchored to the paper as written.

## Novel Insights

The input review's most valuable observation is that the framing of Medix as an "open-world" method overstates what the main experiments actually test (the wild-data OOD setting where training and test OOD distributions coincide). This forces a useful question: would Medix's margin over basides shrink, hold, or grow when the wild and test OOD distributions differ? The paper's own answer (Appendix A.4 claims "Medix outperforms baselines by a significant margin") suggests the method may have genuine open-world capability — but this result should be promoted to the main text before the claims can be substantiated. A second valuable observation is the disconnect between the theoretical bound (≤50% error at π=0.5) and the rhetoric of "provably low error rate," which points to a calibration issue in how theory is presented: the bounds are mathematically interesting but not practically informative at the operating regime.

## Suggestions

1. **Promote the unseen-OOD experiment (Appendix A.4) to the main text or recalibrate the "open-world" claims.** If Medix truly outperforms baselines when P_out^test ≠ P_out, this is the strongest evidence for the paper's framing and should be front and center. If not, the claims need to be adjusted to match the standard wild-data OOD setting that is actually evaluated.

2. **Acknowledge the bound's looseness explicitly and discuss its role.** The statement "provably low error rate" (abstract, conclusion) is misleading at π=0.5 where the worst case is 50%. Reframe as: "provably bounded misclassification with explicit dependence on contamination ratio — guaranteeing correctness in expectation, while empirical performance is substantially better."

3. **Report runtime or FLOPs in the main text.** The computational cost of Algorithm 1 (greedy leave-one-out EWM computation over 50,000 samples) is a practical concern that deserves at least a paragraph, not just a deferred appendix.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>