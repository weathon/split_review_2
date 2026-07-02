### Summary

The paper presents a method for zero-shot image classification using vision-language models (VLMs) like CLIP. The authors introduce Defined Taxonomic Stratification (DefNTaxS), a framework that leverages large language models (LLMs) to cluster related classes into hierarchical subcategories and augment class labels with taxonomic context. This approach aims to disambiguate semantically similar classes and improve classification accuracy without retraining the model or modifying prompts manually. The method is evaluated on seven benchmark datasets, showing improvements over baseline methods.

### Soundness

3

### Presentation

3

### Contribution

2

### Strengths

1. The paper is well-organized, with a clear explanation of the proposed method and its components.
2. The experiments are thorough, covering multiple datasets and comparing against various baselines.

### Weaknesses

#### Some Related Works


#### comment

1. The method's reliance on LLM-generated taxonomic clustering raises concerns about its robustness and potential biases inherited from the LLM. The quality of the clustering is crucial to the method's success, and errors in clustering could lead to significant performance degradation. The paper does not provide a detailed analysis of the LLM's clustering performance, such as precision and recall of the generated taxonomies compared to a gold standard, which makes it difficult to assess the reliability of this crucial step. Furthermore, the paper does not explore the sensitivity of the method to different LLMs or different prompting strategies for the same LLM, which could reveal potential weaknesses in the approach.
2. The paper could benefit from a more in-depth analysis of cases where DefNTaxS does not improve classification accuracy. Understanding these failure modes would provide insights into the method's limitations and potential areas for improvement. Specifically, it is unclear whether the method struggles with fine-grained distinctions, or if the taxonomic context is sometimes detrimental to classification performance. The paper should include a qualitative analysis of misclassified examples, highlighting cases where the taxonomic context either fails to help or actively harms the classification.
3. The paper does not extensively discuss the potential limitations of DefNTaxS in handling datasets with highly specialized or novel classes that may not be well-represented in the LLM's training data. The method's performance could degrade significantly when applied to domains that are not well-covered by the LLM's knowledge base. For example, the method might struggle with datasets containing rare biological species, or highly specialized technical terms, where the LLM's understanding of the underlying taxonomy is limited.

### Suggestions

To address the concerns about the LLM-generated taxonomic clustering, the authors should conduct a more thorough analysis of the clustering quality. This could involve comparing the LLM-generated taxonomies with human-annotated gold standard taxonomies, or using metrics such as precision, recall, and F1-score to quantify the accuracy of the clustering. The authors should also explore the sensitivity of the method to different LLMs and different prompting strategies. This could involve experimenting with different LLMs, such as GPT-4 or other open-source models, and varying the prompts used to elicit the taxonomic information. Furthermore, the authors should investigate the impact of different clustering algorithms on the performance of the method. This could involve comparing the LLM-generated clusters with clusters obtained using traditional clustering algorithms, such as k-means or hierarchical clustering, to determine the relative importance of the LLM's semantic understanding versus traditional clustering techniques. This analysis would provide a more comprehensive understanding of the method's robustness and limitations.

To better understand the failure modes of DefNTaxS, the authors should conduct a detailed qualitative analysis of misclassified examples. This analysis should focus on identifying patterns in the types of errors made by the method. For example, the authors should investigate whether the method struggles with fine-grained distinctions, or if the taxonomic context is sometimes detrimental to classification performance. The authors should also explore whether the method is more likely to fail on classes with ambiguous taxonomic relationships, or on classes that are not well-represented in the LLM's training data. This qualitative analysis should be complemented by a quantitative analysis of the performance of the method on different subsets of the data, such as classes with high intra-class variability or classes with ambiguous taxonomic relationships. This would provide a more nuanced understanding of the method's strengths and weaknesses.

Finally, to address the limitations of DefNTaxS in handling datasets with highly specialized or novel classes, the authors should explore strategies for adapting the method to such domains. This could involve incorporating domain-specific knowledge into the LLM's prompting strategy, or using a combination of LLM-generated taxonomies and human-annotated taxonomies. The authors should also investigate the use of few-shot learning techniques to adapt the method to new domains with limited training data. Furthermore, the authors should evaluate the method on datasets that contain highly specialized or novel classes, to assess its performance in these challenging scenarios. This would provide a more realistic assessment of the method's applicability to real-world problems.

### Questions

1. How does the method perform on datasets with highly specialized or novel classes that may not be well-represented in the LLM's training data?
2. What is the impact of different LLMs on the quality of taxonomic clustering and overall classification accuracy? Have the authors experimented with other LLMs besides GPT-4o-mini?
3. How sensitive is the method to the choice of subcategories and the assignment of classes to these subcategories? What happens if the LLM makes errors in clustering?

### Rating

6

### Confidence

4

**********