Now I have all the information needed. Let me write the final consolidated review.

## Summary

This paper presents a detailed re-analysis of "Turning Up the Heat: MIN-P Sampling for Creative and Coherent LLM Outputs" (ICLR 2025 Oral), systematically scrutinizing all four lines of evidence in the original paper. Through re-analysis of the original human evaluation data (finding 1/3 of scores were omitted), extensive NLP benchmark sweeps with a novel Best-of-N hyperparameter-control method, investigation of LLM-as-a-Judge evaluations, and verification of community adoption claims, the paper convincingly demonstrates that the original paper's evidence does not support its claims of min-p's superiority. A set of general lessons for rigorous ML research is extracted from the case study.

## Strengths

- **Systematic four-pronged re-examination:** The paper independently scrutinizes all four lines of evidence from the original paper (human evals, NLP benchmarks, LLM-as-a-Judge, community adoption), finding problems in each. This breadth makes the case substantially stronger than a one-off critique.
- **Novel Best-of-N hyperparameter control methodology (Section 3.1):** The approach of subsampling equal numbers of hyperparameter combinations per sampler and tracking max performance as a function of search volume is a genuine methodological contribution that addresses a widespread problem in ML — comparing methods with unequal tuning budgets — and is independently useful beyond this case study. Applied across 9 models, 2 model stages, 4 samplers, 31 temperatures, and 6 hyperparameters per sampler, using ~6000 A100-hours.
- **The omitted-data finding (Section 2.1) is unambiguous and decisive:** Discovering that 1/3 of human evaluation scores were excluded from the original paper's methodology, analysis, and results — with the exclusion acknowledged only after being raised, and the published conclusions never updated — is a concrete, non-interpretive finding that undermines the original claim regardless of any other analysis.
- **Data-level transparency:** The authors publicly posted their annotations of the qualitative responses, re-analysis code, and statistical tests, and transparently report their interactions with the original authors, walking the walk of the paper's own principles.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **The Telegram-based selective reporting claim (Section 4.3) is not independently verifiable from the paper itself.** The paper asserts that "the first author publicly shared a Telegram link" showing that the higher of two scores was reported for min-p and the lower for top-p, but does not provide the Telegram content in an appendix or static archival link. For a paper whose core thesis is about rigor and transparency, relying on an ephemeral communication channel for what is arguably the most serious accusation in that section is an evidentiary weakness. The LLM-as-a-Judge section's other points (methodological underspecification, unequal tuning) remain valid, but this particular claim would benefit from stronger documentation.

- **The "blueprint" framing slightly overpromises relative to what is delivered.** The paper delivers a detailed negative case study plus six sensible but largely textbook-level lessons (e.g., "apply statistical tests correctly," "practice data transparency"). Only the Best-of-N hyperparameter-control method (Section 3.1) is a genuinely novel positive methodology. The remaining lessons are well-motivated by the case study but are not synthesized into a reusable practical methodology beyond what is already standard best practice. This is a framing issue, not a content issue — the paper's core re-analysis stands on its own.

- **The NLP benchmark analysis is limited to GSM8K.** The original paper also evaluated on GPQA (5-shot). The authors acknowledge this resource constraint (Section 6), but it means the rigorous Best-of-N quantitative result is demonstrated on only one of the two original benchmarks, leaving an open question about generalizability. Additionally, the finding that min-p produced higher scores on 2 of 12 models (after the prompt-format correction) is mentioned in passing but not explored.

- **Section 2.4: The 7.80 vs. 5.80 discrepancy claim lacks transparency.** The paper states that a value in the original paper's Table 15 "should be 5.80" but does not show the computation that leads to this number. For a paper making a serious accusation of error, showing the arithmetic would strengthen the point and allow independent verification.

- **Section 5: The claim that the camera-ready replacement statement "remains misleading" is stated without elaboration.** This assertion requires justification to be persuasive.

### Trivial
None.

## Nice-to-Haves

- Consider converting the Best-of-N analysis into a standalone methodological section with a clear recipe (how many hyperparameters to sweep, how to subsample, how to compute confidence intervals), which would strengthen the "blueprint" side of the paper and give it independent reuse value.
- Consider extending the NLP benchmark analysis to GPQA (even at reduced scale) to close the most obvious completeness gap, or acknowledge this limitation more prominently.
- Provide the specific computation for the 7.80/5.80 discrepancy in a simple table or formula so readers can independently verify the claim.
- Elaborate on why the camera-ready community adoption statement "remains misleading."

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

1. **Section 4.1 criticism ("doesn't add independent evidence that min-p fails"):** Removed because it misunderstands the paper's thesis. The paper argues that the original evidence *does not support* the superiority claim, not that it proves min-p fails. Showing that the LLM-as-a-Judge methodology is under-specified and cannot be interpreted is entirely consistent with the paper's thesis.

2. **Criticism that Section 4 is "more suggestive than definitive":** Removed for the same reason — the paper's purpose is critique, not independent proof. The section's identification of unequal tuning and methodological ambiguity directly supports the claim that this evidence is unreliable.

3. **"No discussion of practical utility of min-p":** The paper explicitly says in Section 6: "While min-p is useful as another method to try…"

4. **Non-independence of data points concern:** The paper uses paired t-tests and IUT, which inherently account for the paired structure of the data. This criticism appears to misread the methodology.

5. **Section 2.2 statistical tests note about "both approaches have pros and cons":** This is a description of the paper's methodology, not a weakness. The paper explicitly explains why its approach is more appropriate.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- For the Telegram-based claim in Section 4.3, either archive the communication (e.g., as a static HTML screenshot in the supplementary) or reframe the claim as a concern rather than a definitive finding, to avoid the evidentiary gap.
- Repackage the Best-of-N methodology as a standalone recipe so other researchers can directly apply it — this would substantially raise the paper's positive contribution beyond the case study.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>