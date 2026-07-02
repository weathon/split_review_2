Now let me produce the final consolidated review.

## Summary

This paper proposes AutoNFS, a differentiable neural feature selection method that uses Gumbel-Sigmoid relaxation to learn a continuous mask jointly with a task network. The key claimed advantages are: (1) it automatically determines the number of features to select rather than requiring a user-specified feature budget, and (2) its runtime remains nearly constant as input dimensionality grows. Experiments on 11 OpenML benchmark datasets (with three corruption scenarios) and 24 real-world metagenomic datasets show competitive predictive performance while selecting far fewer features than baselines.

## Strengths

- **Automatic feature-count discovery is a genuine practical advantage.** Most differentiable FS methods (STG, Hard-Concrete, LassoNet) require the user to specify the sparsity level or feature budget as a hyperparameter. AutoNFS lets the feature count emerge from optimization via a simple cardinality penalty (ℒ_select, Eq. 2) with λ=1 fixed across all datasets. Sections 3.3–3.4 describe this mechanism cleanly, and Table 1 (RHS) shows the method selects substantially fewer features than the original dimensionality across all 11 datasets.

- **The complexity analysis (Figure 4) is striking and well-executed.** The empirical finding that AutoNFS exhibits near-constant wall-clock time scaling (α≈0.08) across five orders of magnitude of feature dimensionality (10² to 10⁵), while standard methods scale linearly or worse, is a genuinely novel and interesting result. Confidence intervals over 5 runs (Figure 4b) add credibility.

- **Evaluation on 24 real-world metagenomic datasets (Table 2) provides meaningful validation.** High-dimensional biological data is a natural and important application for FS. AutoNFS reduces dimensionality to 7.7% of original while maintaining average predictive performance (MLP: 0.588→0.596, RF: 0.685→0.697)—a practically meaningful result. The per-dataset results are individually reported, enabling readers to inspect the full distribution.

- **Misselection analysis (Figure 3a) is informative.** Showing that AutoNFS achieves zero misselection errors for random and corrupted features, and that its second-order feature selections sometimes capture more information than the original attributes, demonstrates nuanced understanding of the selection behavior.

## Weaknesses

### Fatal

None.

### Major

- **The most directly comparable differentiable FS baselines are absent from experiments.** The Related Work (Section 2) discusses Hard-Concrete gates (Louizos et al., 2017), Stochastic Gates / STG (Yamada et al., 2020b), Concrete Autoencoders (Balin et al., 2019), and INVASE (Yoon et al., 2018) as the closest prior work—all sharing AutoNFS's core approach of learning a continuous relaxation of a discrete selection mask via gradient descent. Yet *none* of these appear in the experimental comparison (Figure 2, Tables 3–5). The baselines that do appear are predominantly classical or tree-based methods, plus LassoNet and Deep Lasso. The abstract claims AutoNFS "consistently outperforms both the classical and neural FS methods," but without STG and Hard-Concrete—arguably the most relevant differentiable neural competitors—this claim is not fully substantiated for the methods in AutoNFS's own technical lineage. The authors should either add these comparisons or appropriately scope the claim.

### Minor

- **No statistical significance assessment for ranking results.** Figure 2 reports average ranks across 11 datasets under 3 scenarios. For the "Random" scenario, AutoNFS has rank 3.9 vs. Deep Lasso at 4.3—a gap of only 0.4 ranking points. With only 11 datasets and 11 methods, this difference may fall within random variation. The paper does not report a Friedman test, Nemenyi post-hoc analysis, or any significance assessment. This gap affects the interpretability of the primary experimental results.

- **Per-dataset degradation in metagenomic results is not discussed.** The paper states that "AutoNFS maintains predictive performance" on average (line 216), but Table 2 shows substantial degradation on several individual datasets: MLP drops from 0.653→0.417 on YuJ_2015 (−0.236), 0.733→0.567 on ThomasAM_2018a (−0.166), 0.469→0.344 on KeohaneDM_2020 (−0.125), and 0.657→0.559 on ZhuF_2020 (−0.098). The average is positive, but the framing should acknowledge that dimensionality reduction comes at a meaningful cost on some datasets. Reporting the distribution of accuracy changes (rather than just the average) and discussing why certain datasets see degradation would better inform readers.

- **Discrepancy in ℒ_select normalization between Eq. 2 and Algorithm 1.** Equation 2 (line 83) defines ℒ_select = (1/D)·∑ⱼ mⱼ (normalized by feature count D), but Algorithm 1 line 118 uses ℒ_select ← (1/B)·∑ⱼ mⱼ (normalized by batch size B). These differ and the paper does not explain which is correct or whether the discrepancy matters in practice.

- **Naming inconsistency.** The method is called "AutoNFS" throughout the text but is labeled "GFS-NetWork" in Figure 2 and "GFSNetwork" in Figure 4 captions. The paper never explains what "GFS-NetWork" stands for or why two names are used.

### Trivial

- The masking network architecture (layers, hidden sizes, embedding dimension D_e) is not specified beyond the function signature f: ℝ^{D_e}→ℝ^D (line 62). These are basic reproducibility details.
- Total number of training epochs E is listed as a parameter in Algorithm 1 but its value is not reported in the main text.

## Nice-to-Haves

- A sensitivity analysis for λ (e.g., accuracy vs. feature count for λ∈{0.1, 0.5, 1, 2, 5} on 2–3 datasets) brought into the main text would increase confidence in the claim that λ=1 works universally. (The paper references Appendix F for this analysis.)
- Explicitly acknowledging that the masking network is essentially a lightweight learned transformation (which explains the near-constant runtime) would strengthen the framing—the simplicity is a virtue.
- Clarifying the temperature schedule: with τ₀=2.0 and α=0.997, after E epochs the temperature is τ=2.0×0.997ᴱ. Reporting E would allow readers to determine whether masks are sufficiently binary by training end.

## Removed Points

- **Speculation about unfair baseline selection procedure.** The harsh reviewer questioned whether "all baseline methods select the same number of features as were in the initial representation (before corruption)" (line 204) implies baselines know which features are original. Re-reading the paper, this means baselines are told to select k features where k = original D—a standard benchmark setup that, if anything, gives baselines *more* features to work with than AutoNFS. This concern was speculative and not supported by evidence in the paper.
- **Generic concerns about evaluation rigor.** Sweeping criticisms without specific anchoring to paper content were removed during filtering.
- **Missing appendix / reference complaints.** The parser strips appendix sections; they exist in the original submission and may contain the details the reviewer requested (λ sensitivity, architecture specifics, etc.).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add STG and Hard-Concrete as experimental baselines. If this is infeasible, revise the abstract and claims to accurately reflect which neural FS methods were compared against.
2. Add statistical significance tests (Friedman + Nemenyi) for the ranking results in Figure 2.
3. Discuss per-dataset variance in Table 2 and acknowledge cases where performance degrades substantially.
4. Resolve the ℒ_select normalization discrepancy between Eq. 2 (1/D) and Algorithm 1 (1/B).
5. Unify the method name (AutoNFS vs. GFS-NetWork) throughout the paper.
6. Report masking network architecture details (layers, D_e) and the total training epoch count.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>