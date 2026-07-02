### Summary

This paper proposes to build a vision-tactile world model by combining the tactile information with the vision world model. Specifically, the model first extracts the visual and tactile latents with pre-trained encoders, then combines the two modalities and feed them into a transformer to obtain the next tokens. The authors show that the proposed method can improve the object permanence and causal compliance of the world model. Finally, they show that the world model can be used to do the model predictive control (MPC) and plan actions for real robot execution.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

The idea of building a vision-tactile world model is interesting and promising. The experiments show that the proposed method can improve the object permanence and causal compliance of the world model. The authors also verify the effectiveness of the world model for planning and control on a real robot.

### Weaknesses

#### Some Related Works


#### comment

1. The authors do not discuss the limitations of the proposed method, which makes the readers do not know when the world model fails.

2. The authors only use the pre-trained vision encoder and the tactile encoder. However, there is no explanation of how these encoders are trained. It is not convincing that the tactile encoder can be directly used for the world model. Specifically, the tactile encoder is trained with a different objective (frame prediction) than the world model (next token prediction), and it is not clear whether the latent space learned by the tactile encoder is suitable for the world model. The authors should provide more analysis of the tactile encoder and its latent space.

3. The evaluation of the world model is not convincing. The authors only use the Fréchet distance to evaluate the object permanence and causal compliance. However, there is no definition or explanation of the Fréchet distance. The authors should provide more details about the Fréchet distance and why it is a suitable metric for evaluating object permanence and causal compliance. Additionally, the authors should consider other metrics to evaluate the world model, such as the prediction error of the next state.

### Suggestions

The authors should provide a more detailed discussion of the limitations of their proposed method. This should include an analysis of the scenarios where the world model is likely to fail, such as when dealing with complex object interactions, occlusions, or novel tactile sensations. For example, the authors could analyze the performance of the model on specific types of manipulation tasks and identify the common failure modes. This would help the readers understand the scope and limitations of the proposed method and guide future research in this area. Furthermore, the authors should investigate the robustness of the model to noisy or incomplete sensory data, which is common in real-world robotic applications.

The authors should also provide a more detailed analysis of the tactile encoder and its latent space. This should include an explanation of how the tactile encoder is trained, what kind of information is captured in the latent space, and how well it aligns with the requirements of the world model. The authors could perform ablation studies to evaluate the contribution of the tactile encoder to the overall performance of the world model. For example, they could compare the performance of the world model with and without the tactile encoder, or with different tactile encoders. Additionally, the authors could visualize the latent space of the tactile encoder to gain a better understanding of the information it captures. This would help to justify the use of the pre-trained tactile encoder and provide insights into the role of tactile information in the world model.

Finally, the authors should provide a more comprehensive evaluation of the world model. This should include a clear definition and explanation of the Fréchet distance and why it is a suitable metric for evaluating object permanence and causal compliance. The authors should also consider other metrics to evaluate the world model, such as the prediction error of the next state, the accuracy of object tracking, and the ability to predict contact events. The authors could also evaluate the world model on a wider range of manipulation tasks and compare its performance with other state-of-the-art world models. This would provide a more thorough assessment of the capabilities and limitations of the proposed method.

### Questions

1. What is the sampling rate for the vision and tactile observation? 

2. In Figure 3, the tactile latents have a much smaller length (5) than the visual latents (1000). Why is that? And does that mean the tactile information is much less useful than the visual information? 

3. In the evaluation, the authors track the keypoints on the objects to evaluate the object permanence and causal compliance. However, the authors do not explain how the keypoints are selected. Also, when the object is occluded, how to track the keypoints?

4. The world model is used for the model predictive control (MPC). However, there is no discussion of the performance of the MPC, such as the inference time. 

5. The authors do not discuss the limitations of the proposed method.

### Rating

6

### Confidence

3

**********