## Summary
The paper introduces InnoGym, a benchmark and framework for evaluating the innovation potential of AI agents, moving beyond correctness-only evaluation. It defines innovation via two complementary metrics: performance gain (improvement over best-known solutions) and novelty (methodological dissimilarity from prior solutions). The benchmark includes 18 curated tasks from real-world competitions and a unified execution environment iGym, and experiments with three agent frameworks reveal that current agents often achieve novelty but lack robustness, resulting in negative performance gains.

## Strengths
- Proposes a principled framework for defining and measuring innovation in AI agents, combining performance gain and novelty as two complementary dimensions, which is a novel and important contribution beyond existing correctness-focused benchmarks.
- First benchmark specifically targeting innovation potential, with careful multi-stage curation of tasks from diverse real-world competitions (NeurIPS, KDD, ROADEF, etc.), ensuring tasks are improvable and have reliable evaluators.
- Provides a unified execution environment iGym that supports reproducible, long-horizon evaluations across different agent systems, addressing practical infrastructure challenges.
- Extensive experiments with multiple agent frameworks (MLAB, CodeAct, AIDE) and ablation studies (time budget, foundation model, sampling temperature) that yield insights into the trade-offs between novelty and performance.
- Clear identification of a key gap: current agents can be novel but lack robustness, highlighting an important direction for future research on agent reliability.

## Weaknesses
### Fatal
None.

### Major
- The novelty metric relies heavily on an LLM-as-judge pipeline (Codex for feature extraction, GPT-5 for scoring dissimilarity). The paper does not provide sufficient validation of this metric’s reliability, reproducibility, or alignment with human judgments. Given that novelty is a core contribution, this is a significant concern that undermines confidence in the benchmark’s central measure.
- All evaluated agents achieve negative performance gains on all tasks, meaning they perform worse than the worst known human baselines. This raises questions about whether the benchmark is too difficult or whether the selected agents are appropriate for these tasks. The benchmark’s discriminative power for positive innovation is not demonstrated, limiting its immediate utility.
- Only 10 of the 18 tasks are used in the main experiments due to resource constraints, and the paper does not clarify how representative these 10 tasks are of the full benchmark. This reduces the claimed breadth of evaluation.

### Minor
- The distance function D is instantiated via LLM-as-judge, but the paper does not explore alternative distance measures (e.g., embedding-based) or compare their consistency, leaving the choice somewhat arbitrary.
- The benchmark excludes “Solved Problems” and “Exploratory Problems”, which may limit the scope of innovation that can be evaluated. The rationale is clear but the benchmark’s coverage of innovation types is narrow.
- The paper claims that iGym addresses limitations of existing SDKs (OpenHands, AutoGen, LangGraph), but does not provide a direct comparison or ablation to demonstrate its advantages quantitatively.

### Trivial
- Table 1 marks “Ref. Sol.” for MLAgentBench as ✓, but it is unclear if that benchmark provides reference solutions in the same structured sense as InnoGym.
- Some figure captions appear duplicated in the text (e.g., Figure 1 caption appears twice).

## Nice-to-Haves
- A human evaluation study to validate the novelty metric would greatly strengthen the paper and address the major concern about its reliability.
- Including tasks where agents can achieve positive performance gain (e.g., simpler tasks or tasks with more room for improvement) would better demonstrate the benchmark’s ability to measure positive innovation.
- Providing an analysis of the computational cost of the novelty evaluation (LLM calls) and its scalability would be useful for practitioners.

## Novel Insights
The paper’s key insight is that innovation in AI agents should be evaluated along two orthogonal axes: performance improvement and methodological novelty. The experimental finding that agents can achieve high novelty but fail to translate it into performance gains due to lack of robustness is a valuable observation that challenges the current focus on creativity alone. The complex-plane representation of the innovation trajectory is a nice conceptual tool for visualizing the trade-off.

## Suggestions
- Provide a thorough validation of the novelty metric, including correlation with human expert ratings and consistency across different LLM judges (e.g., using different backbone models for the judge).
- Consider including tasks where human baselines are weaker or where agents have a chance to outperform them, to better demonstrate the benchmark’s ability to measure positive innovation.
- Report results on all 18 tasks, even if with fewer runs, to give a complete picture of the benchmark’s coverage.
- Compare iGym quantitatively with existing SDKs on metrics like success rate, runtime overhead, and ease of use to substantiate the claimed advantages.

## Score and Decision
Score: 6

Decision: Borderline Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>