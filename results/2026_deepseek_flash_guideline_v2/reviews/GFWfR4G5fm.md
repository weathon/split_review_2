Now let me produce the final review.

## Summary

This paper identifies three critical limitations of static pre-training in Supervised Causal Learning (SCL)—distribution-shift fragility, compositional generalization failure, and a synthetic-to-real performance gap—and proposes TTT-SCL (Test-Time Training for SCL), a framework that dynamically generates causally-aligned training data for each test instance. The instantiation, TACTIC, uses a likelihood-based Alignment of Distribution (AD) metric with sparsity constraints, searches over candidate graphs via stochastic refinement, and trains an SCL model on the generated data. On the real-world Sachs dataset, TACTIC achieves 78.9 AUROC vs. 62.3 for the best SCL baseline (AVICI) and 67.1 for the best traditional method (PC), demonstrating that test-time generation of aligned training data can substantially overcome the documented generalization failures.

## Strengths

1. **Compositional generalization failure diagnosis (Section 3.2, Issue 2, Figure 2).** The "Component-mixed" condition shows that SCL models trained on all *individual* components (graph types, mechanisms, noise distributions) still fail on unseen *combinations* of these components—e.g., RFF_G_97.8 drops from 100 AUROC (i.i.d.) to 91 (Component-mixed); Chebyshev_G_97.8 drops from 100 to 90. Prior work (Montagna et al., 2024) attributed SCL failures only to unseen *individual* components; this paper identifies a more fundamental compositional failure that cannot be fixed by scaling pre-training diversity, directly motivating the paradigm shift to test-time adaptation.

2. **Quantified synthetic-to-real generalization gap (Table 1).** AVICI achieves 97.8 AUROC on synthetic RFF_G data but collapses to 62.3 on real-world Sachs, while traditional PC remains roughly consistent (61.1→67.1). This clean divergence empirically grounds the claim that strong synthetic-benchmark performance does not transfer to real data.

3. **TACTIC bridges the real-world gap (Table 2).** TACTIC (Notears) achieves 78.9 on Sachs (+16.6 over AVICI, +11.8 over PC) and 80.1 on Syntren (+14.7 over AVICI). These are the most practically interesting results and directly support the core claim.

4. **Stage-wise decomposition isolates SCL value (Table 4).** The paper tracks three outputs—seed, highest-score graph from search, and final SCL prediction—showing consistent gains: Sachs 61.8 → 66.6 → 78.9; Chebyshev_G 52.2 → 75.8 → 83.0. The large jump from highest-score graph to final SCL prediction (e.g., +12.3 on Sachs) demonstrates that training an SCL model on generated data provides substantial improvements beyond the score-based search alone, cleanly distinguishing TACTIC from classical score-based methods.

5. **Systematic distribution-shift characterization (Figure 2, Issue 1).** The paper separately measures degradation under graph shift, mechanism shift, and noise shift, identifying mechanism shift as the most damaging. This gives practitioners actionable insight beyond conflating all shift types.

6. **Ablation validates sparsity necessity (Table 3).** Removing the sparsity penalty causes substantial drops across all domains (e.g., Chebyshev_G: 83.0 → 69.7; Sachs: 78.9 → 63.5), confirming that optimizing AD alone yields degenerate dense solutions.

7. **Robustness across initialization quality (Table 2).** Testing both random and NOTEARS-based seeds shows the method works even without a good prior (TACTIC random: 88.4 on RFF_G, 79.6 on Chebyshev_G, 72.0 on Syntren), while consistently benefiting from better initialization.

## Weaknesses

### Major

1. **Transition probability formula is unsound as shown (Figure 3).** The acceptance probability is given as α = min[1, score(G_{k+1})/score(G_k)]. Since score(G) = AD(G, D_test) − λ·‖A_G‖₀ is a log-likelihood-based quantity that is necessarily negative, this ratio is not a valid acceptance probability. When both scores are negative, the ratio behaves perversely: a better graph (e.g., −5 vs. −10) yields ratio 0.5, accepted only 50% of the time, while a worse graph (e.g., −20 vs. −10) yields ratio 2, always accepted. Standard MCMC would use exp(score')/exp(score) or min(1, exp(score'−score)). The main text says only "accepted with probability proportional to its score," which is too vague to resolve this. *If the formula is as rendered, the stochastic search procedure does not have a well-defined stationary distribution and its behavior is unreliable.* **Important caveat:** this formula appears in a figure caption that may be a PDF-to-text parser artifact; the original PDF may contain a mathematically correct formula. The authors must clarify and/or correct this.

### Minor

2. **Unspecified regression method for AD computation (Section 4.1).** Computing AD(G, D_test) in Eq. (3) requires fitting a regression function f_i^k for each variable given its parents using D_test. The paper never states what regression method is used (linear regression, Gaussian processes, neural networks, etc.). This matters enormously: a linear fit would favor linear mechanisms and be misspecified for nonlinear ones, while a flexible nonparametric fit could be computationally prohibitive. The paper mentions "many ways to implement AD as discussed in Appendix A," but the main text must specify the method used for reproducibility.

