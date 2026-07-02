### Summary

The paper presents a method for real-time adaptive neural stimulation, integrating streaming latent space construction, adaptive modeling of stimulation effects, and optimization of stimuli to drive neural dynamics along desired trajectories. The approach is evaluated on both simulated and real neural data, including calcium imaging and electrophysiological recordings, demonstrating its ability to learn stimulation-response mappings and design effective stimuli under realistic experimental constraints. The authors claim the method operates faster than real-time, making it suitable for in vivo applications.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

* The paper introduces a novel streaming method for stimulation-response modeling in affine latent spaces, which is a significant advancement for real-time neural stimulation.
* The method is rigorously evaluated on both simulated and real neural data, including calcium imaging and electrophysiological recordings, demonstrating its effectiveness and robustness.
* The paper is well-structured, with a clear problem statement, detailed methodology, and comprehensive evaluation of the proposed method.
* The method has potential applications in neuroscience research and clinical settings, particularly for brain-machine interfaces and therapeutic interventions.

### Weaknesses

#### Some Related Works


#### comment

 * The method's performance may be sensitive to the choice of hyperparameters, such as the kernel parameters in the kernel regression and the constraints on the optimization problem. A more detailed analysis of the impact of these parameters on the method's performance would be beneficial.
* While the paper demonstrates the method's effectiveness on simulated and real neural data, it does not provide a detailed analysis of the computational cost and scalability of the method, especially for large-scale neural recordings.
* The paper could benefit from a more detailed discussion of the limitations of the proposed method and potential avenues for future research. For example, the authors could discuss the potential impact of neural plasticity on the stimulation-response mapping and how the method could be adapted to account for these changes.

### Suggestions

The paper should include a more thorough investigation into the hyperparameter sensitivity of the proposed method. Specifically, the authors should explore the impact of different kernel bandwidths in the kernel regression on the accuracy and stability of the learned stimulation-response mapping. A systematic analysis, perhaps using a grid search or cross-validation approach, would help to identify optimal parameter ranges and provide insights into the robustness of the method. Furthermore, the constraints used in the optimization problem should be examined more closely. For example, the authors could analyze how different levels of sparsity constraints affect the resulting stimulation patterns and their effectiveness in driving the desired neural dynamics. This analysis should also consider the trade-off between the complexity of the stimulation pattern and its effectiveness, providing practical guidance for users of the method.

To address the lack of computational analysis, the authors should provide a detailed breakdown of the computational cost of each component of their method, including the streaming latent space construction, the adaptive modeling of stimulation effects, and the optimization of stimuli. This analysis should consider the time complexity of each algorithm and the memory requirements, especially when dealing with large-scale neural recordings. The authors should also discuss the scalability of their method to different recording modalities and sizes, and provide recommendations for optimizing the computational performance. For example, they could explore the use of parallel computing or other optimization techniques to reduce the computational burden. A comparison with other existing methods in terms of computational cost would also be beneficial.

Finally, the discussion of limitations should be expanded to include a more in-depth analysis of the potential impact of neural plasticity on the stimulation-response mapping. The authors should discuss how changes in neural connectivity and responsiveness over time could affect the accuracy of the learned mapping and propose strategies for adapting the method to account for these changes. For example, they could explore the use of online learning algorithms that can continuously update the stimulation-response mapping as new data becomes available. Furthermore, the authors should discuss the potential limitations of their method in dealing with complex neural dynamics and non-linear stimulation effects. They should also consider the potential for unintended consequences of neural stimulation and propose safety measures to mitigate these risks.

### Questions

* How does the method handle non-stationary neural dynamics, where the underlying neural activity changes over time?
* What are the limitations of the method in dealing with high-dimensional stimulation patterns, and how can these limitations be addressed?
* How does the method perform when applied to different brain regions or neural circuits, and what are the potential challenges in generalizing the method to new datasets?

### Rating

6

### Confidence

2

**********