Now I have enough anchor data to make a well-calibrated assessment. Let me finalize the review.

**Round 1 bracket:** After comparing with SemiReward (6.0), SemiCLIP (5.8), CLIPSelector (4.5), and Out-Of-Domain SSL (7.0), the plausible bracket for CaPT is **5.5–7.0**.

**Narrowing:** CaPT is clearly stronger than CLIPSelector (4.5) which shares the same "unfair CLIP comparison" criticism but lacks CaPT's mitigating ablation (CaPT-Ada showing co-training matters beyond CLIP alone). It's also stronger than SemiCLIP (5.8) which has negative-weight novelty concerns. Compared to SemiReward (6.0), CaPT has larger and more consistent gains and stronger ablations. The only anchor possibly above CaPT is Out-Of-Domain SSL (7.0), which has a better-integrated theory-method connection and no CLIP asymmetry confound.

**Final score: 6.5** — between borderline accept and accept, reflecting strong empirical contributions tempered by the asymmetric evaluation concern.

Now let me produce the final review.

Here are all the anchor papers I'm considering:

1. /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/dnqPvUjyRI.md (SemiReward, avg 6.0, Round 1, itemized) - Pure SSL method with reward model; CaPT has larger gains and cleaner ablations but the asymmetry concern.
2. /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Bo6GpQ3B9a.md (Out-Of-Domain SSL, avg 7.0, Round 1, itemized) - SSL with DRO and theory; better theory-method integration but less direct empirical comparison.
3. /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/1rgMkDWfYV.md (CLIPSelector, avg 4.5, Round 1, itemized) - Uses CLIP for noisy label learning; CaPT is significantly stronger with better ablations separating CLIP from method.
4. /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/RvUVMjfp8i.md (Realistic SSL Evaluation, avg 8.0, Round 1, itemized) - SSL benchmark paper; less directly comparable.
5. /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/97D725GJtQ.md (SemiCLIP, avg 5.8, Round 2, itemized) - Semi-supervised CLIP training; CaPT has more novel contribution and avoids negative-weight novelty concerns.

Let me write the final review now.## Summary

This paper proposes CaPT, a framework that integrates CLIP into semi-supervised learning (SSL) through asymmetric-modalities co-training. CaPT jointly trains a fully fine-tuned unimodal ViT (UPM) and a PEFT-tuned multimodal CLIP (MPM), using entropy-weighted co-pseudo labels that fuse predictions from both branches. The method is portable (works with any SSL backbone) and computationally efficient (+8% memory, +11% time over FreeMatch). Experiments on USB, ImageNet, and fine-grained benchmarks show large and consistent gains, including +21.38% absolute over the second-best method on CIFAR-100 with one label per class.

## Strengths

- **Large and consistent empirical gains across multiple benchmarks.** In the USB benchmark (Table 1), CaPT outperforms all 12 baselines on all 6 settings with substantial margins (e.g., +4.09% on CIFAR-100 with 2 labels/class, +6.18% on STL-10 with 4 labels/class). On ImageNet with 10 labels/class (Table 2), CaPT leads RegMixMatch by 9.33% Top-1. [item weight: 11.25]

- **The ablation study (Table 6) convincingly validates the design choices.** Each variant (CaPT-Ada, CaPT-Deb, CaPT-Uni) underperforms the full CaPT. Degradation from removing bidirectional flow (CaPT-Uni: -0.88% to -1.49%) and from removing feature-level augmentation (-0.57% to -1.81%) confirms both design choices contribute meaningfully. Critically, CaPT-Ada — which also uses CLIP but without the co-training framework — gets 68.43% vs. CaPT's 84.83% on CIFAR-100, showing co-training matters beyond just having CLIP. [item weight: 10.12]

- **Computational overhead is modest relative to the gain.** Table 4 shows CaPT adds only 8% memory and 11% time over FreeMatch while improving accuracy by 6.23%. [item weight: 9.24]

- **The motivation is empirically well-supported.** Figure 1a–c demonstrate that standard SSL methods degrade sharply under extreme label scarcity and that this degradation connects to pseudo-label quality. [item weight: 8.78]

## Weaknesses

### Major

- **The comparison to SSL baselines is structurally asymmetric.** CaPT additionally leverages CLIP's massive multimodal pretraining (400M image-text pairs), while baselines use only ImageNet/MAE-pretrained ViTs. The paper frames results as "state-of-the-art SSL" without fully controlling for this extra data. The ablation study partially mitigates this (CaPT-Ada at 68.43% vs. CaPT at 84.83% on CIFAR-100 shows co-training adds value beyond CLIP alone). However, a direct control experiment — where MPM uses a vision-only model of comparable capacity (e.g., a larger ViT) instead of CLIP, within the same co-training framework — is absent. Such an experiment would directly test whether the asymmetric-modalities interaction is the source of gains rather than simply CLIP's additional pretraining data. [item weight: 2.64]

### Minor

- **On STL-10, CaPT's final unimodal network underperforms adapter-tuned CLIP alone.** From Table 1: at 4 labels/class, CaPT = 96.07% vs. adapter-tuned CLIP = 96.86% vs. CLIP zero-shot = 97.18%; at 10 labels/class, CaPT = 96.34% vs. adapter-tuned CLIP = 97.15%. This is a case where the full co-training framework yields worse results than simply using adapter-tuned CLIP in isolation. The paper presents these numbers in the table but does not discuss this as a limitation in the main text. [item weight: 4.85]

