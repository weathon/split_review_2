### Summary

This paper introduces a benchmark called **CATS-Bench** for time series captioning and multiple-choice questions about time series. The benchmark is derived from 11 diverse real-world datasets and includes tasks such as time series captioning, time series matching, caption matching, plot matching, and time series comparison. The authors also propose tailored evaluation metrics and benchmark leading Vision-Language Models (VLMs), highlighting both their strengths and persistent limitations.

### Soundness

2

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The benchmark is comprehensive, covering five different tasks. It includes time series data, metadata, and visual plots, making it a robust tool for evaluating time series captioning and reasoning.
3. The authors provide a scalable pipeline for generating high-quality captions, which is validated through factual checks and human indistinguishability studies.

### Weaknesses

#### Some Related Works


#### comment

1. The benchmark is derived from existing datasets, and the caption generation pipeline relies on existing LLMs, which may limit the novelty of the benchmark.

2. The oracle LLMs may introduce biases or inaccuracies that could affect the quality of the captions. The paper does not discuss how to ensure the reliability of the oracle LLMs.

3. The human-revisited subset is relatively small compared to the entire benchmark, which may not be sufficient to ensure the quality of the benchmark.

4. The paper does not provide a detailed analysis of the limitations of the proposed benchmark, such as potential biases in the datasets or limitations in the caption generation pipeline.

5. The evaluation metrics may not fully capture the quality of the generated captions, and the paper does not discuss the limitations of the evaluation metrics.

6. The benchmark may not be scalable to larger datasets or more complex time series captioning tasks.

### Suggestions

The paper should more thoroughly address the potential for bias introduced by the oracle LLMs used in the caption generation pipeline. While human revision is mentioned, a more detailed analysis of the types of errors and biases observed in the initial LLM-generated captions would be beneficial. This should include specific examples of inaccuracies or misleading statements produced by the oracle models, and a discussion of how these issues were identified and mitigated during the human revision process. Furthermore, the paper should explore the potential for systematic biases that may remain even after human revision, and how these biases could impact the evaluation of models trained on the benchmark. A quantitative analysis of the frequency and types of errors corrected during human revision would also strengthen the paper's claims about the quality of the benchmark.

To further enhance the benchmark's robustness, the authors should provide a more detailed discussion of the limitations of the evaluation metrics used. While the paper acknowledges that no single metric is perfect, it does not fully explore the potential shortcomings of the chosen metrics in capturing the nuances of time series captioning. For example, the paper could discuss how the metrics handle captions that are technically accurate but lack important contextual information, or captions that are verbose but do not add significant value. A more in-depth analysis of the correlation between the automated metrics and human judgments would be valuable, including a discussion of cases where the metrics disagree with human evaluators. The paper should also consider the use of additional evaluation metrics that could capture different aspects of caption quality, such as the degree of detail, the clarity of expression, and the relevance to the time series data.

Finally, the paper should provide a more comprehensive analysis of the scalability of the benchmark. While the authors claim that the data collection pipeline is robust and scalable, they do not provide sufficient evidence to support this claim. The paper should discuss the computational resources required to generate captions for larger datasets, and the potential challenges in maintaining the quality of the captions as the dataset size increases. The authors should also consider the limitations of the current benchmark in terms of the complexity of the time series data, and how the benchmark could be extended to include more complex time series, such as those with multiple channels, irregular sampling, or non-stationary behavior. A discussion of the trade-offs between scalability and caption quality would also be beneficial.

### Questions

Please refer to the weaknesses.

### Rating

5

### Confidence

4

**********