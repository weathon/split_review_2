## Summary

This paper proposes R-HORIZON, a method for constructing multi-horizon reasoning benchmarks and training data by composing existing single-problem tasks with sequential arithmetic dependencies. The authors evaluate 26 Large Reasoning Models (LRMs) on their benchmark, documenting significant performance degradation as the reasoning horizon increases and analyzing error types, effective reasoning length, reflection behavior, and thinking budget allocation. They further use R-HORIZON data for reinforcement learning with verifiable rewards (RLVR) and show that training on composed problems improves both multi-horizon and single-horizon reasoning performance on a 7B model.

## Strengths

- **Timely and relevant problem.** Evaluating LRMs on multi-step, interdependent reasoning tasks (rather than isolated problems) addresses a genuine gap in current evaluation paradigms, given the increasing use of test-time scaling and long-chain-of-thought reasoning.
- **Comprehensive evaluation.** The benchmark spans 6 datasets across mathematics, code generation, and agentic tasks, and the evaluation covers 26 models of varying sizes, including frontier models like DeepSeek-R1, o4-mini, and Qwen3-235B. The consistent degradation pattern across model scales and tasks is empirically convincing.
- **Analytical depth.** The paper goes beyond simple accuracy reporting to analyze error types (problem reasoning vs. dependency reasoning vs. early stop), effective reasoning length, reflection frequency and scope, and thinking budget allocation. These analyses provide concrete insights into current LRM limitations.
- **Practical RL contribution.** Using R-HORIZON data for RL training yields positive results: improved performance on both composed and original problems, more efficient token allocation, and better reflection behavior. The controlled experiments with different composition counts and reward schemes provide useful design guidance.

## Weaknesses

### Fatal

None.

### Major

1. **Artificial dependency structure.** The paper constructs dependencies via arithmetic substitution of a previous answer into a subsequent problem’s key variable. While this creates a verifiable sequential constraint, it does not resemble the varied, often non-arithmetic dependencies encountered in real-world long-horizon reasoning (e.g., planning, multi-hop inference across heterogeneous information sources). The ecological validity of the benchmark for measuring true "long-horizon reasoning" is therefore unclear. The results show that models struggle with even this simple structure, which is interesting, but the paper overclaims by framing this as a general evaluation of long-horizon reasoning capabilities.

2. **Limited RL training experiments.** Training experiments use only one base model (R1-Qwen-7B), only math tasks, and up to n=4 composed queries. It is unknown whether the observed benefits generalize to larger models (e.g., 32B or 235B), to code/agent tasks, or to larger composition counts (e.g., n=8+). The claim that R-HORIZON is "scalable" is not supported by the training results.

3. **Questionable expected accuracy metric.** The expected accuracy (Equation 4) is computed as the product of atomic pass rates, implicitly assuming that problem-solving success is independent across problems. However, models may suffer from attention decay, fatigue, or context interference even without explicit dependencies, so the gap between actual and expected accuracy may partly reflect these factors rather than failure to handle dependencies specifically. A stronger baseline would involve presenting the same problems as independent queries in a single prompt without dependencies.

### Minor

1. **Three composition methods mentioned but only one used.** The paper describes Directly Compose, Sequential Compose, and Graphic Compose, but the evaluation and training only use sequential compose for math. The code and agent task construction is described only in the appendix (not provided here), and the results for these tasks appear to use different composition strategies that are not fully explained in the main text.

2. **Descriptive but not causal analysis.** The analyses of reflection, thinking budget, and error position identify correlations but do not establish causal mechanisms. For instance, does the model's early-stop behavior cause performance degradation, or is it a symptom of another underlying limitation?

3. **Limited comparison to prior composition frameworks.** The paper briefly distinguishes from NEST and GSM-Infinite but does not empirically compare against them (e.g., how does R-HORIZON performance degradation compare to NEST's multi-context stress test on the same base models?).

### Trivial

None.

## Nice-to-Haves

- Evaluate RL training benefits on larger models (e.g., 32B) and non-math tasks to test generality.
- Test longer composition horizons (n=8, 16) during training to see if benefits scale.
- Include a controlled baseline where the same problems are presented in a single prompt without explicit dependencies to isolate the effect of dependency handling.
- Compare R-HORIZON's performance degradation patterns with those of NEST or other multi-problem prompting methods on overlapping models.

## Novel Insights

The paper reveals that even frontier LRMs exhibit a finite effective reasoning length—a boundary beyond which performance degrades sharply, and this boundary scales with model size (e.g., ~4-6k tokens for 7B, ~8-10k for 32B on MATH500). The observation that LRMs' reflective behavior is predominantly local (within the current problem) and that they fail to allocate thinking budget appropriately across sequential problems suggests that current architectures lack mechanisms for global reasoning management. The finding that training on composed multi-problem data not only improves multi-horizon performance but also boosts single-problem accuracy and reduces token overhead is particularly interesting—it implies that exposure to dependencies during RL helps models develop more robust and efficient reasoning strategies that generalize to independent tasks.

## Suggestions

1. Strengthen the ecological validity by constructing dependency types beyond arithmetic substitution (e.g., logical entailment, multi-hop QA style dependencies, resource constraints).
2. Add an ablation where problems are presented as independent queries in a single prompt without explicit dependencies to better isolate the effect of dependency handling from general context interference.
3. Expand RL training experiments to at least one larger model (e.g., 32B) and one non-math task to support claims of scalability and generality.

## Score and Decision

I assess this paper as a solid contribution to the evaluation and improvement of LRMs, with clear strengths in comprehensiveness and analytical depth. The main limitations—artificial dependencies and narrow RL experiments—prevent it from being a top-tier contribution but do not invalidate its core findings. The benchmark and training paradigm are likely to be useful to the community as building blocks for further work.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>