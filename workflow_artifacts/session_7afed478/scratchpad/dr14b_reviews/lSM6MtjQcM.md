### Summary

The paper introduces AetherCode, a new benchmark for evaluating the coding abilities of Large Language Models (LLMs) in competitive programming. The authors argue that current benchmarks overstate LLM proficiency due to insufficient difficulty and evaluation bias from low-quality test cases. AetherCode addresses these issues by drawing problems from premier programming competitions (IOI and ICPC) and incorporating expert-validated test suites. The benchmark includes problems categorized by difficulty (Easy, Medium, Hard, Extreme) and algorithmic domains. The authors evaluate several reasoning and non-reasoning models on AetherCode, finding a significant performance gap and highlighting the importance of logical deduction in solving complex algorithmic problems.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper identifies and addresses key limitations in existing code reasoning benchmarks, such as insufficient difficulty and evaluation bias from low-quality test cases.
2. AetherCode is the first benchmark to systematically collect problems from premier programming competitions like IOI and ICPC, ensuring high difficulty and relevance.
3. The hybrid approach to test case construction (combining automated generation with expert annotation) and the achievement of 100% TPR and TNR demonstrate a rigorous evaluation methodology.
4. The paper provides a comprehensive evaluation of multiple models, highlighting the performance gap between reasoning and non-reasoning models and offering insights into model capabilities across different problem categories.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide detailed analysis of the performance of current SOTA models on AethCode, such as o1-mini. This makes it difficult to assess the benchmark's difficulty and the models' capabilities in a practical setting.
2. The paper lacks a detailed analysis of the performance of current SOTA models on AethCode across different problem categories. This makes it difficult to assess the benchmark's difficulty and the models' capabilities in a practical setting.
3. The paper does not provide a detailed analysis of the performance of current SOTA models on AethCode across different difficulty levels. This makes it difficult to assess the benchmark's difficulty and the models' capabilities in a practical setting.
4. The paper lacks a detailed analysis of the performance of current SOTA models on AethCode across different algorithmic domains. This makes it difficult to assess the benchmark's difficulty and the models' capabilities in a practical setting.

### Suggestions

The authors should include a more comprehensive evaluation of state-of-the-art models, such as o1-mini, across various problem categories and difficulty levels. This would involve not only reporting overall performance metrics but also providing detailed breakdowns of results for each category (e.g., dynamic programming, graph algorithms, etc.) and difficulty level (Easy, Medium, Hard, Extreme). Such an analysis would allow researchers to better understand the specific strengths and weaknesses of different models and identify areas where further improvements are needed. For example, if a model performs well on easy problems but struggles with hard ones, this would indicate a limitation in its ability to handle complex reasoning. Similarly, if a model excels in dynamic programming but fails in graph algorithms, this would highlight a specific area for improvement. This level of detail is crucial for the benchmark to be truly informative and useful for the research community.

Furthermore, the paper should include a more in-depth analysis of the types of errors that models make on the AetherCode benchmark. This could involve categorizing errors into different types, such as syntax errors, logical errors, or errors related to specific algorithmic techniques. By analyzing the error patterns, the authors could gain insights into the underlying limitations of current models and identify areas where future research should focus. For instance, if a model frequently makes errors related to handling edge cases, this would suggest a need for better training data or more robust reasoning mechanisms. Similarly, if a model struggles with problems requiring specific algorithmic techniques, this would indicate a need for more targeted training or the development of new models that are better equipped to handle these challenges. This error analysis would significantly enhance the diagnostic value of the benchmark.

Finally, the authors should consider providing more detailed information about the problems themselves, including the specific constraints and requirements of each problem. This would allow researchers to better understand the challenges posed by the benchmark and develop more targeted solutions. For example, if a problem requires a specific data structure or algorithm, this should be clearly stated in the problem description. This level of detail would also help researchers to better understand the types of problems that are most challenging for current models and identify areas where further improvements are needed. Additionally, the authors could consider providing a set of reference solutions for the problems, which would allow researchers to compare their own solutions with the provided ones and identify areas where they can improve.

### Questions

1. Can you provide more details on the process of converting problem statements from PDF to Markdown+LaTeX? How do you ensure the accuracy and consistency of the converted statements?
2. How do you handle problems that require special judges (custom checkers)? Are there any specific examples of such problems in AetherCode?
3. What are the specific criteria used by experts to construct targeted test cases for incorrect solutions? How do you ensure the diversity and comprehensiveness of these test cases?
4. How do you plan to maintain and update the AetherCode benchmark over time? Will new problems be added regularly, and how will you ensure the quality and difficulty of these new problems?
5. Can you provide more details on the evaluation of test case quality using TPR and TNR? How do you collect and categorize correct and incorrect solutions for this evaluation?

### Rating

6

### Confidence

3

**********