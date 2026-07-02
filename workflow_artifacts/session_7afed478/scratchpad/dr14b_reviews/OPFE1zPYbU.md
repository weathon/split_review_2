### Summary

This paper challenges the widely accepted assumption that diffusion models learn the underlying probability distribution of data, particularly in high-dimensional and sparse scenarios. 
The authors argue that the objective function of diffusion models degenerates into predicting a single sample, preventing the model from learning essential statistical quantities of the data distribution. 
Based on this, the paper proposes a new inference framework that unifies existing methods and provides an intuitive, non-statistical perspective on the inference process.

### Soundness

1

### Presentation

1

### Contribution

1

### Strengths

The paper presents an interesting attempt to unify the inference processes of various Diffusion Models (DMs). The visualizations are clear and effectively illustrate the concept.

### Weaknesses

#### Some Related Works


#### comment

 **Weaknesses:**

1.  The paper lacks a clear definition of "sparsity," a term used throughout the text. The author should provide a precise definition of sparsity, preferably in mathematical terms, and explain its relevance to the curse of dimensionality in high-dimensional spaces.

2.  The paper contains several subjective statements that lack rigorous mathematical or experimental support. For instance, the claim that the model cannot learn essential statistical quantities in high-dimensional spaces is presented without sufficient evidence. The authors should either provide a formal mathematical proof or conduct experiments to support this claim. The current analysis relies on an intuitive argument about the posterior distribution, but this needs more rigorous justification.

3.  The paper does not provide any experimental results to validate the claims made about the degradation phenomenon. The authors should design experiments to demonstrate the degradation phenomenon and its impact on the model's ability to learn the true data distribution. This could involve comparing the performance of diffusion models on sparse and dense datasets or analyzing the model's behavior under different levels of sparsity. The lack of empirical validation makes it difficult to assess the practical significance of the proposed framework.

4.  The proposed framework is not validated on any benchmark dataset. The authors should apply their framework to standard benchmark datasets, such as those used in image generation or other relevant tasks, to demonstrate its effectiveness. This would provide a more concrete evaluation of the framework's performance and its potential advantages over existing methods. Without such validation, it is hard to gauge the practical utility of the framework.

5.  The paper's presentation requires significant improvement. The title "Rethinking Diffusion Model in High Dimension" is too broad, given that the analysis primarily focuses on sparse data scenarios rather than high-dimensional spaces in general. The authors should consider a more specific title that accurately reflects the paper's focus. Additionally, the paper suffers from numerous typesetting errors, grammatical mistakes, and unclear notations, which detract from its overall quality. The lack of clarity in notation makes it difficult to follow the mathematical arguments.

6.  The paper lacks a well-structured discussion of its contributions. The authors should clearly articulate the significance of their findings and their impact on the field. This could include a discussion of potential applications, limitations, and directions for future research. The current discussion is too brief and does not fully explore the implications of the proposed framework.

### Suggestions

The paper needs to provide a rigorous definition of sparsity, especially since it is central to the argument. The authors should define sparsity mathematically, perhaps in terms of the number of non-zero elements in a data representation or the distance between data points in a high-dimensional space. They should also explain how this definition relates to the curse of dimensionality, which is a key concept in the paper. Furthermore, the authors should clarify how their definition of sparsity aligns with or differs from existing definitions in the literature. This would provide a solid foundation for the subsequent analysis and make the paper's claims more credible. Without a precise definition, the core argument of the paper remains vague and difficult to evaluate.

The authors should provide more rigorous mathematical or experimental support for their claims. For instance, the assertion that the model cannot learn essential statistical quantities needs to be substantiated with a formal proof or empirical evidence. The authors could analyze the behavior of the posterior distribution in high-dimensional spaces, showing how it concentrates around a single sample and thus prevents the model from learning the true data distribution. This could involve analyzing the variance of the posterior or showing how the model's predictions become increasingly deterministic as the dimensionality increases. Additionally, the authors should conduct experiments to demonstrate the degradation phenomenon, perhaps by comparing the performance of diffusion models on sparse and dense datasets or by analyzing the model's behavior under different levels of sparsity. These experiments should be designed to isolate the effect of sparsity and provide quantitative evidence for the claims made in the paper.

Finally, the paper needs to be validated on benchmark datasets to demonstrate the practical utility of the proposed framework. The authors should apply their framework to standard benchmark datasets, such as those used in image generation or other relevant tasks, and compare its performance to existing methods. This would provide a more concrete evaluation of the framework's effectiveness and its potential advantages. The authors should also provide a more detailed discussion of the limitations of their framework and suggest directions for future research. This would help to contextualize the paper's findings and make it more valuable to the research community. The current lack of empirical validation and discussion makes it difficult to assess the practical significance of the proposed framework.

### Questions

Please refer to Weaknesses.

### Rating

3

### Confidence

4

**********