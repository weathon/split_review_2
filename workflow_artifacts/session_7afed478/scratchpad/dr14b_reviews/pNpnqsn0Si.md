### Summary

The paper introduces Thoughtbubbles, a transformer model variant that performs parallel adaptive computation in latent space by learning to dynamically allocate residual streams. This approach allows tokens requiring more computation to form "bubbles" of cloned residuals, enabling additional processing without explicit chain-of-thought tokens. Thoughtbubbles outperforms standard decoder LMs and non-adaptive parallel computation methods across various perplexity metrics and zero-shot evaluations, demonstrating the potential of unsupervised adaptive computation from pretraining.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. Thoughtbubbles introduces a novel mechanism for adaptive computation in transformers, enabling dynamic allocation of residual streams during pretraining without explicit supervision.
2. The model demonstrates superior performance in perplexity metrics and zero-shot evaluations compared to standard and computation-matched baselines.
3. The approach is interpretable, with the model allocating more computation to regions of higher uncertainty, which aligns with recent findings on the importance of high-entropy tokens.

### Weaknesses

#### Some Related Works


#### comment

1. The current implementation of Thoughtbubbles has lower wall-clock efficiency compared to computation-matched baselines, which may limit its practical applicability in resource-constrained environments. The paper does not provide a detailed analysis of the computational overhead introduced by the dynamic forking mechanism, such as the cost of calculating and applying the cumulative scores, and how this overhead scales with model size and input sequence length. This lack of detailed profiling makes it difficult to assess the true efficiency bottleneck.
2. The top-k selection for residual stream management can lead to a gradient bottleneck, potentially hindering the performance of models with deep forking. The paper does not explore alternative selection mechanisms or provide a thorough analysis of the impact of different top-k values on the model's performance and training dynamics. This raises concerns about the robustness of the method to different hyperparameter settings.
3. The model's performance on downstream reasoning tasks is not fully explored due to hardware limitations, leaving questions about its scalability to more complex tasks. The evaluation is limited to perplexity and zero-shot evaluations, which do not fully capture the model's ability to perform complex reasoning. The paper lacks experiments on more challenging reasoning benchmarks, such as those requiring multi-step inference or symbolic manipulation.

### Suggestions

To address the wall-clock efficiency concerns, the authors should provide a more detailed breakdown of the computational costs associated with Thoughtbubbles. This should include a profiling of the time spent on different operations, such as calculating the cumulative scores, performing the forking operation, and executing the attention mechanism. The analysis should also explore how these costs scale with model size and input sequence length. Furthermore, the authors should investigate hardware-aware optimizations, such as custom kernels for the forking and gathering operations, to improve the practical efficiency of the method. This could involve exploring the use of specialized hardware, such as TPUs or FPGAs, to accelerate these operations. A comparison with optimized baselines, such as models using FlashAttention, would also be beneficial to provide a more accurate assessment of the method's efficiency.

To mitigate the potential gradient bottleneck caused by the top-k selection, the authors should explore alternative selection mechanisms, such as softmax-based sampling or Gumbel-Softmax, which can provide a smoother gradient signal. The paper should also include a thorough analysis of the impact of different top-k values on the model's performance and training dynamics. This analysis should investigate how the choice of k affects the diversity of the residual streams and the stability of the training process. Additionally, the authors could consider incorporating techniques such as residual connections or skip connections to improve the flow of gradients through the network. A comparison of different selection mechanisms and their impact on model performance would provide valuable insights into the robustness of the method.

To better evaluate the model's reasoning capabilities, the authors should conduct experiments on more challenging reasoning benchmarks, such as those requiring multi-step inference or symbolic manipulation. This could include datasets such as the ARC challenge or the MATH dataset. The evaluation should also include a more detailed analysis of the model's performance on different types of reasoning tasks, such as logical reasoning, arithmetic reasoning, and common-sense reasoning. Furthermore, the authors should explore the use of techniques such as chain-of-thought prompting to improve the model's reasoning abilities. A more comprehensive evaluation of the model's reasoning capabilities would provide a more complete picture of its strengths and limitations.

### Questions

1. How does the wall-clock efficiency of Thoughtbubbles compare to standard transformers in real-world applications, and what optimizations could be implemented to improve this?
2. Could alternative mechanisms to top-k selection be explored to mitigate the potential gradient bottleneck in deep forking scenarios?
3. How does the model perform on more complex downstream reasoning tasks, and what hardware or methodological improvements would enable a more thorough evaluation?

### Rating

6

### Confidence

3

**********