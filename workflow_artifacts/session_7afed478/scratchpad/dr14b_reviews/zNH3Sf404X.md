### Summary

The paper presents a novel approach to detecting illicit cryptocurrency transactions, specifically focusing on Bitcoin's Shared Send Mixers (SSMs). The authors argue that data quality, rather than quantity, is crucial for effective semi-supervised learning (SSL) in this domain. They introduce a framework that incorporates high-fidelity features like KeyLinker address clustering and Shared Send Untangling (SSU) complexity metrics to improve the identification of illicit flows. The study contributes a comprehensive historical dataset of 163 million Bitcoin transactions with SSM classification and demonstrates that SSL, when guided by quality-focused features, achieves a strong F1-score of 0.84. The findings emphasize the importance of strategic feature engineering over relying on larger datasets with potentially noisy heuristics.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

1. The paper provides a comprehensive dataset of 163 million Bitcoin transactions, which is a valuable resource for future research in blockchain forensics.
2. The introduction of novel features like KeyLinker address clustering and SSU complexity metrics enhances the detection of illicit flows by focusing on data quality.
3. The study demonstrates that semi-supervised learning can effectively leverage unlabeled data when guided by high-fidelity features, achieving a strong F1-score of 0.84.

### Weaknesses

#### Some Related Works


#### comment

1. The paper's reliance on SSL may introduce biases if the unlabeled data is not representative of the broader transaction patterns. How do you ensure that the unlabeled data used for pseudo-labeling accurately reflects the diversity of Bitcoin transactions, especially given the evolving nature of mixing techniques and the potential for adversarial obfuscation? Specifically, the paper does not address the potential for temporal shifts in transaction patterns, where older transactions might exhibit different characteristics than recent ones, leading to a bias in the pseudo-labeling process. Furthermore, the paper lacks a discussion on how the selection of unlabeled data impacts the final model performance, particularly if the unlabeled data is skewed towards specific transaction types or time periods.
2. The study emphasizes feature quality but does not provide a detailed analysis of how specific features impact model performance across different transaction types. Could you provide a feature importance analysis to clarify which features are most influential in detecting illicit transactions, and how these features perform across various transaction categories? The paper should include a breakdown of feature importance not just globally, but also within specific transaction categories (e.g., mixing services, exchanges, personal transfers) to understand if the same features are consistently important or if different features are more relevant for different types of transactions. This analysis should also consider the potential for feature interactions and how these interactions might affect the model's ability to detect illicit activities.
3. The framework's effectiveness in real-world scenarios, where transaction patterns and mixing techniques are constantly evolving, is not fully addressed. How does your model adapt to new anonymization techniques and changes in user behavior over time? The paper needs to discuss the model's robustness to adversarial attacks, where malicious actors might intentionally alter their transaction patterns to evade detection. Additionally, the paper should explore the model's performance under different levels of noise and obfuscation, which are common in real-world illicit transactions. The paper should also consider the computational cost of retraining the model frequently to adapt to new patterns and whether this is feasible in a real-world setting.

### Suggestions

To address the concern about the representativeness of unlabeled data, the authors should implement a more rigorous data selection process. This could involve stratifying the unlabeled data based on transaction characteristics such as size, frequency, and time of day, ensuring that the pseudo-labeled data reflects the diversity of the overall transaction pool. Furthermore, the authors should explore techniques like temporal cross-validation, where the model is trained on older data and tested on more recent data, to assess its ability to generalize to new transaction patterns. This would help to identify potential biases introduced by temporal shifts in transaction behavior. The authors should also consider using techniques such as adversarial training to make the model more robust to evolving mixing techniques. This would involve generating synthetic transactions that mimic potential adversarial strategies and using these to train the model, thereby improving its ability to detect illicit activities even when they are intentionally obfuscated.

To provide a more detailed analysis of feature importance, the authors should conduct a breakdown of feature contributions across different transaction categories. This could involve using techniques such as SHAP values or permutation importance to quantify the impact of each feature on the model's predictions for specific transaction types. For example, the analysis should reveal whether features related to KeyLinker clustering are more important for detecting mixing services, while features related to transaction frequency are more important for detecting exchanges. This analysis should also consider the potential for feature interactions, where the combination of multiple features might be more informative than individual features alone. The authors should also explore the use of visualization techniques to present the feature importance results in a more intuitive and accessible manner, such as heatmaps or bar charts that show the relative importance of each feature for different transaction categories.

To enhance the framework's adaptability to evolving transaction patterns, the authors should implement a continuous learning approach. This could involve periodically retraining the model on new data, incorporating feedback from human analysts, and using techniques such as online learning to update the model in real-time. The authors should also explore the use of anomaly detection techniques to identify new transaction patterns that might indicate the emergence of novel anonymization techniques. This would allow the model to adapt to new threats more quickly and effectively. Additionally, the authors should consider the computational cost of retraining the model and explore techniques such as model compression or pruning to reduce the computational overhead. The paper should also include a discussion of the trade-offs between model accuracy and computational cost, and how these trade-offs might impact the practical deployment of the framework.

### Questions

1. The paper's reliance on SSL may introduce biases if the unlabeled data is not representative of the broader transaction patterns. How do you ensure that the unlabeled data used for pseudo-labeling accurately reflects the diversity of Bitcoin transactions, especially given the evolving nature of mixing techniques and the potential for adversarial obfuscation?
2. The study emphasizes feature quality but does not provide a detailed analysis of how specific features impact model performance across different transaction types. Could you provide a feature importance analysis to clarify which features are most influential in detecting illicit transactions, and how these features perform across various transaction categories?
3. The framework's effectiveness in real-world scenarios, where transaction patterns and mixing techniques are constantly evolving, is not fully addressed. How does your model adapt to new anonymization techniques and changes in user behavior over time?

### Rating

3

### Confidence

3

**********