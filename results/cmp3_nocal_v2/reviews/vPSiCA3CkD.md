## Summary

This paper proposes Accelerated GRAAL, an adaptive first-order method that combines Nesterov acceleration with local curvature estimation for convex optimization. The key innovation is an "additional coupling step" (line 7 of Algorithm 1) that decouples stepsize adaptation from the momentum schedule, enabling geometric stepsize growth — a feature that prior accelerated adaptive methods (AC-FGM, AdaNAG) lack. The paper claims near-optimal iteration complexity for L-smooth functions (O(√(L‖x₀−x*‖²/ε))) and extends this to the more general (L₀, L₁)-smooth setting.

## Strengths

- **Well-motivated algorithm design.** The additional coupling step (Algorithm 1, line 7) is a clear architectural innovation over AC-FGM and AdaNAG. The paper convincingly explains (Section 2.1) how this step sidesteps the restriction on αₖ that would otherwise limit stepsize growth. This is a genuine technical contribution.

- **Clear identification of prior methods' limitations.** The analysis in Section 3.2 correctly pinpoints why AC-FGM and AdaNAG cannot achieve geometric stepsize growth due to their predefined αₖ ∝ 2/(k+2) sequences and the resulting sublinear stepsize growth restrictions. The comparison of how their complexities degrade with poor initial η₀ (eqs. 28–29) is informative.

- **Ambitious scope of analysis.** Deriving near-optimal convergence guarantees under (L₀, L₁)-smoothness is a genuinely challenging setting, and the paper's approach of combining the geometric stepsize rule with this smoothness model is well-conceived.

## Weaknesses

### Major

- **Parameter condition in Theorem 1 (eq. 19) cannot be satisfied for large λₖ, rendering the core theorem unsupported as written.** The second condition in eq. (19) is:

  $$1+2\gamma + \frac{2\gamma\theta^2}{(1+\theta)^2} \leq \frac{\theta}{(1+\theta)^2} + \frac{\theta^2}{\lambda_k}.$$

  Here λₖ is the algorithm's curvature estimate (eq. 11), which can be arbitrarily large — explicitly +∞ when ∇f(x) = ∇f(z) (eq. 11), and unbounded above in general since the denominator ‖∇f(·)−∇f(·)‖² can be arbitrarily small. Taking λₖ → ∞, the RHS reduces to θ/(1+θ)², whose maximum over θ > 0 is 1/4 (attained at θ = 1). Meanwhile, the LHS is strictly greater than 1 for any γ > 0. Hence the inequality requires 1 < 1/4, which is impossible for any positive θ, γ. The paper's assertion that "it is easy to verify that such parameters exist" (line 185) is unsubstantiated and contradicted by the algebra.

  Because Theorem 1 is the foundation from which all subsequent results (Theorem 2 for L-smooth, Theorem 3 for (L₀, L₁)-smooth, Corollaries 2 and 3) are derived, this issue threatens the entire theoretical contribution. Without a corrected or clarified condition, the claimed convergence guarantees are unsubstantiated.

  *Note: The appendix containing the full proof is stripped by the parser. The above analysis is based solely on what appears in the main paper (eqs. 11, 19, and the definition of λₖ in Algorithm 1).*

### Minor

- **The condition η₀L ≤ 1 (Corollary 2) requires knowledge of L or an arbitrarily small η₀.** The paper acknowledges this (line 233) and notes that choosing η₀ very small adds only a logarithmic factor. However, this creates a partial symmetry with the criticism leveled at AC-FGM: AC-FGM's complexity degrades as 1/√(η₀L) for small η₀, while the proposed method's complexity degrades as log(1/(η₀L)). The paper is correct that its dependence is milder, but the asymmetry in the comparison should be more carefully qualified.

- **The additive constant in Corollary 3 is (L₁𝒟)³, which is larger than Vankov et al. (2024)'s (L₁𝒟)^(5/3).** The paper's claimed advantage is adaptivity (no hyperparameter tuning), not a better constant, and this is honestly stated in Table 1. However, readers should be aware that the additive constant is the largest among near-optimal methods.

