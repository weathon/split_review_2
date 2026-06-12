## Summary

This paper characterizes distributional equivalence in linear non-Gaussian causal models with arbitrary latent variables and cycles. The authors introduce "edge rank" constraints as a new graphical tool, prove a duality between path ranks and edge ranks, and establish a complete graphical criterion for when two latent-variable models induce the same observed distribution set. They further provide a transformational characterization (analogous to the Meek conjecture) for traversing the equivalence class and develop the glvLiNG algorithm for recovering models from data without structural assumptions.

## Strengths

- **First general equivalence characterization with latent variables**: The paper convincingly addresses a fundamental gap in the literature. No prior work has characterized distributional equivalence in any parametric setting with arbitrary latent structure and cycles, making this a genuinely novel contribution.

- **Elegant theoretical framework**: The introduction of edge ranks and the duality theorem (Theorem 1) connecting path ranks and edge ranks is mathematically elegant and provides a genuinely new tool for the causal discovery toolbox. The reduction from global path rank constraints to local edge rank conditions is non-trivial and well-executed.

- **Clean graphical criterion**: Theorem 2 reduces equivalence checking to checking children bases for each singleton observed variable, which is computationally tractable and conceptually clean. This is a significant improvement over the naive path-rank formulation.

- **Complete transformational characterization**: Theorem 3 provides both necessary and sufficient conditions for equivalence via admissible cycle reversals and edge additions/deletions, analogous to the Meek conjecture for Markov equivalence. This is a strong theoretical result.

## Weaknesses

### Major

- **OICA reliance limits practical impact**: The authors acknowledge that glvLiNG relies on overcomplete ICA (OICA), which is known to be computationally challenging and statistically inefficient in practice. While the paper frames glvLiNG as a "proof of concept," the practical utility of the method is severely limited by this dependence. The evaluation on finite samples (Appendix D.4) is not presented in the main text, making it difficult to assess real-world performance.

- **Evaluation is thin in the main paper**: The main text provides only high-level summaries of experimental results (Tables 3-5 are mentioned but not shown). Critical details about finite-sample performance, comparison baselines, and real-data results are relegated to the appendix. For a paper claiming an algorithmic contribution, the main text should include at least representative experimental results.

- **The irreducibility condition may be restrictive**: Proposition 1 requires that each latent variable has at least two children outside itself. While this is justified as ruling out trivial unidentifiability, it excludes many practically relevant structures (e.g., a latent with exactly one observed child). The paper does not discuss how severe this restriction is in practice.

### Minor

- **The paper is dense and notation-heavy**: While the theoretical contributions are substantial, the exposition is challenging to follow. Key concepts (edge ranks, matching ranks, children bases) are introduced rapidly without sufficient intuition-building examples in the main text.

- **Limited discussion of computational complexity**: The paper claims glvLiNG is efficient but does not provide formal complexity analysis. The constraint-based approach for Phase 2 (recovering edges from observed variables) is described as "explicit construction" but the computational cost is not analyzed.

### Trivial

- The paper uses both $\stackrel{X}{\sim}$ and $\stackrel{\mathcal{D}}{\sim}$ notations for equivalence, which is slightly confusing.

## Nice-to-Haves

- A more detailed comparison with the closest prior work (Adams et al., 2021) on when linear non-Gaussian acyclic models can be uniquely identified would help contextualize the contribution.
- Providing pseudocode for the glvLiNG algorithm in the main text would improve accessibility.
- A discussion of how the equivalence class size scales with graph parameters (number of latents, observed variables, density) would be valuable.

## Novel Insights

Beyond the paper's own contributions, a genuinely novel insight is the duality between path ranks and edge ranks (Theorem 1). This reveals that the global, path-based constraints long used in causal discovery (d-separation, t-separation, rank constraints) have a local, edge-based dual that is easier to manipulate. This duality suggests that many existing results in causal discovery that rely on path-based reasoning could potentially be re-derived or simplified using edge ranks, opening up new avenues for theoretical analysis. The observation that edge ranks reduce global equivalence checking to local conditions (checking each singleton observed variable independently) is particularly striking and suggests that the complexity of latent-variable causal discovery may be more tractable than previously thought.

## Suggestions

- Include at least one representative experimental figure in the main text (e.g., a plot showing glvLiNG's performance vs. baselines across sample sizes) to give readers a concrete sense of empirical performance.
- Add a brief complexity analysis (e.g., O(|V|^3) or similar) for the glvLiNG algorithm to substantiate the efficiency claims.
- Discuss the practical implications of the irreducibility condition: how often do real-world latent-variable models satisfy it, and what happens when they don't?

## Score and Decision

The paper makes a significant theoretical contribution by providing the first general characterization of distributional equivalence in linear non-Gaussian models with latent variables and cycles. The edge rank tool and duality theorem are elegant and likely to be influential. However, the practical impact is limited by the reliance on OICA, and the experimental evaluation is insufficiently presented in the main text. The theoretical contribution alone is strong enough to warrant acceptance, but the practical limitations prevent a higher score.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>