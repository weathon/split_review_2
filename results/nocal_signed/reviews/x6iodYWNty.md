## Summary

This paper introduces Neural Predictor-Corrector (NPC), a framework that replaces hand-crafted heuristics in predictor-corrector homotopy solvers with learned policies trained via reinforcement learning. NPC unifies four diverse problem domains — robust optimization (GNC), global optimization (Gaussian homotopy), polynomial root-finding (homotopy continuation), and sampling (annealed Langevin dynamics) — under a common PC formulation, applies a single RL-trained policy to all of them, and demonstrates amortized training where one offline training can generalize to unseen instances.

## Strengths

- **Cross-domain breadth of evaluation:** NPC is evaluated on four qualitatively different homotopy problems using realistic benchmarks in each domain. This is an unusually broad experimental scope for a method paper and provides meaningful evidence that a single RL-based control policy can accelerate PC solvers across diverse settings.
- **Consistent and substantial efficiency gains:** Across all four domains, NPC reduces corrector iterations substantially (≈70–80% in GNC, ≈30–50% in GH, ≈80% in HC, ≈75% in ALD) while maintaining solution quality comparable to classical baselines. The magnitude of these reductions is large enough to be practically meaningful.
- **Amortized training demonstration:** The paper shows that a single policy, trained on one distribution of instances (Aquarius for GNC, randomized Ackley functions for GH, 4-view triangulation for HC, 10-mode GMM for ALD), can be deployed on unseen instances without per-instance retuning. This is a practically relevant property for real-world deployment.

## Weaknesses

### Fatal

- **No measures of uncertainty reported despite 50 trials:** The paper states "All results represent the average over 50 independent trials" (line 230) but reports no standard deviations, confidence intervals, error bars, or any other measure of variance in any table or figure. This makes it impossible to evaluate whether observed differences between methods (especially on accuracy metrics where differences are small — e.g., rotation errors in Table 1 where all methods give nearly identical values, W₂ values in Table 5, or the ablation rankings in Table 6) are real or within noise. The data to compute these exists from the 50 trials; their absence is a fundamental evidential gap that undermines the core quantitative claims, particularly the claim of "comparable" accuracy.

### Major

- **Unsubstantiated claim of "superior numerical stability":** The abstract (line 9), introduction (line 32), contribution bullet (line 38), and conclusion (line 349) repeatedly claim that NPC demonstrates "superior stability" or "superior numerical stability." However, stability is never defined, operationalized, or measured anywhere in the paper. The evidence provided is accuracy preservation (which is a different property), not stability. This claim substantially overstates what the experiments support and should be either removed or properly evidenced with a stability metric (e.g., variance across runs, failure rate, sensitivity to perturbations).

- **Ablation study lacks accuracy metrics:** Table 6 reports only the change in corrector iterations (ΔIter) when RL state components are removed, but does not report corresponding accuracy metrics. The paper interprets increased iterations as evidence that removed components were "essential" and that "corrector statistics are the most informative." However, increased iterations alone could reflect the agent adopting a more conservative policy that still preserves accuracy. Without accuracy metrics to check whether degradation also occurs, the analysis is incomplete and the conclusions about which components are "most informative" are partially speculative.

### Minor

- **Undiscussed NN overhead in runtime:** In the ALD experiments (Table 5), each NPC-guided iteration takes roughly 2× longer than a Classic ALD iteration (~7.0 ms vs ~3.3 ms on the 40-mode GMM). The runtime improvement (1.75×) is much smaller than the iteration reduction (3.7×) would suggest, implying NN forward-pass overhead. This trade-off is not analyzed or discussed anywhere in the paper.

- **Training cost not reported:** The paper reports only inference runtime. For a method whose value proposition includes "amortized training," the training cost (wall time, number of environment steps, PPO updates) is essential context. Without it, a reader cannot assess how many inference instances are needed to recoup the one-time training investment.

- **Limited evaluation scope in two domains:** The GH evaluation is restricted to 2D synthetic functions (Ackley, Himmelblau, Rastrigin), and the HC evaluation tests only three polynomial systems (katsura10, cyclic7, UPnP). While the cross-domain breadth is a genuine strength, within these two domains the evaluation is narrow enough that generalization claims are only weakly supported.

### Trivial

None.

## Nice-to-Haves

- An analysis of hyperparameter sensitivity for the 2×16 MLP policy architecture and PPO defaults.
- A discussion of how NPC would scale to higher-dimensional problems in GH and larger polynomial systems in HC.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **IRLS baseline "chosen to be a poor performer":** The harsh critic claimed IRLS was chosen to inflate NPC's advantage. However, the paper shows IRLS performs comparably to Classic GNC on point cloud registration (Table 1) and transparently notes IRLS is "tailored for a specific task" (line 236). IRLS is a published baseline (Peng et al., 2023) included honestly. This criticism is factually inaccurate and removed.
- **Formatting/bolding complaints in GH table:** The critic argued bolding visually favors NPC. Bolding follows the stated convention and parser-extracted HTML tags may not reflect original formatting. Removed as a formatting artifact.
- **"Unification claim is disputable":** The paper hedges with "To the best of our knowledge" and demonstrating a common PC structure across four domains is a legitimate synthesis. This is a matter of opinion, not a verifiable weakness.
- **Missing appendix content:** The critic noted limitations are "relegated to the (removed) Appendix D." Since the parser strips appendices from all papers, this criticism is invalid by rule.
- **Default PPO hyperparameters / policy architecture not tuned:** Using standard defaults aids reproducibility. The paper is transparent about this design choice; criticizing it without evidence that tuning would improve results is speculative.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add uncertainty measures.** Report standard deviations or confidence intervals for all quantitative results (Tables 1–6, Figure 4). The data from 50 trials already exists.
2. **Remove or substantiate the stability claim.** Either remove the "superior numerical stability" claim entirely, or define a stability metric (variance across runs, failure rate, sensitivity to perturbations) and compare it against baselines.
3. **Add accuracy metrics to the ablation study** (Table 6) so the importance of state components can be evaluated on both efficiency and accuracy dimensions.
4. **Report training cost** (wall time, environment steps, PPO updates) to contextualize the amortized training claim.
5. **Analyze NN overhead.** Discuss the per-iteration cost difference (visible in the ALD results) and clarify when the iteration reduction translates to proportional wall-time reduction versus when it does not.

## Score and Decision

The paper tackles a well-motivated problem and presents an elegant unifying framework with impressively broad cross-domain evaluation. The efficiency gains are large and consistent across all four domains. However, the paper has a decisive evidential gap: **no measures of uncertainty are reported for any quantitative result**, despite 50 trials being run. This makes it impossible to evaluate whether observed differences on accuracy metrics are real or within noise. Combined with an unsubstantiated "superior stability" claim repeated throughout the paper and an incomplete ablation study, the quantitative evidence as presented does not fully support the paper's claims. The contribution has clear merit, but the reporting gap must be closed before the paper can be accepted.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>