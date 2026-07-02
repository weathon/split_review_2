Now I have a clear calibration picture. Let me write the final review.

**Calibration Summary:**

| Anchor Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| UGround (GUI grounding, large-scale) | kxnoqaisCT.md | 7.75 (Accept) | 1, 2 | Much stronger empirical case (up to 20% gains, 6 benchmarks), but less method novelty. Our paper is weaker empirically. |
| Reinforced UI Instruction Grounding | nNyjIMKGCH.md | 5.75 (Reject) | 1, 2 | Uses RL for UI grounding; similar score band. Our paper has more novel method but a factual error this one doesn't. |
| SpiritSight Agent | jY2ow7jRdZ.md | 5.25 (Reject) | 1, 2 | GUI agent with grounding; similar evaluation weaknesses. Our paper has stronger method novelty. |
| Aguvis | FHtHH4ulEQ.md | 5.50 (Reject) | 2 | Pure-vision GUI agent; similar evaluation scope concerns. |
| UI-Pro | 5wmAfwDBoi.md | 4.25 (Reject) | 1 | GUI grounding recipe; less method novelty than ours. |
| Grounding MLLM in GUI World | M9iky9Ruhx.md | 6.00 (Accept) | 1 | Cleaner empirical story, less method novelty. |

**Round 1 Bracket:** 4.0 – 5.5 (between UI-Pro/SpiritSight territory and Reinforced UI Grounding territory)

**Narrowing:** The paper's method novelty and thorough RL documentation push it above UI-Pro (4.25). But the factual error on UI-Vision, the unexplained SFT collapse, and the asymmetric comparison are similar in severity to SpiritSight's (5.25) evaluation concerns. The Reinforced UI Grounding paper (5.75) had cleaner claims and no factual errors. **Final score: 4.5.**

---

## Summary

This paper proposes GUI-Spotlight, a GUI visual grounding model that iteratively invokes specialized visual tools (crop, extract, find_color) over multiple rounds to progressively narrow focus on a target screen element. The model is trained in three stages (SFT warm-up on tool-usage trajectories, then RL with a modified GSPO objective incorporating tool-filtered cross-entropy loss). On ScreenSpot-Pro, GUI-Spotlight (52.8%) surpasses several 7B baselines including V2P-7B (50.6%) and GTA-1-7B (50.1%) while using only 18.5K training samples. The paper provides systematic ablation of RL variants and reward designs, including negative results.

## Strengths

1. **Genuinely novel method design.** The iterative "spotlighting" approach — training a model to dynamically invoke crop/extract/find_color tools over multiple rounds to progressively narrow focus — departs meaningfully from the standard single-pass coordinate-prediction paradigm. The three-tool set is cleanly designed for the nested-focus task.

2. **Thorough RL exploration with negative results documented.** Section 4.1 evaluates seven RL variants under identical conditions, and Section 4.2 compares sparse vs. dense reward formulations and different reward weightings. Including variants that *hurt* performance (e.g., top-p% uncertain prompts, continuous reference-policy updates) is genuinely useful for practitioners and substantiates Contribution #3.

3. **Data efficiency is a real property.** Achieving 52.8% on ScreenSpot-Pro with 18.5K training samples is notable when compared to UGround-7B (10M samples, 16.5%) or V2P-7B (9.6M samples, 50.6%).

4. **Robustness to backbone choice.** The method improves over both UI-TARS-1.5-7B (UI-specialized) and Qwen2.5-VL-7B-Instruct (general), with the Qwen-initialized variant gaining +11.9 points on ScreenSpot-Pro. This suggests the training procedure transfers beyond UI-specific representations.

## Weaknesses

### Fatal
None.

### Major

1. **Factually inaccurate claim on UI-Vision.** Section 5.2 states GUI-Spotlight "outperforms other 7B models" on UI-Vision. Table 4 shows UI-Venus-Ground-7B at 26.5%, exceeding GUI-Spotlight's 23.4%. This claim is wrong as written and must be corrected.

2. **Unexplained SFT accuracy collapse undermines trust in the training pipeline.** Figure 2 shows Stage-1 SFT on 2,561 tool-usage trajectories causes accuracy to crash from 39.3% (untrained base model) to 17.8% — a 21.5-point drop. The paper's explanation ("the model learns to invoke multiple tools but remains under-aligned") does not adequately address why learning tool-use syntax should more than halve visual grounding accuracy. Whether this is catastrophic forgetting of visual representations, format overfitting, or distributional shift is unanalyzed. The subsequent RL recovery (49.6%, then 52.8%) may be undoing damage rather than building constructively. A clear diagnosis is needed for the pipeline to be trusted.

