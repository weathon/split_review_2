## Summary

This paper introduces Dynamic Nested Depth (DND), a post-training method that improves LLM performance by identifying critical tokens via a learned router and reprocessing them through the same transformer layer for additional computation. The method includes a normalized fusion strategy for combining vanilla and nested outputs, along with carefully designed training strategies (router controlling loss and threshold control scheme) to ensure stable and discriminative token selection. Experiments on three dense models (Qwen3-1.7B, Llama3.2-1B, Gemma3-1B) and one MoE model (Qwen3-30B-A3B) demonstrate consistent improvements across diverse benchmarks with minimal parameter overhead.

## Strengths

- **Well-motivated and clean architecture design.** The paper clearly motivates the approach from two perspectives (token-level adaptive computation and latent test-time scaling) and presents a straightforward architecture: a linear router selects tokens, selected tokens are reprocessed through the same layer, and outputs are fused via a normalized gating mechanism. The design choices (token-choice routing over expert-choice to avoid information leakage, applying DND only to intermediate layers) are well-justified.

- **Thorough training strategy design with strong empirical validation.** The dual-objective router controlling loss (score dispersion + distribution preservation) and the threshold control scheme (buffer proportional control + EMA synchronization) are well-designed and well-ablated. Figures 5, 6a, and 6b convincingly demonstrate that each component contributes to stable training. The ablation in Table 4 shows that the full system outperforms any individual component by ~0.3-0.9 points.

- **Comprehensive evaluation and insightful analysis.** The paper evaluates across 4 models and 20+ benchmarks spanning general knowledge, math/STEM, and coding/agent tasks. The token selection analysis (Figures 4a, 4b, 7a, 7b) provides genuine insight: tokens with higher logit entropy are preferentially selected, and DND reduces their entropy, confirming the method works as intended. The hierarchical processing pattern (shallow layers select entities, deeper layers select abstract/syntactic tokens) is an interesting finding.

- **Practical post-training applicability.** Unlike MOR which requires pretraining from scratch on 200B+ tokens, DND can be directly applied to existing pretrained models through SFT, making it immediately useful for practitioners. The parameter overhead is negligible (<0.1M) and throughput reduction is only 7-8%.

## Weaknesses

### Fatal
None.

### Major

- **No direct experimental comparison with MOR (Bae et al., 2025).** The paper extensively discusses differences with MOR in Section 2.2 (training phase, model scale, architecture, routing control) but never provides a head-to-head experimental comparison. Since MOR is the most closely related work sharing the same goal of improving performance via dynamically increased computational depth, this omission makes it difficult to assess DND's relative merit. Even a comparison at the 1B scale where MOR was evaluated would be valuable.

- **Vague training data details undermine reproducibility.** Section 4.2 states the training data "incorporates a significant volume of synthetic material built upon a high-quality seed set of 1-2 million instances curated from human annotations and open-source materials." This is insufficient for reproducibility and raises concerns about data contamination. The SFT data composition could significantly affect benchmark results, and without knowing the data mix, it's impossible to disentangle the contribution of DND from the data.

- **Modest improvements on the MoE scaling experiment.** The average improvement of +0.87 on Qwen3-30B-A3B, while consistent (no degradation on any benchmark), is relatively small. Several individual benchmarks show gains within noise margins (e.g., +0.13 on BBH, +0.15 on MATH, +0.20 on MATH-500). The paper would benefit from statistical significance testing or confidence intervals to distinguish genuine improvements from noise.

### Minor

- **Limited diversity of dense model scales.** All three dense models are in the 1B-1.7B range. Testing on a 7B or 8B dense model would strengthen the claim that DND generalizes across scales, especially since the MoE model's improvements are more modest.

- **Sensitivity analysis of key hyperparameters is incomplete.** The ablation studies cover selection ratio and layer range, but the sensitivity to α (threshold step size), γ (EMA smoothing factor), buffer size, λ_sd, and λ_dp is not analyzed. These hyperparameters could significantly affect training stability and final performance.

- **The claim about ITT's information leakage is somewhat underdeveloped.** The paper states ITT's Top-P-based selection "introduces a mismatch between training and inference, and may also lead to potential information leakage" citing Raposo et al. (2024), but this is only tested on one model (Qwen3-1.7B) and the comparison is limited.

### Trivial
None.

## Nice-to-Haves

- A comparison with MOR at the 1B scale to directly quantify DND's advantage as a post-training method.
- Statistical significance tests or multiple-seed runs for the main results.
- Analysis of how DND interacts with different SFT data compositions or quality levels.
- Discussion of how the method performs on longer-context tasks where token selection might behave differently.

## Novel Insights

The paper's most interesting empirical finding is the hierarchical token selection pattern revealed in Figure 7b: shallower DND layers tend to select essential nouns and entities, while deeper layers select more abstract or syntactically critical tokens like mathematical expressions and key verbs. This suggests the model learns a natural division of labor across depth, where early layers handle entity identification and later layers handle relational/logical processing. This observation, combined with the positive correlation between token logit entropy and selection frequency (Figure 4a), provides useful evidence that the router learns semantically meaningful selection patterns rather than arbitrary ones.

## Suggestions

- Add a direct comparison with MOR on a 1B model to clearly establish DND's advantages as a post-training method.
- Provide more detailed training data specifications (sources, composition ratios, any filtering steps) to enable reproducibility.
- Run experiments with 3+ random seeds and report standard deviations, particularly for the MoE model where improvements are small.
- Include a 7B+ dense model experiment to validate scaling behavior beyond 1B parameters.

## Score and Decision

The paper presents a practical and well-engineered method for improving LLM performance through selective token reprocessing. The architecture is clean, the training strategies are well-designed and thoroughly ablated, and the token selection analysis provides genuine insight. However, the improvements are modest (especially for the MoE model), the most related work (MOR) lacks direct experimental comparison, and training data details are insufficient for reproducibility. The contribution is incremental but solid, sitting at the borderline of acceptability for a top venue.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: Reject