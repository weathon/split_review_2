## Summary

This paper proposes a simplified spectral algorithm for community detection in the two-community stochastic block model (SBM) under constant edge density. The authors claim that by eliminating the degree-based preprocessing step and the correction stage from the original algorithm of Chin et al. (2015), their streamlined method achieves information-theoretic error bounds with fewer steps. They provide theoretical analysis using Chernoff bounds and normal approximations, along with experimental validation across varying graph sizes.

## Strengths

- **Addresses an important problem**: Community detection in the SBM is a fundamental problem in network analysis, and improving the understanding of spectral methods has clear value to the community.
- **Interesting empirical observation**: The experimental finding that Spectral Partition alone may achieve better performance than previously proven bounds is a worthwhile observation that could motivate further theoretical work.
- **Multiple analytical approaches**: The paper attempts to validate its claims through Chernoff bounds, Monte Carlo simulation, normal approximations, and direct algorithm experiments, showing effort to triangulate the results.

## Weaknesses

### Fatal

- **The paper does not prove its central claim.** The authors claim that Spectral Partition alone achieves the inverse-logarithmic error rates of Theorem 1.3 (the information-theoretic bound), but they provide no rigorous proof. The "proof" in Section 3.4 consists of setting up a convex optimization problem with constraints derived from Chernoff bounds, then stating that solving this optimization numerically yields Equation 11. No actual solution of the optimization is presented, no closed-form bound is derived, and the claimed result (Equation 11) is presented without derivation. The paper states "Our theoretical analysis predicts this maximum should satisfy (proof in the appendix)" but the appendix is truncated and contains no such proof.

- **The empirical relationship in Equation 13 is not theoretically justified.** The paper claims that the experimental results fit $\sin \theta = C/\sqrt[3]{\log 2/\gamma}$ and that this "directly yields the final result stated in Theorem 1.3." This is a non-sequitur. Theorem 1.3 requires $\frac{(a-b)^2}{a+b} \geq C_2 \log(2/\gamma)$, which relates the SBM parameters to the error rate. The empirical fit in Equation 13 relates $\sin \theta$ to $\gamma$ with no connection to $a$ and $b$. The paper never bridges this gap.

- **The claimed improvement over Theorem 3.2 is not substantiated.** The paper argues that Theorem 3.2 is "sharp" in general but not for the specific vectors produced by the spectral algorithm. However, the analysis in Sections 3.3-3.5 does not actually prove a tighter bound. The Chernoff analysis produces constraints that depend on $C$, which itself depends on $a$ and $b$ in a complex way, and the resulting bound (Equation 11) is never compared to the original bound (Equation 8) in terms of the relationship between $\gamma$ and $(a-b)^2/(a+b)$.

- **The paper does not demonstrate that the simplified algorithm achieves the claimed information-theoretic bounds.** The experiments show that the algorithm works, but they do not establish that the error rate satisfies the condition in Theorem 1.3. The experiments use fixed $a=0.06n$ and $b=0.04n$, so $(a-b)^2/(a+b) = (0.02n)^2/(0.1n) = 0.004n$, which grows linearly with $n$. The paper never checks whether the observed $\gamma$ values satisfy the required inequality.

### Major

- **The paper claims to eliminate the Correction step but does not compare against the full two-stage algorithm.** The experiments only test the simplified Spectral Partition. Without comparing against the original two-stage algorithm (Spectral Partition + Correction), the paper cannot support its claim that the Correction step is "unnecessary." The Correction step might still improve performance in regimes where Spectral Partition alone is insufficient.

