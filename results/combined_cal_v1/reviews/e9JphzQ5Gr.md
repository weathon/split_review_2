Now I have all the information I need. Let me write the final consolidated review.

---

## Summary

This paper identifies a key limitation in semi-supervised learning (SSL): the utility of unlabeled data is coupled to the quantity and quality of labeled data. To address this, the authors propose CaPT (CLIP as a Prior Teacher), an asymmetric-modalities co-training framework that integrates a unimodal vision network with an adapter-tuned CLIP model. Co-pseudo labels with entropy-based weighting enable bidirectional knowledge exchange. CaPT achieves state-of-the-art results across multiple SSL benchmarks, with especially striking gains under extreme label scarcity (e.g., +21.38% on CIFAR-100 one-label-per-class).

## Strengths

- **Well-motivated empirical grounding (Section 1, Figure 1a–c).** The paper provides clean evidence that SSL methods degrade sharply when labeled data falls below ∼4 samples/class, and that pseudo-label accuracy depends on both the quantity and prototypicality of labeled samples. The "accuracy gain" heatmap (Figure 1c) concretely demonstrates that under one-label-per-class, adding more unlabeled data yields almost no benefit — a strong intellectual anchor for the work.

- **Principled asymmetric-modalities co-training design.** CaPT pairs a pure-vision network with CLIP (vision + language), which naturally satisfies the co-training independence condition (Blum & Mitchell, 1998). The attention map comparison (Figure 3) confirms that the two models encode genuinely different representational biases, mitigating the pattern-homogeneity bottleneck in prior co-training methods.

- **Strong and consistent empirical results across settings.** On CIFAR-100 under one-label-per-class, CaPT achieves 82.51% vs. 60.49% for RegMixMatch (+21.38%). Strong performance on fine-grained datasets (StanfordCars, Flowers102, SVHN) where CLIP's raw zero-shot performance is modest demonstrates that CaPT does more than simply distill CLIP. The ablation study (Table 6) is well-structured and confirms that each component contributes.

- **Efficiency is demonstrated, not just claimed.** Table 4 shows CaPT adds only 8% memory and 11% training time over FreeMatch while achieving much higher accuracy, and is more efficient than RegMixMatch. This directly addresses a key barrier to using CLIP in SSL.

## Weaknesses

### Fatal
None.

### Major
None. The paper has no issues that threaten its core claims.

### Minor

1. **On STL-10, adapter-tuned CLIP alone outperforms CaPT's final output.** From Table 1: on STL-10 with 4 labels/class, CaPT's UPM achieves 96.07%, but adapter-tuned CLIP alone achieves 96.86%, and CLIP zero-shot achieves 97.18%. The co-training framework yields no benefit on this dataset — the final UPM is worse than what CLIP alone can provide. While CaPT still outperforms all SSL baselines (RegMixMatch at 89.89%), this limitation deserves explicit discussion rather than being presented as a uniformly positive result.

2. **The comparison is inherently asymmetrical due to CLIP's massive pre-training.** Baselines use ViTs pre-trained on ImageNet (~1M images) via MAE, while CaPT additionally uses CLIP ViT-B/32 pre-trained on 400M image-text pairs. The paper partially addresses this with fine-grained experiments (Section 4.4), and this is a legitimate research strategy, but the title's "Breaking the Label Dependency" framing overstates the nature of the contribution — the dependency on in-domain labels is substantially reduced but replaced by a dependency on CLIP's massive out-of-domain pre-training.

3. **Missing VLM-assisted SSL baseline from the main comparison.** DebiasPL, the most directly comparable VLM-assisted SSL method, is discussed qualitatively and appears only as an ablation variant (CaPT-Deb), but not in the main comparison table (Table 1). Including it under the USB protocol would strengthen the claim that CaPT's specific co-training design — rather than simply using CLIP — drives the reported gains.

4. **Low standard deviations not explained.** CaPT's standard deviations in Table 1 (0.05–0.13) are an order of magnitude smaller than baselines (0.10–3.34). If real, this is interesting evidence of CLIP's stabilizing effect, but it warrants discussion.

5. **Underperformance on FGVCAircraft not discussed in the main text.** Table 5 shows CaPT underperforms both FreeMatch and RegMixMatch on this dataset. The paper mentions this is discussed in a stripped appendix (Appendix N), but this limitation deserves visibility in the main text.

