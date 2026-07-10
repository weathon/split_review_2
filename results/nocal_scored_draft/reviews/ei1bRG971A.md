Now I have all the information I need. Let me produce the final review.

## Summary

This paper introduces Dynamic Nested Depth (DND), a post-training method that adaptively selects "critical" tokens (via a learned router + threshold) and reprocesses them through the same transformer layer using weight sharing. The router is trained with a dual-objective loss (entropy-based dispersion + MSE-based distribution preservation) and a threshold control scheme using buffer proportional control with EMA synchronization. DND is validated on three dense 1B-class models and a 30B MoE model, showing consistent gains across general knowledge, math/STEM, and coding/agent benchmarks with minimal parameter/FLOPs increase.

## Strengths

- **Clear, well-motivated idea (Sections 1, 3.1).** The observation that prediction difficulty varies across tokens is well-supported, and the proposed response — selectively deepening computation for critical tokens via weight-shared reprocessing — is a natural next step in token-level adaptive computation that keeps parameter overhead near zero. The connection to latent reasoning strategies is coherently drawn.

- **Thoughtful training strategy design (Section 3.2).** The dual-objective router loss (score dispersion via entropy maximization + distribution preservation via MSE pull toward 0.5) addresses a genuine challenge in token-choice routing. The buffer proportional control + EMA synchronization for threshold adjustment is carefully motivated and convincingly demonstrated in Figures 5 and 6. These are non-trivial engineering contributions.

- **Thorough ablation study (Table 4).** The ablation cleanly disentangles the contributions of router controlling loss, threshold control, selection ratio (10%/20%/30%), and layer placement (L_s:L_e), showing that their combination yields the best result. This is the strongest part of the experimental section.

- **Consistent positive results across diverse models and benchmarks.** DND improves performance on all four model scales tested (three dense 1B-class models and a 30B MoE). Gains appear across general knowledge, math/STEM, and coding/agent tasks (Tables 1, 2), not concentrated in a single domain. The per-benchmark breakdown supports the method's generality.

## Weaknesses

### Fatal
None.

### Major

- **Missing uniform-compute control baseline.** The paper's core motivation (line 19: *"Instead of uniformly applying extra recurrent depth to all tokens, we dynamically select..."*) explicitly contrasts selective deepening with uniform deepening, yet no experiment tests whether the same FLOPs increase applied uniformly yields comparable, worse, or better gains. DND adds ~6% FLOPs on the 30B MoE model and yields +0.87 average, but without a control that distributes the same compute uniformly (e.g., an extra forward pass for all tokens scaled to match the FLOPs budget), the improvement cannot be attributed to the selectivity mechanism. This directly affects the interpretation of the paper's central claim.

- **Limited baseline comparisons.** Only one related method (ITT) is compared experimentally, and it achieves essentially zero improvement (+0.05 on Qwen3-1.7B). The paper's explanation — that ITT's Top-P-based selection mismatches auto-regressive inference — is reasonable, but this leaves the evaluation without a strong contemporary baseline. The paper acknowledges MOR requires pretraining from scratch (a reasonable exclusion), but does not test simpler alternatives (e.g., attention-based importance scoring or a learned gating mechanism). The uniform-compute baseline above would partially address this concern.

### Minor

- **Small gains on the 30B MoE model without variance estimates.** Many individual benchmark gains on Qwen3-30B-A3B are very small (e.g., +0.13 on BBH, +0.15 on MATH, +0.20 on MATH-500, +0.37 on CMMLU, +0.50 on MMLU). These are reported as single runs without confidence intervals or error bars. While single-run evaluation is common for large-scale LLM evaluations, the magnitude of these gains is small enough that noise could affect interpretation. Reporting variance estimates on key benchmarks would strengthen confidence.

- **Training data description is vague for reproducibility (lines 199–200).** The data is described only as *"a significant volume of synthetic material built upon a high-quality seed set of 1-2 million instances curated from human annotations and open-source materials."* Which specific datasets and synthetic data procedures were used is not stated, making the experiments difficult to reproduce.

### Trivial

- The β parameter in the fusion equation (Eq. 4) is described as "a learnable parameter" (line 106) without specifying whether it is global, layer-specific, or token-specific. Clarifying this would help.

- The qualitative visualization in Figure 7b is a single example from GPQA; a systematic evaluation across multiple examples would better support the claimed hierarchical processing observation.

## Nice-to-Haves

- Reporting throughput for the dense 1B models would give a more complete compute-performance picture.
- An ablation of the training strategy on the 30B MoE model (not just Qwen3-1.7B) would strengthen scaling claims.

## Removed Points (filtered from inputs, treat with caution)

- *Layer selection for the 30B model not stated explicitly.* The paper does state this (line 253): *"keeping about four layers at both the beginning and the end yielded the best performance. This configuration was retained in the DND experiments on Qwen3-30B-A3B."* 
- *L_sd and L_dp losses may be redundant.* This is speculative; the paper clearly motivates them for different purposes (dispersion vs. gradient preservation) operating on different normalization regimes, with no evidence provided that they are redundant.
- *Demand for dense model throughput.* Reasonable as a nice-to-have addition, not a weakness.
- *Criticisms about missing appendix content.* The appendix is removed by the parser; the original submission contains it.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add a uniform-compute control baseline.** For the Qwen3-30B-A3B model where DND adds ~6% FLOPs, compare against a version where the same FLOPs budget is distributed uniformly (e.g., an extra forward pass through the same layer for all tokens, scaled to match the FLOPs increase). This directly tests whether selectivity drives the gains. This is the single highest-leverage improvement.

2. **Report main results with variance estimates.** Even 2–3 seeds on a subset of key benchmarks (MMLU, GSM8K, HumanEval, BFCL) would substantially increase confidence in the results.

3. **Provide specific training data composition details** (dataset names, synthetic data generation procedure) to support reproducibility.

4. **Clarify whether β in Eq. 4 is global, layer-specific, or token-specific.**

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>