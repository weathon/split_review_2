## Summary

This paper identifies a practical failure mode in GRPO-based RLVR training: when all G sampled responses to a problem are wrong, the group-relative advantage becomes identically zero, producing no learning signal. The authors propose GHPO, which detects such "difficult" queries on-the-fly (all G responses incorrect → difficult) and augments the prompt with a portion of the ground-truth solution trace (controlled by a hint ratio ω), converting a zero-gradient example into one where the model can learn. A multi-stage schedule adapts ω across training. Experiments on Qwen2.5-Base-7B and Qwen2.5-Math-7B across six math benchmarks show consistent improvements over vanilla GRPO and a curriculum-learning baseline.

## Strengths

- **Concrete problem diagnosis with empirical grounding (Section 2.3).** The paper precisely identifies the zero-advantage failure mode of GRPO when all G responses are wrong, and backs it with a statistic: Qwen2.5-7B-Instruct fails on 52% of NuminaMath-1.5 problems, illustrating that reward sparsity is severe in practice, not just a theoretical concern.

- **Low-overhead difficulty detection that reuses existing signals (Section 3.3).** The "all G responses wrong → difficult" rule requires no auxiliary model, no external difficulty scorer, and no manual labeling. It uses the reward signal already computed by GRPO, which is the right engineering direction for a practical RLVR system.

- **Consistent and non-trivial accuracy gains across two model families and multiple benchmarks (Tables 1–2).** GHPO outperforms GRPO on 12 out of 12 model-dataset-benchmark comparisons for Base-7B, and on all 6 benchmarks for Math-7B. Several gains are substantial (e.g., +10% on GPQA-Diamond with the Math dataset, +8% on AIME24 with the Mixed dataset). The improvement holds when moving from a general base model to a math-specialized one, indicating robustness.

## Weaknesses

### Fatal

None.

### Major

- **The core mechanistic claim—that hint-conditioned generations produce usable gradients—is unverified.** When a query is detected as difficult, the prompt is augmented with a portion of the ground-truth solution (Eq. 2). The policy gradient is then applied to these hint-conditioned generations. For the method to work as described, the hint must place the model in a *mixed* regime where some responses succeed and some fail, producing non-uniform group rewards and non-zero advantages. However, if the hint is too informative (all responses correct, all rewards = 1) or too weak (all responses wrong, all rewards = 0), the advantage is again zero and no learning occurs. **The paper provides no analysis of whether, or how often, hint-conditioned generations actually yield non-uniform group rewards.** The entire claim that GHPO "converts sparse rewards into valid learning signals" depends on this dynamic, but it is treated as an assumption rather than verified empirically. The downstream accuracy improvements are suggestive but do not substitute for direct evidence that the hint mechanism itself produces usable gradients (as opposed to the model learning primarily from the non-sparse branch or from the imitation-learning effect of the hints themselves). This is an evidential gap that undermines confidence in how the method works.

- **No experimental comparison against the most directly related RLVR methods.** The paper cites DAPO (dynamic prompt filtering to address too-easy/too-hard problems), Dr. GRPO (unbiased optimization), LUFFY (off-policy rollouts), and VAPO (value-model-based training) in the related work (Section 5) and positions against them in the introduction (Section 1), but evaluates only against vanilla GRPO and a GRPO+curriculum-learning baseline. Without comparisons to DAPO in particular—which directly tackles the same "too easy / too hard" filtering problem using a pure-RL approach—it is impossible to assess whether GHPO's use of solution traces provides meaningful advantage over alternative strategies for the same problem, or whether the reported gains could be matched or exceeded by existing methods. The paper's claim of "consistently outperforming strong on-policy reinforcement learning and curriculum learning baselines" (abstract) cannot be substantiated without these comparisons.

### Minor

- **No variance or statistical significance reporting.** All results in Tables 1 and 2 are single point estimates with no error bars, no standard deviations, and no mention of the number of independent runs. RL training is known to be high-variance. Several reported margins are very small (e.g., Math-500: 0.774 → 0.776 in Table 2), and one benchmark (OlympiadBench on the Mixed dataset) shows a *decrease* (0.396 → 0.389) that goes unremarked. Without multiple seeds or variance estimates, the reliability of these point improvements is unclear.

