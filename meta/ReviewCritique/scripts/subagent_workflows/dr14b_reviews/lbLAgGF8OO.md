### Summary

This paper studies decision making with structured observations (DMSO). Previous work has characterized the complexity of DMSO via the decision-estimation coefficient (DEC), but left a gap between the regret upper and lower bounds that scales with the size of the model class. To tighten this gap, this paper introduces Dig-DEC, a model-free DEC that removes optimism and drives exploration purely by information gain. By applying Dig-DEC to hybrid MDPs with stochastic transitions and adversarial rewards, this paper obtains the first *model-free* regret bounds for *hybrid* MDPs with *bandit* feedback under linear reward and several *general* transition structures, resolving the main open problem left by [LWZ25].

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The authors introduce a new model-free DEC notion, Dig-DEC, that improves over the optimistic DEC of [FGQ+23]. Their approach does not rely on the optimism principle, but adheres more closely to the general idea of DEC that drives exploration purely with information gain. For canonical settings such as bilinear classes or Bellman-complete MDPs with bounded Bellman eluder dimension or coverability, they recover their complexities with improved  T -dependence in the regret, while in some constructed settings, the improvement can be arbitrarily large.
2. The authors establish the first sublinear regret for model-free learning in hybrid bilinear classes and Bellman-complete coverable MDPs with linear reward and bandit feedback, resolving the open question in [LWZ25].
3. The authors improve the online function estimation procedure both in the case of average estimation error and squared estimation error. This allows them to improve the  T 3/2/T 5/6 regret of [FGQ+23] to  T 3/2/T 5/6  in the former case, and improve the  T 3/2  regret of [FGQ+23] to  √T  in the latter case. The techniques they use to achieve them could be of independent interest.

### Weaknesses

#### Some Related Works


#### comment

1. The presentation of this paper is quite abstract and hard to follow. I am not able to catch the main idea of the proof. Could you provide more explanations on the main idea of the proof?

### Suggestions

The paper introduces a novel model-free Decision-Estimation Coefficient (DEC), termed Dig-DEC, which is a significant contribution. However, the presentation could be improved to enhance clarity and accessibility. Specifically, the core concepts, such as the precise definition of Dig-DEC and its relationship to existing DEC notions, should be explained with more intuitive examples and less reliance on abstract mathematical formalism. For instance, providing a concrete example of a bilinear class or a Bellman-complete MDP where Dig-DEC can be explicitly calculated would greatly aid understanding. Furthermore, the paper should include a more detailed explanation of how the information gain is quantified and used to drive exploration in the model-free setting. This would help readers grasp the practical implications of the theoretical results.

To improve the presentation, the authors should consider adding a section that provides a high-level overview of the proof strategy before diving into the technical details. This overview should clearly articulate the key steps and the underlying intuition behind each step. For example, the authors could explain how the removal of optimism in Dig-DEC leads to improved regret bounds and how this is achieved through the specific construction of the algorithm. Additionally, the paper could benefit from a more detailed discussion of the limitations of the proposed approach. Are there specific scenarios where Dig-DEC might not be applicable or where its performance might be suboptimal? Addressing these limitations would provide a more balanced perspective on the contribution of the paper.

Finally, the paper should include more illustrative examples to demonstrate the practical implications of the theoretical results. For instance, the authors could provide a simple example of a hybrid MDP with a linear reward function and a specific transition structure, and then show how the proposed algorithm can be applied to this example. This would help readers understand how the theoretical results translate into practical applications. Furthermore, the paper could include a comparison of the proposed algorithm with existing algorithms in terms of computational complexity and sample efficiency. This would provide a more comprehensive evaluation of the proposed approach and its potential impact on the field.

### Questions

Please see above.

### Rating

6

### Confidence

2

**********