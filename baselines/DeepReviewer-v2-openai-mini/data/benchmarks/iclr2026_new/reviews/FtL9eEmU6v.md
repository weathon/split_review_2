## Summary
# Final Review Report

## Summary

This paper introduces **EditBench**, a benchmark for evaluating LLMs on instructed code editing tasks grounded in real-world user data. The authors developed a VSCode extension that collected 2672 user-accepted code edits from 458 developers, which were then curated and converted into 540 test problems spanning 5 natural languages and 2 programming languages (Python, JavaScript). EditBench is the first benchmark to combine all of: real user instructions, code context, highlighted code regions, and cursor position information. The authors evaluate 40 LLMs and find that only one model (Claude-Sonnet-4) exceeds 60% pass@1, that closed-source models generally outperform open-weight models, and that performance varies substantially across edit categories (bug fixing best at 52.2% average, optimization hardest at 44.6%). The benchmark correlates only weakly with existing edit benchmarks (r=0.24 with Aider Polyglot), suggesting it captures unique variance in model editing capability.

**Manuscript type**: Benchmark/Evaluation paper.  
**Core contribution**: The first static benchmark for instructed code editing built from in-the-wild user data rather than annotator-written or exercise-derived problems.  
**Overall assessment**: Solid and well-motivated benchmark with transparent construction methodology. The main weaknesses are the severe attrition rate from raw data to testable problems (96% loss), the lack of statistical confidence intervals in key experimental findings, and an overly brief limitations section that omits several known threats to validity.

## Strengths
**S1. Real-world grounding is a genuine differentiator.** The paper's primary strength is its data collection methodology: building a VSCode extension to capture real developer edits as they occur in daily workflows. This yields instructions and code contexts that are qualitatively different from annotator-written benchmarks (as convincingly shown in Table 2, where real user instructions like "take the globe countries layer from below // this and add it to the existing globe" are far less specified than the equivalent annotator-written prompts). This ecological validity is the paper's core contribution and is well-motivated throughout.

**S2. Transparent construction methodology.** The paper documents the data collection, problem curation, and test harness creation pipelines in sufficient detail for reproducibility. The authors honestly report their failed attempt to use coding agents for test generation (pattern-matching issues), the use of human annotators with second-review procedures, and the IRB-approved privacy controls. This transparency is commendable and sets a good standard for benchmark construction papers.

**S3. Broad and systematic model evaluation.** Evaluating 40 LLMs across 11 model families provides a much more comprehensive picture than typical benchmark papers. The inclusion of both closed-source and open-weight models, reasoning and non-reasoning models, and multiple sizes within the same family allows for nuanced analysis (e.g., the surprising finding that gpt-5 with default reasoning lags behind gpt-5-mini, or that open-weight models fill only 4 of the top 15 positions).

**S4. Informative context ablation study (Table 3).** The ablation of contextual signals (code only, +highlight, +cursor only, +highlight+cursor) across 7 diverse models is a well-designed experiment that reveals important heterogeneity: highlighted code helps most models but hurts some (o3-mini, qwen3-coder), and cursor position has mixed effects. These findings have practical implications for how IDE tools should format prompts for different backends.

**S5. Weak correlation with existing benchmarks supports the distinctiveness claim.** The finding that EditBench correlates only weakly with Aider Polyglot (r=0.24, p=0.06) and Chatbot Arena coding (r=0.11, p=0.01) provides quantitative evidence that existing edit benchmarks do not fully capture the same capabilities. This strengthens the argument that EditBench fills a gap in the evaluation landscape.

**S6. Multilingual coverage is forward-looking.** With 5 natural languages and a systematic translation pipeline (following HumanEval-XL methodology), EditBench is one of the first code-editing benchmarks to address multilingual evaluation. The native-speaker validation of translations (Chinese, Spanish) adds credibility, even though broader validation is needed.

## Weaknesses
**W1. Severe attrition from raw data to benchmark problems (Major).** From 2672 user-accepted edits, only 109 unique problems (approximately 4%) made it to EditBench-core. The paper notes three filtering stages (language focus, deduplication, trivial/ambiguous removal, and test harness feasibility) but does not quantify each stage's contribution or analyze what types of problems are systematically lost. This is the single greatest threat to the benchmark's external validity claim: if the test harness bottleneck preferentially eliminates certain problem categories (e.g., configuration-heavy tasks, multi-step edits, or dependency-heavy projects), the final benchmark may not represent the full distribution of real-world edits. The 540-problem count (EditBench-complete) is achieved through GPT-4o translation of the 109 core problems, not through additional real-world data, so the diversity bottleneck is at 109 items.

