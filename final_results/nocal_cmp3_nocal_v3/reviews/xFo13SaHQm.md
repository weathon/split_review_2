## Summary

This paper tackles the "copy-paste artifact" in identity-consistent image generation—where models replicate the reference face rather than synthesizing the identity across natural variations in pose, expression, or lighting. It makes three contributions: (1) MultiID-2M, a large-scale dataset of 500k paired group photos with reference banks (~400 images/identity) plus 1.5M unpaired images; (2) MultiID-Bench, a benchmark that uses similarity to ground-truth (Sim(GT)) rather than similarity to reference (Sim(Ref)) as the primary metric, together with a Copy-Paste (CP) metric that quantifies over-replication; and (3) WithAnyone, a FLUX-based model trained with a four-phase pipeline and an ID contrastive loss leveraging the paired data to reduce copy-paste while maintaining identity fidelity.

## Strengths

1. **Well-motivated problem identification (Sections 1–2, Fig. 2).** The "copy-paste artifact" is a genuine and underexplored failure mode. The paper supports it with real data: natural face-pair similarity ranges from 0.30 to 0.77, while models like InstantID produce an artificial peak near 1.0. The framing that Sim(Ref) rewards copying and reconstruction-based training exacerbates it is conceptually clean.

2. **MultiID-2M is a significant resource (Section 3).** At 500k paired group photos with ~400 reference images per identity, this fills a genuine data bottleneck. The four-stage construction pipeline is well-specified, and the ethical documentation (CC-licensed sources, anonymized internal IDs, public figures only) is thorough and responsible.

3. **MultiID-Bench evaluation design is principled (Section 4).** Using Sim(GT) rather than Sim(Ref) as the primary identity metric directly addresses the paper's central critique. The CP metric (Eq. 2: normalized bias toward reference vs. ground truth) is a clever formalization. Fig. 5 convincingly visualizes the trade-off: most methods lie on a regression curve where higher Sim(GT) correlates with stronger copy-paste, while WithAnyone demonstrably occupies a different region.

4. **GT-aligned landmark ID loss is a practical innovation (Section 5.1).** Using ground-truth landmarks to align the generated image for ArcFace embedding extraction avoids the unreliability of extracting landmarks from noisy diffusion outputs. This is cleaner than PortraitBooth's partial application (t < 0.25) and cheaper than PuLID's full denoising.

5. **Comprehensive evaluation scope.** 12+ baselines covering both general customization and face-specific methods, two benchmarks (MultiID-Bench and OmniContext), multiple metrics, and a user study. The breadth is appropriate for the paper's scope.

## Weaknesses

### Major

- **In-distribution evaluation advantage for the home method on MultiID-Bench.** MultiID-Bench is constructed from the same data pipeline (web-scraped celebrity photos with matching to a reference bank) as MultiID-2M, on which WithAnyone was trained. While the paper states test identities have "no overlap to training data," WithAnyone has been trained on the *image distribution* of this pipeline (specific sources, quality characteristics, lighting, poses, camera styles). Baselines like PuLID, InstantID, and UniPortrait were trained on FFHQ, CelebA, or other datasets with substantially different distributions, so their lower scores could partly reflect distribution shift rather than a genuine disadvantage on the task. The OmniContext results provide partial external validation, but (a) OmniContext also evaluates on a different distribution where VLMs dominate, and (b) the paper's headline claims are on MultiID-Bench. The paper does not discuss this confound.

- **No error bars, confidence intervals, or variance estimates on any quantitative metric.** Tables 1 and 2 report point estimates without any measure of uncertainty. Given that several methods are separated by 0.01–0.02 in Sim(GT) (e.g., Ours 0.460 vs. InstantID 0.464 vs. UMO 0.458), it is impossible to assess whether the reported advantages are statistically reliable. This is a significant methodological gap for a paper making comparative state-of-the-art claims.

### Minor

- **CP metric's "moderate" correlation with human judgment is not quantified.** The paper states (Section 6.3) that "the copy-paste metric exhibits a moderate positive correlation with human judgments" but does not report the actual correlation coefficient, a confidence interval, or any disaggregated analysis of cases where the metric and human raters disagree. A proxy metric whose alignment with perception is reported only as "moderate" needs stronger validation before it can serve as primary evidence.

- **Claim of "breaking the trade-off" is overstated.** The Abstract and Conclusion state that WithAnyone "breaks the long-observed trade-off between fidelity and artifacts." The results show a *substantial shift* in the Pareto frontier—competitive Sim(GT) (0.460) with much lower CP (0.144 vs. InstantID's 0.337)—but at the cost of lower Sim(Ref) (0.578 vs. InstantID's 0.734) and the lowest aesthetics score among comparable methods (4.783). The trade-off is shifted, not eliminated. "Substantially reduces copy-paste while maintaining competitive identity fidelity" would be more accurate.

