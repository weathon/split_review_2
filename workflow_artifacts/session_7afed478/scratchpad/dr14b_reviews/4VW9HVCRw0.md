### Summary

This paper proposes a novel task of free-form hand-object interaction generation, which aims to generate controllable, diverse, and physically plausible hand-object interactions conditioned on fine-grained intent, including non-grasping actions. To support this task, the authors construct a large-scale, in-the-wild 3D HOI dataset, WildO2, which includes non-grasping motions derived from internet videos. The authors also propose a three-stage framework, TOUCH, which uses a multi-level diffusion model to generate versatile hand poses beyond grasping priors. The framework is refined with contact consistency and physical constraints to ensure realism. The paper demonstrates the effectiveness of the proposed method through comprehensive experiments.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a new task of free-form hand-object interaction generation, which is a significant advancement over traditional grasp-centric approaches.
2. The construction of the WildO2 dataset is a major contribution, providing a valuable resource for the research community with its diversity in objects, actions, and contact details.
3. The proposed TOUCH framework is technically sound, with a well-designed three-stage process that effectively combines contact modeling, diffusion-based generation, and physical constraints.
4. The paper is well-structured and clearly explains the methodology, experiments, and results, making it accessible to readers with a background in the field.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of the WildO2 dataset, such as potential biases in object representation or interaction types. Specifically, the dataset's reliance on internet videos might introduce biases towards certain object categories or interaction styles that are more frequently captured in such videos. For example, interactions with everyday objects might be overrepresented compared to specialized tools or objects from specific cultural contexts. Furthermore, the method used to extract HOI data from these videos might inadvertently favor certain types of interactions that are easier to detect or reconstruct, leading to an unbalanced dataset.
2. The evaluation metrics, while comprehensive, could be expanded to include more user-centric measures, such as perceived naturalness and usability in real-world applications. The current metrics primarily focus on quantitative measures of contact and pose accuracy, but they do not fully capture the subjective experience of human users interacting with the generated HOIs. Metrics that assess the perceived naturalness of the interactions, such as how realistic and intuitive they appear to a human observer, would be valuable. Additionally, evaluating the usability of the generated HOIs in practical applications, such as VR/AR scenarios or robotic manipulation tasks, would provide a more holistic assessment of the framework's effectiveness.
3. The paper does not extensively discuss the computational requirements and scalability of the TOUCH framework, which could be important for practical applications. The computational cost of training and running the diffusion model, as well as the memory requirements for storing the dataset and intermediate results, should be clearly stated. Furthermore, the scalability of the framework to handle more complex scenes with multiple objects and interactions should be addressed. This is crucial for determining the feasibility of deploying the framework in real-world applications.

### Suggestions

To address the limitations of the WildO2 dataset, the authors should conduct a thorough analysis of potential biases. This could involve examining the distribution of object categories and interaction types within the dataset and comparing it to real-world distributions. They could also investigate whether certain types of interactions are overrepresented due to the method used for data extraction. Furthermore, the authors should consider augmenting the dataset with data from diverse sources to mitigate these biases. For example, they could incorporate data from robotics datasets or create synthetic data using simulation environments to ensure a more balanced representation of objects and interactions. This would improve the generalizability of the framework and make it more robust to real-world scenarios.

To enhance the evaluation metrics, the authors should incorporate user-centric measures such as perceived naturalness and usability. This could involve conducting user studies where participants are asked to rate the naturalness and intuitiveness of the generated HOIs. The authors could also evaluate the usability of the generated HOIs in practical applications by integrating them into VR/AR scenarios or robotic manipulation tasks. For example, they could measure the success rate of a robot performing a task using the generated HOIs or assess the user experience in a VR environment. These user-centric evaluations would provide a more comprehensive assessment of the framework's effectiveness and its potential for real-world applications. Additionally, the authors should consider using metrics that quantify the diversity of generated interactions, ensuring that the framework can produce a wide range of realistic and varied HOIs.

Finally, the authors should provide a detailed analysis of the computational requirements and scalability of the TOUCH framework. This should include the computational cost of training and running the diffusion model, as well as the memory requirements for storing the dataset and intermediate results. The authors should also discuss the scalability of the framework to handle more complex scenes with multiple objects and interactions. This could involve conducting experiments with varying numbers of objects and interactions and measuring the corresponding changes in computational cost and memory usage. Furthermore, the authors should explore potential optimizations to improve the efficiency of the framework, such as using more efficient diffusion sampling techniques or implementing parallel processing. This would make the framework more practical for real-world applications and facilitate its adoption by the research community.

### Questions

1. How does the framework handle interactions with deformable objects or objects with complex geometries?
2. Could the authors elaborate on the potential for extending the framework to handle multi-hand interactions or interactions involving multiple objects?
3. What are the specific challenges in scaling the WildO2 dataset, and how might these be addressed in future work?
4. How does the TOUCH framework compare to other state-of-the-art methods in terms of computational efficiency and resource requirements?

### Rating

6

### Confidence

3

**********