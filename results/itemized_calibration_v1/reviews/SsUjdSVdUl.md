## Summary

The paper proposes Critique-RL, a two-stage reinforcement learning approach for training critiquing language models without requiring a stronger supervisor or human annotations. It first identifies a key failure mode of prior RL-based methods: indirect reward signals (based on actor refinement correctness) optimize helpfulness but neglect discriminability (the ability to judge whether a response is correct), leading to overly conservative or aggressive critics. Based on this diagnosis, Stage I optimizes discriminability via a direct correctness-matching reward, and Stage II optimizes helpfulness via actor refinement rewards while regularizing toward the Stage I policy to preserve discriminability. Experiments on math reasoning tasks (MATH, GSM8K, AQuA) with Qwen2.5-3B and 7B show consistent improvements over SFT, STaR, Retroformer, and CTRL baselines, with additional OOD generalization evidence on SVAMP and TheoremQA.

## Strengths

1. **Empirically grounded problem diagnosis (Section 4.1, Figure 3).** The paper concretely demonstrates that three natural indirect reward functions (r_refine, r_Δ, r_correction) each fail in distinct ways—producing overly conservative or overly aggressive critics—and traces this to poor discriminability. The decomposition into Acc@Dis for originally correct vs. incorrect responses (bottom row of Figure 3) is particularly informative, showing that all three baselines degrade one side of discrimination as training progresses. This diagnosis is the paper's most important contribution and is well-supported by training dynamics plots.

2. **Clean two-stage design directly motivated by the diagnosis.** Stage I directly addresses the identified discriminability bottleneck via a correctness-matching reward. Stage II then builds on this foundation by optimizing helpfulness while regularizing toward the Stage I policy. The design choices are traceable to the empirical findings in Section 4.1, and Algorithm 1 provides a precise specification.

3. **Substantial and consistent empirical gains.** Improvements hold across multiple datasets, model scales (3B, 7B), and metrics. Representative: Qwen2.5-7B on MATH achieves Acc@Refine 58.40% vs. 53.86% for CTRL (+4.54 pts) and Acc@Dis 85.20% vs. 71.42% (+13.78 pts). The discrimination metric improvements are particularly striking and directly validate that Stage I accomplishes its goal.

4. **Informative ablation study (Table 3).** The ablation cleanly separates the contribution of each stage. Removing Stage I drops Acc@Dis by 3.1 points on MATH; removing Stage II discrimination regularization drops it by 5.1 points. The paper also compares alternative reward functions (r_Δ, r_correction) in Stage II, showing r_refine works best.

5. **Generalization evidence across tasks and models.** The method works on OOD tasks (SVAMP, TheoremQA), across model architectures (Llama3.2, in appendix), and includes a non-math task (summarization in appendix). The OOD results in Table 4 show consistent if smaller improvements.

## Weaknesses

### Fatal
None.

### Major

1. **β₂ value is not reported and hyperparameter sensitivity is unexplored.** β₂ is the scaling factor for the KL divergence with the Stage I model in Equation (9) and Algorithm 1—a core component of Stage II's discriminability-maintenance mechanism. The paper reports β₁ = 0.2 (line 274) but never specifies β₂. Additionally, the Stage I KL coefficient β (Equation 8) is not explicitly connected to the "KL coefficient to 0.01" mentioned for RL baselines (line 252). This leaves the method under-specified for reproduction. While this does not invalidate the core claims, it is a genuine reproducibility gap.

2. **The "Stage II w/o discrimination" ablation conflates two separate mechanisms.** As stated in the Table 3 caption, this ablation removes *both* r_dis and KL(π_Stage-I || π_Stage-II) simultaneously. This makes it impossible to tell which mechanism is responsible for maintaining discriminability. Does r_dis alone suffice? Does the KL regularization alone suffice? Or are both necessary? This is a missed analytical opportunity, though it does not undermine the conclusion that maintaining discriminability matters.

3. **No variance or statistical significance reporting.** Main results (Table 1) are point estimates with no confidence intervals or standard deviations. The paper reports "best results" from 500 training steps (line 274), which raises the question of whether reported numbers reflect the peak of a noisy training curve. While most improvements are large enough to be credible (e.g., +13.78 points on Acc@Dis for 7B MATH), some margins are small enough that variance information would help (e.g., Qwen2.5-7B on AQuA: 65.75 vs. CTRL 64.96; TheoremQA Acc: 21.4 vs. CTRL 21.1).

### Minor

1. **The extraction of the critic's correctness judgment f(x,y,c) is underspecified.** The paper defines f as "the critique model's judgment of the correctness of the original response" (line 232) but does not specify how this judgment is extracted from the critique text—whether via parsing the structured output (as in Figure 2's "Correctness of the final answer" field), regex, or logit-based extraction. This affects reproducibility.

2. **The "best results" reporting convention could overstate performance.** Selecting the best checkpoint from 500 training steps post-hoc rather than reporting mean performance over a window or over multiple seeds may inflate reported numbers. For the main claims with large margins this is a minor concern, but it adds uncertainty to smaller-margin comparisons.

