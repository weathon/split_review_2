## Summary

This paper identifies a training-inference misalignment in tree-based speculative decoding: draft models are trained on linear sequences but used to generate trees at inference. The authors propose TALF, a tree-aware loss function that trains the draft model to match the target LLM's predictions across all tree branches, and SALF, a dynamic tree construction algorithm with a provably monotonic stopping criterion that balances tree quality against drafting overhead. Together, these yield 15.6–39.4% and 6.5–24.4% end-to-end speedups over EAGLE-2 and HASS across multiple models and benchmarks.

## Strengths

- **Clear and well-motivated problem identification.** The paper provides concrete empirical evidence of the training-inference misalignment: Figure 2(b) shows that while HASS improves calibration on 1st-ranked tokens, accuracy and ECE degrade for lower-ranked tokens (ranks 2–5), which constitute ~45% of the draft tree. This directly motivates TALF.

- **Thorough experimental evaluation.** The paper tests 3 target models (Llama2-7B, Llama3-8B, DeepSeek-R1-Distill-Llama-8B), 5 diverse benchmarks (MT-bench, HumanEval, GSM8K, Alpaca, CNN/DM), and 2 temperature settings. Table 2 provides a clean 3×3 ablation (3 tree methods × 3 losses) isolating individual contributions, and Tables 3–4 offer detailed parameter sensitivity analyses.

- **Practical and deployable.** The method requires no architectural changes to the draft model, uses the same EAGLE draft model architecture, and the precomputed tree structures are reusable across training epochs. The improvements are consistent and substantial across all tested configurations.

- **Sound theoretical backing.** Theorem 1 establishes that the probability sum in SALF is monotonically decreasing, providing a principled basis for the early stopping criterion. The proof is deferred to the appendix but the result is clean and practically useful.

## Weaknesses

### Fatal
None.

### Major

- **Non-uniform training protocols across models.** For Llama2-7B and Llama3-8B, the paper first trains with EAGLE loss for 10 epochs, then fine-tunes with HASS or TALF for 3 additional epochs. For DeepSeek-R1, all methods are trained for 24 hours from scratch. This inconsistency makes it harder to isolate whether improvements come from the loss function itself or from the training protocol. A uniform protocol (or at least a sensitivity analysis on training epochs) would strengthen the claims.

- **Limited model scale.** All experiments use 7B–8B parameter models. While this is understandable given computational constraints, it is unclear whether the relative improvements hold for larger models (e.g., 70B+), where the draft-target gap and tree structure may behave differently.

### Minor

- **TALF training cost not fully quantified.** The paper mentions that tree structures are precomputed by the target model and reused, but does not report the actual preprocessing time or memory overhead compared to EAGLE/HASS training. For practitioners, this information is important for adoption decisions.

- **SALF threshold sensitivity.** Table 4 shows the optimal threshold varies (0.5 for DeepSeek-R1), and the paper acknowledges this. The default of 0.6 is chosen for "consistent performance" across models, but a more principled or adaptive threshold selection method would be valuable.

### Trivial
None.

## Nice-to-Haves

- A comparison against non-EAGLE speculative decoding methods (e.g., Medusa, layer-skipping approaches) to contextualize the improvements within the broader SpD landscape.
- Wall-clock training time comparisons between EAGLE, HASS, and TALF to quantify the practical training cost difference.
- Experiments on larger target models to assess scalability.

## Novel Insights

The paper's central insight—that tree-based speculative decoding suffers from a fundamental training-inference distribution mismatch because draft models are trained on sequences but used to generate trees—is genuinely valuable and, to my knowledge, not previously articulated in the literature. The empirical demonstration that lower-ranked tree branches are poorly calibrated (Figure 2) provides concrete evidence that this mismatch matters in practice. The combination of a tree-aware training objective with a principled early-stopping criterion for tree construction forms a coherent and complementary pair of contributions.

## Suggestions

- Standardize the training protocol across all models (e.g., train all methods for the same number of epochs or the same wall-clock time) to ensure fair comparison.
- Report TALF preprocessing time (target model tree construction) and total training time alongside inference speedups.
- Consider an adaptive SALF threshold that adjusts based on the observed probability distribution during inference, rather than a fixed hyperparameter.

## Score and Decision

The paper presents a well-motivated, practically useful, and thoroughly evaluated contribution to speculative decoding. The training-inference misalignment is a real and previously underexplored problem, and both TALF and SALF are clean, effective solutions with strong empirical support. The improvements are consistent across models, tasks, and sampling strategies. The major weaknesses (non-uniform training protocol, limited model scale) are notable but do not invalidate the core claims.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: Accept