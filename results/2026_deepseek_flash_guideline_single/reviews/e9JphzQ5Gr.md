Now let me compile the final review with the calibrated score.

**Round 1 bracket:** Based on calibration anchors, the paper sits between the SemiCLIP paper (avg 5.8, borderline accept) and the FixMatch theory paper (avg 8.0, strong accept). It is empirically stronger than SemiCLIP but has the STL-10 omission and framing issues that prevent it from reaching the 7.5+ range. **Initial bracket: 5.5–7.0.**

**Narrowing (Round 2):** The SemiCLIP paper at 5.8 has novelty concerns but still gets accepted. CaPT has stronger empirical impact but the STL-10 omission is a notable gap. The paper is clearly above the reject-level papers (3.0–3.3) and comparable or slightly above the borderline papers (4.5–5.8). **Final score: 6.0**, reflecting a borderline-to-clear accept if the STL-10 issue is addressed.

Let me output the final review.

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| SemiCLIP (97D725GJtQ) | 5.80 | R1/R2 | Similar direction (CLIP + SSL) but lower empirical impact; CaPT has stronger results but a significant omission |
| Weak-to-Strong CLIP (FwkYeLovHk) | 3.33 | R1 | Much weaker; limited evaluation, unrealistic assumptions |
| Clean Label Noise w/ CLIP (1rgMkDWfYV) | 4.50 | R1 | Weaker than SOTA, complex presentation; CaPT is clearly stronger |
| FixMatch Theory (25kAzqzTrz) | 8.00 | R1 | Stronger conceptually with rigorous theory connected to method; CaPT's theory is disconnected |
| LLM2CLIP (HfJxXbXlYJ) | 3.00 | R2 | Mixed results, missing key experiments; CaPT is much stronger |
| VLM Selection (vG9dVXwXQV) | 6.33 | R2 | Different problem; CaPT comparable in quality |
| Out-of-Modal Generalization (LuVulfPgZN) | 6.00 | R2 | Different problem; CaPT comparable |

No papers in the strong reject or strong accept bands were topically similar enough to be directly comparable — CaPT is clearly above the reject-level papers and below the conceptually-deep theory papers.

Here is my final review:

## Summary
This paper proposes CaPT, a co-training framework that integrates CLIP into semi-supervised learning (SSL). The method jointly trains a unimodal vision network (fully fine-tuned) and a multimodal CLIP model (adapter-tuned), using entropy-weighted co-pseudo labels for bidirectional knowledge exchange. The paper identifies that SSL methods degrade sharply under extreme label scarcity, and proposes using CLIP's prior knowledge to mitigate this dependency. Experiments on CIFAR-100, STL-10, EuroSAT, ImageNet, and fine-grained datasets show strong results, particularly under extremely low-label regimes (e.g., +21% on CIFAR-100 with 1 label/class).

## Strengths
1. **Strong empirical results under extreme label scarcity.** On CIFAR-100 with 1 label/class, CaPT achieves 82.51% vs. 60.49% (RegMixMatch) — a 22-point absolute improvement. On ImageNet with 10 labels/class, CaPT achieves 67.68% vs. 58.35% (RegMixMatch). These are large, practically meaningful margins that significantly advance the state of the art in low-label SSL.

2. **Efficiency-aware design is clearly demonstrated.** Table 4 shows CaPT adds only 8% memory and 11% time over FreeMatch while substantially improving accuracy, and is simultaneously cheaper and more accurate than RegMixMatch. The feature-level Mixup for CLIP (avoiding reprocessing high-resolution inputs) is a sensible engineering choice that is validated.

3. **Informative ablation study.** Table 6 tests multiple meaningful variants (CaPT-Ada, CaPT-Deb, CaPT-Uni, only UPM, only MPM, w/o feature augmentation, equal weighting), and the results support the design choices. The bidirectional flow matters (CaPT-Uni drops 0.88–1.49%), feature augmentation matters (w/o feat aug. drops 0.57–1.81%), and entropy-based weighting outperforms equal weighting (drops 0.87–1.57%).

4. **Clear empirical motivation.** Figure 1 (a-c) provides well-documented evidence that SSL methods degrade sharply with very few labels and that the gain from unlabeled data shrinks as labeled data quality declines. This framing is effective and well-supported.

## Weaknesses

### Fatal
None.

### Major

1. **CaPT underperforms its own CLIP-only baseline on STL-10, and this is not discussed.** On STL-10 with 4 labels/class, CaPT achieves 96.07% while the adapter-tuned CLIP alone achieves 96.86%. With 10 labels/class: CaPT 96.34% vs. CLIP-alone 97.15% (Table 1). The paper claims CaPT "leads in all 6 commonly used evaluation settings" without noting that on STL-10, the co-training framework actively harms the CLIP branch's performance. This directly contradicts the claim that "asymmetric-modalities co-training enables richer information exchange and enhances mutual learning." Understanding when co-training helps vs. hurts is more important than the blanket claim of superiority, and the omission of this negative result undermines confidence in the analysis.

