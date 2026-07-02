### Summary

The paper proposes Generative Trajectory Policies (GTPs), a novel approach for offline reinforcement learning (RL) that utilizes generative models to capture complex, multi-modal behaviors from offline datasets. The authors highlight the trade-offs between existing generative models, such as diffusion policies, which offer high expressiveness but are computationally intensive, and consistency models, which are efficient but less performant. GTPs aim to bridge this gap by leveraging a unified framework based on Ordinary Differential Equations (ODEs) to model policy trajectories. The authors introduce two key adaptations to make GTPs practical for offline RL: a score approximation technique for stable training and a value-driven guidance mechanism for policy improvement. The proposed method is evaluated on D4RL benchmarks, where it achieves competitive performance, particularly excelling in challenging tasks like AntMaze.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. Theoretical Foundation: The paper provides a rigorous theoretical framework that connects various generative models through the lens of ODEs, offering valuable insights into the design of generative policies for RL.
2. Innovation: The introduction of GTPs and the unified ODE framework represents a creative combination of ideas from generative modeling and RL, addressing a critical challenge in offline RL.
3. Performance: Empirical results demonstrate that GTPs achieve state-of-the-art performance on several benchmarks, showcasing their effectiveness in capturing complex behaviors and improving policy performance.
4. Comprehensive Evaluation: The authors conduct extensive experiments, including ablation studies, to validate the contributions of different components of the proposed method.

### Weaknesses

#### Some Related Works


#### comment

1. Complexity: The paper introduces a sophisticated framework that might be challenging for practitioners to implement. Providing more implementation details and guidelines could enhance the accessibility of the proposed method.
2. Limited Exploration of Limitations: The paper could benefit from a more thorough discussion of the limitations of GTPs, such as scenarios where the method might fail or underperform compared to simpler approaches.
3. Hyperparameter Sensitivity: There is insufficient discussion on the sensitivity of GTPs to hyperparameter settings, which is crucial for understanding the robustness and practical applicability of the method.

### Suggestions

The paper would greatly benefit from a more detailed exposition of the implementation specifics, particularly concerning the neural network architectures used for the generative model and the critic. For example, the specific choices of activation functions, layer normalization, and the number of layers in both the actor and critic networks are crucial for reproducibility and practical adoption. Furthermore, the paper should elaborate on the optimization algorithms used, including the learning rate schedules, batch sizes, and the specific loss functions employed for both the actor and critic. Providing these details, perhaps in a dedicated appendix or as part of the main text, would significantly lower the barrier to entry for researchers and practitioners interested in utilizing GTPs. It would also be beneficial to include a discussion on the computational resources required for training, such as the GPU memory footprint and the training time, to give a clear picture of the practical demands of the method.

To address the lack of discussion on limitations, the authors should explore scenarios where GTPs might struggle. For instance, how does the method perform in environments with extremely sparse rewards or in situations where the offline dataset is highly biased or lacks sufficient coverage of the state space? A comparative analysis against simpler methods, such as behavior cloning or offline versions of standard RL algorithms, in these challenging scenarios would be insightful. Additionally, the paper should discuss the potential failure modes of the score approximation technique and the value-driven guidance mechanism. Understanding these limitations is crucial for practitioners to know when GTPs are appropriate and when alternative methods might be more suitable. A more thorough investigation into these aspects would strengthen the paper's overall impact and credibility.

Finally, a more detailed analysis of hyperparameter sensitivity is essential. The paper should include a systematic study of how different hyperparameters affect the performance of GTPs. For example, how does the learning rate, the number of hidden layers, the size of the latent space, and the weight decay parameters influence the final performance? The authors should provide guidelines on how to select these parameters, possibly through a sensitivity analysis or a grid search. Furthermore, the paper should discuss the robustness of the method to different initialization schemes and random seeds. This analysis would help practitioners understand the practical considerations involved in deploying GTPs and ensure that the reported results are not overly sensitive to specific hyperparameter choices.

### Questions

1. Could the authors provide more details on the computational requirements of GTPs compared to existing methods?
2. How do GTPs perform in environments with sparse rewards or limited data?
3. Can the authors discuss potential extensions of GTPs to online or on-policy settings?

### Rating

6

### Confidence

3

**********