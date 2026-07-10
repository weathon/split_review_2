## Summary

This paper identifies three fundamental limitations of static supervised causal learning (SCL) — fragility under distribution shifts, compositional generalization failure, and a synthetic-to-real performance gap — and proposes a paradigm shift from static pre-training to test-time adaptation. The TTT-SCL framework dynamically generates a customized training set for each test instance using an Alignment of Distribution (AD) metric with sparsity constraints. The instantiation, TACTIC, performs stochastic search over candidate graphs guided by AD and sparsity, generates aligned training data, and trains an SCL model at test time. Results show substantial improvements on real-world (Sachs) and pseudo-real (SynTREn) benchmarks.

## Strengths

- **Section 3 provides a clean, systematic diagnosis of SCL's OOD failures.** The experiments in Fig. 2 and Table 1 convincingly demonstrate that static pre-training suffers from distribution shifts (across graphs, mechanisms, and noise), fails on held-out component combinations ("Component-mixed"), and exhibits a stark synthetic-to-real gap. The compositional generalization failure — showing models memorize specific (G, f, ε) configurations rather than learning modular representations — is a more fundamental diagnosis than prior work's focus on unseen individual components. [impact: +9.9]

- **The TTT-SCL framework is a genuinely novel idea in the causal discovery space.** Applying test-time training to supervised causal learning is structurally different from existing SCL approaches. The AD metric (Eq. 3) with sparsity constraint (Eq. 4) provides a reasonable operationalization of the alignment idea. The framework's motivation — moving from seeking universal diversity to generating targeted concentration — is clearly articulated. [impact: +9.7]

- **The stage-wise analysis in Table 4 cleanly validates the pipeline's logic.** Showing that (a) seed → highest-scoring graph improves via AD-guided search, and (b) highest-scoring graph → final SCL output improves further via supervised learning, provides direct evidence that the SCL training phase adds value beyond what a score-based method alone would produce. This cleanly distinguishes TACTIC from classical score-based causal discovery. [impact: +9.9]

- **The results on Sachs (78.9 AUROC vs. 62.3 AVICI, 67.1 PC) and SynTREn (80.1 vs. 65.4) are substantial improvements on real-world and pseudo-real benchmarks.** These gains directly support the paper's central thesis that test-time adaptation can bridge the synthetic-to-real gap — the paper's key concern. [impact: +10.0]

## Weaknesses

### Major

- **The stochastic graph refinement acceptance criterion is not well-defined and appears to use a non-standard formula.** The text (line 173) states candidates are "accepted with probability proportional to its score," while Figure 3 shows α = min[1, score(G_{k+1})/score(G_k)]. Since score(G) = AD(G) − λ·Sparsity(G) (Eq. 5), where AD is a log-likelihood, the score is typically negative. Using a ratio of two negative scores as an acceptance probability does not correspond to any standard MCMC criterion (where one would expect exp(score_new − score_old) or similar). This is a central component of the method; the ambiguity prevents both reproducibility and evaluation of whether the search procedure behaves as intended. [impact: -10.0]

- **The selection mechanism for the K=200 training graphs is not specified.** The paper states K=200 training graphs are generated (line 192) and refers to "the final refined graph set" (line 174), but never explains which 200 graphs are selected from the stochastic search trajectory — whether they are the top-200 scoring graphs, the last 200 samples from the Markov chain, a thinned chain, or diverse high-scoring graphs. This directly determines the quality of the training set and affects both reproducibility and result interpretation. [impact: -10.0]

- **The AD metric implementation details are underspecified.** Equation (3) defines AD as (1/d) Σ log p(X_i | f_i^k), where f_i^k is "the fitting function" fitted on D_test via SIM. The main text does not specify what regression method is used (linear, neural network, Gaussian process, etc.), how the likelihood log p(X_i | f_i^k) is computed (what noise variance or distributional assumption is used), or whether the in-sample likelihood evaluation creates an overfitting advantage for denser graphs that the sparsity penalty alone resolves. The paper references Appendix A for implementation alternatives, but the main text lacks the specification needed for independent reproduction. [impact: -9.6]

### Minor

- **The empirical claims are somewhat overstated.** The paper claims TACTIC "significantly outperforms existing SCL and traditional causal discovery methods." However, on RFF_G, AVICI (97.8±1.3) significantly beats TACTIC-Notears (91.8±3.1). On Linear_U, TACTIC-Notears (86.3±4.4) overlaps with SCORE (82.2±18.7), NoGAM (79.2±18.6), and NOTEARS (82.0±4.6) within one standard deviation. On Chebyshev_G, TACTIC-Notears (83.0±8.7) overlaps with AVICI (81.7±10.5). The unambiguously strong results are on Sachs and SynTREn — which are important — but the method does not show clear dominance across all settings. [impact: -0.1]

- **The paper defaults to Gaussian noise N(0,1) for generating training data in TACTIC (Step 3, line 174) yet acknowledges Uniform noise is needed for Linear test data "to ensure identifiability" (line 86).** For linear causal models, Gaussian noise makes the model unidentifiable, yet TACTIC generates linear-mechanism training data with Gaussian noise. The tension between the default noise choice and the identifiability assumptions the framework claims to support (LiNGAM, ANM, Post-NonLinear) is not discussed. [impact: -8.9]

- **Only the sparsity term is ablated (Table 3); there is no ablation of the AD term itself** (e.g., AD removed or replaced with a simpler score). The paper claims both AD and sparsity are "indispensable" (line 227) but only demonstrates indispensability for sparsity. [impact: -6.4]

