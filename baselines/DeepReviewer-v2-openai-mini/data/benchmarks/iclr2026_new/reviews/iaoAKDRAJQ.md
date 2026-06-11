## Summary
# Final Review Report

## Summary

This paper provides a theoretical analysis comparing adaptive optimizers (e.g., Adam, AdaGrad, Shampoo) and Normalized Steepest Descent (NSD) methods (e.g., SignGD, Lion, Muon) through the lens of smoothness assumptions in non-Euclidean geometry. The authors make four main contributions: (1) extending the theory of adaptive smoothness to the nonconvex setting, showing it governs the convergence of adaptive optimizers with general well-structured preconditioner sets; (2) establishing an accelerated $\tilde{O}(T^{-2})$ rate for adaptive optimizers with Nesterov momentum under adaptive smoothness, contrasting with a known $\Omega(T^{-1})$ lower bound under standard smoothness; (3) introducing adaptive gradient variance as an analogue of adaptive smoothness for stochastic noise, enabling dimension-free convergence guarantees for NSD; and (4) developing a novel matrix inequality (Lemma 3.3) that handles noncommutativity in general preconditioner sets, enabling the first unified nonconvex analysis beyond diagonal preconditioners.

The paper is technically rigorous and addresses an important theoretical question about the role of geometry in adaptive optimization. The main weaknesses are: the absence of any empirical validation, several overclaims (optimality of rates, strict superiority over concurrent work) that are not fully justified by the presented evidence, and practical limitations in the accelerated method's parameter requirements. The conclusion is also notably brief and lacks a discussion of limitations.

## Strengths
1. **Technically deep and well-structured theory.** The paper develops a unified theoretical framework that extends adaptive smoothness analysis from convex to nonconvex settings for a broad class of adaptive optimizers. The novel matrix inequality (Lemma 3.3) that handles noncommutativity in general preconditioner sets is a significant technical contribution, enabling the first unified nonconvex analysis beyond diagonal preconditioners. The proof techniques involving logarithmic matrix inequalities are likely to be of independent interest to the optimization theory community.

2. **Clear conceptual contribution.** The paper draws a crisp conceptual distinction between adaptive smoothness (which governs adaptive optimizers) and standard smoothness (which governs NSD methods), and demonstrates that this distinction has concrete optimization consequences. The $\tilde{O}(T^{-2})$ acceleration result under adaptive smoothness versus the $\Omega(T^{-1})$ lower bound under standard smoothness is a compelling separation result that cleanly answers the motivating question about whether the stronger assumption yields concrete benefits.

3. **Principled analogy between smoothness and variance.** The introduction of adaptive gradient variance as a parallel notion to adaptive smoothness is conceptually elegant. The demonstration that adaptive variance enables dimension-free NSD rates (Theorem 4.5), while standard variance necessarily incurs dimension dependence (Theorem 4.7), provides a complete and rigorous separation between the two noise assumptions. This dual treatment of smoothness and noise is a nice intellectual contribution.

4. **Unified algorithmic coverage.** The meta-algorithm framework (Algorithm 1) elegantly unifies AdaGrad, Adam, AdaGrad-Norm, full-matrix AdaGrad, and one-sided Shampoo under a single convergence analysis. This provides a systematic understanding of how different preconditioner choices affect convergence guarantees, which is valuable for both theorists and practitioners designing new optimizers.

## Weaknesses
1. **[Major] Unsubstantiated optimality and superiority claims.** The paper claims its nonconvex rate "matches optimal $\tilde{O}(T^{-1/4})$ rate" (contribution list) without providing or citing any matching lower bound. No formal lower bound is derived or referenced for the adaptive optimizer family under adaptive smoothness. Similarly, the claim that Theorem 4.5 is "strictly better" than the concurrent work Kovalev & Borodich (2025) is made without presenting the competing bound for direct comparison. These unsupported optimality and superiority claims are not consistent with the paper's otherwise rigorous tone and should be softened to "new upper bounds" with appropriate qualifications. *Location: Page 0 - Abstract/Contributions, Page 9 - Section 4.3.*

