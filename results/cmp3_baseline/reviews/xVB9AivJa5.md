## Summary

Blueprint-Bench is a benchmark that evaluates spatial reasoning in AI models by requiring them to convert apartment photographs into 2D floor plans. The authors test leading LLMs, image generation models, and agent systems on 50 apartments, scoring outputs based on room connectivity graphs and size rankings. Results show that most models perform at or below a random baseline, while humans substantially outperform all AI systems, revealing a significant blind spot in current spatial intelligence capabilities.

## Strengths

- **Novel and well-motivated benchmark task**: The task of converting photographs to floor plans requires genuine spatial reasoning (inferring layouts, connectivity, scale) while using an input modality that is well within the training distribution of modern multimodal models. This design cleverly isolates spatial intelligence from modality adaptation.
- **Model-agnostic evaluation framework**: The benchmark accommodates LLMs (via SVG generation), image generation models, and agent systems within a unified scoring pipeline, enabling direct comparisons across fundamentally different architectures. This is a valuable contribution given the growing diversity of AI systems.
- **Open-source and extensible**: The authors release code and a sample of the dataset, accept community submissions, and commit to updating the leaderboard. This supports reproducibility and long-term tracking of progress in spatial reasoning.
- **Clear demonstration of a capability gap**: The results convincingly show that even the best models (GPT-5, Gemini 2.5 Pro) score far below human performance, and many models fail to exceed a random baseline. This provides concrete evidence that spatial reasoning remains a challenging problem for current AI.

## Weaknesses

### Fatal
None.

### Major
- **Small dataset and limited statistical power**: The benchmark contains only 50 apartments, and the human baseline is computed on a subset of 12. With high variance across apartments (visible in the appendix), the conclusions about which models significantly outperform random are not supported by statistical tests. The paper reports means and standard deviations but no confidence intervals or hypothesis tests.
- **Scoring algorithm has arbitrary and potentially distorting weights**: The composite score uses a weighted average (50% edge overlap, 20% degree correlation, 10% density, 10% room count, 5% door count, 5% door orientation) with no justification for these weights. The heavy penalty on size ranking errors (which affects edge overlap indirectly) means that a model that correctly identifies all room connections but misorders room sizes can receive a low score, conflating different aspects of spatial intelligence.
- **Human baseline is not directly comparable**: Humans were allowed iterative refinement while most models produced single-pass outputs. The agent experiments attempt to address this, but only two specific agent scaffolds are tested, and the paper acknowledges that one agent (Codex) did not actually iterate. The human baseline also uses only 12 apartments, and the paper does not report human performance on the full 50-apartment set, making the headline comparison incomplete.
- **Inconsistent random baseline values**: Figure 5 reports a random baseline of 0.279, while Figure 7 (on a subset) reports 0.322. The paper does not explain how the random baseline is computed (e.g., random graph generation, random placement of rooms), making it difficult to interpret whether models are truly above chance.

### Minor
- **Agent experiments are too narrow to support strong conclusions**: The claim that "iterative refinement through agents showed no meaningful improvement" is based on only two agent systems (Codex CLI and Claude Code). The paper notes that Codex did not actually iterate, and Claude Code's iterative process still produced poor results. This is insufficient to conclude that iterative refinement in general is ineffective for this task.
- **Scoring algorithm ignores room shapes and types**: The paper acknowledges this limitation but does not quantify how much information is lost. Since room shape and function are important aspects of spatial understanding, the benchmark may not fully capture the spatial intelligence it claims to measure.
- **Lack of per-model statistical comparisons**: The paper reports mean scores but does not test whether differences between models (e.g., GPT-5 vs. Gemini 2.5 Pro) are statistically significant. Given the high variance, many apparent differences may not be reliable.

### Trivial
- Figure 7 caption mentions "2.5 standard deviation" for error bars, which is an unusual choice and not explained.
- The term "epochs" is used in the results description but not defined (likely multiple runs per model, but this is not stated explicitly).

## Nice-to-Haves

- Include a more detailed description of the random baseline generation process.
- Provide per-apartment results in a table rather than only bar charts to facilitate independent analysis.
- Add a discussion of how the scoring weights were chosen and consider a sensitivity analysis.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Expand the dataset and human baseline**: Increase the number of apartments and collect human performance on the full set to strengthen statistical conclusions. Consider using multiple human annotators to measure inter-annotator agreement.
- **Validate the scoring algorithm**: Perform ablation studies to show how each component (edge overlap, size ranking, etc.) correlates with human judgment of floor plan similarity. Consider alternative scoring methods (e.g., graph edit distance) and compare results.
- **Run more agent experiments**: Test additional agent scaffolds (e.g., ReAct, AutoGPT) with explicit iterative refinement loops to determine whether the lack of improvement is a general phenomenon or specific to the tested systems.
- **Add statistical significance tests**: Report confidence intervals or p-values for comparisons against random baseline and between models. This would greatly strengthen the claims about which models are above chance.

## Score and Decision

The paper introduces a novel and well-motivated benchmark for spatial reasoning, with a clean experimental design and clear results that reveal a meaningful capability gap. However, the evaluation methodology has several significant limitations: a small dataset, an arbitrarily weighted scoring algorithm, an incomplete human baseline, and a lack of statistical rigor. These issues reduce the confidence in the quantitative conclusions but do not invalidate the core contribution of the benchmark itself. The paper is a solid contribution that will be useful to the community, but it requires further validation and refinement.

**Score**: 6 (borderline accept)

**Decision**: Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>