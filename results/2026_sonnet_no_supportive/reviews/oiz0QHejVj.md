Now I have enough to write the draft review. Let me call `draft_review` then run calibration.Round-1 bracket: **4–6**. The paper has a real core contribution (DII, mapping-based compression with genuine extreme-compression gains) but major claim mismatch and unexplained catastrophic Table 2 failures at 50% scale — similar to calibration papers in the 4.67–5.33 range (774F8gF0UO, 9ccZzuix2D, I5S1a1NKxo).## Summary
CLIP-Map proposes a mapping-based compression pipeline for CLIP models, replacing conventional select-based (pruning) approaches with learnable Kronecker-factored width matrices (F_in, F_out) and a linear-combination depth operator (L_depth). The central enabling mechanism is Diagonal Inheritance Initialization (DII), which initializes both Kronecker factors as identity-like matrices to avoid the multiplicative variance explosion inherent to standard initializations of Kronecker products. The method consistently outperforms TinyCLIP at 1% and 10% compression ratios and achieves equivalent accuracy with 2.5× fewer seen samples at 50% compression.

---

## Strengths
- **DII ablation is conclusive and unusually clean.** Table 5 shows: Random init → 0.1% IN-1K, Kaiming → 4.4%, Xavier → 4.9%, DII → 28.9%. This is not a marginal improvement; the proposed initialization is the enabling mechanism without which mapping-based compression completely fails. The theoretical motivation (Eqs. 6–8) correctly identifies the multiplicative variance problem in Kronecker-factored initializations.

- **Strong, consistent gains at extreme compression.** At 1% and 10% compression ratios (Table 1), CLIP-Map_base beats both standard and progressive TinyCLIP on all MSCOCO and Flickr30K recall metrics. E.g., COCO TR@1: 15.8 vs 12.5 (1%); 38.4 vs 36.2 (10%). The result at 1% compression is particularly compelling because this is the regime where initialization quality most dominates retraining recovery.

- **Training efficiency concretely demonstrated.** Table 3 shows CLIP-Map_base achieves 63.7% IN-1K with 0.30B seen samples vs TinyCLIP-39M/16's 63.5% at 0.75B — a 2.5× reduction in training data processed — while matching the final score.

---

## Weaknesses

### Fatal
None.

### Major

- **50% compression results contradict the headline claim.** The abstract states "particularly significant gains observed under high compression settings," yet Table 1 at 50% shows CLIP-Map_base tied or worse vs TinyCLIP across nearly all metrics: COCO TR@1 55.1 vs 54.9 (marginal); COCO IR@1 37.9 vs 38.9 (worse); Flickr30K TR@1 81.9 vs 84.6, TR@5 96.2 vs 96.7, TR@10 98.5 vs 99.0 (all worse). The genuine gains are concentrated at 1–10% compression, but the framing implies broad superiority across all compression ratios.

- **Table 2 (ViT-39M/16, 50% compression) shows catastrophic task-specific failures with no analysis.** At this scale, the paper claims "CLIP-Map exhibits strong performance across most tasks," yet compared to TinyCLIP: STL10 drops from 93.2 to 13.0 (−80.2 pp), Oxford Pets from 80.8 to 48.5 (−32.3 pp), VOC2007 from 76.0 to 22.2 (−53.8 pp). The aggregate IN-1K number (63.7 vs 63.5) masks these severe regressions on standard benchmarks. No mechanism is proposed or even noted for why specific task families fail catastrophically.

### Minor

- **Absolute IN-1K gain from mapping initialization is modest.** Table 4: Manual Drop (0 epoch) achieves 41.1% IN-1K; 5ep mapping achieves 42.1% — a 1 pp absolute gain. COCO TR@1 shows a more meaningful gain (38.3 vs 33.8 = +4.5 pp). The paper's framing of mapping-based initialization as "fundamentally superior" to select-based initialization is overstated by the IN-1K result, though the retrieval metric provides more genuine support.

- **Comparison landscape is narrow at equivalent model sizes.** Tables 1 and 2 compare exclusively against TinyCLIP replicated by the authors. Other recent CLIP compression methods appear only in Table 3 at different scales and training configurations, preventing a direct parameter-matched comparison.

