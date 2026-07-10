## Summary

EditBench introduces a benchmark for evaluating LLMs on instructed code editing, grounded in real-world data collected via an instrumented VSCode extension from ~500 programmers. It comprises 109 unique problems translated across 5 natural languages (540 total problems), spans 2 programming languages, and evaluates 40 models. The paper's core contributions are: (1) sourcing problems from genuine developer-IDE interactions rather than annotator-written or educational data, (2) multilingual scope with native-speaker-validated translations, (3) context-dependent problems requiring highlighted code and cursor position understanding, and (4) a comprehensive 40-model evaluation revealing that only one model exceeds 60% pass@1.

## Strengths

- **Real-world data collection is a genuine advance over prior edit benchmarks.** The paper collects data from ~500 programmers performing real coding tasks in their own IDEs via an open-source VSCode extension. Table 2 convincingly demonstrates that EditBench instructions are messier and more ambiguous (e.g., "do not use R style, use python style") than the templated prompts in CanItEdit and EditEval. This directly addresses a known weakness of prior edit benchmarks that rely on annotator-written or educational-style problems.

- **Multilingual scope is a clear differentiator.** EditBench includes 5 natural languages (English, Russian, Chinese, Polish, Spanish) with native-speaker validation of translations. All prior edit benchmarks are English-only. This enables cross-language performance analyses that no existing edit benchmark supports.

- **Comprehensive and well-executed model evaluation.** Evaluating 40 models across 11 families (GPT, Qwen, Llama, Mistral, Sonnet, Gemma, Grok, DeepSeek, Gemini, Kimi, GLM) with consistent pass@1 methodology provides a solid baseline for the community. The inclusion of both reasoning and non-reasoning variants, and open/closed models, enables useful comparative analysis.

- **Thoughtful analysis of benchmark distinctiveness.** The paper finds weak correlation with Aider Polyglot (r=0.24) and Chatbot Arena coding (r=0.11), and provides a reasoned discussion of why (code-centric input/output, interaction modality, real-world user intent). The ablation on contextual information (Table 3) showing 5/7 models improve with highlighted code, and the finding that hard problems have 5x shorter instructions but longer highlighted code, are genuinely insightful for future research.

## Weaknesses

### Major

- **No contamination analysis.** This is the most significant gap. The problems are derived from real-world code written by developers and likely use libraries, patterns, and idioms that exist in training corpora (e.g., The Stack). The paper does not check for n-gram overlap, perform time-based separation between data collection and model training cutoff dates, or discuss how contamination is mitigated. For a benchmark that aspires to measure real-world editing ability, this omission threatens validity — a model could succeed because it memorized a similar edit from training rather than because it can follow real-world editing instructions. This concern applies to both the real-world code contexts and the instructions themselves.

### Minor

- **Framing inflates effective benchmark size.** The abstract, introduction, and Table 1 state "540 problems," but these are 109 unique problems translated across 5 languages (Section 3.2). While the paper transparently discloses the 109 figure in Section 3.2, the dominant framing of "540 problems" without consistently distinguishing translations from independent scenarios is potentially misleading about the effective sample size for core editing ability. A model that solves the English version has a structural advantage on translated versions (same underlying code logic; only comments and instruction text change). The paper should consistently state "109 unique problems (540 including translations)."

- **Filtering pipeline is not characterized.** From 2672 accepted edits → ~470 interesting/challenging → 109 testable problems, roughly 96% of raw data is removed. The paper acknowledges removing "trivial," "stylistic," and "ambiguous" edits (Section 3.2) but does not characterize the distribution of what is filtered out. If most real-world edits are trivial parameter changes or comment additions, the benchmark evaluates only a hard-problem tail rather than being representative of "real-world usage." The paper should clarify whether EditBench is a challenge set or a representative sample.

- **Key correlation result is not statistically significant.** The correlation with Aider Polyglot (r=0.24, p=0.06, n=17 shared models) does not reach conventional significance thresholds. The paper characterizes this as supporting evidence for uniqueness but should more clearly acknowledge that the null hypothesis (no correlation) cannot be rejected. Supplementing with rank correlation or confidence intervals would strengthen this analysis.

