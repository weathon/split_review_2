Now let me write the final consolidated review.

## Summary

This paper identifies the "underthinking" problem in LongCoT reasoning — models prematurely switching between shallow thoughts without sufficient exploration — and proposes SmartSwitch, a training-free, plug-and-play inference framework. SmartSwitch uses linguistic cues to detect thought switches, employs an off-the-shelf process reward model (PRM) to evaluate the potential of abandoned thoughts, and conditionally intervenes by backtracking and inserting a deepen prompt to encourage deeper exploration. On five math benchmarks, SmartSwitch yields substantial accuracy gains (up to +23.3 points on AIME25) while reducing both token usage and inference time for most models.

## Strengths

- **The "underthinking" problem is well-motivated with empirical grounding.** Section 3 provides qualitative evidence (Figure 1a: an example of 74 shallow thoughts) and quantitative evidence (Figures 1b, 2) establishing that the phenomenon is widespread across models, correlates with problem difficulty, and is more prevalent in incorrect answers.

- **SmartSwitch delivers substantial and consistent accuracy gains.** Table 1 shows improvements across all five benchmarks for models from 1.5B to 32B parameters. Notable examples include: DeepSeek-R1-Distill-Qwen-1.5B on AIME24 (28.9% → 40.0%, +11.1 points) and on AIME25 (20.0% → 36.7%, +16.7 points); the 7B model on AIME25 (30.0% → 53.3%, +23.3 points). These are training-free gains on competition-level math.

- **Efficiency improves alongside accuracy.** Tables 2–3 show that SmartSwitch reduces inference time (e.g., 33.7% reduction for the 1.5B model on AIME24) and response length in most cases, despite the overhead of PRM scoring and backtracking. This dual improvement — better accuracy with less computation — is a strong practical finding.

- **Thorough ablation study provides evidence for design choices.** The paper systematically ablates PRM selection (Table 4), process division strategy (Table 6), score aggregation (Table 7), and score threshold (Table 8). The "Always Intervene" baseline (18.9% vs. 36.7% with PRM-guided intervention) cleanly demonstrates that selective, PRM-guided intervention is essential.

## Weaknesses

### Major

- **The score threshold τ=0.70 was determined by ablating on AIME24 (Table 8), and the same threshold is used to report AIME24 results in Table 1.** Performance is highly sensitive to this threshold: for the 1.5B model, τ=0.69 gives 30.0% while τ=0.70 gives 40.0% (a 10-point absolute swing). Without a held-out validation set, it is unclear whether the reported gains reflect genuine improvement or test-set overfitting. The cross-model consistency (τ=0.70 is the best threshold for all five models in Table 8) partially mitigates this concern, but the paper should validate the threshold on a separate development set or use a principled selection criterion.

- **The comparison with prior underthinking mitigation work (TIP, Wang et al., 2025) is limited to a single setting: one model (1.5B) on one benchmark (AIME24) in Table 5.** This is insufficient to support the claim that SmartSwitch "performs best" relative to competing methods. The comparison should be extended to at least one more model size (e.g., 7B or 14B) and one more benchmark (e.g., AIME25 or AMC23).

### Minor

- **The Underthinking Frequency metric (UF_L, Eq. 1) is definitionally tied to token count.** Since SmartSwitch's intervention mechanically increases thought length on intervened thoughts, the UF_L reduction shown in Figure 4 is partially a direct consequence of the intervention design, not independent evidence of improved reasoning quality. The accuracy gains in Table 1 are the real evidence; UF_L reduction should be presented as a descriptive property of the mechanism rather than converging independent evidence.

- **The paper reports pass@1 accuracy without confidence intervals or statistical significance tests.** Some gains are modest (e.g., +1.9 points on MATH-500 for the 1.5B model), and the reader cannot assess which margins are reliable vs. within sampling noise for 32 responses.

- **The contribution framing overstates novelty relative to the PRM's role.** While the paper is transparent that SmartSwitch uses an off-the-shelf PRM (Abstract, Limitations), Table 4 shows that the PRM choice dominates performance: Universal-PRM-7B gives 36.7% while Qwen2.5-Math-PRM-7B gives only 21.1% (near the vanilla 20.0% baseline), and "Always Intervene" (18.9%) is worse than vanilla. This suggests the core intelligence comes from the PRM's scoring capability, and the framework is primarily a mechanism to deploy it. Reframing SmartSwitch as "a practical framework for PRM-guided online intervention" would better reflect the contribution.

- **The advantage of the proposed process division strategy (v4) is not uniform across model scales (Table 6).** For QwQ-32B, all four strategies are within 3.3 points (70.0%–73.3%), while for the 1.5B model, v4 is 10 points ahead. The paper should discuss when v4 matters most and why.

### Trivial

- For DeepSeek-R1-Distill-Qwen-14B, the total response length slightly increases under SmartSwitch (14,128.90 → 14,480.20 tokens, +0.4%), though the "only correct" column decreases by 15.7%. This minor exception to the efficiency narrative should be explicitly acknowledged.

## Nice-to-Haves

- A controlled experiment comparing SmartSwitch + PRM against a simpler PRM-based post-hoc approach (e.g., PRM-guided best-of-N selection) would clarify whether the online intervention mechanism itself provides additional value beyond the PRM's scoring capability.
- A human evaluation of whether the PRM's scores correlate with ground-truth thought quality (e.g., conditional probability of correctness given PRM score) would strengthen confidence in the method's mechanism.
- Extending the TIP comparison to more model sizes and benchmarks would substantiate the claim of superiority over prior underthinking mitigation methods.

## Removed Points

These points from the Harsh Critic input were removed per filtering rules; treat them with caution:

- **Linguistic cue detection recall/precision**: Removed because the paper already acknowledges this limitation in Section 6 (Discussion): "our current thought-switch detection mechanism is based on linguistic cues, which may not capture all instances of premature abandonment." The paper is aware of this constraint.
- **PRM training data overlap with evaluation benchmarks**: Removed as speculative — there is no evidence in the paper to verify or refute whether Universal-PRM-7B was trained on AIME/AMC/MATH data, and the reviewer has no external sources to substantiate this.
- **14B total response length increase framed as a weakness**: Demoted to Trivial because the data is transparently presented in Table 2 and the decrease in the "only correct" column (−15.7%) is the more relevant efficiency metric.

## Novel Insights

None beyond the paper's own contributions. The threshold-tuning concern and the PRM-dependency observation are credible critical analyses of the paper's methodology, but they do not constitute novel insights about the problem domain.

## Suggestions

- Use a held-out validation set to determine the score threshold τ, or report results with cross-validation.
- Add confidence intervals or error bars for all accuracy numbers.
- Extend the comparison with TIP to at least one additional model size and one additional benchmark.
- Reframe the contribution as "a practical framework for PRM-guided online intervention during LongCoT reasoning" to avoid overstating novelty beyond the empirical results.

## Score and Decision

The paper identifies a genuine problem (underthinking in LongCoT reasoning) and proposes a practical inference-time intervention that yields substantial and consistent accuracy gains (up to +23.3 points) across multiple model sizes and benchmarks while also improving efficiency. The empirical results are the paper's primary strength and are impressive for a training-free method. However, two issues warrant attention: (1) the score threshold was validated on the test set rather than a held-out set, and performance is extremely sensitive to this threshold; (2) the comparison with prior work (TIP) is limited to a single setting, making the claimed superiority insufficiently supported. Both issues are addressable. The paper's contributions are real and practically significant.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>