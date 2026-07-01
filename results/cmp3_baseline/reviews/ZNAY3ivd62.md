## Summary
The paper introduces GUI-Spotlight, a visual grounding model that iteratively refines its focus on a GUI screenshot by invoking specialized tools (crop, extract, find_color) through a multi-turn inference loop trained with reinforcement learning. The model achieves 52.8% on ScreenSpot-Pro with only 18.5K training samples, demonstrating strong data efficiency compared to models trained on millions of samples.

## Strengths
- **Data efficiency**: GUI-Spotlight attains competitive or superior accuracy on ScreenSpot-Pro using only 18.5K curated samples, whereas many baselines use orders of magnitude more data (e.g., V2P-7B with 9.6M). This is a practically important result.
- **Comprehensive ablations**: The paper systematically ablates RL algorithms (GRPO variants) and reward designs, including negative results, providing valuable insights for the community on multi-turn tool-using RL.
- **Well-designed three-stage pipeline**: The staged training (SFT warm-up, stabilized RL with auxiliary cross-entropy loss, high-resolution refinement) is technically sound and each stage is motivated by observed failure modes.
- **Strong benchmark performance**: GUI-Spotlight surpasses all prior 7B models on ScreenSpot-Pro and achieves gains across multiple backbone initializations, indicating robust transfer.

## Weaknesses
### Fatal
None.

### Major
- **Overstatement of UI-Vision results**: The paper claims GUI-Spotlight “outperforming other 7B models” on UI-Vision, but Table 4 shows UI-Venus-Ground-7B achieves 26.5% vs. GUI-Spotlight’s 23.4%. This claim is inaccurate and should be corrected.
- **Incomplete acknowledgment of weaknesses on OSWorld-G**: On OSWorld-G (Table 5), GUI-Spotlight (62.7%) underperforms GTA-1-7B (67.7%), a 7B model trained on 1.56M samples. The paper’s narrative emphasises data efficiency but does not clearly discuss this performance gap, which tempers the claimed “substantial” improvement over comparable models.
- **Modest gains on several benchmarks**: While improvements over the UI-TARS-1.5-7B backbone are consistent, the margins are often small (e.g., +1.6 points on ScreenSpot-Pro over UI-Venus-7B, +0.8 on OSWorld-G). The adjective “substantial” is not universally supported.

### Minor
- **Hand-designed tool set may lack generality**: The three tools (extract, find_color, crop) are manually defined and may not optimally cover all GUI layouts. The paper does not analyse failure cases where the tools are insufficient or misused.
- **Incremental algorithmic contribution**: The main RL modification (adding a cross-entropy loss on correct tool-use examples to stabilise GSPO) is a relatively standard trick; its novelty is modest.
- **Missing inference cost analysis**: The multi-turn tool pipeline increases inference latency, but the paper provides no discussion of computational cost or practical latency, which is relevant for deployment.
- **Limited comparisons on iterative refinement**: Section 5.4 compares only two hand-crafted training-free baselines; a comparison with other recent iterative grounding methods (e.g., UnivGR1) would better contextualise the approach.

## Nice-to-Haves
- Error analysis or case studies illustrating when the iterative spotlighting succeeds or fails would deepen understanding.
- A discussion of the trade-off between number of inference turns and accuracy would help practitioners.
- An estimate of the data removal rate in the filtering pipeline (beyond the 50% UGround retention) would clarify dataset construction effort.

## Novel Insights
None beyond the paper’s own contributions. The idea of iteratively focusing attention via tool calls is intuitive, and the paper’s main novelty lies in the stable RL training recipe for this multi-turn setting.

## Suggestions
- Correct the UI-Vision claim to reflect that UI-Venus-Ground-7B achieves higher accuracy.
- Explicitly discuss the performance gap against GTA-1-7B on OSWorld-G in the main text.
- Include an analysis of inference latency and the number of tool calls per example.
- Provide a qualitative analysis of failure cases (e.g., when the model makes incorrect tool choices).
- Consider comparing against other multi-step grounding approaches beyond simple training-free baselines.

## Score and Decision
MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>