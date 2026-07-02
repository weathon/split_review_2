## Summary

This paper identifies three out-of-distribution failure modes of static pre-training in Supervised Causal Learning (SCL)—fragility to distribution shifts, failure in compositional generalization, and poor transfer from synthetic to real-world data—and proposes Test-Time Training for SCL (TTT-SCL) as a remedy. The key idea is to dynamically construct a customized training set for each test instance by searching over candidate causal graphs and generating synthetic data from them. The paper introduces TACTIC, which uses a stochastic graph refinement procedure guided by a likelihood-based alignment score with sparsity regularization, then trains an SCL model (AVICI) on the generated data. Empirical results on synthetic benchmarks, the Sachs real-world dataset, and Syntren pseudo-real data show TACTIC outperforming both traditional causal discovery methods and the pre-trained AVICI baseline on most settings.

## Strengths

1. **Systematic documentation of SCL's OOD failures (Section 3).** The factorial experiment design varying graph type, mechanism family, and noise distribution goes beyond the typical "same mechanism, different parameters" evaluation. The compositional generalization failure (Issue 2) is particularly insightful: models that have seen all components individually still fail on novel combinations—a stronger indictment of static pre-training than a simple distribution-shift performance drop.

2. **Well-motivated paradigm shift from static diversity to test-time concentration.** The paper correctly identifies that the core bottleneck is the mismatch between synthetic training data and real test instances, and that this cannot be fixed by scaling diversity alone (Issue 2 directly shows compositional failure despite complete component coverage). Moving from "one static training set for all test instances" to "a customized training set per test instance" is a logical and creative response to the documented failures.

3. **Strong empirical results on the most challenging settings.** On Sachs (real-world biological data) and Syntren (pseudo-real), TACTIC (Notears) achieves AUROC of 78.9 and 80.1 respectively, substantially above all baselines (next best: PC at 67.1 on Sachs, AVICI at 65.4 on Syntren). These are exactly the scenarios where existing SCL fails, and the margins are practically meaningful.

4. **Stage-wise analysis (Table 4) provides informative ablation.** Breaking the pipeline into seed graph → highest-scoring search graph → final SCL output isolates what each stage contributes. The fact that the SCL output consistently improves over the highest-scoring search graph (especially on Sachs: 66.6 → 78.9) is the strongest evidence that the SCL training phase adds value beyond what score-based search alone provides.

## Weaknesses

### Fatal
None.

### Major

1. **Only one SCL baseline in the main evaluation (Table 2).** The paper compares against AVICI as the sole SCL method while citing several other SCL approaches (Ke et al. 2022, Dai et al. 2023, Zhang et al. 2025, Froehlich & Koeppel 2024) in the related work. The claim that TACTIC "significantly outperforms existing SCL" (abstract) rests on a comparison with a single method. The paper notes that "Results with other backbones are consistent and shown in Appendix C," but this evidence is deferred to the appendix, and the main evaluation table includes no other SCL baselines. Without results from at least one or two additional SCL methods, the reader cannot determine whether the documented OOD failures are specific to AVICI's architecture or inherent to the static pre-training paradigm more broadly.

2. **Missing variance estimates for Sachs and Syntren in both Tables 1 and 2.** The table captions state "Results are presented as AUROC (standard deviation)," yet the Sachs and Syntren columns report only point estimates without any measure of variability (e.g., 62.3, 67.1, 78.9, 80.1). Sachs is a single fixed dataset, but the TACTIC pipeline involves randomness (stochastic refinement, SCL training), so multiple runs or bootstrap estimates are needed to assess reliability. Without variance estimates, the magnitude and statistical significance of the claimed improvements cannot be properly evaluated.

3. **Ambiguity in how the K=200 training graphs are selected from the search trajectory.** The paper states that "For the final refined graph set {G_train^k}_{k=1}^K, we regress mechanisms via SIM, forward-sample synthetic datasets, and assemble them into a customized training set" (Section 4.2, Stage 3), but does not specify how these K graphs are chosen. Are they the top-K by score? All intermediate graphs visited during the stochastic search? The final K graphs after convergence? This matters for reproducibility and for understanding what the SCL model actually trains on.

### Minor

1. **Overstated novelty of the AD metric.** Equation 3 computes the average conditional log-likelihood of observed variables given their parents under a candidate graph. With Gaussian noise (the default setting, Section 4.2), this is a standard Gaussian log-likelihood. Combined with an L0 sparsity penalty (Equation 4), the joint score (Equation 5) is a penalized likelihood score of the same family as BIC/AIC—well-known in the score-based causal discovery literature. The paper frames AD as a "proposed metric" (contributions list), but the actual novelty is in the *two-stage pipeline* (search → generate training data → train SCL model), not in the AD formulation itself. Section 4.4 partially addresses this by distinguishing TACTIC from classical score-based methods, but the framing in the abstract and introduction is overstated.

