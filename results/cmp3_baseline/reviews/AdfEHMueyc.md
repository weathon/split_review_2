## Summary

This paper proposes a co-design algorithm for soft robots that integrates Graph Attention Networks (GATs) with deep reinforcement learning to enable morphology-aware controller inheritance during evolution. The key idea is to represent robots as graphs, use GATs as policies that can handle varying numbers of sensors and actuators, and introduce a weight-mapping procedure (MAPWEIGHTS) that transfers learned parameters from parent to offspring when morphology changes. Experiments on the EvoGym benchmark across four tasks show that the GAT-based approach achieves higher final fitness and lower variance compared to MLP-based baselines.

## Strengths

- **Novel and well-motivated problem framing**: The paper correctly identifies a fundamental challenge in embodied intelligence co-design—that morphological changes break fixed-architecture MLP policies—and proposes a principled graph-based solution. The motivation for using GNNs to handle varying sensor/actuator layouts is clear and compelling.
- **Clean technical contribution**: The MAPWEIGHTS algorithm (Algorithm 2) provides a concrete, well-specified procedure for transferring GAT-based controllers across morphological changes, with clear rules for shared layers, matched actuators, new actuators, and removed actuators. This is a non-trivial engineering contribution that directly addresses the brittle inheritance problem.
- **Empirical validation on standardized benchmark**: The paper evaluates on four tasks from EvoGym, a recognized benchmark, and compares against two meaningful baselines (MLP with inheritance from scratch, MLP with transfer). The results show consistent improvements in final fitness and variance reduction.

## Weaknesses

### Fatal
None.

### Major
1. **Limited architectural exploration and missing ablations**: The paper uses a single GAT layer with one round of message passing. Given that the core claim is about graph-structured policies being superior, the paper does not ablate the GAT design choices (number of layers, attention heads, message passing rounds) or compare against simpler GNN variants (e.g., GCN, GraphSAGE). Without these ablations, it is unclear whether the benefits come from the graph structure itself, the attention mechanism, or specific architectural choices. The paper also does not compare against a fully-connected Transformer baseline, which Kurin et al. (2021) showed can outperform GNNs in incompatible control settings.

2. **Limited statistical rigor**: The paper reports results from only three independent runs per condition. Given the high variance inherent in evolutionary robotics and RL, three runs provide insufficient statistical power to draw reliable conclusions. The paper does not report any statistical significance tests (e.g., t-tests, Mann-Whitney U, confidence intervals) to support claims that GAT methods "consistently match or surpass" baselines. The standard deviation shading in Figure 3 shows substantial overlap between methods in several tasks (e.g., Carrier-v1), making it difficult to assess whether differences are meaningful.

3. **Incomplete comparison with prior work**: The paper compares against GA-MLP-PPO-Transfer (Harada & Iba, 2024) and GA-MLP-PPO (Bhatia et al., 2021), but does not compare against other graph-based or morphology-aware approaches that have been applied to EvoGym or similar benchmarks. Notably, the paper mentions NerveNet (Wang et al., 2018) and the Transformer-based approach from Kurin et al. (2021) in related work but does not include them as baselines. Given that Kurin et al. found that Transformers can outperform GNNs in incompatible control, this omission weakens the claim that GATs are the best choice for this setting.

4. **Limited analysis of the inheritance mechanism**: The paper claims that inheritance accelerates adaptation, but does not provide direct evidence. There is no ablation comparing GAT with inheritance vs. GAT without inheritance (training from scratch each generation). The comparison is only between GAT-with-inheritance and MLP-with/without-inheritance. Without this ablation, it is impossible to attribute the performance gains to the graph structure, the inheritance mechanism, or their combination. Additionally, the paper does not measure or report the number of training steps/episodes required per generation, which would directly demonstrate the claimed acceleration.

### Minor
1. **Single GAT layer**: The paper uses only one GAT layer with one round of message passing. While this is a design choice, it limits the ability to capture multi-hop dependencies in the robot's structure. The paper should discuss why deeper architectures were not explored or why a single layer is sufficient.
2. **Limited task diversity**: All four tasks involve box manipulation (pushing, throwing, carrying, catching). The paper would benefit from including locomotion-only tasks (e.g., Walker-v0, Climber-v0 from EvoGym) to demonstrate generality beyond object manipulation.
3. **No analysis of computational cost**: The paper does not compare training time, inference time, or parameter counts between GAT and MLP methods. Given that GATs are more complex, it would be useful to know whether the performance gains come at a significant computational cost.

### Trivial
- The paper states "for g = 1 ... p" in Algorithm 1 line 2, which should be "for g = 1 ... n" (using the max generations parameter n).
- The paper uses "p" for both population size and max generations in Algorithm 1, which is confusing.

## Nice-to-Haves
- An ablation comparing GAT-with-inheritance vs. GAT-without-inheritance (training from scratch each generation) would directly measure the benefit of the inheritance mechanism.
- Including a Transformer-based baseline (as in Kurin et al., 2021) would strengthen the claim that GATs are the appropriate architecture for this setting.
- Reporting the number of PPO training steps per generation would quantify the claimed acceleration from inheritance.
- Statistical significance tests (e.g., Mann-Whitney U) on final fitness distributions across runs would strengthen the empirical claims.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add an ablation comparing GAT-with-inheritance vs. GAT-without-inheritance (training from scratch each generation) to isolate the effect of the inheritance mechanism from the graph architecture.
2. Include a Transformer-based baseline (following Kurin et al., 2021) to test whether the benefits are specific to GATs or general to any permutation-invariant architecture.
3. Report the number of PPO training steps per generation for each method to quantify the claimed acceleration from inheritance.
4. Add statistical significance tests (e.g., Mann-Whitney U) comparing final fitness distributions across the three runs for each task.
5. Include at least one locomotion-only task (e.g., Walker-v0) to demonstrate generality beyond object manipulation.

## Score and Decision

The paper addresses a well-motivated problem (morphology-aware controller inheritance in soft robot co-design) with a clean technical contribution (GAT-based policies with topology-consistent weight mapping). The empirical results on EvoGym are positive and consistent across four tasks. However, the paper has several significant limitations: (1) the lack of an ablation isolating the inheritance mechanism from the graph architecture, (2) insufficient statistical rigor (only 3 runs, no significance tests), (3) missing comparisons against other graph-based or Transformer baselines, and (4) limited architectural exploration. These issues prevent the paper from being a definitive contribution, but the core idea is sound and the results are promising. The paper would benefit from additional experiments and analysis before being ready for acceptance.

MY FINAL SCORE: 5.0score</score>
MY FINAL DECISION: Rejectdecision</decision>