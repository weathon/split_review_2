Summary of the Paper:

This paper explores incorporating structural locality features into non-parametric language models that retrieve examples from an external datastore.

The authors propose a simple approach of learning parameters that modify the distance metric used to retrieve examples based on locality information, to improve the likelihood of retrieving local examples.

Experiments on Java source code and Wikipedia text demonstrate that adding locality features improves the perplexity and prediction accuracy compared to baseline models without these features. The authors also analyze how locality contributes to the improvements and why contextual similarity alone does not fully capture the locality structure.

Strengths and Weaknesses:

Strengths:

The paper addresses an important problem of leveraging structural locality in non-parametric language models, which is a ubiquitous feature of real-world datasets. The proposed method is simple yet effective, requiring only a few additional learned parameters.

Experiments on two very different domains demonstrate the broad applicability of the approach. The authors provide an insightful analysis comparing the effect of locality in the two domains.

Weaknesses:

The gains from adding locality features, while consistent, are relatively modest in terms of perplexity and accuracy.

More discussion on the significance of the improvements would be helpful.

The choice of locality features seems somewhat ad-hoc based on domain knowledge.

More principled methods for defining the features could be explored.

Limitations of the approach when locality information is not available or already captured by the model are not discussed in depth.

Clarity, Quality, Novelty, and Reproducibility:

The paper is well-written and easy to follow.

The proposed method is described clearly and the experiments are comprehensive.

The work is novel in studying the effect of locality in non-parametric language models and proposing a lightweight method to incorporate it.

The code and data are provided which aids reproducibility.

The overall quality of the research seems high.

Summary of the Review:

This paper makes a valuable contribution in demonstrating how structural locality information can be leveraged to improve non-parametric language models.

The proposed method is straightforward but effective as shown through experiments on two domains.

The analysis provides useful insights into the differing effects of locality.

While the gains are modest, the work opens up interesting avenues for further exploration of locality-aware retrieval-based language models.

Some additional discussion on the choice and limitations of the locality features would further strengthen the paper.

Overall, this is a solid paper that advances our understanding of an important problem.