### Summary

The paper introduces DGNet, a self-supervised learning model for EEG-based dementia classification that leverages multi-band frequency representation learning. The model employs a multi-head SimCLR architecture to process five key EEG frequency bands (delta, theta, alpha, beta, gamma) independently, allowing for more precise detection of subtle EEG changes associated with dementia. The key contributions include:

1. Frequency-band specific encoding: DGNet decomposes EEG signals into five standard frequency bands (delta, theta, alpha, beta, gamma) for processing, enabling the extraction of frequency-band specific representations.

2. Multi-Band Head: Each frequency band is processed by an independent CNN encoder and projection head, thereby preserving neural information unique to each band.

3. Effective for dementia classification: The model achieves significant performance improvements over training from scratch and single-head approaches, with a 31.5% relative performance improvement over training from scratch, and a 25.4% improvement over the single-head approach.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-organized and clearly written, making it easy to follow the methodology and results.

2. The proposed DGNet model demonstrates a novel approach by combining frequency-band specific representation learning with a multi-head SimCLR architecture, which is a creative fusion of existing ideas applied in a new context.

3. The paper provides a thorough evaluation of the proposed model, including comparisons with major benchmark models and ablation studies, which strengthens the credibility of the results.

### Weaknesses

#### comment

1. The methodological novelty of the proposed approach is limited. The core idea of using a multi-head SimCLR architecture for multi-band EEG data is a straightforward extension of existing techniques. The paper does not introduce any fundamentally new concepts or algorithms, but rather combines existing methods in a relatively obvious way. The use of independent CNN encoders and adaptive temperature parameters for each frequency band, while practically motivated, does not represent a significant theoretical or technical advancement.

2. The ablation study does not provide sufficient evidence to support the effectiveness of the proposed components. The performance gains observed when comparing the full model to the ablated versions are marginal, and it is unclear whether these gains are statistically significant or simply due to random variations in the training process. For example, the difference in accuracy between the full model and the single-head model is only 19.38%, which may not be substantial enough to justify the added complexity of the multi-head architecture. Furthermore, the ablation study lacks a systematic exploration of the parameter space, and the reported results do not convincingly demonstrate the necessity of each component.

3. The experimental evaluation is limited to a single dataset, which raises concerns about the generalizability of the proposed method. The authors do not provide any evidence that the method would perform well on other EEG datasets, particularly those with different characteristics or task requirements. The lack of evaluation on diverse datasets makes it difficult to assess the robustness and practical applicability of the proposed approach.

### Questions

1. How does the proposed multi-head SimCLR architecture specifically address the challenges of low signal-to-noise ratio and high inter-subject variability in EEG data? The paper mentions these challenges but does not provide a detailed explanation of how the proposed method mitigates them.

2. Can the authors provide a more detailed analysis of the performance improvements attributed to the multi-band approach, particularly in comparison to single-head models? The ablation study shows some improvement, but a more in-depth analysis of the feature representations learned by each head could provide valuable insights.

3. How does the proposed method perform on other EEG datasets, particularly those with different characteristics or task requirements? The current evaluation is limited to a single dataset, which raises concerns about the generalizability of the findings.

### Rating

5

### Confidence

3

**********