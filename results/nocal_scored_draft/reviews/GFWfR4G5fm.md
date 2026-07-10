Now I have all the information needed. Let me compose the final consolidated review.

---

## Summary

This paper identifies fundamental limitations of static pre-training in Supervised Causal Learning (SCL)—fragility to distribution shifts, failure in compositional generalization, and a performance gap between synthetic benchmarks and real-world data—and proposes Test-Time Training for SCL (TTT-SCL) as a paradigm shift. The key idea is to dynamically generate training data aligned to each test instance rather than relying on a fixed pre-training set. The paper instantiates this framework as TACTIC, which combines a distribution-alignment metric (AD) with sparsity constraints in a stochastic graph refinement search, then trains an SCL model on the generated data. Experiments across synthetic, pseudo-real, and real-world datasets show substantial improvements over existing methods.

## Strengths

- **The diagnostic study (Section 3) is well-executed and makes a clear independent contribution.** The factorial design across graph structure, mechanism, and noise dimensions, together with the "Component-mixed" condition that tests compositional generalization, is a principled way to expose limitations of static SCL pre-training. The finding that models memorize specific (G, f, ε) configurations rather than learning modular causal representations is concrete and actionable. This diagnosis is arguably as significant as the proposed method.

- **The core idea — generating test-time training data aligned to the test instance — is genuinely novel in the SCL context.** Prior work (Montagna et al., 2024) attributes SCL generalization failures to insufficient diversity solvable by scaling up pre-training. This paper correctly identifies compositional generalization as a deeper problem that cannot be fixed by any finite static training set. The shift from "diversity" to "concentration" as a design principle is a conceptually clear reframing.

- **The two-stage analysis (Table 4) is informative and honestly presented.** Showing the seed graph AUROC, the highest-scoring graph from search, and the final SCL prediction separately allows the reader to see that both the search (1→2) and the learning (2→3) stages contribute. This provides the strongest evidence that the SCL training phase adds value beyond what the score-based objective already captures.

## Weaknesses

### Fatal
None.

### Major

- **Missing error bars for real-world results (Sachs, Syntren) across Tables 1–3.** The paper states results are "presented as AUROC (standard deviation)" but reports only single numbers for these datasets, while synthetic results consistently include standard deviations. For a method involving stochastic graph refinement, forward-sampling with random seeds, and neural network training with random initialization, variance estimates are essential to assess statistical reliability. The reported improvements (78.9 vs. 67.1 for PC on Sachs; 80.1 vs. 65.4 for AVICI on Syntren) are large, but without variance the reader cannot evaluate whether these reflect genuine advantages or favorable single runs. This is the most significant evidential gap in the paper.

### Minor

- **The SCL model architecture used within TACTIC is not specified.** Section 4.2 step 3 states "An SCL model is then trained on this set and applied to infer G_test" without identifying the architecture. The diagnostic study (Section 3.1) uses AVICI as the backbone, but whether TACTIC also uses the AVICI architecture (retrained from scratch) or a different architecture is unclear. This affects reproducibility and the interpretability of comparisons against the pre-trained AVICI (scm-v0) baseline.

- **The ablation study (Section 4.4) only tests removal of the sparsity term** (by setting λ=0) but does not ablate the AD component. The paper claims "both AD and sparsity are indispensable" but provides direct evidence only for sparsity.

- **Hyperparameter λ is not reported and K=200 is not justified.** λ (Eq. 5) balances AD and sparsity but its value in the main experiments is not given and no sensitivity analysis is provided. The choice of K=200 training graphs is stated without rationale or ablation.

- **The "Component-mixed" training condition (Section 3.1) is described only conceptually** ("contains all individual components...but excludes the specific combinations present in the test instances") without specifying the exact training distribution — which combinations are included and which are held out. This limits the reader's ability to assess the strength of the compositional generalization test.

### Trivial
None.

## Nice-to-Haves

- **Control experiment with misaligned training data:** The SCL model within TACTIC is trained on data whose mechanisms are fit from D_test itself. An informative control would be: use the same candidate graphs but regenerate training data with mechanisms fit from a *different* dataset (or random mechanisms) and compare performance. If performance drops substantially, this confirms that distributional alignment is the active ingredient. The paper partially addresses this by setting noise to N(0,1) (creating a distributional gap), but a mechanism-level control would substantiate the claimed mechanism of action.

- **Direct comparison against a score-based method optimizing Eq. (5):** While the paper includes GES as a baseline (Table 2) and provides the stage-wise analysis (Table 4), a cleaner separation would be to run a dedicated search (e.g., GES-style) on Eq. (5) directly and use its output as the final prediction. This would sharpen the distinction between what the scoring function alone can achieve and what the SCL training phase additionally provides.

- **Computational cost in the main text:** The paper defers runtime analysis to Appendix F. A brief mention in the main text (e.g., wall-clock time for Sachs with d=11) would help readers assess practical usability.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

1. "Internal logic raises question about what is being learned (transductive learning concern)" — The concern is framed as speculation ("could represent...or could reflect...") rather than an identified error. The paper provides Table 4 showing SCL improvement over score-based search and acknowledges the N(0,1) noise gap. Moved to Nice-to-Haves as a suggested control experiment.

2. "No comparison against a score-based method using the same objective" — The paper already includes GES as a baseline and provides stage-wise analysis demonstrating added value. Moved to Nice-to-Haves.

3. "AD metric assumes additive noise" — The paper explicitly states applicability under ANM, LiNGAM, or PNL assumptions, directly addressing this concern. Removed.

4. "Computational cost deferred to Appendix F" — The appendix is stripped by the parser; the paper does reference complexity analysis there. Per filtering rules, criticisms about missing appendix content are removed.

5. Pure formatting nitpicks and editorial suggestions — removed per filtering rules.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Run TACTIC at least 5 times on Sachs and Syntren with different random seeds and report mean ± standard deviation. This is the single highest-impact improvement for the paper's credibility.
2. Explicitly state the SCL model architecture used within TACTIC in Section 4.2 step 3.
3. Add an ablation replacing AD with an alternative metric (e.g., MMD) to substantiate the claim that AD is indispensable.
4. Report the value of λ used in main experiments and add a sensitivity analysis showing performance as λ varies.
5. Provide a brief ablation for K (e.g., K=50, 100, 200, 500) to justify the choice.
6. Consider the misaligned-mechanism control experiment described in Nice-to-Haves.

## Score and Decision

The paper makes a genuine contribution: the diagnostic study is well-executed and independently valuable, the TTT-SCL framework is conceptually novel and clearly motivated, and TACTIC shows large and consistent improvements across multiple datasets. The primary weakness — missing error bars for real-world data — is significant but addressable, and the improvement margins are large enough that the core findings are unlikely to be overturned by variance. On balance, the paper merits acceptance.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>