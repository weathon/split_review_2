Now I have sufficient calibration context. Let me finalize the review.

**Round 1 bracket:** Based on calibration, this paper sits in the 5.5–7.5 range. The most directly comparable anchor is "Expand and Compress" (EAC) at avg 6.75, which addresses the exact same problem (continual ST forecasting with prompt tuning on a frozen backbone). STBP has stronger architectural novelty (FreNet + DLGA vs. simple prompt pool) and better efficiency analysis, but has mixed results on AIR-Stream and a more significant evaluation gap (no forgetting measurement). The EAC paper itself didn't measure forgetting with per-period breakdowns either, but EAC also didn't list "mitigating catastrophic forgetting" as a standalone central claim in the same way. I narrow to 5.5–6.5 based on these comparisons.

Here is the final consolidated review.

---

## Summary

This paper proposes STBP, a framework for continual spatio-temporal forecasting that cleanly separates a general-purpose backbone (frequency-domain temporal module + dual-stream linear graph attention) from an incrementally-expanding contextual pattern bank. The backbone is frozen after the first training period to preserve general knowledge, while the pattern bank is expanded and fine-tuned to adapt to new nodes and distributions. Experiments on three real-world streaming datasets show strong improvements on traffic data and more modest gains on air-quality data.

## Strengths

1. **Principled architectural decomposition.** The separation of a frozen general-purpose backbone (handling stable patterns) from an incrementally-expanding pattern bank (handling node-specific adaptation) is a well-motivated response to the "stability vs. adaptability" tension. This is a genuine improvement over existing CSTF work where the backbone and continual-learning strategy are often weakly coupled.

2. **Strong results on PEMS-Stream and CA-Stream.** MAE reductions of ~21% over the best CSTF baseline are substantial and consistent across all forecasting horizons. The few-shot results (Table 2) similarly show clear margins (MAE 13.58 vs. EAC 16.13 on PEMS-Stream 10%). These gains are meaningful by community standards.

3. **Concrete efficiency and scalability evidence.** Figure 8 directly compares training time vs. MAE with scatter size encoding GPU memory, and the toy-dataset study verifies O(N) memory scaling. This targeted analysis is valuable for a continual-learning method where per-period cost is a practical concern.

4. **Qualitative pattern bank analysis.** The t-SNE visualization (Figures 3, 6) demonstrates that the learned pattern bank discovers semantically meaningful node clusters and correctly groups newly-added nodes into existing clusters, validating the "relevance and heterogeneity" claim beyond aggregate metrics.

## Weaknesses

### Major

- **No direct measurement of catastrophic forgetting.** The paper lists "alleviating catastrophic forgetting" as one of its four key challenges and identifies it as a central contribution (abstract, §1, §4.2), yet the evaluation never directly measures forgetting. Standard continual-learning evaluation includes per-period accuracy trajectories, backward-transfer metrics, or explicit forgetting scores. The paper reports only metrics averaged over all periods — a model could maintain decent average performance while degrading on early periods. The architectural design (frozen backbone) is a principled mitigation strategy, but the paper does not empirically validate that it succeeds. This is the most significant gap, as it leaves the core continual-learning claim under-supported.

### Minor

- **The claim of universal superiority is slightly overstated.** The paper states "STBP outperforms all competing models" (line 238) and highlights MAE improvements of 2.35–21.93%. On AIR-Stream, however, STBP underperforms the best baseline on RMSE at horizons 6 (39.81 vs. 39.63) and 12 (44.97 vs. 44.65). The MAE advantage on this dataset is small (2.35%), and the RMSE pattern is not discussed. The full table is reported, so the reader can draw their own conclusions, but the narrative would be more accurate if qualified.

- **Ablation study includes EAC as a comparison variant.** Figure 4 lists "EAC" alongside component ablations like "w/o Backbone" and "w/o DLGA." EAC is a separate published method, not an STBP variant. While the paper explains this inclusion, a clearer separation between component ablation and baseline comparison would avoid the impression that EAC is being positioned as a component of STBP.

