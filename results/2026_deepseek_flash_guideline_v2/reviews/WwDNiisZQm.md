## Summary

This paper introduces Content-Aware Mamba (CAM), a modification to Mamba-style SSMs for learned image compression that addresses two limitations of standard Mamba: (1) content-agnostic raster scanning (remedied by Content-Adaptive Token Permutation, CTP, which reorders tokens by feature-space similarity via codebook-based clustering), and (2) strict causality (remedied by Global-Prior Prompting, GPP, which injects sample-specific global priors into the SSM output matrix). The full model, CMiC, achieves strong BD-rate savings against VTM-21.0 (−15.91%, −21.34%, −17.58% on Kodak, Tecnick, CLIC) while maintaining moderate complexity.

## Strengths

1. **Content-Adaptive Token Permutation via codebook-based clustering.** The paper replaces Mamba's fixed raster scan with a learned permutation that groups tokens by feature-space similarity. The ablation (Table 2) shows CTP alone yields 1.8–2.4% BD-rate improvement on three datasets, and the ERF visualizations (Fig. 9d) confirm it breaks the rigid raster-scan pattern, activating semantically related locations regardless of spatial distance. This is a well-motivated and empirically validated improvement over prior Mamba-based LIC models (MambaVC, MambaIC) that rely on fixed scan orders.

2. **Global-Prior Prompting tied to cluster centroids.** Unlike MambaIRv2's standalone learnable prompt pool, CAM constructs prompts by projecting cluster centroids (Eq. 1), explicitly tying each prompt vector to a specific semantic cluster. Ablations (Table 2) show GPP alone improves the baseline by 0.5–1.4%, and the ERF evidence (Fig. 9c) demonstrates non-zero activations beyond the causal scan boundary — a measurable demonstration of relaxed causality without multi-directional scanning.

3. **Competitive RD performance with moderate complexity.** CMiC achieves the best BD-rate on Tecnick (−21.34%) and CLIC (−17.58%) among all compared methods, while using a single selective scan rather than quadruple multi-directional scans. It reduces parameters by 56%, FLOPs by 57%, and peak memory by 78% compared to MambaIC, while obtaining better RD performance.

4. **Systematic ERF analysis isolating component contributions.** Figure 9 provides a controlled decomposition of how CTP and GPP each affect the receptive field of a single Mamba layer, directly substantiating the paper's causal claims about how each mechanism addresses specific limitations of vanilla Mamba. This goes beyond standard BD-rate reporting and strengthens the evidence for the method's design.

## Weaknesses

### Major

1. **Unqualified "state-of-the-art" claim is contradicted by Table 1 on Kodak.** The abstract and introduction announce "state-of-the-art rate-distortion performance" without qualification. However, Table 1 shows MLICv2 achieves a better BD-rate on Kodak (−16.16% vs. −15.91%). Kodak is arguably the most frequently cited test set in the LIC literature. The paper's further statement that CMiC "consistently outperforms leading methods across all evaluated datasets" (Section 4.3) is factually incorrect for Kodak. The authors should either acknowledge this, discuss why it occurs (e.g., MLICv2 has 22% more parameters and 16% more FLOPs), or qualify the claim by dataset or complexity regime. This overclaiming erodes the paper's credibility despite otherwise strong results.

### Minor

2. **Throughput comparison conditions for baselines are unclear.** Table 3 reports training throughput for TCM-L (17.80), MambaVC (6.55), and MambaIC (9.35) alongside CMiC variants (22.05–23.19 samples/s). It is not stated whether these baselines were measured in the same environment (same GPU, framework, batch size) or taken from their respective papers. Hardware differences could easily explain the large discrepancies (e.g., MambaVC at 6.55 vs. CMiC at 22.05). The same ambiguity applies to peak memory figures in Table 1. The authors should clarify the measurement conditions.

3. **Training conditions of baseline methods are not specified.** The paper trains CMiC on Flickr2W but does not state whether baselines in Table 1 were retrained on the same dataset or whether published numbers from models trained on different datasets (e.g., ImageNet) are used. Since training dataset size and composition affect RD performance, this is an important omission for fair comparison.

