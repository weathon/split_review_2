### Summary

This paper proposes a novel in-context watermarking (ICW) method for large language models (LLMs). Unlike traditional watermarking methods that require access to the model's decoding process, ICW embeds watermarks solely through prompt engineering. The authors introduce four ICW strategies, each with a tailored detection method, and evaluate their effectiveness in both direct text stamping and indirect prompt injection settings. The experiments demonstrate the feasibility of ICW as a model-agnostic approach, with promising performance in detection accuracy, robustness, and text quality. The authors also discuss the limitations of current ICW methods and highlight future research directions.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel approach to watermarking LLMs using in-context learning, which does not require access to the model's decoding process.
2. The authors propose four distinct ICW strategies, each with a tailored detection method, and evaluate them in both direct text stamping and indirect prompt injection settings.
3. The experiments demonstrate the effectiveness of ICW on powerful LLMs, showing promising performance in detection accuracy, robustness, and text quality.
4. The authors acknowledge the limitations of current ICW methods and highlight future research directions, such as improving watermarking instructions and treating ICW as a new alignment task.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a detailed analysis of the computational overhead of the proposed ICW methods. It would be beneficial to understand the time and memory requirements for both embedding and detecting watermarks, especially when dealing with large-scale text generation tasks. A comparison with existing watermarking methods in terms of computational efficiency would also be valuable.
2. The evaluation of ICW methods is limited to a few specific scenarios. It would be beneficial to evaluate the performance of ICW methods in a wider range of applications, such as code generation, creative writing, and question answering. This would provide a more comprehensive understanding of the generalizability of the proposed approach. Furthermore, the robustness of the watermarks against adversarial attacks, such as paraphrasing or synonym substitution, should be more thoroughly investigated.
3. The paper does not discuss the potential for ICW methods to be used for malicious purposes, such as embedding hidden messages or tracking user behavior without their consent. It is important to consider the ethical implications of this technology and propose safeguards to prevent its misuse. The authors should also discuss the potential for adversarial attacks that could remove or alter the watermarks.

### Suggestions

The paper introduces an interesting approach to watermarking LLMs, but several aspects could be strengthened. First, a more detailed analysis of the computational cost is needed. The authors should provide a breakdown of the time and memory requirements for both embedding and detecting the watermarks, including how these scale with the length of the input text and the complexity of the watermark. This analysis should also compare the computational overhead of ICW with existing watermarking methods, such as those that modify the model's parameters or the decoding process. Furthermore, the authors should investigate the impact of different watermark strengths on computational cost and detection accuracy, providing a trade-off analysis that would be useful for practitioners.

Second, the evaluation of the proposed ICW methods should be expanded to include a wider range of applications and more robust adversarial attacks. The current evaluation focuses on a limited set of scenarios, and it is unclear how well the ICW methods would perform in other contexts, such as code generation or creative writing. The authors should also evaluate the robustness of the watermarks against more sophisticated adversarial attacks, such as paraphrasing, synonym substitution, and adversarial rephrasing. This would provide a more comprehensive understanding of the limitations of the proposed approach and identify areas for improvement. For example, the authors could explore the use of semantic-preserving transformations to test the robustness of the watermarks.

Finally, the paper should address the potential ethical implications of ICW methods. The authors should discuss the potential for misuse, such as embedding hidden messages or tracking user behavior without their consent. They should also propose safeguards to prevent such misuse, such as developing methods for detecting and removing watermarks or limiting the use of ICW to authorized parties. The authors should also consider the potential for adversarial attacks that could remove or alter the watermarks, and discuss how these attacks could be mitigated. A thorough discussion of these ethical considerations is crucial for the responsible development and deployment of this technology.

### Questions

1. How does the performance of ICW methods vary across different LLMs with varying capabilities?
2. What are the potential limitations of ICW methods in terms of scalability and applicability to real-world scenarios?
3. How can ICW methods be made more robust against adversarial attacks and attempts to remove or alter the watermarks?

### Rating

6

### Confidence

4

**********