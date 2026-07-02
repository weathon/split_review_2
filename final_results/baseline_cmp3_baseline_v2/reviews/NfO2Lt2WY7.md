## Summary

This paper systematically ablates the GRPO loss function to determine which components are essential for improving LLM reasoning on math tasks. It finds that (1) negative feedback is indispensable, (2) group-relative advantage estimation is crucial for stability, and (3) PPO-style clipping and policy ratio terms are unnecessary. Based on these findings, the authors propose RGR (REINFORCE with Group Relative Advantage), a simplified variant that removes clipping and policy ratios. Experiments on Qwen2.5 (0.5B, 1.5B) and Llama3.2 (1B) models across English/Chinese math and STEM benchmarks show that RGR achieves competitive or better performance than GRPO, with more stable training dynamics.

## Strengths

- **Timely and practically important research question.** GRPO has become a standard post-training method for reasoning LLMs, so understanding which of its many components are truly necessary has high practical value.
- **Clean, systematic ablation methodology.** The paper isolates three specific factors (positive-only advantages, removal of PPO-style clipping, removal of advantage estimation) and evaluates them in controlled settings. This provides clear causal evidence rather than just comparing final variants.
- **Well-supported key findings.** The paper convincingly shows that positive-only training (RAFT, positive-only GRPO) leads to collapse, that removing advantage estimation (direct REINFORCE) destabilizes training, and that removing PPO-style constraints (RGR) does not harm stability and can improve performance. These conclusions are backed by both training dynamics and benchmark scores.
- **Strong empirical performance.** RGR outperforms GRPO on 17 out of 27 individual benchmarks across model families and sizes, and achieves the highest average scores on the English Math, Chinese Math, and STEM benchmark groups for Qwen2.5 models.
- **Emergent reasoning analysis.** The paper provides qualitative examples showing that GRPO and RGR induce explicit reasoning traces while positive-only methods produce direct answers, supporting the claim that proper advantage estimation fosters interpretable reasoning.

## Weaknesses

### Fatal

None.

### Major

1. **Model scale is limited to ≤1.5B parameters.** The paper's central claim that PPO-style clipping is unnecessary for reasoning post-training may not generalize to larger models (e.g., 7B, 70B) where distribution shift is more severe and stable training is harder. The authors acknowledge this as future work, but it fundamentally limits the impact of the conclusions for a venue like ICLR.

2. **Training data is extremely small (1800 examples from GSM8K only).** Using only 1800 instances risks overfitting and raises concerns about whether the findings generalize to larger, more diverse training mixtures. The choice to use such a small subset is not well justified, and it weakens confidence that the insights hold in realistic post-training scenarios.

3. **No hyperparameter tuning analysis for the ablated components.** The paper keeps all hyperparameters (e.g., clipping epsilon, KL coefficient β) identical when comparing GRPO and RGR. If GRPO's clipping hyperparameters were suboptimal for the chosen setting, the comparison may unfairly favor RGR. A sensitivity analysis (e.g., varying β or epsilon) is needed to confirm that the superiority of RGR is not an artifact of poor tuning.

4. **Statistical significance and variance are not reported.** Benchmark results are presented as single-point accuracies without confidence intervals or multiple seeds. Given the small model sizes and training set, run-to-run variance could be substantial. Without error bars, it is unclear whether the observed improvements of RGR over GRPO are reliable.

5. **Code is not provided and the reproducibility statement is incomplete.** The paper states "The link to our code is ." (empty), which severely limits reproducibility. While the algorithm description is clear, the lack of released code is a concern for a paper whose main contribution is an algorithmic simplification.

### Minor

- The paper uses "RGRA" and "RGR" inconsistently (the proposed method is called RGR in the abstract and most sections, but RGRA in some places including the conclusion).
- The paper does not compare against a simple REINFORCE baseline with an exponential moving average baseline (which would further isolate the benefit of group-relative advantage estimation specifically).
- KL regularization is kept in RGR, so the paper does not fully remove all "constraints"—only PPO-style clipping. The contribution should be framed more precisely as "PPO-style clipping is unnecessary" rather than "PPO-style constraints are unnecessary."
- The paper uses LoRA with rank 128 (≈10% parameters). It is not discussed whether full fine-tuning would change the relative ordering of methods.

### Trivial

None.

## Nice-to-Haves

- Providing training compute cost comparisons (time/flops per step) between GRPO and RGR would strengthen the efficiency argument.
- Running experiments at 7B scale (even one model) would substantially increase the impact and generalizability of the findings.
- Reporting results with multiple random seeds and including standard deviations would add rigor.

## Novel Insights

The key novel insight is that the effectiveness of GRPO for reasoning post-training does not stem from its PPO-style clipped surrogate objective, but from the combination of group-relative advantage estimation (which provides a learned, prompt-conditioned baseline) and the inclusion of negative feedback. This suggests that the standard RL motivation for clipping (preventing large policy updates from a randomly initialized policy) does not apply when fine-tuning a strong pre-trained LLM, because the initial policy is already near-optimal in many regions. The paper thus provides evidence that simpler REINFORCE-style methods are sufficient for LLM reasoning post-training, which aligns with and extends recent work questioning the necessity of complex RL objectives in the LLM setting. None beyond the paper's own contributions.

## Suggestions

1. Run at least one experiment at 7B scale to confirm that the findings hold when distribution shift is more significant. Even a single model on the same training setup would greatly strengthen the claims.
2. Add error bars (e.g., 3 seeds) to all benchmark tables. Report the statistical significance of the RGR vs. GRPO differences.
3. Include a hyperparameter sensitivity analysis for the KL coefficient β and the clipping epsilon ε to ensure the comparison between GRPO and RGR is fair.
4. Provide the code and exact training configurations in the supplementary material or repository.

## Score and Decision

The paper addresses an important and timely question with a well-structured ablation methodology. The findings are clear and practically useful. However, the limited model scale and training data size, combined with the lack of statistical rigor and missing code, prevent the paper from making a definitive contribution that would justify strong acceptance. The insights are likely correct but need stronger evidence for broader claims.

MY FINAL SCORE: 6.0<score>6</score>
MY FINAL DECISION: Accept<decision>Accept</decision>