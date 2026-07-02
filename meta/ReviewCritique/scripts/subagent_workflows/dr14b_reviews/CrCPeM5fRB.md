### Summary

This paper introduces the Signal Dice Similarity Coefficient (SDSC), a structure-aware metric for time-series self-supervised representation learning. SDSC focuses on local waveform consistency, capturing sign and magnitude overlap rather than global alignment. It outperforms traditional mean squared error (MSE) by addressing amplitude sensitivity and polarity issues, enhancing semantic alignment. SDSC quantifies structural agreement through signed amplitude intersections, extending the Dice Similarity Coefficient to continuous signals. It can also function as a loss with a differentiable Heaviside approximation. A hybrid loss combining SDSC with MSE improves stability and preserves amplitude when needed. Experiments show SDSC-based pre-training performs comparably or better than MSE in forecasting and classification, especially in low-resource scenarios, suggesting that structural fidelity enhances semantic quality.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

1. The paper is well-written and easy to follow.
2. The SDSC loss function is well-motivated and supported by theoretical analysis.

### Weaknesses

#### Some Related Works


#### comment

1. The experimental results are not very promising. The improvements are marginal, and in some cases, the performance of SDSC-based models is even worse than that of MSE-based models.
2. The paper lacks a clear explanation of why SDSC is better suited for certain datasets or tasks. It would be helpful to provide more insights into the characteristics of datasets where SDSC excels.
3. The paper does not explore the impact of different hyperparameter settings for SDSC. It would be beneficial to investigate how these settings affect performance and provide guidelines for choosing appropriate values.
4. The paper does not provide a detailed analysis of the computational cost of SDSC compared to MSE. This information is crucial for practical applications.
5. The paper does not discuss the limitations of SDSC. It would be beneficial to acknowledge potential drawbacks and areas for future improvement.

### Suggestions

The paper would benefit from a more thorough investigation into the specific conditions under which SDSC outperforms MSE. While the authors mention that SDSC is more sensitive to structural changes, they do not provide a clear framework for identifying datasets where this characteristic is advantageous. For example, a detailed analysis of the frequency content or the presence of specific waveform patterns in datasets where SDSC excels could provide valuable insights. Furthermore, the paper should explore the relationship between the magnitude of the signals and the performance of SDSC. It is possible that SDSC is more effective when the signals have a wide dynamic range, while MSE might be more suitable for signals with small variations. A more in-depth analysis of these factors would help practitioners determine when to use SDSC over MSE. The authors could also consider providing a metric or a set of criteria to quantify the 'structuralness' of a dataset, which could guide the selection of the appropriate loss function.

Further, the paper should include a more comprehensive hyperparameter study for SDSC. The current analysis is limited, and it is unclear how sensitive the performance of SDSC is to different parameter settings. Specifically, the paper should explore the impact of the sharpness parameter α on the stability and convergence of the training process. It would be beneficial to provide guidelines for choosing appropriate values for α based on the characteristics of the dataset. For example, the authors could investigate whether a larger α is more suitable for datasets with high-frequency components, while a smaller α is better for datasets with low-frequency components. Additionally, the paper should explore the impact of the weighting coefficients λsdsc and λmse in the hybrid loss function. A detailed analysis of how these parameters affect the trade-off between structural fidelity and amplitude accuracy would be valuable. The authors could also consider using a grid search or other optimization techniques to find the optimal hyperparameter settings for different datasets.

Finally, the paper needs a more detailed discussion of the computational cost of SDSC compared to MSE. While the authors mention that SDSC is computationally linear, they do not provide a quantitative analysis of the actual runtime or memory usage. This information is crucial for practical applications, especially when dealing with large datasets. The paper should include a comparison of the training time and memory consumption of SDSC and MSE on different datasets. Furthermore, the authors should discuss the potential for optimizing the implementation of SDSC to reduce its computational cost. For example, they could explore the use of efficient numerical integration techniques or parallel processing. The paper should also acknowledge the limitations of SDSC, such as its sensitivity to noise and its inability to capture global temporal dependencies. A more balanced discussion of the strengths and weaknesses of SDSC would help practitioners make informed decisions about when to use it.

### Questions

1. In the classification task, the SDSC-based model performs worse than the MSE-based model in the cross-domain scenario. What could be the reason for this?
2. What is the impact of the sharpness parameter α on the performance of SDSC? How does it affect the stability of training?
3. How does SDSC perform when applied to other time-series models, such as TimesNet or PatchTST?

### Rating

3

### Confidence

3

**********