- **On FGVCAircraft (Table 5), CaPT (50.12%) underperforms FreeMatch (51.43%) with 5 labels/class.** The paper relegates discussion to Appendix N (stripped) without explaining the failure mode in the main text. Since this is likely due to CLIP's weak prior on this dataset, it is informative about the method's limitations and warrants mention. [item weight: 4.26]

- **ImageNet results in Table 2 lack standard deviations or confidence intervals.** At 10 labels/class where variance is typically high, this makes it impossible to assess whether the reported 9.33% lead over RegMixMatch is statistically significant. [item weight: 3.39]

- **The theoretical analysis (Theorem 1.1) is structurally disconnected from the method.** It bounds the pseudo-label error of a nearest-prototype classifier under a GMM but does not involve CLIP, co-training, or any mechanism of CaPT. The bound contains a \(2^{d/2}\) factor that makes it vacuous for high-dimensional inputs, which goes unmentioned. The paper presents this as a contribution ("We identify and theoretically establish the label dependency"), but it serves only as motivation, not as a result that explains or guarantees CaPT's behavior. [item weight: -2.19]

- **The feature-level Mixup concern is not discussed.** When feature-level Mixup (Eq. 9) mixes features from two images with different ground-truth labels, the mixed co-pseudo label (Eq. 14) becomes a soft label not corresponding to any real class. This is a known concern with Mixup-based consistency regularization that the paper does not address. [item weight: 1.02]

### Trivial

None.

## Nice-to-Haves

- Add a control experiment where MPM uses a vision-only model of comparable capacity (e.g., a larger ViT pretrained on ImageNet-21K) instead of CLIP, to test whether the asymmetric-modalities interaction is the source of gains beyond CLIP's additional pretraining.
- Discuss the STL-10 case where adapter-tuned CLIP alone outperforms CaPT's unimodal network, and provide guidance on when to use which.
- Add standard deviations or confidence intervals to ImageNet results.
- Discuss the FGVCAircraft failure mode (weak CLIP prior) in the main text.

## Removed Points

- The critic's claim that the paper presents label dependency as a "novel discovery" — the paper cites prior work and frames its contribution as identifying and *theoretically establishing* the issue, which is a modest but defensible claim. The criticism is overstated.
- "The bound does not explain why CaPT would fix the problem" — merged into the disconnected-theory weakness above. This is a valid observation folded into that item.
- "21.38% claim framing" — the paper clearly states absolute improvement (82.51% − 61.13% = 21.38%), so this is transparent to the reader.
- "Pattern-homogeneity bottleneck supported only by qualitative attention maps" — this is valid but is covered by the broader asymmetry concern in the Major weakness section.
- Missing related works — removed per instructions (no external knowledge to verify).
- Formatting/typography nits — removed per instructions (parser artifacts).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

Add a control experiment where the MPM branch uses a vision-only model of comparable capacity (not CLIP) within the same co-training framework. This single addition would directly separate whether the gains come from (a) CLIP's additional pretraining data, (b) the co-training framework, or (c) the asymmetric-modalities interaction. The current ablation study partially separates (a) from (b)+(c) via CaPT-Ada, but cannot distinguish (b) from (c). Addressing this would substantially strengthen the paper's central claim about cross-modal complementarity.

## Score and Decision

**Calibration anchors considered across two rounds:**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| SemiReward | dnqPvUjyRI.md | 6.0 | R1, R2 | Yes | Pure SSL reward model; CaPT has larger gains, cleaner ablations, but the asymmetry concern |
| SemiCLIP | 97D725GJtQ.md | 5.8 | R2 | Yes | SSL for CLIP; CaPT is more novel (no negative-weight novelty concerns) |
| CLIPSelector | 1rgMkDWfYV.md | 4.5 | R1 | Yes | CLIP for noisy labels; shares "unfair CLIP comparison" criticism but lacks CaPT's mitigating ablation |
| Out-Of-Domain SSL | Bo6GpQ3B9a.md | 7.0 | R1 | Yes | SSL with DRO+theory; better-integrated theory, no CLIP confound |
| Realistic SSL Eval | RvUVMjfp8i.md | 8.0 | R1 | Yes | Benchmark paper, less directly comparable |

**Round 1 bracket:** 5.5–7.0. **Narrowing:** CaPT's strength weights (11.25, 10.12, 9.24, 8.78) are higher than SemiReward's and SemiCLIP's corresponding items, and CaPT avoids the negative-weight novelty concerns that pulled those papers down. Its main weakness (asymmetric comparison, weight 2.64) is the same criticism that appeared in CLIPSelector (weight 0.33–1.75), but CaPT's ablation addresses it far more thoroughly (CaPT-Ada shows a 16% gap). The paper sits above SemiReward (6.0) but below Out-Of-Domain SSL (7.0), which has a tighter theory-method integration and no confound.

**Final score: 6.5** — a solid contribution with strong empirical results and a practically useful framework, held back from a higher score by the unresolved comparison confound and the disconnected theoretical analysis.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>