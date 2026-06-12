## Summary

This paper presents a detailed re-analysis of "Turning Up the Heat: MIN-P Sampling for Creative and Coherent LLM Outputs" (Nguyen et al., 2024), an ICLR 2025 Oral paper. Through four lines of investigation—human evaluations, NLP benchmarks, LLM-as-a-Judge evaluations, and community adoption claims—the authors demonstrate that the original paper's own data invalidate its central claims about min-p's superiority. The paper derives six general lessons for rigorous empirical ML research, though these lessons are standard best practices rather than novel methodological contributions.

## Strengths

1. **Well-documented omitted-data finding (Section 2.1):** The paper discovers that one-third of the original human evaluation data (basic sampling scores) was excluded without justification, and shows that including this data changes the paper's conclusions. This finding is specific, confirmed with the original authors, and clearly presented.

2. **Correct statistical re-analysis with Intersection-Union Test (Section 2.2, Table 1):** The paper correctly applies Bonferroni correction (12 comparisons) and IUT logic to the original claim of "consistent outperformance across all settings"—finding the largest p-value is 0.378, which fails to reject the null. This level of statistical rigor is rare in ML research and provides a template for similar critiques.

3. **Large-scale controlled NLP benchmark sweep (Section 3.1, ~6000 A100-hours):** The paper runs an extensive sweep across 9 models, 2 stages, 4 samplers, 31 temperatures, and 6 HPs per sampler. The Best-of-N analysis controlling for hyperparameter volume is a reasonable approach to testing whether min-p's claimed superiority holds under fair comparison.

4. **Direct evidence that retracted claims swayed peer review (Section 5):** The paper documents that 3 of 4 ICLR 2025 reviewers and the Area Chair cited the retracted 1.1M-GitHub-stars claim as the main justification for acceptance—providing unusually direct evidence of how unsubstantiated ancillary claims can influence top-venue decisions.

5. **Manual re-annotation of qualitative human responses (Section 2.3, Fig. 2):** The authors manually annotate and release the original paper's qualitative preference data, finding 21 evaluators preferred basic sampling vs. 12 who preferred min-p—directly contradicting the original paper's characterization.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **The LLM-as-a-Judge section (Section 4) is noticeably weaker in evidential quality than the other sections.** The paper flags methodological under-specification and presents evidence of selective reporting (Section 4.3, via a Telegram link) and unequal HP tuning (Section 4.2, from "ongoing work to publish"). These are valid concerns, but the section does not constitute an independent re-analysis of the same rigor as Sections 2 and 3—it flags problems rather than providing controlled re-analyses. The paper should either strengthen this section with proper controlled comparisons or explicitly temper the conclusions drawn from it.

2. **The Best-of-N analysis (Section 3.1) addresses a related but slightly different question than the most direct test of the original claims.** The analysis answers "does min-p outperform when HP volume is equalized via random subsampling?" rather than the more direct question of whether the original HP choices were fairly selected. While the former is a reasonable and informative test, the paper would benefit from a more precise framing of what this analysis establishes. The paper's conclusion that min-p "does not outperform" under this analysis is supported, but the evidential link to the original paper's specific HP selection process is indirect.

3. **HP values were "lightly edited" from the original paper's values (line 133).** The paper states that HP values for each sampler "were taken from the original paper; some were lightly edited to make them more evenly distributed." If the original paper selected specific values that work well for each sampler, perturbing them could advantage samplers whose values happen to generalize better rather than those that are genuinely best. The paper should justify these edits or use the original values exactly.

4. **Inter-rater reliability is not reported for the qualitative annotation (Section 2.3).** The manual re-annotation of human evaluators' qualitative preferences appears to be a single-author coding. Since the paper criticizes the original for potentially biased qualitative summaries, it should hold itself to the same standard by reporting agreement metrics or using multiple annotators.

5. **No statistical power analysis for the human evaluation re-testing.** The re-analysis uses 12 one-sided t-tests with df=52 each. The paper does not discuss whether the study had adequate power to detect meaningful differences—failure to reject the null may partly reflect low power rather than true equality. The paper correctly notes that the original claim is unsupported, but acknowledging this nuance would strengthen the analysis.

