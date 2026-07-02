### Summary

The paper studies the problem of data curation. It first provides a theoretical framework to understand when data curation helps and when it does not. Then, it provides empirical results on ImageNet to confirm the theoretical findings.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper is well-written and easy to follow.
- The theoretical results are sound and interesting.

### Weaknesses

#### Some Related Works


#### comment

 - The paper lacks empirical results on LLMs. It would be interesting to see if the theoretical results hold for LLMs.
- The theoretical results are based on a linear model. It would be interesting to see if the theoretical results hold for more complicated models.

### Suggestions

The paper's theoretical framework, while insightful, relies on a linear model assumption, which significantly limits its applicability to real-world scenarios involving complex, non-linear models such as deep neural networks. While the authors provide a theoretical justification for their findings, it is crucial to investigate how these results translate to more practical settings. Specifically, the behavior of data curation in the context of non-linear models, which often exhibit different optimization landscapes and generalization properties, needs to be explored. For example, the impact of data curation on the loss landscape of a neural network, including the presence of local minima and saddle points, is not addressed by the current theoretical framework. Furthermore, the interaction between data curation and regularization techniques commonly used in deep learning, such as dropout or weight decay, is not considered. These factors can significantly influence the effectiveness of data curation strategies and should be investigated to provide a more comprehensive understanding of the phenomenon.

To strengthen the empirical validation, the authors should consider conducting experiments on a wider range of datasets and model architectures. While the ImageNet results are valuable, they do not fully capture the diversity of real-world data and model complexities. It would be beneficial to include experiments on datasets with different characteristics, such as those with imbalanced classes or high-dimensional inputs. Additionally, the authors should explore the impact of different data curation strategies, such as active learning or curriculum learning, on the performance of various models. This would provide a more nuanced understanding of the interplay between data curation and model performance. Furthermore, the authors should investigate the sensitivity of their findings to different hyperparameters, such as the learning rate and batch size, to ensure the robustness of their results. A more thorough empirical analysis would significantly enhance the paper's impact and practical relevance.

Finally, the paper would benefit from a more detailed discussion of the limitations of the theoretical framework and the assumptions made. While the authors acknowledge that their theory is based on a linear model, they should explicitly discuss the potential implications of this assumption on the generalizability of their findings. It would be helpful to provide a more in-depth analysis of the conditions under which the theoretical results are expected to hold and the conditions under which they might break down. This would allow readers to better understand the scope and limitations of the paper's contributions and to identify potential avenues for future research. A more thorough discussion of the limitations would also enhance the paper's credibility and provide a more balanced perspective on the topic.

### Questions

See weaknesses.

### Rating

6

### Confidence

3

**********