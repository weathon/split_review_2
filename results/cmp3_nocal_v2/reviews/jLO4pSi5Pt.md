Now I'll produce the final consolidated review.

---

## Summary

This paper introduces L-TTA, the first method designed for test-time adaptation (TTA) of vision-language models under long-tailed test distributions. It proposes three co-designed components — Synergistic Prototypes (dual DPs and EPs), Rebalancing Shortcuts with a class re-allocation loss, and Balanced Entropy Minimization — to address head-class bias during online adaptation. The method is evaluated across 15 datasets, three imbalance ratios, 11 baselines, and multiple backbone architectures, consistently showing gains in both accuracy and macro-F1.

## Strengths

1. **Well-motivated problem framing.** The paper is the first to identify and formalize the long-tailed TTA setting for VLMs, highlighting two concrete failure modes (Text-induced Tail Erosion and Modality-bias Amplification, §1, Figure 1b) that are specific to VLM-based TTA under imbalance. The problem is timely and practically relevant.

2. **Thorough empirical evaluation.** The method is tested across 15 datasets in three benchmarks (OOD, Cross-Domain, Corruption), at three imbalance ratios (10, 20, 50), against 11 baselines covering prompt-tuning, training-free, and visual-adaptation methods (Tables 1–3). Results are also reported on four additional backbones (ViT-L/14, ViT-H/14, SigLIP-L/16, MetaCLIP-BigG) in Table 5. This breadth credibly demonstrates that L-TTA is not a one-dataset or one-backbone method.

3. **Consistent macro-F1 gains.** The paper reports macro-F1 alongside accuracy, which is the right metric for long-tailed settings. L-TTA achieves the best macro-F1 on nearly every dataset × imbalance combination, with non-trivial margins (e.g., 61.18 vs. 59.65 next best on OOD Average at Imb=10; 63.44 vs. 61.24 on Cross-Domain Average).

4. **Good efficiency-accuracy trade-off.** L-TTA runs in 1.45h on ImageNet (Table 4), substantially faster than several baselines (RLCF: 18.30h, WATT: 27.70h) while outperforming them. The design choice to keep prompts frozen and avoid backprop through the encoder is practical and well-justified.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

1. **BEM notation ambiguity (Eq. 9, §3.2).** The variable $\tilde{\mathbb{P}}$ in $\mathcal{L}_{\text{BEM}} = \mathbb{H}'(\tilde{\mathbb{P}}) = -\sigma(z') \log(\sigma(z')),\; z' = z - (1 - \tilde{\mathbb{P}})^\beta \log(\pi / \sum \pi_i)$ is never explicitly defined. The most natural reading is $\tilde{\mathbb{P}} = \sigma(z)$ (the original predictions before adjustment), but the paper does not state this. The notation $\mathbb{H}'(\tilde{\mathbb{P}})$ is also misleading — the function computes entropy on $\sigma(z')$, not on $\tilde{\mathbb{P}}$ itself. This not a circular dependency (there is no fixed-point problem under the natural interpretation), but it creates unnecessary confusion and should be clarified.

2. **Exclusionary Prototype (EP) mechanism lacks evidence for the claimed semantics (§3.2, Eq. 5).** The paper claims EPs store "the most improbable features of each class" and capture "exclusionary" information. However, the update rule (Eq. 5) adds the current visual embedding to *every* class's EP simultaneously, only modulating the EMA decay factor via $\phi_c$. For a sample predicted as "dog" with 90% confidence, the "cat" EP still receives the dog feature with weight ~1, just with marginally less retention of the old prototype. Over many steps, all class EPs will be weighted averages of all seen embeddings, differentiated only by the subtle $\phi_c$ weighting differences. The paper provides no analysis (e.g., nearest-neighbor retrieval, t-SNE) demonstrating that EPs actually encode complementary/exclusionary information relative to DPs. The empirical contribution of EPs (~1% macro-F1 gain in Table 6, SyP+RS vs. DP+RS) is real, but whether it stems from the claimed "exclusionary" semantics or simply from extra parameters and EMA smoothing is not established.

3. **Theoretical propositions are too vague to carry weight (Propositions 1 and 2, §3.2).** Both propositions depend on splitting classes into head/tail "with certain measurements" without specifying how this split is determined or under what assumptions about the data distribution or model it holds. The statements lack formal connection to the model architecture, class cardinalities, or adaptation dynamics. These are better framed as intuitive motivation for BEM than as formal theoretical results.

4. **No variance reporting despite multiple runs.** The paper states it performs "5 runs for each experiment" (Table 1 caption, p. 154) but reports only point estimates. Given that long-tailed test sets are constructed by random subsampling and data-stream ordering affects TTA, standard deviations or confidence intervals are needed to assess whether the reported margins (often 1–3% macro-F1) are significant relative to run-to-run variance.

### Trivial

- **Table 7 presentation.** The extracted table shows formatting issues (extra columns, repeated $\epsilon$ values). The robustness claim is still readable, but the table structure should be checked in the original PDF.

## Nice-to-Haves

- **Baseline with LT corrections applied to existing TTA methods.** A natural control experiment is to take a strong existing TTA method (e.g., TDA, DPE) and apply logit adjustment or post-hoc class-balancing during its entropy minimization step. This would help isolate whether L-TTA's gains come from its novel architecture or simply from adding any LT-aware correction to TTA.
- **Quantitative diagnostics for the two failure modes.** The paper identifies "Text-induced Tail Erosion" and "Modality-bias Amplification" as motivations. Controlled experiments quantifying these (e.g., per-class accuracy breakdowns showing that standard TTA methods degrade tail classes specifically, or that unimodal TTA on VLM backbones causes modality mismatch) would further strengthen the motivation.

## Removed Points

These points were raised in the input review but are removed with justification:

1. **"Figure 1(b) evidence is never presented in the main paper."** The paper text explicitly refers to Figure 1(b) as demonstrating these failure modes (line 38). The evidence is in the figures, which cannot be inspected in the parsed text. Not verifiable.
2. **"Formatting issues in Eq. 4 denominator."** This is a PDF-parser artifact, not an author error.
3. **"Proofs deferred to appendix (cannot evaluate)."** Deferred proofs are standard; the appendix exists in the original submission.
4. **"Modality-bias Amplification failure mode never directly diagnosed."** The paper claims Figure 1(b.2) contains this evidence. Not verifiable from parsed text.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a genuine tension in the EP design (the claimed "exclusionary" property is not supported by the update rule's mathematics as clearly as stated) and the BEM notation ambiguity, but neither review identifies a fundamentally novel angle or an unforeseen implication of the results.

## Suggestions

1. Explicitly define $\tilde{\mathbb{P}}$ in Eq. 9 (should be $\sigma(z)$, the original predictions before BEM adjustment) and clean up the notation.
2. Add a diagnostic analysis for EPs: for a few classes, retrieve the nearest training images to their DP and EP vectors. If the dog EP retrieves cat images (things that are *not* dogs but are confusable), the exclusionary claim is supported; if it retrieves random or similar images, revise the claim.
3. Report standard deviations or confidence intervals for the main results (Tables 1–3).
4. Reframe Propositions 1 and 2 as intuitive motivation with explicit assumptions, or sharpen them into genuine formal statements.
5. Add an ablation applying logit adjustment to a baseline TTA method to disentangle the effect of LT correction from architectural novelty.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>