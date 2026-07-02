### Summary

This paper presents a theoretical analysis of the injectivity of decoder-only transformer language models, proving that these models are almost surely injective, meaning different prompts yield distinct last-token representations. The authors introduce SIFT, an algorithm that leverages this injectivity to efficiently reconstruct exact input prompts from hidden activations. Through mathematical proofs and extensive empirical validation, the paper establishes injectivity as a fundamental property of transformers, with implications for model interpretability, transparency, and safe deployment.

### Soundness

3

### Presentation

3

### Contribution

2

### Strengths

1. The paper provides rigorous mathematical proofs that establish the almost-sure injectivity of decoder-only transformers, a property that holds across initialization and training, which is a novel and significant theoretical contribution.
2. The introduction of SIFT, the first algorithm capable of provably and efficiently reconstructing exact input prompts from hidden states, is a major technical innovation. The algorithm’s linear-time guarantees and practical effectiveness are impressive.
3. The paper is exceptionally well-written, with clear explanations of complex mathematical concepts and a logical flow that makes the theoretical results accessible. The empirical validation is thorough, with extensive experiments on state-of-the-art models.

### Weaknesses

#### Some Related Works


#### comment

1. The paper’s focus on injectivity of the last token's representation might limit its applicability to other aspects of transformer behavior. While the last token’s representation is crucial for next-token prediction, the injectivity of intermediate hidden states or the representations of other tokens within the sequence is not addressed. This raises questions about the broader applicability of the injectivity result, particularly for tasks that rely on analyzing the full sequence of hidden states rather than just the final token representation.
2. The paper does not explore in detail how the injectivity property can be leveraged in practical applications beyond input reconstruction. While the authors demonstrate the use of SIFT for exact input recovery, they do not fully explore other potential applications of this property, such as improving model interpretability, enhancing security, or enabling new types of analysis. The paper would benefit from a more thorough discussion of how this theoretical result can be translated into practical tools and techniques.

### Suggestions

The authors should consider expanding their analysis to include the injectivity of intermediate hidden states, not just the final token representation. This could involve investigating whether the mapping from input sequences to the hidden states at each layer is also injective, or if there are layers where information is lost. Such an analysis would provide a more complete picture of how information flows through the transformer and would broaden the applicability of the injectivity result. For example, if intermediate layers are also injective, it might be possible to develop new methods for analyzing the internal representations of the model, which could lead to a better understanding of its behavior. Furthermore, exploring the conditions under which intermediate representations lose information could provide insights into the limitations of transformers and suggest ways to improve their architecture.

In addition to expanding the theoretical analysis, the authors should also explore more practical applications of the injectivity property. While SIFT is a valuable tool for input reconstruction, the paper could benefit from a discussion of how this property can be used for other tasks. For example, the injectivity property could potentially be used to develop more robust methods for detecting adversarial attacks, as any modification to the input that does not preserve the injectivity would be easily detectable. Another potential application is in model interpretability, where the injectivity property could be used to trace the flow of information through the model and identify the parts of the input that are most important for the final prediction. The authors could also explore the use of injectivity for model compression or pruning, as the property could potentially be used to identify redundant parts of the model that do not contribute to the final representation.

Finally, the authors should consider the limitations of their theoretical results and discuss the conditions under which the injectivity property might not hold. For example, the paper could explore the impact of quantization or other approximation techniques on the injectivity property. It would also be useful to investigate the robustness of the injectivity property to small perturbations in the input or the model parameters. Such an analysis would provide a more complete understanding of the practical implications of the theoretical results and would help to identify the conditions under which the injectivity property can be reliably used. Furthermore, the authors could explore the relationship between injectivity and other properties of transformers, such as their generalization ability or their robustness to adversarial attacks.

### Questions

1. How does the injectivity property extend to non-standard transformer architectures, such as those with modified attention mechanisms or different layer configurations? Are there specific architectural choices that could enhance or undermine injectivity?
2. The paper focuses on the last-token representation for injectivity. How does the injectivity of intermediate hidden states or other tokens within the sequence compare, and could this be relevant for tasks beyond next-token prediction?
3. While the paper proves that collisions are measure-zero events, have you explored any practical scenarios or adversarial conditions where collisions might be more likely to occur, even if theoretically unlikely?

### Rating

6

### Confidence

3

**********