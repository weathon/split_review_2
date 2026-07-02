### Summary

The paper introduces Bhav-Net, a dual-space graph neural network architecture designed for distinguishing between antonyms and synonyms across multiple languages. The model leverages multilingual BERT encoders to initialize and guide graph convolutional networks, creating separate representational spaces for antonyms and synonyms. The dual-space approach allows for effective modeling of both the shared semantic domains and the oppositional nature of antonyms. The model is evaluated on a dataset spanning eight languages, demonstrating strong cross-lingual generalization and competitive results against state-of-the-art baselines. The paper also provides open-source code and model weights to facilitate reproducible research.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

1. The dual-space architecture is a novel approach to modeling antonym-synonym relationships, allowing for the explicit separation of synonymous and antonymous relationship modeling.
2. The paper provides open-source code and model weights, which promotes transparency and reproducibility in the research community.
3. The model demonstrates strong cross-lingual generalization capabilities, which is valuable for multilingual NLP applications.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a clear explanation of how the graph transformer processes the fused representations. Specifically, the mechanism by which the graph structure influences the learned representations and the subsequent classification is not well-articulated. It is unclear how the edge weights are determined and how these weights affect the message passing process within the graph transformer.
2. The paper does not provide a detailed description of the data collection process for the multilingual datasets used in the experiments. The criteria for selecting word pairs, the sources of the data, and any preprocessing steps are not clearly outlined. This lack of detail makes it difficult to assess the quality and representativeness of the datasets.
3. The paper fails to include a thorough ablation study to evaluate the contribution of each component of the proposed model. For example, the impact of the dual-space projection, the graph transformer, and the contrastive loss function are not individually assessed. This makes it difficult to understand the relative importance of each component and whether the model is over-engineered.
4. The paper does not adequately address the limitations of the proposed approach, such as its sensitivity to domain-specific terminology and polysemous words. The performance of the model on domain-specific texts, such as medical or legal documents, is not evaluated. Furthermore, the paper does not discuss how the model handles words with multiple senses, which could significantly impact the accuracy of antonym-synonym distinction.
5. The paper does not provide a detailed analysis of the computational complexity of the proposed model. The time and memory requirements for training and inference are not reported, making it difficult to assess the practical applicability of the model, especially for large-scale datasets.

### Suggestions

To improve the clarity and rigor of the paper, I suggest a more detailed explanation of the graph transformer's role within the Bhav-Net architecture. The authors should elaborate on how the graph structure is constructed, including the criteria for establishing edges between word pairs and the method for assigning edge weights. A clear description of the message-passing mechanism and how it incorporates the fused synonym and antonym representations would be beneficial. Furthermore, providing a visual representation of the graph structure and its evolution during training could enhance the reader's understanding. This would help clarify how the graph transformer contributes to the model's ability to capture complex semantic relationships and improve classification performance. Additionally, a more thorough discussion of the computational complexity of the graph transformer component would be valuable, including an analysis of its time and memory requirements compared to alternative approaches.

Regarding the multilingual datasets, the authors should provide a comprehensive overview of the data collection process in the main body of the paper. This should include a detailed description of the sources used for each language, the criteria for selecting word pairs, and any preprocessing steps applied to the data. For instance, if WordNet or ConceptNet were used, the specific versions and any filtering criteria should be mentioned. The authors should also discuss the potential biases introduced by the data collection process and how these biases might affect the model's performance. Furthermore, it would be beneficial to include an analysis of the dataset's characteristics, such as the distribution of word pairs across different parts of speech and the presence of any outliers or anomalies. This would allow readers to better understand the scope and limitations of the evaluation. Relocating some of the details from Appendix A to the main body of the paper could improve the paper's readability and flow.

Finally, a more extensive ablation study is needed to evaluate the contribution of each component of the Bhav-Net model. The authors should systematically remove or modify key components, such as the dual-space projection, the graph transformer, and the contrastive loss function, and report the impact on performance. For example, they could compare the performance of the full model with a version that uses only a single projection space, or a version that replaces the graph transformer with a simpler aggregation method. Additionally, they should investigate the sensitivity of the model to different hyperparameters, such as the learning rate, the batch size, and the number of transformer layers. This would help identify the most critical components of the model and provide insights into its robustness and generalizability. The authors should also consider evaluating the model's performance on domain-specific datasets to assess its sensitivity to terminology and on datasets with polysemous words to assess its ability to handle word sense disambiguation.

### Questions

1. How does the graph transformer process the fused synonym and antonym representations to improve classification performance? A more detailed explanation or a visual representation of this process would enhance the reader's understanding.
2. What is the rationale behind the specific thresholds and hyperparameters used in the model, such as the similarity threshold for graph edge creation? An analysis of the sensitivity of the model's performance to these hyperparameters would be valuable.
3. The paper mentions manual verification of samples to remove noisy or ambiguous relationships. Can you provide more details on the criteria used for this manual verification and the impact of this step on the overall data quality?

### Rating

5

### Confidence

3

**********