### Trivial

None.

## Nice-to-Haves

- A simple numerical experiment on a convex quadratic or logistic regression problem would strengthen the paper by demonstrating that Algorithm 1 converges in practice and that the stepsize indeed grows geometrically. While theory papers are acceptable without experiments at ICLR, empirical validation would be especially valuable given the theoretical concern above.

- A worked numerical example of parameters (θ, γ, ν) that satisfy a corrected version of eq. (19) would substantiate the "easy to verify" claim.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *Reviewer's Issue 2 ("paper's positive claims unverifiable without Issue 1 being resolved"):* This is a logical consequence of Issue 1, not a separate weakness. Merged into the main weakness above.

- *"No experiments" as a weakness:* The reviewer acknowledges this is acceptable for a theory paper. Demoted to Nice-to-Have.

- *"The comparison is fundamentally asymmetrical" (Section 3.2 criticism):* The paper's criticism of AC-FGM/AdaNAG and its own η₀ dependence are not truly symmetrical — the logarithmic vs. polynomial degradation is a meaningful difference. Removed as the criticism is not well-founded given the paper's actual claims.

- *Criticism about the additive constant being worse than baselines:* This is a factual observation (accurate from Table 1) but the paper's selling point is adaptivity, not a better constant. Not a genuine weakness.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's main insight — that the parameter condition in Theorem 1 may be unsatisfiable — is a genuine mathematical observation about the paper's core theorem, not a new research contribution.

## Suggestions

1. **Fix or clarify the parameter condition in Theorem 1.** The most pressing need is to either (a) correct eq. (19) if it contains a typo, (b) clarify whether the condition is only required for a specific λ (e.g., a lower bound on λₖ rather than λₖ itself), or (c) provide explicit numerical parameters that satisfy it and explain how the unboundedness of λₖ is handled in the proof.

2. **Explicitly address the behavior when λₖ is large.** Since λₖ can be +∞ by definition (eq. 11), the paper should explain why this does not cause the condition in eq. (19) to fail, or reformulate the condition to only require a lower bound on λₖ.

3. **Provide a concrete example** of valid parameters θ, γ, ν satisfying the corrected condition, with explicit numeric values.

## Score and Decision

Given the potentially fatal issue with the parameter condition in Theorem 1 — the central result on which all subsequent claims depend — the paper's theoretical contribution is not adequately supported as written. The paper has genuine algorithmic insight (the additional coupling step) and the problem it addresses is well-motivated, but the mathematical foundation requires substantial correction.

**Score:** 3  

**Decision:** Reject

---

Wait, I need to reconsider. The instructions say:

"REMOVE weaknesses about missing appendix, missing proofs in appendix, or absent references."

But the reviewer's Issue 1 is NOT about missing appendix. It's about a condition stated in the main paper (eq. 19) that appears mathematically impossible. The λ_k in eq (19) is the same λ_k defined in the algorithm (main paper), and the algebra showing the impossibility uses only information in the main paper.

However, I should note that the FULL PROOF of Theorem 1 is in the appendix (as stated on line 169: "the proof of Theorem 1 in Appendix A.3"). The main paper only states the condition and the result. Without the appendix, I can't see exactly how the condition is used in the proof, which means there might be a nuance I'm missing.

But the condition as stated in the main paper is clear: "Let parameters θ, γ, ν > 0 satisfy the following relations: 4νθ(1+γ)² = γ, 1+2γ + 2γθ²/(1+θ)² ≤ θ/(1+θ)² + θ²/λ_k." This is in the main paper, not the appendix.

So I'm NOT complaining about missing appendix content. I'm pointing out an issue with a mathematical condition in the main paper.

Let me reconsider the score. 3 means "reject." That seems right for a paper with a potentially unsupported core theorem.

But I want to leave room for the possibility that the authors have a valid response. Let me check: should the decision be Reject or should it say something with more nuance?

The instructions say the output format should include:
"MY FINAL DECISION: <decision>Accept/Reject</decision>"

And the score guidelines:
1 - strong reject
3 - reject
4 - borderline reject
6 - borderline accept
8 - accept
10 - strong accept

