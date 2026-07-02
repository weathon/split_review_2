### Summary

This paper presents ScaPre, a novel framework for scalable and precise concept unlearning in text-to-image diffusion models. ScaPre addresses the challenges of conflicting weight updates, imprecise unlearning, and reliance on additional data by introducing a conflict-aware stable design and an Informax Decoupler. The framework achieves efficient closed-form solutions, enabling large-scale unlearning without auxiliary sub-models. Extensive experiments demonstrate that ScaPre outperforms existing methods in both unlearning efficacy and generative quality, setting a new state-of-the-art for large-scale unlearning.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel framework, ScaPre, which addresses the challenges of scalable and precise concept unlearning in text-to-image diffusion models.
2. The method is efficient, requiring no additional data or auxiliary sub-models, and can unlearn up to five times more concepts than the best baseline within acceptable quality limits.
3. The paper is well-organized, with clear explanations of the proposed method and its components.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a detailed analysis of the computational resources required for the proposed method, which could be important for practical applications.
2. The paper could benefit from a more thorough comparison with existing methods, particularly in terms of the trade-offs between unlearning performance and generation quality.

### Suggestions

The paper should include a more detailed analysis of the computational costs associated with the proposed ScaPre method. Specifically, the authors should provide a breakdown of the time and memory requirements for each stage of the unlearning process, such as the conflict-aware stable design and the Informax Decoupler. This analysis should not only include the total time but also the time spent on different operations, such as matrix multiplications, SVD, and other linear algebra routines. Furthermore, the authors should specify the hardware used for the experiments, including the CPU model, GPU model, and memory capacity. This level of detail is crucial for other researchers to reproduce the results and assess the practical applicability of the method. For example, providing a table that shows the time taken for each step of the algorithm for different numbers of concepts to be unlearned would be very helpful. This would allow readers to understand the scalability of the method and its suitability for different use cases.

In addition to computational costs, the paper should provide a more comprehensive comparison with existing unlearning methods. The current comparison is limited and does not fully explore the trade-offs between unlearning performance and generation quality. The authors should include a wider range of baseline methods, including both training-based and closed-form approaches, and evaluate them on the same datasets and metrics. The comparison should not only focus on the overall unlearning performance but also on the quality of the generated images after unlearning. For example, the authors could use metrics such as FID and CLIP score to quantify the generation quality. Furthermore, the authors should analyze the failure cases of the proposed method and compare them with the failure cases of the baseline methods. This would provide a more nuanced understanding of the strengths and weaknesses of the proposed method and its suitability for different scenarios. A more detailed analysis of the trade-offs between unlearning performance and generation quality would greatly enhance the paper's contribution.

Finally, the paper should include a more detailed discussion of the limitations of the proposed method. While the method shows promising results, it is important to acknowledge its limitations and potential areas for future research. For example, the authors could discuss the sensitivity of the method to different hyperparameters, the potential for catastrophic forgetting, and the scalability of the method to a very large number of concepts. The authors should also discuss the potential for adversarial attacks on the unlearning process and how these attacks could be mitigated. A thorough discussion of the limitations would provide a more balanced view of the method and guide future research in this area.

### Questions

1. How does the proposed method handle the unlearning of abstract concepts or styles that are not easily defined by specific keywords or objects?
2. Can the method be extended to unlearn multiple concepts simultaneously, and if so, how does it affect the unlearning performance and generation quality?

### Rating

6

### Confidence

3

**********