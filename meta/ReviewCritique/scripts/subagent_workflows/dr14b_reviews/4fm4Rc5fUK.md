### Summary

The paper proposes an approach to autoformalization that integrates feedback from tools that check the syntactic validity and semantic consistency of the generated formal statements. The approach, called Autoformalizer with Tool Feedback (ATF), consists of two main components: a syntax check tool that uses the Lean 4 compiler to provide compilation feedback, and a consistency check tool that uses a multi-LLMs-as-judge approach to validate the semantic equivalence between informal and formal expressions. The training of ATF involves three phases: a cold-start phase on synthetic tool-calling data, an expert iteration phase to improve formalization capabilities, and a Direct Preference Optimization phase to reduce ineffective revisions. The paper evaluates ATF on three widely-used ATP datasets and shows that it outperforms existing state-of-the-art formalizers in terms of both syntactic validity and semantic consistency. The paper also analyzes the inference-time scaling properties of ATF and contributes a dataset of 750K formal statements to facilitate future research.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The integration of tool feedback into the formalization process is a novel and promising approach that addresses the key challenges of autoformalization. The use of Lean 4 compilers for syntax corrections and a multi-LLMs-as-judge approach for consistency validation are both effective and innovative solutions that enhance the quality and reliability of the generated formal statements.
- The training process of ATF is well-designed and comprehensive, involving three phases that progressively improve the model's ability to use tools and refine its formalization skills. The use of synthetic data, expert iteration, and preference optimization allows the model to learn from both positive and negative examples and to reduce ineffective revisions.
- The experimental results are impressive and demonstrate the superiority of ATF over existing formalizers across different datasets and metrics. The human evaluation further validates the effectiveness of the consistency check tool and the overall performance of ATF. The analysis of inference-time scaling reveals the potential of ATF to benefit from more resources and to generate a diverse set of valid formalizations.

### Weaknesses

#### Some Related Works


#### comment

 - The paper relies on specific tools and models for syntax and consistency checks, which may limit the generalizability and reproducibility of the approach. For instance, the syntax check tool is based on Lean 4 compilers, which are specific to the Lean formal language. This may make it difficult to apply ATF to other formal languages that use different compilers or have different syntax rules. Similarly, the consistency check tool uses a multi-LLMs-as-judge approach, which depends on the availability and performance of specific LLMs. The paper does not explore the sensitivity of the approach to different LLM choices or the potential impact of LLM biases on the consistency checks. It is unclear how the performance of ATF would vary with different LLMs or if the approach is robust to variations in LLM quality.
- The paper does not provide a detailed analysis of the computational cost and efficiency of the tool feedback mechanism. The integration of external tools into the formalization process may introduce additional overhead and latency, especially for large-scale datasets or complex formal statements. The paper lacks a quantitative evaluation of the time and resources required for each tool call, as well as the overall impact on the inference time of ATF. It is important to understand the trade-offs between the improved performance of ATF and the increased computational cost of using external tools. A detailed analysis of the computational complexity of the tool feedback mechanism is needed to assess its scalability and practicality.
- The paper does not fully explore the limitations and potential failure modes of ATF. While the paper acknowledges that ATF may exhibit consecutive identical errors or struggle with increasingly challenging revisions, it does not provide a systematic analysis of the types of errors that ATF is prone to make. For example, it is unclear whether ATF struggles more with certain types of mathematical concepts or logical structures. A more detailed error analysis, including specific examples of failure cases, would be valuable to understand the weaknesses of ATF and to guide future research directions. The paper should also discuss the potential for error propagation due to the iterative nature of the approach.

### Suggestions

To enhance the generalizability of the Autoformalizer with Tool Feedback (ATF) approach, future work should investigate the use of more modular and adaptable tool interfaces. Instead of relying directly on Lean 4 compilers, the authors could explore the development of a generic syntax checking interface that can be implemented for different formal languages. This interface could define a set of common operations for syntax validation, allowing researchers to plug in different compilers or syntax checkers as needed. Similarly, the multi-LLMs-as-judge approach for consistency checking could be made more robust by exploring techniques for ensembling different LLMs or by incorporating methods for uncertainty estimation. This would help to mitigate the impact of individual LLM biases and improve the reliability of the consistency checks. Furthermore, the authors should investigate the sensitivity of ATF to different LLM choices and provide guidelines for selecting appropriate LLMs for different tasks. A thorough analysis of the performance of ATF with different LLMs would be valuable to understand the robustness of the approach and to identify potential limitations.

To address the lack of analysis regarding the computational cost of the tool feedback mechanism, the authors should conduct a detailed profiling of the inference process. This should include a breakdown of the time spent on each tool call, as well as the time spent on other parts of the formalization process. The authors should also investigate the scalability of the approach by evaluating its performance on larger datasets and more complex formal statements. This analysis should consider the impact of different hardware configurations and optimization techniques on the inference time. Furthermore, the authors should explore methods for reducing the computational overhead of the tool feedback mechanism, such as caching tool results or using more efficient tool implementations. A detailed analysis of the computational complexity of the tool feedback mechanism is needed to assess its scalability and practicality. The authors should also provide a clear comparison of the computational cost of ATF with other formalization approaches.

Finally, to better understand the limitations and potential failure modes of ATF, the authors should conduct a more in-depth error analysis. This should include a categorization of the types of errors that ATF is prone to make, as well as specific examples of failure cases. The authors should investigate whether ATF struggles more with certain types of mathematical concepts, logical structures, or formal language features. This analysis should also consider the impact of the iterative revision process on error propagation. The authors should also explore techniques for mitigating the identified failure modes, such as incorporating additional training data or refining the tool feedback mechanism. A detailed analysis of the limitations of ATF would be valuable to guide future research directions and to improve the overall robustness of the approach.

### Questions

- How does the performance of ATF vary with different versions of Lean or different formal languages? Is there a significant difference in the effectiveness of the syntax check tool across different Lean versions or formal languages?
- How does the choice of LLMs affect the performance of the consistency check tool? Is there a significant difference in the effectiveness of the consistency check tool across different LLMs?
- How does the computational cost of ATF compare to other formalization approaches? What is the average inference time for a single formal statement? How does the inference time scale with the length of the formal statement or the number of tool calls?
- What are the most common types of errors that ATF still makes after tool feedback? Are there any specific types of formal statements or mathematical concepts that ATF struggles with? How does the iterative revision process affect the error propagation?

### Rating

6

### Confidence

4

**********