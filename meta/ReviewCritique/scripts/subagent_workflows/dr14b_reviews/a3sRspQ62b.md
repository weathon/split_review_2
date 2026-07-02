### Summary

This paper introduces a flow matching-based generative model to predict turbulent flows with long sequence steps. The authors claim that existing generative models suffer from spectral bias and common-mode noise when generating high-fidelity turbulent flows. To address these issues, they propose several components, including a salient flow attention module, a frequency-guided Fourier mixing module, and a pre-trained masked autoencoder to guide the training of the generative model. The proposed method is evaluated on various turbulent flow benchmarks, including the Compressible Navier-Stokes and Shear Flow datasets from PDEBench, demonstrating superior performance over existing methods.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The proposed method achieves superior performance on multiple benchmarks for turbulent flows.
- The proposed method can handle more long sequence steps compared to the baseline surrogate models.

### Weaknesses

#### Some Related Works


#### comment

 - The authors claim that existing generative models suffer from spectral bias and common-mode noise when generating high-fidelity turbulent flows. However, the authors do not provide sufficient evidence to support this claim. For example, there is no comparison of the spectral bias between the proposed method and existing methods. Similarly, there is no analysis or comparison of common-mode noise. While the authors include some analysis in Appendix C, this analysis is limited and does not include comparisons with existing methods. The spectral analysis in Appendix C only shows the spectrum of the proposed method's output, not a comparison with other generative models to demonstrate a reduction in spectral bias. Without this comparison, the claim that the proposed method mitigates spectral bias remains unsubstantiated. Furthermore, the common-mode noise analysis lacks a quantitative comparison with other methods, making it difficult to assess the effectiveness of the proposed approach in addressing this issue.
- The proposed method is evaluated only on the Compressible Navier-Stokes and Shear Flow datasets from PDEBench. The authors do not evaluate the method on other common turbulent flow datasets, such as the Navier-Stokes Spitting Taylor Green dataset or the 2D Navier-Stokes dataset with a Reynolds number of 1000. This limited evaluation makes it difficult to assess the generalizability of the proposed method to other turbulent flow scenarios. The absence of results on these standard datasets raises concerns about the robustness of the method and its applicability to a wider range of problems in fluid dynamics.
- The authors do not provide a detailed description of the model architecture, including the number of layers, activation functions, and other hyperparameters. This lack of detail makes it difficult to reproduce the results and assess the complexity of the proposed method. The absence of specific details regarding the Salient Flow Attention module, the Spatial-Temporal Transformer Branch, and the Frequency Mixing Branch makes it challenging to understand the exact implementation and to replicate the reported performance. This lack of transparency hinders the ability of other researchers to build upon this work.

### Suggestions

To strengthen the claims regarding spectral bias, the authors should include a comparative analysis of the spectral characteristics of the generated flows between their method and existing generative models. This should involve computing and plotting the power spectral density of the outputs from different methods, including the ground truth, and showing that the proposed method exhibits a spectrum closer to the ground truth and further from the spectra of other generative models. This analysis should be performed for all datasets considered in the paper. Furthermore, the authors should provide a quantitative measure of spectral bias, such as the integrated power in the high-frequency range, to support their claims. This would allow for a more objective comparison and would provide concrete evidence for the effectiveness of the proposed method in mitigating spectral bias. The analysis should also include a discussion of the specific frequency ranges where the proposed method shows improvement.

To address the concerns about the limited evaluation, the authors should evaluate their method on additional standard turbulent flow datasets, such as the Navier-Stokes Spitting Taylor Green dataset and the 2D Navier-Stokes dataset with a Reynolds number of 1000. This would provide a more comprehensive assessment of the method's generalizability and robustness. The evaluation should include the same metrics as used in the current paper, and the results should be compared with existing state-of-the-art methods on these datasets. This would allow for a more thorough understanding of the method's performance across different flow regimes and would increase the confidence in the method's applicability to a wider range of problems. The authors should also discuss any specific challenges or adaptations required to apply their method to these new datasets.

Finally, the authors should provide a detailed description of the model architecture, including the number of layers, activation functions, and other hyperparameters for each component of the model. This should include the Salient Flow Attention module, the Spatial-Temporal Transformer Branch, and the Frequency Mixing Branch. The authors should also provide the exact details of the adaptive fusion mechanism, including the architecture of the 1x1 convolutional layer and the sigmoid activation function. This information should be included in the main text or in an appendix, and it should be sufficient to allow other researchers to reproduce the results. This level of detail is crucial for the reproducibility of the work and for the community to build upon this research. The authors should also discuss the computational complexity of their method and compare it with existing methods.

### Questions

- The authors claim that existing generative models suffer from spectral bias and common-mode noise when generating high-fidelity turbulent flows. However, the authors do not provide sufficient evidence to support this claim. For example, there is no comparison of the spectral bias between the proposed method and existing methods. Similarly, there is no analysis or comparison of common-mode noise.
- The proposed method is evaluated only on the Compressible Navier-Stokes and Shear Flow datasets from PDEBench. The authors do not evaluate the method on other common turbulent flow datasets, such as the Navier-Stokes Spitting Taylor Green dataset or the 2D Navier-Stokes dataset with a Reynolds number of 1000.
- The authors do not provide a detailed description of the model architecture, including the number of layers, activation functions, and other hyperparameters.

### Rating

6

### Confidence

3

**********