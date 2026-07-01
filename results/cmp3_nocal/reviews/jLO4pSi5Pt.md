Now I have all the information I need. Here is the final consolidated review.

---

## Summary

This paper proposes L-TTA, a method for test-time adaptation (TTA) of vision-language models under long-tailed test distributions. It identifies two VLM-specific failure modes (Text-induced Tail Erosion and Modality-bias Amplification) and introduces three co-designed components: Synergistic Prototypes (DPs + EPs) for maintaining multi-modal features, Rebalancing Shortcuts for dynamic class balancing, and Balanced Entropy Minimization (BEM) as a long-tailed variant of standard entropy minimization. Experiments across 15 datasets, three imbalance ratios, and four backbones show consistent improvements over 12 baselines.

## Strengths

1. **Well-motivated problem framing grounded in VLM-specific failure modes.** The paper identifies two concrete failure mechanisms (Text-induced Tail Erosion and Modality-bias Amplification, Section 1, Figure 1b) that go beyond simply noting that TTA suffers under class imbalance. These are specific to the cross-modal nature of VLMs and directly inform the method's design choices.

2. **Consistent and broad empirical advantage.** Tables 1–3 and 5 show L-TTA outperforming 12 baselines across 15 datasets, three imbalance ratios (10, 20, 50), three benchmarks (OOD, cross-domain, corruption), and four backbones (ViT-B/16, ViT-L/14, ViT-H/14, SigLIP-L/16, MetaCLIP-BigG). The macro-F1 gains (e.g., +2.20% averaged across cross-domain datasets, +2.64% on corruption) indicate genuine rebalancing beyond accuracy improvements on head classes.

3. **Systematic ablation evidence.** Table 6 ablates each of the three components (DP, EP, RS, BEM) across two backbones, with each component removal producing measurable degradation (e.g., 3–4% macro-F1 drops when removing DP or EP). This is cleaner and more comprehensive than many papers in this area.

4. **Competitive computational efficiency.** Table 4 shows L-TTA completes in 1.45 hours vs. 18.3h for RLCF and 27.7h for WATT, while achieving higher harmonic-mean accuracy, demonstrating practical utility.

## Weaknesses

### Fatal

None.

### Major

1. **Missing comparison against simple LT-augmented versions of existing TTA methods.** The paper argues (line 134) that "when combining class priors into the logits for rebalancing like what logit adjustment (Menon et al., 2020) or balanced softmax (Ren et al., 2020) did, we may further exacerbate the model's bias toward the head classes." This claim is central to motivating BEM, yet the paper never tests it. The reader is asked to accept on faith that standard EM + logit adjustment fails and that the three-component design is necessary. The minimal missing baselines are: (a) TPT/DPE/SCAP + logit adjustment at inference, and (b) standard EM with class-weighted prediction post-processing. Without these, we cannot determine whether the improvements come from the sophisticated design or simply from adding any class-balancing signal. Table 6 shows BEM improves over standard EM, but this does not address whether simpler LT adaptations of existing TTA methods would match or approach L-TTA's performance.

2. **Exclusionary Prototype (EP) mechanism has an unresolved semantic validity concern.** Equation (5) updates EP for *every* class *c* using *every* view's features, with weight φ_c ≈ 1 for non-predicted (typically tail) classes. This means a tail class's EP aggressively accumulates features from samples of *all* classes — predominantly head-class samples that appear more frequently. The paper claims EP "enrich[es] tail class representations" (line 98), but it is not established that the accumulated features in a tail-class EP are semantically representative of that class at all. TDA's negative cache (cited as a contrast, line 110) at least stores features filtered by prediction entropy for a *predicted* class. Evidence that EP vectors actually correlate with their assigned classes is needed — e.g., nearest-neighbor retrieval showing EP vectors for tail classes retrieve images of that class, or visualization showing EP features clustered near their true class representations.

### Minor

3. **No variance or significance statistics despite reporting 5 runs.** The paper states "We conduct 5 runs for each experiment" (Table 1 caption) but reports only point estimates. Several gains are small (e.g., +0.03% accuracy on ImageNet-V2 at imb=20: 67.29 vs. 66.61 for WATT; +0.79% on ImageNet-S at imb=10: 50.25 vs. 49.32 for DPE). Without standard deviations or confidence intervals, it is unclear whether these differences are meaningful or within run-to-run noise — especially since the paper's own hyperparameter sweeps (Figure 4) show that varying λ₁, λ₂, η, or β by small amounts causes swings of 1–2%, the same magnitude as some claimed improvements.

4. **The theoretical propositions are substantively shallow.** Proposition 1 (head-class gradients are negative, tail-class gradients are positive) is a straightforward consequence of class imbalance amplifying existing prediction biases — more observation than theorem. Proposition 2 (the head-tail gradient gap shrinks under BEM) follows almost directly from BEM's construction. Neither result is wrong, but framing them as "propositions with proofs in the appendix" (line 134, 144) suggests a depth the content does not support. The paper would be better served by presenting these as intuitive formalizations.

