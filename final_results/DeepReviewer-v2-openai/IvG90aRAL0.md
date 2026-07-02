## Summary
This paper proposes quantum algorithms for projection-free (Frank-Wolfe) sparse convex optimization in both vector and matrix domains. For vector domains under ℓ₁-norm and simplex constraints, the authors develop quantum Frank-Wolfe algorithms that achieve query complexity O(√d/ε) and O(1/ε) via function-value oracles, improving over the classical O(d) query cost. For matrix domains under nuclear norm constraints, the authors propose two quantum subroutines—Quantum Top Singular Vector Extraction (QTSVE) and Quantum Power Method (QPM)—that achieve per-update-step complexities of Õ(rd/ε²) and Õ(√rd/ε³), respectively. The main technical contributions include: (i) quantum gradient estimation via forward differences combined with quantum maximum finding for the linear subproblem, (ii) a quantum maximum-finding-based top singular vector extraction pipeline, and (iii) a quantum power method for extracting leading singular vectors. All claims of quantum advantage are relative to dimension d and rely on oracular assumptions (quantum function-value oracle for vectors; quantum-accessible matrix data structures with pre-computed gradients for matrices).

**Key Strengths:** Addresses an important question—whether quantum computing can accelerate Frank-Wolfe methods in high dimensions. Provides a systematic treatment across both vector and matrix domains with multiple constraint types. The technical machinery (quantum gradient circuits, quantum maximum finding for non-uniform states, quantum singular vector estimation) is carefully assembled from existing quantum primitives.

**Key Weaknesses:** (1) The claimed "quantum speedup" conflates query complexity with end-to-end runtime, ignoring QRAM initialization, oracle implementation overhead, and measurement costs. (2) Several strong claims ("first to consider matrix case", "at least O(√d) speedup") are not adequately qualified given the parameter-regime-dependent nature of the comparisons. (3) Core technical novelties (error propagation via Hölder bounds, dominant atom finding) are deferred entirely to the appendix and are not verifiable from the main body. (4) The Power/Lanczos complexity expressions contain formatting errors that affect interpretability, and Theorem 4's complexity contains notational inconsistencies. (5) No empirical validation or resource estimation is provided, which is understandable for a theory paper but limits assessment of practical relevance.

## Strengths
1. **Well-motivated research question.** The paper addresses a timely and important problem: whether quantum computing can accelerate projection-free first-order optimization methods (Frank-Wolfe) in high-dimensional settings. The connection between the linear subproblem bottleneck and quantum search/estimation primitives is natural and well-conceived.

2. **Systematic treatment across domains.** The paper covers both vector and matrix domains with multiple constraint types (ℓ₁-ball, simplex, latent group norm, nuclear norm), providing a unified quantum framework that extends beyond the single setting studied in prior work (Chen & de Wolf 2023). The inclusion of both high-rank and low-rank gradient matrix regimes through two complementary algorithms (QTSVE and QPM) demonstrates thoughtful algorithm design.

