## Summary

CLIP-Map proposes a mapping-based alternative to standard select-based pruning for CLIP compression. Instead of selecting a subset of weights to keep, the method learns differentiable Kronecker-factorized transformations (F_in, F_out for width compression; L_depth for depth compression) that map large pretrained weight matrices into smaller ones, then retrains via knowledge distillation. A Diagonal Inheritance Initialization scheme initializes the mapping near identity to stabilize optimization. The method achieves strong gains over TinyCLIP at high compression ratios (1.0%, 10.0%) with fewer total training samples.

## Strengths

1. **Conceptually clean alternative to pruning.** The paper correctly identifies that pruning discards parameter information and proposes a genuine alternative — learning a differentiable transformation that compresses rather than selecting a subset. This framing is well-motivated in Sections 1 and 3 and clearly illustrated in Figure 1.

2. **Kronecker factorization makes the mapping tractable.** The parameter complexity reduction from O(D₁²D₂²) to O(D₁D₂) (Eqs. 3–4) is substantial and well-explained. Without this, the method would be computationally infeasible.

3. **Diagonal Inheritance Initialization is mathematically motivated and practically critical.** The variance analysis in Eqs. 5–8 correctly identifies why naive independent initialization fails (multiplicative variance). Table 5 shows this initialization is essential — without it, performance collapses to near-zero (0.1% vs 28.9% IN-1K after mapping stage).

4. **Clear gains at high compression ratios.** At 1.0% compression (Table 1), CLIP-Map outperforms TinyCLIP by a large margin: TR@1 15.8 vs 10.5/12.5 on MSCOCO, TR@1 30.3 vs 21.3/24.5 on Flickr30K. At 10.0% compression, consistent gains are also present.

5. **Training efficiency.** CLIP-Map achieves its results with fewer total seen samples (0.45B vs 0.75–1.125B for TinyCLIP at comparable sizes, Table 3).

## Weaknesses

### Fatal
None.

### Major

1. **Comparison set is narrow, limiting the strength of the conclusions.** The paper's headline comparisons are almost exclusively against TinyCLIP. Methods that also use differentiable/learnable mechanisms for CLIP compression (e.g., UPop, which the paper itself cites in Related Work) are not included as experimental baselines. Without comparisons to soft-mask pruning methods, it is unclear whether the observed gains at high compression stem from the *mapping* mechanism specifically or from differences in training recipe. Moreover, the "Manual Drop" baseline in Table 4 (simple subsampling + retraining achieves 41.1 IN-1K at 10% compression vs CLIP-Map's 42.1) suggests the mapping adds only ~1 point — this informative comparison is buried in an ablation rather than presented as a primary baseline.

2. **Depth compression contribution is unsubstantiated.** The paper introduces L_depth (Eq. 2) and presents depth compression as a co-equal contribution alongside width compression. Yet there is no ablation isolating the effect of depth mapping vs width mapping. The tables report only total parameter counts, so it is impossible to determine how much compression came from reducing layer count vs hidden dimensions. There is no experiment showing that learned linear combinations of layers outperform simply dropping layers. This claimed contribution is left entirely unsupported.

### Minor

3. **At moderate compression (50%), gains are marginal or mixed, yet the high-level framing implies uniform superiority.** At 50% compression (Table 1), CLIP-Map and TinyCLIP are essentially tied: on MSCOCO TR@1 55.1 vs 54.9, IR@1 37.9 vs 38.9. On Flickr30K, TinyCLIP leads on several metrics (TR@5 96.7 vs 96.2, TR@10 99.0 vs 98.5). The abstract states CLIP-Map "outperforms select-based frameworks across various compression ratios" without qualifying that the advantage is concentrated at high compression. The main text (Section 4.2) correctly calls the 50% results "competitive" — but the abstract and introduction overstate.

4. **No quantitative analysis of what the learned mapping actually does.** Table 5 shows that Mapping-stage-only performance with Diagonal init (28.9% IN-1K) is much closer to the fully-trained result (42.1%) than to alternatives (0.1–4.9% from random/Kaiming/Xavier init). The paper qualitatively states (Appendix A.7) that the mapping evolves "from an initial diagonal pattern toward a more uniform structure" but provides no quantitative evidence — e.g., Frobenius norm of off-diagonal vs diagonal elements, distance from identity. If the final F matrices remain near-identity, the mechanism is closer to a learned weighted average than to the "full information preservation" narrative claimed in the paper.

