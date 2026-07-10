Now let me finalize the review with calibrated scoring.

## Summary

This paper identifies and formally characterizes the "label dependency" problem in semi-supervised learning (SSL) — the phenomenon that SSL's ability to exploit unlabeled data degrades sharply when labeled data is scarce or low-quality. To address this, the authors propose CaPT (CLIP as a Prior Teacher), an asymmetric-modalities co-training framework that jointly trains a fully fine-tuned unimodal vision network and a parameter-efficiently fine-tuned CLIP model. Co-pseudo labels with entropy-based weighting enable bidirectional knowledge exchange. CaPT achieves state-of-the-art results across multiple SSL benchmarks, with particularly striking gains in extreme low-label regimes (e.g., +21.38% on CIFAR-100 with one label per class).

## Strengths

- **Well-motivated problem with formal grounding.** Section 1 convincingly demonstrates both empirically (Figures 1a, 1b) and theoretically (Theorem 1.1) that SSL methods degrade sharply when labeled data is scarce or low-quality. The theorem bounding pseudo-label error in terms of prototype bias and sample size is a genuine conceptual contribution that formalizes the intuition that SSL's unlabeled-data utilization is coupled to labeled data quality.
- **Thoughtfully designed and thoroughly ablated method.** The three-module architecture (UPM, MPM, PFM) with entropy-based co-pseudo-label weighting is non-trivial, and each design choice is validated in a comprehensive ablation study (Table 6). Feature-augmented consistency regularization (feature-level Mixup) is a practical efficiency innovation for frozen CLIP encoders.
- **Strong results in the most challenging regime.** The one-label-per-class results (Table 3) — especially 21.38% improvement over the second-best method on CIFAR-100 and 4.05% on EuroSAT — demonstrate genuine value where SSL fails most dramatically.
- **Broad evaluation scope.** The paper evaluates across standard SSL benchmarks (USB), large-scale ImageNet, extreme low-label regimes, and fine-grained datasets, providing a comprehensive empirical characterization.

## Weaknesses

### Major

- **Missing direct comparisons against CLIP+SSL baselines in main tables.** The primary comparison set (Tables 1, 2, 3) comprises SSL methods without any vision-language model, while CaPT uses CLIP (trained on 400M image-text pairs). These comparisons demonstrate that "adding CLIP to SSL helps" but do not directly establish that CaPT's *specific co-training framework* is superior to other CLIP+SSL integration approaches. DebiasPL (Wang et al., 2022a) and CLIP-Adapter — the most directly relevant prior work — appear only in the ablation study as reimplementations (CaPT-Deb, CaPT-Ada), not in the main benchmark tables. Without head-to-head comparisons in the primary experiments, the claim that CaPT's framework is the best way to integrate CLIP into SSL is not fully substantiated.

### Minor

- **STL-10 anomaly unaddressed.** On STL-10 (Table 1), CaPT's unimodal network (96.07% with 4 labels, 96.34% with 10 labels) underperforms both its own adapter-tuned CLIP (96.86%, 97.15%) and zero-shot CLIP (97.18%). The paper highlights CaPT's 6.18% lead over RegMixMatch but does not discuss why the co-trained unimodal network does not surpass the CLIP branch alone on this dataset. This is a notable omission in presentation that the authors should acknowledge and analyze.
- **"Pattern-homogeneity bottleneck" evidence is primarily qualitative.** The claim that asymmetric-modalities design mitigates a representational bottleneck relies mainly on attention maps for 8 example images (Figure 3). The ViTs being compared differ in training data, objective, and architecture — not just modality — so the specific role of modality asymmetry is not isolated. Additional experiments are referenced in Appendix B (stripped), but the core evidence for this mechanism remains anecdotal.
- **Theoretical bound is vacuous for realistic dimensions.** Theorem 1.1 contains a 2^(d/2) factor that makes the bound numerically vacuous for image dimensions (d = 3×224×224). While useful as a conceptual tool illustrating the *structure* of label dependency, this limitation should be acknowledged rather than implied to be practically meaningful.

### Trivial

None.

## Nice-to-Haves

- On FGVC Aircraft (5 labels, Table 5), CaPT (50.12%) slightly underperforms FreeMatch (51.43%). The paper mentions this in the conclusion but does not analyze the failure mode. Understanding why CLIP's prior is unhelpful here could yield useful insights.
- The thresholding mechanism (line 196) that replaces low-confidence predictions with all-zero vectors is described in a single sentence and its impact is not ablated separately.

## Removed Points

- **Theory-method disconnection (from Harsh Critic's Critical Issue 3):** The critic argued that Theorem 1.1 (bounding pseudo-label error for a nearest-prototype classifier) and the CaPT method (using deep networks with consistency regularization) are disconnected. However, the paper does not claim the theory informs CaPT's architectural design — it claims the theory establishes the *label dependency problem*, while CaPT is presented as a *solution* to that problem. The problem-solution framing is standard and not a weakness.
- **FGVC Aircraft underperformance:** The paper already acknowledges this limitation in its conclusion section. The critic's observation is valid but the paper is transparent about this failure case.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Include DebiasPL and CLIP-Adapter (or their closest published variants) as proper baselines in the main benchmark tables (Tables 1-3), not just in the ablation study, to directly substantiate the claim that CaPT's specific framework is advantageous over simpler CLIP+SSL integration approaches.
2. Discuss the STL-10 anomaly explicitly: analyze why the co-trained unimodal network underperforms the adapter-tuned CLIP branch on this dataset, and report per-branch accuracy to give a complete picture.
3. Add a more controlled experiment for the "pattern-homogeneity bottleneck" claim — e.g., co-training two vision-only ViTs with different architectures/pretraining to isolate the effect of modality asymmetry.
4. Acknowledge the 2^(d/2) factor limiting the bound's numerical applicability and discuss whether tighter bounds are possible.

## Score and Decision

The paper makes a genuine contribution: it identifies and formally motivates the label-dependency problem in SSL, and proposes a well-designed framework (CaPT) with strong empirical results, thorough ablation, and favorable efficiency. The primary evidential gap — absence of direct CLIP+SSL baselines in main tables — is partially addressed by the ablation study but should be closed. The remaining weaknesses are minor presentation issues. Overall, the paper presents a solid, practical contribution with clear empirical validation.

**Score: 7.5**  
**Decision: Accept**

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>