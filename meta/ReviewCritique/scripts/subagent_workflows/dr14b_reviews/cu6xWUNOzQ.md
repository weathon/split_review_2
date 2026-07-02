### Summary

This paper presents a nonlinear, multimodal prediction model that combines audio and linguistic features from pre-trained models to predict brain responses to speech. The authors demonstrate that their approach outperforms traditional unimodal linear models and prior state-of-the-art models, achieving significant improvements in prediction performance. The study highlights the importance of nonlinear and multimodal approaches in speech encoding and reveals distributed multimodal processing patterns across the cortex that align with key neurolinguistic theories.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

The paper introduces a novel nonlinear, multimodal prediction model that combines audio and linguistic features from pre-trained models, which is a significant advancement over traditional unimodal linear models.

The approach achieves substantial improvements in prediction performance, with a 17.2% and 17.9% improvement in unnormalized and normalized correlation, respectively, over traditional unimodal linear models, and a 7.7% and 14.4% improvement over prior state-of-the-art models.

The paper is well-written, with clear explanations of the methods and results, and the figures and tables are well-designed and informative.

The findings have important implications for future in-silico testing and improved decoding performance, and they reveal distributed multimodal processing patterns across the cortex that align with key neurolinguistic theories.

### Weaknesses

#### Some Related Works


#### comment

The paper could benefit from a more detailed discussion of the limitations of the proposed approach and potential avenues for future research. For example, the authors could discuss the generalizability of their findings to other datasets or populations, or the potential impact of different pre-trained models on the results.

The authors should also consider discussing the computational cost of their approach compared to traditional linear models, as this could be a factor in its practical applicability.

The authors could also discuss the potential for using their approach to investigate other cognitive processes beyond speech comprehension, such as language production or music perception.

The paper could also benefit from a more detailed analysis of the specific brain regions that are most strongly predicted by the model, and how these regions relate to known neural circuits involved in speech processing.

### Suggestions

The authors should delve deeper into the limitations of their model, specifically addressing the potential for overfitting given the complexity of the nonlinear model and the relatively small dataset. While the paper mentions the use of PCA for dimensionality reduction, a more thorough discussion of the impact of PCA on the interpretability of the model's results is needed. For instance, how does the choice of the number of principal components affect the model's performance and its ability to capture meaningful neural signals? Furthermore, the authors should explore the sensitivity of their model to different hyperparameter settings, such as the learning rate and the number of layers in the neural network, and provide a rationale for their chosen values. A more rigorous analysis of the model's robustness would strengthen the paper's conclusions.

In addition to the generalizability of the findings, the authors should also consider the potential impact of individual variability in brain structure and function on the model's performance. It would be beneficial to investigate whether the model's predictions are consistent across different subjects or whether subject-specific models are necessary to achieve optimal performance. The authors could also explore the use of techniques such as cross-validation to assess the model's ability to generalize to unseen data. Furthermore, a discussion of the potential biases introduced by the pre-trained models used in the study is warranted. For example, how might the specific training data of the pre-trained models influence the model's ability to predict brain responses to speech? Addressing these limitations would provide a more comprehensive understanding of the model's strengths and weaknesses.

Finally, the authors should provide a more detailed analysis of the computational cost of their approach compared to traditional linear models. While the paper mentions that the proposed approach is more computationally expensive, a more quantitative analysis of the computational time and memory requirements would be beneficial. This would allow readers to better assess the practical applicability of the proposed approach. The authors should also discuss potential strategies for reducing the computational cost of their model, such as using more efficient optimization algorithms or reducing the dimensionality of the input features. Furthermore, the authors should explore the potential for using their approach to investigate other cognitive processes beyond speech comprehension, such as language production or music perception, and discuss the challenges and opportunities associated with these extensions.

### Questions

See weaknesses.

### Rating

8

### Confidence

3

**********