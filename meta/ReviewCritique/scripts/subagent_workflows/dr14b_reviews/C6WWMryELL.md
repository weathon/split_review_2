### Summary

This paper studies the length volatility problem of LLMs in long-form generation. It proposes a benchmark to measure the length volatility of LLMs and analyses the internal mechanisms behind the length volatility. Finally, it proposes a decoding-stage method to mitigate the length volatility problem.

### Soundness

3

### Presentation

3

### Contribution

2

### Strengths

1. This paper conducts a systematic study on the length volatility of LLMs, which has been neglected in previous research.
2. This paper proposes a benchmark to measure the length volatility. The benchmark covers both structured and unstructured tasks, and considers both English and Chinese.
3. This paper proposes a decoding-stage method to mitigate the length volatility, which is practically useful.

### Weaknesses

#### Some Related Works


#### comment

1. The internal mechanism behind the length volatility remains unclear. The authors argue that the length volatility is caused by attention collapse and attention instability. However, the argument is not supported by empirical evidence. For example, the authors can quantify the correlation between attention patterns and length volatility. Furthermore, the claim of attention collapse is not well-defined. It is unclear what specific attention patterns are considered 'collapsed' and how this differs from normal attention behavior during long sequence generation. The authors should provide a more rigorous definition and analysis of this phenomenon.
2. The proposed benchmark is too difficult for current LLMs, as even a specialized long-form generation model LongWriter fails to generate long and high-quality responses. The benchmark's difficulty raises concerns about its practical relevance and whether it truly isolates length volatility or simply tests the limits of current models' generation capabilities. The fact that even a model designed for long-form generation struggles suggests the benchmark might be measuring a combination of factors, not just length volatility.
3. The proposed method relies on the predefined section titles, which limits its application in more general scenarios. The method's reliance on explicit section titles makes it less applicable to tasks where the structure is not predefined or where the user does not have control over the section titles. This limits the method's generalizability and practical use in real-world scenarios.

### Suggestions

To strengthen the analysis of the internal mechanisms behind length volatility, the authors should provide a more rigorous definition of 'attention collapse' and 'attention instability.' This should include a quantitative measure of attention patterns, such as the entropy or variance of attention weights, and demonstrate how these measures correlate with the observed length volatility. For example, the authors could track the attention weights of specific tokens related to length constraints and show how their attention patterns change during the generation process. Furthermore, the authors should explore the relationship between attention patterns and the generated length, perhaps by plotting the attention weights against the generated tokens to visualize the correlation. This would provide a more concrete and empirical basis for their claims about the internal mechanisms of length volatility. The analysis should also consider the impact of different attention heads and layers, as some heads might be more sensitive to length constraints than others.

To address the issue of the benchmark's difficulty, the authors should consider creating a series of benchmarks with varying levels of difficulty. This would allow for a more nuanced evaluation of LLMs' length volatility at different scales and would help to isolate the length volatility problem from other limitations of current models. For example, the authors could create a benchmark with shorter sequences and fewer sections to test the models' basic ability to control length, and then gradually increase the difficulty to test the limits of the models. Additionally, the authors should provide a more detailed analysis of the performance of different models on the benchmark, including the types of errors they make and the specific scenarios where they struggle the most. This would provide a better understanding of the challenges posed by the benchmark and how it relates to the length volatility problem. The authors should also consider comparing the benchmark to existing long-form generation benchmarks to highlight its unique contributions.

To improve the generalizability of the proposed method, the authors should explore ways to adapt it to scenarios without predefined section titles. One possible approach is to use the model itself to generate section titles dynamically during the generation process. This could be done by adding a mechanism that prompts the model to generate a section title after a certain number of tokens or when a certain condition is met. The authors could also explore the use of reinforcement learning to train the model to generate section titles that are optimal for controlling length volatility. Furthermore, the authors should provide a more detailed analysis of the limitations of the proposed method and discuss potential future directions for research. This would help to clarify the scope of the method and its potential for practical applications.

### Questions

1. What is the internal mechanism behind the length volatility? Why does the attention trace help to mitigate the length volatility?
2. How does the proposed method affect the quality of the generated responses? Does the proposed method help to improve the quality of the generated responses? Does the proposed method hurt the quality of the generated responses?

### Rating

5

### Confidence

4

**********