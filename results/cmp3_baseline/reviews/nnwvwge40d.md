## Summary

The paper proposes **VeriFree**, a method to extend DeepSeek-R1-Zero-style reinforcement learning (RL) to general reasoning domains without requiring any verifier (rule-based or model-based). By assuming a unique correct answer, the verifier-based objective is transformed into an expectation over reasoning traces of the probability assigned to the reference answer. This yields a gradient estimator with lower variance (due to Rao-Blackwellization) that naturally decomposes into a policy gradient term and a supervised learning term. VeriFree is evaluated on multiple general reasoning benchmarks (MMLU-Pro, GPQA, SuperGPQA) and math benchmarks against verifier-based baselines, matching or surpassing them while being simpler, faster, and more memory efficient.

## Strengths

- **Principled and practical derivation.** The paper starts from the standard RLVR objective and, under the single-correct-answer assumption, derives a verifier-free objective that is equivalent in expectation. The resulting gradient estimator enjoys provably lower variance via Rao-Blackwellization, which is both theoretically clean and practically beneficial.
- **Empirical competitiveness across scales.** VeriFree matches or outperforms a verifier-based baseline (using a fine-tuned 1.5B verifier) on Qwen3-1.7B, 4B, and 8B models on MMLU-Pro, GPQA, and SuperGPQA. It also shows stronger learning efficiency (converges faster and to higher accuracy) in training dynamics.
- **Clear practical advantages.** The method eliminates the need for a separate verifier model, reduces memory and computational overhead, and avoids reward hacking issues associated with model-based verifiers. These benefits make it attractive for real-world deployment.
- **Thorough ablations.** The paper carefully examines design choices: tokenization-aware reasoning-trace extraction (critical for training stability), RLOO variance reduction, and the effect of equivalence classes. The ablations support the proposed components.
- **Transferability demonstration.** Training VeriFree on non-math data produces measurable improvement on math benchmarks, suggesting that the method induces genuine general reasoning skills rather than domain-specific pattern matching.

## Weaknesses

### Fatal

None.

### Major

- **Unique answer assumption limits generality.** The core derivation assumes a single correct answer string. In many general reasoning tasks, multiple semantically equivalent answers exist (e.g., “8/5” vs “1.6”). While the paper provides an equivalence-class ablation showing modest gains, the main method does not handle this case, and the theoretical guarantee no longer holds. This is a significant limitation for a method targeting general reasoning.
- **Modest empirical gains and lack of statistical rigor.** The improvements over the verifier baseline are small (often 1–3% absolute, and sometimes slightly lower for the 1.7B model). The paper reports only point estimates without confidence intervals or multiple seeds, leaving it unclear whether the observed differences are robust. The claim of “matching and even surpassing” would be strengthened by uncertainty quantification.
- **Verifier baseline may be weak.** The verifier is a fine-tuned Qwen2.5-Math-1.5B, which is relatively small. A stronger verifier (e.g., 7B+ or a general-purpose LLM judge) might yield better baseline performance and reduce the margin. The paper acknowledges that verifier-based methods depend on verifier quality but does not explore this dimension, weakening the claim that VeriFree is generally superior.

### Minor

- **The method inherits sensitivity to prompt format.** VeriFree relies on a specific template with `<answer> \boxed{} </answer>` and accurate token-boundary detection. Generalization to other output formats is not tested.
- **The transfer experiment (Fig. 5) shows a noticeable but not dramatic improvement (≈5% on the math suite).** While positive, the effect is moderate and could benefit from deeper analysis of which math skills transfer.
- **The main comparison uses different optimization algorithms (VeriFree with RLOO vs. Verifier with Dr.GRPO).** Although both are on-policy estimators, differences in baseline methodology could confound the comparison. The paper could have used the same base algorithm for a cleaner ablation.

### Trivial

- The variance reduction theorem compares single-sample estimators, while the practical algorithm uses group sampling with RLOO; the realized variance reduction may be less pronounced.
- Response length increases after training, which is consistent with R1-Zero behavior but may increase latency.

## Nice-to-Haves

- Provide confidence intervals or run experiments with multiple random seeds (e.g., 3 seeds) for the main tables.
- Test with a larger or stronger verifier (e.g., a 7B reward model or GPT-4o as a judge) to see how VeriFree compares when the verifier is highly capable.
- Explore an extension that integrates equivalence classes natively into the objective (e.g., summing over reference answers or using a soft equivalence).

## Novel Insights

The key insight is that the verifier can be replaced by the model’s own probability of the reference answer given the reasoning trace, which acts as a continuous, lower-variance reward signal. The paper provides a nice example of Rao-Blackwellization in LLM RL—marginalizing out the answer variable analytically reduces variance without changing the expected gradient. Additionally, the strong correlation (ρ=0.82) between model confidence and accuracy suggests that self-estimated likelihood on the correct answer is a reliable proxy for reasoning quality, which could be leveraged beyond this work (e.g., for self-critique or curriculum learning).

## Suggestions

1. Report results with standard deviations or interquartile ranges from multiple training runs, especially for the main comparisons (Tables 1 and 2).
2. Consider an ablation that replaces the verifier baseline with a larger or more capable verifier to test the sensitivity of the main claim.
3. Discuss more explicitly the practical limitations of the unique answer assumption and propose a lightweight extension (e.g., down-weighting reward when the model generates a plausible alternative that differs from the reference) to mitigate it.

## Score and Decision

MY FINAL SCORE: 7.0 <score>7.0</score>
MY FINAL DECISION: Accept <decision>Accept</decision>