6. **The lessons in Section 6 are well-taken but not novel.** The six lessons (control for HP volume, apply stats correctly, demand data transparency, etc.) are standard best practices already well-articulated in the ML reproducibility literature. The paper's primary value is as a thorough documentation of failures in a prominent publication, not as a methodological innovation. The claim that the Best-of-N analysis is a "novel methodology" overstates the case—it is a reasonable tool but not technically novel.

### Trivial
None.

## Nice-to-Haves
- Clarify the Best-of-N subsampling procedure: when N > 6 (the number of HP values per sampler), is sampling done with or without replacement? The effective configuration space is 31 temps × up to 6 HPs = 186 configurations; N=100 is feasible without replacement only if this is the effective space.
- Add a brief statistical power analysis or acknowledge the limitation for the human evaluation t-tests.
- If possible, strengthen the LLM-as-a-Judge section with a proper controlled re-analysis, or explicitly downgrade the conclusions from this section to observations about under-specification.

## Removed Points

- "The abstract and introduction reads like a citation dump" — removed as a formatting/style nitpick.
- "The paper would be stronger if it cited fewer papers more selectively" — removed as a style nitpick.
- "The paper would be strengthened by deepening [Sections 2 and 5] rather than broadening into the weaker LLM-as-a-Judge analysis" — removed as scope creep; the paper is a comprehensive re-analysis.
- The harsh critic's claim that the Best-of-N analysis "conflates two separate issues" in a way that weakens the central argument — the exaggerated framing is removed; the actual concern (indirectness of the test) is retained in weakness #2 above.
- Strength Finder's claim of "novel Best-of-N methodology" — the methodology is useful but not genuinely novel; this is now reflected in weakness #6.

## Novel Insights

None beyond the paper's own contributions. The paper's most novel finding is the documentation of how retracted community-adoption claims directly swayed peer review at a top venue—this provides empirical evidence of a structural failure point in the review process that extends beyond this single case. The other findings are specific to the min-p paper.

## Suggestions

1. Strengthen the LLM-as-a-Judge section by either running controlled re-analyses or explicitly downgrading conclusions from this section.
2. Justify the "lightly edited" HP values or use the original values exactly.
3. Report inter-rater reliability for the qualitative annotation (Section 2.3).
4. Add a discussion of statistical power for the human evaluation t-tests.
5. Clarify the Best-of-N subsampling procedure (with/without replacement) for reproducibility.

---

### Calibration Anchors

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| PdaPky8MUn (Never Train from Scratch) | 8.00 | R1 | Re-analysis + strong positive contribution; our paper lacks comparable positive contribution |
| m2NVG4Htxs (To the Cutoff...and Beyond?) | 6.75 | R2 | Closest match: critique/re-analysis of LLM evaluation; our paper has more specific findings but a weaker section and less novel methodology |
| g16vmAtJ8x (Inadequacy of Similarity-based Privacy) | 6.00 | R2 | Critique of industry metrics; split scores (8,8,6,3,5); our paper is more consistently strong |
| P5UETqZXqT (Model Collapse in Diffusion) | 5.75 | R1 | Analysis + proposed method; unclear connection between analysis and solution |
| qpz84ykqgv (EarthquakeNPP) | 5.25 | R1 | Benchmark + re-analysis; less focused than our paper |
| GbEmJmnQCz (Is Memorization Actually Necessary?) | 4.40 | R1 | Re-analysis paper with unclear methods and overly strong claims; our paper is more rigorous |

**Round 1 Bracket:** 5.5 – 7.0. The paper clearly exceeds the 4–5 range (more thorough than "Is Memorization" or "EarthquakeNPP") but falls short of the 8.0 level ("Never Train from Scratch") because it lacks a strong positive contribution and has a weaker LLM-as-a-Judge section. The closest comparable accepted paper is "To the Cutoff" (6.75). Our paper is slightly below that due to its weaker fourth section and non-novel lessons.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>