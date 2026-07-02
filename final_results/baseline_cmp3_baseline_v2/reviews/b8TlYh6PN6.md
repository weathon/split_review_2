## Summary

This paper provides the first characterization of distributional equivalence for linear non-Gaussian causal models with arbitrary latent variables and cycles. The authors introduce edge rank constraints as a new tool, derive a graphical criterion and a transformational characterization (analogous to Meek's conjecture) of equivalence, and develop glvLiNG, the first structural-assumption-free algorithm for latent-variable causal discovery in this setting. The work fills a long-standing gap in the causal discovery literature, with theoretical contributions that are both clean and broadly applicable.

## Strengths

- **Novel and fundamental contribution**: The paper solves a central open problem in latent-variable causal discovery—characterizing when two models with arbitrary latent structure and cycles are observationally indistinguishable. This is the first such characterization in any parametric setting without structural assumptions, and it directly enables principled discovery methods.
- **Elegant theoretical framework**: The introduction of edge rank constraints and the duality with path ranks (Theorem 1) is insightful and opens a new perspective for the community. The graphical criterion (Theorem 2) reduces exponentially many rank conditions to local checks per observed variable, which is both surprising and practically valuable.
- **Complete characterization toolset**: The paper provides not only a static criterion for equivalence (Theorem 2) but also a transformational characterization (Theorem 3) analogous to Meek's conjecture, plus a representation of the class via a maximal digraph (Theorem 4, appendix). This completeness mirrors the well-studied Markov equivalence framework and will serve as a foundation for future work.
- **Rigorous progression**: The paper carefully builds from distributional equivalence to mixing matrices to path ranks to edge ranks, with clear logical steps, before presenting the final criterion and algorithm. The treatment of irreducibility correctly eliminates trivial unidentifiable cases.
- **First structural-assumption-free method**: glvLiNG demonstrates that the theoretical characterization can be turned into a feasible algorithm, even if the current implementation relies on OICA. The evaluation convincingly shows that existing methods fail under structural misspecification while glvLiNG recovers the full equivalence class.

## Weaknesses

### Major

- **Practical reliance on OICA**: The glvLiNG algorithm assumes oracle access to overcomplete ICA (OICA) or at least a mixing matrix estimate. OICA is known to be computationally challenging and often unreliable in practice, especially as the number of latent variables grows or under finite samples. The paper acknowledges this as a limitation and frames glvLiNG as a proof of concept, but this significantly limits the practical impact of the method. Without a robust OICA estimator, the algorithmic contribution remains largely theoretical.
- **Finite-sample evaluation is relegated to appendix**: The main text reports that finite-sample results "are provided in Appendix D.4" with a brief qualitative summary. For a paper that claims an algorithmic contribution, the core experimental validation should be presented more prominently. The anecdotal real-world stock data example is interesting but cannot substitute for systematic finite-sample benchmarks.

### Minor

- **Notation density**: Sections 3 and 4 contain dense notation and multiple lemmas that are difficult to parse on first reading. While the ideas are sound, the presentation could benefit from more intuitive explanations alongside the formal statements (e.g., a running example throughout the development).
- **Comparison with more recent OICA-free methods**: The paper compares glvLiNG against LaHiCaSi and PO-LiNGAM under oracle inputs, but does not discuss how one could replace OICA with alternatives that provide partial rank information (as mentioned in Section 5). A brief discussion or experiment on such integration would strengthen the practical outlook.
- **Clarity of irreducibility condition**: Proposition 1 states that irreducibility is equivalent to each latent having more than one child outside. The proof sketch mentions OICA identifiability results, but the exact relationship between this graphical condition and OICA's uniqueness guarantee could be spelled out more clearly for readers less familiar with that literature.

### Trivial

- Figure 3 contains redundant caption text (the caption is duplicated twice).
- The notation `\stackrel{\mathcal{D}}{\sim}` in Equation (7) appears to be a typo (should be `\stackrel{X}{\sim}`).

## Nice-to-Haves

- An explicit illustration showing how the edge rank criterion (Theorem 2) plays out step-by-step on a small example (e.g., one of the graphs in Figure 3) would greatly improve accessibility.
- A discussion on whether the equivalence characterization extends to the case where observed variables have no parents at all (i.e., purely latent-to-observed structure) would be helpful, as this is a common scenario in practice.
- The interactive demo at <https://equiv.cc> is a valuable resource; including a few representative screenshots or a description of its functionality directly in the paper would increase visibility.

## Novel Insights

Beyond the paper's own contributions, a genuinely novel insight is the duality between path ranks and edge ranks (Theorem 1) and its implication that bottleneck information in causal graphs can be equivalently read from local bipartite matchings rather than global max-flow cuts. This opens up a new perspective: many rank-based constraints used in causal discovery (including d-separation analogues in cyclic models) can be reframed in terms of matching structure, which may lead to simpler algorithms and new identifiability results in other settings (e.g., linear Gaussian, discrete). The authors are correct that this tool has been underutilized in the causal discovery community.

## Suggestions

- For practical adoption, consider providing a variant of glvLiNG that does not require full OICA but instead uses the partial rank constraints that can be extracted from observed data via covariance/tetrad methods or pairwise independence tests. Alternatively, benchmark the OICA estimation step separately to show when it is reliable.
- The finite-sample evaluation in Appendix D.4 should be summarized with key numbers (e.g., SHD, precision/recall) in the main text to give readers a concrete sense of performance. At minimum, a table with results under the hardest setting (many latents, dense graphs, small sample size) would strengthen the empirical claims.

## Score and Decision

This paper makes a strong theoretical contribution that fills a long-standing gap in causal discovery. The equivalence characterization is novel, rigorous, and elegantly reduces a seemingly intractable problem to local graph operations. The algorithmic demonstration, while limited by OICA practicality, convincingly shows that the theory can be operationalized. The weaknesses are primarily about practical deployment, not about the correctness or significance of the core contribution. The paper meets the bar for acceptance at ICLR.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>