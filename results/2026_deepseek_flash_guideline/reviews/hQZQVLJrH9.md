## Summary

This paper establishes a first-order duality between activation steering and influence functions in neural networks. It shows that, to first order, any steering vector can be represented as a signed influence measure over training data and vice versa. It introduces the Influence-Aligned Steering (IAS) vector, a γ diagnostic that characterizes when steering can succeed, a spectral optimality principle for choosing steering directions, and generalization bounds for low-rank steering. The core contribution is theoretical unification of two previously separate interpretability toolkits.

## Strengths

1. **Genuinely novel theoretical unification.** The paper provides a formal, constructive equivalence (Theorem 4.2) between activation steering and influence functions — two lines of work that have developed independently. The primal-dual formulation (Section 3) and the IAS construction Δh\* = J† J Δθ are mathematically well-posed and bring clarity to the relationship.

2. **Clean geometric framework via the γ diagnostic.** The paper introduces γ(x) = cos ∠_min(𝒮_θ, 𝒮_h) as a single scalar that bounds the residual when steering cannot fully match influence (Theorem 5.1: error ≤ √(1−γ²)) and also provides a No-Free-Lunch impossibility result when γ is small (Theorem 6.2). The experimental validation (Section 7.3, Fig. 2) confirms γ increases monotonically with depth from 0.64 to 0.94 on GPT-2 Medium, supporting the theory.

3. **Generalization bound for low-rank steering.** Theorem 6.1 derives a Rademacher-complexity bound showing that the excess risk from low-rank steering decays as √(2k/dn), providing formal justification for why steering interventions do not harm generalization in wide networks.

4. **Computational tractability of core quantities.** All core quantities (IAS, γ, λ\*) reduce to Jacobian-vector products and a rank-d pseudoinverse, making them feasible for practical use.

## Weaknesses

### Major

1. **Theorem 5.3 (Spectral Optimality) is not clearly justified as stated.** The theorem claims that under an ℓ₂ budget ‖s‖ ≤ B, the steering vector maximizing "expected first-order logit change" is the top eigenvector of Σ (a matrix of influence correlations). For a specific test input x, the direction that maximizes first-order logit change under an ℓ₂ budget is simply ∇_h f_θ(x)/‖∇_h f_θ(x)‖ *—not the top eigenvector of Σ*. If the theorem refers to an expectation over the training distribution, that relationship to Σ needs to be derived, and the formula "B √(λ_max(Σ)) ‖∇_h f_θ(x)‖" mixes training-set and test-set quantities without justification. The experiment (Section 7.4) tests only whether the spectral radius of the true-label direction is statistically significant against random-label directions; it does not compare the spectral direction's steering effect against any baseline steering method, so it cannot support the optimality claim. This is one of the paper's four stated contributions and the theorem statement needs substantial clarification.

2. **The ρ_s data-provenance workflow is entirely unsupported.** The abstract lists as contribution (i) "a constructive algorithm for mapping undesired behaviors back to causal training examples," and Sections 4.1 and 4's "Implication" describe this as a practical payoff. Yet there is *no experiment* showing that top-weighted examples from ρ_s are causally relevant — no retrieval precision test, no ablation study, not even a qualitative example tracing a steering vector to training data. The paper says "see Section 7" but Section 7 contains no such experiment. This is a significant gap between a headline claim and what is demonstrated.

3. **Slope of 1.50 in Fig. 1 is unexplained.** The central first-order equivalence experiment (Section 7.2) reports a cosine of 0.978 (direction is well-predicted) but a slope of 1.50 (the actual logit shift is 50% larger than predicted). The paper calls this "consistent with the expected linear regime," but a well-calibrated first-order approximation should have a slope near 1. A slope of 1.50 indicates either (a) the predicted quantity is not what the paper claims it is, or (b) second-order effects are large and systematic. Since this is the foundational empirical claim, the discrepancy needs explanation — not just a reference to the "linear regime."

4. **Experiments are thin for the scope of claims.** The paper makes four substantive contributions but validates them with only three small experiments on GPT-2 Medium (~350M params) and one on ResNet-50. There are no experiments on larger models, no end-to-end validation of the proposed workflow, and no experiment using the γ diagnostic to actually decide between steering and weight-space editing (a stated practical use). The detoxification comparison (Table 1) shows IAS underperforms CAA on both metrics, with no error bars reported.

### Minor

1. **Eq. 2 contains a mathematical inconsistency.** The dual derivation states Δh\* = J_{h→y}ᵀ J_{θ→y} Δθ, which is missing the (J_{h→y} J_{h→y}ᵀ)† factor that should appear from substituting λ\* back into Δh = −J_{h→y}ᵀ λ\*. Theorem 5.2 correctly states Δh\* = J_{h→y}† J_{θ→y} Δθ. This is likely a typographical error (the correct formula is given elsewhere), but in the central equation of a theory paper this inconsistency is confusing and should be fixed.

2. **The ρ_s measure is asserted to exist but not explicitly constructed.** Theorem 4.2 states "there exists a signed measure ρ_s" over the training set and Corollary 1 references "ρ_s constructed in Eq. 4," but Eq. 4 only asserts existence — it does not give a formula or algorithm for computing ρ_s. The reader cannot determine how to actually compute this quantity from a steering vector.

3. **Theorem 6.1's connection between activation-space steering and weight-space modification is unclear.** The theorem describes "the model obtained by adding a rank-k IAS correction at layer ℓ" as f_θ + αUVᵀ. IAS is an activation-space intervention (a steering vector), not a weight-space modification. How a steering vector gets converted into a rank-k weight matrix update is not explained.

