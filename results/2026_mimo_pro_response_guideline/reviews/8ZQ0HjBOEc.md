Now I have enough calibration data. Let me finalize my assessment.

**Calibration summary:**
- **YN4uWzcbtt (4.25, rejected)** — "Positive Definiteness of NTK": Mathematically clean but incremental, no experiments, limited practical discussion. Our paper is more novel.
- **WH9NhxOeu9 (5.00, rejected)** — "Sharp Generalization for NTK": NTK generalization bound, mixed reviews. Our technique is more novel.
- **VEJzjAvaIy (5.75, accepted)** — "Divergence of NTK in Classification": NTK theory with surprising negative result. Polarizing (8,6,6,3). Comparable level of contribution to our paper.
- **GqI4fTVUXC (6.00, rejected)** — "Disconnect Between Theory and Practice": Empirical NTK study. Well-written, interesting finding, but rejected.
- **5EtSvYUU0v (6.00, rejected)** — "Connecting NTK and NNGP": Interesting unifying idea but lacked rigor. Our paper is more rigorous.
- **O6znYvxC1U (6.33, accepted)** — "Bayesian Treatment of Spectrum": Novel theoretical connections between kernel theory and random matrix theory. More comprehensive.
- **tMzPZTvz2H (7.00, accepted)** — "Generalization of Scaled Deep ResNets": Stronger practical implications and generalization bounds.

**Initial bracket: 5.0–6.0.** Our paper is clearly above 4.25 (more novel technique), comparable to 5.75 (accepted), but slightly below the 6.0-6.33 range (less practical validation, less comprehensive framework). Score: **5.5**.

## Summary

This paper analyzes the neural tangent kernel (NTK) of overparameterized fully-connected ReLU networks as depth L → ∞ under the regime width ≫ depth. The main results are: (1) the normalized limiting kernel converges entry-wise to the matrix of ones (Theorem 2), becoming singular; (2) despite this singularity, the prediction expression κ_x κ^{-1} converges to a well-defined, bounded limit (Theorem 3), proven using rough differential equation (RDE) machinery via the Lyons Universal Limit Theorem. The paper also distills three checkable kernel properties for generalization to other kernel families and provides empirical convergence-rate illustrations.

## Strengths

1. **Novel proof technique using rough differential equations (Theorem 3, lines 173–225):** The paper formulates the prediction expression κ_x κ^{-1} as a system of differential equations driven by paths whose rough path lifts converge, applying the Lyons Universal Limit Theorem to establish a well-defined limit even as the kernel matrix degenerates. This is a genuinely creative proof approach new to the NTK literature.

