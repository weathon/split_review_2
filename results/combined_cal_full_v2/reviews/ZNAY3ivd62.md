Now let me write the final consolidated review.

## Summary

GUI-Spotlight proposes an iterative focus-refinement approach for GUI visual grounding, where a model equipped with three specialized tools (*extract*, *find_color*, *crop*) progressively narrows its search region on a screenshot until the target element is precisely located. The model is trained in three stages (SFT → RL → RL with high-resolution data) using a modified GSPO algorithm stabilized with an auxiliary cross-entropy loss. On ScreenSpot-Pro, GUI-Spotlight (init. UI-TARS-1.5-7B) achieves 52.8% with only 18.5K curated training samples, surpassing several 7B models trained on millions of samples.

## Strengths

- **Well-motivated iterative spotlighting formulation (Section 3.1).** The three tools form a natural coarse-to-fine hierarchy (quadrant-level → color-guided → precise coordinate) that maps cleanly onto the problem structure. Algorithm 1 is clearly specified.

- **Informative RL algorithm and reward design ablations (Sections 4.1–4.2, Figures 3–4).** The paper systematically tests multiple GRPO/GSPO variants (items ①–⑦), documents which ones degrade performance, provides training dynamics showing the collapse of vanilla GSPO, and compares sparse vs. dense reward designs. The documentation of negative results is a genuine methodological contribution.

- **Real data efficiency finding on ScreenSpot-Pro.** Using 18.5K curated samples to reach 52.8% vs. V2P-7B's 50.6% with 9.6M samples is a non-trivial reduction. The cleaning pipeline (Laplacian variance filtering, Qwen2.5-VL-72B auditing) is well-specified.

- **Two backbone initializations demonstrate generality.** GUI-Spotlight initialized from the non-UI-specific Qwen2.5-VL-7B-Instruct gains +11.9 points over its raw baseline (Table 3), showing the approach transfers beyond UI-specialized backbones.

## Weaknesses

### Major

- **Stage-1 SFT collapse is inadequately explained.** ScreenSpot-Pro accuracy drops from 39.3% (base model, no training) to 17.8% after SFT on 2,561 tool-usage trajectories — a 21.5-point decline. The paper only states the model "remains under-aligned" without any investigation. Possible causes (catastrophic forgetting of visual grounding, low-quality SFT trajectories from the Qwen2.5-VL-72B teacher, format overfitting, systematic tool-output parsing failures) are not analyzed. Since the subsequent RL recovery (49.6% in Stage 2, 52.8% in Stage 3) is a central claim, understanding what the SFT actually does to the model is important for establishing that the RL is genuinely learning an effective tool-use policy rather than simply undoing SFT-induced damage.

### Minor

- **Gains are highly uneven across benchmarks.** The improvement over UI-TARS-1.5-7B is +14.1 points on ScreenSpot-Pro but only +5.3 on UI-Vision and a negligible +0.8 on OSWorld-G (Tables 3–5). On OSWorld-G, GUI-Spotlight (62.7%) also trails GTA1-7B (67.7%). The claim of "substantially outperforming comparable 7B baselines" is accurate on ScreenSpot-Pro but overstates the general case.

- **Figure 2 has a stage-numbering inconsistency between text and figure.** The text states Stage 1 uses 2,561 trajectories (SFT), Stage 2 uses 12K examples (RL), and Stage 3 uses 4K samples. However, Figure 2's table shows Stage 0 at 39.3% with 2,561 samples and Stage 1 at 17.8% with 12K samples — a mismatch. The reader cannot tell whether "Stage 0" represents the untrained base model (which should have 0 training samples) or an SFT checkpoint, because the sample-count column is misaligned with the text's stage descriptions.

- **The iterative ablation (Figure 5) would benefit from an additional control.** Strategy ② (repeated single-turn inference without tools) reaches 47.6%, only 5.2 points below the full system (52.8%). While Strategy ① (7.6%) confirms the base model cannot use tools zero-shot, the modest gap between simple iteration and the full system means the contribution of the RL-trained tool policy would be clearer with a control where the same tool set is given to the base model via prompting (zero-shot, multi-turn).

- **No variance or statistical significance is reported for any accuracy number.** Given that some comparisons involve small gaps (e.g., GUI-Spotlight 52.8% vs. V2P-7B 50.6% — a 2.2 point difference), the reader cannot assess whether these differences are meaningful.

- **Inference cost is not analyzed.** The iterative pipeline requires multiple model calls per query (2–3 tool invocations + final answer), while single-step baselines use one forward pass. This trade-off is relevant to practical deployment claims and should be discussed.

