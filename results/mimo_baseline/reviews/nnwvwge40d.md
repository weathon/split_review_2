## Summary

This paper proposes VeriFree, a reinforcement learning method for training LLMs that eliminates the need for explicit answer verification. The key insight is a principled derivation showing that when there is a unique correct answer, the RLVR objective can be analytically reformulated to directly use the model's probability of generating the reference answer (given a reasoning trace) as the reward signal, which is shown to be equivalent in expectation to verifier-based RLVR but with lower variance via Rao-Blackwellization. The method is evaluated across multiple model scales (1.7B, 4B, 8B) on general reasoning benchmarks (MMLU-Pro, SuperGPQA, GPQA) and math benchmarks, demonstrating competitive or superior performance compared to verifier-based approaches.

## Strengths

- **Clean theoretical derivation with practical benefits.** The derivation from the standard RLVR objective to the VeriFree objective (Eq. 2→4→5) is principled and transparent, relying on standard analytical marginalization. The resulting method replaces binary verifier rewards with continuous probability signals, avoids maintaining a verifier model in memory, and has lower gradient variance by construction (Theorem 1 via Rao-Blackwellization).

- **Comprehensive experimental evaluation and ablations.** The paper evaluates across three model scales (1.7B, 4B, 8B), multiple benchmarks spanning diverse domains, and provides thorough ablations isolating the effects of the tokenization-aware extraction strategy, RLOO variance reduction, and equivalence classes. The transfer experiment (Fig. 5) is particularly compelling, showing that training without math data still improves math performance.

- **Competitive performance at scale.** On the 8B model, VeriFree matches or exceeds the verifier-based baseline on MMLU-Pro (67.2 vs. 65.9), SuperGPQA (38.0 vs. 37.1), and achieves strong results across all domains. The training efficiency advantage (Fig. 4, Left) is clearly demonstrated.

- **Practical tokenization handling.** The careful treatment of tokenization boundaries at the reasoning-answer split point (Section 2.4) is a subtle but important engineering contribution, validated by the ablation showing instability when using naive text-based splitting.

## Weaknesses

### Fatal
None.

### Major

- **Evaluation is almost entirely on multiple-choice tasks.** The core method assumes a unique answer string, and all main evaluation benchmarks (MMLU-Pro, SuperGPQA, GPQA) are multiple-choice. The paper's title and framing emphasize "general reasoning," but the evaluation doesn't cover open-ended generation tasks (e.g., free-form question answering, essay-style responses) where multiple valid answer formulations are common and the single-answer assumption breaks down. This significantly limits the demonstrated scope of the method. The equivalence-class ablation (Fig. 6 Right) confirms that when multiple valid answers exist, there is a measurable gap.

- **Verifier baseline comparison is somewhat confounded.** The Verifier baseline includes format compliance rewards (-0.5 for missing boxed) and a length penalty not present in VeriFree, and uses a specific fine-tuned 1.5B verifier model from Ma et al. (2025). While this is a reasonable practical choice, it makes it difficult to isolate whether VeriFree's advantages come from the methodological improvement or from differences in reward design. A cleaner comparison would use the same reward structure (e.g., verifier with only binary correctness reward).

### Minor

- **Math benchmark results are relegated to the appendix.** Given that RLVR was originally designed for math reasoning and that the paper claims transferability to math, presenting math results in the main text would strengthen the narrative. The current main-text results are limited to multiple-choice evaluation.

- **Modest improvements on smaller models.** On the 1.7B model, VeriFree and Verifier are nearly tied (46.9 vs. 47.0 on MMLU-Pro), and the improvements on 4B are also small. The stronger results emerge at the 8B scale, but the paper doesn't discuss why smaller scales show less differentiation.

- **Data filtering details are opaque.** The WebData creation uses Qwen2.5-72B-Instruct to filter "low-quality and noisy data," but no details are provided on filtering criteria, agreement rates, or how this interacts with the training distribution.

### Trivial
None.

## Nice-to-Haves

- An evaluation on at least one open-ended reasoning benchmark (e.g., Arena-Hard, AlpacaEval, or a free-form QA task) to demonstrate the method's behavior when the unique-answer assumption is violated in practice.
- A comparison where the verifier baseline uses only binary correctness rewards (without format/length penalties) to provide a cleaner apples-to-apples comparison.
- Analysis of how VeriFree handles cases where the reference answer is incorrect or ambiguous in the training data.

## Novel Insights

The paper's most insightful contribution is the demonstration that the variance in verifier-based RL stems from a source (answer sampling) that can be analytically removed via Rao-Blackwellization. This provides both theoretical elegance and practical efficiency. The empirical finding that model confidence π_θ(y*|x, z) correlates strongly with downstream accuracy (ρ=0.82) is also noteworthy—it suggests this quantity could serve as a lightweight training monitor or early stopping criterion without needing to run full evaluations. The observation that training on non-math data transfers to math benchmarks suggests that general reasoning training induces broadly useful reasoning skills rather than domain-specific patterns.

## Suggestions

- Include at least one open-ended evaluation benchmark in the main results to more convincingly demonstrate the "general reasoning" claim.
- Add an ablation comparing against the verifier baseline with only binary rewards to disentangle the methodological improvement from reward design differences.
- Discuss the failure modes more explicitly: under what conditions does the single-answer assumption lead to significant performance degradation?

## Score and Decision

This is a solid methodological contribution with clean theoretical grounding, thorough experiments, and a practical method that removes a real engineering burden (verifier maintenance). The core insight—analytically marginalizing over the answer—is elegant though not deeply novel (it follows naturally from standard RL theory). The main limitation is that the evaluation scope is narrow (multiple-choice only), which doesn't fully support the "general reasoning" framing. The improvements over the verifier baseline are real but modest on smaller models, becoming more convincing at 8B scale. The paper is well-written, the ablations are thorough, and the method is practically useful. Overall this is a competent paper with genuine practical value, but the incremental theoretical contribution and evaluation limitations prevent a stronger score.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>