4. **No statistical uncertainty reported.** BD-rate is reported as a single number with no confidence intervals or multi-seed results. Given that the gap between CMiC and MLICv2 on Kodak is only 0.25 percentage points, some indication of variance would help interpret whether the difference is meaningful.

### Trivial

5. The 5 K-Means iterations per training step is mentioned in Section 4.1 (experimental setup) but would be more naturally placed in Section 3.3 (method description).
6. "MambaC" in Table 1 (line 209) appears to be a typo for "MambaIC," the model cited as (Zeng et al., 2025).

## Nice-to-Haves

- Ablate whether the centroid-tied prompt dictionary (GPP) systematically outperforms a standalone learnable prompt pool of the same size, to validate the design choice of tying prompts to centroids.
- Analyze what drives the number of activated centroids (e.g., correlation with image complexity, bpp, or spatial entropy) to strengthen the adaptivity claim.
- Consider comparing CTP against a differentiable relaxation of the permutation (e.g., Gumbel-Softmax clustering) to assess whether the hard argmax assignment is critical for performance.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Non-differentiability of CTP / end-to-end training concern** (Harsh Critic, listed as "structural"): The critic claims the paper does not address gradient flow through the discrete permutation, and that claims of "end-to-end" training are misleading. However, the permutation is a rearrangement of indices (not a replacement of values as in VQ-VAE), so gradients can flow through the SSM back to the original tokens without needing a straight-through estimator. The centroids are indeed updated via non-gradient EMA, but the paper explicitly acknowledges this ("this non-gradient update process," line 120) and the overall pipeline (features, SSM parameters, prompting parameters) is trained end-to-end via the RD loss. The critic's concern partially reflects a misunderstanding of the gradient path through a reindexing operation; the paper's claims about end-to-end training are standard for models of this type.

- **Entropy model limitation deserves more discussion** (Harsh Critic): The paper already notes in Section 4.5 that "adding CAM yields negligible performance gains while increasing latency, indicating a limitation of CAM in enhancing entropy modeling" and references Appendix A.3.2 for details. The observation is honest and appropriately scoped; this is not a weakness.

- **Missing wall-clock training time** (Harsh Critic): The paper already reports that K-Means accounts for "only 5% of each step's training time" (Section 4.1). Requesting absolute wall-clock values is a formatting preference, not a substantive gap.

- **Missing related works / inaccessible appendix / formatting nitpicks**: Removed per policy.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the overclaiming of SOTA status as the primary concern, which is already evident from comparing the paper's claims with Table 1.

## Suggestions

1. Qualify the SOTA claim. Acknowledge that MLICv2 achieves better BD-rate on Kodak, and either discuss why (e.g., parameter count differences, training data) or frame the contribution as "competitive SOTA performance with significantly lower complexity."
2. Clarify whether baseline throughput and memory figures (Tables 1 and 3) were measured in the same environment or taken from published reports. If the latter, specify the source and note hardware differences.
3. State which baselines were retrained on Flickr2W vs. reported from their original papers.
4. Consider adding a small number of multi-seed runs to provide variance estimates for the main BD-rate results.

## Score and Decision

The calibration search tool was unavailable due to a file-system issue in the evaluation environment. Scoring is therefore based on direct analysis of the paper against ICLR standards and comparison with typical learned image compression papers from the literature.

**Calibration note:** In the LIC field, a paper that proposes a novel and well-motivated architectural modification (content-adaptive scanning for Mamba), validates it with clean ablations and ERF analysis, and achieves results that are best-on-two-of-three-datasets with clearly lower complexity than the closest competitor, would typically receive borderline-accept to accept scores (6–7 range). The unqualified SOTA overclaim is the primary detractor. The paper would benefit from a revision round to correct this and clarify experimental conditions.

**Final reasoning:** The paper has genuine methodological novelty (CTP + GPP), good empirical support, and competitive results on standard benchmarks. The main weakness is an overclaiming issue in the paper's narrative (unqualified "SOTA" when MLICv2 outperforms on Kodak) and some unclear experimental reporting details. These are fixable with careful revision. As written, the paper is a borderline accept — the contributions are real and the method works, but the presentation issues reduce confidence in the paper's self-assessment.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>