4. **Theorem 6.2 (No-Free-Lunch) uses ambiguous phrasing.** "For every activation perturbation Δh and the corresponding (best-possible) parameter perturbation Δθ" does not specify how Δθ "corresponds" to Δh or what "best-possible" means. The relationship between the two perturbations is undefined.

5. **Abstract over-states the scope of the duality.** The abstract claims "any steering vector can be represented as an influence weighting over training data and vice versa" without qualification, while the body (Section 4) shows this holds only up to residuals bounded by √(1−γ²) and subject to the spanning condition.

### Trivial
- Table 1 reports no variance or confidence intervals for any method, making it impossible to assess whether the small differences between methods are meaningful.

## Nice-to-Haves
- Validating the γ diagnostic experimentally by showing steering fails when γ is small (and weight-space editing succeeds).
- Adding an experiment tracing a specific steering vector back to training examples via ρ_s (qualitative example or retrieval precision).
- Experiments on larger models (e.g., 7B+) to test scalability of the approach.
- A discussion of the computational cost of H⁻¹ for the influence-function components of the workflow when applied at scale.

## Removed Points

These points from the inputs were removed (with justification):

- **"Mathematical error in the core dual derivation"** → Demoted to Minor. The typo in Eq. 2 is real, but Theorem 5.2 states the correct formula, so the reader *can* tell which formula is intended. A single inconsistent equation in an otherwise correct body of theory is not fatal.
- **"IAS underperforms CAA in detoxification"** → Removed. The paper never claims IAS is SOTA; it is a theoretically principled steering vector. An asymmetric weakness that hurts the author's method (not the baseline) should not be held against the paper per the rules.
- **"Feasibility assumption restrictiveness"** → Removed. The paper explicitly discusses when the assumption fails (γ small → no-free-lunch regime, Theorem 6.2), so the concern is addressed.
- **"Computational cost of H⁻¹ at billion-parameter scale"** → Moved to Nice-to-Haves. The paper acknowledges using damped Gauss-Newton surrogates; the cost is inherent to influence functions and not specific to this paper's contribution.
- **"Missing related works"** → Removed per instruction: cannot raise without external sources.
- **Generality of strength "principled spectral direction replacing ad-hoc steering vectors"** → The Strength Finder overstated this. The spectral direction as a concept is interesting, but Theorem 5.3's confusion means this strength must be significantly downweighted.
- **Strengths about the problem being "important"** → Removed as generic.
- **"Reproducibility nitpicks"** → Removed per instruction.

## Novel Insights

The harsh critic's diagnosis of Theorem 5.3's incoherence is the most genuinely novel insight: the theorem claims the top eigenvector of Σ maximizes first-order logit change under an ℓ₂ budget, but for a specific test input x the optimal direction is simply ∇_h f_θ(x)/‖∇_h f_θ(x)‖. The critic correctly identifies that the theorem either means something different from what it literally states or is mathematically wrong, and that the experimental validation sidesteps this entirely by testing only against random directions rather than comparing to any steering baseline. This observation cuts to a central claimed contribution and is not present in the paper itself.

## Suggestions

1. **Fix Theorem 5.3** — State explicitly what objective is being maximized and over what distribution; derive the connection to Σ rigorously; correct or explain the formula that mixes training-set and test-set quantities. If the theorem cannot be fixed, remove the spectral-optimality claim.
2. **Explain the slope of 1.50 in Fig. 1** — Provide a reason for the systematic bias (e.g., damping λ, second-order effects, or a mis-specified axis). If the axes are different quantities, clarify the protocol.
3. **Add an experiment validating ρ_s** — Even a single qualitative example tracing a steering vector back to training examples would significantly strengthen the paper.
4. **Fix the typo in Eq. 2** to read Δh\* = J_{h→y}† J_{θ→y} Δθ (as in Theorem 5.2).
5. **Either validate the steer-vs-edit decision rule** via the γ diagnostic, or scope it back as a theoretical suggestion.
6. **Add variance estimates to Table 1.**

## Score and Decision

**Calibration anchors (across all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|-----------|
| `/home/.../9wjGUN65tY.md` (Conceptors) | 5.00 | R1 | Most directly comparable: theory+experiments for steering, thin experiments. Current paper has stronger theory but more issues. |
| `/home/.../2XBPdPIcFK.md` (ActAdd) | 5.00 | R1 | Empirical SOTA on steering; stronger exp., narrower scope. Current paper less experimentally thorough. |
| `/home/.../wozhdnRCtw.md` (Instruction-Following) | 7.00 | R1 | Solid empirical paper with comprehensive experiments. Current paper not at this empirical level. |
| `/home/.../NYf2XIXUi3.md` (TLXML) | 4.50 | R2 | Influence functions for meta-learning; novel theory, weak experiments. Current paper has more theorems but also more issues. |
| `/home/.../g1kSMVqaXg.md` (Dynamic Influence Tracker) | 5.00 | R2 | Influence functions paper with solid theory and experiments. Comparable but cleaner. |
| `/home/.../dwademPdV1.md` (Unfairness via Concept Influence) | 5.33 | R2 | Influence functions applied to fairness, rejected. Similar: novel application but experimental gaps. |
| `/home/.../KjBG4JNOc2.md` (Training Robustness via Influence) | 6.20 | R2 | Accepted influence-functions paper with strong empirical validation. Current paper's experiments not at this level. |

**Round 1 bracket:** 4.5–5.5.

**Final score determination:** The paper is clearly above the 3.0-level (incremental/fundamentally flawed) and below the 6.0+ level (solid empirical validation). It is comparable to the 5.0-range anchors, with a stronger but less cleanly-executed theoretical contribution. The core steer-influence duality is genuinely novel, but the confused Theorem 5.3, unexplained slope 1.50, and completely unvalidated ρ_s workflow constitute significant gaps between claims and evidence. Score 5.0 — borderline reject.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>