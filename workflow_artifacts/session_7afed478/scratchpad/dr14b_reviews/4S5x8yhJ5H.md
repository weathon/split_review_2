### Summary

The paper introduces a new video and image dataset for evaluating face recognition algorithms. The dataset includes 2,250 high-quality facial images and 1,550 short videos, including both selfie recordings and sequences that explicitly mimic eKYC workflows. The dataset was collected from 50 diverse subjects, ensuring coverage and balance of demographic attributes, including gender, race, and age.

### Soundness

3

### Presentation

3

### Contribution

2

### Strengths

1. The dataset includes a balanced distribution across demographic attributes, including gender, race, and age.
2. The dataset includes both image and video modalities, which is important for evaluating face recognition algorithms under various conditions.

### Weaknesses

#### Some Related Works


#### comment

1. The scale of the proposed dataset is relatively small compared to existing datasets, such as the SOTERIA dataset, which includes 70 identities and over 80,000 images. The limited number of identities (50) restricts the generalizability of models trained on this dataset, as it may not adequately represent the diversity of real-world facial variations. This is a significant limitation, especially when compared to larger datasets that allow for more robust training and evaluation.
2. The paper does not provide a detailed analysis of the dataset's characteristics, such as the distribution of head poses, lighting conditions, and image quality. Without a thorough quantitative analysis of these factors, it is difficult to assess the dataset's suitability for evaluating face recognition algorithms under various conditions. For example, the lack of information on the range of head pose variations makes it unclear how well the dataset can be used to evaluate algorithms' performance under different viewing angles. Similarly, the absence of a detailed analysis of lighting conditions makes it difficult to assess the dataset's robustness to variations in illumination.
3. The paper does not compare the proposed dataset with existing datasets in terms of their characteristics and performance on various face recognition algorithms. A comparative analysis is crucial to understand the unique contributions of the proposed dataset and its advantages over existing resources. Without such a comparison, it is difficult to determine whether the dataset offers any novel challenges or benefits for evaluating face recognition algorithms.

### Suggestions

The authors should significantly expand the dataset to include a larger number of identities. This would enhance the generalizability of models trained on the dataset and allow for more robust evaluation of face recognition algorithms. The current size of 50 identities is insufficient to capture the diversity of real-world facial variations, and a larger dataset would be more representative of the population. Furthermore, the authors should consider incorporating more challenging variations within each identity, such as different facial expressions, occlusions, and aging effects. This would make the dataset more comprehensive and suitable for evaluating the robustness of face recognition algorithms under various conditions. The inclusion of more diverse data would also help to mitigate potential biases in the algorithms.

To address the lack of detailed analysis, the authors should provide a comprehensive quantitative analysis of the dataset's characteristics. This should include a detailed breakdown of the distribution of head poses, lighting conditions, image quality, and other relevant factors. For example, the authors could use metrics such as the angle of rotation, the intensity of illumination, and the sharpness of the images to quantify these characteristics. This analysis should be presented in a clear and concise manner, with appropriate visualizations to aid in understanding. Furthermore, the authors should also provide a detailed description of the data collection process, including the specific equipment used, the environmental conditions, and the instructions given to the subjects. This would allow other researchers to reproduce the dataset and understand its limitations.

Finally, the authors should conduct a thorough comparative analysis of the proposed dataset with existing datasets. This analysis should include a comparison of the dataset's characteristics, such as the number of identities, the distribution of demographic attributes, and the range of variations. The authors should also compare the performance of various face recognition algorithms on the proposed dataset with their performance on existing datasets. This would help to identify the unique contributions of the proposed dataset and its advantages over existing resources. The authors should also discuss the limitations of the proposed dataset in comparison to existing datasets, and suggest potential directions for future research. This comparative analysis would provide a more comprehensive understanding of the dataset's value and its potential impact on the field of face recognition.

### Questions

1. How does the proposed dataset compare to existing datasets in terms of the number of identities, the distribution of demographic attributes, and the range of variations?
2. What are the specific advantages of the proposed dataset over existing datasets for evaluating face recognition algorithms?
3. How do various face recognition algorithms perform on the proposed dataset compared to their performance on existing datasets?

### Rating

5

### Confidence

5

**********