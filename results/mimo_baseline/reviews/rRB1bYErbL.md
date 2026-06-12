## Summary

The paper proposes R-HORIZON, a method for constructing long-horizon reasoning benchmarks and training data by composing existing single-step problems into multi-step sequences with explicit dependencies. The authors evaluate 25+ LRMs on their benchmark, revealing significant performance degradation as reasoning horizon increases, and demonstrate that RLVR training with composed data improves both multi-horizon and single-horizon reasoning performance.

## Strengths

- **Timely and important research question.** The paper addresses a genuine gap: existing benchmarks evaluate only isolated, single-horizon tasks, while real-world reasoning often requires solving sequences of interdependent problems. The finding that even DeepSeek-R1 drops from 87.3% to 24.6% on AIME25 as composed query count increases from 1 to 5 is striking and well-documented.

- **Comprehensive evaluation scale.** The benchmark covers 6 datasets across math, code, and agentic tasks, with 25+ models ranging from 1.5B to 235B parameters. This breadth provides convincing evidence that the degradation pattern is universal rather than model-specific.

- **Actionable training insights.** The RLVR experiments (Table 1, Figure 4) show that training with composed data yields +7.5 on AIME24 (n=1) and +17.4 on AIME24 (n=2) over single-horizon training, demonstrating that the benchmark is not just diagnostic but also useful for improving models. The rollout efficiency analysis (Figure 10) showing ~20% more effective samples with composed data is a practical contribution for RL training.

- **Detailed failure mode analysis.** The error type decomposition (Figure 5), effective reasoning length analysis (Figure 6), reflection analysis (Figure 7), and thinking budget allocation analysis (Figure 8) provide concrete, interpretable insights into *why* models fail on long-horizon tasks, going beyond simply reporting accuracy numbers.

## Weaknesses

### Fatal
None.

### Major

- **Shallow composition mechanism.** The dependency construction (Algorithm 1) creates dependencies solely through arithmetic substitution of key variables: $f_i(x) \leftarrow x + (m_{i+1} - a_i)$. This means the "dependency" is always a simple linear transformation, and the model's task reduces to correctly propagating a numerical value through a chain. This is a narrow form of long-horizon reasoning and may not generalize to scenarios requiring genuine multi-step planning, state tracking, or complex inter-problem reasoning. The paper would benefit from discussing this limitation and exploring richer dependency types.

- **Limited training experiment scale.** All RLVR experiments are conducted only on R1-Qwen-7B. Given the paper's emphasis on model scale effects in evaluation (larger models degrade less), it is unclear whether the training benefits of composed data hold for larger models or whether the gains diminish. This limits the generalizability of the training contribution.

- **Expected accuracy metric assumes independence.** Equation 4 computes expected accuracy as $\prod p_i$, which assumes each sub-problem is solved independently. However, the composed problems have explicit dependencies, meaning an error in problem $i$ propagates to all subsequent problems. The expected accuracy thus overestimates what a model should achieve, making the gap between actual and expected accuracy appear larger than it may truly be. The paper should acknowledge this and ideally provide a corrected expected accuracy that accounts for error propagation.

### Minor

- **All-or-nothing scoring is very strict.** The binary scoring (Equation 3) means a model solving 15 of 16 sub-problems correctly receives 0 credit. A partial credit metric (e.g., fraction of sub-problems solved) would provide a more nuanced picture and is standard in multi-step evaluation. The paper could include this as a complementary metric.

- **Some table entries appear anomalous.** For instance, Qwen3-32B shows 127.6% accuracy on MATH500 (n=4), which is impossible and likely a parser artifact or error, but the paper does not discuss this. Similarly, several models show non-monotonic accuracy trends (e.g., DeepSeek-R1 on AIME24: 89→76.7→60.1→52.8→67.3), which are not discussed.

- **Code and agentic task construction details are deferred to Appendix A.** Given that the paper claims to cover three task types, the construction methodology for two of them being in an appendix weakens the main paper's self-containedness.

### Trivial
None.

## Nice-to-Haves

- Explore richer dependency structures beyond arithmetic substitution (e.g., logical dependencies, conditional dependencies, graph-structured dependencies as hinted in Figure 2c but not implemented).
- Include a partial-credit metric alongside the all-or-nothing metric.
- Run RLVR experiments on at least one larger model (e.g., 32B) to validate training scalability.
- Provide a corrected expected accuracy that accounts for error propagation through the dependency chain.

## Novel Insights

The paper's most novel insight is that training with composed multi-horizon data improves single-horizon performance more effectively than training with single-horizon data alone (+7.5 on AIME24). This suggests that the structured, sequential nature of composed problems provides a richer training signal that forces models to develop more disciplined reasoning patterns. The rollout efficiency analysis further supports this: composed data yields ~20% more effective training samples by reducing the fraction of "solve all" (trivially easy) and "solve none" (impossibly hard) rollouts, creating a more balanced reward distribution. This has practical implications for RLVR data curation beyond the specific benchmark proposed here.

## Suggestions

- Add a partial-credit evaluation metric (fraction of sub-problems correct) to complement the all-or-nothing metric, as this would reveal more about where models succeed and fail in the chain.
- Discuss the non-monotonic accuracy trends observed for some models (e.g., DeepSeek-R1 on AIME24) and investigate whether these reflect genuine model behaviors or evaluation artifacts.
- Expand RLVR experiments to at least one model beyond 7B scale to validate that training benefits are not scale-dependent.

## Score and Decision

The paper presents a well-motivated and comprehensive study on long-horizon reasoning in LRMs. The benchmark is extensive, the evaluation is thorough, and the training results are practically useful. However, the composition mechanism is quite shallow (simple arithmetic substitution), which limits the claim about evaluating "long-horizon reasoning" in a meaningful sense, and the training experiments are restricted to a single small model. These are significant but not fatal limitations. The paper makes a solid contribution to an important and underexplored problem area.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept