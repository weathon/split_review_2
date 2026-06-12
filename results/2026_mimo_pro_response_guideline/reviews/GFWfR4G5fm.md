## Summary
This paper proposes TTT-SCL, a framework for test-time training in Supervised Causal Learning (SCL), with a concrete instantiation called TACTIC. TACTIC searches over causal graph space using a Distributional Alignment (AD) metric combined with a sparsity constraint, generates K=200 synthetic training instances from high-scoring graphs, and trains an SCL model to predict the final causal graph. Experiments on synthetic (10 variables), pseudo-real (SynTREn, 20 variables), and real-world (Sachs, 11 variables) datasets show TACTIC outperforms both traditional causal discovery methods and the pre-trained AVICI SCL model.

## Strengths
- **Novel identification of compositional generalization failure in SCL**: The Component-mixed training setup (Section 3.1) is a well-designed diagnostic where all individual components are seen in training but specific test-time combinations are excluded. Figure 2/Table data shows concrete AUROC drops (e.g., RFF_G_97.8 drops from 100 to 91), demonstrating SCL models memorize configurations rather than learning modular causal factors. This goes beyond prior work (Montagna et al., 2024) which attributed failures only to unseen individual components.

- **Large improvements on real-world and pseudo-real data**: Table 2 shows TACTIC (Notears) achieves AUROC of 78.9 on Sachs vs. AVICI's 62.3 (~26% relative gain) and 80.1 on Syntren vs. 65.4 (~22% relative gain). These margins are substantial and directly validate the paper's central claim that test-time alignment bridges the synthetic-to-real gap.

- **Stage-wise analysis demonstrating SCL adds value beyond search**: Table 4 shows consistent improvement from seed → highest-score graph → SCL output across most domains (e.g., Chebyshev_G: 52.2 → 75.8 → 83.0), providing evidence the supervised learning phase is not redundant.

- **Well-validated sparsity ablation**: Table 3 shows removing sparsity degrades performance across all settings (e.g., Chebyshev_G: 83.0 → 69.7, Sachs: 78.9 → 63.5), confirming both AD and sparsity are necessary components.

## Weaknesses

### Fatal
None

### Major
- **Missing analysis of why the SCL stage improves over the highest-score graph**: Table 4 shows consistent improvement from stage 2 to stage 3, but the paper provides no analysis of *why* this happens. The most likely explanation is that training on K=200 diverse near-optimal graphs acts as an ensemble/denoising mechanism. The paper should test this hypothesis (e.g., varying K, or generating K random graphs without AD guidance) to isolate what the SCL model contributes. Without this, the contribution could be narrower than claimed — a useful model averaging trick rather than a paradigm shift.

- **Incomplete comparison fairness with AVICI**: TACTIC uses D_test extensively in its optimization loop (search + mechanism fitting + score evaluation), while AVICI (scm-v0) is a fixed pre-trained model that never sees D_test. Traditional baselines (PC, NOTEARS) also see D_test but lack an SCL model. A comparison with AVICI fine-tuned on D_test would be a fairer test of whether TTT-SCL's gains come from the framework design or simply from test-time data access.

### Minor
- **Linear_U stage-wise analysis contradicts search improvement narrative**: Table 4 shows the highest-score graph for Linear_U (80.1) is actually worse than the seed graph (82.0). This means the AD-guided search degraded performance, yet the paper's Section 4.4 claims "1→2 (Search Improvement)" as a general finding without qualification.

- **Missing computational cost analysis**: TACTIC performs stochastic search + mechanism fitting + data generation + SCL training for every test instance. The paper defers complexity analysis to Appendix F but does not provide wall-clock comparisons against AVICI (one forward pass) or NOTEARS in the main text, which is critical for practical adoption.

- **MH acceptance ratio notation issue**: Figure 3 shows α = min[1, score(G_{k+1})/score(G_k)], but score(G) can be negative (log-likelihood minus sparsity penalty). A ratio of possibly-negative numbers is not a valid acceptance probability. The standard MH formulation uses exp(score differences). This is likely a notational simplification but should be corrected for clarity and reproducibility.

- **Key hyperparameters and details underspecified**: The λ value for the sparsity penalty is never specified. The strategy for collecting K=200 graphs from the stochastic chain (last K accepted? K best? thinned sample?) is not described.

- **Overlapping motivation**: Issues 1 and 3 (fragility to distribution shifts vs. synthetic-to-real gap) describe substantially the same phenomenon from different angles, slightly overstating the breadth of the diagnosed limitations.

