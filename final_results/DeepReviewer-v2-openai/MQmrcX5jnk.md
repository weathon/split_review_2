## Summary
# Final Review Report

## Summary

This paper introduces *Constrained Mass Transport* (CMT), a variational framework for sampling from high-dimensional multimodal unnormalized probability densities, with a focus on molecular Boltzmann generators. The key idea is to decompose the difficult reverse-KL minimization into a sequence of constrained optimization subproblems, each using two complementary constraints: (1) a trust-region bound on the KL divergence between successive intermediate densities, ensuring distributional overlap, and (2) a bound on the entropy decay rate, preventing premature mode collapse. The authors show analytically that these constraints yield geometric, tempered, and geometric-tempered annealing paths, and instantiate the framework using normalizing flows with an importance-weighted forward KL objective.

The method is evaluated on four molecular systems of increasing dimensionality (alanine dipeptide d=60, tetrapeptide d=120, hexapeptide d=180, and the newly introduced ELIL tetrapeptide d=219). CMT consistently outperforms state-of-the-art variational baselines (FAB, TA-BG) across EUBO, effective sample size, and Ramachandran TV distance, achieving up to 2.5x higher ESS on the largest system. An ablation study confirms that both constraints are necessary for the best performance.

**Overall assessment:** The paper presents a well-motivated, theoretically grounded framework with convincing empirical results. The main concerns are (a) a potential exponent inconsistency in the Lagrangian derivation that needs clarification, (b) fairness of baseline comparisons (forward KL uses MD samples, TA-BG had numerical failures on ELIL), and (c) limited discussion of practical limitations beyond the training cost. The novelty position relative to closely related work (Blessing et al. 2025, entropy-constrained RL) could be sharper. The paper represents a solid contribution to variational sampling for molecular systems.

## Strengths
1. **Well-motivated framework**: The paper clearly identifies two specific failure modes in existing variational sampling methods — mode collapse from reverse KL minimization and mass teleportation from geometric annealing — and designs constraints that directly address each one. The theoretical connection between the constrained optimization and the resulting annealing paths (Theorem 2.4) provides a solid foundation.

2. **Clean analytical solutions**: The derivation of closed-form optimal densities for each constraint type (Propositions 2.1–2.3) and the dual-function formulation (Eq. 6, 11) are mathematically elegant. The fact that the Lagrangian dual optimization is a low-dimensional convex problem that can reuse already-computed samples is a practical strength.

3. **Strong empirical results**: CMT consistently outperforms strong baselines (FAB, TA-BG) across all four molecular systems on all three metrics (EUBO, ESS, Ram TV). The performance gap grows with system dimensionality, which is promising for scalability. The >2.5x ESS improvement on the hardest system (ELIL tetrapeptide) is practically meaningful.

4. **Inclusive ablation study**: The ablation systematically tests all four constraint variants (none, trust-region only, entropy only, both), showing that both constraints are needed. The diagnostic plots (entropy curves, inter-step ESS) provide mechanistic insight into why each constraint matters.

5. **New challenging benchmark**: The ELIL tetrapeptide (d=219) fills a gap in the existing Boltzmann generator evaluation landscape, providing a larger and chemically more complex test case than previously available. Making the MD data publicly available (Zenodo) and the code open-source (GitHub) supports reproducibility.

6. **Reproducibility commitment**: The code release, public MD data, and detailed experimental setup description (with cross-references to appendix) are commendable and mitigate reproducibility concerns.

## Weaknesses
### (W1) Critical: Lagrangian exponent inconsistency (page 1, Section 2 — Propositions 2.1–2.3)
**Severity: Major | Fixability: Easily fixable**