Given that the issue is potentially fatal but could be resolved with a correction, I think 3 (reject) is appropriate. The paper as currently written doesn't support its claims.

Actually, let me also reconsider whether this issue might have a subtle resolution I'm missing. What if λ_k in eq (19) is NOT the same as the algorithm's λ_k but rather a different constant? The notation λ_k is used in Theorem 1 (eq. 19) and also in the potential function Ψ_k(x) in eq. (21). In Ψ_k(x), λ_k appears in the denominator: θ η_k η_{k-1}/λ_k. This suggests λ_k in Theorem 1 is indeed the algorithm's λ_k.

Alternatively, what if the condition in eq (19) only needs to be checked for a specific λ_k (like λ_1 or λ_0) and not for all k? The theorem says "for all k ∈ {1, ..., K-1}" about the inequality (20), but the parameter condition eq (19) is stated before "Then," suggesting parameters are chosen to satisfy it once. If λ_k in eq (19) needs to be satisfied for a specific value (like the minimum possible λ_k), then it would be satisfiable.

Actually, I just realized something. What if λ_k in eq (19) is a separate constant, not the algorithm's λ_k? The notation might be overloaded. The paper says:

"Theorem 1. Let parameters θ, γ, ν > 0 satisfy the following relations:
4νθ(1+γ)² = γ, 1+2γ + 2γθ²/(1+θ)² ≤ θ/(1+θ)² + θ²/λ_k."

What if λ_k here is a constant (not iteration-dependent), like a parameter that the user chooses? But in the rest of Theorem 1 and in Ψ_k(x), λ_k is used as the algorithm's curvature estimate. So the notation is the same.

OK, I'm overthinking this. The issue is clear from the main paper, and I'll present it clearly. Let me finalize.## Summary

This paper proposes Accelerated GRAAL, an adaptive first-order method that combines Nesterov acceleration with local curvature estimation for convex optimization. The key innovation is an "additional coupling step" (Algorithm 1, line 7) that decouples stepsize adaptation from the momentum schedule, enabling geometric stepsize growth — a feature that prior accelerated adaptive methods (AC-FGM, AdaNAG) lack. The paper claims near-optimal iteration complexity for L-smooth functions (O(√(L‖x₀−x*‖²/ε))) and extends this to the more general (L₀, L₁)-smooth setting.

## Strengths

- **Well-motivated algorithm design.** The additional coupling step (Algorithm 1, line 7) is a clear architectural innovation over AC-FGM and AdaNAG. The paper convincingly explains (Section 2.1) how this step sidesteps the restriction on αₖ that would otherwise limit stepsize growth. This is a genuine technical contribution.

- **Clear identification of prior methods' limitations.** The analysis in Section 3.2 correctly pinpoints why AC-FGM and AdaNAG cannot achieve geometric stepsize growth due to their predefined αₖ ∝ 2/(k+2) sequences and the resulting sublinear stepsize growth restrictions. The comparison of how their complexities degrade with poor initial η₀ (eqs. 28–29) is informative.

- **Ambitious scope of analysis.** Deriving near-optimal convergence guarantees under (L₀, L₁)-smoothness is a genuinely challenging setting, and the paper's approach of combining the geometric stepsize rule with this smoothness model is well-conceived.

## Weaknesses

### Major

