## Summary

This paper proposes CLIP-Map, a mapping-based compression framework for CLIP models that replaces conventional select-based pruning (which discards "unimportant" weights) with learnable linear transformations that combine all original parameters into a compact representation. The method uses Kronecker factorization to make the mapping tractable (reducing complexity from O(D₁²D₂²) to O(D₁D₂)) and introduces a Diagonal Inheritance Initialization scheme to address optimization difficulties. Experiments on zero-shot retrieval and classification benchmarks show clear advantages over the select-based TinyCLIP baseline at high compression ratios (1–10%) with better sample efficiency.

## Strengths

1. **Novel framing of compression as learned mapping rather than selection/pruning.** The paper correctly identifies that select-based pruning discards information from parameters deemed "unimportant" and that this loss is hard to recover through retraining. Replacing selection with a learnable linear mapping that combines all original parameters into a smaller representation is a genuinely different design philosophy, and the paper is the first to apply it to multimodal models.

2. **Kronecker factorization makes the mapping tractable.** A naive full mapping matrix R_t ∈ ℝ^{D₂² × D₁²} would be prohibitively large. The factorization into F_in, F_out ∈ ℝ^{D₂ × D₁} (Eqs. 3–4) reduces complexity from O(D₁²D₂²) to O(D₁D₂). This correctly identifies and solves the right bottleneck.

3. **Diagonal Inheritance Initialization is convincingly demonstrated.** Table 5 shows that random, Kaiming, and Xavier initialization all produce near-zero performance (0.1–4.9% IN-1K accuracy) after the mapping stage, while Diagonal Inheritance Initialization achieves 28.9% — a ~6–289× improvement. The variance analysis in Eqs. 5–8 correctly explains why standard initializations fail: the Kronecker product multiplies variances, leading to distribution shift. This is well-motivated and empirically decisive.

4. **Clear gains at high compression ratios.** At 1% compression (Table 1), CLIP-Map_base (0.84M params) substantially outperforms TinyCLIP at the same size across all retrieval metrics on both MSCOCO and Flickr30K — e.g., MSCOCO TR@1: 15.8 vs. 12.5, Flickr TR@1: 30.3 vs. 24.5. The gap is large and consistent. At 10% compression, the advantage is present across most metrics.

5. **Sample efficiency.** Table 3 shows that CLIP-Map_base achieves 63.7% IN-val accuracy with 0.30B seen samples, while TinyCLIP-39M/16 achieves 63.5% with 0.75B seen samples — a 2.5× sample efficiency advantage.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **At 50% compression, the results are mixed rather than clearly superior.** The paper claims to "outperform select-based frameworks across various compression ratios." At 1% and 10% this is well-supported, but at 50% (Table 1) CLIP-Map_base is comparable to TinyCLIP on some metrics and *worse* on others (e.g., Flickr TR@1: 81.9 vs. 84.6; MSCOCO IR@1: 37.9 vs. 38.9). The paper should explicitly acknowledge this regime dependence rather than presenting "superior performance" as blanket across all compression ratios.

2. **The "fewer training epochs" claim is not quantified in the primary comparison tables.** Tables 1 and 2 annotate TinyCLIP's epoch budgets (e.g., "2×25ep", "3×25ep") but do not state CLIP-Map's corresponding totals. Table 4 implies 5+20=25 epochs for the 10% setting, but whether this same budget applies to the 1% and 50% settings in the main tables is not stated. Table 3's "seen samples" column partially addresses efficiency, but the epoch-level comparison should be explicit in the main comparison tables to substantiate the central efficiency claim.

3. **Table 5's ablation is incomplete — it only reports mapping-stage results.** The table shows that Diagonal Inheritance Initialization achieves 28.9% IN-1K vs. 0.1–4.9% for other initializations *after the mapping stage only*. The paper does not report whether the poorly-initialized baselines recover during the full retraining stage (25 epochs). If they remain near-zero, that would strengthen the case for the method; if they recover substantially, the advantage would be more about training stability than final capability. Either outcome is informative and should be reported.

4. **The comparison with TinyCLIP is thorough but narrow.** The main results (Tables 1, 2) compare almost exclusively against TinyCLIP. Table 3 includes MoPE-CLIP, CLIP-KD, ViT-T/16, and MobileCLIP, but only on IN-val accuracy rather than the retrieval or 21-dataset classification benchmarks. Demonstrating that the mapping approach beats other compression strategies (e.g., structured pruning with recovery, SparseGPT applied to CLIP) on a broader set of tasks and compression ratios would strengthen the generality of the paper's conclusions.

5. **The computational overhead of the mapping stage is not discussed.** During the mapping stage, the method stores and trains learnable mapping matrices (F_in, F_out) that, while parameter-efficient, introduce real GPU memory and compute costs. A brief quantification of total training FLOPs or wall-clock time of the two-stage pipeline versus TinyCLIP's progressive pipeline would clarify the practical trade-off. (The paper references appendix A.6 for a speed-up visualization; a main-text summary would help.)

6. **The effect of depth compression is not separately ablated.** The method includes both width compression (F_in, F_out) and depth compression (L_depth, Eq. 2), but the ablation studies (Tables 4, 5) only examine the overall pipeline. An ablation isolating the depth mapping from the width mapping would clarify whether the depth compression contributes significantly.

7. **No variance or statistical significance is reported.** Several results in Table 1 are close at 50% compression (e.g., TR@1 55.1 vs. 54.9). Without error bars or multiple seeds, it is impossible to assess whether these differences are meaningful.

### Trivial
- The value of λ in Eq. 13 (weighting between task loss and distillation loss) is not stated in the main text (presumably in the appendix).
- The off-diagonal elements in Eq. 9 are specified as exactly 0, but the text says "zero or small random values" — this minor ambiguity in the initialization scheme should be resolved.

## Nice-to-Haves
- An ablation of depth compression vs. width compression separately.
- Error bars or multiple-seed results for the main comparisons, especially at 50% compression where differences are small.
- A main-text summary of the training speed-up analysis currently in appendix A.6.

## Removed Points
- **Table 2 formatting criticism** ("difficult to parse in text format — 22 columns with many numbers"): This is a parser artifact, not an author issue. The table is correctly formatted in the PDF.
- **Architecture details deferred to appendix**: Standard practice; not a valid weakness.
- **The reviewer's confusion about "50.0 on ImageNet-1K" in Table 2**: This was a misreading caused by the text rendering. The actual value for CLIP-Map at 1% is 19.0 on ImageNet-1K, and the 50.0 entry corresponds to a different dataset column.
- **"Less engineering complexity" being debatable**: This is a framing claim that the reviewer opined on; it does not constitute a technical weakness of the paper.
- **Whether F_in/F_out are per-layer**: The text says "for the parameter block in l-th layer" (Section 3.2.2), which clearly indicates per-layer. The reviewer's uncertainty is unwarrated.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add the total training epoch count for CLIP-Map directly into the headers or captions of Tables 1 and 2 so the "fewer epochs" claim is transparent.
2. Complete the ablation in Table 5 by reporting final retrained accuracy for Random, Kaiming, and Xavier initializations after the full pipeline.
3. Add a brief paragraph quantifying the mapping stage's computational overhead (e.g., mapping parameter count, training FLOPs, wall-clock time) to help practitioners assess the practical trade-off.
4. Include explicit regime-dependent characterization: the method provides largest benefits at ≤10% compression, while at ~50% compression it is competitive rather than clearly superior.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>