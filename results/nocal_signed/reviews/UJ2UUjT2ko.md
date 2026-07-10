The impact scores confirm the picture: all four strengths are highly impactful (+9.0 to +9.7), while all weaknesses are mild (-3.6 maximum). No fatal or major issues. This overwhelmingly supports acceptance.

Here is my final consolidated review:

---

## Summary

This paper challenges the prevailing view that LMs retrieve bound entities solely via a positional mechanism. Through counterfactual interchange interventions on the residual stream, it identifies two additional information channels — a **lexical mechanism** (retrieving the target using its bound counterpart) and a **reflexive mechanism** (retrieving the target via a direct pointer). The core finding is a U-shaped pattern: the positional mechanism dominates at context edges but becomes diffuse and unreliable in middle positions, where the lexical and reflexive mechanisms compensate. The paper validates this across 9 models (2B–72B, three families) and 10 binding tasks, and formalizes the findings in a parametric causal model achieving 95% JSS.

## Strengths

- **Clean counterfactual design to disambiguate three information channels.** The dataset construction in §3.2 is methodologically well-executed: by designing counterfactual inputs where each mechanism predicts a different entity under intervention, the paper creates an unambiguous test bed for determining which information channel drives LM behavior in a given setting. The worked example (Figure 1, Equation 1) makes the logic easy to verify.

- **Careful confound removal for the reflexive mechanism (§3.4).** The paper correctly identifies that the basic counterfactual design cannot distinguish the reflexive pointer from the answer entity, and runs a controlled experiment where the counterfactual answer is absent from the original input. The result — at layer ℓ the model does *not* output the absent entity, while at layer ℓ+1 it does (ruling out a suppressive mechanism) — cleanly validates a reflexive pointer distinct from a direct answer copy.

- **Extensive evaluation breadth.** The paper evaluates across 9 models from 3 families (Llama 3.1, Gemma 2, Qwen 2.5) spanning 2B to 72B parameters, on up to 10 binding tasks. The core U-shaped pattern (positional dominates at edges, lexical/reflexive compensate in the middle) appears robust across this sweep, substantiating that the findings are not artifacts of a single model or template.

- **The causal model (§4, Equation 2) formalizes the qualitative findings.** The parametric model — a Gaussian positional term with quadratic variance plus one-hot lexical and reflexive terms — encodes the paper's main empirical claims in a falsifiable form. The ablation results (e.g., removing the lexical term barely affects JSS for t_entity=1 but severely for t_entity=3, and vice versa for the reflexive term) cleanly validate the asymmetry predicted by the autoregressive left-to-right attention constraint.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **The "competitive synergy" claim in §3.3 overstates the evidence.** The paper observes that when lexical and positional indices are close in the counterfactual design, the lexical logit contribution is amplified while the positional one is weakened, and terms this "competitive synergy." However, this observation is about the output logit distribution under intervention, which is equally consistent with the three information channels operating independently and being combined through an aggregation function. The term implies mechanism-level interaction that has not been causally demonstrated — no intervention directly manipulates one channel and measures a causal effect on another. A more conservative framing (e.g., "the logit contributions are not purely additive; proximity in index space modulates their weights") would better match the evidence. *(Impact: -3.2)*

- **The 95% JSS is a goodness-of-fit on the counterfactual intervention distribution, without quantitative out-of-distribution validation of the parametric model.** The 95% JSS reported in §4 measures fit on held-out points from the same 8,000-combination counterfactual grid (i_P, i_L, i_R). The parametric model's quantitative fit is not evaluated on the free-form text experiments in §5, which report only effect category distributions and accuracy — not JSS (or any analogous metric) for Equation 2's predictive fit on naturalistic inputs. This limits the strength of the claim that the *parametric form* generalizes beyond the counterfactual intervention distribution. *(Impact: -3.6)*

- **The reflexive mechanism is behaviorally validated but computationally underspecified in the main text.** The §3.4 confound-removal experiment cleanly demonstrates that the reflexive mechanism involves a pointer distinct from the answer entity. However, its computational implementation is minimally characterized in the main text. The paper gestures toward Appendix Figure 7 and attention knockout experiments (§F, stripped by parser), but does not trace the pointer to specific attention patterns or sub-circuitry in the main body. *(Impact: -1.0)*

### Trivial

- **No confidence intervals for the main intervention results (§3.3, Figures 2, 3).** The causal model fits in §4 include CIs, but the intervention effect proportions in §3.3 are reported without variability measures. Given 150 interventions per condition, this information is feasible to include. *(Impact: -0.1)*

## Nice-to-Haves

- Clarify in §2 that the paper's level of analysis is the *information content* of the residual stream (causal abstraction level), not circuit-level identification, to preempt misinterpretation.
- Note in the main text whether the learned σ(i_P) curve (Figure 5) transfers across models and tasks, or is specific to gemma-2-2b-it on the *music* task.
- Acknowledge explicitly in §5 that the free-form text experiments use entity-less filler sentences, which lack competing bindings and anaphora present in more natural text.

## Removed Points

These points were flagged by the input reviewer but are removed per filtering rules:

1. **"Three mechanisms are information channels, not distinct sub-circuits"** — Removed as a scope-mismatch. The paper explicitly represents each mechanism as a causal model with a single intermediate variable (§3.1), which is the standard level of analysis in the causal abstraction framework (Geiger et al. 2021, 2025a,b). The paper never claims circuit-level identification (specific attention heads or MLP neurons), so demanding that granularity is outside the paper's stated scope.

2. **Missing limitations section** — Removed per hard rule (the parser strips appendix/reference sections; the full submission may contain this in the appendix or elsewhere).

## Novel Insights

Beyond the paper's own contributions, the synthesis reveals a concrete mechanistic hypothesis for the "lost-in-the-middle" effect: the positional mechanism (dominant at context edges) becomes diffuse for middle positions, while the lexical and reflexive mechanisms that could compensate also weaken under heavy padding (§5, Figure 6). This connects a well-known behavioral phenomenon to specific, testable information-channel dynamics inside the model — a framing that could guide future long-context improvement work.

## Suggestions

- Report JSS (or an analogous fit metric) for the parametric model on the free-form text experiments to strengthen the generalization claim.
- Soften or more precisely scope the "competitive synergy" language to reflect output-level modulation rather than proven mechanism-level interaction.
- Summarize key results from the attention knockout experiments and reflexive mechanism's attention patterns from the appendix in the main text.
- Add confidence intervals or variability measures to the main intervention figures where feasible.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>