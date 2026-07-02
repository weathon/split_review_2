### Summary

The paper introduces a novel framework for detecting lead-lag relationships in financial markets using Temporal Graph Neural Networks (TGNNs). The authors frame lead-lag detection as a temporal link prediction task on dynamic graphs, where nodes represent financial assets, and edges capture predictive relationships. They propose a new benchmark dataset of financial assets enriched with temporal, structural, and sentiment features, and evaluate multiple TGNN architectures, including GraphMixer, which achieves superior performance. The findings demonstrate the effectiveness of TGNNs in modeling complex lead-lag relationships and open new avenues for data-driven financial market analysis.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel formulation of lead-lag detection as a temporal link prediction problem on dynamic graphs, providing a fresh perspective on this important financial task. This approach allows for the simultaneous modeling of multiple assets with interdependent time dynamics, extending beyond the limits of traditional pairwise or static analysis methods.
2. The study adapts and evaluates a range of State-of-the-Art temporal GNN architectures, from simple LSTMs to complex TGNN models, providing a comprehensive benchmark for the task. The inclusion of a novel GraphMixer model, which achieves superior performance, demonstrates the potential of simpler architectures when effectively leveraging temporal and structural information.
3. The paper introduces a new dataset of financial assets with five years of daily pricing data, financial indicators, and sentiment features, which serves as a valuable benchmark for evaluating temporal graph models in finance. This dataset, along with the detailed experimental setup and ablation studies, enhances the reproducibility and reliability of the findings.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a thorough comparison with traditional non-ML methodologies for lead-lag detection, which could provide a more comprehensive understanding of the advantages of the proposed approach. Specifically, the absence of comparisons against established statistical methods like Granger causality, or vector autoregression (VAR) models, makes it difficult to assess the relative improvement offered by the proposed TGNN framework. These methods, while not directly modeling dynamic graphs, offer valuable baselines for evaluating the performance gains of more complex models.
2. The problem formulation, particularly the definition of lead-lag relationships based on a fixed threshold, could be more rigorously justified and compared with existing statistical definitions. The choice of a fixed threshold for both positive and negative returns, without a clear rationale based on financial theory or empirical analysis, raises concerns about the robustness of the detected relationships. Furthermore, the paper does not explore the sensitivity of the results to different threshold values, which is crucial for understanding the practical implications of this parameter.
3. The paper could benefit from a more detailed discussion on the practical implications of the findings for trading strategies and risk management. While the paper demonstrates the ability to detect lead-lag relationships, it does not provide concrete examples of how these findings can be translated into actionable investment decisions or risk mitigation strategies. The lack of discussion on transaction costs, market impact, and the robustness of the strategy in different market conditions limits the practical relevance of the study.

### Suggestions

The paper would significantly benefit from a more rigorous comparison with traditional statistical methods for lead-lag detection. Specifically, the authors should include baselines such as Granger causality and vector autoregression (VAR) models. These methods, while not designed for dynamic graph structures, are widely used in finance and provide a crucial benchmark for evaluating the performance of the proposed TGNN framework. The comparison should not only focus on predictive performance but also on the interpretability and computational cost of each method. For instance, Granger causality, despite its limitations in capturing non-linear relationships, offers a clear statistical framework for assessing lead-lag relationships. The authors should also explore the possibility of adapting these traditional methods to incorporate temporal graph information, which could lead to more robust and interpretable models. This would provide a more comprehensive understanding of the advantages and limitations of the proposed approach.

Furthermore, the paper needs a more detailed justification for the chosen threshold-based definition of lead-lag relationships. The authors should explore the sensitivity of their results to different threshold values and provide a rationale for their specific choice based on financial theory or empirical analysis. For example, they could analyze the distribution of returns and select a threshold that corresponds to a specific quantile or standard deviation from the mean. Additionally, the authors should consider alternative definitions of lead-lag relationships, such as those based on statistical significance tests or information-theoretic measures. This would allow for a more robust and comprehensive analysis of the lead-lag phenomenon. The paper should also discuss the potential limitations of the threshold-based approach, such as its sensitivity to noise and its inability to capture subtle or complex relationships.

Finally, the paper should include a more detailed discussion on the practical implications of the findings for trading strategies and risk management. The authors should provide concrete examples of how the detected lead-lag relationships can be used to develop actionable investment strategies. This should include a discussion of transaction costs, market impact, and the robustness of the strategy in different market conditions. For example, the authors could propose a specific trading strategy based on the predicted lead-lag relationships and evaluate its performance using historical data. They should also discuss how the identified relationships can be used for risk management, such as by diversifying portfolios or hedging against potential losses. The paper should also address the limitations of the proposed approach in real-world trading scenarios, such as the impact of latency and the potential for model overfitting.

### Questions

1. Why is the threshold-based relationship definition in Equation 1 considered a paradigmatic shift from traditional statistical approaches like Granger causality? Could you provide more justification for this new definition and compare it with existing statistical definitions of lead-lag relationships?
2. How does the proposed framework compare with traditional statistical methods for lead-lag detection, such as Granger causality or vector autoregression (VAR) models? Could you provide a comparison or discuss the potential for integrating these approaches?
3. What is the rationale behind the specific choice of ε = 5% for the threshold? How sensitive are the results to different values of ε, and could you provide an analysis of this sensitivity?
4. Could you provide more details on the practical implications of the findings for trading strategies and risk management? How can the detected lead-lag relationships be used to inform investment decisions in real-time trading scenarios?
5. How does the proposed framework handle noisy or incomplete data, which is common in real-world financial markets? Could you discuss the robustness of the approach to such data quality issues?
6. The paper mentions that the GraphMixer model performs best with only node description embeddings. Could you provide more insights into why this is the case and how it compares with the performance of other models when using different feature sets?

### Rating

6

### Confidence

3

**********