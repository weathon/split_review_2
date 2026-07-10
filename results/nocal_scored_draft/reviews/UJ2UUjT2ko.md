## Summary

This paper challenges the prevailing view that LMs retrieve bound entities purely through a positional mechanism. Through controlled interchange interventions, the authors show that LMs mix three mechanisms — positional, lexical, and reflexive — with the positional mechanism becoming unreliable in middle positions while lexical and reflexive mechanisms compensate. The findings are validated across 9 models (2B–72B, three families) and up to 10 binding tasks, and are formalized in a causal model achieving JSS = 0.95.

## Strengths

- **Clean counterfactual design that separates three mechanisms (Section 3.2).** The construction of original/counterfactual pairs such that positional, lexical, and reflexive mechanisms each predict different entities under interchange intervention is well-executed and non-trivial — the three predictions could easily have been correlated.

- **Rigorous validation of the reflexive mechanism (Section 3.4).** The modified counterfactual (where the answer does not appear in the original context) cleanly rules out the confound that the patched signal is the answer entity itself rather than a pointer. The control at layer ℓ+1 rules out a suppressive mechanism.

- **The causal model and its ablations (Section 4, Figure 5).** The model achieves JSS = 0.95 vs. 0.44 for the one-hot positional baseline. Ablations are informative and consistent with the intervention results. The learned σ curve (wide in middle, narrow at ends) directly mirrors the paper's central empirical finding.

- **Scope across models and tasks.** Nine models (2B–72B, three families) on up to ten binding tasks — substantially more than prior work on entity binding, which typically examines 1–2 small models on 1–2 narrow settings.

- **The paper takes an honest position on what it cannot explain.** The mixed cases (Figure 2) are discussed rather than hidden, and the analysis in Figure 3 acknowledges the three-mechanism picture is not fully complete.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Section 5's claim about explaining the lost-in-the-middle effect is not well-supported by the evidence presented.** The free-form text experiment shows accuracy remaining stable at ~0.85 while mechanism contributions shift — meaning the model still performs well. The lost-in-the-middle effect is about performance degradation; a stable accuracy of 0.85 with shifting mechanism contributions indicates strategy adaptation, not a failure explanation. The paper's hedging ("suggests," "might be") limits the overclaim, but the framing still implies more than the data supports.

- **The three mechanisms are characterized at the behavioral level rather than through circuit isolation.** The experiment patches the full last-token residual stream and classifies a mechanism based on which entity's probability increases, but this does not localize distinct circuits — it identifies what information the residual stream carries. The paper's framing of "mechanisms" implies more granularity than the method can distinguish. This does not invalidate the contribution, but the contribution is better described as a behavioral characterization of what information is used rather than a demonstration of distinct internal circuits.

- **At middle positions (Figure 2, index=10), ~30% of the patch effect falls into "mixed" or "no effect" categories** not explained by any single mechanism. While the paper acknowledges these cases and trains a Gaussian positional term that captures some of this diffuseness (bringing JSS to 0.95), the three-mechanism picture provides a clean account primarily at the extremes. The middle region is messier than the prose suggests.

- **JSS=0.95 is measured on held-out intervention data from the same counterfactual setup used for training the causal model.** The free-form text experiment (Section 5) tests generalization but uses a different metric (distribution of effects rather than JSS), creating a gap between the headline number and the generalization evidence. The free-form evaluation is informative but does not directly verify the model's predictive accuracy on novel inputs.

### Trivial

- **The reflexive mechanism is described in somewhat ambiguous terms** — both as a "direct pointer" (Section 3.1) and as involving a two-step retrieval process ("the queried entity is retrieved with a direct pointer that was previously retrieved via the query entity," line 53). These suggest different claims about what the mechanism does. The validation in Section 3.4 supports the pointer interpretation, but the description could be more precise.

- **No confidence intervals or variance information is reported for the core patch-effect results** (Figures 2, 4). CIs are reported only for the causal model (Figure 5). For a study that quantifies how much each mechanism contributes, the absence of variance information on the main intervention results is notable.

## Nice-to-Haves

- Report task-level accuracy on the main 20-group binding experiments to help readers contextualize whether the mechanistic analysis describes successful computation or failure modes.
- Finer-grained circuit localization (e.g., patching specific attention heads or MLP neurons rather than the entire residual stream) would move from behavioral characterization toward circuit isolation.

## Removed Points

*These points are flagged to be removed; treat them with caution.*
- "The boxes and music tasks are never described in the main text" — Removed because this refers to appendix content (Appendix Table 1) that was stripped by the parser; the tasks exist in the original submission.
- "No behavioral (task-level) accuracy reported for the main experiments" — Moved to Nice-to-Haves. The paper's focus is mechanistic analysis, not task performance, but reporting it would contextualize the findings.
- "The quantitative contribution may be overstated" (Critical Issue 4 from the harsh critic) — Removed because the causal model is correctly evaluated on held-out intervention data, which is standard practice for causal abstraction. The free-form text experiment separately tests generalization using an appropriate different metric.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- In Section 5, either run the experiment until accuracy degrades (longer padding/more noise) or reframe the results as showing mechanism adaptation rather than a mechanistic explanation of lost-in-the-middle.
- Add confidence intervals or variance bands to the main intervention results (Figures 2, 4) to strengthen the quantitative grounding.
- Clarify the description of the reflexive mechanism to consistently present it as a pointer mechanism, resolving the ambiguity between "direct pointer" and "two-step retrieval" framings.

## Score and Decision

The paper makes a genuine contribution: a well-designed counterfactual setup that cleanly separates three retrieval mechanisms, rigorous validation of each, broad scaling across models/tasks, and a simple causal model that captures the dynamics. The weaknesses are all minor — they concern framing precision and the scope of claims in one section, not the validity of the core results. The strengths are strongly evidenced and non-trivial. Overall the paper warrants acceptance with revisions.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>