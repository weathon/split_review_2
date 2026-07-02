### Summary

This paper introduces a novel method for training synaptic delays in recurrent spiking neural networks (RSNNs) using surrogate gradient learning (SGL) and backpropagation. The proposed method, DelRec, leverages a differentiable interpolation technique to handle non-integer delays with well-defined gradients at training time. The authors demonstrate that trainable recurrent delays outperform feedforward ones, leading to new state-of-the-art (SOTA) results on two challenging temporal datasets (Spiking Speech Command and Permuted Sequential MNIST). Additionally, the method matches SOTA performance on the Spiking Heidelberg Digit dataset using only vanilla Leaky-Integrate-and-Fire neurons with stateless synapses. The results highlight the importance of recurrent delays in temporal processing for SNNs and suggest that DelRec can effectively optimize these delays for efficient deployment on neuromorphic hardware with programmable delays.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel method for training recurrent synaptic delays in RSNNs using surrogate gradient learning, which is a significant advancement in the field of spiking neural networks.
2. The method achieves state-of-the-art results on two challenging temporal datasets (Spiking Speech Command and Permuted Sequential MNIST), demonstrating its effectiveness.
3. The authors provide a detailed analysis of the method's performance under low parameter constraints and sparsity, showing its robustness.
4. The paper is well-written and clearly explains the technical details of the method, making it accessible to a broad audience.
5. The authors provide a functional study of delays, comparing feedforward and recurrent delays and analyzing performance under low parameter constraints and sparsity.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a detailed discussion of the computational complexity and scalability of the proposed method. Specifically, the analysis should include a breakdown of the computational cost associated with the differentiable interpolation technique, considering both time and memory requirements. It is unclear how the method's efficiency scales with an increasing number of neurons and time steps, particularly in the context of large-scale networks. The paper should also discuss the memory footprint of storing the scheduling matrix, especially for long sequences and large networks.
2. The method's reliance on a specific surrogate gradient function may limit its applicability. The paper does not explore the sensitivity of the results to different surrogate gradient choices, which could impact the robustness and generalizability of the method. A more thorough investigation into the impact of different surrogate gradients on the learned delays is needed. The paper should also discuss the potential for the surrogate gradient to introduce bias in the learning process, and how this might affect the final performance.
3. The differentiable interpolation technique may introduce approximations that affect the accuracy of delay learning, especially for large delays. The paper does not provide a quantitative analysis of the approximation error introduced by the interpolation, nor does it discuss how this error might propagate through the network and affect overall performance. It is unclear how the method maintains accuracy when dealing with a wide range of delay values. The paper should also discuss the potential for the interpolation to introduce numerical instability, especially for very small or very large delay values.
4. The paper does not provide a detailed analysis of the method's sensitivity to hyperparameters, such as the learning rate and the width parameter of the interpolation function. The lack of a systematic hyperparameter study makes it difficult to assess the robustness of the method and to provide guidelines for its application in different contexts. The paper should also discuss the potential for the method to be sensitive to the initialization of the delay parameters, and how this might affect the final performance.

### Suggestions

The paper should include a more detailed analysis of the computational complexity of the proposed method, focusing on the differentiable interpolation technique. This analysis should include a breakdown of the time and memory requirements for both training and inference, considering the impact of the number of neurons, time steps, and the range of delay values. Specifically, the authors should provide a theoretical analysis of the computational cost associated with the interpolation, and validate this analysis with empirical measurements. It would be beneficial to show how the method's efficiency scales with increasing network size and time series length, and to discuss the potential bottlenecks that may arise in large-scale applications. Furthermore, the authors should explore the trade-offs between accuracy and computational cost, providing guidelines for selecting appropriate parameters for different use cases. For example, the authors could investigate the impact of different interpolation kernel sizes on both computational cost and accuracy, providing a practical guide for users to balance these factors.

To address the sensitivity of the method to the choice of surrogate gradient, the authors should conduct a systematic study comparing the performance of different surrogate gradient functions. This study should include a range of commonly used surrogate gradients, such as the sigmoid and tanh functions, and should evaluate their impact on the learned delays and the overall performance of the network. The authors should analyze the convergence behavior of the method under different surrogate gradients, and discuss the potential reasons for any observed differences. This analysis should also include a discussion of how the choice of surrogate gradient might affect the robustness of the method to noise and perturbations. The authors should also investigate whether the method is sensitive to the specific parameters of the surrogate gradient function, such as the slope of the sigmoid function. This would provide a more complete understanding of the method's limitations and potential for generalization.

Finally, the paper should include a more detailed analysis of the approximation error introduced by the differentiable interpolation technique, particularly for large delays. This analysis should include a quantitative evaluation of the error as a function of the delay value and the width parameter of the interpolation function. The authors should also discuss how this error might propagate through the network and affect the overall performance. It would be beneficial to provide a theoretical analysis of the approximation error, and to validate this analysis with empirical measurements. The authors should also explore the trade-offs between accuracy and computational cost, providing guidelines for selecting appropriate parameters for different use cases. Additionally, a more thorough hyperparameter study is needed, focusing on the learning rate and the width parameter of the interpolation function. This study should include a systematic exploration of the parameter space, and should provide guidelines for selecting appropriate hyperparameters for different datasets and network architectures. The paper should also discuss the potential for the method to be sensitive to the initialization of the delay parameters, and how this might affect the final performance.

### Questions

1. How does the method scale with larger and deeper recurrent networks in terms of computational efficiency and performance?
2. What are the potential trade-offs between accuracy and computational cost when using DelRec in large-scale applications?
3. How sensitive is the method to the choice of surrogate gradient function?
4. What are the potential limitations or challenges of deploying DelRec on current neuromorphic hardware platforms?
5. How does the method handle very large delays, and is there a limit to the delay values that can be effectively learned?

### Rating

6

### Confidence

4

**********