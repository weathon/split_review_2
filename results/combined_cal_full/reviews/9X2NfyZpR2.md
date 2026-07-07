Now let me write the final review.

## Summary

This paper introduces TbLTA, the first framework for dense long-term action anticipation (LTA) trained exclusively from video transcripts — ordered action lists without timing or duration information — rather than expensive frame-level annotations. The architecture combines a temporal alignment module (ATBA) to generate pseudo-labels, a cross-modal attention layer to ground video features with transcript semantics, and a CTC/CRF-based training objective to enforce temporal coherence. Experiments on Breakfast, 50Salads, and EGTEA establish the first transcript-only baselines for dense LTA.

## Strengths

- **The problem is well-motivated and the core idea is sound.** Section 1 clearly articulates the annotation bottleneck in dense LTA — frame-level labels are expensive, and no prior work has attempted to eliminate them entirely. Using video transcripts (ordered action lists without timing/duration) as the sole supervision signal is a natural choice for LTA since the task is about understanding procedural structure.

- **The paper establishes the first transcript-only baseline for dense LTA across three benchmarks (Breakfast, 50Salads, EGTEA).** Tables 1 and 2 provide concrete reference points that future weakly-supervised LTA work can build on.

- **On Breakfast, the deterministic TbLTA model (29.03 average MoC) modestly outperforms the best fully-supervised method, ActFusion (28.45).** At 30% observation, TbLTA achieves 40.28 vs. 35.79 for ActFusion at 10% anticipation — a genuine result demonstrating that transcript-based supervision can capture procedural structure well on regular, stereotyped activities.

- **The stochastic Top-1 variant on Breakfast (37.15 average MoC) provides a useful upper bound** showing the potential of transcript-based models when multiple plausible futures are considered.

## Weaknesses

### Fatal
None.

### Major

- **Framing oversell of "competitive with fully supervised methods."** The abstract and conclusion claim TbLTA is "competitive with, and in certain settings even superior to, fully supervised methods" (lines 9, 291). The evidence is uneven: on Breakfast, TbLTA edges ActFusion by +0.58 MoC; on 50Salads, it lags by -7.47 (20.92 vs. 28.39); on EGTEA, it trails by -11.43 (65.37 vs. 76.80). The paper acknowledges these gaps in the text but retains unqualified "competitive" framing in the abstract and conclusion, overstating the results. The honest contribution — that transcript-only supervision works well on procedurally regular activities but struggles on harder benchmarks — is still interesting but requires reframing.

- **Ablation study uses the stochastic Top-1 metric rather than the deterministic metric, conflating model accuracy with sampling distribution changes.** Table 4 reports all ablations on the Top-1 variant, which selects the best among multiple stochastic samples. Removing a component could affect results in two confounded ways: (a) reducing core accuracy, or (b) changing the sampling variance (which affects how high the best sample can go). The paper states this choice is "for clarity" (line 231) but never reports deterministic ablation results, making it impossible to isolate component contributions for the model a practitioner would actually deploy. This is a significant methodological limitation.

- **Loss weight hyperparameters (γ₁, γ₂, γ₃) are not numerically specified.** These appear in lines 154, 164, and 168 for the alignment, CTC, and duration losses respectively, but their values are never stated in the main paper, making the method incompletely specified from the main text alone.

### Minor

- **The only weakly-supervised baseline (WS-DA, Zhang et al., 2021) is reported for a single configuration** (Obs 30%, one anticipation horizon) on each dataset (Table 1), making the comparison thin. The paper also discusses language-based methods (Kim et al., 2024) in related work without direct comparison, though this is partly justified since those methods tackle a different formulation (symbolic sequence prediction rather than dense frame-level forecasting).

- **The duration loss (Eq. 7, lines 182-186) has a circular dependency that is not discussed.** It trains a regressor using targets derived from the model's own pseudo-labels, stored in a momentum buffer. If the pseudo-labels misclassify frames, the duration estimates will be wrong and the loss will reinforce those errors.

- **No analysis of pseudo-label quality is provided.** The entire method hinges on pseudo-labels from the ATBA alignment module being good enough to supervise both segmentation and anticipation. Yet no analysis of pseudo-label accuracy vs. ground truth, or systematic error patterns, is given. This is a missed opportunity to understand where and why the method works or fails.

### Trivial
None.

## Nice-to-Haves

- Adding variance or confidence intervals to the results would be useful given the stochastic nature of the method and the small ablation differences (e.g., 0.2–0.8 points).
- A section analyzing failure modes would strengthen the paper by revealing whether errors correlate with specific action types, boundary transitions, or dataset characteristics.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **"First weakly-supervised approach" claim needing qualification.** REMOVED. The abstract says "the first weakly-supervised approach for LTA, which relies solely on video transcripts during training" — this specifically qualifies the supervision type. WS-DA (Zhang et al., 2021) uses frame-level labels for the observed segment and weak labels for the first future action; it is semi-weakly supervised, not transcript-only. The paper's claim is accurate.

