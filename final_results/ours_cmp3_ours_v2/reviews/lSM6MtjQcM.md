## Summary

AetherCode is a new benchmark of 456 competitive programming problems sourced from premier competitions (IOI, ICPC World Finals, ICPC regionals, NOI, USACO, CCPC), designed to evaluate LLM coding and reasoning abilities. The benchmark features expert-validated test cases constructed through a hybrid of automated generation and human curation, achieving 100% TPR/TNR on a collected solution set of over 30,000 submissions. The authors evaluate 17 LLMs and report that even the best model (o4-mini-high) achieves only 35.5% Pass@1.

## Strengths

1. **Novel problem sourcing from premier competitions.** AetherCode is the first benchmark to systematically collect problems from IOI, ICPC World Finals, ICPC regionals, NOI, USACO, and CCPC (Section 2.1). This fills a genuine gap — prior competition-level benchmarks rely on CodeForces, LeetCode, or AtCoder, which have different difficulty distributions and problem design constraints.

2. **Rigorous test case construction methodology.** The TPR/TNR evaluation framework (Section 2.3.1) is a principled departure from naive "more test cases = better" approaches. The hybrid pipeline combining automated G-V Agent generation (89.9% TNR) with 67 competitive programming experts (Codeforces ratings >2000) and an elite audit team of multi-gold ICPC medalists (Section 2.3.3) represents a serious investment in test suite quality that exceeds what most prior benchmarks document.

3. **Comprehensive model evaluation.** 17 models (11 reasoning, 6 non-reasoning) are evaluated with results broken down by difficulty tier, year, and 10 algorithmic categories (Tables 3, 4), providing a useful snapshot of the current landscape.

4. **Clean decontamination metadata.** Each problem is annotated with its contest date (Section 2.2), enabling researchers to filter by model training cutoff. Results are reported separately for 2024 and 2025 problems (Table 3).

5. **Qualitative error analysis.** The diagnosis of failure reasons (Section 3.3), including the finding that Claude models tend toward correct-but-inefficient solutions and that GLM-4.5 often uses the wrong programming language, provides actionable insights.

## Weaknesses

### Major

1. **The claimed LLM-human gap is asserted without a human baseline.** The abstract claims "a substantial gap between LLMs and elite human programmers" and the conclusion states "there remains a significant gap compared to top human experts," yet **no human performance numbers are reported on AetherCode**. The difficulty classification uses contest results (e.g., "Extreme" = no human solved in competition), but those results come from different formats (5-hour sessions, team structures for ICPC, pre-college students for IOI) that are not comparable to the LLM evaluation setup. The paper also never defines what "elite human" means in measurable terms. Without a controlled human baseline on the same benchmark under comparable conditions, this central claim is an assertion, not a finding. *(Relevant text: Abstract, lines 9-10; Conclusion, lines 267-268)*

2. **Data contamination risk is flagged but not substantively addressed.** 400 of 456 problems (88%) are from 2024 (Table 2). Most evaluated models (o4-mini-high, Gemini-2.5-Pro, DeepSeek-R1, Claude-4-Opus, GPT-4.1, etc.) were trained on data that likely includes 2024. IOI and ICPC problem statements are publicly available on contest websites. The paper annotates contest dates "for decontamination purposes" (Section 2.2) and criticizes other benchmarks for contamination (Section 4.2: "outdated data, posing a significant risk of data contamination"), but performs **no actual decontamination** — no memorization probes, no training data overlap analysis, no separate reporting excluding potentially contaminated problems. The 2025-only subset (56 problems) is reported in Table 3 but is too small for reliable conclusions. This does not invalidate the benchmark as a resource, but the evaluation results as presented are not fully interpretable. *(Relevant text: Table 2, Section 2.2 lines 94-95, Section 4.2 lines 261)*

### Minor

3. **Difficulty star rating (★★★) contradicts the paper's framing.** Table 1 rates AetherCode as ★★★ difficulty, while USACO, CodeContests, CodeELO, and LiveCodeBench Pro are all rated ★★★★. A reader looking at Table 1 would conclude AetherCode is *easier* than several benchmarks the paper criticizes for "insufficient difficulty" — the opposite of what the abstract ("higher difficulty") and introduction (Section 1, "Insufficient Difficulty and Scope") claim. While the empirical results (best model 35.5% Pass@1) demonstrate the benchmark is genuinely hard, this inconsistency damages the paper's presentation coherence. *(Relevant text: Table 1, Abstract line 9, Section 1 lines 17-21)*

4. **No statistical uncertainty reported.** Each model is evaluated 4 times per problem and averages are reported without confidence intervals, standard deviations, or significance tests (Section 3). With 456 binary-outcome problems and only 4 samples per model, the variance in Pass@1 estimates is non-trivial. The claim that top models form "an elite tier with a significant gap" (Section 3.1) is an impression from point estimates, not a statistically supported finding. The paper notes Pass@4 >> Pass@1 for top models, which itself implies high variance — yet the reported numbers are treated as stable. *(Relevant text: Section 3, lines 166; Section 3.1, lines 171-172)*

