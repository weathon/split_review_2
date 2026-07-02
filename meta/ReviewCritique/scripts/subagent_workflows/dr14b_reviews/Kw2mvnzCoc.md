### Summary

The paper introduces TSPulse, a compact pre-trained model for time-series analysis with a focus on diagnostic tasks like anomaly detection, imputation, and classification. TSPulse achieves this by learning disentangled representations across time, frequency, and semantic spaces, allowing it to capture complementary cues from different perspectives. The model employs a TSMixer backbone and multiple heads for distinct objectives, such as reconstruction and semantic signature prediction. TSPulse demonstrates strong zero-shot and fine-tuned performance across various datasets, outperforming larger models while maintaining efficiency and supporting GPU-free deployment.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The paper introduces a novel pre-training framework that combines masked reconstruction with disentanglement across multiple spaces and abstraction levels, allowing the model to capture complementary cues from time, frequency, and semantic domains.
3. The paper introduces lightweight post-hoc fusers that selectively combine the disentangled views based on the task type, enabling effective task specialization.
4. The paper introduces a hybrid masking strategy that randomizes both masking types and span lengths, enhancing pre-training robustness and mitigating mask-induced bias.
5. The paper demonstrates strong empirical results across various time-series diagnostic tasks, including anomaly detection, imputation, classification, and similarity search.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a detailed analysis of the computational cost of TSPulse compared to other pre-trained models. While the authors mention that TSPulse is compact, a more thorough comparison of training and inference time, as well as memory usage, would be helpful. Specifically, a breakdown of the computational cost associated with each component of the model (e.g., TSMixer backbone, disentanglement heads, post-hoc fusers) would be valuable for understanding the efficiency gains. Furthermore, the paper lacks a comparison of the number of parameters and FLOPs with other pre-trained models, making it difficult to assess the true computational advantage of TSPulse.
2. The paper focuses on four specific time-series diagnostic tasks. It would be interesting to see how TSPulse performs on other time-series tasks, such as forecasting or anomaly detection. While the paper mentions anomaly detection, it does not explore the performance of TSPulse on forecasting tasks, which are also crucial in many real-world applications. The lack of evaluation on forecasting limits the generalizability of the proposed approach.
3. The paper could benefit from a more in-depth discussion of the limitations of the proposed approach and potential directions for future research. For example, the paper does not discuss the potential impact of the choice of pre-training data on the performance of TSPulse. It would be beneficial to explore how the model's performance varies when pre-trained on different datasets or with different masking strategies. Additionally, the paper could discuss the limitations of the disentanglement approach and potential challenges in applying it to more complex time-series data.

### Suggestions

To address the lack of detailed computational analysis, the authors should include a comprehensive comparison of training and inference times, as well as memory usage, against other pre-trained models. This comparison should not only focus on the overall computational cost but also provide a breakdown of the cost associated with each component of the model. For example, the authors could report the time and memory usage for the TSMixer backbone, disentanglement heads, and post-hoc fusers separately. Furthermore, the paper should include a comparison of the number of parameters and FLOPs with other pre-trained models, which would provide a more concrete understanding of the computational efficiency of TSPulse. This analysis should be conducted on a standardized hardware setup to ensure fair comparisons. Additionally, the authors should explore the scalability of TSPulse with respect to the length of the input time series and the number of channels, as this is a critical factor in real-world applications.

To broaden the scope of the paper, the authors should evaluate TSPulse on a wider range of time-series tasks, particularly forecasting. While the paper demonstrates strong performance on diagnostic tasks, forecasting is a crucial application of time-series analysis. The authors could explore how the disentangled representations learned by TSPulse can be leveraged for forecasting tasks. This could involve adapting the model architecture or training procedure to accommodate forecasting objectives. For example, the authors could investigate the use of the learned representations as input features for a forecasting model or explore the possibility of fine-tuning the entire TSPulse model for forecasting. This would provide a more comprehensive evaluation of the model's capabilities and its potential for real-world applications. Furthermore, the authors should consider evaluating the model on datasets with different characteristics, such as varying time series lengths, sampling rates, and noise levels, to assess the robustness of TSPulse.

Finally, the authors should provide a more in-depth discussion of the limitations of the proposed approach and potential directions for future research. This discussion should include an analysis of the impact of the choice of pre-training data on the performance of TSPulse. The authors could explore how the model's performance varies when pre-trained on different datasets or with different masking strategies. Additionally, the paper should discuss the limitations of the disentanglement approach and potential challenges in applying it to more complex time-series data. For example, the authors could discuss the potential for information loss during the disentanglement process and how this might affect the model's performance on downstream tasks. The authors should also consider the potential for bias in the pre-training data and how this might affect the model's generalization capabilities. This discussion should provide a more balanced and realistic assessment of the proposed approach and guide future research in this area.

### Questions

Please refer to the weakness.

### Rating

8

### Confidence

3

**********