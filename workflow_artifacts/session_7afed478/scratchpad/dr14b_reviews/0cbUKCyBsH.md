### Summary

The paper introduces a new paradigm in time series forecasting called Influence-Aware Time Series Forecasting (IATSF), which aims to overcome the limitations of traditional self-stimulation methods by explicitly modeling external influences. The authors present a theoretical framework that demonstrates the inherent error bounds in self-stimulated models and show how incorporating influence information can reduce these bounds. They introduce the FIATS model, a lightweight, LLM-free architecture designed to integrate textual influences into time series forecasting. The paper also introduces a new benchmark dataset that is temporally aligned and leak-free, addressing the limitations of existing datasets.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. **Theoretical Rigor**: The paper provides a solid theoretical foundation for the proposed IATSF paradigm, using control theory to analyze the limitations of self-stimulation in time series forecasting. The mathematical derivations and proofs are well-supported and add depth to the argument.

2. **Novel Benchmark**: The introduction of a temporally-synced, leak-free benchmark dataset is a significant contribution. It addresses the limitations of existing datasets and provides a more realistic and challenging evaluation framework for influence-aware forecasting models.

3. **Innovative Model Design**: The FIATS model is well-designed and incorporates novel mechanisms, such as Channel-Aware Adaptive Sensitivity Modeling (CASM) and Channel-Aware Parameter Sharing (CAPS). These innovations enhance the model's ability to handle external influences effectively and efficiently.

4. **Empirical Validation**: The paper includes extensive experiments across various datasets, including synthetic, physics-based, and market systems. The results demonstrate the effectiveness of the proposed approach and provide strong empirical support for the theoretical claims.

5. **Interpretability and Robustness**: The paper emphasizes the interpretability of the FIATS model through attention maps and provides an ablation study to verify the robustness of the architecture. This adds credibility to the proposed method.

### Weaknesses

#### Some Related Works


#### comment

1. **Complexity of Implementation**: The FIATS model, while innovative, may be complex to implement and require significant computational resources. The paper could benefit from providing more details on the practical aspects of deploying the model, including specific hardware requirements and optimization strategies. For instance, the paper does not discuss the memory footprint of the model during training and inference, nor does it provide details on the specific optimization algorithms used and their hyperparameter tuning, which are crucial for reproducibility and practical application.

2. **Sensitivity to Noise in Influence Data**: The paper acknowledges that the model's performance can degrade with inaccurate influence inputs. However, the analysis of noise sensitivity could be more comprehensive. The paper should explore different types of noise (e.g., random, systematic, adversarial) and their impact on the model's performance. Additionally, the paper could investigate methods for denoising or robustifying the influence data, such as using Kalman filters or other noise reduction techniques, to improve the model's resilience.

3. **Generalizability to Other Domains**: While the paper demonstrates the effectiveness of IATSF across several datasets, it is unclear how well the approach generalizes to other domains or types of external influences. The paper should include experiments on a wider range of datasets, including those with different characteristics (e.g., higher dimensionality, different temporal scales, different types of external influences). For example, the performance of the model on datasets with highly correlated external influences or datasets with sparse influence data should be evaluated. A more thorough analysis of the model's limitations in different contexts would be beneficial.

4. **Dependence on High-Quality Influence Data**: The success of the IATSF paradigm heavily relies on the availability and quality of external influence data. In many real-world scenarios, such data may be scarce, unreliable, or difficult to obtain. The paper should discuss the implications of missing or incomplete influence data and explore methods for handling such situations, such as using imputation techniques or developing models that can learn from incomplete influence data. The paper could also investigate the use of proxy variables when direct influence data is not available.

### Suggestions

To address the complexity of implementation, the authors should provide a detailed guide on the practical aspects of deploying the FIATS model. This should include specific hardware requirements, such as GPU memory and CPU specifications, as well as optimization strategies, such as gradient accumulation and mixed-precision training. The paper should also include a discussion of the computational cost of training and inference, and how this cost scales with the size of the dataset and the complexity of the model. Furthermore, the authors should provide a sensitivity analysis of the model's performance to different hyperparameters, such as learning rate, batch size, and the number of training epochs. This would help practitioners to tune the model for their specific applications and ensure reproducibility of the results. The paper should also include a discussion of the limitations of the model, such as its sensitivity to noisy data and its dependence on high-quality influence data, and provide guidance on how to mitigate these limitations.

To improve the robustness of the model to noise in influence data, the authors should conduct a more comprehensive analysis of the impact of different types of noise on the model's performance. This should include experiments with random noise, systematic noise, and adversarial noise. The paper should also investigate methods for denoising or robustifying the influence data, such as using Kalman filters, moving average filters, or other noise reduction techniques. Furthermore, the authors should explore the use of data augmentation techniques to improve the model's generalization ability. For example, the authors could add small amounts of noise to the influence data during training to make the model more robust to noisy inputs. The paper should also include a discussion of the limitations of these methods and provide guidance on how to choose the most appropriate method for a given application.

To enhance the generalizability of the model, the authors should include experiments on a wider range of datasets, including those with different characteristics, such as higher dimensionality, different temporal scales, and different types of external influences. The paper should also evaluate the model's performance on datasets with highly correlated external influences or datasets with sparse influence data. Furthermore, the authors should investigate the use of transfer learning techniques to adapt the model to new domains or types of external influences. This would allow practitioners to leverage the knowledge learned from one dataset to improve the performance of the model on another dataset. The paper should also include a discussion of the limitations of the model in different contexts and provide guidance on how to choose the most appropriate model for a given application.

### Questions

1. **Scalability**: How does the FIATS model scale with very large datasets or high-dimensional time series? Are there any limitations in terms of computational resources or training time?

2. **Handling Noisy Influence Data**: What strategies can be employed to improve the model's robustness to noisy or inaccurate influence data? Are there any methods for denoising or filtering the influence inputs?

3. **Generalizability**: How well does the IATSF approach generalize to domains where the external influences are less structured or more complex? Are there any plans to test the model on a wider range of applications?

4. **Interpretability**: Can the attention maps generated by the CASM block be further analyzed to provide more insights into the specific influence patterns? How can these insights be used to improve the model or gain a better understanding of the underlying system dynamics?

5. **Real-World Deployment**: What are the practical challenges of deploying the FIATS model in real-world scenarios? How can these challenges be addressed to make the model more accessible and usable for practitioners?

### Rating

6

### Confidence

4

**********