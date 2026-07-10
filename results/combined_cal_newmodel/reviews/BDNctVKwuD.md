Now I have all the evidence I need. Let me write the final consolidated review.

## Summary

This paper identifies a non-trivial theoretical limitation of HiResCAM explanations: they are not uniquely determined because softmax is invariant to constant shifts, which propagates to an arbitrary per-spatial-location matrix shift M across all class explanations (Theorem 3.2). To remove this redundancy, the authors propose ContrastiveCAMs — contrastive differences between HiResCAMs — that are M-invariant (Theorem 3.5). Using ContrastiveCAMs, they decompose cross-entropy into core and non-core contributions (Proposition 4.2) and derive Core-Focused Cross-Entropy (CFCE), a loss that suppresses non-core regions during training. Experiments on Hard-ImageNet show dramatic improvements in feature alignment (ContrastiveCAM IoU rising from ~30% to ~93%) and the benefits transfer to downstream segmentation.

## Strengths

- **Theorem 3.2 identifies a genuine, non-trivial limitation of HiResCAMs.** The observation that they are not uniquely determined because softmax is invariant to constant shifts (Proposition 3.1), and that this propagates to a per-spatial-location matrix shift M across all class explanations, is correct and previously unarticulated. This is a clean theoretical result. [favorability=11.74]

- **ContrastiveCAMs (Definitions 3.3, 3.4) are a simple, principled fix.** Subtracting HiResCAMs across classes removes the spurious M (Theorem 3.5), and the reconstruction formula recovers single-class interpretations. The approach follows directly from the identified problem with no ad-hoc assumptions. [favorability=10.85]

- **Proposition 4.2 / Remark 4.3 provides a clean theoretical decomposition of cross-entropy into core and non-core contributions using ContrastiveCAMs**, giving the derivation of CFCE a clear justification. [favorability=11.42]

- **The Hard-ImageNet results (Table 2) are genuinely striking.** Models trained with CFCE show core-ablation accuracy dropping from ~76% (CE) to ~32-37%, while ContrastiveCAM IoU reaches 89-93%. These represent a fundamentally different behavior where the model has largely stopped relying on non-core regions. [favorability=12.29]

- **The downstream segmentation benefit (Section 5.3) provides out-of-distribution validation** that the feature alignment is real and not merely overfitting to the masks, since better backbone features transfer to a different task. [favorability=11.53]

## Weaknesses

### Major

- **Proposition 4.1 is oversold in the text.** The paper claims (lines 158-159) that any input-dependent change to probability predictions is "precisely reflected by a proportionate change to ContrastiveCAMs." However, Proposition 4.1 as stated only shows that softmax probabilities are a *function* of ContrastiveCAMs (Equation 11) — a static identity. The relationship involves exponentials and sums, so the word "proportionate" implying linear/monotonic proportionality is not established. The proposition itself is correct, but the framing goes beyond what is proven. [favorability=2.55]

- **The faithfulness claims for ContrastiveCAMs are stated more strongly than the evidence supports.** The paper claims ContrastiveCAMs provide "faithful attention maps" (abstract) and "faithful attention maps at the class probability level" (line 99). The theoretical justification (M-invariance + Proposition 4.1) shows that ContrastiveCAMs are *uniquely determined* by class probabilities — it does not demonstrate that the maps accurately reflect the features the model actually relies on for its predictions. Standard faithfulness evaluations (deletion/insertion or causal importance metrics) are absent. The paper's evaluation measures IoU with human-annotated core masks, which is alignment with human annotations, not faithfulness to model internals. The paper should either add faithfulness evaluations or recalibrate its claims to "non-arbitrary" or "uniquely determined." [favorability=-0.32 aggregated; individual sub-items range from -2.30 to 2.91]

### Minor

- **The accuracy trade-off on Hard-ImageNet is acknowledged but not analyzed.** Unablated accuracy drops from 94.25% (CE) to 90.53% (CFCE) — ~4 percentage points (Table 2). On Oxford Pets, there is essentially no drop (99.40% vs 99.32%), yet this discrepancy is not discussed. The paper should investigate whether this reflects a genuine Pareto trade-off or is recoverable with tuning. [favorability=0.88]

- **The KL regularization results are inconsistent across settings without discussion.** On Oxford Pets with GT masks, KL adds ~10% IoU (82.92% → 92.72%). With SAM-generated masks, KL slightly hurts IoU (83.95% → 83.54%). The paper warns that KL should not be used with bounding boxes but does not explain why it helps with GT masks and hurts with SAM masks. Hyperparameters λ₁, λ₂, λ₃ in Eq. (18) are not specified. [favorability=1.19 aggregated]

