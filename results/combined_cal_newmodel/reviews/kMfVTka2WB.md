## Summary

This paper argues that standard SVM's equal-margin allocation is suboptimal when classes have different covariance structures. It proposes Covariance-Adjusted SVM (CSVM): use class-specific Cholesky decomposition to whiten each class separately, run linear SVM on the transformed data, and adjust the decision boundary's offset in the original space. An iterative self-training procedure (SM Algorithm) is introduced to estimate class covariance matrices when test labels are unknown. Experiments on five datasets compare CSVM against standard SVM kernels and PCA/ZCA whitening.

## Strengths

- **The problem framing is legitimate.** Standard SVM's equal-margin allocation does ignore class-specific covariance structure, which can be suboptimal when class dispersions differ substantially. The paper correctly identifies this limitation and grounds it in prior literature (Tsang et al. 2006, Peng & Xu 2012, Wang et al. 2007, Zafeiriou et al. 2007).
- **The algebraic connection between Mahalanobis distance and Euclidean distance via Cholesky decomposition** (Section 2, Equations 1–3) is mechanically correct and clearly presented.

## Weaknesses

### Major

- **The theoretical derivation in Section 2 is internally inconsistent.** Equations (10)–(13) present two different optimization objectives (minimize ½θᵀΣ₁⁻¹θ vs. minimize ½θᵀΣ_{-1}⁻¹θ) for the **same** parameter vector θ. These cannot be simultaneously minimized unless Σ₁ = Σ_{-1}, which the paper argues is not the case. Lemma 2.2 (claiming two unique classifiers for binary problems) follows from this contradictory setup. Yet the paper's own SM Algorithm does not actually solve both problems — it solves one standard SVM on transformed data and adjusts θ₀. The theoretical apparatus does not coherently support the algorithm, and the claimed "two classifiers" result is contradicted by the paper's own implementation.

- **Lemma 2.3 asserts that "KKT boundary conditions are not valid" in the input space** with the sole justification being that the margin depends on covariance. This is a non-sequitur: KKT conditions apply to constrained optimization problems in any inner product space, and the paper never demonstrates why or how they would fail. This unsubstantiated claim inflates the paper's contribution and misrepresents the nature of the technical challenge.

- **The empirical evaluation lacks basic statistical rigor.**
  - **(a)** Only a single 80/20 train-test split is used, with no replication, no confidence intervals, and no standard deviations reported for any metric in Tables 1–4.
  - **(b)** Baselines (RBF, polynomial, sigmoid SVM) are not tuned. No hyperparameter selection (C, γ, degree) is reported. The fact that linear SVM beats RBF on several datasets (Breast Cancer: 0.956 vs 0.947; Red Wine: 0.731 vs 0.650) strongly suggests baselines were improperly configured, making the comparison uninformative.
  - **(c)** None of the six cited prior methods that incorporate covariance into SVM (Tsang et al. 2006, Peng & Xu 2012, Ke et al. 2018, Huang et al. 2004, Wang et al. 2007, Zafeiriou et al. 2007) are included as baselines, even though the paper claims to "address the limitations" of these studies.
  - **(d)** Reported improvements are marginal (Δ = 0.002–0.026 on accuracy, e.g., Pulsar: 0.981 vs 0.979) and could plausibly fall within the noise of a single split.

- **The SM Algorithm is a heuristic self-training/transductive procedure** presented as a principled covariance estimation method. It has no convergence guarantees; its convergence criterion ("changes in test data labels are below a certain threshold") is underspecified with no threshold value; no analysis of error propagation is provided (self-training is known to reinforce initial errors); and the algorithm requires access to test data during training (transductive) with no description of how to handle genuinely new test points at inference time.

### Minor

- **Dataset characteristics are not reported.** Sample sizes, number of features, and class balance are absent for all five datasets, making it difficult to assess generalizability or whether the method's assumptions (e.g., non-singular covariance matrices for Cholesky decomposition) are satisfied.
- **No ablation study** isolates the contribution of the two claimed novel components: class-specific Cholesky whitening vs. the SM iterative algorithm vs. standard linear SVM on globally whitened data. Without this, the source of any reported improvement is unclear.
- **The computational complexity trade-off** is raised by the authors themselves but is not quantified — no wall-clock time or asymptotic complexity comparison is provided.

### Trivial

None.

## Nice-to-Haves

- If the derivation were corrected, a comparison against the most directly comparable prior methods (MCVSVM, Mahalanobis TSVM, weighted Mahalanobis distance kernels) would substantially strengthen the paper.
- Repeated stratified train-test splits with standard deviations and properly tuned baselines would make the empirical results interpretable.

## Removed Points

