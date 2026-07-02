### Summary

This paper proposes a new foundation model for crowdsourced label aggregation called CrowdFM, which aims to address the challenge of inferring ground truth from noisy, crowdsourced labels. The authors point out that the dominant paradigm of dataset-specific parameter estimation is not scalable and cannot transfer knowledge between datasets. They also note that recent efforts toward universal aggregation models do not account for the structural and behavioral complexities of human-annotated crowdsourcing, resulting in poor real-world performance.

To address these limitations, CrowdFM is designed as a bipartite graph neural network that is pre-trained on a vast, domain-randomized synthetic dataset to learn diverse behavioral patterns. The model uses a size-invariant initialization and attention-based message passing to learn universal principles of collective intelligence. The authors claim that their single, fixed model consistently matches or surpasses bespoke, per-dataset methods in both accuracy and efficiency across 22 real-world benchmarks.

In addition to label aggregation, the representations learned by CrowdFM are said to readily support diverse downstream applications, such as worker assessment and task assignment. The authors provide extensive experimental results to demonstrate the effectiveness of their approach and make their code available to the public.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel foundation model, CrowdFM, for crowdsourced label aggregation that addresses the limitations of existing approaches. The concept of a foundation model for this task is relatively new, and the authors provide a clear motivation for its development.
2. The authors conduct extensive experiments on 22 real-world benchmarks to evaluate the performance of CrowdFM. This comprehensive evaluation demonstrates the robustness and generalizability of the proposed model across diverse datasets and scenarios. 
3. The paper is well-organized and easy to follow. The authors provide a clear problem formulation, detailed methodology, and comprehensive experimental results. 
4. The authors make their code publicly available, which enhances the reproducibility of their results and facilitates further research in this area.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of the proposed approach. While the authors mention some limitations in the conclusion, a more thorough analysis of potential weaknesses and areas for improvement would strengthen the paper. Specifically, the paper lacks a discussion on the sensitivity of the model to the quality and diversity of the synthetic pre-training data. The performance of CrowdFM is likely contingent on the synthetic data accurately reflecting the complexities of real-world crowdsourcing scenarios, and this dependency should be explored more thoroughly. Furthermore, the paper should discuss the computational cost associated with pre-training the model, as this could be a barrier to adoption for some researchers.
2. The synthetic data generation process is a crucial component of the proposed approach, yet it is not discussed in sufficient detail in the main body of the paper. Providing more information about the data generation process, including the distributions used to sample worker abilities, task difficulties, and other parameters, would enhance the reproducibility and understanding of the results. The current description is too high-level and lacks the necessary specifics for other researchers to replicate the data generation process. For example, the specific ranges and distributions used for sampling worker abilities and task difficulties should be explicitly stated.

### Suggestions

The paper would benefit from a more in-depth analysis of the synthetic data generation process. Specifically, the authors should provide details on the distributions used to sample worker abilities, task difficulties, and other parameters. This should include the specific ranges and parameters of the distributions, as well as the rationale behind the choices. For example, if worker abilities are sampled from a beta distribution, the parameters of the distribution should be provided, and the reason for choosing a beta distribution over other distributions should be explained. Furthermore, the paper should include an analysis of the sensitivity of the model to the parameters of the synthetic data generation process. This would help to understand how the model's performance is affected by the quality and diversity of the synthetic data. For example, the authors could conduct experiments where they vary the parameters of the distributions used to sample worker abilities and task difficulties and analyze the impact on the model's performance on real-world datasets. This analysis would provide valuable insights into the robustness of the model and its applicability to different crowdsourcing scenarios.

Additionally, the paper should include a more detailed discussion of the computational cost associated with pre-training the model. This should include the time and resources required for pre-training, as well as the impact of different hyperparameter settings on the computational cost. This information is crucial for researchers who are considering adopting the model, as it will help them to assess the feasibility of using the model for their own research. The authors could also explore techniques for reducing the computational cost of pre-training, such as using more efficient optimization algorithms or reducing the size of the pre-training dataset. Furthermore, the paper should discuss the limitations of the model in terms of its ability to handle very large datasets or datasets with highly complex annotation patterns. This would help to clarify the scope of the model and its applicability to different types of crowdsourcing tasks.

Finally, the paper should include a more thorough analysis of the model's performance on different types of crowdsourcing tasks. While the authors have conducted experiments on 22 real-world benchmarks, it would be useful to analyze the model's performance on specific types of tasks, such as image classification, text annotation, or sound event recognition. This would help to identify the strengths and weaknesses of the model and its suitability for different applications. For example, the authors could analyze the model's performance on datasets with varying levels of annotation noise or datasets with different types of worker behavior. This analysis would provide a more nuanced understanding of the model's capabilities and limitations.

### Questions

Please refer to the weakness.

### Rating

6

### Confidence

3

**********