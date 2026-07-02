### Summary

The paper presents a novel method for fine-tuning quantized neural networks using zeroth-order optimization. The key idea is to perturb the continuous quantization scale to estimate gradients, rather than perturbing the discrete weights directly. This approach allows for memory-efficient fine-tuning of large language models (LLMs) on resource-constrained hardware. The authors also propose a directional derivative clipping method to stabilize training. The method is evaluated on various LLMs and NLP tasks, demonstrating significant memory savings compared to existing methods while maintaining competitive performance.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

* The paper addresses an important problem in the field of efficient deep learning, namely the memory bottleneck in fine-tuning large models.
* The proposed method is novel and well-motivated. The idea of perturbing the quantization scale is intuitive and elegant.
* The paper provides a theoretical justification for the directional derivative clipping method, showing that it reduces the variance of gradient estimates.
* The experimental results are comprehensive and convincing. The method achieves significant memory savings compared to existing methods while maintaining competitive performance on various tasks.
* The paper is well-written and easy to follow. The authors provide clear explanations of the proposed method and its implementation details.

### Weaknesses

#### Some Related Works


#### comment

 * The paper does not provide a detailed analysis of the computational overhead of the proposed method compared to existing approaches. While memory savings are significant, the computational cost is also an important factor to consider.
* The paper focuses primarily on NLP tasks. It would be interesting to see how the method performs on other domains, such as computer vision or speech recognition.
* The paper does not explore the sensitivity of the method to different hyperparameters, such as the perturbation scale and the clipping threshold. A more thorough ablation study would be helpful to understand the robustness of the method.

### Suggestions

The paper would benefit from a more detailed analysis of the computational overhead associated with the proposed method. While the memory savings are substantial, the computational cost of perturbing the quantization scale and estimating gradients using zeroth-order optimization needs to be thoroughly examined. Specifically, the authors should provide a breakdown of the FLOPs required for each step of the algorithm, including the forward and backward passes, and compare these to the computational cost of standard gradient-based fine-tuning methods. It would also be useful to analyze the impact of the perturbation scale on the computational cost, as larger perturbations may require more forward passes to obtain accurate gradient estimates. Furthermore, the authors should investigate the potential for optimizing the implementation of the zeroth-order gradient estimation to reduce the computational overhead. For example, techniques such as gradient compression or quantization could be explored to further improve the efficiency of the method. A detailed analysis of the computational cost would provide a more complete picture of the trade-offs between memory savings and computational efficiency.

To broaden the applicability of the proposed method, the authors should evaluate its performance on a wider range of tasks beyond NLP. While the results on NLP tasks are promising, it is important to assess the method's effectiveness in other domains, such as computer vision and speech recognition. For example, the authors could evaluate the method on image classification tasks using standard benchmark datasets like ImageNet, or on speech recognition tasks using datasets like LibriSpeech. This would help to determine the generalizability of the method and identify any potential limitations. Furthermore, the authors should investigate the impact of different quantization schemes on the performance of the method in these domains. For example, it would be interesting to see how the method performs with different bit-widths and quantization techniques. Evaluating the method on a diverse set of tasks would provide a more comprehensive understanding of its strengths and weaknesses.

Finally, a more thorough ablation study is needed to understand the sensitivity of the method to different hyperparameters. The authors should systematically vary the perturbation scale and the clipping threshold and analyze their impact on the performance of the method. This would help to identify the optimal hyperparameter settings and understand the robustness of the method to different parameter choices. For example, the authors could plot the performance of the method as a function of the perturbation scale and the clipping threshold, and analyze the trends. Furthermore, the authors should investigate the impact of these hyperparameters on the stability of the training process. It would be useful to analyze the variance of the gradient estimates and the convergence behavior of the method for different hyperparameter settings. A more detailed ablation study would provide valuable insights into the behavior of the method and help to improve its practical applicability.

### Questions

* How does the computational cost of QZO compare to existing methods? Can you provide a detailed analysis of the FLOPs required for each step of the algorithm?
* Have you considered applying QZO to other domains beyond NLP, such as computer vision or speech recognition? How do you expect the method to perform in these domains?
* How sensitive is the method to the choice of hyperparameters, such as the perturbation scale and the clipping threshold? Have you conducted any ablation studies to analyze the impact of these parameters on the performance of the method?

### Rating

6

### Confidence

4

**********