### Summary

This paper proposes a lightweight denoising autoencoder (DAE) plug-in to enhance the generalization of existing SR models. The DAE is trained to reconstruct the input LR image from the output of SR networks, and can be used as a training loss or an inference post-processing step. The DAE aligns the noise-perturbed HR features with the LR features, enabling denoising noisy HR features to be equivalent to denoising noisy LR features. The authors demonstrate the effectiveness of the proposed method on various SR models and datasets.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The idea of using a DAE to enhance the generalization of SR models is novel and interesting.
- The method can be applied to various SR models and datasets, and can be used as a training loss or an inference post-processing step.
- The authors provide extensive experiments and ablation studies to support their claims.

### Weaknesses

#### Some Related Works


#### comment

 - The motivation for using the DAE is not very clear. The authors state that the DAE models the SISR degradation process within the DAE framework, but do not explain why this is necessary or beneficial. Specifically, it's unclear how modeling the degradation process within the DAE framework leads to improved generalization compared to other regularization techniques. The connection between the DAE's denoising operation and the desired properties of a good SR model is not well-established.
- The authors claim that the DAE leverages a property of diffusion models, where after noise is added, HR images and LR features become aligned, but this property is not well-explained or justified. The explanation of how adding noise aligns HR and LR features is superficial. It lacks a detailed explanation of the underlying mechanism, such as how the noise distribution affects the feature space and why this alignment is crucial for the proposed method. Furthermore, the authors do not provide any theoretical or empirical evidence to support this claim, making it difficult to assess its validity.
- The design of the DAE is not very intuitive. The authors introduce several modules, such as the degradation prediction module and the noise addition module, but do not explain their roles or functions clearly. For example, the purpose of the degradation prediction module is unclear. Why is it necessary to predict the degradation before denoising? What specific information does this module provide that is useful for the denoising process? Similarly, the noise addition module's role is not well-justified. Why is adding noise to the HR features beneficial for the DAE's performance? The lack of clear explanations for these modules makes it difficult to understand the overall design and functionality of the DAE.

### Suggestions

To improve the clarity and effectiveness of the proposed method, the authors should provide a more detailed explanation of the motivation behind using a DAE for enhancing SR generalization. This should include a clear articulation of how modeling the degradation process within the DAE framework leads to improved generalization. The authors should also discuss the limitations of existing regularization techniques and how their approach addresses these limitations. Furthermore, a more thorough explanation of the connection between the DAE's denoising operation and the desired properties of a good SR model is needed. This could involve a theoretical analysis or empirical evidence demonstrating how the DAE's denoising process encourages the SR model to learn more robust and generalizable features. For instance, the authors could explore the impact of the DAE on the feature space of the SR model, showing how it encourages the model to learn features that are less sensitive to noise and other artifacts.

The authors should provide a more rigorous explanation of the alignment property between HR and LR features in diffusion models. This should include a detailed analysis of how the noise distribution affects the feature space and why this alignment is crucial for the proposed method. The authors could consider providing a visualization of the feature space before and after noise addition to demonstrate the alignment. Additionally, they should provide theoretical or empirical evidence to support their claim that this alignment is beneficial for the DAE's performance. This could involve comparing the performance of the DAE with and without this alignment property, or providing a mathematical analysis of how this alignment affects the denoising process. The authors should also discuss the limitations of this alignment property and how it might affect the performance of the DAE in different scenarios.

The design of the DAE should be made more intuitive by providing clear explanations for the roles and functions of each module. For example, the authors should explain why the degradation prediction module is necessary and what specific information it provides that is useful for the denoising process. They could also provide a detailed analysis of the degradation prediction module's architecture and how it is trained. Similarly, the authors should justify the role of the noise addition module and explain why adding noise to the HR features is beneficial for the DAE's performance. This could involve a discussion of the noise schedule and how it affects the DAE's learning process. The authors should also consider providing ablation studies to demonstrate the importance of each module and how they contribute to the overall performance of the DAE. This would help to clarify the design choices and make the method more understandable.

### Questions

- How does the DAE differ from other regularization techniques, such as data augmentation or adversarial training?
- How does the alignment property between HR and LR features in diffusion models help the DAE to perform better?
- What is the degradation prompt $P_D$ and how is it learned?
- How does the DAE handle different types of degradations, such as blur, noise, and compression?
- How does the DAE affect the computational cost and memory consumption of the SR models?

### Rating

6

### Confidence

4

**********