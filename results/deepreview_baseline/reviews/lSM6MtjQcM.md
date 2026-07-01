## Summary

This paper introduces AetherCode, a new benchmark for evaluating LLMs on competitive programming problems sourced from premier competitions (IOI and ICPC series). The benchmark features 456 recent problems (2024-2025) with rigorous test cases constructed through a hybrid automated and expert-annotated pipeline, achieving 100% True Positive Rate and 100% True Negative Rate on a corpus of over 30,000 human solutions. Evaluation of 17 models reveals that even top reasoning models (o4-mini-high, Gemini-2.5-Pro) solve only about 35% of problems, demonstrating a substantial gap between LLMs and elite human competitors.

## Strengths

- **Timely and well-motivated problem selection.** AetherCode is the first benchmark to systematically collect problems from both the OI series (IOI, national OIs) and the ICPC series, including regional and world finals. This directly addresses the limitation of prior benchmarks that rely on easier or more homogeneous sources (LeetCode, CodeForces). The inclusion of "Extreme" problems (unsolved by humans) provides a genuinely challenging test.

- **Rigorous test case generation methodology.** The hybrid pipeline combining an automated Generator-Validator agent with human expert annotation and auditing by elite problem setters (multiple ICPC gold medalists) is a significant step forward. The use of TPR and TNR as direct quality metrics on a large collected solution set is principled, and the stated goal of 100% on both metrics sets a high standard for the field.

- **Comprehensive evaluation with meaningful analysis.** The evaluation includes 11 reasoning and 6 non-reasoning models with multiple runs, detailed breakdowns by difficulty, year, algorithm category, and failure reasons. The analysis of failure types (e.g., Claude's tendency toward correct but inefficient algorithms, GLM-4.5's language-following issues) provides actionable insights for model development.

## Weaknesses

### Fatal

None.

### Major

- **Limited scope of the collected solution set for validating test case quality.** The claim of 100% TPR and 100% TNR is only on the curated set of solutions (≥5 correct, ≥20 incorrect per problem). If the incorrect solutions are predominantly simple or obvious failures, achieving high TNR is less informative about coverage of subtle errors. Conversely, the correct solutions might not represent the full range of valid algorithmic approaches. The paper does not discuss the distribution or diversity of solutions, nor does it provide evidence that the solution set is representative of the space of all plausible solutions. A benchmark's test suite could achieve 100% on a narrow solution set yet still miss many failure modes.

- **Lack of controlled comparison of test case quality against existing benchmarks.** The paper criticizes prior benchmarks for low-quality test cases but does not directly measure TPR/TNR of those benchmarks' test suites on the same solution sets (or a common held-out set). Without such a comparison, the claimed superiority is stated but not demonstrated. For example, how does AetherCode's test suite compare to CodeForces' official test cases (which many prior works use via API) on a common set of solutions?

- **Potential selection bias in problem difficulty.** The benchmark includes 456 problems from a narrow time window (2024–2025). While this helps avoid contamination, it also means the difficulty distribution may be influenced by specific contest trends in those two years. The paper does not analyze whether the difficulty and algorithm distribution is representative of the broader space of competitive programming problems, which limits the generalizability of claims about LLM capabilities.

### Minor

- **The 100% TPR/TNR claim is made on the "collected solution set," but the paper does not specify whether the same solutions were used for both generating and evaluating the test cases.** If the test cases were tuned to pass/fail the same solutions they were evaluated on, the metric may overfit. A hold-out validation set would strengthen the claim.

- **The paper mentions "over 30,000 human-written solutions" but provides no detail on the distribution across problems, language diversity, or correctness verification criteria for the "incorrect" solutions.** For example, an incorrect solution might be trivially wrong (e.g., a random print) or subtly wrong (nearly correct but missing a corner case). The TNR metric treats all failures equally, which may mask differences in test case sensitivity.

- **The human expert annotation step relies on recruiting experts with Codeforces ratings >2000 and ICPC gold medalists.** While impressive, the reproducibility of this process is limited. The paper does not discuss inter-annotator agreement or the criteria used by experts to design test cases that target specific incorrect solutions.

### Trivial

None.

## Nice-to-Haves

- A direct comparison of AetherCode's test case quality (TPR/TNR) against those of LiveCodeBench, CodeContests, or USACO on a shared set of solutions would strongly substantiate the claims of improved rigour.
- Releasing a held-out set of solutions (used only for final validation, not during test case construction) would increase trust in the 100% TPR/TNR figure.
- Including an analysis of the difficulty distribution in each algorithm category (as mentioned in the text but deferred to an appendix that is not available) would help interpret the per-category performance results.

## Novel Insights

The paper's central insight—that existing benchmarks inflate LLM proficiency through a combination of insufficient problem difficulty and insufficiently discriminating test cases—is not entirely novel, as other works (Wang et al., 2025b; Shi et al., 2024) have pointed to similar issues. However, AetherCode operationalizes this insight more fully than prior efforts by simultaneously addressing both dimensions: sourcing problems from truly elite competitions (IOI/ICPC) and constructing test cases with a gold-standard quality assurance process validated against human solution data. The finding that even the best current reasoning models achieve only ~35% Pass@1, with a large gap between reasoning and non-reasoning models, provides a concrete updated picture of LLM code reasoning ability. The failure analysis showing that top models still primarily fail due to incorrect algorithmic logic (not implementation errors) suggests that deeper reasoning improvements are needed beyond better code generation alone.

## Suggestions

- Explicitly report the TPR and TNR of existing benchmarks (LiveCodeBench, CodeContests, etc.) on the same set of solutions used for AetherCode, ideally using a cross-benchmark evaluation to demonstrate the gap.
- Provide a validation set of solutions held out from test case construction to avoid overfitting and increase confidence in the 100% metric.
- Expand the metadata to include per-problem solution diversity (e.g., number of distinct correct algorithmic approaches) to help interpret TPR/TNR results.

## Score and Decision

**Score:** 7.0

This paper makes a solid contribution by addressing a clear need in the LLM evaluation ecosystem. The benchmark is well-motivated, carefully constructed, and thoroughly evaluated. The test case quality methodology is a step forward, though the lack of direct comparative evidence against existing benchmarks weakens the claimed advantage. The evaluation results are informative and already provide useful insights into model capabilities. The paper is clearly written and will be a valuable resource for the community. Minor weaknesses around the validation of test case quality and the limited temporal scope prevent a higher score, but the work is well above the acceptance threshold.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>