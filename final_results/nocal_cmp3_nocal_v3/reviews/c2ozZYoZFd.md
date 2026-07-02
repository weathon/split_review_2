Now let me produce the final consolidated review.

## Summary

This paper presents a detailed case study re-examining a high-profile ICLR 2025 Oral paper on min-p sampling (Nguyen et al., 2024). Through re-analysis of all four lines of evidence from the original paper — human evaluations, NLP benchmark evaluations, LLM-as-a-Judge evaluations, and community adoption metrics — the paper demonstrates that the original claims of min-p's superiority are not supported by the data. The paper also contributes a methodological tool (Best-of-N subsampling for fair hyperparameter comparison) and derives six general lessons for rigorous empirical ML research.

## Strengths

- **Large-scale hyperparameter-controlled benchmark analysis (Section 3).** The ~6,000 A100-hour sweep across 9 models × 2 stages × 4 samplers × 31 temperatures × 6 hyperparameters × 3 seeds is a substantial empirical contribution. The Best-of-N subsampling methodology for equalizing hyperparameter tuning volume is a genuinely useful tool that addresses a known failure mode (cherry-picking via unequal tuning), and the paper demonstrates rather than merely advocates for it.

- **Statistical re-analysis of human evaluations (Section 2) is crisp and consequential.** The paper documents that one-third of human evaluation data was omitted, shows that the original claim of "consistent" superiority collapses under proper multiple-comparison correction (Bonferroni: 1 of 12 comparisons significant at α=0.05, 0 of 12 at α=0.01), and introduces an Intersection-Union Test that formalizes why "consistent" outperformance was never supported. This combination of data discovery and correct statistical framing is the paper's sharpest analytical contribution.

- **Documentation of the selective reporting issue in the LLM-as-a-Judge results (Section 4.3).** The claim that the higher of two scores was reported for min-p but the lower for top-p — with specific win rates provided (52.01 vs. 50.14 for min-p, 50.07 vs. 50.43 for top-p) — is a concrete instance of a systemic problem that, if accurate, substantially undermines the credibility of that line of evidence.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

- **Qualitative annotation methodology is under-described (Section 2.3).** The paper states that the authors "manually annotated" the qualitative responses and "publicly posted" the annotations, but provides no description of the annotation procedure: how many annotators, whether annotations were conducted independently, or whether inter-rater reliability was assessed. The claim that "more human evaluators explicitly preferred basic sampling than preferred min-p" depends on the reliability of these annotations. In a paper that critiques another's human evaluation methodology, this gap is conspicuous. The conclusion may well be correct, but the current manuscript does not provide sufficient detail to fully trust the annotation process.

- **The "3 of 4 ICLR 2025 reviewers" claim is unsupported (Section 5).** The paper states that "3 of 4 ICLR 2025 reviewers and the Area Chair identified these retracted community adoption numbers as the main justification for their strong endorsement" without providing a citation or source for this assertion. If this information is verifiable (e.g., from the published reviews), it should be cited; otherwise, it is an unsubstantiated claim about the original review process.

- **Uncertainty quantification is missing from the hyperparameter sweep results (Section 3).** The paper's large-scale benchmark evaluation concludes that min-p "does not outperform" other samplers, but reports results entirely through point estimates averaged over seeds and subsampling iterations. The 150 subsampling iterations naturally produce a distribution from which confidence intervals could be computed, but none are reported. Since "does not outperform" is a claim about absence of difference, some characterization of uncertainty (e.g., confidence intervals on the difference scores in Figure 5, or a statement about minimum detectable effect size) would substantially strengthen this conclusion.

