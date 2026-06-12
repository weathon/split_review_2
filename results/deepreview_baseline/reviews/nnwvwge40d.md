## Summary

This paper proposes VeriFree, a verifier-free reinforcement learning method for training large language models on general reasoning tasks. The key insight is that under a unique correct answer assumption, the standard RLVR (RL with verifiable rewards) objective can be rewritten to directly maximize the probability of generating the reference answer, eliminating the need for rule-based or model-based verifiers. The method derives a gradient estimator that marginalizes out the answer variable, achieving lower variance through Rao-Blackwellization while matching the expected gradient of verifier-based approaches. Experiments across MMLU-Pro, GPQA, SuperGPQA, and math benchmarks show VeriFree matches or outperforms verifier-based methods while being simpler, faster, and more memory-efficient.

## Strengths

- **Principled derivation with theoretical grounding**: The paper provides a clean mathematical derivation showing that VeriFree's objective is equivalent in expectation to the verifier-based objective under the unique answer assumption, with a formal variance reduction proof via Rao-Blackwellization. This theoretical foundation is a genuine contribution.

- **Practical significance of removing verifiers**: The method addresses a real bottleneck in extending R1-Zero-style training to general domains. Eliminating the need for rule-based or model-based verifiers reduces computational overhead (no additional model in memory), avoids reward hacking vulnerabilities, and simplifies the training pipeline. This is a practically valuable contribution.

- **Strong empirical results across multiple scales**: The experiments are conducted at three model scales (1.7B, 4B, 8B) on multiple challenging benchmarks (MMLU-Pro, GPQA, SuperGPQA). VeriFree consistently matches or exceeds verifier-based baselines, and the results are reported with detailed per-domain breakdowns, lending credibility to the claims.

- **Well-designed ablation studies**: The paper systematically ablates key design choices (tokenization-aware splitting, RLOO variance reduction, equivalence class handling) and provides clear evidence for each component's importance. The analysis of training dynamics and the correlation between model confidence and accuracy (ρ=0.82) is insightful.

## Weaknesses

### Major

- **Limited comparison to prior verifier-free methods**: The paper mentions JEPO and LaTRO as related verifier-free approaches and provides a gradient comparison, but the experimental comparison is relegated to Appendix E.2. Given that the paper's central claim is that VeriFree outperforms prior verifier-free methods, the main text should include at least a summary of these comparisons. The claim that JEPO and LaTRO "consistently underperform" verifier-based methods is stated without sufficient evidence in the main body.

- **The unique answer assumption is a significant limitation**: The derivation relies on the assumption of a single correct answer string. While the paper acknowledges this and provides an ablation on equivalence classes, the ablation shows only "slight performance improvements" from incorporating equivalence classes. For many real-world general reasoning tasks, multiple valid answer formulations exist, and the method's handling of this is acknowledged as a "minor limitation" but the practical impact is not thoroughly explored. The equivalence class experiment is also done only on math data, not on the general reasoning tasks that are the paper's focus.

- **Missing details on the verifier baseline**: The verifier baseline uses a model initialized from Qwen2.5-Math-1.5B fine-tuned on Gemini-generated data. The quality and training of this verifier are critical to the fairness of the comparison. If the verifier is weak, the comparison favors VeriFree. The paper does not report verifier accuracy or provide analysis of how verifier quality affects the comparison. Additionally, the verifier baseline uses additional reward components (format penalty, length penalty) that VeriFree does not use, making the comparison not perfectly apples-to-apples.

### Minor

- **The training dataset curation process is underspecified**: The paper mentions filtering to retain samples with answers fewer than seven tokens and using Qwen2.5-72B-Instruct to filter low-quality data, but provides no details on the filtering criteria, quality metrics, or the resulting dataset composition beyond a category distribution figure. This limits reproducibility.

- **Evaluation on math benchmarks is limited**: While the paper shows transfer to math, the math evaluation is presented as a single "Math-Eval-Suite" bar in Figure 5 without per-benchmark breakdown. Given that the method is motivated for general reasoning, more detailed math results would strengthen the transfer learning claims.

- **The variance reduction claim is not empirically validated**: Theorem 1 proves variance reduction theoretically, but the paper does not provide empirical measurements of gradient variance during training. This would strengthen the claim that variance reduction explains the improved learning efficiency.

### Trivial

- The paper uses "VeriFree" and "Verifier" as method names, but "Verifier" is also used as a generic term, which can cause minor confusion in reading.

## Nice-to-Haves

- An empirical comparison of training wall-clock time and memory usage between VeriFree and verifier-based methods would strengthen the practical benefits claim.
- Analysis of how the method performs when the reference answer is not in the model's vocabulary or when tokenization of the reference answer is problematic.
- Discussion of how VeriFree handles cases where the model generates a correct answer through an incorrect reasoning trace (the "lucky guess" problem).

## Novel Insights

The paper's key insight is that the verifier-based RL objective can be reformulated to use the model's own probability of the reference answer as a reward signal, which is both theoretically equivalent in expectation and practically beneficial due to variance reduction. This reframing of RLVR as a form of reward-weighted supervised learning with Rao-Blackwellization is a genuinely novel perspective that bridges policy gradient methods and supervised fine-tuning. The observation that model confidence π_θ(y^*|x,z) serves as a proxy for reasoning capability (ρ=0.82 correlation with accuracy) is also a useful empirical finding that could inform future work on self-supervised reasoning improvement.

## Suggestions

- Move the JEPO/LaTRO experimental comparison from the appendix to the main text, or at minimum include a summary table showing relative performance.
- Report verifier accuracy on the evaluation benchmarks to help readers assess the fairness of the verifier-based baseline comparison.
- Provide empirical gradient variance measurements to support the theoretical variance reduction claim.
- Include per-benchmark breakdowns for the math transfer experiment (Figure 5) rather than a single aggregate bar.

## Score and Decision

The paper presents a clean, theoretically grounded method that addresses a genuine practical limitation in extending R1-Zero-style training to general domains. The empirical results are strong and consistent across model scales. The main weaknesses are the limited comparison to prior verifier-free methods in the main text and the reliance on the unique answer assumption without thorough exploration of its practical impact. However, these are addressable and do not invalidate the core contribution. The paper is a solid contribution to the LLM reasoning literature.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>