## Summary

This meta-scientific paper presents a detailed case study re-analyzing the ICLR 2025 Oral paper "Min-P Sampling" (Nguyen et al., 2024) across its four lines of evidence. The authors demonstrate that the original paper's own data do not support its central claims, identifying specific errors: omitted baseline data comprising 1/3 of human evaluations, incorrect statistical testing (pooling across conditions, no multiple comparison correction), mischaracterized qualitative responses, selectively reported LLM-as-a-Judge results, and unsubstantiated community-adoption claims. The paper contributes a "Best-of-N" methodology for fair comparison when methods differ in hyperparameter tuning volume, and derives general lessons for rigorous empirical ML research. The analysis across 9 models × 2 stages × 4 samplers × 31 temperatures × 6 hyperparameters (~6000 A100-hours) consistently shows Min-p does not outperform baselines when tuning is equalized.

---

## Strengths

1. **Concrete, documented flaws backed by the original paper's data.** The paper identifies specific verifiable errors: (a) Basic sampling scores comprising 1/3 of human evaluation data were collected but excluded from the published methodology without mention (Sec. 2.1); (b) the original paper's statistical test pooled across conditions and failed to correct for multiple comparisons — after proper analysis, only 1/12 comparisons survive Bonferroni correction (Table 1); (c) manual re-annotation of qualitative responses shows more evaluators preferred Basic than Min-p (Fig. 2), directly contradicting the original's claim; (d) LLM-as-a-Judge results reported the higher of two scores for Min-p (52.01 vs 50.14) but the lower for Top-p (50.07 vs 50.43) (Sec. 4.3); (e) claimed 54k repositories/1.1M GitHub stars were unsubstantiated and later retracted (Sec. 5). Each finding is backed by the original paper's own publicly available data.

2. **The Best-of-N hyperparameter-control methodology (Sec. 3).** This is a genuine practical contribution: a simple, transparent technique for comparing methods when they receive different volumes of hyperparameter tuning. The analysis is thorough and consistently shows Min-p does not outperform baselines when tuning is equalized (Figs. 4, 5).

3. **Constructive engagement with original authors.** The paper documents multiple interactions: confirming the omitted data, being directed to the high-diversity setting, having the original authors conduct a new human evaluation and update their camera-ready, and correcting their own prompt formatting after the original authors flagged an issue (Sec. 3). This demonstrates scientific good-faith.

4. **The paper practices the rigor it advocates.** The authors apply Bonferroni correction, Intersection-Union Test, confidence intervals, and visualization. They release their annotations publicly and are transparent about their key limitation (Sec. 6).

