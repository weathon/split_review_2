## Summary

EditBench introduces a benchmark for evaluating LLMs on instructed code editing, grounded in real user data collected via a VS Code extension from ~500 developers. The dataset comprises 540 problems (originating from 109 unique user edits, translated across 5 natural languages) featuring code context, highlighted code, and cursor position. An evaluation of 40 models shows that only one model (claude-sonnet-4) exceeds 60% pass@1, that contextual information meaningfully affects performance, and that the benchmark correlates only weakly with existing code editing benchmarks, confirming it measures something distinct.

## Strengths

- **Genuinely real-world data collection (Section 3.1).** The paper develops a VS Code extension and recruits ~500 real developers in their normal workflows. This is a principled departure from prior work (CanItEdit, EditEval, Aider Polyglot) that relies on annotator-written or educational/competitive-programming problems. The inclusion of user-acceptance signals ("whether the user accepted the edit") provides an additional grounding signal absent from other code-editing benchmarks.

- **Context-dependent problems advance the evaluation paradigm (Section 3.2, Table 1, Table 3).** EditBench is the first benchmark to include highlighted code, cursor position, and full file context together for instructed code editing. The ablation in Table 3 validates that highlighted code improves performance for 5 of 7 top models, and the finding that "hard" problems have 5× shorter instructions but longer highlighted code (Section 5.1) is a nontrivial insight that emerges directly from the benchmark's design.

- **Diversity across natural languages, libraries, and task categories (Table 1, Figure 3).** EditBench spans 5 natural languages, 74 unique Python imports (vs. 25 for CanItEdit, 15 for Polyglot, 16 for EditEval), and 4 functional edit categories. This is a concrete improvement in coverage that matters for evaluating multilingual and general-purpose coding assistants.

- **Weak correlation with existing benchmarks is well-characterized (Section 5.2).** The finding that EditBench has only weak correlation with Aider Polyglot (r=0.24, p=0.06) and Chatbot Arena Coding (r=0.11, p=0.01) is exactly the evidence a new benchmark should provide to show it is not redundant. The paper's interpretation (code-centric IO, interaction modality, real-world intent) is reasonable.

## Weaknesses

### Fatal

None.

### Major

- **Selection bias from filtering is acknowledged but uncharacterized (Section 3.2).** The chain from 2672 accepted edits to 109 unique problems (a ~4% yield) involves multiple subjective filtering decisions: excluding problems that are "too similar," "trivial," "stylistic," or "ambiguous," and retaining only those that annotators found "interesting" and "challenging" and could create test harnesses for. The paper does not analyze how the final distribution compares to the raw distribution of accepted edits. While the paper's core claim—that problems originate from real users—is not invalidated, the claim that EditBench captures "real-world usage" (abstract) is substantially weaker without evidence about what kinds of real-world edits were filtered out. The paper should at minimum report statistics (category frequencies, instruction lengths, context lengths) for the raw 2672 edits alongside the final 109 to clarify what was lost.

### Minor

