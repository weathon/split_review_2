### Summary

This paper addresses the issue of plasticity loss in deep reinforcement learning (RL) by analyzing the optimization dynamics of RL agents. The authors develop a theoretical framework that reveals two key mechanisms contributing to plasticity loss: the rank deficiency of the Neural Tangent Kernel (NTK) and the decay of gradient magnitude. To combat this, they propose Sample Weight Decay (SWD), a lightweight method that adjusts the sampling probability of data in the replay buffer based on its age. SWD aims to maintain the gradient magnitude and sustain the learning capacity of neural networks. The method is evaluated on various RL benchmarks, including MuJoCo, ALE, and DMC, demonstrating consistent performance improvements across different RL algorithms and environments.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper provides a novel theoretical analysis of plasticity loss in RL, linking it to specific mechanisms like NTK rank deficiency and gradient decay.
2. SWD is a simple yet effective method that can be easily integrated into existing RL algorithms.
3. The empirical results are comprehensive, showing consistent improvements across multiple benchmarks and algorithms.

### Weaknesses

#### Some Related Works


#### comment

1. The theoretical analysis primarily focuses on gradient decay, with limited exploration of how SWD directly addresses the rank collapse of the NTK Gram matrix, leaving a gap in fully explaining its theoretical effectiveness against all identified causes of plasticity loss.
2. The paper’s evaluation is limited to specific RL algorithms and environments, which may not fully demonstrate SWD’s generalizability across a broader range of RL tasks and architectures.
3. The method relies on specific hyperparameters, such as decay rate and minimum weight, which may require careful tuning for different environments, potentially limiting its ease of use in practice.
4. The paper does not extensively compare SWD with other existing plasticity-preserving methods, such as network reset or noise injection, which could provide a more comprehensive understanding of its relative advantages and limitations.

### Suggestions

The paper would benefit from a more thorough investigation into the relationship between Sample Weight Decay (SWD) and the Neural Tangent Kernel (NTK) rank collapse. While the authors identify NTK rank deficiency as a contributing factor to plasticity loss, the theoretical analysis primarily focuses on gradient decay. A deeper analysis should explore how SWD's age-based weighting scheme impacts the NTK's eigenvalue spectrum, and whether it can prevent or mitigate the rank collapse. For instance, the authors could investigate if the proposed weighting scheme leads to a more uniform distribution of the NTK's eigenvalues, which would indicate a more stable and expressive network. Furthermore, it would be beneficial to analyze the sensitivity of SWD to the choice of the decay rate and minimum weight, and how these parameters affect the NTK's properties. This analysis could provide a more complete picture of how SWD addresses the identified causes of plasticity loss.

To strengthen the empirical evaluation, the authors should consider expanding their experiments to include a wider range of RL algorithms and environments. While the current evaluation covers several benchmarks, it is limited to specific algorithms like SAC, TD3, and Double DQN. Testing SWD on other algorithms, such as PPO or A3C, would provide a more comprehensive understanding of its generalizability. Additionally, the authors should consider evaluating SWD on more complex and diverse environments, including those with sparse rewards or high-dimensional state spaces. This would help to demonstrate the robustness of SWD and its ability to handle different types of challenges. Furthermore, it would be valuable to analyze the performance of SWD in long-horizon tasks, where plasticity loss is often more pronounced. Such an analysis would provide a more complete picture of SWD's effectiveness in various RL scenarios.

Finally, the paper should include a more detailed comparison of SWD with other existing plasticity-preserving methods. While the authors mention network reset and noise injection, they do not provide a thorough comparison. A direct comparison with these methods would help to highlight the advantages and limitations of SWD. For example, the authors could compare the computational cost of SWD with that of network reset, or analyze the sensitivity of SWD to its hyperparameters compared to noise injection. Furthermore, it would be beneficial to explore whether SWD can be combined with these other methods to achieve even better performance. Such an analysis would provide a more complete understanding of the relative strengths and weaknesses of SWD and its potential for practical application.

### Questions

1. How does SWD theoretically mitigate the rank collapse of the NTK Gram matrix, as this is not fully addressed in the theoretical analysis?
2. Can the authors provide additional experiments or analysis demonstrating SWD’s effectiveness across a wider variety of RL tasks and neural network architectures?
3. How sensitive is SWD to the choice of hyperparameters, such as decay rate and minimum weight, and can the authors provide guidelines for setting these in different environments?
4. How does SWD compare with other plasticity-preserving techniques, such as network reset or noise injection, in terms of performance and computational efficiency?

### Rating

6

### Confidence

3

**********