- **UI-TARS-1.5 (Table 3) is listed without model size or training information.** It achieves 61.6% on ScreenSpot-Pro — 8.8 points above GUI-Spotlight — but is placed in the closed-source section with no discussion, making it difficult for the reader to contextualize this comparison.

- **Per-domain breakdowns reveal uneven gains.** On the Scientific domain, GUI-Spotlight (52.4%) trails several 7B models (V2P-7B 56.3%, GTA-1-7B 57.1%, UI-Venus-7B 57.1%). This is not discussed.

### Trivial

None.

## Nice-to-Haves

- An analysis of *find_color* tool usage (how often invoked, whether it helps) would strengthen the claim about multi-tool coordination.
- A dedicated limitations section would improve completeness.
- The Stage 3 bucketed sampling (uniform across tool types) is described mechanically but not analyzed — showing whether this design choice drives the +3.2 point gain would be useful.

## Removed Points

These points from the input review were removed during filtering — treat them with caution:

1. **"Data efficiency claim is misleading because it ignores pre-training data"** — all baselines (V2P-7B, GTA-1-7B, etc.) also start from pre-trained VL backbones; the comparison is about GUI-specific training data, which is standard convention in this literature. The paper explicitly states it initializes from UI-TARS-1.5-7B.

2. **"Data cleaning with Qwen as auditor risks systematic bias (circular dependency)"** — speculative concern, not a verified problem shown in the paper.

3. **"Missing appendix details"** — the paper states hyperparameters and prompts are in Appendix A, which was stripped by the parser.

4. **"Paper does not ablate repeatedly applying tool-based approach without RL training"** — this is addressed by Strategy ① (multi-turn conversational inference with same tool prompts), which achieves only 7.6%, confirming zero-shot tool use fails.

5. **"Stage-1 SFT collapse drops to below-random performance"** — 17.8% is low but not necessarily below random on ScreenSpot-Pro's precise coordinate task; the framing overstates.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Investigate the Stage-1 collapse systematically.** Provide per-token loss breakdowns, analyze whether the SFT model can still answer direct grounding queries without tools, check whether tool-output parsing fails systematically, and evaluate SFT trajectory quality from the teacher model. This is the most important gap to fill.

2. **Clarify the Figure 2 stage naming.** Align the figure's stage numbering and sample counts with the text's three-stage description.

3. **Add variance estimates.** Report standard deviations or confidence intervals across multiple runs, especially for the comparisons where gaps are small (GUI-Spotlight vs. V2P-7B, vs. UI-Venus-7B).

4. **Discuss inference cost.** Report the average number of model calls per query and compare total inference cost against single-step baselines.

5. **Add the missing control ablation.** Evaluate the base model (UI-TARS-1.5-7B) given the same tool set via prompting without any training to directly measure the value of RL-trained tool policy vs. zero-shot tool use.

## Score and Decision

**Round 1 bracket:** After filtering the input review, I estimated a plausible score range of 4.0–7.0 based on topical similarity to anchors: UGround (4.40/7.75), GUI-World (6.25), Grounding MLLM in GUI World (6.00), SpiritSight (5.25), Reinforced UI (5.75), UI-Pro (4.25).

**Round 2 narrowing:** I itemized Grounding MLLM in GUI World (avg 6.00, accepted), UI-Pro (avg 4.25, rejected), Reinforced UI Instruction Grounding (avg 5.75, rejected), and UGround (avg 4.40/7.75, accepted) for close comparison.

**Weighted-item comparison:** GUI-Spotlight's strengths (weights 8.99–11.14) are comparable to Grounding MLLM in GUI World (8.87–10.77) and above UI-Pro (7.19–9.68). However, GUI-Spotlight's weakest-item weight (the iterative ablation gap at 7.63) is more concerning than Grounding MLLM's weakest (error analysis at 5.47) and sits in the same range as Reinforced UI's weakest (8.48). The paper lacks the large-scale dataset contribution that earned UGround its high rating despite similar weaknesses. The Stage-1 SFT collapse is a gap that no accepted anchor had to the same degree.

**Final placement:** GUI-Spotlight sits between Grounding MLLM in GUI World (6.00, accepted) and Reinforced UI/SpiritSight (5.75/5.25, rejected). The method is well-motivated and the ablations are informative, but the unexplained Stage-1 collapse and the uneven cross-benchmark gains are significant concerns that prevent acceptance in the current form.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>