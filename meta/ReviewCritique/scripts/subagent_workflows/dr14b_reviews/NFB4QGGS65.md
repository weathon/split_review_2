### Summary

This paper provides a novel geometric interpretation of GPTQ, showing that it is equivalent to Babai’s nearest plane algorithm for solving the closest vector problem (CVP) on a specific lattice. This new perspective offers an intuitive geometric understanding of GPTQ’s error propagation step and allows the authors to derive a tight error bound for GPTQ under the assumption of no weight clipping. Leveraging this theoretical insight, the authors propose new post-training quantization methods that avoid weight clipping, achieving better accuracy than the original GPTQ. Additionally, they develop efficient GPU inference kernels for the resulting representations, further enhancing the practical value of their approach.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper establishes a novel connection between GPTQ and Babai’s nearest plane algorithm, providing a deeper understanding of GPTQ’s inner workings.
2. The authors derive a tight error bound for GPTQ under the no-clipping assumption, which is a valuable theoretical contribution.
3. The proposed no-clipping quantization methods outperform the original GPTQ in terms of accuracy, demonstrating the practical benefits of the theoretical insights.
4. The development of efficient GPU inference kernels for the proposed representations makes the approach more practical for real-world deployment.

### Weaknesses

#### Some Related Works


#### comment

1. The theoretical analysis relies on the assumption of no weight clipping, which may not always be feasible in practice, especially for very low bitwidths. The practical implications of this assumption, particularly concerning the behavior of the algorithm when clipping is unavoidable, are not fully explored. It's unclear how the derived error bounds would be affected by the introduction of clipping, and whether the proposed methods would still offer a significant advantage over existing clipping-based quantization techniques in such scenarios.
2. The paper primarily focuses on linear layers and does not extend the analysis to other types of layers commonly found in large language models, such as attention layers. The absence of a discussion on how the proposed methods could be adapted to handle the unique challenges posed by attention mechanisms, such as the quadratic complexity of the attention matrix, limits the applicability of the work to a broader range of models. Furthermore, the paper does not address the quantization of other non-linear activation functions, which are also crucial components of modern neural networks.
3. The experimental evaluation is limited to a specific set of models and datasets. More extensive experiments on a wider range of models and tasks would strengthen the empirical validation of the proposed methods. The evaluation lacks a thorough exploration of the performance of the proposed methods across different model architectures and sizes, and it does not include a comparison with other state-of-the-art quantization techniques, making it difficult to assess the true practical impact of the proposed approach.

### Suggestions

The paper makes a significant contribution by establishing a connection between GPTQ and Babai's nearest plane algorithm, providing a novel geometric interpretation of the quantization process. However, to enhance the practical impact of this work, it is crucial to address the limitations imposed by the no-clipping assumption. Future work should investigate the behavior of the proposed methods when clipping is necessary, perhaps by developing adaptive clipping strategies that minimize the impact on the derived error bounds. Furthermore, a more detailed analysis of the trade-offs between accuracy and computational efficiency when using no-clipping methods compared to traditional clipping-based approaches would be beneficial. This could involve exploring different bit-widths and analyzing the resulting performance degradation under various clipping scenarios. Such an analysis would provide a more comprehensive understanding of the practical applicability of the proposed methods in real-world scenarios.

To broaden the scope of the work, it is essential to extend the analysis to other types of layers commonly found in large language models, particularly attention layers. This would involve adapting the geometric framework to handle the unique characteristics of attention mechanisms, such as the quadratic complexity of the attention matrix. One possible approach could be to explore the use of block-wise quantization techniques, where the attention matrix is divided into smaller blocks that can be quantized independently. Additionally, the paper should address the quantization of non-linear activation functions, which are also crucial components of modern neural networks. This could involve investigating the use of techniques such as piecewise linear approximations or other non-linear quantization methods. By extending the analysis to these other layer types, the practical applicability of the proposed methods would be significantly increased.

Finally, the experimental evaluation should be expanded to include a wider range of models and datasets. This would involve testing the proposed methods on different model architectures and sizes, as well as on a more diverse set of tasks. Furthermore, a more thorough comparison with other state-of-the-art quantization techniques is needed to assess the true practical impact of the proposed approach. This could involve comparing the proposed methods with other one-shot quantization techniques, as well as with more advanced quantization methods that use iterative optimization. The evaluation should also include a detailed analysis of the computational efficiency of the proposed methods, including the memory footprint and the inference speed. By addressing these points, the paper would provide a more comprehensive and convincing evaluation of the proposed methods.

### Questions

1. How sensitive is the performance of the proposed methods to the choice of quantization parameters, such as the scale and zero-point?
2. Can the geometric interpretation of GPTQ be extended to other quantization algorithms, such as AdaQuant or QuIP?
3. How does the performance of the proposed methods compare to other state-of-the-art quantization techniques, such as AdaQuant or FlexRound, on a wider range of models and tasks?
4. What are the computational overheads of the proposed no-clipping quantization methods compared to the original GPTQ?
5. Can the theoretical error bound derived in the paper be used to guide the selection of quantization parameters in practice?

### Rating

6

### Confidence

3

**********