6. **The confidence threshold for pseudo-label filtering is underspecified in the method section.** Line 196 states a threshold is used, but the precise mechanism is deferred to Section 4.1 ("We adopt the adaptive threshold strategy from FreeMatch"). This should be described in Section 3 for reproducibility.

### Trivial
None.

## Nice-to-Haves

- A training dynamics analysis (pseudo-label accuracy over time, evolution of entropy weights Γ^a and Γ^b) would strengthen the mechanistic claim that "the unimodal network gradually takes over from CLIP" (line 163).
- A deeper analysis of the CIFAR-100 one-label setting (only 100 labeled images total) — explaining how the UPM surpasses CLIP's zero-shot (65.10%) despite almost no supervised signal — would be highly informative.

## Removed Points
These points are flagged to be removed, treat them with caution:
- *"Theorem 1.1 is not a meaningful theoretical contribution"* — Removed as overblown. The bound with 2^(d/2) factor is dimension-dependent, which is standard for this style of theoretical bound. The theorem provides a formal illustration of the qualitative relationship between label quality and pseudo-label error; it is not presented as a tight quantitative guarantee. The critic's assertion conflates looseness with lack of meaning.
- *"The STL-10 results undermine the paper's central narrative"* — Removed as overstated (the paper's narrative is about improving SSL, and CaPT improves over all SSL baselines on STL-10). The milder observation about adapter-tuned CLIP alone outperforming CaPT's UPM is retained above.
- *"Entropy weighting is batch-level, not sample-level"* — Removed as a trivial notation point that does not affect correctness.
- *Several generic strengths from the input* removed as not sufficiently grounded.

## Novel Insights

None beyond the paper's own contributions. The most useful observation surfaced by the reviews — that adapter-tuned CLIP alone outperforms CaPT's UPM on STL-10 — is already transparent from the data the paper reports (Table 1). The insight is about interpretation, not discovery.

## Suggestions

1. Add a brief discussion in Section 4.1 explaining why CaPT's UPM underperforms adapter-tuned CLIP on STL-10, and consider reporting the best branch's accuracy for that dataset.
2. Include DebiasPL in the main comparison table if feasible under the USB benchmark protocol.
3. Move the thresholding mechanism description to Section 3 (Method) rather than deferring to Section 4.1.
4. Briefly address the unusually low standard deviations.
5. Refine the title/abstract language from "Breaking Label Dependency" to "Substantially Reducing Label Dependency" for precision.

## Score and Decision

**Round 1 bracket:** After comparing my draft's weighted items against calibration anchors, I identified an initial plausible range of 6.0–7.5. The paper is clearly stronger than the Semi-Supervised CLIP Training anchor (5.80, which had severe novelty concerns at weights -7.80 and -6.49) and the cross-modal synergy paper (6.33, which had a -7.45 weight mischaracterization concern). It is comparable to CLIPSelf (7.00, strong empiricals with moderate weaknesses -5.02, -5.33) but has even milder negative weights (none below -2.38). It is below the FixMatch Theory paper (8.00, which had a +7.22 theoretical weight) since CaPT does not have a comparably outstanding single dimension.

**Calibration anchors used:**
- 97D725GJtQ (Semi-Supervised CLIP Training, 5.80, Round 1, itemized) — novelty concerns; this paper is stronger.
- 1rgMkDWfYV (Cleaning label noise with VLMs, 4.50, Round 1, itemized) — writing/novelty concerns; this paper is much stronger.
- DjzvJCRsVf (CLIPSelf, 7.00, Round 1, itemized) — similar quality level; this paper has milder weaknesses.
- 5BXWhVbHAK (Cross-modal synergy, 6.33, Round 2, itemized) — had mischaracterization concerns; this paper is stronger.
- 25kAzqzTrz (FixMatch Theory, 8.00, Round 2, itemized) — outstanding theoretical weight (+7.22) but also strong negatives; this paper is more balanced.

**Final placement:** The paper sits at 7.0. It has no fatal or major weaknesses, strong empirical contributions, and a clean method. It is clearly above the acceptance threshold but the minor concerns (STL-10 limitation, asymmetrical pre-training advantage, missing DebiasPL baseline) keep it from being an unambiguous strong accept.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>