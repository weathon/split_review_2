### Summary

This paper proposes the Fast and Slow Effect (FSE), a unified evaluation framework designed to assess annotation sufficiency without human supervision.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

- The paper is well-written

### Weaknesses

#### Some Related Works


#### comment

 - The Figure 2 is so confusing, the reviewer cannot understand this figure according to the caption and the text.
- The evaluation seems to be problematic, the LLMs/VLMs may fail to generate the sufficient concepts for the test images, and with the CRI index, the evaluation is also questionable.
- The contribution of the paper may not match the bar of ICLR.

### Suggestions

The paper's core contribution, the Fast and Slow Effect (FSE) framework, needs significant clarification and more robust justification. The current presentation of Figure 2 is indeed problematic, as it is unclear how the different components of the framework interact and what the precise flow of information is. Specifically, the diagram should clearly delineate the inputs, outputs, and transformations at each stage of both the 'fast' and 'slow' modes. The caption and surrounding text should provide a step-by-step explanation of the process, including the specific algorithms or models used at each stage. Without a clear understanding of the framework's mechanics, it is difficult to assess the validity of the evaluation results. Furthermore, the paper should provide a more detailed explanation of the Concept Representation Index (CRI) and its sensitivity to variations in concept quality. The authors should also consider including a sensitivity analysis to demonstrate the robustness of the CRI metric.

The evaluation methodology requires substantial improvement. The concern that LLMs/VLMs may not generate sufficient concepts is valid, and the paper needs to address this directly. The authors should provide a detailed analysis of the generated concepts, including their diversity, relevance, and completeness. It is not enough to simply state that the models generate concepts; the quality of these concepts must be rigorously evaluated. For example, the paper could include a comparison of the generated concepts with human-annotated concepts to assess the level of agreement. Additionally, the paper should explore the impact of different prompting strategies on the quality of the generated concepts. The current evaluation seems to rely heavily on the CRI index, which may not be a comprehensive measure of annotation sufficiency. The authors should consider incorporating other evaluation metrics, such as precision, recall, and F1-score, to provide a more complete picture of the performance of the FSE framework. The paper should also discuss the limitations of the CRI index and how these limitations might affect the interpretation of the results.

Finally, the paper needs to more clearly articulate its contribution and significance within the context of the ICLR bar. The current presentation of the FSE framework and its evaluation seems incremental rather than groundbreaking. The authors should emphasize the novelty of their approach and its potential impact on the field. The paper should also discuss how the FSE framework addresses the limitations of existing evaluation methods and how it can be used to advance the development of more robust and reliable LLMs/VLMs. The paper should also consider including a discussion of the potential applications of the FSE framework in other domains. The authors should also provide a more detailed comparison of their work with existing literature, highlighting the unique aspects of their approach and its advantages over existing methods. Without a clear articulation of its contribution and significance, the paper risks being perceived as incremental and not meeting the high standards of ICLR.

### Questions

Please see the weaknesses.

### Rating

3

### Confidence

4

**********