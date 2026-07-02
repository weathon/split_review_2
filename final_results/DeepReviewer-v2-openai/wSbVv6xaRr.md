## Summary
# Final Review Report

## Summary

This paper proposes FedMPDD, a federated learning algorithm that compresses client gradients by computing directional derivatives along multiple random Rademacher vectors, reducing uplink communication from O(d) to O(m) per client per round (m << d). The key idea is that averaging m projections yields an unbiased gradient estimator whose norm can be approximately preserved via the Johnson-Lindenstrauss lemma, achieving a convergence rate of O(1/√K) matching FedSGD. The paper further claims inherent privacy against gradient inversion attacks, arguing that the rank-deficient projection creates a gradient reconstruction error of (d-1)/m that is independent of gradient magnitude — unlike additive-noise methods. Experiments on MNIST and CIFAR-10 compare FedMPDD against QSGD, Top-k sparsification, lp-proj sketching, and SA-FedLora under fixed communication budgets, showing favorable accuracy-privacy trade-offs.

**Core contribution claims:**
- **C1:** Communication-efficient gradient compression via multi-projected directional derivatives
- **C2:** Inherent privacy against GIAs through rank-deficient projections (no additive noise needed)
- **C3:** O(1/√K) convergence rate matching FedSGD via multi-projection averaging

**Overall assessment:** The paper presents an interesting conceptual direction — using projected directional derivatives for joint communication efficiency and privacy in FL. However, there are significant gaps in theoretical presentation (undefined symbols in Theorem 2, dimensional inconsistencies in key notation, insufficient justification of descent claims), overstatement of privacy guarantees (no formal DP analysis, conflation of gradient reconstruction error with data privacy), and missing statistical rigor in experiments (no variance reporting). The novelty position relative to the large body of gradient compression and DP-FL literature cannot be fully assessed without external retrieval (deferred). The paper has potential but requires substantial revision before publication.

## Strengths
1. **Conceptually clean mechanism.** The use of projected directional derivatives for gradient compression is a well-motivated and geometrically intuitive idea. Averaging multiple random projections to overcome the dimension-dependent variance of a single projection (while preserving unbiasedness) is a principled solution. The connection to the Johnson-Lindenstrauss lemma for norm preservation is technically sound and provides a clear theoretical foundation for setting m = O(log(d)/ε²).

2. **Joint treatment of communication and privacy.** Unlike most prior work that treats communication compression and privacy as separate concerns (often with post-hoc privacy injection), FedMPDD attempts to address both through the same mechanism. The observation that rank-deficient projections create inherent gradient ambiguity — and that this ambiguity is independent of gradient magnitude — is a genuine insight that distinguishes the approach from additive-noise methods.

3. **Strong empirical results under constrained budgets.** Tables 1 and 2 convincingly show that FedMPDD operates effectively under tight communication budgets where FedSGD cannot function at all. The 356× communication reduction over FedSGD for the same target accuracy (CIFAR-10, Table 2) is impressive, and the SSIM values below 0.22 demonstrate meaningful empirical privacy protection against gradient inversion attacks.

4. **Tunable privacy-communication-accuracy trade-off.** The parameter m provides a clean, one-dimensional control knob between compression rate, convergence speed, and privacy level. This is practically useful because it allows deployment-specific tuning without changing the algorithm structure.

## Weaknesses
### W1. Factual inconsistency in convergence rate claim (Major)
The Abstract states that FedMPDD "converges at a rate of O(1/K), matching the performance of FedSGD," which contradicts Theorem 2 (Page 4) that establishes O(1/√K). This is not a minor typo — an O(1/K) rate (linear convergence in the strongly convex sense) is substantially faster than O(1/√K) (sublinear for non-convex). The abstract must be corrected to O(1/√K) to match the theorem. This error erodes reader trust in the theoretical claims.

### W2. Undefined symbols and missing assumptions in Theorem 2 (Major)
Theorem 2 references "Assumption 1" which is never stated in the main text, and uses symbols G and σ that are not defined anywhere in the main body. Without these definitions, the convergence bound is incompletely specified and cannot be verified. The main text should include at minimum: L-smoothness, bounded variance (σ²), and bounded gradient (G) assumptions. Currently, the theorem appears to assume knowledge from the appendix, which violates self-containedness.

### W3. Notation errors and dimensional inconsistencies in core definitions (Major)
The contribution paragraph (Page 1, line 15) states $\hat{\mathbf{g}}_i(\mathbf{x}_k) = \mathbf{U}_{k,i} \mathbf{g}_i(\mathbf{x}_k) \mathbf{U}_{k,i}$, which is dimensionally inconsistent regardless of whether $\mathbf{U}_{k,i}$ is a vector or a matrix. The correct form is either $(\mathbf{u}^\top \mathbf{g}) \mathbf{u}$ (scalar-times-vector for single projection) or $\frac{1}{m} \mathbf{U} \mathbf{U}^\top \mathbf{g}$ (matrix form for multi-projection). This error appears in the paper's primary definitional paragraph and signals incomplete proofreading of mathematical content. Similarly, Lemma 1's equation (6) uses the subscript $\mathbf{u}_{k,j}^{(j)}$ where it should refer to client i (not j).

