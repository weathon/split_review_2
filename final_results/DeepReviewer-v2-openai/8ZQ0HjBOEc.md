## Summary
# Final Review Report

## Summary

This paper studies the behavior of the Neural Tangent Kernel (NTK) for infinitely-wide fully-connected ReLU networks as depth $L$ increases, under the scaling condition $L \in o(\min_i n_i)$ (width grows faster than depth, ensuring determinism). The authors prove two main results: (1) the normalized limiting NTK $\bar{\Theta}_\infty^{(L)}$ converges entrywise to 1 (the matrix of ones), implying the kernel becomes singular; and (2) despite this singularity, the NTK predictor $\kappa_x^\top \kappa^{-1}$ — the closed-form kernel solution describing the trained network's output — converges to a well-defined bounded limit, established using rough differential equations (RDEs). The paper also provides an empirical illustration of convergence rates on synthetic data and MNIST, and identifies abstract properties that allow generalizing the results to other kernel families.

**Core research value**: The paper addresses a genuine gap in the NTK literature — the joint scaling of depth and width — and provides a rigorous treatment of the singular-kernel regime that prior work (Xiao et al., 2020) explicitly excluded. The use of RDE machinery is technically novel for this problem. However, the paper's theoretical contributions are limited by several gaps in the proofs and a lack of experimental validation of the core predictions.

## Strengths
1. **Addresses a genuine gap in NTK theory.** The paper tackles the underexplored regime where both depth and width increase, with width dominating depth. This fills a missing piece between the fixed-depth NTK (Jacot et al., 2018a) and the depth-dominated stochastic regime (Hanin & Nica, 2020). The paper correctly identifies that prior NTK analysis assumed kernel invertibility and did not cover the singular limiting case.

2. **Novel technical machinery.** Using rough differential equations (RDEs) to analyze the convergence of the NTK predictor in the singular-kernel limit is a creative and potentially productive approach. The interpolation argument in Theorem 3, if correctly justified, provides a way to reason about the limiting predictor without requiring the kernel matrix to be invertible in the limit — a genuine technical advance over Xiao et al. (2020).

3. **Clear characterization of kernel convergence.** Proposition 4 and Theorem 2 provide a clean, explicit characterization of how the normalized NTK evolves with depth, including the monotonic convergence to 1. The definition of the normalization $\bar{\Theta}_\infty^{(L)} = \frac{n_0 2^{L-1}}{L} \Theta_\infty^{(L)}$ is well-chosen to highlight the depth-dependent scaling.

4. **Abstraction beyond ReLU.** The paper identifies three abstract properties (Section 6) that allow the results to generalize to other kernel families beyond the ReLU NTK. This conceptual distillation is valuable for future theoretical work on deep kernel methods.

5. **Honest scope limitation.** The paper explicitly acknowledges that its analysis does not cover the stochastic regime (Hanin & Nica, 2020) where depth dominates width, and correctly situates itself in the complementary deterministic regime.

## Weaknesses
### W1 (Major) — Undefined notation in Theorem 3
The paper carefully defines $\Theta_\infty^{(L)}$ and $\bar{\Theta}_\infty^{(L)}$, but Theorem 3 and the surrounding text use $\tilde{\Theta}_\infty^{(L)}$ without ever defining this symbol. Based on context, $\tilde{\Theta}_\infty^{(L)}$ appears to be the normalized kernel $\bar{\Theta}_\infty^{(L)}$, but this is never stated. Since Theorem 3 is the paper's central theoretical contribution, this omission makes the main result ambiguous and prevents readers from independently verifying the claims. **Fix**: Add an explicit definition of $\tilde{\Theta}_\infty^{(L)}$ before Theorem 3.