The Lagrangian formulation in Eq. (3) for the trust-region constraint (2) yields the Euler-Lagrange solution q_{i+1} ∝ p̃^{1/(1+λ)} * q_i^{λ/(1+λ)}, where q_i appears with exponent λ/(1+λ). However, Proposition 2.1 states q_{i+1} ∝ q_i^{1/(1+λ)} * p̃^{1/(1+λ)} — both with the same exponent 1/(1+λ). These are not mathematically equivalent unless λ is reparameterized (e.g., λ' = 1/λ), which is not stated. 

**Impact:** If the exponents used in the actual algorithm differ from the theoretically derived ones, the connection between the Lagrangian multipliers and the annealing path parameters (α, β in Theorem 2.4) may be incorrect. This could affect the actual path that CMT follows and the correctness of the schedule tuning.

**Action:** The authors should provide a complete step-by-step derivation in the appendix and clarify the exact mapping between λ, η and the exponents. If the published formula is correct, the Lagrangian must be written with a different coefficient (e.g., L = D_KL(q||p) + λ^{-1} D_KL(q||q_i)). A numerical verification on a simple 1D case would resolve the discrepancy.

---

### (W2) Major: Baseline comparison fairness concerns (page 1, Section 5 — Table 1)
**Severity: Major | Fixability: Partially fixable**

Three issues affect the interpretation of the results:

(a) **Forward KL uses MD samples**: The forward KL baseline is trained on MD samples rather than energy evaluations, making it an apples-to-oranges comparison. Including it in the same table with the other methods (which use energy evaluations only) is potentially misleading, even with the caveat in the caption.

(b) **TA-BG on ELIL**: Only 2 of 4 seeds were successful for TA-BG on the largest system, yet Table 1 reports mean±std over those 2 runs. This selective reporting may inflate the perceived advantage of CMT. The failed runs should be reported (e.g., as NaN) and discussed.

(c) **Uneven computational budget**: Target evaluations alone do not capture the full computational cost. The number of intermediate steps I (or T-tilde), the sample size N per step, and the neural network architecture details should be reported for all methods to confirm fairness.

**Action:** Report wall-clock time on uniform hardware, include all seeds for all methods (successful or not), and move forward KL to a separate table with a clear indication that it uses a different training signal.

---

### (W3) Major: Entropy-only constraint ignores q_i entirely (page 1, Section 2 — Proposition 2.2)
**Severity: Major | Fixability: Already acknowledged, but under-discussed**

Proposition 2.2 reveals that the entropy-constrained optimal density q_{i+1}(x, η) ∝ p̃(x)^{1/(1+η)} has no dependence on the current density q_i. This means:
- Each entropy-constrained step jumps directly to a tempered target, regardless of the current distribution.
- This can cause the very overlap failure the method aims to prevent (as the authors note for the initial step).
- The claim that the trust-region constraint "fixes" this is empirically supported (Figure 2-3) but lacks theoretical analysis.

**Action:** Provide a bound or argument showing that adding the KL constraint (Eq. 9) re-introduces q_i dependence in a controlled way. A theoretical guarantee that the combined constraints always produce better overlap than either alone would strengthen the paper.

---

### (W4) Major: Novelty/comparison claims require external verification (deferred)
**Severity: Major | Fixability: Informational only**

This audit was conducted in Retrieval-Disabled Mode (external paper search unavailable). The following novelty claims should be verified against the literature in the authors' revision:

(a) "first explicit link between trust-region optimization and geometric annealing paths" (attributed to Blessing et al. 2025) — the paper should clearly state how CMT extends this.
(b) "To the best of our knowledge... largest system studied to date" for ELIL tetrapeptide.
(c) The entropy-constrained optimization "has not yet been extended to sampling problems" and the connection to annealing paths "has not previously been established."

**Action:** Authors should provide explicit comparison with Blessing et al. 2025, including a discussion of what conceptual elements are shared vs. novel in CMT. Claims about "first" and "largest" should be verified against recent preprint servers.

---

### (W5) Moderate: Importance-weighted forward KL variance (page 1, Section 3 — Eq. 15)
**Severity: Major | Fixability: Easily addable**

The practical algorithm uses importance weights w(x) = q_{i+1}(x)/q_i(x) in the forward KL objective (Eq. 15). The paper claims the trust-region constraint "controls the variance of the importance weights, keeping it approximately constant, independent of d." However:
- No theoretical variance bound is provided.
- The claim of dimension-independence is strong and requires empirical validation.
- No empirical diagnostic (e.g., effective sample size of the importance weights) is shown in the main text.

**Action:** Provide a variance bound (even a loose one) in terms of ε_tr. Add an empirical plot of importance weight variance or ESS across training steps for at least the two largest systems.

---

### (W6) Moderate: Limitations discussion too narrow (page 1, Section 6 — Conclusion)
**Severity: Minor | Fixability: Easily fixable**

The conclusion mentions only "large number of gradient updates" as a limitation. Other practical limitations that deserve mention: hyperparameter sensitivity to ε_tr and ε_ent, use of fixed steps rather than adaptive stopping, normalizing flow expressivity constraints, and potential scalability challenges to systems beyond d=219.

**Action:** Expand the limitations paragraph to cover these points and provide concrete mitigation strategies (e.g., heuristic for selecting constraint bounds, path to adaptive stopping).

## Score
**Final Score: 7/10**

**Rationale:** The paper presents a well-motivated, theoretically grounded framework with convincing empirical results spanning multiple molecular systems. The dual-constraint idea is clean and the empirical gains (especially on larger systems) are practically meaningful. However, the score is constrained by the following factors:

- **Mathematical rigor (weight: high):** The Lagrangian exponent inconsistency (W1) is a non-trivial concern that needs resolution before the theoretical claims can be fully trusted. This is fixable but currently unresolved.
- **Empirical validity (weight: high):** The baseline comparison is somewhat weakened by the forward KL using MD samples and TA-BG having only 2/4 successful runs on ELIL (W2). The results are still positive but the magnitude of the claimed advantage may be somewhat inflated.
- **Novelty (weight: high):** The paper builds on known ideas (trust-region from RL, geometric annealing) in a novel combination. The entropy-difference constraint is a genuine innovation. However, the exact novelty boundaries relative to Blessing et al. 2025 are not sharply drawn. External verification is needed (W4).
- **Presentation quality (weight: medium):** The paper is well-written overall but the method section could benefit from more intuition before formalism. The limitations discussion is too brief.

The paper is above the acceptance threshold for a strong venue after addressing W1, W2, and W6. The core ideas are solid and the empirical evidence, even with noted caveats, supports the main claims.

**Post-Revision Target:** [8, 9]/10 — achievable if the exponent discrepancy is resolved, baseline comparisons are made fully fair, and limitations are expanded.