### Summary

This paper proposes to learn a three-channel codec to encode the common and task-specific information from the input image for multiple vision tasks. The proposed method is inspired by the Gray-Wyner network in information theory. The authors characterize the bounds of the common information and propose an objective to balance the inherent tradeoffs in learning the representations. The authors conduct experiments on two-task scenarios across six vision benchmarks to evaluate the proposed method.

### Soundness

2

### Presentation

1

### Contribution

2

### Strengths

1. The authors provide theoretical insights on the bounds of the common information and the transmit-receive tradeoff optimization. 
2. The authors evaluate the proposed method on multiple benchmarks and conduct ablation studies on the architecture design.

### Weaknesses

#### Some Related Works


#### comment

1. The motivation for learning the common and task-specific information is not well-explained. The authors should provide a more detailed explanation of the applications of the proposed method. The paper lacks a clear articulation of why separating common and task-specific information is beneficial, especially in practical scenarios. It is unclear how this separation leads to improved performance or efficiency compared to existing methods that do not explicitly enforce this separation. The paper should elaborate on the specific use cases where this approach offers a significant advantage.
2. The paper is poorly written and hard to follow. The authors should improve the clarity of the paper and avoid using too many notations. The excessive use of mathematical notations without clear explanations makes it difficult to grasp the core ideas. The paper would benefit from more intuitive explanations and examples to illustrate the concepts. The lack of clear definitions for some of the notations further complicates the understanding of the proposed method.
3. The authors should provide more details on the architectures of the proposed method in the main paper. Specifically, the interaction between the common and task-specific channels needs to be clarified. The paper does not provide sufficient detail on how the common information is extracted and how it is used by the different task-specific decoders. A more detailed description of the network architecture, including the specific layers and their configurations, is needed to fully understand the proposed method.
4. The performance of the proposed method is limited. The proposed method does not outperform the Joint method in both transmit rate and receive rate. The proposed method achieves worse transmit rate than the Joint method in Fig. 5. The fact that the proposed method does not consistently outperform the Joint method raises questions about its effectiveness. The paper should provide a more thorough analysis of the trade-offs between the proposed method and the Joint method, and explain why the proposed method is still valuable despite its performance limitations.

### Suggestions

The paper needs to clearly articulate the practical benefits of separating common and task-specific information. The authors should provide concrete examples of how this separation can be leveraged in real-world applications. For instance, in a scenario where multiple tasks are performed on the same input, such as in a multi-task learning setting, the common information could be used to reduce redundancy and improve efficiency. The authors could also explore applications in conditional computation, where the common information is used to determine which tasks need to be performed. The paper should also discuss the potential for using the common information for tasks such as image retrieval or indexing, where the common information could serve as a compact representation of the image. The authors should provide a more detailed explanation of how the proposed method can be used in these scenarios and how it compares to existing approaches.

The paper should be significantly improved in terms of clarity and readability. The authors should reduce the use of mathematical notations and provide more intuitive explanations of the concepts. The paper should include more examples and illustrations to help the reader understand the proposed method. The authors should also provide clear definitions for all the notations used in the paper. The paper should be organized in a more logical manner, with a clear flow of ideas. The authors should also consider adding a table of contents and clear section headings to improve the readability of the paper. The paper should also include a glossary of terms to help the reader understand the technical concepts.

The paper should provide a more detailed description of the network architecture, including the specific layers and their configurations. The authors should also provide a clear explanation of how the common information is extracted and how it is used by the different task-specific decoders. The paper should include a diagram of the network architecture to help the reader visualize the proposed method. The authors should also provide a detailed explanation of the training process, including the loss function and the optimization algorithm. The paper should also include an ablation study to evaluate the impact of different components of the proposed method. The authors should also provide a comparison of the proposed method with other existing methods for learning common and task-specific representations.

### Questions

Please refer to the weaknesses. 
Additionally, the authors could consider adding the following references:
1. A theoretical analysis of deep multi-view coding (CVPR 2021)
2. The efficiency of joint coding (IEEE Trans. Inf. Theory, 2021)
3. Conditional image synthesis with auxiliary classifier gans (ECCV 2016) 
4. Multi-task representation learning with adversarial training (AAAI 2018)

### Rating

3

### Confidence

4

**********