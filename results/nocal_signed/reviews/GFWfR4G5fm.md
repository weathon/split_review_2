Now let me write the final consolidated review.

## Summary

This paper identifies three limitations of static pre-training in supervised causal learning (SCL): fragility under distribution shifts, failure in compositional generalization, and poor transfer from synthetic to real-world data. To address these, the authors propose TTT-SCL, a framework that dynamically generates test-aligned training data at test time, and instantiate it as TACTIC, which uses a stochastic graph search guided by a distributional alignment (AD) metric and sparsity constraint. Experiments on synthetic, pseudo-real, and real-world datasets show TACTIC substantially outperforms existing SCL methods and traditional causal discovery approaches, particularly on the Sachs benchmark (78.9 AUROC vs. 62.3 for AVICI and 67.1 for PC).

## Strengths

- **Genuinely novel diagnosis of compositional generalization failure (Section 3, Issue 2).** The paper goes beyond prior analyses (e.g., Montagna et al., 2024) by showing that SCL models fail not only on unseen *individual* components but also on novel *combinations* of seen components. This is the most novel finding of the empirical critique and effectively motivates the need for test-time adaptation. The experimental design in Fig 2 clearly distinguishes this failure mode from simple distribution shift.

- **Strong and practically meaningful real-world result (Table 2).** TACTIC (Notears) achieves 78.9 AUROC on the Sachs dataset — a ~16-point improvement over AVICI (62.3) and ~12 points over PC (67.1). On a widely used causal discovery benchmark, this is a substantial advancement. The result is reinforced by consistent strong performance on the Syntren pseudo-real dataset (80.1 AUROC).

- **Well-structured problem framing (Sections 1, 4).** The contrast between "diversity" (static pre-training) and "concentration" (test-time adaptation) cleanly motivates the approach. Decomposing the core challenge into quantifying similarity (AD metric) and efficient search makes the framework easy to follow and conceptually extensible.

## Weaknesses

### Fatal
None.

### Major

- **SCL model training procedure is underspecified in the main text.** Line 174 states "An SCL model is then trained on this set" without clarifying whether this involves (a) training from scratch on K=200 generated instances, (b) fine-tuning a pre-trained AVICI checkpoint, or (c) some other initialization. Since AVICI is a transformer trained on millions of instances (Lorch et al., 2022), a from-scratch training on 200 instances raises questions about overfitting, while fine-tuning from pre-trained weights would carry information from the original training distribution into the test-time process — a distinction that affects how the 2→3 "Learning Improvement" in Table 4 should be interpreted. The main text should state this explicitly rather than deferring entirely to the appendix.

### Minor

- **Anomalous Linear_U result in stage-wise analysis (Table 4).** The highest-scoring graph found by TACTIC's search achieves *lower* AUROC (80.1) than the NOTEARS seed (82.0) on Linear_U, meaning the score-based search degraded graph quality on this dataset by the AUROC metric. Yet the final SCL model improves to 86.3. The paper should explain this pattern and discuss what it reveals about the relationship between the score proxy and the evaluation metric.

- **Missing variance for Sachs and Syntren results (Table 2).** The table header promises "AUROC (standard deviation)," but Sachs and Syntren columns for TACTIC and most baselines report bare AUROC values without variance. Even single real-world datasets permit bootstrap or multi-seed estimates; without them, the reliability of the headline 78.9 (Sachs) result is harder to assess.

- **Acceptance probability may be ill-defined for negative scores (Figure 3).** The stochastic refinement uses α = min[1, score(G_{k+1})/score(G_k)], but scores can be negative (penalized log-likelihood). A ratio of two negative values is positive, and the resulting acceptance probability may not properly reflect graph quality. The paper should either fix the formulation or explain why scores are guaranteed positive in practice.

- **Hyperparameter λ not reported.** The sparsity regularization strength λ in Eq 5 is never stated for the main experiments (only λ=0 is reported in the ablation). The actual value, selection procedure, and sensitivity should be reported.

### Trivial

- **Asymmetric ablation design (Table 3).** The sparsity ablation removes the sparsity term (λ=0) but does not ablate the AD metric itself (e.g., replacing AD with a random or constant score). This leaves unclear whether any structured search (not specifically AD-based) would produce similar training data.

## Nice-to-Haves

- The noise distribution is fixed to standard Gaussian (line 174). A discussion of robustness to noise distribution mismatch, or pointing to an appendix analysis, would strengthen the method's practical guidance.
- The specific likelihood form assumed for the AD metric (Eq 3) — Gaussian vs. nonparametric — should be briefly stated in the main text rather than deferred to Appendix A.

## Removed Points

These points are flagged to be removed, treat them with caution:
- The claim that AD+sparsity reduces to a score-based method (reviewer's Issue 4): the paper explicitly acknowledges this relationship in the stage-wise analysis. Not a weakness.
- "Paradigm shift" as hyperbole: style nitpick, not substantive.
- Computational cost not discussed: complexity analysis is in Appendix F (exists in original submission).
- Missing likelihood form for AD: deferred to Appendix A (exists in original submission).
- Noise distribution assumption: a design choice, not a flaw; likely discussed in appendix.
- Several section-by-section editorial observations.

## Novel Insights

The harsh critique's most useful observation involves the Linear_U anomaly in Table 4. Rather than being a flaw, this pattern could actually deepen the paper's contribution if discussed explicitly: the fact that the score-based search finds a graph scoring worse (by AUROC) than the seed, yet the SCL model trained on the search outputs still substantially improves, suggests that the generated training data contains useful causal signal that transcends the proxy score. This tension between the search objective and the final evaluation metric is worth surfacing and analyzing.

## Suggestions

1. **Clarify SCL training procedure in the main text.** State whether the model is trained from scratch or fine-tuned from a pre-trained checkpoint, and include training hyperparameters (learning rate, epochs, optimizer).
2. **Explain the Linear_U anomaly.** Why does the score-based search regress on this dataset? What does this reveal about the score-AUROC relationship?
3. **Add variance for Sachs and Syntren.** Report bootstrap or multi-seed standard deviations for real-world results.
4. **Report λ and its sensitivity.** State the value used, how it was chosen, and show a sweep.
5. **Fix the acceptance probability formulation** to handle potentially negative scores, or justify that scores are always positive.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>