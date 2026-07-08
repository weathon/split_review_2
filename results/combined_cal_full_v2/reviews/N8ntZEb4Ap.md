Now let me compile the final review.

## Summary

This paper proposes AutoNFS, a neural feature selection method that uses a Gumbel-Sigmoid mask with a cardinality penalty to automatically determine both which features to select and how many to retain. The method consists of a masking network (producing a feature mask from a learned embedding) and a task network (evaluating selected features on the downstream task), trained end-to-end. The paper evaluates AutoNFS on 11 OpenML benchmark datasets under three corruption scenarios (random, Gaussian-corrupted, second-order features) and 24 real metagenomic datasets, comparing against 10 FS methods.

## Strengths

- **Well-motivated and clean idea.** The paper identifies a genuine practical pain point: many feature selection methods require the user to pre-specify the number of features to retain, which is expensive and dataset-dependent. AutoNFS's core idea — learning the cardinality automatically via a regularized Gumbel-Sigmoid mask — is sensibly motivated and clearly presented. (Evidence: lines 16, 28-29, 82-89)

- **Compelling real-world evidence from metagenomic data.** Across 24 real biological datasets, AutoNFS reduces dimensionality from an average of 535 to 41 features (7.7%) while maintaining or slightly improving predictive performance (MLP: +0.7 pp, RF: +1.2 pp on average). This is a concrete demonstration that the method can produce sparse, practically useful feature subsets on challenging high-dimensional data. (Evidence: Table 2, lines 214-258)

- **Strong noise rejection.** AutoNFS achieves zero misselection errors for random and corrupted feature scenarios (Figure 3a), meaning it perfectly identifies and discards the artificial noise features. This provides direct evidence that the selection mechanism works as intended. (Evidence: lines 206-207)

- **Broad evaluation framework.** The evaluation follows the well-established Cherepanova et al. (2023) benchmark with three corruption scenarios and compares against 10 methods including both classical (Lasso, ANOVA, Mutual Information, RFE, Random Forest) and neural (LassoNet, Deep Lasso, Attention-based) FS approaches. (Evidence: lines 194-200)

## Weaknesses

### Major

