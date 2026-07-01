## Summary

This replication case study re-examines a high-profile ICLR 2025 Oral paper that introduced "min-p" sampling for LLMs. The current paper systematically re-analyzes all four lines of evidence from the original work (human evaluations, NLP benchmarks, LLM-as-a-Judge, community adoption) and finds that none support the claimed superiority of min-p. It also contributes a Best-of-N methodology for controlling hyperparameter tuning volume when comparing sampling methods.

## Strengths

1. **Thorough multi-evidence re-analysis.** The paper systematically re-examines four independent lines of evidence from the original publication (human evaluations, NLP benchmarks, LLM-as-a-Judge, community adoption), finding convergent problems across all of them. This breadth strengthens the conclusion substantially — it is not a single-pinprick critique but a comprehensive failure of the original paper's evidence architecture.

2. **Discovery of omitted data (Section 2.1).** Finding that one-third of human evaluation data (basic sampling scores) was excluded from the original analysis without justification, and that including it changes the conclusions, is the single strongest finding. This is concrete, well-documented, and independently verifiable from the original authors' published data.

3. **Best-of-N hyperparameter analysis (Section 3).** The methodology for controlling hyperparameter volume — subsampling equal numbers of hyperparameters and averaging over repeated subsamples — is a genuinely useful methodological contribution that cleanly addresses a subtle but pervasive failure mode in empirical ML: comparing methods that differ in how much tuning they received.

4. **Selective reporting evidence (Section 4.3).** The documentation that Table 3(b) reported the higher of two scores for min-p but the lower of two scores for top-p is specific, verifiable from a public source the original authors shared, and clearly problematic.

5. **Transparency.** The paper uses the original authors' published data and code, confirms findings with the authors, and makes its own annotations publicly available. This is the right way to conduct a replication study.

## Weaknesses

### Fatal
None.

### Major

1. **NLP benchmark re-analysis covers only GSM8K, not GPQA, but the conclusion is framed generally.** The original paper claimed min-p superiority "across benchmarks and temperatures," testing both GSM8K and GPQA (5-shot). This re-analysis, despite requiring ~6000 A100-hours, evaluates only GSM8K CoT (under two prompt formats). GPQA is absent. The paper acknowledges the compute budget constraint (line 150: "Due to our compute budget, we only evaluated GSM8K CoT"), but the abstract claims "min-p's claimed superiority vanishes when controlling for the volume of hyperparameter tuning" — broader than the single-benchmark evidence supports. The original claim about GPQA remains unaddressed. Either GPQA should be included or the conclusion should be explicitly bounded to GSM8K in the abstract and introduction.

2. **The new human evaluation analysis (Section 2.4) lacks the statistical rigor applied to the original study.** The paper meticulously applies Bonferroni correction, IUT tests, and structured hypothesis testing (Table 1) to critique the original study's statistics. However, when analyzing the new human evaluation data (run by the original authors in response to feedback), the conclusion that "min-p does not outperform baseline sampling methods" rests entirely on visual inspection of a scatter plot (Figure 3) and one numerical correction. No equivalent t-tests, multiple comparison corrections, or IUT are applied. This asymmetry matters because the paper's own Lesson 2 emphasizes applying "statistical tests rigorously and transparently." The paper should either apply the same tests to the new data or explain why they are unnecessary.

### Minor

1. **Blueprint lessons beyond the Best-of-N analysis are standard methodological principles.** The paper frames itself as providing "a blueprint for conducting more meticulous science" (abstract) with six general lessons. However, Lessons 2–6 (apply statistics rigorously, demand data transparency, scrutinize qualitative summaries, ensure methodological clarity, watch for selective reporting) are well-established research methodology principles. The paper correctly reserves the "novel methodology" claim for the Best-of-N analysis (Lesson 1, line 27). The other five lessons are valuable as an *exemplar* of how these failures manifest in a real high-profile case, rather than as novel principles. The paper would be stronger if it positioned itself more explicitly as an illustrative case study rather than suggesting it derives novel methodological principles from this exercise.

### Trivial
None.

## Nice-to-Haves

- **Extend the NLP benchmark sweep to GPQA (or a subset).** Even a smaller-scale sweep on GPQA (fewer models or fewer seeds) would address the most significant evidence gap. If compute is truly prohibitive, explicitly bound the conclusion to GSM8K in the abstract and introduction.
- **Apply the same statistical tests (t-tests, Bonferroni, IUT) to the new human evaluation data (Section 2.4)** to make the analysis symmetric and prevent any appearance of double standards.
- **Discuss the implementation change more prominently.** The paper notes that the original authors changed from applying temperature after truncation to before truncation (line 100). This is a nontrivial methodological change — if the implementation changed, the original paper's results may correspond to a different method than the one now being claimed. This substantive point could be highlighted more.

## Removed Points

These points from the input review were removed as they do not constitute substantive weaknesses:

- **Basic sampling clarity in Table 1**: The reviewer suggested separating the critique about top-p alone from the critique about adding basic sampling. The paper handles this adequately — Section 2.1 addresses the omission directly, and Table 1 transparently includes both baselines. Minor presentation preference, not a weakness.
- **Low diversity setting limitation**: The reviewer noted this as a limitation but acknowledged "the paper addresses this" (three justifications are provided on lines 64-65). No retained weakness.
- **Section 4 being weaker evidentially**: The reviewer explicitly stated "This is acceptable for a critique paper." An observation, not a weakness.
- **Comparison of min-p with top-k clarity**: A presentational suggestion about how to structure the Section 3 discussion.

## Novel Insights

The most striking insight from the review process is that the paper's strongest finding — the omitted human evaluation data — is also the simplest: one-third of the collected data was excluded without mention, and including it flips the conclusions. This highlights that foundational data transparency issues can be more consequential than sophisticated methodological errors. The second genuinely novel insight is the Best-of-N analysis itself, which reveals a subtle but pervasive failure mode: when methods differ in the volume of hyperparameter tuning they receive, reported performance differences can be artifacts of unequal search effort rather than genuine method quality. This insight generalizes well beyond the min-p case study to any empirical ML comparison involving hyperparameter tuning.

## Suggestions

1. Explicitly bound the NLP benchmark conclusion to GSM8K in the abstract, or extend the sweep to include GPQA.
2. Apply the same structured hypothesis testing (t-tests with multiple comparison correction) to the new human evaluation data in Section 2.4.
3. Reframe the "blueprint" discussion to more clearly distinguish the genuinely novel Best-of-N contribution from the standard methodological principles illustrated by the case study.

## Score and Decision

Based on the paper's strengths — thorough multi-evidence re-analysis, the important discovery of omitted data, the novel Best-of-N methodology, and clean documentation of selective reporting — versus the bounded weaknesses (partial benchmark coverage, asymmetric statistical rigor, and overstated blueprint framing), the paper makes a compelling case that the original paper's evidence does not support its claims. The weaknesses constrain but do not invalidate the core findings.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>