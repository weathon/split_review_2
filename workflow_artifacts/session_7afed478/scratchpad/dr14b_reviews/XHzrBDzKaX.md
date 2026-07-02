### Summary

This paper introduces a new benchmark called **VisFactor** for evaluating the visual cognitive abilities of Multimodal Large Language Models (MLLMs). The benchmark consists of 20 tasks adapted from the **Factor-Referenced Cognitive Test (FRCT)**, covering key areas of visual cognition such as spatial reasoning, memory, and perceptual skills. The authors systematically evaluate 23 MLLMs on VisFactor, revealing significant limitations in their performance, particularly in tasks involving mental rotation, spatial inference, and figure-ground discrimination.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- **Originality**: The paper introduces a novel benchmark, VisFactor, which adapts tasks from established cognitive tests (FRCT) for evaluating MLLMs. This approach brings a fresh perspective by grounding MLLM evaluation in human cognitive science, addressing a gap in existing benchmarks that often focus on task-specific performance rather than foundational visual reasoning skills.

- **Quality**: The benchmark is carefully designed to reduce chance-level accuracy and includes both original and synthetically generated test cases, ensuring robustness and scalability. The evaluation is thorough, covering a wide range of models and prompting techniques.

- **Clarity**: The paper is well-organized, with clear explanations of the benchmark design, task variations, and evaluation protocols. The figures and tables effectively illustrate the tasks and results.

- **Significance**: The findings highlight critical gaps in MLLMs' visual reasoning abilities, despite high performance on other benchmarks. This work challenges the assumption that large-scale pretraining alone suffices for human-like visual cognition, providing valuable insights for future research and development in multimodal AI.

### Weaknesses

#### Some Related Works


#### comment

 - **Synthetic Data Limitations**: While the synthetic data generation is a strength for scalability, the paper could benefit from a deeper analysis of how well synthetic tasks mirror the complexity of real-world visual reasoning. Are there specific cognitive skills that synthetic data fails to capture effectively?

- **Model Interpretability**: The paper could explore in more depth why certain models perform better on specific tasks. A more detailed error analysis could provide insights into the models' strengths and weaknesses.

- **Task Difficulty Calibration**: The paper mentions controllable difficulty but lacks a detailed analysis of how difficulty levels are calibrated and validated. A clearer explanation of the difficulty metrics and their impact on model performance would be beneficial.

### Suggestions

The paper introduces a valuable benchmark, but further investigation into the synthetic data's representativeness is needed. While the authors mention that the synthetic data is based on the same principles as the original FRCT tasks, a more rigorous analysis is required to ensure that the generated tasks capture the full spectrum of cognitive skills assessed by the original tests. For example, the paper could include a comparison of model performance on original versus synthetic tasks, specifically looking for discrepancies that might indicate limitations in the synthetic data. This analysis should not only focus on overall accuracy but also on the types of errors made by the models, which could reveal specific cognitive skills that are not well-captured by the synthetic data. Furthermore, the paper should explore the impact of different parameters used in the synthetic data generation process on the difficulty and nature of the generated tasks. This would help in understanding the limitations of the synthetic data and how it can be improved to better reflect real-world visual reasoning challenges.

To enhance the interpretability of the results, the paper should include a more detailed error analysis, focusing on the specific types of errors made by the models on different tasks. This analysis should go beyond simply identifying the tasks where models perform poorly and should delve into the underlying reasons for these failures. For instance, in tasks involving mental rotation, the paper could analyze whether the models struggle with specific angles of rotation or particular types of objects. Similarly, in tasks involving figure-ground discrimination, the paper could investigate whether the models are more likely to fail with certain types of visual patterns or levels of complexity. This detailed error analysis should be coupled with a discussion of the architectural differences between the models, which could help in understanding why certain models are better suited for specific types of visual reasoning tasks. This would provide valuable insights for future model development and benchmark design.

Finally, the paper should provide a more detailed explanation of how the difficulty levels are calibrated and validated. While the authors mention that the difficulty is controlled by key question parameters, a more rigorous analysis is needed to understand how these parameters affect the cognitive load required to solve the tasks. For example, the paper could include a psychometric analysis of the generated tasks, which would help in quantifying the difficulty of each task and validating the effectiveness of the difficulty control mechanism. This analysis should also explore the relationship between the difficulty parameters and the types of errors made by the models, which could provide insights into the specific cognitive skills that are affected by the difficulty level. Furthermore, the paper should discuss the limitations of the current difficulty control mechanism and suggest potential improvements for future work.

### Questions

- **Model Interpretability**: The paper could explore in more depth why certain models perform better on specific tasks. A more detailed error analysis could provide insights into the models' strengths and weaknesses.

- **Task Difficulty Calibration**: The paper mentions controllable difficulty but lacks a detailed analysis of how difficulty levels are calibrated and validated. A clearer explanation of the difficulty metrics and their impact on model performance would be beneficial.

### Rating

6

### Confidence

3

**********