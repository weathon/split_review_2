### Summary

This paper proposes a novel framework, D2GS, to enhance sparse-view 3D reconstruction using 3D Gaussian Splatting (3DGS). The framework addresses two key failure modes: overfitting in near-field regions and underfitting in far-field areas. The Depth-and-Density Guided Dropout (DD-Drop) mechanism selectively removes redundant Gaussians based on depth and density, while the Distance-Aware Fidelity Enhancement (DAFE) module strengthens supervision in distant regions. Additionally, the paper introduces a new evaluation metric, Inter-Model Robustness (IMR), to quantify the stability of learned Gaussian distributions. Experiments on LLFF and Mip-NeRF360 datasets demonstrate that D2GS achieves state-of-the-art results in both visual quality and robustness under sparse-view conditions.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper identifies and addresses two critical failure modes of 3DGS in sparse-view settings: overfitting in near-field regions and underfitting in far-field regions. The proposed Depth-and-Density Guided Dropout (DD-Drop) and Distance-Aware Fidelity Enhancement (DAFE) modules are well-motivated and effectively tackle these issues.

2. The introduction of the Inter-Model Robustness (IMR) metric is a significant contribution, as it provides a quantitative measure of the stability of learned Gaussian distributions, which is crucial for evaluating the robustness of 3DGS models.

3. The experimental results are comprehensive and demonstrate the effectiveness of the proposed method. The paper includes comparisons with several state-of-the-art methods and shows significant improvements in both quantitative and qualitative metrics.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a detailed analysis of the computational cost associated with the proposed method. While the method shows improvements in reconstruction quality, it is important to understand the trade-offs in terms of computational efficiency, especially for real-time applications. Specifically, the paper lacks a breakdown of the time spent on each stage of the proposed method, such as the depth-and-density guided dropout and distance-aware fidelity enhancement modules. This makes it difficult to assess the practical applicability of the method, particularly in resource-constrained environments. Furthermore, the paper does not discuss the memory footprint of the proposed method, which is also a critical factor for real-time applications.

2. The paper primarily focuses on sparse-view settings but does not extensively evaluate the performance of the proposed method in dense-view scenarios. It would be beneficial to see how the method performs when more views are available, and whether the proposed modules introduce any drawbacks in such cases. For example, it is unclear if the dropout strategy, which is designed to mitigate overfitting in sparse-view settings, might lead to underfitting or loss of detail when applied to dense-view scenarios with abundant information. A thorough evaluation across a range of view densities is needed to fully understand the method's behavior.

3. The paper could benefit from a more detailed discussion on the limitations of the proposed method. For instance, how does the method perform in scenes with complex occlusions or reflective surfaces? Are there specific types of scenes where the method struggles? The paper should also discuss the sensitivity of the method to hyperparameter settings, such as the dropout rate and the distance-aware fidelity enhancement parameters. Without a clear understanding of these limitations, it is difficult to assess the generalizability of the proposed method.

### Suggestions

To address the lack of computational cost analysis, the authors should provide a detailed breakdown of the time spent on each stage of their proposed method, including the depth-and-density guided dropout and distance-aware fidelity enhancement modules. This analysis should be performed on a standard hardware setup and should include both training and inference times. Furthermore, the authors should compare the computational cost of their method with existing state-of-the-art methods to provide a clear understanding of the trade-offs. The memory footprint of the proposed method should also be analyzed and discussed, as this is a critical factor for real-time applications. This analysis should include the memory usage of the Gaussian primitives, the depth maps, and any other intermediate data structures. The authors should also investigate the scalability of their method with respect to the number of Gaussian primitives and the size of the input images. This would provide a more complete picture of the computational cost of the proposed method.

To evaluate the performance of the proposed method in dense-view scenarios, the authors should conduct experiments using datasets with varying numbers of input views. This evaluation should include a comparison of the proposed method with existing state-of-the-art methods in both sparse-view and dense-view settings. The authors should also analyze the impact of the dropout strategy on the reconstruction quality in dense-view scenarios. Specifically, they should investigate whether the dropout strategy leads to underfitting or loss of detail when applied to dense-view scenarios with abundant information. The authors should also explore alternative strategies for handling dense-view scenarios, such as adaptive dropout rates or different fidelity enhancement techniques. This would provide a more comprehensive understanding of the method's behavior across a range of view densities.

To address the limitations of the proposed method, the authors should conduct experiments on scenes with complex occlusions and reflective surfaces. This evaluation should include a qualitative analysis of the reconstruction quality and a discussion of the challenges posed by these types of scenes. The authors should also analyze the sensitivity of the method to hyperparameter settings, such as the dropout rate and the distance-aware fidelity enhancement parameters. This analysis should include a discussion of the optimal hyperparameter settings for different types of scenes and a comparison of the method's performance with different hyperparameter settings. The authors should also discuss the potential failure modes of their method and provide guidance on how to mitigate these issues. This would provide a more complete understanding of the limitations of the proposed method and its generalizability.

### Questions

1. Could the authors provide more details on the computational cost of the proposed method? How does it compare to existing methods in terms of training and inference time?

2. How does the proposed method perform in dense-view scenarios? Are there any potential drawbacks when applying the method to such cases?

3. Could the authors elaborate on the limitations of the proposed method? Are there specific types of scenes or conditions where the method might struggle?

### Rating

6

### Confidence

4

**********