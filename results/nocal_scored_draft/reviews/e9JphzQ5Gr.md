Now let me write the final, consolidated review.

## Summary

This paper proposes CaPT (CLIP as a Prior Teacher), an asymmetric-modalities co-training framework that integrates CLIP into semi-supervised learning (SSL). It jointly trains a fully fine-tuned unimodal vision network and a parameter-efficiently fine-tuned multimodal CLIP model, using co-pseudo labels to exchange supervision between the two modules. The key insight is that CLIP's text-conditioned representations diverge from pure-vision representations, creating the view independence that classical co-training requires. Empirically, CaPT achieves strong results across multiple SSL benchmarks, with particularly large gains in the one-label-per-class regime (e.g., 82.51% vs. 60.49% on CIFAR-100).

## Strengths

- **Strong empirical results in the extreme low-label regime:** Table 3 shows CaPT achieves 82.51% on CIFAR-100 with one label per class, compared to 60.49% for RegMixMatch and 61.13% for FreeMatch — a ~22 point gain at this level of scarcity. Fine-grained dataset results (Table 5) are also convincing across six diverse domains.

- **The asymmetric-modalities co-training idea is well-motivated:** Figure 3 demonstrates that two pure-vision ViTs with different initializations still produce similar attention patterns, while CLIP's text-conditioned representations attend to different regions (e.g., the rooster's comb vs. its eye/beak), providing a clear basis for why unimodal+multimodal co-training can succeed where two unimodal networks plateau.

- **The efficiency analysis (Table 4) is informative:** Adding only 8% memory and 11% time over FreeMatch while improving accuracy by ~6 points shows the framework is practical, not just a laboratory exercise.

- **Comprehensive ablation study (Table 6) isolates each design choice:** Removing the adapter (CaPT-Ada: -16 points), reverting to a DebiasPL-like flow (CaPT-Deb: -3.8 to -12.7 points), and removing bidirectional information flow (CaPT-Uni: -0.9 to -1.5 points) all degrade performance, confirming the co-training framework is doing real work.

## Weaknesses

### Fatal
None.

### Major

- **Missing error bars for the headline one-label-per-class results (Table 3) and ImageNet results (Table 2).** The paper itself demonstrates (Figure 1a) that with one label per class, which specific sample is chosen can dramatically affect outcomes — the paper explicitly constructs three different "sets" using prototypicality ordering to show this effect. Yet the main one-label results in Table 3 are reported as point estimates without standard deviations, number of seeds, or any variance information. The 21.38% improvement on CIFAR-100 is the paper's most striking result and must be accompanied by variance estimates across different draws of the single labeled sample per class to establish reliability.

### Minor

- **Theorem 1.1 is formally disconnected from the actual method.** The theorem analyzes a nearest-prototype classifier under a prototype-based Gaussian-mixture generative model, whereas CaPT (and its baselines) use deep networks, softmax confidence thresholds, and consistency regularization. The multiplicative (K-1)2^{d/2} factor makes the bound extremely loose for high-dimensional features (e.g., d≥768 for ViT features), which is not discussed. The paper frames this as a "supporting theorem" revealing "an inherent limitation of SSL," which overclaims what the analysis actually establishes. This is not a fatal problem — the theorem provides useful motivating intuition, and the paper's empirical evidence (Figure 1a-c) independently demonstrates the label dependency — but the framing should be softened.

- **Missing direct comparison with DebiasPL (Wang et al., 2022a),** the closest prior work integrating CLIP into SSL. The CaPT-Deb ablation in Table 6 approximates DebiasPL but disables adapter tuning, making it a weaker proxy rather than a proper baseline. Without a direct DebiasPL comparison, it is hard to assess how much of CaPT's gain comes from the co-training framework versus simply using CLIP more carefully than prior work.

- **The FGVCAircraft failure case —** where CaPT underperforms FreeMatch (5 labels/class) and RegMixMatch (10 labels/class) — receives only a one-sentence acknowledgment in the main paper with deferral to the appendix. For a paper claiming broad scalability, this dataset warrants at least a paragraph of analysis in the main body explaining why CLIP's prior is unhelpful on this domain.

### Trivial

- The paper does not explicitly state whether a supervised cross-entropy loss on labeled data is used alongside the consistency losses L^a and L^b. Additionally, the thresholding mechanism (line 196: "a pseudo label is retained only if the weak-prediction confidence exceeds a threshold") could be clearer about whether the confidence check is applied to UPM, MPM, or both independently.

## Nice-to-Haves

- Comparing CaPT against a baseline that uses CLIP's zero-shot or adapter-tuned predictions directly as fixed pseudo-labels within a standard SSL pipeline (e.g., FreeMatch with CLIP-derived targets) would help disentangle the value of the co-training loop from the value of CLIP's prior. This is complementary to the existing CaPT-Deb ablation since that ablation disables adapter tuning, making it a weaker proxy.
- Adding standard deviations for the one-label-per-class and ImageNet results.

## Removed Points

- **"Comparisons are structurally unfair because baselines lack CLIP":** Removed. On CIFAR-100 with 2 labels, FreeMatch (78.60%) already outperforms CLIP zero-shot (65.10%) and adapter-tuned CLIP (74.90%), so CaPT's 84.83% advantage over FreeMatch cannot be explained by "just having CLIP." The ablations (only UPM vs. only MPM vs. full CaPT) further isolate the co-training contribution.
- **"Future-proof / portable claims unsubstantiated":** Removed per hard rule — the paper references Appendix N for supporting experiments; the appendix was stripped by the parser.
- **"STL-10 caveat as a major weakness":** Removed. CaPT still improves FreeMatch from 87.27% to 96.07% on STL-10. The fact that CLIP zero-shot (97.18%) is even higher is a caveat but does not undermine CaPT's contribution in improving SSL. A more direct acknowledgment would be helpful but the criticism as stated is overstated.
- **"Augmentation asymmetry criticism," "Missing co-training literature," "Missing standard SSL pipeline discussion":** Removed per filtering rules (see assessment in the review body).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add standard deviations for one-label-per-class results (Table 3) across multiple draws of the single labeled sample.
2. Include a direct DebiasPL comparison.
3. Add a paragraph in the main paper analyzing the FGVCAircraft failure case.
4. Clarify the supervised loss formulation and the thresholding mechanism details.

## Score and Decision

This paper makes a genuine contribution. The CaPT framework is well-motivated (the attention-map divergence in Figure 3 cleanly motivates why asymmetric modalities help), the efficiency is practical (8% memory overhead), and the empirical results — especially the 22-point gain on CIFAR-100 with one label per class — are striking. The ablation study convincingly shows that the co-training framework, not just CLIP's presence, drives the gains.

The main weaknesses are addressable: reporting variance for the one-label results (which the paper already knows matters, per Figure 1a), adding a DebiasPL comparison, and softening the theorem's framing. None of these threaten the paper's core validity. The paper has a well-supported contribution that would benefit from a tighter evaluation.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>