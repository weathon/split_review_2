## Summary

The paper introduces AetherCode, a competitive programming benchmark comprising 456 problems sourced from premier competitions (IOI, ICPC, NOI, USACO, CCPC) with test cases constructed through a hybrid of automated generation (G-V Agent) and expert annotation by 67 competitive programming experts. The benchmark achieves 100% TPR and 100% TNR against a collected corpus of 30,000+ submissions, and evaluation of 17 LLMs reveals that even top models solve only ~35% of problems (Pass@1), with reasoning models substantially outperforming non-reasoning ones.

## Strengths

- **Genuinely superior problem sources and difficulty.** Sourcing from IOI, ICPC, NOI, USACO, and CCPC (rather than online judges like LeetCode/CodeForces) is a meaningful improvement. The benchmark discriminates well across models: o4-mini-high at 35.5% Pass@1, while GPT-4o achieves only 4.4%, confirming that the problems are challenging enough to expose real capability gaps rather than saturating.

- **Rigorous test case methodology.** The framework of treating test suites as binary classifiers evaluated via TPR/TNR against 30,000+ collected submissions is a genuinely valuable methodological contribution that surpasses naive random mutation or small handwritten test sets. The combination of automated generation (89.9% TNR) with expert curation to reach 100%/100% provides a replicable and defensible standard. This directly addresses a well-documented weakness in existing benchmarks (e.g., constraint-violating test cases in CodeContests).

- **Comprehensive categorization with expert involvement.** The hierarchical taxonomy (10 major, 144 sub-categories) combined with human-annotated difficulty levels and contest metadata enables fine-grained analysis, as demonstrated by the per-category performance breakdown in Table 4 showing that models struggle differentially across algorithmic domains (e.g., computational geometry vs. basic algorithms).

- **Practical benchmark design.** The focus on recent problems (2024–2025) mitigates data contamination risk, the open-source self-contained test suite avoids the compliance and rate-limiting issues of relying on CodeForces judging services, and the plan for versioned updates supports longitudinal tracking.

## Weaknesses

### Fatal

None.

### Major

- **Small problem set relative to claimed scope.** At 456 problems with only 20 "Extreme" problems and as few as 20–26 problems in some categories (Strings, Trees), the benchmark may lack sufficient statistical power for fine-grained conclusions. The "Extreme" tier (20 problems) yields near-zero scores across all models, providing essentially no discriminating signal. For a benchmark claiming to be "the first to comprehensively collect" from premier competitions, the coverage is modest.

- **No contamination analysis despite high-risk sources.** Problems from IOI, ICPC, NOI, and USACO are widely discussed in competitive programming communities, editorials are published post-contest, and solutions circulate freely. The paper does not analyze whether current LLMs may have seen these problems or their solutions during training. The 2024–2025 recency helps but does not eliminate risk, especially for widely publicized events like ICPC World Finals. This is a critical gap for a benchmark intended to measure reasoning rather than memorization.

- **ICPC team-based problems evaluated individually.** ICPC problems are designed for teams of 3 with one computer, potentially incorporating problem design assumptions about collaborative solving. The paper does not discuss whether this creates any evaluation unfairness or whether the problem nature differs systematically from individually-posed OI problems (only 76 of 456 problems are OI).

### Minor

- **No comparison to direct baselines.** The paper thoroughly motivates the limitations of CodeELO and LiveCodeBench Pro but does not provide head-to-head comparisons on shared problem subsets or explain how AetherCode's rankings correlate with established CodeForces rating-based evaluations. This makes it harder for practitioners to calibrate the new benchmark against existing results.

- **No ablation on test case quality components.** The paper claims both automated and expert components are essential but does not quantify the marginal contribution of each (e.g., TNR from G-V Agent alone vs. after expert annotation vs. after the elite audit team). This would strengthen the argument for the hybrid approach.

- **Lack of cost and scalability analysis.** Running 17 models × 456 problems × 4 samples involves ~31,000 API calls with 32K token budgets. The paper does not discuss evaluation cost, which is relevant for researchers planning to use the benchmark.

### Trivial

- Minor presentation inconsistencies: "Ssed-1.6-Thinking" appears in Table 3 while "Seed-1.6-Thinking" appears in Table 4; "Ssed-1.6-Thinking-0715" vs. "Seed-1.6-Thinking-0715." These appear to be typographical variations.

## Nice-to-Haves

- A contamination risk analysis, even a preliminary one, examining whether problems or solutions appear in known training corpora or common crawl data.
- Head-to-head comparison with CodeELO or LiveCodeBench Pro on overlapping problem sources or shared model rankings.
- Discussion of how team-based ICPC problem design philosophy may differ from individual OI problems and how this affects evaluation.

## Novel Insights

The paper's key novel insight—that current LLM evaluations substantially overstate competitive programming proficiency due to both insufficient problem difficulty and unreliable test suites—is well supported by the empirical results. Even the best model (o4-mini-high) solves only about one in three problems, and the dramatic performance drop from "Easy" (~65%) to "Hard" (~8%) to "Extreme" (~3.8%) reveals that the capability gap is concentrated at higher difficulty levels that existing benchmarks rarely test. The observation that non-reasoning models cannot match reasoning models even with Pass@4 suggests a fundamental architectural bottleneck in solution space exploration for complex algorithmic problems.

## Suggestions

- Add a contamination risk assessment section, even brief, discussing which problems are most at risk and what the recency cutoff implies.
- Present an ablation comparing TNR from the automated G-V Agent alone versus after expert annotation to quantify the value of each component.
- Provide evaluation cost estimates (tokens consumed, wall-clock time, approximate API cost) to help researchers replicate the evaluation.

## Score and Decision

The paper makes a well-motivated contribution: it identifies real limitations in existing competitive programming benchmarks and provides a carefully constructed alternative with superior problem sources and a rigorous test case methodology. The 100% TPR/TNR standard, while necessarily limited to the collected solution set, represents a meaningful quality bar. The evaluation is thorough and the results are informative. However, the small problem count (456), minimal "Extreme" tier (20), absence of contamination analysis for high-risk public competition problems, and ICPC team-vs-individual evaluation asymmetry limit the benchmark's robustness and generalizability. These are addressable but represent substantive gaps for a benchmark paper at a top venue.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>