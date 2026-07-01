## Summary

This paper proposes a training-free inference-time method to elicit strong reasoning from base LLMs by sampling from a power distribution \(p^\alpha\) using a Metropolis-Hastings MCMC algorithm that iteratively resamples token subsequences according to the base model's own likelihoods. The method achieves single-shot performance that matches or exceeds GRPO-based RL posttraining on MATH500, HumanEval, GPQA, and AlpacaEval 2.0 across several model families, while maintaining generation diversity (pass@k) that RL methods collapse. The work is motivated by the distribution sharpening hypothesis and demonstrates that base models contain latent reasoning capabilities that standard sampling fails to surface.

## Strengths

- **Novel and clever approach**: The paper identifies a concrete target distribution (the power distribution) for reasoning and provides a principled MCMC algorithm to approximately sample from it, directly testing the distribution sharpening hypothesis without training.
- **Strong empirical results**: Across three model families (Qwen2.5-Math-7B, Qwen2.5-7B, Phi-3.5-mini-instruct) and four tasks, the method consistently matches or outperforms the GRPO baseline. On out-of-domain tasks like HumanEval and AlpacaEval, it often surpasses GRPO by a clear margin.
- **Preserved diversity**: The pass@k analysis (Figure 5) convincingly shows that the method avoids the diversity collapse characteristic of RL posttraining, achieving both strong single-shot performance and high multi-sample coverage.
- **Training-free and verifier-free**: The algorithm requires no additional training, curated datasets, or external reward signals, making it broadly applicable to domains where verifiable rewards are unavailable.
- **Clear writing and motivation**: The paper motivates the power distribution through the distribution sharpening literature and provides an intuitive example (Example 1) illustrating why power sampling differs from low-temperature sampling.

## Weaknesses

### Fatal
None.

### Major

1. **Computational cost is enormous and not characterized**  
   The expected token generation per sample scales as \( \frac{N_{\text{MCMC}} T^2}{4B} \). With \(T=3072\), \(B=192\), and even a modest \(N_{\text{MCMC}}=10\), this yields ~1.2M generated tokens per final sample. The paper reports no wall-clock time, FLOPs, or comparison of inference compute against GRPO inference or simple baselines (e.g., best-of-N with a verifier). Without this information, it is impossible to assess whether the method is practically viable or fundamentally inferior in compute efficiency. The claim "inference-time scaling" is true, but the scaling may be prohibitively expensive.

2. **Comparison to GRPO is not entirely fair and lacks context**  
   GRPO is trained only on the MATH training split and evaluated on MATH500, HumanEval, GPQA, and AlpacaEval. The method's strong out-of-domain performance is partly attributable to GRPO overfitting to MATH. The paper should compare against GRPO trained on a broader or multi-task dataset, or against other RL methods. Additionally, the GRPO baseline uses default hyperparameters from Shao et al. (2025), but no evidence is given that these are optimal for each model and task. The widening gap on out-of-domain tasks is consistent with GRPO's specialization and does not necessarily imply the method is superior for general reasoning.

3. **Lack of hyperparameter sensitivity analysis**  
   The method depends on \(\alpha\), block size \(B\), number of MCMC steps \(N_{\text{MCMC}}\), and the proposal temperature. The paper fixes \(\alpha=4.0\) and a specific \(B\) and proposal temperature, but provides no ablation to show how robust the results are to these choices. Given the computational cost, it is important to understand whether performance degrades significantly under suboptimal settings or whether the method is easy to tune.

4. **No theoretical or empirical guarantee of convergence**  
   The MCMC chain converges to the target \(p^\alpha\) only in the limit of infinite steps with an irreducible, aperiodic proposal. The paper uses a finite \(N_{\text{MCMC}}\) and a specific blockwise schedule (Algorithm 1). There is no analysis of mixing time, no diagnostic (e.g., effective sample size, trace plots), and no proof that the final samples approximate \(p^\alpha\) rather than some other distribution. The likelihood analysis in Figure 4 shows that the method samples higher-likelihood regions than the base model, but does not demonstrate that it samples from \(p^\alpha\) specifically.

### Minor

- The title claims "sampling directly from the base model", but the method samples from the power distribution \(p^\alpha\), not from the base model \(p\). While this is clarified in the body, the title could mislead readers.
- The pass@k analysis for GRPO (Figure 5) uses \(k\) samples from the RL model. Since GRPO is trained on a single correct answer per problem, it is not designed for diversity; the advantage of the proposed method in diversity is convincing but expected. A comparison against GRPO with higher temperature or explicit diversity regularization would strengthen the point.
- The algorithm's name "Power Sampling" may cause confusion with existing literature on power posteriors or tempering methods.

### Trivial
None.

## Nice-to-Haves

- Include a compute comparison (wall-clock time or FLOP-equivalent) between the proposed method, low-temperature sampling, and GRPO inference (single forward pass) to give readers a practical sense of the tradeoff.
- Provide an ablation study varying \(\alpha\), \(B\), and \(N_{\text{MCMC}}\) on a small subset of MATH500 to show sensitivity.
- Compare against best-of-N sampling with an oracle verifier (when available) to situate the method among other inference-time compute strategies.
- Discuss practical use cases where the high computational cost is acceptable (e.g., high-stakes problems, small-batch settings).

## Novel Insights

Beyond the paper's own contributions, the work offers a crisp empirical validation of the distribution sharpening hypothesis: RL posttraining primarily concentrates probability mass on high-likelihood base-model regions, and a well-designed inference-time sampler can recover most of that benefit without training. The observation that single-shot reasoning can be nearly matched by MCMC-based sampling from the base model is both surprising and practically important, as it suggests that "reasoning skills" are not created by RL but are latent in the base distribution and simply under-sampled by standard decoding methods. The maintained diversity under the proposed sampler further demonstrates that the sharpening effect of RL is not necessary for performance—it is a side effect that can be avoided.

## Suggestions

- To make the computational cost concrete, report the average number of forward passes per final sample and wall-clock time for the Qwen2.5-Math-7B experiments (e.g., on one A100 GPU). Compare this to the cost of GRPO inference and low-temperature sampling.
- Run an ablation on MATH500 (maybe 100 examples) varying \(\alpha\) from 2.0 to 6.0 and \(N_{\text{MCMC}}\) from 1 to 20 to show the Pareto frontier of compute vs. accuracy.
- Consider including an additional RL baseline trained on a broader mix of tasks (e.g., combined math + code + science) to better match the out-of-domain setting.
- Discuss the practical scenario where a verifier is available: how does the method compare to best-of-N with a verifier at equivalent compute budget?

## Score and Decision

The paper presents a genuinely novel and well-motivated sampling algorithm that achieves impressive results across multiple models and tasks. The core idea—that MCMC sampling from a sharpened base distribution can rival RL posttraining—is both interesting and practically relevant for settings where training or verifiers are unavailable. However, the lack of characterization of the enormous computational cost and the absence of hyperparameter sensitivity analysis are significant concerns that limit the paper's immediate impact and reproducibility. The empirical comparisons, while strong, would benefit from more context (e.g., broader RL baselines). The paper is a solid borderline accept that deserves a chance to address these issues in discussion.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>