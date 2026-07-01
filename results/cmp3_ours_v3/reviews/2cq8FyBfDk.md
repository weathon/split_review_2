Now I have my calibration anchors. Let me write the final review.

**Round 1 bracket:** Based on calibration, the paper sits in the 5.0–6.0 range. It is substantially more rigorous than ProteiNexus (3.67, Rejected) but less comprehensive than SaProt (7.33, Accepted). It is closest in quality to the Pre-training Sequence/Structure/Surface paper (5.75, Accepted) and E3Former (5.25, Rejected).

---

## Summary

This paper introduces ProteinVista, a 3D CNN encoder that voxelizes full heavy-atom protein structures and is pre-trained on ~500,000 AlphaFold-2 structures via contrastive alignment with ESM-2 embeddings. Evaluated on three protein–ligand prediction tasks (transporter-substrate, enzyme-substrate, and drug-target IC50), it matches or outperforms ESM-2 models while using ~100× less pre-training compute. The paper also documents honest negative results (GO annotation) and provides a stratified analysis showing when structure-based representations help versus sequence-only models.

## Strengths

- **Compute efficiency is concretely documented.** Pre-training on 4 A100s for 48 hours (~192 GPU-hours) vs ESM-2₆₅₀M on 128 H100s for ~7 days (~21,504 GPU-hours) is a genuine ~100× reduction, with real implications for accessibility (Section 4.3, Fig. 3). Inference throughput (20s vs 426s per 1000 proteins) is also meaningfully faster.

- **Informative ablation study (Section 4.2, Fig. 2e).** Tests voxel resolution (1.0Å vs 1.5Å, −1.1% R²), pre-training objective (contrastive vs Rosetta regression, −1.0% R²), augmentation during fine-tuning (essentially zero effect), and ensemble size (1 vs 5 views, −6.4% R²). These are the right ablations and the results tell a clear story about what matters.

- **Honest reporting of negative results (Section 3.4).** The GO annotation experiment shows ProteinVista underperforms ESM-2 (Fmax 0.57 vs 0.62), and the authors correctly interpret this as structure encoders adding limited value for homology-driven tasks. This strengthens trust in the positive results.

- **Stratified analysis by sequence identity, TM-score, and pLDDT (Section 4.1, Fig. 2a–c).** This diagnostic shows *when* each model works: ProteinVista excels when structures are well-represented in training, while ESM-2 handles low-similarity cases better. The finding that sequence and structure signals are complementary is the paper's most nuanced result.

## Weaknesses

### Major

1. **Contrastive pre-training aligns with ESM-2 embeddings, which complicates the central "outperforms sequence transformers" framing.** ProteinVista is pre-trained via contrastive loss to match ESM-2's embedding space (Section 2.3). This means its downstream performance partly reflects knowledge inherited from ESM-2, not purely from 3D geometry. However, the ablation study partially mitigates this concern: replacing the contrastive objective with a purely structural one (Rosetta regression) drops R² by only 1.0% on IC50 (Section 4.2), suggesting ESM-2 distillation is not the dominant factor. The paper should reframe its headline claim accordingly (e.g., "a 3D CNN that learns complementary representations to ESM-2 and, when fine-tuned, can exceed its teacher on structure-sensitive tasks").

2. **No direct comparison to structure-aware graph-based methods.** The paper motivates its approach by arguing that graph representations (GearNet, ESM-GearNet, GPS-Fun) lose atom-level detail, but never tests whether this is actually true on the same benchmarks. The experiments compare only against ESM-2 (a sequence model). Comparing ProteinVista to at least one graph-based structure method would validate the paper's motivating claim about the importance of full-atom detail.

### Minor

3. **The comparison pipeline may systematically disadvantage ESM-2.** The paper uses an identical simple pipeline (fixed MolFormer embeddings, two-layer prediction head) for both ProteinVista and ESM-2, which the authors acknowledge "likely underestimates for all models the peak accuracy achievable" (Section 3.1). While the IC50 gap (R² 0.69 vs 0.61) is large enough that a fairer comparison would likely still show an advantage, the optimized pipeline (Section 3.3) is only evaluated as an ensemble, so we never see whether ESM-2 alone under optimized conditions narrows the gap.

4. **On the ESP benchmark, standalone ProteinVista essentially ties with ESM-2₆₅₀M** (Acc 91.8% vs 91.9%, ROC-AUC 0.951 vs 0.955, MCC 0.78 vs 0.79; Table 1). The title-level claim that ProteinVista "outperforms sequence transformers" relies primarily on the TSP and IC50 benchmarks and should be scoped accordingly.

