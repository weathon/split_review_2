### Summary

The paper proposes a method to measure the quality of reasoning in a prompt response by calculating the sum of the top 0.5% of token entropies. The authors use this method in several experiments with SFT, RFT, and RL to demonstrate that selecting data with high-quality reasoning generalizes across different training paradigms.

### Soundness

2

### Presentation

3

### Contribution

2

### Strengths

The proposed method is straightforward and appears effective. The experimental results demonstrate that selecting high-quality reasoning data improves performance across various training paradigms, suggesting good generality.

### Weaknesses

#### Some Related Works


#### comment

1. The authors do not provide a detailed explanation of how HES addresses the limitations of previous methods, particularly in distinguishing between high- and low-quality reasoning samples. The paper lacks a clear articulation of the specific shortcomings of existing entropy-based metrics, such as average entropy, and how summing only the top 0.5% of token entropies overcomes these issues. It is not clear why focusing on the highest entropy tokens, which are often incorrect, would lead to better reasoning quality compared to considering all tokens or other selection methods.
2. In Section 4.1.2, the authors should compare their method with more up-to-date baselines. The current comparison is limited, and it is essential to benchmark against more recent and state-of-the-art methods to properly evaluate the effectiveness of the proposed approach. The paper should also include a more comprehensive set of baselines, including methods that use different types of entropy or other metrics for reasoning quality.
3. The authors should include comparisons with more up-to-date baselines in the RFT and RL experiments. The current baselines are not sufficient to demonstrate the superiority of the proposed method. The paper should include comparisons with more recent and state-of-the-art methods in both RFT and RL to ensure a fair evaluation.
4. The authors should explain why the HES-based method performs better than other baselines. The paper lacks a detailed analysis of the underlying reasons for the observed performance improvements. It is not clear why selecting data based on the top 0.5% of token entropies leads to better reasoning quality compared to other selection methods. The authors should provide a more in-depth analysis of the characteristics of the selected data and how it contributes to improved performance.

### Suggestions

The paper needs to provide a more thorough explanation of how HES addresses the limitations of existing methods. Specifically, the authors should elaborate on why summing only the top 0.5% of token entropies is superior to using average entropy or other entropy-based metrics. A detailed analysis of the characteristics of high-entropy tokens and their impact on reasoning quality is necessary. For instance, the authors could analyze the types of errors that occur at these high-entropy positions and how they relate to the overall quality of the reasoning. Furthermore, the authors should provide a more detailed comparison with other methods for selecting high-quality reasoning data, including those that use different types of entropy or other metrics. This comparison should include a discussion of the advantages and disadvantages of each method and why HES is a better choice.

In addition to the theoretical explanation, the authors should also provide more empirical evidence to support their claims. This could include a more detailed analysis of the correlation between HES and other metrics for reasoning quality, such as human evaluations or other automated metrics. The authors should also conduct experiments with a wider range of datasets and tasks to demonstrate the generalizability of their method. The current experiments are limited in scope and do not provide sufficient evidence to support the claim that HES is a robust and effective method for selecting high-quality reasoning data. The authors should also consider including ablation studies to analyze the impact of different parameters, such as the 0.5% threshold, on the performance of the method.

Finally, the authors should provide a more in-depth analysis of the underlying reasons for the observed performance improvements. It is not clear why selecting data based on the top 0.5% of token entropies leads to better reasoning quality compared to other selection methods. The authors should provide a more detailed analysis of the characteristics of the selected data and how it contributes to improved performance. This could include an analysis of the types of reasoning steps that are present in the selected data and how they differ from those in the unselected data. The authors should also consider including a qualitative analysis of the selected data to provide more insights into the method's behavior. This analysis should include examples of high and low HES scores and how they relate to the quality of the reasoning.

### Questions

1. The proposed method appears to differ from previous approaches by calculating entropy based on the distribution of all tokens at each position and summing only the top 0.5%. Could the authors clarify the novelty of this approach and how it differs from existing methods?
2. In the Introduction, the authors state that previous methods fail to distinguish between high- and low-quality reasoning samples, but it is unclear how HES addresses this limitation. Could the authors provide a more detailed explanation?
3. The authors should include comparisons with more recent baselines to ensure a fair evaluation of their method's effectiveness.

### Rating

5

### Confidence

4

**********