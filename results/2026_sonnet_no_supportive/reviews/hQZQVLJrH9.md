Now I have a complete picture of the paper. Let me draft the review.Based on the calibration search, let me read one anchor paper for comparison.**Round 1 Bracket:** Based on the calibration anchors, papers with theoretical frameworks for activation steering that have limited or mixed empirical support score around 3–5.5. Papers with genuine conceptual novelty but incomplete experiments cluster at 4–5. The paper under review is closer to this range than to the 6+ zone (strong interpretability papers like "Sparse Feature Circuits" or "Capturing Temporal Dependence of Data Influence," which have solid experiments and sound proofs).

**Round 2 Narrowing:** The most comparable papers are:
- *Effectively Steer LLM via Building Confident Directions* (avg 5.5, rejected) — also a theoretical steering framework, stronger experimental section
- *From Steering Vectors to Conceptors* (avg 5.0, rejected) — theoretical + steering, similar empirical depth
- *Functional Gradients for ICL* (avg 3.57, rejected) — theoretical unification paper with modest empirical support

The paper under review sits between these: more conceptually novel than the 3.57-band papers (it makes a genuine new connection), but hampered by a flawed Corollary 1 proof, negative empirical results in its main comparison, and a missing provenance experiment. I settle on **4.0**.

---

## Summary
The paper establishes a first-order equivalence between activation steering and influence functions, showing both reduce to linear effects in logit space via shared Jacobian structure. From this geometric duality, the authors derive the Influence-Aligned Steering (IAS) vector, a feasibility diagnostic γ (principal-angle cosine), generalization bounds under low-rank steering, and a spectral recipe for optimal steering directions. Experiments on GPT-2 Medium and ResNet-50 provide partial validation.

## Strengths
- **Clean primal-dual geometric setup (Section 3).** The observation that the parameter–logit Jacobian J_{θ→y} and activation–logit Jacobian J_{h→y} form a primal-dual pair in convex-analysis sense, sharing the same linear logit-space structure (Eqs. 1–2), is a natural and well-formulated contribution that genuinely unifies two previously disconnected tools.
- **Layer-depth ablation (Fig. 2).** The finding that γ increases monotonically from 0.64 (layer 0) to 0.94 (layer 11) on GPT-2 Medium is concrete, reproducible, and motivates a practical layer-selection heuristic ("pick smallest layer with γ ≥ 0.7").
- **Practical γ diagnostic (Section 4.2).** The principal-angle cosine as a cheap pre-check before committing to steering — requiring only two small SVDs — is a genuinely useful contribution, providing a principled stopping criterion instead of empirical trial-and-error.

## Weaknesses

### Fatal
None.

### Major
- **Slope 1.50 in Figure 1 undermines the primary quantitative validation.** Section 7.2 reports a predicted-vs-actual logit shift with cosine 0.978 but slope 1.50, and calls this "consistent with the expected linear regime." A first-order approximation requires slope ≈ 1.0; a 50% systematic underestimation of actual shifts is not. The paper provides no explanation for this discrepancy and no ablation showing whether the slope converges to 1.0 at smaller magnitudes α. Since this is the central empirical test of the paper's core equivalence claim, its failure is significant.

- **IAS underperforms CAA in the only task-level comparison (Table 1).** CAA achieves toxicity 0.0150 and perplexity 13291, while IAS achieves 0.0164 and 13701 — on both metrics, the proposed theoretically-optimal method loses to a simple empirical heuristic. The paper neither acknowledges nor explains this gap. For a method framed as the minimum-norm, influence-aligned direction, this unexplained shortfall undermines the practical motivation.

- **Corollary 1 proof is logically invalid.** The proof (Section 4.1) argues: "If another measure ν achieved the same shift with smaller ℓ₁ norm, one could scale ρ_s down and still match the shift, contradicting the definition of α as the steering magnitude." This is circular: scaling ρ_s changes both the steering vector and its magnitude; it does not involve the same (s, α) pair. A different measure ν with smaller ℓ₁ norm reproducing the same shift is not precluded by fixing α. The ℓ₁-minimality claim requires LP duality or a proper sparsity argument using affine independence, neither of which is provided.

- **Core practical claim (provenance tracing) is never empirically demonstrated.** The Introduction, Section 4, and Abstract all promise that ρ_s "points straight to the most causal training documents" and can "debug bias or privacy leaks." The three experiments test linear approximation quality (Fig. 1), layer-depth γ trends (Fig. 2), and spectral significance vs. random baselines (Fig. 3), but no experiment shows that a steering-derived ρ_s actually recovers interpretable or actionable training examples. The central practical payoff is entirely unsupported empirically.

### Minor
- **Misleading "causal" language throughout Section 4.** The paper states ρ_s "points straight to the most causal training documents" and can "debug bias or privacy leaks." First-order influence functions measure gradient alignment, not counterfactual causation. The paper itself cites Basu et al. (2021) showing influence functions in deep learning are often fragile. "Attributive" or "gradient-correlated" would be more accurate.

