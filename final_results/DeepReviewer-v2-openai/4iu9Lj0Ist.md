## Summary
# Final Review Report

## Summary

This paper establishes a theoretical foundation for certified machine unlearning within the ℓ2-regularized continual learning framework, where models are trained on sequentially arriving tasks without storing past data. The key conceptual contribution is a decomposition of the post-unlearning excess risk into two components: the excess risk inherent to continual learning and the additional loss caused by unlearning. The paper shows that these two terms are coupled through the regularization hyperparameter λ, creating a fundamental tradeoff absent in static unlearning or standard continual learning.

The authors adapt two families of certified unlearning methods to this setting: (1) a natural-forgetting (gradient-based) algorithm that leverages the forgetting effect of continual learning to add calibrated Gaussian noise, achieving zero storage overhead but potentially larger unlearning loss; (2) a Hessian-based algorithm that uses second-order Taylor approximations for more accurate unlearning, at the cost of O(td²) storage. Theoretical bounds are provided for both approaches, including an excess-risk bound (Theorem 3.1) that extends prior linear-model results to convex losses. Experiments on MNIST with a linear model validate the predicted tradeoffs and demonstrate the influence of unlearning request ordering.

The paper addresses an important and underexplored problem—privacy-preserving unlearning in continual learning—and provides rigorous theoretical analysis under convexity assumptions. However, several concerns affect the current version: potential index errors in the main theorem bound (Eq. 8), a theory-experiment gap due to violated strong-convexity assumptions, an anomalous result where the unlearned model outperforms retraining (Table 1), limited empirical validation (single dataset, linear model only), and the absence of explicit limitations discussion. The novelty claims cannot be independently verified in this run (Retrieval-Disabled Mode). Major revisions addressing these issues are needed before the paper meets its full potential.

## Strengths
**1. Important and timely problem formulation.** The paper tackles a real and growing challenge: performing certified data deletion in continual learning environments where past data is inaccessible. This is increasingly relevant as deployed models (e.g., conversational AI, recommendation systems) operate under continual learning and face regulatory deletion requirements. The problem framing is clear and motivates the work effectively.

**2. Clean decomposition of post-unlearning excess risk.** The decomposition into unlearning loss (Eq. 6) and continual learning excess risk (Eq. 7) is a conceptually strong contribution. It reveals that the two objectives are coupled through the regularization parameter λ—a finding that does not arise in static unlearning or standard continual learning alone. This decomposition provides a principled foundation for analyzing any unlearning algorithm in a continual learning context.

**3. Rigorous theoretical analysis under stated assumptions.** The paper provides complete theoretical bounds (Theorem 3.1, 4.1, Propositions 5.1-5.2, Corollary 5.3) under clear assumptions (L-Lipschitz, μ-strong convexity, M-smoothness). The analysis of how the natural forgetting effect (ρ factor) reduces unlearning loss for early tasks, and the derivation of a second-order bound for the Hessian-based method, demonstrate technical depth.

**4. Two complementary algorithm families with clear tradeoff characterization.** The paper analyzes both a low-storage (gradient-based, zero storage) and a high-accuracy (Hessian-based, O(td²) storage) approach, and explicitly evaluates their tradeoffs. The combined forgetting-enhanced Hessian algorithm that reduces storage to the interval between consecutive unlearning times is a practical design insight.

**5. Honest discussion of the balancing challenge.** The paper explicitly identifies that preventing forgetting (which helps continual learning) can increase unlearning loss—a nuanced point that distinguishes this work from treating the two problems independently.

## Weaknesses
### W1. Potential index errors in Theorem 3.1 (Eq. 8) — MAJOR

The excess-risk bound in Eq. (8) contains two terms where the same index appears in both positions of a difference, making them trivially zero. Specifically:

