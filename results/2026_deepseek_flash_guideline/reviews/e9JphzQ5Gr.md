Now let me write the final consolidated review.

## Summary

This paper identifies a "label dependency" problem in SSL — pseudolabel quality degrades when labeled data is limited or of poor quality — and proposes CaPT (CLIP as a Prior Teacher), an asymmetric-modalities co-training framework that integrates CLIP into SSL. CaPT jointly trains a fully fine-tuned unimodal vision network and an adapter-tuned multimodal CLIP model, fusing their predictions through entropy-weighted co-pseudolabels. Experiments on USB benchmarks, ImageNet, extremely-scarce-label settings, and six fine-grained datasets show large gains over 12 SSL baselines (e.g., +21.38% on CIFAR-100 with 1 label/class).

## Strengths

1. **Large-margin empirical gains in extreme low-label regimes.** Table 3 shows CaPT outperforms the second-best method by 21.38% on CIFAR-100 with one label/class (82.51% vs 61.13%) and by 4.05% on EuroSAT. These are substantial jumps that directly demonstrate the method's practical value when labeled data is minimal. The gain on ImageNet at 10 labels/class (67.68% vs RegMixMatch 58.35%, Table 2) is also notable.

2. **Efficiency-accuracy Pareto improvement.** Table 4 shows CaPT (0.1044 sec/iter, 5050 MiB) is both faster and more memory-efficient than RegMixMatch (0.1484 sec/iter, 6578 MiB) while achieving higher accuracy (84.83% vs 80.74%) on CIFAR-100 2-label. This counters the natural concern that adding CLIP would be a computational liability.

3. **Proactive handling of CLIP data-contamination concerns.** Section 4.4 evaluates on six fine-grained datasets (FGVCAircraft, Flowers102, StanfordCars, SUN397, DTD, SVHN) precisely to preclude advantages from CLIP's training corpus overlap. CaPT outperforms baselines on 5 of 6 datasets, including SVHN (81.20% vs 70.23% for RegMixMatch with 2 labels/class), showing robustness beyond CLIP's distribution.

4. **Well-structured ablation study.** Table 6 systematically isolates the contributions of each component (adapter-tuning, bidirectional flow, feature augmentation, entropy weighting), showing each design choice is beneficial.

## Weaknesses

### Major

1. **CaPT underperforms its own CLIP components on STL-10 — a result the paper does not discuss.** From Table 1: on STL-10 with 4 labels/class, CaPT (96.07%±0.05) is worse than both adapter-tuned CLIP (96.86%±0.01) and zero-shot CLIP (97.18%). On STL-10 with 10 labels/class, CaPT (96.34%±0.08) is again worse than adapter-tuned CLIP (97.15%±0.01). This is a genuine negative result, suggesting that co-training with the unimodal network can degrade CLIP's standalone predictions rather than complementing them. The paper claims CaPT "leads in all 6 commonly used evaluation settings" (line 210, relative to SSL baselines) but never discusses why the co-training framework underperforms its own CLIP components on STL-10. This omission is notable given that STL-10 is one of only three main-benchmark datasets.

2. **The evaluation does not control for CLIP's pretraining advantage, limiting what the "SOTA" claims reveal.** CaPT leverages CLIP (trained on 400M image-text pairs) while the 12 SSL baselines use standard ViT backbones without CLIP. The paper does not compare against SSL methods that also have access to CLIP features (e.g., initializing the SSL backbone with CLIP weights, or providing CLIP features as additional input). The ablation (Table 6) partially addresses this — CaPT outperforms CaPT-Uni (-0.88% on CIFAR-100) — but the headline framing ("outperforms 12 SSL methods") conflates the co-training framework's contribution with the raw advantage of having CLIP. The paper would be substantially stronger if it controlled for this confound.

### Minor

3. **The theoretical result (Theorem 1.1) is decoupled from the actual method.** The theorem bounds pseudolabel error for a nearest-prototype classifier under a Gaussian-mixture model, but the paper's experiments use deep networks trained with consistency regularization. The paper presents this as establishing a "fundamental limitation of existing SSL methods" (line 35), but the formal connection between the simplified generative model and actual deep SSL methods is not bridged. The empirical motivation (Figure 1) is sufficient on its own; the theorem is a formalization of known behavior in a specialized setting rather than a novel theoretical contribution.

4. **Pattern-homogeneity claim relies on qualitative evidence.** Figure 3 shows attention maps for 8 images to argue that pure-vision co-training suffers from representational homogeneity. The paper cites Appendix B for further experiments, but the main-paper evidence is only qualitative and cherry-picked. A quantitative similarity metric (e.g., CKA) over the full validation set would substantially strengthen this claim.

5. **Variance is not reported in several tables.** Table 1 reports mean±std over 3 seeds, but Tables 2, 3, and 5 report only point estimates despite the paper stating "Each algorithm is trained three times with different random seeds" (line 206).

