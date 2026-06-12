## Summary

This paper introduces a conditional scaling law that extends the Chinchilla framework to incorporate architectural factors—hidden size, MLP-to-attention ratio, and grouped-query attention (GQA)—for jointly optimizing inference efficiency and model accuracy. By training over 200 models from 80M to 3B parameters and fitting a two-step calibration (reference optimal loss + architecture-conditional adjustment), the authors develop a practical search framework that identifies Pareto-optimal architectures achieving up to 42% higher inference throughput and 2.1% better accuracy than LLaMA-3.2 baselines.

## Strengths

- **Timely and practical research question.** The paper addresses a genuinely important gap: most scaling laws ignore inference cost, yet inference constitutes the dominant expense in real-world LLM deployment. The framing of architecture-aware scaling laws under fixed parameter/token budgets is well-motivated and practically relevant.

- **Extensive empirical study.** Training 200+ model variants across 80M–3B parameters with systematic architectural sweeps (varying hidden size, MLP-to-attention ratio, GQA) is a substantial effort. The systematic characterization of U-shaped curves for both hidden size and MLP-to-attention ratio (Figures 4, 5) provides useful empirical evidence that informs the scaling law design.

- **Actual validation through scaling up.** Unlike many scaling-law papers that stop at fitting, the authors validate their predictions by training 1B and 3B models (Panda and Surefire) and demonstrating real improvements. The progressive fitting strategy (Task 1→3) provides a principled evaluation methodology. The 42% throughput gain and 2.1% accuracy gain on real benchmarks are concrete, meaningful results.

- **Cross-platform robustness.** The authors validate throughput gains across vLLM and SGLang serving frameworks and on both A100 and H200 GPUs (Appendices F, G), showing that efficiency improvements transfer across serving stacks and hardware.

- **Practical ablation of fitting strategy.** The finding that fitting the scaling law on models closest in scale to the target (e.g., 1B data for 3B prediction) yields better predictions than the full progressive strategy is a useful practical insight for practitioners applying this framework.

## Weaknesses

### Fatal

None.

### Major

- **Limited evaluation scale (max 3B).** The paper never validates beyond 3B parameters. The authors acknowledge this limitation but it substantially constrains the claimed generality of the framework. At 3B, the accuracy improvement over LLaMA-3.2-3B is only ~0.6% on average, and the downstream evaluation is only on zero-shot benchmarks. It is unclear whether these architectural insights hold at 7B, 13B, or 70B scales, which is where inference cost becomes most critical. The Spearman correlation of 0.5 when extrapolating from 80M–1B to 3B (Figure 8 left) raises additional concerns about the scaling law's reliability at larger scales.

- **Narrow baseline comparisons.** The only baselines compared are LLaMA-3.2-1B and LLaMA-3.2-3B. Other open-source models at similar scales (e.g., Qwen2.5-1.5B, Gemma-2B, Phi-3-mini) use different architectural choices and would serve as stronger comparison points. Without these, it is hard to assess whether the proposed architectures are truly state-of-the-art or merely better than one particular baseline.

- **GQA not integrated into the scaling law.** GQA is handled via a separate local search with early stopping rather than being incorporated into the conditional scaling law, because the authors find it "does not exhibit a consistent continuous relationship with loss." This is a significant limitation since GQA contributes substantially to the throughput gains (the jump from GQA=3 to GQA=7 likely accounts for much of Surefire-3B's 42% throughput advantage over LLaMA-3.2-3B). The framework's claim of being "architecture-aware" is weakened when one of the three key architectural factors must be handled outside the scaling law.

### Minor

- **Separability assumption.** The scaling law assumes the effects of hidden size and MLP-to-attention ratio are separable (Eq. 3). While the authors report that non-separable formulations don't improve predictions (mentioned in §5), the results are deferred to an appendix and not directly substantiated in the main text. A brief justification or inline result would strengthen confidence.

- **Limited downstream evaluation.** Only 9 benchmarks in zero-shot setting are used, all of which are relatively easy comprehension/reasoning tasks. Stronger benchmarks (e.g., MMLU, GSM8K, HumanEval) would provide more compelling evidence, especially at the 3B scale where such tasks become partially tractable.

- **Fixed training tokens (100N).** All models are trained at 100N tokens (5× Chinchilla optimal). The paper does not explore whether architectural optima shift under different data regimes—e.g., compute-optimal (20N tokens) or data-rich (500N+) settings—which would be valuable for practitioners with different constraints.

### Trivial

None.

## Nice-to-Haves

- A brief analysis of what architectural features of Surefire models are most responsible for the throughput gains (GQA vs. MLP ratio vs. hidden size decomposition).
- Comparison of downstream task performance on more challenging benchmarks to assess whether the architectural choices affect capabilities beyond simple zero-shot accuracy.
- Analysis of whether the optimal MLP-to-attention ratio trends with model size, which would inform practitioners about scaling decisions.

## Novel Insights

The paper offers a genuinely useful empirical observation: under fixed parameter budgets, there exist interior optima for both hidden size and MLP-to-attention ratio that balance capacity allocation between attention and MLP components. The finding that current open-source models (particularly LLaMA-3.2) are suboptimally configured—with excessively high MLP-to-attention ratios (r≈4.8 at 3B) versus the predicted optimum (r≈1.0–1.2)—is a practically actionable insight. The practical lesson that scaling laws should be fit on models closest in scale to the target rather than always including all available data is also valuable for practitioners.

## Suggestions

- Scale the evaluation to 7B+ models to demonstrate that the architectural insights hold at the scales where inference cost matters most. Even a single 7B validation run would significantly strengthen the paper.
- Compare against a broader set of baselines beyond LLaMA-3.2, particularly Qwen2.5 and Gemma models at comparable parameter counts.
- Provide a decomposition of the throughput gains to separate the contributions of GQA, hidden size, and MLP-to-attention ratio, helping practitioners understand which architectural changes yield the most impact.

## Score and Decision

The paper tackles an important practical question with substantial empirical work and provides a useful framework validated at up to 3B scale. The conditional scaling law is a reasonable and practical contribution. However, the limited evaluation scale (3B max), narrow baselines (only LLaMA-3.2), incomplete integration of GQA into the scaling law, and modest accuracy improvements at 3B (0.6%) temper enthusiasm. The 42% throughput gain is impressive but likely dominated by GQA and hardware-level effects rather than the scaling law itself. The paper is a solid incremental contribution but falls short of being strongly impactful due to these limitations.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>