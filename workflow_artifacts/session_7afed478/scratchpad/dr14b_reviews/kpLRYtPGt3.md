### Summary

The paper proposes a new finetuning strategy called Neon that is able to improve the generation quality of generative models. The proposed finetuning strategy simply reverses the direction of finetuning of a generative model on its own generated samples. The paper provides a theoretical justification for this strategy and shows that this strategy is effective for several types of generative models, including diffusion models, flow matching models, and autoregressive models.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

The proposed finetuning strategy is very simple and seems to be quite effective for improving the generation quality of a wide range of generative models. The strategy requires no additional data or model, which makes it easy to use in practice. The paper also provides a theoretical justification for the proposed strategy, making it more convincing.

### Weaknesses

#### Some Related Works


#### comment

The paper only evaluates the proposed strategy on several relatively small datasets, such as CIFAR-10 and ImageNet. It would be interesting to see how the proposed strategy works on larger datasets, such as FFHQ-1024 or LAION.

### Suggestions

The paper's evaluation is limited to relatively small datasets, which raises concerns about the generalizability of the proposed finetuning strategy. While the results on CIFAR-10 and ImageNet are promising, these datasets do not fully capture the complexities of real-world image distributions. To strengthen the paper, the authors should evaluate their method on higher-resolution datasets such as FFHQ-1024, which would provide a better understanding of the method's effectiveness on more complex and detailed images. Furthermore, the evaluation should include a more diverse range of image types and styles, potentially by incorporating datasets like LAION, which contains a vast array of images from the internet. This would help to demonstrate the robustness of the proposed method across different image domains and complexities. The absence of such evaluations makes it difficult to assess the practical applicability of the method in real-world scenarios where high-resolution and diverse data are common.

In addition to the dataset size, the paper should also explore the impact of different training configurations on the effectiveness of the proposed finetuning strategy. For example, the authors could investigate how the number of finetuning steps, the learning rate, and the batch size affect the final generation quality. It would be beneficial to provide a more detailed analysis of the sensitivity of the method to these hyperparameters. Furthermore, the paper should explore the impact of the proposed method on different generative model architectures. While the paper demonstrates the effectiveness of the method on diffusion models, flow matching models, and autoregressive models, it would be valuable to investigate its performance on other types of generative models, such as GANs or normalizing flows. This would help to establish the generality of the proposed method and its applicability to a wider range of generative modeling techniques. A more comprehensive evaluation across different models and training configurations would significantly enhance the paper's impact and credibility.

Finally, the paper could benefit from a more in-depth analysis of the theoretical underpinnings of the proposed finetuning strategy. While the paper provides a theoretical justification, it would be helpful to delve deeper into the reasons why reversing the finetuning direction leads to improved generation quality. A more detailed analysis of the loss landscape and the optimization dynamics could provide further insights into the method's effectiveness. For instance, the authors could investigate whether the reversed finetuning direction helps the model escape from local minima or saddle points, or whether it leads to a more robust solution. Furthermore, it would be valuable to explore the relationship between the proposed method and other techniques for improving generative models, such as regularization or adversarial training. A more thorough theoretical analysis would not only enhance the paper's understanding but also provide a solid foundation for future research in this area.

### Questions

1. How does the proposed strategy work for larger and more diverse datasets, such as FFHQ-1024 or LAION?
2. Can the proposed strategy be combined with other techniques for improving generation quality, such as regularization or adversarial training?

### Rating

6

### Confidence

3

**********