- **Theorem 6.2 (No-Free-Lunch) is classical subspace geometry.** The inequality ‖J_{h→y} Δh‖ / ‖J_{θ→y} Δθ‖ ≤ γ is the definition of the cosine of the smallest principal angle — a standard result in numerical linear algebra, and in fact the same Björck & Golub (1973) paper already cited in Theorem 5.1. Presenting this as a novel named theorem inflates its contribution.

- **Compute claim in Introduction is overstated.** Point 4 states "all quantities reduce to two backward passes per input," but Theorem 5.3's spectral direction Σ requires computing (H+λI)⁻¹ ∇_θ ℓ(z,θ) for every training point in mini-batches — the Hessian inverse step is the dominant cost in influence function methods and is not free. The claim should be qualified.

### Trivial
None.

## Nice-to-Haves
- Slope-vs-α ablation curve for Figure 1: showing whether slope converges to 1.0 at smaller magnitudes would clarify whether the 50% error is a regime issue or structural.
- Empirical validation of the feasibility assumption: what fraction of inputs and layers satisfy Im(J_{θ→y}) ⊆ Im(J_{h→y}), and how does IAS behave when this is violated?
- A provenance experiment: given a known empirical steering direction (e.g., the detoxification vector from CAA), rank training examples by ρ_s and show that top-ranked examples are interpretably related to the behavior. This is the most impactful missing experiment.

## Removed Points
*These points are flagged for removal; treat them with caution.*

- **Feasibility assumption inadequately acknowledged:** The critic argued this assumption is "minimized." The paper explicitly lists it as Assumption (i) in Section 2 and provides the residual bound (Eq. 3) when it fails. This is a reasonable treatment for a theory paper. Removed as a standalone weakness.
- **ResNet-50 experiment is too weak:** The critic argues comparing spectral direction vs. random directions is trivially expected to succeed. However, this provides a sanity check on the spectral construction. Demoted to nice-to-have rather than a major weakness.
- **Abstract omits feasibility conditions:** Removed. The abstract says "to first order" and standard theory-paper convention does not require all assumptions in the abstract.
- **Theorem 6.1 (Rademacher) is a direct application of Pinto et al. (2024):** The paper explicitly acknowledges this in the sketch ("Combine Thm. 2 of Pinto et al. (2024) with..."). Applying a known bound to the IAS setting is a legitimate contribution; removed.

## Novel Insights
None beyond the paper's own contributions. The core novelty — that activation steering and influence functions share a first-order Jacobian structure enabling constructive equivalence — is the paper's own claim. The reviewers do not surface independent observations beyond verifying (and partially refuting) this claim.

## Suggestions
1. **Fix or retract Corollary 1.** The ℓ₁-minimality proof needs LP duality or a proper sparsity argument. If this cannot be proved rigorously, soften the claim.
2. **Explain or ablate the slope discrepancy in Fig. 1.** Add a slope-vs-α curve or restrict experiments to the regime where slope ≈ 1, making the empirical validation actually support the first-order theory.
3. **Acknowledge and explain the CAA vs. IAS gap in Table 1.** Even a theoretical discussion of why first-order logit-shift matching may not optimize toxicity reduction would substantially improve intellectual honesty.
4. **Add a provenance experiment.** Take an empirically found steering direction, compute ρ_s, and inspect whether top-ranked training examples are interpretably related to the targeted behavior.
5. **Replace "causal" with "attributive" or "gradient-correlated"** throughout Section 4 to avoid overclaiming.

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| z1yI8uoVU3 | 3.0 | R1 | Empirical steering evaluation, limited novelty — weaker theoretical content than this paper |
| OLtD2vDF5X | 4.88 | R1 | Practical influence function with methodological contribution, stronger experiments |
| ZPkNrs6aNO | 5.5 | R2 | Theoretical steering framework, better-supported empirical section |
| 9wjGUN65tY | 5.0 | R2 | Theory + steering, similar experimental depth, rejected |
| 2XBPdPIcFK | 5.0 | R2 | CAA method paper, purely empirical, accepted range split |
| uqLQjtSdFN | 3.57 | R2 | Theoretical unification of LLM mechanisms, incomplete experiments |
| I4e82CIDxv | 8.0 | R1 | Sparse Feature Circuits — much stronger empirics, sound methodology, accepted |
| uHLgDEgiS5 | 8.0 | R1 | Temporal data influence — rigorous theory + strong experiments, accepted |

**Round 1 bracket:** 3.5 – 5.5

**Round 2 narrowing:** Papers most similar in content and scope (ZPkNrs6aNO at 5.5, 9wjGUN65tY at 5.0) sit around 5.0 and were rejected. The paper under review has more conceptual novelty (genuine cross-domain duality) but is comparably penalized by: an invalid Corollary 1 proof, primary empirical validation that contradicts the theory (slope 1.50), task comparison where IAS loses, and missing provenance experiment. These four issues together pull it below the 5.0 anchors. Final score: **4.0**.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>