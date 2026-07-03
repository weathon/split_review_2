Now I have all the information I need. Let me produce the final consolidated review.

## Summary

This paper introduces TNT, a two-stage training paradigm for deep memory modules (RNNs with test-time learned fast weights, e.g., Titans). Stage 1 uses a hierarchical memory: a global module with large chunks for throughput, plus multiple parallel local modules with periodic state resets to enable context parallelism. A Q-K projection addresses a compression-retrieval domain mismatch. Stage 2 is a brief fine-tuning with smaller chunk sizes to optimize inference. Evaluated on Titans at 150M scale, TNT achieves up to 17× training speedup over the most accurate baseline while matching or improving perplexity.

## Strengths

1. **Periodic state reset for context parallelism in non-linear RNNs** (Section 4.1.1, Eq. 6): Resetting local memory states to a shared learned initial state at shard boundaries breaks sequential dependency, enabling true context parallelism for models with non-linear recurrences (LayerNorm, deep update rules) that cannot use parallel scans. This is a genuinely novel solution to a well-known bottleneck — prior work on parallelizing RNNs has largely been limited to linear state transitions.

2. **Empirical demonstration of decoupling training speed from accuracy**: Table 1 (time-to-quality) shows TNT reaches target loss **17.37× faster** than the most accurate Titans baseline (C=8: 1.12 hrs vs. 19.48 hrs) while simultaneously achieving higher quality in Table 2 (23.13 vs. 25.07 avg. PPL). Even at the same chunk size (C_L=C=8), TNT is 7.68× faster, demonstrating that the speedup is not solely an artifact of using larger chunks.

3. **Q-K Projection with clean ablation evidence** (Section 4.1.2, Table 3): The paper identifies a principled problem — compression optimizes f(W, k)→v but retrieval inputs q instead of k — and the ablation shows removing Q-K projection degrades perplexity from 21.04→22.01 and commonsense accuracy from 40.6%→36.4%, cleanly isolating this mechanism's contribution.

4. **Informativeness of the ablation study**: Table 3 systematically ablates each component (global memory, Q-K projection, number of local modules, Stage 2), making it clear what each design choice contributes. This is good experimental practice.

## Weaknesses

### Major

1. **Comparison between TNT and Titans conflates training paradigm with architectural changes** (Tables 1, 2, 3). TNT replaces a single deep memory module (Titans baseline) with 1 global + N local modules, each a full sub-network with its own fast weights. Both are reported as "150M parameters" but the paper provides no explanation of how parameters are redistributed (e.g., smaller hidden dimensions per module) and no ablation controlling for parameter count, FLOPs per step, or total compute budget. A matched-capacity baseline — a single-module model with equivalent parameters — is absent. Consequently, the headline accuracy improvements (23.13 vs. 25.07 PPL) cannot be cleanly attributed to the TNT _training paradigm_ versus the added model capacity from the hierarchical architecture itself. Even the speed comparison (Table 1) partially confounds architecture (parallel global+local modules) with training method (periodic resets).

2. **No evidence that TNT generalizes beyond Titans.** The abstract states "Evaluated on Titans and TTT models," but the experiments (Section 5) only instantiate TNT on Titans. TTT appears solely as a baseline (one row in Table 2, achieving 27.62 PPL). The contributions page more cautiously says "We validate TNT on the Titans architecture," but the paper's framing as a "general training paradigm applicable to any deep memory module" (Section 1) remains entirely unsupported. A single data point on one architecture does not establish generality.

3. **No error bars, confidence intervals, or statistical significance anywhere in the paper.** Every result — perplexity, commonsense accuracy, runtime — is reported as a point estimate. The paper itself acknowledges that downstream task accuracy "can be subject to higher variance" (Section 5.3), yet reports a single run. Many reported differences are small enough to fall within noise (e.g., Stage 2 improvement from 23.13 to 23.09 PPL; 41.0% vs. 39.7% accuracy against Gated Transformer). Without variance information, the reliability of these comparisons is unclear.

### Minor

4. **Stage 2 fine-tuning improvements are marginal relative to the claim of resolving Challenge 3 (chunksize mismatch).** The best Stage 2 result (23.09 PPL) improves over the best Stage 1 result (23.13 PPL) by only 0.04 PPL. For the 1-local configuration, Stage 2 improves from 21.04 to 20.86 PPL (0.18 gain). While Stage 2 is cheap (5% additional compute), the tiny improvement magnitude provides weak evidence that it "solves" the chunksize mismatch problem. The paper should compare Stage 2 fine-tuning against simply training from scratch with small chunks at equivalent compute.