- **The near-constant complexity claim (α ≈ 0.08) is not adequately explained.** The paper asserts in the abstract and as a bullet contribution that AutoNFS achieves "nearly constant computational overhead regardless of input dimensionality." The masking network *f* outputs a *D*-dimensional vector, so its forward pass must involve at least *O(D)* operations (even a single linear layer from ℝ^{D_e} to ℝ^D requires D×D_e multiply-adds). The empirical finding that wall-clock time scales as *t ∝ D^{0.08}* (Figure 4b) would mean that increasing features by 100× increases runtime by only ~1.45×, yet the paper offers no explanation for this behavior. Plausible explanations exist (e.g., the task network's forward pass dominates at all scales; GPU kernel launch overhead; a fixed-size bottleneck in *f*), but none are discussed. Since this is one of the three bullet contributions, the lack of any explanatory analysis is a significant gap. (Evidence: lines 22, 29, 58, 275-279)

- **The main benchmark comparison conflates cardinality determination with selection quality.** The paper states explicitly: "all baseline methods select the same number of features as were in the initial representation (before corruption), whereas our method automatically chooses a much smaller subset" (line 204). This means baselines are forced to select *D* features (the pre-corruption dimensionality; e.g., 128 for aloi) while AutoNFS selects fewer (e.g., 65 for aloi). The comparison therefore tests both cardinality-determination and selection-quality simultaneously, without isolating which drives the performance difference. The headline claim "consistently outperforms" is partially confounded — the results show AutoNFS outperforms methods *handicapped by a fixed feature budget*. A controlled experiment fixing the feature count across methods, or sweeping the budget for baselines, is needed to separate these effects. (Evidence: line 204, Table 1 RHS)

### Minor

- **Naming inconsistency.** The method is called "AutoNFS" throughout the text but appears as "GFS-NetWork" in Figure 2 captions, tables, and Figure 4 legends. The alt-text in Figure 2 says "AutoNFS (GFS-NetWork)." While likely a simple renaming artifact, this creates confusion. (Evidence: lines 151, 165, 265, 271)

- **Masking network architecture under-specified.** The embedding dimension *D_e*, the number of layers, hidden dimensions, and activation functions of the masking network *f* are not given in the main text. These may appear in the stripped appendix, but the main text should provide sufficient detail for basic reproducibility assessment. (Evidence: line 62)

- **λ sensitivity not shown in main text.** The paper claims λ=1 works universally across datasets (line 89) but relegates the sensitivity analysis to Appendix F. Since λ directly controls the sparsity-accuracy trade-off, its impact is central to understanding the method's behavior. (Evidence: lines 85-89)

- **Benchmark datasets are not high-dimensional.** The OpenML datasets have only 8–136 original features (Table 1). The paper's claims about high-dimensional scalability are supported mainly by the synthetic complexity experiment (Figure 4), not by FS performance on high-dimensional tabular tasks. The metagenomic data (308–718 features) partially addresses this but is still moderate by modern standards. (Evidence: Table 1)

- **No variance or error bars on main benchmark results.** Figure 2 shows only point estimates of average rank across datasets. Given that the Gumbel noise injects randomness, single-run results are insufficient to assess stability. The complexity analysis (Figure 4b) does report 5-run confidence intervals, making this omission in the main results notable. (Evidence: Figure 2 vs Figure 4b)

- **Complexity comparison omits other neural FS methods.** The complexity analysis (Figure 4) compares AutoNFS against classical methods (ANOVA, Mutual Information, RF, RFE, Delete2Vec) but not against other differentiable neural FS methods (STG, LassoNet, Concrete Autoencoders, Deep Lasso) that also benefit from GPU minibatch training. This makes it unclear whether the scaling advantage is specific to AutoNFS's design or general to neural FS. (Evidence: Figure 4, lines 275-279)

- **Metagenomic improvements are modest with no significance reported.** The average improvements over "full data" are 0.7 pp (MLP) and 1.2 pp (RF). Several individual datasets show performance degradation (e.g., FengQ_2015: 0.662→0.607 for MLP; YachidaS_2019: 0.636→0.608 for RF). No statistical significance is reported. (Evidence: Table 2)

### Trivial

None.

## Nice-to-Haves

- Run a controlled experiment where baselines are forced to select the same number of features as AutoNFS, or sweep the feature budget for baselines, to isolate selection quality from cardinality determination.
- Include at least one differentiable neural FS method (STG or LassoNet) in the complexity comparison.
- Add λ sensitivity analysis to the main text.
- Report variance/confidence intervals on the main benchmark results.
- Unify the method name (AutoNFS vs GFS-NetWork) throughout the paper.

## Removed Points

These points from the input review were removed with justification:
- **"Complexity scaling is physically implausible"** — softened to "not adequately explained" because plausible explanations exist (task network dominance, GPU overhead) and the issue is lack of explanation, not physical impossibility.
- **"Paper and experiments may be misaligned due to naming"** — pure speculation beyond the observed naming inconsistency; removed.
- **Missing hyperparameters (η₁, η₂, E, B)** — likely in the stripped Appendix C; cannot verify absence.
- **"No ablation of masking network architecture"** — could be in stripped appendix; a nice-to-have rather than a core flaw.
- **Demand for comparison with dynamic feature acquisition methods** — outside the paper's stated scope (line 44: "they solve a different problem than ours").
- **"STG and LassoNet also learn sparsity automatically"** — the paper acknowledges this in Section 2 (lines 36-38); the criticism about insufficient differentiation is reasonable but addressed in part.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Provide a theoretical or empirical breakdown of where the α ≈ 0.08 scaling comes from: profile the masking network vs. task network compute, and report whether the measurement is dominated by GPU kernel launch overhead at small *D*.
2. Run a head-to-head comparison where all methods select the same number of features, to disentangle cardinality-determination from selection quality. This would make the "consistently outperforms" claim much more interpretable.
3. Report variance over at least 5 random seeds for all main benchmark results.
4. Include at least one differentiable neural FS baseline (STG or LassoNet) in the complexity scaling experiment.
5. Move the λ sensitivity analysis from the appendix to the main text, or at least summarize key findings.

## Score and Decision

### Calibration Anchors

| Filepath | Avg Score | Round | Itemized? | Comparison |
|----------|-----------|-------|-----------|------------|
| lt6xKGGWov.md (Neural MI FS) | 2.33 | 1 | No | Much weaker: only synthetic experiments; our paper clearly stronger. |
| PauyrluLud.md (Band Selection, Gumbel-Softmax) | 4.00 | 1 | No | Topically similar, uses Gumbel-Softmax for selection. Our paper has more extensive experiments and clearer motivation. |
| 3M3jtMDjUb.md (RelChaNet) | 5.25 | 1,2 | Yes | Neural FS with strong empirical outperformance. Our paper has comparable experimental breadth but weaker head-to-head claims. |
| Ai4L058yoO.md (Unsupervised FS) | 4.50 | 2 | Yes | Dynamic FS with significant writing/technical issues. Our paper is better presented. |

**Bracketing (Round 1):** The most similar papers (RelChaNet at 5.25, Band Selection at 4.00) suggest the paper sits in the 4.0–5.5 range. It is clearly stronger than the Neural MI paper (2.33) but less compelling than RelChaNet (5.25), which had stronger novelty and cleaner empirical comparisons.

**Narrowing (Round 2):** Comparing weighted items: RelChaNet's strongest items (novelty at weight=10.06, "outperforms 7/9 datasets" at weight=8.54) exceed our paper's strongest items (practical motivation at 9.06, metagenomic results at 8.21). Conversely, our two Major weaknesses (complexity claim not explained at weight=3.53, confounded comparison at weight=1.57) are genuine threats to the headline claims. The band selection paper (4.00) had more severe weaknesses but a similar technical approach. Our paper improves on it in experimental scope and motivation quality but shares its under-specification issues.

**Final calibration:** The paper's core idea is sound and the metagenomic results are valuable, but the two Major weaknesses directly affect the abstract's and contributions' strongest claims ("nearly constant computational overhead," "consistently outperforms"). The comparison protocol issue means we cannot tell whether AutoNFS selects better features or just benefits from a more favorable feature budget. The complexity result is asserted without explanation. These problems are significant enough to place the paper below the acceptance threshold but above papers with fatal methodological flaws or no real-data experiments.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>