**Required action**: Add a flow-diagram or Sankey chart quantifying each curation stage. Conduct and report a manual analysis of the ~361 problems lost between 470 candidates and 109 testable items, categorizing why each was lost. Discuss how this attrition may bias the benchmark.

---

**W2. Missing statistical rigor in key experimental findings (Major).** Several central claims lack appropriate statistical support:
- The context ablation study (Table 3) reports per-model deltas without confidence intervals or significance tests. Given that pass@1 is computed from a single sample per problem, the variance of these deltas could be substantial, and readers cannot assess which observed differences are reliable.
- The easy/hard difficulty split (k=20) is arbitrary and relative to the current 40-model pool. Without bootstrap analysis or alternative threshold reporting, the classification is fragile.
- The correlation with Aider Polyglot (r=0.24, p=0.06) is not statistically significant at conventional levels. The paper reports it as a finding but does not qualify its marginal significance.

**Required action**: Add bootstrap confidence intervals for all main results (pass@1 per model, context ablation deltas, correlation coefficients). Report pass@3 or pass@5 as a robustness check. Acknowledge marginal significance for the Polyglot correlation.

---

**W3. Language inconsistency between sections (Minor).** The abstract and introduction state 5 languages as "English, Spanish, Russian, Chinese, Portuguese" while Section 3.2 (Problem Curation) lists "English, Russian, Chinese, Polish, and Spanish." Portuguese appears in the abstract but Polish appears in Section 3.2. This is a factual inconsistency that must be resolved before publication.

---

**W4. Underexplored cursor position confusion (Major).** In Table 3, glm-4.6 shows a dramatic performance drop when cursor position is added alongside highlighted code (from 56.48 to 44.81, an 8.15% decrease). This is a large effect that goes unexplained. The paper dismisses cursor position as having "mixed performance" but does not investigate whether the problem stems from prompt formatting, model-specific tokenization issues, or genuine confusion about cursor semantics. If cursor position systematically degrades certain models, this has important implications for how IDE tools should format prompts.

**Required action**: Analyze the glm-4.6 failure cases in the +Highlight+Cursor condition to determine the root cause. Add a discussion of how cursor position should be represented in prompts to minimize model confusion. Consider adding a recommended prompt format for cursor position.

---

**W5. GPT-4o translation dependency without bias analysis (Medium).** The 5-language translation pipeline relies on GPT-4o to translate problems. While native speakers validated a subset, the paper does not analyze whether GPT-4o translations systematically alter problem difficulty. If GPT-4o's translations contain subtle cues or simplifications that advantage GPT-family models (or disadvantage others) differentially across languages, the multilingual rankings could be biased. Additionally, only Chinese and Spanish translations were validated by native speakers — Russian and Portuguese translations lack direct validation, and the Section 3.2 text mentions Polish (not Portuguese) as the fifth language, raising questions about which languages were actually validated.

**Required action**: Conduct a controlled experiment comparing model performance on original (English) vs. translated problems for a subset of languages, stratified by model family, to test for translation-induced bias. Validate Russian and Portuguese translations as well.

---

**W6. Limited edit scope relative to real-world development (Medium).** EditBench focuses on single-file edits where the model regenerates the entire file. Real-world code editing frequently involves multi-file changes, configuration updates, and dependency management. The paper positions itself as complementary to SWE-Bench (which handles multi-file agentic edits), but does not discuss where on the spectrum from single-line to multi-file its problems lie. The restriction to single-file edits is acknowledged implicitly but the implications for external validity are not discussed in the limitations section.

**Required action**: Add a quantitative analysis of edit scope (average lines changed, number of functions modified per problem) in the benchmark statistics section. Explicitly state the range of edit complexity covered and identify which real-world edit scenarios are not represented.

---

