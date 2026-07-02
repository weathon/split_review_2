## Summary

The paper proposes **RLIE**, a framework that integrates LLMs with probabilistic modeling (logistic regression) to learn a set of weighted natural-language rules for binary classification. The framework consists of four stages: LLM-based rule generation, regularized logistic regression for global weighting and selection, error-driven iterative refinement, and evaluation of different inference strategies. Experiments on six text classification datasets show that RLIE with direct linear-only inference outperforms several baselines, and that injecting rules and weights back into an LLM for inference degrades performance.

## Strengths

- **Clear and well-motivated framework.** The paper identifies a genuine gap—existing LLM-based rule learning methods lack principled probabilistic aggregation—and proposes a structured four-stage pipeline (generation, logistic regression, iterative refinement, evaluation) that is clearly described and easy to follow.
- **Systematic evaluation of inference strategies.** The hierarchical comparison of four inference methods (Linear-only, LLM+Rules, LLM+Rules+Weights, LLM+Rules+Weights+Linear Prediction) is a valuable contribution. The finding that the simplest linear combiner consistently outperforms LLM-based strategies is non-trivial and provides practical guidance for the community.
- **Empirical breadth.** The method is evaluated on six diverse real-world text classification datasets from HypoBench, covering deception detection, mental stress, engagement, citations, AI-generated content, and retweets. The results show consistent top-two performance across datasets.

## Weaknesses

### Fatal
None.

### Major
- **Inconsistent experimental setup and missing standard deviations.** The paper states that “All experiments involving LLMs utilized gpt-4o-mini” (Section 4.3), yet Table 1 lists RLIE with backbones Qwen3-Next-80B, Qwen3-235B, and DeepSeek-V3, while baselines use DeepSeek-V3. It is unclear which LLM is used for rule generation, rule judgment, and inference in each setting. This lack of control makes the comparison between RLIE and baselines difficult to interpret. Furthermore, the paper claims to report mean and standard deviation, but Table 1 shows only point estimates without any variance, undermining the statistical reliability of the results.
- **Modest and inconsistent improvements.** While RLIE often ranks first or second, the margin over baselines is small on several datasets (e.g., Reviews: 70.9 vs. HypoGeniC 69.1; Retweets: 65.7 vs. HypoGeniC 61.9). The claim of “superior over all performance” is overstated given these modest gains and the lack of controlled comparisons.
- **Limited baseline coverage.** The paper compares against only three LLM-based rule learning methods (Zero-shot Gen, IO Refinement, HypoGeniC) plus LoRA finetuning on a much smaller model. Other relevant approaches (e.g., predicate invention, neuro-symbolic methods, or more recent hypothesis generation frameworks) are not included, limiting the assessment of relative novelty and effectiveness.

### Minor
- **No sensitivity analysis.** Key hyperparameters (rule capacity H=10, number of hard examples k=20, new rules per iteration h=5, coverage threshold γ=0.2) are fixed without any ablation or sensitivity study. The robustness of the framework to these choices is unknown.
- **Computational cost not discussed.** The framework requires many LLM calls (rule generation, per-rule judgment on all training samples for coverage, iterative refinement). The paper does not report runtime, API cost, or practical feasibility, which is important for reproducibility and deployment.
- **Generalizability limited to text.** All datasets are text classification tasks. The method’s applicability to other modalities (e.g., tabular data, images) or to multi-class problems is not addressed.

### Trivial
None.

## Nice-to-Haves

- Include standard deviations in all result tables and perform statistical significance tests (e.g., paired bootstrap) to support claims of superiority.
- Conduct an ablation study on key hyperparameters (H, k, h, γ) to demonstrate robustness.
- Report computational cost (number of LLM calls, total tokens, runtime) to help practitioners assess feasibility.
- Extend evaluation to additional datasets or tasks (e.g., multi-class, regression) to broaden the scope.

## Novel Insights

Beyond the paper’s own contributions, the most striking insight is that LLMs, despite their semantic prowess, consistently fail to improve upon a simple logistic regression combiner when given explicit rule weights and reference predictions. This suggests a fundamental limitation: LLMs are unreliable at fine-grained probabilistic integration, and a clean division of labor—LLMs for local semantic judgment, classical models for global aggregation—is more effective. This finding has implications for the design of neuro-symbolic systems and cautions against over-reliance on LLMs for structured reasoning.

## Suggestions

- Clarify the experimental setup: specify exactly which LLM is used for rule generation, rule judgment (coverage computation), and inference in each configuration. Ensure that the backbone LLM is controlled across all compared methods to isolate the effect of the RLIE framework.
- Add standard deviations to Table 1 and Table 2, and consider reporting confidence intervals or performing significance tests.
- Tone down the claim of “superior over all performance” to reflect the modest and dataset-dependent improvements.

## Score and Decision

**Score:** 4  
**Decision:** Reject

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>