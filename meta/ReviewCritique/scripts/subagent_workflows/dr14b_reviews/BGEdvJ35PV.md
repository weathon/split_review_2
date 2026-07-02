### Summary

This paper proposes a new sampling strategy to improve the performance of diffusion models for 3D molecular generation. The authors first analyze the unique structure of molecular data distributions, which are highly concentrated and densely packed, making diffusion-based generative processes fragile. Then, they propose DIST, a plug-in corrective module that can be seamlessly integrated into diverse diffusion-based molecular generation methods. The key idea is to diffuse and steer the intermediate distribution, realigning inference trajectories toward a valid molecular distribution. Extensive experiments on multiple benchmarks and backbones demonstrate that DIST not only improves stability and overall performance, but also reduces computational cost to nearly half the standard number of timesteps.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The authors provide a novel perspective on the challenges of applying diffusion models to molecular generation, highlighting the unique structure of molecular data distributions.
2. The proposed DIST method is theoretically grounded and provides a general framework for improving the stability and performance of diffusion-based molecular generation.
3. The experimental results are comprehensive and demonstrate the effectiveness of DIST across multiple architectures and datasets.
4. The paper is well-written and clearly explains the motivation, methodology, and results.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of the proposed approach and potential failure cases. Specifically, it is unclear how the method performs when the initial molecular structure is far from the target distribution, or if the diffusion process gets stuck in local minima. A more thorough analysis of these scenarios would be beneficial.
2. The computational cost analysis could be more detailed, especially regarding the trade-off between performance and efficiency. While the paper mentions a reduction in timesteps, it does not fully explore the overhead introduced by the corrective sampling strategy. A breakdown of the computational cost for each step, including the pilot subset evaluation and the selective reverse process, would be valuable.

### Suggestions

The authors should provide a more in-depth analysis of the scenarios where the proposed DIST method might fail or underperform. For instance, it would be beneficial to investigate how the method behaves when the initial molecular structure is significantly different from the target distribution. This could involve testing the method on molecules with highly diverse chemical structures or those that are far from the training data distribution. Furthermore, the authors should explore the potential for the diffusion process to get trapped in local minima during the sampling process. This could be analyzed by visualizing the trajectory of the molecular structure during the reverse diffusion process and identifying instances where the structure does not converge to a valid molecular conformation. A detailed discussion of these limitations would provide a more complete understanding of the method's applicability and robustness.

To enhance the computational cost analysis, the authors should provide a more granular breakdown of the time spent on each step of the DIST method. This should include the time required for the pilot subset evaluation, the selective reverse process, and any other overhead introduced by the corrective sampling strategy. It would be helpful to compare the computational cost of DIST with the standard diffusion process, not just in terms of the number of timesteps, but also in terms of the actual wall-clock time. This analysis should also consider the impact of different batch sizes and the number of pilot samples on the overall computational cost. A detailed analysis of these factors would provide a more comprehensive understanding of the trade-off between performance and efficiency.

Finally, the authors should explore the sensitivity of the method to the choice of hyperparameters, such as the number of pilot samples and the threshold for selecting the corrected distribution. A sensitivity analysis would help to determine the optimal settings for these parameters and provide guidance for practitioners who wish to apply the method to their own datasets. This analysis should also consider the potential for the method to be sensitive to the specific characteristics of the dataset, such as the size and diversity of the molecular structures. A thorough investigation of these factors would help to ensure the robustness and generalizability of the proposed method.

### Questions

1. How does the performance of DIST vary across different types of molecules or molecular properties?
2. Can the authors provide more insights into the choice of hyperparameters for DIST, such as the number of pilot samples and the threshold for selecting the corrected distribution?

### Rating

6

### Confidence

3

**********