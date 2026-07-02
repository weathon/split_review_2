### Summary

This paper introduces the Open Proof Corpus (OPC), a large-scale dataset of LLM-generated proofs for mathematical problems from various competitions. The authors use the OPC to investigate several open questions in LLM proof generation, such as the gap between natural language and formal proof generation, the relation between final answer accuracy and proof correctness, and the effectiveness of best-of-n selection strategies. The paper also presents a fine-tuned 8B parameter model on the OPC that achieves 88.1% judgment accuracy, close to the best model, GPT-5.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper makes a valuable contribution to the field of automated theorem proving by introducing a large-scale, human-validated dataset of LLM-generated proofs. The OPC is the first of its kind and can serve as a benchmark for future research in this area.
- The paper addresses several open questions in LLM proof generation and provides new insights into the strengths and limitations of LLMs in mathematical reasoning. The findings are well-supported by empirical evidence and analysis.
- The paper is well-written and easy to follow. The methodology is clearly explained, and the results are presented in a clear and concise manner.

### Weaknesses

#### Some Related Works


#### comment

 - The human evaluation process could be more rigorous. The paper mentions that each proof is labeled as either correct or incorrect by one or two human judges. However, it would be beneficial to have more details on the background and expertise of the judges, the specific grading criteria, and the process for resolving disagreements between judges. The paper should also report the inter-annotator agreement to quantify the reliability of the human judgments. The current description lacks sufficient detail to assess the quality of the human evaluation, which is a critical component of the dataset's value.
- The paper does not explore the potential of using the OPC for training and fine-tuning LLMs for proof generation. This would be a natural next step and could provide valuable insights into the effectiveness of the OPC for improving LLM performance. The paper focuses on evaluating models, but the dataset's potential for model training remains largely unexplored, which is a missed opportunity.
- The paper does not discuss the potential biases in the dataset, such as the selection of problems, the distribution of difficulty levels, and the representation of different mathematical domains. The dataset's composition and potential biases need to be thoroughly examined to understand its limitations and generalizability. Without this analysis, the dataset's applicability to diverse mathematical problems is unclear.

### Suggestions

The paper should provide a more detailed account of the human evaluation process. This should include specific information about the educational background and experience of the judges, such as the number of judges with PhDs in mathematics or related fields, and their experience with mathematical competitions or proof writing. The paper should also provide the exact criteria used to determine proof correctness, including how judges should handle incomplete proofs or those with minor errors. It would be beneficial to include examples of proofs that were deemed correct and incorrect, along with the corresponding justifications. Furthermore, the paper should report the inter-annotator agreement using a metric such as Cohen's kappa, which would provide a quantitative measure of the reliability of the human judgments. The process for resolving disagreements between judges should also be described in detail, including whether a third judge was involved or if the judges discussed their disagreements to reach a consensus. These details are crucial for assessing the quality and reliability of the human evaluation, which is a cornerstone of the dataset's value.

To fully leverage the potential of the Open Proof Corpus (OPC), the paper should explore the use of the dataset for training and fine-tuning LLMs for proof generation. This could involve training a model from scratch or fine-tuning an existing model on the OPC and evaluating its performance on a held-out set of problems. The paper should investigate different training strategies, such as varying the learning rate, batch size, and number of epochs, and report the results of these experiments. It would also be beneficial to analyze the types of errors made by the fine-tuned model to understand the limitations of the dataset and the model's ability to generalize to unseen problems. This analysis should include a comparison of the model's performance before and after fine-tuning, as well as a comparison to other state-of-the-art models. This would provide valuable insights into the effectiveness of the OPC for improving LLM performance in mathematical proof generation.

Finally, the paper should include a thorough analysis of the potential biases in the dataset. This should include an examination of the selection of problems, the distribution of difficulty levels, and the representation of different mathematical domains. For example, the paper should analyze the number of problems from each competition, the average difficulty level of problems from each competition, and the distribution of difficulty levels within each competition. It should also analyze the representation of different mathematical domains, such as algebra, geometry, and number theory. The paper should discuss the potential impact of these biases on the generalizability of the dataset and the models trained on it. This analysis should also include a discussion of the limitations of the dataset and potential strategies for mitigating these biases in future work. This would provide a more complete understanding of the dataset's strengths and limitations.

### Questions

- How did you ensure the quality of the human judgments? What were the background and expertise of the judges? What were the specific grading criteria? How did you resolve disagreements between judges? What is the inter-annotator agreement?
- How does the performance of LLMs on the OPC relate to their performance on other mathematical reasoning benchmarks, such as MATH or GSM8k? Does the OPC capture different aspects of mathematical reasoning that are not captured by existing benchmarks?
- What are the limitations of the OPC? How generalizable are the findings to other datasets and domains? What are the potential biases in the dataset, and how might they affect the results?
- What are the most common types of errors made by LLMs on the OPC? Are there any patterns or trends in the errors? How do the errors relate to the difficulty level of the problems?
- What are the ethical implications of using LLMs for mathematical proof generation? Could LLMs be used to automate the process of mathematical discovery? What are the potential benefits and risks of such automation?

### Rating

6

### Confidence

4

**********