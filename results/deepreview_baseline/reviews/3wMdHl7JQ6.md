## Summary

The paper proposes a simplified spectral algorithm for two-community stochastic block models by removing a degree-based preprocessing step and the correction stage required in prior work. It claims that the simplified Spectral Partition alone achieves inverse-logarithmic error rates that approach information-theoretic limits. The authors provide theoretical analysis based on Chernoff bounds and normal approximations, along with numerical optimization and Monte Carlo simulations to support their claim, and validate on synthetic graphs.

## Strengths

- **Empirical observation of potential simplification**: The paper identifies that in practice, the spectral partition step may already yield strong performance without the correction stage, which is an interesting and potentially practically useful observation.
- **Clear motivation**: The idea that algorithmic simplification could improve both computational efficiency and performance is well-motivated and aligns with the "less is more" principle stated in the paper.
- **Reproducibility effort**: The authors provide parameter details, simulation counts, and state that code is submitted to reproduce figures, which is good practice.

## Weaknesses

### Fatal

1. **The main theoretical claim is not supported by any rigorous proof.** The paper asserts that the simplified spectral partition achieves the information-theoretic bound of Theorem 1.3 (inverse-log relation between error rate \(\gamma\) and the signal strength \((a-b)^2/(a+b)\)). However, the analysis presented is entirely about the relationship between \(\gamma\) and \(\sin\theta\) (the angle between true and estimated eigenvectors). The gap between \(\sin\theta\) and the condition on \((a-b)^2/(a+b)\) is never bridged. The paper states that Equation 13 combined with Theorems 2.2 and 3.1 "directly yields" Theorem 1.3, but provides no derivation or argument. This is a logical leap that invalidates the central claim.

2. **The entire theoretical analysis is heuristic and does not constitute a proof.** The Chernoff-derived optimization (Section 3.4) and the normal approximation (Section 3.5) are used to produce numerical bounds and fitted curves. The derivation of the constraints (the inequalities involving \(C\) and the decay rates) is sketched but not rigorously justified. The paper does not prove that the actual algorithm’s eigenvector entries satisfy these constraints with high probability. Instead, it assumes a distributional approximation (Equation 10) that has an \(O(1/\sqrt{n})\) error, and then draws conclusions about asymptotic rates without bounding this error propagation. Consequently, the claimed “improved error bounds” are not established as mathematical theorems.

### Major

1. **Empirical validation is insufficient to support the central claim.** The experiments use only one set of edge probabilities (\(a=0.06n, b=0.04n\)) and graph sizes \(n\in\{500,\dots,1000\}\). This range is small compared to the asymptotic regime in which the theoretical bounds are meant to apply (constants \(a,b>C_1\) where \(C_1\) may be large). The observed \(\gamma\) values are around 0.2–0.5 (Figure 5), far from the low-error regime needed to demonstrate the claimed inverse-log bound. Without experiments for larger \(n\) or different \((a,b)\) values, it is unclear whether the pattern generalizes.

2. **The empirical fit (Equation 13) is not derived and has questionable theoretical basis.** The paper fits \(\sin\theta = C/\sqrt[3]{\log 2/\gamma}\) to the spectral algorithm results but provides no explanation for why this specific functional form should arise. The claim that this form “bridges our results to established theoretical frameworks” is vague. The connection between this fitted curve and the conditions of Theorem 1.3 is not made explicit.

3. **The paper conflates the optimization analysis with the actual algorithm’s performance.** The Chernoff- and normal-based bounds (blue and green curves in Figure 5) are derived from hypothetical vectors that satisfy certain constraints or distributions, not from the actual eigenvector computed by the spectral algorithm. The paper does not prove that the spectral algorithm’s eigenvector lies within the feasible set of the optimization or matches the normal approximation. Thus, the agreement between the optimization/simulation results and the actual algorithm (orange points) is empirical, not theoretical.

### Minor

- The writing is occasionally unclear, particularly in describing the optimization constraints and the derivation of Equation 11. The steps from the Chernoff bound to the decay-rate inequalities are not explained.
- The paper claims that removing the degree-based deletion step “preserves statistical independence” in eigenvector entries, but does not exploit this property in any concrete analysis beyond a mention in the future work section.

### Trivial

- The caption of Figure 4 refers to a “Quadratic Lemma” that is never defined in the body of the paper.
- The notation \(M'\) is introduced for the case with deletion, but the proof of Theorem 2.2 without deletion is cited to the appendix, which is not accessible to the reviewer.

## Nice-to-Haves

- A clear theorem statement with a rigorous bound on \(\gamma\) in terms of \((a-b)^2/(a+b)\) would be necessary to support the paper’s title and abstract.
- Experiments with larger \(n\) (e.g., \(n=5000,10000\)) and varying \((a,b)\) pairs would significantly strengthen the empirical case.
- A comparison of running times between the original and simplified algorithm would demonstrate the computational benefit.

## Novel Insights

None beyond the paper’s own contributions. The observation that the correction step may be unnecessary in practice is empirically interesting, but the paper fails to provide a theoretical justification or a complete empirical characterization.

## Suggestions

1. Either provide a rigorous proof that Spectral Partition alone achieves the information-theoretic bound (Theorem 1.3), or substantially downscope the claims to an empirical study showing that the correction step can be omitted in practice under specific parameter ranges.
2. Derive a provable relationship between \(\sin\theta\) and the signal strength \((a-b)^2/(a+b)\) when using the simplified algorithm, and then combine it with the \(\gamma\)-\(\sin\theta\) analysis to obtain a bound on \(\gamma\).
3. Add experiments over a wider range of \(n\) (e.g., up to \(10^4\) or \(10^5\)) and over multiple \((a,b)\) values that satisfy the theoretical conditions (e.g., \(a=100, b=50\) scaled by \(n\)).
4. Clarify the derivation of the Chernoff-based constraints and the optimization problem; provide a proof that the spectral algorithm’s eigenvector satisfies these constraints with high probability.

## Score and Decision

The paper presents an interesting simplification but its main theoretical claim is unsupported. The analysis is heuristic, the empirical evaluation is limited, and the link between the analysis and the claimed information-theoretic bound is missing. Therefore, the paper does not meet the bar for acceptance at ICLR.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>