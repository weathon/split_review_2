Now I have sufficient calibration data. Let me write the final review.

## Summary

This paper identifies and formalizes SSL's label dependency (Theorem 1.1 shows pseudo-label error grows with limited/biased labeled data), then proposes CaPT, a framework that integrates CLIP into SSL via asymmetric-modalities co-training. CaPT jointly trains a fully fine-tuned unimodal network and an adapter-tuned CLIP model, fusing their predictions through entropy-weighted co-pseudo labels. The method achieves strong results on several SSL benchmarks with modest overhead (8% memory, 11% time).

## Strengths

1. **Well-motivated problem diagnosis (Section 1, Theorem 1.1, Figure 1).** The formalization of SSL's label dependency is solid — Theorem 1.1 provides a clean bound showing pseudo-label error grows with prototype bias and shrinks with labeled sample size. Figure 1c's demonstration that SSL's gain from unlabeled data collapses under extreme label scarcity is a genuinely useful empirical observation that goes beyond generic narratives.

2. **Thoughtful architectural design (Sections 3.1–3.3).** The asymmetric-modalities co-training design is sensible and well-executed: CLIP (multimodal, adapter-tuned) provides a prior that is gradually handed off to a fully fine-tuned unimodal network, mediated by entropy-based weighting. The feature-level augmentation for CLIP (Section 3.2.2) is a practical efficiency contribution.

3. **Ablation study validates design choices (Table 6).** The four ablated variants (CaPT-Ada, CaPT-Deb, CaPT-Uni, and one-sided variants) cleanly show that each component contributes. The 12–16% drops when removing either branch confirm that both the unimodal and multimodal modules are needed.

4. **Efficiency is genuinely good (Table 4).** Only 8% more memory and 11% more training time than FreeMatch, while outperforming it substantially. This is a meaningful engineering contribution.

## Weaknesses

### Fatal

None.

### Major

1. **Missing direct comparison against the closest prior works (DebiasPL, CLS).** The paper identifies DebiasPL (Wang et al., 2022a) and CLS (Yao et al., 2022) as the most relevant prior art for integrating CLIP into SSL and co-training, respectively. Yet neither method appears in any comparison table. The ablation includes CaPT-Deb (described as inspired by DebiasPL), but this is an ablated variant of CaPT, not the actual DebiasPL implementation. Since the paper's contribution is a framework for integrating CLIP into SSL, the most informative baselines are other CLIP+SSL frameworks — their absence is a significant gap.

2. **Framing overstates the contribution by making comparisons against non-CLIP SSL methods the primary evidence.** Tables 1–5 compare CaPT (which uses CLIP with adapter-tuning) against SSL methods that do not have access to any vision-language model. For example, on CIFAR-100 with 1 label/class, CLIP zero-shot alone (65.10%) already beats FreeMatch (61.13%) — CaPT's 82.51% builds on top of this. On STL-10, CLIP zero-shot (97.18%) actually outperforms CaPT (96.07–96.34%), yet this case is not discussed. The paper should consistently report CLIP zero-shot / adapter-tuned CLIP performance across all tables (not just Table 1) and position comparisons against non-CLIP SSL methods as secondary evidence.

### Minor

3. **Theorem 1.1 is disconnected from the CaPT method.** The theorem provides a bound on pseudo-label error under a prototype-based GMM, motivating why SSL needs external priors. However, it is never referenced in Section 3 (Method) — none of CaPT's design choices (asymmetric modalities, entropy weighting, adapter-tuning, co-pseudo labels) are derived from or justified by the theory. The theory is a meaningful finding on its own, but the paper presents it as contribution 1 without showing how it informs the solution.

4. **The STL-10 case (CaPT underperforms CLIP zero-shot: 96.07% vs 97.18%) is not discussed in the main text.** CLIP zero-shot and adapter-tuned CLIP are reported only in Table 1, not in Tables 2, 3, or 5. Discussing when CaPT provides diminishing returns relative to CLIP alone would sharpen the paper's claims.

5. **On FGVCAircraft (Table 5), CaPT underperforms FreeMatch (50.12 vs 51.43 with 5 labels) and RegMixMatch (64.33 vs 66.21 with 10 labels).** The paper mentions this is discussed in Appendix N, but given that CLIP's zero-shot on this dataset is only 18.97%, this is precisely the failure mode that tests the framework most critically. A brief in-line discussion of why this happens would strengthen the paper.

6. **ImageNet results (Table 2) lack standard deviations or error bars**, unlike Table 1. Given the 10-label-per-class setting across 1000 classes, variance could be substantial.

7. **The entropy-based weighting (Eq. 11–12) uses batch-level average entropy rather than per-sample weights.** The paper does not justify this choice, and per-sample entropy weighting would be more adaptive.

### Trivial

None.

## Nice-to-Haves

