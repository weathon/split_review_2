### Summary

The paper proposes a language confusion gate (LCG) to address the language confusion issue in LLMs. The LCG is a small MLP that predicts the language family of the next token. During inference, the LCG masks tokens that do not belong to the predicted language family. The LCG is trained using self-distillation, where the teacher model is the LLM itself. The LCG is trained to predict the language family of the top-k tokens predicted by the LLM. The paper shows that the LCG reduces language confusion in several LLMs without significantly degrading their performance on downstream tasks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

* The paper addresses an important problem in LLMs, which is language confusion.
* The proposed method is simple and effective.
* The paper provides a thorough analysis of the language confusion problem and the proposed solution.
* The paper evaluates the proposed method on several LLMs and tasks.

### Weaknesses

#### Some Related Works


#### comment

 * The paper does not provide a detailed analysis of the computational overhead of the LCG. It would be helpful to understand the impact of the LCG on the inference speed and memory usage of LLMs.
* The paper does not explore the possibility of using other methods for training the LCG, such as adversarial training or reinforcement learning. It would be interesting to see if these methods could further improve the performance of the LCG.
* The paper does not provide a detailed analysis of the failure cases of the LCG. It would be helpful to understand the types of language confusion that the LCG is unable to handle.

### Suggestions

The paper should include a more thorough analysis of the computational costs associated with the Language Confusion Gate (LCG). Specifically, it is important to quantify the impact of the LCG on inference latency and memory footprint. This analysis should go beyond simply stating that the LCG is lightweight and should provide concrete metrics, such as the percentage increase in inference time per token and the additional memory required for the LCG's parameters and computations. Furthermore, the analysis should consider how these costs scale with the size of the base language model and the length of the generated text. For example, does the overhead of the LCG become more significant for larger models or longer sequences? Providing such a detailed analysis would allow practitioners to make informed decisions about whether to deploy the LCG in resource-constrained environments.

Exploring alternative training methods for the LCG could potentially lead to further performance improvements. While the current approach uses norm-adjusted self-distillation, it would be beneficial to investigate the effectiveness of adversarial training and reinforcement learning. Adversarial training could enhance the robustness of the LCG by training it to handle more challenging language confusion scenarios. For example, the LCG could be trained to distinguish between subtle differences in language usage that might be missed by the current approach. Reinforcement learning could be used to optimize the LCG's performance on specific tasks, such as translation or text summarization. This could be achieved by defining a reward function that encourages the LCG to reduce language confusion while maintaining or improving task performance. The paper should discuss the potential benefits and challenges of these alternative training methods and provide a rationale for the chosen approach.

Finally, a more detailed analysis of the failure cases of the LCG is needed to fully understand its limitations. The paper should provide specific examples of language confusion scenarios that the LCG is unable to handle effectively. For instance, does the LCG struggle with code-switching or the use of mixed-language text? Does it have difficulty with low-resource languages or specific language families? Understanding these failure cases would help to identify areas for future improvement and would provide a more complete picture of the LCG's capabilities. This analysis should also consider the potential impact of the training data on the LCG's performance. For example, if the training data does not include examples of certain types of language confusion, the LCG may not be able to handle them effectively.

### Questions

* How does the LCG affect the inference speed and memory usage of LLMs?
* Have you considered using other methods for training the LCG, such as adversarial training or reinforcement learning?
* What are the limitations of the LCG? Are there any specific types of language confusion that it is unable to handle?

### Rating

6

### Confidence

4

**********