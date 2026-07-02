### Summary

This paper introduces Vidar, a method for learning robotic policies with less data through the use of a large, pre-trained video diffusion model and a masked inverse dynamics model. The video diffusion model is pre-trained on a large-scale dataset of internet videos, then fine-tuned on a smaller dataset of robot demonstrations. The masked inverse dynamics model learns to predict actions from the video diffusion model's generated videos, focusing only on action-relevant parts of the image. Vidar is evaluated on a variety of simulated and real-world tasks, demonstrating improved performance over baselines in low-data settings.

### Soundness

2

### Presentation

3

### Contribution

3

### Strengths

- The paper is well-written and easy to follow. The three-stage training pipeline (pre-training, embodied domain pre-training, and target domain fine-tuning) is clearly explained, as is the unified observation space and the use of multi-view data.
- The use of a video diffusion model as a prior for robot learning is an interesting approach that has the potential to significantly reduce the amount of data required to train robust policies.
- The proposed method demonstrates impressive results on a variety of tasks in both simulation and real-world settings, outperforming baselines in low-data regimes and generalizing well to unseen tasks and backgrounds.

### Weaknesses

#### Some Related Works


#### comment

 - The paper's method requires significant computational resources for training and inference, which may limit its accessibility. The authors should provide more details on the specific hardware requirements and training times. In addition, the authors should consider releasing their code and pre-trained models to the community to facilitate reproducibility and further research.
- The paper does not provide a detailed analysis of the limitations of the proposed method. For example, how does the method perform on tasks that require more complex reasoning or manipulation skills? What are the failure modes of the video diffusion model and the masked inverse dynamics model? Addressing these questions would provide a more complete picture of the method's capabilities and limitations.
- The paper does not adequately address the ethical implications of using large-scale video datasets for robot learning. For example, what are the potential biases in the datasets, and how might these biases affect the behavior of the robot? How can we ensure that the robot's actions are safe and aligned with human values?

### Suggestions

The paper would benefit from a more thorough analysis of the computational demands of the proposed method. While the authors mention the use of an 8-episode trajectory for training, they should provide a breakdown of the computational cost associated with each stage of the pipeline, including the pre-training of the video diffusion model, the fine-tuning on robot demonstrations, and the inference process. Specifically, they should quantify the GPU memory requirements, the training time per epoch, and the inference latency. This would allow the community to better assess the practicality of the method and identify potential bottlenecks. Furthermore, a comparison of the computational cost with other state-of-the-art methods would be valuable. The authors should also investigate techniques to reduce the computational burden, such as model compression or knowledge distillation, and discuss the trade-offs between computational efficiency and performance.

To address the lack of analysis on the method's limitations, the authors should conduct a more rigorous evaluation on a wider range of tasks, including those that require more complex reasoning and manipulation skills. For example, they could evaluate the method on tasks that involve tool use, multi-step planning, or interaction with dynamic environments. A detailed analysis of the failure modes of both the video diffusion model and the masked inverse dynamics model is also necessary. This should include an investigation into the types of errors that each model makes, and how these errors propagate through the pipeline. For instance, the authors could analyze cases where the video diffusion model generates unrealistic or physically implausible videos, and how this affects the performance of the inverse dynamics model. They should also explore the sensitivity of the method to variations in the input data, such as changes in lighting conditions or camera viewpoints. This would provide a more comprehensive understanding of the method's robustness and generalization capabilities.

Finally, the authors need to address the ethical implications of using large-scale video datasets for robot learning more directly. They should acknowledge the potential for biases in these datasets to propagate into the robot's behavior, and discuss methods for mitigating these biases. For example, they could explore techniques for data augmentation or debiasing that can reduce the impact of skewed data. They should also consider the potential for the robot to learn harmful or unsafe behaviors from the video data, and discuss how to ensure that the robot's actions are aligned with human values. This could involve the use of safety constraints or reward shaping techniques that encourage safe and ethical behavior. The authors should also discuss the limitations of their approach in terms of ensuring ethical behavior, and acknowledge the need for further research in this area.

### Questions

I would like to hear from the authors about the points raised in the weaknesses section.

### Rating

6

### Confidence

4

**********