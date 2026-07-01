## Summary

The paper introduces InnoGym, a benchmark and framework for evaluating the innovation potential of AI agents using two complementary metrics: performance gain (G, improvement over best-known solutions) and novelty (N, methodological dissimilarity from prior solutions). The benchmark includes 18 curated "improvable tasks" from real-world engineering and scientific domains, standardized through multi-stage filtering and a unified execution environment (iGym). Experiments on three agent frameworks show that current agents uniformly fail to surpass human state-of-the-art on these tasks, and that novelty without robustness does not translate to meaningful performance gains.

## Strengths

- **Principled formalization of innovation.** The task definition as a quadruple (P, S, V, D) and the clean decomposition into performance gain G and novelty N (Section 2.2) provide a clear conceptual vocabulary for an underexplored dimension of agent evaluation. The taxonomy of solved, improvable, and exploratory tasks (Section 2.3) is well-motivated and grounded.

- **Systematic dataset curation pipeline.** The two-stage filtering process from 197 to 18 tasks (Sections 3.1–3.2), with attention to resource availability, evaluator executability and correctness, score normalization (Pearson ≥ 0.9, Kendall-τ ≥ 0.8), and domain balance, is more rigorous than what typical benchmark papers provide.

- **Useful controlled analysis experiments.** The experiments on Circle Packing (Section 4.3) showing that N decreases with execution time and increases with sampling temperature, and the G-N trajectory in Figure 5, provide behavioral validation that the metrics respond sensibly to known factors.

## Weaknesses

### Fatal
None.

### Major

1. **The novelty metric—the paper's core distinctive contribution—lacks direct validation in the main text.** The novelty score N(s) is the feature that differentiates InnoGym from every benchmark in Table 1. Yet its implementation (Codex extraction → GPT-5 rating along six rubric dimensions on a 0–4 scale) is presented without any ground-truth validation in the main text. No human expert judgments are collected to establish what "methodological dissimilarity" means for these tasks. No inter-rater reliability is reported. No correlation with an external measure (e.g., code embedding distance, human classification) is shown. The paper references Appendix F for "behavior and reliability of D," but the main text presents only indirect sanity checks (e.g., N decreases with time, increases with temperature—Section 4.3) that could emerge from any noisy measure correlated with randomness. For a benchmark whose entire value proposition over prior work is evaluating novelty, the main text must provide sufficient evidence that N(s) captures *methodological* novelty and not just output diversity or noise. *Verification: Section 4.1 and 4.3, Table 2.*

2. **Best-of-3 reporting without variance estimates.** Section 4.1 states: "each configuration is run three times... We report the best score over these three runs." This inflates values, masks variance, and makes cross-framework comparisons unreliable. With n=3 and best-score selection, the observed differences between frameworks (MLAB avg Gain -24.32 vs CODEACT -41.58 vs AIDE -42.68) could reflect noise rather than genuine superiority. No confidence intervals, significance tests, or per-run breakdowns are provided. Many entries are "/" (no valid submission across all 3 runs), making comparisons across tasks sparse. *Verification: Section 4.1, final paragraph; Table 2.*

3. **Uniformly negative performance gains prevent the benchmark from demonstrating its distinguishing feature.** Table 2 shows every agent on every task has G(s) < 0. The paper's motivating scenario—"two agents may arrive at the same correct answer while following entirely different approaches" (Section 1)—never materializes. The benchmark exists to discriminate innovation when performance is comparable, but no agent achieves adequate performance. This means the framework's core value proposition (distinguishing two agents with comparable G but different N) is never validated empirically. While hard tasks that stump current systems are valuable, the paper's claims about evaluating "innovation potential" are undersupported when no positive-G case exists and no controlled experiment demonstrates the framework operating in its intended regime. *Verification: Table 2; Section 1, paragraph 1; Section 2.2, innovation taxonomy.*

### Minor

