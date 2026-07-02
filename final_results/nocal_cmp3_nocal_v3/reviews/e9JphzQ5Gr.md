Now I have a thorough understanding of the paper and all reviewer claims. Let me produce the final consolidated review.

## Summary

The paper identifies an inherent label-dependency in semi-supervised learning (SSL): pseudo-label quality degrades when labeled data is scarce or low-quality, creating a vicious cycle. It proposes CaPT (CLIP as a Prior Teacher), a co-training framework that jointly trains a fully fine-tuned unimodal network (vision backbone) and a parameter-efficiently fine-tuned multimodal CLIP model. Predictions from both modules are fused via entropy-weighted co-pseudo labels. CaPT achieves state-of-the-art results across 12 baseline methods on standard benchmarks (USB), large-scale ImageNet, extreme low-label settings (one label per class), and fine-grained datasets, with only modest overhead in training time (+11.18%) and memory (+8.00%).

## Strengths

1. **Strong and consistent empirical results across diverse settings.** CaPT outperforms every baseline in every benchmark-configuration pair in the USB evaluation (Table 1), with especially large margins in extreme low-label regimes: +4.09% on CIFAR-100 (2 labels/class), +6.18% on STL-10 (4 labels/class). In the one-label-per-class setting (Table 3), it improves over the second-best method by +21.38% on CIFAR-100 and +4.05% on EuroSAT. On ImageNet (Table 2), CaPT leads by +9.33% at 10 labels/class. The consistency of these wins across 12 baselines, multiple datasets, and varying label counts is the paper's strongest evidence.

2. **Well-motivated problem with supporting analysis.** Both the empirical demonstration (Figure 1 — label quantity/quality driving SSL collapse) and the theoretical bound (Theorem 1.1 — linking prototype bias and sample size to pseudo-label error) convincingly establish that SSL's reliance on labeled data is a fundamental limitation. This motivation is clean and actionable.

3. **Genuinely efficient integration of CLIP.** The runtime/memory comparison (Table 4) shows CaPT adds only 11.18% training time and 8.00% memory over FreeMatch while outperforming it by 6.23%. This is a meaningful practical contribution — the method does not simply throw a second large model at the problem.

4. **Solid ablation isolating each component.** Table 6 cleanly shows: (a) the full CaPT beats all ablated variants, (b) both "only UPM" and "only MPM" are much worse individually, confirming the co-training synergy, (c) feature-augmented consistency and entropy-based weighting each contribute non-trivially, and (d) the CaPT-Ada/Deb/Uni variants map cleanly to the design space in Figure 2.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Theorem 1.1 is motivationally useful but analytically disconnected from the method.** The bound concerns nearest-prototype classifiers under a Gaussian mixture model, while CaPT (and all baselines) use deep neural networks with consistency regularization and pseudo-labeling in an iterative training loop. The theorem does not model representation learning, the SSL training dynamics, or how CLIP integration specifically addresses the bound. Additionally, the $2^{d/2}$ term in the bound (Eq. 1) makes it vacuous for raw pixel-level dimensionality (e.g., $224 \times 224$). The theorem could operate in a lower-dimensional latent space, but this is not stated. The paper would be equally strong without this theorem, as the empirical demonstration in Figure 1 already makes the motivational point.

2. **The comparison is in an asymmetric resource regime.** Standard SSL baselines (FreeMatch, RegMixMatch, FixMatch, etc.) use a single pre-trained ViT backbone (~86M parameters). CaPT uses that same ViT *plus* CLIP ViT-B/32 (another ~86M visual encoder + a text encoder) with adapter modules. While the ablation (Table 6) partially addresses this by showing that CLIP alone ("only MPM," 68.32%) is weaker than the unimodal network alone ("only UPM," 78.60%) and both are weaker than the combined CaPT (84.83%), this does not fully rule out that part of CaPT's advantage comes from the extra model capacity and pre-training data. A stronger control — e.g., providing a baseline SSL method with the same dual-backbone setup — would strengthen this analysis. The paper should be more transparent in the main text about this regime difference rather than leaving it implicit.

