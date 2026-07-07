## Summary

The paper presents pcLLM, a progressive consistency distillation framework that trains autoregressive (AR) LLMs as efficient parallel decoders using Jacobi decoding. The key innovations are (1) a progressive noise schedule that gradually increases the noise ratio across blocks within a cyclic window, reducing the difficulty of predicting future tokens conditioned on noisy context; (2) a noise-aware causal attention mask enabling single-pass training loss computation via sequence packing; and (3) multi-block decoding with rejection recycling at inference time. On coding and math benchmarks, pcLLM achieves 3.6–3.8× wall-clock speedup over AR baselines while largely preserving quality, outperforming open-source diffusion LLMs (dLLMs) in both speed and accuracy.

## Strengths

- **Strong and clear empirical results**: pcLLM achieves 3.5–3.7× speedup over AR baselines while incurring only modest accuracy degradation (e.g., 87.8→84.8 on HumanEval, 92.4→91.4 on GSM8K). This decisively dominates open-source dLLMs (LLaDA, Dream, Fast-dLLM, D2F), which lose 2–4× in accuracy and still fall behind in speed.
- **Well-motivated progressive training strategy**: The progressive noise schedule is soundly motivated—reducing the longest noisy context span from O(nN) to O(⌈tn⌉)—and empirically validated in Table 4, where it outperforms both random and reverse schedules.
- **Training efficiency via sequence packing**: The noise-aware causal attention mask reduces training forward/backward passes from O(N) to O(1), a practically important contribution that enables efficient training on long reasoning chains.
- **Informative ablations**: Tables 4 and 5 cleanly isolate the contributions of noise schedule and mask type; the FLOPs utilization analysis in Figure 4 is useful for practitioner decisions.

## Weaknesses

### Fatal
None.

### Major

- **EAGLE-3/HASS comparison is deferred to the appendix.** Speculative decoding (especially EAGLE-3, which reuses target features) is the most directly competitive alternative for fast AR inference and is arguably a stronger comparison than dLLMs. Relegating it to the appendix obscures the actual competitive landscape. Without seeing these numbers, it is unclear whether pcLLM's overhead (trajectory generation + fine-tuning an entire model) is justified over adding a small draft head.

- **Multi-block decoding (MR) delivers marginal improvements over base pcLLM in several settings.** On A100/HumanEval, the gain from MR is 3.57→3.62× speedup—well within measurement noise. On A100/MBPP and GSM8K/MATH the gains are more visible, but the algorithm description (Algorithm 1) and Figure 3 add significant complexity. The paper would benefit from a clearer explanation of when MR materially helps versus when it does not, and why the gain is small on HumanEval despite 4.2× token acceptance count.

### Minor

- The iterative training round (progressively larger block sizes) is presented as yielding "up to 20%" speedup improvement, but with "slight degradation." This degradation is never quantified in the main paper, making it impossible to judge the tradeoff.
- The comparison to dLLMs uses models not specifically trained for coding/math in the same way pcLLM is (training on domain-specific instruction-following data). The performance gap between pcLLM and dLLMs may partly reflect training data quality rather than architectural or algorithmic differences.

### Trivial
- "qualitative speedup" in Section 3.2 appears to mean "quantitative."

## Nice-to-Haves

- A latency breakdown showing the cost of trajectory generation relative to training time and inference gains would help practitioners assess end-to-end value.
- Evaluation on longer sequences (e.g., reasoning traces >2048 tokens) would be valuable given the paper's stated motivation around chain-of-thought latency.

## Novel Insights

The key insight—that progressively increasing noise difficulty during consistency distillation training (rather than applying uniform or random noise) substantially improves the quality of predicted future tokens under Jacobi decoding—is genuinely useful. The observation that pcLLM produces high-quality draft n-grams in the trailing portion of unconverged blocks (Figure 2), and that this structure can be exploited by rejection recycling and multi-block decoding, is a well-presented empirical finding that could inspire further work on hybrid parallel/autoregressive decoding schemes.

## Suggestions

- Move the EAGLE-3/HASS comparison into the main results table, even in a summary form, to give a complete picture of the AR acceleration landscape.
- Quantify the accuracy drop from the second-round training with larger block sizes (20% speedup improvement at what quality cost?) to allow principled decisions about whether to use it.
- Provide an end-to-end wall-clock time analysis that includes trajectory generation and training overhead amortized over a realistic number of queries.

## Score and Decision

pcLLM is a solid contribution that addresses a genuine open question (can AR models be trained to match or beat dLLMs as parallel decoders?) with a well-designed training recipe, sound experiments, and results that clearly advance the state of the art for AR-based Jacobi decoding. The progressive noise schedule and sequence packing are the most technically interesting contributions. The missing comparison against speculative decoding in the main text is a meaningful gap that partially weakens the comparative claims, but does not undermine the contribution itself.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>