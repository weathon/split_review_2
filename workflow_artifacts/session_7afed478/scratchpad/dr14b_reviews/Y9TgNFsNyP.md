### Summary

This paper introduces a novel unlearning framework specifically designed for Forward-Forward (FF) models. It leverages a goodness-guided strategy to effectively remove the influence of specific training data without full retraining. The proposed method, FF-Erase, employs a goodness-based membership inference attack (G-MIA) for robust verification of unlearning performance. Experimental results demonstrate that FF-Erase efficiently removes the influence of target forgetting data on FF models while preserving model utility on the remaining data, achieving faster unlearning compared to retraining from scratch.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel unlearning framework specifically designed for Forward-Forward (FF) models, addressing a previously unexplored problem in this domain.

2. The proposed FF-Erase method leverages a goodness-guided strategy, which is a unique and effective approach for unlearning in FF models.

3. The introduction of a goodness-based membership inference attack (G-MIA) provides a robust and practical verification method for unlearning performance.

4. The experimental results demonstrate the efficiency and effectiveness of FF-Erase, showing significant speedups compared to retraining from scratch while preserving model utility.

### Weaknesses

#### Some Related Works


#### comment

1. The paper primarily focuses on the Forward-Forward algorithm. It would be interesting to explore whether the proposed techniques could be adapted to other biologically plausible learning methods beyond FF models. Specifically, the reliance on goodness scores, which are central to the Forward-Forward algorithm, might limit the applicability of this approach to other learning paradigms that do not explicitly compute or utilize such scores. The paper does not discuss how the core ideas of FF-Erase, such as the goodness-guided strategy, could be translated to methods that rely on different mechanisms for learning and representation.

2. The paper could benefit from a more detailed discussion of the limitations of the proposed approach. For example, how does the performance of FF-Erase vary with different types of forgetting data or different model architectures? The paper lacks a thorough analysis of the sensitivity of FF-Erase to the characteristics of the data being unlearned. For instance, does the method perform equally well when unlearning data that is highly similar to the remaining training data, or does it struggle with outliers or noisy examples? Furthermore, the paper does not explore how the effectiveness of FF-Erase might be affected by the depth or complexity of the FF model being used. It is unclear if the method scales well to larger, more complex models, or if its performance degrades with increasing model size.

3. The choice of hyperparameters, such as the learning rate and the number of unlearning epochs, seems crucial to the performance of FF-Erase. The paper could provide more guidance on how to select these parameters in practice. The paper does not provide a clear methodology for selecting these hyperparameters, which could significantly impact the performance of the unlearning process. The lack of a systematic approach to hyperparameter tuning makes it difficult to reproduce the results and apply the method in different settings. It would be beneficial to include a discussion on how these parameters should be chosen based on the specific characteristics of the model and the data.

### Suggestions

The paper should explore the potential for adapting the core ideas of FF-Erase to other biologically plausible learning methods. While the current implementation is specific to the Forward-Forward algorithm, the underlying principles of goodness-guided unlearning could be relevant to other learning paradigms. For example, the paper could investigate how the concept of 'goodness' could be redefined or approximated in other models that do not explicitly compute goodness scores. This could involve exploring alternative measures of data influence or model sensitivity that could be used to guide the unlearning process. Furthermore, the paper should discuss the challenges and potential solutions for adapting FF-Erase to models with different architectures or learning mechanisms. This would broaden the impact of the work and make it more relevant to a wider range of research areas.

To address the limitations of the proposed approach, the paper should include a more detailed analysis of the sensitivity of FF-Erase to different types of forgetting data and model architectures. This could involve conducting experiments with various types of data, such as outliers, noisy examples, and data that is highly similar to the remaining training data. The paper should also explore how the performance of FF-Erase varies with different model architectures, such as deeper or more complex FF models. This analysis should include a discussion of the potential limitations of the method and the conditions under which it might not perform well. Furthermore, the paper should provide guidelines for selecting appropriate hyperparameters for FF-Erase, such as the learning rate and the number of unlearning epochs. This could involve conducting a sensitivity analysis to determine how these parameters affect the performance of the unlearning process. The paper should also provide recommendations for choosing these parameters based on the specific characteristics of the model and the data.

Finally, the paper should provide a more detailed explanation of the goodness-based membership inference attack (G-MIA) and its advantages over existing methods. The paper should discuss the specific properties of the goodness scores that make them suitable for membership inference attacks. It should also provide a comparison of G-MIA with other membership inference attacks, highlighting its strengths and weaknesses. This would help to clarify the contribution of the proposed verification method and its potential impact on the field of machine unlearning. The paper should also discuss the computational cost of G-MIA and its scalability to larger models and datasets.

### Questions

1. Could the authors provide more insights into the computational cost of FF-Erase compared to retraining from scratch? Are there any specific optimizations or techniques used to achieve faster unlearning?

2. How does the performance of FF-Erase vary with different types of forgetting data? Are there any specific scenarios where FF-Erase might struggle or be less effective?

3. Can the authors elaborate on the potential for extending FF-Erase to handle more complex unlearning scenarios, such as unlearning a large portion of the training data or unlearning data that is highly similar to the remaining data?

### Rating

6

### Confidence

4

**********