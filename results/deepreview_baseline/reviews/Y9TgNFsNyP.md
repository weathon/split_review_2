## Summary

This paper introduces FF-Erase, the first machine unlearning framework specifically designed for Forward-Forward (FF) neural networks. The authors identify that conventional gradient-based unlearning methods cause model collapse in FF models due to their layer-wise independent training and sensitivity to parameter tuning. To address this, they propose a goodness-guided unlearning approach that uses a guidance model to provide stable target goodness distributions, along with a novel goodness-based membership inference attack (G-MIA) for black-box verification. Experiments demonstrate that FF-Erase achieves 1.9-3.1× speedup over retraining from scratch while maintaining comparable effectiveness and model utility.

## Strengths

- **Novel problem formulation**: The paper is the first to formally identify and address the unique challenges of machine unlearning for Forward-Forward models, which is a timely contribution given the growing interest in biologically plausible alternatives to backpropagation.
- **Well-motivated technical approach**: The goodness-guided strategy using KL-divergence to shift goodness distributions toward a guidance model is a principled solution that directly addresses the instability issues caused by FF models' layer-wise independent training.
- **Comprehensive evaluation framework**: The paper provides both an unlearning method and a verification method (G-MIA), creating a complete pipeline. The ablation study on guidance model configurations (Table 1) is thorough and provides practical insights into efficiency-performance trade-offs.

## Weaknesses

### Major

- **Limited baseline comparisons**: The paper only compares against retraining from scratch and direct gradient ascent. There are many approximate unlearning methods (e.g., influence functions, Fisher forgetting, SCRUB, EU-k) that could potentially be adapted to FF models. The claim that "existing machine unlearning methods are not feasible for FF models" would be stronger if demonstrated against a broader set of adapted baselines rather than just GA.
- **Unclear practical significance of G-MIA**: While G-MIA outperforms other black-box MIAs, the paper does not clearly establish why a black-box MIA is necessary for verification when the model owner (who performs unlearning) presumably has white-box access. The motivation that "data owners may not have full access to model parameters" conflates the unlearning performer with the verifier. The practical scenario where a third party needs to verify unlearning using only goodness scores is not well-articulated.

### Minor

- **Limited dataset and model scope**: All experiments use relatively small image datasets (CIFAR-10/100, MNIST, Fashion-MNIST) and modest architectures (TinyCNN, AlexNet, VGG13). The paper would benefit from at least one experiment on a larger-scale dataset or more modern architecture to demonstrate scalability.
- **Missing statistical significance**: The paper reports single-run results without confidence intervals or standard deviations. Given the stochastic nature of training and unlearning, multiple trials would strengthen the reliability of the reported numbers.
- **The G-MIA attack model training requires synthetic data generation**: The paper assumes attackers can synthesize data with similar distribution to training data, which is a strong assumption that may not hold in practice. The sensitivity of G-MIA to the quality of synthetic data is not explored.

### Trivial

- The notation in Equation (1) uses $\mathbf{g}^l = \|\mathbf{h}^l\|_1$ but the text later describes it as a vector of class-wise scores, which is slightly inconsistent with the L1 norm notation.

## Nice-to-Haves

- A comparison with exact unlearning methods (e.g., SISA) adapted for FF models would strengthen the positioning of FF-Erase as an approximate unlearning method.
- Analysis of how the unlearning performance degrades as the forgetting set size increases beyond 20% would be valuable for practical deployment.
- Discussion of potential negative societal impacts or failure modes of the G-MIA attack (e.g., privacy leakage beyond unlearning verification) would be responsible.

## Novel Insights

The key insight is that FF models' layer-wise goodness distributions provide a natural and informative signal for both unlearning and membership inference that is not available in backpropagation-based models. The paper demonstrates that the goodness distribution carries more membership information than final-layer outputs, and that guiding unlearning toward a reference goodness distribution (rather than directly minimizing goodness) prevents the catastrophic collapse that occurs when layers diverge during independent gradient updates. This suggests that the layer-wise independence of FF models, while a challenge for unlearning, also creates new opportunities for verification that are not possible in BP models.

## Suggestions

- Add experiments with at least one larger dataset (e.g., Tiny ImageNet) and a deeper FF architecture to demonstrate scalability.
- Report results over multiple random seeds (at least 3-5) with standard deviations.
- Include adapted versions of at least one additional approximate unlearning method (e.g., influence function-based or Fisher-based) as baselines to strengthen the claim that existing methods fail on FF models.
- Clarify the practical verification scenario for G-MIA: who is the attacker/verifier, what access do they have, and why is black-box access the realistic assumption?

## Score and Decision

The paper addresses a genuinely novel and well-motivated problem with a technically sound solution. The main limitations are the narrow baseline comparison and limited experimental scope, but these do not invalidate the core contribution. The paper is clearly written, the methodology is reproducible, and the results convincingly demonstrate the effectiveness of FF-Erase. Given the novelty of the problem and the quality of the proposed solution, this paper merits acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>