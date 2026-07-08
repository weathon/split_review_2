## Summary

This paper introduces EditBench, a benchmark for evaluating LLM abilities to perform instructed code edits, built from real-world user data collected via a VS Code extension used by ~500 developers. The benchmark features 109 core problems (translated into 5 languages for 540 total) that require models to process user instruction, full file code, highlighted code, and cursor position together — a combination no prior edit benchmark includes. The authors evaluate 40 models across 11 families and find that EditBench is only weakly correlated with existing benchmarks (Aider Polyglot r=0.24, Chatbot Arena r=0.11), suggesting it captures a distinct capability axis.

## Strengths

- **Genuinely in-the-wild data source (Section 3.1).** The VS Code extension collected data from ~500 real developers performing actual coding tasks. Unlike existing edit benchmarks (CanItEdit, EditEval, Aider Polyglot) that rely on annotator-written or educational problems, EditBench captures messy, underspecified instructions real users write — including error-trace dumps, multi-language instructions, and informal requests like "fix this." Table 2 effectively illustrates this qualitative difference. **[weight=7.74]**

- **First benchmark to include all four information channels for instructed code editing (Sections 1, 3.2).** EditBench is the first edit benchmark to require models to process user instruction, full file code, highlighted code, and cursor position together. Table 1 confirms no prior benchmark includes highlighted code, and the ablation in Table 3 shows this context matters for most models (up to +3.52pp improvement). **[weight=8.22]**

- **Weak correlation with existing benchmarks (Section 5.2).** The finding that EditBench has only weak positive correlation with Aider Polyglot (r=0.24, p=0.06) and Chatbot Arena coding (r=0.11, p=0.01) meaningfully demonstrates that EditBench captures a different capability distribution. The discussion of why (code-centric input/output, interaction modality, real-world user intent) is thoughtful and provides face validity. **[weight=8.95]**

- **Substantial model evaluation (Section 5).** Evaluating 40 models spanning 11 families (including both open and closed models) with controlled temperature=0 is thorough. The category-level breakdown in Figure 5 (bug fixing, feature addition, modification, optimization) reveals informative patterns — e.g., models excel at bug fixing (most similar to existing benchmarks) but struggle with optimization. **[weight=8.66]**

- **Diverse problem coverage (Section 4).** EditBench covers 74 unique library imports (vs. 25 for CanItEdit, 15 for Polyglot, 16 for EditEval), indicating substantially broader application-domain coverage. The four-category taxonomy derived from actual user data is well-motivated and useful. **[weight=8.47]**

## Weaknesses

### Major

1. **Inflated headline problem count (109 core problems presented as 540).** The paper reports "540 problems" throughout the abstract, introduction, and Table 1, but 431 of these are GPT-4o translations of the same 109 core problems (EditBench-core → EditBench-complete). In Table 1, "540" is directly compared against benchmarks with 105, 194, and 225 *unique* problems — an apples-to-oranges comparison that inflates the benchmark's apparent diversity. The 109→540 pipeline is described in Section 3.2, which somewhat mitigates this concern, but the headline number remains misleading where it matters most (Table 1's comparison column). This is fixable: report 109 (core) in the table with a footnote clarifying the 540 total includes translated variants.

2. **No confidence intervals, variance estimates, or significance testing for the 40-model ranking.** All results are single-pass pass@1 at temperature=0. Many models are separated by <3pp (e.g., glm-4.6 at 56.48% vs. kimi-k2-0905 at 56.48% — identical — and deepseek-chat-v3.1 at 54.26%). Without bootstrapped confidence intervals or repeated trials, fine-grained model rankings are not statistically supported, and surprising findings (e.g., "gpt-5 lags behind gpt-5-mini") could be noise. The paper presents the ranking as ordinal without caveats. Bootstrapping over the 109 problems would address this.

3. **Undisclosed contamination risk from the data collection pipeline.** The benchmark is constructed from *accepted edits* — model-generated outputs that users accepted (Section 3.1). The paper does not disclose which "state-of-the-art models" powered the extension's suggestions. If the extension used the same model families (GPT-4o, Claude) that are then evaluated on the benchmark, those models could have a systematic advantage because the test cases derived from their accepted edits may be implicitly calibrated to their output style. The paper mentions safeguards in Section 3.3 (annotators instructed to write generalizable test cases, second-reviewer process), but does not disclose the extension models or provide evidence that model performance is not correlated with which model generated the accepted edit.

