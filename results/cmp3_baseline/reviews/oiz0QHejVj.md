## Summary

The paper proposes **CLIP-Map**, a mapping-based compression framework for CLIP models that replaces traditional select-based pruning with learnable transformation matrices. It uses Kronecker-factorized width compression and linear depth combination to map pretrained weights into a smaller network, and introduces a **Diagonal Inheritance Initialization** to stabilize optimization and preserve weight inheritance. The method follows a two-stage pipeline: first learning the mapping parameters with a frozen teacher, then retraining the compressed model with knowledge distillation. Experiments show that CLIP-Map consistently outperforms select-based baselines such as TinyCLIP, especially at high compression ratios (1% and 10%), while using fewer training samples.

## Strengths

- **Novel formulation for compression**: Reframing CLIP compression as a learnable mapping problem (rather than subset selection) is a principled and underexplored direction. The use of Kronecker factorization to reduce the mapping parameter count from \(\mathcal{O}(D_1^2 D_2^2)\) to \(\mathcal{O}(D_1 D_2)\) is clever and practically important.
- **Diagonal Inheritance Initialization** effectively addresses the distribution shifting problem that arises from naïve Kronecker factor initialization, and demonstrably stabilises early training (Table 5 shows a jump from 4.9% to 28.9% IN-1K accuracy compared to Xavier init).
- **Strong empirical gains under extreme compression**: At 1.0% and 10.0% compression ratios, CLIP-Map outperforms TinyCLIP by sizable margins (e.g., +5.3 TR@1 on MSCOCO at 1.0% compression), and requires fewer total seen training samples than progressive pruning baselines.
- **Clean two-stage pipeline**: The mapping + retraining design is conceptually simple, reduces engineering complexity compared to multi-stage progressive pruning, and is shown to be effective across multiple CLIP variants (OpenCLIP, Meta-CLIP, ResNet backbone).

## Weaknesses

### Major

1. **Limited controlled comparisons**: The paper compares extensively with TinyCLIP but does not provide a direct controlled comparison with other competitive compression methods (e.g., CLIP-KD, MoPE-CLIP) using the same base model, same training data, and same architecture. Table 3 mixes different backbones, training sets, and sample counts, making it hard to isolate the benefit of the mapping approach. For a method paper, such comparisons are essential.
2. **No statistical significance or variability reported**: All results appear as single runs without standard deviations or confidence intervals. Given the stochastic nature of training and the relatively modest gains at moderate compression (50%), it is unclear whether the improvements are statistically robust.
3. **Incomplete ablation of the mapping design**: The paper does not ablate the contribution of width vs. depth mapping separately, nor does it compare Kronecker-based full mapping against a simpler baseline (e.g., only diagonal inheritance without learnable off-diagonals, or a smaller linear projection). This leaves ambiguity about which component drives the improvement.
4. **Potential overfitting concern**: Table 4 shows that extending the mapping stage beyond 5 epochs degrades performance. The paper attributes this to "introducing unnecessary computational overhead," but it could indicate that the mapping overfits to the frozen teacher parameters. A deeper analysis of this phenomenon is needed.

### Minor

- The notation in Eq. 1 uses a large mapping matrix \(R_t\), but the method never constructs it explicitly. The paper could clarify earlier that Kronecker parametrization is used to avoid this explicit construction.
- Some claims about "less engineering complexity" are not substantiated; the mapping stage still requires careful hyperparameter tuning and introduces additional training steps.
- The figures (especially Figure 2) have captions that are not fully self-contained and contain redundant text, but this does not affect technical quality.

## Nice-to-Haves

- An ablation that compares full Kronecker mapping against a simpler linear layer (e.g., a single low-rank matrix) would help isolate the benefit of the structured parameterization.
- Reporting results with multiple random seeds or a bootstrap analysis would strengthen the empirical conclusions.
- A brief analysis of the learned mapping matrices (e.g., whether off-diagonal entries are indeed non-zero and meaningful) would provide insight into what the mapping stage actually learns.

## Novel Insights

Beyond the paper’s own contributions, the observation that a Kronecker-structured mapping can be initialized as an identity-like transformation (via diagonal inheritance) to avoid variance explosion is a useful recipe for any neural network compression or growth task that uses factorized mappings. The analysis of multiplicative variance growth (Eq. 8) provides a clear mathematical justification for why standard initializations fail, and the proposed diagonal initialization directly counteracts that.

## Suggestions

- Include controlled comparisons with CLIP-KD and MoPE-CLIP using OpenCLIP-ViT-B/16 as the common teacher, trained on the same data (YFCC-15M) for a fair head-to-head.
- Report results averaged over at least 3 seeds with standard deviations.
- Perform an ablation that separates the contributions of width mapping, depth mapping, and the diagonal initialization in a factorial design.

## Score and Decision

**Score**: 6.5  
**Decision**: Accept

The paper introduces a genuinely novel perspective on CLIP compression with a technically sound method, strong empirical gains at high compression, and a clever initialization scheme. The weaknesses (limited comparisons, lack of statistical rigor, incomplete ablation) are significant but not fatal—they can be addressed in a revision or discussion. The contribution is above the typical ICLR borderline and warrants acceptance.

MY FINAL SCORE: <score>6.5</score>  
MY FINAL DECISION: <decision>Accept</decision>