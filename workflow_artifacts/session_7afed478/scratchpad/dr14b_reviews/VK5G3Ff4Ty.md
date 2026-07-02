### Summary

The paper investigates the effectiveness of small language models (SLMs) and small vision-language models (SVLMs) in clinical text summarization and radiology report generation tasks. It compares these models against their larger, domain-adapted counterparts, exploring whether SLMs and SVLMs can achieve comparable performance with reduced computational resources. The study employs a "Collapse Analysis" framework to evaluate quality trade-offs in smaller models across dimensions like task adherence, hallucination rate, and prompt robustness. The findings suggest that while SLMs can approach or sometimes exceed the performance of larger models with fine-tuning, SVLMs still lag in generating detailed radiology reports, highlighting the need for larger models in visual reasoning tasks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper addresses an important and practical research question by exploring whether small language models (SLMs) and small vision-language models (SVLMs) can achieve comparable performance to their larger counterparts in clinical text summarization and report generation tasks. This is particularly relevant given the high computational costs and privacy concerns associated with deploying large language models (LLMs) on-premise in clinical settings.
2. The experimental setup is comprehensive, evaluating models across various adaptation methods (zero-shot, few-shot, fine-tuning) and using multiple metrics to assess different aspects of generation quality. The inclusion of a "Collapse Analysis" to identify performance degradation points in smaller models adds value to the study.
3. The study includes a diverse set of models, including both general-purpose and domain-adapted models, providing a broad perspective on the capabilities of smaller models in clinical NLP tasks.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a clear and explicit statement of its main contributions in the introduction. While the research question is interesting, the absence of a dedicated contributions section makes it difficult to immediately grasp the novelty and significance of the work.
2. The experimental evaluation is limited to a small number of datasets (MeQSum and MIMIC-CXR), which may not fully represent the diversity of clinical text summarization and report generation tasks.
3. The paper does not provide sufficient detail on the experimental setup, including hyperparameter settings, training procedures, and the specific prompts used for each task. This lack of detail makes it difficult to reproduce the results and assess the robustness of the findings.
4. The evaluation of generation quality relies heavily on automatic metrics, which may not fully capture the nuances of clinical language and the factual accuracy required in medical reports.

### Suggestions

To address the lack of clarity regarding the paper's contributions, the introduction should be revised to include a dedicated paragraph that explicitly states the key contributions of the work. This paragraph should highlight the novelty and significance of the findings, such as the identification of a minimum viable model size for clinical tasks, the development of the "Collapse Analysis" framework, and the empirical findings regarding the performance of SLMs and SVLMs. This will help readers quickly understand the main takeaways of the paper and appreciate its contributions to the field. Furthermore, the introduction should clearly articulate the research gap that the paper aims to fill, emphasizing the importance of exploring the capabilities of smaller models in clinical settings due to the computational and privacy concerns associated with large language models.

To improve the generalizability of the findings, the study should expand the evaluation to include a more diverse set of clinical datasets. In addition to MeQSum and MIMIC-CXR, the authors should consider incorporating datasets that contain discharge summaries, progress notes, and other types of clinical documents. This would provide a more comprehensive assessment of the models' ability to handle different types of clinical text and would strengthen the paper's conclusions regarding the applicability of SLMs and SVLMs in real-world clinical settings. The inclusion of diverse datasets would also help to identify potential limitations of the models and would provide a more nuanced understanding of their performance across different clinical tasks. The authors should also consider using datasets that represent different medical specialties to further assess the generalizability of their findings.

To enhance the reproducibility and robustness of the findings, the paper should include a detailed description of the experimental setup in the appendix. This description should include specific information about the hyperparameter settings, training procedures, and the exact prompts used for each task. For example, the authors should specify the learning rates, batch sizes, optimization algorithms, and the number of training epochs used for fine-tuning. Additionally, the exact prompts used for zero-shot, few-shot, and fine-tuning scenarios should be provided. This level of detail is crucial for other researchers to replicate the experiments and validate the results. Furthermore, the authors should consider providing the code and trained models to facilitate reproducibility and further research in this area. Finally, the authors should incorporate human evaluations by clinical experts to assess the clinical relevance and accuracy of the generated summaries and reports. This would provide a more reliable assessment of the models' performance in real-world clinical settings.

### Questions

1. Could you provide a clear list of the paper's main contributions in the introduction? This would help readers quickly understand the key takeaways and the novelty of your work.
2. Have you considered evaluating your models on additional clinical datasets to demonstrate the generalizability of your findings? Including more diverse datasets could strengthen your conclusions about the effectiveness of SLMs and SVLMs.
3. Could you provide more details about your experimental setup, including hyperparameter settings, training procedures, and the specific prompts used? This would improve the reproducibility of your results.
4. Have you considered incorporating human evaluations by clinical experts to assess the clinical relevance and accuracy of the generated summaries and reports? This could provide a more reliable assessment of your models' performance in real-world settings.

### Rating

6

### Confidence

4

**********