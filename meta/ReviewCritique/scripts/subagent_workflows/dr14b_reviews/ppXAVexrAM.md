### Summary

This paper presents a novel approach to autoregressive visual generation using a GPT-style decoder-only model. The key innovation lies in the use of a video tokenizer to convert continuous image sequences into discrete tokens, coupled with a camera encoder that translates camera trajectories into 3D positional guidance. To enhance the quality of generated content while preserving the autoregressive structure, the authors introduce a random spatial permutation of tokens, which maintains temporal order while optimizing the spatial arrangement. The method is evaluated on public datasets, demonstrating performance comparable to state-of-the-art view synthesis techniques based on diffusion models.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel application of autoregressive models in visual generation, specifically for novel view synthesis, which is a departure from traditional diffusion-based methods. The use of a GPT-style decoder-only model for this task is innovative and addresses the challenge of imposing a causal structure in camera trajectories.

2. The authors propose a video tokenizer that captures both spatial and temporal encoding, which is a significant improvement over independent per-frame tokenization. This approach helps in preserving temporal consistency across generated views.

3. The introduction of a camera encoder that converts camera trajectories into 3D positional guidance using Plücker raymaps is a creative solution to encode camera information effectively. This allows for precise camera control during the view synthesis process.

4. The paper provides extensive experimental results on public datasets, demonstrating that the proposed method achieves comparable performance to state-of-the-art diffusion models. The qualitative and quantitative comparisons are thorough and support the claims made.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion on the limitations of the proposed method, especially in scenarios with complex camera trajectories or highly dynamic scenes. The current evaluation does not thoroughly explore the boundaries of the method's applicability, particularly in situations where rapid camera movements or significant occlusions might occur. It is unclear how the method would handle scenarios with significant changes in viewpoint or lighting conditions between frames, which could potentially disrupt the temporal consistency that the video tokenizer aims to preserve.

2. While the paper compares the proposed method with diffusion models, a more in-depth analysis of the computational efficiency and scalability of the autoregressive approach would be valuable. The paper lacks a detailed comparison of training and inference times, as well as memory usage, which are critical factors for practical applications. It would be beneficial to understand how the method scales with increasing sequence lengths or higher resolution images, and how it compares to diffusion models in these aspects.

3. The paper mentions the use of a video tokenizer but does not delve into the potential challenges or limitations associated with this component. For instance, how does the choice of video tokenizer affect the quality of the generated views? Are there specific types of video tokenizers that are more suitable for this task? The paper does not explore the sensitivity of the method to different video tokenization strategies, nor does it discuss the potential for information loss during the tokenization process, which could impact the quality of the generated views.

### Suggestions

To address the limitations regarding complex camera trajectories and dynamic scenes, the authors should consider including a more rigorous evaluation that specifically targets these scenarios. This could involve testing the method on datasets with more challenging camera paths, such as those involving rapid rotations or significant changes in viewpoint. Additionally, the authors should analyze the impact of occlusions and lighting variations on the quality of the generated views. A detailed analysis of failure cases would also be beneficial, highlighting the specific conditions under which the method struggles to maintain temporal consistency or generate realistic views. Furthermore, the authors could explore techniques to mitigate these limitations, such as incorporating attention mechanisms that are more robust to changes in viewpoint or occlusions, or using a more sophisticated video tokenizer that can better capture the temporal dynamics of the scene.

Regarding computational efficiency and scalability, the authors should provide a detailed comparison of the training and inference times of their method with those of state-of-the-art diffusion models. This comparison should include a breakdown of the computational cost associated with each component of the proposed method, such as the video tokenizer, camera encoder, and autoregressive transformer. The authors should also investigate how the method scales with increasing sequence lengths and image resolutions, and provide recommendations for optimizing the method for practical applications. It would be valuable to explore techniques for reducing the computational cost of the autoregressive transformer, such as using sparse attention mechanisms or model compression techniques. A thorough analysis of the memory usage of the method would also be beneficial, particularly for large-scale datasets or high-resolution images.

Finally, the authors should conduct a more in-depth analysis of the video tokenizer and its impact on the quality of the generated views. This could involve comparing the performance of the method with different types of video tokenizers, such as those based on transformers or convolutional neural networks. The authors should also investigate the sensitivity of the method to the choice of video tokenizer parameters, such as the number of tokens or the size of the embedding space. A detailed analysis of the information loss during the tokenization process would also be valuable, and the authors could explore techniques for minimizing this loss, such as using a more efficient quantization scheme or a more sophisticated video representation. The authors should also discuss the limitations of the video tokenizer and its potential impact on the overall performance of the method.

### Questions

1. Can the authors provide more insights into the choice of the video tokenizer? How does it compare to other tokenization methods in terms of performance and efficiency?

2. The paper mentions the use of Plücker raymaps for camera trajectory encoding. Could the authors elaborate on the advantages of using Plücker raymaps over other representations?

3. How does the proposed method handle scenarios with significant changes in viewpoint or lighting conditions between frames?

### Rating

6

### Confidence

3

**********