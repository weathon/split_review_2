### Summary

This paper studies the generalization error of algorithms that can be described by a trajectory of iterates or, more generally, a data-dependent random set. The authors introduce a notion of stability for such algorithms and use it to derive bounds on the generalization error in terms of this stability measure and a Rademacher complexity term. They apply their framework to obtain bounds based on fractal and topological complexity measures.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

The paper combines empirically relevant complexity measures with a framework that avoids intractable quantities, which is a significant advancement.

### Weaknesses

#### Some Related Works


#### comment

The paper is difficult to read, with many terms and concepts that could benefit from clearer explanations. For instance, the authors mention "mild measure-theoretic conditions" without specifying what these are. The notion of "data-dependent selection" is also not well-explained, and the definition provided in Definition 3.1 is not intuitive. The core of the paper, Assumption 3.1, is not clearly motivated, and it is not evident how this assumption relates to the generalization error. The connection between the stability parameter and the Rademacher complexity term is also not well-established. The authors use Lemma 3.4, which is a known result, but it is not clear how this lemma specifically applies to the random set stability framework they have introduced. The derivation of Corollaries 3.5 and 3.6 from Lemma 3.4 is not straightforward, and the assumptions used in these derivations are not clearly stated. The paper also lacks a clear explanation of how the Rademacher complexity is evaluated over the random set, and the use of a sample \tilde{S}_J that is independent of the random set W_{S,U} is not well-justified. The authors also do not provide sufficient details on how the Lipschitz continuity of the loss function is used in their analysis, and the implications of this assumption are not clear. The authors claim that their framework is computationally tractable, but they do not provide concrete examples of how to compute the stability parameter in practice. The authors also do not provide a clear explanation of how their results compare to existing generalization bounds, and it is not clear whether their bounds are tighter or more informative than existing bounds.

### Suggestions

The paper would greatly benefit from a more detailed explanation of the measure-theoretic foundations underlying their framework. Specifically, the authors should provide a precise definition of the probability spaces they are working with, including the underlying sigma-algebras and the measures themselves. This would clarify the meaning of terms like "almost surely" and "random variable" in their context. Furthermore, the authors should provide a more intuitive explanation of the data-dependent selection process. Instead of simply stating that it is a deterministic mapping, they should provide a concrete example of how such a selection is made in practice. For instance, they could describe a specific algorithm that performs this selection and explain how it relates to the overall goal of bounding the generalization error. This would make the concept much more accessible to the reader. The authors should also provide a more detailed explanation of the motivation behind Assumption 3.1. They should explain why this particular form of stability is relevant for bounding the generalization error and how it relates to existing notions of stability. They should also provide examples of algorithms that satisfy this assumption and examples of algorithms that do not. This would help the reader understand the scope and limitations of their framework.

To improve the clarity of the technical results, the authors should provide a more detailed explanation of how Lemma 3.4 is applied in their setting. They should explain why the Rademacher complexity is evaluated over the random set and how this relates to the stability parameter. They should also provide a more detailed derivation of Corollaries 3.5 and 3.6, including all the necessary assumptions and steps. This would make it easier for the reader to follow the logic of their arguments. The authors should also provide a more detailed explanation of how the Lipschitz continuity of the loss function is used in their analysis. They should explain how this assumption is used to bound the difference in loss values between different iterates and how this relates to the stability parameter. They should also discuss the limitations of this assumption and whether it is necessary for their results to hold. The authors should also provide concrete examples of how to compute the stability parameter in practice. This would help the reader understand the practical implications of their work. For instance, they could describe a specific algorithm for computing this parameter and provide a numerical example to illustrate the process. This would make their work more accessible to a wider audience.

Finally, the authors should provide a more detailed comparison of their results to existing generalization bounds. They should explain how their bounds compare to existing bounds in terms of tightness, computational complexity, and practical relevance. They should also discuss the limitations of their approach and whether it is possible to obtain tighter bounds using their framework. This would help the reader understand the significance of their work and its place in the broader context of generalization theory. The authors should also clarify the role of the parameter J in Lemma 3.4 and how it affects the final bound. They should explain why this parameter is needed and how it relates to the other parameters in their analysis. They should also discuss the implications of choosing different values for J and whether there is an optimal choice for this parameter. This would help the reader understand the trade-offs involved in their approach and how to choose the parameters to obtain the best possible bounds.

### Questions

1. The authors write "Note that the existence of such a random variable is ensured under mild measure-theoretic conditions (Molchanov (2017)." What exactly are these measure-theoretic conditions? For instance, what is the underlying probability space, and what is the sigma-algebra on which the random variable is defined? A more precise explanation of these measure-theoretic foundations would be helpful.

2. The authors write "a data-dependent selection of W_{S,U} is a deterministic mapping w: CL(R^d) × Z^n → R^d." This is not a definition, as it does not explain what a data-dependent selection is. Could the authors provide a more intuitive explanation of what a data-dependent selection is and how it is used in their framework?

3. What is the motivation behind Assumption 3.1? Why is this particular form of stability relevant for bounding the generalization error? How does this assumption relate to existing notions of stability in the literature?

4. In Lemma 3.4, why is the Rademacher complexity evaluated over the random set W_{S,U}? Could the authors provide a more detailed explanation of how this is done and why it is necessary for their analysis?

5. In Lemma 3.4, the authors use a sample \tilde{S}_J that is independent of the random set W_{S,U}. Why is this independence necessary? Could the authors provide a more detailed explanation of how this independence is used in their analysis?

6. In the derivation of Corollaries 3.5 and 3.6 from Lemma 3.4, what assumptions are used? Could the authors provide a more detailed explanation of the steps involved in these derivations?

7. How is the Lipschitz continuity of the loss function used in the analysis? Could the authors provide a more detailed explanation of how this assumption is used to bound the difference in loss values between different iterates?

8. Could the authors provide concrete examples of how to compute the stability parameter in practice? This would help the reader understand the practical implications of their work.

9. How do the authors' results compare to existing generalization bounds in the literature? Are their bounds tighter or more informative than existing bounds? Could the authors provide a more detailed comparison of their results to existing work?

### Rating

3

### Confidence

3

**********