6. **Missing comparisons against directly related methods.** The paper discusses CLS (Yao et al., 2022) and DebiasPL (Wang et al., 2022a) in Related Work but provides no experimental comparison against either. DebiasPL is only approximated through the CaPT-Deb ablation.

### Trivial

None.

## Nice-to-Haves

- A figure tracking entropy-based weights (Γ^a, Γ^b) over training steps to directly support the claim that "CLIP dominates early and the unimodal network gradually takes over" (line 163). Currently this is plausible but unsupported.
- A comparison against SSL methods initialized with CLIP ViT-B/32 weights would cleanly isolate the co-training framework's contribution from the pretraining advantage.

## Removed Points

- **Thresholding mechanism unclear (Harsh Critic).** REMOVED — the paper specifies "We adopt the adaptive threshold strategy from FreeMatch to filter pseudo labels, as in RegMixMatch" (line 206). This is sufficiently clear for reproducibility.
- **"Breaking label dependency" framing is oversold (Harsh Critic).** REMOVED — while the title is aspirational, many papers use ambitious framing. The method genuinely reduces label dependency substantially, and the FGVCAircraft limitation is acknowledged by the authors. This is a presentation preference rather than a flaw.
- **Several Strength Finder claims that were generic or sycophantic.** REMOVED — e.g., generic praise for "addressing an important problem" without specific evidence anchoring. Only concrete, evidence-grounded strengths are retained above.

## Novel Insights

None beyond the paper's own contributions. The key insight — that asymmetric-modalities (vision-only + vision-language) co-training enriches mutual learning beyond pure-vision co-training — is clearly articulated in the paper itself.

## Suggestions

1. **Discuss the STL-10 result explicitly.** Why does co-training with the unimodal network degrade CLIP's predictions on this dataset? Is it because CLIP already saturates performance on STL-10 and the unimodal network adds noise? Characterizing when the framework helps vs. hurts would greatly strengthen the paper.
2. **Add a controlled experiment:** initialize a competitive SSL baseline (FreeMatch or RegMixMatch) with CLIP's ViT-B/32 weights (or provide CLIP features as additional input) and compare against CaPT. This would isolate what the co-training framework itself contributes beyond simply having better features.
3. **Report standard deviations for Tables 2, 3, and 5.** The paper states 3 seeds are used; the variance should be reported consistently.
4. **Supplement Figure 3 with a quantitative representational similarity analysis** (e.g., CKA between ViT(θ₁), ViT(θ₂), and CLIP ViT over the full validation set) to replace the cherry-picked attention maps.

---

### Calibration Anchors

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/97D725GJtQ.md` (SemiCLIP) | 5.80 | 1 | Also uses CLIP + SSL; proposes semi-supervised CLIP training via concept mining and trapezoidal consistency. Smaller gains (1.7–6.6%) and weaker novelty (incremental on CyCLIP). CaPT has larger gains and more novel framework. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/1rgMkDWfYV.md` (Cleaning label noise with VLMs) | 4.50 | 1 | Uses CLIP for sample selection in noisy-label learning. Results inferior to SOTA. CaPT is significantly stronger empirically. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/FwkYeLovHk.md` (Weak-to-Strong CLIP) | 3.33 | 1 | Weak-to-strong generalization for CLIP; limited experiments, unclear practical applicability. CaPT has much stronger evaluation and clearer contribution. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/g1fkhbhHjL.md` (Black Sheep) | 7.00 | 1 | Identifies spurious attribute reliance in VLMs; clean two-module design, extensive generalization experiments. CaPT's framework design and large empirical gains are comparable, but CaPT has more pronounced weaknesses (STL-10, comparison fairness). |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/4JbrdrHxYy.md` (Zip) | 6.00 | 2 | Combines CLIP and SAM for annotation-free segmentation; pipeline-style contribution with heuristic aspects. CaPT has more principled design and stronger ablation, but also more notable unaddressed caveats. |

**Bracket reasoning (Round 1):** I first retrieved anchors across six score bands. The 3.0–3.5 band contained papers with limited experiments or unclear contributions (below CaPT). The 4.0–5.0 band contained papers with ideas but inferior results (below CaPT). The 5.5–6.0 band (SemiCLIP, Zip) contained papers with solid contributions but clear limitations — CaPT is comparable or slightly stronger. The 7.0 band (Black Sheep) contained a cleaner paper with fewer caveats. This placed CaPT in the 5.5–7.0 range.

**Narrowing (Round 2):** I inspected Zip (6.00) and SemiCLIP (5.80) in detail. CaPT's framework is more novel than Zip's pipeline-style contribution and SemiCLIP's incremental extension of CyCLIP. CaPT's empirical gains are substantially larger. However, CaPT's unaddressed STL-10 underperformance and asymmetric comparison are more significant caveats than those in Zip or Black Sheep. This anchors CaPT slightly above Zip/SemiCLIP but below Black Sheep — consistent with 6.0–6.5.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>