## Summary

ARENABENCHER proposes a framework for automatically evolving static benchmarks to combat data leakage and saturation. Given an existing benchmark and a pool of models, it extracts the core ability of each test case, generates candidate rewrites, verifies them with an LLM judge, and selects candidates that consistently degrade performance across multiple sampled models. The process iterates with in-context demonstrations of strong candidates. Experiments on GSM8K, CommonsenseQA, and AdvBench show that the updated benchmarks increase difficulty while maintaining alignment, fairness, and separability.

## Strengths

- **Addresses a timely and important problem.** Data contamination in static benchmarks is a well-documented threat to valid evaluation, and the paper tackles it with a practical, automated solution. The motivation is clear and the problem is of high relevance to the community.
- **Multi-model feedback is a principled design choice.** Using a diverse pool of models to score candidates (rather than a single model) mitigates model-specific bias and overfitting. The $\sqrt{K}$ sampling heuristic and the uniform sampling tracking are sensible engineering choices that balance diversity, stability, and cost.
- **Comprehensive evaluation across three domains.** The paper tests on math reasoning (GSM8K), commonsense reasoning (CSQA), and safety (AdvBench), demonstrating that the framework generalizes beyond a single task type. The four desiderata (difficulty, separability, fairness, alignment) provide a multi-faceted view of benchmark quality.
- **Human annotation validates alignment and correctness.** The human evaluation on 100 GSM8K samples (95% aligned, 96% correct) provides strong evidence that the automatic updates are not merely adversarial but preserve task intent in the vast majority of cases.

## Weaknesses

### Fatal
None.

### Major
- **The paper does not compare against any baseline method for benchmark evolution.** The experiments only compare the original benchmark to the ARENABENCHER-updated version. Without comparisons to alternative approaches (e.g., simple paraphrasing, numerical perturbation, single-model adversarial rewriting, or prior work like MATH-Perturb or Automatic Robustness Stress Testing), it is impossible to determine whether the observed improvements are due to the specific design of ARENABENCHER or simply to the fact that *any* perturbation increases difficulty. This is a critical omission that weakens the claim of contribution.
- **The fairness metric is potentially misleading.** The fairness metric measures how evenly failures are distributed across models, but a benchmark that is "fair" by this definition could still be systematically biased if the failures are concentrated on a subset of test cases that happen to be equally hard for all models. More importantly, the metric does not account for the *baseline* fairness of the original benchmark. The reported fairness values for the original benchmarks (e.g., 84.8 for GSM8K) are already quite high, and the improvements are marginal (e.g., 87.8 for ARENABENCHER₃). The paper should discuss whether these differences are statistically significant and practically meaningful.
- **The alignment metric relies entirely on an LLM judge (GPT-4o).** While the human annotation provides some validation, the main alignment numbers in Table 2 are based on the same model family used for generation and verification. This creates a circular dependency: the same model that generates and verifies candidates also judges alignment. The paper should either use a different judge model for alignment evaluation or provide more extensive human validation across all domains, not just GSM8K.
- **The case study reveals a genuine failure mode that is not systematically analyzed.** The failure case in Figure 2 shows that the framework can produce unsolvable or misaligned queries. The paper acknowledges this but does not quantify how often such failures occur beyond the 100-sample human annotation. Given that the human annotation found 5% misaligned and 4% incorrect, the paper should discuss whether these rates are acceptable and how they might be reduced.

### Minor
- **The model pool is limited to small open-source models (1B–7B).** While this is a practical choice for computational feasibility, it raises questions about whether the findings generalize to larger models (e.g., 70B+ or proprietary models). The paper should acknowledge this limitation more explicitly.
- **The iterative refinement uses only 3 rounds and 5 candidates per round.** The paper does not provide an ablation study on these hyperparameters. It is unclear whether more rounds or more candidates would yield further improvements or whether the process converges quickly.
- **The difficulty metric uses the *max* accuracy across models.** This is an unusual choice; most benchmarks report average accuracy. Using the max accuracy means that a single strong model can dominate the difficulty score, which may not reflect the overall challenge for the model pool. The paper should justify this choice or report both max and average.

### Trivial
- The paper uses "ARENABENCHER" and "ARENA BENCHER" inconsistently in the text (e.g., in Algorithm 1 caption).
- The reference list contains a typo: "Balocci" should be "Balloccu."

## Nice-to-Haves

- An ablation study comparing ARENABENCHER to simpler baselines (e.g., random perturbation, single-model adversarial rewriting, or a version without iterative refinement) would greatly strengthen the paper.
- A discussion of the computational cost of the framework (e.g., total API calls, time per test case) would help practitioners assess its practicality.
- An analysis of which types of test cases are most likely to fail (e.g., those requiring multi-step reasoning vs. single-step) would provide deeper insight into the failure modes.

## Novel Insights

None beyond the paper's own contributions. The core idea of using multi-model feedback for benchmark evolution is novel, but the individual components (ability extraction, LLM-based generation and verification, iterative refinement) are all established techniques. The paper's main insight is the combination of these components with a focus on cross-model fairness and shared failure patterns.

## Suggestions

- Add baseline comparisons to at least two alternative methods: (1) a simple perturbation baseline (e.g., replacing numbers or names) and (2) a single-model adversarial rewriting baseline (e.g., using GPT-4o to maximize loss for one model). This would directly test the claim that multi-model feedback is beneficial.
- Report the alignment and correctness rates from human annotation for all three domains, not just GSM8K.
- Use a different LLM judge for the alignment metric (e.g., Claude or Gemini) to break the circular dependency with the generator/verifier.
- Provide a statistical significance test (e.g., bootstrap confidence intervals) for the fairness and separability differences between the original and updated benchmarks.

## Score and Decision

The paper addresses an important problem with a well-motivated and reasonably designed framework. The experiments are comprehensive across three domains, and the human annotation provides valuable validation. However, the lack of any baseline comparison is a significant weakness that prevents the paper from demonstrating that its specific design choices are responsible for the observed improvements. Without baselines, the paper essentially shows that "perturbing benchmarks makes them harder," which is already known. The contribution of the multi-model feedback mechanism and the iterative refinement strategy cannot be properly evaluated.

Given the severity of this omission, the paper is not yet ready for acceptance. The core idea is promising, but the experimental evaluation is incomplete.

MY FINAL SCORE: 4.0score</score>
MY FINAL DECISION: Reject</decision>