### Summary

This paper introduces a new benchmark called LPFQA to evaluate the capabilities of LLMs in handling long-tail, professional knowledge across 20 diverse academic and industrial fields. LPFQA is constructed from real-world professional forums and features four innovations: fine-grained evaluation dimensions, a hierarchical difficulty structure, authentic scenario modeling, and integration of interdisciplinary knowledge. The benchmark consists of 502 tasks that assess LLMs' expertise in specialized areas. The authors conduct experiments on 12 mainstream LLMs, revealing significant performance variations, particularly in specialized reasoning tasks.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

1. The authors propose a new benchmark, LPFQA, to address the limitations of existing benchmarks in evaluating LLMs' abilities to handle long-tail and professional knowledge. The construction process is fully automated, ensuring scalability and reliability.
2. The paper evaluates 12 mainstream LLMs on the proposed benchmark, providing a comprehensive analysis of their performance across different domains. The experiments reveal significant performance disparities among the models, highlighting the challenges of long-tail knowledge.

### Weaknesses

#### Some Related Works


#### comment

1. The motivation of the paper is not clear. The authors should explain the relationship between the long-tail distribution and the professional forums. It is unclear why a long-tail distribution necessitates a professional forum. The authors should clarify why existing benchmarks are insufficient for evaluating long-tail knowledge, and how professional forums specifically address these insufficiencies.
2. The authors claim that the current LLMs exhibit a significant long-tail phenomenon. However, the paper lacks a definition of the long-tail phenomenon and does not provide any experimental results to support this claim. A clear definition of what constitutes the 'long-tail' in the context of LLM performance is needed, along with empirical evidence demonstrating this phenomenon in existing models.
3. The benchmark is not novel. It is a simple combination of multiple community questions. The authors should highlight the unique aspects of their benchmark compared to existing ones. The paper needs to articulate how the specific combination of fine-grained evaluation, hierarchical difficulty, authentic scenarios, and interdisciplinary knowledge makes LPFQA distinct from other benchmarks, rather than just stating it is a combination of community questions.
4. The authors should provide a detailed description of the quality control measures implemented during the construction of the benchmark. The paper lacks sufficient detail on how the quality of the forum data is assessed and ensured, including the specific criteria used for filtering and the process for verifying the accuracy of the questions and answers.
5. The experimental analysis is not sufficient. The authors should provide more in-depth insights into the performance of different LLMs on the proposed benchmark. The analysis should go beyond simply reporting scores, and delve into the specific types of questions where models struggle or excel, and provide a more detailed comparison of model strengths and weaknesses across different domains.

### Suggestions

The paper needs to more clearly articulate the motivation behind using professional forums to address the long-tail knowledge problem. The authors should explain why existing benchmarks are inadequate for evaluating long-tail knowledge and how professional forums specifically overcome these limitations. For example, they could discuss how traditional benchmarks might focus on more general knowledge, while professional forums provide a more nuanced and specialized context. The authors should also clarify the relationship between long-tail distributions and professional forums, explaining why questions from these forums are more likely to represent the kind of rare, specialized knowledge that is characteristic of the long tail. This should include a discussion of how the forum data is selected and filtered to ensure it aligns with the long-tail concept, and how this selection process differs from how data is collected for other benchmarks.

The paper should provide a clear and precise definition of the long-tail phenomenon in the context of LLM performance. This definition should be accompanied by empirical evidence demonstrating that existing LLMs exhibit this phenomenon. For example, the authors could analyze the performance of several LLMs on a range of tasks, showing that their accuracy drops significantly on less frequent or more specialized knowledge. This could involve analyzing the distribution of performance across different types of questions, showing a clear disparity between common and rare knowledge. The authors should also explain how their benchmark specifically measures this long-tail phenomenon, and how the design of LPFQA allows for a more accurate assessment of LLMs' abilities in handling long-tail knowledge. This should include a discussion of how the benchmark's design choices, such as the fine-grained evaluation dimensions and hierarchical difficulty structure, contribute to this assessment.

The authors need to provide a more detailed explanation of the quality control measures implemented during the construction of the benchmark. This should include a description of the specific criteria used for filtering questions and answers, the process for verifying the accuracy of the content, and the methods used to ensure the consistency and reliability of the benchmark. For example, the authors could describe the specific steps taken to remove duplicate or low-quality content, the process for verifying the correctness of answers, and the methods used to ensure that the questions are clear and unambiguous. The authors should also provide more in-depth analysis of the experimental results, going beyond simply reporting scores. This should include a detailed comparison of the performance of different LLMs across various domains, an analysis of the types of questions where models struggle or excel, and a discussion of the potential reasons for these performance differences. The authors should also provide insights into the strengths and weaknesses of each model, and how these relate to the specific characteristics of the benchmark.

### Questions

1. What is the long-tail phenomenon? Can you provide a definition and examples of how it manifests in LLMs?
2. How do professional forums address the challenges of evaluating long-tail knowledge in LLMs?
3. What are the unique aspects of the proposed benchmark compared to existing ones? How does the combination of fine-grained evaluation dimensions, hierarchical difficulty structure, authentic professional scenarios, and interdisciplinary knowledge integration contribute to the novelty of the benchmark?
4. What quality control measures were implemented during the construction of the benchmark? How was the quality of the collected data ensured?
5. Can you provide more in-depth analysis and insights into the performance of different LLMs on the proposed benchmark? What are the strengths and weaknesses of each model in handling long-tail knowledge?

### Rating

3

### Confidence

4

**********