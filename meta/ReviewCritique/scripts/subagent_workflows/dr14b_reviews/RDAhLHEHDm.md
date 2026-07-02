### Summary

This paper studies how to use scientific large language models (Sci-LLMs) for biological discovery. It first identifies a tokenization dilemma for biomolecular sequences: the sequence-as-language approach breaks down important biological structures, while the sequence-as-modality approach introduces alignment challenges. To address this, the paper proposes a context-driven approach that provides Sci-LLMs with structured context from bioinformatics tools instead of raw sequences. Experiments show that this context-only approach outperforms other input modes, suggesting that Sci-LLMs are better at reasoning over structured knowledge than interpreting raw sequences.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is clearly written and easy to follow.
2. The proposed context-driven approach is novel and useful in practice. It provides a new perspective on how to utilize large language models in scientific discovery.
3. The experimental results are convincing. They demonstrate the effectiveness of the proposed context-driven approach.

### Weaknesses

#### Some Related Works


#### comment

1. The context-driven approach relies on existing bioinformatics tools, which may limit its ability to discover novel biomolecular patterns. This dependence could restrict the exploration of truly novel biological insights, as the context is constrained by the capabilities and biases of these pre-existing tools. For instance, if a new type of RNA structure is present but not recognized by the tools, the context will not include this information, thus limiting the model's ability to identify it.
2. The context-driven approach may require additional computational resources and time to generate the context for each sequence. While the authors demonstrate the effectiveness of their approach, they do not fully explore the computational overhead associated with generating the context using bioinformatics tools. This could be a significant bottleneck for large-scale analyses, especially when dealing with complex biological systems that require multiple rounds of context generation. The paper should include a more detailed analysis of the computational cost and scalability of the proposed method.

### Suggestions

The paper introduces a compelling context-driven approach for utilizing Sci-LLMs in biological discovery, but there are several avenues for further exploration and improvement. First, while the reliance on existing bioinformatics tools provides a solid foundation, it is crucial to investigate methods for mitigating the limitations imposed by these tools. One potential direction is to explore techniques for integrating novel pattern discovery directly into the context generation process. This could involve training smaller, specialized models to identify patterns not captured by existing tools and incorporating their outputs into the context. For example, a model could be trained to identify novel motifs or structural features in sequences, and these features could be included in the context provided to the Sci-LLM. This would allow the approach to move beyond the constraints of existing tools and potentially uncover new biological insights. Furthermore, the authors should investigate methods to reduce the computational cost of context generation. This could involve optimizing the use of bioinformatics tools, exploring parallel processing techniques, or developing more efficient algorithms for context extraction. A detailed analysis of the computational bottlenecks and potential optimization strategies would be valuable for the practical application of the proposed method. 

Second, the paper should delve deeper into the types of biological questions that are best suited for the context-driven approach. While the experiments demonstrate the effectiveness of the approach for certain tasks, it is important to understand its limitations and identify the types of questions where it may not be as effective. For example, the approach might be less suitable for questions that require a deep understanding of the underlying biophysical mechanisms or for questions that involve complex interactions between multiple biomolecules. A more detailed analysis of the strengths and weaknesses of the approach for different types of biological questions would be beneficial. This could involve categorizing biological questions based on their complexity and the type of information required, and then evaluating the performance of the context-driven approach for each category. This would provide a more nuanced understanding of the applicability of the method and help researchers choose the most appropriate approach for their specific research questions. 

Finally, the paper should explore the potential of combining the context-driven approach with other methods for biological discovery. For example, the context-driven approach could be used to generate initial hypotheses, which could then be further investigated using other techniques such as molecular dynamics simulations or wet-lab experiments. This would allow researchers to leverage the strengths of different approaches and potentially accelerate the pace of biological discovery. The authors should also consider the potential of using the context-driven approach to guide the development of new bioinformatics tools. For example, the insights gained from the context-driven approach could be used to identify areas where existing tools are lacking and to develop new tools that are better suited for the task. This would create a positive feedback loop, where the context-driven approach and bioinformatics tools mutually enhance each other.

### Questions

1. Given that the context-driven approach relies on existing bioinformatics tools, how does it perform when encountering novel biomolecular sequences that lack established context?
2. For what kinds of biological questions should we consider using the context-driven approach? When it may not be a good idea to use this approach?

### Rating

6

### Confidence

3

**********