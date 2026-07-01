## Summary

This paper introduces ARENABENCHER, a framework for automatically evolving static benchmarks to combat data leakage and saturation in LLM evaluation. The method extracts the core ability tested by each benchmark item, generates candidate variants using an LLM, verifies them, and selects those that consistently degrade performance across a diverse pool of models via multi-model feedback scoring. The framework is evaluated on GSM8K, CommonsenseQA, and a safety benchmark, showing increased difficulty, preserved alignment, and maintained fairness across model families.

## Strengths

- **Addresses a timely and important problem**: Data contamination and benchmark saturation are well-recognized issues in LLM evaluation, and the paper tackles the practical challenge of automatically refreshing benchmarks while preserving their original intent.
- **Multi-model feedback design is principled**: Using a sampled subset of models (√K heuristic) to score candidates avoids overfitting to any single model's idiosyncrasies and promotes discovery of shared failure modes, which is a clear improvement over single-model adversarial approaches.
- **Comprehensive evaluation across diverse domains**: The framework is tested on mathematical reasoning (GSM8K), commonsense reasoning (CSQA), and safety (AdvBench), demonstrating applicability beyond a single task type.
- **Human validation provides grounding**: The human annotation study on 100 GSM8K samples (95% alignment, 96% correctness) adds credibility to the automatic metrics and shows the method produces reasonable outputs in practice.

## Weaknesses

### Major

- **The paper does not compare against any baseline methods for benchmark evolution or augmentation.** The experiments only show performance before and after applying ARENABENCHER, with no comparison to alternative approaches such as simple paraphrasing, numerical perturbation (e.g., Mirzadeh et al., 2024), MATH-Perturb (Huang et al., 2025), or other LLM-based rewriting methods. Without baselines, it is impossible to determine whether ARENABENCHER's multi-model feedback mechanism provides meaningful advantages over simpler alternatives. This is a critical omission for a method paper.

- **The evaluation metrics for benchmark quality are not validated against human judgment of "better" benchmarks.** The paper defines difficulty, separability, fairness, and alignment as desiderata, but does not establish that improvements on these metrics correspond to genuinely better evaluation instruments. For example, increasing difficulty by making questions unsolvable (as shown in the case study failure) would trivially increase the difficulty metric but produce a worse benchmark. The human validation only checks alignment and correctness, not whether the updated benchmark is actually more useful for evaluation.

- **The case study reveals a fundamental failure mode that is not systematically addressed.** Figure 2 shows an updated test case that is both invalid (missing necessary information) and misaligned (requiring additional operations). While the paper acknowledges this as a failure case, it does not analyze how frequently such failures occur across the full benchmark, nor does it propose mechanisms to prevent them beyond the existing verifier. The 5% misalignment and 4% incorrectness from human annotation suggest these issues are non-negligible.

### Minor

- **The paper uses GPT-4o for generation, verification, and judgment, creating potential circularity.** The same model family is used for ability extraction, candidate generation, verification, and alignment judgment. This raises concerns about whether the high alignment scores (90-94%) reflect genuine preservation of task intent or simply consistency within the same model's outputs. Using an independent judge model or human evaluation for alignment would strengthen the claims.

- **The model pool is limited to relatively small open-source models (1B-7B parameters).** The paper claims ARENABENCHER is "model-agnostic" and generalizable, but only evaluates on models up to 7B parameters. It is unclear whether the framework would work as effectively for frontier models (e.g., GPT-4, Claude 3.5) or whether the multi-model feedback from small models would generalize to larger ones.

- **The √K sampling heuristic is motivated by ensemble methods from tree-based models (Random Forests, XGBoost), but the connection is not rigorously justified.** The paper does not provide any analysis of how different sampling sizes affect the quality of feedback, nor does it compare √K against other sampling strategies (e.g., stratified sampling by model family, or full model pool evaluation).

### Trivial

- The paper repeatedly uses "ARENABENCHER" in all caps in running text, which is visually distracting.
- Figure 1 appears twice in the paper (duplicated in the PDF extraction).

## Nice-to-Haves

- An ablation study comparing ARENABENCHER against simpler baselines (e.g., random perturbation, single-model adversarial generation, or paraphrasing without multi-model feedback) would substantially strengthen the paper.
- Analysis of how the quality of updated benchmarks changes with the number of refinement iterations (R) would help practitioners understand the cost-benefit tradeoff.
- A discussion of computational cost (e.g., total LLM API calls, time per benchmark update) would help readers assess practical feasibility.

## Novel Insights

None beyond the paper's own contributions. The core idea of using multi-model feedback to select benchmark variants is sensible but not deeply surprising given the existing literature on ensemble methods and adversarial robustness. The paper's main novelty lies in the specific combination of ability extraction, multi-model scoring, and iterative refinement applied to benchmark evolution.

## Suggestions

- Add baseline comparisons against at least two alternative methods: (1) simple numerical/paraphrase perturbation without multi-model feedback, and (2) single-model adversarial generation. This is essential to demonstrate that the multi-model feedback mechanism provides concrete benefits.
- Conduct a systematic analysis of failure cases from the human annotation study to characterize the types of errors ARENABENCHER makes and propose targeted mitigations.
- Validate the alignment metric by comparing LLM-as-a-judge alignment scores against human judgments on a held-out set, to ensure the automatic metric is trustworthy.

## Score and Decision

The paper addresses an important problem and proposes a reasonable framework, but the lack of baseline comparisons is a critical weakness that prevents assessment of whether the method advances beyond existing approaches. The evaluation is otherwise solid, with multiple domains, human validation, and thoughtful metrics. However, without baselines, the contribution cannot be properly contextualized.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>