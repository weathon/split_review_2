### Summary

This paper studies the faithfulness of LLM-generated answers to the retrieved context in the standard RAG setting. The authors find that there is an inverse correlation between the amount of copy in the generated answer and the faithfulness of the answer, i.e., answers with more copy are more faithful to the retrieved context. Motivated by this observation, the authors propose a two-stage framework to increase the copying amount in the answers. In the first stage, the authors propose three prompting methods (CP-Link, CP-Order, and CP-Refine) to increase the copying amount in the generated answers. In the second stage, the authors use the outputs from stage 1 to train CopyPasteLLM via preference learning, where the preference data is constructed using an automated pipeline. The authors demonstrate that their proposed CopyPasteLLM model performs better on FaithEval and ConFiQA, and they provide interpretability results demonstrating that CopyPasteLLM relies more on contextual knowledge compared to the base model.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper studies an important problem in the RAG literature. As the authors highlight, there has been a lot of recent work on citations and faithfulness, but ensuring consistency between the generated content and its cited sources remains a challenge. This paper makes progress towards addressing this problem.
- The authors demonstrate that their proposed CopyPasteLLM model outperforms SOTA models on FaithEval and ConFiQA.
- The authors propose three prompting methods to increase the copying amount in the generated answers. These methods are simple but effective and can be used to augment data for model training.
- The authors provide detailed ablation studies and interpretability results, which add depth to the paper.

### Weaknesses

#### Some Related Works


#### comment

 - The authors focus on the setting where there is a single document in the retrieved context. It would be good to have some discussion about how this approach would work when there are multiple retrieved documents with potentially conflicting information.
- The proposed CopyPasteLLM model trains a LLM to have a high copying degree. It would be good to have some discussion on the limitations of this approach, e.g., what are some cases where high copying is not desirable?
- The authors use an automated pipeline to construct the preference data for training CopyPasteLLM. It would be good to have some human annotations to validate the quality of this data.

### Suggestions

The paper's focus on a single retrieved document limits its applicability in real-world scenarios where multiple documents are often retrieved, potentially containing conflicting information. The authors should discuss how their approach would handle such cases. For example, how would the model decide which document to copy from when faced with contradictory information across multiple sources? Would it attempt to synthesize information from multiple documents, and if so, how would it ensure faithfulness to each source? A discussion of these challenges and potential solutions would significantly enhance the paper's practical relevance. Furthermore, the authors should consider exploring techniques for identifying and resolving conflicts between documents, such as using attention mechanisms to weigh the importance of different sources or incorporating a conflict detection module into their framework. This would make the proposed method more robust and applicable to complex retrieval scenarios.

While the paper demonstrates the effectiveness of CopyPasteLLM in improving faithfulness through increased copying, it is crucial to acknowledge the limitations of this approach. High copying is not always desirable, especially when the retrieved context contains irrelevant or redundant information. The authors should discuss scenarios where abstractive summarization or creative generation would be more appropriate than verbatim copying. For instance, in tasks requiring reasoning or synthesis of information from multiple sources, a model that simply copies may not perform well. The authors should also consider the potential for copying to propagate errors or biases present in the source material. A discussion of these limitations would provide a more balanced view of the proposed method and its applicability. Moreover, the authors could explore hybrid approaches that combine copying with abstractive summarization to mitigate these limitations, allowing the model to copy when appropriate and generate abstractive responses when necessary.

The use of an automated pipeline for constructing preference data raises concerns about the quality of the training data. While automated methods can be efficient, they may not always accurately reflect human judgments of quality and faithfulness. The authors should validate the quality of the preference data using human annotations. This would involve having human annotators evaluate the generated responses and assess whether the preference data accurately reflects the relative quality of different responses. Such an evaluation would provide more confidence in the robustness of the proposed approach. Furthermore, the authors should consider the potential for bias in the automated pipeline and discuss how they have addressed this issue. For example, if the pipeline favors responses with higher copying degrees, it may lead to a model that prioritizes copying over other important factors such as relevance and coherence. A thorough analysis of the preference data and its potential biases would strengthen the paper's findings.

### Questions

Please see the weaknesses above. Additionally,

- How do you ensure that CP-Refine does not hurt fluency? Table 2 shows that CP-Refine has the worst perplexity.
- In Figure 3, what do you mean by "logits power"? Also, can you provide more details about the findings from the interpretability analysis?
- In Figure 4, how do you get the hidden states distributions?

### Rating

6

### Confidence

4

**********