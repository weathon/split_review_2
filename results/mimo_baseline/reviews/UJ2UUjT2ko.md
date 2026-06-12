## Summary

This paper challenges the prevailing view that language models retrieve bound entities solely via a positional mechanism. Through extensive interchange intervention experiments on 9 models (2B–72B parameters across Gemma, Qwen, and Llama families) and 10 binding tasks, the authors identify three mechanisms—positional, lexical, and reflexive—that are mixed together, with the mixture depending on the target entity's position. They develop a causal model combining all three that achieves 95% Jensen-Shannon similarity with actual next-token distributions, and demonstrate generalization to longer inputs interleaved with free-form text.

## Strengths

- **Rigorous counterfactual design to distinguish three mechanisms.** The paired original/counterfactual inputs (§3.2) are carefully constructed so that interchange interventions on P, L, and R each produce distinct predictions. The further validation of the reflexive mechanism (§3.4) using counterfactuals where the answer entity doesn't appear in the original input is particularly elegant, eliminating the confound between a reflexive pointer and the answer entity itself. This is methodologically stronger than prior work on binding.

- **Broad experimental coverage establishing generalizability.** The paper evaluates 9 models across 3 families and sizes from 2B–72B, plus 10 binding tasks—far broader than prior work (Prakash et al., 2025 studied only n∈{2,3} and the last entity in a group; Prakash et al., 2024 and Dai et al., 2024 found weak positional effects in n=7 settings but didn't explain them). The consistent pattern across all models and tasks strengthens the core claims substantially.

- **Quantitative causal model with strong performance.** The mixture model M achieves 0.95 JSS, dramatically outperforming the prevailing positional-only view (0.44 JSS, worse than uniform at 0.50). The ablation study in Figure 5 clearly shows that each mechanism is necessary and their contributions shift predictably with t_entity, providing a clean decomposition of model behavior.

- **Mechanistic explanation for the "lost-in-the-middle" effect.** The finding that the positional mechanism becomes diffuse in middle positions (Figures 2–3), with lexical/reflexive mechanisms compensating, and that padding experiments (§5) show the lexical mechanism weakening relative to an increasingly noisy positional mechanism provides a compelling mechanistic account of a well-known empirical phenomenon.

## Weaknesses

### Fatal

None.

### Major

- **All experiments use templatic binding tasks.** Every experiment—including the padding experiments—preserves the exact same syntactic template "X loves Y" with only filler sentences added between groups. Real-world entity binding involves varied syntactic structures (relative clauses, coreference, discourse-level binding). The paper's framing that findings apply to "more natural settings" (§5) overstates the case, since the structural regularity of templates likely makes binding easier than natural text. The "X loves Y" structure also means the model can exploit syntactic position within clauses, which wouldn't generalize to arbitrary binding patterns.

- **The causal model is trained and evaluated on intervention-generated distributions, not natural model behavior.** The 0.95 JSS figure measures agreement between the causal model and the LM's behavior *under interchange interventions*, not the LM's natural next-token predictions. The paper doesn't directly validate that the causal model's predicted distributions match what the model outputs in standard (un-intervened) inference on these tasks. While the intervention-based approach is sound for mechanistic analysis, reporting 95% "agreement" without this caveat could mislead readers about the causal model's fidelity.

### Minor

- **Limited characterization of mechanism interaction dynamics.** The paper describes "competitive synergy" qualitatively (lexical amplifies near positional, suppresses near reflexive) but the causal model M treats the mechanisms additively with learned position-dependent weights—it doesn't model the suppressive/amplifying interactions between mechanisms. The gap between the qualitative observations and the quantitative model isn't fully addressed.

- **No control for entity-specific co-occurrence statistics.** Counterfactual designs swap specific entities (e.g., "Ann" ↔ "Joe"), but different name-food pairs may have different memorized co-occurrence statistics that could confound intervention results. The paper doesn't discuss this potential confound or how the entity sets are constructed to control for it.

### Trivial

None.

## Nice-to-Haves

- A direct comparison of the causal model's predicted distributions against the LM's actual natural (un-intervened) predictions on these same tasks would significantly strengthen the paper.
- Analysis on non-templatic binding structures (e.g., coreference resolution tasks) would substantially increase confidence in naturalistic generalization.
- Visualization of which attention heads implement each mechanism would connect the abstract causal model more tightly to specific model components.

## Novel Insights

The paper's most novel insight is that the positional mechanism's unreliability in middle positions is not simply a failure mode but is actively compensated for by complementary lexical and reflexive mechanisms, creating a robust retrieval system. The finding that the choice between lexical and reflexive mechanisms is governed by the target entity's position within a group (t_entity)—with lexical dominating when the target is at the end (accessible via backward attention) and reflexive dominating when at the beginning (requiring a forward pointer)—is a genuinely new observation that prior work on binding did not capture, as it restricted analysis to t_entity = m. The connection between this mechanism mixture and the "lost-in-the-middle" effect provides a mechanistic bridge between interpretability research and the practical context-length limitations of LMs.

## Suggestions

- Report the causal model's accuracy on un-intervened natural model predictions as a supplementary validation metric.
- Add at least one non-templatic binding task (e.g., from coreference benchmarks) to test naturalistic generalization more directly.
- Provide a brief analysis of entity set construction to address potential co-occurrence confounds.

## Score and Decision

This paper makes a clear, well-supported contribution by identifying and quantifying three mechanisms for entity binding that go substantially beyond the prevailing positional-only view. The experimental methodology is rigorous, the breadth of evaluation (9 models, 10 tasks) is commendable, and the causal model achieves impressive quantitative agreement. The main limitation—reliance on templatic tasks—tempers enthusiasm but does not invalidate the contribution, as the templatic setting is the appropriate first step and the padding experiments provide meaningful evidence of robustness. The work advances our mechanistic understanding of in-context reasoning and has clear implications for improving long-context LMs.

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>