### Summary

This paper introduces a Fourier Neural Filter (FNF) to enhance Fourier Neural Operator (FNO) in vision tasks. FNF integrates adaptive modulation and selective activation to improve sensitivity to high-frequency components and balance information flow between local and global representations. Experiments show that FNF outperforms Transformer and Mamba-based models on tasks like image classification, object detection, and semantic segmentation.

### Soundness

3

### Presentation

2

### Contribution

2

### Strengths

- The paper provides a thorough theoretical analysis of FNO’s limitations, such as over-smoothing and bandwidth bottlenecks, and clearly explains how FNF addresses these issues.

- The proposed FNF is simple and effective. It can be easily integrated into various models.

- The authors conducted extensive experiments to validate the effectiveness of FNF.

### Weaknesses

#### Some Related Works

[1] Fourier neural operator for learning dynamics of complex systems.
[2] Mamba-out: An efficient vision mamba for mobile deployment.

#### comment

 - The main contribution of this paper is the integration of FNF into vision tasks, which falls between the vision mamba and FNO [1]. Both of these components have strong global modeling capabilities, so this combination is not particularly surprising.

- The novelty of the proposed FNF module is limited. It simply combines two different backbones to leverage their advantages.

- The paper lacks an analysis of the complexity of the proposed FNF.

- The authors should include an analysis of the impact of the hyperparameters $\alpha$ and $\beta$.

- The performance gains of FNF are not significant enough to justify the additional complexity it introduces compared to vision mamba.

- The authors should compare their method to the latest state-of-the-art approaches, such as EfficientVMamba [2].

- The authors should provide more comparisons and visualizations of the model's effectiveness in image restoration tasks.

### Suggestions

The paper would benefit from a more detailed analysis of the computational complexity of the proposed FNF module. While the authors claim it is simple, a rigorous analysis, including FLOPs and memory usage, is necessary to understand its practical implications, especially when compared to other methods like Vision Mamba. This analysis should also consider the overhead introduced by the adaptive modulation and selective activation mechanisms. Furthermore, a breakdown of the computational cost associated with each component of FNF would be valuable for readers to assess its efficiency. The authors should also discuss the trade-offs between performance gains and the added complexity, providing a clear justification for the design choices made in FNF. A comparison with other methods should not only focus on accuracy but also on computational efficiency, which is crucial for real-world applications.

A more thorough investigation into the hyperparameters $\alpha$ and $\beta$ is needed. The current analysis lacks a detailed exploration of how these parameters affect the model's performance. The authors should provide a sensitivity analysis, showing how the model's accuracy and other metrics change as these parameters vary. This analysis should include a range of values for both $\alpha$ and $\beta$, and the results should be presented in a clear and concise manner, such as through tables or graphs. It is also important to discuss the optimal range for these parameters and provide a rationale for why these values work best. This would help readers understand the robustness of the model and how to tune these parameters for different tasks. Without this analysis, it is difficult to assess the practical applicability of the proposed method.

Finally, the paper should include a more comprehensive comparison with state-of-the-art methods, particularly in image restoration tasks. While the authors present results on image classification, object detection, and semantic segmentation, the comparison in image restoration is limited. The authors should include more recent methods, such as EfficientVMamba [2], and provide a detailed analysis of the performance differences. This comparison should not only focus on quantitative metrics but also include visualizations of the restored images to provide a qualitative assessment of the model's effectiveness. The authors should also discuss the limitations of their method in image restoration and suggest potential future directions for improvement. This would help readers understand the strengths and weaknesses of the proposed method and its potential for real-world applications.

### Questions

Please refer to the weaknesses.

### Rating

5

### Confidence

4

**********