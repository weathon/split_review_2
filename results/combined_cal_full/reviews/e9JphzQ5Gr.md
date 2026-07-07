Now I have all the calibration data needed. Let me write the final authoritative review.

## Summary

This paper identifies that semi-supervised learning (SSL) methods remain inherently dependent on labeled data quality and quantity, and proposes CaPT, an asymmetric-modalities co-training framework that integrates CLIP into SSL. CaPT jointly trains a unimodal vision network (fully fine-tuned) and CLIP (adapter-tuned), using co-pseudo labels with entropy-based weighting and feature-augmented consistency regularization. The paper demonstrates strong empirical results, particularly in extreme low-label regimes (e.g., +21.38% over the best SSL baseline on CIFAR-100 with 1 label/class), with modest computational overhead.

## Strengths

- **Clear problem identification with empirical and theoretical backing.** Figures 1a-c empirically demonstrate SSL's label dependency (sharp accuracy drop at 1 label/class, sensitivity to prototypicality, reduced benefit from unlabeled data under scarcity), and Theorem 1.1 formalizes this under a prototype-based model, providing a clean organizing principle.

- **Genuinely strong results in the extreme low-label regime.** On CIFAR-100 with 1 label/class, CaPT achieves 82.51% — a 21.38% absolute improvement over the best SSL baseline. Similar substantial margins hold on CIFAR-10 and EuroSAT under the same setting (Table 3). These are not incremental gains; they transform settings where existing SSL collapses into useful regimes.

- **Well-designed ablation study (Table 6)** systematically decomposes each component's contribution: the "only UPM" (pure SSL, 78.60%) vs "only MPM" (adapter-tuned CLIP alone, 68.32%) vs full CaPT (84.83%) cleanly demonstrates synergy rather than one model dominating. CaPT-Ada, CaPT-Deb, and CaPT-Uni ablations further isolate design choices.

- **Favorable efficiency documented (Table 4).** CaPT adds only 8% memory and 11% training time over FreeMatch while improving accuracy by 6.23% — a compelling efficiency-accuracy tradeoff compared to RegMixMatch (41% more memory, 58% more time, only 2.14% gain).

## Weaknesses

### Major

- **Comparison fairness — SSL baselines do not have access to CLIP.** The paper's headline improvements conflate two factors: having CLIP (pre-trained on 400M image-text pairs) and the CaPT co-training framework itself. When CaPT outperforms FreeMatch by 4.09% on CIFAR-100 (2 labels/class), it is unclear how much of that gap comes from the co-training mechanism vs. simply having CLIP's vastly superior pretraining available as a second opinion. The ablation study (Table 6) partially mitigates this: CaPT-Deb (81.03%) vs full CaPT (84.83%) shows a 3.80% gap from co-training + adapter-tuning, and "only MPM" (CLIP alone, 68.32%) underperforms "only UPM" (78.60%). However, a baseline using CLIP predictions in a simple manner (e.g., distillation-style loss, fixed prior) without mutual learning would better isolate the framework-level contribution. This does not invalidate CaPT's contribution — the ablation evidence for synergy is real — but it means the paper's claims about outperforming SSL methods by large margins need qualification.

- **On STL-10, CaPT underperforms the adapter-tuned CLIP alone, without discussion.** In Table 1, on STL-10 with 4 labels/class, the adapter-tuned CLIP alone achieves **96.86%**, while full CaPT achieves **96.07%** — a 0.79% *degradation*. The same pattern holds at 10 labels (97.15% vs. 96.34%). Since CaPT's final performance is reported using the unimodal network, the co-training framework is actively producing a vision model that underperforms CLIP alone on this dataset. The paper neither acknowledges nor analyzes this, which is a notable omission. (This does not undermine the paper's core SSL claim — CaPT still beats all SSL baselines on STL-10 — but it suggests the framework's benefits are dataset-dependent in ways not well understood.)

### Minor

- **Theorem 1.1 does not connect to the method.** It derives an upper bound on pseudo-label error for a *nearest-prototype classifier* under a Gaussian-mixture model — not for the neural-network setting CaPT actually uses. The theorem motivates the *problem* (label dependency) but does not explain why CLIP helps, how adapter-tuning reduces prototype bias, or provide formal guarantees for co-training. The paper's claim to "theoretically establish" something about CaPT slightly oversells the theory's scope.

- **The one-label-per-class setting (Table 3) — CaPT's most dramatic 21.38% improvement — compares CaPT against only two SSL baselines (FreeMatch and RegMixMatch).** The broader Table 1 includes 12 SSL methods, but the extreme-scarcity evaluation tests only two. While the margin is large enough to likely survive broader comparison, the omission weakens the evidence for the paper's headline result.

- **ImageNet results (Table 2) lack an adapter-tuned CLIP baseline.** CLIP zero-shot achieves roughly 70%+ top-1 on ImageNet. Without the adapter-tuned CLIP alone baseline, the reader cannot assess whether CaPT's 67.68% (10 labels/class) adds value beyond CLIP or merely matches it.

- **Feature-level Mixup vs. input-level strong augmentation (e.g., RandAugment) is not ablated.** The paper justifies feature-level Mixup by efficiency, but whether it provides comparable consistency-regularization benefit to standard input-level strong augmentation is not examined.

- **The paper claims entropy-based weighting lets CLIP dominate early and the vision model later, but does not empirically show the weighting dynamics (Γᵃ and Γᵇ) over training iterations.**

## Nice-to-Haves

- An additional baseline where CLIP's predictions serve as a fixed supervision signal (distillation-style) without bidirectional co-training, to more cleanly isolate the framework's contribution.
- Analysis of the STL-10 underperformance: does the vision model inject too much noise early in training, or does entropy-based weighting misassign weights on this dataset?
- Ablation comparing feature-level Mixup vs. input-level strong augmentation for the MPM consistency loss.
- A plot of the entropy-based weighting parameters over training iterations.

## Removed Points

These points from the input review were removed per the review guidelines:

- "Related work is thin on CLIP-integration side" — REMOVED per hard rule against citing missing related works; the reviewer cannot confirm what approaches exist.
- Request for statistical significance testing — REMOVED; confidence intervals from 3 seeds are standard for this type of SSL benchmark evaluation.
- Comments about content deferred to the appendix ("discussed in Appendix N") — REMOVED per hard rule (the parser strips appendices from all papers; they exist in the original submission).
- Speculation about what other unlisted SSL methods might achieve under 1-label settings — merged into the verified weakness about narrow baseline selection rather than treated as independent speculation.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add an adapter-tuned CLIP baseline to the ImageNet results (Table 2) to contextualize CaPT's performance.
2. Analyze the STL-10 underperformance relative to adapter-tuned CLIP alone — is the vision model too noisy early in training? Does entropy-based weighting misassign weights on this dataset?
3. Include more SSL baselines (at least ReMixMatch, SimMatch, SoftMatch) in the 1-label-per-class setting (Table 3) to strengthen the paper's most dramatic claim.
4. Add a baseline where CLIP predictions are used as fixed pseudo-labels without bidirectional co-training, to disentangle the framework-level contribution from the mere availability of CLIP.
5. Show the evolution of Γᵃ and Γᵇ over training iterations to validate the claimed dynamic weighting behavior.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>