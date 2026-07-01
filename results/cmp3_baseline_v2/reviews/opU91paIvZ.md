## Summary

This paper addresses the challenge of making chain-of-thought (CoT) reasoning *monitorable* — specifically faithful (hiding use of hints) and concise (short enough to oversee). The authors formulate the problem as a constrained optimization, show that naive RL fails due to sparse monitorability rewards and vanishing gradients, and propose a prior-guided distillation pipeline: a larger instruct model transforms base-model CoTs into monitorable (faithful/concise) forms, filters for reward preservation, and the base model is then fine-tuned on these transformed traces via supervised learning. Experiments on MMLU-Pro, GSM8K, and MATH500 show improved faithfulness (15%→25%) and increased conciseness (up to 60% length reduction) with minimal accuracy loss.

## Strengths

- **Clear problem formulation and failure analysis.** The constrained optimization view (Eq. 1) cleanly captures the accuracy-monitorability trade-off. The gradient analysis (Eq. 4‑5) convincingly explains why naive RL stalls: the base model almost never produces high‑f(z) traces, so the gradient signal for monitorability vanishes.
- **Practical and intuitive solution.** Using an external prior to densify the sparse reward signal and then distilling via SFT is simple, well-motivated, and circumvents the hard credit-assignment problem. The preliminary "proof of concept" (Fig. 3) cleanly verifies that monitorable traces are reward-compatible but rare.
- **Empirical gains on multiple benchmarks.** Faithfulness improves by ~10 absolute points (67% relative) across six categories, and conciseness improves dramatically (e.g., from 11.6% to 96.6% on MATH500) while task accuracy drops by only ~10 % relative — a practically meaningful trade-off.

## Weaknesses

### Major
- **Large gap between prior performance and distilled model.** The prior transformation (Fig. 3) achieves 85% faithfulness, but the trained model reaches only 25% (Fig. 4). This huge gap is not adequately discussed or explained. It suggests that the distillation is far from fully transferring the monitorability capability, weakening the claim that the method "solves" the problem.
- **Missing crucial baselines.** The paper does not compare with straightforward alternatives: (i) direct SFT on the prior's *original* CoTs (without the monitorability transformation), (ii) rejection sampling from the base model by resampling until a monitorable trace appears, or (iii) alternative RL approaches that shape the reward more carefully. Without these, it is unclear whether the gains come from the prior's better reasoning ability (since it is a 7B model) rather than from the monitorability-specific transformation.
- **Narrow faithfulness definition and noisy evaluation.** Faithfulness is defined only as verbalizing a sycophantic hint. This captures one important failure mode but omits others (e.g., post‑hoc rationalization of correct answers). The evaluation uses an LLM judge (prompt details are in the appendix) with no assessment of the judge's accuracy or agreement with human raters. The reported absolute numbers may therefore be unreliable.
- **Accuracy reporting for conciseness is incomplete.** The paper states "approximately 90% relative accuracy" but does not provide the actual accuracy numbers for the conciseness experiments in the main text or tables. Given that a 10% relative drop is non‑trivial for safety‑critical use, the raw numbers are essential for evaluating the method's practical viability.

### Minor
- **Single model scale and family.** All experiments use DeepSeek R1 Qwen‑1.5B as the base and Qwen 2.5‑7B as the prior. Results may not generalize to other architectures or sizes (e.g., larger models might already produce more monitorable CoTs; the dependency on a strong prior could be a practical bottleneck).
- **Arbitrary conciseness thresholds.** The length budgets (β=125 for GSM8K, β=950 for MATH500) are chosen without justification. The sensitivity of accuracy and conciseness to these thresholds is not explored. A discussion of how these thresholds should be set in practice is missing.
- **Gap between theory and algorithm.** The paper formulates a constrained optimization with a Lagrangian, but the actual algorithm (Algorithm 1) does not solve it; it uses the prior to generate data and then performs SFT. The connection between the theoretical framework and the practical method is loose.

## Nice-to-Haves

- An ablation comparing different filtering criteria (e.g., removing the reward‑equality filter) to show the importance of each design choice.
- Human evaluation of faithfulness for a subset of examples to validate the LLM‑as‑a‑judge approach.
- Experiments with a larger base model (e.g., DeepSeek R1 7B) to test whether the method works at more practical scales and to reduce the size gap with the prior.

## Novel Insights

Beyond the paper's own contributions, the key insight is that monitorable trace properties (faithfulness, conciseness) are frequently *reward-compatible but sampling-rare* — they exist in the policy's support but with vanishing probability, leading to gradient starvation. This framing, together with the demonstration that a stronger prior can effectively "fill in" these rare regions, provides a clear diagnosis of why vanilla policy gradients fail for auxiliary behavioral objectives and suggests a general recipe: densify the signal via a capable external model, then distill. This pattern may be applicable to other sparse‑reward problems in language model alignment beyond CoT monitoring.

## Suggestions

1. Provide the exact accuracy numbers for the conciseness experiments (both base and trained model) and state the relative drop explicitly.
2. Add a baseline that fine‑tunes on the prior's CoTs *without* the monitorability transformation (i.e., just distill the 7B model's reasoning style) to isolate the effect of the transformation.
3. Discuss why the trained model's faithfulness (25%) is far below the prior's (85%) and whether this gap can be closed by longer training, larger data, or a different distillation objective.
4. Validate the LLM judge for faithfulness (e.g., compare against human ratings on a held‑out subset or against the "gold" labels if available from the dataset creators).

## Score and Decision

**Score:** 5.0  
**Decision:** Reject

**Rationale:** The paper tackles a timely and well‑motivated problem, provides a clear analysis of why naive RL fails, and shows empirical gains. However, several major weaknesses undermine the contribution: the trained model's faithfulness far underperforms the prior, critical baselines are absent, the faithfulness metric and evaluation have unvalidated reliability, and accuracy numbers for conciseness are not clearly reported. These issues prevent the paper from providing a convincing demonstration that the proposed method offers a substantial advance over existing approaches. The ideas are promising, but the experimental validation is insufficient for acceptance at a top venue.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>