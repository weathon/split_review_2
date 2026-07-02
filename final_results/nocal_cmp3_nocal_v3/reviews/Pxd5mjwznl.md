## Summary

This paper proposes Difference Back Propagation (DBP), a modification to standard backpropagation for sigmoid activation functions. Instead of using the derivative \(a(1-a)\) in the chain rule \(\frac{dl}{dz} = \frac{dl}{da} \cdot \frac{da}{dz}\), DBP replaces \(\frac{da}{dz}\) with a finite-difference ratio \(\frac{a' - a}{z' - z}\), where \(a' = a - \text{lr} \cdot \frac{dl}{da}\) and \(z' = \text{inv\_sigmoid}(a')\). The paper claims this improves gradient fidelity for finite learning rates and alleviates vanishing gradients, and presents experiments on tiny networks (3–5 neurons) and a small transformer.

## Strengths

- **The core observation is mathematically sound.** With a finite (non-infinitesimal) learning rate, the derivative \(\frac{da}{dz}\) at a single point is only a local linear approximation of the sigmoid, and the actual change in \(a\) for a finite step in \(z\) can differ from this approximation. This is correctly noted in Section 2 and illustrated in Figure 1.
- **The paper correctly identifies a practical nuisance with sigmoid.** When \(z > 36\), float64 precision makes \(a\) indistinguishable from 1, causing the derivative to evaluate to exactly 0 (Section 2). Using a finite-difference approach conceptually sidesteps this issue.
- **The proposed modification is simple to state.** The formula in Eq. 6 is straightforward and the paper's explanation of the computation is clear enough to replicate.

## Weaknesses

### Major

1. **The motivation for DBP rests on a model of training that does not match how neural networks are actually optimized.**  
   The paper's "inconsistency" argument (Eq. 3–4, Section 2) treats the activation \(a\) as a free parameter that is directly updated via \(a_{\text{updated}} = a - \text{lr} \cdot \frac{dl}{da}\). In actual neural network training, gradients are computed with respect to *weights and biases*, not activations. Activations are deterministic functions of the weights and input; they are not independent variables that can be "updated" separately. The supposed inconsistency between the derivative-predicted \(z'\) and \(\text{inv\_sig}(a')\) does not arise in real training because weight updates automatically preserve the functional relationship between \(z\) and \(a\) through the next forward pass. The paper's core motivation is built on a conceptual model that does not correspond to how neural networks are actually optimized.

2. **DBP produces a learning-rate-dependent quantity whose optimization properties are entirely uncharacterized.**  
   The proposed gradient \(\frac{dl}{dz} = \frac{a' - a}{z' - z} \cdot \frac{dl}{da}\) depends on the learning rate \(lr\) through \(a' = a - lr \cdot \frac{dl}{da}\) and \(z' = \text{inv\_sig}(a')\). This means DBP does not compute the gradient of any fixed objective function — the "gradient" changes when the learning rate changes, even before the optimizer applies it. The paper provides no analysis of what optimization landscape DBP navigates, whether it converges to stationary points of the loss, or even whether it guarantees descent on any well-defined quantity. Without such characterization, DBP is not validated as an optimization algorithm; it is a heuristic whose behavior (even in the limit \(lr \to 0\)) is unexamined.

3. **The experimental evaluation is far too weak to support the paper's claims.**  
   - The primary experiments are on a \((1,2,1)\) network (3 neurons, 5 parameters) and a \((1,2,2,1)\) network, trained on 100 synthetic data points from an unspecified scaled cosine function.  
   - No train/test split is used on the synthetic data because "generalizability or over-fitting is not under consideration" (Section 3). This means the results only show training fit, not generalization — the actual goal of machine learning.  
   - No standard benchmarks are evaluated (MNIST, CIFAR-10, or any commonly used dataset).  
   - No comparisons against standard optimizers beyond basic gradient descent (Adam, SGD with momentum, etc.) are provided.  
   - No statistical significance is reported: all curves appear to be single runs with no seed averaging or error bars.  
   - The transformer experiment (d_model=32, 2 layers, 4 heads on AG News) shows a sub-1% accuracy difference with no indication of whether this is consistent across multiple seeds.  
   - No ablation studies, learning rate sensitivity analysis, or investigation of the clipping thresholds (\(10^{-16}\) bounds on \(a\)) are performed.  
   - Claiming that a method affects training dynamics at the scale of LLMs while evaluating only on networks with \(\leq 10\) parameters is not supported evidence.

### Minor

4. **The paper's claim about novelty is inaccurate.**  
   Section 1 states: "To our knowledge, no new method for performing backpropagation has been proposed." This is an overstatement. There exists a substantial literature on alternatives and modifications to standard backpropagation (e.g., biologically plausible learning rules, feedback alignment, forward-mode differentiation variants, equilibrium propagation). Even if the paper intends a narrower claim about replacing the derivative with a finite-difference at the activation function, that should be stated precisely and contextualized against known finite-difference and zeroth-order optimization methods (e.g., SPSA). The current claim is unnecessarily broad and undermines confidence in the paper's scholarship.

5. **The motivation (large-scale models with billions of parameters) is disconnected from the evaluation scale.**  
   The introduction discusses BERT (110M parameters) and V-MoE (15B parameters) and suggests DBP could affect outcomes at that scale. The largest network evaluated has parameters in the single digits (excluding the small transformer). There is no discussion of how DBP would scale, whether the computational overhead of computing \(\text{inv\_sigmoid}\) per neuron is acceptable at scale, or whether the clipping operations cause issues in deeper networks where activations naturally saturate. The evaluation does not engage with the scaling narrative that motivates the work.

6. **A critical numerical issue is deferred.**  
   The inverse sigmoid requires \(a \in (0,1)\) exclusively, but the sigmoid output approaches 1 asymptotically. The paper mentions that "This problem can be solved by utilizing the Taylor Expansion... This is beyond the scope of this paper" (Section 2). Since the numerical handling of near-saturated activations is central to whether DBP works in practice (especially for preventing the very vanishing-gradient problem it claims to solve), deferring this is a significant gap. The paper instead sets an arbitrary constraint \(a \in (10^{-16}, 1 - 10^{-16})\) with no analysis of how this affects optimization or in which regimes it breaks down.

### Trivial

- None.

## Nice-to-Haves

- Establish whether DBP descends a well-defined objective. A derivation of what quantity DBP minimizes, or at minimum an empirical demonstration that it converges to known global optima on tractable problems, would ground the method.
- Evaluate on at least one standard benchmark (e.g., CIFAR-10 with a small CNN) with proper statistical reporting (multiple seeds, confidence intervals).
- Compare DBP against standard techniques that address similar sigmoid issues, such as gradient clipping or alternative activation functions (ReLU, tanh).
- Analyze the computational overhead of computing \(\text{inv\_sigmoid}\) per neuron at practical scales.

## Removed Points

- **"Circular dependency" in DBP formula:** The reviewer claimed the gradient \(\frac{dl}{dz}\) creates a circular dependency. In the actual backward pass, \(\frac{dl}{da}\) is received from the next layer first, then \(a'\), then \(z'\), then \(\frac{dl}{dz}\) — the computation is feed-forward, not circular. The broader concern (that DBP does not compute a true gradient) is retained in Major weakness #2.
- **"No code release":** The paper states code will be released after the double-blind review period. This is standard practice and not a valid criticism of the submission.
- **"The paper claims generality for other activation functions but only tests sigmoid":** This is a real limitation, but it is already subsumed by Major weakness #3 (the entire evaluation is too weak).
- **Strawman claim about "the paper neglects the massive innovation in optimizers (Adam, AdamW, RMSprop)":** The paper's introduction says models "have been using the same derivative-based back propagation algorithm" — this statement is about the gradient computation mechanism, not about optimizers. The paper is referring to the chain-rule gradient computation, not the parameter update rule. This criticism conflates two different components of training.
- **Pure section-by-section notes and formatting observations:** These are either subsumed by the main weaknesses or are speculations not anchored to specific paper content.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Re-evaluate whether the inconsistency identified in Eq. 3–4 is a genuine issue in weight-space optimization, or only an artifact of treating activations as directly updated parameters. If the latter, the paper's motivation needs fundamental rethinking.
2. Characterize the relationship between DBP's update direction and the true gradient — under what conditions do they coincide or diverge? Does DBP correspond to a valid first-order optimization method for any well-defined objective?
3. Substantially expand the experimental evaluation to at least one standard small-scale benchmark (e.g., MNIST with a fully-connected network, CIFAR-10 with a small CNN) with multiple random seeds, error bars, and comparisons with standard optimizers.

## Score and Decision

This paper identifies a mathematically valid observation about finite learning rates and sigmoid activations, but the contribution is not viable in its current form. The core argument motivating DBP is built on an incorrect model of how training updates interact with activations (treating activations as directly updatable parameters). The proposed formula produces a learning-rate-dependent quantity whose optimization landscape is uncharacterized, and the experimental evaluation is orders of magnitude too weak to support the claimed contribution. The gap between the motivational framing (billions of parameters) and the evidence (networks with <10 parameters) is severe.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>