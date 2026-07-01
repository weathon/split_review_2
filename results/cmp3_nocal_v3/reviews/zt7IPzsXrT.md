## Summary

This paper proposes ScaPre, a unified framework for large-scale multi-concept unlearning in diffusion models. It introduces three components: (1) a conflict-aware stable design combining spectral trace regularization and Bures-distance geometry alignment to suppress conflicting updates, (2) an Informax Decoupler that uses mutual information to identify concept-coupled parameters and adaptively reweight updates, and (3) a closed-form core optimization (Sylvester equation) with a lightweight proximal refinement step. Experiments across object-level (Imagenette, ImageNet-Diversi50), fine-grained (ImageNet-Confuse5), artistic style (50 artists), and explicit content (I2P) benchmarks show strong unlearning effectiveness with competitive generation quality and high efficiency (50 concepts in ~120 seconds).

## Strengths

1. **Well-motivated problem framing.** The paper clearly identifies three concrete challenges faced by existing methods at scale — conflicting weight updates, imprecise targeting, and auxiliary data/module overhead (Section 1) — and designs components to address each.

2. **Informax Decoupler is a principled architectural contribution.** Using mutual information to quantify parameter-concept coupling and adaptively scaling updates (Section 4.2) is a clean approach to precision that avoids per-concept masks or separate adapters, contrasting favorably with methods like MACE (separate LoRAs) or UCE (uniform parameter treatment).

3. **Strong efficiency and scalability results.** Unlearning 50 concepts in ~120 seconds with ~5 GB peak memory (Section 5.5, Figure 3) is substantially faster than SPM (~4.5 hours, ~18 GB) and ESD (~4 hours, ~15 GB), which is practically significant for deployment.

4. **Broad and thoughtful evaluation.** The paper tests across object-level, fine-grained disentanglement (ImageNet-Confuse5 is a well-designed confusion benchmark specifically targeting the precision claim), artistic styles (50 artists), and explicit content (I2P), with visual comparisons alongside quantitative metrics.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
1. **"Closed-form" branding is inconsistent with the method's actual structure.** The abstract and conclusion describe ScaPre as a "closed-form framework" and "the first closed-form framework specifically designed for large-scale concept unlearning." Yet Section 4.3 states that the geometry alignment term (Bures distance) "involves matrix square roots nested inside covariance operators, which makes the overall objective no longer purely quadratic and therefore incompatible with direct closed-form optimization." The method is a two-stage procedure — a closed-form Sylvester solve followed by a non-closed-form proximal refinement. The paper honestly describes this in Section 4.3 but reverts to unqualified "closed-form" language in the framing sections, creating a credibility gap that detracts from the real contributions.

2. **UQ metric is non-portable and hard to interpret.** The unified metric UQ (Section 5.1) is a harmonic mean of sigmoid-normalized accuracy and CLIP score, where the normalization statistics are computed *across the set of methods being compared*. This means UQ values from Table 1 are not comparable to those from Table 3, and adding/removing a baseline would shift all values. The community has no calibration for what a UQ difference of 14 points means. This is partially mitigated because raw accuracy and CLIP scores are also reported separately, but the paper's headline comparisons lean on UQ.

3. **MI estimation procedure is underspecified.** The Informax Decoupler (Section 4.2) is central to the precision claim, but several details needed for reproducibility are missing from the main text: (a) how is the adaptive threshold τ_i per channel set? (b) what is the total sample size K? (c) what exactly are the "neutral inputs" used for y=0 samples (concept-name prompts, generic captions, or a separate dataset)? These should be stated or clearly cross-referenced to the appendix.

4. **"No additional data" claim needs clarification.** The paper asserts "requiring no additional data" (abstract, contributions), but the MI estimation requires forward passes on both target-concept inputs and "neutral inputs" (y=0) whose nature and source are never specified. If these are generic prompts requiring no separate labeled dataset, this should be stated explicitly.

5. **"SP" baseline is never defined.** The acronym "SP" appears in every experimental table (Tables 1–4) and figure captions alongside FMN, SPM, MACE, ESD, UCE, and RECE, but is never introduced or expanded in the paper. Section 2.2 (Related Work) describes methods including MACE, SPM, Sculpting Memory, ESD, UCE, and RECE — none mapped to "SP." This prevents assessment of whether the comparison is appropriate.

6. **No variance or confidence estimates.** All results in Tables 1–4 are single point estimates from a stochastic generation process. For example, ScaPre achieves 0.8% accuracy on Imagenette — without multiple seeds or confidence intervals, the reader cannot assess whether performance gaps between methods are statistically meaningful.

### Trivial
- A runtime breakdown (time spent on MI estimation vs. Sylvester solve vs. proximal refinement vs. matrix construction) would help explain where efficiency gains come from.

## Nice-to-Haves

- **Supplement UQ with metric-agnostic comparisons.** A scatter plot of accuracy vs. CLIP score (or FID) with a Pareto frontier across methods would let readers evaluate tradeoffs without relying on a paper-specific composite metric.
- **Discuss the preserve accuracy gap on ImageNet-Confuse5.** ScaPre achieves 76.3% preserve accuracy vs. the original SD v1.5's 86.6% (Table 4). While vastly better than other unlearning methods, the 10-point gap relative to the original model warrants discussion about remaining collateral damage.
- **Add a limitations section.** Two obvious candidates: (a) ScaPre operates only on cross-attention layers, so concepts encoded primarily in other modules may be harder to unlearn; (b) the Bures distance refinement requires matrix square roots that may be numerically unstable for ill-conditioned covariance matrices.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

- **"The method is not closed-form" framed as a fatal/major issue:** The paper honestly describes the two-stage procedure in Section 4.3. The branding in the abstract/conclusion is overstated but the technical description is correct. This is a presentation inconsistency, not a methodological flaw.
- **"UQ metric is not a reliable basis for comparison" framed as an evidential issue:** The paper also reports raw accuracy and CLIP scores separately in every table. Headline claims are supported by individual metrics, not UQ alone.
- **Speculative extrapolation about MI estimation requiring "extra data":** The paper does not specify what "neutral inputs" are, making clarification necessary, but the reviewer's stronger claim that this would "constitute extra data" is speculative without knowing what the neutral inputs actually are (they could be simple generic prompts).
- **Complaint about Eq. 10's Kronecker-form system size (589,824 × 589,824):** This misunderstands Sylvester solvers — standard methods (e.g., Bartels-Stewart) solve in O(d_in³ + d_out³), not O((d_in·d_out)³), making the system tractable.
- **Section-by-section note about Eq. 3's dimensional reasoning:** The reviewer acknowledges it works out mathematically; the observation is a presentation preference, not a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Qualify the "closed-form" language throughout.** Replace "closed-form framework" with "closed-form core optimization followed by a lightweight geometric refinement" or equivalent in the abstract, contributions list, and conclusion.
2. **Specify the MI estimation details.** State K (sample size), the τ_i setting mechanism, and the exact source of neutral inputs in Section 4.2.
3. **Define the "SP" baseline** — expand the acronym or replace it with the method's full name.
4. **Add variance estimates** (at minimum 3 random seeds) to main experimental tables.
5. **Add a brief limitations paragraph** discussing the cross-attention-only scope and the numerical stability of the Bures refinement.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>