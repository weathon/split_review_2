### Summary

This paper introduces a method to augment the training data of LLMs by reformulating the existing data into diverse, contextually-rich variations. The method is called Massive Genre Audience (MGA) reformulation. The paper shows that the method is effective in improving the performance of LLMs on various benchmarks, especially in data-constrained scenarios. The paper also analyzes the role of diversity and consistency in the reformulation process, and how they affect the learning process and the validation loss of the models. The paper claims that the MGA method provides a reliable pathway to overcome the data repetition bottleneck and enable more efficient scaling of LLMs.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper proposes a novel and principled framework for corpus reformulation, called MGA, that can generate diverse and contextually-rich variations of the existing data. The framework consists of two stages: adaptive genre-audience pair generation and controlled reformulation. The paper shows that the MGA method can expand the original corpus by 3.9x while maintaining high quality and diversity.
2. The paper conducts extensive experiments to validate the effectiveness of the MGA method in improving the performance of LLMs on various benchmarks, especially in data-constrained scenarios. The paper shows that the MGA method outperforms the baselines of data repetition and upsampling, and that the performance gap widens with increasing model size and data budget. The paper also analyzes the role of diversity and consistency in the reformulation process, and how they affect the learning process and the validation loss of the models. The paper reveals that a balanced approach of limited consistency yields the best reformulation quality and subsequent model performance, and that the MGA method can benefit the model's learning process by prioritizing generalizable patterns over memorizing specific sequence dependencies.
3. The paper is well-written and organized, with clear figures and tables. The paper provides sufficient details and references for the implementation and evaluation of the MGA method. The paper also discusses the limitations and future directions of the work.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a clear definition of the term "genre-audience pairs", which is a key concept in the MGA framework. The paper only gives some examples of genres and audiences, but does not explain how they are defined, selected, or combined. The paper also does not explain how the genre-audience pairs are related to the source text, and whether they are based on the content, style, or purpose of the text. A more rigorous definition of the genre-audience pairs would help the reader understand the logic and motivation behind the MGA framework, and how it differs from other data augmentation methods. For example, it is unclear if the genre is based on the type of document (e.g., news article, scientific paper), or the intended use (e.g., summary, analysis). Similarly, the audience could refer to the demographic group (e.g., teenagers, experts) or the level of expertise (e.g., novice, advanced). Without a clear definition, it is difficult to assess the validity and generalizability of the proposed method.
2. The paper does not provide a clear explanation of the "Limited Consistency" principle, which is the central principle of the MGA framework. The paper only states that the principle seeks to balance stylistic diversity with factual fidelity, but does not explain how this balance is achieved, measured, or controlled. The paper also does not explain what are the criteria or metrics for determining the optimal level of consistency, and how they vary across different types of data and tasks. A more detailed explanation of the "Limited Consistency" principle would help the reader understand the trade-offs and challenges involved in the reformulation process, and how the MGA framework addresses them. For instance, how is the factual fidelity assessed? Is it based on some form of semantic similarity or logical consistency check? How is the stylistic diversity quantified? Is it based on some measure of textual variation or entropy? Without a clear explanation of these aspects, it is difficult to evaluate the effectiveness and robustness of the proposed method.

### Suggestions

The paper should provide a formal definition of genre-audience pairs, clarifying the specific criteria used to define both genres and audiences. For example, the paper could specify that genres are defined based on the communicative purpose of the text (e.g., to inform, to persuade, to entertain), and that audiences are defined based on their level of expertise and background knowledge. The paper should also explain how these pairs are generated from the source text, and whether this process is manual or automated. Furthermore, the paper should provide a detailed analysis of the relationship between the source text and the generated genre-audience pairs, including examples of how different pairs lead to different reformulations. This analysis should also discuss the potential limitations of the current approach, such as the possibility of generating pairs that are not relevant or useful for the source text. A more rigorous definition and analysis of genre-audience pairs would significantly enhance the clarity and credibility of the proposed method.

To address the lack of clarity regarding the "Limited Consistency" principle, the paper should provide a more detailed explanation of how this principle is implemented and controlled. Specifically, the paper should define the metrics used to measure both stylistic diversity and factual fidelity. For example, the paper could use metrics such as perplexity or BLEU score to measure stylistic diversity, and metrics such as semantic similarity or logical consistency checks to measure factual fidelity. The paper should also explain how these metrics are used to determine the optimal level of consistency, and how this level varies across different types of data and tasks. Furthermore, the paper should provide a detailed analysis of the trade-offs involved in balancing stylistic diversity and factual fidelity, and how the MGA framework addresses these trade-offs. This analysis should include examples of how different levels of consistency affect the quality and diversity of the reformulated data, and how these effects impact the performance of the trained models. A more detailed explanation of the "Limited Consistency" principle would significantly enhance the understanding and reproducibility of the proposed method.

Finally, the paper should include a more thorough discussion of the limitations of the MGA framework, including potential biases introduced by the genre-audience pairs and the challenges of ensuring factual fidelity in complex reformulations. The paper should also discuss the computational cost of the MGA method, and how it compares to other data augmentation techniques. Furthermore, the paper should provide a more detailed analysis of the generalizability of the MGA method to different types of data and tasks, and discuss the potential challenges of applying the method to new domains. This discussion should also include a comparison of the MGA method with other data augmentation techniques, highlighting the advantages and disadvantages of each approach. A more thorough discussion of the limitations and generalizability of the MGA method would significantly enhance the practical value and impact of the paper.

### Questions

1. Can you provide a clear definition of the term "genre-audience pairs", and explain how they are related to the source text?
2. Can you provide a clear explanation of the "Limited Consistency" principle, and how it is implemented and controlled in the MGA framework?
3. Can you provide more details on the implementation and evaluation of the MGA framework, such as the choice of the tool SLMs, the prompts, the filtering criteria, and the hyperparameters?

### Rating

6

### Confidence

4

**********