## Summary

The paper introduces SWINGARENA, an adversarial evaluation framework for LLMs that simulates real-world software development through a submitter-reviewer interaction protocol. It pairs LLMs as *submitters* (generating patches) and *reviewers* (creating test cases), with verification via real CI pipelines across C++, Python, Rust, and Go. The framework includes a Retrieval-Augmented Code Generation (RACG) module for long-context code understanding and a curated dataset of 2,300 GitHub issues with 400 evaluation instances.

## Strengths

- **Adversarial evaluation protocol is conceptually novel.** The submitter-reviewer role-switching design with CI feedback goes beyond static benchmark evaluations and captures an important dimension of real-world software collaboration that prior benchmarks like SWE-Bench do not model.
- **Multi-language coverage is a genuine practical contribution.** Covering C++, Python, Rust, and Go with curated CI-grounded instances (100 per language) addresses a clear gap in existing benchmarks that are predominantly Python-only.
- **Thorough evaluation across multiple proprietary models.** The paper evaluates GPT-4o, Claude-3.5, Gemini-2.0, and DeepSeek-V3 in both self-play and cross-play configurations, revealing behavioral differences (e.g., GPT-4o's aggressive patching vs. DeepSeek's reliability) that a single-metric benchmark would miss.
- **Ablation studies on RACG and retrieval granularity are informative.** Table 3 and Table 6 provide concrete evidence for the value of chunk-level retrieval over BM25 and quantify the impact of the RACG module.

## Weaknesses

### Fatal
None.

### Major

- **Duplicated "Battle Protocol" text appears twice in the paper.** The protocol description in Section 3.2 is repeated almost verbatim at the end of Section 3.3, indicating a significant copy-paste error that should have been caught during preparation. This undermines confidence in the overall care with which the paper was assembled.

- **The win rate metric is confounded and hard to interpret.** High win rates (0.89–1.00) in Table 1 could reflect strong submitters, weak reviewers, or easy tasks. The paper acknowledges this ("higher values may also indicate weaker reviewer tests") but does not provide a disentangled analysis. Without a controlled baseline (e.g., random reviewer or fixed human-written tests), the adversarial win rate alone is not a reliable measure of model capability.

- **No direct comparison with existing benchmarks.** The paper positions SWINGARENA as addressing blind spots in SWE-Bench and others, but does not evaluate the same models on SWE-Bench or HumanEval to demonstrate what new or different insights SWINGARENA surfaces. A comparative analysis is essential to establish the framework's added value over the status quo.

- **RACG contribution is described as "not a standalone algorithmic contribution" yet consumes substantial space and is featured as a main contribution.** The paper states RACG is "positioned as a strong baseline to support SwingArena rather than a standalone algorithmic contribution," but then devotes an entire subsection (3.3) and ablation experiments to it. This creates a mismatch between the stated scope and the actual emphasis.

- **No confidence intervals or statistical significance reported for any results.** Tables 1–3 and Figure 3 lack error bars, making it impossible to assess whether observed differences (e.g., Best@3 of 0.59 vs. 0.57) are meaningful or within noise.

- **Open-source model results are referenced (Table 4) but not shown in the provided paper.** The main text mentions "Additional results on open-source models are summarized in Table 4" but the table is absent from the content provided, making the evaluation incomplete.

### Minor

- **The ablation study (Table 3) uses Qwen2.5-Coder-7B-Instruct, a much smaller model than the proprietary ones in the main evaluation.** RACG gains may not generalize to larger models with larger context windows.
- **The paper claims "over 400 high-quality real-world GitHub issues" but uses exactly 400 evaluation instances.** This is a small discrepancy but the framing as "over 400" is imprecise.
- **The "Best@k" analysis for reviewers in Figure 3 is unclear:** what constitutes "success" for a reviewer test (failing the submitter patch while passing the golden patch) is a joint condition that conflates two sources of variance.
- **RACG gains in Table 3 are modest in several cases** (e.g., Python Best@3 improves from 0.44 to 0.46, a 2pp gain that may not be practically significant).

### Trivial
None.

## Nice-to-Haves

- A direct comparison between SWINGARENA scores and SWE-Bench scores for the same models to validate that the adversarial protocol surfaces genuinely different failure modes.
- A breakdown of win rates by whether the reviewer test actually revealed a genuine bug (vs. spurious failure).
- Analysis of how the number of CI checks per repository correlates with pass rates.

## Novel Insights

The paper's core insight—that pairing LLMs as adversarial submitters and reviewers in a CI-grounded loop reveals trade-offs between aggressive patching and reliability that static benchmarks cannot capture—is genuinely interesting. The finding that GPT-4o produces high win rates but lower CI pass rates, while DeepSeek yields lower win rates but higher CI stability, suggests that model selection for software engineering tasks involves a nuanced performance profile that goes beyond pass@k. This insight could inform practical deployment decisions.

Beyond the paper's own contributions, the observation that "prompts are much shorter than repository context (code dominates the token budget)" (Section 4.4) highlights a practical challenge for long-context evaluation that is worth deeper investigation.

## Suggestions

1. Remove the duplicated "Battle Protocol" text and ensure a single, clean presentation.
2. Add a comparative evaluation of the same models on SWE-Bench (or HumanEval) to demonstrate what novel signal SWINGARENA provides.
3. Report confidence intervals or bootstrap estimates for all metrics, especially in Tables 1–3.
4. Include the open-source results (Table 4) in the main paper rather than referencing an absent table.
5. Disentangle the win rate metric by reporting submitter-vs-reviewer success rates separately with controlled baselines.
6. Clarify how the RACG module's token-budget-aware packing interacts with the evaluation—are all models given the same token budget?

## Score and Decision

**Score:** 4.5

The paper presents a genuinely novel evaluation framework with practical multi-language coverage and reveals interesting behavioral differences across models. However, the duplicated protocol text, the absence of comparison with existing benchmarks, the lack of statistical rigor, and the confounded primary metric are substantial issues that prevent acceptance at a top venue in its current form. The core idea has merit, but the execution needs significant refinement.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>