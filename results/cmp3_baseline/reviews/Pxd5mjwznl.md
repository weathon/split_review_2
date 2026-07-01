## Summary

The paper proposes Difference Back Propagation (DBP), which replaces the derivative of the sigmoid activation function with a finite-difference slope computed using the inverse sigmoid. The key idea is that when updating neuron values during gradient descent, the derivative-based update is inconsistent with the actual change in the activation function, so using the difference (Δa/Δz) yields a more consistent update. Experiments on small neural networks and a small transformer show marginal improvements in convergence speed and final loss.

## Strengths

- The paper identifies a genuine issue: with finite learning rates, the gradient descent update based on the derivative at the current point does not exactly correspond to the change in the activation function after the update. This observation is conceptually interesting.
- The idea of using the inverse function to compute a more consistent update is a creative direction that could potentially inspire further work on alternative gradient approximations.

## Weaknesses

### Fatal

- **The proposed method is not a valid backpropagation algorithm.** The gradient of the loss with respect to \(z\) must be computed at the current point using the chain rule. DBP instead computes \(\frac{dl}{dz} = \frac{a' - a}{z' - z} \frac{dl}{da}\), where \(a' = a - \eta \cdot dl/da\) and \(z' = \text{inv\_sig}(a')\). This requires knowing the *updated* activation \(a'\) before computing the gradient for \(z\), which is not available during standard backpropagation. The resulting update does not correspond to the gradient of any loss function; it is a heuristic finite-difference scheme that depends on the learning rate and the current gradient direction. The paper provides no theoretical justification for why this should converge or what objective it optimizes.

- **The experiments are insufficient to support the claims.** Only two tiny synthetic networks (1,2,1) and (1,2,2,1) are tested on 100 data points, with no train/test split, no statistical significance (single run, no error bars), and no comparison with standard optimizers (Adam, momentum, etc.). The transformer experiment on AG News uses a very small model (\(d_{\text{model}}=32\), 2 layers) and shows only a tiny improvement in accuracy (roughly 0.2–0.4%). Without multiple seeds, hyperparameter tuning, or comparison to baselines, it is impossible to conclude that DBP is effective. The paper does not even report whether the method actually computes gradients correctly (e.g., by checking the gradient norm or comparing to finite differences).

### Major

- **The paper overclaims novelty and misrepresents the literature.** It states “no new method for performing backpropagation has been proposed,” which is false. Many alternatives exist (e.g., feedback alignment, synthetic gradients, equilibrium propagation, difference target propagation). The paper does not discuss any related work on alternative backpropagation or gradient approximation methods, making it impossible to assess the contribution relative to existing approaches.

- **The method’s handling of numerical issues is ad hoc and not analyzed.** The inverse sigmoid requires clipping \(a\) to \((10^{-16}, 1-10^{-16})\), and \(z' - z\) is forced to 1 when zero. These constraints introduce biases that are not studied. The paper claims DBP avoids gradient vanishing, but the sigmoid still saturates; the difference-based gradient may be larger in some regimes, but no theoretical or empirical analysis is provided to support this claim.

### Minor

- The paper is poorly structured and lacks clarity. The algorithm is described in a single paragraph with confusing notation (e.g., \(a'\) is used both as the updated activation and as a variable in the gradient formula). The figures are not well explained and the captions are repetitive.
- The introduction lists many large datasets and models (ImageNet, BERT, V-MoE) that are not used in the experiments, giving a misleading impression of the paper’s scope.

### Trivial

- Some references are irrelevant to the paper’s content (e.g., Twitter100k, BuildingNet, TextCaps are mentioned but never used).

## Nice-to-Haves

- A rigorous theoretical analysis of the proposed update rule: what objective does it optimize? Under what conditions does it converge?
- Experiments on standard benchmarks (e.g., MNIST, CIFAR) with proper statistical evaluation (multiple seeds, error bars) and comparison to standard optimizers and other alternative backpropagation methods.
- An ablation study to understand the effect of the clipping thresholds and the learning rate on the method’s behavior.

## Novel Insights

None beyond the paper’s own contributions. The core idea of using a finite-difference slope computed via the inverse function is not new in the context of numerical optimization, and the paper does not provide a principled reason why this should outperform standard backpropagation.

## Suggestions

- The authors should reconsider the formulation: the proposed update is not a gradient; it is a finite-difference approximation that depends on the learning rate. They should clarify what optimization problem this solves and provide a convergence analysis.
- Conduct experiments with multiple random seeds and report mean and standard deviation. Compare with standard optimizers (SGD, Adam) and with a simple finite-difference gradient approximation to isolate the effect of the inverse sigmoid.
- Discuss related work on alternative backpropagation methods (e.g., feedback alignment, target propagation) and explain how DBP differs.

## Score and Decision

**Score:** 1  
**Decision:** Reject

MY FINAL SCORE: <score>1</score>  
MY FINAL DECISION: <decision>Reject</decision>