4. **Only 10 of 18 benchmark tasks are evaluated** (Section 4.1, paragraph 2), with the justification "more tractable under our computing and engineering constraints." The 8 excluded tasks are not analyzed, so it is unclear what coverage (domain, difficulty, resource profile) the evaluated subset preserves and whether selection bias affects the conclusions.

5. **No discussion of the novelty metric's limitations.** The paper does not address known concerns with LLM-as-judge approaches: sensitivity to prompt phrasing, potential contamination (GPT-5/Codex may share training data with agent outputs), temporal instability of API models, and the cost/scalability of the two-LLM pipeline. A dedicated limitations section would significantly strengthen the paper.

6. **No ablation of the novelty metric pipeline.** The paper presents D as general but only tests one complex instantiation (Codex extraction + GPT-5 comparison). The necessity of the two-stage pipeline is not examined—would embedding-based dissimilarity (e.g., code-BERT) produce similar results at lower cost? This makes it difficult to assess how much of the metric's behavior comes from the method vs. the LLM judges.

7. **Claims about MLAB leadership are not robust.** The paper states MLAB "leads in both Performance Gain and Novelty" (Section 4.2), but the data is sparse: on BEETL(Sleep), only MLAB and AIDE have scores; on BEETL(MI), only MLAB; on tasks where multiple agents have scores (OAG: -28.59, -30.38, -29.87; CirclePacking: -0.43, -0.008, -0.25), differences are small or CODEACT wins. The average Gain is dominated by different task subsets per framework due to "/" entries.

### Trivial
None.

## Nice-to-Haves

- Validate the novelty metric against human expert judgments on at least 5–10 tasks (20–30 solution pairs), showing correlation between LLM-as-judge scores and domain-expert ratings of methodological dissimilarity.
- Report mean ± standard deviation across runs (or all individual run data) instead of best-of-3.
- Construct a controlled experiment where two solutions have comparable performance but known methodological differences (e.g., gradient-based optimizer vs. genetic algorithm on CirclePacking) to directly validate that N distinguishes methods while G treats them as comparable.
- Distinguish between "agent failed to produce any valid submission" and "not evaluated" in Table 2's "/" entries.

## Removed Points

The following points from the input review were removed with justification:

- **"Novelty metric issue is fatal/structural"** — The paper references Appendix F for reliability analysis (which exists in the original submission). The framework is agnostic to the specific D instantiation (Section 2.1 states "D can be any task-appropriate dissimilarity function"). Downgraded from fatal to Major.
- **"The six rubric dimensions are not named or motivated"** — The dimensions are described in Appendix H.2 (referenced in Section 4.1). The reviewer frames this as a main-text gap rather than a missing appendix complaint; the main text does adequately describe the pipeline and defers details to the appendix, which is standard practice. Removed.
- **"Table 2 formatting obscures information"** — A formatting/style nitpick. Removed per hard rules.
- **"Introduction oversells the contribution"** — Generic criticism. The InnovatorBench comparison resolves the concern (Table 1 shows Eval Novelty: ✗). Removed.
- **"The taxonomy is never operationalized"** — The taxonomy is conceptual framing; requiring it to be operationalized for every result entry is scope creep. Removed.
- **"Novelty scores don't provide actionable insight beyond performance"** — Partially redundant with weakness #3. Removed to avoid duplication.

## Novel Insights

The input review does not contribute genuinely novel observations beyond the paper's own contributions. The core tension it identifies—that a novelty-measuring benchmark must validate its novelty metric against human judgment—is a standard methodological expectation, not a novel insight.

## Suggestions

1. Move the novelty metric reliability analysis (currently Appendix F) into the main text, including at minimum: human-expert correlation on a subset of tasks, inter-rater reliability between two LLM calls, and a comparison against a simple embedding-based baseline.
2. Report per-run results (mean ± std) rather than best-of-3 to support meaningful cross-framework comparisons.
3. Add a limitations paragraph discussing LLM-as-judge concerns (contamination, prompt sensitivity, cost, temporal stability).
4. Either evaluate all 18 tasks or provide a principled analysis of what the 10-task subset preserves in terms of domain and difficulty coverage.

## Score and Decision

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>