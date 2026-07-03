The calibration search infrastructure appears unavailable. I will proceed with my analysis and assign a score based on careful comparison with the standards articulated in the ICLR guidelines.

Let me write the final consolidated review.

## Summary

This paper introduces FedMPDD, a federated learning algorithm that encodes each client's gradient as m scalar directional derivatives along random Rademacher vectors, reducing uplink communication from O(d) to O(m). The server reconstructs an unbiased gradient estimate by aggregating these scalar projections. The method provides formal reconstruction-error lower bounds against gradient inversion attacks (Lemmas 1 and 2) and proves an O(1/√K) convergence rate (Theorem 2) by leveraging the JL lemma. Experiments on MNIST and CIFAR-10 demonstrate communication savings and GIA resistance.

## Strengths

1. **Multi-projection mechanism provably overcomes the single-projection convergence bottleneck.** The paper identifies that single-projection FedPDD suffers from a √d scaling in the estimator norm (line 96), forcing η = O(1/(d√K)). By averaging m projections and applying the JL lemma (lines 108–112), FedMPDD bounds the estimator norm by (1+ε)‖g‖ with high probability using m = O(log(d)/ε²), decoupling the convergence rate from d. Theorem 2 establishes an O(1/√K) rate with a decomposition of error sources — a principled improvement over single-projection approaches.

2. **Formal reconstruction-error lower bounds for GIA defense.** Lemma 1 gives the exact expected relative gradient reconstruction error: 𝔼[‖ĝ−g‖²]/‖g‖² = (d−1)/m. Lemma 2 translates this into a lower bound on data reconstruction error that is independent of gradient magnitude, unlike LDP's noise which scales inversely with ‖g‖², leaving large gradients poorly protected (Remark 5, Appendix C). The empirical validation (Table 2) supports this: FedMPDD(m=600) achieves SSIM 0.14 while compression-only baselines show SSIM 0.74–0.93.

3. **Empirical demonstration of joint communication efficiency and GIA resistance.** Table 2 evaluates methods under identical conditions (CIFAR-10, CNN, 0.9 GB budget). Compression baselines (lp-proj, Top-k, SA-FedLora, QSGD) achieve communication savings but have high SSIM (0.74–0.93), indicating privacy leakage. FedMPDD(m=600) achieves 40.84% accuracy (highest among methods within budget) with SSIM 0.14 — a ~5–7× privacy improvement — while using less total communication (1.32 GB vs 1.84–2.30 GB) to reach 60% target accuracy. This joint evaluation supports the claimed dual benefit.

4. **Multi-round composition bound.** Remark 2 (line 148) provides the condition T×m < d under which unique gradient recovery remains impossible after multiple rounds, offering a quantifiable operational guideline beyond single-round analysis.

5. **Computational cost analysis with an efficiency condition.** Remark 1 acknowledges the O(dm) encoding cost and identifies a condition (m < hpT/(h+p)) under which Jacobian-vector products make the projected-forward approach strictly cheaper than computing the full gradient.

## Weaknesses

### Fatal
None.

### Major

1. **Privacy claims are overstated and the comparison with LDP is misleading.** The paper systematically presents its reconstruction-error bounds as a "privacy guarantee" comparable to differential privacy. Lemma 1 and Lemma 2 bound the error of a *specific attack strategy* (matching the projected gradient via gradient descent on dummy inputs). This is not a formal privacy framework: it does not bound information leakage or characterize indistinguishability of inputs. A stronger adversary with a different reconstruction strategy could potentially achieve much lower error. The claim that FedMPDD "eliminates the fluctuating nature of LDP" (line 31, Remark 3) compares incomparable frameworks — LDP provides information-theoretic (ε,δ) guarantees about indistinguishability of individual data points, while FedMPDD provides a lower bound on reconstruction error for one attack class. The paper would be much stronger if it honestly positioned its contribution as a *provable defense against GIAs* with a formal error floor, rather than as a "privacy guarantee" that invites comparison with DP. This is the paper's most significant weakness because it affects how readers interpret the core contribution.

### Minor

2. **Abstract contains a technical error: claims O(1/K) but proves O(1/√K).** The abstract (line 9) states that FedMPDD "converges at a rate of O(1/K)." Theorem 2 (line 114) proves O(1/√K), and the contribution list (line 32) correctly states O(1/√K). The correct rate for non-convex SGD is O(1/√K), not O(1/K). While this does not invalidate any result, it signals carelessness in a paper whose headline claim is technical.

3. **SSIM "Defendability" threshold is not stated.** Table 2 shows FedMPDD(m=2000) with SSIM=0.22 marked ✓ and FedSGD+Laplace(var=10) with SSIM=0.23 marked ✗. The threshold for binary classification is not specified, creating ambiguity about whether all methods are evaluated under the same standard.

