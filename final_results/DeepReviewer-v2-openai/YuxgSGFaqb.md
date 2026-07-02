## Summary
# Final Review Report

## Summary

This paper presents SWINGARENA, an adversarial evaluation framework for LLMs that models real-world CI-driven software development through paired submitter-reviewer agents. Unlike static benchmarks like HumanEval, MBPP, or SWE-Bench, SWINGARENA operationalizes full CI pipelines with dynamic role-switching between patch submitters and test-case-generating reviewers. The framework includes a Retrieval-Augmented Code Generation (RACG) module for handling long-context code retrieval across C++, Python, Rust, and Go, and a curated dataset of 2,300 GitHub issues (400 for evaluation, 100 per language). Experiments across proprietary models (GPT-4o, Claude-3.5, Gemini-2.0, DeepSeek-V3) reveal behavioral patterns: GPT-4o excels at aggressive patch generation (Win Rate >=0.90 as submitter) while DeepSeek and Gemini achieve higher CI pass rates (SPR up to 0.66), highlighting a trade-off between assertiveness and reliability. The authors identify that self-play win rates are uniformly high (0.91–1.00), which may partially reflect reviewer weakness rather than submitter strength — an important caveat for adversarial evaluation design.

**Overall Assessment:** The paper addresses a relevant and underexplored problem — interactive, CI-grounded evaluation of LLM code-generation capabilities. The adversarial submitter-reviewer protocol is the strongest contribution; the RACG module and dataset are supporting infrastructure. However, the novelty of RACG is limited (modest empirical gains, combination of existing techniques), the Win Rate metric needs more careful disentanglement from reviewer quality, and the data construction pipeline has selection biases that should be explicitly discussed. The paper is methodologically sound for a benchmark/system contribution but would benefit from stronger empirical validation of the adversarial protocol's discriminative power.

## Strengths
1. **Relevant problem framing.** The paper identifies a genuine gap in LLM code evaluation: existing benchmarks ignore CI-native, multi-agent, iterative workflows. The adversarial submitter–reviewer protocol is a well-motivated design that moves beyond simple unit-test pass/fail evaluation.

2. **Practical infrastructure contribution.** SWINGARENA provides a fully automated, containerized CI evaluation pipeline across four languages, with reproducible artifacts (pinned Docker images, scripts, prompts, JSON schemas). This lowers the barrier for future research on interactive code evaluation.

3. **Comprehensive multi-model analysis.** The paper evaluates four proprietary models and one open-source model across 16 matchup combinations, covering both self-play and cross-play scenarios. The analysis reveals non-trivial behavioral patterns (GPT-4o's aggressive patching vs. DeepSeek's reliability) that static benchmarks cannot capture.

4. **Honest self-assessment.** The paper acknowledges limitations of its RACG module (fixed Top-5 file retrieval bottleneck, reliance on existing components) and the caveat that Win Rate is adversarial and should be interpreted alongside CI pass rates. This transparency is commendable.

5. **Multi-language coverage.** Including C++, Python, Rust, and Go in the same CI-driven evaluation framework is a practical advance over Python-only benchmarks. The language-specific performance breakdown (Table 2) provides useful insights for model developers.

## Weaknesses
### W1. Win Rate confound with reviewer quality not adequately addressed (Major)

The paper correctly notes that "Win Rate is adversarial: higher values may also indicate weaker reviewer tests" and recommends interpreting Win Rate with SPR/RPR. However, no formal decomposition is provided. Claude self-play achieves Win Rate 1.00 with SPR only 0.62 — meaning ~38% of CI checks fail yet the reviewer never catches a flaw. This could reflect either genuine alignment or weak testing. The paper's claim of "strong internal alignment" is indistinguishable from reviewer weakness without additional diagnostics. **Impact:** Undermines confidence that the adversarial protocol provides discriminative signal beyond what SPR alone would give. **Fix:** Add a reviewer strictness metric (e.g., fraction of reviewer-generated tests that fail on the golden patch, or test rejection rate) and report it alongside Win Rate and SPR/RPR.

### W2. RACG contribution modest relative to its billing as a core contribution (Major)

RACG is listed as a core contribution (C2), yet ablation results show small gains: Best@3 improves by 0.04–0.09 absolute across languages, and simpler baselines like Top-20 retrieval achieve comparable results (Best@3 = 0.43 vs. 0.42–0.58). The paper itself describes RACG as "a strong baseline to support SwingArena rather than a standalone algorithmic contribution." This self-description conflicts with listing it as a top-level contribution. **Impact:** The paper would be stronger with two contributions (adversarial protocol + dataset) rather than three, with RACG repositioned as infrastructure. **Fix:** Either (a) demote RACG to a supporting component and reframe contributions, or (b) provide per-component ablation showing which RACG sub-modules drive gains, and demonstrate superiority over simpler baselines with significance tests.

