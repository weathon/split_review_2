### Summary

This paper introduces a new benchmark, GeoGramBench, to evaluate the ability of LLMs to translate programmatic drawing code into geometric reasoning. The benchmark consists of 500 problems organized into three levels of geometric complexity: Primitive Recognition, Local Relation Composition, and Global Abstract Integration. The authors evaluate 19 state-of-the-art LLMs on this benchmark and find that even the most advanced models achieve less than 50% accuracy on the highest complexity level. The paper also analyzes the performance of LLMs on different subtypes of problems and identifies common failure patterns.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper addresses an important and under-explored aspect of LLMs' capabilities, i.e., their ability to reason about geometric information expressed in code.
- The benchmark is carefully designed and curated, with a clear taxonomy of problem types and difficulty levels. The authors also take care to prevent answer leakage and ensure the quality of the benchmark.
- The evaluation is comprehensive, covering a wide range of LLMs and providing detailed analysis of their performance on different subtypes of problems.
- The paper is well-written and easy to follow, with clear explanations of the methodology and results.

### Weaknesses

#### Some Related Works


#### comment

 - The paper focuses primarily on the evaluation of LLMs and does not propose any new methods or techniques to improve their performance on the program-to-geometry task. 
- The analysis of the results is mostly descriptive and does not provide much insight into the underlying reasons for the observed performance patterns. For example, it would be interesting to investigate why certain models perform better than others on specific subtypes of problems, or why the performance of all models degrades significantly on the highest complexity level. 
- The paper could benefit from a more detailed discussion of the limitations of the benchmark and potential directions for future research. For example, the benchmark only covers a limited range of geometric concepts and relationships, and it does not include any problems that require dynamic or interactive reasoning. It would also be interesting to explore the use of visual inputs in addition to code, as this is a more natural way for humans to reason about geometry.

### Suggestions

The paper's primary weakness lies in its focus on evaluation without offering concrete solutions to the identified problems. While the benchmark is valuable, the lack of exploration into methods for improving LLM performance on program-to-geometry tasks limits the paper's impact. Future work should investigate techniques such as incorporating external geometric reasoning libraries or developing specialized architectures that can better handle symbolic-to-spatial transformations. For example, one could explore integrating a symbolic math solver to preprocess the code and extract relevant geometric parameters before feeding it to the LLM. This could potentially mitigate the observed performance degradation on higher complexity levels by reducing the burden on the LLM to parse and interpret the code directly. Furthermore, the paper could benefit from a more in-depth analysis of the error patterns. Instead of just reporting aggregate statistics, a detailed examination of the types of mistakes made by different models could reveal specific weaknesses in their reasoning capabilities. For instance, are models struggling with specific geometric transformations, or are they failing to correctly interpret the spatial relationships between objects? Such analysis could inform the development of targeted training strategies or architectural modifications. 

Another area for improvement is the limited scope of the benchmark. While the current benchmark covers a range of geometric concepts, it does not include problems that require dynamic or interactive reasoning. Expanding the benchmark to include such problems would provide a more comprehensive evaluation of LLMs' geometric reasoning abilities. For example, problems involving animations or simulations of geometric objects could be included. This would require models to reason about changes in spatial relationships over time, which is a crucial aspect of real-world geometric reasoning. Moreover, the paper should explore the potential benefits of incorporating visual inputs alongside code. Humans naturally rely on visual information when reasoning about geometry, and it is possible that providing visual cues could improve the performance of LLMs. This could involve generating images from the code and feeding them to the model alongside the code itself. This multimodal approach could potentially lead to more robust and accurate geometric reasoning.

Finally, the paper should delve deeper into the reasons behind the observed performance differences between models. While the paper notes that larger models tend to perform better, it does not provide a detailed explanation of why this is the case. A more thorough analysis of the architectural differences between models and their impact on geometric reasoning could provide valuable insights. For example, do models with specific types of attention mechanisms or memory modules perform better on certain types of problems? Understanding these correlations could guide the development of more effective models for geometric reasoning. Furthermore, the paper should explore the effect of different prompting strategies on model performance. Are there specific prompts that can elicit better reasoning from the models? A systematic investigation of different prompting techniques could reveal ways to improve the performance of LLMs on the program-to-geometry task without requiring changes to the model architecture.

### Questions

- Have you considered incorporating visual inputs in addition to code, as this is a more natural way for humans to reason about geometry?
- Have you explored the use of external tools or libraries for geometric reasoning, such as computer algebra systems or geometric software packages?
- Have you investigated the effect of different prompting strategies on model performance? For example, have you tried using chain-of-thought prompting or few-shot learning?

### Rating

6

### Confidence

4

**********