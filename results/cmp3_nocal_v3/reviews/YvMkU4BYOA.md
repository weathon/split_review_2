Now I have verified all claims against the paper text. Let me produce the final consolidated review.

## Summary

This paper proposes XBIC, a score-based causal discovery method for discrete Bayesian networks that integrates Shapley values from per-node classifiers into the BIC complexity penalty. The idea is that when a candidate parent contributes strongly to predicting its child (measured via Shapley values), the penalty for including that edge is reduced. The method preserves standard BIC as a special case when the Shapley signal is absent, and reverting to BIC serves as a safety property. Experiments on ten benchmark networks across seven sample-size regimes (700 runs) show modest aggregate improvements in oriented-edge F1 over BIC hill-climbing (+5.6% relative, +0.04 absolute), PC (+20.9%), and a GES variant (+9.6%).

## Strengths

- **Novel and creative connection between XAI and causal discovery.** The idea of using Shapley values from per-node predictive models to modulate the BIC penalty is genuinely novel. Most work at the causality–explainability interface injects known causal structure into explanations; reversing the pipeline to use explanations to *learn* structure is a clever inversion (see §2.2–2.3 for proper situating relative to prior work).

- **Clean default-to-BIC property.** When the Shapley signal is absent (weak classifiers, few confident predictions, or $w=0$), XBIC reduces exactly to standard BIC (Eq. 2, line 113). This is a nice safety property — the method does not hurt when it cannot help — and it makes the approach low-risk as a practical drop-in.

- **Reasonable evaluation scope.** Ten networks (6–76 nodes) across seven sample-size regimes with 700 total runs is a solid evaluation for a paper in this space. The use of identical data splits across methods (line 192) is good practice.

## Weaknesses

### Fatal
None.

### Major

**M1. The core directional-asymmetry assumption is asserted without justification.** The paper's central claim (line 127) states: "Intuitively, if $|\bar{\phi}_{1 \rightarrow 2}| \gg |\bar{\phi}_{2 \rightarrow 1}|$, the edge $X_1 \rightarrow X_2$ has stronger directional support than $X_2 \rightarrow X_1$." This intuition is the linchpin of the entire method, yet the paper provides **no theoretical analysis and no direct empirical test** of whether or under what conditions Shapley-value asymmetry correlates with causal direction. Consider a true edge $X_1 \rightarrow X_2$: the classifier $f_2$ will assign high Shapley value to $X_1$ (the direct cause), but the reverse classifier $f_1$ can also assign high Shapley value to $X_2$ (the effect) because effects carry information about causes through the reverse statistical association. Whether $|\bar{\phi}_{1 \rightarrow 2}| > |\bar{\phi}_{2 \rightarrow 1}|$ holds depends on noise levels, functional forms, and discrete distribution characteristics — not on causal direction alone. The paper provides no argument, synthetic experiment, or analysis isolating this claim. The "consistency remark" (lines 155–159) only addresses asymptotic penalty growth, not the validity of the directional signal. Without this validation, the method's mechanism is unsubstantiated, and observed F1 improvements could arise from the penalty modulation acting as an unrelated regularizer.

**M2. PDAG-to-DAG completion penalizes baselines with noise that XBIC does not face.** The paper states (line 190): "For baselines that return a PDAG, we complete it to a DAG by randomly orienting undirected edges (while preserving acyclicity) before computing directed-edge metrics." This is a significant confound. PC and GES output CPDAGs/PDAGs where undirected edges represent genuine ambiguity within the Markov equivalence class. Randomly orienting them introduces a random component into the baseline metrics that XBIC (which outputs a fully directed graph) does not face. The reported directed-edge F1 for PC and GES therefore underestimates their performance *as PDAG outputters*. A fair comparison would report skeleton-level metrics alongside directed-edge metrics, or evaluate at the PDAG level by treating two DAGs in the same equivalence class as equivalent (matching against the ground-truth CPDAG). Because the paper's central claim is about resolving Markov-equivalence class ambiguities, the absence of metrics that separate orientation quality from skeleton recovery is a critical gap.

**M3. No analysis isolating *where* the improvement comes from.** The paper frames its contribution as resolving Markov-equivalence class ambiguities (mediator vs. confounder motifs, §1) but never directly tests this claim. No metrics are reported broken down by edge type (collider vs. non-collider orientations, ambiguous vs. unambiguous edges). The paper does not isolate performance on the subset of edges where BIC-HC already finds the correct skeleton but gets the orientation wrong. Without such evidence, the narrative linking the method's mechanism (Shapley asymmetry → improved orientation within equivalence classes) to the empirical results is untested. A simple ablation replacing SHAP(G) with random values across edges would also help confirm that the specific directional signal, not just the softer penalty, drives the result.

### Minor

**M4. Improvements over the primary baseline (BIC-HC) are modest and inconsistent.** The headline improvement over BIC-HC is **+0.04 absolute F1** (Table 4). Table 2 shows that several individual network/sample-size entries are zero or negative (e.g., Asia at $2M^2$: −0.12; Win95pts at $8M^2$: −0.09; Water at $0.125M^2$: −0.01). While the aggregate is positive and the statistical tests support significance, the per-configuration inconsistency and small absolute magnitude mean the practical value of the method for any *specific* dataset is unclear. Combined with the PDAG completion issue (M2), it is difficult to assess how much of this small gain is genuine orientation improvement versus artifact.