3. **Missing a baseline that uses frozen CLIP zero-shot predictions as soft targets without co-training.** The ablation compares against variants of CLIP integration (CaPT-Ada, CaPT-Deb, CaPT-Uni) but does not include a simple baseline where CLIP's zero-shot logits are directly used as soft targets for the unimodal network's consistency loss (without the co-training loop or adapter-tuning). Such a comparison would help isolate whether the co-training framework itself is essential or whether simpler CLIP knowledge distillation achieves comparable gains.

4. **Incomplete reporting of statistical variability.** Standard deviations are reported for the USB benchmark (Table 1, 3 seeds) but not for ImageNet (Table 2) or the one-label-per-class setting (Table 3). Given the substantial improvements claimed, reporting variance for these settings would strengthen the evidence.

### Trivial

1. **The entropy-based weighting (Eq. 11–12) operates at the batch level** — the average entropy over the batch produces a single module weight applied to all samples. This means confident and uncertain samples within the same batch receive identical weights. The paper could discuss whether per-sample weighting would be more appropriate, or justify the batch-level design choice.

2. **The FGVCAircraft limitation** (where CaPT slightly underperforms baselines) is discussed only briefly in the conclusion and deferred to Appendix N. Given that this represents a meaningful failure mode of the approach, a short paragraph in the main experimental section would be more appropriate.

## Nice-to-Haves

- A quantitative analysis of how the two modules' predictions evolve over training (prediction agreement/disagreement curves) would strengthen the "asymmetric-modalities complementarity" claim beyond the qualitative attention maps (Figure 3).
- The paper acknowledges potential CLIP data contamination on standard benchmarks (line 268, Appendix M) and tests on fine-grained datasets as a control. A brief mention in the main text of whether de-duplication against evaluation benchmarks was attempted would further strengthen transparency.
- The bound in Theorem 1.1 would benefit from a brief discussion of its regime of applicability (e.g., latent feature dimension vs. pixel dimension) to address the $2^{d/2}$ vacuity concern.

## Removed Points

These points were considered but removed with justification:

- **"CLIP data contamination confounds the headline results"** — The paper explicitly acknowledges this concern at line 268 ("To preclude any advantage for CaPT arising from potential overlap between CLIP's corpus and simple benchmarks") and references Appendix M for in-depth discussion. The fine-grained results (Table 5) serve as a control. The paper adequately addresses this standard concern for CLIP-based methods.
- **"The paper should discuss whether de-duplication was attempted"** — This is a request for information likely contained in Appendix M (which the parser stripped); the paper clearly states it discusses the issue there.
- **"Per-batch weighting could be suboptimal"** — Kept as trivial but downgraded from the stronger framing; it is a design choice, not an error.
- **"The bound's reliance on d in the exponential term"** — Folded into Minor weakness #1 (theorem disconnection) rather than as a standalone point.

## Novel Insights

The input review does not surface genuinely novel insights beyond the paper's own contributions. The observation that CaPT-Uni (one-way CLIP→vision flow) achieves most of the gain (83.95% vs. 84.83% on CIFAR-100, a drop of only 0.88%) is implicit in Table 6 but worth highlighting: the paper's backward flow (vision→CLIP) contributes positively but modestly. This suggests that the primary mechanism is CLIP providing a reliable prior to the vision model, with bidirectional co-training providing a secondary boost.

## Suggestions

1. Report standard deviations for ImageNet (Table 2) and the one-shot experiments (Table 3).
2. Add a baseline using frozen CLIP zero-shot logits as soft targets for the unimodal network (without co-training).
3. Discuss the model capacity asymmetry in the main text (not just implicitly through the ablation).
4. Add a brief discussion of the bound's $2^{d/2}$ term and its dependence on dimensionality.
5. Move the FGVCAircraft limitation discussion from the appendix into the main experimental section.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>