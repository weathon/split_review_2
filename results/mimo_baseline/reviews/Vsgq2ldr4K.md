## Summary

This paper proposes "Power Sampling," a training-free inference-time algorithm that approximates sampling from the power distribution $p^\alpha$ of a base LLM using a block-wise Metropolis-Hastings MCMC procedure. The key theoretical insight is that the power distribution (sum-of-exponents over futures) is fundamentally different from and superior to low-temperature sampling (exponent-of-sums) for reasoning tasks, as it implicitly favors tokens with fewer but higher-likelihood future completions. The method achieves single-shot performance comparable to GRPO on in-domain math tasks and often outperforms it on out-of-domain tasks (HumanEval, GPQA, AlpacaEval 2.0) across three model families, while preserving generation diversity.

## Strengths

- **Clean theoretical contribution.** Proposition 1 rigorously distinguishes power distribution sampling from low-temperature sampling, and Example 1 provides clear intuition. The observation that $p^\alpha$ upweights tokens with few high-likelihood future paths (sum-of-exponents) vs. low-temperature sampling which upweights tokens with many lower-likelihood completions (exponent-of-sums) is a genuinely useful analytical lens for understanding inference-time reasoning.

- **Strong and consistent empirical results across models and tasks.** Table 1 shows results across Qwen2.5-Math-7B, Qwen2.5-7B, and Phi-3.5-mini-instruct on MATH500, HumanEval, GPQA, and AlpacaEval 2.0. Power sampling consistently matches or exceeds GRPO, with particularly striking gains on out-of-domain tasks (e.g., +59.8% relative on HumanEval for Phi-3.5-mini, and consistent outperformance on AlpacaEval 2.0). The results are robust across model families.

- **Diversity preservation is a significant practical advantage.** Figure 5 demonstrates that power sampling's pass@k curve strictly dominates both GRPO and the base model, and converges to the base model's high-k performance. This addresses a well-documented failure mode of RL-posttraining (diversity collapse) and gives the method a genuine practical edge for best-of-N or multi-sample settings.

- **Novel framing connecting distribution sharpening to inference-time sampling.** The paper reframes the "distribution sharpening" hypothesis not as a limitation but as an actionable principle: if RL-posttrained models are sharpened base distributions, then explicit sharpened sampling from the base model should suffice. This is a creative and well-motivated research direction.

## Weaknesses

### Fatal
None.

### Major

- **Missing computational cost analysis.** Equation 12 estimates expected tokens generated as $N_{\text{MCMC}} T^2/(4B)$, but $N_{\text{MCMC}}$ is never stated in the main paper (only block size $B=192$ and $T_{\max}=3072$ are given). With plausible values of $N_{\text{MCMC}} \sim 5\text{-}10$, this yields on the order of $10^5$ tokens generated per single sample—a factor of 100-200× more inference compute than a single autoregressive pass. The paper never reports wall-clock time, FLOPs, or total tokens consumed. Since the method is framed as "inference-time scaling," this computational overhead is central to evaluating the contribution and should be transparently reported and compared against GRPO's inference cost.

- **No comparison with other inference-time compute methods.** The only baselines are low-temperature sampling and GRPO. Missing are comparisons with best-of-N sampling (with a verifier or reward model), beam search, self-consistency, or other inference-time scaling approaches (e.g., compute-optimal strategies). Without these, it is difficult to assess whether power sampling's gains come specifically from the power distribution target or simply from using more inference compute.

- **Unfair out-of-domain comparison against GRPO.** GRPO was trained exclusively on MATH, so its out-of-domain performance on HumanEval and GPQA reflects distribution shift from the training data, not a fundamental limitation of RL. The paper's strongest claims about outperformance are therefore against a suboptimally adapted baseline. This should be discussed more explicitly, and ideally a GRPO variant trained on coding or science data should be included.

### Minor

- **No sensitivity analysis on key hyperparameters.** The choice of $\alpha=4.0$ and $N_{\text{MCMC}}$ are not justified or ablated. The method's robustness to these choices is unclear. A simple ablation showing performance vs. $\alpha$ and $N_{\text{MCMC}}$ would significantly strengthen confidence in the method.

- **Weak GRPO baseline for Phi-3.5.** On Phi-3.5-mini-instruct, GRPO achieves 0.406 on MATH500 (barely above the 0.400 base) and 0.134 on HumanEval (below the 0.213 base), suggesting training difficulties. The paper acknowledges instability issues but this makes the Phi-3.5 comparisons less informative.

- **No MCMC convergence diagnostics.** The paper does not discuss how convergence to the target distribution is assessed. In high-dimensional token spaces, MCMC mixing can be unreliable, and some evidence of effective convergence (e.g., acceptance rates, effective sample sizes) would strengthen the methodological claims.

### Trivial
None.

## Nice-to-Haves

- A wall-clock time comparison table showing total inference tokens/FLOPs for each method across all benchmarks.
- An ablation study on $\alpha$ and $N_{\text{MCMC}}$ to understand sensitivity.
- Comparison with best-of-N sampling using the base model's own likelihoods as a scoring function.

## Novel Insights

The paper's core novel insight is that the power distribution $p^\alpha$ (sum-of-exponents over futures) is fundamentally better suited for reasoning than low-temperature sampling (exponent-of-sums), because it implicitly performs a form of "future-aware" token selection that avoids critical windows and pivotal tokens that lead to dead-end completions. Combined with the empirical finding that this simple distributional change can nearly replicate RL-posttraining gains—while preserving diversity—this provides a compelling argument that much of RL's value for reasoning lies in sharpening rather than learning new capabilities, and that this sharpening can be achieved at inference time alone.

## Suggestions

- Report $N_{\text{MCMC}}$ and total inference compute explicitly; include a compute-normalized comparison (e.g., accuracy vs. total tokens generated) against GRPO and best-of-N.
- Add an ablation over $\alpha \in \{1, 2, 4, 8, 16\}$ and $N_{\text{MCMC}} \in \{1, 3, 5, 10\}$ to characterize the method's sensitivity and scaling behavior.
- Include a comparison with best-of-N sampling (using base model likelihood as the selector) to isolate the contribution of the power distribution target from the contribution of simply using more inference compute.

## Score and Decision

The paper presents a clean theoretical insight (power vs. temperature sampling), a practical MCMC algorithm, and strong empirical results across multiple models and tasks. The diversity advantage is a genuine and important contribution. However, the absence of computational cost transparency and comparison with other inference-time methods significantly limits the ability to evaluate the true contribution. These are addressable issues but represent a meaningful gap in the current submission.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <score>Accept</score>