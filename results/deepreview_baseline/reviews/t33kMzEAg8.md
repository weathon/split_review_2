## Summary

The paper proposes SWIREASONING, a training-free inference framework that dynamically switches between explicit chain-of-thought reasoning and latent (continuous space) reasoning based on block-wise confidence estimated from entropy trends in next-token distributions. The framework also includes a switch count controller that caps the number of transitions to suppress overthinking and improve token efficiency. Experiments on 11 benchmarks across mathematics, STEM, coding, and general reasoning with four LLM families (Qwen3-1.7B/8B/32B, DeepSeek-R1-Distill-Llama-8B) show consistent improvements in accuracy (1.8%–3.1%) and token efficiency (57%–79%) over single-mode baselines.

## Strengths

- **Well-motivated and principled design**: The paper clearly identifies the complementary strengths and weaknesses of explicit reasoning (collapsing probability mass, discarding uncertainty) and training-free latent reasoning (preserving multiple hypotheses but introducing noise and overthinking). The key insight that reasoning should switch modes based on confidence is intuitive and well-supported by the entropy trend analysis. The asymmetric dwell window design (immediate switch when confidence rises in latent mode, delayed switch when confidence drops in explicit mode) is logically justified by the different roles of exploration and convergence.

- **Strong and comprehensive empirical validation**: The experiments cover 11 benchmarks across four domains, four model scales (1.7B, 8B, 32B), and three model families. SWIREASONING consistently outperforms all three baselines (CoT with sampling, CoT with greedy, Soft Thinking) under both unlimited and limited token budgets. The gains are particularly notable on harder benchmarks (e.g., +5.0% on AIME for Qwen3-1.7B, +18.18% on hard-level LeetCode-Contest). The Pass@k analysis further shows SWIREASONING achieves peak accuracy with significantly fewer samples (72% fewer on AIME24), which is valuable for budget-constrained scenarios.

- **Thorough ablation studies**: The paper systematically ablates the switch window size, signal mixing weights (α₀, β₀), and maximum switch count, providing insight into how each component affects performance. The results confirm the design choices (e.g., β₀=0.7 peaks near the best average, an intermediate window size of 512 works best) and reveal meaningful patterns (e.g., β₀=0.0 catastrophically degrades accuracy, showing the importance of the exit bias). This level of analysis strengthens confidence in the method.

## Weaknesses

### Fatal
None.

### Major
- **Limited comparison to other adaptive reasoning approaches**: The paper compares only to single-mode baselines (pure explicit or pure latent). It does not compare to other adaptive or hybrid reasoning methods such as dynamic depth control, early exit strategies, or methods that combine explicit and latent reasoning in different ways. While these are not exactly similar, the lack of comparison makes it harder to gauge the relative advantage of the specific switching mechanism. The paper also does not compare to any contemporary training-required latent reasoning methods, though the authors explicitly focus on training-free, so this is less critical.

- **No statistical significance reported**: The results report Pass@1 accuracy without error bars, confidence intervals, or any measure of variability (e.g., across multiple runs or random seeds). Given that CoT with sampling is inherently stochastic, and SWIREASONING also involves randomness (sampling in explicit blocks), the lack of significance testing makes it unclear whether the observed gains are reliable or within noise. This is important because many gains are modest (e.g., +0.39% on GSM8K for Qwen3-1.7B).

### Minor
- **Hyperparameter sensitivity not fully resolved**: The method introduces several hyperparameters (switch window size W, mixing weights α₀ and β₀, maximum switch count C_max) that require tuning for each benchmark. The ablations show that performance can vary notably with these values (e.g., β₀ sensitivity in Table 2, where AIME24 drops from ~50% to ~8% when β₀=0.0). The paper stops at ablating these values and recommends leaving α₀ to users per task; this limits the practical "training-free" appeal, as users must do non-trivial hyperparameter search. The paper does not propose an automatic adaptation strategy.

- **Clarity issues in the unlimited budget setting**: The paper states "token budgets are set large enough to ensure that each method is allowed to conduct sufficient thinking (refer to Appendix B.2 for detailed settings)". However, the definition of "sufficient thinking" and how the unlimited budget is operationalized (e.g., are all methods simply allowed to generate until they naturally stop?) is vague without reading the appendix. The main text could benefit from a clearer sentence summarizing the budget used.

- **The entropy-based switching criterion is deterministic and local**: The confidence estimate relies on a simple comparison of current entropy to a single reference entropy from the start of the block. This can be sensitive to noise in individual-token entropy fluctuations. The dwell window mitigates this somewhat, but the paper does not explore more robust aggregation (e.g., moving average, trend detection over multiple steps). The simple baseline seems effective empirically, but the paper could acknowledge this limitation.

### Trivial
- The figure captions in the paper body (Figure 3, Figure 4, Figure 5) contain redundant text that repeats the caption within the figure box. This appears to be a formatting artifact.

## Nice-to-Haves

- A sensitivity analysis showing performance as a function of C_max across benchmarks (currently only a brief description with reference to appendix).
- A comparison to a simple "random switch" baseline to isolate the benefit of the entropy-guided switching signal.
- Discussion of the computational overhead of computing entropy and performing the switch logic at each step (though this is presumably negligible).

## Novel Insights

Beyond the paper's own contributions, the key insight is that explicit and latent reasoning naturally form a complementary exploring-exploiting cycle where confidence signals (as measured by next-token entropy) serve as a reliable indicator for mode selection. The asymmetric dwell window design—immediate switching when confident in latent mode but delayed switching when uncertain in explicit mode—is a non-obvious but intuitively sound principle that prevents oscillation while allowing quick consolidation. The observation that switch count control can leverage partial reasoning trajectories at natural block boundaries (rather than arbitrarily truncating) provides a principled way to curb overthinking in latent reasoning, which is a problem that remains under-addressed in the literature.

## Suggestions

1. Add error bars or confidence intervals to the main accuracy results (Table 1, Table 4, Table 5) to help readers assess the reliability of the gains. At minimum, report whether gains are consistent across multiple seeds.
2. Compare against a "random switching" baseline (at uniform or fixed-interval switches) to empirically demonstrate that the entropy-guided criterion provides meaningful signal beyond simply alternating modes.
3. Consider adding an automatic hyperparameter selection rule for the switch window size and mixing weights (e.g., based on calibration set statistics) to reduce manual tuning and strengthen the "training-free" claim.
4. In the main text, provide a clearer statement of the unlimited token budget (e.g., "allowed to generate up to 4096 tokens or until the model naturally terminates").

## Score and Decision
**Score**: 8 (Accept)
**Decision**: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>