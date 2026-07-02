### Summary

This paper proposes a unified 3DGS-based few-shot NVS method focusing on initializing and optimizing 3DGS representation using generative completion-based strategies to enhance scene completion. The proposed method includes a generative point cloud completion-based strategy and a generative pseudo view completion-based strategy. Extensive experiments demonstrate the effectiveness of the proposed method.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

The proposed method enhances the 3DGS’ capability of scene completion and mitigates appearance distortion and floating artifacts caused by the hallucination of generative models.
The experiments are extensive and demonstrate the effectiveness of the proposed method.

### Weaknesses

#### Some Related Works


#### comment

Is there any inference speed evaluation or comparison? I am concerned about the inference speed of the proposed method due to the involvement of multiple generative models.

How is the performance of the proposed method on more sparse input views, such as 3 views?

In the experiments, the proposed method achieves worse results than BinogS on some datasets under certain conditions. Could the authors further explain the reason?

### Suggestions

The paper introduces a novel approach to few-shot novel view synthesis (NVS) using generative models for scene completion and pseudo-view generation, which is a promising direction. However, the practical applicability of the method is questionable without a thorough analysis of its computational cost. The authors should provide a detailed breakdown of the inference time, including the time taken by each component of the pipeline, such as the point cloud completion, pseudo-view generation, and the final 3D Gaussian Splatting (3DGS) rendering. This analysis should be performed on a standard hardware setup and compared against existing state-of-the-art methods, such as BinogS, to provide a clear understanding of the trade-off between performance and speed. Furthermore, it would be beneficial to explore potential optimizations to reduce the inference time, such as model pruning or knowledge distillation, to make the method more practical for real-world applications. The current lack of speed evaluation is a significant limitation that needs to be addressed.

Regarding the performance on sparse input views, the authors should provide a more in-depth analysis of the method's behavior under varying levels of sparsity. While the paper presents results for 3-view input, it would be beneficial to investigate the performance with even sparser views, such as 2 or 4 views, to understand the limitations of the proposed method. Specifically, it would be helpful to analyze how the quality of the generated point cloud and pseudo-views degrades as the number of input views decreases. This analysis should include both quantitative metrics, such as PSNR and SSIM, and qualitative visualizations to demonstrate the visual quality of the generated novel views. Understanding the performance limits of the method under extreme sparsity is crucial for determining its applicability in real-world scenarios where input views are often limited.

Finally, the authors should provide a more detailed explanation for the cases where the proposed method performs worse than BinogS. The current explanation, which attributes the worse performance to the small number of input views and the resulting hallucinations, is not entirely satisfactory. A more in-depth analysis is needed to understand the specific conditions under which the proposed method fails to outperform BinogS. For example, it would be helpful to analyze the types of scenes or object geometries where the proposed method struggles. Furthermore, the authors should investigate whether the performance difference is due to the point cloud completion strategy, the pseudo-view generation, or the optimization process. A more detailed analysis of these factors would provide valuable insights into the strengths and weaknesses of the proposed method and guide future research directions.

### Questions

Please see the Weaknesses.

### Rating

6

### Confidence

4

**********