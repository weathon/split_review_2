## Summary

This paper introduces LPFQA, a benchmark for evaluating LLMs on long-tail professional knowledge sourced from real technical forums across 20 fields (505 questions). The benchmark is constructed via an eight-step pipeline: forum collection, link scraping, screenshot capture, MLLM-based QA generation, LLM-based cleaning, format conversion, expert verification, and difficulty calibration. The authors evaluate 12 frontier models and report scores ranging from 32.40 to 47.28, with additional ablation studies examining tool-augmented reasoning. The paper claims four innovations: fine-grained evaluation dimensions (knowledge depth, reasoning, terminology comprehension, contextual analysis), hierarchical difficulty, authentic professional scenario modeling with user personas, and interdisciplinary knowledge integration.

## Strengths

- **Well-motivated gap with a reasonable construction approach.** The paper correctly identifies that existing benchmarks either test broad but shallow knowledge (MMLU), use overly artificial scenarios (HLE), or lack domain depth (Arena-Hard). Sourcing real forum questions from professional technical forums to capture long-tail knowledge is a sensible and underexplored direction. The eight-step pipeline (data collection → screenshot capture → MLLM-based QA generation → cleaning → format conversion → expert verification → difficulty calibration) is clearly described and largely reproducible if the appendix delivers its promised prompts and forum lists (Section 3.2).

- **Broad and timely model coverage.** The evaluation spans 12 frontier models including GPT-5, Gemini-2.5-Pro, DeepSeek-R1, o3-high, Claude-4, and Grok-4 (Section 4), providing a useful comparative snapshot. Results are averaged over three trials (line 211).

- **Ablation studies on tool augmentation.** The experiments with code interpreter and web search tools (Section 4.2.2) are interesting — showing that neither tool reliably helps on long-tail knowledge — and yield a non-trivial finding about the difficulty of retrieving such knowledge from the web.

## Weaknesses

### Major

