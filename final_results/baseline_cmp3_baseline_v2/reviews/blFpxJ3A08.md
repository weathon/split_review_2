## Summary

This paper introduces LPFQA, a benchmark for evaluating LLMs on long-tail professional knowledge, constructed from 505 questions sourced from real technical forums across 20 academic fields. The benchmark features fine-grained evaluation dimensions (knowledge depth, reasoning, terminology, contextual analysis), hierarchical difficulty, and expert verification. The authors evaluate 12 mainstream LLMs and find significant performance disparities, with GPT-5 achieving the highest score (47.28) and GPT-4o the lowest (32.40), while ablation studies suggest the benchmark primarily measures domain knowledge rather than reasoning ability.

## Strengths

- **Real-world authenticity**: The benchmark is derived from actual professional forum discussions (Project Euler, CONTROL.com, Mathematics Stack Exchange, Chemistry Stack Exchange), which grounds evaluation in genuine practitioner needs rather than artificial scenarios. This addresses a genuine gap in existing benchmarks that often rely on simplified or idealized tasks.

- **Comprehensive domain coverage**: With 20 academic fields spanning from Computer Science to Aerospace to Law, the benchmark offers broad interdisciplinary coverage that challenges models to demonstrate cross-domain generalization. The inclusion of long-tail knowledge from specialized forums is a meaningful contribution.

- **Thoughtful ablation studies**: The experiments with code interpreter and search tools (Tables 3 and 4) provide interesting insights—showing that adding these tools often degrades performance, which the authors correctly attribute to the long-tail nature of the knowledge being difficult to retrieve or compute. This is a non-obvious finding.

## Weaknesses

### Fatal
None.

### Major

- **Small dataset size (505 questions) limits statistical reliability**: With only 505 total questions and as few as 3 questions in some fields (e.g., Data Science), the benchmark's ability to produce statistically meaningful comparisons is severely limited. The performance differences between models (e.g., GPT-5 at 47.28 vs. DeepSeek-V3 at 32.60) could easily be driven by a handful of questions. After filtering, the dataset shrinks to 421-436 questions, making the per-field sample sizes even smaller. This undermines the claim of providing a "robust" and "discriminative" benchmark.

- **Narrow performance range limits discriminative power**: The main results (Table 1) show scores ranging from 32.40 to 47.28—a spread of only ~15 points on what appears to be a 0-100 scale. With 12 models evaluated, the average separation between adjacent models is roughly 1.3 points. Given the small sample size, it is unclear whether these differences are statistically significant. The paper does not report confidence intervals or statistical significance tests.

- **Unclear evaluation methodology**: The paper states that questions are in "multiple-choice or short-answer form" but does not specify how short-answer responses are evaluated. The example shows a "Key Point" field for short-answer questions, but the actual scoring mechanism (exact match? semantic similarity? LLM-as-judge?) is not described. This is a critical omission for reproducibility.

- **Contradictory claims about what the benchmark measures**: The ablation study with code interpreter (Table 3) shows performance decreases, leading the authors to conclude "LPFQA primarily reflects a model's mastery of domain knowledge rather than its reasoning ability." However, the paper's title and introduction emphasize "complex reasoning" as a key evaluation target. If the benchmark primarily measures knowledge memorization rather than reasoning, this significantly weakens the claimed contribution.

- **No comparison to existing benchmarks**: The paper does not report how LPFQA correlates with or differs from established benchmarks like MMLU, HLE, or Arena-Hard. Without such comparisons, it is difficult to assess whether LPFQA provides genuinely new information about model capabilities or simply recapitulates existing rankings.

### Minor

- **Limited model selection details**: The paper lists model names (e.g., "Qwen-3-235B") but does not specify which specific checkpoint, API version, or inference configuration was used. Given that model performance can vary significantly across versions, this lack of specificity hinders reproducibility.

- **Radar charts are difficult to interpret**: Figures 3 and 4 use 12 separate radar charts with 12 axes each, making direct comparison across models nearly impossible. A single multi-line plot or heatmap would be far more informative.

- **The "filtered LPFQA" analysis is confusing**: The paper creates LPFQA⁻ (removing questions no model could answer) and LPFQA⁼ (further removing questions all models could answer). The rationale is to increase discriminative power, but this post-hoc filtering means the benchmark's composition depends on which models are evaluated, making it non-static and difficult to use as a standard benchmark.

### Trivial

- The paper states "DeepSeek-V3 demonstrates the most balanced and consistent performance across disciplines" in the analysis, but Table 1 shows DeepSeek-V3 has the second-lowest overall score (32.60). "Balanced" is not clearly defined and seems to contradict the overall ranking.

## Nice-to-Haves

- Reporting confidence intervals or bootstrap estimates for model scores would greatly strengthen the claims about model ranking.
- A correlation analysis with existing benchmarks (MMLU, HLE, Arena-Hard) would help position LPFQA within the existing evaluation landscape.
- Providing example questions from multiple difficulty levels would help readers understand the benchmark's range.

## Novel Insights

The key insight is that adding external tools (code interpreter, search) to LLMs can actually *decrease* performance on long-tail knowledge tasks, because the knowledge is rare enough that retrieval introduces noise rather than signal. This is a non-trivial finding that challenges the assumption that tool augmentation is always beneficial. However, this insight is somewhat undermined by the small dataset size—the observed effects could be noise.

## Suggestions

1. **Expand the dataset significantly**—at minimum to several thousand questions—to ensure statistical reliability, especially for per-field comparisons.
2. **Clarify the evaluation methodology** for short-answer questions, including the exact scoring mechanism and whether human evaluation or automated metrics are used.
3. **Report statistical significance** (e.g., bootstrap confidence intervals) for all model scores and comparisons.
4. **Provide correlation analysis** with existing benchmarks to demonstrate that LPFQA captures something new.
5. **Reconcile the contradiction** between claiming the benchmark evaluates "complex reasoning" and the ablation study suggesting it primarily measures knowledge.

## Score and Decision

The paper addresses a genuine need—evaluating LLMs on authentic, long-tail professional knowledge—and the construction pipeline is well-motivated. However, the small dataset size (505 questions, with some fields having only 3 questions) fundamentally limits the benchmark's reliability and discriminative power. The lack of statistical significance testing, unclear evaluation methodology for short-answer questions, and the contradiction between the claimed focus on reasoning and the ablation results are significant concerns. While the idea has merit, the current implementation does not yet provide a sufficiently robust benchmark to warrant acceptance.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>