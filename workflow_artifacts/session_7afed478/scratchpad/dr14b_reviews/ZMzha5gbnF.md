### Summary

This paper investigates the safety vulnerabilities of masked diffusion language models (MDLMs), particularly focusing on a phenomenon termed "priming vulnerability." The authors demonstrate that if an affirmative token for a harmful query appears at an intermediate step of the denoising process, it can steer the model toward generating a harmful response. To address this, they propose a novel safety alignment method called Recovery Alignment (RA), which trains models to recover from contaminated intermediate states and generate safe responses. The experiments show that RA effectively mitigates the priming vulnerability while maintaining task performance.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel concept, the "priming vulnerability," which highlights a previously underexplored security risk in MDLMs. This contribution is significant as it advances the understanding of safety issues in MDLMs and sets the stage for future research in this area.
2. The proposed Recovery Alignment (RA) method is a practical and effective solution tailored to the unique characteristics of MDLMs. By training models to recover from contaminated intermediate states, RA addresses the priming vulnerability directly and offers a promising approach for enhancing MDLM safety.
3. The paper is well-structured and clearly written, making the complex concepts accessible to readers. The authors provide thorough explanations of the priming vulnerability and the RA method, supported by illustrative diagrams and examples.

### Weaknesses

#### Some Related Works


#### comment

1. The paper primarily focuses on the priming vulnerability within MDLMs, but it could benefit from a broader discussion of how these findings relate to the security of LLMs in general. This would help situate the work within the larger context of LLM security research and highlight its broader implications.
2. The experiments mainly evaluate the effectiveness of RA in mitigating the priming vulnerability and enhancing robustness against jailbreak attacks. However, the paper could be strengthened by including more comprehensive evaluations of the model's performance across a wider range of downstream tasks and real-world applications. This would provide a more holistic view of the impact of RA on the model's overall utility and robustness.

### Suggestions

The paper's focus on the priming vulnerability in Masked Diffusion Language Models (MDLMs) is a valuable contribution, but it would be beneficial to expand the discussion to encompass the broader landscape of Large Language Model (LLM) security. Specifically, the authors should consider how the identified vulnerability might manifest in other types of LLMs, such as autoregressive models, even if the underlying mechanisms differ. A comparative analysis of the priming vulnerability in MDLMs versus other LLMs would provide a more comprehensive understanding of the security challenges across different model architectures. This could involve exploring whether similar 'affirmative token' phenomena exist in other models, or if the vulnerability is unique to the iterative denoising process of MDLMs. Furthermore, the authors should discuss the potential for adversarial attacks that exploit the priming vulnerability in conjunction with other known vulnerabilities, such as prompt injection or data poisoning, to demonstrate the broader implications of their findings for the security of LLMs in general. This would help to contextualize the significance of the work and highlight the need for robust security measures across various LLM paradigms.

To strengthen the experimental evaluation, the authors should include a more diverse set of downstream tasks that go beyond the current focus on jailbreak attacks and general capability benchmarks. For example, evaluating the model's performance on tasks that require complex reasoning, such as commonsense reasoning or logical inference, would provide a more comprehensive assessment of the impact of Recovery Alignment (RA) on the model's overall utility. Additionally, the authors should consider evaluating the model's robustness against more sophisticated adversarial attacks that are specifically designed to exploit the priming vulnerability. This could involve crafting adversarial prompts that strategically introduce affirmative tokens at different stages of the denoising process to test the limits of the RA method. Furthermore, the evaluation should include a more detailed analysis of the trade-offs between safety and performance, as it is possible that the RA method may introduce some performance degradation on certain tasks. A thorough analysis of these trade-offs would provide a more nuanced understanding of the practical implications of the proposed method.

Finally, the paper would benefit from a more detailed discussion of the limitations of the proposed RA method and potential avenues for future research. For instance, the authors should explore the computational cost of training with RA and whether it scales effectively to larger models and datasets. It would also be valuable to investigate the sensitivity of RA to different hyperparameters and training configurations. Furthermore, the authors should discuss the potential for adversarial attacks that specifically target the recovery mechanism of RA, as it is possible that an attacker could craft inputs that bypass the recovery process. Addressing these limitations and exploring potential future research directions would further enhance the impact and significance of the work. This could include exploring alternative recovery mechanisms or combining RA with other security techniques to achieve more robust protection against a wider range of attacks.

### Questions

1. Could the authors elaborate on how the priming vulnerability might manifest in other types of LLMs, such as autoregressive models, and whether similar vulnerabilities have been observed?
2. How does the proposed Recovery Alignment (RA) method compare to other existing safety alignment techniques in terms of effectiveness and computational efficiency? Are there scenarios where RA might be less effective?

### Rating

6

### Confidence

3

**********