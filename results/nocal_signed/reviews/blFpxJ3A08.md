## Summary

LPFQA is a benchmark of 505 questions derived from professional technical forums across 20 academic/industrial fields, designed to evaluate LLMs on long-tail professional knowledge in authentic contexts. The paper describes a three-phase construction pipeline (data collection, automated MLLM-based question generation with quality control, expert verification and difficulty calibration), and reports scores for 12 mainstream LLMs along with ablation studies testing code-interpreter and search-tool integration.

## Strengths

- **Well-scoped motivation (Section 1).** The paper correctly identifies a real gap: existing benchmarks either test broad but shallow knowledge (MMLU), crowd-sourced conversational ability (Arena-Hard), or extreme difficulty with low practical relevance (HLE). There is genuine space for a benchmark targeting long-tail professional knowledge from authentic practitioner contexts.

- **Principled data sourcing strategy (Section 3.2).** Using professional technical forums as raw material, with a pipeline of crawling, filtering by metadata (date, replies, votes), and screenshot capture for multi-modal content, is a sensible approach to obtaining naturally-occurring, non-synthetic questions.

- **Broad domain coverage (Section 3.3, Figure 2).** The 20 fields span natural sciences, engineering, law, medicine, finance, etc. — broader than most existing specialized benchmarks, with fields like Aerospace, Energy, and Law going beyond typical STEM offerings.

- **Ablation studies go beyond the standard template (Section 4.2.2).** Testing the effect of code interpreter integration and search-tool augmentation represents genuine extra effort to characterize what the benchmark measures, even though the conclusions drawn from these experiments are problematic (see Weaknesses).

## Weaknesses

### Fatal
None. The core benchmark idea has merit; the issues below are severe but individually addressable through revision.

### Major

- **The evaluation metric "Score" is never defined.** Tables 1–4 report "Score" values (e.g., 47.28, 32.40) but the paper never states what these numbers represent — percentages? raw correct counts? weighted averages? For short-answer questions (which use "key knowledge points" as a rubric), there is no specification of how responses are graded (automated exact match? LLM-as-judge? human grading?) or how per-question judgments are aggregated. A benchmark paper that does not define its evaluation metric has an opaque central methodological specification, making results uninterpretable and irreproducible.

- **The main results section (Section 4.1) contains a clear factual error contradicted by the paper's own data.** Line 265 states: "DeepSeek-V3 demonstrates the most balanced and consistent performance across disciplines, with no apparent weaknesses, and can thus be regarded as the overall best-performing model." However, Table 1 shows DeepSeek-V3 scoring **32.60** — the second-worst score among 12 models, far below GPT-5 (47.28), Gemini-2.5-Pro (44.42), o3-high (43.03), etc. Even the "no apparent weaknesses" claim is contradicted by the paper's own Min scores analysis (Section 4.1) listing "DeepSeek-V3 in Misc" as a minimum. This error undermines confidence in the entire results section.

- **The four "fine-grained evaluation dimensions" claimed as a key contribution are never operationalized.** The paper touts "knowledge depth, reasoning ability, terminology comprehension, and contextual analysis" in the Abstract and Section 1 as a central innovation, but the experiments report only a single overall Score per model. No results are broken down by these dimensions, no rubric is provided for assigning questions to dimensions, and no evidence is presented that the benchmark actually measures these distinct capabilities. A claimed contribution with zero supporting evidence weakens the paper.

- **The ablation study conclusions do not follow from the evidence.**
  - **Code Interpreter experiment (Table 3):** Adding a Jupyter Code Interpreter causes a small average drop (39.08 → 36.15) and the paper concludes "LPFQA primarily reflects a model's mastery of domain knowledge rather than its reasoning ability." This is a non-sequitur — a code interpreter is a computational tool, not a general reasoning amplifier, and performance could degrade for many reasons (prompt integration issues, context handling) unrelated to the knowledge-vs-reasoning distinction.
  - **Search tool experiment (Table 4):** The conclusion that "simply augmenting models with online search does not provide a positive effect and may even be detrimental" is far broader than the evidence supports — only one specific tool configuration on one benchmark was tested.

- **No validation against existing benchmarks.** For a new benchmark paper, demonstrating what LPFQA captures that existing benchmarks do not is essential. The paper provides no correlation analysis between LPFQA scores and results on MMLU, GPQA, HLE, or Arena-Hard, leaving the claim that LPFQA "fills a gap" asserted but untested.

