### Summary

This paper presents ChaosNexus, a foundation model for forecasting chaotic systems, addressing the challenge of multi-scale dynamics. The model introduces a U-Net-inspired architecture named ScaleFormer to capture both fine-grained and coarse-grained temporal structures. The model is augmented with Mixture-of-Experts (MoE) layers and wavelet-based frequency fingerprints. The model performance is evaluated on a large testbed of synthetic chaotic systems and real-world weather forecasting.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper introduces a novel architecture (ScaleFormer) that explicitly addresses the multi-scale nature of chaotic systems. This is an important contribution as existing foundation models often operate at a single resolution.
- The model achieves notable improvements in long-term attractor statistics and competitive point-wise forecasting accuracy on a large-scale testbed of synthetic chaotic systems.
- The model demonstrates exceptional data efficiency in real-world weather forecasting, achieving competitive zero-shot performance and further improvement with few-shot fine-tuning.
- The paper provides a guiding principle for scientific foundation models that cross-system generalization stems from the diversity of training systems rather than the sheer volume of data.

### Weaknesses

#### Some Related Works


#### comment

 - While the paper demonstrates superior performance on chaotic systems, it's unclear how well the approach would generalize to other types of dynamical systems that may not exhibit multi-scale temporal structures. The focus on chaotic systems, while important, raises questions about the broader applicability of the proposed architecture. For instance, systems with dominant low-frequency dynamics or those governed by algebraic equations might not benefit from the multi-scale approach.
- The paper could benefit from a more detailed analysis of the computational complexity and efficiency of the ScaleFormer architecture, especially when compared to existing methods. The analysis should include not just the number of parameters, but also the FLOPs and memory requirements, particularly when scaling to longer time series or higher-dimensional systems. A comparison with models like Transformers, which have well-understood scaling properties, would be beneficial.
- The paper does not discuss potential limitations or challenges in deploying the model in real-world scenarios, such as computational cost or data requirements for fine-tuning. While the paper touches on data efficiency, a more detailed discussion of the practical computational resources needed for training and inference, especially for high-resolution weather models, is needed. This should include the cost of the MoE layers and wavelet transformations.

### Suggestions

The paper should include a more thorough investigation into the generalizability of the proposed ScaleFormer architecture beyond chaotic systems. This could involve testing the model on a diverse set of dynamical systems, including those with different spectral characteristics and temporal dependencies. For example, the authors could evaluate the model's performance on systems with predominantly low-frequency dynamics, or on systems governed by algebraic equations rather than differential equations. This would help to clarify the scope of the proposed method and identify the types of systems for which it is most suitable. Furthermore, it would be beneficial to analyze the model's performance on systems with varying degrees of chaos, to understand how the model's performance degrades as the system becomes less chaotic.

To address the concerns about computational complexity, the authors should provide a detailed analysis of the computational cost of the ScaleFormer architecture, including the number of parameters, FLOPs, and memory requirements. This analysis should be compared to existing methods, such as Transformers, to provide a clear understanding of the trade-offs between performance and computational cost. The analysis should also consider the scaling properties of the model when applied to longer time series or higher-dimensional systems. It would be useful to include a breakdown of the computational cost of different components of the model, such as the MoE layers and wavelet transformations, to identify potential bottlenecks. This analysis should also consider the impact of different hardware configurations on the model's performance.

Finally, the paper should include a more detailed discussion of the practical challenges of deploying the model in real-world scenarios. This should include a discussion of the computational resources needed for training and inference, as well as the data requirements for fine-tuning. The authors should also discuss the potential limitations of the model, such as its sensitivity to hyperparameter settings and its robustness to noisy data. It would be beneficial to provide guidelines for selecting appropriate hyperparameters and for preprocessing data to ensure optimal performance. The authors should also discuss the potential for using model compression techniques to reduce the computational cost of the model.

### Questions

- How does the computational complexity of ScaleFormer compare to existing architectures, particularly when scaling to longer time series or higher-dimensional systems?
- What are the potential challenges or limitations of deploying ChaosNexus in real-world applications, such as computational cost or data requirements for fine-tuning?

### Rating

6

### Confidence

3

**********