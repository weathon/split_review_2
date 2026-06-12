## Summary

This paper provides the first graphical characterization of distributional equivalence for linear non-Gaussian causal models with arbitrary latent variables and cycles. The authors introduce a novel tool called "edge ranks" that provides a local complement to the global "path ranks," establish a duality between the two, and use this to derive both a determining criterion and a transformational characterization (analogous to Meek's conjecture) for equivalence classes. They further develop a proof-of-concept algorithm, glvLiNG, that recovers latent-variable models up to equivalence from data without any structural assumptions.

## Strengths

- **Fundamental theoretical contribution filling a genuine gap.** The paper addresses a well-motivated and important open problem: equivalence characterization for latent-variable models in parametric settings. The step-by-step development from algebraic conditions (Lemma 1) through path ranks (Lemma 3) to the final graphical criterion (Theorem 2) and transformational characterization (Theorem 3) is logically clean and well-structured. The claim of being the first such characterization without structural assumptions appears well-supported.

- **Novel tool with broad potential impact.** The introduction of edge ranks (Definition 4) and the duality theorem (Theorem 1) constitute a genuinely novel contribution to the rank-based toolbox for causal discovery. The paper convincingly argues that edge ranks are more local and manipulable than path ranks, and the duality reveals that every statement about d-separation/t-separation can be rephrased in terms of edge ranks. This tool has potential utility well beyond the specific setting studied.

- **Elegant analogies to classical results.** The paper systematically draws parallels to the acyclic, causally sufficient setting: Theorem 2 as counterpart to "same adjacencies and v-structures," Theorem 3 as counterpart to "Meek conjecture," and Theorem 4 (in appendix) as counterpart to CPDAGs. This makes the results accessible and positions them clearly within the broader causal discovery landscape.

- **Honest and transparent presentation.** The authors are forthright about limitations (OICA inefficiency, proof-of-concept nature of the algorithm) and provide an interactive demo for exploring equivalence classes, which aids understanding and reproducibility.

## Weaknesses

### Fatal
None.

### Major

- **Reliance on OICA limits practical impact.** The glvLiNG algorithm depends on oracle OICA to estimate the mixing matrix, which is known to be computationally expensive and statistically challenging in practice. While the authors acknowledge this and frame the algorithm as a proof of concept, the gap between the elegant theory and practical applicability is significant. The experimental results in §5 show mixed performance: glvLiNG outperforms baselines on denser graphs but performs worse on sparser ones, and the baselines themselves are shown to fail under structural misspecification. This raises the question of whether the theoretical equivalence characterization can be leveraged by more practical estimation procedures in the near term.

- **Limited experimental evaluation.** The simulation study (Appendix D.4) and real-world application (single stock returns dataset) are relatively thin for a paper of this scope. The comparison with only two baselines (LaHiCaSi and PO-LiNGAM), both evaluated under oracle conditions in one experiment, provides limited insight into practical utility. A more thorough empirical investigation—e.g., testing on more diverse real-world datasets, providing confidence intervals, or comparing against a wider range of methods—would strengthen the paper considerably.

### Minor

- **The irreducibility condition (Proposition 1) could benefit from more intuition.** While the condition is stated clearly, the connection between "more than one child outside" for each non-empty latent subset and the identifiability of the number of latents via OICA could be elaborated. The brief mention of "proportional columns in mixing matrices" is suggestive but somewhat terse.

- **Scalability of equivalence class traversal.** The transformational characterization (Theorem 3) enables BFS/DFS traversal of equivalence classes, but the paper provides limited analysis of how large these classes can grow in practice beyond the small examples in Table 3 (up to 6 vertices). Understanding the scalability of traversal would help assess practical utility.

### Trivial
None.

## Nice-to-Haves

- A discussion of how the edge rank framework might extend to other settings (e.g., linear Gaussian, discrete) would be valuable, especially given the authors' mention of future directions in §6.
- A more detailed comparison with the closest prior work (Adams et al., 2021) on when acyclic linear non-Gaussian models are uniquely identified, clarifying exactly what the new characterization adds beyond that result.

## Novel Insights

The duality between path ranks and edge ranks (Theorem 1) is a genuinely novel insight that connects two seemingly disparate graphical quantities—global max-flow-min-cut quantities and local bipartite matching quantities—through a clean algebraic identity. This reveals that the "bottleneck" structure in digraphs has complementary local and global perspectives, and that the well-studied matroid-theoretic duality (König, Perfect, Ingleton) has direct implications for causal discovery. The observation that edge ranks enable a local decomposition of equivalence conditions (Theorem 2), where checking each observed variable independently suffices rather than all subsets, is a key technical insight that makes the final criterion practical.

## Suggestions

- Consider developing or at least sketching an OICA-free variant of glvLiNG that uses partial rank information from more practical estimators, even if it recovers a superset of the equivalence class. This would significantly increase practical impact.
- The interactive demo at equiv.cc is excellent; consider adding a tutorial or worked example that walks through the full pipeline from data to equivalence class for a moderately sized example.

## Score and Decision

This paper makes a strong theoretical contribution by solving a fundamental open problem in causal discovery. The equivalence characterization for arbitrary latent structure and cycles in linear non-Gaussian models fills a genuine gap, the edge rank tool is novel and potentially broadly useful, and the transformational characterization is elegant. The main limitations are practical (OICA reliance) rather than theoretical, and the authors are transparent about these. For a theory paper at ICLR, the contribution is substantial.

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>