- **The "overall performance" analysis (line 265) directly contradicts the data in Table 1.** Table 1 shows DeepSeek-V3 scoring 32.60 (second-worst, barely above GPT-4o's 32.40) while GPT-5 leads at 47.28. Despite this, the text states: *"Among all evaluated systems, DeepSeek-V3 demonstrates the most balanced and consistent performance across disciplines, with no apparent weaknesses, and can thus be regarded as the overall best-performing model."* It further claims GPT-5 "in some cases surpasses DeepSeek-V3" — GPT-5 is 45% higher overall. This is not a minor phrasing issue; the written analysis is inconsistent with the paper's own empirical results. This erodes confidence in the entire results section and must be corrected.

- **The four "fine-grained evaluation dimensions" are claimed as a core innovation but never operationalized.** The abstract, introduction (line 25), Section 3.1 (line 60), and conclusion all claim that LPFQA evaluates LLMs across four dimensions: *knowledge depth, reasoning ability, terminology comprehension, and contextual analysis.* Yet the evaluation section contains no per-dimension scores, no rubric for classifying questions into these dimensions, no inter-annotator agreement, and no validation that the dimensions are separable. The only ablation study (Section 4.2.2) treats "knowledge vs. reasoning" as a binary question, not a four-dimensional framework. A contribution that exists only as a textual claim is not a substantiated contribution.

- **No quantitative comparison with existing benchmarks.** This is a benchmark paper whose motivation hinges on limitations of MMLU, HLE, and Arena-Hard. Yet it provides zero quantitative evidence that LPFQA addresses these gaps — no rank-correlation analysis, no discriminative-power comparison, no overlap analysis of knowledge coverage, and no comparison of how model rankings differ across benchmarks. The motivation remains an informed assertion rather than a demonstrated fact. Adding even a basic correlation analysis with one existing benchmark would substantively strengthen the paper.

### Minor

- **The "user persona" claim is asserted but not demonstrated.** The contribution list (line 27) states the benchmark includes *"constructing detailed user personas and realistic contextual scenarios."* However, no user persona is ever described, shown, or analyzed anywhere in the paper. The construction pipeline (Section 3.2) does not mention persona construction, and the two example questions in Figure 1 present raw forum questions without any persona framing. This claim appears unsupported by any evidence in the current manuscript.

- **The ablation study's conclusion overreaches its evidence.** Section 4.2.2 concludes that because a Jupyter Code Interpreter tool did not improve performance, LPFQA *"primarily reflects a model's mastery of domain knowledge rather than its reasoning ability."* A code interpreter supports numerical computation and code execution — it is not a general-purpose reasoning amplifier. Failure of this one narrow tool does not imply the benchmark lacks a reasoning component; many forms of reasoning (analogical, causal, diagnostic) are not aided by code execution. The experiment shows that LPFQA questions are not primarily computational, which is a weaker claim. Additionally, this conclusion sits uneasily with the paper's own title and framing around evaluating "complex reasoning."

- **Severe field imbalance with no caveats on per-field comparisons.** Several fields have ≤10 questions: Data Science (3), ICE (7), AI (8), Aerospace (8), Energy (9), EIE (10), EIS (10). Per-field model comparisons on 3–10 questions are essentially noise, yet the paper reports radar charts and draws conclusions about model strengths/weaknesses in these fields without acknowledging sample-size limitations (Section 3.3, Section 4.1).

- **Scoring methodology for short-answer questions is underspecified.** The paper states that short-answer responses are evaluated against "key knowledge points" (line 128) but never describes how this matching is performed — is it exact match, LLM-as-judge, human evaluation, or some automated rubric? Without this, the reproducibility of the core evaluation is unclear.

- **The filtered LPFQA introduces a circularity concern (Section 4.2.1).** The paper removes questions that no model could answer (69 questions) and also questions all models got right (15 questions) based on the performance of the exact same 12 models being evaluated. While the motivation (removing non-discriminative questions) is understandable, the filtered benchmark is optimized for this specific model set. The resulting "improved" scores (Table 2) are partly an artifact of filtering on the test set.

### Trivial

- **"502 tasks" (abstract, line 9) vs. "505 questions" (introduction, line 21; Section 3.1, line 58)** — a minor numerical inconsistency.
- **"CS (2121)" in Figure 5 caption and Table 2 (line 234, 238)** — clearly a formatting error; should be "21" or similar.
- **The "relatively narrow range" characterization (line 230)** — describing 32.40–47.28 (a ~32% relative spread) as "narrow" is debatable, though not a substantive error.

## Nice-to-Haves

- Add a correlation/overlap analysis with at least one existing benchmark (e.g., MMLU or HLE) to demonstrate that LPFQA captures distinct knowledge.
- Operationalize the four evaluation dimensions by showing per-dimension scores, or remove the claim from the contribution list.
- Acknowledge the sample-size limitations for fields with <15 questions when drawing per-field conclusions.
- Clarify the short-answer scoring procedure.

## Removed Points

These points were identified by the harsh critic but are removed based on the filtering rules:

- *"The related work section is entirely generic"* — This is a subjective opinion about writing style, not a specific weakness that can be verified against the paper's claims. No concrete error is identified.
- *"Missing appendix" concerns about prompts and forum lists* — The paper states these will be in the appendix (Reproducibility Statement, line 333). Per instructions, missing appendix content is not a valid criticism since the parser strips appendix sections from all papers.
- *Criticism that DeepSeek-V3 claim "could be a typo (intended to say DeepSeek-R1)"* — Even if corrected to DeepSeek-R1 (38.25, below average 39.08), calling it "overall best-performing" would still be inconsistent. This speculation is subsumed by the verified factual contradiction. The core error stands regardless of which model was intended.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the gap between the paper's claimed contributions (four evaluation dimensions, user personas) and what is actually demonstrated, but this is a standard gap between aspiration and execution rather than a novel observation about the field.

## Suggestions

1. **Fix the DeepSeek-V3 error.** Reconcile the textual analysis in Section 4.1 with Table 1. If DeepSeek-V3 was meant to be DeepSeek-R1, the claim of "overall best-performing" still requires justification given its below-average overall score.
2. **Either operationalize or remove unsubstantiated claims.** The four evaluation dimensions and user persona claims appear in the abstract, contributions, and conclusion but have zero supporting evidence. Either provide per-dimension results and inter-annotator agreement, or remove these claims.
3. **Add benchmark comparison data.** At minimum, report rank correlations between LPFQA and one existing benchmark (e.g., MMLU) and show which models shift position — this would demonstrate that LPFQA captures information not present in existing evaluations.
4. **Add sample-size caveats** for per-field comparisons on fields with ≤10 questions.

## Score and Decision

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>