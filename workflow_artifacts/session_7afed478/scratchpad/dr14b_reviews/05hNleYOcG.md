### Summary

This paper proposes a multi-turn attack framework, PLAGUE, which consists of a Planner, Primer, and Finisher module to generate multi-turn attacks. The Planner module generates a plan for the attack, the Primer module builds an adversarial context, and the Finisher module generates the final response. The authors evaluate PLAGUE on several models and show that it outperforms existing methods.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The proposed PLAGUE framework is novel and effective in generating multi-turn attacks.
2. The authors evaluate PLAGUE on multiple models and show that it outperforms existing methods.
3. The paper is well-written and easy to understand.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of the proposed approach and potential future research directions. For example, the authors could discuss the potential for adversarial training to defend against multi-turn attacks or the development of more robust evaluation metrics for multi-turn attacks. Specifically, the paper lacks a discussion on how the framework might be vulnerable to defenses that detect and mitigate adversarial inputs at each turn, rather than just at the final response. Furthermore, the evaluation could be strengthened by considering metrics that assess the semantic coherence and naturalness of the generated attack sequences, beyond just the success rate of the final attack.
2. The paper could provide more details on the implementation of the proposed approach, such as the specific algorithms used for the Planner, Primer, and Finisher modules. For example, the authors could provide pseudocode or flowcharts to illustrate the algorithms. The current description lacks sufficient detail to allow for reproducibility or a deep understanding of the framework's inner workings. For instance, the paper does not specify how the Planner module determines the optimal sequence of adversarial prompts, or how the Primer module ensures the generated context is both adversarial and coherent.

### Suggestions

The paper would benefit from a more thorough discussion of potential defense mechanisms against the proposed multi-turn attack framework. Specifically, the authors should consider defenses that operate at each turn of the dialogue, rather than just at the final response. This could include techniques such as adversarial training, where the model is trained on both benign and adversarial examples, or input sanitization methods that attempt to remove or neutralize adversarial content. Furthermore, the authors should explore the potential for using anomaly detection techniques to identify unusual patterns of interaction that might indicate an ongoing attack. A detailed analysis of these potential defenses would provide a more complete picture of the framework's strengths and weaknesses, and would help to guide future research in this area. The discussion should also consider the computational cost and practical feasibility of these defenses, as well as their potential impact on the usability of the system.

To improve the clarity and reproducibility of the proposed approach, the authors should provide more detailed information about the implementation of the Planner, Primer, and Finisher modules. This could include pseudocode or flowcharts that illustrate the algorithms used by each module, as well as a detailed description of the data structures and parameters involved. For example, the paper should specify how the Planner module selects the sequence of adversarial prompts, including the criteria used to evaluate the effectiveness of different plans. The authors should also describe how the Primer module ensures that the generated context is both adversarial and coherent, and how it maintains the context across multiple turns. Furthermore, the paper should provide details on the specific language models used for each module, as well as any fine-tuning or customization that was performed. This level of detail would allow other researchers to reproduce the results and build upon the proposed framework.

Finally, the evaluation of the proposed framework could be strengthened by considering a wider range of metrics beyond just the success rate of the final attack. For example, the authors could consider metrics that assess the semantic coherence and naturalness of the generated attack sequences, as well as the diversity of the attacks. This could include metrics such as perplexity, BLEU score, or other measures of text similarity. Furthermore, the authors should consider evaluating the framework on a wider range of models and datasets, to ensure that the results are generalizable. The evaluation should also include a comparison with other multi-turn attack methods, to demonstrate the superiority of the proposed framework. A more comprehensive evaluation would provide a more robust assessment of the framework's effectiveness and its potential impact.

### Questions

1. How does the proposed approach compare to other multi-turn attack methods in terms of computational efficiency and scalability?
2. What are the potential ethical implications of using the proposed approach for generating multi-turn attacks?

### Rating

6

### Confidence

3

**********