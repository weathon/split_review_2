### Summary

This paper proposes RetrievalFormer, a transformer-based dual-encoder architecture for recommendation systems. The model addresses two key challenges in recommendation systems: scalability and cold-start item recommendation. The authors evaluate RetrievalFormer on Amazon and MovieLens benchmarks, demonstrating competitive accuracy and significant latency reduction compared to strong transformer-based sequential baselines. The model's ability to recommend cold-start items is also evaluated using a new Leave-One-Out Cold (LOOC) protocol.

### Soundness

3

### Presentation

3

### Contribution

2

### Strengths

1. The paper is well-written and easy to follow. The authors clearly explain the motivation behind their work and the technical details of their proposed model.
2. The proposed Leave-One-Out Cold (LOOC) evaluation protocol is a valuable contribution to the field, as it provides a more realistic assessment of a model's ability to handle truly unseen items.
3. The authors demonstrate the practical applicability of their model by showing that it can be deployed efficiently using Approximate Nearest Neighbor (ANN) search, which is crucial for large-scale recommendation systems.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a thorough discussion of the limitations of the proposed approach. For example, the authors do not discuss the potential biases introduced by the ANN retrieval process or the impact of feature quality on the model's performance.
2. The experimental evaluation could be more comprehensive. While the paper compares RetrievalFormer with some sequential recommendation models, it lacks comparisons with other relevant baselines, especially those that handle large-scale catalogs or cold-start scenarios effectively.
3. The paper does not provide sufficient details on the computational resources required for training and deploying the model, which is an important consideration for practical applications.

### Suggestions

The paper should delve deeper into the potential biases introduced by the Approximate Nearest Neighbor (ANN) retrieval process. Specifically, the authors should investigate whether the ANN index tends to favor certain types of items over others, potentially leading to a lack of diversity in recommendations. For example, if the item embeddings are clustered in a way that reflects popularity rather than relevance, the ANN search might disproportionately recommend popular items, even if they are not the most suitable for a given user. Furthermore, the authors should explore the impact of different ANN algorithms and parameters on the final recommendation quality. A sensitivity analysis of the ANN index construction and search parameters would provide valuable insights into the robustness of the proposed approach. This analysis should include metrics beyond just accuracy, such as diversity and novelty of recommendations.

To strengthen the experimental evaluation, the authors should include comparisons with a wider range of baselines, particularly those designed for large-scale catalogs and cold-start scenarios. For instance, methods that explicitly model item metadata or use knowledge graphs to infer relationships between items could be relevant baselines. Additionally, the authors should consider evaluating their model on datasets with varying degrees of sparsity and item feature quality. This would help to better understand the limitations of the proposed approach and identify scenarios where it performs particularly well or poorly. The evaluation should also include a more detailed analysis of the cold-start performance, perhaps by categorizing cold-start items based on their feature similarity to existing items and reporting performance separately for each category. This would provide a more nuanced understanding of the model's ability to handle truly novel items.

Finally, the paper should provide a more detailed analysis of the computational resources required for training and deploying the model. This should include not only the training time and memory requirements but also the inference latency and throughput. The authors should specify the hardware used for their experiments, including the type of CPU, GPU, and memory. Furthermore, they should provide a breakdown of the computational cost of each component of the model, such as the transformer encoder and the ANN index construction and search. This information is crucial for practitioners who want to deploy the model in real-world applications. The authors should also discuss the scalability of the model with respect to the size of the item catalog and the number of users.

### Questions

1. How does the model perform when there is limited or no feature information available for new items?
2. What are the computational resources required for training and deploying the model, and how does this scale with the size of the item catalog?
3. How does the model handle user behavior that deviates significantly from the patterns seen in the training data?

### Rating

6

### Confidence

3

**********