5. **Claim of "simplified pipeline" / "less engineering complexity" is unsubstantiated.** Contribution 2 states the pipeline has "less engineering complexity," but the retraining stage (Section 3.2.4) uses standard CLIP knowledge distillation (InfoNCE + cross-entropy with teacher logits) — the same loss as TinyCLIP and CLIP-KD. Meanwhile, CLIP-Map adds new learnable parameters (F_in, F_out, L_depth) and an additional training stage (mapping). The paper does not specify in what sense the pipeline is simpler.

6. **ResNet generalization results are incomplete.** The paper evaluates on ResNet-50 as vision encoder but only performs the mapping stage (5 epochs) without the retraining stage (Section 4.1). The result (25.5 TR@1 on MSCOCO, 19+19M params) is presented transparently with "w/o Retraining" annotation, but it represents only a lower bound — the full method was not applied. This weakens the claim of generalizability to non-ViT architectures.

### Trivial

7. **No variance reporting.** All results in Tables 1–5 are reported as single numbers with no indication of variance or number of seeds. For the close comparisons at 50% compression, this makes it impossible to assess whether differences are meaningful or within noise.

## Nice-to-Haves

- Include a comparison against a learnable-mask pruning method (e.g., UPop) to better isolate the effect of mapping vs selection.
- Measure feature similarity (e.g., CKA) between the mapped model and the original model vs between a pruned model and the original, to directly test the "information preservation" thesis.
- Provide quantitative analysis of the trained F matrices (e.g., Frobenius norm of off-diagonal elements, distance from identity).
- Isolate width vs depth contributions in an ablation study.

## Removed Points

- SparseGPT/Wanda baselines: these are LLM pruning methods; applying them to multimodal CLIP is outside the paper's scope. Not a fair criticism.
- "logits_{2T-1}" typo claim: this is unclear notation, not necessarily a typo. The parser may also have introduced artifacts.
- Lambda not specified in main text: the paper states it is in the appendix, which was removed by the parser. This is a known parsing issue.
- Missing comparison with progressive TinyCLIP (3×25ep) at certain settings: the paper includes progressive TinyCLIP results († symbol) appropriately in Table 1.
- Claim about "fewer training epochs" vs "fewer seen samples": the paper uses "fewer training epochs" in the introduction but supports it with total seen samples in Table 3, which is a more meaningful comparison metric.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Broaden baselines: include a learnable-mask pruning method (e.g., UPop) in the main results table. Elevate the "Manual Drop" baseline to a primary comparison.
2. Add an ablation separating width-only, depth-only, and combined mapping to substantiate the depth compression claim.
3. Include variance estimates or at minimum report the number of seeds for key results.
4. Provide quantitative analysis of trained F matrices (e.g., off-diagonal norm ratio).
5. Qualify contribution claims in the abstract to specify that the largest gains are at high compression ratios (1–10%).
6. Apply the full mapping+retraining pipeline to ResNet to properly validate generalizability, or drop the ResNet claim.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| LLM2CLIP (HfJxXbXlYJ) | 3.00 | 1 | Stronger empirical support in CLIP-Map; rejected for weak core claim |
| HyperCLIP (a4nSE2kpoq) | 4.00 | 1 | Similar CLIP-efficiency topic; weaker motivation and evidence |
| Inference Optimal VLMs (6VhDQP7WGX) | 5.80 | 1 | Similar quality: novel findings with generalization concerns |
| TempMe (lVp97zZ5i8) | 6.00 | 1 | Comparable: efficient CLIP-based retrieval, solid but incremental |
| Bridging Compressed Latents (GSUNPIw7Ad) | 6.00 | 1 | Comparable: practical contribution with clear limitations |
| SAE for CLIP (imT03YXlG2) | 6.50 | 1 | Stronger on analysis depth; comparable overall quality |

**Round 1 bracket:** 5.5 – 7.0

CLIP-Map proposes a genuinely novel approach (mapping-based ≠ selection-based compression) with strong results at high compression ratios and a well-motivated technical core. However, the narrow baseline comparison (essentially only TinyCLIP), unsubstantiated depth compression claim, and overclaiming at moderate compression prevent a higher score. The paper sits comfortably above reject-level papers (scores 3–4) and is comparable to other borderline-accept CLIP efficiency papers (scores 5.5–6.5).

**MY FINAL SCORE: <score>6.0</score>**
**MY FINAL DECISION: <decision>Accept</decision>**