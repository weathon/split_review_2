Here is the final consolidated review.

---

## Summary

GUI-Spotlight proposes an iterative tool-use approach for GUI visual grounding, where a 7B model is trained via a three-stage pipeline (SFT → RL → refinement) to invoke specialized tools (crop, extract, find_color) that progressively narrow focus. On ScreenSpot-Pro, it achieves 52.8% accuracy with only 18.5K training samples, surpassing several 7B baselines trained on millions of examples. The paper also documents a thorough ablation of RL algorithm variants and reward designs.

## Strengths

- **Data efficiency is genuinely impressive and well-supported.** Table 3 shows GUI-Spotlight (52.8%) surpassing V2P-7B (50.6%, 9.6M samples), GTA-1-7B (50.1%, 1.56M samples), and UI-Venus-7B (50.8%, 107K samples) while using only 18.5K training samples. The ratio of performance to training data is striking and forms the paper's most compelling contribution.

- **The iterative spotlighting idea is cleanly implemented.** The three-tool design (extract for coarse quadrant narrowing, crop for fine-grained refinement, find_color for color-guided focusing) maps naturally onto the problem of locating elements in cluttered GUI screens. Algorithm 1 is clearly specified, and the registry mechanism tracking offsets relative to the original image is sound.

- **The RL exploration in Section 4 is thorough and transparent.** The paper documents 7 algorithm variants, compares sparse vs. dense reward formulations, and includes negative results (discarded modifications ④ and ⑥). This provides genuine practical value for practitioners building similar systems.

- **The ablation in Section 5.4 provides a meaningful controlled comparison.** Strategy ② (repeated single-turn inference at 47.6%) vs. GUI-Spotlight (52.8%) isolates the benefit of learned tool coordination over a training-free iterative baseline, confirming that the training does real work beyond simple iteration.

## Weaknesses

### Fatal

None.

### Major

- **Inference cost is entirely unquantified, making the practical contribution uninterpretable.** GUI-Spotlight performs multi-turn tool invocations at inference time, each requiring a forward pass of the 7B model. The paper reports none of the following: average number of tool calls per example, median/maximum steps, total inference latency, or FLOPs per query compared to a single-step baseline. Furthermore, the maximum turn limit `T_max` in Algorithm 1 (line 57: "for t = 1 to T_max do") is never assigned a value anywhere in the paper. Without this information, the practical value of a method that uses multi-step inference cannot be assessed. The repeated single-turn ablation (Strategy ② at 47.6%) shows that most of the gap to single-step methods comes from iteration itself, but without knowing how many steps each strategy uses, even this comparison is incomplete. A method using 3× the inference compute for a 5-point gain (52.8% vs. 47.6%) is interesting; a method using 10× is a much harder sell for interactive GUI agents.

- **A factual error in the UI-Vision reporting.** Section 5.2 states: "GUI-Spotlight trained from UI-TARS-1.5-7B surpassing its backbone UI-TARS-1.5-7B by +5.3 points and outperforming other 7B models." However, Table 4 shows UI-Venus-Ground-7B at **26.5%** vs. GUI-Spotlight (UI-TARS) at **23.4%** — a 3.1 percentage point gap in the wrong direction. This also affects the contribution statement (line 31), which claims "substantially outperforming comparable 7B baselines." On UI-Vision, this claim is incorrect for at least one 7B baseline. The ScreenSpot-Pro claim is unaffected, but this error should be corrected and discussed.

### Minor

- **OSWorld-G results weaken the generality claim, but the paper does not discuss this.** On OSWorld-G (Table 5), GUI-Spotlight (62.7%) is outperformed by GTA1-7B (67.7%) — a 5-point gap. The paper's Section 5.3 discussion emphasizes how GUI-Spotlight "remains competitive with 72B-scale models" and "provides clear benefits even when starting from a non-UI-specific backbone," but does not acknowledge or explain the gap to a 7B baseline. This narrows the scope of the method's claimed generality.

- **The `find_color` tool requires the model to predict a target RGB value, but how the model does this is not analyzed.** The paper describes the tool's mechanics (scanning 10×10 patches, minimizing ΔE in CIE Lab space) but provides no analysis of: how often the model guesses the correct color, how sensitive performance is to this prediction, or what happens when the color prediction is wrong. An ablation with oracle RGB values would clarify the ceiling of this tool.

- **The headline comparisons do not explicitly disclose the inference protocol asymmetry.** The abstract and introduction compare GUI-Spotlight (multi-step, iterative) to single-step baselines (V2P-7B, GTA-1-7B, UI-Venus-7B) without noting that the inference cost structure is fundamentally different. The paper does not hide its multi-step nature — the pipeline diagram and algorithm make this clear — but the central framing emphasizes data efficiency rather than the accuracy-vs-compute tradeoff. The ablation in Section 5.4 partially addresses this, but the headline results are presented without this context.

### Trivial

- **Missing variance or confidence intervals.** The three benchmarks are modest in size (ScreenSpot-Pro, UI-Vision at ~83 apps, OSWorld-G at 564 screens). Reporting standard deviations or confidence intervals would strengthen the reliability of the reported numbers. (This is not a standard requirement for this class of benchmark, but would be a welcome addition.)

## Nice-to-Haves

- The data filtering pipeline uses Qwen2.5-VL-72B to audit samples, discarding ~50% of UGround data. An analysis of whether this filtering systematically removes challenging cases that the smaller model would need to learn would strengthen the data curation story.
- Reporting `T_max` and the distribution of inference steps across benchmarks would directly address the largest evaluation gap.

## Removed Points

- **"Strategy ② surpasses most single-step baselines" (from the harsh critic):** This claim is factually incorrect. Strategy ② achieves 47.6%, which is below V2P-7B (50.6%), GTA-1-7B (50.1%), and UI-Venus-7B (50.8%) as shown in Table 3. Removed.
- **Request for standard grounding benchmarks (RefCOCO, etc.):** The paper is scoped to GUI-specific grounding; requesting non-GUI benchmarks is scope creep. Removed.
- **Data filtering bias speculation:** The concern that Qwen2.5-VL-72B filtering could systematically remove challenging cases is a reasonable hypothesis but unsupported by evidence in the review. Removed.
- **Missing related works:** Removed per instructions.

## Novel Insights

The most interesting observation emerging from the reviews is that the repeated single-turn baseline (Strategy ②) at 47.6% already rivals or approaches many single-step 7B methods, despite using no learned tool coordination. This suggests that the inference protocol itself — the ability to iterate and refine — accounts for a large fraction of the total gain, with trained tool coordination contributing the remaining ~5 points. Neither the paper nor the critic fully unpacks what the 5-point marginal gain represents: is it better cropping decisions, more efficient use of `find_color`, or fewer wasted turns? Disentangling these would be a valuable direction for understanding what RL actually learns in this setting.

## Suggestions

1. **Report inference cost.** Add a table showing average/median/maximum number of tool calls per example on each benchmark, total wall-clock time per query, and a comparison with the repeated single-turn baseline. Assign a concrete value to `T_max`.
2. **Correct the UI-Vision claim.** Remove or qualify "outperforming other 7B models" in Section 5.2 and add a brief discussion of why GUI-Spotlight underperforms UI-Venus-Ground-7B on this benchmark.
3. **Add an oracle ablation for `find_color`.** Evaluate performance on a subset where the correct RGB is provided, to bound the impact of color prediction errors.
4. **Discuss the OSWorld-G result.** Acknowledge the gap to GTA1-7B and explain possible reasons (e.g., domain differences, training data overlap).
5. **Add confidence intervals or error bars** to the main results tables.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>