5. **Rotation robustness claim is overstated.** The model uses 90°-increment rotations and test-time averaging of 5 views; reducing to 1 view drops R² by 6.4% (Section 4.2). The abstract's "rotation-robust" and line 31's "rotation-invariant predictions" overstate what is actually achieved with discrete augmentations and ensembling.

6. **Inconsistency in reported Rosetta scores.** Section 2.3 says "23 in silico computed Rosetta scores" while Section 5 says "33 Rosetta scores" (lines 73 vs 219). This discrepancy should be resolved.

### Trivial

7. **The density function equation (Section 2.1) contains a formatting/notation artifact.** The expression is garbled; the intended Gaussian density is clear but the raw text could cause confusion for readers implementing from the paper.

## Nice-to-Haves

- A purely structure-based pre-training objective (masked voxel prediction, rotation prediction) as an additional ablation would directly test whether the 3D geometry itself drives performance.
- Reporting the number of test-points per bin in the stratified analysis (Fig. 2a–c) would clarify whether low-identity bins are underpowered.
- Discussing the impact of cropping large structures at the 160³-voxel boundary on distal binding sites.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

- **"Compute cost of AlphaFold structures not included in comparison"**: The paper compares pre-training compute on publicly available AlphaFoldDB structures. Including structure prediction cost is outside the paper's scope.
- **"Missing statistical power analysis for stratification bins"**: A reasonable suggestion but not a core weakness; moved to Nice-to-Haves.
- **"Cropping at 160³ could discard functional regions"**: Valid but speculative; moved to Nice-to-Haves.
- **The harsh critic's severity assessment of Issue 1 as "Structural"** was downgraded because the ablation (1.0% drop) demonstrates ESM-2 distillation is not the dominant performance factor.
- **Generic framing criticisms** merged into weakness #1.
- **Strengths that were generic/superficial** (e.g., "the paper addresses an important problem") were removed; only concrete, evidence-backed strengths are retained.

## Novel Insights

The most interesting observation from the reviews is that the paper's own ablation study (1.0% gap between contrastive and Rosetta regression pre-training) provides stronger evidence *against* the ESM-2 distillation concern than the paper itself seems to realize. The "complementarity" finding — that ProteinVista and ESM-2 excel in different similarity regimes (high vs low sequence/structural identity) — is more valuable than the headline "outperforms" claim and deserves greater emphasis. The review also surfaces that the paper's real contribution is not proving that 3D CNNs beat everything, but rather demonstrating that they are *tractable* and bring complementary information, which is a more defensible and interesting thesis.

## Suggestions

1. **Reframe the central claim.** The paper would be more credible and accurate if it positioned itself as "a compute-efficient 3D CNN that provides complementary information to ESM-2 and can outperform it on structure-sensitive tasks" rather than "outperforms sequence transformers."
2. **Add a graph-based structure baseline** (e.g., GearNet or ESM-GearNet) on at least one benchmark to validate the motivating claim about atom-level detail.
3. **Provide ESM-2 results under an optimized pipeline** (not just the ensemble) so readers can assess the magnitude of the comparison gap fairly.
4. **Resolve the 23 vs 33 Rosetta score inconsistency.**

## Score and Decision

**Score derivation:** The paper was compared against calibration anchors as follows:

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| ProteiNexus | 3.67 (Reject) | R1 | Less rigorous evaluation, our paper is clearly stronger |
| Pre-training Seq/Struct/Surface | 5.75 (Accept) | R1 | Similar contribution type; comparable quality, our paper has better compute analysis |
| Multimodal Distillation (ProteinSSA) | 5.67 (Reject) | R2 | Similar framing issues; our paper has better ablations |
| E3Former | 5.25 (Reject) | R2 | Structure-aware; comparable quality but our paper has stronger empirical evidence |
| SaProt | 7.33 (Accept) | R1 | Much broader evaluation (10 tasks); our paper less comprehensive |

**Round 1 bracket:** 4.5–6.5 → **Narrowed to:** 5.0–6.0 based on comparison with E3Former (5.25) and Pre-training Seq/Struct/Surface (5.75).

The paper has genuine contributions (compute efficiency, honest analysis, complementary representation learning) that place it above the reject range. However, the overstated framing, absence of graph-based baselines, and minor inconsistencies prevent it from reaching the upper half of the accept range. Score is rounded to .5.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>