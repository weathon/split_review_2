### Summary

The paper introduces EditBench, a benchmark designed to evaluate the code editing capabilities of Large Language Models (LLMs) in real-world scenarios. Unlike existing benchmarks, EditBench is based on real-world usage, collecting user instructions and code contexts directly from developers using a VS Code extension. The benchmark comprises 540 problems across multiple natural and programming languages, including Python and JavaScript, and covers diverse use cases such as bug fixing and feature addition. The study evaluates 40 different LLMs, revealing that only one model achieves a pass@1 score above 60%, indicating the challenging nature of the benchmark. The paper also analyzes the impact of contextual information, such as highlighted code and cursor position, on model performance, finding that these factors significantly affect task success rates.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel benchmark, EditBench, which is specifically designed to evaluate the code editing capabilities of LLMs in a realistic setting. This fills a gap in the existing literature, as most current benchmarks focus on code generation from scratch rather than code editing.
2. The data is collected from real-world usage scenarios, making it more representative of actual software development tasks compared to synthetic or educational datasets.
3. The paper provides a comprehensive evaluation of 40 diverse LLMs, offering valuable insights into the current state of LLM code editing capabilities.
4. The analysis of how different levels of contextual information (e.g., highlighted code, cursor position) affect model performance is insightful and can guide future model development.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a detailed analysis of the types of errors that LLMs make when editing code. This would be valuable for understanding the specific challenges that models face and for guiding future research.
2. The paper does not compare the performance of LLMs on EditBench with their performance on other code-related tasks, such as code generation or bug fixing. This makes it difficult to assess the relative strengths and weaknesses of LLMs in code editing compared to other tasks.
3. The paper does not discuss the potential biases that may be present in the collected data. For example, the data may be biased towards certain types of code edits or programming languages, which could affect the generalizability of the benchmark.
4. The paper does not provide a detailed analysis of the computational resources required to run the benchmark. This information is important for researchers who want to use the benchmark, especially those with limited computational resources.

### Suggestions

The authors should conduct a more detailed error analysis, categorizing the types of mistakes made by LLMs during code editing. This analysis should go beyond simple pass/fail metrics and delve into the specific reasons for failure. For example, are models struggling with understanding the context of the code, or are they making syntactic errors? Are they failing to correctly interpret the user's instructions, or are they generating code that is semantically incorrect? A breakdown of error types, such as incorrect logic, syntax errors, or failure to adhere to coding style guidelines, would be beneficial. Furthermore, the analysis should investigate whether certain types of edits are more challenging than others, such as bug fixes versus feature additions. This detailed error analysis would provide valuable insights into the specific weaknesses of current LLMs in code editing and guide future research efforts to address these limitations.

To better contextualize the performance of LLMs on EditBench, the authors should compare their results with performance on other code-related benchmarks. This comparison should include tasks such as code generation, code summarization, and bug fixing. For example, how do models that perform well on code generation tasks fare on EditBench? Are models that are specifically trained for bug fixing more effective on EditBench compared to general-purpose LLMs? This comparative analysis would help to identify the specific strengths and weaknesses of LLMs in code editing relative to other code-related tasks. It would also help to determine whether the challenges posed by EditBench are unique to code editing or whether they are shared with other code-related tasks. This analysis should also consider the types of contextual information used in different benchmarks, as this can significantly impact model performance.

Finally, the authors should provide a more detailed discussion of the potential biases in the collected data and the computational resources required to run the benchmark. The authors should analyze the distribution of code edits across different programming languages and identify any potential biases towards specific languages or types of code. They should also analyze the distribution of edit types (e.g., bug fixes, feature additions) to ensure that the benchmark is representative of real-world code editing tasks. Furthermore, the authors should provide a detailed breakdown of the computational resources required to run the benchmark, including the time taken to run the tests, the memory usage, and the hardware requirements. This information is crucial for researchers who want to use the benchmark, especially those with limited computational resources. The authors should also discuss the scalability of the benchmark and whether it can be used to evaluate larger models or more complex code editing tasks.

### Questions

1. How do the authors plan to address the issue of data contamination, given that the benchmark is based on real-world data that may be available online?
2. Can the authors provide more details on the process of collecting user instructions and code contexts? How did they ensure the quality and diversity of the collected data?
3. How do the authors plan to maintain and update the benchmark over time, given that software development practices and programming languages are constantly evolving?

### Rating

6

### Confidence

3

**********