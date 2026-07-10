## Summary

This paper proposes a theoretical framework explaining how saddle-to-saddle dynamics drives a simplicity bias in neural network training. The framework has three components: (1) a hierarchy of embedded fixed points (Theorem 1), showing that minima of narrower networks are saddles in wider networks; (2) invariant manifolds (Theorem 3), showing that certain weight relationships are preserved under gradient flow, corresponding to "effectively narrower" networks; and (3) dynamics arguments connecting timescale separation (data-driven for linear activations, initialization-driven for quadratic activations) to evolution near these invariant manifolds. The theory is developed for two-layer networks with homogeneous polynomial activations (linear and quadratic), with experimental evidence extending to ReLU, convolutional, and linear self-attention architectures.

## Strengths

- **A clean unifying formalism.** Equation (1) captures fully-connected, convolutional, and attention-based layers within a single mathematical structure. This enables Theorems 1 and 3 to be stated and proven once, simultaneously covering all these architectures, extending prior work (Fukumizu & Amari, 2000) that was restricted to two-layer fully-connected networks.

- **New fixed-point constructions that matter for dynamics.** Theorem 1's items (vi) and (vii) go beyond known embeddings. Remark 1 importantly shows that the fixed points actually visited during learning (Figure 1B-G) fall under constructions (v), (vi), and (vii), not the generic construction (iv) from Fukumizu & Amari. This extension is necessary for the dynamical story.

- **Invariant manifold analysis (Theorem 3).** The observation that certain weight relationships are preserved under gradient flow, combined with the connection to effective width, gives a clean geometric picture of how dynamics cannot leave certain low-complexity subspaces once it enters them.

- **Disentangling two mechanisms.** The distinction between data-driven timescale separation (linear case, Section 5.1) and initialization-driven timescale separation (quadratic case, Section 5.2) is clear and well-supported. This resolves an ambiguity in the literature by showing both are instances of the same saddle-to-saddle framework.

- **Concrete, testable predictions.** Section 6 makes specific predictions about the effects of width, data distribution, and initialization on plateau structure (Figure 2). The contrast between linear networks (width doesn't matter) and quadratic/self-attention networks (width shortens plateaus) is sharp and testable.

## Weaknesses

### Major

- **Framing gap between abstract/intro and scope of dynamical analysis.** The abstract claims to "show" that "ReLU networks learn solutions with an increasing number of kinks" and "self-attention models learn solutions with an increasing number of attention heads," and that the framework incorporates "fully-connected, convolutional, and attention-based architectures." However, the formal dynamical analysis (Section 5) is carried out only for two-layer networks where φ is a homogeneous polynomial in the weights (linear or quadratic). The paper is transparent about this on line 122 ("To analyze learning dynamics, however, we must work with concrete architectures"), but the abstract creates an impression of broader theoretical coverage than the body delivers. For ReLU networks, the evidence is experimental (Figure 1D,E) and the fixed-point/invariant-manifold theory applies (Theorems 1(iii), 3(iii)), but no formal dynamical analysis is provided. For self-attention, the analysis covers "linear self-attention" (softmax removed), whereas real self-attention uses softmax nonlinearity. For convolutional networks, the analysis covers "linear convolutional" networks. This is a significant framing issue that should be corrected.

- **The central link between timescale separation and invariant manifold dynamics is heuristic, not rigorously proven.** The paper shows (Theorem 4) that weights in linear networks become approximately low-rank and (Proposition 5) that one unit dominates in quadratic networks. It also shows (Theorem 3) that exactly low-rank or exactly sparse weights lie on invariant manifolds. However, the paper does not prove that *approximate* behavior (nearly low-rank, nearly sparse) implies the trajectory stays near the true invariant manifold, nor does it bound the approximation error. The paper acknowledges this on line 118 ("we develop heuristic arguments"), but the core mechanism — that saddle-to-saddle dynamics arises from the interplay of timescale separation and invariant manifolds — rests on this unclosed gap.

- **The experimental validation is too narrow to support the breadth of the claims.** Section 6 tests only linear fully-connected and linear self-attention networks on synthetic data with power-law singular values. It does not test predictions on ReLU networks, nonlinear convolutional networks, or any real-world dataset. The paper claims to "validate our theory and demonstrate its predictive power" (line 206), but the evidence is largely illustrative of internal consistency for the architectures already covered by the formal analysis, rather than independent empirical validation of the broader claims.

### Minor

- **The related work discussion in the main text is notably brief** (one paragraph, lines 33) given the breadth of the claims. The paper does not clearly delineate in the main text how its dynamical analysis goes beyond existing work on deep linear networks (Saxe et al., 2014, 2019) that already studied saddle-to-saddle dynamics governed by singular value gaps. The paper references Appendix A for a more detailed treatment.

## Nice-to-Haves

- A perturbation analysis or attraction argument connecting approximate low-rank/sparse behavior to nearness of invariant manifolds would turn the central heuristic into a theorem — this is the single highest-leverage improvement.
- Testing predictions on a non-synthetic problem (e.g., a small-scale real dataset with measurable plateau structure) would increase confidence that the theory captures real learning phenomena.
- A more explicit discussion relating the effective-width notion of simplicity to other definitions (e.g., spectral bias in Rahaman et al., 2019) would strengthen the connection to the broader simplicity bias literature.

## Removed Points

These points were flagged to be removed; treat with caution:

- "The framing is unfair to existing literature" — subjective judgment, not a verifiable weakness.
- "Scalar output case for quadratic networks limits generality" — paper explains the choice (line 170); reasonable design decision.
- "No comparison to lazy/feature learning literature" — paper discusses this in Section 6 (line 214); partially outside stated scope.
- "Definition of simplicity not connected to broader simplicity bias literature" — scope creep; paper defines simplicity on its own terms.
- "No error bars / statistical rigor" — single-run plots are standard for theory papers.
- Criticisms about missing appendix content — hard rule: parser strips appendices; they exist in original submission.
- "Figure 2 model sizes are tiny" — H=800 for linear networks is substantial; H=25 for self-attention is a design choice.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Revise the abstract and introduction to precisely match the scope of the formal dynamical analysis, explicitly noting that the formal analysis covers two-layer networks with linear/quadratic polynomial activations while the structural results (fixed points, invariant manifolds) hold more broadly.
2. Add a perturbation analysis attractive argument bridging approximate to exact invariant manifold behavior.
3. Include at least one experiment on a non-synthetic problem with measurable plateau structure.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>