## Summary

This paper proposes a theoretical framework explaining simplicity bias in neural networks through saddle-to-saddle learning dynamics. The authors show that for a broad class of architectures (linear, ReLU, convolutional, quadratic, and linear self-attention networks), gradient descent visits a sequence of saddles corresponding to solutions expressible with progressively more "effective units" (hidden neurons, kernels, or attention heads). The framework identifies two mechanisms for timescale separation—data-induced (between directions) and initialization-induced (between units)—that drive the dynamics along invariant manifolds connecting embedded fixed points.

## Strengths

- **Unifying theoretical framework**: The paper provides a single mathematical formalism (Equation 1) that encompasses fully-connected, convolutional, and attention-based architectures, and derives general results about embedded fixed points (Theorem 1) and invariant manifolds (Theorem 3) that hold across these architectures. This is a genuine theoretical contribution that goes beyond prior work which focused on specific architectures.

- **Clear mechanistic explanation**: The paper convincingly disentangles two distinct mechanisms for saddle-to-saddle dynamics—timescale separation between directions (linear case, data-driven) versus between units (quadratic case, initialization-driven)—and shows how these lead to qualitatively different behaviors (low-rank vs. sparse weights). The analysis of how data distribution and initialization affect plateau duration (Figure 2) provides testable predictions.

- **Rigorous theoretical results**: Theorems 1 and 3 are clean, well-proven results about the loss landscape and dynamics. The analysis of the linear case (Theorem 4) and quadratic case (Proposition 5) provides concrete mathematical grounding for the claimed mechanisms.

## Weaknesses

### Major

- **Gap between theory and experiments for deep networks**: The paper's dynamical analysis (Section 5) is limited to two-layer networks, yet the experiments in Figure 5 show deep networks. The authors acknowledge this limitation but the "conjecture" about deep networks (Section 7) is not supported by any theoretical analysis. Given that the paper's title claims to explain simplicity bias "across neural network architectures," the lack of dynamical analysis for deep networks is a significant gap.

- **The quadratic case analysis is heuristic**: Proposition 5 analyzes a simplified dynamical system (Equation 14) that drops the data-dependent terms. The authors then use a scalar analogy ($\dot{v}_i = v_i^2$) to argue for timescale separation. While the intuition is plausible, the analysis does not rigorously connect the simplified dynamics to the actual gradient flow dynamics of quadratic networks. The claim that "the general case... is more complicated" (Section 5.2) but the timescale separation "essentially comes from the same mechanism" is not fully justified.

- **Limited empirical validation of predictions**: Figure 2 tests predictions about width, data distribution, and initialization, but only for linear networks and linear self-attention. The paper would be stronger with empirical validation for ReLU networks, convolutional networks, and quadratic networks under the same experimental manipulations.

### Minor

- The paper claims that "saddle-to-saddle dynamics depends on two conditions" (Section 7) but does not provide a formal characterization of when these conditions are met. The discussion of tanh networks as a counterexample is qualitative.

- The connection between "simplicity" (number of effective units) and the actual complexity of learned functions could be more precisely characterized. The paper defines simplicity as "expressible with few hidden units" but does not discuss whether this notion of simplicity aligns with other measures (e.g., function smoothness, spectral complexity).

### Trivial

- The notation in Equation (2) for self-attention is non-standard and somewhat forced; the paper acknowledges this but it may confuse readers.

## Nice-to-Haves

- A more formal treatment of when saddle-to-saddle dynamics breaks down (e.g., for tanh networks) would strengthen the paper's claims about the conditions for simplicity bias.
- Analysis of how skip connections in transformers affect the invariant manifold structure would be valuable.
- Discussion of whether the framework extends to modern architectures like mixture-of-experts or normalization layers.

## Novel Insights

The paper's key insight is that permutation symmetry of units in feed-forward networks creates a nested hierarchy of fixed points and invariant manifolds, and that the specific properties of the activation function (linear vs. quadratic in weights) determine whether timescale separation occurs between directions or between units. This provides a principled explanation for why some architectures exhibit stage-like learning while others do not, and why the effect of scaling width differs between fully-connected networks and attention-based models. The distinction between data-induced and initialization-induced saddle-to-saddle dynamics is particularly novel and has practical implications for understanding when feature learning occurs.

## Suggestions

- Strengthen the dynamical analysis for the quadratic case by providing a more rigorous connection between the simplified dynamics (Equation 14) and the full gradient flow dynamics, perhaps through perturbation analysis or by identifying a Lyapunov function.
- Add experiments testing the predictions about data distribution and initialization effects for ReLU and convolutional networks to demonstrate the framework's generality beyond linear/quadratic cases.
- Clarify the relationship between the paper's notion of simplicity (number of effective units) and other established measures of function complexity in the literature.

## Score and Decision

The paper makes a genuine theoretical contribution by providing a unified framework for understanding simplicity bias across multiple architectures. The results on embedded fixed points and invariant manifolds are clean and general. However, the dynamical analysis is limited to two-layer networks, and the quadratic case analysis is heuristic rather than rigorous. The paper's claims about "across architectures" are partially supported by the fixed point/invariant manifold analysis but not fully by the dynamical analysis. The paper is a solid contribution that advances our theoretical understanding, but the gaps in the dynamical analysis for deep networks and the heuristic treatment of the quadratic case prevent it from being a definitive treatment.

MY FINAL SCORE: 6.0score</score>
MY FINAL DECISION: Accept</decision>