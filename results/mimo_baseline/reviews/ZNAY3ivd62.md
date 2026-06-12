## Summary

The paper introduces GUI-Spotlight, a multi-tool iterative visual grounding model for GUI agents that dynamically narrows its focus on target UI elements using three specialized tools (crop, extract, find_color). The model is trained in three stages—SFT warm-up on tool-use trajectories, RL on filtered data with a modified GSPO objective that includes an auxiliary cross-entropy loss for stability, and final RL refinement on high-resolution data—achieving 52.8% on ScreenSpot-Pro with only 18.5K training samples, outperforming 7B baselines trained on orders of magnitude more data.

## Strengths

- **Impressive data efficiency**: GUI-Spotlight achieves 52.8% on ScreenSpot-Pro with only 18.5K samples, substantially outperforming V2P-7B (50.6% with 9.6M samples) and GTA-1-7B (50.1% with 1.56M). This is a genuinely compelling result for practitioners with limited data budgets.

- **Thorough empirical analysis including negative results**: Section 4 systematically benchmarks RL algorithm variants (Figure 3, left) and reward designs (Figure 4), explicitly reporting which approaches failed (e.g., top-p% uncertain prompts, continuous reference policy updates, dense answer reward). This documentation is valuable for the community building similar systems.

- **Effective stabilization of multi-turn RL**: The auxiliary cross-entropy loss on tool-filtered positives (J'(θ)) addresses a real problem—RL training collapse due to format violations in multi-tool settings—and Figure 3 (right) convincingly shows it prevents oscillation that afflicts vanilla GRPO/GSPO.

## Weaknesses

### Fatal

None.

### Major

- **SFT stage causes a catastrophic accuracy drop (39.3% → 17.8%) that is poorly explained**: The base UI-TARS-1.5-7B achieves 39.3% on ScreenSpot-Pro without any tool use, but after Stage 1 SFT on 2561 tool-use trajectories, accuracy drops to 17.8%. This 21.5-point collapse suggests the model initially performs much worse when forced to use tools than when predicting directly. The paper acknowledges the model "remains under-aligned" but does not analyze why SFT is so destructive, whether SFT is truly necessary versus jumping to RL, or whether this represents a fundamental tension in the training approach. This is a significant gap given that Stage 1 is the foundation of the entire pipeline.

- **Substantial gap between training-free iterative inference and trained GUI-Spotlight is modest**: Section 5.4 shows that strategy ② (repeated single-turn inference with the untrained base model) already achieves 47.6%, while the fully trained GUI-Spotlight achieves 52.8%—only a 5.2-point improvement. The multi-step inference framework itself contributes ~8 points over direct prediction (39.3% → 47.6%), while the entire three-stage training pipeline contributes only 5.2 additional points. This raises questions about whether the training complexity is justified by the marginal gains.

- **Mixed results across benchmarks contradict claims of generality**: On OSWorld-G (Table 5), GUI-Spotlight achieves 62.7% but GTA-1-7B reaches 67.7% (5 points higher). On UI-Vision (Table 4), UI-Venus-Ground-7B achieves 26.5% vs GUI-Spotlight's 23.4%. The paper's claims of "substantially outperforming comparable 7B baselines" and robustness are only supported by ScreenSpot-Pro results, while the method underperforms on two of three evaluation benchmarks.

- **Extreme sensitivity to base model choice**: GUI-Spotlight initialized from Qwen2.5-VL-7B-Instruct achieves only 38.7% on ScreenSpot-Pro (identical to the raw UI-TARS-1.5-7B baseline) and 8.3% on UI-Vision (worse than most baselines). The paper claims this shows "our RL objective and multi-tool coordination transfer beyond UI-specialized backbones," but the Qwen variant is actually worse than many non-tool-augmented 7B baselines, suggesting the method does not transfer well.

### Minor

- **No ablation on individual tools**: The paper introduces three tools (crop, extract, find_color) but never evaluates their individual contributions. The reward analysis in Section 4.2 examines Crop/Extract weighting but doesn't isolate find_color. Given that find_color uses a relatively ad-hoc mechanism (10×10 patch scanning in CIE Lab space), understanding its contribution is important.

- **No latency/efficiency analysis at inference time**: The multi-step tool-augmented inference requires multiple forward passes and image processing operations. For practical GUI agents where click latency matters, the computational overhead relative to single-pass methods should be discussed.

- **Figure 2 stage labeling is inconsistent with text**: The figure/table shows Stage 0 with "2561 samples" but Stage 0 should be the base model. The stage numbering between the figure and Section 3.2.2 text creates confusion about which accuracy corresponds to which training phase.

### Trivial

None.

## Nice-to-Haves

- A latency comparison between GUI-Spotlight and single-pass baselines, since iterative inference adds computational cost
- Analysis of when the model chooses to use each tool and whether tool selection patterns correlate with task difficulty
- Error analysis categorizing failure modes (wrong tool choice, premature stopping, format violations)

## Novel Insights

The paper's most valuable contribution beyond its method is the empirical insight that adding an auxiliary cross-entropy loss on tool-filtered correct samples prevents RL training collapse in multi-turn tool-use settings. This is a non-obvious finding: standard GRPO/GSPO degrades after ~300 steps due to format violations producing sparse, volatile rewards, while the auxiliary loss maintains stable reward curves. This finding could benefit any multi-turn RL training pipeline for tool-using agents, not just GUI grounding.

## Suggestions

- Add an ablation that individually removes each tool to quantify their contributions and justify the specific tool set
- Analyze and explain the SFT accuracy collapse in more detail—is this because the model needs to learn to use tools before it can leverage them, and could curriculum learning or a different SFT strategy mitigate this?
- Include a comparison of wall-clock inference time vs. single-pass baselines to contextualize the multi-step overhead
- Reconcile the figure stage numbering with the text to eliminate confusion

## Score and Decision

The paper presents an interesting iterative tool-use approach for GUI grounding with strong data efficiency. However, the SFT collapse, modest gains over training-free multi-step inference (5.2 points), mixed benchmark results (underperforming on 2 of 3 benchmarks), and heavy dependence on base model quality weaken the core claims. The empirical insights section on RL training stability is valuable but not sufficient to overcome these issues.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: Reject