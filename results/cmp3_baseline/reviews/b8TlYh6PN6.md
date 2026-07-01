## Summary

This paper studies distributional equivalence in linear non-Gaussian (LiNG) causal models with latent variables and cycles. The authors characterize when two graphs with arbitrary latent structure and cycles induce the same set of observed distributions, introduce a new tool called "edge rank" constraints that complements the well-known path rank perspective, and develop a transformational characterization of the equivalence class. Based on these theoretical results, they propose glvLiNG, a structural-assumption-free algorithm for recovering causal models up to distributional equivalence from data.

## Strengths

- **First general equivalence characterization with latent variables**: The paper provides, to the authors' knowledge, the first characterization of distributional equivalence in any parametric setting that allows arbitrary latent structure and cycles without restrictive structural assumptions. This fills a significant gap in the literature and addresses a core obstacle to developing general latent-variable causal discovery methods.

- **Novel and elegant theoretical tool**: The introduction of edge rank constraints and the duality theorem between path ranks and edge ranks (Theorem 1) is a genuinely novel contribution that enriches the rank-based toolbox for causal discovery. The duality is mathematically elegant and has potential applications beyond the specific setting studied here.

- **Clean and complete theoretical framework**: The paper systematically develops the theory from first principles (irreducibility, path rank equivalence, edge rank duality) to a practical graphical criterion (Theorem 2) and a transformational characterization (Theorem 3). The results are presented with clear analogies to classical Markov equivalence theory, making the contributions accessible.

- **Proof-of-concept algorithm**: The glvLiNG algorithm demonstrates that the theoretical characterization is actionable, and the evaluation provides evidence that structural-assumption-free recovery is feasible, even if the current implementation relies on OICA.

## Weaknesses

### Major

- **OICA dependency limits practical impact**: The algorithm's reliance on over-complete independent component analysis (OICA) is a significant practical limitation, as the authors themselves acknowledge. OICA is known to be computationally challenging and unreliable in finite samples, especially as the number of latent variables grows. While the paper frames glvLiNG as a proof of concept, the evaluation on finite-sample data (point 4 in evaluation) is not presented in sufficient detail in the main text to assess how severe this limitation is in practice. The paper would benefit from a more thorough discussion of when OICA is expected to work and when it fails.

- **Evaluation depth and clarity**: The evaluation section is quite compressed and lacks sufficient detail for reproducibility and critical assessment. The results tables (Tables 3-5) are referenced but not shown in the main text, and the finite-sample simulation results are described only qualitatively ("performs particularly better on denser graphs"). Without seeing the actual numbers, error bars, and comparison metrics, it is difficult to evaluate the practical significance of the claims. The real-world application (stock returns) is mentioned but the results are deferred to the appendix.

- **Scalability concerns**: While the paper reports that glvLiNG solves cases with n=10 vertices in under 5 seconds, this is a relatively small scale. Many real-world causal discovery problems involve dozens or hundreds of variables. The combinatorial nature of the equivalence class traversal (even with pruning) raises questions about scalability to larger systems.

### Minor

- **The paper's framing of "structural-assumption-free" is slightly overstated**: While the method does not require assumptions like pure measurement models or acyclicity, it still relies on linearity, non-Gaussianity, and the faithfulness assumption. These are parametric assumptions, and the paper would benefit from more precise language about what "structural-assumption-free" means in context.

- **The connection to existing work on cycle reversals could be better integrated**: Lemma 6 (admissible cycle reversals) is attributed to Lacerda et al. (2008), but the paper does not clearly explain how this result fits into the broader picture or whether the proof is novel.

### Trivial

- The paper uses both $\stackrel{X}{\sim}$ and $\stackrel{\mathcal{D}}{\sim}$ notation for equivalence, which appears to be a minor inconsistency.

## Nice-to-Haves

- A more detailed ablation study showing how much of the performance gain comes from the equivalence characterization versus the specific algorithmic choices in glvLiNG.
- Discussion of how the edge rank tool might be applied to other settings (e.g., linear Gaussian, discrete) as suggested in the conclusion.
- A visual or tabular summary of the equivalence class sizes for different latent configurations to help readers develop intuition.

## Novel Insights

Beyond the paper's own contributions, the key novel insight is the duality between path ranks and edge ranks (Theorem 1), which reveals that the global, path-based perspective and the local, edge-based perspective are two sides of the same coin. This duality suggests that many problems in causal discovery that have been approached through path-based reasoning (d-separation, t-separation, rank constraints) could be re-examined through the lens of edge ranks, potentially leading to simpler algorithms and new theoretical results. The fact that edge ranks admit a local decomposition that reduces global equivalence checking to per-vertex checks (Theorem 2) is a concrete demonstration of this principle.

## Suggestions

- Provide the evaluation tables (Tables 3-5) and finite-sample results in the main text or a more accessible format, with error bars and clear comparisons to baselines.
- Include a discussion of the computational complexity of the equivalence class traversal and the conditions under which it remains tractable.
- Clarify the relationship between the proposed method and existing OICA-based approaches (e.g., Salehkaleybar et al., 2020) to help readers understand what is genuinely new versus an application of existing techniques.

## Score and Decision

The paper makes a significant theoretical contribution by providing the first general characterization of distributional equivalence in linear non-Gaussian latent-variable models with cycles. The edge rank tool is elegant and has potential beyond this specific setting. However, the practical impact is currently limited by the OICA dependency, and the evaluation is not presented with sufficient detail to fully assess the algorithm's performance. The theoretical contribution alone is strong enough to warrant acceptance, but the practical limitations and evaluation gaps prevent a higher score.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>