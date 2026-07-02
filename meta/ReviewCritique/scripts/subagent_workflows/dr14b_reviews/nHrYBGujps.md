### Summary

This paper introduces BIRD-INTERACT, a benchmark designed to evaluate LLMs in a dynamic text-to-SQL environment. The contributions include 1) a high-fidelity interactive environment, 2) two evaluation settings, 3) a comprehensive and challenging task suite. The interactive environment couples each database with a hierarchical knowledge base, metadata files, and a function-driven user simulator. The two evaluation settings reflect real-world interaction settings, with c-Interact having a predefined conversational protocol and a-Interact allowing the model more autonomy. The task suite covers the full CRUD spectrum and includes ambiguous and follow-up sub-tasks. The authors' experiments show that state-of-the-art models struggle with BIRD-INTERACT, highlighting the difficulty of the benchmark.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The authors have created a comprehensive benchmark that more closely resembles real-world applications than previous text-to-SQL benchmarks. The inclusion of a hierarchical knowledge base, metadata files, and a function-driven user simulator in the interactive environment is a significant improvement.
2. The authors provide a thorough analysis of the performance of different LLMs on the benchmark, offering valuable insights into the strengths and weaknesses of various models. The findings highlight the importance of effective interaction for achieving success in dynamic text-to-SQL tasks.

### Weaknesses

#### Some Related Works


#### comment

1. The scale of this work seems to be not larger than previous works. For example, the number of tasks in BIRD-INTERACT-FULL is 600, while the number of tasks in the BIRD dataset is 2000. 
2. Although this work is more complex than previous works, the authors only use close-source LLMs for evaluation. I think it is better to include some open-source LLMs, which can provide more insights for the community.

### Suggestions

The authors should consider expanding the number of tasks in the BIRD-INTERACT-FULL dataset to better align with the scale of existing benchmarks like the BIRD dataset, which contains 2000 tasks. While the focus on interactive and multi-turn scenarios is a valuable contribution, the relatively small size of the dataset may limit its utility for training and evaluating models. A larger dataset would allow for more robust training of models and a more comprehensive evaluation of their performance. Furthermore, increasing the number of tasks would also allow for a more granular analysis of model performance across different types of interactions and database operations. This could involve creating more diverse scenarios with varying levels of ambiguity and complexity, which would further enhance the benchmark's value.

To address the limitation of only using closed-source LLMs, the authors should include a more diverse set of open-source models in their evaluation. This would not only make the benchmark more accessible to the research community but also provide valuable insights into the performance of different types of models. Specifically, the authors should consider including models with different architectures and training methodologies, such as those based on transformers and recurrent neural networks. This would allow for a more comprehensive comparison of the strengths and weaknesses of different models and provide a better understanding of the factors that contribute to successful performance on the BIRD-INTERACT benchmark. Furthermore, the inclusion of open-source models would facilitate further research and development in the field by allowing researchers to build upon the results of this work.

Finally, the authors should provide more detailed information about the types of ambiguities and follow-up tasks included in the benchmark. This would help researchers better understand the challenges posed by the benchmark and develop more effective strategies for addressing them. For example, the authors could provide a taxonomy of the different types of ambiguities and follow-up tasks, along with examples of each. This would also help in the development of more targeted evaluation metrics that can capture the nuances of model performance on these types of tasks. Additionally, the authors should consider releasing the code used to generate the benchmark, which would further enhance its accessibility and utility for the research community.

### Questions

1. For the User Simulator, how do the authors ensure that the simulated users are realistic and representative of real-world users? What methods do the authors use to validate the realism of the simulated users?
2. The authors mention that the a-Interact setting allows the model to autonomously decide when to query the user simulator or explore the DB environment. How do the authors evaluate the model's decision-making process in this setting? What metrics do the authors use to measure the effectiveness of the model's decisions?

### Rating

6

### Confidence

4

**********