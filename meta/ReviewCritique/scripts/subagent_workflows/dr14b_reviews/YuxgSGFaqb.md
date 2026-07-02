### Summary

This paper introduces SWINGARENA, an adversarial evaluation framework for Large Language Models (LLMs) that approximates real-world software development workflows. SWINGARENA pairs LLMs as submitters, who generate patches, and reviewers, who create test cases and verify the patches through continuous integration (CI) pipelines. The framework includes a retrieval-augmented code generation (RACG) module that handles long-context challenges by providing relevant code snippets from large codebases across multiple programming languages (C++, Python, Rust, and Go). The experiments, using over 400 high-quality real-world GitHub issues, indicate differing behavioral tendencies across models in patch generation versus validation.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The paper introduces a novel adversarial evaluation framework that models real-world software development workflows, which is a significant advancement over static benchmarks.
3. The framework supports multiple programming languages (C++, Python, Rust, and Go) and handles long-context challenges, making it highly relevant for real-world applications.
4. The experiments are comprehensive, involving over 400 high-quality real-world GitHub issues, and provide valuable insights into the behavioral tendencies of different LLMs.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not discuss the computational resources required to run the framework, which could be a concern for researchers with limited access to computing resources.
2. The paper does not provide a detailed analysis of the types of errors that LLMs make in the submission and review process. Understanding these errors could help improve the models and the framework itself.
3. The paper does not discuss the potential for bias in the dataset, which could affect the fairness and generalizability of the evaluation results.

### Suggestions

The paper should include a detailed analysis of the computational resources required to run the framework, including the cost of API calls, memory usage, and processing time. This information is crucial for researchers who may want to use the framework, especially those with limited access to computing resources. The authors should provide a breakdown of the costs associated with different components of the framework, such as the retrieval-augmented code generation module and the continuous integration pipelines. Furthermore, they should explore ways to optimize the framework to reduce its computational footprint, such as using more efficient models or caching intermediate results. This would make the framework more accessible to a wider range of researchers and practitioners.

To improve the framework's utility, the authors should conduct a more in-depth analysis of the types of errors that LLMs make during the submission and review process. This analysis should go beyond simple success/failure metrics and categorize errors based on their nature, such as logical errors, syntax errors, or misunderstandings of the problem description. The authors should also investigate whether certain types of errors are more common in specific programming languages or types of tasks. This detailed error analysis would provide valuable insights into the strengths and weaknesses of LLMs in software development and could help guide future research in this area. Furthermore, it could help in the development of targeted training strategies to improve the performance of LLMs in specific areas.

Finally, the authors should address the potential for bias in the dataset and explore ways to mitigate it. This includes analyzing the distribution of issues across different repositories, programming languages, and complexity levels. The authors should also investigate whether the dataset contains any biases related to the developers who submitted the issues or the reviewers who validated the solutions. Furthermore, the paper should discuss how the framework handles cases where the CI pipeline fails due to issues outside of the submitted patch or review. The authors should also explore the impact of different prompting strategies on the performance of the LLMs and discuss the potential for the framework to be used for training LLMs, rather than just evaluation. These additional analyses and discussions would significantly enhance the paper's contribution and make the framework more robust and reliable.

### Questions

1. Can you provide more details on the computational resources required to run the framework, and the cost of using the API calls for the LLMs?
2. How do you ensure the quality and consistency of the CI pipelines across different programming languages and repositories?
3. What are the most common types of errors that LLMs make in the submission and review process, and how do these errors vary across different programming languages and types of tasks?
4. How do you handle cases where the CI pipeline fails due to issues outside of the submitted patch or review?
5. Have you explored the impact of different prompting strategies on the performance of the LLMs in the submission and review process?
6. Have you considered using the framework for training LLMs, rather than just evaluation?

### Rating

6

### Confidence

4

**********