2. **[Major] No empirical validation.** The paper is purely theoretical with no experiments. While this is acceptable for a theory paper, the motivating questions (Q1, Q2) are framed in practical terms — readers naturally wonder whether the theoretical distinctions between adaptive smoothness and standard smoothness manifest in observable optimization behavior. The paper does not include any synthetic experiments, such as verifying that the adaptive smoothness constant predicts convergence speed, or that the accelerated method empirically outperforms standard NSD. Including even a small-scale numerical illustration would significantly strengthen the paper's impact. *Location: Entire paper.*

3. **[Major] Learnability issue in accelerated method.** Theorem 4.3 achieves an $\tilde{O}(T^{-2})$ rate but requires the optimal learning rate $\eta = D$, where $D = \max_t \|\mathbf{x}_t - \mathbf{x}^*\|_{\mathcal{H}}$ is unknown a priori. Remark 4.4 proposes a projected variant that still requires prior knowledge of $D$ to set the projection radius. This circular dependency between the unknown $D$ and the algorithm parameters is a significant practical limitation that is not adequately addressed. For comparison, standard Nesterov acceleration does not require knowledge of the distance to the optimum. *Location: Page 8 - Theorem 4.3 and Remark 4.4.*

4. **[Major] Over-interpretation of the "adaptivity" of Adam.** The paper states (Section 2.1) that Adam's adaptivity is demonstrated by "its ability to automatically identify and adapt to the best diagonal matrix-induced norm." This conflates the mathematical property of the convergence bound (which involves an infimum over $\mathbf{H}$) with Adam's algorithmic mechanism. The bound being independent of $\mathbf{H}$ after minimization means the *analysis* is robust to the choice of norm, not that Adam *automatically identifies* the best geometry — a much stronger claim requiring additional analysis. *Location: Page 3 - Section 2.1.*

5. **[Moderate] Overstated distinction between smoothness notions as "fundamentally different."** The paper emphasizes that adaptive and standard smoothness are "fundamentally different," yet Proposition 2.5 shows they differ by at most a factor of $d$, and the two definitions are related through a common mathematical framework (minimization over $H \in \mathcal{H}$). The paper would benefit from a more precise characterization: they are different but related through a bounded gap, with the key difference being the order of quantization (infimum vs supremum) over the preconditioner set. *Location: Page 4 - Section 2.2.*

6. **[Moderate] Notation inconsistency in smoothness comparison.** The inequality chain comparing smoothness notions (lines 75-78) contains a labeling error: the right-hand side after the inequality is written as $L_{\|\cdot\|_{\mathcal{H}}}(f)$ but should be $L_{\|\cdot\|_H}(f)$. This makes the derivation appear circular. While the conclusion is still correct, this error could confuse readers trying to follow the technical argument. *Location: Page 4 - Comparison paragraph.*

7. **[Minor] Conclusion is too brief.** The conclusion (3 sentences) simply restates the results without discussing limitations, open questions, or practical implications. The paper mentions several important caveats internally (the $\log d$ factor gap, the $D$-dependence, the lack of tightness proofs) but none appear in the conclusion. A stronger conclusion would discuss boundary conditions and future work, improving the paper's completeness. *Location: Page 9 - Section 5.*

8. **[Minor] Abstract overclaims "precise characterization."** The abstract states adaptive smoothness "precisely characterizes" convergence, but the rates involve $\tilde{O}$ notation with hidden logarithmic factors. The word "precisely" overstates the granularity of the results. *Location: Page 0 - Abstract.*

## Score
**Final Score: 7/10**

