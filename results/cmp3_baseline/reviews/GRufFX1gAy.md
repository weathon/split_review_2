## Summary

The paper introduces **InnoGym**, a benchmark and framework for evaluating the innovation potential of AI agents. It defines innovation along two complementary dimensions—performance gain (improvement over best-known solutions) and novelty (methodological dissimilarity from prior approaches)—and provides 18 curated tasks from real-world engineering and scientific domains, along with a unified execution environment (iGym). Experiments with several agent frameworks reveal that current agents often achieve novelty without robustness, highlighting a gap between creativity and reliable performance.

## Strengths

- **Addresses an important gap**: Existing benchmarks focus almost exclusively on correctness, ignoring the diversity of methods behind solutions. The paper’s emphasis on both performance gain and novelty is a timely and valuable contribution.
- **Principled formalization**: The task quadruple (P, S, V, D) and the definitions of performance gain and novelty are clearly laid out, providing a solid conceptual foundation for evaluating innovation.
- **Careful task curation**: The two-stage filtering process (resource availability, evaluator quality, domain balance) is thorough, and the resulting 18 tasks span diverse domains with real-world relevance.
- **Unified execution environment (iGym)**: Providing a common SDK for reproducible, long-horizon evaluations across different agent frameworks is a practical contribution that reduces infrastructure confounds.
- **Informative experiments**: The main results and ablation studies (temporal dynamics, foundation model impact, temperature trade-offs) yield concrete insights about the current limitations of AI agents, particularly the gap between novelty and robustness.

## Weaknesses

### Fatal
None.

### Major
- **Novelty metric relies on an LLM-as-judge without sufficient validation**: The distance function D is instantiated via a Codex extraction prompt followed by a GPT-5 judge that rates methodological dissimilarity. The paper does not provide evidence that this judge is reliable (e.g., correlation with human expert ratings, inter-rater agreement, sensitivity to prompt variations). Since novelty is a core contribution, this lack of validation is a significant concern.
- **Small scale and limited statistical rigor**: Only 10 of the 18 tasks are used in the main experiments, each configuration is run only three times, and the best score is reported without measures of variance. This makes it difficult to assess the robustness of the observed performance gaps and framework rankings.
- **Unfair comparison to human SOTA**: Agents are given at most 12 hours per task, while human solutions often involve weeks or months of effort. The claim that “no agent managed to surpass the state-of-the-art human solutions” is therefore unsurprising and may overstate the performance gap. The paper should acknowledge this asymmetry.
- **Dynamic nature of “best-known” solutions**: The performance gain metric is anchored to leaderboard scores that may become outdated. The paper does not discuss how the benchmark will be maintained or updated to remain relevant.

### Minor
- **Use of hypothetical model names**: “GPT-5-2025-08-07” and “Gemini-2.5-Pro” are referenced without clarifying whether these are publicly available versions or internal/anticipated models. This could confuse reproducibility.
- **Novelty definition via min-distance**: Using the minimum distance to any known solution may penalize solutions that are genuinely novel but happen to be close to a single known solution in the embedding space. The paper does not discuss this sensitivity.
- **Exclusion of Solved and Exploratory tasks**: While the focus on Improvable tasks is reasonable, the paper could briefly discuss how the framework might extend to the other categories, or why they are not suitable for the current benchmark.

### Trivial
None.

## Nice-to-Haves

- Human evaluation of the novelty metric (e.g., expert annotators rating methodological dissimilarity) to validate the LLM-as-judge approach.
- Statistical significance tests (e.g., confidence intervals or bootstrapped comparisons) for the main results in Table 2.
- A plan for expanding the benchmark with more tasks or periodic updates to leaderboard baselines.
- Release of the iGym environment and benchmark data (presumably in the appendix, but not visible in the main text).

## Novel Insights

The paper’s key insight is that current AI agents can generate methodologically novel solutions but fail to translate that novelty into reliable performance gains due to a lack of robustness. This decoupling of creativity from effectiveness is a nuanced finding that goes beyond simple “agents are not good enough” narratives. The complex-plane visualization (performance gain as magnitude, normalized novelty as angle) offers a compact way to track the innovation trajectory of an agent over time, revealing that novelty often peaks early and then declines as the solution converges. The exploration-exploitation trade-off at different sampling temperatures further illustrates how agent behavior can be tuned, with a “sweet spot” around 0.5–0.75 temperature that balances performance and novelty.

## Suggestions

1. **Validate the novelty metric**: Conduct a human study where experts rate methodological dissimilarity on a subset of solutions, and report correlation with the LLM-as-judge scores. Alternatively, use a simpler, more transparent distance (e.g., embedding cosine distance) and compare results.
2. **Report variance**: Include standard deviations or interquartile ranges for the three runs, and consider using more runs for key configurations to increase confidence.
3. **Acknowledge the time/resource asymmetry**: Explicitly state that the 12-hour limit is a practical constraint and that human baselines involve far more effort, so the comparison is not a direct measure of capability.
4. **Clarify model versions**: Specify exact model identifiers (e.g., “DeepSeek-v3.1-xxxx”, “Gemini-2.5-Pro-xxxx”) and note whether GPT-5 is a publicly available model or a placeholder.
5. **Discuss maintenance**: Outline how the benchmark will be kept up-to-date as leaderboard scores improve, or propose a versioning scheme.

## Score and Decision

The paper makes a valuable contribution by proposing a principled framework for evaluating innovation beyond correctness, and the benchmark and environment are well-constructed. However, the reliance on an unvalidated LLM-as-judge for the novelty metric is a major weakness that undermines the core claim of measuring methodological novelty. The experiments are informative but limited in scale and statistical rigor. With stronger validation of the novelty metric and more robust experimental reporting, the paper would be significantly stronger. In its current form, it is a borderline accept.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>