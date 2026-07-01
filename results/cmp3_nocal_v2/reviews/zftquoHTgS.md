Now I have all the information needed. Let me write the final consolidated review.

## Summary

This paper identifies the "underthinking" phenomenon in LongCoT LLMs (prematurely abandoning promising reasoning paths) and proposes SmartSwitch, a plug-and-play inference framework that detects thought switches via linguistic cues, scores the abandoned thought with a PRM, and intervenes with a "deepen prompt" when the PRM score exceeds a threshold. Experiments on 5 mathematical reasoning benchmarks across DeepSeek-R1-Distill (1.5B–32B) and QwQ-32B show consistent accuracy gains (e.g., +16.7 points on AIME25 for the 1.5B model) and simultaneous reductions in inference time and token usage.

## Strengths

1. **Well-diagnosed problem with concrete evidence.** Section 3 provides both qualitative (Figure 1a) and quantitative (Figures 1b, 2) support for the underthinking phenomenon. The UF metric, while simple, effectively demonstrates that the problem is widespread across model families, worsens with problem difficulty, and correlates with incorrect answers. This diagnostic contribution is independently useful.

2. **Simple, practical, model-agnostic method.** SmartSwitch is genuinely plug-and-play: no fine-tuning, works across model sizes (1.5B to 32B) and families (DeepSeek-R1-Distill, QwQ-32B), uses only off-the-shelf components (linguistic cue detection, a PRM, a deepen prompt). The implementation is clearly described in Section 4.2.

3. **Non-trivial efficiency gains alongside accuracy improvements.** Tables 2 and 3 show that SmartSwitch reduces both response length and wall-clock inference time while improving accuracy — a genuinely surprising finding for a method that explicitly encourages deeper thinking. For example, 33.7% time reduction on AIME24 for the 1.5B model (Table 3) and 16.2% length reduction on correct answers for the 32B model (Table 2).

4. **Informative ablations.** The "Always Intervene" baseline (Table 4) cleanly shows that indiscriminate intervention degrades performance (18.9% vs 20.0% vanilla), establishing the need for selective PRM-guided intervention. The comparisons of four process division strategies (Table 6), five score-mapping strategies (Table 7), and five PRMs (Table 4) provide reasonably thorough characterization of the method's components.

5. **Preservation of correct answers.** Section 5.3 reports that SmartSwitch maintains 100% accuracy on previously correct answers while recovering 20% of previously incorrect ones (R1-Distill-14B on AIME24). This is strong evidence that the method is genuinely helpful on hard cases without regressing on easy ones.

## Weaknesses

### Fatal
None.

### Major

1. **Threshold sensitivity with potential test-set contamination on AIME24.** The promising score threshold τ=0.70 is used for all main results (Table 1). Table 8 presents a sweep of τ on AIME24 itself, showing τ=0.70 is the peak — meaning the AIME24 accuracy numbers in Table 1 are partially in-sample for this critical hyperparameter. The sensitivity is extreme: for the 7B model, accuracy goes from 66.7% (τ=0.70) to 43.3% (τ=0.71), below the 55.5% vanilla baseline. A 0.01 shift collapses the gain. The paper acknowledges the sensitivity as a limitation (lines 318) but does not select τ on a held-out validation set. **Why it matters:** The AIME24 results are the primary headline gains; their magnitude may be overstated due to test-set tuning. The AIME25 results are not affected by this concern (tuning was on AIME24), and the pattern of improvement across the other four benchmarks (AIME25, AMC23, MATH-500, GaoKao2023en) is consistent and independent, so this weakness does not invalidate the overall contribution — but it weakens the strongest claimed result.

### Minor

2. **Limited comparison to alternative methods.** The only underthinking-specific baseline compared (Table 5) is TIP (Wang et al., 2025), tested on a single model (1.5B) on a single benchmark (AIME24), without evidence that TIP's hyperparameters were tuned for this setting. The paper claims SmartSwitch "performs best" but the comparative evaluation is too narrow to support broad superiority claims. This is fixable by expanding to more models and benchmarks.

3. **No confidence intervals or variance estimates.** All results are point estimates averaged over 32 responses (Tables 1–3) with no confidence intervals, standard deviations, or statistical significance tests. Given the extreme threshold sensitivity documented in Weakness 1, variance information would help readers assess whether the reported gains are robust.

4. **The UF metric conflates brevity with shallowness, and SmartSwitch mechanically reduces it.** The Underthinking Frequency metric (Eq. 1) defines underthinking purely by token length (|T_i| < L). SmartSwitch's intervention adds tokens to thoughts it targets, which mechanically reduces UF regardless of whether reasoning depth actually improves. The paper interprets UF reduction as evidence of "more focused and coherent reasoning trajectories" (line 214), but this inference is not well-supported by the metric alone. **Why it matters:** The accuracy results (Table 1) are the real evidence for the method's effectiveness; the UF reductions should be treated as a secondary signal, not primary validation. The paper would benefit from clarifying this distinction.

