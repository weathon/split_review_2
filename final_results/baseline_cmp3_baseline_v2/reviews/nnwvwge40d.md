## Summary

The paper proposes **VeriFree**, a verifier-free reinforcement learning method that extends R1-Zero-style training to general reasoning domains. Instead of using a rule-based or model-based verifier to check answer correctness, VeriFree directly maximizes the probability of the reference answer given a sampled reasoning trace, which is shown to be equivalent in expectation to the verifier-based objective under a unique correct answer assumption. The derived gradient estimator has lower variance (Rao-Blackwellization) and naturally avoids the practical overhead of maintaining a verifier. Experiments on Qwen3 models (1.7B–8B) across MMLU-Pro, GPQA, SuperGPQA, and math benchmarks show that VeriFree matches or outperforms verifier-based baselines while being simpler and more compute-efficient.

## Strengths

- **Principled theoretical derivation.** The paper derives the verifier-free objective directly from the verifier-based RL objective by analytic marginalization over the answer, establishing formal equivalence in expectation. The variance reduction argument (Theorem 1) is theoretically grounded and practically meaningful.
- **Practical relevance.** VeriFree eliminates the need for rule-based verifiers (which are often infeasible for general reasoning) and model-based verifiers (which are expensive, memory-hungry, and prone to reward hacking). The method is simple, reduces compute, and is easy to implement.
- **Strong empirical results across multiple scales.** The method is evaluated on three different model sizes (1.7B, 4B, 8B) and four comprehensive benchmarks. VeriFree consistently matches or exceeds the verifier-based baseline, and often approaches or surpasses the much larger instruct model in thinking mode.
- **Well-designed ablation studies.** The paper carefully ablates key design choices: tokenization-aware trace extraction, RLOO variance reduction, and the handling of equivalence classes. These experiments validate the importance of each component and provide clear practical guidance.
- **Demonstration of transferable reasoning.** Training VeriFree on non-math data still leads to improvement on math benchmarks, supporting the claim that the method induces general, transferable reasoning skills rather than domain-specific memorization.

## Weaknesses

### Fatal

None.

### Major

- **Uncontrolled comparison with the verifier baseline.** The verifier baseline (Ma et al., 2025) uses a composite reward function that includes format compliance (−0.5) and length penalties (−0.05×min(10,…)), while VeriFree optimizes only the proxy probability reward. The paper claims "all other settings are consistent" but the reward signals differ fundamentally. It is unclear whether VeriFree’s advantage stems from avoiding the verifier or simply from having a cleaner, less noisy reward. A controlled ablation—where the verifier baseline uses a pure correctness reward (1/0) without extra penalties—is necessary to isolate the effect of verifier-free training.

- **The verifier baseline itself is a potential confound.** The verifier is fine-tuned from Qwen2.5-Math-1.5B on Gemini-generated data. The quality of this verifier for general reasoning is not analyzed (e.g., its accuracy on the evaluation benchmarks). If the verifier is weak or miscalibrated, the baseline may be unfairly handicapped. The paper should report verifier accuracy or at least discuss this limitation.

- **Missing experimental comparison with JEPO/LaTRO in the main paper.** The paper claims that JEPO and LaTRO underperform verifier-based methods while VeriFree does not, but the supporting results are only in the appendix (which is not available for review). For a key claim (our method is better than prior verifier-free attempts), having these experiments in the main paper or at least summarized with numbers would strengthen the argument considerably.

### Minor

- **The “unique correct answer” assumption is limiting.** The method uses a single reference answer string, which cannot capture natural answer equivalence (e.g., different numerical formats). The ablation on equivalence classes (Fig. 6) shows only a slight gain, but for open-ended generation tasks this limitation could be significant. The paper acknowledges this but does not propose a practical solution for general use.

- **The variance reduction theorem (Theorem 1) is deferred to the appendix.** While the proof is not required in the main paper, providing a brief intuition or the key steps would improve readability. The current main text only states the result without any sketch.

- **The training dynamics plot (Fig. 4 Left) is smoothed with a moving average of 384 steps.** This heavy smoothing makes it hard to assess the true step-to-step behavior and the relative convergence rates. Raw curves or less aggressive smoothing would be more informative.

### Trivial

None.

## Nice-to-Haves

- Compute the additional cost of the extra forward pass needed to compute \( \pi_\theta(y^*|x,z) \) for each rollout, to quantify the overhead of VeriFree vs. verifier-based methods.
- Evaluate on a model family other than Qwen (e.g., Llama) to demonstrate generalizability.
- Include a qualitative analysis of generated reasoning traces (e.g., does VeriFree produce more coherent or logically sound chains of thought than the baseline?).

## Novel Insights

The paper’s central insight is that a verifier can be replaced by the model’s own conditional probability of the correct answer given the reasoning trace, without changing the expected gradient. This perspective reframes R1-Zero-style RL as optimizing a latent-variable model where the answer is marginalized out analytically, yielding a Rao-Blackwellized estimator with intrinsically lower variance. The comparison with JEPO and LaTRO further reveals that how one weights the answer-supervision term (probability vs. fixed weight) crucially affects learning dynamics—high-weighting poor reasoning traces can hurt. This is a subtle but practically important observation that improves upon prior verifier-free attempts.

## Suggestions

1. **Run a controlled experiment** where the verifier baseline uses a pure correctness reward (1/0) without format/length penalties, and compare with VeriFree under the same reward structure. This would directly test whether the performance gap is due to the verifier or to reward design.
2. **Report verifier accuracy** on the evaluation benchmarks to calibrate how much of the baseline’s behavior is due to verifier imperfection.
3. **Include a brief proof sketch or intuitive explanation** for Theorem 1 in the main paper (even one paragraph) so readers can grasp the variance reduction argument without accessing the appendix.
4. **Add concrete numbers for the JEPO/LaTRO comparison** in the main paper, or at least a clear statement that full results are in the appendix, if space permits.

## Score and Decision

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Borderline Accept</decision>