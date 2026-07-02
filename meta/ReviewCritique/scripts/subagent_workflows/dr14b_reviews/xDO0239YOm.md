### Summary

The paper introduces a method for selecting the optimal resolution in single-cell and Perturb-seq clustering. The authors propose a framework called **HYPOTHENEA**GENT, which leverages a large language model (LLM) to transform cluster annotation into a quantitatively optimizable task. The LLM analyzes each gene program and generates hypotheses with confidence scores. The method then calculates intra-cluster agreement and inter-cluster separation to derive a resolution score, which is maximized when clusters are coherent and distinct. The approach is validated on a K562 CRISPRi Perturb-seq dataset and demonstrates improved performance over traditional metrics.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

1. The paper introduces a novel approach to cluster annotation and resolution selection using a large language model, which is a creative application of AI in genomics.
2. The method is validated on a public dataset, and the results show that it can select clustering granularities that align better with known biological pathways compared to traditional metrics.

### Weaknesses

#### Some Related Works


#### comment

1. The method relies heavily on the performance of the LLM, which may introduce biases or inaccuracies if the model is not well-calibrated or if the input data is noisy. The paper does not sufficiently address the potential for the LLM to generate spurious or inconsistent annotations, especially given the complexity of gene expression data and the inherent stochasticity in single-cell measurements. The reliance on a single LLM also raises concerns about the generalizability of the approach across different models and datasets.
2. The evaluation is performed on a single dataset, which may not be representative of other datasets or experimental conditions. The K562 CRISPRi Perturb-seq dataset, while a valuable resource, represents a specific cell type and experimental setup. The lack of validation on diverse datasets, including those with different cell types, perturbation methods, and levels of noise, limits the ability to assess the robustness and general applicability of the proposed method. The paper needs to demonstrate that the method can perform well across a range of experimental conditions.
3. The paper does not provide a clear comparison with other state-of-the-art methods for cluster annotation and resolution selection. While the authors mention traditional metrics, they do not compare their method against other recent approaches that also leverage machine learning or network analysis for similar tasks. A more comprehensive comparison is needed to establish the advantages and limitations of the proposed method relative to existing techniques.

### Suggestions

To address the dependence on the LLM, the authors should explore methods to mitigate potential biases and inaccuracies. This could involve techniques such as ensemble learning, where multiple LLMs are used to generate annotations and the results are aggregated to improve robustness. Another approach would be to incorporate uncertainty quantification into the LLM's predictions, allowing the method to down-weight annotations with low confidence. Furthermore, the authors should investigate the sensitivity of their method to different LLMs and prompt designs, providing a more thorough analysis of the impact of these choices on the final results. It would also be beneficial to explore methods for data augmentation or noise reduction to improve the quality of the input data for the LLM.

To improve the generalizability of the method, the authors should evaluate their approach on a more diverse set of datasets. This should include datasets from different cell types, perturbation methods (e.g., CRISPRi, CRISPRa, shRNA), and experimental platforms. The evaluation should also consider datasets with varying levels of noise and complexity. Furthermore, the authors should investigate the impact of different preprocessing steps on the performance of their method, providing guidelines for optimal data preparation. The inclusion of a more diverse set of datasets would provide a more comprehensive assessment of the method's robustness and applicability.

Finally, the authors should provide a more thorough comparison with other state-of-the-art methods for cluster annotation and resolution selection. This should include a comparison with methods that leverage machine learning, network analysis, or other approaches for similar tasks. The comparison should be performed on the same datasets and using the same evaluation metrics, allowing for a fair assessment of the relative performance of each method. The authors should also discuss the advantages and limitations of their method compared to existing techniques, providing a clear understanding of the contributions of their work. This comparison should not only focus on quantitative metrics but also on the biological interpretability of the results.

### Questions

1. How does the method perform on other datasets or experimental conditions?
2. How does the method compare with other state-of-the-art methods for cluster annotation and resolution selection?
3. What are the computational requirements of the method, and how does it scale with the size of the dataset?

### Rating

3

### Confidence

3

**********