Here is my final consolidated review.

---

## Summary

Critique-RL proposes a two-stage online RL method for training LLMs to critique other models' outputs without stronger supervision. Through careful empirical analysis, the paper first identifies that existing RL approaches using only indirect reward signals from actor refinement (e.g., correctness of the refined answer) fail to optimize the critic's *discriminability* — its ability to judge whether a response is correct. The paper then introduces a two-stage remedy: Stage I optimizes discriminability using a direct binary correctness-judgment reward; Stage II optimizes helpfulness (refinement quality) while preserving discriminability via a continuing discrimination reward and KL regularization toward the Stage-I policy. Experiments on Qwen2.5-3B/7B across MATH, GSM8K, AQuA (in-domain) and SVAMP, TheoremQA (OOD) show consistent and often large improvements over SFT, STaR, Retroformer (PPO), and CTRL (GRPO) baselines.

## Strengths

1. **Empirical diagnosis of why indirect RL rewards produce bad critics (Section 4.1, Figure 3).** The paper demonstrates concretely that when the critic is trained only on rewards derived from the actor's refinement correctness (r_refine, r_correction, r_Δ), discriminability degrades asymmetrically: critics optimize judgment for either originally-correct or originally-incorrect responses at the expense of the other, leading to "overly conservative" or "overly aggressive" behavior. This analysis goes significantly beyond prior work (Retroformer, CTRL) and convincingly motivates the method.

2. **Clean, well-motivated two-stage design (Section 4.2, Algorithm 1, Equations 7–9).** Stage I directly optimizes a binary discrimination reward. Stage II jointly optimizes refinement accuracy and discrimination, anchored to the Stage-I policy via KL regularization. The ablations (Table 3) isolate each component: removing Stage I drops Acc@Refine from 48.6→47.6 on MATH; removing discrimination components from Stage II drops Acc@Dis from 82.8→77.7.

3. **Consistent and substantial empirical gains across models and datasets (Table 1).** On Qwen2.5-7B MATH, Critique-RL achieves 58.40% Acc vs. CTRL's 53.86% and 85.20% Acc@Dis vs. CTRL's 71.42% — a 13.78-point discriminability gap. These patterns replicate across both model sizes and all three in-domain tasks.

