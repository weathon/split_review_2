## Summary

This paper proposes a training-free inference-time sampling algorithm that uses Metropolis-Hastings MCMC to approximately sample from the power distribution \(p^\alpha\) of a base language model. The authors argue that RL-posttraining primarily sharpens the base model distribution, and that sampling from the power distribution can achieve comparable single-shot reasoning performance without any training, curated datasets, or verifiers. Experiments across multiple base models (Qwen2.5-Math-7B, Qwen2.5-7B, Phi-3.5-mini-instruct) and benchmarks (MATH500, HumanEval, GPQA, AlpacaEval 2.0) show that their method nearly matches or outperforms GRPO, while also maintaining better generation diversity.

## Strengths

- **Novel and well-motivated approach.** The paper provides a clean theoretical motivation for why sampling from the power distribution \(p^\alpha\) is beneficial for reasoning, clearly distinguishing it from low-temperature sampling via Proposition 1 and Example 1. The connection to distribution sharpening in RL-posttraining is well-articulated and gives a principled reason to expect the method to work.
- **Strong empirical results across multiple models and tasks.** The method achieves substantial improvements over base models (e.g., +25.2% on MATH500, +51.9% on HumanEval) and is competitive with or outperforms GRPO on both in-domain and out-of-domain tasks. The results are demonstrated across three different base model families (Qwen2.5-Math-7B, Qwen2.5-7B, Phi-3.5-mini-instruct), showing generality.
- **Addresses a known limitation of RL-posttraining.** The paper convincingly shows that their method avoids the diversity collapse that afflicts GRPO, as evidenced by the pass@k curves (Figure 5) and the likelihood/confidence histograms (Figure 4). This is a genuine advantage over RL-based approaches.
- **Training-free, dataset-free, and verifier-free.** The method requires no additional training, no curated datasets, and no external verifier, making it broadly applicable to domains where verifiable rewards are unavailable. This is a significant practical advantage.

## Weaknesses

### Fatal
None.

### Major
- **Computational cost is not adequately addressed.** The expected token generation cost is \(\frac{N_{\text{MCMC}} T^2}{4B}\), which scales quadratically with sequence length \(T\). For \(T=3072\), \(B=192\), and \(N_{\text{MCMC}}\) (not explicitly stated but implied to be moderate), this can be orders of magnitude more expensive than a single forward pass. The paper does not report wall-clock time, FLOPs, or total token generation cost for their experiments, making it difficult to assess the practical trade-off. While the method is "training-free," the inference cost may be prohibitive for many applications, and this is a significant practical limitation that is not adequately discussed.

- **Limited analysis of hyperparameter sensitivity.** The method introduces several hyperparameters (power \(\alpha\), block size \(B\), number of MCMC steps \(N_{\text{MCMC}}\), proposal distribution temperature) with no systematic ablation study. The paper states that \(\alpha=4.0\) and \(B=192\) are "most performant" but does not show how performance varies with these choices. The sensitivity of the method to these hyperparameters is important for understanding its practical robustness.

- **The GRPO baseline may be weak for out-of-domain tasks.** The paper uses GRPO trained only on MATH, which is a reasonable choice for studying in-domain vs. out-of-domain generalization. However, the claim that power sampling "outperforms" RL on out-of-domain tasks (HumanEval, AlpacaEval) is less surprising given that GRPO was not trained on those domains. A stronger baseline would be GRPO trained on a mixture of domains, or a comparison with other inference-time methods like self-consistency or best-of-N sampling.

### Minor

- **The pass@k analysis (Figure 5) uses a small number of samples (k up to 16).** While the trend is clear, the claim that power sampling "matches the base model" at high k is based on only 16 samples. The curves for base and power sampling converge at k=16, but it is unclear if this convergence holds for larger k (e.g., k=100 or k=1000). The paper would benefit from a discussion of whether the convergence is asymptotic or if power sampling eventually underperforms the base model at very large k.
- **The method is only evaluated on relatively small models (7B and below).** While the paper claims broad applicability, it is unclear how the method scales to larger models (e.g., 70B+). The quadratic token cost in T may become prohibitive for larger models, and the MCMC mixing properties may differ.

### Trivial
None.

## Nice-to-Haves
- An ablation study showing the effect of different values of \(\alpha\), \(B\), and \(N_{\text{MCMC}}\) on performance and computational cost.
- Wall-clock time or FLOPs comparison between power sampling, GRPO, and standard sampling to contextualize the computational cost.
- Experiments on larger models (e.g., 70B scale) to test scalability.

## Novel Insights

The paper's key insight is that the power distribution \(p^\alpha\) provides a principled and theoretically motivated target for inference-time reasoning that is distinct from low-temperature sampling. The formal distinction (Proposition 1) and the illustrative example (Example 1) clearly show that power sampling inherently accounts for future path likelihoods, which is valuable for reasoning tasks involving "pivotal tokens." The empirical finding that this training-free method can match RL-posttraining while maintaining diversity is a genuinely novel observation that challenges the prevailing narrative that RL is necessary for eliciting strong reasoning capabilities.

## Suggestions
- Report wall-clock time or total generated tokens for the method vs. baselines to allow practitioners to assess the computational trade-off.
- Include an ablation study varying \(\alpha\), \(B\), and \(N_{\text{MCMC}}\) to show robustness and guide hyperparameter selection.
- Add a comparison with other inference-time methods such as self-consistency (majority voting over multiple samples) or best-of-N sampling with a verifier, to better contextualize the method's performance.

## Score and Decision

The paper presents a novel, well-motivated, and empirically strong method for inference-time reasoning that challenges the prevailing RL paradigm. The theoretical distinction between power sampling and low-temperature sampling is clear and insightful. The empirical results are impressive across multiple models and tasks, and the method's ability to maintain diversity while achieving strong single-shot performance is a genuine advantage. However, the lack of computational cost analysis and limited hyperparameter sensitivity analysis are notable weaknesses. The paper is a solid contribution to the community.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>