- **Baseline setup for static STGNNs is uninformative.** GWNet and STID are retrained from scratch each period using only current-period data, guaranteeing poor performance since they cannot leverage any historical knowledge. The paper transparently acknowledges this (citing prior work), and the proper CSTF baselines (TrafficStream, STKEC, PECPM, STRAP, EAC) provide the meaningful comparison. Still, including these methods inflates the apparent gap between "conventional" and "continual" approaches.

- **Ambiguous notation in Eq. 5.** The operation denoted by `·` in H'_τ = P_τ^(1) · h_θ(H_τ · (1 + P_τ^(0))) is not specified; both operands are ℝ^{N×d}. Clarifying this would improve readability.

### Trivial

None.

## Nice-to-Haves

- Per-period accuracy breakdowns and a forgetting-score curve would directly support the catastrophic-forgetting claims.
- Statistical significance tests (e.g., paired t-test) for the AIR-Stream comparison where the MAE advantage is only 2.35%.
- The in-text discussion could acknowledge the mixed RMSE on AIR-Stream and offer a hypothesis (e.g., hourly-sampled meteorological data vs. 5-minute traffic data).

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

- **Table garbling (Issue 2):** Parser artifact — the original submission does not have this problem. Removed per instructions.
- **Missing appendix content (number of periods, per-period dataset details, proofs):** Appendix sections are stripped by the parser; assumed present in the original submission. Removed per instructions.
- **Code/data availability concerns:** Removed per instructions on reproducibility nitpicks.
- **"Number of experimental runs not stated":** Minor reproducibility nitpick. Removed.
- **"Section-by-section notes about §2, §4.3, §5.2 framing":** Speculative discussion points that do not identify concrete errors in the paper.
- **"The 'w/o Backbone' naming is misleading":** The paper clearly explains what this ablation does; the criticism is not valid.
- **"Related work overlap concern":** This is a framing preference, not an error. The paper distinguishes its prompt interaction mechanism from prior pattern bank methods.
- **"Strengthening the Paper on Its Own Terms" points about diagnostic experiments:** These are suggestions for additional work, not flaws in the existing paper.
- **Various minor presentation nitpicks:** Removed as not substantive.

## Novel Insights

The most valuable observation from the reviewing process is that the paper's central claim about catastrophic forgetting is evaluated only indirectly — through aggregate accuracy and architectural design — rather than through direct metrics (per-period breakdown, backward transfer). This is a genuine gap that the authors could address with additional experiments without changing the method. The AIR-Stream RMSE pattern (STBP loses on two of three horizons despite winning on MAE) is also worth probing further, though it does not invalidate the paper's overall contribution.

## Suggestions

1. Add per-period accuracy trajectories and a forgetting metric to directly support the catastrophic-forgetting claims.
2. Qualify the universal-outperformance claim to note that on AIR-Stream the advantage is mainly in MAE, with mixed RMSE performance at longer horizons.
3. Separate the ablation figure into: (a) component ablations of STBP, and (b) baseline comparisons against methods like EAC.
4. Clarify the operation in Eq. 5.
5. Consider refocusing the "conventional methods" discussion to emphasize the CSTF baselines over retrained-from-scratch STGNNs.

## Score and Decision

Based on calibration: The closest anchor is "Expand and Compress: Exploring Tuning Principles for Continual Spatio-Temporal Graph Forecasting" (EAC, avg 6.75, scores 3/8/8/8), a directly comparable paper on the same problem. STBP has stronger architectural novelty (FreNet, DLGA, three-group pattern bank) and better efficiency analysis, but weaker results on one of three datasets (AIR-Stream) and a significant evaluation gap (no direct forgetting measurement). The "Learning system dynamics without forgetting" paper (avg 6.25, scores 5/6/6/8) and "DyGPrompt" (avg 6.0, scores 6/6/6/6) provide additional anchors at the lower end of the bracket.

**Round 1 bracket:** 5.5–7.5 (anchored by EAC at 6.75)
**Final:** Given the evaluation gap and the overstated claim, I place STBP slightly below EAC at 6.0 — a borderline accept with clear contributions that need strengthening in evaluation rigor.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>