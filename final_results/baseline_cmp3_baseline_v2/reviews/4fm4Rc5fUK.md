## Summary
This paper presents ATF (Autoformalizer with Tool Feedback), a framework that integrates syntactic (Lean 4 compiler) and semantic consistency (multi-LLM judge) tools into the autoformalization process. The model is trained via a three-stage pipeline—cold start on synthetic tool-calling data, expert iteration, and Direct Preference Optimization—to iteratively refine formal statements based on tool feedback. ATF substantially outperforms existing formalizers on three benchmarks, especially on the out-of-distribution CombiBench, and the authors open-source a 750K formal statement dataset.

## Strengths
- **Strong and consistent empirical results.** ATF-32B surpasses all baselines across three benchmarks on both syntax and consistency metrics. On the challenging CombiBench, it achieves 65.38% consistency Pass@1 vs. the best baseline’s 36.25% (+29.13%). The gains are validated by human evaluation, which also shows a high correlation (Pearson r=0.746) with the automatic consistency check.
- **Well-motivated problem and clean methodology.** The paper clearly identifies two key challenges in autoformalization (lack of formal knowledge, unreliable consistency validation) and designs dedicated tools to address each. The training pipeline (cold start → expert iteration → DPO) is logically structured, and each component is ablated to show its contribution.
- **Thorough analysis and scaling behavior.** The paper goes beyond main results to analyze inference-time scaling (revision attempts and sampling), tool usage patterns across datasets, and the distribution of consistency check success rates by attempt number. The finding that ATF benefits from more revision attempts even beyond training is insightful.
- **Open-source dataset contribution.** Numina-ATF (750K formal statements) is released to the community, which can accelerate future research in autoformalization and automated theorem proving.
- **Efficient small model variant.** ATF-8B-Distilled, trained on the same data, still outperforms 32B baselines on most metrics, demonstrating that the method can produce efficient yet effective formalizers.

## Weaknesses
### Fatal
None.

### Major
- **The consistency check tool relies on a multi-LLM ensemble that is validated on a synthetic benchmark.** The benchmark used to select the consistency judge is constructed by perturbing positive statements with a single model (Gemini-2.5-Pro). While the paper reports a strong correlation with human evaluation (0.746), the synthetic nature of the perturbation dataset may not cover all types of semantic misalignment that occur in practice. The ensemble approach also reduces recall (TPR), meaning some valid formalizations may be incorrectly rejected as inconsistent during training/inference, potentially limiting the ceiling of the method. The overall results are strong enough to mitigate this concern, but the tool’s reliability could be more thoroughly justified.

### Minor
- **The improvement from the DPO phase is modest.** For example, on CombiBench consistency Pass@1, adding DPO to expert iteration raises performance from 63.88% to 65.38%. While the paper frames DPO as reducing ineffective revisions, the gains are small relative to the preceding phases. This does not invalidate the contribution but suggests the primary benefits come from cold start and expert iteration.

### Trivial
- None worth noting.

## Nice-to-Haves
- It would be interesting to see the performance of ATF when using different base models (e.g., other 32B or 7B architectures) or when trained on larger and more diverse informal-formal pairs beyond NuminaMath.
- An analysis of failure cases where ATF cannot pass the consistency check after many revisions, to understand the fundamental limitations of the approach.
- Comparison with a version that uses a lean verifier (e.g., attempting to prove the formalized statement) as an additional semantic check, though this may be too expensive.

## Novel Insights
Beyond the paper’s own contributions, the analysis reveals that the model learns to allocate more revision attempts to harder datasets (average 8.35 tool calls on CombiBench vs. 3.19 on FormalMath-Lite) and that consistency check success rates decay sharply with attempt number (from ~70% on first attempt to <10% on eighth). This suggests that the model is effectively learning to apply its most confident revision strategies early and struggles with more obscure misalignments later—a pattern that could inform future designs of iterative refinement systems. Additionally, the inference scaling result (performance continues to improve with more revision attempts even beyond training) indicates that the model has internalized a generalizable revision strategy.

## Suggestions
- Provide more details on the decontamination procedure used to ensure no overlap between training data and evaluation benchmarks.
- Consider releasing the consistency check benchmark (the 800 query perturbation dataset) to facilitate standardized evaluation of consistency verification tools.
- In future work, explore training a lightweight learned verifier for consistency, replacing the multi-LLM judge to reduce inference cost and improve recall.

## Score and Decision
MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>