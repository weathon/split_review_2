## Summary
This paper initiates the theoretical study of certified machine unlearning within a continual learning framework. The authors formulate a two-stage process where new tasks are learned sequentially and unlearning requests can arrive at any time. They adapt gradient-based (natural forgetting) and Hessian-based certified unlearning methods to this setting, derive upper bounds on the post-unlearning excess risk by decomposing it into continual learning excess risk and unlearning loss, and validate the theory with MNIST experiments. The main theoretical contribution is the first formal connection between the two areas, with explicit trade-offs between forgetting, storage, and privacy guarantees.

## Strengths
- **Novel problem and formalization**: The paper is the first to provide rigorous theoretical guarantees for certified unlearning within a continual learning framework. The decomposition of post-unlearning excess risk into two components (continual learning error and unlearning loss) is insightful and enables principled analysis of trade-offs.
- **Solid theoretical analysis**: Theorems 3.1, 4.1, Propositions 5.1, 5.2, and Corollary 5.3 provide non-trivial bounds that extend prior results from linear models to convex models with smoothness and strong convexity. The analysis of how the unlearning sequence order affects performance (especially in the Hessian-based algorithm) is a valuable new insight.
- **Clear algorithmic design and comparison**: Two complementary algorithms are developed—one with zero additional storage (natural forgetting, Alg. 1) and one with tighter approximation but higher storage cost (Hessian-based, Alg. 2). The forgetting-enhanced variant (Section 5.3) intelligently combines both approaches to reduce storage.
- **Interpretation of the trade-off via λ**: The paper clearly demonstrates that the regularization parameter λ controls the tension between continual learning accuracy (excess risk) and unlearning effectiveness (unlearning loss), which is a fundamental new design consideration.

## Weaknesses

### Fatal
None.

### Major
- **Experimental validation does not support claimed superiority of Hessian-based method**: The abstract and Section 5.2 claim that the Hessian-based algorithm “largely outperforms” the gradient-based one, yet the experimental results in Figure 2(b) show that the natural forgetting algorithm actually achieves *lower* unlearning loss (≈0.08 vs. ≈0.20 for Hessian over most λ). Moreover, Table 1 only reports test accuracy for the Hessian algorithm and perfect retraining, omitting the natural forgetting baseline. Without a direct comparison of the final post-unlearning excess risk (or accuracy) for both algorithms, the claim is unsubstantiated by the presented experiments.

### Minor
- **Strong convexity assumption restricts scope**: The theory (Assumption 2.1) requires μ-strong convexity, which excludes widely used losses such as cross-entropy without regularization. The experiments relax this assumption but remain in the convex regime (linear model, softmax). The paper therefore does not fully address non-convex models (e.g., deep neural networks), which are the dominant use case for both continual learning and unlearning.
- **Limited experimental scope**: Experiments are confined to a single dataset (MNIST) and a linear model. The impact of unlearning sequence patterns is mentioned but only shown in the appendix (not provided for review), and storage overhead is not empirically measured.
- **Task-level unlearning focus**: The paper targets unlearning entire tasks; extension to sample-level unlearning is stated as straightforward but not shown. This limits direct applicability to fine-grained deletion requests.

### Trivial
- Some notation is overloaded (e.g., $w_t^{-S_{1:t}}$ vs $w_t^{-S_{\leq t}}$), but the exposition is generally clear.

## Nice-to-Haves
- Include empirical comparison of both algorithms on final post-unlearning excess risk (e.g., test accuracy or loss after unlearning) to validate the claimed advantage of the Hessian approach.
- Show results on a more complex dataset (e.g., CIFAR-10 with a small convolutional network) with appropriate convex approximations or empirical verification.
- Provide storage cost measurements to complement the theoretical complexity analysis.

## Novel Insights
Beyond the paper’s own contributions, the key insight is that the presence of unlearning introduces a *new tension* into the design of continual learning algorithms: a large regularization penalty λ helps reduce catastrophic forgetting (good for continual learning) but simultaneously increases the unlearning loss (bad for unlearning). This trade-off is absent in prior work on either topic separately. The analysis of how the order of unlearning requests affects approximation error—especially the sensitivity of the Hessian-based method to disruptive sequences—is also a novel observation that could inform practical scheduling of deletion requests.

## Suggestions
- **Add a direct experimental comparison** of the two proposed algorithms under the same post-unlearning accuracy metric, and discuss why the theoretical advantage of the Hessian method (second-order) does not translate to empirical gains in the current setup.
- **Clarify the claim** in the abstract and elsewhere: if the Hessian algorithm is intended to outperform only in the second-order regime (i.e., when the loss is nearly quadratic), state this explicitly and note that the linear-model experiments may not capture that advantage.
- Consider discussing limitations of the strong convexity assumption and potential extensions via relaxations (e.g., PL condition) to broaden the applicability.

## Score and Decision
This paper makes a strong theoretical contribution by formulating and analyzing certified unlearning in continual learning for the first time. The ideas are original and the analysis is rigorous. However, a major weakness is the mismatch between the claimed superiority of the Hessian-based algorithm and the experimental evidence presented; the experiments do not validate this claim and omit the necessary baseline comparison. This significantly weakens the empirical support for one of the paper’s central assertions. Overall, the theoretical value is high, but the experimental gap prevents full confidence.

MY FINAL SCORE: 6.0</score>
MY FINAL DECISION: Borderline Accept</decision>