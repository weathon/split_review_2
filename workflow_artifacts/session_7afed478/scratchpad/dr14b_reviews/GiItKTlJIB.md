### Summary

This paper investigates the extent to which large language models (LLMs) rely on chain-of-thought (CoT) reasoning when solving physics problems. The authors introduce a systematic deletion framework to evaluate the models' dependence on their reasoning traces by selectively removing tokens from the CoT during generation. They apply this framework to three open-source models—Magistral, Phi-4, and Qwen-A3B—across multiple physics benchmarks. The results show that models can maintain accuracy even with significant deletions (40-60%) by "cramming" reconstructed steps into the final answer. Overlap analyses reveal that deleted equations and facts often reappear in the final answers, but inconsistently, suggesting a shallow reliance on CoT. The study highlights the need for evaluation methods that go beyond accuracy to assess the faithfulness of reasoning in scientific domains.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel deletion-based probing methodology to evaluate the faithfulness of CoT reasoning in LLMs, which is particularly relevant for structured problem-solving domains like physics.

2. The study provides empirical evidence of "cramming" behavior in LLMs, where models compensate for deleted CoT tokens by reconstructing reasoning steps in the final answer. This insight is valuable for understanding the limitations of current LLMs in scientific reasoning.

3. The paper is well-organized, with clear explanations of the methodology, experiments, and results. The use of multiple benchmarks and models strengthens the robustness of the findings.

### Weaknesses

#### Some Related Works


#### comment

1. The study focuses exclusively on physics problem-solving, which may limit the generalizability of the findings to other scientific domains or general reasoning tasks. The specific structure and language of physics problems, such as the use of equations and specific terminology, might lead to different behaviors in models compared to domains like biology or chemistry, which rely more on descriptive reasoning and qualitative analysis. Furthermore, the observed 'cramming' behavior might be amplified or diminished in other domains, making it difficult to draw broad conclusions about the faithfulness of CoT reasoning across diverse tasks.

2. The paper does not explore the internal mechanisms that enable models to "cram" missing information, which could provide deeper insights into model behavior. It is unclear whether this behavior arises from the model's ability to memorize common problem-solving patterns, or if it reflects a more sophisticated form of reasoning. Analyzing the model's attention patterns or hidden states during the 'cramming' process could reveal whether the model is genuinely reconstructing the reasoning steps or simply retrieving memorized solutions. Without this analysis, the conclusions about the faithfulness of CoT remain somewhat superficial.

3. The analysis relies heavily on overlap metrics, which may not fully capture the nuances of reasoning faithfulness. While overlap metrics can indicate the presence of similar tokens or phrases, they do not assess the semantic correctness or logical coherence of the reconstructed reasoning. For example, a model might generate an equation that is syntactically similar to the original but semantically incorrect, which would not be captured by simple overlap metrics. A more nuanced evaluation would require metrics that assess the logical validity and scientific correctness of the reconstructed reasoning steps.

### Suggestions

To address the limitations of the study, future work should expand the scope of evaluation to include a broader range of scientific domains and reasoning tasks. This would involve selecting benchmarks from fields such as biology, chemistry, and mathematics, and adapting the deletion framework to accommodate the specific characteristics of these domains. For example, in biology, the reasoning might involve more descriptive and qualitative analysis, while in mathematics, it might involve more symbolic manipulation. By comparing the model's behavior across these diverse domains, it would be possible to gain a more comprehensive understanding of the generalizability of the observed 'cramming' behavior and the faithfulness of CoT reasoning. Furthermore, it would be beneficial to investigate the impact of different problem formats and question types on the model's reliance on CoT, as this could reveal potential biases or limitations of the approach.

To gain deeper insights into the internal mechanisms behind the 'cramming' behavior, future research should focus on analyzing the model's internal states during the reasoning process. This could involve techniques such as attention analysis, which would reveal which parts of the input and intermediate reasoning steps the model is focusing on when generating the final answer. Additionally, probing the hidden states of the model could provide clues about the information that is being stored and retrieved during the 'cramming' process. For example, it would be interesting to investigate whether the model is accessing memorized problem-solving patterns or generating novel reasoning steps. This analysis could be further enhanced by comparing the internal states of the model when it is generating faithful reasoning traces versus when it is 'cramming' information. Such an analysis would provide a more nuanced understanding of the model's reasoning process and the limitations of CoT.

Finally, to overcome the limitations of overlap metrics, future work should explore more sophisticated evaluation methods that can assess the semantic correctness and logical coherence of the reconstructed reasoning. This could involve the use of domain-specific knowledge graphs to verify the scientific validity of the generated equations and facts. Additionally, it would be beneficial to develop metrics that can assess the logical flow of the reasoning steps, ensuring that the reconstructed reasoning is not only syntactically similar to the original but also logically sound. For example, one could use a formal logic framework to represent the reasoning steps and then evaluate the logical validity of the reconstructed reasoning. This would provide a more comprehensive and accurate assessment of the faithfulness of CoT reasoning and help to identify the specific areas where current models are lacking.

### Questions

1. How do the authors ensure that the deletion process does not inadvertently remove critical tokens that are essential for maintaining the logical flow of reasoning, rather than just redundant information?

2. Could the authors provide more details on the overlap metrics used in the study? How do these metrics account for the semantic similarity of tokens, rather than just lexical overlap?

### Rating

6

### Confidence

3

**********