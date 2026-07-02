### Summary

This paper proposes a new generative model for images based on flow matching. The main contribution is to leverage vector quantization to represent images in a discrete space, while using a continuous representation to capture the underlying structure of the data distribution. The authors show that their approach, called Purrception, achieves faster convergence and better sample quality than existing continuous and discrete flow matching methods on ImageNet-1k 256x256 generation.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper is well-written and easy to follow. The authors provide a clear motivation for their work, a detailed description of their method, and a thorough evaluation of their results.
- The proposed approach is novel and interesting. To the best of my knowledge, this is the first paper to combine vector quantization and flow matching for image generation.
- The experimental results are impressive. The authors show that Purrception converges faster and achieves better FID scores than both continuous and discrete flow matching baselines. They also provide qualitative results that demonstrate the diversity and quality of the generated samples.

### Weaknesses

#### Some Related Works


#### comment

 - The paper does not provide any analysis of the computational cost of Purrception compared to other methods. This makes it difficult to assess the practical applicability of the proposed approach.
- The authors only evaluate their method on a single dataset (ImageNet-1k) and resolution (256x256). It would be interesting to see how Purrception performs on other datasets and higher resolutions.
- The paper does not discuss the limitations of the proposed approach in detail. For example, how does Purrception handle complex scenes or objects with multiple parts? How does the choice of the vector quantization codebook affect the performance of the model?

### Suggestions

The paper would benefit from a more thorough analysis of the computational demands of Purrception. While the authors present impressive results on ImageNet-1k, the practical applicability of the method hinges on its computational efficiency. A detailed breakdown of the FLOPs required for both training and inference, along with a comparison to other state-of-the-art flow matching methods, is crucial. This should include not only the total FLOPs but also the time required for each step of the process, such as the vector quantization, the flow matching training, and the sampling. Furthermore, it would be beneficial to analyze the memory footprint of the model, as this can be a limiting factor for large-scale image generation. Without this information, it is difficult to assess whether the proposed method is a viable alternative to existing approaches in real-world scenarios.

Expanding the evaluation to include a wider range of datasets and resolutions is essential to demonstrate the robustness and generalizability of Purrception. While ImageNet-1k is a standard benchmark, it is important to evaluate the method on datasets with different characteristics, such as those with more complex scenes, different object categories, or varying image styles. For example, evaluating on datasets like COCO or CelebA would provide insights into the model's ability to handle complex scenes and diverse object arrangements. Additionally, it is crucial to assess the performance of Purrception at higher resolutions, such as 512x512 or 1024x1024, as this is where the limitations of current generative models often become apparent. This would require a detailed analysis of how the model scales with increasing resolution and whether any modifications are needed to maintain performance.

Finally, a more in-depth discussion of the limitations of Purrception is needed. The paper should explore how the model handles complex scenes with multiple objects and intricate relationships between them. For instance, does the model struggle with occlusions or objects that are partially hidden? How does the choice of the vector quantization codebook affect the quality of the generated images? Does a larger codebook lead to better results, or are there diminishing returns? It would also be beneficial to analyze the failure cases of the model and identify the types of images that it struggles to generate. This would provide valuable insights into the strengths and weaknesses of the proposed approach and guide future research directions.

### Questions

- How does the choice of the vector quantization codebook affect the performance of Purrception? Have you experimented with different codebook sizes and architectures?
- Can you provide more insights into the limitations of Purrception? What are the main challenges that you foresee for future work in this area?
- How does Purrception handle complex scenes or objects with multiple parts? Have you conducted any ablation studies to analyze the impact of different components of your model on the final results?

### Rating

6

### Confidence

3

**********