**M5. Computational cost is very high relative to the gain.** From Table 5, XBIC is 50–500× slower than BIC-HC (Asia: 0.39s vs 74.78s, a 192× slowdown; Win95pts: 75s vs 2139s, a 28× slowdown). The paper acknowledges this in the limitations (line 313) and notes parallelization potential, but does not quantify whether the cost-benefit ratio is acceptable for realistic use cases. A 50–500× runtime increase for a +0.04 absolute F1 gain merits a more thorough discussion of practical viability.

**M6. GES comparison in the abstract lacks necessary caveats.** The abstract states "+9.6% over GES" without qualification. The paper's §4.5 explains that GES exceeded the 7-day limit on many settings and comparisons were only on the subset where GES completed. Notably, the paper explicitly states this is a "favorable filtering for GES" (line 278), meaning the comparison is conservative (it likely *understates* XBIC's advantage rather than inflating it). However, the abstract still presents the number without indicating it applies to a non-representative subset, which could mislead readers.

### Trivial

- The confidence threshold $\tau$ used in the main experiments (Table 2) is not explicitly reported. The paper states it was varied between 0.7 and 0.95 with $<1\%$ effect on F1 (line 194), but the actual value used in the main runs is unspecified.
- Individual Table 2 entries report only point estimates ($\Delta F_1$) without standard deviations or confidence intervals, even though each setting is repeated 10 times (line 192). Variance information is available and should be included.
- The functional form of Eq. (2) — dividing $\dim(G)$ by $\exp(w \cdot \text{SHAP}(G))$ — is not motivated or derived; it is presented as a design choice without alternatives considered.
- "Avg. MB Size" in Table 1 is not defined in the text.

## Nice-to-Haves

- **Direct validation of the asymmetry assumption.** The most important addition would be a controlled simulation with known causal pairs: compute $\bar{\phi}_{j \rightarrow i}$ and $\bar{\phi}_{i \rightarrow j}$ for each pair under varying noise levels and check whether the sign/size of the asymmetry predicts the correct direction above chance. This would directly test whether the paper's core premise holds.
- **Isolation of orientation performance.** Report metrics on the subset of edges where BIC-HC finds the correct skeleton but gets the direction wrong. If XBIC improves on these edges, the claim about resolving Markov-equivalence classes would be directly supported.
- **Skeleton-level metrics.** Reporting undirected-edge precision/recall would clarify whether XBIC improves orientation specifically or also finds a different skeleton.
- **Random-Shapley ablation.** Replace SHAP(G) with permuted values across edges and show the improvement disappears, confirming the directional signal drives the result rather than just the softer penalty.

## Removed Points

These points from the input review were removed with justification:

- **C2 (GES survivorship bias inflates XBIC's advantage):** REMOVED. The paper explicitly states "Despite this favorable filtering for GES" (line 278), meaning the comparison subset *favors GES*, making the comparison conservative. The critic's claim that the comparison "inflates XBIC's apparent advantage" misreads the paper's own description. The transparency concern about the abstract is retained as M6.
- **Missing NOTEARS/gradient-based comparison:** REMOVED. NOTEARS and DAG-GNN are designed for continuous data; demanding their inclusion for a purely discrete setting is scope creep.
- **"Likely false in general" assertion about asymmetry:** The critic asserts the core assumption is "likely false in general" but provides no proof. The criticism that the assumption is *unvalidated* is retained as M1; the stronger claim that it is false is speculation.
- **Several section-by-section nitpicks:** Formatting observations, minor phrasing preferences, and comments on figure readability in parsed text are removed as parser artifacts or trivial observations.

## Novel Insights

None beyond the paper's own contributions. The reviews primarily identify gaps in validation rather than offering new interpretations of the method.

## Suggestions

1. **Validate the core assumption directly.** Run controlled simulations with known causal pairs across varying noise levels and functional forms. Compute the rank correlation between Shapley-value asymmetry ($|\bar{\phi}_{1 \rightarrow 2}| - |\bar{\phi}_{2 \rightarrow 1}|$) and correct direction. This is the minimal experiment that would substantiate the method's premise.
2. **Add skeleton-level metrics and PDAG-compatible evaluation.** Report undirected precision/recall and F1 alongside the directed-edge metrics. For PC and GES, also report metrics at the PDAG level (treating undirected edges as correct if they match the skeleton) so the reader can distinguish orientation quality from skeleton recovery.
3. **Isolate orientation-specific improvement.** Report performance on the subset of edges where BIC-HC finds the correct skeleton but wrong orientation. This directly tests the claim about resolving Markov-equivalence classes.
4. **Report variance.** Include standard deviations or confidence intervals for the Table 2 entries (10 repetitions are already available).
5. **Add a random-Shapley ablation.** Compare XBIC against a version where SHAP(G) is replaced by permuted or random values, to verify that the directional signal (not just a softer penalty) causes the improvement.
6. **State the confidence threshold $\tau$ value** used in the main experiments.
7. **Caveat the GES number in the abstract** to reflect the comparison subset.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>