2. **The asymmetric-modalities advantage over symmetric co-training is asserted but not directly tested.** The paper argues that CaPT mitigates the "pattern-homogeneity bottleneck" of co-training two vision models (Sec. 1, Fig. 3), but never compares CaPT against a symmetric co-training baseline (e.g., two ViTs with different seeds following CLS's protocol on the same datasets). Figure 3's attention maps show only that differently pre-trained models attend to different regions — not that modality asymmetry specifically is advantageous. Without a direct head-to-head comparison, this claimed advantage remains unsubstantiated. Given that CLIP ViT-B/32 is itself a vision transformer, the "modality asymmetry" could simply be "different pre-training data," and the paper does not disentangle these.

3. **Theorem 1.1 is disconnected from the method.** The theorem bounds pseudo-label error under a prototype-based Gaussian mixture model using a nearest-prototype classifier. It is never referenced in the Method section, plays no role in designing CaPT, and its assumptions (prototype-based GMM, nearest-prototype classifier) are far from the consistency-regularization SSL methods the paper targets. It is used solely as motivational framing, inflating contribution 1 ("theoretically establish the label dependency") beyond what is warranted. The paper would be neither weaker nor stronger if the theorem were removed.

### Minor

4. **CaPT loses to FreeMatch on FGVCAircraft (5 labels/class): 50.12% vs 51.43%.** The paper acknowledges this in a parenthetical (line 268: "discussed in Appendix N") but the main text claim that "CaPT outperforms competing methods across all other datasets" is accurate but masks a case where the proposed method clearly underperforms the baseline.

5. **The "portability" claim is not demonstrated.** The paper claims CaPT is a general framework for integrating any VLM into SSL (Sec. 5, Appendix L), but only CLIP ViT-B/32 is evaluated. Showing results with at least one other VLM (e.g., SigLIP, EVA-CLIP) would substantiate this claim.

### Trivial
None.

## Nice-to-Haves
- A direct symmetric co-training baseline (two ViTs with different seeds) would substantiate or refute the pattern-homogeneity bottleneck claim.
- A baseline using CLIP's predictions as fixed pseudo labels (without updating CLIP) would isolate the contribution of bidirectional flow vs. just using CLIP as a fixed teacher — the CaPT-Uni ablation partially addresses this but the CLIP branch is still being updated.
- Systematic characterization of when CaPT helps vs. hurts (e.g., STL-10 vs. CIFAR-100) would strengthen the paper considerably.

## Removed Points
1. "No comparison against concurrent VLM-assisted SSL methods" — Removed per policy: missing related works cannot be externally verified.
2. "Thresholding details not in main text" — The paper explicitly states it uses FreeMatch's adaptive threshold and defers to Appendix F. This is standard practice.
3. "Label selection protocol underspecified" — Configuration details are in Appendix F, which is standard for SSL papers.
4. "The contribution is engineering, not scientific insight" — This is a matter of opinion/scope interpretation, not a verifiable flaw. The empirical results are strong regardless of how the contribution is categorized.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Discuss and analyze the STL-10 case.** This is the most impactful suggestion. Understanding when CaPT helps (CIFAR-100, EuroSAT) vs. hurts (STL-10) would improve the paper substantially and is needed for scientific integrity.
2. **Add a symmetric co-training baseline** (two ViTs with different seeds following CLS's protocol) to verify the claimed advantage of asymmetric modalities.
3. **Qualify the "breaking label dependency" framing** — the paper's contribution as a practical, efficient integration of CLIP into SSL is already strong and needs no overclaiming.
4. **Either connect the theorem to the method or remove it.** If it cannot inform the method design, it should be de-emphasized.
5. **Include at least one additional VLM** to support the portability claim.

## Score and Decision

Based on calibration against human-reviewed anchor papers:

- **Strong reject band (< 1.5):** No comparable papers — CaPT has genuine content and strong experiments.
- **Reject band (1.5–3.5):** Papers like LLM2CLIP (3.00) and Weak-to-Strong CLIP (3.33) have unconvincing results or unrealistic assumptions. CaPT is clearly above this band.
- **Borderline band (3.5–5.5):** Papers like label noise CLIP (4.50) have decent ideas with evaluation gaps. CaPT's empirical results and evaluation are substantially stronger.
- **Borderline accept (5.5–6.5):** Papers like SemiCLIP (5.80) have similar scope (CLIP + SSL) but smaller empirical gains. CaPT has larger margins but has the STL-10 omission that SemiCLIP does not.
- **Accept (6.5–7.5):** Papers with strong empirical contributions and clear framing. CaPT could reach this band after addressing the STL-10 issue and adding missing baselines.
- **Strong accept (> 7.5):** Papers like the FixMatch theory paper (8.00) have substantive conceptual or theoretical advances. CaPT's disconnected theorem prevents reaching this band.

**Final score: 6.0** — Borderline accept. The paper presents a practically effective framework with strong empirical results, but has a significant omission (STL-10 underperformance vs. CLIP-alone not discussed) and a missing comparison (symmetric co-training baseline) that prevent a higher rating. The core contribution is real and useful; the issues are addressable.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>