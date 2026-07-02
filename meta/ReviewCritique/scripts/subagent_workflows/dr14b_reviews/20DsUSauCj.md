### Summary

This paper presents an automated pipeline to extract persona vectors from natural language trait descriptions. The authors demonstrate that these vectors can be used to monitor and control model behavior both in deployment and during training. They also propose a novel preventative steering method that proactively limits unwanted persona drift during finetuning, and show that finetuning-induced persona shifts can be predicted before finetuning by analyzing training data projections onto persona vectors.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper presents a comprehensive approach to understanding and controlling persona shifts in LLMs, with applications for deployment, training, and pre-training data screening.
2. The authors demonstrate the strong correlation between finetuning shifts along persona vectors and changes in trait expression, providing empirical evidence for their approach.
3. The preventative steering method is shown to effectively limit unwanted persona drift during finetuning while preserving general capabilities, outperforming prompt-based baselines.
4. The ability to predict finetuning-induced persona shifts before training begins opens up possibilities for proactive mitigation strategies.

### Weaknesses

#### Some Related Works


#### comment

1. The paper primarily focuses on three negative traits (evil, sycophancy, and hallucination). It would be useful to see an analysis of how the effectiveness of the proposed approach varies across a wider range of traits, including positive traits and more nuanced personality characteristics.
2. The paper relies heavily on LLM-based evaluation of trait expression. While the authors validate this approach, it would be beneficial to include more human evaluations, especially for traits that are difficult to measure automatically.
3. The preventative steering method is compared to prompt-based baselines, but it would be useful to see comparisons with other training interventions, such as regularization techniques or adversarial training.
4. The paper does not extensively discuss the computational cost of the proposed methods, particularly the preventative steering approach, which could be a concern for large-scale applications.
5. The generalizability of the findings to different model architectures and sizes is not fully explored.
6. The paper acknowledges that the steering methods are less reliable for subtle behavioral changes in deployment settings. It would be useful to explore more robust methods for detecting and mitigating these subtle shifts.

### Suggestions

The paper would benefit from a more thorough investigation into the applicability of the proposed persona vector approach across a broader spectrum of traits. While the focus on negative traits like 'evil,' 'sycophancy,' and 'hallucination' is understandable given their potential for harm, it is crucial to understand how the method performs with more nuanced and positive personality characteristics. For example, traits such as 'empathy,' 'curiosity,' or 'creativity' could provide a more comprehensive evaluation of the method's versatility. Furthermore, it would be valuable to explore how the method handles traits that are not easily defined by a single dimension, such as 'ambiguity tolerance' or 'openness to experience.' This could involve generating persona vectors for these traits and evaluating their effectiveness in controlling model behavior. Such an analysis would provide a more robust understanding of the method's limitations and potential for generalization.

To strengthen the evaluation, the authors should incorporate more human evaluations, particularly for traits that are challenging to assess automatically. While LLM-based evaluations offer scalability, they may not fully capture the nuances of human perception, especially for complex traits like sycophancy. Human evaluations could involve asking annotators to rate the model's responses based on the presence and intensity of specific traits. This would provide a more reliable measure of the method's effectiveness in controlling trait expression. Additionally, it would be beneficial to explore different evaluation metrics that are less susceptible to bias, such as those that focus on the semantic content of the responses rather than just the stylistic choices. This could involve using metrics that measure the degree to which the model's responses align with the intended trait, rather than simply detecting the presence of the trait. Such an approach would provide a more nuanced understanding of the method's performance.

Finally, the paper should include a more comprehensive comparison of the preventative steering method with other training interventions, such as regularization techniques or adversarial training. While the comparison to prompt-based baselines is useful, it does not fully capture the range of available methods for mitigating persona drift. Regularization techniques, such as adding a penalty term to the loss function to discourage deviations from the base model's behavior, could be a relevant comparison point. Similarly, adversarial training, where the model is trained to be robust against perturbations that induce persona drift, could provide a more challenging benchmark. Furthermore, the authors should provide a more detailed analysis of the computational cost of the proposed methods, particularly the preventative steering approach, and compare it to the computational cost of other methods. This would help to assess the practical feasibility of the approach for large-scale applications. Additionally, the authors should explore the generalizability of the findings to different model architectures and sizes, as the effectiveness of the method may vary depending on the underlying model.

### Questions

1. How does the effectiveness of the persona vector approach vary across different types of traits beyond the ones studied in the paper?
2. What is the computational cost of the preventative steering method compared to other training interventions?
3. How well does the approach generalize to different model architectures and sizes beyond the ones tested in the paper?
4. What are the limitations of the steering methods for detecting and mitigating subtle behavioral changes in deployment settings?
5. How does the quality of the generated contrastive prompts impact the effectiveness of the persona vector approach?

### Rating

8

### Confidence

4

**********