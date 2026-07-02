### Summary

This paper introduces CausalNovo, a model-agnostic framework designed to improve de novo peptide sequencing by addressing the challenges posed by noisy spectral data. Traditional deep learning models often capture superficial correlations within noisy mass spectra, leading to spurious associations that hinder generalization. CausalNovo tackles this issue by focusing on causal representations of mass spectra, specifically targeting signal fragment ions. The framework employs causal interventions and information-theoretic objectives based on the principles of independence and sufficiency to disentangle causal factors from noise. Extensive experiments on three public datasets demonstrate that CausalNovo consistently enhances performance across varying noise levels, achieving up to a 10% improvement in amino acid, peptide, and post-translational modification (PTM) level metrics.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper presents a novel approach to de novo peptide sequencing by integrating causal inference principles into the model training process. This is a significant departure from traditional statistical methods that often rely on superficial correlations, making the work innovative and potentially impactful.

2. The authors provide a thorough experimental evaluation of CausalNovo across multiple datasets and baseline models, demonstrating consistent performance improvements. The framework's ability to generalize across different noise levels and datasets is a strong indicator of its robustness and practical utility.

3. The paper is well-structured and clearly explains the motivation, methodology, and experimental results. The use of Structural Causal Models (SCMs) and information-theoretic objectives is well-articulated, making the technical contributions accessible to readers with a background in computational proteomics and machine learning.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a detailed discussion on the computational overhead introduced by the CausalNovo framework. While the authors mention that the CEM module adds negligible inference time, they do not provide a comprehensive analysis of the training time and resource requirements, particularly for large-scale datasets. This omission makes it difficult to assess the practical feasibility of the framework in real-world applications where computational efficiency is crucial. Specifically, the paper should include a breakdown of the time spent on each component of the CEM, such as the mutual information estimation and the perturbation process, to better understand the sources of computational cost.

2. The evaluation primarily focuses on standard benchmark datasets, which may not fully capture the diversity and complexity of real-world mass spectrometry data. The paper would benefit from additional experiments on more challenging datasets, such as those with higher levels of noise or more complex peptide modifications. This would provide a more robust assessment of the framework's generalizability and its ability to handle the variability encountered in practical proteomics research. For example, datasets with a higher proportion of post-translationally modified peptides or those derived from complex biological samples could be used to further validate the method.

3. The paper does not provide a detailed analysis of the sensitivity of the CausalNovo framework to the choice of hyperparameters, such as the perturbation threshold (γ) and the fraction of peaks replaced (α). A more thorough exploration of how these parameters affect the model's performance and stability would be valuable for practitioners looking to implement the framework. It is important to understand the trade-offs between robustness and sensitivity to these parameters, and to provide guidelines for selecting appropriate values for different datasets and experimental conditions.

### Suggestions

To address the lack of detailed computational analysis, the authors should include a comprehensive breakdown of the training time for the CausalNovo framework, comparing it directly to the baseline models. This should include a per-epoch analysis, as well as the total training time, and should be presented in a table format for clarity. Furthermore, the authors should investigate the scalability of the framework by evaluating its performance on larger datasets, and provide an analysis of how the training time scales with the size of the dataset. This would provide a more complete picture of the computational demands of the framework and its suitability for real-world applications. The authors should also consider providing an analysis of the memory footprint of the framework, as this can also be a limiting factor in large-scale experiments.

To enhance the evaluation of the framework, the authors should include experiments on more challenging datasets that better reflect the complexity of real-world mass spectrometry data. This could include datasets with higher levels of noise, more complex peptide modifications, or data from different types of mass spectrometers. The authors should also consider using datasets that are publicly available and well-annotated, to ensure that the results are reproducible and comparable to other methods. Additionally, the authors should provide a more detailed analysis of the performance of the framework on different types of peptides, such as those with post-translational modifications or those with unusual amino acid sequences. This would provide a more nuanced understanding of the strengths and limitations of the framework.

Finally, to address the sensitivity of the framework to hyperparameters, the authors should conduct a more thorough analysis of the impact of the perturbation threshold (γ) and the fraction of peaks replaced (α) on the model's performance. This should include a systematic exploration of different values for these parameters, and an analysis of how the model's performance varies as a function of these parameters. The authors should also provide guidelines for selecting appropriate values for these parameters, based on the characteristics of the dataset and the experimental conditions. This would make the framework more accessible to practitioners and would increase its practical utility. The authors should also consider providing a sensitivity analysis of other hyperparameters, such as the learning rate and the batch size, to ensure that the framework is robust to variations in these parameters.

### Questions

1. Could the authors provide a more detailed analysis of the computational overhead introduced by the CausalNovo framework, particularly in terms of training time and resource requirements? How does the training time of CausalNovo compare to that of the baseline models, and is the framework scalable for large-scale datasets?

2. How sensitive is the CausalNovo framework to the choice of hyperparameters, such as the perturbation threshold (γ) and the fraction of peaks replaced (α)? Could the authors provide guidelines or recommendations for selecting these parameters in different experimental settings?

3. The paper focuses on improving the robustness of de novo sequencing models to noise. However, it would be valuable to understand how the framework performs on datasets with different types of noise or interference. Could the authors discuss the potential limitations of CausalNovo in handling other forms of spectral artifacts, such as those arising from co-eluting peptides or chemical contaminants?

4. The CausalNovo framework is designed to be model-agnostic. Could the authors provide more examples of how it can be integrated with other types of deep learning models for peptide sequencing, and discuss any potential challenges or limitations in doing so?

### Rating

6

### Confidence

3

**********