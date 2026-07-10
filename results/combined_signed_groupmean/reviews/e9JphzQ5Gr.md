Now let me finalize the review.

## Summary

This paper proposes CaPT (CLIP as a Prior Teacher), a framework that integrates CLIP into semi-supervised learning through asymmetric-modalities co-training between a fully fine-tuned unimodal ViT (UPM) and a PEFT-tuned multimodal CLIP model (MPM). The two branches exchange supervision via entropy-weighted co-pseudo labels, and feature-augmented Mixup consistency is applied to CLIP's frozen encoder for efficiency. CaPT achieves strong empirical results across USB benchmarks, ImageNet, extremely-scarce-label settings, and fine-grained datasets, with thorough ablations confirming each component's contribution.

## Strengths

- **Novel and principled framework design (Sections 3.1–3.3).** The asymmetric-modalities co-training between a fully fine-tuned unimodal ViT and a PEFT-tuned multimodal CLIP is a thoughtful architectural choice. The entropy-based adaptive weighting (Eq. 12) that lets CLIP dominate early and the ViT take over later is sensible. The feature-augmented Mixup consistency regularization (Section 3.2.2) is a pragmatic efficiency measure given CLIP's high-resolution input requirements. **[draft impact: +9.93]**

- **Strong and consistent empirical results (Tables 1, 2, 3, 5).** CaPT outperforms all 12 SSL baselines across all 6 USB settings, often by large margins (e.g., +4.09% on CIFAR-100 with 2 labels, +6.18% on STL-10 with 4 labels). The 1-shot results on CIFAR-100 (82.51% vs. 61.13% for FreeMatch) are striking and suggest genuine synergy beyond what CLIP alone provides (CLIP zero-shot: 65.10%). **[draft impact: +10.00]**

- **Thorough ablation study (Table 6).** The ablations isolate each component's contribution: adapter tuning vs. frozen CLIP, bidirectional vs. unidirectional information flow, feature augmentation, and entropy weighting. The "only UPM" (78.60) vs. "only MPM" (68.32) vs. "CaPT" (84.83) comparison cleanly demonstrates the combination provides a non-trivial benefit beyond either branch alone. **[draft impact: +10.00]**

- **Resource efficiency (Table 4).** The modest overhead (+8% memory, +11% time over FreeMatch) makes the framework practically usable despite incorporating a second model. **[draft impact: +8.57]**

- **Well-motivated problem with empirical grounding (Section 1, Figure 1).** The paper demonstrates that SSL methods' performance collapses in extreme low-label regimes and that pseudo label accuracy degrades with poor-quality labeled samples. **[draft impact: +3.48]**

## Weaknesses

### Major

- **The comparison against SSL baselines is structurally asymmetric and the framing overreaches.** CaPT uses CLIP (pretrained on 400M image-text pairs) as an auxiliary model, while baselines use only a single ViT with ImageNet-scale pretraining. The paper's headline claims about "breaking label dependency" should more precisely acknowledge that this is achieved through injecting external CLIP knowledge. The abstract and introduction frame the results as "SSL breakthroughs" rather than "CLIP-augmented SSL breakthroughs." This does not invalidate the engineering contribution — the framework for integrating CLIP into SSL is useful — but the paper's strongest scientific framing ("breaking label dependency" as a general property) overstates what the experiment shows. The paper partially mitigates this by reporting CLIP-Adapter and CLIP zero-shot baselines and testing on fine-grained datasets, but remains imprecise in its central claims. **[draft impact: -9.90]**

### Minor

- **On STL-10, CaPT underperforms adapter-tuned CLIP alone without discussion.** From Table 1: STL-10 4 labels — CaPT 96.07 vs. adapter-tuned CLIP 96.86 (and CLIP zero-shot 97.18); STL-10 10 labels — CaPT 96.34 vs. adapter-tuned CLIP 97.15. The paper reports these numbers but only highlights improvement over SSL baselines ("leads by 6.18%" against RegMixMatch), without noting that on this dataset the co-training framework does not improve over its own CLIP branch. Some analysis (e.g., tracking entropy weights over training) would clarify whether this is a meaningful boundary condition. **[draft impact: -0.00]**

- **The theoretical result (Theorem 1.1) is disconnected from the method.** The theorem is a standard concentration bound for nearest-prototype classification in a Gaussian mixture model, showing that pseudo label error depends on prototype bias B and sample size n_min. It provides useful background motivation but does not involve CLIP, adapter-tuning, co-training, or any aspect of CaPT. The paper claims as Contribution 1 to "theoretically establish the label dependency that constrains SSL," but the theorem is background material. Removing it or connecting it to CaPT would be clearer. **[draft impact: -0.20]**

- **The 1-shot experiments (Table 3) do not report adapter-tuned CLIP alone.** This makes it harder to disentangle how much of CaPT's gain in the 1-shot setting comes from the co-training framework vs. from CLIP's prior being exploited even with minimal fine-tuning. **[draft impact: -0.00]**

- **ImageNet results (Table 2) lack standard deviation.** Unlike the USB experiments where 3 seeds with ±std are reported, ImageNet results are single-run numbers, making reliability harder to assess. **[draft impact: -0.00]**

