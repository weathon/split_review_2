The calibration tool has a persistent error. I will proceed with my assessment without it, drawing on my expertise.

Let me finalize the review.

## Summary

This paper proposes CLIP-Map, a parameter-efficient CLIP compression framework that replaces the standard "select-based" pruning paradigm with a "mapping-based" approach. Instead of heuristically selecting a subset of weights to keep, CLIP-Map learns Kronecker-factorized mapping matrices (F_in, F_out) that transform pretrained weight matrices into smaller compressed ones via bilinear projection (W' = F_out @ W @ F_in^T). Depth compression is handled via learnable linear combinations of layers. The mapping matrices are optimized with the original CLIP model frozen, and the resulting compressed weights serve as initialization for a knowledge distillation retraining stage. The key technical contribution is Diagonal Inheritance Initialization, which initializes the mapping matrices as near-identity to avoid the multiplicative variance explosion that arises from naive independent initialization of Kronecker factors. Experiments across multiple CLIP backbones, compression ratios (1%-50%), and benchmarks show consistent improvements over TinyCLIP baselines, with the largest gains at extreme compression ratios.

## Strengths

1. **Substantial and consistent empirical gains at aggressive compression ratios.** At 1.0% compression (Table 1), CLIP-Map_tiny achieves 15.8 TR@1 on MSCOCO vs. 10.5 for the standard TinyCLIP baseline and 12.5 for the progressive (3×25ep) TinyCLIP — a 26–50% relative improvement. At 10% compression, CLIP-Map_small (38.4 TR@1) similarly outperforms both standard (33.8) and progressive (36.2) TinyCLIP. These gains are consistent across MSCOCO and Flickr30K and across all recall metrics.

2. **Diagonal Inheritance Initialization is well-motivated and empirically critical.** Section 3.2.3 mathematically diagnoses (Eqs. 5–8) that independent initialization of Kronecker factors produces multiplicative variance (Var(R) = σ²_A · σ²_B), causing training instability. Table 5 confirms this empirically: Diagonal Init achieves 28.9% IN-1K accuracy, while Xavier (4.9%), Kaiming (4.4%), and Random (0.1%) all effectively fail. This demonstrates the initialization is not just helpful but essential to the method's viability.

3. **Kronecker factorization makes the mapping computationally practical.** The full mapping matrix R_t would have O(D1²D2²) parameters — larger than the compressed model itself at typical ratios. The factorization into F_in, F_out ∈ ℝ^{D2×D1} (Eqs. 3–4) reduces this to O(D1D2), making the approach feasible. The resulting mapping introduces negligible parameter overhead during training.

4. **Training efficiency advantage.** CLIP-Map consistently requires fewer seen training samples than comparable methods (Table 3): CLIP-Map_base (0.30B samples) achieves 63.7 IN-val vs. TinyCLIP-39M/16's 63.5 using 0.75B samples (2.5× more). This is supported by the ablation in Table 4 which controls for total training epochs and shows mapping initialization provides a clear benefit.

5. **Generalization across multiple CLIP architectures.** The method is validated on OpenCLIP-ViT-B/16, Meta-CLIP, and ResNet-50 vision encoder, showing the approach is not architecture-specific.

## Weaknesses

### Fatal
None.

### Major
- **The conceptual framing overstates the distinction from pruning.** The paper repeatedly contrasts "mapping-based" (information-preserving) vs. "select-based" (information-destructive) compression. However, the learned projection W' = F_out @ W @ F_in^T is still a lossy transformation — information is inevitably lost when projecting from D1² to D2² parameters. The real advantage is that the mapping is *optimized* rather than heuristically defined, not that it avoids information loss. The paper's results at 50% compression (essentially tied with TinyCLIP: 55.1 vs. 54.9 TR@1) are consistent with the interpretation that the mapping provides a better *initialization* for retraining rather than fundamentally preserving more information. The framing should be adjusted to match what the method actually delivers.

- **No statistical significance or variance reporting.** All results are reported as single runs without error bars or multiple-trial statistics. Given that several improvements are modest (e.g., 55.1 vs. 54.9 TR@1 at 50% compression on MSCOCO, or the ~1-point gain on IN-1K from mapping initialization in Table 4's Manual Drop comparison), the reader cannot assess whether these differences are reliable or within run-to-run noise. While single-run reporting is common in the model compression literature, the most marginal comparisons would benefit from variance estimates.

### Minor
- **Training epoch specification is incomplete for some configurations.** The ablation (Table 4) clearly specifies the 5+20 schedule for the 10% compression case with the small model variant, but the main results (Table 1) do not state the exact training schedule used for the 50% compression (CLIP-Map_base) or Meta-CLIP variants. While one can reasonably assume a similar schedule, the reader should not have to infer this.

- **The Kronecker factorization imposes a structural assumption that is not discussed.** Eq. 4 enforces that the compression is separable — the mapping applies independent linear reductions in the input and output dimensions. Not all linear maps from ℝ^{D1×D1} to ℝ^{D2×D2} can be expressed as a single Kronecker product. The paper does not discuss whether this expressivity limitation might be suboptimal for different types of weight matrices (Q/K/V/O projections, MLP up/down projections) that may have different spectral properties. This does not invalidate the method but is a notable omission.

### Trivial
- The "ResNet-50 w/o Retraining" row in Table 1 (19+19M, 25.5 TR@1) is visually confusing in its placement — it is listed under the 50% compression section but uses a different architecture (ResNet vs. ViT) and does not undergo retraining, making it not directly comparable to adjacent rows. A footnote or separate table placement would improve clarity.

## Nice-to-Haves
- A controlled comparison against SVD-based initialization (truncated SVD of each weight matrix as the compressed initialization) would help isolate whether the gains come from the *learned optimization* of the mapping or simply from using any structured low-rank projection.
- Feature-level distillation (in addition to logit-level) could potentially further improve performance and would make the comparison with methods like CLIP-KD more direct.

## Removed Points

**Criticism about training budget confound (Harsh Critic Point 2):** Removed. The ablation in Table 4 explicitly controls for total training epochs (all configurations sum to 25 total epochs: 0+25, 1+24, 3+22, 5+20, 7+18). The claim that the comparison conflates initialization with training budget is factually incorrect given this controlled experiment.

**Criticism about joint width/depth compression not being specified:** Removed. The paper explicitly states in the Fig. 3 caption: "We firstly perform width-compression in both input-dimension and output-dimension on each layers parameter blocks. Then, we perform depth-compression to linear combining the compressed parameter blocks to a new layer parameter block." The sequential nature is clearly described.

**Criticism about missing feature-level distillation creating unfair comparison:** Removed. The paper's comparison is against its own replication of the official TinyCLIP pipeline. Using a simpler distillation scheme (logit-only) makes the comparison conservative — it disadvantages CLIP-Map relative to methods that include additional distillation terms, so it does not threaten the paper's conclusions.

**Criticism about "less engineering complexity" being unsupported:** Removed. This is a reasonable claim — a unified end-to-end differentiable pipeline objectively avoids the need for handcrafted pruning schedules and progressive multi-stage compression, which is a meaningful engineering simplification.

**Criticism about ViT-T/16 comparison in Table 3 not being informative:** Removed. While ViT-T/16 uses different training data (CC3M+CC12M), it serves as a useful reference point showing competitive performance. The paper does not claim an apples-to-apples comparison.

**Strength: "This paper addressed an important problem":** Removed as generic.

**Strength: General importance of initialization:** Removed — this is a generic observation, not a specific strength of this paper.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's observation that the method is effectively a learned initialization scheme reframes rather than contradicts the paper's own description (the paper is transparent: "CLIP-Map first acquires a better initialization of compressed model using learnable mappings, and then retrain"). The key insight that is genuinely interesting is that the model-growth literature's mapping approach can be inverted for compression with a carefully designed initialization to make optimization feasible — but this is the paper's own contribution, not a novel synthesis by the reviewers.

## Suggestions

1. **Adjust the framing** in the abstract, introduction, and contributions to describe the method as a *learned initialization* for compressed models rather than an "information-preserving" alternative to pruning. The empirical advantage is in the quality of the learned transformation, not in avoiding information loss (which is mathematically impossible at these compression ratios).
2. **Add error bars or multiple-run statistics** for at least the key comparisons where improvements are modest (50% compression results, Table 4).
3. **Specify the exact training schedules** for all model variants (especially CLIP-Map_base at 50% compression) in the main text or in a clearly referenced table.
4. **Discuss the Kronecker factorization's expressivity** — acknowledge that the separable structure (independent input/output dimension reduction) is a constraint, and briefly justify why it is reasonable for CLIP's transformer weight matrices.

## Score and Decision

Based on my assessment, this paper presents a genuinely novel approach to CLIP compression with a well-motivated initialization scheme and strong empirical results, especially at aggressive compression ratios. The method is clean, the ablation studies are informative, and the evaluation is thorough. The main weaknesses are presentational (overclaimed framing) and evidential (lack of error bars for marginal comparisons), neither of which threatens the core contribution.

I calibrate this as a clear accept: the idea of applying learned mapping (from model growth) to model compression is novel; the Diagonal Inheritance Initialization is technically sound and empirically critical; the results at 1% and 10% compression are strong; and the paper is largely well-written. The framing adjustment and variance reporting are addressable in a revision.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>