5. **The "100% TPR/TNR" claim is only on the collected solution set.** The paper is transparent about this (Section 2.3.1: "on our collected solution set"), and the elite audit (Section 2.3.3) partially mitigates the limitation. However, the paper does not report how many test cases were added or modified by the expert audit, nor how many failure modes the initial automated set missed. *(Relevant text: Section 2.3.1, line 124; Section 2.3.3, lines 156-161)*

### Trivial

6. **Pass@N computation method is not specified.** The paper reports Pass@1, Pass@2, Pass@4 but does not state whether the standard unbiased estimator (Chen et al., 2021) is used or if these are empirical averages. With only 4 samples, Pass@4 equals the empirical average, but the methodology should be stated.

7. **Test case statistics are minimal.** Only the average number of test cases (47.15) is reported; the median, min, max, and per-problem distribution would be informative.

## Nice-to-Haves

- A human baseline on a representative subset (50–100 problems solved by a few experts under controlled, time-limited conditions) would transform the LLM-human gap claim from assertion into evidence.
- A memorization probe (e.g., checking whether models can regurgitate known solutions from problem statements) would strengthen the contamination analysis.
- Reporting the number of test cases contributed by the expert audit stage (vs. automated generation) would clarify the test suite construction process and help readers assess the value added by the human effort.

## Removed Points

- **"Test case validation has circularity concerns" (from Harsh Critic Item 4)**: Removed because the paper is explicit that 100% TPR/TNR is "on our collected solution set" (line 124), and the elite audit stage (Section 2.3.3) explicitly addresses this concern by having experts write additional corner cases and incorrect solutions. The paper does not overclaim generalizability to unseen solutions.
- **Three-equal-categories inconsistency (from Section-by-Section notes)**: Removed because the text is actually consistent — it states there are four levels (Easy, Medium, Hard, Extreme) but the first three are roughly equal in size, with Extreme being a small special category (20 problems). Figure 2 confirms this distribution.
- **"Over 30,000 solutions vs. minimum implied ~11,400" (from Section-by-Section notes)**: Removed because this is not a meaningful issue — some problems naturally have more collected solutions than the minimum, and the paper is not required to justify every surplus solution.
- **Language specification concern (from "Missing Parts")**: Removed because the paper does specify that models were instructed to use C++ (Section 3.3, line 247: "it writes a Python program while being instructed to use C++"). The appendix is said to contain full details.
- **Expert team size for elite audit**: Removed because this is a minor detail that can be addressed in a footnote; it does not affect the paper's validity.

## Novel Insights

None beyond the paper's own contributions. The reviews surface structural concerns (missing human baseline, contamination) that the paper should address, but do not add new analytical findings beyond what the authors present.

## Suggestions

1. Provide a human baseline — even a small controlled study with a few experts solving a representative subset under comparable conditions would substantiate the LLM-human gap claim or allow the authors to temper it appropriately.
2. Conduct and report a contamination analysis: test for memorization (e.g., prompting models to regurgitate solutions from problem statements), and report results separately for problems whose contest dates demonstrably postdate each model's training cutoff.
3. Correct or explain the ★★★ difficulty rating in Table 1. If the rating reflects average difficulty across all problems (including Easy ones), clarify this. If it is a mistake, fix it.
4. Add confidence intervals or bootstrap estimates to the main results table or at minimum acknowledge the variance due to 4 samples per problem.
5. Specify the Pass@N computation methodology explicitly in the experimental setup.

## Score and Decision

**Round 1 bracket**: 4.5 – 6.0, based on calibration against comparable benchmarks.

**Calibration anchors used:**

| Anchor Paper | Avg Score | Round | Comparison to AetherCode |
|---|---|---|---|
| LiveCodeBench (chfJJYC3iL) | 6.25 | 1,2 | Most directly comparable: code reasoning benchmark. LiveCodeBench's strength is contamination-free evaluation; AetherCode has stronger test case methodology and premier-competition sourcing but weaker contamination handling and lacks a human baseline. |
| MHPP (TVFVx8TUbN) | 4.25 | 2 | Smaller benchmark (210 problems) with similar motivation (insufficient difficulty in existing benchmarks). AetherCode is larger, has better test case methodology, and broader sourcing — clearly stronger. |
| Tests-as-Instructions (sqciWyTm70) | 4.00 | 1 | Less comparable (TDD-focused, React-specific). AetherCode has broader scope and more rigorous construction. |
| Codev-Bench (c2C2NQKjZw) | 4.25 | 2 | Less comparable (code completion-focused, industry-oriented). AetherCode addresses a different evaluation niche. |

**Final score justification**: AetherCode fills a genuine gap in the code reasoning benchmark landscape through its premier-competition sourcing and expert-validated test case pipeline. The benchmark resource itself is valuable. However, the paper has two structural issues — an unsupported LLM-human gap claim and unaddressed contamination risk — alongside several presentation inconsistencies. Comparing against LiveCodeBench (6.25), which similarly constructs a competition-level benchmark but addresses contamination as its central feature, AetherCode is slightly weaker because its main limitations (contamination, unsupported central claim) are more consequential. It is clearly stronger than MHPP (4.25). The final score of 5.0 reflects a benchmark paper with genuine contributions that needs to address significant gaps in its evidence and framing before acceptance.

My FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>