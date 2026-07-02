### Summary

This paper studies the relationship between activation steering and influence functions. The authors prove that, to the first order, these techniques are equivalent: any steering vector can be represented as an influence weighting over training data and vice versa. This duality yields a constructive algorithm for mapping undesired behaviors back to causal training examples, an optimal-control perspective on steering that reveals its regularization properties, and generalization bounds for low-rank steering interventions.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper is well-written and easy to follow.
- The theoretical results are solid and interesting.
- The experiments are solid and convincing.

### Weaknesses

#### Some Related Works


#### comment

 - The experiments are only conducted on GPT-2. It would be better to include more experiments on other models, such as Llama-3.

### Suggestions

The paper's theoretical contributions are strong, but the empirical validation could be significantly strengthened by expanding the experimental scope. While GPT-2 is a reasonable starting point, its architecture and training regime are not representative of all modern language models. Specifically, the paper should include experiments on models with different architectural designs, such as those employing different attention mechanisms or normalization techniques. Furthermore, the scale of the models tested should be increased. Testing on larger models, such as Llama-3, would provide a more robust evaluation of the proposed methods and their scalability. This would also help to determine if the observed equivalences between activation steering and influence functions hold across a wider range of model sizes and complexities. The current experiments, while solid, are limited in their ability to generalize to the broader landscape of language models.

In addition to expanding the model scope, the paper should also consider a more diverse set of tasks and datasets. The current experiments focus on a single task, which limits the generalizability of the findings. Testing on a variety of tasks, such as text classification, question answering, and summarization, would provide a more comprehensive evaluation of the proposed methods. Furthermore, the paper should consider using datasets that are more challenging and diverse, which would help to identify potential limitations of the proposed methods. For example, datasets with more complex linguistic structures or those that require more reasoning abilities could reveal potential weaknesses in the current approach. This would also help to determine if the observed equivalences between activation steering and influence functions are robust to different types of data.

Finally, the paper should provide more details on the implementation of the proposed methods. While the theoretical framework is well-defined, the practical implementation details are not fully described. This makes it difficult for other researchers to reproduce the results and build upon the proposed methods. The paper should include a detailed description of the algorithms used, the hyperparameter settings, and the computational resources required. Furthermore, the paper should provide a clear explanation of how the influence functions are computed and how the steering vectors are derived. This would make the paper more accessible and allow for a more thorough evaluation of the proposed methods.

### Questions

See weaknesses.

### Rating

8

### Confidence

3

**********