## Summary

This paper develops a unifying theoretical framework for understanding dynamical simplicity bias in neural networks through saddle-to-saddle dynamics. The authors show that for a broad class of architectures (linear, ReLU, convolutional, quadratic, self-attention), fixed points of narrower networks are recursively embedded as saddle points in wider networks (Theorem 1), that invariant manifolds constrain networks to behave as if they have fewer effective units (Theorem 3), and that timescale separation—either between directions (data-induced, linear case) or between units (initialization-induced, quadratic case)—drives the dynamics along these manifolds, progressively recruiting one effective unit at a time. The framework makes testable predictions about the effects of width, data distribution, and initialization on the presence and duration of loss plateaus.

## Strengths

- **Unified framework across architectures.** The paper genuinely unifies prior results on fixed points (originally from Fukumizu & Amari 2000 for fully-connected nonlinear networks) and extends them to convolutional and attention-based architectures. The construction of embedded fixed points (Theorem 1) and invariant manifolds (Theorem 3) under a single general layer definition (Equation 1) is elegant and substantive.

- **Clean distinction between two mechanisms of timescale separation.** The decomposition into data-induced (linear case, singular values of the input-output correlation) and initialization-induced (quadratic case, "rich-get-richer" dynamics) timescale separation is a valuable conceptual contribution. This distinction generates qualitatively different predictions: e.g., increasing width has no effect on linear networks but shortens plateaus in self-attention (Figure 2A); equal singular values eliminate plateaus in linear networks but not in self-attention (Figure 2B).

- **Novel and testable predictions.** The prediction that initializing with large low-rank weights produces saddle-to-saddle dynamics without an initial plateau (Figure 2C) is novel and provides nuance to the feature learning vs. lazy learning distinction. The prediction that larger initialization scales shorten plateaus (Figure 2D) is also well-supported. These are concrete, falsifiable predictions that go beyond explaining existing observations.

- **Thorough experimental validation.** The simulations cover all major architectures discussed (linear FC, linear conv, ReLU FC, ReLU conv, linear self-attention, quadratic networks) and validate predictions across varying widths, data distributions, and initialization regimes. The paper also extends to deep networks in Figure 5, demonstrating that the mechanism persists beyond the two-layer theory.

## Weaknesses

### Fatal

None.

### Major

- **Two-layer dynamics only.** The theoretical analysis of learning dynamics (Section 5) is restricted to two-layer networks. Deep networks are discussed heuristically and experimentally (Figures 5, discussion in Section 7), but no rigorous theoretical results are provided for deep architectures. Since the paper's primary claim is a unified framework "across neural network architectures," the gap between the two-layer theory and the deep network discussion is significant. The conjecture about predicting timescale separation type via the activation's order (Section 7) remains unproven.

- **Linear self-attention as a proxy for attention.** The self-attention analysis removes the softmax nonlinearity, which is arguably the most architecturally distinctive feature of attention. The paper acknowledges this is done to show the framework's applicability, but linear self-attention is a substantially different model from standard self-attention, and the gap is not carefully discussed. The practical relevance for understanding actual transformer training is therefore limited.

- **Validation limited to simple settings.** All experiments use small-scale settings with scalar or low-dimensional inputs/outputs, simple data distributions (power-law singular values, linear or quadratic targets), and relatively small networks. While this is appropriate for validating the theory in its stated regime, it limits confidence in the framework's applicability to realistic deep learning settings. No connection to standard benchmarks or practical training scenarios is attempted.

### Minor

- **Exhaustiveness of fixed points and invariant manifolds.** The authors acknowledge (Section 7) that it is an open question whether the identified fixed points and invariant manifolds are exhaustive. If there are additional families of fixed points, the picture could be substantially more complex than described. For instance, data-dependent fixed points or invariant manifolds not arising from the architecture's symmetries could alter the dynamics.

- **The quadratic case analysis (Proposition 5) is less rigorous than the linear case (Theorem 4).** While Theorem 4 provides an explicit quantification of the separation (with exponents $\epsilon^{1-s_{r+1}/s_1}$), Proposition 5 only claims the remaining units are $O(\epsilon)$ "almost surely." The proof relies on a simplified scalar equation and heuristics about the matrix case. This is acknowledged by the structure (Proposition vs. Theorem) but the gap in rigor is notable.

- **Connection between effective units and task complexity.** The paper defines simplicity as "expressible with few hidden units" but does not connect this architectural notion of simplicity to the task-level complexity that practitioners care about. The theory does not explain why a rank-1 solution is "simpler" in any meaningful sense for the learning task.

### Trivial

None.

## Nice-to-Haves

- An explicit characterization of when the two-layer theory extends to deep networks (e.g., conditions under which each layer independently exhibits timescale separation).
- Validation with a real attention layer (with softmax) on a small-scale but non-trivial task, even if only empirically.
- A more detailed discussion of how the "effective units" notion relates to known inductive biases of architectures (e.g., convolutional networks' translation equivariance, attention's permutation equivariance).

## Novel Insights

The distinction between data-induced and initialization-induced timescale separation is genuinely novel and provides a useful organizing principle. The prediction that large low-rank initialization leads to saddle-to-saddle dynamics without initial plateaus (Figure 2C) is a new observation that refines the feature-learning/lazy-learning dichotomy. The observation that increasing the number of attention heads shortens plateaus while increasing the width of linear FC networks does not is a theoretically grounded architectural comparison that has practical implications.

## Suggestions

- Provide a more rigorous treatment of the quadratic case, or at least a formal reduction to a tractable scalar dynamical system with proven guarantees.
- Extend the experimental analysis to deeper networks (e.g., depth-3 or depth-4) to test whether the two-layer predictions hold for each layer independently.
- Include a comparison between linear self-attention and full self-attention to quantify the effect of the softmax nonlinearity on the dynamics.

## Score and Decision

The paper makes a genuine theoretical contribution by unifying fixed-point, invariant-manifold, and dynamical perspectives across multiple architectures. The framework is well-motivated, the main theorems are clean, and the predictions are validated within the stated regime. The main limitations are the restriction to two-layer networks for the dynamics analysis and the gap between the theoretical settings and practical relevance. These limitations are significant but do not invalidate the contribution. The paper would benefit from the research community as a theoretical framework that clarifies an important phenomenon and generates testable predictions.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept