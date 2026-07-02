### Summary

This paper introduces Dynamic Nested Depth (DND), a novel method that improves the performance of off-the-shelf LLMs by selecting critical tokens for reprocessing in a nested depth manner. Specifically, at the end of the given transformer layer, DND identifies more critical tokens with a router and feeds them back for an extra round of processing, effectively “reviewing” difficult tokens while avoiding redundant computation for easier ones. The dynamic selection mechanism is tailored for precise control via two novel strategies: a router controlling loss to enhance token selection distinguishability, and a threshold control scheme to ensure selection stability.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The proposed method is novel and effective. It is a post-training method that can be directly integrated into existing dense and Mixture-of-Experts (MoE) architectures through post-training to achieve notable performance gains with minimal parameter and computation increase.
2. The paper is well-written and easy to follow.
3. The authors provide extensive experiments to demonstrate the effectiveness of the proposed method.

### Weaknesses

#### Some Related Works


#### comment

1. The authors should provide more details about the synthetic data used for training, such as the data sources and construction methods.
2. The authors should provide more details about the training process, such as the training steps and batch size.
3. The authors should provide more details about the hyperparameters used in the experiments, such as the values of $\lambda_{sd}$, $\lambda_{dp}$, $\alpha$, and $\gamma$.

### Suggestions

The paper would benefit from a more detailed explanation of the synthetic data generation process. Specifically, the authors should clarify the types of tasks or domains from which the seed data is derived, and the specific rules or models used to expand this seed data into a larger synthetic dataset. For example, if the seed data consists of question-answer pairs, the authors should describe how they generate new questions and answers that maintain the same structure and complexity as the original data. Furthermore, it would be beneficial to understand the quality control measures used to ensure the synthetic data is of high quality and does not introduce noise or bias into the training process. This level of detail is crucial for the reproducibility of the results and for assessing the generalizability of the proposed method.

Regarding the training process, the authors should provide a more comprehensive description of the training procedure. This includes specifying the exact number of training steps, the batch size used, the learning rate schedule, and the optimization algorithm. It would also be helpful to know if any specific techniques, such as gradient clipping or learning rate warm-up, were used to stabilize the training process. Furthermore, the authors should clarify whether the model is trained end-to-end or if there are any specific training stages. Providing these details will allow other researchers to replicate the training process and compare the results with other methods. Additionally, the authors should discuss the computational resources required for training, such as the number of GPUs and the training time, to provide a better understanding of the practical feasibility of the proposed method.

Finally, the paper needs a more thorough discussion of the hyperparameter selection process. The authors should provide the specific values used for $\lambda_{sd}$, $\lambda_{dp}$, $\alpha$, and $\gamma$, and explain how these values were chosen. It would be beneficial to include an ablation study that shows the impact of each hyperparameter on the performance of the model. This would help to understand the sensitivity of the method to different hyperparameter settings and provide guidance for future users of the method. Furthermore, the authors should discuss the range of values explored for each hyperparameter and the criteria used to select the optimal values. This level of detail is essential for the reproducibility and practical application of the proposed method.

### Questions

Please refer to the Weaknesses.

### Rating

6

### Confidence

3

**********