3. **Limited real-world evaluation.** The only real-world dataset is Sachs (11 variables, 853 samples). The "pseudo-real" Syntren data is still generated by a simulator designed to mimic gene expression. For a paper making strong claims about real-world applicability (bridging "the significant performance gap between synthetic benchmarks and real-world data"), evaluation on additional real-world datasets with different characteristics would substantially strengthen the evidence.

4. **Missing standard deviations for Sachs and Syntren (Tables 1-3).** Standard deviations are reported for synthetic benchmarks but not for Sachs or Syntren. Given the small sample sizes and the practical importance of these results, readers cannot assess the reliability of the claimed improvements (e.g., whether the 78.9 vs. 67.1 on Sachs is significant).

5. **Anomaly in stage-wise analysis on Linear_U (Table 4).** The highest-score graph found during TACTIC's search (Stage 2, AUROC=80.1) is *worse* than the NOTEARS seed graph (Stage 1, AUROC=82.0). This means the score-based search actively degraded graph quality for this setting. Although the final SCL prediction (86.3) recovers, the paper does not discuss why the score function is not well-aligned with graph quality in this case, or what limits this imposes on the method's robustness.

### Trivial

6. **Transition probability formula only in figure caption.** The acceptance formula appears only in the Figure 3 caption, not in the main text. The main text (Section 4.2) says only "accepted with probability proportional to its score," which is ambiguous.

## Nice-to-Haves

- A comparison to a simpler alternative: directly using the highest-scoring graph from the search (with refit mechanisms) as the final prediction, skipping the SCL phase. This would isolate whether the benefit comes from ensembling over multiple graphs, from learning patterns the AD metric misses, or from some regularization effect of training on synthetic Gaussian-noise data.
- An analysis of why the SCL model improves over the score-based search on Linear_U despite the search producing a worse graph than the seed.
- An acknowledgment of the test-time computational cost asymmetry vs. baselines (the paper notes complexity analysis is in Appendix F, which is stripped from the review copy).
- Evaluation on additional real-world datasets beyond Sachs.

## Removed Points

These points from the input reviews were evaluated against the paper and removed with justification:

- **"AD metric is a standard score-based objective repackaged as novel"** — Removed because: the paper's contribution is the TTT-SCL framework and using AD as an alignment tool for *training data generation*, not the metric itself. The harsh critic acknowledges this doesn't invalidate the contribution. AD is a likelihood-based score, but the novelty lies in its application within the TTT paradigm, not in the mathematical form. The criticism inflates the concern.

- **"The three issues are manifestations of the same problem (distribution shift)"** — Removed because: the paper's claim is that they are *related but distinct* failure modes (the compositional failure is conceptually different from simple distribution shift). This is a subjective reframing, not a concrete weakness.

- **"Component-mixed doesn't test truly novel mechanisms/topologies"** — Removed because: the paper's claim is about compositional generalization of *seen components in unseen combinations*, which is exactly what this test evaluates. The critic asks for a different experiment than what the paper claims to do.

- **"AD is in-sample goodness-of-fit without complexity penalty"** — Removed because: the paper explicitly adds a sparsity penalty (Eq. 4–5), which directly addresses this concern. Standard BIC-style penalties are one approach; the L0 sparsity penalty serves the same purpose in this framework.

- **"Noise distribution mismatch (Gaussian generated vs. Uniform test)"** — Removed because: the paper explicitly states this design choice ("We set the noise distribution to a standard Gaussian distribution by default"); the results demonstrate the method works despite this mismatch. This is a feature, not a bug.

- **Strengths dropped from the Strength Finder** — None dropped; all identified strengths are concrete, evidence-grounded, and specific to the paper.

## Novel Insights

The most interesting observation emerging from the cross-review is the Linear_U anomaly in Table 4: the score-based search (Stage 2) produces a graph *worse* than the NOTEARS seed, yet the final SCL prediction (Stage 3) still achieves the best result (86.3). This suggests the SCL training phase provides a form of regularization, ensembling, or error correction that the paper does not analyze. Understanding why training on synthetic data from imperfect graphs yields better predictions than the graphs themselves would be a valuable contribution in itself. It may be that the SCL model averages across multiple candidate graphs, benefiting from the "wisdom of the crowd," or that training on Gaussian-noise data imposes a beneficial inductive bias.

## Suggestions

1. **Clarify/correct the transition probability formula.** If the formula is as rendered, replace score(G')/score(G) with exp(score(G'))/exp(score(G)) or exp(score(G') − score(G)). If it was a parser artifact, state the correct formula explicitly in the main text.
2. **Specify the regression method** used for fitting f_i^k in the AD computation (Section 4.1).
3. **Report standard deviations** for Sachs and Syntren results across multiple runs or bootstrap samples.
4. **Discuss the Linear_U anomaly** (Table 4): why the search degrades the seed, and how the SCL phase recovers from it.
5. **Add at least one additional real-world dataset** with different characteristics (larger variable count, different domain) to strengthen the claim of real-world applicability.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>