3. **Clean integration of quantum primitives.** The algorithmic construction assembles known quantum building blocks—quantum function-value oracle, forward-difference gradient estimation, quantum maximum finding (Durr & Hoyer), quantum singular value estimation, quantum matrix-vector multiplication, and quantum state tomography—into a coherent Frank-Wolfe pipeline. The theoretical error propagation analysis that connects gradient approximation error to Frank-Wolfe subproblem slack (via Hölder's inequality) is a technically sound contribution, though deferred to the appendix.

4. **Transparent concurrent-work acknowledgement.** The paper candidly notes an independent work (Chen et al. 2025a) on the quantum power method, comparing access models and complexity regimes. This scholarly transparency is commendable.

5. **Potential for broader impact.** If the quantum resource assumptions (QRAM, function-value oracle) can be realized, the proposed algorithms would offer meaningful dimension-reduction speedups for important problems including sparse regression, matrix completion, and support vector machines—all of which involve structured convex constraints over high-dimensional spaces.

## Weaknesses
### W1. Conflation of query complexity with end-to-end speedup (Critical)

The abstract and introduction repeatedly claim quantum speedup (e.g., "reducing a factor of O(√d) over the best classical algorithm"), but the comparison metric shifts between settings without adequate qualification. For the vector case, the speedup is in **query complexity** (calls to the function-value oracle $U_f$), not end-to-end runtime. The actual end-to-end cost depends on (i) the implementation cost $T_f$ of $U_f$, which could scale with dimension $d$, (ii) QRAM initialization and maintenance for state preparation, (iii) quantum measurement overhead for extracting classical information (the maximum-gradient index), and (iv) the iteration overhead of quantum error correction. For the matrix case, the complexity advantage excludes gradient computation cost ($T_\nabla$ is listed separately in Table 2), and the pre-computed gradient assumption (Remark 3) effectively decouples the quantum subroutine from the full optimization loop. These caveats are not highlighted in the abstract, creating an impression of unconditional quantum advantage that is not supported by the analysis.

**Severity: High impact.** Overclaiming speedup can mislead readers about practical viability. The paper would be strengthened by: (a) explicitly distinguishing query complexity from time complexity throughout, (b) discussing the overhead costs required for end-to-end speedup, and (c) adding a "resource assumptions and limitations" paragraph.

### W2. Unverifiable novelty claims deferred to appendix (Major)

The paper makes several strong technical novelty claims—"novel error propagation analysis for dual norm computation under gradient approximation, deriving bounds via Hölder's inequality" and "quantum subroutine for dominant atom finding"—yet none of these are presented in the main body. The core technical derivations, including all convergence proofs, error bounds, and parameter settings, are deferred to an appendix that is not included in the provided manuscript preview. This means reviewers cannot verify the correctness or novelty of the claimed contributions from the main text alone. For a theory paper, the key lemmas and proof sketches should appear in the main body.

**Severity: Major.** Without access to the appendix, the paper's claimed contributions are not independently assessable. **Action:** Include at minimum a proof sketch of the Hölder-based error bound and the dominant-atom-finding subroutine in the main text, as these are advertised as novel contributions.

### W3. Parameter-regime-dependent speedup claims overstated (Major)

The abstract claims that matrix-case algorithms achieve "at least a factor of O(√d) speedup over the best classical algorithm." However, comparing the complexities in Table 2 shows a nuanced picture:
- QTSVE (Theorem 3): Õ(σ₁²(M)d / ((σ₁-σ₂)ε²)) — has an ε² factor vs. classical ε, and an extra σ₁² factor vs. classical √σ₁ and d vs. d²/√... 
- QPM (Theorem 4): Õ(√r σ₁⁴(M)d / ((1-σ₁)³γ_min^{2.5})) — involves γ_min (a poorly characterized lower-bound quantity) and (1-σ₁)³ in the denominator.

The "O(√d) speedup" holds only after factoring out spectral gap, rank r, and precision ε dependencies, which the paper does not clearly do. The overhead from quantum tomography (which costs O(d log d / δ²) per vector extraction) also contributes a d-dependence that is not fully separated in the claimed speedup.

**Action:** Provide a regime table showing when (under which spectral gap, rank, and precision conditions) each quantum algorithm outperforms each classical baseline. Replace blanket "O(√d) speedup" claims with parameter-dependent statements.

### W4. Missing empirical resource estimation (Major)

As a quantum algorithms paper, the manuscript would benefit substantially from complexity constant estimation or resource count comparison. Quantum algorithms are known for large constant factors (e.g., the 1/ε² scaling in QTSVE vs. 1/ε in classical Lanczos, the poly(log d) factors from amplitude amplification, and the O(d log d / δ²) tomography overhead). Without at least a discussion of constant factors or a small-scale resource estimate, it is difficult to assess whether the proposed quantum methods would offer any advantage for practically relevant problem sizes. This is particularly important because the quantum algorithms involve multiple layers of approximation (gradient estimation, maximum finding, tomography) whose errors accumulate.

**Action:** Add a "resource comparison" subsection that estimates the total T-gate count or query complexity with explicit constants for a representative problem size (e.g., $d=10^5$, $\varepsilon=10^{-3}$). If this is not feasible, add a limitations paragraph discussing constant factors and accumulation of approximation errors.

### W5. Notational and formatting errors affecting interpretability (Minor-Major)

Several technical expressions contain formatting or notational issues:
- Eq. (4): Outer angle brackets used as delimiters conflict with inner product notation; should be parentheses.
- Power/Lanczos complexity expressions (Page 6, lines 125-126): The parameter $\varepsilon'$ appears as an exponent in the denominator, which is a formatting artifact that changes the mathematical meaning.
- Theorem 4 (Page 9): The complexity expression uses $\gamma_{\min}$ (without prime) while the definition uses $\gamma'_{\min}$ (with prime). The denominator $(1-\sigma_1(M_t))^3$ uses a different gap measure than the classical analysis ($\sigma_2/\sigma_1$ ratio), and its behavior when $\sigma_1=1$ is not discussed.
- Theorem 3 statement: "$f(X^\top) - f(X^*)$" has a formatting issue — the superscript T (transpose) should be the iteration index $T$.

**Action:** Carefully proofread all complexity expressions and fix notational inconsistencies.

### W6. Query oracle model assumption misalignment with applications (Minor)

The paper lists many practical applications (Lasso, matrix completion, SVMs, AdaBoost) but does not analyze whether the assumed oracle model (function-value-only access) is realistic for these problems. For least-squares problems like matrix completion, the objective involves a data matrix $A$ — computing $f(X) = \|A(X) - Y\|^2$ requires operations on the data, and implementing $U_f$ efficiently may require quantum access to $A$ itself. The paper's assumption that $U_f$ has constant cost $T_f$ independent of $d$ is not justified for these concrete applications. The application claims should be bounded by noting the additional data-access requirements.

## Score
**Final Score: 6/10**

**Rationale:** The paper tackles an interesting and well-motivated problem (quantum acceleration of Frank-Wolfe optimization) and provides a systematic algorithmic framework spanning both vector and matrix domains. The technical construction is coherent and builds on established quantum primitives. However, the score is limited by: (1) the conflation of query complexity with end-to-end speedup, which overstates the practical quantum advantage claimed in the abstract; (2) key technical novelty claims being deferred entirely to the appendix and thus not verifiable from the main text; (3) the "at least O(√d) speedup" claim not being consistently supported across the parameter regimes relevant to the matrix algorithms; (4) the absence of any resource estimation or discussion of constant factors, which is important for quantum algorithms to assess practical relevance; and (5) notational/formatting errors in complexity expressions that affect interpretability. The core algorithmic ideas have merit and the systematic treatment is a useful contribution to the quantum optimization literature, but the presentation needs substantial revision to align claims with evidence.

---

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Paper: Quantum Algorithms for Projection-Free Sparse Convex Optimization]
│
├── [Claim 1: Vector-domain QFW achieves O(√d/ε) query complexity]
│   ├── Evidence: Theorem 1 + Lemma 2-4 + Algorithm 2
│   ├── Gap: Query complexity ≠ time complexity; QRAM overhead not counted
│   └── Risk: Speedup may not survive end-to-end accounting
│
├── [Claim 2: Matrix-domain QFW achieves O(√d) update-computation speedup]
│   ├── Evidence: Theorem 3 (QTSVE), Theorem 4 (QPM) + Table 2
│   ├── Gap: Speedup factor depends on spectral gap, rank r, precision ε
│   └── Risk: Blanket "at least O(√d)" claim is regime-dependent
│
├── [Claim 3: Novel error propagation via Hölder bounds + dominant atom finding]
│   ├── Evidence: Claimed in Section 1 bullet, but deferred to Appendix
│   ├── Gap: No main-text derivation or explicit bound statement
│   └── Risk: Unverifiable from main body; undermines contribution novelty
│
└── [Application claims: Lasso, matrix completion, SVMs, etc.]
    ├── Evidence: Listed in Section 1, discussed in Appendix A.6
    ├── Gap: Oracle-model alignment not analyzed per application
    └── Risk: Overclaims practical readiness without data-access analysis