4. **No variance or error bars reported.** Tables report single values (e.g., "77.37" test accuracy). FL results are typically noisy due to client sampling, data distribution differences, and random seeds. Without variance estimates, it is impossible to assess whether differences between methods are statistically meaningful.

5. **The distortion parameter ε is not instantiated for the experimental m choices.** Theorem 2's third convergence term is O(εG²/√K), where ε relates to m via the JL lemma (m = O(ln(d/δ)/ε²)). The paper does not report what ε values the experimental m choices (e.g., m=600 for d≈300k) correspond to, making it hard to assess the practical magnitude of the projection-induced convergence degradation.

6. **Multi-round composition bound (T×m < d) is stated but its practical consequences are not explored.** The bound is restrictive (T < 500 for the CIFAR-10 CNN setup with m=600). When T exceeds d/m, the "privacy" guarantee is undefined — the paper's response about "the natural evolution of gradients during training provides stronger practical protection" (Remark 2) is qualitative and unquantified. A graceful degradation analysis of how reconstruction error grows as T increases beyond d/m would be valuable.

7. **The GIA attack (Yu et al., 2025) is used as-is on projected gradients.** The paper does not describe whether the attack was adapted for projected (rather than full) gradients. An attack designed for full gradients may underperform on projected gradients simply because it does not exploit the projection structure, which could overstate the reported privacy protection.

### Trivial

8. **Notational error in the Introduction (line 27).** The expression $\hat{\mathbf{g}}_i(\mathbf{x}_k) = \mathbf{U}_{k,i} \mathbf{g}_i(\mathbf{x}_k) \mathbf{U}_{k,i}$ is dimensionally inconsistent (U ∈ ℝ^{d×m}). The correct expression appears later (line 102): $\frac{1}{m} U_{k,i} (U_{k,i}^\top \mathbf{g}_i(\mathbf{x}_k))$.

## Nice-to-Haves

- A graceful degradation analysis of reconstruction error when T exceeds d/m, rather than the current all-or-nothing bound.
- Wall-clock time comparisons alongside communication costs, since Remark 1 notes that the current implementation computes the full gradient before projecting.
- Clarification of whether the GIA attack was adapted for projected gradients and discussion of how this affects interpretation.

## Removed Points

These points were raised by the input reviews but removed after verification against the paper:

- **"Apples-to-oranges" comparison with FedSGD**: The harsh critic argued that "matching FedSGD's performance" cannot be verified because experiments compare under a fixed budget. The abstract's claim is about convergence rate (matching FedSGD's O(1/√K) rate), not accuracy under unconstrained communication. REMOVED as a misunderstanding of the paper's claim.
- **Structured/sketched updates bias claim**: The paper uses the qualifier "often" (line 48). REMOVED as nitpick.
- **Equation (2) ambiguity**: The equation is readable in context and the intent is clear from Algorithm 2. REMOVED as formatting nitpick.
- **Table 2 "*" and "not reached" confusion**: The caption explains "* indicates budget exceeded in the first iteration." REMOVED.
- **Computational cost of full gradient computation**: Remark 1 explicitly acknowledges this and discusses the JVP alternative. REMOVED because the paper already addresses it.
- **No discussion of SSIM limitations**: While SSIM is indeed a perceptual metric, it is the standard evaluation metric in the GIA literature the paper builds on. REMOVED as an overly broad critique of standard practice.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Correct the abstract to state O(1/√K) instead of O(1/K).
2. Recalibrate the privacy claims: present Lemmas 1 and 2 as a *provable defense against GIAs with a formal error floor* rather than as a "privacy guarantee" comparable to DP/LDP. Remove or substantially revise the claim that LDP has "fluctuating" protection when compared to FedMPDD.
3. State the SSIM threshold used for Defendability classification, or report SSIM as a continuous measure without binary labels.
4. Report variance (e.g., over 3–5 random seeds) for the main experimental results.
5. Instantiate ε for the experimental m choices and discuss how the third convergence term affects practical performance.
6. Clarify whether the GIA attack was adapted for projected gradients and discuss implications.

## Score and Decision

The paper proposes a genuinely novel and well-motivated method (multi-projected directional derivatives for FL). The theoretical analysis connecting the JL lemma to convergence and the reconstruction-error bounds are solid technical contributions. The experiments demonstrate real communication savings with measurable GIA resistance.

However, the paper **systematically overstates its privacy contribution**, presenting reconstruction-error bounds as a "privacy guarantee" comparable to differential privacy frameworks. This is the paper's central weakness: the technical content is meaningful when properly scoped (a provable defense against GIAs with formal error floors), but the current framing invites misleading comparisons with LDP that do not hold up. Additionally, the abstract contains a clear technical error (O(1/K) vs O(1/√K)), and several evaluation details (SSIM threshold, variance, ε values) are unspecified.

The contribution is real but narrower than advertised. A substantially revised version that honestly positions the privacy contribution would be a solid paper. In its current form, the gap between the claims and what is established is too large.

**Score: 5.0**

**Decision: Reject**

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>