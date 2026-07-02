### Summary

This paper introduces HASTE, a framework for compressing code context to fit LLMs' limited context window size. HASTE integrates AST-based structural information with semantic relevance to provide LLMs with coherent and pertinent code snippets, addressing the trade-off between relevance and structural integrity in context retrieval. HASTE achieves up to 85% code compression while improving the success rate of automated code edits, representing an advancement in AI-assisted software development.

### Soundness

2

### Presentation

1

### Contribution

2

### Strengths

- HASTE effectively combines structure-aware and relevance-focused approaches, addressing a key challenge in using LLMs for software engineering tasks. By leveraging ASTs, HASTE preserves syntactic integrity while ensuring semantic relevance, which is well-motivated given the limitations of previous methods.
- The authors have conducted a thorough evaluation, including comparisons with baseline methods and using an LLM-as-judge framework. The results demonstrate HASTE's effectiveness in achieving high compression rates while maintaining or improving the quality of code edits.

### Weaknesses

#### Some Related Works


#### comment

 - The paper suffers from poor writing and lacks clarity in describing its methodology and technical details. For instance, the overview figure (Fig. 1) is difficult to interpret, and many components are not adequately explained. The flow of information and the purpose of each module should be clarified to improve readability.
- The technical details of each module are insufficiently described. Key components, such as the "Partial Builder" and "Identifier Evaluation," are mentioned but not explained in detail. The paper would benefit from a more thorough explanation of these modules, including how they function and contribute to the overall pipeline.
- The "Hybrid Reranker" is not explained at all. Given its importance in combining lexical and semantic relevance, a detailed description of its implementation and algorithms is necessary.
- The "Payload Builder" is described as assembling enriched structural and lexical data, but the specific process and data structures used are unclear. The paper should provide more details on how this module operates and how it integrates with the rest of the pipeline.
- The paper lacks a thorough discussion of the limitations of the proposed approach. For example, it is unclear how HASTE handles cross-file dependencies or more complex code structures. Additionally, the generalizability of the approach to other programming languages beyond the ones tested is not addressed.
- The observability part seems unnecessary and out of place. Its function and importance are not well-justified in the main paper. If it is crucial, it should be explained more clearly; otherwise, it could be moved to the appendix.

### Suggestions

The paper needs a significant overhaul in its presentation and technical detailing to be considered for publication. The core idea of combining structural and semantic information for code context compression is promising, but the current manuscript fails to convey the technical depth and novelty adequately. The overview figure (Fig. 1) should be redrawn to clearly illustrate the flow of information and the purpose of each module. Each component, especially the "Partial Builder," "Identifier Evaluation," "Hybrid Reranker," and "Payload Builder," should have a dedicated section or subsection explaining its functionality, algorithms, and data structures. For instance, the "Partial Builder" needs a clear explanation of how it processes code snippets, what kind of partial code units it creates, and how these units are represented. Similarly, the "Identifier Evaluation" should detail the metrics used to evaluate identifiers and how these metrics contribute to the selection of relevant code contexts. The "Hybrid Reranker" requires a thorough explanation of how it combines lexical and semantic signals, including the specific algorithms and weighting schemes used. Without these details, the paper remains opaque and difficult to evaluate.

Furthermore, the paper should address the limitations of the proposed approach more explicitly. The current discussion is insufficient, and the paper should delve into how HASTE handles complex code structures, such as nested functions, classes, and conditional statements. The treatment of cross-file dependencies is also a critical area that needs further exploration. While the paper mentions that HASTE can handle cross-file contexts, it does not provide sufficient details on how it achieves this. The paper should explain the mechanisms used to identify and retrieve relevant code snippets from different files, and how it ensures the structural integrity of the retrieved context. Additionally, the generalizability of HASTE to other programming languages should be investigated and discussed. The paper should provide evidence or arguments to support the claim that HASTE can be effectively applied to languages with different syntax and semantics. The evaluation should also be expanded to include more diverse and challenging code editing tasks to better demonstrate the effectiveness of HASTE.

Finally, the observability component needs to be either justified more clearly or moved to the appendix. If it is intended to be a core part of the paper, its function and importance should be explained in detail. The paper should clarify how the metrics collected by the observability layer are used to improve the performance of HASTE or to debug issues. If the observability component is not essential to the core contribution of the paper, it should be moved to the appendix to avoid distracting from the main narrative. The writing quality needs to be improved throughout the paper, with a focus on clarity, conciseness, and technical accuracy. The paper should be revised to ensure that all technical terms are clearly defined, and that the arguments are presented in a logical and coherent manner.

### Questions

- Can you provide more details on the "Partial Builder" and "Identifier Evaluation" modules? What specific techniques are used in these steps, and how do they contribute to the overall performance of HASTE?
- How does the "Hybrid Reranker" combine lexical and semantic relevance scores? Are there any specific algorithms or weighting schemes used?
- In the "Payload Builder" section, you mention enriched structural and lexical data. Can you provide more details on what this data includes and how it is used in the retrieval process?
- How does HASTE handle cross-file dependencies and more complex code structures?
- Have you considered the generalizability of HASTE to other programming languages? If so, what modifications would be necessary?
- What is the purpose of the observability component, and why is it included in the main architecture diagram?

### Rating

3

### Confidence

4

**********