### W2 (Major) — Lemma 1 (correlation convergence) is stated without proof
Lemma 1 claims $\rho^{(L)}(x,x') \to 1$ as $L\to\infty$ for $\rho^{(1)}\in(-1,1)$, but no proof is provided. This result is essential — it drives Proposition 4, Theorem 2, and the entire asymptotic analysis. While convergence can likely be established by analyzing the fixed point of the map $g(\rho)$ from Proposition 2, the paper does not provide this analysis. **Fix**: Add a concise proof showing that $g$ is increasing, maps $[0,1]$ to itself, has a unique fixed point at $\rho=1$, and the sequence $\rho^{(L)}$ converges monotonically. A symmetry argument handles negative $\rho^{(1)}$.

### W3 (Major) — Theorem 3 proof contains an unjustified determinant manipulation
The proof of Theorem 3 (Page 7, lines 112-116) attempts to bound a ratio of determinants by replacing $\det(A_n^{(L+1)}(t))$ with $\det(\tilde{\Theta}_\infty^{(L+1)}(XX^\top))^{\psi_{\mathcal{D}}(2t-1)} \det(\tilde{\Theta}_\infty^{(L)}(XX^\top))^{1-\psi_{\mathcal{D}}(2t-1)}$. This step assumes that the determinant of a convex combination of matrices equals the corresponding weighted product of determinants, which is not generally true unless the two matrices commute and are simultaneously diagonalizable — a property not established in the paper. **Fix**: Either (a) prove that $\tilde{\Theta}_\infty^{(L)}$ and $\tilde{\Theta}_\infty^{(L+1)}$ are simultaneously diagonalizable (which holds if they converge to the same rank-1 matrix), or (b) restructure the proof using a different approach such as the Woodbury formula for nearly-singular kernel matrices.

### W4 (Major) — Theorem 3 statement's logical structure is unclear
The theorem asserts existence of paths $v_{ij}^{(L)}$ that converge to 0 and "drive" a differential equation whose solution equals the NTK predictor. However, the relationship between the paths $v_{ij}^{(L)}$, the matrix $A_n^{(L+1)}(t)$, and the NTK predictor is not stated in the theorem — it is only revealed during the proof. Additionally, the claim $\frac{d}{dt}u_i^{(L)}(t)=0$ appears contradictory because $u^{(L)}(t)$ is driven by a non-trivial RDE (due to $v_{ij}^{(L)}$), not a trivial ODE. The theorem mixes the limiting behavior ($v\to 0$ implying $u$ becomes constant) with the finite-L case. **Fix**: Restructure Theorem 3 as three clear claims: (a) construction of $A_n^{(L)}(t)$ and $b_n^{(L)}(t)$; (b) the solution $u^{(L)}(t)$ to $A_n^{(L)}u=b_n^{(L)}$ satisfies $u^{(L)}(1) = \tilde{\Theta}_\infty^{(L)}(x^\top X)^\top (\tilde{\Theta}_\infty^{(L)}(XX^\top))^{-1}$; (c) as $L\to\infty$, $u^{(L)}(1)$ converges to a bounded limit.

### W5 (Moderate) — Proposition 1 proof sketch is insufficient
The proof sketch for the closed-form NTK under perfect correlation contains a non-sequitur ("$\mu = 0$ implies $x^\top x' \geq 0$ with probability $\frac12$") and does not show the induction step. Since Proposition 1 is used to derive the normalization in Definition 4, this undermines a foundational calculation. **Fix**: Provide a complete induction showing $(\Sigma^{(l)},\dot{\Sigma}^{(l)})$ satisfy the claimed recurrences.

### W6 (Moderate) — Experiments are too limited to validate theoretical claims
The experimental section (Section 6) tests only two datasets (synthetic uniform and MNIST) with modest depth ($L=30$) and no quantitative convergence rate estimation. The paper claims "sublinear" convergence and "exponentially faster" predictor convergence, but no rates are actually computed. The claim about "convergence to the limiting solution is fast, provided the determinant is small" is stated as a hypothesis, not a validated finding. **Fix**: (a) Compute convergence rates numerically (log-log slopes); (b) Test on at least one additional dataset with varying $n_0$ and $n$; (c) Validate Theorem 3's prediction by comparing finite-$L$ NTK predictor with the extrapolated limit.

### W7 (Minor) — Introduction narrative is too generic
The first paragraph of the Introduction opens with broad truisms about ML and does not clearly state the technical gap until late in the paragraph. The contribution claims are interleaved with defensive positioning against prior work. **Fix**: Restructure to follow: motivation (depth+width scaling gap) $\to$ technical challenge (kernel singularity) $\to$ proposed approach (RDE machinery) $\to$ key results $\to$ comparison with prior work.

### W8 (Minor) — Related Work lacks thematic organization
The Related Work section reads as a chronological list of papers rather than grouping by topic (NTK foundations, depth analysis, spectral analysis, stochastic vs. deterministic regimes). **Fix**: Reorganize into thematic subsections.

### W9 (Minor) — Conclusion introduces unsupported claims
The conclusion hypothesizes about a "pointwise limit" for the stochastic regime (Hanin & Nica, 2020) and claims generalizability to CNNs without any supporting evidence. **Fix**: Remove speculative statements and keep conclusion bounded to validated results.

### W10 (Minor) — Textual duplication error
In the conclusion-like paragraph (line 190), the phrase "convergence for the limiting kernel" appears twice in the same sentence with contradictory descriptions (sublinear vs. fast), creating confusion. The second instance should refer to the limiting predictor, not the limiting kernel. **Fix**: Replace the second instance with "the convergence of the NTK predictor to its limit is experimentally fast."

### W11 (Minor) — Sphere projection assumptions limit applicability without discussion
The paper's results require data to lie on the sphere $S^{n_0-1}$, requiring a projection step for arbitrary data. The effect of this projection (norm information loss, distance distortion for stereographic projection) on the depth-dependent kernel behavior is not discussed. **Fix**: Add a remark on practical applicability and discuss whether the asymptotic predictions are projection-dependent.

### W12 (Minor) — Related Work omits positioning on singular kernel literature
The paper distinguishes itself from Xiao et al. (2020) on the invertibility assumption but does not discuss how its results relate to Seleznova & Kutyniok (2022) on NTK singularity, beyond a brief mention. A more detailed comparison — including whether the singular limit characterized here is the same as the "ordered phase" singularity in Xiao et al. (2020) — would help readers understand the novelty. **Recommendation**: Add a short comparison paragraph explaining how the singular limit in Theorem 2 relates to the phase diagram of Xiao et al. (2020).

## Score
**Final Score: 5/10**

The paper addresses a meaningful gap in NTK theory and introduces an interesting technical approach (RDEs for singular-kernel analysis). However, several major defects significantly reduce confidence in the claimed results:

- The central theoretical result (Theorem 3) relies on an undefined notation ($\tilde{\Theta}_\infty^{(L)}$) and a proof step (determinant inequality chain) that is not mathematically justified without additional assumptions.
- A foundational lemma (Lemma 1 on $\rho^{(L)}\to 1$) is stated without proof, yet all asymptotic results depend on it.
- The empirical validation is too limited in scope and quantitative depth to serve as convincing support.

These issues are fixable, but in their current form they prevent the paper from meeting the standard for acceptance at a top venue. The paper's strengths — the research question, the RDE framework, and the abstract kernel properties — are real and provide a foundation for a stronger revised version.

**Post-Revision Target: [6, 7]/10**

A revision that addresses the proof gaps (especially the determinant inequality and Lemma 1 proof), clarifies the Theorem 3 statement, provides a definition for $\tilde{\Theta}_\infty^{(L)}$, and adds basic experimental validation of the predicted convergence rates could raise the paper to a score of 6-7. Reaching the top of this range would require a clean resolution of the determinant argument and a validation experiment showing the limiting predictor from Theorem 3 matches finite-$L$ NTK predictions.