5. **Q-K Projection operates over a limited context (within-chunk keys only).** Equation 7 projects q onto the subspace of keys seen within the current local chunk only (summation bounds ξ(t, C_L) to t). The paper frames this as projecting "onto the subspace spanned by previously observed keys," which is technically true but the available subspace is far more restricted than the full history. The paper does not discuss this limitation or ablate the effect of projection context size.

6. **Abstract overclaims experimental scope.** The abstract says "Evaluated on Titans and TTT models" (line 9), which suggests TNT was applied to both architectures. In reality, only Titans is used as the TNT base model; TTT is a baseline. This should be corrected.

### Trivial

7. **Experimental configurations differ between speed and quality benchmarks without stated rationale** (Section 5.1): S_L=2048 for efficiency benchmarks but S_L=4096 for performance evaluation. The reason for this discrepancy is not explained.

## Nice-to-Haves

- Report error bars or confidence intervals, especially for perplexity and downstream accuracy.
- Provide a controlled comparison: train a single-module model at the same parameter count with TNT-style training versus standard chunkwise training, holding architecture fixed.
- Validate TNT on a second deep memory architecture (TTT or Atlas) to substantiate the generality claim.
- Study sensitivity to the local window size S_L (currently just two fixed values).
- Discuss the within-chunk limitation of Q-K Projection and ablate the projection context size.

## Removed Points

These points were raised in reviews but removed after verification against the paper:

1. **"Periodic reset is actively harmful without global memory"** (Harsh Critic Critical Issue 2): The paper already acknowledges this trade-off explicitly in Section 5.4: "removing the global memory is detrimental (PPL increases to 25.60), confirming its critical role in capturing long-range dependencies that are otherwise lost due to the local memories' reset mechanism." This is a transparent discussion of the design's limitation, not a hidden weakness. **Removed — already addressed by paper.**

2. **"Challenge 2 framing as 'fundamental inconsistency' is overstated"**: Whether the compression-retrieval mismatch warrants the term "fundamental inconsistency" is a subjective framing judgment, not a technical flaw. The paper provides empirical evidence (Table 3 ablation) that the mismatch causes measurable degradation. **Removed — subjective framing criticism.**

3. **Missing operational details about W_init (shared across modules? how learned?)**: The paper states W_init is "shared, learnable" (Section 4.1.1). Specifics about joint training are standard implementation details appropriate for the appendix. **Removed — trivial implementation detail.**

4. **"TNT is slower than FlashAttention at short sequences"**: The paper acknowledges this — "our implementation does not yet outperform highly optimized baselines like the Gated Transformer with FlashAttention" (Section 5.2). The crossover point where TNT becomes faster is discussed transparently. **Removed — already addressed by paper.**

5. **Formatting, style nitpicks, and requests for content in stripped appendices**: These are parser artifacts or out-of-scope criticisms. **Removed per filtering rules.**

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Run a controlled architecture experiment**: Take a single-memory-module Titans model at the same parameter count. Train it with standard chunkwise training, then with TNT's periodic reset mechanism (without adding global or additional local modules). This would isolate the effect of the training paradigm from the effect of added model capacity, resolving the paper's most significant weakness.

2. **Add error bars** for the main perplexity and accuracy results in Table 2 — at minimum, report results over multiple seeds or use bootstrap confidence intervals.

3. **Correct the abstract** to accurately reflect that TNT was validated on Titans, not on "Titans and TTT models."

4. **Validate on at least one additional architecture** (TTT or Atlas) to support the claim of being a "general training paradigm."

5. **Discuss the within-chunk limitation** of Q-K Projection and ablate how performance changes with different projection context sizes.

## Score and Decision

This paper makes a genuine contribution — the periodic reset mechanism for enabling context parallelism in non-linear deep memory modules is novel, well-motivated, and backed by impressive speedup results. However, the evaluation has a significant confound: TNT changes both the training method _and_ the architecture simultaneously (adding global + multiple local modules versus a single-module Titans baseline). This makes the central accuracy claims uninterpretable — we cannot tell how much comes from the training paradigm versus the added model capacity. Additionally, the paper lacks any error bars, generalizes to only one architecture despite claiming generality, and overclaims in the abstract. These are fixable issues, but they are substantial enough that the paper in its current form does not reliably support its claims. A revised version with controlled comparisons, error bars, and second-architecture validation would be a meaningful contribution.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>