5. **Implementation vs. ablation discrepancy for hyper-parameter K.** The implementation details (line 207–208) state K = 0.3 (number of hyper-class vectors in RSs), but the ablation study (line 334, Figure 4c) finds that "setting K = 0.2 yields the best performance." This inconsistency needs clarification — either the stated default is wrong, or the ablation's "best" value was not used in the main experiments.

6. **Potential circular dependency in BEM not discussed.** The penalty term (1 − \tilde{P})^β in Eq. (9) reduces the prior penalty for confident predictions. If the model confidently misclassifies a tail-class sample as a head class, then (1 − \tilde{P}) is small, the penalty is weak, and the bias toward head classes persists. The paper does not discuss or test this failure mode, though the overall results suggest it does not dominate in practice.

7. **"First attempt" / "first study" framing is slightly overbroad.** The Related Work (line 58–59) acknowledges DELTA (Zhao et al., 2023a) and SAR (Niu et al., 2023), which address class bias in TTA. The paper's actual novelty is in addressing *VLM-specific* LT-TTA challenges (cross-modality misalignment, text-prior bias). The abstract and contributions should be precise about this narrower claim.

### Trivial

8. **Equation (4) notation ambiguity.** The denominator of the DP update formula reads `\|N_{c^*,s}^{\text{DP}} - 1\|\mathbf{v}_{c^*} + \tilde{\mathbf{v}}_{c^*}\|` where it is unclear whether the Euclidean norm wraps the whole sum or only the first term. The intended meaning (norm of the sum) is clear from context but the notation should be clarified for reproducibility.

## Nice-to-Haves

- **Class prior stability analysis.** The class prior π is "continually updated based on the current predicted pseudo-labels" (line 138), creating a risk of error accumulation if early predictions are wrong. An analysis tracking estimated π vs. ground-truth cardinality over the data stream would increase confidence in robustness.
- **Test-data ordering specification.** The paper constructs long-tailed test sets via random sampling (line 206) but does not specify the sequential ordering used in Tables 1–3. Table 7 studies one ordering variant, but the default ordering should be stated.
- **CRA mechanism visualization.** The claim that CRA loss "ensure[s] discernable feature clustering and reduc[es] dominance of head-class prototypes" (line 120) could be substantiated with attention matrix visualizations or hyper-class vector analysis.

## Removed Points

These points are flagged to be removed; treat them with caution if referenced elsewhere.

- **Figure 4 formatting (reviewer note about garbled y-axis).** This is a PDF parsing artifact (the figure is an embedded image); the original submission does not have this issue. Removed per Hard Rules.
- **Equation (4) ambiguity as a "formatting issue" claimed by the reviewer.** Kept as a trivial notation concern (see Weakness #8) because it genuinely affects reproducibility, but the reviewer's framing as a larger "formatting issue" is moderated.
- **"Strengthening the Paper on Its Own Terms" experiments.** The suggestion to strip L-TTA into sub-combinations is partially addressed by Table 6 (which already ablates components), so the "missing baseline" framing of that suggestion is absorbed into Weakness #1 (LT-augmented baselines). The specific additional experiments suggested (TPT + reweighted entropy) are constructive proposals, moved to Weakness #1's framing.

## Novel Insights

The most interesting observation from the review is the tension between the EP mechanism's design (updating *all* class prototypes from *every* sample) and the semantic validity of those stored features for tail classes. This is a genuinely non-obvious failure mode that the paper does not address. If verified, it could motivate a more principled update gating mechanism. Conversely, if the EPs are empirically shown to retrieve semantically correct tail-class features despite being updated with cross-class samples, that would be a noteworthy finding about the robustness of the soft-weighting scheme. Currently the paper provides neither the evidence nor the counter-evidence, leaving a meaningful gap.

## Suggestions

1. **Add LT-augmented baselines.** Run TPT, DPE, and SCAP with logit adjustment (Menon et al., 2020) applied at inference, and with post-hoc class-balanced softmax. If these underperform L-TTA, the paper's architectural claims are supported. If they match L-TTA, the contribution should be reframed around efficiency and simplicity rather than necessity of the three-component design.
2. **Validate EP semantic content.** For each class, retrieve the top-K nearest images to its EP vector from the test stream and report the fraction belonging to that class, broken down by head vs. tail. This directly addresses whether EPs for tail classes are semantically meaningful or noise accumulators.
3. **Report standard deviations.** Add error bars or std dev values to Tables 1–3 for the 5 claimed runs.
4. **Resolve the K inconsistency** between the stated default (K=0.3) and the ablation finding (K=0.2).
5. **Moderate the novelty claims** to specify "VLM-specific long-tailed TTA" rather than "the first" to solve LT-TTA broadly.

## Score and Decision

<score>7</score>
<decision>Accept</decision>