- **The hyperparameter ranges across samplers may not be equally informative (Section 3.1).** Min-p's p ∈ {0.01, 0.02, 0.05, 0.1, 0.2, 0.3} and top-p's p ∈ {0.99, 0.98, 0.95, 0.9, 0.8, 0.7} span different scales, and these ranges may not correspond to equally informative exploration of the sampling behavior space. The Best-of-N subsampling handles the count disparity statistically, but the initial grid choice constrains what the sweep can discover. The paper notes values were "lightly edited to make them more evenly distributed" but does not discuss whether the ranges are equally informative. This is a limitation worth acknowledging explicitly.

- **The selective reporting claim (Section 4.3) relies on an external reference.** While the paper does provide the specific numerical values from the Telegram link (52.01 vs. 50.14 for min-p, 50.07 vs. 50.43 for top-p), the evidence for this serious allegation would be strengthened by reproducing the data in a self-contained table or screenshot rather than referencing an external communication channel.

### Trivial

None.

## Nice-to-Haves

- Reproduce the Telegram-based evidence from Section 4.3 in a self-contained table showing the full set of win rates for both hyperparameter choices for both min-p and top-p.
- Provide standard errors or bootstrap confidence intervals for the difference scores in Figure 5 to quantify uncertainty around the "does not outperform" conclusion.
- Add a brief numeric breakdown of the omitted human evaluation data (Section 2.1) showing N per sampler × condition.
- Include a note acknowledging that Bonferroni correction is conservative when tests are correlated (a standard caveat, not a flaw).
- Discuss statistical power of the human evaluation study to clarify the range of effect sizes the data can rule out.

## Removed Points

These points are flagged to be removed; treat them with caution:

1. **"Long list of citations is rhetorically overdone"** (from Section-by-Section notes) — REMOVED: pure style nitpick.
2. **"Bonferroni is conservative when tests are correlated"** — REMOVED: not a flaw; the critic explicitly notes it is standard practice.
3. **"Section 2.1 would benefit from numeric breakdown"** — REMOVED: the paper already states "1/3rd of the total collected scores"; this is a minor presentation preference moved to Nice-to-Haves.
4. **"Section 4.1 critique is valid but brief"** — REMOVED: this is an observation, not a weakness of the current paper.
5. **"Star comparison does not by itself prove the claim was false"** — REMOVED: the paper's evidence for falsity is the authors' retraction, which is documented; the star comparison is supporting context, not the primary evidence.
6. **"No discussion of statistical power"** — REMOVED: the critic's own framing acknowledges this would not invalidate the conclusion; moved to Nice-to-Haves.
7. **"Does not address possibility min-p is genuinely better but effects are small"** — REMOVED: the paper's conclusion that min-p "offers no apparent advantage" is a reasonable summary of the evidence presented, and the paper explicitly acknowledges its conclusions may change with new evidence (Section 6 "Key Limitation").

## Novel Insights

None beyond the paper's own contributions. The harsh critic's analysis largely surfaces sensible suggestions for strengthening the paper (direct evidence reproduction, annotation detail, uncertainty quantification) rather than identifying structural flaws or unrecognized contributions.

## Suggestions

- Add a self-contained table in Section 4.3 reproducing the win-rate data from both hyperparameter values for both min-p and top-p, so the selective reporting claim does not depend on an external reference.
- Include standard errors, bootstrap confidence intervals, or variance estimates for the difference scores in Figure 5 to quantify the precision of the "does not outperform" conclusion.
- Document the qualitative annotation protocol (number of annotators, independence, inter-rater reliability) in Section 2.3 or, at minimum, state that annotations were straightforward categorizations of expressed preferences and note that the raw annotations are publicly posted for independent verification.

## Score and Decision

This is a well-executed re-analysis / reproducibility case study. The paper's core claims are strongly supported: the omitted data discovery, corrected statistical analysis, large-scale hyperparameter-controlled sweep, and documentation of retracted community-adoption claims are substantial and generally well-presented. The weaknesses identified are minor — they do not threaten the paper's central contribution but reflect concrete gaps where the paper falls short of the standards it advocates. The contribution stands as-is and would be strengthened by addressing these issues. I recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>