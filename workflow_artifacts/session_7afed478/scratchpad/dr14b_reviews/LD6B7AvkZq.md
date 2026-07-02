### Summary

The paper introduces a novel approach to understanding how language models acquire syntax, focusing on the learning dynamics with respect to the substructure of context-free grammars (CFGs). The authors define subgrammars and prove fundamental results showing that the loss of language modeling obeys recurrences with respect to subgrammars. They empirically demonstrate that small transformers learn subgrammars in parallel, unlike children who acquire language sequentially. The study also explores whether curriculum learning using an inductive bias by pretraining on a subgrammar can improve performance. Finally, the authors reveal that models struggle with deeper recursive structures, highlighting fundamental challenges in how neural networks represent hierarchical syntax.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel approach to understanding how language models acquire syntax by focusing on the substructure of context-free grammars (CFGs). This is a creative and original contribution to the field, offering a new perspective on the learning dynamics of language models.
2. The authors provide a rigorous theoretical framework, including the definition of subgrammars and proofs of fundamental results. This demonstrates a high level of methodological rigor and enhances the credibility of the findings.
3. The empirical experiments provide valuable insights into the learning behaviors of small transformers and the potential benefits of curriculum learning. These findings have practical implications for improving the training of language models.
4. The paper is well-structured and clearly written, making it accessible to a broad audience. The authors effectively communicate their ideas and results, contributing to the overall impact of the work.

### Weaknesses

#### Some Related Works


#### comment

1. The theoretical results in Section 4 rely on strong assumptions, such as the context-insensitivity of the model for its subgrammars. It is unclear to what extent these assumptions hold in practice and how they affect the validity of the results. Specifically, the assumption that the model's behavior on a subgrammar is independent of the context in which it appears within the larger grammar is a significant simplification. This assumption needs more rigorous justification, as it is not immediately clear that a neural network trained on a full grammar would exhibit such context-insensitive behavior at the subgrammar level. The paper should provide a more detailed analysis of the conditions under which this assumption is valid and the potential impact of its violation on the theoretical results.
2. The experiments in Section 5 are conducted on synthetic CFGs with limited complexity. It is unclear whether the findings generalize to more complex grammars and natural languages. The synthetic CFGs used in the experiments appear to be relatively simple, with limited recursion depth and a small number of production rules. This raises concerns about the applicability of the results to more complex, real-world grammars. The paper should provide a more thorough discussion of the limitations of the experimental setup and the potential challenges in generalizing the findings to more complex language structures. Furthermore, the paper should consider experiments on more complex, realistic grammars to validate the findings.
3. The paper does not provide a clear explanation of why the model learns all subgrammars in parallel, which is a surprising and counterintuitive result. The observation that the model learns all subgrammars simultaneously, rather than sequentially, is not well-explained. The paper should provide a more detailed analysis of the underlying mechanisms that lead to this parallel learning behavior. It is important to investigate whether this is a fundamental property of the model architecture or a consequence of the specific training procedure used.
4. The CKA analysis in Section 5.2 is not very informative and does not provide any significant insights. The CKA analysis presented in Section 5.2 does not offer a clear interpretation of the results. The paper should provide a more detailed explanation of what the CKA results signify and how they relate to the overall findings of the paper. It is important to clarify whether the observed changes in CKA scores are meaningful and what they imply about the model's internal representations.
5. The paper does not explore the question of grammar induction, which is an important aspect of language acquisition. The paper focuses on the learning dynamics of language models given a fixed grammar, but it does not address the problem of grammar induction, which is a crucial aspect of language acquisition. The paper should discuss the limitations of not addressing grammar induction and suggest future directions for research in this area.

### Suggestions

The paper would benefit from a more thorough investigation into the context-insensitivity assumption. Specifically, the authors should explore the extent to which the model's behavior on subgrammars is influenced by the surrounding context within the larger grammar. This could involve conducting experiments where the context of subgrammars is systematically varied and analyzing the impact on the model's performance. Furthermore, the authors could investigate whether specific architectural modifications or training techniques could encourage context-insensitivity at the subgrammar level. A more detailed analysis of the conditions under which this assumption holds, and the potential consequences of its violation, would significantly strengthen the theoretical results. It would also be beneficial to explore the use of techniques such as attention visualization to understand how the model attends to different parts of the input sequence when processing subgrammars in different contexts.

To address the limitations of the experimental setup, the authors should consider expanding their experiments to include more complex and realistic CFGs. This could involve using grammars with deeper recursion, a larger number of production rules, and more intricate dependencies between non-terminals. The paper should also discuss the challenges of scaling the experiments to larger models and more complex datasets. Furthermore, the authors could explore the use of techniques such as curriculum learning to facilitate the learning of complex grammars. It would be valuable to investigate how the model's performance scales with the complexity of the grammar and to identify the specific factors that contribute to the difficulty of learning complex language structures. The paper should also consider experiments on grammars that are more representative of natural language, even if they are still synthetic.

Finally, the paper should provide a more detailed analysis of the parallel learning behavior observed in the experiments. This could involve investigating the relationship between the learning rates of different subgrammars and the architecture of the model. The authors should also explore whether this parallel learning behavior is specific to the transformer architecture or whether it is a more general property of neural networks. Furthermore, the paper should discuss the implications of this parallel learning behavior for our understanding of language acquisition. It would be valuable to compare the model's learning behavior to human language acquisition data and to identify the key differences and similarities. The paper should also explore the potential benefits and drawbacks of parallel learning compared to more sequential learning approaches.

### Questions

1. How do the theoretical results in Section 4 relate to the experimental findings in Section 5? Can you provide any theoretical explanations for the observed phenomena, such as the parallel learning of subgrammars?
2. What are the implications of your findings for the development of more effective language models? How can we leverage the insights about subgrammar learning to improve the performance of language models on natural language tasks?
3. Can you provide any insights into the differences between the learning behavior of language models and human language acquisition? Why do children seem to acquire language in a more structured and sequential manner, while language models learn all subgrammars in parallel?
4. How does the depth of recursion affect the learning dynamics of language models? Can you provide any theoretical or empirical analysis of the relationship between recursion depth and model performance?
5. What are the limitations of your approach, and what future directions do you see for this research? What are the most important open questions that remain to be addressed?

### Rating

6

### Confidence

3

**********