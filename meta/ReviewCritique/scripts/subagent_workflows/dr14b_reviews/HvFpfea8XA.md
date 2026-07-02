### Summary

This paper proposes AMADEUS, a framework for developing role-playing agents (RPAs) based on large language models (LLMs) and retrieval-augmented generation (RAG) techniques. The authors introduce a novel approach to enhance persona consistency in RPAs, even when addressing queries beyond the character's explicit knowledge. AMADEUS comprises three main components: Adaptive Context-aware Text Splitter (ACTS), Guided Selection (GS), and Attribute Extractor (AE). To evaluate the proposed framework, the authors created CharacterRAG, a dataset containing persona documents for 15 fictional characters and associated question-answer pairs.

### Soundness

3

### Presentation

3

### Contribution

2

### Strengths

1. The paper presents a comprehensive approach to role-playing by integrating ACTS, GS, and AE, which work together to maintain persona consistency and infer attributes for more realistic responses.
2. The introduction of the CharacterRAG dataset is a significant contribution, as it provides a resource for developing and evaluating RPAs.

### Weaknesses

#### Some Related Works


#### comment

1. The paper's reliance on LLMs for attribute extraction and guided selection may introduce biases or inaccuracies if the LLMs have not been appropriately trained on diverse datasets. The paper does not discuss how the choice of LLM impacts the performance of these components, which is a critical oversight. Specifically, the potential for the LLM to misinterpret or fail to extract nuanced attributes due to a lack of training on relevant character types or domains is not addressed. This could lead to inconsistent or inaccurate persona representations, especially when dealing with complex or less common character archetypes.
2. While the paper proposes a novel framework, it does not extensively compare AMADEUS with other state-of-the-art role-playing or RAG-based systems, which could strengthen the validation of its effectiveness. The lack of a rigorous comparative analysis makes it difficult to ascertain the true advancement offered by AMADEUS. A more thorough evaluation would involve benchmarking against existing methods using standardized metrics and datasets, which is currently absent.
3. The paper could benefit from a more detailed discussion on the scalability of AMADEUS, especially when dealing with a large number of characters or more complex role-playing scenarios. The current analysis does not provide sufficient insight into how the system would perform under increased load or with a more diverse set of characters. The computational cost of the attribute extraction and guided selection processes, particularly in relation to the size of the persona database, needs further investigation.

### Suggestions

To address the potential biases and inaccuracies introduced by the reliance on LLMs, the authors should conduct a more thorough analysis of how different LLMs impact the performance of the Attribute Extractor (AE) and Guided Selection (GS) components. This should include a systematic evaluation of multiple LLMs, including open-source options, and a detailed analysis of the types of errors each model makes. The authors should also explore methods to mitigate these biases, such as fine-tuning the LLMs on a more diverse dataset or incorporating a post-processing step to validate the extracted attributes. Furthermore, the paper should include a discussion on the limitations of using LLMs for attribute extraction, particularly in cases where the character's attributes are subtle or complex. This would provide a more balanced and realistic assessment of the proposed framework's capabilities.

To strengthen the validation of AMADEUS, the authors should conduct a more extensive comparison with existing role-playing and RAG-based systems. This should include a benchmarking analysis using standardized metrics and datasets, where available. The comparison should not only focus on overall performance but also on specific aspects such as persona consistency, response accuracy, and computational efficiency. The authors should also consider comparing AMADEUS with systems that use different approaches to role-playing, such as those based on rule-based systems or those that use different methods for attribute extraction. This would provide a more comprehensive understanding of the strengths and weaknesses of AMADEUS compared to other state-of-the-art methods. The lack of such comparison makes it difficult to assess the true novelty and effectiveness of the proposed framework.

Finally, the authors should provide a more detailed discussion on the scalability of AMADEUS, particularly in relation to the number of characters and the complexity of the role-playing scenarios. This should include an analysis of the computational cost of the different components of the framework, such as the Adaptive Context-aware Text Splitter (ACTS), Guided Selection (GS), and Attribute Extractor (AE). The authors should also explore methods to improve the scalability of the system, such as using more efficient algorithms for attribute extraction or implementing a caching mechanism for frequently accessed persona information. The paper should also include a discussion on the limitations of the current approach in terms of scalability and provide recommendations for future research in this area.

### Questions

1. How does AMADEUS handle situations where a character's attributes are ambiguous or evolve over time?
2. What measures are in place to prevent the model from reinforcing negative stereotypes through role-playing?
3. How well does AMADEUS perform with characters from diverse cultural backgrounds?

### Rating

5

### Confidence

4

**********