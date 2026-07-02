## Summary
# Final Review Report

## Summary

This paper introduces AetherCode, a new benchmark for evaluating LLMs on competitive programming tasks. The benchmark contains 456 problems sourced from premier programming competitions (IOI, ICPC, NOI, USACO, CCPC) from 2024-2025, with a focus on higher difficulty and broader algorithmic scope than existing benchmarks. A key methodological contribution is the test case construction pipeline, which combines automated Generator-Validator agent systems with human expert annotation by 67 competitive programmers, achieving 100% True Positive Rate (TPR) and 100% True Negative Rate (TNR) on a collected solution set of over 30,000 submissions. The evaluation of 17 models (11 reasoning, 6 non-reasoning) shows that even the best model (o4-mini-high) achieves only 35.5% Pass@1, revealing a substantial gap between current LLMs and elite human competitors. The benchmark provides fine-grained analysis across difficulty levels, algorithmic categories, and error types, demonstrating high discriminative power.

## Strengths
**1. Genuine gap in benchmark difficulty addressed.** The paper correctly identifies that existing benchmarks (HumanEval, MBPP, LiveCodeBench) suffer from ceiling effects for state-of-the-art LLMs and may overstate coding proficiency. Sourcing problems from premier competitions (IOI, ICPC) that require multi-step algorithmic reasoning and complete program implementation (not just single-function calls) fills a real need in the evaluation ecosystem. The inclusion of an "Extreme" difficulty tier (problems with zero human solvers) is a thoughtful design choice for measuring upper-bound capability.

**2. Rigorous test case construction methodology.** The hybrid G-V Agent + expert annotation approach for test case generation is well-conceived. The conceptual framework of treating a test suite as a binary classifier (TPR for correctness, TNR for comprehensiveness) is a principled departure from the quantity-focused evaluation in prior benchmarks. The involvement of 67 competitive programming experts (many with Codeforces ratings >2000) and an elite review team with multiple ICPC gold medals provides strong quality assurance for test case correctness.

**3. Comprehensive model evaluation.** The paper evaluates 17 models including both reasoning and non-reasoning variants across multiple families (OpenAI, DeepSeek, Qwen, Gemini, Claude, GLM), providing a broad snapshot of the current landscape. The multi-dimensional analysis (difficulty tiers, algorithmic categories, error types, Pass@N) gives richer insight than simple leaderboard reporting. The finding that even the best model achieves only 35.5% Pass@1 is a meaningful result that quantifies the gap between LLMs and elite human programmers.

**4. Transparent benchmark release.** The paper provides detailed metadata (contest dates, organizers, competition scope) and includes decontamination considerations, supporting reproducibility and longitudinal tracking of model progress. The open-source release with self-contained test cases addresses compliance risks associated with CodeForces-based evaluation approaches.

## Weaknesses
### W1. Missing statistical rigor in model evaluation (Major)
**Location:** Page 1 - Section 3 Evaluation, Section 3.1 Main Results, Tables 3 and 4

The paper reports Pass@1, Pass@2, Pass@4 point estimates from 4 runs per model per problem, but provides no variance measures, confidence intervals, or statistical significance tests. This is a critical flaw because:

- Many comparisons central to the paper's claims (e.g., o4-mini-high 35.5% vs. Gemini-2.5-Pro 32.7% for Pass@1) rely on small absolute differences that may not be statistically significant given only 4 samples per problem.
- Subcategory analyses (Table 4) have very small sample sizes (Tree: 24 problems, Geo: 36 problems). A 2-3 problem difference between models translates to ~8-12 percentage points, meaning the reported ranking within small categories is highly uncertain.
- The paper's conclusion that AetherCode provides "high degree of discrimination" is partially supported by the large absolute spread between top and bottom models, but the fine-grained claims about specific model rankings are not statistically grounded.