3. **Headline comparisons are confounded by asymmetric inference budget.** GUI-Spotlight uses multiple model forward passes interleaved with tool executions per prediction, while all baselines use a single forward pass. The Section 5.4 ablation (52.8% vs. repeated single-turn inference at 47.6% from the same base model) is a useful step, but limited to one base model (UI-TARS-1.5-7B). We do not know whether other competitive models (V2P-7B, GTA-1-7B) would narrow or close the gap if given the same iterative setup. The abstract's framing of "substantially outperforming comparable 7B baselines" does not acknowledge this asymmetry.

### Minor

4. **Modest and inconsistent gains across benchmarks.** The headline +2.0 points over UI-Venus-7B on ScreenSpot-Pro is narrow. On OSWorld-G, GUI-Spotlight (62.7%) is essentially flat against its base model (61.9%, +0.8 points) and trails GTA1-7B (67.7%) by 5 points. On UI-Vision, it trails UI-Venus-Ground-7B. The "substantially outperforming" framing in the abstract and contributions list is overstated given these results.

5. **No inference cost reporting.** The iterative pipeline requires 2–4 model forward passes per prediction (vs. 1 for all baselines), but the paper reports no average tool-call count, latency, or FLOPs comparison. This cost-accuracy tradeoff is material for any practical deployment assessment and should be reported.

6. **No statistical significance for OSWorld-G result.** The +0.8 point improvement over the base model on OSWorld-G (62.7% vs. 61.9%) falls within likely measurement noise, yet no standard errors or significance tests are provided.

7. **RL variant ⑦ is not disentangled.** In Section 4.1, variant ⑦ (tool-filtered positives + additional cross-entropy loss) achieves 47.6%, a large jump from 37.3% (GRPO). The two modifications are combined without ablating separately, so the reader cannot isolate which component drives the gain.

8. **Reward ratio experiment has limited granularity.** The Crop/Extract reward ratio comparison in Section 4.2 tests only two configurations (0.25/0.05 and 0.15/0.15). The claimed 10.5% gap may be driven by the specific weight values chosen rather than a general principle.

### Trivial
None.

## Nice-to-Haves

- Extending the controlled iterative-inference comparison (Section 5.4) to at least one other competitive base model (e.g., running the repeated single-turn strategy from V2P-7B or GTA-1-7B) would strengthen the claim that RL training adds value beyond iterative inference.
- An error analysis categorizing failure modes (failed tool calls, wrong tool selection, imprecise coordinates) would strengthen the empirical contribution.
- Reporting the total compute footprint of the data collection pipeline (Selenium crawling + Qwen2.5-VL-72B auditing) would contextualize the "only 18.5K training samples" narrative.

## Removed Points

These points were flagged for removal from the original review; treat with caution:

- **Bucket construction may create perverse incentives (Section 3.2.2):** The reviewer speculated uniform sampling across tool types could create perverse incentives. This is speculative and unsupported by evidence in the paper. REMOVED.
- **Compute investment of data pipeline not acknowledged:** The reviewer noted that the 15K high-res samples and Qwen2.5-VL-72B auditing represent substantial compute. This is a nice-to-have clarification, not a core weakness. MOVED to Nice-to-Haves.
- **Missing error analysis:** The reviewer noted no error analysis. This is a nice-to-have, not a core flaw. MOVED to Nice-to-Haves.
- **Section 5.4 may not control for total compute budget:** The reviewer asked whether the comparison controls for same number of forward passes. Subsumed by Weakness #5 (inference cost) and too speculative to stand alone. REMOVED.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Correct the UI-Vision claim in Section 5.2 to acknowledge that UI-Venus-Ground-7B (26.5%) exceeds GUI-Spotlight (23.4%) on this benchmark.
2. Add a diagnostic analysis of the Stage-1 SFT accuracy collapse (e.g., measuring whether visual representations degrade or whether the model simply overfits to tool-call formatting).
3. Report average number of tool calls per prediction and compare inference latency with single-pass baselines.
4. Add standard errors or confidence intervals for key comparisons, especially the OSWorld-G result.
5. Tone down the "substantially outperforming" framing in the abstract and Contribution #1 to accurately reflect the magnitude and consistency of gains.
6. Disentangle the two components of RL variant ⑦ in Section 4.1 to show which drives the improvement.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>