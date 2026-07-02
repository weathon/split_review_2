### Summary

This paper introduces a novel approach to differentially private (DP) data synthesis by leveraging dataset distillation techniques. The proposed method, SPS (Summarize-Privatize-Synthesize), generates synthetic datasets that preserve the utility of the original data while ensuring privacy. The authors further enhance SPS with multitask clipping and grouped pseudo-classes, resulting in SPS+. The paper demonstrates that SPS+ outperforms existing DP methods on image classification tasks, achieving higher accuracy and better scalability. Additionally, the authors highlight the practical advantages of their approach, including support for model ensembling, federated learning, and continual learning without additional privacy costs.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper presents a novel approach to differentially private data synthesis by combining dataset distillation with privatization techniques. This is a creative combination of existing ideas that leads to significant improvements in accuracy compared to prior work.
2. The authors provide rigorous theoretical analysis of the privacy guarantees of their method, including detailed proofs for the RDP composition. The empirical evaluation is comprehensive, including experiments on multiple datasets (CIFAR-10, CIFAR-100, CAMELYON17), different privacy budgets, and comparisons with state-of-the-art baselines.
3. The paper is well-written and clearly explains the technical details of the proposed method. The authors provide a thorough explanation of the motivation behind their approach and the challenges they address. The use of figures and tables effectively illustrates the key concepts and results.

### Weaknesses

#### Some Related Works


#### comment

1. The method relies on the availability of a suitable public pre-trained model. The performance may degrade if the pre-trained model is not well-suited for the target dataset. The paper does not explore the sensitivity of the method to the choice of pre-trained model architecture or the degree of mismatch between the pre-training and target datasets. This is a critical dependency that needs further investigation, as the method's practical applicability is directly tied to the availability of appropriate pre-trained models.
2. The paper primarily focuses on image classification tasks. It is unclear how well the method would generalize to other types of data or machine learning tasks. The evaluation lacks experiments on diverse data modalities such as text, time-series data, or graphs. The method's reliance on intermediate activation statistics might not be directly transferable to other data types, and the paper does not discuss potential adaptations or limitations in these contexts.
3. The paper does not provide a detailed analysis of the computational cost of the proposed method compared to DP-SGD. While the authors mention that their method is faster, a quantitative comparison of training time, memory usage, and other relevant metrics is missing. This makes it difficult to assess the practical trade-offs between the proposed method and existing approaches. The paper should include a breakdown of the computational cost associated with each step of the proposed method, such as the summarization, privatization, and synthesis phases.

### Suggestions

The paper should include a more thorough investigation into the sensitivity of the proposed method to the choice of pre-trained model. Specifically, experiments should be conducted using pre-trained models with varying architectures and trained on datasets with different levels of similarity to the target dataset. This would help to quantify the impact of pre-trained model selection on the performance of the proposed method. Furthermore, the authors should explore techniques to mitigate the performance degradation when a suitable pre-trained model is not available, such as using ensemble methods or fine-tuning the pre-trained model on a small amount of public data. A detailed analysis of the computational cost of the proposed method is also needed. This should include a breakdown of the time and memory requirements for each step of the algorithm, as well as a comparison with the computational cost of DP-SGD. The authors should also investigate the scalability of the proposed method to larger datasets and more complex models.

To address the limited scope of the evaluation, the authors should extend their experiments to include other data modalities and machine learning tasks. This could involve adapting the proposed method to handle text data, time-series data, or graph data. For example, the authors could explore the use of recurrent neural networks or graph neural networks as the base models for extracting intermediate activation statistics. The evaluation should also include a wider range of tasks, such as regression, natural language processing, and reinforcement learning. This would provide a more comprehensive assessment of the generalizability of the proposed method. The authors should also discuss the potential limitations of the proposed method when applied to different data types and tasks, and suggest potential solutions to overcome these limitations.

Finally, the paper should provide a more detailed explanation of the multitask clipping and grouped pseudo-classes techniques. The authors should discuss the rationale behind these techniques and provide a theoretical analysis of their effectiveness. The paper should also include ablation studies to evaluate the impact of these techniques on the performance of the proposed method. This would help to better understand the contribution of each component of the proposed method and provide insights into potential areas for further improvement. The authors should also discuss the limitations of these techniques and suggest potential directions for future research.

### Questions

1. How does the performance of the proposed method vary with different choices of public pre-trained models? Are there any specific characteristics of the pre-trained model that are crucial for achieving good performance?
2. Can the proposed method be extended to other types of data or machine learning tasks beyond image classification? What are the potential challenges and limitations in such extensions?
3. What is the computational cost of the proposed method compared to DP-SGD? How does the computational cost scale with the size of the dataset and the complexity of the model?
4. How does the choice of hyperparameters, such as the number of pseudo-classes and the number of stages in multistage clipping, affect the performance of the proposed method? Are there any guidelines for selecting these hyperparameters in practice?

### Rating

6

### Confidence

3

**********