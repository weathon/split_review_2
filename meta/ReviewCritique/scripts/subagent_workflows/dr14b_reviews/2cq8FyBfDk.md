### Summary

This paper introduces a new model called ProteinVista, which is a 3D convolutional neural network designed to capture detailed atomic information in protein structures. Unlike traditional protein language models that rely on sequence-based representations, ProteinVista uses full-atom 3D voxel grids to represent protein structures, allowing it to capture fine-grained structural details that are essential for understanding molecular interactions. The model is pre-trained on over 500,000 protein structures from AlphaFold-2 and fine-tuned on specific downstream tasks such as enzyme-substrate classification, transporter-substrate classification, and drug-target inhibition prediction. The authors demonstrate that ProteinVista outperforms sequence-based models like ESM-2 on these tasks, highlighting the importance of 3D structural information for accurately predicting protein function and interactions. Additionally, the paper shows that combining ProteinVista with ESM-2 through ensembling further improves performance, suggesting that sequence and structure-based representations are complementary.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel approach to protein representation learning by using a 3D convolutional neural network (3D CNN) to directly process full-atom voxelized protein structures. This approach captures fine-grained atomic details that are often missed by sequence-based models and protein graph neural networks, providing a more detailed and accurate representation of protein geometry and interactions.
2. The model is pre-trained on a large dataset of over 500,000 protein structures from AlphaFold-2, which is significantly smaller than the datasets used for training large protein language models (PLMs) but still substantial. Despite this smaller pre-training dataset, ProteinVista achieves competitive or superior performance on several downstream tasks compared to PLMs like ESM-2, demonstrating the efficiency and effectiveness of the 3D CNN approach.
3. The paper demonstrates that ProteinVista outperforms sequence-based models on tasks that require detailed structural information, such as enzyme-substrate classification, transporter-substrate classification, and drug-target inhibition prediction. This highlights the importance of 3D structural information for accurately predicting protein function and interactions, especially in cases where precise binding pocket geometry and atomic interactions are critical.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a detailed analysis of the model's performance on proteins with low pLDDT scores, which are often difficult to predict accurately. It is unclear how the model handles low-confidence regions in the predicted structures and whether these regions negatively impact performance. Specifically, the paper lacks an analysis of how the model's performance degrades as pLDDT scores decrease, and whether there is a threshold below which the model's predictions become unreliable. This is crucial because real-world applications often involve proteins with regions of low confidence, and understanding the model's behavior in these scenarios is essential for practical use.
2. The paper lacks a comprehensive comparison with other 3D-based protein representation methods, particularly those that use graph neural networks (GNNs) to model atomic interactions. While the authors compare against sequence-based models, a more thorough comparison with methods that explicitly model 3D structure, such as those using atom-level graphs, is needed to fully contextualize the performance of ProteinVista. The absence of such comparisons makes it difficult to assess the true novelty and effectiveness of the proposed approach relative to existing 3D-aware methods.
3. The paper does not explore the potential of using alternative 3D representations, such as point clouds or surface meshes, which could capture different aspects of protein structure and potentially improve performance. The choice of voxel grids, while intuitive, might not be the most efficient or informative representation for all types of protein structures. Exploring alternative representations could reveal whether the observed performance is specific to voxel grids or a more general property of the 3D CNN architecture.

### Suggestions

To address the lack of analysis on low pLDDT regions, the authors should perform a more granular evaluation of the model's performance across different pLDDT score ranges. This should include not only overall performance metrics but also a detailed analysis of how the model's predictions change as pLDDT scores decrease. For example, the authors could bin the test set into different pLDDT ranges (e.g., 90-100, 80-90, 70-80, etc.) and report performance metrics for each bin. This would reveal the specific pLDDT thresholds where the model's performance starts to degrade significantly. Furthermore, it would be beneficial to analyze the types of errors the model makes in low pLDDT regions, such as misclassification of binding sites or incorrect predictions of interaction partners. This could involve visualizing the predicted interactions and comparing them to the ground truth, focusing specifically on regions with low pLDDT scores. Such an analysis would provide a more complete understanding of the model's limitations and potential areas for improvement.

To better contextualize the performance of ProteinVista, the authors should include a more comprehensive comparison with other 3D-based protein representation methods, especially those that use graph neural networks (GNNs) to model atomic interactions. This comparison should not be limited to sequence-based models but should also include methods that explicitly model 3D structure using atom-level graphs. The authors should select several state-of-the-art GNN-based methods for protein representation and evaluate them on the same downstream tasks as ProteinVista. This would allow for a direct comparison of the performance of different 3D-aware methods and would help to determine whether ProteinVista's voxel-based approach offers any advantages over graph-based approaches. The comparison should include not only overall performance metrics but also an analysis of the computational cost and memory requirements of each method. This would provide a more complete picture of the trade-offs between different 3D-aware representation methods.

Finally, the authors should explore the potential of using alternative 3D representations, such as point clouds or surface meshes, to capture different aspects of protein structure. While voxel grids are a simple and intuitive representation, they may not be the most efficient or informative for all types of protein structures. Point clouds, for example, could offer a more compact representation that is less sensitive to the choice of voxel size. Surface meshes, on the other hand, could capture the overall shape and topology of the protein more effectively. The authors could implement and evaluate these alternative representations using the same 3D CNN architecture as ProteinVista. This would allow them to determine whether the observed performance is specific to voxel grids or a more general property of the 3D CNN architecture. The authors should also analyze the computational cost and memory requirements of each representation to determine which is most suitable for different applications.

### Questions

1. How does the model handle proteins with low pLDDT scores, and what is the impact of low-confidence regions on the model's performance?
2. How does ProteinVista compare to other 3D-based protein representation methods, such as those using graph neural networks on atomic structures?
3. What is the impact of different voxel resolutions on the model's performance, and is there an optimal resolution for capturing detailed structural information?
4. How does the model generalize to proteins with novel folds or low sequence similarity to the training data?
5. What is the computational cost of training and fine-tuning ProteinVista compared to sequence-based models, and how does the model scale to larger protein structures?

### Rating

6

### Confidence

3

**********