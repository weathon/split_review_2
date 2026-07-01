## Summary

This paper introduces FF-Erase, the first machine unlearning framework for Forward-Forward (FF) models. It identifies that standard unlearning methods (e.g., gradient ascent) cause model collapse in FF models due to their sensitivity to parameter tuning and layer-wise independent training. To address this, the authors propose a goodness-guided approach that uses a guidance model to produce stable target goodness distributions, steering the original model to unlearn forgetting data by minimizing KL divergence between goodness vectors. Additionally, the paper presents G-MIA, a black-box membership inference attack that leverages the unique layer-wise goodness scores of FF models for accurate unlearning verification. Experiments demonstrate that FF-Erase achieves comparable effectiveness to retraining from scratch while being 1.9–3.1× faster, and G-MIA outperforms existing black-box and even white-box MIAs on several FF architectures.

## Strengths

- **Novel problem formulation.** This paper is the first to formally identify and address the challenges of machine unlearning for Forward-Forward models, a biologically plausible alternative to backpropagation. The failure analysis of naive gradient ascent on FF models is clearly reasoned and experimentally validated.
- **Principled method design.** The proposed FF-Erase adapts gradient-based unlearning to the FF architecture through a distillation-like loss that shifts goodness distributions toward a stable guidance model, effectively preventing the layer divergence and model collapse observed with direct ascent.
- **Practical verification tool.** G-MIA provides a lightweight, black-box verification method that exploits the multi-layer goodness signals intrinsic to FF models. Its strong empirical performance (outperforming white-box attacks on deeper networks) makes it a valuable contribution beyond the unlearning context.
- **Thorough experimentation.** The paper evaluates across multiple datasets (CIFAR-10, CIFAR-100, MNIST, Fashion-MNIST), architectures (TinyCNN, AlexNet, VGG13), and FF training variants (CwComp, Deeperforward). The ablation study on guidance model strategies demonstrates flexible efficiency-performance trade-offs.

## Weaknesses

### Major
- **Limited baseline comparison for unlearning.** The comparison is restricted to retraining from scratch and direct gradient ascent. While the paper argues that other approximate unlearning methods (e.g., influence functions) are not directly applicable, a brief empirical attempt to adapt such methods (or a discussion of why adaptation is fundamentally impossible) would strengthen the claim that existing approaches universally fail on FF models.
- **Potential dependence on guidance model quality.** The effectiveness of FF-Erase relies on the guidance model being both stable and ignorant of the forgetting data. While the proposed mini-retraining and fast-distillation strategies are reasonable, the paper does not analyze scenarios where the guidance model is imperfect (e.g., when remaining data is scarce or noisy). The ablation only varies data proportion and training epochs, not data quality.

### Minor
- **G-MIA assumptions.** G-MIA assumes the attacker can synthesize data with a similar distribution to the training set (via model inversion or public data) and can obtain the full set of layer-wise goodness vectors from the target model. While the paper classifies G-MIA as black-box, the requirement of per-layer goodness outputs may not be available in all deployment settings (e.g., APIs that only return the final prediction). A brief discussion of this limitation would improve clarity.
- **Efficiency claims.** The speedup of 1.9–3.1× over retraining is demonstrated, but the overhead of generating the guidance model (e.g., 15% of retraining time) is counted in total time. The actual speedup relative to retraining may be smaller when guidance model generation time is included; the paper acknowledges this but could state the net speedup more explicitly.

### Trivial
- The paper refers to "goodness decrease" and "goodness increase" in a way that conflates the vector of class-wise goodness scores with a scalar direction. The precise mathematical relationship (e.g., softmax of goodness) is clear, but the phrasing could be slightly misleading on first reading.

## Nice-to-Haves
- An analysis of how the number of classes (J) affects the dimensionality of the goodness vector and consequently the performance of G-MIA.
- A comparison with a baseline that applies gradient ascent only on the predictor layer (since FF models often use a final predictor on top of goodness vectors) to isolate the source of model collapse.
- A discussion of whether G-MIA could be extended to verify unlearning in BP-based models by using intermediate activations, or whether the property is unique to FF models.

## Novel Insights
Beyond the paper’s own contributions, a genuinely novel observation is that the layer-wise independence of FF training makes membership signals more distributed and discriminative than in BP models. This explains why G-MIA can outperform white-box attacks that rely on gradient information: the goodness scores from multiple layers encode membership in a way that is not easily obscured by standard regularization. This insight suggests that future privacy research on FF models should consider the per-layer goodness signal as a primary leakage channel.

## Suggestions
- To strengthen the claim that existing methods are infeasible, the authors could briefly attempt a simple adaptation (e.g., applying gradient ascent per layer independently) and report its failure mode, even qualitatively, in the main text (beyond Figure 5).
- Clarify in the G-MIA section whether the attacker needs access to the original model’s training set statistics (e.g., mean/variance for synthetic data generation) or only the model output. This would help practitioners assess the realism of the threat model.

## Score and Decision

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>