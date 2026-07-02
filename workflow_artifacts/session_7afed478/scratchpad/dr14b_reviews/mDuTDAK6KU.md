### Summary

This paper proposes a novel adversarial detection method based on the disagreement between KL divergence and L0-based similarity metrics. The authors provide a theoretical proof of correctness under certain assumptions and demonstrate the effectiveness of their approach through experiments on CIFAR-10 and Tiny-ImageNet.

### Soundness

3

### Presentation

3

### Contribution

2

### Strengths

1. The idea of using metric disagreement for adversarial detection is novel and interesting.
2. The theoretical analysis provides a formal justification for the proposed method.
3. The method is lightweight and does not require adversarial training or architectural changes.

### Weaknesses

#### Some Related Works


#### comment

1. The theoretical analysis relies on several assumptions (A1-A4) that may not always hold in practice. For instance, the assumption of a sufficiently large separation between class prototypes in the feature space might not be satisfied for all models or datasets, especially those with high intra-class variability or low inter-class separability. This could limit the applicability of the method in real-world scenarios where feature spaces are not perfectly separated. The paper does not provide a quantitative analysis of how the degree of separation affects the detection performance, making it difficult to assess the practical robustness of the method.

2. The experiments are limited to two datasets (CIFAR-10 and Tiny-ImageNet) and two model architectures (ResNet-18 and CLIP). While these are common benchmarks, they do not fully represent the diversity of real-world applications. The method's performance on more complex datasets with higher resolution images, more classes, or different data modalities (e.g., text, audio) is unknown. Furthermore, the chosen models are relatively shallow compared to state-of-the-art models, which may have different feature space characteristics. The lack of experiments on more complex models and datasets makes it difficult to generalize the findings.

3. The paper does not explore the impact of different types of adversarial attacks beyond those tested. The method's robustness against more sophisticated attacks, such as those designed to specifically target the feature space or the specific metrics used (KL divergence and L0-based similarity), is not evaluated. This leaves a gap in understanding the method's resilience against adaptive adversaries. The paper should include an analysis of the method's performance against a wider range of attack types, including those that are specifically designed to evade detection.

4. The method's performance is highly dependent on the quality of the pre-trained image encoder and the fine-tuning process. If the encoder does not produce well-separated class prototypes, the detection performance may degrade significantly. The paper lacks a detailed analysis of how the choice of encoder and the fine-tuning hyperparameters affect the final detection performance. The sensitivity of the method to these factors needs to be thoroughly investigated.

### Suggestions

To strengthen the paper, the authors should first address the limitations of the theoretical analysis by providing a more detailed discussion of the assumptions and their implications. Specifically, they should investigate the sensitivity of the method to violations of assumptions A1-A4. This could involve experiments where these assumptions are intentionally violated, such as by using datasets with known high intra-class variability or by manipulating the feature space to reduce inter-class separability. Furthermore, the authors should provide a more rigorous analysis of the conditions under which the class prototypes are sufficiently separated, possibly by introducing a quantitative measure of separation and relating it to the detection performance. This would provide a clearer understanding of the method's applicability and limitations in different scenarios. Additionally, the authors should explore the impact of different pre-trained encoders and fine-tuning strategies on the detection performance, providing a more comprehensive analysis of the method's sensitivity to these factors.

Second, the experimental evaluation needs to be significantly expanded to include a wider range of datasets and model architectures. The authors should consider evaluating their method on more complex datasets, such as ImageNet or datasets with higher resolution images, and on more diverse model architectures, including deeper networks and models from different families (e.g., Transformers). This would provide a more comprehensive assessment of the method's generalizability and robustness. Additionally, the authors should explore the method's performance on different data modalities, such as text or audio, to demonstrate its versatility. This could involve adapting the method to handle different types of input data and evaluating its performance on relevant benchmarks. Such an expansion would greatly enhance the paper's impact and credibility. The authors should also investigate the method's performance against a wider range of adversarial attacks, including those that are specifically designed to evade detection, to provide a more thorough evaluation of its robustness.

Finally, the authors should provide a more detailed analysis of the computational cost of their method, including the time and memory requirements for both training and inference. This analysis should compare the computational cost of their method to other adversarial detection methods, providing a more complete picture of its practical feasibility. The authors should also discuss the potential limitations of their method in real-world applications, such as the impact of noisy or corrupted data on its performance. Addressing these practical considerations would make the paper more relevant and useful to the broader research community.

### Questions

1. How sensitive is the method to violations of the assumptions (A1-A4) in the theoretical analysis? Are there scenarios where these assumptions are likely to fail, and how would that affect detection performance?

2. How does the method perform on more complex datasets or with deeper, more modern architectures? Are there any known limitations in scaling the approach to larger or more diverse models?

3. What is the impact of different types of adversarial attacks on the detection performance? Have the authors tested the method against more sophisticated attacks, such as those designed to specifically target the feature space or the metrics used?

4. How does the choice of the pre-trained image encoder and the fine-tuning process affect the final detection performance? Is there a sensitivity to the quality of the pre-trained model or the fine-tuning hyperparameters?

### Rating

6

### Confidence

3

**********