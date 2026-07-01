## Summary
This paper establishes the first theoretical framework connecting certified machine unlearning with continual learning. It adapts gradient-based and Hessian-based certified unlearning methods to a continual learning setting where tasks arrive sequentially and deletion requests can occur at any time. The authors derive upper bounds on the post-unlearning excess risk by decomposing it into a continual learning excess risk term and an unlearning loss term, and they analyze the trade-offs between the two approaches: the Hessian-based method achieves lower unlearning loss at the cost of storage, while the gradient-based method requires no storage but incurs higher unlearning loss. Experiments on MNIST validate the theoretical findings and illustrate the effect of the unlearning request sequence.

## Strengths
- **Novel problem formulation**: The paper is the first to provide a rigorous theoretical treatment of certified unlearning within a continual learning framework, clearly defining the post-unlearning excess risk and decomposing it into interpretable components.
- **Solid theoretical contributions**: The authors extend existing excess-risk bounds for ℓ₂-regularized continual learning from linear to nonlinear convex models (Theorem 3.1) and derive tight approximation-error bounds for both the natural-forgetting (gradient-based) and Hessian-based unlearning algorithms (Theorem 4.1, Propositions 5.1–5.2). The analysis of how the unlearning request sequence affects the approximation error is a nuanced and valuable insight.
- **Clear trade-off analysis**: The paper systematically compares the two adapted algorithms, highlighting the storage–accuracy trade-off and showing that the Hessian-based method can be improved by incorporating natural forgetting to reduce storage costs (Section 5.3). This provides practical guidance for system design.

## Weaknesses
### Major
- **Restrictive assumptions**: The theoretical analysis relies on strong convexity, Lipschitz continuity, and smoothness of the loss function (Assumption 2.1). The experiments, however, use cross-entropy loss with a softmax output, which is not strongly convex. While the authors acknowledge relaxing this assumption in the experiments, the gap between theory and practice is significant and limits the direct applicability of the bounds to realistic models.
- **Limited experimental validation**: The experiments are conducted only on MNIST with a linear model. Given that the paper is primarily theoretical, this is acceptable, but the empirical support would be much stronger with additional experiments on more complex datasets (e.g., CIFAR-10) or with neural networks, even if only to confirm the qualitative trends predicted by the theory.

### Minor
- **Notation density**: The paper uses many superscripts and subscripts (e.g., \(w_t^{-S_{1:t}}\), \(n_{t_i,s+1}^i\)), which makes the presentation hard to follow in places. A table of notation or a more streamlined exposition would improve readability.
- **Storage cost discussion**: The storage overhead of the Hessian-based algorithm is stated as \(O(t d^2 + 2td)\), but the paper does not discuss how this scales with model dimension \(d\) in practice (e.g., for deep networks). A brief comment on feasibility would be helpful.

### Trivial
- None.

## Nice-to-Haves
- An empirical comparison of the two algorithms on a non-convex model (e.g., a small CNN) would strengthen the claim that the theoretical insights extend beyond convex settings.
- A more detailed ablation study on the effect of the unlearning sequence order (beyond the single example in Table 2) would further illustrate the sensitivity predicted by Proposition 5.1.

## Novel Insights
Beyond the paper’s own contributions, the key insight is that the natural forgetting inherent in continual learning can be both a curse and a blessing: it helps reduce the unlearning loss for old tasks (by making the model already close to the retrained model) but simultaneously increases the excess risk if the regularization parameter \(\lambda\) is too large. This tension is formalized through the decomposition of the post-unlearning excess risk and leads to the conclusion that the optimal \(\lambda\) for continual learning alone is not optimal when unlearning is required. The analysis of how the order of unlearning requests interacts with the approximation error (especially the additional error terms when requests arrive out of order) is a novel and practically relevant observation.

## Suggestions
- Consider adding a short discussion on how the theoretical bounds could be extended to non-convex losses (e.g., via convex relaxation or local strong convexity), even if only as a conjecture or future work.
- Clarify the notation in the Hessian update (13) by explicitly defining the product operator and the indices, as the current presentation is dense.

## Score and Decision
MY FINAL SCORE: 7.5
MY FINAL DECISION: Accept