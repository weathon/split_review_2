### Summary

The paper introduces GRAID, a framework designed to enhance spatial reasoning in Vision Language Models (VLMs) through high-fidelity data generation. GRAID leverages 2D bounding boxes from object detectors to create qualitative spatial VQA data, avoiding the errors associated with 3D reconstruction and generative hallucinations. The authors apply GRAID to three datasets (BDD100k, NuImages, and Waymo), generating over 8.5 million VQA pairs. The resulting datasets demonstrate high accuracy rates (91.16%) in human validation, significantly improving upon previous methods. Models trained on GRAID data show enhanced generalization capabilities, with substantial accuracy gains across various benchmarks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper presents an innovative framework that uses 2D geometric primitives to generate high-quality spatial reasoning data, avoiding the limitations of 3D reconstruction and generative models.
- The generated datasets are large-scale and have been rigorously validated, achieving high human-verified accuracy rates, which underscores the reliability of the data generation process.
- Models trained on GRAID-generated data demonstrate significant improvements in spatial reasoning tasks, with strong generalization to unseen question types and benchmarks.

### Weaknesses

#### Some Related Works


#### comment

 - The framework primarily focuses on 2D spatial relationships, which may limit its applicability to tasks requiring a deeper understanding of 3D spatial reasoning.
- While the SPARQ component improves efficiency, the process of generating and filtering large-scale VQA data can still be computationally intensive, potentially limiting scalability for real-time applications.
- The paper could benefit from more detailed comparisons with a broader range of existing methods, particularly in terms of computational efficiency and error analysis.

### Suggestions

The paper's focus on 2D spatial relationships, while effective for many tasks, inherently limits its ability to fully capture the complexities of 3D space. For instance, tasks involving viewpoint changes, object occlusion, or precise depth estimation would likely benefit from a 3D-aware approach. The current method, relying on 2D bounding boxes, may struggle with scenarios where the same 2D projection can result from different 3D configurations. To address this, future work could explore incorporating depth information or pseudo-3D cues derived from monocular or multi-view setups. This could involve integrating depth estimation models or leveraging techniques like structure from motion to enrich the spatial understanding of the framework. Furthermore, the framework could be extended to handle more complex spatial relationships beyond simple bounding box interactions, such as relative positioning and orientation of objects in 3D space.

While the SPARQ component enhances efficiency, the overall data generation process remains computationally demanding, particularly when scaling to larger datasets or more complex scene configurations. The filtering process, while necessary, adds to the computational overhead. To mitigate this, the authors could explore more efficient predicate evaluation techniques, such as parallel processing or approximate filtering methods. Additionally, the framework could benefit from a more detailed analysis of the computational bottlenecks, identifying specific steps that contribute most to the overall processing time. This would allow for targeted optimizations, such as algorithmic improvements or hardware acceleration. The authors should also consider the trade-off between the quality of the generated data and the computational cost, exploring methods to generate high-quality data with reduced computational resources.

Finally, the paper would benefit from a more comprehensive comparison with existing methods, particularly in terms of computational efficiency and error analysis. While the authors demonstrate the effectiveness of their approach through human evaluations and model performance, a more detailed analysis of the types of errors made by the model and how they compare to other methods would be valuable. This could involve categorizing errors based on the type of spatial relationship or the complexity of the scene. Furthermore, a more thorough comparison of the computational cost of GRAID with other data generation methods would be beneficial, providing a clearer understanding of the trade-offs between accuracy and efficiency. This would allow readers to better assess the practical applicability of the proposed framework.

### Questions

Have you explored the possibility of extending GRAID to incorporate 3D spatial relationships using depth estimation or multi-view setups, and if so, how would this impact the accuracy and computational efficiency of the framework?

### Rating

6

### Confidence

3

**********