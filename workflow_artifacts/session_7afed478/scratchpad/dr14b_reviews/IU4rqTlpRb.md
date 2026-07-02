### Summary

This paper investigates the phenomenon of benign relearning in machine unlearning, where models unintentionally recover forgotten information after fine-tuning on seemingly benign data. The authors challenge the prevailing view that topical relevance is the primary driver of relearning, demonstrating instead that syntactic similarity between the relearn and target datasets plays a more significant role. They show that syntactically similar data, even without topical overlap, can trigger the recovery of forgotten content. To mitigate this issue, the authors propose a method called syntactic diversification, which paraphrases the forget set into diverse syntactic structures before unlearning. This approach effectively suppresses benign relearning, accelerates the forgetting process, and improves the trade-off between unlearning efficacy and model utility. The paper's findings highlight the importance of considering syntactic factors in unlearning and offer a practical solution to enhance the robustness of unlearning methods.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper presents a novel perspective on the drivers of benign relearning, shifting the focus from topical relevance to syntactic similarity. This insight is valuable for understanding the mechanisms behind unlearning failures.
2. The authors provide a thorough analysis of the relationship between syntactic similarity and relearning, using various metrics and visualizations to support their claims.
3. The proposed syntactic diversification method is a practical and effective solution to mitigate benign relearning. The experiments demonstrate its benefits in terms of both unlearning efficacy and model utility.
4. The paper is well-structured and clearly written, making it accessible to a broad audience. The figures and tables are informative and effectively support the narrative.

### Weaknesses

#### Some Related Works


#### comment

1. The experiments primarily focus on the TOFU dataset, which has a specific structure. It is unclear how well the findings generalize to other datasets with different characteristics. The authors should consider expanding their evaluation to include a wider range of datasets to strengthen the robustness of their conclusions. Specifically, the TOFU dataset's synthetic nature and its reliance on a limited set of syntactic templates might not fully capture the complexities of real-world data, potentially limiting the generalizability of the observed syntactic similarity effects. The dataset's structure, with its consistent question-answer pairs, might artificially inflate the impact of syntactic similarity, making it difficult to assess the method's effectiveness on more diverse and less structured datasets.
2. The paper could benefit from a more detailed discussion of the limitations of the proposed method. For instance, how does syntactic diversification perform when the syntactic structures of the forget set are inherently diverse? Are there any scenarios where this method might fail or be less effective? The method's reliance on paraphrasing to achieve syntactic diversity might be less effective when the initial forget set already exhibits a high degree of syntactic variation. In such cases, the paraphrasing process might not introduce sufficient diversity to prevent relearning. Furthermore, the computational cost of generating diverse paraphrases, especially for large datasets, could be a limiting factor in practical applications. The paper should also explore the potential for adversarial attacks that could circumvent the diversification strategy.
3. While the paper demonstrates the effectiveness of syntactic diversification, it would be valuable to explore how this method compares to other potential solutions for mitigating benign relearning. Are there alternative approaches that could complement or outperform syntactic diversification? The paper should consider comparing the proposed method against other unlearning techniques, such as gradient-based methods or methods that focus on modifying the model's internal representations. A comparative analysis would provide a more comprehensive understanding of the strengths and weaknesses of syntactic diversification relative to existing approaches. It would also be beneficial to explore whether combining syntactic diversification with other techniques could lead to further improvements in unlearning performance.

### Suggestions

To address the limitations regarding dataset diversity, the authors should expand their evaluation to include datasets with varying degrees of syntactic complexity and topical diversity. This could involve using datasets derived from real-world sources, such as social media posts, news articles, or customer reviews, which often exhibit a wider range of syntactic structures and semantic content. Additionally, the authors could consider using datasets that are specifically designed to test the robustness of unlearning methods, such as those that include adversarial examples or datasets with varying levels of noise. By evaluating the proposed method on a more diverse set of datasets, the authors can provide a more comprehensive assessment of its generalizability and robustness. This would also help to identify potential limitations and areas for improvement.

To further investigate the limitations of syntactic diversification, the authors should conduct experiments on forget sets with varying degrees of initial syntactic diversity. This would help to determine the effectiveness of the method when the initial forget set already exhibits a high degree of syntactic variation. The authors should also explore the computational cost of generating diverse paraphrases and investigate methods to reduce this cost, such as using more efficient paraphrasing techniques or limiting the number of paraphrases generated. Furthermore, the authors should consider the potential for adversarial attacks that could circumvent the diversification strategy. This could involve testing the method against adversarial examples that are designed to exploit the limitations of the paraphrasing process. By addressing these limitations, the authors can provide a more complete understanding of the method's strengths and weaknesses.

Finally, the authors should conduct a comparative analysis of syntactic diversification against other unlearning techniques, such as gradient-based methods or methods that focus on modifying the model's internal representations. This would provide a more comprehensive understanding of the strengths and weaknesses of syntactic diversification relative to existing approaches. The authors should also explore whether combining syntactic diversification with other techniques could lead to further improvements in unlearning performance. This could involve experimenting with different combinations of techniques and evaluating their performance on a range of datasets. By comparing the proposed method against other approaches, the authors can provide a more complete picture of the state of the art in unlearning and identify potential avenues for future research.

### Questions

1. How does the proposed syntactic diversification method perform on datasets with different characteristics than TOFU?
2. What are the limitations of syntactic diversification when applied to forget sets with inherently diverse syntactic structures?
3. How does syntactic diversification compare to other methods for mitigating benign relearning, and are there any complementary approaches that could further enhance its effectiveness?

### Rating

6

### Confidence

3

**********