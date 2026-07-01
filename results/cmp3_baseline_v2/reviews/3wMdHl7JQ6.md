## Summary

This paper proposes a simplified spectral algorithm for community detection in the two-community stochastic block model (SBM) under constant edge density. The authors argue that by eliminating the degree-based preprocessing step and the correction stage from the original algorithm of Chin et al. (2015), the spectral partition alone achieves information-theoretic error rates. They provide theoretical analysis using Chernoff bounds and normal approximations, along with experimental validation, to support their claim that algorithmic simplification leads to both computational efficiency and enhanced performance.

## Strengths

- **Addresses an important question**: The paper tackles whether unnecessary algorithmic complexity can be removed from spectral community detection methods, which is a valuable direction for the field.
- **Clear motivation**: The observation that spectral partition alone might achieve inverse-log performance without correction is well-motivated and could have practical significance.
- **Multiple analytical approaches**: The paper attempts to validate its claims through Chernoff bounds, normal approximations, Monte Carlo simulation, and direct experiments, showing effort to provide comprehensive evidence.

## Weaknesses

### Fatal

1. **The core theoretical claim is not properly established**: The paper claims that spectral partition alone achieves the inverse-log relationship of Theorem 1.3, but the analysis does not actually prove this. The empirical fit in Equation 13 (sin θ = C/∛(log 2/γ)) is presented as a curve fit to experimental data, not a proven theoretical result. The paper states this "directly yields the final result stated in Theorem 1.3" but provides no rigorous proof connecting this empirical relationship to the required theoretical bounds.

2. **The optimization framework in Section 3.4 is fundamentally flawed**: The derivation of constraints from Chernoff bounds appears to contain serious mathematical errors. The "concentration constant" C is defined in a way that does not correspond to any standard Chernoff bound formulation. The constraints relating consecutive entries x_i/x_{i+1} to logarithms of C and indices are presented without any justification for how they follow from concentration inequalities. The final inequality (11) is stated without proof and its derivation is not provided in the appendix (which is stripped). This makes the entire theoretical contribution unverifiable.

3. **The claimed improvement over Theorem 3.2 is not demonstrated**: The paper argues that Theorem 3.2 (γ ≤ C₂√(a+b)/(a-b)) is not tight for the spectral algorithm's output, but the analysis in Sections 3.3-3.5 does not actually derive a provably tighter bound. The numerical optimization and simulation results show empirical relationships, not theoretical guarantees. The paper conflates empirical observations with theoretical improvements.

### Major

4. **The "simplification" claim is misleading**: The paper claims to eliminate the degree-based preprocessing step (step 2 of Spectral Partition), but Theorem 2.2 (the spectral norm bound) is stated to hold "without deletion, with only modest increases in constants" and the proof is relegated to the appendix. Without seeing this proof, the claim that the simplification preserves theoretical guarantees is unsubstantiated.

5. **Experimental setup has serious issues**: The experiments use a = 0.06n and b = 0.04n, which means a and b scale with n rather than being constants. This violates the constant edge density assumption stated in the abstract and the SBM formulation in Section 1 where a and b are constants. The paper uses a = 0.06n = 30 for n=500, which is not a constant. This makes the experimental results incomparable to the theoretical framework.

6. **The normal approximation justification is weak**: The paper claims the normal approximation is valid because "both np ≥ 20 and n(1-p) ≥ 20 hold," but with a = 0.06n, p = a/n = 0.06, so np = 0.06n. For n=500, np=30, which barely satisfies the condition. More importantly, the paper does not account for the dependence structure between entries of the eigenvector, which invalidates the assumption of independent normal entries.

### Minor

7. **Figure descriptions are confusing and partially contradictory**: The text describes Figure 4 with conflicting labels (e.g., "Chernoff-optimizer" is described as representing Theorem 3.2 in one place and as optimization results in another). The figure captions are repetitive and contain garbled text.

8. **The claim about perfect recovery with sin θ > 0 is not properly justified**: The paper states that "perfect community recovery (γ = 0) is achievable even when the eigenvectors are not perfectly aligned (sin θ > 0)" but does not provide a rigorous argument for why this would hold in general.

### Trivial

9. The paper uses "Spectral Algorithm" and "Spectral Partition" inconsistently to refer to different procedures.

## Nice-to-Haves

- A rigorous proof of the main theoretical claim (that spectral partition alone achieves inverse-log rates) would significantly strengthen the paper.
- Experiments with constant a,b values (not scaling with n) would make the results more directly comparable to the theoretical framework.
- A discussion of why the degree-based preprocessing step is unnecessary, with explicit bounds on the spectral norm without deletion.

## Novel Insights

None beyond the paper's own contributions. The observation that spectral partition might perform better than previously analyzed is interesting but not rigorously established. The "less is more" principle is stated as a conclusion but not convincingly demonstrated.

## Suggestions

1. Provide the complete proof that spectral partition alone achieves the inverse-log relationship claimed in Theorem 1.3, or clearly state that this remains an empirical observation.
2. Fix the experimental setup to use constant a,b values consistent with the theoretical framework.
3. Clarify the derivation of the Chernoff-based constraints and provide the missing proof of inequality (11).
4. Address the mathematical errors in the optimization framework, particularly the definition of the concentration constant C and the derivation of constraints on consecutive entries.

## Score and Decision

The paper addresses an interesting question but contains fatal flaws in its theoretical analysis and experimental setup. The core claim that spectral partition alone achieves information-theoretic bounds is not properly proven, and the mathematical derivations contain serious errors. The experimental validation uses parameters inconsistent with the theoretical framework. These issues invalidate the paper's main contributions.

MY FINAL SCORE: 3.0<score>3.0</score>
MY FINAL DECISION: Reject<decision>Reject</decision>