- **The experiments focus exclusively on ResNet-50.** Showing results on at least one other architecture (e.g., ConvNeXt, a ViT variant, or DenseNet) would strengthen claims of generality. [favorability=-0.74]

### Trivial

- **The absolute value in the non-core penalty term of CFCE (Eq. 15)** treats negative ContrastiveCAM values (evidence *against* class c_t relative to c') equivalently to positive ones. This design choice is not motivated or discussed. A negative value in a non-core region means the region provides evidence for class c' over c_t; suppressing it may be counterproductive in some settings. [favorability=1.35]

## Nice-to-Haves

- The paper could include standard faithfulness evaluations (deletion/insertion or ROAR) for ContrastiveCAMs to directly support the "faithful" framing, though this would require significant additional experiments.
- An ablation comparing CFCE against a version using non-invariant CAMs (e.g., GradCAM) would clarify whether M-invariance is practically essential or merely theoretically nice.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **"The connection between ContrastiveCAMs and CFCE is weaker than claimed"** — REMOVED. The CFCE loss specifically relies on the ContrastiveCAM decomposition (Proposition 4.2); using HiResCAMs would make the core/non-core split ill-defined because the spurious M would contaminate both terms. The connection is well-motivated.
2. **"CE w/Arch baseline makes CFCE's improvement look larger"** — REMOVED. The paper includes multiple baselines (CE, CORM, DFR) alongside the architecture-controlled comparison. This criticism misreads the experimental design.
3. **"More baselines needed (Aniraj et al.)"** — REMOVED per meta-reviewer rules: requesting additional baselines beyond what is standard in the field.
4. **"Standard faithfulness evaluations (deletion/insertion) missing"** — folded into the retained Major weakness on faithfulness.
5. **Appendix-based concerns about proofs** — REMOVED per meta-reviewer rules: missing appendix content is a parser artifact.

## Novel Insights

The core tension identified by the reviews is that the paper's "faithfulness" framing would require evidence beyond what is provided: M-invariance establishes that ContrastiveCAMs are **uniquely determined** by class probabilities, but uniqueness is not equivalent to faithfulness (accurate reflection of the model's internal decision process). The paper's own evaluation of ContrastiveCAMs uses IoU with human-annotated core masks, which measures alignment with human labels — a valuable but distinct property. This is a framing mismatch, not a fundamental flaw, and can be corrected by recalibrating the claims. Separately, the empirical strength of CFCE on Hard-ImageNet (30%→93% IoU) is compelling regardless of whether one accepts the faithfulness framing.

## Suggestions

1. Either add standard faithfulness evaluations (deletion/insertion, ROAR) for ContrastiveCAMs, or recalibrate claims from "faithful" to "non-arbitrary" / "uniquely determined by class probabilities."
2. Investigate whether the ~4% accuracy drop on Hard-ImageNet is recoverable with longer training or better hyperparameters, and discuss the discrepancy with Oxford Pets.
3. Explain why KL regularization helps with GT masks but hurts with SAM masks on Oxford Pets; report λ₁, λ₂, λ₃ values.
4. Motivate the use of absolute value in the non-core penalty term (Eq. 15).
5. Extend experiments to at least one additional architecture to demonstrate generality.

**Calibration anchors considered (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| wZiH43e5Ah | 3.00 | R1 | Yes | Concept extraction paper rejected due to limited validation. Our paper has stronger theory and clearer experiments. |
| L7jtdGhWzT | 4.67 | R1 | Yes | Faithfulness paper with mixed results and outdated baselines. Our paper is stronger. |
| U7VW3KBm34 (SRD) | 6.00 | R1 | Yes | Accepted XAI method with thorough evaluation. Our paper's theoretical novelty and downstream application give it an edge. |
| 57NfyYxh5f (How to Probe) | 6.25 | R2 | Yes | Accepted. Similar weakness profile (ResNet-50 only). Our paper has stronger theoretical novelty and empirical results. |
| OZWHYyfPwY | 7.00 | R2 | Yes | Rejected despite 7.0 due to weak theory-experiment connection. Our paper has a stronger connection. |
| 5Ca9sSzuDp (CLIP) | 8.00 | R1 | Yes | Highly polished interpretability analysis; our paper is not at this level of comprehensiveness. |

**Round 1 bracket:** 5.5–7.5. **Round 2 narrowing:** comparison against itemized anchors (especially "How to Probe" at 6.25 and SRD at 6.0) places the paper in the 6.0–6.5 range. Our paper shares the ResNet-50 limitation and the need for more comprehensive evaluation with "How to Probe" (6.25), but has stronger theoretical novelty and more striking empirical results. The faithfulness overclaiming is a framing gap, not a factual error — it does not invalidate the core contributions. Score: **6.5**.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>