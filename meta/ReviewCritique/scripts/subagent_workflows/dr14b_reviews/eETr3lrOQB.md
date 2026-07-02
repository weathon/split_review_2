### Summary

The paper introduces VQ-Transplant, a framework that enables the integration of new Vector Quantization (VQ) modules into pre-trained visual tokenizers without the need for costly end-to-end retraining. This approach preserves the encoder-decoder parameters of existing tokenizers, allowing for efficient experimentation with novel quantization techniques. The authors also propose MMD-VQ, a new VQ method that leverages maximum mean discrepancy to align feature and codebook distributions, enhancing compatibility with VQ-Transplant. The framework demonstrates significant reductions in training costs while maintaining high reconstruction fidelity, making it a valuable tool for advancing research in visual tokenization.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The VQ-Transplant framework is a novel approach that addresses the computational challenges associated with training quantization modules for state-of-the-art VQ-based models. By enabling plug-and-play integration of new VQ modules into pre-trained tokenizers, it significantly reduces the need for resource-intensive end-to-end retraining.
2. The introduction of MMD-VQ, a new VQ method, is a significant contribution. By leveraging maximum mean discrepancy to align feature and codebook distributions, MMD-VQ improves compatibility with the VQ-Transplant framework and enhances reconstruction fidelity.
3. The paper provides a comprehensive empirical evaluation of VQ-Transplant, demonstrating its effectiveness across various VQ algorithms and datasets. The results show significant improvements in reconstruction fidelity and training efficiency, validating the framework's practical utility.

### Weaknesses

#### Some Related Works


#### comment

1. The paper primarily focuses on the VAR tokenizer. While the results are promising, it's unclear how well VQ-Transplant generalizes to other types of visual tokenizers. The authors should provide more evidence of its compatibility with different architectures and pre-training strategies. Specifically, the paper lacks a rigorous analysis of how the encoder and decoder architectures within different tokenizers might affect the performance of VQ-Transplant. For example, tokenizers with significantly different encoder/decoder depths or attention mechanisms might exhibit varying degrees of compatibility with the proposed framework. The current evaluation is limited to a single tokenizer family, making it difficult to assess the general applicability of the method.
2. The decoder adaptation strategy, while effective, is relatively simple. The paper could explore more sophisticated adaptation techniques or provide a more in-depth analysis of the decoder's role in the overall performance. The current approach only fine-tunes the decoder for a few epochs, which might not be sufficient to fully adapt the decoder to the new quantized latent space. A more thorough investigation into the decoder's learning dynamics and the impact of different adaptation strategies is needed. For instance, exploring techniques like knowledge distillation or more advanced fine-tuning methods could potentially yield better results.
3. The paper could benefit from a more detailed discussion of the limitations of VQ-Transplant. For example, are there specific types of VQ modules or datasets where the framework might not perform well? The paper does not adequately address potential failure cases or scenarios where the proposed method might not be suitable. For example, it is unclear how the method would perform with VQ modules that have significantly different codebook sizes or quantization strategies. A more comprehensive discussion of these limitations would provide a more balanced view of the method's applicability.

### Suggestions

To address the limited scope of the evaluation, the authors should conduct experiments on a wider range of visual tokenizers, including those with different architectures and pre-training strategies. This would involve testing VQ-Transplant on tokenizers beyond the VAR family, such as those based on transformers or convolutional networks, and those trained on different datasets. The analysis should also include a detailed investigation of how the encoder and decoder architectures of these different tokenizers affect the performance of VQ-Transplant. This could involve varying the depth of the encoder and decoder, the type of attention mechanisms used, and the pre-training objectives. Such an analysis would provide a more comprehensive understanding of the generalizability of the proposed framework and identify potential limitations. Furthermore, the authors should explore the impact of different pre-training datasets on the performance of VQ-Transplant. For example, tokenizers trained on datasets with different characteristics (e.g., image resolution, object diversity) might exhibit varying degrees of compatibility with the framework. A thorough investigation of these factors would provide a more robust assessment of the method's applicability.

Furthermore, the authors should explore more sophisticated decoder adaptation techniques to improve the performance of VQ-Transplant. Instead of simply fine-tuning the decoder for a few epochs, they could investigate methods like knowledge distillation, where the pre-trained decoder is used as a teacher to guide the adaptation of the new decoder. They could also explore more advanced fine-tuning techniques, such as adaptive learning rate schedules or regularization methods, to prevent overfitting and improve the stability of the adaptation process. A detailed analysis of the decoder's learning dynamics, including the evolution of its weights and activations during adaptation, would also provide valuable insights into the effectiveness of different adaptation strategies. This would help to identify the optimal adaptation approach for different types of VQ modules and tokenizers. Additionally, the authors should investigate the impact of different decoder architectures on the adaptation process. For example, decoders with different numbers of layers or attention mechanisms might require different adaptation strategies.

Finally, the authors should provide a more detailed discussion of the limitations of VQ-Transplant, including specific scenarios where the framework might not perform well. This should include an analysis of how the method performs with VQ modules that have significantly different codebook sizes or quantization strategies. The authors should also investigate the impact of the quality of the pre-trained tokenizer on the performance of VQ-Transplant. For example, they could test the method on tokenizers trained with different amounts of data or different pre-training objectives. This would help to identify the boundaries of the method's applicability and provide a more balanced view of its strengths and weaknesses. A thorough discussion of these limitations would also guide future research in this area and help to improve the robustness and generalizability of the proposed framework. The authors should also consider the computational cost of the decoder adaptation process, especially when using more sophisticated techniques, and discuss the trade-offs between performance and computational resources.

### Questions

1. How does the quality of the pre-trained tokenizer affect the performance of VQ-Transplant? Is there a threshold below which the framework's benefits diminish?
2. Can VQ-Transplant be applied to other modalities beyond vision, such as natural language processing or audio processing? If so, what modifications would be necessary?
3. The paper mentions that adversarial training is inherently unstable. How does VQ-Transplant mitigate this instability when integrating new VQ modules that rely on adversarial training?

### Rating

6

### Confidence

4

**********