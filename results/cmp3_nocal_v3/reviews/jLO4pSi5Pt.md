## Summary

This paper proposes L-TTA, the first method for test-time adaptation (TTA) of vision-language models (VLMs) under long-tailed test distributions. It identifies two failure modes specific to VLM-based LT-TTA (Text-induced Tail Erosion and Modality-bias Amplification) and introduces three co-designed components: Synergistic Prototypes (SyPs) with Deterministic and Exclusionary prototypes to enrich tail-class representations, learnable Rebalancing Shortcuts (RSs) for dynamic adaptation, and Balanced Entropy Minimization (BEM) as a modified objective to counteract head-class bias. Extensive experiments on 15 datasets across three benchmarks (OOD, cross-domain, corruption) with imbalance ratios 10/20/50 show consistent improvements over 11+ baselines in both accuracy and macro-F1.

## Strengths

- **Well-motivated problem framing (Section 1).** The paper identifies a genuine gap: existing VLM TTA methods are evaluated on (nearly) balanced datasets, but real-world test streams can be long-tailed. The two identified failure modes — Text-induced Tail Erosion and Modality-bias Amplification (Figure 1) — are specific to *VLM-based* TTA and go beyond what would apply to unimodal long-tailed TTA. This concrete analysis makes the motivation substantially stronger than a generic "long-tailed test sets are harder" framing.

- **Comprehensive evaluation (Tables 1-3, 5).** The experimental design is thorough: 15 datasets across three benchmark types (OOD, cross-domain, corruption), three imbalance ratios (10, 20, 50), 11+ baselines, and both accuracy and macro-F1 reported. The inclusion of macro-F1 is essential for a long-tailed evaluation, and many baselines show a notable macro-F1 gap that L-TTA narrows. Results on four additional backbones (ViT-L/14, ViT-H/14, SigLIP-L/16, MetaCLIP-BigG) strengthen generalizability claims.

- **Consistent empirical advantage.** Across nearly all settings in Tables 1-3, L-TTA places first or close to first. The gains are more consistent for macro-F1 than accuracy, which is the expected pattern for a method claiming to improve class balancing. The margins persist across diverse conditions (OOD, cross-domain, corruption) and are not cherry-picked.

- **Ablation isolating component contributions (Table 6).** The ablation cleanly shows that each component (DP, EP, RS, BEM) contributes positively, and the full combination is best. This meets the minimum bar for a multi-component method, and the gradual degradation pattern (rather than all-or-nothing) lends credibility to the design.

## Weaknesses

### Fatal
None.

### Major

1. **Unclear treatment of test-set class priors in BEM and missing analysis of prior estimation (Eq. 9, line 138).** The BEM loss (Eq. 9) incorporates class priors π. The paper states these are "set to the cardinality of all classes ... in default" and are "continually updated based on the current predicted pseudo-labels." This is ambiguous: if the *default initialization* uses the true test-set cardinalities (which are known by construction in the controlled benchmark), the method has access to oracle information about which classes are head/tail and by how much — information unavailable in a genuine TTA scenario. If instead the priors are purely estimated online from pseudo-labels (as the "continually updated" clause suggests), the paper provides no analysis of estimation quality: no ablation comparing oracle vs. estimated priors, no analysis of convergence speed (especially for tail classes that may appear rarely early in the stream), and no discussion of how many samples are needed before estimates stabilize. This is not a fatal flaw — the paper explicitly describes online estimation — but the missing analysis and ambiguity are significant gaps given that BEM is a core claimed contribution.

2. **Hyperparameter inconsistency for K (lines 208 vs. 334).** The implementation details (line 208) state K = 0.3 as the default for the number of hyper-class vectors in RSs. However, the ablation study (Section 4.2, line 334) explicitly states: "Our experiment results show that setting K = 0.2 yields the best performance." If K=0.2 is optimal on the datasets tested, using K=0.3 for all main experiments is unexplained. This inconsistency undermines confidence in whether reported results use optimal hyperparameters. The paper should either use K=0.2 for main experiments, or explain why K=0.3 is preferable despite the ablation finding.