- **Post-hoc test-set-trimming raises concerns about discriminative power.** The raw LPFQA (Table 1) shows all models scoring below 50% (32.40–47.28), paralleling the paper's own critique of HLE: "extreme difficulty [that] may lead to poor performance from most models, thus limiting its utility as a regular evaluation tool" (Section 2.2). The paper then removes 69 questions that no model could answer and 15 that all models could answer (Section 4.2.1) — a procedure that trims the test set based on the test results themselves. This is data-dependent calibration on the evaluation set, and the resulting LPFQA⁻ scores only reach 54.43% (GPT-5).

- **Severe dataset imbalance undermines field-level comparisons.** Several fields have very small question counts: Data Science (3), AI (8), Aerospace (8), Energy (9), ICE (7), EIE (10), EIS (10). With 3 questions in Data Science, a single correct/incorrect answer shifts the accuracy by 33 percentage points. The paper reports field-level radar charts and disciplinary conclusions (Section 4.1) without confidence intervals, variance estimates, or any discussion of the enormous uncertainty in these per-field measurements.

### Minor

- The paper says "502 tasks" in the Abstract but "505 questions" throughout the body — a minor inconsistency.

- The example questions shown (Figure 1) raise concerns. The first is a meta-question about a forum post rather than a direct professional question, adding unnecessary framing complexity. The second includes a scoring rubric ("Just agree with the semantics expressed in the reference answer") that is not operationalizable for automated evaluation.

- The extent and rigor of expert verification are not quantified: how many experts, what was their inter-annotator agreement, what proportion of auto-generated questions were rejected or corrected?

### Trivial

- Figure 2's y-axis is labeled "Quality of items" but the text and context indicate it shows the count of items per field — a labeling mismatch.

## Nice-to-Haves

- Perform a decontamination analysis against known LLM training corpora, since questions are derived from public internet forums.
- Report results broken down by multiple-choice vs. short-answer format to explore whether they probe different capabilities.
- Include confidence intervals or statistical significance tests, especially for per-field comparisons with small sample sizes.
- Quantify the expert verification process (number of experts, agreement rate, rejection rate).

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **Criticism about MMLU-Pro and later variants** — This references a benchmark variant not cited in the paper. Per guidelines, missing-related-work criticisms are not included.
2. **Concerns about forum/cited-resource availability** — All cited references are assumed to exist per guidelines.
3. **Formatting nitpicks and minor writing style complaints** — These are parser artifacts or paper presentation issues outside the review's scope.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the gap between claimed evaluation dimensions and their operationalization, and the tension between the paper's critique of HLE's difficulty and LPFQA's own uniformly low scores. Neither constitutes an unexpected insight about the dataset or the evaluation landscape.

## Suggestions

1. **Define the Score metric explicitly.** State whether it is percentage accuracy, how short-answer responses are judged (exact match, LLM-as-judge, human), and how per-question results are aggregated.
2. **Correct the DeepSeek-V3 error in Section 4.1.** The claim that a model scoring 32.60 (second-worst) is the "overall best-performing" must be fixed.
3. **Either operationalize the four evaluation dimensions with reported per-dimension results, or remove this claimed contribution from the innovation list.**
4. **Reframe the ablation study conclusions** to match what the experiments actually support (e.g., "adding a code interpreter did not improve performance on LPFQA") rather than making unsupported inferences about knowledge vs. reasoning.
5. **Add a comparison/validation analysis** showing how LPFQA rankings correlate with or diverge from existing benchmarks (MMLU, GPQA, HLE, Arena-Hard).
6. **Acknowledge and discuss the dataset imbalance** and its implications for per-field reliability, or consider consolidating very small fields.

## Score and Decision

The paper addresses a genuine need and the data-sourcing pipeline is well-motivated, but the execution has critical weaknesses that prevent acceptance in its current form. The undefined evaluation metric, a clear factual error in the results section, unoperationalized claimed contributions, unsupported conclusions from ablation studies, and lack of any validation against existing benchmarks collectively represent too many gaps for a rebuttal to resolve. The benchmark idea has merit and could form the basis of a strong paper with substantial revision, but the present manuscript is not yet publication-ready.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>