### W4. Overstated privacy guarantees without formal DP analysis (Major)
The paper claims "strong and constant privacy level" and marks methods as "defendable" (Tables 1-2) based on low SSIM values and the gradient reconstruction error bound $(d-1)/m$. However:
- No $(\epsilon,\delta)$-differential privacy analysis is provided, which is the standard for privacy-preserving ML.
- Low SSIM under gradient inversion attacks does not constitute a general privacy guarantee. The connection between gradient reconstruction error and data reconstruction depends on problem-specific constants ($L_v(x)$ in Lemma 2) that are not quantified.
- The comparison with LDP uses "FedSGD + Laplace" without gradient clipping, which is not a proper DP baseline. Standard DP-FL methods (e.g., DP-SGD) require clipping + calibrated noise.
- The multi-round composition bound ($T \times m < d$) is stated without formal proof in the main text.

The privacy claims should either be backed by a formal $(\epsilon,\delta)$ analysis or substantially weakened to focus on empirical attack resistance.

### W5. No statistical significance in experimental results (Major)
All experiments report single-run point estimates without variance, confidence intervals, or multi-seed averages. This is a critical omission because:
- FedMPDD involves both random projections and random client sampling — inherent sources of variance.
- Performance margins between FedMPDD and baselines are sometimes small (e.g., 40.84% vs 38.11% in Table 2), making it impossible to assess statistical reliability.
- The comparison between different m values (Table 1: 77.37% vs 67.75% vs 58.49%) could be confounded by noise rather than reflecting a true trend.
- SSIM values in Table 1 are listed as "$\ll 0.03$" — an imprecise bound — while Table 2 shows exact values (0.14, 0.22), raising questions about measurement consistency.

### W6. Unsupported descent property claim (Major)
The paper states that unbiasedness of the projected directional derivative implies iterative successive descent, but this is not generally true. The descent lemma for SGD requires L-smoothness and a step size bounded by the inverse Lipschitz constant. For the single-projection case, the variance amplification of $\sqrt{d}$ means the descent condition requires $\eta \leq 1/(Ld)$, a much stricter condition than implied. The text should explicitly state the required assumptions and step-size regime for the descent property to hold.

### W7. Conclusion introduces unsupported claim (Minor)
The conclusion states "smaller m values sometimes yielded faster convergence with stronger privacy" without controlled experimental evidence. The observed effect (Table 1) is confounded by the fixed communication budget — larger m runs exhaust the budget earlier, so the comparison is not about convergence speed but about total usable communication. Additionally, the explanation that the nullspace effect "suppresses noise" is not theoretically justified.

### W8. Privacy-communication trade-off analysis lacks depth (Minor)
While the paper correctly identifies the trade-off governed by m, it does not provide practical guidance for choosing m. The JL-based setting $m = O(\log(d)/\epsilon^2)$ requires choosing $\epsilon$ and $\delta$, which are not intuitively connected to privacy or accuracy targets. A practitioner cannot easily determine whether m=400 or m=600 is appropriate for their deployment. The paper would benefit from a practical m-selection guideline.

### W9. Novelty verification deferred (Note)
Due to the unavailability of external literature search in this run, all novelty claims (including "first work to introduce projected directional derivative in FL") cannot be independently verified. This review defers novelty and positioning conclusions to follow-up manual literature verification. No citation-based weaknesses are assessed here.

## Score
**Final Score: 5/10**

**Rationale:** The paper presents a genuinely interesting conceptual direction — using multi-projected directional derivatives for joint communication efficiency and privacy in FL. The core idea is well-motivated and the empirical results under constrained budgets are promising. However, the score is depressed by several validity-impacting weaknesses:

- **Research value (+):** The joint compression-privacy mechanism is a meaningful contribution, and the gradient reconstruction error analysis (Lemma 1) provides useful insight. The empirical demonstration of 356× communication reduction is practically relevant.
- **Novelty (−):** The novelty position relative to the large body of gradient compression, sketched updates, and DP-FL literature cannot be fully assessed (retrieval unavailable). The claimed "first" introduction of projected directional derivatives in FL requires manual verification. The core technique (random projections for gradient compression) shares conceptual similarity with existing sketched update methods, and the paper's differentiation — dynamic per-client, per-round projections — may be incremental.
- **Validity/soundness (−):** The theoretical presentation has multiple gaps: undefined symbols in Theorem 2, notation errors in core definitions, and an overstated descent property claim. The privacy guarantees are presented without formal DP analysis, exceeding what the evidence supports.
- **Experimental rigor (−):** The absence of variance/confidence intervals across all experiments is a significant weakness. Without multi-seed reporting, the reliability of comparisons cannot be assessed.
- **Reproducibility (+):** The algorithm is clearly specified (Algorithm 2), and the communication budget framework is well-explained. The reliance on random seeds is transparent.

The paper falls in the "revision required" range. If the authors address the theoretical gaps (W1, W2, W3), substantially qualify the privacy claims (W4), and add statistical rigor (W5), the score could be raised to 6-7/10. However, the deferred novelty verification means the upper bound on contribution significance remains uncertain.