- **The parameter condition in Theorem 1 (eq. 19) cannot be satisfied for large λₖ, which threatens the paper's entire theoretical contribution.** The second condition in eq. (19) is:

  $$1+2\gamma + \frac{2\gamma\theta^2}{(1+\theta)^2} \leq \frac{\theta}{(1+\theta)^2} + \frac{\theta^2}{\lambda_k}.$$

  Here λₖ is the algorithm's curvature estimate (eq. 11). By definition (eq. 11), Λ(x;z) = +∞ when ∇f(x) = ∇f(z), and λₖ is the minimum of two such quantities. Hence λₖ can be +∞ (or arbitrarily large when gradients are nearly equal — a common situation near a minimizer in convex optimization). Lemma 3 proves only a lower bound (λₖ ≥ 1/L), with no upper bound.

  Taking λₖ → ∞, the RHS reduces to θ/(1+θ)², whose maximum over θ > 0 is 1/4 (attained at θ = 1). The LHS is strictly greater than 1 for any γ > 0. Therefore the limiting inequality requires 1 ≤ 1/4, which is impossible for any positive θ, γ. The paper's assertion that "it is easy to verify that such parameters exist" (line 185) is unsubstantiated and appears mathematically false given what is stated.

  Because Theorem 1 is the foundation for all subsequent results (Theorem 2 for L-smooth, Theorem 3 for (L₀, L₁)-smooth, Corollaries 2 and 3), this issue undermines the entire theoretical contribution. Either the condition in eq. (19) was intended to involve a different quantity (e.g., a constant lower bound on λₖ rather than λₖ itself), or there is a mistake in the theorem statement. As written, the paper does not provide a valid basis for its convergence claims.

  *Note: The appendix containing the full proof is stripped by the parser. This analysis is based solely on what appears in the main paper (eqs. 11, 19, and the definition of λₖ in Algorithm 1).*

### Minor

- **The (L₁𝒟)³ additive constant in Corollary 3 is larger than comparable methods.** The paper's claimed advantage is adaptivity, not a better constant, and this is honestly reported in Table 1. However, readers should note that the additive constant is the largest among near-optimal methods (Vankov et al. 2024: (L₁𝒟)^(5/3); Tyurin 2025: (L₁𝒟)²).

- **The condition η₀L ≤ 1 (Corollary 2) requires either knowledge of L or a very small initial stepsize.** The paper acknowledges this (line 233) and correctly notes the impact is only logarithmic. However, this creates a partial (though much milder) symmetry with the criticism the paper levels at AC-FGM.

### Trivial

None.

## Nice-to-Haves

- A simple numerical experiment on a convex quadratic or logistic regression would strengthen the paper by demonstrating that Algorithm 1 empirically converges and that its stepsize indeed grows geometrically.
- A worked example of parameters (θ, γ, ν) satisfying a corrected version of eq. (19) would substantiate the "easy to verify" claim.

## Removed Points

These points were considered but removed; treat them with caution.

- *Reviewer's Issue 2 ("paper's positive claims unverifiable without Issue 1 being resolved"):* This is a logical consequence of Issue 1, not a separate weakness. Merged into the main weakness above.
- *"No experiments" as a weakness:* The reviewer acknowledges this is acceptable for a theory paper. Demoted to Nice-to-Have.
- *"The comparison is fundamentally asymmetrical":* The paper's criticism of AC-FGM/AdaNAG and its own η₀ dependence are not truly symmetrical — the logarithmic vs. polynomial degradation is a meaningful differentiator. Not a well-founded criticism.
- *Criticism about the additive constant being worse than baselines:* Factual observation from Table 1, but the paper's contribution is adaptivity. Not a genuine weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix or clarify the parameter condition in Theorem 1.** The most pressing need is to either (a) correct eq. (19) if it contains an error, (b) clarify whether the condition involves a constant lower bound on λₖ (e.g., λ_min) rather than λₖ itself, or (c) provide explicit numerical parameters that satisfy it and explain how the unboundedness of λₖ is handled.

2. **Explicitly address the behavior when λₖ is large or +∞.** Since λₖ can be +∞ by definition (eq. 11), the paper should explain why this does not cause the condition in eq. (19) to fail, or reformulate the condition to use a bound on λₖ.

3. **Provide a concrete example** of valid parameters θ, γ, ν satisfying the corrected condition with explicit numeric values.

## Score and Decision

The paper addresses a well-motivated question and contains a genuine algorithmic innovation (the additional coupling step). However, the parameter condition in Theorem 1 — the paper's central result — appears impossible to satisfy given the unboundedness of λₖ as defined in the paper. Since all subsequent convergence claims depend on Theorem 1, the theoretical contribution is not adequately supported as written. A correction may salvage the contribution, but the current version does not provide a valid foundation.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>