Now let me write the final review.

## Summary

This paper proposes SPS and SPS+, differentially private synthetic data generation algorithms that adapt activation-statistic-matching dataset distillation (D3S) to the DP setting. The key idea is to collect privatized class-conditional activation statistics through a public pretrained model (removing the need for a privately trained teacher), then synthesize a private dataset by matching these statistics. SPS+ introduces multitask clipping and grouped pseudo-classes to handle high-privacy, multi-class regimes. On CIFAR-10/100 at ε=1, SPS+ achieves 96.2%/76.6%, outperforming DP-SGD (94.8%/70.3%), and demonstrates practical advantages in federated learning, continual learning, and model ensembling that DP-SGD cannot support.

## Strengths

1. **Novel technical contribution (Sections 3, 4).** Adapting D3S-style distillation to the DP setting is non-trivial and carefully engineered: removing the privately trained model, introducing class-conditional statistics with hard labels, random projections to control dimensionality, noise redistribution via scaling, and the multitask clipping and grouped pseudo-classes techniques. The paper correctly identifies and exploits the post-processing property as a genuine advantage over DP-SGD.

2. **Empirically competitive results (Table 1).** Even in the architecture-controlled comparison (SPS+ WRN28-10 vs DP-SGD WRN28-10), SPS+ achieves 95.1% on CIFAR-10 at ε=1 vs 94.8%, and 71.0% on CIFAR-100 at ε=1 vs 70.3%. The CIFAR-100 improvements are consistent across all ε values. This is, per the paper's claim, the first generation-based method to match or exceed DP-SGD on these benchmarks.

3. **Practical advantage demonstrations (Sections 5.5, 5.6).** The federated learning (89.5% at ε=1 across 5 parties) and continual learning experiments directly substantiate the paper's central thesis that data-based privacy unlocks workflows gradient-based methods cannot support — asynchronous federation, unlimited reuse, and model ensembling without additional privacy cost.