### Trivial

- The paper does not specify which exact CLIP checkpoint is used (original OpenAI release, OpenCLIP, LAION?). ViT-B/32 is mentioned (line 206), but the exact checkpoint matters for reproducibility. **[draft impact: -0.67]**
- The Mixup coefficient λ (Eq. 9, 14) is described as sampled from Beta(α, α) but it is not specified whether λ is sampled per batch or per sample, or whether the same λ is used for both feature mixing and label mixing. **[draft impact: -0.09]**

## Nice-to-Haves

- Add a baseline that gives SSL methods access to comparable CLIP representations (e.g., using CLIP's frozen visual encoder as the backbone for FreeMatch/RegMixMatch) to test whether CaPT's advantage comes from the co-training framework or simply from CLIP's superior representations.
- Analyze the STL-10 case where CaPT underperforms adapter-tuned CLIP alone — a diagnostic analysis (e.g., tracking entropy-based weights over training, measuring prediction shift) would characterize this boundary condition.
- Either remove Theorem 1.1 or extend it to connect to CaPT.
- Report standard deviations for ImageNet results and adapter-tuned CLIP results for the 1-shot setting.

## Removed Points

- The paragraph about "Paradoxically and unexpectedly" phrasing: this is a stylistic judgment, not a substantive weakness. The observation that SSL degrades sharply below a certain label threshold is a real finding, and the framing as a paradox is a rhetorical device, not a factual error.
- The suggestion that missing related works should be discussed: as per evaluation guidelines, I cannot confirm the existence of external works not cited in the paper.
- Minor reproducibility nitpicks about undisclosed hyperparameters beyond the CLIP checkpoint and Mixup λ specification: these go beyond what is reasonable to expect in a conference submission.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Recalibrate the paper's central claims: the contribution is a CLIP-augmented SSL framework, not a discovery about SSL's fundamental properties. Adjust the abstract and conclusion to say "CaPT breaks label dependency by injecting CLIP's external knowledge" rather than "SSL's label dependency is broken."
2. Add a discussion of why CaPT underperforms adapter-tuned CLIP alone on STL-10. Provide analysis of entropy weight dynamics or prediction shifts.
3. Add a baseline with CLIP as frozen backbone for a standard SSL method (e.g., FreeMatch with CLIP visual encoder replacing ViT) to isolate the co-training effect.
4. Report adapter-tuned CLIP results for the 1-shot setting.
5. Add standard deviations for ImageNet results.
6. Specify the exact CLIP checkpoint used and clarify whether λ in Mixup is per-batch or per-sample.

## Score and Decision

### Calibration Analysis

I performed bracketed retrieval across 6 score bands and itemized 6 anchors. The most comparable papers:

| Anchor | Avg Score | Decision | Comparison |
|--------|-----------|----------|------------|
| SemiCLIP (97D72) | 5.80 | Accept | Semi-supervised CLIP training with limited paired data. Weaker empirical results than CaPT but similar "using CLIP advantage" concern. |
| Modality Synergy (5BXWh) | 6.33 | Accept | Asymmetric modality co-training without paired data — closest methodology match. Has similar overclaiming weakness (-9.96 impact) but was accepted due to strong theory and validation. |
| Cleaning label noise (1rgMk) | 4.50 | Reject | Uses CLIP for noisy label learning. Similar "unfair comparison" concern but far weaker results and poor presentation. |
| Image Clustering with CLIP (ptCIl) | 5.80 | Accept | Uses CLIP features for clustering. Similar "unfair backbone advantage" criticism. |
| FixMatch theory (25kAz) | 8.00 | Accept | SSL theory paper — very different contribution type. |
| C-CLIP (sb7qH) | 6.50 | Accept | Continual learning for CLIP with strong empirical results and thorough experiments. |

**Bracket (Round 1):** The paper's impact profile (extreme high-magnitude empirical strengths [+10.00, +9.93, +10.00] with one high-magnitude framing weakness [-9.90]) matches papers in the 5.5–7.5 band. The framing weakness is similar in severity to the "overclaiming" weakness in the accepted Modality Synergy paper (6.33), but our paper lacks that anchor's theoretical depth. The empirical breadth exceeds SemiCLIP (5.80) but shares a similar dependency on pre-trained model advantage.

**Narrowing (Round 2):** Compared to accepted anchors in the 5.8–6.5 range, this paper has stronger empirical results (beats all 12 baselines across all settings) and a more thorough ablation than SemiCLIP (5.80). The "structural asymmetry" weakness is real but partially addressed by reporting CLIP-only baselines and fine-grained evaluations. The paper's practical efficiency (+8% memory, +11% time) is a genuine strength. The key gap relative to higher-scoring papers like C-CLIP (6.50) is the disconnected theorem and the absence of analysis for the STL-10 case.

**Final placement:** The paper sits at **6.0** — a borderline accept. The framework contribution is solid, the empirical evidence is strong, and the ablations are thorough. The main concerns (comparison framing, STL-10 degradation, disconnected theorem) are addressable but prevent a higher score.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>