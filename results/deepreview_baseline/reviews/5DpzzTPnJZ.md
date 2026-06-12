## Summary

This paper studies plasticity loss in deep reinforcement learning from a theoretical perspective. The authors identify two causal mechanisms: rank collapse of the Neural Tangent Kernel (NTK) Gram matrix and a Θ(1/t) decay of gradient magnitude. Focusing on the second mechanism, they propose Sample Weight Decay (SWD), a lightweight method that assigns higher sampling weights to more recent experiences in the replay buffer to counteract gradient attenuation. Experiments on MuJoCo, ALE, and DMC tasks with TD3, Double DQN, and SAC demonstrate consistent performance improvements.

## Strengths

- **Theoretical grounding of plasticity loss**: The paper provides a formal theoretical analysis connecting plasticity loss to gradient attenuation with a Θ(1/k) decay pattern, which goes beyond purely empirical observations common in prior work. Theorem 3 explicitly characterizes how distributional shift and target drift contribute to gradient decay at initialization.

- **Principled and lightweight method**: SWD is a simple, theoretically motivated intervention that operates at the data distribution level via experience replay weighting, requiring minimal computational overhead. The method is orthogonal to existing network-level approaches (e.g., network reset, neuron recycling), enabling synergistic combinations as demonstrated in Section 6.5.

- **Comprehensive empirical validation**: The paper evaluates SWD across three distinct benchmark suites (MuJoCo, ALE, DMC), three different RL algorithms (TD3, Double DQN, SAC), and multiple network architectures. The use of aggregate reliable metrics (IQM, Median, Mean, Optimality Gap) with stratified bootstrap confidence intervals follows best practices in RL evaluation.

- **Reverse validation and ablation studies**: The SWA (Sample Weight Augmentation) counterfactual experiment in Section 6.2 provides strong evidence that the temporal weighting direction is causally important, not just any non-uniform sampling. The GraMa metric analysis directly links SWD to maintained plasticity.

## Weaknesses

### Fatal
None.

### Major
- **Theoretical gap between analysis and method**: Theorem 3 characterizes gradient decay at the *initialization* of each iteration (evaluated at the previous iteration's minimizer), but SWD operates on the *sampling distribution* during training. The paper does not rigorously prove that SWD's age-based weighting actually restores the gradient magnitude to a specific desired scale or that it counteracts the Θ(1/k) decay in a precise mathematical sense. The connection between the theoretical result and the algorithmic design is intuitive but not formally established.

- **Limited comparison to existing replay buffer methods**: The paper compares SWD only to PER (Prioritized Experience Replay) in Figure 4, but there is a rich literature on experience replay weighting strategies (e.g., Hindsight Experience Replay, Energy-Based Prioritization, LaBER, etc.) that are not discussed or compared. The claim that SWD is "orthogonal to existing methods" is well-supported for network-level methods, but the paper does not adequately position SWD within the existing replay buffer literature.

- **Incomplete ablation of the linear decay assumption**: The theoretical analysis identifies a Θ(1/k) decay, but SWD uses a *linear* decay weighting scheme (1 - age/T). The paper compares linear vs. exponential vs. polynomial decay in Appendix F (Table 13), but does not test a weighting scheme that directly mirrors the 1/k form. The connection between the theoretical decay rate and the practical weighting function is not fully explored.

### Minor
- **Theoretical scope limited to FQI**: The analysis is conducted for Fitted Q-Iteration, and the paper claims it extends to entropy-regularized MDPs (Appendix B.4) and value-based methods, but the extension to actor-critic methods (SAC, TD3) used in experiments is not explicitly proven. The paper would benefit from a clearer statement of which theoretical results carry over to which algorithm classes.

- **Hyperparameter sensitivity not fully characterized**: While Section 6.6 mentions low sensitivity to T and w_min, the results are only shown in the appendix. The main text would benefit from a brief summary of the range of effective hyperparameters.

- **Bucket-based approximation not evaluated in main text**: The compute-efficient approximation (Table 2 in Appendix D) is mentioned but not discussed in the main experimental results. Given that computational overhead is a practical concern, this deserves more prominence.

### Trivial
- The paper uses "GramA" and "GraMa" interchangeably; consistency would improve readability.

## Nice-to-Haves

- A direct comparison with other replay weighting methods beyond PER (e.g., LaBER, energy-based prioritization) would strengthen the empirical contribution.
- An analysis of how SWD interacts with different replay buffer sizes would be informative for practitioners.
- A theoretical or empirical analysis of the optimal decay schedule (beyond linear) could further improve the method.

## Novel Insights

The paper's key insight is that plasticity loss in RL can be decomposed into two distinct mechanisms—NTK rank collapse and gradient magnitude decay—and that the gradient decay follows a specific Θ(1/k) pattern tied to the non-stationarity of the data distribution. This provides a theoretical lens through which existing empirical methods (network reset, neuron recycling) can be understood as addressing the first mechanism, while SWD addresses the second. The insight that gradient attenuation is driven by the 1/k coefficient in the distributional shift term (Theorem 3) and that this can be counteracted by age-based reweighting is genuinely novel and opens a new axis for plasticity-preserving interventions.

## Suggestions

- Provide a more rigorous theoretical connection between the Θ(1/k) gradient decay and the linear weighting scheme of SWD. Specifically, show that SWD's sampling distribution approximately restores the gradient magnitude to a scale independent of k, or characterize the residual decay after applying SWD.
- Include a comparison with at least one additional replay weighting method (e.g., LaBER or a simple recency-based baseline) to better contextualize SWD's performance.
- Move the hyperparameter sensitivity analysis (Table 12) and the bucket-based approximation results (Table 2) to the main text, as they address practical concerns about usability and computational cost.

## Score and Decision

The paper makes a meaningful theoretical contribution to understanding plasticity loss in RL and proposes a simple, effective, and well-motivated method. The empirical evaluation is thorough across multiple algorithms, environments, and metrics. The main weaknesses are the gap between the theoretical analysis and the algorithmic design, and the limited comparison to other replay buffer methods. However, these do not invalidate the core contribution. The paper is a solid contribution to the field.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>