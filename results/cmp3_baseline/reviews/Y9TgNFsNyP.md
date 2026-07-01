## Summary
This paper introduces FF-Erase, the first machine unlearning framework specifically designed for Forward-Forward (FF) neural networks. It addresses the unique challenges of FF models—sensitivity to parameter tuning and layer-wise independent training—by using a guidance model to direct layer-wise updates via KL divergence on goodness scores. Additionally, it proposes G-MIA, a goodness-based membership inference attack that leverages FF-specific properties for black-box unlearning verification. Experiments on multiple datasets and architectures show FF-Erase achieves unlearning effectiveness comparable to retraining from scratch while being 1.9–3.1× faster.

## Strengths
- **Novel problem and solution**: The paper identifies a previously unexplored and important problem—machine unlearning for Forward-Forward models—and provides the first tailored solution (FF-Erase). The analysis of why standard gradient-ascent methods fail on FF models (sensitivity, layer-wise divergence) is well motivated.
- **Methodologically principled**: The goodness-guided unlearning via KL divergence against a guidance model is a natural adaptation of knowledge distillation to the FF setting, effectively stabilizing the otherwise unstable parameter updates. The two practical strategies for acquiring guidance models (mini-retrained, fast-distilled) add flexibility.
- **Verification contribution**: G-MIA uses layer-wise goodness vectors to perform membership inference, achieving stronger accuracy than conventional black-box attacks and often matching white-box attacks. This provides a practical verification tool for FF unlearning.
- **Thorough empirical evaluation**: Experiments cover four image benchmarks (CIFAR-10/100, MNIST, Fashion-MNIST) and three architectures (TinyCNN, AlexNet, VGG13) with state-of-the-art FF algorithms. Ablation studies on guidance model parameters and comparisons to gradient ascent across multiple λ values convincingly demonstrate the method’s effectiveness and trade-offs.

## Weaknesses
### Fatal
None.

### Major
- **Restrictive “black-box” assumption for G-MIA**: The paper classifies G-MIA as a black-box attack, but it requires access to all layer-wise goodness vectors (not just the final output). In many real-world scenarios, intermediate layer outputs may not be available to data owners. The threat model should be clarified and the term “black-box” may be misleading.
- **Limited baseline comparison**: The only unlearning baselines are retraining from scratch and direct gradient ascent. While the paper argues other unlearning methods (e.g., influence functions, Fisher forgetting) are designed for BP models, an empirical demonstration of their failure on FF models (or a simple adapted version) would strengthen the claim. Without this, the paper’s assertion that existing methods are “not feasible” is largely based on reasoning rather than evidence.

### Minor
- **Efficiency gains are modest**: The reported 1.9–3.1× speedup over retraining is helpful but not dramatic, especially considering the additional complexity of selecting hyperparameters for guidance model generation. The paper does not discuss how the method scales to larger models (e.g., ResNet-sized) or larger forgetting fractions.
- **Unlearning granularity not explored**: Only random 20% forgetting is tested. Real-world unlearning requests may be class-wise or involve outlier removal. The paper does not examine whether FF-Erase behaves well under structured forgetting.
- **Hyperparameter sensitivity**: While the ablation covers guidance model parameters, other hyperparameters (K, λ, thresholds ϵ₁, ϵ₂) are fixed without sensitivity analysis. It is unclear how robust FF-Erase is to their choice.

### Trivial
None.

## Nice-to-Haves
- Provide an analysis of why the KL-divergence loss is more stable than direct goodness minimization for FF models, perhaps using a simple 1-layer FF network.
- Discuss the applicability of FF-Erase to sequential (multi-request) unlearning scenarios.
- Include a comparison on a larger-scale dataset (e.g., CINIC-10 or Tiny ImageNet) to test scalability.

## Novel Insights
None beyond the paper’s own contributions.

## Suggestions
1. Clarify the threat model for G-MIA: specify what information the attacker is assumed to have (e.g., can they query all layer goodness scores? Is the model owner expected to provide these?). If this is not a standard black-box setting, consider renaming it “limited-access” or “intermediate-access” MIA.
2. Add at least one adapted baseline: e.g., applying gradient ascent with per-layer learning rate tuning, using random label assignments on forgetting data, or using the guidance model to simply reinitialize weights. This would further validate the claim that no simple adaptation works.
3. Report the standard deviation of G-MIA accuracy/AUC over multiple runs (or for the main unlearning experiments) to quantify the reliability of the results.
4. Discuss limitations: the approach requires training a guidance model, which adds overhead; the paper already addresses this but could highlight scenarios where this overhead may negate the speedup for very small forgetting sets.

## Score and Decision
**Score: 7.0**

The paper addresses a novel and relevant problem with a well-designed, principled solution. The empirical validation is thorough, and the G-MIA contribution is practical. The weaknesses are not fatal but limit the paper’s impact: the restricted threat model for verification and the lack of broader baseline comparisons prevent it from being a strong accept. Nonetheless, the work represents a meaningful step forward for machine unlearning in alternative training paradigms.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>