## Summary

EditBench introduces a benchmark for evaluating LLM code editing capabilities, built from real user instructions and code contexts collected via a VS Code extension used by ~500 programmers. The benchmark comprises 109 unique problems (translated into 5 natural languages for 540 total problems), requiring models to jointly ingest user instructions, code context, highlighted code, and cursor position. The paper evaluates 40 LLMs, finding that only the top model exceeds 60% pass@1, that context (especially highlighted code) improves performance, and that EditBench correlates only weakly with existing edit benchmarks like Aider Polyglot.

## Strengths

1. **In-the-wild data source (Section 3.1).** The data is collected from ~500 real programmers performing their actual work via a VS Code extension, which is qualitatively different from prior benchmarks built on annotator-written problems or educational exercises. Table 2 convincingly demonstrates that real user instructions are less specified and more varied than existing benchmark prompts (e.g., error-trace dumps as instructions vs. well-formed natural language requests). This is the paper's core contribution and it is a genuine one.

2. **Context-dependent problem design (Section 1, Table 3).** EditBench is the first benchmark to require models to jointly ingest the user instruction, full code file, highlighted code region, and cursor position. The ablation in Table 3 validates this design: adding highlighted code improves performance for 5/7 models by up to 3.5%, confirming the benchmark measures something beyond simple instruction-following.

3. **Weak correlation with existing benchmarks (Section 5.2).** The finding that EditBench has only weak correlation with Aider Polyglot (r=0.24) and Chatbot Arena coding (r=0.11) demonstrates that the benchmark is not redundant with existing ones and captures a different dimension of code editing capability — the messiness of real-world usage rather than clean exercise-style problems.

4. **Large-scale model evaluation.** Evaluating 40 models across multiple families, sizes, and reasoning schemes provides useful resolution, and the per-category breakdown (Figure 5) and easy/hard split analysis offer insights beyond a single ranking.

## Weaknesses

### Fatal

None.

### Major

- **Effective benchmark size is 109 unique tasks, not 540 (Sections 3.2, 4, Abstract).** From 2672 collected user-accepted edits, the filtering pipeline yields 109 core problems. The 540 figure comes from translating these same 109 problems into 5 natural languages (EditBench-complete), producing 5 variants of each task. The abstract, Table 1 (which compares against benchmark counts of 105–225), and the body prominently feature "540 problems" without adequately qualifying that the unique task set is 109. For a benchmark paper, the independent problem count matters for discriminative power and statistical reliability — with n=109, each problem accounts for ~0.9% of pass@1, making the gap between top models potentially a matter of 1–2 problems. The paper reports no confidence intervals. Furthermore, the multilingual translation leaves the underlying code editing task identical across language versions (code itself is unchanged; only comments and instructions are translated), so this is not equivalent to 540 independent problems. This does not invalidate the benchmark but the framing inflates its apparent scale.

- **No inter-annotator reliability for test harness creation (Section 3.3).** The test cases are created by 5 human annotators who reconstruct the user's intent from the instruction, code, highlighted region, and cursor position. The paper acknowledges that instructions can be "too ambiguous" and that annotators were told to "adhere to the user's intent" while removing ambiguous problems. However, the user's original intent is not directly observable — it must be inferred from the same context the LLM receives, creating a circularity concern. The paper reports that a second annotator reviewed each test case but provides no inter-annotator agreement statistic. Without calibration data on how often annotators agreed or disagreed, or how disagreements were resolved, it is difficult to assess whether the test cases represent objective ground truth or annotator-specific interpretations. This matters because another team annotating the same raw data might produce different test cases and potentially different model rankings.

### Minor

- **Full-file regeneration protocol diverges from real-world editing practice (Section 5).** The paper states: "the model is given the user instruction and main code context and requested to edit the entire file by regenerating the entire code context." In real instructed-code-editing tools (Copilot, Cursor), the model typically produces a surgical edit to the highlighted region, not a full file regeneration. Requiring the model to reproduce all unchanged code verbatim is a harder task that measures faithful reproduction alongside editing capability. This creates a modest gap between the paper's framing ("real-world" code editing) and its evaluation protocol. The paper should at least discuss this design choice and its implications for result interpretation.

