## Summary

This paper proposes a training-free inference-time sampling algorithm that uses Metropolis-Hastings MCMC to approximately sample from the "power distribution" p^α of a base LLM, where α > 1 sharpens the distribution toward higher-likelihood sequences. The authors demonstrate that this method achieves single-shot reasoning performance on MATH500, HumanEval, GPQA, and AlpacaEval 2.0 that is comparable to or better than GRPO-based RL post-training across multiple base models (Qwen2.5-Math-7B, Qwen2.5-7B, Phi-3.5-mini-instruct), while maintaining generation diversity that RL post-training loses.

## Strengths

- **Compelling empirical results**: The method matches or exceeds GRPO on 3 out of 4 benchmarks across 3 different base model families, with particularly striking gains on out-of-domain tasks like HumanEval (+59.8% on Phi-3.5) and AlpacaEval 2.0. The pass@k analysis showing sustained diversity is a clear advantage over RL post-training.

- **Clean theoretical motivation**: The paper provides a clear mathematical distinction between low-temperature sampling and true power distribution sampling (Proposition 1), with a concrete toy example (Example 1) that illustrates why the power distribution is better suited for reasoning tasks involving "pivotal tokens."

- **Practical significance**: The method requires no training, no curated datasets, and no verifier, making it applicable to domains where reward signals are unavailable. This addresses a genuine limitation of current RL-based reasoning enhancement approaches.

## Weaknesses

### Major

- **Computational cost is not adequately addressed**: The expected token generation cost scales as O(N_MCMC * T² / B) (Equation 12). For T=3072, B=192, and N_MCMC unspecified (but presumably non-trivial), this could be orders of magnitude more expensive than a single forward pass. The paper reports no wall-clock time comparisons, FLOP estimates, or practical runtime analysis against GRPO inference. Without this, it's unclear whether the method is practically useful or merely a theoretical curiosity.

- **Missing ablation on N_MCMC and B**: The paper states B=192 and α=4.0 are used, but provides no ablation study showing how performance varies with these critical hyperparameters. The mixing time of the MCMC chain is a central concern, and the paper's claim that "we empirically find a value for B that makes Algorithm 1 performant for relatively small values of N_MCMC" is unsupported without showing what N_MCMC values were used and how performance degrades with smaller values.

- **The "single-shot" framing is misleading**: The paper claims "single-shot" performance, but Algorithm 1 makes many inference calls per final sample (potentially hundreds or thousands). This is not single-shot in the conventional sense used in the LLM literature (one forward pass). The paper should clearly distinguish between "one final response" and "one forward pass" and discuss the computational budget trade-off.

### Minor

- **Limited RL baseline comparison**: Only GRPO trained on MATH is used as the RL baseline. While GRPO is standard, the paper would benefit from comparison with other RL methods (PPO, Reinforce, etc.) or with supervised fine-tuning baselines to isolate whether the gains are specific to RL or more general.

- **The power distribution motivation relies on the "distribution sharpening" hypothesis being correct**: If RL post-training actually learns genuinely new behaviors (not just sharpening), the theoretical motivation weakens. The paper acknowledges this debate but doesn't fully address the possibility that their method might work for different reasons than those claimed.

### Trivial

- The paper uses "AlpacaEval2.0" in Figure 1 but "AlpacaEval 2.0" in the text; consistency would be appreciated.

## Nice-to-Haves

- A comparison with best-of-N sampling from the base model at equivalent compute budgets would help isolate whether the MCMC structure provides benefits beyond simple repeated sampling.
- Analysis of how the acceptance rate in the MH step varies across tasks and during the course of sampling would provide insight into chain mixing.
- Discussion of the failure cases where power sampling underperforms GRPO (e.g., MATH500 on Qwen2.5-Math-7B: 74.8 vs 78.5).

## Novel Insights

The paper's key insight—that the power distribution p^α, which is distinct from low-temperature sampling, can be approximately sampled via MCMC and yields reasoning improvements comparable to RL post-training—is genuinely novel. The formal distinction between "sum of exponents" (power distribution) and "exponent of sums" (low-temperature) in Proposition 1 is a clean theoretical contribution that clarifies a common misconception. The empirical finding that this training-free method maintains generation diversity while matching RL single-shot performance is practically significant and suggests that base models contain more latent reasoning capability than current sampling methods reveal.

## Suggestions

- Add a computational cost analysis: report wall-clock time per sample, total FLOPs, or number of forward passes for power sampling vs. GRPO inference, and include a plot of performance vs. compute budget.
- Provide an ablation study showing performance as a function of N_MCMC and B, with at least 3-5 values for each hyperparameter.
- Clarify the "single-shot" terminology throughout the paper, perhaps using "single-response" to describe the output and explicitly stating the inference-time compute cost.

## Score and Decision

The paper presents a well-motivated, theoretically grounded, and empirically strong method that achieves surprising results. The main concern is the lack of computational cost analysis, which is critical for assessing practical utility. However, the core contribution—showing that training-free MCMC sampling from the power distribution can match RL post-training—is significant enough to warrant acceptance even with this limitation, as the paper opens a new direction for inference-time reasoning enhancement.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>