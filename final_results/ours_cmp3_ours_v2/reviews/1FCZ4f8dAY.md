Now I have all the calibration data I need. Let me write the final review.

## Summary
This paper provides a unified theoretical framework for constructing equivariant polynomial (and entire) functions on tensors under three classical Lie groups: the orthogonal group O(d), the indefinite orthogonal group O(s,d-s) (including the Lorentz group), and the symplectic group Sp(d). Using classical invariant theory, it characterizes these functions as linear combinations of tensor products of inputs with group-isotropic tensors, with coefficients that are functions of invariant inner products. Corollary 1 gives a concrete, implementable parameterization for the practically important case of vector inputs and tensor outputs. Experiments on stress-strain prediction, path signature approximation, and sparse vector estimation demonstrate that the equivariant models outperform non-equivariant baselines.

## Strengths
- **A genuinely unified theoretical framework.** The paper characterizes O(d)-, O(s,d-s)-, and Sp(d)-equivariant polynomial (and entire) functions on tensors within a single invariant-theoretic framework, covering parity/pseudotensors. This level of generality — covering three classical Lie groups and handling arbitrary-order tensor inputs — is a clear advance over existing results that are group-specific (e.g., O(d) only) or method-specific (e.g., Clebsch–Gordan for small d). The connection to classical invariant theory (Jeffreys 1973; Roe Goodman 2009) is well-articulated and translated into a form usable by ML frameworks.
- **Corollary 1 provides a concrete, implementable architecture.** The parameterization in (11) — where an equivariant function from vectors to a k'-tensor is expressed as a linear combination of tensor products of input vectors and Kronecker deltas, with coefficients that are functions of the pairwise inner products — is clean, interpretable, and directly implementable. The paper is honest about its computational complexity (O(k'! n^{k'} (Q d n^2 + d^{k'}))) and the regime where it is practical (k' ∈ {1,2,3,4}).
- **The stress-strain experiment shows a genuinely large improvement.** In Table 1, the proposed method outperforms the MLP baseline, the augmented MLP, and the TFENN equivariant method by roughly one to two orders of magnitude across all dataset sizes. This is a striking result.
- **Honest treatment of the relationship to Clebsch–Gordan methods.** The paper explicitly acknowledges (Related Work) that CG-based methods "are more memory efficient than our general formulation" and that the methods should have equivalent computational and approximation power for the Corollary 1/3 setting. This contextualizes the contribution realistically.

## Weaknesses

### Fatal
None.

### Major
- **No comparison against the closest related equivariant methods on O(d) tasks.** The paper discusses e3nn (Geiger & Smidt 2022), escnn (Cesa et al. 2022), and Domina et al. (2025) as the closest related work, noting that these CG-based methods are "specific for SO(d) and O(d) for d=2,3." Yet in all three experiments, the only equivariant baseline is TFENN (stress-strain only), and even that is transcribed from Garanger et al. (2024) rather than re-run under controlled conditions. For the path signature and sparse vector experiments, there are *no equivariant baselines at all*. This gap means the experiments cannot substantiate any practical advantage of this specific parameterization over existing equivariant methods on O(d) problems — they only demonstrate that enforcing equivariance helps (a well-established finding). The paper would be substantially strengthened by a direct comparison against e3nn or similar on at least the stress-strain problem, where the method's performance advantage is largest.

- **Path signature experiment lacks any equivariant baseline.** Table 2 compares against MLPs (same width, same parameters, augmented with 4 rotations) and a discrete approximation. There is no comparison against any existing equivariant method. The large improvement over the augmented MLP (0.007→0.002 for O(d); 0.186→0.005 for Lorentz) is suggestive but hard to interpret without knowing whether a standard equivariant baseline would achieve similar performance. This is especially important because the paper's own related-work discussion centers on CG-based methods as the closest competitors.

### Minor
- **Sparse vector results are more nuanced than the text suggests.** While the method performs well overall, SoS wins on multiple settings (Bernoulli-Gaussian under all three covariance types: Random 0.962 vs 0.937, Diagonal 0.949 vs 0.463, Identity 0.962 vs 0.342). The full "Ours" model also underperforms "Ours (Diag)" on Diagonal and Identity covariances for several sampling methods. The paper acknowledges the BG exception (line 293) but the overall framing emphasizes successes. A more balanced discussion would help readers assess the method's regime of advantage.

- **No runtime, memory, or scaling measurements.** The paper acknowledges the O(k'! n^{k'}) complexity (line 135), and notes that CG methods "are more memory efficient than our general formulation" (line 33). However, no wall-clock times, GPU memory usage, or scaling curves are provided for any experiment. Without efficiency data, the practical competitiveness claim is unsubstantiated.

- **Symplectic group appears prominently but is never tested.** The title and contributions prominently feature the symplectic group, and Corollary 3 covers Sp(d). Yet none of the three experiments involve symplectic equivariance. While a theory paper need not experimentally validate every group covered, the prominence of Sp(d) in the framing raises unmet expectations.

- **No limitations paragraph.** The Discussion section (Section 6) is brief and does not discuss computational scaling, the restriction to small k', or when the method might fail. A candid limitations discussion would strengthen the paper.

### Trivial
- **Minor notation inconsistency in Corollary 1.** The sum over permutations is written as σ ∈ S_k (line 129) but the surrounding text and Figure 1 caption refer to S_{k'} (line 135, line 173). Since the output is a k'_{(+)}(+)-tensor, S_{k'} is correct.

## Nice-to-Haves
- A direct computational comparison against e3nn/escnn on the stress-strain problem, with wall-clock and memory measurements.
- An ablation study testing which components of the parameterization matter most (e.g., restricting the q functions to not depend on certain inner products).
- A brief discussion of when the method is likely to fail (e.g., large k' or large n).

## Removed Points
These points from the harsh review were removed after verification against the paper:
- **"Universally expressive" overpromises**: Removed because Remark 1 (line 137) justifies the claim via Stone-Weierstrass approximation on compact sets, which is standard usage in the ML theory literature. The paper explicitly qualifies that the architecture can approximate continuous equivariant functions on compact sets.
- **Small number of trials (3-5)**: Removed because 3-5 trials with standard deviations are standard for neural network experiments of this type, and the paper reports variance.
- **Clebsch–Gordan methods "can in principle extend to higher d"**: Removed because the paper's statement about *current implementations* (d=2,3) is factually accurate; the possibility of extension is speculative.
- **No positive definite constraint handling**: Removed because the paper does not claim to enforce this property; the physics formula (23) maps SPD input to SPD output by construction, and the model learns the mapping.
- **Path signature needs cubature/ODE baselines**: Removed because the discrete Riemann-sum approximation included in the paper IS the standard baseline for signature approximation from discrete samples.
- **"Polynomial vs entire function" asymmetry unexplained**: Removed because the reason may be in the stripped appendix (Appendix G). Cannot verify whether this is addressed there.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add a comparison against e3nn or a similar CG-based equivariant method on the stress-strain benchmark, with runtime and memory measurements. This is the single most impactful improvement you can make.
2. Add an equivariant baseline to the path signature experiment, or clearly reframe that experiment as a proof-of-concept demonstrating Lorentz equivariance rather than a competitive benchmark.
3. Add a limitations paragraph to the Discussion section that honestly discusses the factorial-in-k' scaling, the restriction to small output tensor ranks, and the lack of symplectic experiments.
4. Fix the S_k/S_{k'} notation inconsistency in Corollary 1 (line 129).
5. Provide at least a brief scaling study showing wall-clock time vs. n and k'.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>