- **Strength: "Paper is clearly written"** — generic/superficial praise lacking specific discriminating evidence. Removed per policy.
- **Criticism about missing appendix/proofs in appendix** — these sections are stripped by the parser; they exist in the original submission. Removed per policy.
- **Criticism questioning whether cited models/datasets exist** — all cited references are assumed to exist. Removed per policy.
- **Formatting/style nitpicks** — parser artifacts, not author errors. Removed per policy.

## Novel Insights

None beyond the paper's own contributions. The combined review confirms that the core idea (class-conditional whitening + linear SVM) is a known preprocessing strategy, and the claimed theoretical advances (the non-Euclidean space argument, the two-classifier result, KKT invalidity) are either incorrect or artifacts of a confused derivation. The paper's actual algorithmic contribution is a transductive self-training procedure with no convergence guarantees and an underspecified stopping criterion.

## Suggestions

1. **Resolve the derivation inconsistency.** Either (a) derive a single unified optimization problem that incorporates both class covariances, or (b) transparently present the method as: whiten each class separately via Cholesky → run standard SVM on transformed data → reverse-transform the decision boundary and adjust θ₀ using the margin ratio. Do not claim multiple classifiers when the algorithm produces one.
2. **Benchmark against cited prior work.** Include MCVSVM (Zafeiriou et al. 2007), Mahalanobis TSVM (Peng & Xu 2012), and weighted Mahalanobis distance kernels (Wang et al. 2007) as baselines.
3. **Provide a statistically rigorous evaluation.** Use repeated stratified splits (e.g., 10 runs) with means and standard deviations. Tune all baselines (C, γ, degree) using the same procedure. Report dataset sizes, feature counts, and class balance.
4. **Specify the SM Algorithm's convergence threshold** and analyze its behavior (e.g., sensitivity to initialization, typical iteration count, error propagation in the self-training loop).

## Score and Decision

### Calibration Anchors

| Anchor Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| `ZDoaLbOFaP.md` (Sparse Covariance Neural Networks) | 3.00 | R1 | Yes | Sound theory and experiments but incremental; our paper has *structural* mathematical errors that are more fundamental. |
| `anek0q7QPL.md` (Covariance + Hessian Eigenanalysis) | 5.00 | R1 | Yes | Methodologically more rigorous with formal proofs; our paper lacks comparable rigor. |
| `bwOndfohRK.md` (Neural Networks on Symmetric Spaces) | 6.00 | R1 | Yes | Well-developed theoretical framework with diverse experiments; our paper is much weaker on both theory and evaluation. |
| `qcyn7ESaM8.md` (Bridging PCA and Neural Networks) | 2.50 | R2 | Yes | Limited novelty and unclear presentation but no mathematical errors; our paper's inconsistent derivation is a more serious flaw. |
| `ZINaxJyoQr.md` (Why Barlow Twins Work) | 1.50 | R2 | Yes | Essentially incomplete (no experiments); our paper at least presents a runnable algorithm, so it is not this weak. |
| `WVIq7jYIda.md` (Manifold Kernel Rank Reduced Regression) | 3.00 | R1 | No | Similar score range but different topic. |
| `NYPJz0CL5X.md` (Optimal Hyperdimensional Representation) | 3.00 | R1 | No | Different topic. |
| `ClixrtIHUJ.md` (Language Models as Feature Extractors) | 5.25 | R1 | No | Uses Mahalanobis distance for continual learning; stronger empirical methodology. |

### Bracket and Narrowing

**Round 1 bracket:** 1.5–3.5 (given the paper's theoretical inconsistencies and weak evaluation, it clearly falls below the 3.5 threshold of borderline-acceptable papers).

**Round 2 narrowing:** Comparing itemized favorability ratings, our paper's most negative item (missing prior work baselines, favorability = −1.91) is less extreme than the 2.5–3.0 anchors' most negative items (which reach −3.1 to −3.6). However, those anchors' negative items concern *incremental novelty* and *presentation quality*, whereas our paper's negative items concern a *mathematically inconsistent derivation* and *unsupported central claims* — qualitatively more severe flaws. The 2.5-rated paper (Bridging PCA) had no mathematical errors. Our paper's theoretical apparatus is not merely incremental; it is self-contradictory. This places it below 2.5. The 1.5-rated paper (Barlow Twins) was essentially incomplete with no empirical validation; our paper does present a working algorithm with some experimental results, so it is not at the 1.5 level.

### Final Score

**2.0** — The paper identifies a legitimate problem but its core theoretical derivation is mathematically inconsistent (two contradictory optimization objectives for the same parameter vector), its central claims about KKT invalidity are stated without proof, its empirical evaluation lacks the most basic statistical rigor (single split, no error bars, untuned baselines, no comparison against the relevant prior work it claims to improve upon), and the proposed SM Algorithm is an underspecified heuristic with no convergence analysis. These issues are structural, not fixable by additional experiments alone.

**Decision: Reject**

MY FINAL SCORE: <score>2.0</score>
MY FINAL DECISION: <decision>Reject</decision>