### Trivial
- Sec 3.2.3 text says "set the off-diagonal elements to zero **or small random values**" but Eq. 9 specifies exactly zero — a minor inconsistency.

---

## Nice-to-Haves
- Analysis of what learned L_depth coefficients converge to (whether they approximate diagonal layer selection or produce genuine layer blending) would validate whether depth compression is principled.
- Brief diagnostic of the STL10/Oxford Pets/VOC2007 failures at ViT-39M/16 scale — whether these are consistent across runs and what may cause them.
- Wall-clock training time or GPU-hours alongside seen-samples in Table 3 for a more complete efficiency picture.

---

## Removed Points
*These points were removed from the main review; treat them with caution.*

- **"Less engineering complexity" claim unvalidated (Harsh Critic):** Valid observation that no metric is reported, but this is a qualitative pipeline description; no formal experiment is required. Removed as trivial framing nitpick.
- **L_depth initialization not specified in main text (Harsh Critic):** Appendix was stripped by parser; removed per rules on absent appendix content.
- **Table 4 epoch-budget confound (Harsh Critic):** "7+18 degradation might reflect insufficient retraining" — speculative; the authors' conclusion (5ep optimal) is sufficiently supported by the monotonic improvement from 0→5ep and degradation at 7ep. Demoted to "addressed by design."
- **Comparison fairness with CLIP-KD/MoPE-CLIP at different scales (Harsh Critic):** These comparisons in Table 3 are at different scales; the asymmetry is not clearly in the authors' favor so the comparison is genuinely incomplete — but subsumed under the "narrow comparison landscape" Minor weakness above.

---

## Novel Insights
The paper surfaces a principled observation about Kronecker-factored linear maps: standard initializations (Kaiming, Xavier) cause the variance of the product matrix R = A ⊗ B to scale multiplicatively (Var(R) = σ_A² · σ_B²), leading to gradient instability. The DII remedy — initializing both factors to near-identity — is a sound and general principle likely applicable to any context where Kronecker-factored linear maps are jointly trained. This is a transferable insight beyond CLIP compression.

---

## Suggestions
1. Reframe the abstract and introduction to scope the gains accurately: "particularly at 1–10% compression ratios" rather than implying broad superiority at all compression levels. The honest story (extreme compression) is compelling on its own.
2. Add a brief section or paragraph analyzing the task-specific failures at ViT-39M/16 (Table 2) — identify which task families are affected and hypothesize a cause. Even a negative result documented properly strengthens the paper.
3. Include visualization of converged L_depth coefficients across experiments to validate whether the depth compression converges to principled layer selection.

---

## Score Calibration

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| I5S1a1NKxo | 5.00 | R1 | VLM distillation compression; similar scope, similar level of evaluation gaps; rejected |
| 774F8gF0UO | 4.67 | R1 | MLLM compression survey; less novel than CLIP-Map's DII contribution |
| 9ccZzuix2D | 5.33 | R1 | Data pruning + KD; cleaner claims-evidence alignment; rejected |
| LC6ZtQV6u2 | 6.50 | R1 | Foundation model distillation at ImageNet cost; stronger eval breadth; accepted |
| iIT02bAKzv | 5.50 | R2 | VLM pruning (ECoFLaP); more comprehensive evaluation; accepted |
| pAVJKp3Dvn | 5.67 | R2 | Differentiable structured matrices; strong theory+practice; accepted |
| z9UBpl4pv5 | 4.33 | R2 | Structured initialization for ViT; narrower contribution; rejected |
| KksPo0zXId | 5.00 | R2 | Post-training structured pruning; comparable scope; rejected |

**Round 1 bracket:** 4–6  
**Round 2 narrowing:** Papers with genuine novel contributions + real empirical gains but significant presentation mismatches and unexplained experimental failures cluster at 5.0–5.5. CLIP-Map's DII ablation is cleaner than most papers in the 5.0 range, but the catastrophic Table 2 failures and overclaimed abstract pull it below papers like iIT02bAKzv (5.5) that have more honest scoping. Final placement: **5.0**.

---

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>