- **The theoretical analysis of the simplified algorithm is incomplete.** The paper states that Theorem 2.2 (bound on $\|M'\|$) holds without the deletion step "with only modest increases in the constants," but the proof is relegated to the (truncated) appendix. Even if this is true, the paper does not show that the rest of the original analysis (Theorem 3.1, Theorem 3.2) still holds without the deletion step. The entire theoretical framework of the original paper depends on the deletion step, and the current paper does not reconstruct it.

- **The Monte Carlo analysis in Section 3.5 has a fundamental flaw.** The paper generates samples of $A\mathbf{u}_2$ entries and then uses Equation 9 to compute $\cos \theta$ for a given error level $k$. But Equation 9 assumes a specific ordering of the $x_i$ entries (sorted descending) and a specific pattern of misclassifications (the $k$ smallest-magnitude entries from each community). The paper does not justify that the actual eigenvector entries from the spectral algorithm follow this optimal misclassification pattern. The simulation generates independent samples from the approximate distribution of $A\mathbf{u}_2$ entries, but the actual eigenvector $\mathbf{v}_2$ is not simply a scaled version of $A\mathbf{u}_2$—it is the result of a spectral decomposition that introduces dependencies.

- **The paper's central claim contradicts established results.** The information-theoretic lower bound (Equation 2) states that when $\frac{(a-b)^2}{a+b} \leq c \log(1/\gamma)$, recovery is impossible. The original two-stage algorithm achieves the matching upper bound. If Spectral Partition alone achieved the same bound, this would be a significant theoretical advance, but the paper provides no rigorous proof and the experimental evidence is insufficient given the asymptotic nature of the claim.

### Minor

- **The paper does not specify the constants in its bounds.** The original Theorem 1.3 has explicit constants $C_1, C_2$. The paper's analysis produces bounds with unspecified constants, making it impossible to verify whether the claimed improvement is meaningful.

- **The experimental setup uses a narrow parameter range.** All experiments use $a=0.06n$ and $b=0.04n$, which gives a fixed ratio $(a-b)^2/(a+b) = 0.004n$. The paper does not explore different values of $a$ and $b$ to test whether the simplified algorithm works across the full parameter range where Theorem 1.3 applies.

- **The paper claims that "perfect community recovery ($\gamma=0$) is achievable even when the eigenvectors are not perfectly aligned ($\sin \theta > 0$)."** This is trivially true—the partition is based on the sign of the eigenvector entries, not on exact alignment. The relevant quantity is whether the signs of $\mathbf{v}_2$ match the signs of $\mathbf{u}_2$, not the angle between them. The paper's focus on $\sin \theta$ as the key metric is somewhat misplaced.

### Trivial

- The paper repeatedly refers to "Theorem 3.2" as establishing $\gamma \leq C_2 \frac{\sqrt{a+b}}{a-b}$, but this is actually the bound from Theorem 2.1 (the Spectral Partition bound). The paper's numbering is confusing.

## Nice-to-Haves

- A comparison against the full two-stage algorithm (Spectral Partition + Correction) would strengthen the claim that the Correction step is unnecessary.
- Experiments across a wider range of $(a,b)$ values, including regimes near the information-theoretic threshold, would provide stronger empirical support.
- A rigorous proof that the simplified algorithm achieves the inverse-logarithmic bound, or at least a clear statement of what is proven versus conjectured.

## Novel Insights

None beyond the paper's own contributions. The observation that Spectral Partition may perform better than its proven bounds is interesting but not rigorously established. The paper does not provide a new theoretical technique or a fundamentally new algorithm—it proposes removing steps from an existing algorithm and provides heuristic analysis.

## Suggestions

1. Clearly separate what is proven from what is conjectured. The paper currently presents the Chernoff analysis as if it proves the inverse-logarithmic bound, but it does not.
2. Compare the simplified algorithm against the original two-stage algorithm experimentally to support the claim that the Correction step is unnecessary.
3. Test the algorithm across a range of $(a,b)$ values, not just one fixed ratio.
4. Provide a rigorous proof that the simplified algorithm satisfies the conditions of Theorem 1.3, or revise the claims to match what is actually proven.

## Score and Decision

The paper addresses an interesting question and makes an empirical observation that could be valuable, but it does not deliver on its central claims. The theoretical analysis is incomplete, the claimed improvement over existing bounds is not proven, and the experimental validation is insufficient to support the strong conclusions. The paper would need substantial revision and additional theoretical work to be acceptable.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>