5. **The contribution of the intervention framework beyond the PRM is not fully disentangled.** Table 4 shows that PRM quality dominates the method's performance (Universal-PRM-7B at 36.7% vs. Qwen2.5-Math-PRM-7B at 21.1%). The "Always Intervene" baseline (18.9%) establishes that intervention without PRM guidance hurts, which partially addresses this concern. However, the paper does not isolate what the intervention module (the deepen prompt and backtracking) contributes beyond simply using the PRM score to decide whether to continue or switch at each step. The paper's distinctive claim is the integrated framework, but the evidence is largely consistent with the PRM being the decisive component.

### Trivial

6. **"Ours" line in Figure 1(b) is confusing.** The Figure 1(b) caption includes an "Ours" line plotted alongside other models, but this appears in Section 3 (preliminary analysis) before the SmartSwitch method is introduced in Section 4. It is unclear whether this line refers to a vanilla model not previously listed or to a SmartSwitch-enhanced model shown as a preview. Clarifying this would improve readability.

7. **Maximum intervention count (capped at 3) is not ablated.** The paper fixes the intervention cap at 3 throughout but never studies its effect. Similarly, the single "deepen prompt" phrasing is not varied.

## Nice-to-Haves

- Select τ on a held-out validation subset (e.g., 5 AIME24 problems) and report results on the remainder, then show τ=0.69 and τ=0.71 as bounds to quantify robustness.
- Expand the TIP comparison to at least 2–3 models and 2–3 benchmarks, with appropriate hyperparameter tuning for TIP.
- Add a simple heuristic baseline (e.g., intervene on thoughts exceeding a length threshold without PRM scoring) to quantify the PRM's added value beyond a cheap proxy.
- Report confidence intervals (e.g., bootstrap over the 32 responses) for the main accuracy results.
- Ablate the maximum intervention count (e.g., 1, 3, 5, unlimited) and study whether the deepen prompt phrasing matters.
- Discuss the computational cost of PRM invocations: for models with 50+ thought switches (Figure 4b), the method may call the 7B PRM dozens of times per problem, which matters for practitioners comparing cost vs. benefit.

## Removed Points

These points were raised in the input review but are removed (with justification):

- *"The list of linguistic cues is not visible in the main text; it is impossible to assess recall without seeing it."* — The paper explicitly states the full list is in Appendix D.2. The appendix is stripped from the review copy. Per policy, absence of appendix content is not a weakness of the paper.
- *"The cognitive science analogy is not directly supported by evidence."* — The analogy is used as rhetorical motivation, not as a claimed finding. The reviewer correctly notes this is "fine for a motivation section."
- *"TPR quality dominates — the framework may be a thin wrapper over the PRM."* — The "Always Intervene" baseline already demonstrates that the framework without PRM guidance hurts. The PRM alone (a scoring model) cannot produce answers without a generation framework. This criticism overstates the case; the remaining valid kernel is kept as Weakness 5.
- *"No comparison to self-consistency, tree-of-thoughts, or reread baseline."* — These are general reasoning strategies, not specific underthinking mitigation methods. The paper's scope is underthinking mitigation, and evaluating against every possible inference strategy is beyond reasonable scope.
- *"Mechanistic evidence for efficiency improvement is insufficient."* — The paper provides a plausible explanation (pruning wasteful oscillation) and reports actual wall-clock time reductions. More granular analysis would strengthen the claim but the current evidence is not empty.

## Novel Insights

The input reviews surface one genuinely novel observation beyond the paper's own contributions: the extreme non-monotonicity of the threshold sensitivity (Table 8) suggests the PRM scores cluster around 0.70 for the types of thoughts the model is about to abandon. The fact that performance collapses at τ=0.71 (above 0.70) rather than degrading smoothly implies the PRM's calibration has a sharp cutoff — thoughts scored ≥0.70 are disproportionately likely to be genuinely promising, while those at 0.69 or below are not. This diagnostic insight about PRM score distributions (not explored in the paper) could be valuable for understanding when PRM-guided intervention works and why it is fragile.

## Suggestions

1. For the camera-ready version, pick τ on a small held-out subset of AIME24 (e.g., 5 problems), then report results on the remaining 25. Show results at τ=0.69 and τ=0.71 as sensitivity bounds alongside the chosen τ to give readers a realistic picture of robustness.
2. Expand the TIP comparison to at least 3 models × 2 benchmarks, with tuned TIP parameters. Add a simple heuristic baseline (e.g., intervene on any thought that exceeds 200 tokens without PRM scoring) to further isolate the PRM's contribution.
3. Add bootstrap confidence intervals to the main accuracy tables.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>