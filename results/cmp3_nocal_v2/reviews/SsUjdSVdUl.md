## Summary

This paper proposes Critique-RL, a two-stage reinforcement learning approach for training critiquing language models without stronger supervision. The key insight is that using only indirect rewards (based on whether the actor refines correctly) optimizes the critic's helpfulness but fails to improve its discriminability — the ability to judge whether a response is correct. The authors first demonstrate this failure mode empirically, then propose Stage I (optimizing discriminability via a direct correctness-matching reward) followed by Stage II (optimizing helpfulness via refinement reward while regularizing to preserve discriminability). Experiments on math reasoning tasks show consistent improvements over SFT, STaR, Retroformer (PPO), and CTRL (GRPO) baselines.

## Strengths

1. **Clear diagnosis of a real failure mode (§4.1, Figure 3).** The paper identifies and empirically demonstrates that indirect reward signals (r_refine, r_Δ, r_correction) optimize helpfulness at the expense of discriminability, producing critics that are either "conservative" (resisting changes) or "aggressive" (flipping correct answers to incorrect). The training dynamics visualization in Figure 3 convincingly shows that all three indirect-reward baselines stagnate on Acc@Dis while the two-stage approach improves it substantially.

2. **Well-motivated, clean two-stage design that follows from the diagnosis (§4.2).** The decoupling of discriminability (Stage I, using direct r_dis reward) and helpfulness (Stage II, using refinement reward + KL regularization to preserve discriminability) is a natural and principled solution. The method is not over-engineered — it directly addresses the identified optimization bottleneck.

3. **Consistent and substantial empirical gains on in-domain math tasks (Table 1).** Critique-RL outperforms all baselines across MATH, GSM8K, and AQuA for both Qwen2.5-3B and Qwen2.5-7B. The gains on discriminability are particularly large (e.g., Acc@Dis for Qwen2.5-3B on MATH: 69.29 → 82.80), and the accuracy improvements are consistent (e.g., MATH 3B: 46.14 → 48.60; MATH 7B: 53.86 → 58.40).

4. **Ablation study confirms the contribution of both stages (Table 3).** Removing either Stage I or the discrimination regularization in Stage II causes a measurable performance drop, providing strong internal validity for the two-stage design.

## Weaknesses

### Fatal
None.

### Major

1. **RL algorithm confound between method and baselines.** Critique-RL uses RLOO as its base RL algorithm, while Retroformer uses PPO and CTRL uses GRPO (lines 250–274). Because the RL algorithm and the reward design change simultaneously, the contribution of the two-stage reward design itself is not fully isolated from the choice of optimizer. It is possible that simply switching the baselines to RLOO (while keeping their reward functions) would close some of the reported gap. An ablation holding the RL algorithm fixed and varying only the reward scheme is needed to cleanly attribute the gains to the two-stage design. This is an evidential gap rather than a structural flaw, but it weakens the precision of the central claim.

2. **No statistical significance or variance reporting.** All tables report only point estimates — no confidence intervals, standard deviations, or significance tests are provided. This is consequential because several comparisons rest on narrow margins. On TheoremQA for Qwen2.5-7B (Table 4), Critique-RL (21.4) vs. CTRL (21.1) is a 0.3-point gap; on AQuA for 7B (Table 1), the gap is 0.79 points (65.75 vs. 64.96). Without any measure of uncertainty, the reader cannot assess whether these narrow-margin differences are reliable or within the range of random seed variation.

### Minor

1. **"Scalable oversight" framing is only partially supported by the evidence.** All main-text experiments are on math reasoning tasks where correctness is automatically verifiable by an oracle reward function during training. While the paper is careful to state that it does not require an oracle *during testing*, the scalable oversight problem is motivated by settings where reliable reward signals are unavailable. The summarization experiments in Appendix G are a step toward addressing this, but their absence from the main text limits the strength of the generalization claim. The paper would benefit from an explicit discussion of this limitation.

2. **Failure-mode diagnosis (Figure 3) is limited to one model and one dataset.** The preliminary analysis showing the "conservative vs. aggressive" pattern is conducted only on Qwen2.5-3B on GSM8K. Replicating this finding on a larger model (e.g., 7B) or an additional dataset would strengthen the generality of the motivating observations.

3. **No analysis of whether Stage I discriminability reflects genuine quality assessment.** The discrimination reward r_dis (Eq. 7) is a binary indicator of whether the critic's judgment matches the oracle. This is straightforward but sparse, and the paper does not analyze whether the critic learns genuine quality assessment or exploits superficial heuristics (e.g., predicting "correct" for long responses). An analysis of false-positive vs. false-negative rates across difficulty levels would be informative.

4. **Iterative training results (Table 2) are reported only for one model/dataset.** The iterative improvement experiment is conducted only for Qwen2.5-3B on MATH. While the gains from iteration are encouraging (48.6 → 51.0 Acc), showing this pattern on at least one additional configuration would strengthen the claim.

5. **No discussion of failure cases or systematic biases.** The paper does not analyze where Critique-RL's critics still get things wrong — e.g., whether there are systematic biases toward certain reasoning patterns or difficulty levels. A qualitative analysis of disagreement cases between the critic and the oracle would strengthen the claims about discriminability quality.

### Trivial

- The compute cost of the two-stage RL procedure (training steps, wall-clock time, comparison to baselines) is not reported, which would help practitioners assess practical trade-offs.

## Nice-to-Haves

- A controlled ablation where Retroformer/CTRL are reimplemented with RLOO (keeping their reward functions) would cleanly isolate the two-stage design's contribution.
- Error bars from 3+ seeds on the main results (Table 1) would substantially raise confidence, especially for narrow-margin comparisons.
- Replicating the Figure 3 analysis on Qwen2.5-7B would confirm that the failure pattern generalizes beyond one model size.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **SFT initialization from same model family (§5.1):** The reviewer notes that using Qwen2.5-3B-Instruct (same family) to generate SFT data produces a "weak" baseline and suggests comparing against GPT-4o-generated critiques. This is removed because the paper's stated goal is to develop critique models "without relying on stronger labeling" — asking for a comparison using stronger supervision contradicts the paper's own framing. The self-consistency of the approach is a feature, not a weakness.

- **Stage II ablation robustness observation (§6):** The reviewer notes that replacing r_refine with r_Δ or r_correction in Stage II causes only a "slight performance drop" and says "this is actually informative" — the paper "could lean into this finding more explicitly." This is a positive observation and a presentation suggestion, not a weakness.

## Novel Insights

None beyond the paper's own contributions. The review does not surface a novel perspective that the paper itself does not articulate.

## Suggestions

1. Add error bars (standard deviation or confidence intervals from multiple random seeds) to all main result tables, especially for comparisons with narrow margins.
2. Add an ablation that controls for the RL algorithm (e.g., re-implement Retroformer and CTRL using RLOO) to isolate the contribution of the two-stage reward design.
3. Include an explicit limitations paragraph discussing the reliance on an oracle reward function during training, and how the method could be extended to settings without verifiable rewards.
4. Add a qualitative analysis of disagreement cases between the critic and the oracle to show whether discriminability reflects genuine quality assessment.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>