- **No confidence intervals for model scores.** Individual model pass@1 scores are reported as point estimates without confidence intervals. While pass@1 with temperature=0 is deterministic for a given problem set, bootstrap CIs across problems would help assess whether observed gaps between models (e.g., the spread in the top tier) are meaningful rather than noise from the specific problem sample.

## Nice-to-Haves

- A small ablation comparing full-file regeneration vs. diff-only output vs. highlighted-region-only output on a subset of models would validate (or reveal biases in) the chosen evaluation protocol.
- The collected user votes between model pairs (mentioned in Section 3) could support an analysis correlating pass@1 with human preference — a valuable validation left on the table.

## Removed Points

These points were raised by the input reviewers but removed after cross-checking against the paper:

- **Full-file regeneration evaluation**: The critic argued this diverges from how code editing works in practice. However, since EditBench evaluates via unit tests (pass@1), not diff-matching, regenerating the full file is appropriate — the test harness measures functional correctness, not edit minimality. SWE-Bench uses the same approach. **REMOVED** (misunderstands evaluation design.)
- **Human evaluation data not used**: The critic argued collected user votes are not analyzed. This is scope creep — the paper's contribution is the benchmark, not a human evaluation study. **REMOVED**.
- **Multiple valid edits not discussed**: The paper explicitly states annotators were instructed to create tests "generalizable to different potential implementations" (Section 3.3). This concern is already addressed. **REMOVED**.
- **Missing appendix content / reproducibility**: The appendix was stripped by the PDF parser. **REMOVED** per guidelines.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Add a contamination analysis**: Check n-gram overlap between EditBench code contexts and common training datasets (e.g., The Stack, GitHub repos with permissive licenses). Perform temporal separation between data collection dates and model training cutoff dates. This single addition would substantially strengthen the benchmark's validity.
- **Characterize the filtering pipeline**: Show the distribution of filtered edits (e.g., "40% comment additions, 25% single-parameter changes, 15% ambiguous") and argue why the retained 4% are the most informative for evaluating model capability. This would clarify whether EditBench is a challenge set or a representative sample.
- **Rephrase benchmark size**: Consistently use "109 unique problems (540 including language translations)" to avoid inflating the apparent sample size.
- **Report confidence intervals**: Provide bootstrap CIs across problems for model pass@1 results to enable meaningful comparison of model gaps.
- **Acknowledge the statistical limitation**: Caveat the p=0.06 correlation more prominently, and consider supplementing with Spearman rank correlation.

## Anchors Used for Calibration

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| SWE-bench (`VTF8yNQM66.md`) | 6.25 | 1 | Yes | Larger-scale real-world benchmark (2294 problems). EditBench has multilingual scope and single-edit focus but smaller unique problem set and lacks contamination analysis. |
| LiveCodeBench (`chfJJYC3iL.md`) | 6.25 | 1 | Yes | Contamination-free benchmark using competition problems. EditBench uses real-world data (stronger ecological validity) but does not address contamination (LiveCodeBench's main strength). |
| ML-Bench (`sf1u3vTRjm.md`) | 5.75 | 2 | Yes | Repository-level ML benchmark with data leakage concerns similar to EditBench's contamination gap. EditBench has clearer methodology and better presentation. |
| Codev-Bench (`c2C2NQKjZw.md`) | 4.25 | 1 | Yes | Developer-centric code completion benchmark with small dataset and unclear methodology. EditBench is substantially stronger across all dimensions. |

Round 1 bracket: 5.0–7.0. Round 2 narrowed the range by anchoring against ML-Bench (5.75, weaker presentation/methodology) on the lower end and SWE-bench (6.25, larger scale and influence) on the upper end. The final score of 6.0 reflects that EditBench has genuine, well-executed contributions (real-world data, multilingual scope, comprehensive evaluation) with favorability-rated strengths all above 8.0, but is pulled down by the contamination gap (weakness favorability 1.27 — the lowest-rated item), which prevents it from reaching the level of SWE-bench or LiveCodeBench. The paper is stronger than ML-Bench (5.75) which was rejected partly due to similar data leakage concerns compounded by presentation issues.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>