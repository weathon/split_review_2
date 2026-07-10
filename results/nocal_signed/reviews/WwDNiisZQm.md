I have all the information needed. Let me write the final consolidated review.

---

## Summary

This paper introduces Content-Aware Mamba (CAM) for learned image compression, addressing two specific limitations of Mamba-style SSMs when applied to images: (1) the fixed raster scan ignores feature-space similarity in favor of spatial proximity, and (2) strict causality is mismatched with the non-causal structure of images. Two mechanisms are proposed—Content-Adaptive Token Permutation (CTP), which reorders tokens by codebook-based clustering to group semantically similar tokens, and Global-Prior Prompting (GPP), which injects sample-specific global priors into the SSM to relax causality. The resulting CMIC model achieves competitive rate-distortion performance (BD-rate -15.91% / -21.34% / -17.58% vs. VTM-21.0 on Kodak/Tecnick/CLIC) with substantially better efficiency than prior Mamba-based LIC models (69M params vs. MambaIC's 157M).

## Strengths

- **Well-motivated problem framing.** The paper correctly identifies two genuine limitations of applying Mamba to images—the fixed raster scan ignores feature-space similarity in favor of spatial proximity, and strict causality is mismatched with the non-causal structure of images—and proposes two targeted mechanisms (CTP and GPP) that directly address them. The motivation is clear and specific.

- **Strong diagnostic evidence via ERF analysis.** Figure 9 traces the effective receptive field of a single SSM layer through successive ablations, directly visualizing how GPP breaks the causal boundary (zero activation after the anchor token → nonzero activation) and how CTP reshapes the ERF toward semantically related rather than spatially adjacent regions. This provides mechanistic insight beyond standard performance ablations.

- **Clean ablation design.** Table 2 shows all four combinations of CTP and GPP on three datasets with consistent patterns: each component individually improves performance, and the combination is always best. The baseline is a correct control (vanilla single-scan Mamba). Table 4 further validates CAM against Conv blocks, 2D Mamba, attention-only, and CAM-only alternatives, showing clear additive benefits.

- **Competitive RD performance with good efficiency.** CMIC achieves BD-rate savings of –15.91% (Kodak), –21.34% (Tecnick), –17.58% (CLIC) against VTM-21.0 with 69.11M params, 2.39 TFLOPs, and 0.405s latency—substantially more efficient than the closest Mamba competitor (MambaIC: 157M params, 5.56 TFLOPs) while also outperforming it on RD.

- **Informative clustering visualization (Figure 10).** Confirms that codebook-based clustering groups semantically meaningful regions (red doors, sky, feathers) and that different images activate different centroid subsets, supporting the claim of content adaptivity. The observation that centroid #10 responds to edges, #26 to red/yellow textured regions, and #33 to smooth blue/green backgrounds provides compelling qualitative evidence.

## Weaknesses

### Fatal
None.

### Major
- **Training data mismatch confounds the SOTA claim.** CMIC is trained on Flickr2W (2,000 images), while baseline numbers (MLICv2, DCAE, S2CFormer, etc.) in Table 1 are quoted from their original papers, which used different and often larger training sets. The paper does not acknowledge this confound nor report what training data each baseline used. Without a controlled comparison—retraining baselines on Flickr2W or training CMIC on the same data as competitors—the magnitude of claimed advantages cannot be fully attributed to architecture. This is a known limitation of LIC evaluation culture, but the paper should at minimum discuss it. The core methodological contribution (CTP + GPP) remains valid, but the "state-of-the-art" label is asserted without caveat about this comparison gap.

### Minor
- **Gradient flow through the hard token permutation is unspecified.** The clustering assignment uses argmax over cosine similarities (Algorithm 1, line 4), which is nondifferentiable. The permutation π is a hard reordering of tokens based on these assignments. The paper does not clarify whether a straight-through estimator or another gradient approximation is used to enable end-to-end training (claimed as a contribution). This is a straightforward implementation detail to clarify and does not threaten the paper's validity, but it should be stated explicitly.

- **BD-rate reported without variance estimates.** BD-rate numbers in Tables 1, 2, 4, and 6 are point estimates with no confidence intervals, standard deviations, or bootstrap ranges. While this is common practice in LIC, the Kodak set has only 24 images, making BD-rate potentially noisy. The lack of variance information makes it difficult to assess whether cross-dataset patterns (e.g., CMIC slightly behind MLICv2 on Kodak but ahead on Tecnick and CLIC) are robust.

### Trivial
None.

## Nice-to-Haves
- A controlled retraining experiment (train the strongest baselines on Flickr2W, or train CMIC on the same data as competitors) would eliminate the training-data confound and strengthen the SOTA claim substantially.
- Ablating the coupling between CTP and GPP (i.e., independent prompting not tied to cluster assignments) could illuminate whether the coupling is beneficial.
- A brief experiment comparing straight-through estimation to alternatives (e.g., Gumbel-softmax) would strengthen the methodological contribution.

## Removed Points
*(These points were raised in the original review but are removed or downgraded per the filtering guidelines. They are documented here for completeness.)*

- **GPP novelty boundary (removed):** The paper explicitly cites MambaIRv2 (Guo et al., 2024a) for the Attentive State-Space equation and clearly states how its approach differs ("this differs from MambaIRv2... where the prompt pool is a standalone learnable matrix..."). The attribution is adequate.
- **Multi-directional scanning complexity claim (removed):** The paper's claim that multi-directional scanning "quadruples computational complexity" refers to FLOPs, which is correct. The reviewer's point about parallel execution concerns wall-clock time, not computational complexity.
- **Training patch size not stated (removed):** A minor detail that does not affect evaluation; training protocols are standard.
- **Naming inconsistency ("MambaC" vs "MambaIC") (removed):** Trivial formatting artifact.
- **Initialization concern for K-Means (removed):** Speculative criticism; the paper demonstrates stable clustering via EMA updates.
- **Missing appendix content / references (removed):** Per instructions, the parser strips appendix sections that exist in the original submission.

## Novel Insights
None beyond the paper's own contributions. The review process did not surface a fundamentally new interpretation of the paper's results beyond what the authors already provide.

## Suggestions
- In the rebuttal, retrain the most competitive baselines on Flickr2W (or conversely, train CMIC on the same data) to directly address the training-data confound.
- Add one sentence clarifying gradient flow through the permutation: e.g., "the permutation operation is treated as a fixed indexing operation; gradients from the SSM pass through to the encoder features before permutation."
- Report BD-rate with bootstrapped confidence intervals or multi-seed variance estimates for Kodak.
- Explicitly acknowledge the training-data limitation in the paper when comparing with baselines trained on different datasets.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>