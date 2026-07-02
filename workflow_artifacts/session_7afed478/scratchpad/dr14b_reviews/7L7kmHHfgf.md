### Summary

This paper proposes PIRN, a prototype-based reconstruction framework for few-shot multi-modal anomaly detection. The key contributions include the balanced prototype assignment module, the adaptive prototype refinement module, and the multi-modal normality communication module. The experiments show the effectiveness of the proposed method.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The proposed method is reasonable and effective.
3. The experimental results demonstrate the effectiveness of the proposed method.

### Weaknesses

#### Some Related Works


#### comment

1. The authors should provide more details about the training process of PIRN, such as the loss function and optimization algorithm. Specifically, the exact form of the loss function, including any weighting factors or regularization terms, should be specified. Furthermore, the optimization algorithm should be detailed, including the learning rate schedule, batch size, and any specific libraries or frameworks used.
2. The authors should provide more details about the datasets used in the experiments, such as the number of samples, the resolution of the images, and the types of anomalies present. It would be beneficial to include a more detailed breakdown of the anomaly types, perhaps with examples, to better understand the challenges posed by each dataset. Additionally, the specific preprocessing steps applied to the data should be described.
3. The authors should provide more details about the evaluation metrics used in the experiments, such as the definition of each metric and how it is calculated. For instance, for metrics like AUROC, AUROC_P, and AUPRO, the specific implementation details, such as how the anomaly scores are generated and compared to the ground truth, should be clarified. It is also important to specify whether the metrics are calculated on a pixel-wise or image-wise basis.

### Suggestions

The paper would benefit from a more detailed explanation of the training process. Specifically, the authors should provide the exact mathematical formulation of the loss function used to train PIRN. This should include all terms, their weights, and any regularization techniques applied. Furthermore, the optimization algorithm should be described in detail, including the specific optimizer used (e.g., Adam, SGD), the initial learning rate, the learning rate schedule (e.g., step decay, cosine annealing), the batch size, and the number of training epochs. It would also be helpful to specify the hardware and software environment used for training, including the GPU model, the deep learning framework (e.g., PyTorch, TensorFlow), and the specific libraries used for implementation. This level of detail is crucial for reproducibility and allows other researchers to understand the training process fully.

To enhance the experimental section, the authors should provide a more comprehensive description of the datasets used. For each dataset, the authors should specify the number of training and testing samples, the resolution of the images, and the types of anomalies present. A detailed breakdown of the anomaly types, perhaps with visual examples, would be beneficial to understand the challenges posed by each dataset. Additionally, the authors should describe any preprocessing steps applied to the data, such as normalization, resizing, or data augmentation. This information is essential for understanding the experimental setup and for comparing the results with other methods. Furthermore, the authors should clarify how the data is split into training and testing sets, including the number of samples used for each split.

Finally, the authors should provide a more detailed explanation of the evaluation metrics used in the experiments. For each metric, the authors should provide the mathematical definition and explain how it is calculated. For example, for AUROC, AUROC_P, and AUPRO, the authors should clarify how the anomaly scores are generated and compared to the ground truth. It is also important to specify whether the metrics are calculated on a pixel-wise or image-wise basis. The authors should also explain the rationale behind choosing these specific metrics and discuss their limitations. This level of detail is crucial for understanding the experimental results and for comparing the performance of PIRN with other methods.

### Questions

Please refer to the weaknesses.

### Rating

6

### Confidence

3

**********