4. **Domain transfer demonstration (Section 5.2, Table 2).** The CAMELYON17 results (92.6% at ε=8 vs DP-SGD's 90.5% at ε=10) show the method works under significant domain mismatch between ImageNet-pretrained features and histopathology data.

## Weaknesses

### Fatal
None.

### Major

1. **Theorem 4.1 contains an incorrect formula (Section 4.3).** The theorem states ε = Mα/(2δ²). From the Gaussian mechanism in eq. (4) with noise σ = b₀‖v‖_max and sensitivity ‖v‖_max, the correct RDP guarantee for a single mechanism is ε(α) = α/(2b₀²), and with M-fold composition ε(α) = Mα/(2b₀²). The denominator uses δ (the DP parameter, set to 10⁻⁵ in experiments) where it should use b₀ (the noise multiplier). This is not a parsing artifact — it is the paper's central privacy guarantee, stated with the wrong symbol. While this is very likely a notational error (the standard RDP composition of Gaussian mechanisms is well-understood and the experimental privacy accounting appears to use correct calibration), the theorem as published is mathematically incorrect and must be corrected. If the proof in Appendix C.1 uses b₀ correctly, the main text needs a clear fix; if the proof shares the error, the privacy analysis requires revision.

### Minor

2. **Headline comparison uses a different architecture and ensembling (Abstract vs Table 1).** The abstract leads with "96.2% at ε=1" (SPS+ WRN34-10 Ensemble) compared to DP-SGD's "94.8%" (WRN28-10 single model). The paper does present the architecture-controlled comparison (SPS+ WRN28-10: 95.1%) in Table 1, and this controlled comparison still favors SPS+. However, consistently foregrounding the WRN34-10 ensemble numbers creates an inflated impression of the margin (1.4% vs 0.3% on CIFAR-10). The controlled comparison should be the primary headline.

3. **Grouped pseudo-classes mechanism is inadequately explained (Section 4.2).** The paper states this technique "only works due to dynamics of optimizing the loss function, specifically the Σ inversion in the KL-divergence, and the eigenvalue clipping of Σ" and "does not offer benefits for direct mean estimation." This admits dependence on uncharacterized optimization dynamics. The main text does not specify how pseudo-class groups are constructed (random partition? overlapping? how are conflicts from overlapping class assignments resolved?), nor why KL optimization would prefer noisier pseudo-class statistics over direct class statistics. Given that grouped pseudo-classes are central to SPS+'s CIFAR-100 improvement (SPS: 48.9% vs SPS+: 71.0% at ε=1), the mechanism needs a clearer explanation or at minimum an empirical characterization in the main text.

4. **CAMELYON17 baselines at mismatched ε (Table 2).** The comparison reports Ours at ε=8, DP-Diffusion at ε=10, Private Evolution at ε=7.56, and DP-SGD at ε=10. While SPS+ still leads, matching ε across all methods would strengthen the comparison.

5. **Ensemble results lack error bars (Table 1).** Ensemble accuracy is reported as single numbers while individual models include ± ranges. Reporting variance across ensemble seeds would be informative.

### Trivial
None.

## Nice-to-Haves

- Quantify generation cost (GPU-hours) to contextualize the computational overhead trade-off vs DP-SGD, as noted in the limitations section.
- Include an ablation varying the grouped pseudo-class grouping strategy (random vs similarity-based groups, number of groups) to establish when and why it works.
- Report matched-ε comparisons for CAMELYON17.

## Removed Points

These points are flagged to be removed; treat them with caution:

1. **"Full-size datasets contradict 'distillation' naming."** The critic argued generating 50,000 images (same size as original) makes the "dataset distillation" framing misleading. However, (a) the paper does show compression experiments (Figure 5) at ~10× ratio with only ~1% accuracy loss, (b) the method is derived from distillation techniques, and (c) the paper is transparent about dataset size. This is a framing preference, not a substantive weakness.

2. **"SiLU/GSAM downstream training conflates comparison."** The critic noted that using SiLU activations and GSAM for downstream training means the comparison is less about generation quality. However, this is a genuine advantage of the data-based approach enabled by the post-processing property, not a confound. The paper correctly presents this as a feature.

3. **"'First alternative' claim is overbroad."** The paper scopes this to "image-classification tasks" and immediately concretizes with CIFAR-10/100. The scope is reasonable.

4. **"Typo: 'key advantage of SPS of DP-SGD'."** This is a parser artifact; the original submission does not have this issue.

5. **"Oversized distillation questions."** Rehashes the full-size framing critique. The paper demonstrates both compression (Figure 5) and oversizing (Table 3) — both valid investigations.

## Novel Insights

The reviews surface a tension between the "dataset distillation" framing and the primary full-size experiments. The method's most novel aspect is not compression (as distillation traditionally implies) but rather the ability to generate private data of any size with a one-shot privatization cost. The compression results (Figure 5) — achieving strong performance at 10% of original dataset size — are arguably more practically significant than the full-size results, yet they are underemphasized relative to the headline numbers. This finding is a more compelling story: SPS+ can produce compact private datasets for distribution at scale.

## Suggestions

1. Fix Theorem 4.1: replace δ² with b₀² in the denominator, or clarify notation if δ is being repurposed.
2. Restructure the presentation: make the WRN28-10 architecture-controlled comparison the primary headline result, with WRN34-10 ensemble as a secondary demonstration of the flexibility advantage.
3. Add a mechanistic explanation or ablation for grouped pseudo-classes in the main text, even if the full analysis remains in the appendix.
4. Add error bars (or a stability statement) to ensemble results in Table 1.
5. Report matched-ε CAMELYON17 comparisons or explicitly note the ε range.

## Score and Decision

This paper makes a genuine contribution: it is the first generation-based method to match or exceed DP-SGD on standard image classification benchmarks, and it convincingly demonstrates downstream advantages (federated learning, continual learning, ensembling) that are structurally impossible for DP-SGD. The core methodological idea is sound and the experimental evidence is robust even after controlling for architecture.

The Theorem 4.1 error is the most significant issue — it must be fixed. However, the fix is straightforward (replacing δ² with b₀² in the denominator follows from the standard RDP composition formula given the mechanism in eq. 4), and the experimental privacy accounting appears consistent with standard practice. The grouped pseudo-classes explanation is thinner than desirable but is not a fatal gap given the strong empirical results and the reference to the appendix.

With the theorem corrected and the presentation tightened, this paper would make a strong contribution to the DP literature.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>