## Summary

This paper introduces IRIS, a reinforcement learning framework that fine-tunes autoregressive text-to-image (T2I) models using only an intrinsic reward defined as the negative self-certainty (NSC) of the model’s output token distribution—i.e., minimizing the KL divergence from a uniform distribution. The key insight is that, unlike in language reasoning where maximizing self-certainty improves performance, for T2I generation, lower self-certainty leads to more visually rich and diverse images that better align with human preferences. Experiments on Janus-Pro models across GenEval, T2I-CompBench, and WISE show that IRIS achieves performance competitive with methods that use external reward models, without requiring any human labeled data or domain-specific verifiers.

## Strengths

- **Novel application of intrinsic reward to T2I:** IRIS is the first framework to successfully apply a purely intrinsic, self-derived reward signal (negative self-certainty) for aligning autoregressive T2I models, removing the need for human annotation or external verifiers.
- **Clear and interesting empirical observation:** The paper convincingly demonstrates, both qualitatively and quantitatively, that minimizing self-certainty improves T2I quality, in stark contrast to findings in text-based reasoning. This task-dependent role of self-certainty is a valuable insight.
- **Thorough ablation study:** The authors systematically ablate key design choices (CoT vs. no CoT, maximize vs. minimize image/text self-certainty, forward vs. backward KL, RL vs. direct optimization) and provide clear visualizations, which strongly support their design decisions.
- **Comprehensive evaluation:** Results are reported on three diverse benchmarks (GenEval, T2I-CompBench, WISE) with multiple sub-categories, and the authors include standard deviations and comparisons to a range of external reward baselines.

## Weaknesses

### Fatal
None.

### Major

- **Performance advantage over external rewards is marginal and not convincingly “superior”:** The paper claims IRIS is “competitive with or superior to external rewards,” but in almost all benchmark sub-categories (especially for the 7B model) IRIS underperforms the T2I-R1 external-reward baseline. For 1B, overall scores are 0.72 vs. 0.75 (GenEval), 0.37 vs. 0.38 (WISE); for 7B, 0.77 vs. 0.78 and 0.48 vs. 0.50. The narrative overstates the empirical advantage. The “superior” claim rests on early-training steps, not final best performance.
- **Insufficient explanation for the core mechanism:** The paper attributes the success of minimizing self-certainty to producing “visually rich and colorful images,” but does not provide a deeper analysis of why this occurs—e.g., does it increase diversity, reduce mode collapse, or improve exploration? The observation is correlational, and the causal link is not convincingly established.
- **The “enhanced reasoning” claim is not well supported:** The paper states that IRIS “enhances the reasoning capabilities of T2I models” and improves “reasoning and planning.” However, the intrinsic reward only encourages token-level uncertainty, not any explicit reasoning process. The improvements on WISE could stem from increased output diversity rather than genuine reasoning. Without targeted reasoning metrics or analysis, this claim is overreaching.
- **Comparison of self-certainty trends (Figure 2) is not a controlled experiment:** The comparison between LLM math reasoning (Qwen2.5) and T2I image tokens (Janus-Pro) uses different models, tasks, and reward structures. The conclusion that “external reward decreases self-certainty for T2I” may not generalize, and the figure would be more convincing if the same model architecture was trained on both text and image tasks with similar reward types.
- **Direct optimization fails, but the reason is unclear:** The ablation showing that direct gradient maximization of NSC leads to collapse (Figure 9) is a significant practical limitation. The paper’s explanation that GRPO is “more conservative” is vague. Since the reward is differentiable, this failure suggests instability or reward gaming that warrants deeper investigation.

### Minor

- The contribution statement “first to successfully train T2I models without external reward supervision” is a strong claim that is not verified against any potential prior unpublished or concurrent work. While plausible, it could be toned down.
- The paper focuses exclusively on Janus-Pro models. The “Further Discussions” section mentions other architectures but provides no experiments, leaving the generality of IRIS unvalidated.
- The wording “enhance the reasoning capabilities” is used throughout, but T2I CoT is more about planning and description than reasoning in the traditional sense; this may confuse readers.
- Table 1 contains minor formatting quirks (e.g., unclear abbreviations “Und.” and “Gen.” in the caption).

### Trivial

- Some grammatical issues: “the model’s the Negative Self-Certainty” in Section 3.
- Figure captions are excessively long and contain repetitive descriptions.

## Nice-to-Haves

- Apply IRIS to other T2I architectures (e.g., diffusion models, masked models) to demonstrate architectural generality.
- Include a human evaluation study to confirm that the increased visual richness translates to genuine preference.
- Provide a deeper analysis of the relationship between self-certainty and output diversity (e.g., using LPIPS, FID, or diversity metrics) to support the causal explanation.
- Compare against other intrinsic reward baselines such as simple entropy maximization or curiosity-driven exploration.

## Novel Insights

The paper’s central insight—that the role of model self-certainty is task-dependent, with high certainty beneficial for objective reasoning (math, code) and low certainty beneficial for subjective generation (T2I)—challenges the prevailing assumption that maximizing self-certainty is always desirable. This observation, supported by empirical evidence, offers a useful guideline for designing alignment methods for multimodal generative models. The demonstration that a purely intrinsic reward can produce T2I improvements comparable to external reward models, despite the stylistic nature of the task, is noteworthy.

## Suggestions

- **Rewrite the “superior” claim:** Clearly state that IRIS achieves competitive performance to external-reward methods, and only use “superior” if statistically significant evidence across all metrics supports it. Highlight that the main advantage is the elimination of external supervision, not raw score.
- **Strengthen the reasoning claim:** Either provide explicit evidence that IRIS improves compositional or world-knowledge reasoning (e.g., through CoT quality analysis or human evaluation) or reframe the claim as improved visual diversity and prompt-following.
- **Add a controlled experiment for self-certainty trends:** Train the same LLM on both text reasoning and T2I with a comparable reward setup to directly show the divergence in self-certainty behavior.
- **Discuss the collapse in direct optimization more thoroughly:** Analyze whether it is due to reward hacking, instability, or the non-convex nature of the objective, and suggest potential remedies.
- **Soften the novelty claim:** Acknowledge that the self-certainty reward is adapted from text domain work (Zhao et al., Zhang et al.) and the main novelty is its application and reversal for T2I.

## Score and Decision

The paper presents a novel and interesting approach to reward-free T2I alignment, supported by thorough ablations. However, the empirical performance is not clearly superior to existing external-reward methods, several key claims (“superior”, “enhanced reasoning”) are overstated, and the core mechanism remains insufficiently explained. Despite these weaknesses, the contribution is valuable and the experiments are solid.

MY FINAL SCORE: 4.0</score>
MY FINAL DECISION: Reject</decision>