- **Selection bias in data collection is acknowledged but not characterized (Section 3.1).** Users receive free API access in exchange for their data, creating a specific demographic. The paper reports 458 users and 2672 accepted edits, but does not report: (a) the acceptance rate of model suggestions (which would indicate how filtered the data is), (b) the distribution of contributions across users (whether problems come from many users or a few heavy contributors), or (c) the nature of the projects (personal, coursework, professional). These do not invalidate the benchmark but constrain generalizability claims.

- **Translation validation is thin (Section 3.2).** The paper states that translations were validated by "native speakers evaluating a subset" but does not specify the subset size, the agreement rate, or how many translations (if any) were flagged as poor and corrected. The underlying code is unchanged across languages, so the multilingual dimension adds value primarily through instruction phrasing and code comments — the quality of these translations should be better documented.

- **Limitations section omits key concerns (Section 6).** The limitations section focuses on wanting more examples and languages but does not address the test harness subjectivity concern, the 109 vs. 540 framing issue, or the evaluation protocol mismatch. This is a missed opportunity for transparency about the benchmark's known boundaries.

### Trivial

- **Specific quantitative claim without supporting statistic (Section 5.1).** The paper states that "hard instructions tend to have shorter instructions (by nearly 5 times)" without providing the actual numbers for easy vs. hard instruction lengths. This should be reported for completeness.

## Nice-to-Haves

- Report confidence intervals or bootstrap variance estimates for pass@1 scores, especially given the 109-problem effective size.
- Provide inter-annotator agreement metrics (e.g., Cohen's κ or simple agreement rate) for test harness creation, or explicitly discuss why this was not feasible.
- Compare model outputs against the user's original accepted edit (from the data collection phase) as a sanity check on whether test cases align with real user preferences.
- Include the exact prompt formatting for highlighting and cursor position (likely in the stripped appendix) in the camera-ready version.

## Removed Points

These points from the input review were removed under the filtering rules:
- *"The interpretation in the conclusion is somewhat stronger than the evidence supports" for the correlation finding.* Removed because the paper accurately describes r=0.24 as a "weak" correlation and does not overclaim.
- *Comments about the stripped appendix (prompts, additional results).* Removed per the rule that parser-stripped sections exist in the original submission.
- *"Missing Parts" items about per-problem granularity and clarifying EditBench-core vs. -complete.* These overlap with weaknesses already included above; removing duplication.
- *Comment about the correlation with Aider Polyglot not being statistically significant.* The paper reports p=0.06 and uses appropriate cautious language; this is not a paper error.

## Novel Insights

The reviews surface a tension inherent in benchmark construction from in-the-wild data: the very property that makes EditBench valuable (real, messy user instructions) also makes it harder to construct objective ground truth, since the annotator must reconstruct unobservable user intent from the same context the model sees. This circularity is not unique to EditBench but the paper would benefit from explicitly addressing it. Additionally, the 109-vs-540 observation highlights a broader question for the multilingual benchmark community: when a benchmark is translated, should the translated variants be counted as independent test instances, or should they be treated as a single task across languages?

## Suggestions

1. Transparently frame the benchmark by its unique problem count (109) throughout the paper, presenting the multilingual 540 version as an augmentation rather than the primary count.
2. Report inter-annotator agreement for test harness creation, even if retrospective on a subset.
3. Add a brief discussion of why the full-file regeneration protocol was chosen and how results might differ under a surgical-edit protocol.
4. Provide the actual statistics for the easy vs. hard instruction length comparison.
5. Report the distribution of user contributions (e.g., number of edits per user, acceptance rate of suggestions) to help readers assess dataset diversity.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>