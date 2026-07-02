## Summary

The paper proposes a new backpropagation algorithm called “Difference Back Propagation” (DBP) that replaces the derivative of the sigmoid activation function with a finite-difference quotient computed using the inverse sigmoid function. The goal is to maintain consistency between pre- and post-activation neuron updates under finite learning rates and to mitigate vanishing gradients. Experiments on tiny MLPs and a small transformer show marginal improvements in convergence speed and final accuracy compared to standard backpropagation.

## Strengths

- **Novel idea**: Replacing the analytic derivative with a finite difference computed via the inverse activation function is a genuinely new modification to backpropagation that has not, to my knowledge, been explored before.
- **Identifies a real inconsistency**: The paper correctly notes that with a finite learning rate, the update to the pre-activation value \(z\) via gradient descent is not consistent with the update to the post-activation value \(a\) through the sigmoid function; DBP attempts to restore that consistency.
- **Potential to avoid vanishing gradients**: Because the difference quotient \(\frac{a' - a}{z' - z}\) does not rely on the derivative \(a(1-a)\), it does not become arbitrarily close to zero when the sigmoid saturates, offering a potential benefit for deep networks using sigmoid activations.

## Weaknesses

### Fatal
None.

### Major

1. **Lack of theoretical justification**: DBP is not derived from a principled optimization framework. The update rule is ad-hoc: first update \(a\) via gradient descent on \(a\), then apply the inverse sigmoid to obtain a candidate \(z'\), then use the ratio \(\frac{a'-a}{z'-z}\) as a multiplicative factor in the gradient for \(z\). The paper does not show that this procedure corresponds to any standard optimization method (e.g., gradient descent on a reparameterized loss) or that it converges to a stationary point of the original loss. Without theory, the method is a heuristic whose behavior is unclear.

2. **Insufficient experimental validation**:
   - Experiments are limited to tiny models: a (1,2,1) MLP on 100 synthetic points and a (1,2,2,1) MLP on the same data. The only non-toy experiment is a small transformer (d_model=32, 2 layers) on AG News, which shows tiny improvements (accuracy near 99% for both methods).
   - No error bars, multiple seeds, or statistical tests are reported; the claimed improvements may not be significant.
   - The paper does not test on standard benchmarks (MNIST, CIFAR-10, etc.) or with larger models, despite motivating the work with large-scale deep learning.
   - The method is only concretely defined for sigmoid; the claim of generality to any invertible function is not demonstrated.

3. **Incomplete algorithmic specification and practical issues**:
   - The inverse sigmoid has domain (0,1), requiring clamping of \(a\) to \((10^{-16}, 1-10^{-16})\). This ad-hoc clipping is not principled and may affect training.
   - The paper mentions using Taylor expansion to handle \(a\) near 1 but does not implement it; instead it relies on clamping.
   - The computation of the inverse sigmoid at every neuron and every step adds overhead compared to the derivative, which is not discussed.
   - The method as described requires computing the updated \(a\) before backpropagating through the layer, which mixes forward and backward computations and could complicate implementation in standard frameworks.

### Minor

- The claim that “no new method for performing backpropagation has been proposed” is an overstatement; many alternatives exist (e.g., feedback alignment, synthetic gradients), though they do not exactly replace the derivative with a finite difference in this way.
- The motivation about large models and big data is generic and disconnected from the tiny experiments actually performed.
- The paper states the code will be open-sourced later; at review time there is no code to verify the results.

### Trivial

- Some figure descriptions are difficult to parse (parser artifacts), but the core content is still understandable.

## Nice-to-Haves

- Provide a theoretical analysis: prove that DBP is equivalent to gradient descent on a consistent discretization or under some reparameterization, or at least show convergence to a stationary point in a simplified setting.
- Evaluate on standard benchmarks (e.g., MNIST, CIFAR-10) with moderate-sized networks and sigmoid activations, comparing directly with standard backprop and other anti-vanishing-gradient techniques.
- Show explicit applications to other activation functions (tanh, ReLU with a preimage approximation) to substantiate the claim of generality.
- Report computational cost and wall-clock time, not just iteration count.
- Include multiple runs with error bars to assess statistical significance of the small observed improvements.

## Novel Insights

None beyond the paper’s own contributions: the core idea of using the inverse activation function to compute a finite-difference “gradient” is novel, but the paper does not provide deeper insight beyond the initial observation of inconsistency.

## Suggestions

- Derive DBP from a formal optimization perspective, e.g., as gradient descent on a loss that is reparameterized via the inverse sigmoid, or as a form of alternating minimization that ensures consistency.
- Replace the ad-hoc clamping with a principled approach (e.g., the suggested Taylor expansion or log-space computation).
- Run experiments on a standard task like MNIST with a small fully-connected network using sigmoid, and include at least 5 seeds per method with error bars.
- Discuss the computational overhead of computing the inverse sigmoid versus the derivative, and consider approximations if needed.

## Score and Decision

The paper introduces a novel modification to backpropagation, but it lacks theoretical grounding and sufficient experimental validation. The experiments are on tiny toy problems with marginal improvements, and the method is not fully specified for general use. For a top venue like ICLR, the contribution is not yet convincing or impactful enough. I recommend rejection.

**MY FINAL SCORE:** <score>3</score>  
**MY FINAL DECISION:** Reject