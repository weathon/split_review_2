## Summary

This paper introduces a Graph Attention Network (GAT)-based policy representation for the co-design of morphology and control in soft robots. The authors model robots as graphs, using GATs with DRL to enable controller inheritance across morphological mutations through a topology-consistent weight mapping procedure. Experiments on four EvoGym tasks show that the GAT-based approach achieves higher final fitness and stronger robustness to morphological variations compared to MLP-only co-design baselines.

## Strengths

- **Novel and well-motivated problem framing**: The paper addresses the genuine challenge of controller inheritance under morphological mutation in soft robot co-design. The core idea that graph-structured policies can naturally handle variable sensor/actuator configurations is both intuitive and principled.

- **Clear technical contribution**: The MAPWEIGHTS algorithm (Algorithm 2) provides a concrete, implementable procedure for transferring GAT-based controllers across morphologies with changing node counts. The separation of shared GAT layers, fully transferred MLP hidden layers, and per-actuator output heads is a clean design.

- **Comprehensive empirical evaluation on a standardized benchmark**: The experiments cover four distinct tasks of varying difficulty (Pusher-v1, Thrower-v0, Carrier-v1, Catcher-v0) on EvoGym, comparing against both the prior MLP transfer method (Harada & Iba, 2024) and the from-scratch baseline (Bhatia et al., 2021). Qualitative visualizations of evolved morphologies and throwing trajectories add useful context.

## Weaknesses

### Major

1. **Insufficient statistical rigor**: Results are reported over only three runs with standard deviation. Given the high variance typical of evolutionary algorithms plus deep RL, three runs are insufficient to draw reliable conclusions about statistical significance. No hypothesis tests, effect sizes, or confidence intervals are provided. The claims that GAT methods "consistently match or surpass" MLP baselines are not supported by appropriate statistical evidence.

2. **Missing ablation that isolates the contribution of graph representation vs. inheritance mechanism**: The paper compares (a) GAT+inheritance, (b) GAT+global mean, (c) MLP+inheritance, and (d) MLP+no inheritance. However, there is no ablation that uses a GAT policy *without* inheritance (i.e., training from scratch each generation). Without this, it is unclear whether the observed gains come from the graph policy architecture itself, the inheritance procedure, or their interaction. This is a critical missing control experiment.

3. **Limited architecture exploration and justification**: The paper uses a single GAT layer with one attention head. Modern graph network literature for control typically uses deeper architectures, residual connections, or multi-head attention with more heads. The authors do not justify this minimal design or explore whether performance improves with more GAT layers or more attention heads. Similarly, no sensitivity analysis is performed on the choice of node features or graph construction.

### Minor

1. **The performance advantage on Carrier-v1 is negligible**: All four methods converge to similar high fitness. While the paper notes this, it still frames the results as supporting the GAT advantage. The claim that GAT methods show "robustness" on Carrier-v1 is not quantitatively supported when all methods achieve near-identical terminal performance.

2. **The role of attention is not directly validated**: The paper claims attention helps the policy "identify how specific sensor-actuator interactions shape movement," but no attention weight analysis is provided. Visualizing or quantifying which edges receive high attention would substantiate this claim.

3. **Computational cost is not reported**: The paper acknowledges that GAT controllers can converge slower, but provides no wall-clock time or iteration-count comparison. The reader cannot assess whether the improved asymptotic performance justifies the additional computational expense.

## Nice-to-Haves

- A head-to-head comparison against the Kurin et al. (2021) Transformer-based controller on the same EvoGym tasks would strengthen the paper, given that the authors cite it as showing GNNs can be outperformed by Transformers in incompatible control settings.
- Reporting results with more random seeds (e.g., 10 or 20) and using bootstrapped confidence intervals or Mann-Whitney U tests would substantially increase confidence in the conclusions.
- An ablation where GAT controllers are trained from scratch each generation (no inheritance) would cleanly separate the effect of graph policies from the effect of inheritance.

## Novel Insights

The most genuinely novel insight is that the *combinatorial structure* of a graph policy—specifically, inheriting shared GAT parameters while only randomly initializing output weights for new actuators—provides a natural inductive bias for transferring control knowledge under morphological change. This is distinct from prior MLP-based inheritance work (Harada & Iba, 2024) which had to rely on ad-hoc heuristic mappings. The observation that local node features outperform global mean features on tasks requiring fine-grained coordination (Pusher, Thrower) while global features excel on whole-body synchronization tasks (Catcher) is also an interesting empirical finding that could guide future architecture choices.

## Suggestions

Add an ablation experiment: "GA-GAT-PPO-NoInheritance" where GAT controllers are trained from scratch after each morphological mutation. This would directly isolate whether the advantage comes from the graph representation, the inheritance mechanism, or both.

## Score and Decision

The paper addresses an important and recognized problem in embodied intelligence and evolutionary robotics. The core idea is sound and the methodology is well-motivated. However, the experimental evaluation is underpowered (3 runs only) and missing a critical control ablation. These issues prevent full confidence in the paper's central claims. With stronger statistical evidence and the suggested ablation, the paper would be a clear accept. In its current form, the empirical support is not strong enough.

**Score**: 5 (borderline reject, leaning toward reject mainly due to insufficient statistical evidence and missing ablation)

**MY FINAL SCORE**: <score>5</score>
**MY FINAL DECISION**: <decision>Reject</decision>