2. **Resolution of the invertibility gap in Xiao et al. (2020) (lines 227–228):** The paper directly addresses the open problem left by Xiao et al., where the proof required invertibility of a decomposed limiting matrix. Theorem 2 guarantees the determinant converges to 0 (making Xiao et al.'s proof inapplicable), and Theorem 3 provides the replacement result without requiring invertibility. This is a concrete, verifiable contribution.

3. **Well-scoped theoretical framework (line 129):** The paper precisely specifies its regime L ∈ o(min n_i) and explicitly distinguishes it from Hanin & Nica (2020), where depth-to-width ratio can be arbitrary and the NTK becomes stochastic. This careful delineation avoids overclaiming.

4. **Distillation of generalizable kernel conditions (Section 6, lines 237–241):** The paper identifies three essential properties—diagonal dominance, positive definiteness for sufficiently large L, and convergence of the normalized determinant to zero—that separate the proof technique from the specific ReLU NTK, enabling application to other architectures.

## Weaknesses

### Fatal

None.

### Major

- **The limiting predictor C(x) is not functionally characterized.** Theorem 3 establishes that κ_x κ^{-1} converges to a limit, and that C(x) is continuous and bounded on S^{n₀-1} and equals e_i at training points (lines 187–191). However, for test points x ∉ X, the paper provides no description of what the limiting predictor actually computes. Without knowing the functional form of C(x), it is difficult to assess whether this limiting behavior is useful, benign, or degenerate. The paper's stated goal is to "understand the role of depth," but understanding is limited without knowing what the limit *does*. This substantially constrains the paper's significance.

- **Experiments are convergence visualizations of mathematical quantities, not validation of practical relevance.** Section 6 and Figure 1 plot kernel entries and the ratio κ_x κ^{-1} for depths L = 1,...,30 on synthetic uniform-on-sphere data (n₀ = 128) and MNIST. No actual neural network training is performed, no generalization performance is measured, and no comparison with finite-width/finite-depth networks is conducted. The most natural reader question—"Does this matter for actual networks?"—goes unanswered. Even a single experiment comparing NTK predictions at depth L with trained network outputs would substantially strengthen the paper.

### Minor

- **Generalization to other kernels is claimed but not proven.** Section 6 (lines 237–243) lists three properties and provides the η^(L) example, but never proves these conditions are *sufficient* for Theorem 3 to apply. The conclusion (line 262) overstates this: "we provided a list of key properties that were necessary to obtain our results to generalize to other kernels" — these are identified properties used in the proof, not proven sufficient conditions for arbitrary kernel families.

- **Writing errors.** Line 227 is missing the inverse symbol — it reads `Θ̃_∞^(L)(XX^⊤)` but should be `(Θ̃_∞^(L)(XX^⊤))^{-1}`. Line 262 contains a self-contradictory sentence: "while convergence for the limiting kernel is sublinear, the convergence for the limiting kernel is experimentally fast" — the second "limiting kernel" should be "limiting solution" (κ_x κ^{-1}). These undermine the paper's clarity.

- **Unsupported claim about CNN adaptation (line 247).** The paper states "the proof technique of Theorem 3 can be adapted to other kernels that arise from other architectures such as CNNs" without providing any sketch, evidence, or demonstration of this adaptation.

### Trivial

None.

## Nice-to-Haves

- An explicit rate bound for the convergence of κ_x κ^{-1} (even a loose one) would make the "fast convergence" claim precise rather than empirical.
- Discussion of the gap between the NTK regime (width ≫ depth) and practical network widths.
- Numerical visualization of C(x) on a fine grid of test points for a small dataset (e.g., n=5, n₀=3) to convey what the limiting function actually looks like on the sphere.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Notation inconsistency (Θ̃ vs Θ̄):** The paper defines Θ̄_∞^(L) (bar) in Definition 4 (line 139) but Theorem 3 uses Θ̃_∞^(L) (tilde) throughout (lines 183–227). This appears to be a parser artifact (overline → tilde conversion in some equations), not an actual inconsistency in the original paper. Removed per formatting artifact rule.

- **Proof sketch gap in inequality chain (lines 220–222):** The harsh critic flagged that replacing the geometric mean of determinants with their product requires both determinants to be < 1, and the paper's justification ("for L large enough, the strictly positive determinants are all smaller than 1") may need more support. However, the full proof is in the appendix (stripped by parser), so this cannot be verified as a genuine gap. Demoted from a standalone weakness.

## Novel Insights

The application of rough differential equations to handle the degenerate kernel limit in the NTK framework is genuinely novel. The key insight—that the ratio κ_x κ^{-1} converges even as the kernel matrix becomes singular because the driving terms of the associated RDE vanish faster than the determinant shrinks—provides a new analytical tool for the NTK literature. The resolution of the specific invertibility gap left by Xiao et al. (2020) fills a concrete open question. The paper also makes a useful observation about the differential convergence rates: the kernel converges slowly (logarithmically) while the prediction formula converges rapidly, which has practical implications for moderate-depth networks.

## Suggestions

- Characterize C(x) numerically on a grid of test points for a small dataset to convey what the theory says about the learned function.
- Add at least one experiment comparing NTK predictions at depth L with trained finite-width network outputs.
- Frame the generalization to other kernels as a conjecture with supporting evidence rather than implying it is proven.
- Fix the two writing errors: the missing inverse on line 227 and the contradictory sentence on line 262.

## Calibration Anchors

| Anchor | Path | Avg Human Score | Round | Comparison |
|--------|------|----------------|-------|------------|
| Weak Correlations in Gradient-Based Learning | 2NwHLAffZZ | 2.33 | 1 | Less novel technique, rejected for incremental contribution |
| NTK with Derivative Labels | fUz6Qefe5z | 3.00 | 1 | NTK extension paper, rejected |
| Faster GD in Deep Linear Networks | NbbsRnPBoS | 2.33 | 1 | Related depth analysis, rejected |
| Understanding GD through Training Jacobian | kkVTeMvC9D | 3.40 | 1 | NTK-adjacent, rejected for limited novelty |
| Positive Definiteness of NTK | YN4uWzcbtt | 4.25 | 1 | Most topically similar rejected paper; clean result but incremental |
| Infinitely Deep ResNets as GPs | 3LLkES6nNs | 4.25 | 1 | Related depth analysis, rejected for weak presentation |
| Sharp Generalization for Over-Parameterized NNs | WH9NhxOeu9 | 5.00 | 2 | NTK generalization bound, mixed reviews |
| Adversarial Attacks as Near-Zero Eigenvalues | r5d8zkYizS | 5.33 | 2 | Kernel analysis, rejected |
| Divergence of NTK in Classification | VEJzjAvaIy | 5.75 | 1 | Closest comparison: NTK theory paper, accepted with similar contribution level |
| Connecting NTK and NNGP | 5EtSvYUU0v | 6.00 | 1 | Interesting idea but lacked rigor; our paper is more rigorous |
| Disconnect Between Theory and Practice | GqI4fTVUXC | 6.00 | 2 | Empirical NTK study, rejected despite good writing |
| Novel Kernel Models Beyond Over-Parameterization | kOtFuzoA93 | 4.00 | 1 | Kernel theory, rejected |
| Bayesian Treatment of Empirical Kernel | O6znYvxC1U | 6.33 | 2 | Novel kernel theory, accepted; more comprehensive |
| Generalization of Scaled Deep ResNets | tMzPZTvz2H | 7.00 | 1 | Stronger practical implications; our paper is weaker |
| Sharper Guarantees for NN Classifiers | h7GAgbLSmC | 7.00 | 1 | Stronger generalization bounds |
| Exploring Activation Functions in Neural ODEs | AoraWUmpLU | 8.00 | 1 | Much stronger contribution |

**Round 1 bracket: 5.0–6.0.** Our paper is clearly above the 4.25 NTK positive definiteness paper (novel RDE technique vs. incremental relaxation), comparable to the 5.75 "Divergence of NTK" paper (both are solid NTK theory contributions), but slightly below the 6.0–6.33 range (those papers had either better experimental validation or more comprehensive theoretical frameworks). Final score: **5.5**.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>