```

### ASCII Diagram — Revision Strategy Roadmap

```text
[Priority 0 (Before Resubmission)]
─────────────────────────────────────────────
Replace "quantum speedup" language with "improvement
in query complexity under oracular assumptions"
    → Expected gain: Aligns claims with evidence
    → Sections affected: Abstract, Introduction, Conclusion

[Priority 1 (Add to Main Text)]
─────────────────────────────────────────────
Add proof sketch of Hölder-based error bound
Add explicit subproblem slack δ ← gradient error ε_g derivation
    → Expected gain: Novelty becomes verifiable
    → Sections affected: Section 3, Section 2.2

[Priority 2 (Presentation Correction)]
─────────────────────────────────────────────
Fix ε' exponent error in Power/Lanczos complexities
Harmonize γ'_min/γ_min in Theorem 4
Fix angle bracket notation in Eq. (4)
Fix $X^⊤$ → $X^T$ in Theorem 3
Add parameter-regime comparison table
    → Expected gain: Correctness + interpretability

[Priority 3 (Strengthen Verification)]
─────────────────────────────────────────────
Add resource estimate (T-gate count) for representative
problem size (d=10^5, ε=10^-3)
Add limitations paragraph on error accumulation
(quantum gradient error + max-finding error + tomography error)
    → Expected gain: Practical relevance assessment
