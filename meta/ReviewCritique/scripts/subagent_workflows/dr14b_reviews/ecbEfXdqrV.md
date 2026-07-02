### Summary

This paper explores the counterintuitive phenomenon of likelihood in anomaly detection with deep generative models, specifically focusing on tabular data. The authors demonstrate that, unlike in the image domain, where deep generative models often assign higher likelihoods to anomalous data, this behavior is rare in tabular settings. They introduce a domain-agnostic definition of the counterintuitive phenomenon and conduct extensive experiments on 57 datasets, showing that likelihood-based anomaly detection with normalizing flows is effective and reliable for tabular data. The paper also provides theoretical and empirical analyses, linking the rarity of the counterintuitive phenomenon in tabular data to lower dimensionality and weaker feature correlations compared to image data.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

The paper provides a domain-agnostic definition of the counterintuitive phenomenon, which is a valuable contribution as it allows for a consistent understanding and evaluation of the phenomenon across different data types and domains. This definition can be applied beyond the specific context of tabular and image data, making it a more general tool for anomaly detection research.

The paper conducts extensive experiments on a wide range of datasets, which enhances the robustness and generalisability of the findings. The use of 57 datasets from ADBench, a benchmark suite, allows for a comprehensive evaluation of the phenomenon across different types of data and models.

The paper provides a detailed analysis of the experimental results, including visualisations and statistical analysis. This helps to understand the phenomenon and its implications better. The authors also discuss the limitations of their study and suggest directions for future research, which shows a critical and reflective approach to their work.

The paper is well-written and organised, making it easy to follow and understand. The authors provide clear explanations of the concepts, methods, and results, which makes the paper accessible to a wider audience.

### Weaknesses

#### Some Related Works


#### comment

The paper's focus on tabular and image data may limit the generalisability of the findings to other types of data, such as time series or graph data. Further research is needed to investigate whether the phenomenon also occurs in these domains.

The paper does not provide a detailed analysis of the computational complexity of the proposed method. This could be a limitation for practical applications, especially when dealing with large datasets.

The paper does not compare the proposed method with other state-of-the-art anomaly detection methods. This makes it difficult to assess the relative performance of the method and its potential advantages and disadvantages.

### Suggestions

The paper would benefit from a more thorough investigation into the generalizability of the findings across different data modalities. While the focus on tabular and image data is a good starting point, it is crucial to explore whether the observed counterintuitive likelihood phenomenon extends to other data types such as time series, graph data, or even text. Each of these data types has unique characteristics that could influence the behavior of generative models and the resulting likelihoods. For example, time series data often exhibits temporal dependencies, while graph data has complex relational structures. Analyzing how these structures affect likelihood-based anomaly detection would provide a more complete understanding of the phenomenon. Furthermore, the authors should consider exploring the impact of different data characteristics, such as dimensionality, sparsity, and the presence of outliers, on the observed phenomenon. This would help to identify the conditions under which likelihood-based methods are most effective and when they might fail.

To enhance the practical relevance of the work, a detailed analysis of the computational complexity of the proposed method is essential. The paper should provide a clear understanding of how the computational cost scales with the size of the dataset, the number of features, and the complexity of the generative model. This analysis should include both theoretical considerations and empirical measurements. Furthermore, the authors should compare the computational efficiency of their method with other state-of-the-art anomaly detection techniques. This would allow practitioners to make informed decisions about which method is most appropriate for their specific needs. The paper should also discuss potential strategies for improving the computational efficiency of the method, such as using more efficient generative models or implementing parallel processing techniques. This would make the method more accessible to researchers and practitioners working with large datasets.

Finally, the paper needs a more comprehensive evaluation of the proposed method in comparison to other state-of-the-art anomaly detection techniques. The authors should compare their method with a range of both traditional and deep learning-based methods, using a consistent set of evaluation metrics. This comparison should include a discussion of the strengths and weaknesses of each method, as well as the conditions under which each method performs best. The paper should also explore the impact of different hyperparameter settings on the performance of the method. This should include a sensitivity analysis to determine which hyperparameters are most critical for achieving good performance. Additionally, the authors should investigate the effect of different data preprocessing techniques on the performance of the method. This should include a discussion of the advantages and disadvantages of different preprocessing techniques, such as normalization, standardization, and feature selection. This would provide a more complete understanding of the practical considerations for using likelihood-based anomaly detection with tabular data.

### Questions

Could you provide more details on the computational complexity of the proposed method and how it scales with the size of the dataset and the number of features?

How does the proposed method perform on other types of data, such as time series or graph data? Are there any plans to extend the experiments to these domains?

What are the limitations of the proposed method, and how do you plan to address them in future work?

### Rating

6

### Confidence

4

**********