2. **Transition probability inconsistency.** The main text says candidate graphs are "accepted with probability proportional to its score" (Section 4.2, line 173), but Figure 3's caption shows alpha = min[1, score(G_{k+1})/score(G_k)]—a Metropolis-Hastings ratio, which is different from "proportional to its score." This discrepancy needs to be resolved.

3. **Strong parametric assumption in the AD metric.** The paper sets the noise distribution to N(0,1) by default (Section 4.2, Stage 3) when generating training data from searched graphs. However, the test data may have non-Gaussian noise (e.g., the Linear_U synthetic setting uses Uniform noise). The paper does not discuss how this mismatch affects the quality of the generated training data or whether alternative noise models were explored.

### Trivial
None.

## Nice-to-Haves
- Report wall-clock time or relative computational cost compared to baselines in the main text. TACTIC involves NOTEARS initialization, stochastic refinement with per-candidate mechanism fitting, generating 200 training instances, and training a full neural network—potentially orders of magnitude more expensive than running PC, GES, or the pre-trained AVICI. This trade-off is important for practitioners.
- Add at least one additional SCL baseline to strengthen the generality of the conclusions.
- Provide variance estimates for Sachs and Syntren results.
- Specify the value of the sparsity penalty hyperparameter λ and how it was chosen (if not already in Appendix B).
- Provide more detail on the stochastic search trajectory: number of iterations, convergence criteria, and how the final set of graphs is sampled.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"The AD metric novelty is not clearly articulated"** was downgraded from Critical to Minor. The paper does partially acknowledge the relationship to classical score-based methods in Section 4.4, and the core contribution is the two-stage pipeline, not the metric itself. The framing is slightly overstated but not a fatal flaw.
- **"Computational cost is opaque in the main text"** was moved to Nice-to-Have. The paper explicitly states "Complexity analysis and runtime variation with the number of nodes are detailed in Appendix F" (line 176). This content was stripped by the parser, not missing from the submission.
- **"Hyperparameter λ is never specified"** was removed. The paper states "more detailed configurations can be found in the appendix B" (line 91), which was stripped by the parser. The value likely appears there.
- **"The claim that strong synthetic performance fails to translate to real-world data is overblown (only one SCL model)"** was subsumed into Major weakness #1 (only one SCL baseline). This is the same issue.
- **"Section 3.1 Component-mixed training construction needs more detail"** was removed; the description is brief but conceptually clear enough for understanding the experimental design.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Include at least one additional SCL baseline (e.g., a transformer-based or autoregressive SCL method) in Table 2 to support the claim that OOD failures are general to static pre-training, not specific to AVICI.
2. Provide bootstrap variance estimates or multiple-run standard deviations for Sachs and Syntren across all methods.
3. Clarify how the K=200 training graphs are selected from the stochastic search trajectory (top-K by score, all visited graphs, or post-convergence sampling).
4. Resolve the discrepancy between the text ("accepted with probability proportional to its score") and Figure 3 (Metropolis-Hastings ratio) for the acceptance rule.
5. Discuss the impact of the Gaussian noise assumption on the quality of generated training data when test data have non-Gaussian noise.
6. Tone down the novelty claims about the AD metric itself; instead, emphasize that the novelty lies in using score-based search to generate training data for an SCL model.

---

**Calibration anchors used across rounds:**

| Path | Avg Human Score | Round | Comparison |
|---|---|---|---|
| Demystifying amortized causal discovery with transformers (`lQYi2zeDyh.md`) | 5.00 | 1 | Analyzes SCL OOD failures but only bivariate/synthetic; no solution proposed. Paper under review is stronger |
| Zero-Shot Learning of Causal Models (`x3F8oPxKV2.md`) | 6.25 | 2 | Requires known causal graphs and noise samples; stronger assumptions. Comparable quality |
| A Robust Method to Discover Causal or Anticausal Relation (`Q0s6kgrUMr.md`) | 6.67 | 1 | Similar-level methodological concerns; similar empirical scope |
| A Meta-Learning Approach to Bayesian Causal Discovery (`eeJz7eDWKO.md`) | 6.00 | 2 | Comparable paper with similar evaluation depth |
| Resource Efficient Test-Time Training (`7iuFxx9Ccx.md`) | 6.00 | 1 | TTT paper on a different domain; similar evaluation quality |
| Causal Structure Learning Supervised by LLM (`JzFLBOFMZ2.md`) | 3.20 | 1 | Weaker paper with less convincing empirical support |
| The best of both worlds (`AvXrppAS2o.md`) | 3.00 | 1 | Weaker paper with marginal improvements |

**Round 1 bracket (from 6-query sweep):** 5.5–7.0. **Narrowing:** The paper is clearly stronger than "Demystifying" (5.00) because it proposes a working solution validated on real data. It is comparable to "Zero-Shot Learning" (6.25) but with fewer fundamental assumptions. The main weaknesses (single SCL baseline, missing variances, ambiguous graph selection) are addressable gaps, not structural flaws. **Final score anchored** between the 5.00 (too low given real-data validation and proposed solution) and 6.25 (too high given methodological gaps) anchors, settling at **6.0**.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>