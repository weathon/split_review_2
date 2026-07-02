### Summary

This paper introduces an approach to in-context image editing by training a model directly on video data, eliminating the need for task-specific pipelines and expert models. The authors develop a scalable method to annotate videos as interleaved multimodal sequences and design three proxy tasks—next-image prediction, current segmentation prediction, and next-segmentation prediction—to facilitate learning. They also propose a new multi-turn image editing benchmark. Extensive experiments show that the model achieves strong in-context editing capabilities and state-of-the-art results on two multi-turn editing benchmarks. Despite being trained solely on video data, the model demonstrates promising performance in multi-concept composition, story generation, and chain-of-editing applications.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel approach to in-context image editing by training a model directly on video data, which is a creative and original solution to the challenge of acquiring contextualized training data. This approach leverages the rich, dynamic information in videos to learn multi-turn interactions, which is a fresh perspective in the field of image editing.

2. The paper presents a well-structured and logically coherent methodology. The construction of the interleaved multimodal sequence, the design of the three proxy tasks, and the training process are clearly explained and well-integrated.

3. The paper provides a thorough evaluation of the proposed model, using both existing and newly proposed benchmarks. The results demonstrate the model's strong performance and its ability to generalize to various editing tasks, which is a testament to the robustness of the approach.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of the proposed approach. For example, how does the model handle cases where the video data does not adequately represent the desired editing task? Are there specific types of edits or scenarios where the model struggles, and if so, why? The paper should delve deeper into the failure modes of the model, particularly when the video data lacks explicit examples of the desired edit. For instance, if the model is trained on videos where objects are added in specific locations, how does it perform when asked to add an object in a novel location not seen in the training data? This is a critical aspect that needs further exploration.

2. The paper could provide more details on the computational resources required for training and inference. This information is crucial for assessing the scalability and practicality of the proposed approach. The paper should specify the exact hardware used, including the type and number of GPUs, CPU, and memory, as well as the training time for different model sizes and dataset sizes. This level of detail is necessary for other researchers to reproduce the results and understand the resource requirements of the method.

3. The paper could benefit from a more thorough comparison with existing image editing methods, particularly those that do not rely on video data. This would help to better contextualize the advantages and disadvantages of the proposed approach. The comparison should not only focus on quantitative metrics but also on qualitative aspects, such as the visual quality of the edited images and the types of edits that each method can handle. A more comprehensive comparison would help to highlight the unique contributions of this work and its limitations compared to other approaches.

### Suggestions

To address the limitations regarding the model's handling of novel editing scenarios, the authors should explore techniques to improve the model's generalization capabilities. This could involve incorporating data augmentation strategies that introduce variations in object placement and editing instructions during training. For example, the model could be trained with synthetic edits where objects are added in random locations, or by using techniques like inpainting to create diverse training examples. Additionally, the authors could investigate the use of attention mechanisms that allow the model to focus on the relevant parts of the image and instruction, which could help it to better understand the desired edit even in novel situations. Furthermore, exploring methods to explicitly model the relationship between the editing instruction and the spatial location of the edit could be beneficial. This could involve incorporating spatial information into the model's input or using techniques like spatial transformers to guide the editing process.

To provide a more comprehensive analysis of the computational resources required, the authors should include a detailed breakdown of the training and inference times for different model sizes and dataset sizes. This should include the exact hardware specifications, such as the type and number of GPUs, CPU, and memory, as well as the training time for each configuration. The authors should also report the inference time for different image resolutions and model sizes. This information is crucial for other researchers to understand the resource requirements of the method and to reproduce the results. Furthermore, the authors should discuss the scalability of the approach and how the computational cost scales with the size of the training data and the model complexity. This would provide a more complete picture of the practicality of the proposed approach.

To enhance the comparison with existing image editing methods, the authors should include a more detailed qualitative analysis of the edited images. This should involve a visual comparison of the results produced by the proposed method and other state-of-the-art techniques, highlighting the strengths and weaknesses of each approach. The authors should also discuss the types of edits that each method can handle and the limitations of each approach. For example, the authors could compare the visual quality of the edited images, the consistency of the edits with the input instruction, and the ability of the method to handle complex editing scenarios. This would provide a more comprehensive understanding of the advantages and disadvantages of the proposed approach compared to other methods. Furthermore, the authors should consider including a user study to evaluate the perceptual quality of the edited images, which would provide a more subjective assessment of the method's performance.

### Questions

1. How does the model handle cases where the video data does not adequately represent the desired editing task? Are there specific types of edits or scenarios where the model struggles, and if so, why?

2. What are the computational resources required for training and inference? This information is crucial for assessing the scalability and practicality of the proposed approach.

3. How does the proposed method compare to existing image editing methods, particularly those that do not rely on video data? A more thorough comparison would help to better contextualize the advantages and disadvantages of the proposed approach.

### Rating

6

### Confidence

3

**********