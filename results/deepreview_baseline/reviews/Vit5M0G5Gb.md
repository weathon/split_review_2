## Summary

This paper proposes a theoretical framework explaining simplicity bias in neural networks through saddle-to-saddle learning dynamics. The authors show that for a broad class of architectures (linear, ReLU, convolutional, quadratic, and linear self-attention networks), fixed points of narrower networks are embedded as saddle points in wider networks, connected by invariant manifolds that preserve simplicity. The key insight is that timescale separation—either between directions (data-induced) or between units (initialization-induced)—steers gradient descent along these invariant manifolds, causing networks to progressively recruit additional effective units (neurons, kernels, or attention heads) and learn increasingly complex solutions.

## Strengths

- **Unifying theoretical framework**: The paper provides a single mathematical framework (Theorem 1 on embedded fixed points, Theorem 3 on invariant manifolds) that applies across fully-connected, convolutional, and attention-based architectures, which is a significant advance over prior architecture-specific analyses.

- **Clear mechanistic distinction**: The identification of two distinct mechanisms for timescale separation—between directions (linear case, data-driven) versus between units (quadratic case, initialization-driven)—is insightful and leads to testable predictions about how width, data distribution, and initialization affect learning dynamics.

- **Predictive power validated by experiments**: The paper makes specific, falsifiable predictions (e.g., increasing width shortens plateaus in self-attention but not linear networks; power-law data exponents affect plateau length) and validates them with simulations in Figure 2.

- **Rigorous mathematical foundation**: Theorems 1 and 3 are clean, general, and proven carefully. The analysis of dynamics in Sections 5.1 and 5.2, while heuristic, is grounded in explicit calculations and provides genuine insight.

## Weaknesses

### Major

- **Dynamics analysis is heuristic, not rigorous**: Sections 5.1 and 5.2 analyze approximate dynamics (Equations 10 and 14) rather than the true gradient flow. The paper acknowledges this ("heuristic arguments") but the gap between the rigorous fixed point/invariant manifold theory and the dynamics analysis is substantial. Theorem 4 and Proposition 5 analyze simplified systems, and the connection to actual gradient flow trajectories is argued rather than proven. This limits the paper's contribution as a *theory* of learning dynamics.

- **The "simplicity bias" claim is overstated**: The paper claims to "explain a simplicity bias across neural network architectures," but the analysis only covers two-layer networks for dynamics. Deep networks are discussed only via conjecture (Section 7, "Deep networks" paragraph). Given that practical neural networks are deep, the claim of explaining simplicity bias "across architectures" is not fully supported by the analysis presented.

- **Limited novelty relative to prior work**: The embedded fixed points (Theorem 1, cases i and ii) were discovered by Fukumizu & Amari (2000). The invariant manifold for equal weights (Theorem 3, case i) is straightforward. The main novel theoretical contributions are the extended fixed point constructions (cases iii and iv) and the invariant manifolds for proportional/linearly dependent weights. While valuable, the core insight that saddle-to-saddle dynamics explains progressive learning has been explored in prior work cited by the authors (Jacot et al., 2022; Berthier, 2023; Pesme & Flammarion, 2023).

### Minor

- **The definition of "simplicity" is circular in places**: Simplicity is defined as "expressible with few hidden units." But the paper then shows that networks learn solutions expressible with few units. This is somewhat tautological—the conclusion is built into the definition.

- **The quadratic case analysis is limited**: Proposition 5 analyzes a simplified system (Equation 14) and uses a scalar toy example ($\dot{v}_i = v_i^2$) to build intuition. The actual dynamics (Equation 44 in Appendix) is more complex, and the claim that "the timescale separation between units essentially comes from the same mechanism" is not fully justified.

### Trivial

- The paper uses "saddle-to-saddle dynamics" to describe what is sometimes called "progressive learning" or "stage-wise learning" in the literature; this terminological choice is fine but worth noting.

## Nice-to-Haves

- A more rigorous analysis of the dynamics, perhaps proving that gradient flow trajectories stay close to the invariant manifolds for a quantified duration, would significantly strengthen the paper.
- Experimental validation on deeper networks (beyond two layers) would make the "across architectures" claim more convincing.
- Discussion of how the theory relates to the "grokking" phenomenon (delayed generalization) would be interesting, as grokking exhibits similar stage-like dynamics.

## Novel Insights

The paper's most novel insight is the distinction between data-induced timescale separation (between directions, leading to low-rank weights) and initialization-induced timescale separation (between units, leading to sparse weights). This provides a principled explanation for why different architectures exhibit qualitatively different learning dynamics and why the same architecture can show either stage-like or smooth learning depending on initialization. The observation that increasing width can *shorten* plateaus in self-attention (but not linear networks) is counterintuitive and practically relevant.

## Suggestions

- Consider adding a theorem or proposition that bounds the distance between the true gradient flow trajectory and the approximate dynamics analyzed in Sections 5.1 and 5.2, even under restricted conditions (e.g., for sufficiently small initialization or short time intervals).

## Score and Decision

The paper makes a genuine contribution by providing a unified theoretical framework for understanding simplicity bias across architectures, with clean mathematical results on fixed points and invariant manifolds. However, the dynamics analysis—which is central to the paper's claims about explaining learning behavior—remains heuristic rather than rigorous. The paper is well-written, the experiments support the qualitative predictions, and the framework is likely to be influential. But the gap between the rigorous theory (fixed points, invariant manifolds) and the heuristic dynamics analysis prevents this from being a fully satisfying theoretical contribution.

MY FINAL SCORE: 6.0</score>
MY FINAL DECISION: Accept</decision>