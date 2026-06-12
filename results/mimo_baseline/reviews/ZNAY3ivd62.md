## Summary

GUI-Spotlight introduces an iterative visual grounding approach for GUI agents that dynamically invokes specialized tools (crop, extract, find_color) to progressively narrow focus on target UI elements. The model is trained through a three-stage pipeline combining SFT warm-up on tool-use trajectories and two stages of modified GSPO-based reinforcement learning, achieving 52.8% on ScreenSpot-Pro with only 18.5K training samples—surpassing 7B models trained on millions of samples.

## Strengths

- **Impressive data efficiency:** GUI-Spotlight achieves 52.8% on ScreenSpot-Pro with 18.5K samples, surpassing V2P-7B (50.6%, 9.6M samples) and GTA-1-7B (50.1%, 1.56M samples). This is a genuinely compelling result demonstrating that structured tool-augmented reasoning can compensate for data scarcity.

- **Systematic empirical investigation (including negative results):** The paper transparently benchmarks 8 RL algorithm variants (Section 4.1) and multiple reward designs (Section 4.2), clearly documenting which approaches failed. For instance, continuously updating the reference policy and retaining only top-p% most-uncertain prompts both degraded performance. This level of methodological transparency is rare and highly valuable for practitioners.

- **Effective stabilization mechanism for multi-turn RL:** The auxiliary cross-entropy loss $\mathcal{J}'(\theta)$ on tool-filtered positive examples prevents training collapse (Figure 3, right panel), addressing a genuine and under-studied challenge of applying RL to multi-turn tool-use scenarios where sparse format-invalid trajectories cause policy drift.

- **Consistent improvements across benchmarks:** The method demonstrates gains over its base models across three diverse benchmarks—ScreenSpot-Pro (+14.1 points over UI-TARS-1.5-7B), UI-Vision (+5.3 points), and OSWorld-G (+0.8 points)—and from two different backbone initializations, suggesting the approach generalizes rather than overfitting to one setting.

## Weaknesses

### Fatal
None.

### Major

- **Training-free baseline is weak, partially inflating the contribution of multi-step reasoning.** In Section 5.4, the training-free multi-turn baseline (Strategy ①) achieves only 7.6% on ScreenSpot-Pro, demonstrating the base model has no inherent tool-use capability. The repeated single-turn baseline (Strategy ②) achieves 47.6%. GUI-Spotlight achieves 52.8%, a 5.2-point gap. However, Strategy ② is a simple heuristic (crop centered on predicted point, re-predict), and no comparison is provided against stronger iterative inference baselines such as best-of-N sampling, self-consistency, or tree-search over multiple attempts. The headline 52.8% result is strong on its own, but the paper's claim about the *value of learned multi-step reasoning* would be more convincingly supported with a stronger non-trained iterative baseline.

- **Missing inference cost analysis.** Multi-turn tool invocation at inference time involves multiple forward passes (potentially up to $T_{\max}$ turns), each processing the full dialogue history with accumulated image crops. This can substantially increase latency and GPU memory compared to single-pass models. For GUI agents where response time matters, this tradeoff between accuracy and speed is critical and should be quantified. How many turns does the model typically take? What is the average inference time compared to a single-shot baseline?

### Minor

- **Figure 2 axis inconsistency and unclear stage labeling.** The figure caption and table describe stages 0–3, but the x-axis labels read "Stages" with tick marks from 0 to 3. The description says "Stage 1: We perform one epoch of SFT on 2561 trajectories" while the figure labels this as the jump from 39.3% (Stage 0) to 17.8% (Stage 1)—a *drop*. Yet the surrounding text says "Stage 1" corresponds to SFT with 2561 samples and "Stage 2" to RL with 12K. The accuracy table beneath the figure shows Stage 0 at 39.3% (base model), Stage 1 at 17.8% (after SFT), Stage 2 at 49.6% (after 12K RL), and Stage 3 at 52.8% (after 4K more RL). This is confusing—the sharp drop from 39.3% to 17.8% after SFT deserves explicit discussion, as it suggests the model is learning tool invocation but losing its direct grounding ability during imitation learning.

- **Inconsistent gains across backbones on UI-Vision.** GUI-Spotlight initialized from Qwen2.5-VL-7B achieves only 8.3% on UI-Vision (Table 4), barely above UGround-V1-7B (12.9%) and far below the UI-TARS-initialized variant (23.4%). This suggests the method is substantially backbone-dependent, which somewhat undermines the "generality" claim. The paper should discuss why the Qwen backbone fails so dramatically on UI-Vision compared to other benchmarks.

- **find_color tool utility is unclear.** The find_color tool searches for a target RGB value, which seems poorly matched to the task of locating a text label or button by its description. In the inference pipeline (Figure 1), only extract and crop are demonstrated. The paper does not show how often each tool is invoked or what fraction of successful trajectories use find_color. Without this analysis, the tool may be contributing little or even adding noise.

### Trivial
None.

## Nice-to-Haves

- A per-tool invocation frequency analysis showing which tools are used how often and in what sequences would strengthen understanding of the learned behavior.
- Analysis of the number of inference turns distribution and its correlation with accuracy.
- Comparison with simpler data augmentation strategies (e.g., random crop-based training without RL) to isolate the contribution of RL versus tool-augmented data.

## Novel Insights

The most novel insight is that multi-turn tool-use in visual grounding can be effectively trained via RL when accompanied by a stabilizing supervised loss on correctly-formatted outputs. The finding that standard GRPO/GSPO collapses around 300 steps due to format-violation drift—and that filtering positive examples into the cross-entropy term prevents this—is a practical insight that extends beyond GUI grounding to any multi-turn tool-augmented RL setting. The ablation showing that the Extract tool is easier to use than Crop (Section 4.2) and should receive lower reward weight is also a useful design principle: rewarding easier intermediate steps more encourages the model to build up grounding progressively rather than attempting precise actions prematurely.

## Suggestions

- Add a table or figure showing average inference turns, latency, and GPU memory usage compared to single-pass baselines.
- Provide tool-usage statistics (frequency of each tool per trajectory, average number of turns).
- Discuss the SFT accuracy drop (39.3% → 17.8%) more explicitly—this is a significant regression that warrants explanation, even if RL subsequently recovers and surpasses the baseline.
- Add a stronger iterative inference baseline (e.g., best-of-N with self-consistency) to better quantify the value of learned multi-step reasoning over simple heuristics.

## Score and Decision

The paper presents a well-motivated and empirically validated approach to an important problem. The data efficiency claim is strong and well-supported, the ablations are thorough, and the negative result documentation adds genuine value to the community. The major weaknesses—missing inference cost analysis and a somewhat weak iterative baseline—weigh against acceptance but do not invalidate the core contribution. The inconsistent backbone behavior on UI-Vision and the unanalyzed find_color tool are minor issues. Overall, this is a solid methodological contribution with clear practical value.

MY FINAL SCORE: 6.5
MY FINAL DECISION: Accept