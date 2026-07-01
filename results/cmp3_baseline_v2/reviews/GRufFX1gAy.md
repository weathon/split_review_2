## Summary

The paper introduces InnoGym, a benchmark and framework for evaluating the innovation potential of AI agents. It formalizes innovation along two complementary dimensions—performance gain (improvement over best-known solutions) and novelty (methodological dissimilarity from prior approaches)—and provides 18 curated tasks from real-world engineering and scientific domains, along with a unified execution environment (iGym). Experiments with three agent frameworks reveal that current agents often produce novel approaches but lack the robustness to translate novelty into meaningful performance gains.

## Strengths

- **Important and timely problem.** The paper correctly identifies a critical gap in existing benchmarks: they measure correctness but ignore the diversity of methods. Evaluating both performance and methodological novelty is a valuable direction that could shift how the community thinks about agent capability.
- **Principled formalization.** The framework defines tasks as quadruples (P, S, V, D) and provides clear mathematical definitions for performance gain and novelty, grounding the evaluation in a rigorous structure. The taxonomy of solved, improvable, and exploratory problems is well-motivated.
- **Thorough benchmark curation.** The two-stage filtering process (resource availability, evaluator quality, domain balance) is systematic and transparent. The standardization steps (task specification, validator construction, solution collection, evaluator normalization) demonstrate careful attention to reproducibility and fairness.
- **Informative experimental analysis.** The ablation studies on execution time, foundation model choice, and sampling temperature provide useful insights into the dynamics of agent innovation, particularly the exploration-exploitation trade-off and the dependence on base model strength.

## Weaknesses

### Major

- **The novelty metric (D) is an LLM-based judge with insufficient validation.** The distance function D is instantiated via a Codex extraction prompt followed by a GPT-5 rubric-based evaluation. The paper does not provide any human correlation study, inter-annotator agreement, or sensitivity analysis to demonstrate that this metric reliably captures methodological dissimilarity. Since novelty is half of the core contribution, the lack of validation is a significant concern. The appendix is referenced but not available for review; the main paper alone does not establish the metric's trustworthiness.
- **Limited scale and discriminative power.** The benchmark contains only 18 tasks, with 10 used in main experiments. All evaluated agents achieve negative performance gains on every task, meaning the benchmark currently only measures *failure to innovate* rather than differentiating degrees of innovation. While the paper acknowledges this gap, the benchmark's utility for ranking agents by innovation potential is not yet demonstrated.

### Minor

- **The novelty metric is only computed for feasible solutions, but many agents fail to produce feasible solutions on several tasks.** This leads to many missing entries in Table 2, reducing the amount of data available for analyzing novelty.
- **The paper uses a hypothetical model (GPT-5-2025-08-07) in one ablation, which may not be publicly available or reproducible.** This weakens the reproducibility of that specific experiment.
- **Statistical significance is not reported.** With only three runs per configuration and best-score reporting, it is unclear whether observed differences between frameworks are meaningful.

### Trivial

- The paper occasionally refers to figures and tables that are not fully described in the caption text (e.g., Figure 1 caption is repeated and contains incomplete sentences).

## Nice-to-Haves

- A human evaluation study validating the novelty metric against expert judgments would substantially strengthen the paper.
- Including tasks where some agents achieve positive performance gain would make the benchmark more discriminative and useful for future work.
- Reporting results with confidence intervals or error bars would improve the reliability of the experimental conclusions.

## Novel Insights

The paper's key insight is that innovation in AI agents should be evaluated along two orthogonal axes—performance gain and methodological novelty—and that current agents exhibit a "creativity-robustness gap": they can generate novel ideas but fail to implement them correctly. The complex-plane representation of the solution development process (Figure 5b) is a clever way to visualize the joint evolution of these two dimensions. The finding that novelty decreases over time while performance improves (diminishing returns) is a concrete empirical observation that aligns with intuitive notions of convergent refinement.

## Suggestions

- Provide a validation study for the novelty metric, e.g., human ratings on a subset of solutions compared to the LLM-based scores, with correlation coefficients.
- Consider including tasks where the performance ceiling is not extremely high, so that some agents can achieve positive performance gain, making the benchmark more informative.
- Report results with standard deviations or confidence intervals across runs to support the claims about framework differences.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>