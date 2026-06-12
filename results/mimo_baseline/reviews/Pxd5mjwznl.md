## Summary

The paper proposes "Difference Back Propagation" (DBP), which replaces the derivative-based chain rule for the sigmoid activation function with a finite difference computed using the inverse sigmoid. The authors claim this maintains "consistency" between pre- and post-activation neuron values during training, and demonstrate marginal improvements on toy problems and a small transformer experiment.

## Strengths

- The paper identifies an interesting observation: with finite learning rates, the derivative is a linear approximation of the actual nonlinear mapping, and the update to z does not correspond exactly to the update to a under the activation function. This is a legitimate observation about the mechanics of gradient descent.
- The idea of using the inverse activation function to enforce consistency between neuron values is at least novel, and the paper is concise and mostly clear in its presentation.

## Weaknesses

### Fatal
- **Flawed core premise**: The central claim—that the update to z should satisfy z_updated = inv_sig(a_updated)—is not justified from an optimization-theoretic perspective and reflects a conceptual misunderstanding. In gradient-based optimization, you update each parameter by following the gradient of the loss. The fact that z_updated ≠ inv_sig(a_updated) is not an "inconsistency" or a flaw; it is the expected behavior of gradient descent applied to a parameterized function. The loss is not a function of a alone—it depends on the entire computation graph. The paper provides no theoretical analysis (e.g., convergence guarantees, fixed-point analysis, or connection to known optimization frameworks) to justify why enforcing this "consistency" would lead to better optima or faster convergence.

### Major
- **Circular dependency baked into gradient computation**: The method requires computing a' = a − lr·∂l/∂a, then z' = inv_sig(a'), then using (a'−a)/(z'−z) as the effective gradient. This means the learning rate is embedded directly into the gradient computation, making the "gradient" dependent on the hyperparameter lr. This is not a gradient in any standard sense—it is an ad hoc modification that conflates the optimization direction with the step size. The paper does not analyze the implications of this conflation or how it interacts with learning rate schedules, momentum, or adaptive optimizers like Adam.
- **Extremely weak experimental evaluation**: The primary experiments use (1,2,1) and (1,2,2,1) networks trained on 100 synthetic data points with a scaled cosine function. These are toy problems from which no meaningful conclusions about the method's utility can be drawn. No real-world benchmarks, no scaling experiments, no ablation studies, no error bars or multiple random seeds, and no comparison with properly tuned baselines are provided. The transformer experiment on AG News (Fig. 5) is slightly more convincing but is still a single run on a small model with insufficient detail to evaluate.

### Minor
- **Fairness of comparison**: The standard backpropagation baseline does not appear to be independently tuned (e.g., with different learning rates) to match the effective step size that DBP implicitly uses. The observed marginal improvement could simply reflect that DBP is implicitly scaling the gradient differently, which is achievable with a learning rate adjustment.
- **Limited scope of analysis**: The paper only considers the sigmoid activation function in detail. Claims about applicability to non-differentiable functions (e.g., leaky ReLU) are stated but not demonstrated, and the inverse of leaky ReLU is itself not well-defined at zero.
- **No analysis of computational cost**: Each neuron requires computing an inverse sigmoid (logarithm) and a division, adding overhead that is not quantified or discussed for scalability.

### Trivial
- The paper states "To our knowledge, no new method for performing backpropagation has been proposed," which ignores a large body of work on alternatives to standard backpropagation (e.g., feedback alignment, target propagation, forward-forward algorithm, synthetic gradients).

## Nice-to-Haves

- A formal analysis of the convergence properties of DBP compared to standard backpropagation, even in the simplest setting (e.g., a single sigmoid neuron).
- Experiments on standard benchmarks with properly tuned baselines and multiple seeds to establish statistical significance.

## Novel Insights

The observation that the derivative and the finite difference of sigmoid diverge for large |z| is not itself new, but the specific proposal to use the inverse sigmoid to compute a difference-based "gradient" and incorporate it into backpropagation is at least a novel formulation. However, without theoretical grounding or convincing empirical evidence, the insight remains speculative. The paper does not convincingly demonstrate that the "inconsistency" it identifies actually causes problems in practice, nor that DBP resolves any real limitation of backpropagation.

## Suggestions

- Provide a theoretical analysis showing under what conditions (if any) DBP converges to a better solution than standard backpropagation, or at least analyze the fixed points of the modified update rule.
- Replace toy experiments with experiments on standard benchmarks (CIFAR-10, MNIST, etc.) using reasonable architectures, with properly tuned baselines and multiple random seeds.
- Clarify the relationship between DBP and known methods—it may be interpretable as a particular preconditioning or as an approximation to a second-order method, which would connect it to established literature.

MY FINAL SCORE: <score>2</score>
MY FINAL DECISION: <decision>Reject</decision>