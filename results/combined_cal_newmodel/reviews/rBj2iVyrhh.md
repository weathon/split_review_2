Now I have all the calibration data I need. Let me compose the final review.

## Summary

This paper proposes Classifier-Constrained Alternating Training (CCAT), a two-stage framework for mitigating modality imbalance in multimodal learning. The core insight is that existing alternating-training methods prevent encoder-level gradient interference but leave the classifier biased toward the dominant modality. CCAT first pre-trains a shared classifier with a regularization term that penalizes modality contribution disparities, then freezes it during alternating training while using modality-specific LoRA adapters. Experiments on CREMA-D, Kinetic-Sound, and MVSA show consistent improvements, most notably +6.76% on Kinetic-Sound.

## Strengths

- **The core idea — bridging class imbalance and modality imbalance remedies — is conceptually novel and well-motivated.** The paper identifies a genuine limitation in existing alternating-training approaches (they prevent encoder-level gradient interference but do not address the classifier's learned preference for the dominant modality). Borrowing the "fix the classifier" strategy from class imbalance literature (Section 3.1) is a creative transfer, and the two-stage design (pretrain unbiased classifier, then freeze) follows naturally from this diagnosis.

- **The empirical gains on Kinetic-Sound are substantial.** The +6.76% absolute improvement over LFM (72.53 → 79.29, Table 1) is a large and practically meaningful margin on a real audio-visual benchmark.

- **The ablation study (Table 2) is well-structured and informative.** Each of the four components (classifier freezing, alternating training, secondary updates, LoRA) is ablated individually against the full pipeline. The pattern of results confirms that all components contribute positively on most metrics, and the relative importance varies across datasets in interpretable ways.

## Weaknesses

### Fatal
None.

### Major

1. **The abstract contains an arithmetic error in a headline claim.** The abstract states "+1.35% on CREMA-D," but Table 1 shows the best prior SOTA (LFM) at 83.62% and CCAT at 85.89% — a difference of **+2.27 percentage points**, not +1.35%. An error in a headline number at the very top of the paper erodes trust and must be corrected and checked across all reported results.

2. **The "mutual information" quantity (Eq. 5) is not mutual information.** Eq. (5) defines: MI(zᵢᵐ, fᵢ) = log(N) + 𝔼_D[ log( exp(⟨f̄ᵢ, z̄ᵢᵐ⟩) / Σₗ exp(⟨f̄ᵢ, z̄ᵢˡ⟩) ) ]. This is a log-softmax of cosine similarities over exactly two modalities — a reasonable heuristic proxy for relative modality contribution — but it is **not mutual information**, which requires density estimation or variational lower bounds (e.g., InfoNCE, MINE). The method's regularization (Eq. 7), sample-level imbalance detection (Algorithm 1), and the paper's claimed theoretical grounding all rely on this quantity. The paper should rename it (e.g., "relative contribution score") or adopt a recognized MI estimator.

3. **Section 3.1 overclaims its theoretical contribution.** The paper states it "establishes a unified theoretical framework and provides a proof" of isomorphism between class and modality imbalance (line 59), and later calls it a "profound theoretical isomorphism" (line 87). What is actually shown is that both problems exhibit similar gradient dynamics (one term dominates the gradient) — a reasonable analogy that motivates the design choice, not a formal proof or isomorphism. This framing inflates the paper's contribution beyond what is demonstrated. The section should be reframed as an analogy/inspiration, not a proof.

### Minor

4. **No variance or statistical significance is reported.** Table 1 reports "average test accuracy (%) of three random seeds" but provides no standard deviations, confidence intervals, or significance tests. Several improvements are modest (~2 pp on CREMA-D and MVSA), and some unimodal ablation results show the full method underperforming partial configurations (e.g., KS-Audio: full method 61.65 vs. Alt✗ 63.01; KS-Video: full method 53.75 vs. Fix✗ 54.32), suggesting noise may be a factor. Variance estimates are needed to assess statistical reliability.

5. **The unimodal ablation results on Kinetic-Sound partially contradict the claimed mechanism.** On KS-Audio, removing alternating training (Alt✗) yields 63.01, higher than the full method's 61.65. On KS-Video, removing classifier freezing (Fix✗) yields 54.32, higher than the full method's 53.75. The paper's narrative emphasizes "liberating weak modalities" (lines 270–274), yet the unimodal numbers do not consistently show improvement. The paper's main benefit is in multimodal accuracy, which is coherent, but this pattern deserves explicit discussion.

6. **The Figure 1 caption contains an error.** It describes the 'Ours' lines as showing "more pronounced imbalance" when the data (lines 36–43) shows Ours achieving **better** balance (0.65/0.35) than MLA (0.90/0.10). The caption contradicts the data it describes.

### Trivial

7. **The same hyperparameters (SGD, LR 0.001, batch size 32, etc.) are used across all baselines** (lines 236–243). It is unclear whether each baseline (MLA, MMPareto, LFM, OGM-GE, etc.) was individually tuned to its optimal configuration, which could affect fairness of comparison.

## Nice-to-Haves

- Add standard deviations / confidence intervals for all main results (Table 1, Table 2).
- Include sensitivity analysis for the regularization coefficient λ (fixed at 0.001 without ablation).
- Quantify the computational overhead of the two-stage CCAT training relative to baselines.
- Consider a direct measurement of classifier bias (e.g., gradient-based feature attribution before/after freezing) to more directly validate the claimed mechanism.
- Discuss settings where CCAT might not help (e.g., more balanced modalities, three+ modalities beyond the two-modality demonstrations).

## Removed Points

These points were raised in the input review but are removed for the stated reasons:
- **"LoRA novelty is minimal"** — removed because the paper does not claim LoRA as a key innovation; it uses a standard tool appropriately.
- **"The method may not scale to 3+ modalities"** — removed because the paper explicitly notes tri-modal extension as future work (Section 6); criticizing it as a present weakness is scope creep.
- **Speculative concerns about missing appendix content or proofs** — removed per parsing rules (the parser strips these sections; they exist in the original submission).
- **"Strengthening the Paper on Its Own Terms" specific proposals** — moved to Nice-to-Haves as these are enhancement suggestions for future work, not identified weaknesses of the current paper.
- **Weaknesses about missing related work** — removed per rules (cannot confirm existence of unlisted works without external sources).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Fix the abstract's CREMA-D claim from "+1.35%" to the correct value (+2.27%).
2. Rename the "mutual information" quantity (Eq. 5) to an appropriate term (e.g., "relative contribution score") and clearly acknowledge it as a heuristic proxy.
3. Reframe Section 3.1 as an analogy / design inspiration rather than claiming a "proof" or "unified theoretical framework."
4. Add standard deviations to all tables reporting multiple random seeds.
5. Correct the Figure 1 caption to accurately describe the data.
6. Add explicit discussion of the unimodal KS ablation results (Table 2), acknowledging where the full method does and does not improve unimodal performance.
7. Report whether each baseline was individually tuned or used the same hyperparameters, and discuss the potential impact.

## Score and Decision

### Calibration Anchors

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| A Theory of Unimodal Bias in Multimodal Learning | `ul1cjLB98Y.md` | 5.25 (Reject) | R1 | Yes | Theoretical paper on same problem space; cleaner framing but weaker empirical contribution than CCAT. |
| Two Effects, One Trigger | `uAFHCZRmXk.md` | 8.00 (Accept) | R1 | Yes | Significantly stronger paper — clean analysis, well-supported claims, no factual errors. Above CCAT. |
| Test-time Adaptation against Multi-modal Reliability Bias | `TPZRq4FALB.md` | 8.00 (Accept) | R1 | Yes | Significantly stronger — rigorous experiments, honest framing. Above CCAT. |
| Can One Modality Model Synergize Training | `5BXWhVbHAK.md` | 6.33 (Accept) | R2 | Yes | Stronger theory and narrative; fewer presentation issues. Above CCAT. |
| Smoothing the Shift (SuMi) | `rObkvzJxTG.md` | 5.50 (Accept) | R2 | Yes | Comparable — has weaknesses about fragmented method and limited evaluation but accepted. CCAT's issues (abstract error, MI mislabeling) are more concrete. |
| Cross-modality debiasing | `o1TKGCrSL7.md` | 4.75 (Reject) | R2 | No | Weaker empirical story. Below CCAT. |
| Mitigate the Gap (AlignCLIP) | `aPTGvFqile.md` | 6.29 (Accept) | R2 | No | Cleaner execution of a simpler idea. Above CCAT. |

**Round 1 bracket:** 4.5 – 6.5. Based on comparison with the theoretical unimodal bias paper (5.25, rejected) and the stronger accepted papers (6.33, 8.00).

**Narrowing (Round 2):** Compared against "Can One Modality Model Synergize Training" (6.33) and "Smoothing the Shift" (5.50), the current paper has stronger empirical results on KS (+6.76%) and a more novel core idea, but it is dragged down by:
- An arithmetic error in the abstract (favorability=-1.28 in draft review)
- A technically incorrect quantity label ("mutual information")
- Overclaimed theoretical framing (favorability=-0.59)
- Missing variance estimates (favorability=-0.85)

The 6.33 anchor has no comparable factual errors. The 5.50 anchor had issues about methodological fragmentation but no concrete errors. CCAT sits between these: stronger in empirical contribution than the 5.50 paper, but with more concrete (fixable) mistakes holding it back.

**Final Score: 5.0 — Reject.** The core method is well-motivated and the Kinetic-Sound results are genuinely strong. However, the combination of a factual error in the abstract, a technically incorrect quantity presented as "mutual information," overclaimed theoretical framing, and missing variance reporting means the paper is not ready for acceptance in its current form. These issues are fixable; a revised submission with corrected claims, proper terminology, and variance estimates would merit reconsideration.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>