- **Assumption 1 formalizes out-of-distribution generalization, but the experiments do not test it.** Assumption 1 (Section 3.1) explicitly involves OOD problem distributions $\mathcal{D}_{OOD}$ and claims that training with hints on failing problems improves OOD generalization. However, all six evaluation benchmarks are mathematical reasoning datasets drawn from a similar distribution as the training data (MATH + NuminaMath). There is no evaluation on qualitatively different tasks (e.g., coding, scientific reasoning, symbolic manipulation). The claim that "we demonstrate the effectiveness of this Assumption 1 through comprehensive experiment" is therefore overstated; the experiments demonstrate improved in-distribution or near-distribution accuracy, not OOD generalization as formalized.

- **The persistent ~60% hint rate throughout training (Figure 3) raises questions about the RL-vs-imitation balance.** Figure 3 shows that approximately 60% of problems are classified as "difficult" and receive hints even after 160 training steps. This means the majority of training data is processed in hint-conditioned mode rather than free-exploration mode. The paper frames GHPO as a hybrid of RL and imitation learning, but does not quantify what fraction of parameter updates receive a non-zero gradient from the RL objective versus behaving as behavioral cloning on hint-conditioned prompts. This analysis would clarify whether the method's effectiveness stems from the RL objective or primarily from the supervised signal in the hints.

### Trivial

- The abstract's "approximately 5% average performance gain" appears to round up from the actual averages (~4.4% for Base-7B on Math, ~3.3% on Mixed), and it is ambiguous whether this is absolute or relative improvement.

## Nice-to-Haves

- **Ablation: systematically sweep ω** (hint ratio) from 0 (pure RL) to 1 (full solution trace) to characterize the method's sensitivity to this key parameter and validate the multi-stage schedule.
- **Cold-start N=20:** The paper sets N=20 without evidence or sensitivity analysis. An ablation varying this value would clarify whether the cold-start phase is important and how robust the method is to this choice.
- Clarify whether the improvement in gradient smoothness (Section 4.4, smaller gradient norms) reflects genuine optimization stability or simply the fact that hints make the task easier (reducing gradient magnitudes for that reason).
- Report the group size G used in experiments; it is not stated in the main text.

## Removed Points

These points were raised in the input review but are removed per the filtering rules. Treat them with caution:

- **ω schedule deferred to Appendix B.3** — removed per hard rule: the appendix exists in the original submission; the parser strips it.
- **Baseline naming confusion (GRPO-CL-H(0.5))** — removed as a presentation nitpick; the naming is sufficiently clear for an expert reader.
- **"52% failure rate measured on Instruct model, not base model"** — removed because the paper explicitly uses the Instruct model's failure rate as an *underestimate* of the base model's rate ("even the Qwen2.5-7B-Instruct model... failed to solve 52%... let alone..."). The argument is correctly framed, not a flaw.
- **"Eq. 1 is identical to GRPO's objective"** — the reviewer acknowledges this is not a flaw; removed as non-critical.
- **"5% figure rounding"** — trivial presentation point, kept above only as a Trivial note.
- **General "related work missing" concerns** — removed per hard rule: the reviewer is not asked to identify missing citations.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface an overlooked obstacle, a hidden assumption the paper fails to examine, or a reinterpretation of the results that changes their meaning. The identified gaps (mechanistic verification of the hint-conditioned gradient, missing SOTA baselines, OOD overclaim) are standard evidential weaknesses that the authors can address; they do not constitute novel insights into the problem itself.

## Suggestions

1. **Directly measure whether hint-conditioned generations produce non-uniform group rewards.** For a sample of training steps, report the fraction of difficult problems where the hint leads to a mixed group reward (some correct, some wrong) versus uniform (all correct or all wrong). This would validate or refute the core mechanism.

2. **Add DAPO as a baseline** (and Dr. GRPO or LUFFY if feasible). DAPO addresses the same problem (too-easy/too-hard filtering) with a pure-RL approach and would let readers evaluate whether GHPO's use of solution traces provides a meaningful advantage over RL-only alternatives.

3. **Report means and standard deviations over at least 3 random seeds** for all main results. Given the small margins on some benchmarks, variance reporting is essential to establish that the improvements are reliable.

4. **Move a brief description of the multi-stage ω schedule into the main text** (at minimum: number of stages, how ω initializes and changes, whether it is per-problem or global). The current full deferral to the appendix obscures the method's only introduced parameter.

5. **Either remove or re-scope Assumption 1.** If the experiments only evaluate on math benchmarks (near-distribution to the training data), the assumption should be restated in terms of generalization to held-out math problems, not OOD generalization to unrelated task types. Alternatively, add one OOD evaluation (e.g., coding or scientific reasoning) to substantiate the current claim.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>