## Summary

This paper introduces AetherCode, a new benchmark for evaluating LLMs on competitive programming problems sourced exclusively from premier competitions (IOI, ICPC, and related contests). The benchmark addresses two perceived limitations of existing code reasoning benchmarks: insufficient problem difficulty/scope and evaluation bias from low-quality test cases. AetherCode provides 456 problems (2024–2025) with test cases constructed through a hybrid automated-expert pipeline, achieving 100% TPR and 100% TNR on a collected solution set of over 30,000 submissions. The evaluation of 17 models reveals a significant performance gap between top reasoning models and others, and between reasoning and non-reasoning models overall.

## Strengths

- **Timely and well-motivated benchmark.** The paper correctly identifies that existing benchmarks (HumanEval, MBPP, LiveCodeBench) are becoming saturated, and that test case quality is a genuine concern. The focus on premier competitions (IOI, ICPC) rather than online judges like CodeForces/LeetCode is a meaningful differentiator that increases problem difficulty and diversity.

- **Rigorous test case construction methodology.** The hybrid approach combining automated generation (G-V Agent) with expert annotation by 67 competitive programming experts (many with Codeforces rating >2000) and an elite audit team (ICPC gold medalists) is thorough. The use of TPR/TNR as direct quality metrics, rather than raw test case count, is a principled improvement over prior work.

- **Comprehensive evaluation with clear discrimination.** The evaluation covers 17 models across reasoning and non-reasoning categories, with results showing strong separation between model tiers. The analysis of performance across 10 algorithmic categories and the failure diagnosis (Wrong Answer vs. TLE vs. Runtime Error) provide useful insights for the community.

- **High-quality expert involvement.** The recruitment of 67 experts and an elite audit team with multiple ICPC gold medals and problem-setting experience lends credibility to the test case quality and the difficulty annotations.

## Weaknesses

### Fatal
None.

### Major

- **Overclaim of "first" in problem sourcing.** The paper states that AetherCode is "the first benchmark to systematically collect latest problems from premier programming competitions worldwide." However, existing benchmarks such as USACO Bench, LLM-Pros, OJBench, and ICPCEval also source problems from premier competitions (USACO, NOI, ICPC). While AetherCode may be broader and more recent, the claim of being first is inaccurate and should be qualified (e.g., "first to comprehensively collect from a wide range of premier competitions with recent data").

- **No human baseline performance reported.** The paper repeatedly claims that LLMs still lag behind elite human competitors, but it does not provide any human performance data on the AetherCode benchmark itself. Without human baselines (e.g., contestant solve rates or expert performance on the same problems), the claim of a "significant gap" is not directly supported by the paper's own evaluation. The difficulty classification is based on human contest data, but actual human solve rates on the benchmark are not reported.

- **Test case quality claim is limited to the collected solution set.** The paper reports 100% TPR and 100% TNR, but this is achieved on a specific set of collected solutions (at least 5 correct, 20 incorrect per problem). The paper acknowledges this limitation for problems with fewer than 50 incorrect solutions and adds an expert audit, but the headline claim of "100% TPR and 100% TNR" could be misinterpreted as exhaustive coverage. The solution set may not capture all possible failure modes, especially for harder problems.

### Minor

- **Difficulty classification methodology is somewhat subjective.** The paper ranks problems within the same contest by number of solvers, but uses expert evaluation for cross-contest ranking and for contests without leaderboards. This introduces subjectivity, and the final split into Easy/Medium/Hard/Extreme is described as "roughly equal" (except Extreme), which is not a precise criterion.

- **Model naming inconsistencies.** Table 3 contains apparent typos: "Ssed-1.6-Thinking-0715" (likely Seed), "Claude-4.5-Sonnet-thinking" (Claude 4.5 Sonnet is not a standard model name as of the paper's date), and "nothingking" instead of "nothinking" in the last row. These errors reduce confidence in the carefulness of the evaluation.

- **Decontamination process is mentioned but not described.** The paper states that contest dates are collected "for decontamination purposes," but no decontamination procedure is described. Given that many of these problems may appear in training data, this is an important omission.

### Trivial

- Minor typos: "The majority of the problem statements was originally in PDF format" (subject-verb agreement).
- The paper uses "G-V Agent" without defining the acronym at first use (defined later in Section 2.3.2).

## Nice-to-Haves

- A human baseline (e.g., expert solve rates or contestant performance on the same problems) would significantly strengthen the claim that LLMs lag behind top humans.
- A discussion of the computational cost of evaluation (e.g., API costs, time) would be useful for practitioners.
- The paper could benefit from a more detailed analysis of why certain categories (e.g., Tree) have very low scores—is it due to inherent difficulty or small sample size?

## Novel Insights

None beyond the paper's own contributions. The key novel elements are the benchmark itself (problem selection from premier competitions) and the test case quality framework (TPR/TNR metrics with hybrid generation). The evaluation results confirm expected trends (reasoning models outperform non-reasoning, top models show larger gains from multiple samples) but do not reveal unexpected phenomena.

## Suggestions

- **Qualify the "first" claim** to accurately reflect prior work (e.g., "first to comprehensively collect from a wide range of premier competitions with recent data").
- **Report human baseline performance** on the benchmark, even if only approximate (e.g., contestant solve rates from the original competitions).
- **Describe the decontamination procedure** used to ensure that problems are not in model training data.
- **Correct model names** in Table 3 and ensure consistency throughout the paper.
- **Release the benchmark publicly** (code, data, and leaderboard) to maximize community impact.

## Score and Decision

The paper presents a well-motivated and carefully constructed benchmark that addresses genuine limitations in existing code reasoning evaluations. The test case quality methodology is a clear improvement over prior work, and the evaluation provides useful discrimination across models. The weaknesses (overclaim of "first," lack of human baseline, and minor errors) are not fatal and can be addressed. The benchmark is likely to be a valuable resource for the community.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>