- **Ablation table has an interpretive gap (Table 3).** The "w/o Ext. Neg." row shows CP = 0.074—substantially *lower* (better) than the full model's 0.161. The paper notes that "the effectiveness of ID contrastive loss is greatly reduced," but a less careful reader could misinterpret the lower CP as a success when it actually reflects failed identity preservation (Sim(G) drops to 0.368 from 0.405). Moreover, the CP threshold filtering (Sim(GT) > 0.40 for Table 1, > 0.35 for Table 2) is not applied in Table 3, making cross-comparison difficult.

- **WithAnyone's low aesthetics score is not discussed.** In Table 1, WithAnyone achieves the lowest Aes score (4.783) among comparable face-specific methods, below InstantID (5.255), PuLID (4.839), and UniPortrait (5.018). If this metric reflects perceptual quality, the paper should address whether the CP improvement comes at a quality cost and whether this is acceptable for the intended use cases.

- **ArcFace matching threshold (0.4) not justified (Section 3).** The threshold of 0.4 for identity matching is stated without rationale. Given that ArcFace thresholds typically range from 0.3–0.7 depending on task strictness, 0.4 is relatively permissive and could allow identity mismatches that add label noise to the paired data.

- **Different CP filtering thresholds not explained.** The benchmark applies Sim(GT) > 0.40 for single-person subsets (Table 1) and Sim(GT) > 0.35 for multi-person subsets (Table 2). No rationale is given for why different thresholds are used, or for how these specific values were chosen.

- **User study lacks statistical detail (Section 6.3).** Ten participants and 230 groups is a reasonable size, but the paper reports only a vague "moderate positive correlation" without the correlation coefficient, confidence interval, or any measure of inter-rater reliability. The figure description refers to the method as "Cure" rather than "WithAnyone," indicating a labeling inconsistency.

### Trivial

- **Figure 8 describes the method as "Cure" instead of "WithAnyone."** The figure caption and body text refer to "Cure" (e.g., "Our method (Cure) consistently shows the largest bubbles"), which appears to be an internal working name that was not updated in the figure. This does not affect the scientific content but should be fixed.

## Nice-to-Haves

- Calibrate the CP metric against human judgment more rigorously: report the actual correlation coefficient with confidence intervals, and analyze cases where CP and human ratings diverge.
- Quantify the distribution mismatch between MultiID-Bench and each baseline's training set (e.g., FID or distributional distance) to assess the magnitude of the in-distribution advantage concern.
- Ablate the negative pool size to show whether performance saturates beyond 4096.
- Justify the identity-matching threshold (0.4) and the CP filtering thresholds (0.40 vs. 0.35) empirically.

## Removed Points

These points are flagged to be removed — treat them with caution:

- *"The formatting of Table 3 is also corrupted by the parser and would need cleanup"* — This is a parser artifact, not an author error. (Hard Rule: formatting nitpicks.)
- *"DynamicID excluded from experiments due to code unavailability"* — This is the paper's own explicit footnote (Section 2), not a reviewer-raised weakness. The reviewer mentions it neutrally; it does not constitute a criticism.
- *"The bubble chart description... suggests a figure-label mismatch in the original PDF"* — This is real but already captured as a Trivial weakness above ("Cure" naming). The duplicate framing is removed.
- *"Section-by-section notes about OmniContext leaderboard showing general models outperform face-specific methods"* — The paper already acknowledges this (Section 6.1: "VLMs... emphasize non-identity attributes... WithAnyone still has best performance among face customization models"). The reviewer's observation is accurate but the paper already addresses it; no separate weakness is needed.

## Novel Insights

The most valuable insight from the cross-review is the recognition that the "evaluation confound" (in-distribution advantage) and the "lack of error bars" are not independent issues. If error bars had been reported, they would reveal both the variance in the method's own performance and the distribution-sensitivity of the baselines — which is precisely the information needed to assess whether the MultiID-Bench numbers are robust or inflated by data-source overlap. These two weaknesses together point to a single underlying gap: the paper does not provide the statistical tools a reader needs to distinguish genuine methodological advantage from confounds in the evaluation setup. Addressing both simultaneously (e.g., reporting confidence intervals and comparing distributional similarity) would substantially strengthen the credibility of the results.

## Suggestions

1. Report confidence intervals or bootstrap-based error bars for all main metrics (Sim(GT), CP, Sim(Ref), etc.) to establish whether the observed advantages are statistically significant.
2. Add a discussion of the in-distribution evaluation concern, acknowledging the shared data pipeline between MultiID-2M training data and MultiID-Bench test images, and present the OmniContext results as a distribution-robustness check.
3. Temper the "breaking the trade-off" claim to describe the results as a "substantial shift" or "significant improvement" in the Pareto frontier rather than a complete decoupling.
4. Report the actual CP-vs-human correlation coefficient (with confidence interval) and discuss cases where the metric and human judgments diverge.
5. Address the aesthetics gap: explain why WithAnyone scores lower on aesthetics and whether this is an inherent cost of the approach.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>