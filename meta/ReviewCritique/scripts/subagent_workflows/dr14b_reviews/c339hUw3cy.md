### Summary

This paper introduces a kernel generation dataset, ConCuR, and a trained kernel generation model, KernelCoder. ConCuR is created using a two-stage pipeline that first generates PyTorch-to-CUDA kernel pairs and then filters these pairs based on performance and reasoning trace criteria. KernelCoder, trained on ConCuR, achieves sota results on KernelBench, outperforming other models in execution accuracy and speed.

### Soundness

2

### Presentation

3

### Contribution

2

### Strengths

- The paper is well-organized, with clear visualizations that help understand the dataset creation process and the model’s performance.
- The ConCuR dataset provides a valuable resource for the kernel generation community, offering high-quality CUDA kernels with reasoning traces that could support future model training and evaluation.

### Weaknesses

#### Some Related Works


#### comment

 - The paper could benefit from a more detailed explanation of the reasoning trace selection process, particularly regarding how “concise” and “informative” reasoning traces are defined and identified. The lack of clarity around these definitions makes it difficult to assess the robustness of the data curation pipeline. For example, it is unclear what specific metrics or heuristics are used to determine if a reasoning trace is concise, or how the information content of a trace is quantified.
- The paper’s claim that concise reasoning traces lead to better kernel performance is counterintuitive and could be better substantiated. The reasoning provided does not fully explain why shorter traces, which might omit crucial details, would result in higher-quality kernels. This claim needs more rigorous justification, especially given that it contradicts the common assumption that more detailed reasoning leads to better outcomes. The paper should explore potential confounding factors that might contribute to this observation.
- The data curation process appears to have potential risk of data leakage. Specifically, the paper does not clearly delineate the exact versions of KernelBench used for data generation and evaluation. If the same tasks or very similar tasks are used in both stages, the reported performance metrics, such as Exec and fast_1, could be inflated, leading to an overestimation of the model's generalization capabilities. This lack of clarity undermines the validity of the experimental results.
- The paper’s efficiency comparison in Table 3 could be misleading, as it compares models trained with different methodologies (e.g., SFT vs. GRPO). A more controlled comparison within the same parameter range would provide a fairer assessment of KernelCoder’s efficiency. The current comparison does not isolate the impact of the proposed dataset and training approach from the effects of different training methodologies.

### Suggestions

To address the lack of clarity regarding reasoning trace selection, the authors should provide a more detailed explanation of how 'concise' and 'informative' are defined and operationalized. This should include specific metrics or heuristics used to identify such traces. For example, if 'concise' is based on token length, the exact token count range should be specified. If 'informative' is determined by the presence of specific keywords or logical steps, these should be explicitly listed and justified. Furthermore, the authors should provide examples of both high-quality and low-quality reasoning traces, along with a detailed explanation of why each is categorized as such. This would help readers better understand the selection criteria and assess the robustness of the data curation pipeline. The authors should also consider including an analysis of the correlation between reasoning trace characteristics (e.g., length, keyword presence) and kernel performance to provide empirical support for their selection process.

To strengthen the claim that concise reasoning traces lead to better kernel performance, the authors should conduct a more in-depth analysis of the relationship between reasoning length and kernel quality. This should include an exploration of potential confounding factors, such as the possibility that shorter traces might be associated with simpler tasks. The authors should also investigate whether the observed correlation holds across different types of kernel generation tasks and different model architectures. A more rigorous analysis, possibly involving statistical methods, is needed to establish a causal link between reasoning conciseness and kernel performance. The authors should also consider alternative explanations for the observed correlation, such as the possibility that shorter traces are simply a byproduct of a more efficient reasoning process, rather than a direct cause of better kernel performance. A controlled experiment where reasoning traces are artificially shortened or lengthened could provide further insights into this relationship.

To address the potential data leakage issue, the authors must clearly delineate the exact versions of KernelBench used for data generation and evaluation. They should also provide a detailed description of the task selection process, including the criteria used to select tasks for data generation. If any tasks used for evaluation are similar to those used for data generation, the authors should conduct an additional evaluation on a completely separate set of tasks to demonstrate the model's generalization capabilities. This would help to ensure that the reported performance metrics are not inflated due to data leakage. Furthermore, the authors should provide a more detailed analysis of the overlap between the tasks used for data generation and evaluation, including a quantitative assessment of the similarity between these tasks. This would help to clarify the extent to which the model is learning generalizable patterns rather than memorizing specific solutions.

### Questions

- Could the authors clarify how the reasoning traces were selected? Specifically, what criteria were used to define “concise” and “informative” reasoning traces, and how were these criteria applied in the curation process?
- Did the authors investigate whether the correlation between reasoning length and correctness varies across different model architectures or reasoning domains? Understanding this could help clarify whether the observed correlation is robust across contexts.
- In Section 3.5, how does the model determine the “correct” reasoning length for each task? Is this based on empirical testing, or are there predefined heuristics that guide reasoning length selection?
- To prevent potential data leakage, could the authors clarify whether any tasks in ConCuR overlap with KernelBench? Additionally, an evaluation on a separate benchmark or dataset would help demonstrate generalization.
- In Table 3, the efficiency comparison might be more accurate if models using different training methods (e.g., SFT vs. GRPO) were compared within the same parameter range. This would isolate the impact of the dataset and training approach more effectively.

### Rating

5

### Confidence

4

**********