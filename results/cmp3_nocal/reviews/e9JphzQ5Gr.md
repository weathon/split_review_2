Now I have all the information needed. Let me produce the final consolidated review.

---

## Summary

This paper identifies that SSL methods remain label-dependent — their unlabeled-data utilization degrades when labeled data is scarce or of poor quality. The authors propose CaPT, an asymmetric-modalities co-training framework that integrates CLIP (via lightweight adapters) with a standard unimodal vision network through co-pseudo labels with entropy-based weighting. The method is evaluated across numerous benchmarks (USB, ImageNet, fine-grained datasets) and consistently outperforms existing SSL methods, especially in extreme low-label regimes (e.g., +21.38% on CIFAR-100 with one label per class), while adding only ~10% overhead.

## Strengths

1. **Well-motivated problem with clear empirical grounding.** Figure 1a-c convincingly demonstrates that SSL performance collapses when labeled data drops to one sample per class and that the *quality* of those few labels matters. This observation (label dependency beyond simple scarcity) is genuine and the paper provides both empirical and theoretical formalization.

2. **Consistent, large-margin improvements across many settings.** The results are strong and reproducible across diverse conditions: +4.09% on CIFAR-100 with 2 labels/class (Table 1: 84.83 vs. 80.74), +9.33% on ImageNet with 10 labels/class (Table 2: 67.68 vs. 58.35), +21.38% on CIFAR-100 with 1 label/class (Table 3: 82.51 vs. 61.13). These are not marginal gains; they represent a qualitatively different operating regime.

3. **Genuinely efficient integration of CLIP.** Table 4 shows CaPT uses only 8% more memory and 11% more training time than the unimodal FreeMatch baseline, while achieving substantially higher accuracy. The asymmetric-modalities + PEFT design is convincingly justified.

4. **Thorough ablation study.** Table 6 systematically tests five ablated variants (CaPT-Ada, CaPT-Deb, CaPT-Uni, only UPM, only MPM) plus feature-augmentation and weighting ablations. Each variant isolates a concrete design decision, and the results cleanly show that all components contribute.

## Weaknesses

### Fatal
None.

### Major
None. The paper's empirical core is sound, and the weaknesses listed below are addressable without invalidating the central contribution.

### Minor

1. **No direct comparison with CLIP-aware SSL baselines.** The paper positions itself against DebiasPL and CLS (Section 2) but does not include them in the main experimental tables. The ablation study includes CaPT-Ada and CaPT-Deb, which approximate aspects of these methods, but these are ablated variants of the proposed framework rather than independently implemented competitive methods. A reader cannot fully assess whether CaPT's specific co-training mechanism adds value over simpler alternatives such as (a) using CLIP zero-shot predictions as static pseudo-labels for SSL training, or (b) DebiasPL's approach of expanding the labeled set with CLIP's high-confidence predictions. This does not undermine the paper's primary contribution (outperforming standard SSL methods), but it weakens the claim that CaPT's *specific design* is optimal among CLIP+SSL approaches.

2. **Theorem 1.1 is disconnected from the method.** The theorem bounds pseudo-label error under a Gaussian-mixture model, showing that degradation depends on label quantity and quality. This formalizes the *problem* but does not analyze CaPT, motivate its specific design choices (asymmetric modalities, co-training, entropy weighting), or predict how the method improves the bound. The paper's Contribution 1 ("theoretically establish the label dependency that constrains SSL") is accurate as stated, but readers expecting theory that guides or explains the method will be disappointed. The theorem adds framing value, not analytical value, to the core contribution.

3. **No variance reported for the one-label-per-class setting (Table 3).** Unlike Table 1 (which reports mean ± std over 3 seeds), Table 3 shows only single numbers. Since Figure 1a demonstrates that performance at one-label-per-class varies dramatically depending on *which* sample is selected (Set 0 vs. Set 2), the absence of variance information makes it impossible to assess the stability of the 21.38% gap. The paper should report multiple seeds with standard deviations for this setting.

4. **Pattern-homogeneity bottleneck claim relies on qualitative evidence.** Figure 3 shows attention maps for 8 images to argue that two ViTs with different initializations exhibit "pattern homogeneity" while CLIP diverges. This is anecdotal. A quantitative measure (e.g., CKA similarity, representation dissimilarity) would substantiate the claim. The paper references Appendix B for additional experiments, but the main-text evidence is thin for a claim that is used to motivate the core architectural choice of asymmetric modalities.

5. **Label selection protocol for Table 3 is unspecified.** Given that Section 1 clearly demonstrates label *quality* matters enormously at one-label-per-class (accuracy varies by >20 points between Set 0 and Set 2), the paper must specify how the single labeled sample per class was selected for the experiments in Table 3. Without this, the results are not reproducible and their comparability to prior work is unclear.

