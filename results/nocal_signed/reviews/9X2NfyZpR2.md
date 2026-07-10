Now I have all the information needed. Let me synthesize the final review.

---

## Summary

This paper introduces TbLTA, the first fully weakly-supervised framework for dense long-term action anticipation that relies solely on video transcripts (ordered action lists without timing or duration) during training. The architecture uses a temporal alignment module to generate pseudo-labels, then leverages cross-modal attention, CTC loss, CRF-based sequence coherence, and a self-supervised duration loss to train an encoder-decoder for frame-level future prediction. Experiments on Breakfast, 50Salads, and EGTEA show that transcript-only supervision can produce competitive results on procedurally regular datasets, outperforming all fully-supervised methods on Breakfast at Obs 30%.

## Strengths

- **First fully weakly-supervised LTA framework using only transcripts.** Prior LTA work requires dense frame-level annotations (Abu Farha et al., 2018; Gong et al., 2022b; 2024) or at-minimum temporally localized human annotations (Zhang et al., 2021). TbLTA eliminates all frame-level supervision by relying solely on ordered action lists without timing or duration. Given the annotation cost of dense LTA labels, this direction is well-motivated and the paper's primary contribution is genuine.

- **Competitive results on Breakfast at Obs 30%.** Table 1 shows TbLTA (deterministic) achieving 40.28, 35.76, 31.67, 28.79 at Obs 30% across all prediction horizons on Breakfast — surpassing all supervised baselines including ActFusion (35.79, 31.76, 29.64, 28.78). This is a non-trivial result, suggesting that on datasets with strong procedural regularities, transcript-level order information can partially substitute for frame-level labels.

- **Ablations isolate component contributions.** Table 4 shows meaningful degradation when removing each component: CTC (~0.6–0.8 pts), cross-attention (~1.3–5.7 pts depending on dataset), CRF (~4.1–5.3 pts at long horizons), and duration loss (~0.2–3.3 pts). These ablations demonstrate that all proposed modules contribute, and the large cross-attention drop on Breakfast (5.7 pts) indicates the cross-modal design is not redundant with the alignment module.

## Weaknesses

### Major

- **Text/table discrepancy in the duration loss ablation.** The ablation text (§4.3, "Effect of duration loss") states that removing the duration loss reduces accuracy by ≈0.2 on 50Salads. However, Table 4 shows a 2.2 point drop (TbLTA avg 28.5 vs. w/o duration avg 26.3). The Breakfast figure (≈3.3) correctly matches the table (37.2 − 33.9 = 3.3). This is a factual inconsistency that needs correction — regardless of whether the intended number is ≈2.2 or refers to a specific sub-condition, the presentation as given does not match the evidence.

### Minor

- **Incomplete weakly-supervised baseline comparison.** The only comparable weakly-supervised method (WS-DA, Zhang et al., 2021) is reported at only a single setting per dataset (Obs 30% only) — all other cells in Table 1 are dashes. Consequently, the paper does not establish a meaningful weakly-supervised comparison for most of the 16 evaluated settings. While this partly reflects the limited published results from WS-DA (which is itself a semi-weakly method that still uses some frame-level labels), the paper's framing as "the first fully weakly-supervised LTA framework" would be strengthened by a more complete comparison or an explicit discussion of why these numbers are unavailable.

- **EGTEA evaluation is too thin to support the claims drawn from it.** Table 2 compares TbLTA against only two supervised baselines. TbLTA achieves 65.37 mAP (All) vs. Anticipatr's 76.80 — an 11.4 point gap. The claim about competitiveness on rare classes rests on a 0.41 point improvement over Timeception (60.11 vs. 59.70) against these two baselines alone. No weakly-supervised baseline is reported for EGTEA at all. This provides limited support for the statement that "high-level semantic supervision from transcripts can mitigate data imbalance."

- **No variance or statistical significance reported.** Results in Tables 1, 2, and 4 are reported as point estimates without standard deviations, even though they are averaged over 4–5 folds on small datasets (50Salads has only 50 videos). Without variance estimates, it is difficult to assess whether reported improvements are statistically reliable or within the noise of the evaluation.

- **Stochastic protocol insufficiently explained in the main text.** The Top1 stochastic results in Table 1 are the paper's strongest numbers (e.g., 37.15 avg on Breakfast vs. 29.03 deterministic, and 28.51 on 50Salads vs. ActFusion's 28.39). Yet the main text mentions the stochastic protocol only in a single sentence: "We also report the stochastic protocol of Abu Farha & Gall (2019) in the supp. mat." The main text should at minimum explain how multiple futures are generated and how Top1 is selected, so readers can assess whether these numbers are directly comparable to deterministic single-output methods. (The supplementary material, stripped by the parser, likely contains these details.)

### Trivial

None.

## Nice-to-Haves

- Include a "w/o CTC" row directly in the LTA ablation (Table 4) to show CTC's contribution to anticipation, rather than relying on a separate IAS table.
- Expand the EGTEA evaluation with additional baselines (even if only supervised ones) and weakly-supervised comparisons if available.
- Report per-fold results or confidence intervals for the main benchmarks, especially for 50Salads where variance is likely higher due to small sample size.

## Removed Points

These points are flagged to be removed; treat them with caution:
- **Loss weights not specified in main text (γ₁, γ₂, γ₃):** REMOVED per hard rule — the parser strips the appendix/supplementary material where these values reside; they exist in the original submission.
- **"as shown in 3" incomplete reference:** REMOVED per hard rule — the reference is to Table 3 (IAS), which was in the appendix that was stripped.
- **Table 4 duplication:** REMOVED as a parser artifact.
- **CRF/stochastic variant confusion in Related Work:** REMOVED — the paper frames its overall approach as having a stochastic variant (via the Abu Farha & Gall protocol), not that the CRF itself generates stochastic outputs. The transition is slightly unclear but does not affect core claims.
- **Abstract "robust" claim unsupported:** REMOVED — the abstract's claim is about transcript supervision being a "robust and less costly alternative," and the paper extensively qualifies this with dataset-dependent performance discussion in §4.2.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the text/table discrepancy** for the duration loss ablation on 50Salads (≈0.2 → correct value of ≈2.2, or clarify the specific sub-condition being reported if that is the intent).
2. **Expand the main-text description of the stochastic protocol** — explain how multiple futures are generated and how Top1 is selected, so the paper's strongest results can be properly interpreted without requiring readers to consult the supplementary material.
3. **Add variance estimates** — report standard deviations or per-fold results for the main tables, especially for 50Salads.
4. **Complete or honestly qualify the WS-DA comparison** — either obtain the missing numbers from the original method's protocol or explain explicitly why they are unavailable.
5. **Include a "w/o CTC" row in the LTA ablation** (Table 4) to directly show CTC's contribution to anticipation.

## Score and Decision

The paper's core contribution — the first fully weakly-supervised LTA framework using only transcripts — is genuine and well-motivated. The architecture is coherent, the ablations are informative, and the competitive results on Breakfast at Obs 30% are non-trivial. The weaknesses are real but addressable: the text/table discrepancy is a presentation error (not a methodological flaw), the incomplete WS-DA comparison partly reflects the limited published baselines, and the EGTEA evaluation is supplementary to the main contribution. The stochastic protocol is likely fully described in the appendix. None of the weaknesses invalidate the core claim.

Taking these factors together with the per-item impact signals (very strong strengths, mild-to-moderate weaknesses), the paper merits a score in the borderline-accept to accept range.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>