### Summary

This paper presents LAION-COMP, a large-scale dataset with structural annotations for complex scene generation. The dataset contains 540K+ aesthetic images annotated with detailed scene graphs, explicitly encoding multiple objects, corresponding attributes, and intricate relations. The authors also introduce CompSGen Bench, a benchmark designed to evaluate complex scene generation. The paper demonstrates that models trained on LAION-COMP outperform their prompt-only counterparts and advanced scene-graph-based methods on both the new and existing compositional benchmarks. Additionally, the learned structural conditioning enables fine-grained, object-level image editing.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a large-scale dataset, LAION-COMP, with high-quality structural annotations for complex scene generation. The dataset contains 540K+ aesthetic images annotated with detailed scene graphs, explicitly encoding multiple objects, corresponding attributes, and intricate relations.
2. The paper demonstrates that models trained on LAION-COMP outperform their prompt-only counterparts and advanced scene-graph-based methods on both the new and existing compositional benchmarks.
3. The learned structural conditioning enables fine-grained, object-level image editing, demonstrating its potential as an effective editing interface.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of the proposed dataset and models, including potential biases and failure cases. Specifically, the paper lacks a thorough analysis of how the structural annotations might introduce biases, such as favoring certain object relationships or attribute combinations over others. Furthermore, the paper should explore scenarios where the models fail to generate accurate or coherent compositional scenes, providing specific examples of these failure modes and their potential causes. For instance, how does the model handle complex spatial relationships or occlusions, and are there specific types of objects or attributes that are more prone to errors?
2. While the paper mentions human evaluation, more details on the evaluation process and results would strengthen the claims about the effectiveness of the proposed approach. The paper should include a more detailed description of the human evaluation protocol, including the number of participants, the specific instructions given to them, and the criteria used for assessing the quality of the generated images. Additionally, the paper should provide a more in-depth analysis of the human evaluation results, including statistical significance tests and a discussion of any discrepancies between human judgments and automated metrics. It is also important to understand the inter-annotator agreement to assess the reliability of the human evaluation.

### Suggestions

The paper should include a more comprehensive analysis of the limitations of the LAION-COMP dataset and the proposed models. This should include a detailed investigation into potential biases introduced by the structural annotations. For example, the authors could analyze the distribution of object relationships and attributes in the dataset to identify any imbalances or biases. They could also explore how these biases might affect the performance of the models, particularly in generating diverse and realistic compositional scenes. Furthermore, the paper should provide a more thorough analysis of the failure cases of the models. This should include specific examples of scenarios where the models fail to generate accurate or coherent compositional scenes, along with a discussion of the potential causes of these failures. For instance, the authors could analyze how the models handle complex spatial relationships, occlusions, or unusual object combinations. This analysis should also consider the limitations of the scene graph representation itself, and whether it is sufficient to capture the complexity of real-world scenes. The authors should also consider the impact of the training data on the model's performance, and whether the dataset contains sufficient examples of complex compositional scenes to train robust models.

To strengthen the claims about the effectiveness of the proposed approach, the paper should provide more details on the human evaluation process and results. This should include a detailed description of the evaluation protocol, including the number of participants, the specific instructions given to them, and the criteria used for assessing the quality of the generated images. The authors should also provide a more in-depth analysis of the human evaluation results, including statistical significance tests and a discussion of any discrepancies between human judgments and automated metrics. It is also important to understand the inter-annotator agreement to assess the reliability of the human evaluation. The paper should also consider using a more diverse set of human evaluators, including those with different backgrounds and levels of expertise, to ensure that the evaluation is robust and representative. Furthermore, the paper should explore the use of more fine-grained evaluation metrics that can capture the nuances of compositional accuracy and fidelity, such as metrics that assess the correctness of object relationships and attribute bindings.

Finally, the paper should also discuss the computational cost of the proposed models and the scalability of the approach. This should include an analysis of the training time and memory requirements of the models, as well as the inference time for generating new images. The authors should also discuss the limitations of the current approach in terms of generating very large or complex scenes, and whether there are any potential bottlenecks that could limit the scalability of the approach. The paper should also consider the potential impact of the proposed approach on the broader field of image generation, and whether it could be used to generate other types of images, such as videos or 3D scenes. The authors should also discuss the ethical implications of the proposed approach, particularly in terms of the potential for misuse or bias.

### Questions

1. How does the performance of the proposed models compare to other state-of-the-art text-to-image models on standard benchmarks, and what are the key differences in their approaches?
2. What are the computational costs associated with training and using the proposed models, and how do they compare to existing methods?
3. How does the model handle more complex compositional instructions, and what are the limitations of the current approach in terms of generating very large or complex scenes?
4. Can the proposed approach be extended to other modalities, such as video or 3D scene generation, and what are the potential challenges in doing so?

### Rating

6

### Confidence

4

**********