- **No inter-annotator agreement statistics (Section 3.3).** Five annotators wrote test cases interpreting user intent from instructions, code context, highlighted code, and cursor position. The paper mentions a second-review step but reports no agreement metrics (e.g., what fraction of tests were accepted without changes, or Cohen's κ on a subset). For a benchmark where human judgment mediates the primary correctness signal, this is a gap that should be filled.

- **Translation inflates the problem count without accounting for statistical dependencies (Section 3.2).** The 540-problem figure comes from translating 109 unique core problems across 5 languages. Results are reported aggregated over all 540 problems, but the underlying tasks are not independent (the same coding problem appears 5 times in different languages). Reporting pass@1 on the 109 English core subset separately, or showing variance across language translations within each problem, would clarify whether language-specific noise or actual multilingual difficulty drives the results.

- **No contamination analysis.** Since models are trained on GitHub data, some EditBench problems may have near-exact matches in training data. The paper does not discuss this, even as a limitation.

- **No reliability analysis.** For a benchmark intended to rank models, the paper does not report test-retest reliability or split-half consistency, making it unclear how much of the observed performance differences reflect genuine capability gaps versus measurement noise.

- **"User accepted the edit" signal is collected but not used as a validation signal.** The extension logs whether users accepted the suggested edit (Section 3.1). Comparing this signal against benchmark correctness could validate the test harnesses—if users accepted edits that the benchmark marks as wrong (or vice versa), it would indicate a test quality issue. This analysis is absent.

- **The glm-4.6 anomaly in Table 3 is reported but not explained.** The +Highlight+Cursor column shows a -8.15 drop from the code-only baseline—a larger effect than any other model shows. This outlier deserves investigation to rule out a bug in the evaluation pipeline or a meaningful model-specific failure mode.

### Trivial

- The derivation of the four edit categories (Section 4, line 150) is described as "by analyzing in-the-wild user instructions...we derive four different categories." The method of derivation (clustering? manual labeling? annotator consensus?) is not specified.

## Nice-to-Haves

- A qualitative error taxonomy across a few representative models would increase the benchmark's diagnostic value beyond the aggregate pass@1 scores and the single anecdotal observation about gpt-5 formatting issues.
- Results disaggregated by natural language (e.g., English vs. translated problems) would clarify whether translation quality affects model rankings.

## Removed Points

- **Concern about Appendix C not being available:** Removed because the parser strips appendices from all papers; they exist in the original submission.
- **Concern about the "few benchmarks directly evaluate this capability" claim being undercut by CanItEdit/Polyglot:** Removed because the paper correctly acknowledges these benchmarks and differentiates itself; "few" does not mean "none."
- **Speculative concern about GPT-4o/Sonnet 3.7 solutions "anchoring" annotators:** Weakened and moved here because the paper transparently states these were used "to give insight into possible solutions" (not as ground truth), and this is a standard practice in benchmark creation. No evidence is presented that anchoring actually occurred.
- **Concern about evaluation protocol (full-file regeneration vs. diff-based editing):** Moved here because this is the standard evaluation protocol used by prior code editing benchmarks (CanItEdit, EditEval), and the paper applies it consistently across all models. The comparison is fair; a different protocol would be a design choice, not a flaw.
- **Concern about the p=0.06 for Polyglot correlation not being "statistically significant":** Removed because the paper transparently reports the p-value and does not overclaim significance (it says "weak, positive correlation," which is accurate regardless of the p-value threshold).
- **Participant selection bias (developers already using AI tools):** Removed because this is a reasonable design choice for collecting naturalistic data and is implicitly acknowledged.

## Novel Insights

The most interesting finding to emerge across the review is the tension between the paper's strength—genuinely grounding a benchmark in real user data via an IDE extension—and the methodological challenge this creates: the data collection pipeline is rich but noisy, and the multi-stage filtering from 2672 raw accepted edits to 109 testable problems introduces selection biases that are hard to quantify. This tension is common to all in-the-wild benchmark construction efforts, but EditBench illustrates it more clearly than most. The paper's own finding that "hard" problems have shorter instructions but longer highlighted code demonstrates that the benchmark is diagnostic precisely because it preserves the ambiguity and context-dependence of real user requests—but this same ambiguity makes constructing unambiguous test harnesses difficult, and the paper's reliance on human annotator interpretation without agreement metrics is the weak link. This suggests that future work on real-world code editing benchmarks should invest in automated or semi-automated test generation procedures that can be validated at scale.

## Suggestions

1. **Characterize the filtering gap.** Add a table comparing the raw distribution of the 2672 accepted edits with the final 109 problems across dimensions: edit category, instruction length, code context length, programming language. This would directly address the most significant concern about selection bias.
2. **Report results on the 109 core English problems separately** from the full 540-translated set. If the rankings are consistent, this alleviates concerns about the translation pipeline; if they shift, it surfaces a genuine methodological issue.
3. **Add inter-annotator agreement metrics** for test harness creation (e.g., what fraction of tests required changes after the second review, or a small-scale double-annotation study with Cohen's κ).
4. **Discuss contamination risk** explicitly, even if only to acknowledge it as a limitation.
5. **Investigate and explain the glm-4.6 anomaly** in Table 3—a -8.15 drop in the +Highlight+Cursor condition is an outlier that warrants a brief analysis or caveat.

## Score and Decision

<score>6.5</score>
<decision>Accept</decision>