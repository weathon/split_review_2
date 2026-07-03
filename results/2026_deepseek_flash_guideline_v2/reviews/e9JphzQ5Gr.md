The calibration search tool is unavailable due to directory access issues. I'll proceed with direct calibration based on my thorough reading and review verification.

Let me write the final review.

## Summary

This paper proposes CaPT, a framework that integrates CLIP into semi-supervised learning via asymmetric-modalities co-training. It jointly trains a fully fine-tuned unimodal vision network (UPM) and an adapter-tuned multimodal CLIP model (MPM), fusing their pseudo-labels through entropy-weighted co-pseudo labels (PFM). The paper also provides a theoretical bound (Theorem 1.1) showing that SSL pseudo-label error depends on labeled data quantity and quality. Empirically, CaPT achieves strong results across USB benchmarks, ImageNet, and fine-grained datasets, with a particularly large margin (21.38%) on CIFAR-100 with one label per class.

## Strengths

1. **Strong empirical results in low-label regimes** (Table 3): On CIFAR-100 with 1 label/class, CaPT achieves 82.51% vs. 61.13% (FreeMatch), a 21+ point improvement that far exceeds typical SSL gains. This directly demonstrates that CLIP integration can unlock unlabeled data where conventional SSL collapses entirely.

2. **Well-motivated asymmetric-modalities design** (Section 1, Figure 3): The paper identifies the "pattern-homogeneity bottleneck" in co-training two vision-only networks—two ViTs with different initializations still attend to nearly identical regions (both fixating on a rooster's eye and beak). CLIP's vision-language representations attend to different regions (the comb), providing qualitative evidence for why cross-modal asymmetry yields genuinely complementary views, which prior symmetric co-training cannot achieve.

3. **Thorough ablation study isolating each design component** (Table 6): Ablates 7 variants including replacing UPM with CLIP-Adapter (−16.40 pts), removing adapter tuning (−12.73 on EuroSAT), removing bidirectional flow (−1.49), removing feature augmentation (−1.81), and replacing entropy weighting with equal weights (−1.57). Each degradation is cleanly interpretable and provides controlled evidence for each design choice.

4. **Computational efficiency with direct comparison** (Table 4): On CIFAR-100 (2 labels/class), CaPT uses 5,050 MiB vs. 6,578 for RegMixMatch (−23.3%) and 0.1044 sec/iter vs. 0.1484 (−29.6%), while achieving higher accuracy (84.83% vs. 80.74%). This quantifies the practical advantage of adapter-tuning CLIP rather than full fine-tuning.

5. **Strong generalization across diverse dataset types** (Tables 1, 2, 5): Outperforms baselines on 5 of 6 fine-grained datasets (StanfordCars: 80.36% vs. 68.75% at 5 labels/class, +11.61 pts), on ImageNet (67.68% vs. 58.35% top-1 at 10 labels/class), and across all 6 USB benchmark settings. This shows the framework is not restricted to simple or CLIP-overlapping benchmarks.

## Weaknesses

### Major

- **Missing direct quantitative comparison against DebiasPL in the main benchmark tables.** The paper discusses DebiasPL (Wang et al., 2022a) qualitatively—presenting it in Figure 2c, describing it in lines 37 and 77—and includes CaPT-Deb (a DebiasPL-like ablation that disables adapter tuning and bidirectional flow) in Table 6. However, DebiasPL is the most directly comparable prior work for CLIP+SSL, and its published numbers should be included in the main tables (Table 1, Table 3) alongside the pure-SSL baselines. Without this comparison, it is difficult to assess whether CaPT's co-training design is genuinely superior to DebiasPL's simpler two-stage filtering approach, or whether both methods benefit similarly from CLIP's presence. The CaPT-Deb ablation is a reasonable proxy but does not exactly replicate DebiasPL's methodology.

### Minor

- **The theoretical contribution (Theorem 1.1) is disconnected from the method.** The theorem formalizes a bound on pseudo-label error under a prototype-based GMM with nearest-prototype classifier, showing that label scarcity or biased prototypes degrade pseudo-label accuracy. This observation is well-known empirically and has been demonstrated in prior SSL work. More critically, the bound is never referenced in the method section (Section 3), does not motivate any specific design choice in CaPT (adapter-tuning, asymmetric modalities, entropy weighting, feature-level Mixup), and the assumed generative model does not correspond to how CaPT operates. The theorem serves as motivation but is not a methodological contribution that connects to or informs the proposed framework.

- **STL-10 case where CaPT's unimodal network underperforms CLIP zero-shot is not analyzed.** On STL-10 (4 labels/class, Table 1), CaPT's reported unimodal network achieves 96.07%, while CLIP zero-shot achieves 97.18% and the adapter-tuned CLIP branch alone achieves 96.86%. The SSL co-training process produces a unimodal model that is slightly *worse* than using CLIP directly on this dataset. While CaPT substantially improves over CLIP on CIFAR-100 and EuroSAT, this case suggests dataset-dependent behavior that the paper does not discuss or explain. Understanding why the framework fails to match CLIP on STL-10 would strengthen the paper's practical guidance.

- **The "pattern-homogeneity bottleneck" claim rests on qualitative evidence.** Figure 3 shows attention maps for 8 examples, which is suggestive but not quantitative. The paper would benefit from a representation similarity analysis (e.g., CKA, SVCCA) across the full validation set to substantiate the claim that ViT(θ₁) and ViT(θ₂) are more similar to each other than either is to ViT(CLIP).

### Trivial

- None.

## Nice-to-Haves

- Include CLIP zero-shot performance in Table 2 (ImageNet) for context, since Table 1 already provides it for the USB datasets.
- Analyze failure cases on FGVCAircraft (where CaPT underperforms FreeMatch at 5 labels/class: 50.12 vs. 51.43) to characterize when CLIP's prior is harmful (domain gap? class-name granularity?). The paper mentions this is discussed in Appendix N, but it is worth surfacing.
- Consider adding confidence intervals or discussing the unusually low variance of CaPT results (±0.05–0.13) compared to baselines (±0.3–3.3), which warrants a brief comment even if the explanation is straightforward.

## Removed Points

- **"Experimental comparison is fundamentally apples-to-oranges because CaPT uses CLIP and baselines don't."** This criticism misunderstands the paper's contribution. The paper is explicitly about *integrating CLIP into SSL*—the title, abstract, and introduction all state this clearly. Comparing against pure SSL methods is the correct way to demonstrate the value of the proposed integration. The paper transparently reports CLIP zero-shot and Adapter-tuned CLIP baselines. The relevant comparison that is legitimately missing is against *other CLIP+SSL methods* (DebiasPL), which is captured in the Major weakness above.

- **"Standard deviations for CaPT are extremely small... could indicate CLIP's predictions dominate, reducing variance but also potentially masking dataset-dependent failures."** Speculative and unsupported. Lower variance can equally indicate robustness, and the ablation study (Table 6) shows that the unimodal network contributes meaningfully (only UPM: −6.23%, only MPM: −16.51% on CIFAR-100), so CLIP does not dominate.

- **"The paper sidesteps rather than breaks label dependency"** — This is a framing preference, not a factual error. The paper's framework injects external knowledge to break the coupling, which is a valid interpretation of "breaking."

- **Strength Finder's overstatement of Theorem 1.1 as a major contribution** — The theorem is too disconnected from the method to be a primary strength.

- **Various formatting and grammar nitpicks** — These are parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a tension between the paper's theoretical framing ("breaking label dependency from within SSL") and its actual approach (injecting external VL knowledge via CLIP), but this is a framing-level observation, not a novel synthesis.

## Suggestions

1. **Add DebiasPL results to the main benchmark tables** (Tables 1 and 3). This is the most important revision. If DebiasPL's numbers are not directly comparable due to different backbones, clarify this and include the comparison in a controlled setting.
2. **Either connect Theorem 1.1 to the method or downweight it.** If the authors can develop a theoretical result that explains why asymmetric-modalities co-training improves over symmetric co-training (e.g., analyzing the conditional independence of two views), that would be a genuine contribution. Otherwise, honestly reframe the theorem as empirical motivation and remove "theoretically establish" from the contribution list.
3. **Discuss the STL-10 result explicitly.** Explain why the unimodal network underperforms CLIP zero-shot and whether this reveals a systematic limitation of the approach on certain data distributions.
4. **Add quantitative representation analysis** (CKA or similar) to support the pattern-homogeneity bottleneck claim beyond the 8-example qualitative visualization.

## Score and Decision

Based on my analysis, this paper makes a genuine contribution: the asymmetric-modalities co-training framework is novel and well-motivated, the empirical results are strong across multiple benchmarks including extreme low-label settings, and the ablation study convincingly isolates each design choice. The main weaknesses are the missing DebiasPL comparison (addressable) and the disconnected theoretical component (fixable with recalibrated claims). These are not fatal — they reduce the paper from excellent to solid.

Scoring rationale: Strong empirical contributions and a novel method outweigh the framing and evaluation gaps. The paper would benefit from revisions but deserves acceptance in its current form.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>