**Rationale:** The paper makes a technically solid theoretical contribution to understanding adaptive optimizers through the lens of adaptive smoothness and adaptive variance. The unified nonconvex analysis and the novel matrix inequality (Lemma 3.3) are genuine advances. However, the score is reduced due to: (1) unsubstantiated optimality/superiority claims that are not backed by the presented evidence, (2) the complete absence of empirical validation even at a synthetic level, which weakens the connection to the practice-motivated framing, (3) several over-interpretations (e.g., conflating bound robustness with algorithmic adaptivity), and (4) practical limitations in the accelerated method that are not adequately resolved. The paper's primary value is as a theoretical synthesis and unification, with the strongest technical contribution being the noncommutative matrix inequality. The novelty claims cannot be fully verified without external literature access, but based on the manuscript's own framing, the core ideas (adaptive smoothness characterization in nonconvex setting, adaptive variance for dimension-free NSD) appear to be incrementally building on the authors' prior work (Xie et al., 2025b) and concurrent work (Kovalev, 2025a; Kovalev & Borodich, 2025). With careful revision to address overclaims and the addition of at least synthetic experiments, the paper could merit a higher score.

```text
ASCII Diagram — Paper Structure & Evidence Map

[Problem: How do adaptive optimizers and NSD exploit non-Euclidean geometry?]
    |
    v
[Claim C1: Adaptive smoothness governs nonconvex convergence of adaptive optimizers]
    |-- Evidence: Theorems 3.1-3.2, Lemma 3.3 (unified bound)
    |-- Gap: No matching lower bound provided; "optimal" claim unsubstantiated
    |
[Claim C2: Adaptive smoothness enables acceleration (Section 4.2)]
    |-- Evidence: Theorem 4.3, $\tilde{O}(T^{-2})$ rate
    |-- Gap: Optimal $\eta$ depends on unknown $D$; circular dependency in projection
    |
[Claim C3: Adaptive variance enables dimension-free NSD rates (Section 4.3)]
    |-- Evidence: Theorems 4.5-4.7 (upper + lower bounds)
    |-- Gap: "Strictly better" claim vs concurrent work not fully quantified
```

```text
ASCII Diagram — Revision Strategy Roadmap

[Overclaim: optimal rate] --> [Fix: Replace "optimal" with "new upper bound"] --> [Expected: honest framing]
[Overclaim: strictly better] --> [Fix: Present competing bound, soften claim] --> [Expected: verifiable comparison]
[No experiments] --> [Fix: Add 1-2 synthetic experiments verifying rates] --> [Expected: empirical grounding]
[Notation error in comparison] --> [Fix: Correct $L_{\|\cdot\|_H}(f)$ vs $L_{\|\cdot\|_{\mathcal{H}}}(f)$] --> [Expected: clarity]
[Brief conclusion] --> [Fix: Add limitations + open questions] --> [Expected: completeness]
```

```text
ASCII Diagram — Related-Work Taxonomy Tree (Layered)
(Note: Novelty verification deferred due to Retrieval-Disabled Mode; taxonomy based on manuscript's own citations)

Optimization under Non-Euclidean Geometry (Root)
├── Branch 1: Adaptive Optimizers
│   ├── Leaf 1.1: Diagonal preconditioning (Adam, AdaGrad, RMSProp)
│   │   └── Prior: Maladkar et al. 2024, Xie et al. 2025a
│   ├── Leaf 1.2: Full-matrix preconditioning (Shampoo, ASGO)
│   │   └── Prior: Xie et al. 2025b, An et al. 2025
│   └── Leaf 1.3: Unified analysis with well-structured sets
│       └── This paper (nonconvex extension of Xie et al. 2025b)
├── Branch 2: Normalized Steepest Descent
│   ├── Leaf 2.1: Sign-based methods (SignGD, Lion)
│   │   └── Prior: Bernstein & Newhouse 2024, Pethick et al. 2025
│   └── Leaf 2.2: Spectral-norm methods (Muon)
│       └── Prior: Jordan et al. 2024, Team et al. 2025
└── Branch 3: Smoothness Theory
    ├── Leaf 3.1: Standard smoothness under general norms
    │   └── Prior: Guzmán & Nemirovski 2015, Pethick et al. 2025
    └── Leaf 3.2: Adaptive / $\mathcal{H}$-smoothness
        └── Prior: Xie et al. 2025b, Kovalev 2025a
        └── This paper: nonconvex extension + acceleration
```

**Novelty & Comparison Note:** External literature verification is unavailable in this run (Retrieval-Disabled Mode). Novelty and comparison conclusions in this review are based solely on the manuscript's own content and should be verified manually before final decision.