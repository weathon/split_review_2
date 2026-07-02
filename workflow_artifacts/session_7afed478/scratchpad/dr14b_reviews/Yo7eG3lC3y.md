### Summary

The paper introduces LEGO-EVAL, a new evaluation framework for assessing 3D scene synthesis guided by detailed instructions. Current evaluation methods often fail to accurately assess the alignment between instructions and generated scenes due to a lack of deep 3D understanding. LEGO-EVAL addresses this by using a set of tools to explicitly ground scene components, enabling more accurate and interpretable evaluations. The framework is designed to handle complex constraints, including object attributes and spatial relationships. Additionally, the paper presents LEGO-BENCH, a benchmark dataset with fine-grained instructions for evaluating scene generation methods. Results show that LEGO-EVAL significantly outperforms existing methods in assessing scene-instruction alignment, highlighting the limitations of current scene generation approaches.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper identifies a critical gap in current scene synthesis evaluation methods, addressing the inability to handle fine-grained, realistic instructions.
- The LEGO-EVAL framework is innovative, using tool-augmented VLMs to achieve a deeper understanding of 3D scenes and more accurately assess alignment with detailed instructions.
- The LEGO-BENCH benchmark provides a standardized way to evaluate scene generation methods, facilitating fair comparisons and progress tracking.
- The paper provides thorough experimental validation, demonstrating LEGO-EVAL's superiority over existing methods and benchmarking current scene generation approaches.
- The paper is well-written and easy to follow, with clear explanations and effective visualizations.

### Weaknesses

#### Some Related Works


#### comment

 - The paper could provide more discussion on the limitations of the proposed evaluation method and potential failure cases.
- The paper could benefit from a more detailed analysis of the proposed evaluation method and its relationship to existing methods, including a discussion of the specific advantages and disadvantages of each.
- The paper could provide more qualitative examples to illustrate the effectiveness of the proposed evaluation method and its ability to capture fine-grained details in 3D scenes.

### Suggestions

The paper would benefit from a more thorough discussion of the limitations of LEGO-EVAL, particularly regarding its reliance on explicit constraints. While the current benchmark focuses on instructions with clear, definable constraints, real-world instructions often involve implicit constraints or require more abstract reasoning. For example, instructions like "the chair should be comfortable" or "the room should feel cozy" are difficult to evaluate with the current framework. The paper should explore how LEGO-EVAL might be extended to handle such cases, perhaps by incorporating methods for inferring implicit constraints or by allowing for more flexible evaluation criteria. Furthermore, the paper should discuss the potential for error propagation due to the multi-step nature of the evaluation process, where errors in early steps could cascade to subsequent steps. A detailed analysis of these failure cases would provide a more complete understanding of the framework's capabilities and limitations.

To strengthen the paper, a more detailed comparison of LEGO-EVAL with existing evaluation methods is needed. The paper should delve into the specific mechanisms of methods like CLIPScore and VLM-as-a-judge, highlighting their strengths and weaknesses in the context of 3D scene evaluation. For instance, while CLIPScore is mentioned as being limited to 2D scenes, the paper could elaborate on why this is the case and how LEGO-EVAL overcomes this limitation. A more granular analysis of the types of errors that each method makes would be beneficial. For example, does CLIPScore struggle with spatial relationships, or is it more sensitive to object attribute mismatches? Similarly, the paper should discuss the specific challenges that VLM-as-a-judge faces in localizing and reasoning about 3D objects, and how LEGO-EVAL's tool-augmented approach addresses these challenges. This detailed comparison would provide a clearer understanding of the unique contributions of LEGO-EVAL.

Finally, the paper should include more qualitative examples to illustrate the effectiveness of LEGO-EVAL. While the quantitative results demonstrate the framework's superiority, qualitative examples would provide a more intuitive understanding of its capabilities. The paper could include visualizations of scenes where LEGO-EVAL correctly identifies failures that other methods miss, highlighting the fine-grained details that LEGO-EVAL can capture. For example, a visualization could show a scene where the spatial relationship between objects is subtle, and how LEGO-EVAL is able to correctly assess this relationship while other methods fail. Additionally, the paper could include examples of scenes where LEGO-EVAL makes mistakes, providing insights into the limitations of the framework. These qualitative examples would make the paper more compelling and provide a more nuanced understanding of LEGO-EVAL's strengths and weaknesses.

### Questions

- How does the proposed evaluation method handle instructions with implicit constraints or those that require more abstract reasoning?
- What are the potential failure cases for the proposed evaluation method, and how might these be addressed?
- How does the proposed evaluation method compare to existing methods in terms of computational efficiency and scalability?

### Rating

6

### Confidence

3

**********