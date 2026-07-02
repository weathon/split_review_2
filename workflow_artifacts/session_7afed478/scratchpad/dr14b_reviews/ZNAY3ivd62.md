### Summary

This paper introduces GUI-Spotlight, a novel visual grounding model designed to enhance GUI systems by dynamically narrowing its focus to relevant screen regions through the use of specialized tools. The model employs a three-stage training process, including supervised fine-tuning and reinforcement learning, to effectively coordinate these tools. The authors also developed a high-resolution dataset specifically for GUI visual grounding tasks, which they used to train and evaluate GUI-Spotlight. The model demonstrates competitive performance on multiple benchmarks, including ScreenSpot-Pro, UI-Vision, and OSWorld-G, outperforming other models with similar parameter sizes.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper is well-written and easy to follow.
- The proposed method is novel, and the experiments demonstrate its effectiveness.
- The authors provide a detailed analysis of the RL training process, including ablation studies on different reward designs and RL algorithms.
- The authors developed a high-resolution dataset specifically for GUI visual grounding tasks, which is a valuable contribution to the field.
- The model achieves competitive performance on multiple benchmarks, outperforming other models with similar parameter sizes.

### Weaknesses

#### Some Related Works


#### comment

 - The paper lacks a detailed analysis of the computational resources required for training and deploying GUI-Spotlight. This information is crucial for assessing the practicality of the model in real-world applications.
- The paper does not discuss the potential limitations of the model in handling dynamic or frequently changing GUI elements. This is an important consideration for real-world GUI systems, where the interface may change frequently.
- The paper does not provide a detailed analysis of the model's failure cases. Understanding when and why the model fails is important for identifying areas for improvement and for assessing the model's robustness.
- The paper does not discuss the potential impact of the model on user experience. While the model is designed to improve GUI systems, it is important to consider how it may affect the user's interaction with the system.

### Suggestions

The paper should include a more thorough analysis of the computational demands of GUI-Spotlight. Specifically, the authors should provide details on the training time, GPU memory usage, and inference latency. This should include a breakdown of the computational cost associated with each stage of the model, such as the tool coordination and the visual grounding process. Furthermore, it would be beneficial to compare the computational requirements of GUI-Spotlight with other state-of-the-art models in the field. This analysis should also consider the scalability of the model, i.e., how the computational cost increases with the size of the input image or the complexity of the GUI. Such information is critical for assessing the practicality of deploying the model in real-world applications, especially those with limited computational resources.

To address the limitations regarding dynamic GUI elements, the authors should investigate the model's performance on interfaces that undergo frequent changes. This could involve evaluating the model on a dataset that includes GUIs with animations, transitions, or other dynamic elements. The analysis should focus on how well the model adapts to these changes and whether it can maintain accurate visual grounding. The authors should also consider incorporating techniques that allow the model to handle dynamic elements, such as using temporal information or employing a recurrent architecture. Furthermore, the paper should discuss the potential impact of these dynamic elements on the model's performance and provide insights into how the model can be improved to handle such scenarios. This is crucial for ensuring the model's robustness in real-world applications.

Finally, the paper should include a more detailed analysis of the model's failure cases. This should involve categorizing the types of errors the model makes and identifying the underlying reasons for these failures. For example, the authors could analyze cases where the model fails to identify the correct GUI element due to visual ambiguity, occlusion, or complex layouts. This analysis should also include a discussion of the model's limitations and potential areas for improvement. Furthermore, the paper should discuss the potential impact of the model on user experience. This could involve evaluating the model's performance in terms of user satisfaction, task completion time, and error rates. The authors should also consider the potential for the model to introduce new types of errors or to negatively impact the user's interaction with the system.

### Questions

- How does the model handle cases where the target element is not clearly defined or is ambiguous?
- Can the authors provide more details on the specific scenarios where GUI-Spotlight excels or struggles compared to other models?
- What are the potential real-world applications of GUI-Spotlight beyond the benchmarks used in the paper?

### Rating

6

### Confidence

3

**********