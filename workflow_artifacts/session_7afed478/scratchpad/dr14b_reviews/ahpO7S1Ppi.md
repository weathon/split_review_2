### Summary

The paper introduces PCTX, a novel personalized context-aware tokenizer designed for generative recommendation models. Unlike traditional tokenization methods that are static and apply a universal item representation, PCTX allows the same item to be tokenized differently based on the user's historical interactions, thereby capturing multiple interpretive standards of items. The core innovation lies in incorporating user-specific contexts during the tokenization process, which enables generative recommendation models to produce more personalized predictions. The authors demonstrate the effectiveness of PCTX through extensive experiments on three public datasets, showing significant improvements in performance over non-personalized tokenization baselines.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1) The paper introduces a novel approach to tokenization in the context of generative recommendation by personalizing the tokenization process based on user context. This is an interesting departure from the static tokenization methods that dominate the current literature.

2) The proposed method incorporates user historical interactions into the tokenization process, which is a step towards capturing user-specific interpretations of items.

3) The paper provides a comprehensive set of experiments across three public datasets, which demonstrates the generalizability of the proposed method to different domains.

### Weaknesses

#### Some Related Works


#### comment

1) The proposed method introduces significant complexity by incorporating personalized context into the tokenization process. This includes clustering context representations, merging semantic IDs, and data augmentation strategies, which might make the model more difficult to train and tune. Specifically, the clustering of context representations using k-means++ introduces a hyperparameter that requires careful selection, and the merging of semantic IDs, while intended to improve generalizability, adds another layer of complexity to the tokenization process. The data augmentation strategy, while potentially beneficial, also introduces additional computational overhead and requires careful tuning to avoid introducing noise into the training data.

2) The paper primarily focuses on the Amazon Review datasets, which, while diverse, may not fully represent the complexity and scale of real-world industrial applications, such as those in short video or social media recommendation systems. The sequential nature of interactions and the type of item metadata in these datasets might differ significantly from the Amazon Review datasets, potentially affecting the performance of the proposed method. For example, the short video domain often involves more implicit feedback and rapidly changing user preferences, which may not be well-captured by the proposed approach.

3) The paper does not extensively discuss the scalability of PCTX, especially concerning the computational cost of the personalized tokenization process in large-scale systems. The personalized context representation and the subsequent clustering and merging steps could become computationally expensive as the number of users and items grows. The paper lacks a detailed analysis of the time and memory complexity of these operations, making it difficult to assess the practical applicability of the method in large-scale industrial settings.

### Suggestions

To address the complexity concerns, the authors should explore alternative methods for context representation that are less computationally demanding than k-means++ clustering. For example, they could investigate using a learned embedding for user context that does not require explicit clustering. This could involve training a separate neural network to map user interaction histories to a dense vector representation, which could then be used to personalize the tokenization process. Additionally, the authors should provide a more detailed analysis of the sensitivity of the model to the hyperparameters associated with the clustering and merging steps. This would help practitioners understand the trade-offs between model performance and computational cost, and provide guidance on how to tune these parameters effectively. Furthermore, the authors should consider exploring simpler data augmentation techniques that do not introduce as much computational overhead, such as random masking or swapping of tokens, to reduce the overall complexity of the proposed method.

To better demonstrate the generalizability of PCTX, the authors should conduct experiments on datasets from other domains, such as short video or social media platforms. This would help to assess the robustness of the method to different types of user interactions and item metadata. Specifically, the authors should consider datasets that include implicit feedback and rapidly changing user preferences, which are common in many real-world applications. The authors should also provide a detailed analysis of the performance of PCTX on these datasets, including a comparison to existing baselines. This would help to demonstrate the practical applicability of the method in a wider range of scenarios. Moreover, the authors should investigate the impact of different types of item metadata on the performance of PCTX, and explore methods for incorporating this information into the tokenization process.

Finally, the authors should provide a more detailed analysis of the computational cost of PCTX, including the time and memory complexity of the personalized tokenization process. This analysis should consider the scalability of the method to large-scale systems with millions of users and items. The authors should also explore techniques for optimizing the tokenization process, such as using efficient data structures and parallel computing. This would help to make the method more practical for real-world applications. Furthermore, the authors should provide a comparison of the computational cost of PCTX to existing baselines, to demonstrate the trade-offs between model performance and computational efficiency. This would help practitioners to make informed decisions about whether to use PCTX in their applications.

### Questions

1) How does the computational complexity of PCTX compare to traditional tokenization methods, especially in terms of training time and memory usage? Can the authors provide a detailed analysis of the computational overhead introduced by the personalized tokenization process?

2) How sensitive is PCTX to the choice of hyperparameters, such as the number of clusters for context representations and the frequency threshold for merging semantic IDs? Can the authors provide ablation studies that show the impact of these hyperparameters on model performance?

3) Have the authors considered the potential for user privacy concerns with PCTX, given that it incorporates user historical interactions into the tokenization process? How does the method ensure compliance with data protection regulations such as GDPR or CCPA?

### Rating

6

### Confidence

3

**********