### W3. Selection bias in data construction not sufficiently discussed (Major)

The pipeline filters by (a) high-star repositories (popularity bias), (b) CI-pass-only instances, and (c) LLM-as-a-Judge (Grok-3-beta) followed by expert filtering. The combined effect is a curated dataset that may not represent the full spectrum of real-world GitHub issues. The paper does not report drop rates at each filtering stage, making it impossible to assess how representative the final 400 instances are. **Impact:** Limits external validity and generalizability claims. **Fix:** Add a section reporting the number of instances removed at each filtering stage, with discussion of how selection biases may affect benchmark difficulty and model rankings.

### W4. Missing statistical significance and variance reporting (Major)

All metrics (Win Rate, SPR, RPR, Best@k) are reported as point estimates without confidence intervals, standard deviations, or significance tests. Given the relatively small sample sizes (100 per language, 400 total), observed differences (e.g., DeepSeek 0.59 vs. GPT-4o 0.57 in Best@3) may not be statistically reliable. **Impact:** Readers cannot assess the stability of model rankings. **Fix:** Report metrics with bootstrapped 95% confidence intervals or standard deviations across at least 3 evaluation seeds (when temperature > 0). For the primary evaluation (temperature=0), use bootstrapping over task samples.

### W5. Abstract lacks quantitative anchoring (Minor)

The abstract describes the framework and reports qualitative findings but contains no numerical results. For a benchmark/framework paper, including at least one key result (e.g., Win Rate range, SPR range) would significantly strengthen reader engagement and scientific credibility. **Fix:** Include 1–2 concrete quantitative findings in the abstract, e.g., "GPT-4o achieves win rates >=0.90 across all reviewers, while DeepSeek attains the highest CI pass rate (SPR=0.66)."

### W6. Related Work organized as list rather than structured comparison (Minor)

Sections 2.1–2.3 follow a paper-by-paper enumeration style rather than being organized around comparison axes (language coverage, CI integration, adversarial capacity, automation level). Readers cannot quickly see where SWINGARENA differs from each prior work on specific dimensions. **Fix:** Reorganize with a concise comparison table (covering SWE-Bench, CrossCodeEval, RepoBench, etc.) showing coverage across 4–5 axes, then discuss differences in prose.

### W7. Battle Protocol duplication (Minor)

The Battle Protocol definition appears nearly verbatim in two places (Section 3.2 and end of Section 3.3), suggesting an editing oversight. **Fix:** Remove the duplicate in Section 3.3 and replace with a forward-reference.

### W8. Conclusion too brief (Minor)

The conclusion is a single paragraph that restates rather than synthesizes. It lacks explicit limitations, concrete validated findings with evidence anchors, and actionable future directions. **Fix:** Expand to three paragraphs: (1) key findings, (2) bounded limitations, (3) prioritized future work.

### W9. Novelty/comparison claims deferred (Deferred)

Due to external literature retrieval being unavailable in this run, novelty assertions (e.g., "first" adversarial CI evaluation framework, positioning relative to SWE-Bench and extensions) could not be independently verified against the literature. **Status:** All novelty and comparative-strength claims in this review are manuscript-grounded only; external verification is deferred.

## Score
Final Score: 6.5/10

**Rationale:** The paper addresses a relevant and practically important problem — evaluating LLMs in CI-driven, multi-agent software workflows — and contributes a functional, reproducible evaluation infrastructure. The adversarial submitter–reviewer protocol (C1) and the multi-language CI-grounded dataset (C3) are the strongest contributions. However, three factors prevent a higher score:

1. **Novelty constraints.** The RACG module (C2) is presented as a core contribution but delivers modest empirical gains and is acknowledged by the authors as "a strong baseline" rather than a novel algorithm. The adversarial protocol itself, while well-motivated, builds on existing concepts (SWE-Bench, LLM-as-a-Judge, multi-agent evaluation) without introducing a fundamentally new evaluation paradigm — the main advance is operationalizing CI integration.

2. **Empirical validity concerns.** The Win Rate metric has a known confound with reviewer quality that is not adequately disentangled. Point estimates are reported without confidence intervals or significance tests, making it difficult to assess the stability of model rankings. Selection biases in data construction are acknowledged but not quantified.

3. **Writing and presentation gaps.** The abstract lacks quantitative results, related work is organized as a list rather than structured comparison, and the conclusion is too brief for a benchmark paper. These issues are individually minor but collectively reduce the paper's scholarly polish.

The paper represents a solid infrastructure contribution that will likely be useful to the community. With stronger empirical validation (significance testing, reviewer quality metrics, selection bias analysis) and reframed contributions, the score could reasonably reach the 7–7.5 range.