4. **Out-of-domain generalization (Table 4).** Critics trained on three math tasks transfer to SVAMP and TheoremQA without retraining (e.g., SVAMP Acc 89.7% vs. CTRL's 85.1% on Qwen2.5-7B), demonstrating the learned critiquing ability is not dataset-specific.

5. **Iterative training continues to improve (Table 2).** A second iteration of the two-stage procedure on MATH 3B further raises Acc from 48.6→51.0 and Acc@Dis from 82.8→86.5, showing the method does not quickly saturate.

6. **Inference-compute scaling analysis (Figure 1).** Critique-RL's accuracy continues to improve with more samples and at each compute budget outperforms baselines, with K× response-critique-refinement sampling being more compute-efficient than 3K× parallel sampling.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **RL algorithm confound in baseline comparisons (Table 1).** Critique-RL uses RLOO, while Retroformer uses PPO and CTRL uses GRPO. The main results therefore compare *both* a different RL algorithm *and* the two-stage design simultaneously. The ablations in Table 3 partially address this — they use RLOO throughout and show that single-stage RLOO variants underperform the two-stage method. This confirms the two-stage design adds value *given RLOO*. However, a direct control re-implementing Retroformer or CTRL with RLOO would fully eliminate the confound. As it stands, a small portion of the reported gains could reflect the RL algorithm choice rather than the two-stage design.

2. **No variance or multiple-seed reporting.** All results in Tables 1–4 are point estimates without variance, confidence intervals, or multiple runs. RL training is sensitive to random seeds and hyperparameter choices. While the largest gaps (e.g., 13.78-point Acc@Dis on MATH 7B) are clearly meaningful, smaller gaps (e.g., 65.75 vs. 64.96 on AQuA 7B) would benefit from some measure of variability to assess robustness.

3. **"Best results" selection (line 274).** The paper reports "best results" across 500 training steps. Without also reporting final-step values or the checkpoint selection criterion, there is a risk of optimistic selection bias. Combined with the absence of variance reporting, this modestly weakens confidence in the exact magnitudes reported.

### Trivial

1. **SFT data filtering.** Line 148 states critique SFT data was "filtered based on the correctness of refinement" without specifying the exact criterion or dataset size after filtering.

2. **Hyperparameter β documentation.** The paper sets β=0.01 (Stage I KL), β_1=0.2 (Stage II r_dis coefficient), but β_2 (Stage II KL coefficient) is not explicitly specified (it appears to share the same β as Stage I). No sensitivity analysis is provided for any β coefficient.

## Nice-to-Haves

- The Stage I reward r_dis is binary (0/1), which is sparse. Discussing whether any continuous or smoothed proxy was considered would be informative for practitioners.
- A direct comparison of "RLOO + single-stage indirect reward" vs. "RLOO + two-stage" (beyond the ablations already in Table 3) would cleanly isolate the two-stage contribution from the RL algorithm choice.
- Clarifying whether the "best results" selection uses a held-out validation set or the test set would address the optimism bias concern.

## Removed Points

The following points from the Harsh Critic are removed as invalid, already addressed, or not verifiable from the paper:

1. **"9.02% and 5.70% gains ambiguous (percentage vs. percentage points)"** — Removed as a misunderstanding. Reporting relative percentage gains on top of a baseline accuracy is standard practice; the figure is unambiguous when read in context.

2. **"Oracle verifier framing should be sharpened"** — Removed as already addressed. The paper explicitly states (line 96) "without relying on stronger labeling or an oracle reward function *during testing*," which clearly acknowledges that oracle rewards are used during training. This is standard for RL methods trained on tasks with verifiable answers.

3. **"Evaluation temperature of 0 should be clarified more explicitly"** — Removed as already stated at line 274: "During evaluation, the temperature is set to 0." This is explicit.

4. **Generic "Strengthening the Paper on Its Own Terms" items** — The three items listed by the Harsh Critic (add multiple seeds, control for RL algorithm, clarify best results) are already captured in the weaknesses above. Redundant framing removed.

5. **"The harsh critic's point about Stage I reward sparsity"** — This is a valid observation but too minor even for the minor tier; moved to Nice-to-Haves.

## Novel Insights

The key insight that emerges beyond the paper's own framing is that indirect reward signals for critique optimization have an inherent "zero-sum" property: they improve discriminability for one response class (correct or incorrect) at the expense of the other. This finding, shown clearly in Figure 3's bottom-row plots, suggests a fundamental limitation of single-objective RL for tasks that require two distinct capabilities (discrimination + helpfulness). It implies a broader design principle: when an agent's task decomposes into separable sub-capabilities, explicit staged optimization may be necessary even if a monolithic reward function could in principle capture both aspects. This principle likely extends beyond critiquing to other multi-aspect LLM training problems (e.g., factuality + style, safety + helpfulness).

## Suggestions

1. Add variance estimates (at least 3 seeds with standard deviation) for the main results in Table 1 and key ablations in Table 3 to address the largest evidential gap.
2. Include a control condition that re-implements a single-stage indirect-reward baseline using RLOO to fully control for the RL algorithm confound.
3. Report both the best and final-step values (or clarify the checkpoint selection procedure) to address the optimism bias concern.
4. Provide a brief sensitivity analysis for the β coefficients (β_1, β_2) in Stage II, as these control the critical discriminability-helpfulness trade-off.

## Score and Decision

**Score:** 7.5

**Decision:** Accept

This paper makes a clear, well-supported contribution. The empirical diagnosis of why indirect RL rewards produce poor critique models (Section 4.1) is a genuine finding that goes beyond prior work. The two-stage method is clean, intuitive, and convincingly validated by ablations. The experimental scope is thorough: multiple model sizes, three in-domain datasets, two OOD datasets, iterative training, inference-compute scaling, and oracle-verifier analysis. The main weaknesses — absence of variance reporting and the RL algorithm confound in baseline comparisons — are genuine but do not threaten the core claims; the gaps are large enough to be meaningful even accounting for these concerns, and the ablations partially address the confound. These are fixable gaps in an otherwise solid paper.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>