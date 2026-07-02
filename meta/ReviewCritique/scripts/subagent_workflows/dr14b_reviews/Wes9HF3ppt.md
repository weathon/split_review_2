### Summary

This paper introduces insertion language models (ILMs) that learn to insert tokens at arbitrary positions in a sequence. The authors propose a tailored network parameterization and a simple denoising objective to train ILMs. The authors demonstrate the effectiveness of ILMs on planning tasks and text generation/infilling.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper is well-written and easy to follow.
- The proposed method is novel and interesting. It provides a new perspective on language modeling.
- The authors demonstrate the effectiveness of ILMs on planning tasks and text generation/infilling.

### Weaknesses

#### Some Related Works


#### comment

 - The authors only conduct experiments on small-scale datasets. It would be beneficial to evaluate the proposed method on larger datasets to assess its scalability and generalizability.
- The authors only compare ILMs with ARMs and MDMs. It would be helpful to include comparisons with other relevant baselines to provide a more comprehensive evaluation of the proposed method.
- The authors do not provide a detailed analysis of the computational cost of the proposed method. It would be useful to report the training and inference time of ILMs and compare them with other methods.

### Suggestions

The authors should investigate the performance of their insertion language models (ILMs) on larger datasets to better understand their scalability. While the current experiments provide a proof of concept, the generalizability of the approach remains unclear without evaluation on more substantial datasets. For instance, datasets like the C4 dataset used in training large language models, or the Pile dataset, could provide a more rigorous test of the model's ability to handle diverse and complex language patterns. Furthermore, it would be beneficial to analyze the performance of ILMs across different dataset sizes to identify potential bottlenecks or limitations in their scalability. This analysis should include not only the final performance metrics but also the training dynamics, such as convergence speed and stability, as the dataset size increases. Such an investigation would provide a more complete picture of the practical applicability of ILMs.

In addition to expanding the dataset size, the authors should also consider comparing their ILMs with a wider range of baseline models. While the comparison with autoregressive models (ARMs) and masked diffusion models (MDMs) is valuable, it is important to include other relevant models that are commonly used in sequence generation tasks. For example, comparing ILMs with models based on recurrent neural networks (RNNs) or transformer architectures could provide a more comprehensive understanding of the strengths and weaknesses of the proposed approach. Furthermore, it would be beneficial to compare ILMs with other non-autoregressive models, such as those based on iterative refinement or parallel decoding. This would help to clarify the unique advantages of ILMs compared to other approaches that also deviate from the standard autoregressive paradigm. The comparison should not only focus on final performance metrics but also on other aspects such as training stability, inference speed, and memory usage.

Finally, a more detailed analysis of the computational cost of ILMs is needed. The authors should provide a breakdown of the computational resources required for training and inference, including the number of parameters, FLOPs, and memory usage. This analysis should also compare the computational cost of ILMs with that of other models, such as ARMs and MDMs. Furthermore, it would be beneficial to analyze the computational cost of different components of the ILM architecture, such as the insertion module and the denoising module. This would help to identify potential areas for optimization and improve the efficiency of the proposed approach. The authors should also investigate the impact of different hyperparameters on the computational cost of ILMs, such as the number of layers, the hidden size, and the number of attention heads.

### Questions

Please refer to the weaknesses.

### Rating

6

### Confidence

4

**********