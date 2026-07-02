### Summary

This paper introduces INFOTok, an adaptive video tokenizer that leverages Shannon’s information theory to optimize token compression rates based on video complexity. Unlike fixed-rate tokenizers, INFOTok dynamically adjusts token lengths using an ELBO-based router, achieving near-optimal compression. This approach significantly improves token efficiency, saving 20% of tokens without sacrificing performance and outperforming previous adaptive methods by 2.3× in compression rates.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper provides a rigorous theoretical foundation, proving the suboptimality of existing fixed-rate tokenizers and demonstrating the near-optimality of INFOTok’s adaptive approach through theorems grounded in Shannon’s information theory.

2. INFOTok demonstrates substantial empirical improvements, achieving 20% token savings without performance loss and outperforming prior adaptive tokenizers by a 2.3× compression rate, validated across multiple video datasets.

### Weaknesses

#### Some Related Works


#### comment

1. The ELBO-based routing adds computational overhead, requiring an additional decoder pass to estimate video complexity. This may impact real-time applications, especially for long video sequences. The author should discuss this in the paper and provide an estimation on the extra time cost of this decoder pass.

2. The evaluation is primarily focused on reconstruction quality, with limited exploration of downstream tasks. The impact of adaptive tokenization on tasks like video generation or action recognition remains unclear. The author should at least include more experiments on video downstream tasks like action recognition.

3. The router and adaptive compressor add complexity to the model architecture. The sensitivity of the model to the hyperparameters of the router and compressor is not thoroughly explored. The author should at least include an ablation study on the hyperparameters of the router and compressor.

4. The paper primarily demonstrates INFOTok's effectiveness on standard video datasets. Its performance in domains with different characteristics, such as medical or surveillance video, is not evaluated. The author should at least include some discussions about this.

5. The author claims that INFOTok can save approximately 50% tokens without loss of reconstruction quality compared to state-of-the-art fixed-length tokenizers, and it can outperform previous adaptive tokenizers by an average compression rate of $2.3\times$ and number of evaluations (NFEs) by $11\times$. However, the baseline model used in the comparison is not a recent one. The author should compare the performance of INFOTok with more recent baselines.

### Suggestions

The paper introduces an interesting approach to adaptive video tokenization using an ELBO-based router. However, several aspects require further investigation to solidify its practical applicability and theoretical grounding. First, the computational overhead of the ELBO-based routing needs a more thorough analysis. While the paper mentions an additional decoder pass, it lacks a detailed breakdown of the time cost associated with this step, especially in the context of long video sequences. A more granular analysis, perhaps showing the time cost as a function of video length, would be beneficial. Furthermore, the paper should explore potential optimizations to mitigate this overhead, such as using a lighter-weight network for complexity estimation or employing techniques like frame-skipping during the routing phase. This is crucial for real-time applications where latency is a critical factor.

Second, the evaluation of INFOTok should be expanded beyond reconstruction quality. While high reconstruction fidelity is important, the ultimate goal of video tokenization is often to enable downstream tasks. The paper should include experiments on video generation, action recognition, or other relevant tasks to demonstrate the effectiveness of the adaptive tokenization strategy in these contexts. For example, the authors could evaluate the performance of INFOTok when used as input to a video generation model, comparing the quality and diversity of generated videos against those produced using fixed-length tokenizers. Similarly, the authors could assess the impact of adaptive tokenization on the accuracy and efficiency of action recognition models. Such experiments would provide a more comprehensive understanding of the practical benefits of INFOTok.

Finally, the paper should address the sensitivity of the model to the hyperparameters of the router and compressor. The current analysis lacks a detailed exploration of how different hyperparameter settings affect the performance of INFOTok. An ablation study varying the parameters of the router and compressor would be valuable. This study should not only focus on reconstruction quality but also on compression rate and computational cost. Furthermore, the paper should discuss the potential limitations of INFOTok in domains with different characteristics, such as medical or surveillance video. While the current results are promising, it is important to acknowledge that the performance of the model may vary across different types of video data. A discussion of these limitations would provide a more balanced perspective on the applicability of INFOTok.

### Questions

Please refer to the weakness.

### Rating

6

### Confidence

4

**********