- Include DebiasPL and CLS as primary baselines in comparison tables.
- Report CLIP zero-shot and adapter-tuned CLIP performance consistently across all tables.
- Discuss the STL-10 failure case to clarify when CaPT is most valuable.
- Add standard deviations to the ImageNet table.
- Consider per-sample entropy weighting or justify why batch-level is preferable.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Headline comparisons are fundamentally unfair"** — softened to Major weakness #2. The comparison is not fundamentally unfair (the paper does include CLIP rows in Table 1, and CaPT's design is genuinely novel), but the framing choices inflate the apparent contribution.
- **"Thresholding mechanism mentioned as afterthought"** — removed. The mechanism is described in a dedicated paragraph (line 196) in Section 3.3 as part of the PFM description.
- **"CaPT-Uni shows only 0.88% drop challenging bidirectional flow claim"** — removed. The drop on EuroSAT is 1.49%, and the paper's claim about bidirectional exchange is about the overall trend across datasets, not a single number.
- Critic's various "Section-by-Section Notes" that are descriptive observations rather than actionable weaknesses.
- Critic's "Strengthening the Paper on Its Own Terms" points — subsumed into Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The key insight from the reviews is that the evaluation framing inflates the apparent contribution by using non-CLIP SSL methods as primary comparators, but this is a positioning/presentation issue rather than a novel scientific observation.

## Suggestions

1. Restructure the evaluation: make comparisons against CLIP+SSL methods (DebiasPL, CLS, CLIP-Adapter full fine-tuning) primary, and place non-CLIP SSL methods as secondary context.
2. Report CLIP zero-shot and adapter-tuned CLIP performance in every experimental table alongside CaPT, and discuss cases where CaPT does not improve upon CLIP alone.
3. Either connect Theorem 1.1 to specific design choices in CaPT, or reframe the theoretical contribution as purely motivational.
4. Add standard deviations to the ImageNet table.

## Score and Decision

**Calibration Summary.** All anchors retrieved across rounds (R1 = Round 1, R2 = Round 2; I = itemized):

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| u1cQYxRI1H | 0.50 | R1 | No | Unrelated (illumination harmonization) |
| gwZ90hFSL2 | 1.00 | R1 | No | Unrelated (robot NLP) |
| 5lUdTogEL3 | 1.00 | R1 | No | Unrelated (person re-ID) |
| 5kMwiMnUip | 1.40 | R1 | No | Unrelated (LLM jailbreaking) |
| HfJxXbXlYJ (LLM2CLIP) | 3.00 | R1 | Yes | Overclaimed, marginal improvements, poor presentation. CaPT is significantly stronger. |
| FwkYeLovHk | 3.33 | R1 | No | Weak-to-strong for CLIP; 3.33 avg |
| j1FLTvgyAh | 2.50 | R1 | No | CLIP few-shot prompting; 2.50 avg |
| hgayrNSbri | 3.40 | R1 | No | Retrieval-augmented captioning |
| 1rgMkDWfYV | 4.50 | R1 | Yes | CLIP for noisy labels, rejected. Unfair comparison concerns similar to CaPT but weaker on novelty. |
| baNW94qdsU | 4.00 | R1 | No | Self-training for VLM alignment |
| gqjEhvUC6H | 4.50 | R1 | No | Data dedup for CLIP pretraining |
| PD8JVDg8mB | 4.25 | R1 | No | Annotation bootstrapping |
| **97D725GJtQ (SemiCLIP)** | **5.80** | R1+R2 | **Yes** | SSL+CLIP training. Novelty concerns (-4.10, -3.77 favorability). CaPT has more novel asymmetric co-training and cleaner ablation — stronger. |
| **yD2JMeKumt (DOTA)** | **6.00** | R2 | **Yes** | CLIP TTA. Significant methodological clarity issues. CaPT has clearer methodology. |
| Zkq4fsyjfp | 6.25 | R2 | No | CLIP backbone ensembling |
| k9NYnsC4Mq | 5.67 | R2 | No | CLIP continual learning |
| TLADT8Wrhn | 6.25 | R2 | No | Continual CLIP training |
| 9bMZ29SPVx | 7.50 | R2 | No | CLIP data selection |
| **DjzvJCRsVf (CLIPSelf)** | **7.00** | R1 | **Yes** | CLIP self-distillation. Stronger experiments, cleaner contribution. CaPT is weaker primarily due to missing baselines. |
| RvUVMjfp8i | 8.00 | R2 | No | SSL evaluation framework (different contribution type) |

**Round-1 Bracket:** Between 5.5 and 7.5.

**Round-2 Narrowing:** Compared against SemiCLIP (5.80), DOTA (6.00), and CLIPSelf (7.00):

- CaPT's weakest items have favorability -1.30 (missing baselines) and -0.70 (theory disconnection). By contrast, SemiCLIP's weakest items have favorability -4.10 (lack of novelty) and -3.77 (incremental). CaPT's weaknesses are less severe and more fixable.
- CaPT's strongest items (16.02 for architectural design, 13.60 for problem diagnosis) are comparable to CLIPSelf's (16.20 for experiments, 14.26 for results). However, CLIPSelf has no major missing-baseline issue, putting it ahead.
- CaPT's missing baselines and framing issues are real gaps that prevent it from reaching the CLIPSelf tier.

**Final Score: 6.5.** The paper presents a genuinely novel framework (asymmetric-modalities co-training for CLIP+SSL) with solid empirical validation via ablation and efficiency analysis. However, the missing comparisons against the most relevant prior work (DebiasPL, CLS) and the framing that treats non-CLIP SSL methods as primary comparators are significant issues that need to be addressed. The core contribution is sound and fixable.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>