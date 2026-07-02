### Summary

This paper introduces a novel framework for PPI candidate ranking, aiming to prioritize interactions for experimental testing. The approach leverages domain knowledge through interpretability-guided ranking and further refines prioritization by integrating complementary sources of evidence, including interaction scores, structural plausibility, and biomedical language features. Evaluations on a large-scale dataset constructed from successive STRING releases demonstrate that the approach yields significant improvements over two state-of-the-art PPI prediction models, providing more accurate and biologically coherent rankings.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel problem formulation, PPI candidate ranking, which is crucial for guiding experimental testing and accelerating the discovery of new protein-protein interactions.
2. The proposed framework is innovative, combining interpretability-guided ranking with a re-ranking strategy that integrates diverse biological signals.
3. The evaluations are conducted on a large-scale dataset from STRING database releases, demonstrating the practical applicability and scalability of the approach.
4. The paper is well-organized, with clear problem formulation, methodology, and experimental setup. The results are presented with comprehensive metrics and visualizations.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of the proposed approach, particularly regarding its dependence on the availability of known interactions and the potential biases in the STRING database.
2. The computational cost of the re-ranking process, especially the structure-based methods, is not thoroughly discussed. This could be a significant factor for researchers with limited computational resources.

### Suggestions

The authors should provide a more in-depth analysis of the limitations inherent in their approach, specifically addressing the reliance on existing interaction data. While leveraging known interactions is a reasonable starting point, the method's performance on proteins with sparse or no prior interaction data needs to be rigorously evaluated. The authors should explore alternative strategies to mitigate this limitation, such as incorporating protein features that are independent of interaction data, or by using a pre-training strategy on a larger, more diverse set of proteins before fine-tuning on known interactions. Furthermore, a more detailed analysis of the performance of the method on proteins with varying degrees of interaction coverage would be beneficial to understand the extent of this bias. This analysis should include a discussion of the potential impact of these limitations on the generalizability of the method to novel proteins or less well-studied organisms.

Regarding the computational cost, the authors should provide a more detailed breakdown of the time and memory requirements for each step of the pipeline, especially the structure-based docking using SpeedPPI. While the authors mention that SpeedPPI is an accelerated pipeline, the actual computational cost can still be significant, particularly when dealing with large-scale protein datasets. It would be helpful to provide a more detailed analysis of the computational scaling of the method with respect to the number of proteins and the length of the sequences. This analysis should include the time required for each step, such as embedding generation, contact map prediction, and docking, as well as the memory requirements for storing intermediate results. This information is crucial for researchers to assess the feasibility of using the method on their own datasets. The authors should also discuss potential strategies for reducing the computational cost, such as using more efficient docking algorithms or implementing parallel processing techniques.

Finally, the authors should consider a more rigorous validation of the predicted interactions. While the authors use a hold-out set from the STRING database, this approach is limited by the fact that the test set may still contain biases present in the training set. A more robust validation would involve using an independent dataset of experimentally validated interactions that were not included in the STRING database. This would provide a more objective assessment of the method's ability to predict novel interactions. Additionally, the authors should consider performing a more detailed analysis of the types of interactions that are predicted by their method, to understand if there are any biases towards specific types of interactions or protein domains.

### Questions

1. How does the method perform on proteins with very few or no known interactions? Is there a minimum number of known interactions required for the method to be effective?
2. What are the computational requirements for applying the re-ranking strategies, especially the structure-based methods? How does the computational cost scale with the size of the protein dataset?
3. Have the authors considered evaluating their method on other interaction databases besides STRING to ensure robustness?

### Rating

8

### Confidence

3

**********