### Minor

3. **Missing variance statistics (Tables 1-3).** The paper states "5 runs" are conducted in captions but reports only point estimates without standard deviations. For a method with multiple interacting hyperparameters (λ₁, λ₂, η, K, β, θ), variance information would help assess whether reported margins over baselines are statistically robust.

4. **No failure-case analysis.** The evaluation shows L-TTA works better than baselines on average, but there is no discussion of settings where improvement is marginal (e.g., Aircraft in Table 2 shows only ~1% accuracy gain over DPE) or whether any condition degrades performance relative to a baseline. Analyzing where the method struggles would strengthen scientific rigor.

5. **Theoretical propositions are relatively shallow (Section 3.2, Propositions 1-2).** Proposition 1 (entropy gradient sign separates head/tail classes) and Proposition 2 (BEM narrows the gradient gap) are framed as formal propositions with proofs deferred to the appendix. In practice, they are fairly direct consequences of the definitions of entropy and the BEM penalty term. The paper would be better served presenting these as intuitive justifications rather than formal claims.

6. **Missing "TTA + rebalancing" baseline.** The paper argues in prose (lines 134-135) that combining standard TTA with logit adjustment or balanced softmax "may further exacerbate the model's bias" but provides no experiment to support this. Adding a baseline like TPT + logit adjustment or TPT + re-weighted entropy would help isolate whether the gains come from BEM's specific design or from adding any form of rebalancing.

### Trivial
7. **Corruption benchmark scope (Table 3).** The main corruption results use only Gaussian noise (ℓ ∈ {0.1, 0.2, 0.4}) with imb=10. The paper references 16 other corruption types in Appendix J but these are not in the main paper.

## Nice-to-Haves
- An ablation comparing oracle (ground-truth) vs. online-estimated class priors for BEM.
- An analysis of whether tail-class prototype quality (EPs/DPs) lags behind head-class quality over the course of the test stream.
- A conceptual verification experiment for the EP update mechanism (Eq. 5), which updates *all* class prototypes for every view — this circular dependency (good EPs require good predictions, good predictions require good EPs) deserves analysis.

## Removed Points
- *"The BEM loss reliance on class priors is a structural/fatal flaw"* — The paper explicitly states the prior is "continually updated based on the current predicted pseudo-labels," describing an online estimation approach. The valid concern is about missing analysis, not a fundamental design flaw.
- *"Figure caption repetitions"* — These are parser artifacts, not a paper problem.
- *"Equation (1) over-specifies the CLIP architecture"* — A presentation preference; the notation, while dense, is functional.
- *"Corruption severity metric ℓ is non-standard"* — Gaussian noise with controlled variance is a reasonable choice; requiring ImageNet-C alignment is scope creep.
- *"Missing related work"* — Not verifiable without external sources.

## Novel Insights
None beyond the paper's own contributions. The review confirms the paper's stated strengths and identifies gaps that the authors themselves would need to fill.

## Suggestions
1. Clarify the class prior initialization for BEM: specify whether "set to the cardinality of all classes" means the true test-set cardinalities (known in the controlled benchmark but not in deployment) or a uniform prior that is then updated online. Provide an ablation separating oracle vs. online-estimated priors.
2. Resolve the K inconsistency by either using K=0.2 (the ablation optimum) in main experiments, or explaining why K=0.3 is preferred and how the ablation figure was interpreted.
3. Add error bars (standard deviations over 5 runs) to all main tables.
4. Include a baseline that combines an existing TTA method (e.g., TPT) with a simple rebalancing technique (logit adjustment or re-weighted entropy) to empirically validate the claim that this combination fails.
5. Add a brief discussion of conditions where L-TTA shows marginal or no improvement.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>