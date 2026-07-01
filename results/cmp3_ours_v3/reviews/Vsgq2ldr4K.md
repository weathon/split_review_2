## Summary

This paper proposes "Power Sampling," a training-free inference-time sampling algorithm that uses MCMC (Metropolis-Hastings) to approximately sample from the power distribution p^α of a base LLM. The key insight is that RL posttraining (GRPO) "sharpens" the base distribution, and the power distribution provides a natural training-free way to achieve a similar effect. Experiments across three model families (Qwen2.5-Math-7B, Qwen2.5-7B, Phi-3.5-mini-instruct) and reasoning benchmarks (MATH500, HumanEval, GPQA, AlpacaEval 2.0) show that power sampling matches or exceeds GRPO's single-shot accuracy while maintaining generation diversity.

## Strengths

1. **Clean conceptual framing (Section 1, 4.1).** The paper builds on the distribution-sharpening hypothesis for RL posttraining and identifies the power distribution p^α as a well-motivated inference-time target for emulating this effect. This gives the method intellectual coherence beyond empirical results alone.

2. **Proposition 1 and the distinction between power sampling and low-temperature sampling (Section 4.1).** The sum-of-exponents vs. exponent-of-sums distinction (Eqs. 7–8) is a genuine technical insight, and the toy example (Example 1) effectively illustrates how these converge to different distributions in a nontrivial case. The connection to "critical windows" / "pivotal tokens" in reasoning is plausible and well-articulated.

3. **Training-free, dataset-free, verifier-free.** This is a genuine practical advantage over RL methods — no reward model, no training data curation, no training stability issues, and no requirement for a verifiable reward signal. The method applies wherever the base model can be run.

4. **Competitive results across multiple model families (Table 1).** Power sampling matches GRPO on MATH500 and outperforms on HumanEval and AlpacaEval 2.0 for two of three base models. The improvements over low-temperature sampling are substantial and consistent across Qwen2.5 models.

5. **Pass@k diversity advantage (Figure 5).** This is the clearest empirical win. GRPO's diversity collapse is well-documented, and the paper convincingly shows that power sampling avoids it while still achieving strong single-shot performance. The pass@k curve for power sampling dominates both the base model and GRPO at all k > 1.

6. **Likelihood and confidence analysis (Figure 4).** Provides direct evidence that power sampling does what it claims — sample from higher-likelihood regions of the base model — connecting the method's mechanism to its empirical results.

## Weaknesses

### Fatal
None.

### Major

1. **N_MCMC — the number of MCMC steps — is never reported (Section 5.1, Algorithm 1).** N_MCMC is listed as a hyperparameter in Algorithm 1 and directly controls the computational cost (Eq. 12: E[tokens] ≈ N_MCMC · T²/(4B)). The paper states "we empirically find a value for B that makes Algorithm 1 performant for relatively small values of N_MCMC" (Section 4.3) but never reports what N_MCMC actually is. With T=3072 and B=192, even moderate N_MCMC values (e.g., 10–50) can lead to 123K–614K tokens generated per output — orders of magnitude more than a single forward pass. The paper frames power sampling as "inference-time scaling" but provides no scaling curve, no compute budget, and no indication of how much compute is actually used. This makes it impossible to assess the efficiency of the approach relative to alternatives.

2. **No comparison against simple inference-time methods that spend comparable compute.** The paper compares against GRPO (training-based) and low-temperature sampling (single-pass). If power sampling spends 10–100× more inference compute per output, the right comparison is against methods that also spend more inference compute: best-of-N sampling, self-consistency / majority voting, or repeated GRPO runs. Best-of-N is the simplest inference-time method that trades compute for quality and directly competes with the claimed contribution. Without these baselines, it is unclear whether the performance gains come from the specific power-distribution+MCMC design or simply from spending more FLOPs at inference time.

3. **Phi-3.5-mini-instruct GRPO baseline appears degraded on HumanEval (Table 1).** On HumanEval, GRPO scores 0.134 — substantially *worse* than the base model's 0.213 (a 37% degradation). The paper states the GRPO hyperparameters "converge to improvement over the base model over a large number of epochs," but the HumanEval results contradict this. While GRPO is trained on MATH (not code), such severe degradation inflates the relative performance of power sampling (which achieves 0.732 on this task). This should be acknowledged and discussed, or the GRPO results re-verified.

### Minor

4. **No ablation studies on key hyperparameters (α, B, N_MCMC).** The paper acknowledges the tradeoff between B and N_MCMC (Section 4.3) but provides no empirical analysis of how performance varies with these choices. α = 4.0 controls the sharpness of the target distribution, yet there is no sensitivity analysis. For a method whose main axis of improvement is "use more inference compute," understanding how performance scales with compute is essential.

5. **Algorithm 1 acceptance ratio uses π_k when the target is π_{k+1} (Section 4.3, Algorithm 1, line 7).** The algorithm states "Given prefix x_{0:kB}, we wish to sample from π_{k+1}" (line 3), but the MH acceptance ratio (line 7) uses π_k in the numerator and denominator. Since π_k is defined only over sequences of length kB and the proposals have length (k+1)B, this is dimensionally inconsistent — the ratio should use π_{k+1}. This appears to be a bug in the pseudocode.