- The first double sum contains `∑_{i=1}^k ∑_{j=2, j≠i}^k ρ^{τ_j - τ_j} ||w_{τ_j}^* - w_{τ_j}^*||`. Here τ_j - τ_j = 0, so ρ⁰ = 1, and ||w_{τ_j}^* - w_{τ_j}^*|| = 0, making this term vanish.
- Similarly, `L ρ^{τ_k} ∑_{i=2}^k ||w_{τ_i}^* - w_{τ_i}^*||` is zero because the norm is taken between identical vectors.

These appear to be copy-editing errors from index renaming. Additionally, the term `(τ_k - 2)` in the denominator expression could become negative when τ_k = 1 or 2, which would produce an invalid bound.

**Impact:** As printed, the bound is not meaningful. The authors must carefully re-derive and correct the indices, verify the domain of τ_k, and provide a sanity check (e.g., k=1 case collapsing to single-task bound).

**Required fix:** Replace all self-difference norms with meaningful cross-term differences (e.g., ||w_{τ_i}^* - w_{τ_j}^*|| for i≠j with appropriate distance-based exponents). Replace (τ_k - 2) with max(0, τ_k - 2) or clarify that τ_k ≥ 3 in the setting.

### W2. Theory-experiment assumption gap — MAJOR

Assumption 2.1 requires μ-strong convexity, which is used critically in the proofs (via ρ = λ/(μ+λ) and denominators involving μ). However, the experiments (Section 6) use a linear softmax model with cross-entropy loss, which is **not** μ-strongly convex. The paper states it "relaxes" this assumption "to show more general results under a non-strongly convex setting," but provides no theoretical justification that the bounds remain valid or degrade gracefully when μ → 0.

**Impact:** The experimental results cannot be interpreted as validating the theoretical bounds. The observed trends may be consistent with the theory, but the quantitative values of the bounds diverge (denominators approach zero as μ → 0). This undermines the claim of "validating theoretical findings with experiments on the MNIST dataset."

**Required fix (P0):** Either (a) run experiments under the assumed conditions (e.g., ℓ2-regularized logistic regression with sufficient regularization to ensure strong convexity) and directly compare empirical excess risk with the theoretical bound value, or (b) provide a formal analysis of how the bounds change when μ → 0 (e.g., showing they reduce to a different known bound).

### W3. Table 1 anomaly: unlearned model outperforms retraining — MAJOR

At λ = 30, the Hessian-based unlearning achieves 71.59% accuracy while the perfect retraining model achieves only 71.05%. This contradicts the premise that unlearning approximates retraining — if the unlearned model is strictly better, the approximation guarantee is violated, or the retraining baseline is suboptimal.

**Potential explanations:** (a) Statistical noise from single-seed evaluation, (b) retraining at λ=30 is poorly tuned (accuracy drops sharply from 75.81% at λ=20 to 71.05% at λ=30, suggesting optimization issues), or (c) the Hessian correction uses information not available during retraining.

**Required fix (P0):** Report multi-seed means and standard deviations. Investigate why retraining accuracy drops at λ=30. If the anomaly persists, provide a theoretical justification or acknowledge it as a limitation of the retraining comparison.

### W4. Insufficient empirical validation for a theory paper — MAJOR

The experiments use only:
- One dataset (MNIST) — a simple benchmark
- One model class (linear softmax) — despite claiming extension to nonlinear convex models
- No variance or confidence intervals reported
- No direct comparison between the theoretical bound value and observed risk
- Sequence-order experiments relegated to Appendix E without summary in the main text

For a paper whose primary contribution is theoretical, the experiments should serve as a sanity check of the bounds, not merely qualitative trend plots. Without measuring the bound itself, the reader cannot verify that the theory predicts the observed behavior.

**Required fix (P0):** Add at least one more dataset, one nonlinear convex model, standard deviations over ≥3 seeds, and a plot comparing the bound (8) with observed risk. Move the key sequence-order result to the main text.

### W5. Missing limitations discussion in conclusion — MINOR

