## Summary

This paper presents a detailed re-analysis of an ICLR 2025 Oral paper on "min-p" sampling. It examines four lines of evidence from the original paper (human evaluations, NLP benchmarks, LLM-as-a-Judge evaluations, and community adoption claims) and finds each unsupported by the underlying data. It also introduces a "Best-of-N" methodology for fairly comparing methods with different hyperparameter tuning volumes and draws general lessons for rigorous empirical ML research.

## Strengths

1. **The omitted-data finding (Section 2.1) is concrete and verifiable.** The original paper excluded one-third of its human evaluation scores (the "basic" sampling condition) without acknowledgment. The omission was confirmed by the original authors, and the paper shows that including this data changes the conclusions. This single finding undermines the original paper's primary line of evidence.

2. **The "Best-of-N" hyperparameter-volume-control analysis (Section 3.1, Figures 4–5) is a genuinely useful methodological contribution.** The procedure—subsampling equal numbers of hyperparameter combinations per sampler, computing max performance, and repeating—provides a principled way to detect whether a method's reported advantage is an artifact of more extensive tuning. It is simple, interpretable, and demonstrated at scale (~6000 A100-hours across 9 models).

3. **The selective reporting in the LLM-as-a-Judge results (Section 4.3) is well-documented.** The paper shows that the original authors reported the higher of two win rates for min-p (p=0.05 → 52.01%) but the lower of two for top-p (p=0.9 → 50.07%, where p=0.98 yields 50.43%). This asymmetry is difficult to explain as an innocent oversight.

4. **The paper engages transparently with the original authors**, noting when errors were confirmed, when corrections were made, and when formatting issues in the re-analysis were pointed out. This gives the re-analysis credibility and models the kind of scientific dialogue it advocates.

## Weaknesses

### Fatal
None.

### Major

1. **The NLP benchmark re-analysis covers only GSM8K (one of the two benchmarks the original paper evaluated).** Line 150 states: "Due to our compute budget, we only evaluated GSM8K CoT." Yet the abstract and Section 3 claim that "min-p's claimed superiority vanishes when controlling for the volume of hyperparameter tuning"—asserted as a general claim but supported by evidence from a single mathematical reasoning benchmark. The original paper also evaluated GPQA (5-shot). The conclusion may well be correct, but the gap between claim strength and evidence breadth is substantial. For a paper whose central subject is scientific rigor and avoiding overclaiming, this is a meaningful tension.

### Minor

2. **The LLM-as-a-Judge section (Section 4) identifies genuine methodological flaws but does not provide an alternative re-analysis of comparable rigor.** The analysis in Section 4.2 is based on visualizing data from a public GitHub repository of ongoing work rather than a controlled experiment with proper statistical analysis. The paper would be stronger if it either (a) re-ran the experiment with proper controls and direct comparisons, or (b) explicitly framed this section as a methodological critique rather than as direct evidence against min-p's empirical performance.

3. **The limitations section (lines 209–211) is only three sentences long and does not grapple with specific limitations** such as the single-benchmark NLP analysis or the lack of a re-run LLM-as-a-Judge experiment. For a paper whose subject is scientific rigor, this lack of self-reflection is a notable gap.

4. **The hyperparameter values for each sampler were "lightly edited to make them more evenly distributed" (line 133),** but the paper does not discuss whether these edited ranges are equally well-suited to each method or run a sensitivity analysis. This introduces a potential confounder in the otherwise strong Best-of-N analysis.

5. **The statistical analysis applies Bonferroni correction for 12 positively correlated tests without discussing alternatives** (e.g., Holm-Bonferroni, Benjamini-Hochberg) that would be less conservative for correlated tests. The paper also provides uncorrected results, implicitly acknowledging the issue, but does not address it explicitly. This is a gap in statistical thoroughness for a paper whose central credential is statistical thoroughness—though it does not invalidate the analysis.

### Trivial

6. The introduction (lines 13–14) cites 20+ references in a single sentence enumerating "scandals," mixing blog posts, preprints, and verified cases. A more measured selection of a few well-established cases would be more effective.

7. The paper mentions one possibly-incorrectly-reported value in the new human evaluation (line 117: 7.80 vs. 5.80) in passing, without the same rigor of analysis applied to the original data.

## Nice-to-Haves

- Extend the Best-of-N analysis to GPQA to broaden the NLP evidence base.
- Clarify the relationship between Best-of-N and standard bootstrap confidence intervals, and justify the choice of 150 replicates.
- Consider discussing alternative multiple-comparison corrections (Holm-Bonferroni, Benjamini-Hochberg) for the human evaluation analysis.

## Removed Points

- *"The community adoption retraction's weight in the paper's overall argument is exaggerated"* — The paper itself documents that 3 of 4 reviewers and the AC cited these numbers as justification for endorsement. This is a relevant finding about the review process, not a weakness of the paper's own argument; including it within the case study is appropriate.
- *"The paper does not discuss whether practitioners have found min-p useful despite lack of rigorous validation"* — Scope creep. The paper's stated aim is to evaluate the original paper's evidence, not to survey practitioner sentiment.
- *"The paper does not provide a quantitative meta-analysis combining evidence"* — This demands a methodological standard not typical for re-analysis papers and would be a nice-to-have, not a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Restrict the NLP benchmark conclusion** to GSM8K (or the benchmarks actually tested) rather than asserting universal refutation of min-p's NLP performance.
2. **Either re-run the LLM-as-a-Judge experiment** with proper controls and direct comparisons, or **reframe the section** explicitly as a methodological critique rather than as direct evidence.
3. **Expand the limitations section** to address the single-benchmark limitation and the lack of a re-run LLM-as-a-Judge analysis.
4. **Discuss the fairness of the hyperparameter ranges** used in the Best-of-N analysis and consider running sensitivity checks.
5. **Address the multiple-comparison correction choice** (Bonferroni vs. alternatives) in the human evaluation analysis.

---

**Calibration details.** I retrieved and inspected reviews for 6 anchor papers across score bands. The most structurally similar anchors were: "Is Memorization Actually Necessary for Generalization?" (avg 3.75–4.40, re-analysis of prior work, rejected for limited generalizability and no novel method), "On Evaluating the Durability of Safeguards for Open-Weight LLMs" (avg 6.50, case-study critique with lessons), and "What does the Knowledge Neuron Thesis Have to do with Knowledge?" (avg 7.33, reassessment paper). The current paper has stronger evidence than the memorization papers (verified omitted-data error, novel Best-of-N method) but narrower evidence coverage than the higher-scored anchors (GSM8K-only NLP analysis, no re-run LLM-as-a-Judge). Round 1 bracket: 5.5–6.5. Final score: 6.0.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>