**Required action:** Report standard deviations or 95% confidence intervals alongside all point estimates. Add statistical significance tests (e.g., bootstrap or McNemar's test) for key pairwise model comparisons. Specify whether the 4 runs used independent random seeds.

### W2. Evaluation circularity in 100% TPR/TNR claim (Major)
**Location:** Page 1 - Section 2.3.1 Test Case Quality Assessment, Section 2.3.3 Expert Annotation

The paper claims "100% TPR and 100% TNR on our collected solution set" as a key achievement, but this metric is evaluated on the same solution set that was used to guide test case construction. The G-V Agent system is tuned using these solutions, and the expert annotators are explicitly instructed to "construct targeted test cases specifically designed to fail the various incorrect solutions we had collected." The elite review team further "writes various incorrect and inefficient solutions to verify the comprehensiveness" — meaning the solution set itself is iteratively expanded during construction.

This creates a circular evaluation: the test cases are designed to reject the collected incorrect solutions, so achieving 100% TNR is expected rather than surprising. Without held-out validation on solutions not used during construction, the 100% claim lacks external validity.

**Required action:** Reserve a held-out test set of solutions (e.g., 20%) before any test case construction begins. Report TPR/TNR on this held-out set separately from the development set. If 100% is still achieved, the claim becomes much stronger. If not, report the actual held-out performance and discuss remaining gaps.

### W3. "First benchmark" claim overreach (Major)
**Location:** Page 1 - Introduction (line 18), Page 1 - Section 4.2 Code Reasoning Benchmarks (line 167)

The paper claims AetherCode is "the first benchmark to systematically collect latest problems from premier programming competitions worldwide." However, the paper's own related work (Section 4.2) cites multiple prior benchmarks that collect competition problems: USACO Bench (Shi et al., 2024), LLM-Pros (Hossain et al., 2025), OJBench (Wang et al., ), and ICPCEval (Xu et al., 2025). While AetherCode is indeed larger, more recent, and broader in scope (both OI and ICPC), the "first" claim is overreaching. This is a defensive writing issue: the paper's genuine contributions (comprehensiveness, recency, dual-series coverage, rigorous test cases) are sufficient without needing an unfalsifiable first-of-its-kind label. Reviewers familiar with the literature may view this as an overstatement that undermines credibility.

**Required action:** Replace "first benchmark" with bounded comparative phrasing, e.g., "most comprehensive and up-to-date benchmark of premier competition problems, spanning both OI and ICPC series with problems from 2024-2025."

### W4. Lack of quantitative calibration for the difficulty gap claim (Major)
**Location:** Page 1 - Introduction Paragraph 2 (lines 12-13), Page 1 - Abstract

The paper's central thesis is that existing benchmarks overstate LLM proficiency because they are too easy. However, the paper never directly compares model performance on existing benchmarks vs. AetherCode to quantify this overstatement. The argument for "insufficient difficulty" is supported only by qualitative reasoning about benchmark design (LeetCode is easier, CodeForces has limited problem scope) rather than empirical comparison. Adding a quantitative comparison — e.g., "GPT-4o achieves 85.7% on HumanEval vs. 4.4% on AetherCode, suggesting that prior benchmarks systematically underestimate the challenge of competition-level programming" — would substantially strengthen the motivation.

**Required action:** Add a direct cross-benchmark comparison table showing Pass@1 of representative models on HumanEval/MBPP/LiveCodeBench vs. AetherCode, using consistent evaluation settings.

### W5. Inconsistent difficulty classification (Moderate)
**Location:** Page 1 - Section 2.2 Difficulty Segmentation (lines 55-57)

The difficulty classification methodology is described inconsistently. The paragraph states both "problems were divided into four levels of difficulty" and "we divide the dataset into three roughly equal categories: Easy, Medium, and Hard" (with Extreme as a separate category). The exact criteria for each level are not specified (e.g., what solve rate threshold separates Easy from Medium?). Figure 2 shows the categories are not "roughly equal" — Easy (159) is 20% larger than Hard (132). The paper mentions ranking by participant solve rates "within the same contest" and expert evaluation "across contests," but does not provide the algorithmic rule used for the final assignment.

**Required action:** Specify explicit thresholds (e.g., Easy: >50% human solve rate, Medium: 20-50%, Hard: <20%, Extreme: 0%) or provide the algorithmic decision rule. Clarify whether the classification is 3-tier or 4-tier and reconcile with Figure 2.

### W6. High-level category imbalance undermines per-category analysis (Moderate)
**Location:** Page 1 - Section 3.2 Performance Across Algorithms, Table 4, Figure 2

The 10 major algorithmic categories exhibit severe class imbalance (Basic: 225 problems, Tree: 24, Geo: 36). Per-category Pass@1 scores for small categories have wide confidence intervals (approximately ±10-15 percentage points for N<30), making the reported rankings within those categories unreliable. The paper acknowledges this in passing ("individual categories may happen to be particularly difficult") but does not quantify the uncertainty. The 144 sub-categories (Appendix B) average ~3 problems each, making per-tag evaluation essentially meaningless.

**Required action:** Report category-level confidence intervals in Table 4. Consider merging small categories (Tree, Geo, Graph) into a "Structural Problems" super-category for more reliable per-domain analysis. Clarify that the 144 sub-categories are for metadata tagging only, not for statistical evaluation.

### W7. Shallow failure analysis (Moderate)
**Location:** Page 1 - Section 3.3 Diagnosis of Failure Reasons (lines 157-161)

The failure analysis reports approximate percentages (70-80%) without citing specific data, uses generic error categories that apply equally to human programmers, and does not identify LLM-specific failure patterns. The finding about GLM-4.5 using wrong programming languages is interesting but presented as an anecdote. The qualitative analysis of o4-mini-high failures does not link error types to problem categories (e.g., do geometric problems cause more wrong answers? Do DP problems cause more TLE?). This weakens the paper's contribution to understanding LLM code reasoning limitations.

**Required action:** Move the error-type distribution table (Appendix E Table 8) to the main text. Provide per-category error breakdowns to link with Table 4. Expand the analysis of model self-awareness (declining to answer) as this is a novel and interesting finding.

### W8. Conclusion lacks quantitative impact (Minor)
**Location:** Page 1 - Section 5 Conclusion (lines 168-170)

The conclusion uses vague phrasing ("only a small fraction of problems") instead of reporting the concrete results that distinguish the paper (35.5% best Pass@1, 3.8% on Extreme). It also does not provide human baseline performance, so the claimed "significant gap compared to top human experts" remains an assertion without quantitative evidence.

**Required action:** Include specific numbers in the conclusion. Add human performance baselines if available from competition results.

### W9. Related work is descriptive rather than comparative (Minor)
**Location:** Page 1 - Section 4.1 Code Benchmarks (line 165)

Section 4.1 reads as a flat enumerated list of benchmarks without explicit comparison to AetherCode. Each paragraph should follow: category scope -> representative methods -> why this category is insufficient for AetherCode's goal -> how AetherCode fills the gap.

**Required action:** Restructure each related-work paragraph as a comparison, not a list. Clearly state how AetherCode differs from each category.

### W10. Excessive descriptive detail in problem collection (Minor)
**Location:** Page 1 - Section 2.1 Problem Collection (lines 40-46)

The paper devotes substantial space to describing the format of OI and ICPC competitions (how many players per team, how many problems, how many regions) that is not relevant to benchmark construction. This space could be better used for problem selection statistics, coverage analysis, or decontamination procedures.

**Required action:** Condense to 1-2 sentences. Move detailed competition format descriptions to an appendix if needed.

## Score
**Final Score: 6/10**

**Rationale:** This score reflects a balanced assessment of the paper's strengths and weaknesses. The benchmark addresses a genuine need in the LLM evaluation ecosystem, and the test case construction methodology is principled. The comprehensive evaluation of 17 models provides useful empirical data. However, the paper has three significant weaknesses that prevent a higher score: (1) the absence of statistical rigor (no confidence intervals, no significance tests) undermines the reliability of reported rankings and model comparisons; (2) the key "100% TPR/TNR" claim suffers from evaluation circularity, as the test cases are evaluated on the same solution set that guided their construction; and (3) several novelty claims ("first benchmark") are overreaching and need qualification. These weaknesses are fixable in revision (adding statistical reporting, held-out validation, and more precise claims), but in their current form they materially reduce confidence in the paper's core empirical contributions.