The conclusion does not discuss any limitations. For a theoretical paper with strong assumptions, this omission weakens scientific credibility. Key missing limitations include the strong convexity requirement, Hessian storage cost, single-dataset validation, and unobserved quantities needed for noise calibration.

**Required fix:** Add a limitations paragraph as suggested in the annotation for Page 8 - Conclusion.

### W6. Unexamined practical feasibility of Hessian-based approach — MINOR

The paper notes O(td²) storage for Hessian-based unlearning but does not discuss what this means for practical models. For d ~ 10⁷ (modern neural networks), storing full Hessian matrices is completely infeasible. The paper should explicitly position its approach as targeting linear/Kernel models with moderate d, and discuss approximations (diagonal, KFAC) as future work.

### W7. Novelty claims require external verification — DEFERRED

The paper claims "the first theoretical foundation connecting continual learning and machine unlearning." Due to Retrieval-Disabled Mode in this run, external literature verification was not possible. The authors should ensure their novelty claims are scoped precisely (e.g., "first theoretical foundation for certified unlearning within ℓ2-regularized continual learning under convexity assumptions") and include a thorough comparison with prior work, especially Liu et al. (2022), Chatterjee et al. (2024), Cha et al. (2024), and Huang et al. (2025) which are cited as related but heuristic.

### W8. Introduction narrative improvement needed — MINOR

The introduction opens with a dense citation block in the first paragraph (7+ citations in 3 sentences), which weakens the motivational hook. The contribution list could more clearly distinguish between the analytical contribution (excess-risk decomposition) and the adaptation contributions (gradient/Hessian algorithms). Suggested rewrites are provided in the annotations for Page 1 - Introduction.

## Score
**Final Score: 5.5/10**

**Rationale:** The paper tackles an important and timely problem, offers a clean conceptual decomposition (excess risk = CL excess risk + unlearning loss), and provides rigorous theoretical bounds under stated convexity assumptions. However, the current version is affected by several validity concerns that prevent a higher score. Potential index errors in the core Theorem 3.1 (Eq. 8) raise correctness questions. The experiments violate the strong-convexity assumption required by the theory, creating a gap that prevents empirical validation of the bounds. An anomalous result in Table 1 (unlearned model outperforming retraining) undermines confidence in the experimental setup. Empirical validation is limited to a single dataset and linear model, insufficient for a theory paper claiming general results. Novelty claims could not be independently verified in this run.

The paper has a solid foundation and the core ideas are promising. With careful correction of the mathematical errors, expanded experiments that respect the theoretical assumptions, explicit handling of the retraining anomaly, and addition of limitations discussion, the paper could become a strong contribution. The score reflects potential combined with required major revisions.

---

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Paper: Certified Unlearning in Continual Learning]
    |
    ├── [Problem Formulation] (Section 2)
    |   ├── Assumption 2.1: μ-strong convexity, L-Lipschitz, M-smooth
    |   ├── Eq (1): ℓ2-regularized CL objective
    |   └── Eqs (5)-(7): Post-unlearning excess risk decomposition
    |       → KEY CONCEPT: unlearning loss + CL excess risk (coupled via λ)
    |
    ├── [Theoretical Foundation] (Section 3)
    |   └── Theorem 3.1: Excess-risk bound for ℓ2-CL [Eq. 8]
    |       → W1: Potential index errors (self-difference terms vanish)
    |       → W2: Requires μ>0 but experiments violate this
    |
    ├── [Algorithm 1: Natural Forgetting] (Section 4)
    |   ├── Leverages forgetting effect for zero-cost unlearning
    |   ├── Theorem 4.1: (ε,δ)-certified guarantee [Eqs. 9-10]
    |   └── Storage: 0    |   Accuracy: lower for recent tasks
    |
    ├── [Algorithm 2: Hessian-based] (Section 5)
    |   ├── Second-order approximation for accurate unlearning
    |   ├── Prop 5.1/5.2: First/second-order bounds [Eqs. 14-15]
    |   ├── Storage: O(td²) | Accuracy: higher overall
    |   └── W6: Impractical for large d
    |
    └── [Experiments] (Section 6)
        ├── MNIST, linear softmax, 30 non-i.i.d. tasks
        ├── Table 1: Hessian-based accuracy > retraining at λ=30 (W3)
        ├── No variance, single dataset, linear only (W4)
        └── W2: Assumption violation → theory-experiment gap
