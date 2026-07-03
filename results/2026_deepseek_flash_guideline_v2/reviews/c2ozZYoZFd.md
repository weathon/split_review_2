Now I have sufficient verification. Let me produce the final consolidated review.

## Summary

This paper is a detailed case study re-examining the four lines of evidence in Nguyen et al. (2024)'s ICLR 2025 Oral paper on "min-p" sampling for LLMs: human evaluations, NLP benchmarks, LLM-as-a-Judge evaluations, and community adoption claims. Through careful re-analysis and extensive new experiments (~6000 A100-hours across 9 models), the paper demonstrates that the original evidence does not support min-p's claimed superiority. It also contributes a generalizable methodological innovation—Best-of-N hyperparameter control—and derives concrete lessons for rigorous ML research.

## Strengths

1. **Best-of-N hyperparameter control methodology (Section 3.1, Figures 4–5):** The paper develops a principled procedure—subsampling equal numbers of hyperparameters per sampler and computing expected maximum score across 150 repetitions—to fairly compare methods that receive unequal amounts of hyperparameter tuning. This is a genuine methodological contribution applicable beyond this case study. The sweep is large-scale: 9 models × 2 stages × 4 samplers × 31 temperatures × 6 hyperparameters per sampler.

2. **Discovery and documentation of omitted human evaluation data (Section 2.1):** The paper identifies that scores for a baseline sampler ("basic") comprising 1/3 of total collected human evaluation data were excluded from the original paper's methodology, analysis, and results without justification. This finding was confirmed with the original authors, and the data were added to the camera-ready version—though conclusions were not updated.

3. **Intersection-Union Test framework (Section 2.2, Table 1):** The paper correctly identifies that when a paper claims "consistent" superiority across all settings, the appropriate null hypothesis is that the method fails in at least one setting. Applying an IUT to the original data (largest p-value = 0.378) cleanly shows the claim is unsupported. This is more principled than the original paper's pooled t-test.

4. **Detection of asymmetric/selective reporting in LLM-as-a-Judge evaluations (Section 4.3):** The paper documents that for the original Table 3(b), the higher of two available scores was reported for min-p (52.01 vs. 50.14) but the lower of two scores for top-p (50.07 vs. 50.43), citing specific hyperparameter configurations from data shared by the first author.

5. **Verification of retracted community adoption claims (Section 5):** The paper confirms that the original claims of 54k GitHub repositories and 1.1M GitHub stars were unsubstantiated and retracted—and that 3 of 4 reviewers and the AC cited these numbers as justification for strong endorsement.

## Weaknesses

### Major
None.

### Minor

1. **Framing overreach in the abstract.** The abstract claims the original paper's conclusions are "invalidated by its own data" (line 9). This is accurate for the human evaluation analysis (Section 2), which re-analyzes the original data. However, it is imprecise for the NLP benchmark analysis (Section 3), which relies on extensive new experiments (~6000 A100-hours) and a novel Best-of-N methodology, and for the LLM-as-a-Judge analysis (Section 4), which partly relies on externally posted data. The re-analysis is methodologically sound, but the framing invites an unnecessary counter-argument. The paper's body is more careful than its framing.

2. **The universal negative claim ("improves neither quality nor diversity") slightly exceeds what is demonstrated.** The abstract states min-p "improves neither quality, nor diversity, nor the trade-off between quality and diversity" (line 25). The body is more measured (line 208: "do not support min-p's claimed superiority"; line 210: "Conclusions here are based on that evidence. We emphasize that new evidence might lead to different conclusions"). The evidence convincingly shows the original paper's claims are unsupported and that min-p does not consistently outperform in the settings tested, but a universal negative claim is not strictly established by the evidence presented.

3. **Evidence for the selective reporting claim (Section 4.3) rests partly on a Telegram link.** The paper alleges that the higher of two scores was reported for min-p and the lower for top-p. The data source is cited as a "Telegram link" shared by the first author. For a claim of this gravity, a directly citable and publicly archived source would be more appropriate. (Note: the LLM-as-a-Judge data visualizations in Section 4.2 do cite a public GitHub repository—this weakness applies specifically to the selective reporting claim in 4.3.)

4. **NLP benchmark analysis covers only GSM8K, not GPQA.** The paper acknowledges this due to compute budget (line 150), and the original paper evaluated both GSM8K and GPQA. The GPQA results from the original paper are critiqued in passing (line 121) but are not independently re-analyzed with the same controlled methodology. This is acknowledged transparently but does leave one of the original claims less directly addressed.

### Trivial
None.

## Nice-to-Haves

- The finding that min-p produced higher scores for 2 of 12 models in the corrected prompt formatting run (line 165) could be explored further—what distinguishes those models where min-p seems to help?
- The Bonferroni correction for 12 comparisons could be supplemented with a less conservative correction (e.g., Benjamini-Hochberg) to show robustness; the IUT already makes the main point.
- The paper's focus on the "high diversity" human evaluation setting is justified with three concrete reasons (line 64), but a brief acknowledgment that this leaves one experimental condition from the original paper not independently re-analyzed would improve transparency.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"No discussion of practical usefulness"**: The paper is a methodological critique and re-analysis, not a practical deployment guide. Outside stated scope.
- **"The list of scandals is excessive"**: Subjective presentation preference, not a substantive weakness.
- **"The number of submissions is skyrocketing is not a crisis"**: Not a weakness of the paper's methodology or claims.
- **"Reproducibility concerns (undisclosed hyperparameters, missing appendix)"**: Per instructions, parser-stripped content and trivial implementation details are not valid criticisms.
- **"Formatting/style/typo nitpicks"**: Per instructions, parser artifacts are not author errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Recalibrate the abstract's framing.** Replace "invalidated by its own data" (which is accurate only for the human evaluations section) with a more precise two-part framing: (a) the original paper's own data do not support its human evaluation claims, and (b) when fairly controlled, the benchmark and LLM-as-a-Judge evidence does not support min-p's superiority. This eliminates a vulnerability without weakening the core message.

2. **Replace the Telegram link citation (Section 4.3)** with a direct citation to a publicly archived snapshot of the data (e.g., a GitHub release or archived repository page). If such an archive already exists, cite it; if not, create one.

3. **Add a brief discussion of the 2/12 models** where min-p showed higher scores in the corrected prompt formatting experiment. Even a short paragraph speculating about what distinguishes those models would improve the paper's nuance.

4. **Explicitly scope the GPQA gap** by adding a sentence acknowledging that the original paper's GPQA results are critiqued but not independently re-analyzed with the same controlled methodology.

## Score and Decision

**Calibration note:** The calibration retrieval tool was unavailable due to an indexing error, preventing anchor-based comparison. The score below is based on direct evaluation of the paper's content against the ICLR scoring rubric.

This is a strong, well-executed re-analysis paper. It identifies genuine, serious flaws in a high-profile publication, supports its claims with extensive evidence (including ~6000 A100-hours of new experiments), introduces a useful methodological innovation (Best-of-N hyperparameter control), and extracts generalizable lessons. The weaknesses are primarily framing/calibration issues that are fixable without changing the core contributions. There are no fatal methodological flaws.

The paper is stronger than a mere "borderline accept" (6)—it has real methodological novelty and large-scale experimental support—but falls short of a clean "accept" (8) due to the framing overreach and thin evidence for the selective reporting claim. 7.5 captures "a solid paper with clear contributions and fixable issues."

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>