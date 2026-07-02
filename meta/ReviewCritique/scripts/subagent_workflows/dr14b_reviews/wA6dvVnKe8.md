### Summary

This paper proposes a model-agnostic adversarial patch attack and corresponding defense strategies for VLA models. The attack, Embedding Disruption Patch Attack (EDPA), can be readily applied to different VLA models without requiring prior knowledge of the model architecture. The paper also introduces an adversarial fine-tuning scheme for the visual encoder to enhance the robustness of VLA models against such attacks. Extensive evaluations on the LIBERO robotic simulation benchmark demonstrate the effectiveness of the proposed attack and defense strategies.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper proposes a model-agnostic adversarial patch attack, EDPA, which can be readily applied to different VLA models without requiring prior knowledge of the model architecture, action space, or the controlled robotic manipulator.
2. The paper introduces an adversarial fine-tuning scheme for the visual encoder, which enhances the robustness of VLA models against adversarial patch attacks.
3. The paper conducts extensive evaluations on the LIBERO robotic simulation benchmark, demonstrating the effectiveness of the proposed attack and defense strategies.

### Weaknesses

#### Some Related Works


#### comment

1. The evaluation is only conducted on a single dataset, LIBERO. It is recommended to evaluate the proposed methods on multiple datasets to demonstrate their generalization capabilities.
2. The paper only compares the proposed attack with two baseline methods, UADA and UPA. It is suggested to include more recent adversarial patch attacks for a comprehensive comparison.
3. The paper lacks ablation studies to analyze the impact of different components of the proposed attack and defense methods. It is recommended to conduct ablation studies to provide more insights into the effectiveness of the proposed methods.

### Suggestions

The paper would benefit significantly from a more thorough evaluation of the proposed attack and defense methods across diverse datasets. While the LIBERO dataset provides a useful starting point, its limitations in terms of task variety and environmental complexity raise concerns about the generalizability of the findings. To address this, the authors should consider evaluating their methods on additional robotic manipulation benchmarks that feature different types of objects, task complexities, and environmental conditions. For example, datasets like CALVIN or RoboMimic could provide a more robust assessment of the proposed approach's performance in more realistic scenarios. This would help to demonstrate the practical applicability of the proposed methods and their ability to generalize beyond the specific conditions of the LIBERO dataset. Furthermore, the evaluation should include a more diverse set of tasks, such as those involving more complex manipulation skills or multi-step procedures, to fully assess the robustness of the proposed attack and defense strategies.

In addition to expanding the evaluation to multiple datasets, the paper should also include a more comprehensive comparison with state-of-the-art adversarial patch attacks. The current comparison with only UADA and UPA is insufficient to fully contextualize the performance of the proposed EDPA attack. The authors should consider including more recent and advanced adversarial patch attack methods, particularly those that have demonstrated strong performance in similar settings. This would provide a more rigorous evaluation of the proposed attack's effectiveness and its advantages over existing approaches. Furthermore, the comparison should not only focus on the attack success rate but also consider other relevant metrics, such as the computational cost and the transferability of the generated adversarial patches to different models or environments. This would provide a more complete picture of the proposed attack's strengths and weaknesses.

Finally, the paper would greatly benefit from a detailed ablation study that analyzes the impact of different components of the proposed attack and defense methods. For the attack, it would be valuable to investigate the effect of varying the size, shape, and location of the adversarial patch, as well as the optimization parameters used to generate the patch. This would provide insights into the sensitivity of the attack to different parameters and help to identify the most critical factors that contribute to its effectiveness. For the defense method, it would be important to analyze the impact of different fine-tuning parameters, such as the learning rate, the number of epochs, and the choice of adversarial examples used for training. This would help to understand the robustness of the defense method and its ability to generalize to different types of adversarial attacks. The ablation study should also include an analysis of the trade-off between robustness and performance on clean examples, which is a critical aspect of any defense strategy.

### Questions

1. How does the size of the adversarial patch affect the performance of the proposed attack and defense methods? It is recommended to conduct an ablation study to analyze the impact of different patch sizes.
2. What is the computational cost of the proposed attack and defense methods? It is suggested to provide a comparison of the computational cost with existing methods.
3. How does the proposed defense method affect the performance of the VLA models on clean inputs? It is important to ensure that the defense method does not degrade the performance of the models on clean inputs.

### Rating

6

### Confidence

3

**********