3. **The method requires a rule-based correctness verifier for the direct reward.** This limits the method's primary applicability to tasks with automatic answer verification (e.g., math reasoning). The paper acknowledges this and provides a summarization experiment (Appendix G) using a learned reward model as a substitute, which partially addresses the concern. The abstract's phrasing "without stronger labeling" is technically correct—a rule-based answer verifier is not a "stronger model"—but underspecifies that a correctness signal is still required.

### Trivial
None.

## Nice-to-Haves
- A component-level ablation in Stage II that separates r_dis from KL regularization to isolate each mechanism's contribution.
- Sensitivity analysis for β₂ (and ideally β₁ and the Stage I β) across a range of values.
- Multi-seed reporting with confidence intervals for the main results, especially for smaller-margin comparisons.
- Clarification of how the critic's correctness judgment f(x,y,c) is extracted from text.

## Removed Points
These points were raised in the input review but removed or downgraded after verification against the paper:
- **"Reliance on rule-based verifier is a critical issue"** → Downgraded to Minor. The paper acknowledges this limitation and includes a summarization experiment with a learned reward model (Appendix G). The abstract's claim of "without stronger labeling" is technically correct since a rule-based verifier is not a stronger model.
- **"Actor model trained on refinement dataset limits generality"** → Removed. The reviewer acknowledges the actor is fixed across all comparisons, so this does not affect relative rankings.
- **"Missing related works"** → Removed by instruction (cannot verify external knowledge without external sources).
- **"Missing appendix content"** → Removed by instruction (parser strips appendices; they exist in the original submission).
- **Formatting/style nitpicks** → Removed by instruction (parser artifacts, not author errors).

## Novel Insights
The most valuable observation emerging from the review is the conflation of two mechanisms in the Stage II discrimination ablation—this reveals that while the paper convincingly shows that "maintaining discriminability matters," it does not disentangle whether the reward signal (r_dis), the KL regularization, or both are responsible. This is a genuinely insightful analytical gap that the authors could productively address. Beyond this, the review largely confirms the paper's own framing: the core contribution (diagnosing the discriminability bottleneck and proposing a targeted two-stage fix) is valid, well-supported, and represents a meaningful step forward for the critique model literature.

## Suggestions
- Report β₂ explicitly and include a sensitivity analysis across a range of values (e.g., {0.01, 0.05, 0.1, 0.2, 0.5}).
- Add separate ablation rows: "Stage II w/o r_dis (only KL)" and "Stage II w/o KL (only r_dis)" to complement the current combined ablation.
- Clarify how the critic's correctness judgment f(x,y,c) is extracted from the critique output (parsing, regex, or logit-based).
- Report the mean and standard deviation over multiple training seeds, or clarify that temperature-0 evaluation makes the evaluation deterministic and only training is stochastic.

## Calibration and Score

**Round 1 — Bracketing.** I searched the calibration corpus for papers on training critique/critic models with RL. The following anchors were retrieved:

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| `JEehcb48Vp.md` (Critic-CoT) | 5.75 | 1 | Yes | Similar topic (training critiquing for reasoning). Critic-CoT's main weakness was reliance on GPT4-Turbo annotations (weight -4) and unclear source of improvements. Critique-RL does not have these problems, making it stronger. |
| `38E4yUbrgr.md` (LM Self-improvement by RL Contemplation) | 6.00 | 1 | Yes | Similar spirit (RL without stronger supervisor). That paper's weaknesses included limited novelty and small-scale models (780M Flan-T5). Critique-RL has stronger novelty (discriminability diagnosis), larger models (3B/7B), and more thorough ablations. |
| `Sx038qxjek.md` (CRITIC) | 6.50 | 1 | Yes | Tool-interactive self-correction. Strong results but novelty concerns. Roughly comparable quality to Critique-RL. |
| `50P9TDPEsh.md` (Critique Ability of LLMs) | 4.67 | 1 | Yes | Benchmark/evaluation paper, not a method paper. Less directly comparable. |
| `e3odKmatZr.md` (Critique-out-Loud Reward Models) | 5.25 | 1 | Yes | Different framing (reward models). Had distillation concerns and no RLHF verification. Critique-RL is stronger. |
| `vf8iou7FNF.md` (RLSF) | 5.75 | 1 | Yes | Symbolic feedback in RL. Had incremental novelty concerns and unfair experimental comparisons. Critique-RL is stronger. |

**Round 1 bracket:** 6.0 – 7.0.

**Final score calibration.** Compared to Critic-CoT (5.75): Critique-RL shares stronger problem diagnosis but Critic-CoT had a fatal dependency on GPT4 annotations that Critique-RL avoids. Compared to LM Self-improvement (6.00): Critique-RL has a more novel core finding (discriminability bottleneck vs. "evaluation is easier than generation") and operates at larger model scales. Compared to CRITIC (6.50): both have strong empirical results but different scopes; CRITIC's weakness was novelty concerns, while Critique-RL's weaknesses (β₂ unreported, combined ablation) are addressable in revision.

The β₂ gap and combined ablation are the primary factors preventing a higher score (7+). These are real but bounded issues that do not threaten the paper's core claims. With the empirical diagnosis of discriminability as a strong novel finding, clean two-stage design, and large consistent gains, the paper sits comfortably in the accept range.

**Final score: 6.5. Decision: Accept.**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>