```

### ASCII Diagram — Revision Strategy Roadmap

```text
Priority 0 (Must fix — publication-critical)
├── [W1: Index errors in Eq. (8)]
│   ├── Fix: Replace self-difference indices with cross-term indices
│   ├── Fix: Clarify domain of τ_k or replace (τ_k - 2) with max(0, τ_k-2)
│   ├── Fix: Verify k=1 collapse to single-task bound
│   └── Expected impact: Theorem correctness restored
│
├── [W3: Table 1 anomaly — unlearning > retraining]
│   ├── Fix: Add multi-seed variance; investigate retraining drop at λ=30
│   ├── If anomaly persists: Provide theoretical explanation
│   └── Expected impact: Experimental credibility restored
│
├── [W2: Theory-experiment assumption gap]
│   ├── Option A: Run ℓ2-regularized logistic regression (satisfies μ>0)
│   ├── Option B: Provide formal analysis of μ→0 limit
│   └── Expected impact: Empirical validation becomes meaningful
│
└── [W4: Insufficient experiments]
    ├── Fix: Add ≥1 more dataset, nonlinear convex model, ≥3 seeds
    ├── Fix: Compare theoretical bound to observed excess risk
    └── Expected impact: Claims become empirically supported

Priority 1 (Should fix — quality improvement)
├── [W5: Missing limitations] → Add limitations paragraph
├── [W6: Practical feasibility] → Scope claims to moderate-d models
└── [W8: Intro narrative] → Reduce citation density, improve hook

Priority 2 (Nice to have)
└── [W7: Novelty claims] → Scope precisely after literature review
```

### ASCII Diagram — Related-Work Taxonomy Tree (Layered)

```text
Certified Unlearning in Sequential/Continual Settings (Root)
├── Branch A: Certified Unlearning (static, full-data access)
│   ├── Leaf A1: Hessian-based methods [Sekhari+2021, Suriyakumar+2022]
│   ├── Leaf A2: Hessian-based extensions [Qiao+2024, Basaran+2025]
│   ├── Leaf A3: Gradient-based methods [Neel+2021, Chien+2024a]
│   ├── Leaf A4: Langevin/noisy-SGD methods [Chien+2024b, Koloskova+2025]
│   └── Limitation: Assume full dataset access; static learning setting
│
├── Branch B: Continual Learning Theory
│   ├── Leaf B1: Forgetting analysis in linear models [Lin+2023]
│   ├── Leaf B2: Regularization-based CL (EWC) [Kirkpatrick+2017]
│   └── Limitation: Focus on retention, not deletion
│
├── Branch C: Continual Learning + Unlearning (heuristic)
│   ├── Leaf C1: System-level frameworks [Liu+2022, Chatterjee+2024]
│   ├── Leaf C2: Instance-wise unlearning [Cha+2024]
│   └── Limitation: No theoretical guarantees provided
│
└── Branch D: This Paper (Novel Position)
    └── D1: First theoretical framework combining certified unlearning
         and ℓ2-regularized continual learning
         Value: Formal decomposition of post-unlearning excess risk;
         analysis of λ-coupled tradeoff; two algorithm families
         with provable guarantees.
         *Novelty verification deferred (Retrieval-Disabled Mode)*
```

**Post-Revision Target:** [6.5, 7.5]/10 — achievable if W1 (index errors), W3 (Table 1 anomaly), and W2 (assumption gap) are resolved with concrete corrections and expanded experiments.