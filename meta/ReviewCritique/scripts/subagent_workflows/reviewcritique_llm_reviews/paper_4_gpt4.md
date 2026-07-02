Summary of the Paper

This paper evaluates the effectiveness of pre-trained deep neural networks (DNNs) in approximating human similarity judgments across images, audio, and video modalities, revealing a substantial gap between DNN and human performances.

To bridge this gap, the authors introduce language-based methods for similarity approximation, leveraging an adaptive tag collection pipeline (STEP-Tag) for efficient data gathering.

They further enhance approximation accuracy by combining language embeddings with DNN embeddings ("stacked" methods), demonstrating superior performance across all tested modalities.

The study provides a comprehensive guide for researchers on approximating human similarity judgments efficiently, supported by a large dataset of 206,339 human judgments and a detailed analysis of various modeling approaches.

Strengths and Weaknesses

Strengths:

Comprehensive Evaluation: The evaluation of 611 pre-trained models across three distinct modalities presents a thorough and broad analysis, showcasing the extensive work undertaken.

Innovative Language-based Methods: The introduction of language-based methods for similarity approximation, alongside the novel STEP-Tag pipeline, represents a significant contribution to the field, particularly in terms of efficiency and scalability.

High-Quality Dataset: The large dataset of human judgments collected and released provides a valuable resource for future research, enhancing reproducibility and further study.

Practical Guide for Researchers: The concise guide based on experimental results is a practical tool for researchers facing limitations in judgment collection or model access, facilitating more effective research design.

Weaknesses:

Model-Specific Analysis Limitations: The paper's focus on pre-trained models might limit its applicability to domains where such models are not available or suitable.

Additionally, the performance gap noted between human judgments and DNNs might be model-specific rather than a general limitation of DNNs.

Potential Bias in Language Data: The reliance on language-based methods might introduce biases related to language use and representation, which the paper does not fully address in terms of potential impacts on similarity judgments.

Ethical Considerations: While the paper briefly mentions the risk of embedding human biases in ML datasets, a deeper analysis of ethical implications, especially concerning the use of language data and the broader societal impacts of these biases, would strengthen the paper.

Clarity, Quality, Novelty, and Reproducibility

Clarity and Quality: The paper is well-structured and clear, with a strong emphasis on methodological rigor and comprehensive data analysis.

The quality of the research is evident in the extensive dataset and detailed experimental setup.

Novelty: The novel use of language-based methods and the STEP-Tag pipeline for approximating human similarity judgments is a significant and innovative contribution to the field.

Reproducibility: With the release of the dataset and detailed descriptions of the methodologies and models used, the study sets a high standard for reproducibility.

Summary of the Review

The paper presents a comprehensive and innovative approach to approximating human similarity judgments using pre-trained DNNs and novel language-based methods.

The strengths lie in the extensive model evaluation, the innovative methodology for data collection, and the practical guide for researchers.

However, the study could be improved by addressing potential biases introduced through language data and by expanding the discussion on the ethical implications of their findings.

Overall, the contributions are significant, providing valuable insights and resources for the NLP and broader AI research community.