6. **No statistical significance or error bars.** The paper reports no confidence intervals, standard deviations, or variance estimates for any result. Given the stochastic nature of both sampling algorithms and GRPO training, some measure of variance is important, especially for comparisons where margins are small (e.g., MATH500: 74.8 vs 78.5 for Qwen2.5-Math; GPQA: 38.9 vs 39.9).

7. **Different proposal temperature for AlpacaEval without analysis (Section 5.1).** The proposal distribution uses temperature 1/α = 0.25 for reasoning tasks but τ = 0.5 for AlpacaEval, stated to "improve performance" without any supporting analysis. If proposal hyperparameters need domain-specific tuning, this weakens the claim of broad applicability.

### Trivial

8. **"Single-shot" framing could be clarified.** The paper evaluates all methods "single-shot" (one final response string). For GRPO this is one forward pass; for power sampling it involves many internal passes. The framing is technically consistent (one final output per problem) but could be misleading without the compute discussion in (1).

## Nice-to-Haves

- A convergence diagnostic for the MCMC chain (e.g., how acceptance rates or task performance vary with N_MCMC) would substantiate the claim that samples approximately follow p^α.
- An analysis directly examining whether power-sampled responses avoid "critical window" failure modes (linking Section 4.1's theoretical motivation to empirical observation) would ground the motivation.
- Performance vs. inference compute curves (with α and B as parameters) compared against best-of-N and self-consistency would clarify whether power sampling is Pareto-efficient relative to simpler compute-scaling strategies.

## Removed Points

- "The proposal distribution terms in the MH ratio need to account for the uniform selection of the resampling index m" — REMOVED as factually incorrect. The uniform selection factor (1/((k+1)B)) appears in both q(x|x') and q(x'|x) and cancels in the ratio, so the pseudocode is correct on this point.
- Generic/superficial strengths (e.g., "the paper addressed an important problem") — REMOVED as they lack specificity to the paper's content.
- The characterization of Issue 1 as "fatal" — DEMOTED from fatal to Major. The paper's core claim is about accuracy matching GRPO (a training-based method), not about computational efficiency. The missing N_MCMC makes the compute cost opaque but does not invalidate the accuracy comparison.

## Novel Insights

The harsh critic insight that the paper's results could largely be a consequence of spending more compute at inference time is a useful framing. Even if that were the case, the paper's conceptual contributions remain valuable: the power-distribution vs. low-temperature distinction (Proposition 1), the distribution-sharpening analysis connecting to RL posttraining, and the demonstration that diversity collapse is avoidable without sacrificing single-shot performance. These contributions are separable from the question of whether the specific MCMC implementation is Pareto-optimal relative to simpler compute-scaling strategies.

## Suggestions

1. Report N_MCMC explicitly in Section 5.1, and include a plot of accuracy vs. total inference FLOPs (or wall-clock time) across different settings of N_MCMC and α, compared against best-of-N and self-consistency baselines.
2. Re-verify or discuss the Phi-3.5 GRPO results on HumanEval — either provide evidence that 0.134 is the correct result after proper tuning, or acknowledge the degradation and discuss its implications.
3. Fix the Algorithm 1 pseudocode to use π_{k+1} in the acceptance ratio.
4. Add error bars or confidence intervals for at least the main results.
5. Add ablation studies for α and B (and N_MCMC, once reported) to show how performance varies with these parameters.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Comparison to this paper |
|------|-----------|-------|------------------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/0xUEBQV54B.md (Large Language Monkeys) | 5.00 | R2 | Similar topic (inference-time compute scaling). LLM paper has cleaner experiments but less theoretical contribution. Roughly comparable. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/DQfHkEcUqV.md (Learning Extrapolative Sequence Transformations from Markov Chains) | 4.75 | R1 | Similar methodology (MCMC+LLM). Current paper has stronger presentation and results. Score above this. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/VNckp7JEHn.md (Inference Scaling Laws) | 5.75 | R1 | More rigorous empirical methodology (error bars, multiple baselines). Current paper has weaker empirical controls but stronger theory. Score below this. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/77gQUdQhE7.md (Inference-Aware Fine-Tuning for BoN) | 5.67 | R2 | Cleaner evaluation methodology. Accepted. Current paper has more gaps. Score below this. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/xoXn62FzD0.md (Syntactic Control via SMC) | 8.00 | R1 | Much stronger paper across all dimensions. Current paper not in this range. |

**Round 1 bracket:** 4.5 – 5.5. **Narrowing:** The closest comparable paper is Large Language Monkeys (5.00, Reject), which also studies inference-time scaling and was rejected due to limited novelty / missing elements. The current paper has a stronger theoretical contribution but weaker empirical reporting. The Inference Scaling Laws paper (5.75, Accept) sets a higher bar for empirical rigor that the current paper does not meet.

**Final score:** 5.0 — The paper has a genuinely interesting idea and clean theoretical motivation, but the empirical presentation has significant gaps (N_MCMC unreported, no compute-equivalent baselines, no error bars, no ablation studies) that prevent acceptance in the current form. The major weaknesses are addressable.

**Decision:** Reject

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>