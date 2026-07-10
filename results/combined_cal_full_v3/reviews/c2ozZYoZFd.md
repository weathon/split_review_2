## Summary

This paper is a detailed forensic case study of "Turning Up the Heat: Min-P Sampling for Creative and Coherent LLM Outputs" (Nguyen et al., 2024), a high-profile ICLR 2025 Oral paper. The authors re-examine all four lines of evidence from the original paper—human evaluations, NLP benchmarks, LLM-as-a-Judge evaluations, and community adoption claims—and conclude that none support the claimed superiority of min-p sampling. The paper also derives general methodological lessons for the field, including a novel Best-of-N hyperparameter analysis for fair comparison across methods with different tuning budgets.

## Strengths

- **Concrete, documented data omission (Sec. 2.1).** The discovery that one-third of human evaluation data (the basic sampling condition) was excluded from the original paper's analysis without mention is a clear, verifiable flaw, confirmed with the original authors. After being raised, the data was added to the camera-ready but without updating methodology or conclusions.

- **Careful statistical re-analysis (Sec. 2.2, Table 1).** The paper correctly re-runs the original paper's statistical tests, showing only 5/12 comparisons reach significance at α=0.05 without correction and only 1/12 with Bonferroni correction. The use of the Intersection-Union Test (IUT) as the formally correct test for a "consistently outperforms" claim is a strong methodological contribution.

- **Best-of-N hyperparameter analysis (Sec. 3.1, Figs. 4-5).** A genuinely novel and transferable methodological tool for controlling for the number of hyperparameters swept when comparing methods. This is the paper's most significant methodological contribution and addresses a real, underappreciated problem in empirical ML.

- **Selective reporting documentation (Sec. 4.3).** The finding that the original paper reported the higher of two win rates for min-p but the lower of two for top-p is a specific, damning instance of selective reporting that is hard to explain as accidental.

- **Transparency of the re-analysis process.** The authors made their annotations, code, and analyses publicly available, engaged with the original authors, and documented what was confirmed vs. disputed.

## Weaknesses

### Major
None. The core re-analysis findings (data omission, statistical errors, selective reporting) are well-supported and the paper's central thesis is not threatened by any verified weakness.

### Minor

- **The hyperparameter sweep is limited to a single benchmark (GSM8K CoT), constraining the generality of the conclusion that "samplers perform approximately equally if given equal hyperparameter tuning" (Sec. 6, line 208).** The paper conducts an extensive sweep (9 models, 31 temperatures, ~6000 A100-hours) but only on math reasoning. Sampling methods are often motivated by text generation quality where diversity-coherence tradeoffs matter most. The paper acknowledges compute constraints and notes that "new evidence might lead to different conclusions" (line 210), but the stated conclusion still extends beyond the GSM8K-only evidence base.

- **The claim about reviewer motivations is unsourced (Sec. 5, line 204).** The paper states that "3 of 4 ICLR 2025 reviewers and the Area Chair identified these retracted community adoption numbers as the main justification for their strong endorsement" without providing a citation or source. This claim is not central to the paper's scientific contribution but should be sourced or removed.

- **The LLM-as-a-Judge evidence partly relies on informally sourced data (Sec. 4).** Some findings depend on data from a "public GitHub repository," a "Telegram link" shared by the first author, and "ongoing work to publish" (lines 183, 189, 193). While informative and corroborative, the provenance is not independently reproducible from static, archived sources.

- **The new human evaluation study (Sec. 2.4) changed many variables simultaneously** (sampler implementation, participant pool, hyperparameters, reading time, text length, rubric), making it impossible to attribute the lack of min-p advantage to any specific factor. The paper uses this as supporting evidence but does not explicitly discuss how these confounds limit causal attribution.

### Trivial
None.

## Nice-to-Haves

- Archive the LLM-as-a-Judge Telegram link and GitHub data in a static, citable form.
- If feasible, extend the hyperparameter sweep to a task where output diversity matters more (e.g., creative generation), to broaden the evidence base for the "samplers perform approximately equally" conclusion.

## Removed Points

- "The list of citations documenting crises in ML research feels like name-dropping rather than a synthesized argument" — removed as a presentation/style nitpick.
- "Bonferroni correction assumes tests are independent" — the critic explicitly acknowledges this works in the paper's favor and the evidence is robust regardless; not a weakness.
- Criticisms about missing appendix content, reproducibility of trivial implementation details, or questioning the existence of cited models/repositories — all removed per hard rules (these are parser artifacts or reflect reviewer knowledge gaps).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Source or remove the unsourced claim about reviewer motivations in Sec. 5 ("3 of 4 ICLR 2025 reviewers and the Area Chair identified these retracted community adoption numbers as the main justification for their strong endorsement").
2. Add a sentence in Sec. 2.4 acknowledging that the simultaneous methodological changes in the new human evaluation limit causal attribution.
3. Calibrate the scope of the "samplers perform approximately equally" conclusion (Sec. 6) to match the GSM8K-only evidence, or reframe it as a tentative finding.
4. Archive the LLM-as-a-Judge evidence in a static, citable form.

## Score and Decision

**Calibration anchors considered across rounds:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| GbEmJmnQCz.md (Is Memorization Actually Necessary?) | 4.40 | R1 | Yes | Similar re-analysis paper but weaker: its own methodological issues and lack of definitive contribution led to rejection. Current paper is stronger. |
| lf8QQ2KMgv.md (Is Memorization Actually Necessary?) | 3.75 | R1 | Yes | Same paper, similar issues. Current paper's core findings are more airtight. |
| fXJCqdUSVG.md (Evaluating Durability of Safeguards) | 6.50 | R1 | Yes | Comparable critical case study; accepted. Similar type and quality. |
| 7W3GLNImfS.md (Human Feedback is not Gold Standard) | 6.50 | R2 | Yes | Comparable critical analysis with empirical evidence; accepted. Similar rigor and scope of limitations. |
| E8gYIrbP00.md (Beyond Correlation) | 6.75 | R2 | Yes | Comparable methodology critique; accepted. Similar structure and contribution type. |
| PdaPky8MUn.md (Never Train from Scratch) | 8.00 | R1 | Yes | Stronger constructive contribution (proposed solution, not just critique); current paper not at this level. |
| jOmk0uS1hl.md (Training on the Test Task) | 8.00 | R1 | Yes | Stronger contribution with proposed corrective method and broader implications. |

**Round-1 bracket:** 5.5 – 7.5. The paper is clearly above the 3.75–4.40 re-analysis papers (which were rejected due to their own methodological weaknesses) and below the 8.00 papers (which had strong constructive contributions).

**Narrowing:** Comparing favorability ratings against the 6.50-level anchors (which share similar structure and contribution type), this paper's strengths (6.96–9.04) and weaknesses (2.35–3.64) pattern consistently with accepted papers in this range. The weaknesses are real but bounded—none threaten the core findings. The paper is not at the 8.00 level because those papers offered explicit solutions (e.g., fine-tuning on task data as a fix) rather than just critique, and had broader empirical scope.

**Final score: 6.5.** This is a strong meta-scientific paper whose core contribution—demonstrating that a high-profile ICLR Oral paper's evidence does not support its claims—is well-supported and convincingly argued. The weaknesses are scope limitations and presentation issues, not flaws in the core re-analysis.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>