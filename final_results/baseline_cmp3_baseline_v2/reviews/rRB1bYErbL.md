## Summary

The paper proposes R-HORIZON, a method that composes existing single-step problems into multi-step reasoning sequences with explicit numerical dependencies. Using this method, the authors construct a benchmark spanning math, code, and agent tasks, and evaluate 26 LRMs, revealing substantial performance degradation as reasoning horizon increases. They further use R-HORIZON to create training data for reinforcement learning with verifiable rewards (RLVR), showing that training on composed data improves both multi-horizon performance and original single-task accuracy. The work addresses the underexplored gap of evaluating and training LRMs on interdependent, multi-step reasoning.

## Strengths

- **Addresses an important gap**: Current benchmarks overwhelmingly evaluate single, isolated problems, while real-world reasoning often requires handling multiple interdependent tasks. R-HORIZON directly targets this underexplored dimension.
- **Comprehensive evaluation with clear findings**: The evaluation spans 26 models (including closed-source models like o4-mini, Gemini-2.5-Pro, Claude-Sonnet-4) across three domains (math, code, agent). The consistent degradation trend is clearly documented and visually presented, providing strong empirical evidence that even the most advanced LRMs struggle with multi-horizon reasoning.
- **Insightful analysis of failure modes**: The paper goes beyond aggregate numbers to analyze error types (problem reasoning errors, dependency errors, early stopping, truncation), effective reasoning length, reflection scope, and thinking budget allocation. These analyses provide actionable insights about *why* performance degrades.
- **Meaningful RL training results**: Training R1-Qwen-7B with composed data yields substantial improvements on both composed tasks (e.g., +17.4 on AIME24 n=2) and original single-problem tasks (+7.5 on AIME24). The analysis of rollout efficiency and thinking budget allocation further strengthens the training contribution.
- **Practical and low-cost methodology**: R-HORIZON repurposes existing benchmarks, making it easy to adopt without requiring new data collection. The composition pipeline is clearly described and reproducible.

## Weaknesses

### Fatal

None.

### Major

- **Artificial dependency construction limits ecological validity**: The dependency mechanism relies entirely on extracting integers and creating simple arithmetic substitutions (e.g., *v = a_i + (m_{i+1} - a_i)*). While this creates formal dependencies, real multi-horizon reasoning often involves qualitative, logical, or constraint-based dependencies that are not reducible to integer arithmetic. The paper does not sufficiently discuss whether insights from this synthetic setup transfer to more natural multi-step scenarios.
- **Training experiments are limited in scope**: Only one base model (R1-Qwen-7B) is trained, and only on math tasks. The maximum composed query count is 4. While the authors show generalization to longer horizons during evaluation, the training findings need verification on larger models and across code/agent domains. The claim that R-HORIZON is "scalable" is not well-supported by the training experiments.
- **No direct comparison to simpler baselines**: The paper mentions NEST (concatenating independent problems) but does not systematically compare R-HORIZON to simply concatenating problems without dependencies, or to training on longer independent problem sequences. Such ablations would isolate the specific benefit of *dependencies* versus *longer context*.
- **Some evaluation results are anomalous**: On WebShaper, several models (e.g., o4-mini, DeepSeek-R1) show *higher* accuracy on composed queries than on single queries, or non-monotonic trends. This suggests that the dependency construction or evaluation protocol for agent tasks may have confounds, and the paper does not adequately explain these anomalies.

### Minor

- The "expected accuracy" metric (product of pass rates) assumes independence between sub-problems. While useful as a heuristic, the gap between actual and expected accuracy conflates two factors: (1) failure due to increased reasoning length/compound difficulty and (2) failure to handle dependencies. The paper does not attempt to disentangle these.
- The table in Figure 3 contains an impossible value (127.6 for Qwen3-32B on MATH500 n=4), which suggests a parsing or transcription error. While this is likely a formatting artifact from PDF extraction, it reduces confidence in the data.
- The code and agent task construction is relegated to the appendix with limited detail. The quality and validity of these datasets are harder to assess than the math construction.

### Trivial

None.

## Nice-to-Haves

- Training on larger models (e.g., 32B or 70B) would significantly strengthen the claim that R-HORIZON is a scalable training paradigm.
- Evaluating trained models on other long-horizon reasoning benchmarks (e.g., GSM-Infinite, agent planning tasks with natural dependencies) would test generalization beyond the R-HORIZON construction itself.
- A study of how the difficulty of the composed problems (e.g., varying the complexity of the dependency function) affects performance would deepen the understanding.

## Novel Insights

The most interesting finding is that training on composed problems not only improves multi-horizon performance but also *reduces overthinking* on single problems — the model learns to allocate thinking budget more efficiently and produces shorter responses. This suggests that multi-step dependencies provide a form of regularization or learning signal that encourages the model to balance depth across steps rather than over-investing in the first problem. Additionally, the observation that reflection in LRMs is highly localized (confined to the current problem) points to a fundamental limitation in current reasoning architectures that is not captured by single-problem evaluations.

## Suggestions

- Add an ablation that compares R-HORIZON composed data to training on the same number of independent problems (without dependencies) matched for total difficulty or token length. This would isolate whether the benefits come from the dependency structure or simply from having more total reasoning steps in the training data.
- Include an analysis of the sensitivity to the type of dependency function (e.g., nonlinear functions, string substitutions) to understand how general the construction is.
- For the anomalous WebShaper results, clarify whether the dependency constraint is actually enforced during evaluation (i.e., does the model truly need to use previous answers, or could it solve problems independently?).
- Fix the parsing error in the table and ensure all accuracy values are valid.

## Score and Decision

The paper addresses an underexplored problem, provides a useful benchmark with extensive evaluation, and demonstrates a promising training approach. However, the artificial nature of the dependency construction and the limited training scope (one model, one domain) temper the strength of the claims. The contribution is solid but not exceptional.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>