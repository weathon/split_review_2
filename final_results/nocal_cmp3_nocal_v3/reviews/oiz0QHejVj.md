## Summary

This paper proposes CLIP-Map, a compression framework that replaces the standard select-based pruning paradigm with learnable linear mappings for CLIP models. The method applies Kronecker-factorized matrices to compress layer width and linear combinations to compress depth, then retrains via knowledge distillation. The key technical innovation is Diagonal Inheritance Initialization, which initializes mapping matrices to identity-like transformations, mitigating optimization instability from Kronecker-structured mappings. The paper reports improvements over TinyCLIP at high compression ratios (1%–10%) with fewer training epochs.

## Strengths

- **Conceptually novel departure from pruning-based compression.** Reframing CLIP compression as a learned mapping/transformation problem rather than weight selection (Sections 3.2.2–3.2.3) is a clean break from the dominant pruning-retraining pipeline. This is not a marginal modification of existing methods.

- **Diagonal Inheritance Initialization is well-motivated and empirically decisive.** The variance analysis in Eqs. 5–8 correctly identifies the multiplicative variance issue in Kronecker-structured mappings. The ablation in Table 5 is stark: Diagonal Init achieves 28.9% IN-1K accuracy at 10% compression versus 4.9% for Xavier and 0.1% for Random. This is the difference between the method working and failing.

- **Substantial gains at extreme compression ratios.** At 1.0% compression (Table 1), CLIP-Map achieves TR@1=15.8 on MSCOCO versus TinyCLIP's 10.5 (non-progressive) and 12.5 (progressive). At 10.0% compression, gains are consistent across all retrieval metrics on both MSCOCO and Flickr30K. These are non-trivial improvements where existing methods degrade sharply.

- **Training efficiency advantage.** Total training budget is 25 epochs (5 mapping + 20 retraining) versus TinyCLIP's 50–75 epochs (2–3 progressive stages × 25 epochs each). Table 3 quantifies seen-sample counts, confirming CLIP-Map uses fewer training samples than comparable baselines.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

1. **Overstated framing of the mapping-versus-pruning distinction.** The paper repeatedly claims (Abstract, lines 9, 17–18; Contribution 1, line 33) that select-based pruning "inevitably leads to information loss" while mapping "preserves as much information...as possible" and "better preserves the full information." This is technically imprecise: the mapping operation \(W' = F^{out} W (F^{in})^T\) produces a matrix in \(\mathbb{R}^{D_2 \times D_2}\) with \(D_2 < D_1\), whose rank cannot exceed \(D_2\) — information is necessarily lost in both approaches. The real advantage is that mapping learns *which linear combinations* to retain rather than committing to a hard subset a priori, which is a genuine contribution that does not require overclaiming "information preservation." The empirical results speak for themselves without this framing.

2. **Depth compression via linear combination of layers is under-analyzed.** Equation 2 defines each new layer as a weighted average of all original layers. A transformer processes layers sequentially, but a linear combination of all original layers collapses this sequential structure into a parallel mixing step. The paper does not discuss whether the resulting network behaves qualitatively differently, whether depth compression interacts with width compression beyond the stated order of operations (Fig. 3: width first, then depth), nor does it provide an ablation isolating depth compression's effect. Without this, it is unclear whether depth compression contributes meaningfully or whether width compression alone accounts for the gains.

3. **Mixed results at moderate compression are not reflected in the headline claims.** The Abstract states "outperforms select-based frameworks across various compression ratios." At 50% compression (Table 1), CLIP-Map_base achieves TR@1=55.1 versus TinyCLIP's 54.9 (essentially a tie) and is *worse* on TR@10 (86.5 vs. 87.2), IR@1 (37.9 vs. 38.9), and consistently lower on most Flickr30K metrics. At the base scale in Table 2, results are mixed — wins on some datasets (e.g., RESISC45: 55.6 vs. 52.4) but losses on others (e.g., Oxford Pets: 48.5 vs. 80.8). The paper's strongest evidence is at high compression ratios (1%–10%). The claims should be scoped accordingly.

4. **Under-specification of how compression applies to ViT architecture components.** The method treats each layer as a monolithic \(\mathbb{R}^{D_1 \times D_1}\) matrix (Eqs. 1–4, Section 3.2.2). A ViT layer contains distinct parameter tensors: attention Q/K/V/O projections, MLP up/down projections, layer norms, and embeddings. The paper does not specify which tensors undergo width mapping, whether each tensor gets its own \(F^{in}, F^{out}\) pair, or how attention heads interact with dimension reduction. While the core idea transfers regardless, this abstraction creates a reproducibility gap for readers trying to apply the method to specific architectures.

5. **No variance or statistical significance reported.** For a comparison where many results are close (e.g., 50% compression in Table 1, various base-scale classification results in Table 2), the absence of standard deviations or multiple-seed reporting makes it impossible to assess whether the reported differences are meaningful.

6. **ResNet experiment is incomparable.** Table 1 includes a ResNet-50 row labeled "w/o Retraining" with 25.5 TR@1. The paper states (lines 273–274) that when using ResNet, retraining is not performed. Comparing this against TinyCLIP rows that include retraining is apples-to-oranges and does not support the claimed advantages.

### Trivial

None.

## Nice-to-Haves

- **Isolate depth compression via ablation.** Adding an experiment where depth compression is removed (width mapping only) would clarify whether this component contributes meaningfully or adds complexity without benefit.
- **Analyze what the mapping matrices learn.** Section 4.3 observes that mapping matrices evolve from diagonal to uniform distributions — a brief visualization or analysis of what structure the mappings discover (e.g., dimension de-emphasis, modular weight structure) would strengthen the paper without requiring new experiments.
- **Report wall-clock time.** The paper claims training efficiency via epoch counts but does not report actual training time. The mapping stage introduces additional parameters (\(F^{in}, F^{out}\) per layer) that add forward/backward cost; the practical speedup may be smaller than epoch counts suggest.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Wall-clock time comparison** — The paper references A.6 for training speed-up visualization. Since the appendix is stripped by the parser, this criticism is removed per policy.
- **Temperature λ not specified** — The paper references A.5 for detailed training settings containing hyperparameter values (λ, etc.). Removed per policy on stripped appendix content.
- **Token pruning papers not CLIP-specific** — The reviewer claimed the cited token-pruning papers (Rao et al., Bolya et al., Shi et al., Cao et al.) are "primarily unimodal" but Cao et al. (2024) is explicitly multimodal (MADTP). Removed as factually partially incorrect.
- **ViT architecture specification in main text** — The reviewer's detailed question about which tensors, attention heads, and independent compression is partially addressed by the paper's reference to Appendix A.3 Table 6. The main-text abstraction is a reasonable design choice given page limits; the core idea is unaffected. Demoted from original framing.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Scope the claims to high-compression regimes.** The paper's strongest and most consistent evidence is at 1%–10% compression ratios. Leading with "substantially outperforms at high compression, competitive at moderate compression" is more accurate and does not weaken the contribution — extreme compression is the harder regime.
2. **Add a depth-compression ablation** to isolate whether width mapping alone explains the gains.
3. **Report standard deviations** (multiple seeds) for the 50% compression comparison where results are close.
4. **Clarify architectural specification** in the method section: state how attention/MLP tensors are handled and whether text/image encoders receive independent mappings.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>