---

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Selective focus on the high-diversity condition in the human evaluation re-analysis (Sec. 2.2).** The paper excludes the "low diversity" setting from its re-analysis, justified by three reasons (the original authors said to focus on high diversity, top-p's hyperparameter was poorly chosen in low diversity, and the claim is about the quality-diversity tradeoff). These justifications are reasonable, but the decision creates a tension with the paper's own sharp critique of the original for omitting data without mention (Sec. 2.1). The paper would be stronger if it showed that including the low-diversity data does not change conclusions, or offered a more formal exclusion criterion. As written, this is an asymmetry in the paper's own evidential standards — though the paper acknowledges and justifies the choice, unlike the original.

2. **NLP benchmark evaluation limited to GSM8K CoT; GPQA not covered.** The paper acknowledges this is due to compute budget (~6000 A100-hours), which is understandable. However, the original paper reported results on both GSM8K and GPQA, so the re-analysis does not fully cover the original's benchmark claims. The paper notes results were "nearly identical" for corrected prompt formatting and that Min-p produced higher scores for 2 of 12 models. Without GPQA, we cannot be certain whether the original's strongest claim would have held on a different benchmark.

3. **The Best-of-N analysis has an asymmetry in hyperparameter counts that merits more explicit discussion.** Basic sampling has 31 unique settings (31 temperatures × 1 parameter), while other samplers have 186 (31 temperatures × 6 hyperparameter values). When subsampling N settings, Basic's maximum converges to its true ceiling as N approaches 31, while others have far more settings. The paper addresses this by extending N to 100 (sampling Basic with replacement), and the consistent finding that Min-p does not outperform even at N=100 is persuasive. However, this asymmetry and the fact that sampling with replacement from 31 settings differs from sampling without replacement from 186 deserves a clearer acknowledgment.

### Trivial
None.

---

## Nice-to-Haves

- Include the low-diversity setting in the human evaluation re-analysis to show conclusions are unchanged, removing the asymmetry with the paper's own critique of data omission.
- Run the NLP benchmark analysis on GPQA (even with a smaller model subset) to close the gap with the original paper's claims.
- Add a summary table mapping each original-paper claim → original evidence → re-analysis finding → general lesson for easier reference.
- The data discrepancy finding (reported 7.80 vs computed 5.80 in Sec. 2.4) is mentioned in passing; if confirmed as a genuine error, it deserves more prominence.
- Include a brief reproducibility statement about whether the original paper's code ran without modification.

---

## Removed Points

*These points were flagged during review but removed after verification against the paper; they are listed here only for transparency and should be treated with caution.*

- **"Introduction is self-indulgent with citations"** — A rhetorical style observation about the number of citations in one sentence (line 13). Does not affect substance; removed as a style nitpick.
- **"Could have used a less conservative correction (Holm-Bonferroni, BH)"** — This would only strengthen the paper's argument. The choice of Bonferroni is standard and defensible. Moved to nice-to-have.
- **"LLM-as-a-Judge section is weaker than others"** — Vague qualitative assessment without specific actionable content. Removed.
- **"No formal reproducibility assessment of the original paper's code"** — The paper uses the original code extensively (Sec. 3) and documents running it; this is a stretch as a weakness. Moved to nice-to-have.
- **"The paper could include a summary table"** — A presentation suggestion, not a weakness.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. In Sec. 2.2, include an analysis showing that including the low-diversity setting does not change the conclusions, to remove the evidential asymmetry with the paper's own critique of data omission.
2. In Sec. 3, add an explicit paragraph discussing the hyperparameter-count asymmetry in the Best-of-N analysis and why the N=100 results are robust despite sampling Basic with replacement from only 31 settings.
3. If the 7.80 vs 5.80 data discrepancy (Sec. 2.4) can be confirmed as an error, give it more prominence; if not, add a hedging clarification.

---

## Calibration Analysis

**Anchors retrieved:**
| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Im2neAMlre.md` (One slice is not enough) | 7.33 | Round 2 | Yes | Closest analogue: meta-evaluation paper with rigorous methodology, exhaustive experiments, practical contribution. The current paper has stronger methodological contribution (Best-of-N) and more consequential findings (exposing errors in an ICLR Oral). |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/lf8QQ2KMgv.md` (Is Memorization Actually Necessary?) | 3.75 | Round 2 | Yes | Re-analysis paper rejected because its criticisms were viewed as unfounded (-4), it failed to replicate key analyses (-4), and its fixes changed the setup unfairly (-4). The current paper has none of these fatal issues — its criticisms are well-documented, verified with original authors, and the results are robust. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/xI71dsS3o4.md` ((Mis)Fitting Scaling Laws) | 5.75 | Round 1 | Yes | Survey/critique paper; criticized for being "just a survey" (-3) and lacking empirical results (-2). The current paper is much more empirically grounded with ~6000 A100-hours of experiments and a novel methodology. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/icTZCUbtD6.md` (Dissecting Sample Hardness) | 6.20 | Round 1 | Yes | Taxonomy/benchmarking paper with toolkit contribution. Criticized heavily for limited scope (-4, -5 weights on dataset limitations). The current paper's weaknesses are milder (scope limitations acknowledged, conclusions unaffected). |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/pf9J3GNxSe.md` (Critical Phase Transition) | 4.50 | Round 1 | Yes | LLM sampling paper; criticized for unclear implications (-4), narrow model scope (-4). Not a close analogue. |

**Bracket reasoning (Round 1):** The paper's weaknesses are all Minor — no fatal or major issues. Its strengths (concrete documented flaws, genuine methodological contribution, extensive experiments, constructive engagement with authors) are strong. This places it well above the 3.75-5.75 range of flawed critique papers and above the 6.20 anchor whose weaknesses were more severe. The closest analogue (Im2neAMlre, 7.33) shares the same profile: rigorous methodology, exhaustive experiments, practical contribution. The current paper's Best-of-N methodology is a stronger standalone contribution than the benchmark release in Im2neAMlre, and its findings (exposing errors in a published Oral paper) are more consequential.

**Narrowing (Round 2):** The paper lacks the heavy-weight negative items that brought down lf8QQ2KMgv (-4 weight on "critique unfounded," -4 on "failed to replicate," -4 on "setup changed unfairly") and icTZCUbtD6 (-5 on "unsatisfying categorization," -5 on "contradictory claims"). Its own weaknesses (data exclusion tension, missing one benchmark, asymmetry discussion) are all Minor — none carry the weight of fundamental methodological flaws. This puts the paper solidly above all anchors except Im2neAMlre (7.33), and marginally above it given the stronger methodological contribution.

**Final bracket:** 7.0–8.0 → **7.5**

---

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>