- **The hyperparameter λ (balancing AD and sparsity in Eq. 5) is not stated and no sensitivity analysis is provided.** Given the method's dependence on this tradeoff, this is needed for reproducibility and to assess robustness. [impact: -0.8]

- **The "compositional generalization" framing (Section 3, Issue 2) is somewhat inflated.** The "Component-mixed" condition tests held-out combinations of (mechanism, graph, noise) with a limited design space (6-12 combinations). This is better described as a held-out combination test than "compositional generalization," which typically implies systematic recombination of learned primitives. The experiments are valid but the framing overreaches. [impact: -0.0]

### Trivial

- None beyond the minor issues listed above.

## Nice-to-Haves

- Provide a direct ablation of the AD term (e.g., replacing AD with a simpler baseline score) to demonstrate its indispensability, as is claimed.
- Include a computational cost comparison (time per test instance) in the main text to help readers assess the practical cost of test-time training.
- The paper describes "TTT-SCL" as a framework but presents only one instantiation (TACTIC). Consider framing this more precisely.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **Computational cost being unaddressed**: Removed because the paper explicitly references Appendix F for complexity analysis (hard rule about missing appendices — the appendix exists in the original submission).
- **AD metric overfitting (in-sample likelihood)**: Removed because the sparsity penalty serves as a complexity regularizer analogous to standard practice in score-based causal discovery (BIC, etc.).
- **Missing AVICI fine-tune baseline**: Removed as a nice-to-have rather than a genuine weakness — the paper compares against the strongest pre-trained SCL model available.
- **Style/formatting nitpicks and presentation concerns**: Removed per hard rules.

## Novel Insights

The interplay between the three major weaknesses is notable: the stochastic search uses an acceptance criterion that (as written) does not correspond to any standard MCMC form; yet simultaneously the search output selection (which 200 graphs are kept) is unspecified, and the metric guiding the search (AD) lacks implementation detail. These three gaps together mean the core algorithmic loop of the paper — the mechanism by which training data quality is controlled — is insufficiently defined to be reproducible or fully evaluable. This is a qualitatively different pattern from the typical "missing baseline" or "limited scope" critique: it is a specification failure at the method-definition level. The strengths (problem diagnosis, novel paradigm, real-world results) are real and substantial, but they stand in tension with the fact that the engine driving the method's success is not fully specified.

## Suggestions

1. Specify the exact acceptance criterion for the stochastic search. If it is min[1, exp(score_new − score_old)] (standard Metropolis), state this explicitly and correct Figure 3. If it is something else, provide the formula and justify it.
2. State how the K=200 graphs are selected from the search trajectory (e.g., top-200 by score, last 200, thinned chain).
3. Specify the regression method used for f_i^k and the distributional assumption (noise variance) used in the likelihood computation for AD.
4. Discuss the choice of default Gaussian noise for training data generation and its relationship to the identifiability assumptions of the test domain.
5. Calibrate the empirical claims (e.g., "significantly outperforms" → "achieves competitive or superior performance on several benchmarks, particularly on real-world data").
6. Report the value of λ used and include a sensitivity analysis.
7. Add an ablation of the AD term to support the claim that both components are indispensable.

## Score and Decision

**Calibration procedure.** Round 1 bracketing retrieved 24 calibration anchors across 6 score bands. The most thematically relevant anchors were:

| Anchor Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| lQYi2zeDyh.md (Demystifying amortized CD) | 5.0 | R1 | Yes | Similar domain (SCL analysis); my paper has stronger experiments (multi-variable, real data) but more specification gaps |
| TRHyAnInUC.md (D³PM diffusion CD) | 3.25 | R1 | Yes | My paper is clearly stronger — better motivation, cleaner experiments, real-world validation |
| x3F8oPxKV2.md (Zero-shot SCM learning) | 6.25 | R1 | Yes | Similar specification issues; my paper has stronger real-world validation but the search procedure ambiguity is more central |
| eeJz7eDWKO.md (Meta-learning Bayesian CD) | 6.0 | R1 | Yes | My paper is more novel conceptually but less polished in specification |
| 8GhwePP7vA.md (Feature Matching Intervention) | 4.25 | R2 | No | Weaker experiments, less relevant |
| q07DDpu8Xb.md (Distribution shifts + identifiability) | 5.25 | R2 | No | Theoretical paper, less comparable |

**Bracket.** Round 1 placed the paper in the 4.0–6.0 range. Round 2 narrowing confirmed the closest comparator is lQYi2zeDyh.md (avg 5.0), which shares the SCL analysis focus but lacks real-world validation and multi-variable experiments that my paper provides. However, that anchor paper's method was clearly specified, whereas my paper has three high-severity specification gaps (transition probability, graph selection, AD details) at the core of its algorithmic loop.

**Final placement.** The paper has genuine high-magnitude strengths (problem diagnosis: +9.9, novel paradigm: +9.7, real-world results: +10.0, stage-wise validation: +9.9) that are comparable to or exceed those of the 5.0–6.0 anchors. However, it also has multiple major specification gaps at the method-definition level (acceptance criterion: -10.0, graph selection: -10.0, AD details: -9.6) that are more central to the paper's contribution than the specification issues seen in the 6.0+ anchors. These gaps are fixable but currently prevent reproducibility and confident evaluation of the core algorithm. The paper is therefore below the threshold for borderline accept (6) but above the reject scores (3-4), placing it solidly in the borderline reject range.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>