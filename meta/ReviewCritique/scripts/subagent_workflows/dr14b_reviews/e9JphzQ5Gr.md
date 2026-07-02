### Summary

This paper introduces a novel semi-supervised learning (SSL) framework called CaPT, which leverages CLIP as a prior teacher to address the label dependency issue in SSL. The authors identify the inherent limitation of SSL, where the effectiveness of utilizing unlabeled data is heavily dependent on the quantity and quality of labeled data. To mitigate this, CaPT leverages CLIP's zero-shot capabilities as a prior teacher, guiding the training of a unimodal network through co-pseudo labels. The framework employs an asymmetric-modalities co-training approach, combining a fully fine-tuned unimodal network with a parameter-efficiently fine-tuned CLIP model. The authors demonstrate that CaPT achieves state-of-the-art performance across multiple SSL benchmarks, particularly in low-label regimes.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel approach to integrating CLIP into SSL, addressing the label dependency issue by leveraging CLIP's zero-shot capabilities. The asymmetric-modalities co-training framework is a creative solution that combines the strengths of both unimodal and multimodal models.
2. The authors provide a theoretical analysis of the label dependency in SSL, which is a valuable contribution to the understanding of the field. The proposed CaPT framework is rigorously evaluated across multiple benchmarks, demonstrating its effectiveness and robustness. The significant performance gains, especially in low-label regimes, highlight the practical impact of the work.
3. The paper is well-structured and clearly written. The authors effectively communicate their ideas and findings, making the paper accessible to a broad audience. The use of figures and tables is effective in illustrating the concepts and results.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the computational resources required for training CaPT compared to other SSL methods. While the authors mention the efficiency of parameter-tuning CLIP, a quantitative comparison of training time and memory consumption would be valuable. Specifically, the paper should include a breakdown of the computational cost associated with each component of the CaPT framework, such as the unimodal network, the CLIP model, and the co-pseudo labeling process. This would allow for a more direct comparison with existing SSL methods and a better understanding of the trade-offs between performance and computational cost.
2. The paper primarily focuses on classification tasks. It would be interesting to see how CaPT performs on other types of tasks, such as object detection or segmentation. The current evaluation is limited to image classification datasets, and it is unclear how well the proposed approach would generalize to tasks with different output spaces and evaluation metrics. For example, object detection often requires bounding box regression, and segmentation requires pixel-level predictions, which are significantly different from classification.
3. While the paper demonstrates strong performance on several benchmarks, it would be beneficial to include experiments on a wider range of datasets, particularly those with different characteristics (e.g., medical images, satellite imagery). The current evaluation is primarily focused on natural image datasets, and it is not clear how well CaPT would perform on datasets with different statistical properties, such as medical images with subtle features or satellite imagery with complex backgrounds. This would help to establish the generalizability of the approach.

### Suggestions

To address the lack of detailed computational analysis, the authors should include a comprehensive breakdown of the computational cost associated with each component of the CaPT framework. This should include the training time, memory consumption, and the number of parameters for both the unimodal network and the CLIP model. A comparison with other state-of-the-art SSL methods, such as FreeMatch and RegMixMatch, should be provided, detailing the trade-offs between performance and computational resources. Furthermore, the authors should explore the scalability of CaPT by evaluating its performance on larger datasets and with different batch sizes. This would provide a more complete picture of the computational requirements of the method and its suitability for different applications. The authors should also consider providing guidelines for selecting appropriate hyperparameter values based on the computational resources available.

To broaden the applicability of CaPT, the authors should evaluate its performance on tasks beyond image classification, such as object detection and segmentation. This would involve adapting the framework to handle different output spaces and evaluation metrics. For object detection, the authors could explore how the co-pseudo labeling process can be extended to include bounding box regression. For segmentation, the authors could investigate how the framework can be modified to produce pixel-level predictions. The authors should also consider using datasets that are commonly used in these tasks, such as COCO for object detection and Cityscapes for segmentation. This would allow for a more direct comparison with existing methods in these domains. Furthermore, the authors should discuss the challenges and limitations of applying CaPT to these more complex tasks.

To further establish the generalizability of CaPT, the authors should include experiments on a wider range of datasets with different characteristics. This should include datasets from domains such as medical imaging, satellite imagery, and remote sensing. For example, the authors could evaluate the performance of CaPT on medical image datasets such as Camelyon17 for pathology and UCI for dermatology. They could also explore the performance of CaPT on remote sensing datasets such as EuroSAT for image classification and NWPU-RESISC45 for land-cover classification. This would help to demonstrate the robustness of the method to different types of data and its ability to generalize to real-world applications. The authors should also discuss the challenges and limitations of applying CaPT to these diverse datasets and provide insights into how the method can be further improved.

### Questions

1. Could the authors provide more details on the computational resources required for training CaPT compared to other SSL methods? How does the training time and memory consumption scale with the size of the dataset and the complexity of the model?
2. How sensitive is CaPT to the choice of hyperparameters, and what is the process for selecting optimal values? Could the authors provide guidelines or recommendations for practitioners who want to apply CaPT to their own problems?
3. The paper primarily focuses on classification tasks. How do the authors envision adapting CaPT to other types of tasks, such as object detection or segmentation? Are there any specific challenges or limitations that need to be addressed?
4. The paper demonstrates strong performance on several benchmarks. However, it would be interesting to see how CaPT performs on a wider range of datasets, particularly those with different characteristics (e.g., medical images, satellite imagery). Are there any plans to evaluate CaPT on such datasets?

### Rating

6

### Confidence

3

**********