6. **The benefit of bidirectional "mutual learning" is modest.** Ablation CaPT-Uni (which removes the unimodal→CLIP information flow, retaining only CLIP→unimodal) loses only 0.88% on CIFAR-100 and 1.49% on EuroSAT (Table 6). This suggests that most of CaPT's gain comes from the CLIP→unimodal direction and that the bidirectional exchange touted in the paper's framing is marginally beneficial rather than "crucial" as claimed. The paper acknowledges this but the framing overstates the role of bidirectionality.

### Trivial

- The ImageNet experimental setup (Section 4.2) states "Similar to RegMixMatch, we use MAE pre-trained ViT-B as the training backbone for UPM." It is unclear whether RegMixMatch itself also uses MAE pre-trained ViT-B, which matters for whether the comparison is controlled. This should be clarified.
- Equation 13 combines one-hot pseudo-labels via convex weighting to produce a soft co-pseudo-label. The paper does not explicitly state whether the resulting target is soft or hard for the consistency loss (Equation 15). The use of standard cross-entropy implies a soft target, but this should be stated explicitly.

## Nice-to-Haves

- A symmetric co-training baseline (two vision models, or two CLIP models) would directly test the "asymmetric modalities" claim. Currently the paper only compares against unimodal-only and CLIP-only variants, which does not isolate asymmetry from simply having more parameters.
- Ablating the sensitivity to FreeMatch's adaptive threshold strategy would be informative, since CaPT inherits this hyperparameter from prior work.
- A quantitative measure (e.g., CKA) of representation similarity between ViT(θ₁), ViT(θ₂), and CLIP would strengthen the pattern-homogeneity bottleneck claim beyond qualitative attention maps.

## Removed Points

These points were flagged for removal; treat them with caution:

- *"The comparison is structured so that the strongest baselines cannot win"* — This overstates the issue. The paper compares against 12 standard SSL methods across controlled benchmarks (USB, ImageNet), which is appropriate for its stated claim of outperforming SSL methods. The absence of CLIP-aware baselines is real but the paper does not "structure" the comparison unfairly.
- *"Theorem merely states that if you have fewer or worse labels, pseudo-labels are worse"* — This undersells the theorem, which provides a specific exponential bound with explicit dependencies on prototype bias (B), sample size (n_min), inter-class distance (g), and noise variance (σ²). The formalization goes well beyond stating the intuition.
- *"21.38% is a one-datapoint result under a single extreme setting"* — While the variance concern is valid, CaPT also shows consistent gains on CIFAR-10 (+0.72%) and EuroSAT (+4.05%) in the same table, and the pattern holds across all settings in Table 1.
- *"CaPT underperforms on FGVCAircraft"* — The paper transparently acknowledges this ("Except for FGVCAircraft, discussed in Appendix N"). This is not a hidden weakness.
- *"Adapter-tuned CLIP often underperforms standard SSL methods — why?"* — The paper explains this at line 37: CLIP-Adapter "fail[s] to capture the diversity present in SSL training data" due to limited learnable parameters. This is briefly but adequately discussed.

## Novel Insights

The input review's key insight beyond the paper's own contributions is that the CaPT-Uni ablation (removing the unimodal→CLIP information flow) loses only ~1%, which undermines the "bidirectional mutual learning" framing. This is a genuine observation that the paper's own data partially contradicts its rhetorical emphasis. Additionally, the observation that the theoretical result (Theorem 1.1) serves as problem motivation rather than method analysis is a meaningful distinction that the paper's contribution list elides. These insights collectively indicate that the paper's strongest contribution is practical (efficiently integrating CLIP into SSL with strong results) rather than theoretical or architectural-novelty-based, and the paper would be improved by acknowledging this boundary more directly.

## Suggestions

1. Add at least one CLIP-aware baseline comparison (e.g., a simple CLIP zero-shot pseudo-labels + standard SSL training baseline, or a re-implementation of DebiasPL) to the main experiments.
2. Report mean ± std over multiple seeds for all one-label-per-class results (Table 3), and specify the selection protocol for the single labeled sample.
3. Tone down the "bidirectional mutual learning is crucial" claim given CaPT-Uni's small degradation, or add evidence that the unimodal→CLIP flow provides value beyond what the ablation captures.
4. Clarify the ImageNet backbone setup: does RegMixMatch also use MAE pre-trained ViT-B?
5. Either strengthen the pattern-homogeneity bottleneck evidence quantitatively or soften the claim.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>