### Minor

4. **Unanalyzed selection bias from ~23% conversion rate.** Only 109 of ~470 candidate problems (23%) were successfully turned into testable problems (Section 3.2). The paper does not characterize what distinguishes the 361 filtered-out problems. If problems easy to write test cases for differ systematically from those that aren't (e.g., simpler edits, more deterministic expected behavior), the benchmark may not represent the full distribution of real-world edits. The diversity analysis (74 unique imports, varied context lengths) only applies to the surviving problems.

### Trivial

None.

## Nice-to-Haves

- **Characterize filtered-out problems:** Even a brief categorization of the ~361 excluded problems (e.g., "30% too ambiguous, 25% too many external dependencies") would directly address the representativeness concern.
- **Add caveats for fine-grained ranking:** Note in the results section that differences below ~5pp should be interpreted cautiously without confidence intervals.
- **SWE-Bench correlation:** While the paper argues EditBench and SWE-Bench target different tasks (single-file instructed edits vs. multi-file agentic fixes), adding this comparison for the 40 models would strengthen the positioning against the most prominent real-world coding benchmark.

## Removed Points

These points are flagged as removed; treat them with caution.

- **"8% performance variation" as overstatement (Harsh Critic):** The critic argued the abstract's "performance varying up to 8%" uses the worst negative case (glm-4.6, -8.15%). However, "up to 8%" is factually accurate for the range of observed effects (both positive and negative). The abstract does not claim this is the typical effect. Removed as not substantively misleading.
- **Circular easy/hard split (Harsh Critic):** The critic noted that defining hard problems as those solved by ≤k models makes the 59.3% gap tautological. While technically true, the paper's real insight — hard problems have 5× shorter instructions and slightly longer highlighted code — is independently informative. Removed as minor presentation point that does not affect the paper's claims.
- **Missing SWE-Bench correlation (Harsh Critic):** The paper explicitly scopes itself to single-file instructed edits and distinguishes this from SWE-Bench's multi-file agentic bug fixes. The critic's suggestion to add SWE-Bench correlation is scope creep. Removed per Soft Rule on scope.

## Novel Insights

The review process reveals that the paper's core contribution — a real-world code editing benchmark that includes highlighted code and cursor position as first-class evaluation dimensions — is genuine and fills a clear gap. However, the paper's presentation choices (headline "540" problem count treated as comparable to other benchmarks' unique counts, uncaveated model rankings) systematically overstate the contribution's strength. The contamination concern, while plausible, would be straightforward to address with a disclosed-model analysis. This pattern — a solid core contribution undermined by over-claiming in presentation — is common in benchmark papers and accounts for the gap between the paper's genuine merits and the support for its strongest claims.

## Suggestions

1. **Revise the headline problem count:** Report 109 (core) as the primary count in Table 1 and throughout the paper, with the 540 total clearly distinguished as "including 4× language variants."
2. **Add bootstrapped confidence intervals:** For the 40-model ranking, compute 95% CIs via bootstrapping over the 109 problems and add a caveat that differences within overlapping intervals should not be interpreted as meaningful rankings.
3. **Disclose extension models:** State explicitly which models powered the VS Code extension and provide an analysis showing that model performance is not correlated with which model generated the accepted edit.
4. **Characterize the filtered-out problems:** Even a brief analysis of why the ~361 candidate problems were excluded would substantially strengthen the representativeness claim.

## Score and Decision

**Calibration:** Paper compared against 11 anchor papers retrieved across two rounds. The closest comparators are SWE-bench (6.25, accepted), Coeditor (6.25, accepted), and LiveCodeBench (6.25, accepted) — all with stronger positive-weighted items (multiple 9+ weights) in their reviews than EditBench's strongest items (8.95 max). EditBench's weaknesses (1.27–4.98) are all moderately positive, clearly above severely negative items in rejected papers like Codev-Bench (-6.45, -6.91) and the TDD benchmark (-4.94). This places EditBench above the reject region but below the clear-accept bar of the 6.25+ papers.

**Score rationale:** The paper makes a genuine contribution — a real-world code editing benchmark with contextual information that no prior benchmark includes — and the 40-model evaluation is thorough. However, the inflated headline problem count, lack of any statistical reliability for model rankings, and undisclosed contamination risk collectively prevent a clear acceptance recommendation. These issues are all fixable.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>