**W7. Single-sample evaluation limitations (Medium).** Using pass@1 with one sample per problem at temperature=0 provides no variance estimate. For a 109-problem benchmark, stochasticity in a few problems can shift rankings. The paper acknowledges this implicitly but does not discuss the impact on ranking stability. Additionally, "temperature=0 when possible" is ambiguous — which models could not use temperature=0 and what settings were used instead?

**Required action**: Report the number of models where temperature=0 was not available and the alternative settings. Add a ranking stability analysis (e.g., bootstrapped rank distributions or split-half reliability).

---

**W8. Selection bias from recruitment model (Minor).** Participants received free API access to state-of-the-art models rather than monetary compensation. This likely attracts developers who already use and value AI coding assistants, potentially skewing the problem distribution toward more AI-familiar users. The paper does not discuss this bias or its implications for benchmark representativeness.

**Required action**: Add a 1-2 sentence discussion of this selection bias in the limitations section, noting that future work should validate findings on a broader developer population.

---

**W9. Missing comparison to SWE-Bench rankings (Medium).** Given that SWE-Bench is the most prominent real-world code benchmark, the correlation analysis would be more informative if it included SWE-Bench. If EditBench also correlates weakly with SWE-Bench, that would strengthen the claim that it captures unique variance. If it correlates strongly, the differentiation argument would need refinement.

**Required action**: If feasible, compute correlation between EditBench pass@1 and SWE-Bench pass@1 for the overlapping model set. If not feasible, explicitly discuss why SWE-Bench was excluded from the comparison.

---

**W10. "First" claim scope (Minor).** The paper states "We are the first benchmark to include this combination of features for instructed code edits." This is a narrow first-claim ("combination of features") that is defensible but may be perceived as trivial (no prior work happens to include this exact feature set). The paper should consider rephrasing to focus on the substantive contribution (real-world grounding with multi-context integration) rather than the combinatorial novelty.

**Required action**: Rephrase to emphasize the substantive differentiation: "EditBench is the first code editing benchmark grounded entirely in real user workflows, combining natural language instructions with code context, highlighted regions, and cursor position to faithfully reproduce the IDE editing experience."

## Score
**Final Score: 7/10**

**Scoring rationale**: The score prioritizes research value and methodological soundness as primary dimensions, with novelty and reproducibility as supporting factors.

- **Research Value (8/10)**: EditBench addresses a genuine gap in the evaluation landscape. The real-world data collection methodology is a clear improvement over annotator-written and exercise-derived benchmarks. The benchmark has the potential to influence how code editing models are evaluated in both academia and industry. The 40-model evaluation provides immediate utility as a model ranking resource.

- **Novelty (7/10)**: The core idea — collecting instructed code edits from real IDE usage — is novel within the code editing benchmark literature. However, the approach builds directly on prior work in arena-style evaluation (Copilot Arena, Chatbot Arena) and real-world benchmark construction (SWE-Bench). The novelty lies in the specific combination of features (real instructions + multi-context signals + multilingual coverage), which is incremental but meaningful. External literature verification was not available in this run, so novelty conclusions are based on manuscript-internal evidence and should be treated as provisional pending manual literature review.

- **Soundness (6/10)**: The construction methodology is transparent and generally sound, but three weaknesses reduce confidence: (1) the 96% attrition rate from raw data to benchmark problems is not adequately analyzed, threatening external validity; (2) key experimental findings lack statistical rigor (no confidence intervals, marginal p-values, single-sample evaluation); (3) the language inconsistency (Portuguese vs. Polish) and underexplored cursor-position confusion effect suggest gaps in the analytical depth.

- **Reproducibility (8/10)**: The paper provides the VSCode extension, the leaderboard, and sufficient methodological detail to reproduce both the benchmark and the evaluation. The open-source release and the two-stage annotation review process are strong points. The main gap is the lack of prompt templates in the main text (deferred to Appendix D, which was truncated).

The benchmark is a solid contribution that will likely be used by the community. The main weaknesses are fixable through additional analysis (attrition audit, confidence intervals, cursor confusion analysis) and do not require fundamental redesign. The score reflects the current manuscript state; most weaknesses are addressable in a revision.

**Post-Revision Target**: [7.5, 8.5]/10 — achievable if the authors address W1 (attrition analysis), W2 (statistical rigor), W4 (cursor confusion), and W5 (translation bias), plus resolve the language inconsistency.