```

### ASCII Diagram — Related-Work Taxonomy Tree (Layered)

```text
Quantum-Enhanced Optimization (Root)
├── Branch 1: Quantum methods for convex optimization
│   ├── Leaf 1.1: Interior-point methods [Apers & Gribling 2023]
│   └── Leaf 1.2: SDP solvers [Brandão & Svore 2017]
├── Branch 2: Quantum Frank-Wolfe / conditional gradient
│   ├── Leaf 2.1: HHL-based FW for linear regression [Chen & de Wolf 2023]
│   └── Leaf 2.2: Oracle-based FW (THIS PAPER)
│       ├── Vector domain: QFW with ℓ₁/simplex/latent group constraints
│       └── Matrix domain: QFW with QTSVE / QPM for nuclear norm
├── Branch 3: Quantum linear algebra primitives
│   ├── Leaf 3.1: Quantum SVE [Kerenidis & Prakash 2020, Bellante et al. 2022]
│   ├── Leaf 3.2: Quantum matrix-vector multiplication [Chakraborty et al. 2019]
│   └── Leaf 3.3: Quantum power method [Chen et al. 2025a] (concurrent)
└── Branch 4: Classical projection-free optimization
    ├── Leaf 4.1: Frank-Wolfe analysis [Jaggi 2013]
    ├── Leaf 4.2: Power/Lanczos methods [Kuczynski & Woźniakowski 1992]
    └── Leaf 4.3: Latent group norm constraints [Dunn & Harshbarger 1978]

Note: Novelty verification deferred due to Retrieval-Disabled Mode.
External literature comparison requires manual verification.
```

### Page Coverage Audit

| Page(s) | Section(s) | Annotation Count | Coverage Status |
|---------|-----------|-----------------|-----------------|
| 1 (Abstract) | Abstract | 1 | Covered |
| 1 (Introduction) | Section 1 (whole) | 6 | Covered (paragraph-by-paragraph) |
| 1 (Preliminaries) | Section 2.1-2.2 | 2 | Covered |
| 1 (Vector Methods) | Section 3 | 2 | Covered |
| 1 (Matrix Methods) | Section 4 | 2 | Covered |
| 1 (Conclusion) | Section 5 | 1 | Covered |
| Appendix | Not in provided text | 0 | Skipped (no manuscript text) |

All substantive paragraphs in the provided main body (Abstract, Introduction, Method/Sections 2-4, Conclusion) have been annotated. The appendix content was not available for annotation.