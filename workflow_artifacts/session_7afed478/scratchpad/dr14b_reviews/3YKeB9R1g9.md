### Summary

This paper studies the collapse phenomenon of training loss curves (TLCs) across different model sizes. The authors find that TLCs collapse when the AdamW timescale $\tau$, the tokens-per-parameter ratio (TPP), and the learning-rate schedule are fixed. Based on this finding, the authors introduce Celerity, a model family trained with optimal $\tau$ scaling and demonstrating TLC collapse. The paper also proposes a simple functional form for normalized TLCs, enabling early stopping in large-scale hyperparameter tuning. The authors validate their findings on a GPT2-like LLM and release the Celerity models.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The finding that TLCs collapse under specific conditions (fixed $\tau$, TPP, and learning-rate schedule) is interesting and provides valuable insights into the training dynamics of large language models.
3. The introduction of Celerity, a model family trained with optimal $\tau$ scaling and demonstrating TLC collapse, is a significant contribution. The Celerity models are shown to be compute-efficient and achieve state-of-the-art performance on several downstream tasks.
4. The proposed method for early stopping in large-scale hyperparameter tuning based on the predictability of normalized TLCs is a practical and valuable contribution.

### Weaknesses

#### Some Related Works


#### comment

1. The paper primarily focuses on a specific type of model (GPT2-like LLMs) and a specific training setup (e.g., using SlimPajama dataset). It is unclear how well the findings generalize to other types of models (e.g., encoder-decoder models) and other training setups (e.g., different datasets, optimizers, and hardware). The authors should provide more evidence to support the generalizability of their findings. For instance, the observed collapse phenomenon might be sensitive to the specific architecture of GPT2-like models, and it is not clear if the same would hold for models with different architectural choices, such as those employing linear attention mechanisms or different normalization layers. Furthermore, the SlimPajama dataset, while diverse, might not fully represent the complexities of other datasets, and the collapse behavior could be different when training on datasets with different statistical properties or domain-specific characteristics. The paper lacks a thorough investigation into these aspects.
2. While the paper provides some theoretical insights into the collapse phenomenon, a more in-depth theoretical analysis would be beneficial to better understand the underlying mechanisms. The current explanation relies on the AdamW timescale, tokens-per-parameter ratio, and learning-rate schedule, but it does not delve into the fundamental reasons why these factors lead to the observed collapse. A more rigorous theoretical framework could potentially reveal the connection between these factors and the loss landscape, and provide a deeper understanding of the training dynamics. For example, it would be beneficial to explore if the collapse is related to the properties of the loss function, such as its curvature or the presence of saddle points, and how these properties interact with the chosen training parameters.

### Suggestions

To strengthen the paper, the authors should conduct a more comprehensive evaluation of their findings across a wider range of models and training setups. Specifically, they should investigate the collapse phenomenon in encoder-decoder models, which have different architectural characteristics than the GPT2-like models used in the study. This would involve training models like T5 or BART with similar scaling strategies and observing if the TLCs exhibit the same collapse behavior. Additionally, the authors should explore the impact of different datasets, including those with varying sizes, domain specificities, and statistical properties. For example, training on datasets like C4 or the Pile could provide insights into the generalizability of the collapse phenomenon. Furthermore, the authors should experiment with different optimizers, such as Adam or Lion, and different hardware setups to assess the robustness of their findings. This would help to determine if the observed collapse is specific to the AdamW optimizer and the hardware used in the study, or if it is a more general phenomenon.

In addition to empirical validation, the authors should also delve deeper into the theoretical underpinnings of the collapse phenomenon. This could involve analyzing the loss landscape and its properties, such as the curvature and the presence of saddle points, and how these properties interact with the chosen training parameters. A more rigorous theoretical framework could potentially reveal the connection between the AdamW timescale, tokens-per-parameter ratio, learning-rate schedule, and the loss landscape. For example, the authors could explore if the collapse is related to the convergence of the model to a specific region of the loss landscape, or if it is a result of the interplay between the optimization dynamics and the model's capacity. This theoretical analysis could also provide insights into the optimal choice of training parameters and how to achieve the best performance for different model sizes and datasets. The authors could also investigate the role of regularization techniques, such as weight decay and dropout, in the collapse phenomenon.

Finally, the authors should provide a more detailed analysis of the practical implications of their findings. While the paper demonstrates the potential of using TLC collapse for early stopping in hyperparameter tuning, it would be beneficial to explore other potential applications. For example, the authors could investigate if the collapse phenomenon can be used to diagnose training issues or to guide the selection of model architectures. Furthermore, the authors should discuss the limitations of their approach and identify areas for future research. This could include exploring the impact of different learning rate schedules, batch sizes, and other training hyperparameters on the collapse phenomenon. By providing a more comprehensive analysis of the practical implications and limitations of their findings, the authors can further enhance the impact of their work.

### Questions

1. How does the collapse phenomenon relate to other scaling laws observed in large language models? Can the authors provide a theoretical explanation for the observed collapse phenomenon?
2. How sensitive is the collapse phenomenon to the choice of hyperparameters, such as the learning rate, batch size, and regularization strength? The authors should provide more details on the hyperparameter tuning process and how it affects the collapse phenomenon.
3. Can the authors provide more details on the computational cost of training the Celerity models and how it compares to other state-of-the-art models?

### Rating

6

### Confidence

3

**********