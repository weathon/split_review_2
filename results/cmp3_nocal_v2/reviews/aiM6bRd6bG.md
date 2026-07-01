## Summary

This paper introduces a PPI candidate ranking problem: given a target protein with known interaction partners, rank candidate novel partners to prioritize experimental validation. The proposed two-stage framework first uses D-SCRIPT/Topsy-Turvy's internal contact maps to identify "active residues" from known interactions, then computes cosine similarity between these active regions and candidate proteins. A second re-ranking stage integrates interaction scores, structural plausibility (pDockQ via SpeedPPI), functional annotations, and LLM-based semantic signals. Evaluation uses STRING v11 interactions as "known" and STRING v12 additions as ground truth, producing clear early-ranking improvements (5–32× depending on metric).

## Strengths

**Prospective evaluation design (STRING v11→v12, Section 5.1).** Treating v11 interactions as known and v12 additions as novel is a genuinely more meaningful test than standard retrospective splits. It asks whether methods can anticipate interactions confirmed only in a later database release, avoiding inflation from cross-validation artifacts within a single snapshot.

**Well-motivated problem framing (Section 4).** Aligning evaluation with the actual use case—ranking candidates for expensive experimental testing rather than binary classification—is practically important. The formal setup (KP(p), NP(p), ranking over P \ KP(p)) is clean and reproducible.

**Measurable early-ranking gains (Table 1).** Improvements at top ranks are substantial: D-SCRIPT-based Recall@10 rises from 0.0124 to 0.2641 (~21×), MRR from 0.0340 to 0.1685 (~5×), and Success@5 from 0.0000 to 0.0778. These are practically meaningful for experimental screening.

## Weaknesses

### Major

**1. The "two orders of magnitude" claim is factually unsupported (Lines 25, 279).**

The paper states twice that it "improves ranking metrics by two orders of magnitude" (i.e., 100×). The largest measurable improvement in Table 1 is approximately 32× (Success@10: 0.0040 → 0.1277). Most metrics improve by 5–26× (Recall@5: 25.8×; MAP@5: 26.4×; MRR: ~5×). No metric approaches 100×. Even the paper's own discussion acknowledges "4–6 times" improvement for MRR (line 233). This is a factual error in a headline claim. Correcting it to "up to 32× improvement" would be accurate and still impressive, but the current exaggeration undermines credibility.

**2. The evaluation does not isolate whether gains come from the interpretability-guided active-region extraction vs. simply using known partners (Table 1).**

The baselines rank candidates by raw D-SCRIPT/Topsy-Turvy interaction scores, using no information about known partners. The proposed method uses known partners KP(p) as anchors and computes similarity between candidates and these anchors. The critical missing control is a baseline that also leverages known partners via full-embedding cosine similarity *without* the active-region extraction. Without this ablation, it is impossible to tell how much of the gain comes from (a) the interpretability-guided active-region extraction (the paper's claimed mechanism) vs. (b) simply using known partners with full-embedding similarity. The paper's central framing emphasizes "interpretability-guided" ranking, but the current evidence does not isolate this component's contribution.

### Minor

**3. Re-ranking evaluation is limited to top-10 candidates and measures rank shifts, not discovery (Section 4.2, Table 2).**

The re-ranking module only operates on the top-10 candidates from the initial retrieval. If a true novel partner was not ranked in the top 10, it is excluded from analysis. The metric in Table 2—fraction of v12 interactions whose ranking was maintained or improved—only measures relative rank changes within an already-retrieved set. It does not measure whether re-ranking brings *new* true positives into the top 10 or pushes false positives out. The claim that Table 2 "highlights the strength of semantic signals" (line 265) would be better supported by measuring whether re-ranking discovers novel partners that would otherwise be missed.

**4. No statistical uncertainty reported (Table 1, Table 2).**

All results are point estimates without standard deviations, confidence intervals, or significance tests. Since per-protein ranking difficulty varies with protein properties and the number of known partners, the reader cannot assess whether improvements are consistent or driven by a subset of favorable cases.

**5. Potential overlap between ground-truth signal and the structural re-ranking signal (Section 5.1).**

The paper notes that STRING v12's new interactions are "driven by high-throughput experiments and structure-based predictions" (line 194). The re-ranking module uses SpeedPPI (built on AlphaFold2) to compute pDockQ scores. If some STRING v12 interactions were included based on AlphaFold2-related predictions, then evaluating pDockQ-based re-ranking against this ground truth risks circularity for those entries. The paper does not discuss what fraction of v12 novel interactions have structural vs. purely experimental evidence. This does not affect the main retrieval results (which don't use structural signals), but it weakens interpretation of the pDockQ re-ranking findings.

### Trivial

- The contiguous binding interface assumption (selecting a single contiguous active region from the contact map) is acknowledged neither in the method description nor in the limitations section. Many proteins have discontinuous binding epitopes or multiple interfaces. This is a modeling assumption worth noting.

## Nice-to-Haves

- **Add a full-embedding cosine similarity baseline** that uses known partners as anchors without the active-region extraction. This would isolate whether the interpretability-guided component adds value beyond simply leveraging known partners.
- **Enrich the re-ranking evaluation** by measuring what fraction of true novel partners enter the top-10 after re-ranking that were not there before, and whether different re-ranking signals discover complementary sets of novel partners.
- **Report per-protein breakdowns** of performance by properties such as the number of known partners, protein class, or interface characteristics, to identify where the method works best.

## Removed Points

- **"Interpretability-guided framing is overclaimed"** — Removed because the paper explicitly clarifies its definition: "we do not frame interpretability here as a means to generate explanations for users; rather, we leverage interpretable model structures as a methodological device to exploit internal representations for ranking" (Section 1, line 21). The reviewer's criticism ignores this clarification.
- **"Baseline comparison strategy is underspecified"** — Removed because the context (ranking by raw predicted interaction scores for (p, p_c) pairs) is clear enough from Table 1's labeling and standard practice.
- **"CD-HIT at 40% identity may be too aggressive"** — Removed because 40% identity clustering is a standard redundancy reduction threshold in the PPI literature, not a specific weakness of this paper.
- **"Missing limitations (computational cost, contiguous interfaces)"** — Removed because the paper mentions runtime ("hundreds of hours," line 233) and the contiguous-interface assumption is a minor modeling choice, not a central weakness.
- **"xCAPT5 discussion is confusing"** — Removed because the paper does discuss xCAPT5's early precision (line 233), and its overall weaker recall/MRR/Success justifies the paper's primary focus on D-SCRIPT and Topsy-Turvy.
- **"10:1 negative ratio acknowledged to produce easy negatives"** — Removed because the paper acknowledges this honestly as standard practice; it's not a weakness.
- Various formatting/style nitpicks and section-by-section opinions — Removed as non-substantive.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Correct the "two orders of magnitude" claim to actual numbers (e.g., "up to 32× improvement in early ranking metrics").
2. Add a full-embedding cosine similarity ablation (using known partners without active-region extraction) to isolate the contribution of the interpretability-guided component.
3. Report confidence intervals or per-protein variance for the main retrieval metrics.
4. For the re-ranking analysis, measure whether additional true positives enter the top-10 after re-ranking, not just rank shifts within a fixed set.
5. Acknowledge and discuss the potential overlap between STRING v12's structure-based predictions and the pDockQ re-ranking signal.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>