2. **ATBA module contribution ambiguity.** REMOVED. The paper clearly states "we adopt the ATBA module proposed in (Xu & Zheng, 2024)" at line 126. The contribution claim in line 33 ("propose to temporally align video transcripts") refers to the application to LTA, not to inventing the module itself. The wording is sufficiently transparent.

3. **Missing comparison with language-based methods (Kim et al., 2024).** REMOVED as scope creep. The paper scopes itself to dense frame-level LTA (line 52-53: "we focus on the task of dense long-term action anticipation, where the aim is to generate frame-level forecasts"). Kim et al. predicts symbolic sequences, not dense frame-level predictions. The paper's scope is well-defined.

4. **EGTEA metric inconsistency (mAP vs. MoC).** REMOVED. The paper explains this follows the established evaluation protocol of Nagarajan et al. (2020) (line 194). Dataset-specific evaluation norms are standard practice.

5. **Qualitative results lacking failure mode analysis.** REMOVED as a nice-to-have that does not threaten core claims.

6. **Strength about stochastic Top-1 upper bound.** KEPT but reframed from "sets a high upper bound" to "provides a useful upper bound" to avoid implying it's a directly comparable result.

## Novel Insights

None beyond the paper's own contributions. The key insight that emerges from the review is that transcript-based supervision succeeds on procedurally stereotyped activities (Breakfast) but lags significantly on more varied or denser benchmarks (50Salads, EGTEA). This finding — which is implicit in the data but not explicitly discussed by the authors — is arguably the paper's most actionable result: it tells the community where transcript-only approaches are viable and where hybrid supervision is needed. The paper would benefit from making this diagnostic point explicitly.

## Suggestions

1. **Reframe the headline claim** to accurately reflect the evidence: transcript-only supervision works well on procedurally regular datasets (Breakfast) but lags on harder benchmarks (50Salads, EGTEA). This is a more honest and more interesting finding than the current "competitive with fully supervised" framing.

2. **Report all ablations on the deterministic model**, not just the Top-1 stochastic variant. Without this, it is impossible to assess which components actually improve the deployable model.

3. **Provide numerical values for γ₁, γ₂, γ₃** in the main paper.

4. **Add an analysis of pseudo-label quality:** what fraction of frames receive correct pseudo-labels? Are errors systematic (e.g., concentrated near action boundaries, or specific to certain action classes)?

5. **Expand the WS-DA comparison** to more configurations where published data exist, to give a more informative weakly-supervised benchmark comparison.

---

**Round 1 bracket:** 5.0–6.0  
**Closest anchors:** AntGPT (Bb21JPnhhr, avg 6.25) — an LTA paper with stronger positive results and weaker novelty; InterAct (sEARCNzhrP, avg 5.00) — a weaker paper with more severe novelty and claim-support issues. Our paper sits between these two.

**Weighted-item comparison:** Our draft's strongest positives (Breakfast outperformance +4.47, Top-1 upper bound +3.06) are weaker than AntGPT's strongest positives (SOTA benchmarks +4.89/+4.93, interesting question +7.70). Our strongest negatives (WS-DA thin -5.62, ablation on Top-1 -4.19) are less severe than AntGPT's negatives (limited novelty -8.36, marginal improvement -6.47). The trade-off places this paper below AntGPT but above InterAct, consistent with a score of 5.5.

**All anchor papers retrieved:**
- **5lUdTogEL3** (avg 1.00, Round 1, not itemized) — Clothing-Irrelevant ReID, completely unrelated topic.
- **2HdZPEQUig** (avg 3.00, Round 1, itemized) — Object-centric learning, weaker paper with severe evaluation issues.
- **sEARCNzhrP** (avg 5.00, Round 1, itemized) — Temporal action segmentation, weaker novelty and claim support.
- **HCoSsULNxG** (avg 4.75, Round 2, not itemized) — Weakly supervised activity understanding, moderately relevant.
- **oO3oXJ19Pb** (avg 4.80, Round 2, not itemized) — Dense video captioning, tangential topic.
- **Bb21JPnhhr** (avg 6.25, Round 1+2, itemized) — AntGPT, LTA paper with stronger results but weaker novelty.
- **f3CdjpPkSq** (avg 6.50, Round 1, itemized) — Action sequence augmentation, stronger novelty and results.
- **HEXtydywnE** (avg 6.00, Round 2, not itemized) — Weak supervision scene graphs, different task.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>