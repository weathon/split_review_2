### Summary

The paper introduces EmoSign, a novel multimodal dataset for understanding emotions in American Sign Language (ASL). Unlike spoken languages, where prosodic features convey emotion, emotion indicators in sign language are less understood, creating communication barriers. EmoSign addresses this gap by providing 200 ASL videos with sentiment and emotion labels, annotated by experienced Deaf ASL signers. The dataset includes benchmarks of baseline models for sentiment and emotion classification, highlighting the current limitations of multimodal models in integrating visual cues for emotional reasoning. The authors emphasize the need for new architectures that can distinguish between syntactic and affective functions of visual cues in sign languages.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel dataset, EmoSign, which is the first of its kind to focus on sentiment and emotion recognition in ASL videos. This dataset fills a significant gap in sign language research and provides a valuable resource for the development of emotion-aware models for sign languages.
2. The dataset is annotated by three Deaf ASL signers with professional interpretation experience, ensuring high-quality and culturally relevant annotations. The inclusion of open-ended descriptions of emotion cues adds depth to the dataset and provides insights into how emotions manifest in ASL.
3. The paper establishes baseline models for sentiment analysis and emotion classification using state-of-the-art multimodal models. The benchmark results highlight the limitations of current models in integrating visual cues into emotional reasoning and exhibit a bias towards positive emotions.
4. The work has broader implications for multimodal models, suggesting the need for specialized visual encoders trained specifically on non-verbal emotional expression and the development of architectures that prevent text from overwhelming visual information.

### Weaknesses

#### Some Related Works


#### comment

1. The dataset size is relatively small, with only 200 utterances, which may limit its usefulness for training robust machine learning models. This is particularly concerning given the complexity of sign language and the potential for subtle variations in emotional expression. The limited number of samples per emotion category could lead to overfitting and poor generalization, especially for less frequent emotions. Furthermore, the dataset's size may not be sufficient to capture the full range of emotional nuances present in ASL.
2. The paper does not evaluate the performance of the baseline models on multi-label emotion classification tasks, which could pose further challenges for current multimodal models' emotion and video understanding capabilities. The absence of multi-label evaluation leaves a gap in understanding the models' ability to handle complex emotional expressions that may involve multiple emotions simultaneously. This is a significant limitation, as real-world emotional expressions are often nuanced and multi-faceted.
3. The paper does not discuss the potential biases in the dataset or the annotation process. Since the annotators are all Deaf ASL signers with professional interpretation experience, their interpretations of emotions might not be representative of the broader Deaf community. This could introduce biases that affect the performance of models trained on the dataset, particularly if the models are deployed in diverse Deaf communities with varying cultural norms and emotional expressions.

### Suggestions

The authors should consider expanding the dataset to include a larger number of utterances, which would allow for more robust training of machine learning models. This expansion should also aim to balance the representation of different emotions to mitigate potential class imbalance issues. Furthermore, the authors should explore data augmentation techniques to artificially increase the size of the dataset, which could improve the generalization capabilities of the models. Techniques such as temporal jittering, random cropping, and color perturbation could be considered to create additional training samples while preserving the emotional content of the videos. The authors should also investigate the impact of dataset size on model performance by conducting experiments with varying amounts of training data, which would provide insights into the scalability of the proposed approach.

To address the lack of multi-label emotion classification evaluation, the authors should incorporate a multi-label annotation scheme in future iterations of the dataset. This would involve annotating each video clip with multiple emotion labels, reflecting the complexity of real-world emotional expressions. The authors should then evaluate the performance of the baseline models on this multi-label task, using appropriate metrics such as the F1 score or the area under the ROC curve. This would provide a more comprehensive understanding of the models' ability to handle nuanced emotional expressions. Additionally, the authors should consider exploring more advanced models that are specifically designed for multi-label classification, such as those based on attention mechanisms or graph neural networks.

Finally, the authors should address the potential biases in the dataset by including a more diverse group of annotators, representing different backgrounds and experiences within the Deaf community. This would help to ensure that the dataset is more representative of the broader Deaf community and reduce the risk of introducing biases. The authors should also conduct a thorough analysis of the annotation process to identify and mitigate any potential sources of bias. This could involve comparing the annotations of different annotators and analyzing the reasons for any discrepancies. Furthermore, the authors should consider using techniques such as adversarial training to reduce the impact of biases on model performance.

### Questions

1. How do the baseline models perform on multi-label emotion classification tasks, and what are the implications for the dataset's use in more complex emotion recognition scenarios?
2. What are the specific challenges in sign language emotion recognition that the EmoSign dataset aims to address, and how do these challenges differ from those in spoken language emotion recognition?
3. How do the baseline models handle the disentanglement of grammatical and emotional functions of visual cues in sign language, and what are the implications for the development of new architectures?

### Rating

6

### Confidence

4

**********