### Trivial
None

## Nice-to-Haves
- Scalability analysis or discussion for larger graphs (50–100 variables); largest tested is 20 variables.
- Sensitivity analysis for λ and K hyperparameters.
- Statistical significance tests for improvements over AVICI on Chebyshev_G (83.0 ± 8.7 vs 81.7 ± 10.5 — overlapping confidence intervals).

## Removed Points
These points are flagged to be removed, treat them with caution:
- Harsh critic's framing that the contribution is "misleadingly framed" — the paper does address the distinction from score-based methods in Table 4 and Section 4.4. The concern about understanding the SCL contribution is valid but the "misleading" framing is too strong.
- Harsh critic's claim that "Issues 1 and 3 are essentially the same phenomenon" — while overlapping, Issue 3 makes a specific claim about the synthetic→real gap (Table 1 shows PC is consistent across domains while AVICI collapses), which is a distinct observation.
- Harsh critic's assertion that the MH ratio is "mathematically incorrect" — the formula likely reflects a simplified notation of the actual implementation, not a fundamental algorithmic error.

## Novel Insights
The identification of compositional generalization failure in SCL — where models trained on all individual components still fail on novel combinations — is a genuinely novel diagnostic finding that goes beyond prior work attributing SCL failures only to unseen components. Combined with the test-time training framework, this paper makes a concrete contribution to understanding and addressing SCL limitations. However, the deeper question of *why* the SCL stage improves over score-based search remains unanswered, leaving the precise mechanism of the contribution somewhat ambiguous.

## Suggestions
- Add an experiment generating K=200 random (non-AD-guided) graphs to train the SCL model, isolating whether the AD alignment or the ensemble effect drives improvement.
- Include AVICI fine-tuned on D_test as a baseline for a fairer comparison.
- Specify λ value, K collection strategy, and actual sample sizes n in the main text.
- Correct the MH acceptance ratio to use exp(score differences) for clarity.
- Add computational cost comparison in the main text.

## Calibration Reporting

**Round 1 bracketing anchors:**
| Anchor | Avg Score | Round | Relevance |
|--------|-----------|-------|-----------|
| TICL (test-time training for SCL from interventional data) | 5.50 | 1 | Very similar topic — also proposes TTT for SCL; rejected with high variance (8,3,6,5). Our paper has stronger empirical results and cleaner diagnostics. |
| Demystifying amortized causal discovery with transformers | 5.00 | 1 | Analyzes why SCL transfers from synthetic to real; rejected for limited scope (bivariate only). Our paper has broader experiments. |
| Causal Structure Learning Supervised by LLM | 3.20 | 1 | Novel LLM+CSL framework; rejected for weak math and limited validation. Our paper is substantially stronger. |
| Meta-Learning Approach to Bayesian Causal Discovery | 6.00 | 1 | New framework for causal discovery; accepted with consistent 6s. Our paper has stronger empirical results. |
| Causal Modelling Agents | 6.25 | 1 | LLM + DSCM for causal discovery; accepted. Our paper has more focused contribution. |
| When Selection meets Intervention | 8.00 | 1 | Strong theoretical contribution with rigorous proofs; accepted. Our paper has less theoretical depth. |
| CausalRivers | 7.33 | 1 | Benchmarking paper; accepted. Our paper has more methodological novelty. |

**Round 2 narrowing anchors:**
| Anchor | Avg Score | Round | Relevance |
|--------|-----------|-------|-----------|
| Test-Time Learning of Causal Structure from Interventional Data | 5.50 | 1 | Most directly comparable paper — same TTT+SCL paradigm. |
| Meta-Learning Approach to Bayesian Causal Discovery | 6.00 | 1 | Comparable framework novelty; our empirical results are stronger. |
| CausalRivers | 7.33 | 1 | Our paper has more methodological novelty but less benchmarking rigor. |

**Bracket: 5.5 – 7.0**

**Final score rationale:** The paper sits above the TICL paper (5.5, rejected) due to stronger empirical results on real-world data, the novel compositional generalization diagnosis, and cleaner experimental design. It is comparable to the Meta-Learning paper (6.0, accepted) in framework novelty but has stronger empirical validation. It falls below the 7.33+ papers due to methodological gaps (missing analysis of why SCL helps, incomplete baselines, underspecified hyperparameters). The score of 6.5 reflects a paper with genuine contributions — particularly the compositional generalization diagnosis and strong real-world results — but with insufficient analysis of the core mechanism to warrant a stronger recommendation.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>