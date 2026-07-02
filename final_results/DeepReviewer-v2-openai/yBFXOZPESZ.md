## Summary
# Final Review Report

## Summary

This paper proposes Ano (and its variant Anolog), a new stochastic optimizer that decouples update direction and magnitude—using momentum sign for directional smoothing and instantaneous gradient magnitude for step-size scaling. The core idea is motivated by improving robustness under noisy and non-stationary optimization landscapes (particularly RL) while remaining competitive on standard benchmarks. The paper provides a theoretical convergence analysis (O(K^{-1/4}) rate under standard assumptions) and evaluates on CV (CIFAR-100), NLP (GLUE), and DRL (MuJoCo SAC, Atari PPO) benchmarks.

**Core contributions claimed:**
- C1: A direction-magnitude decoupled gradient-scaling mechanism with same memory cost as Adam.
- C2: Non-convex convergence rate analysis (O(K^{-1/4})).
- C3: Empirical validation showing gains in noisy/non-stationary settings.

**Overall assessment:** The paper addresses an important problem (optimizer robustness under noise) with a clean conceptual design. However, the manuscript has several critical issues that prevent acceptance in current form: (1) a fundamental mathematical discrepancy between Algorithm 1 and the core equation in Section 3 (g_k vs |g_k|), (2) theory-empirical mismatch where the convergence proof analyzes a different algorithm than what is evaluated, (3) a claim about modifying Yogi's variance update that is factually incorrect (the equation is identical to standard Yogi), (4) impossible hardware/software specifications (RTX 5090, CUDA 12.9, PyTorch 2.9.0) that undermine reproducibility, and (5) table errors including duplicate Adam entries and mislabeled schedules. Novelty verification is deferred (Retrieval-Disabled Mode active); external literature comparison needed.

**Recommendation:** Major revision required. The conceptual contribution is potentially valuable, but the manuscript requires substantial corrections to experimental reporting, mathematical consistency, and claim verification before it can be evaluated for publication.

## Strengths
1. **Clean conceptual design.** The core idea of decoupling direction and magnitude in optimizer updates (momentum sign for direction, instant gradient magnitude for scale) is intuitive, well-motivated, and addresses a genuine limitation of Adam-style momentum coupling. The design is simple enough to be practical while addressing a known failure mode.

2. **Honest experimental scope.** The paper explicitly acknowledges that Ano is designed for noisy/non-stationary regimes and does not claim superiority on standard CV/NLP benchmarks. The asymmetry in evaluation (RL as primary, CV/NLP as diagnostic checks) is a principled approach that avoids overclaiming.

3. **Strong RL empirical results.** On MuJoCo SAC and Atari PPO tasks, Ano consistently achieves higher returns and faster convergence than Adam, Lion, and other baselines, with 95% confidence intervals reported. The hyperparameter sensitivity analysis (Figure 3) suggests Ano is more robust to learning rate and beta choices than Adam, which is practically valuable.

4. **Comprehensive ablation study.** Table 6 systematically ablates design components (Yogi tweak, gradient norm, momentum norm, momentum direction, decoupled weight decay, β₁ scheduling), providing clear evidence for the contribution of each component.

5. **Good reproducibility effort.** The paper provides anonymous source code, pip packages for three frameworks (PyTorch, TensorFlow, JAX), and detailed hyperparameter search protocols. The use of fixed seeds and multi-seed evaluation (5-10 seeds) and CI95% reporting follows best practices.

6. **Anolog variant for hyperparameter-free β₁.** Removing the need to tune momentum coefficient via logarithmic scheduling is a practical contribution for users with limited tuning budgets.

## Weaknesses
### Critical Issues

**W1. Algorithm-Equation discrepancy in core update rule.** Algorithm 1 computes `x_{k+1} = x_k - (η_k/√(v̂_k+ε)) · g_k · sign(m_k)` while the text equation in Section 3 uses `|g_k| · sign(m_k)`. These are mathematically different: the elementwise product `g_k · sign(m_k)` can be negative when sign(m_k) and g_k disagree, potentially inverting the intended update direction. This is a fatal inconsistency — the paper cannot simultaneously claim clean direction-magnitude decoupling while the algorithm permits sign conflict to override the direction signal. **Severity: Critical. Location: Page 1 — Algorithm 1 (line 31) vs Section 3 equation (line 42).**

**W2. Impossible hardware/software specifications.** The reproducibility statement lists "RTX 5090 GPU", "CUDA 12.9", and "PyTorch 2.9.0" — none of which exist as of 2025. This raises serious questions about whether the experiments were actually conducted. Even as a placeholder error, it indicates a lack of quality control. **Severity: Critical. Location: Page 1 — Reproducibility Statement (line 267).**

**W3. Theory-empirical mismatch.** The convergence proof (Section 5.1) assumes β_{1,k} = 1 - 1/√k and η_k = η/k^{3/4}. The Ano algorithm in Section 3 uses fixed β₁ = 0.92 with no mention of time-varying scheduling. The theory therefore proves convergence for a different algorithm than the one being empirically evaluated. The claim that Ano has "non-convex convergence guarantees" is misleading. **Severity: Major. Location: Page 1 — Abstract (line 6) and Section 5.1 (lines 55-62).**

### Major Issues

**W4. False claim about Yogi extension.** Section 3 states "We extend Yogi by introducing a decay factor that explicitly controls variance memory." However, the provided equation v_k = β₂v_{k-1} - (1-β₂)·sign(v_{k-1} - g_k²)·g_k² is EXACTLY the standard Yogi update — no additional decay factor is present. The claimed extension does not exist. **Severity: Major. Location: Page 1 — Section 3 Second-Moment Term (lines 43-45).**

**W5. Duplicate/mislabeled Adam entries in GLUE table.** Table 3 contains two rows labeled "Adam" in both Default and Tuned sections with different values. One is likely AdamW or a different configuration, but the table does not distinguish them. This makes the baseline comparison uninterpretable. **Severity: Major. Location: Page 1 — Table 3 (lines 111-119).**

**W6. Convergence proof drops coordinate-wise adaptivity.** The descent inequality uses a global bound (G) in the denominator, but the actual algorithm applies per-coordinate normalization via √(v̂_{k,i}). The proof does not account for the very adaptive behavior that distinguishes Ano from non-adaptive methods. **Severity: Major. Location: Page 1 — Section 5.1 proof sketch (line 60).**

**W7. Anolog's schedule not covered by theory.** The variant Anolog uses β_{1,k} = 1 - 1/log(k+2), but the convergence proof uses β_{1,k} = 1 - 1/√k. The paper claims Anolog is "inspired by our convergence analysis" yet provides no theoretical justification for the logarithmic schedule. **Severity: Major. Location: Page 1 — Section 4 Extension (lines 48-51).**

**W8. RL tuning bias confound.** Hyperparameters are tuned on 100k-step HalfCheetah proxy. Since Ano is designed for larger steps, this short-horizon tuning may systematically favor Ano over baselines. The reported "+10%" improvement may partially reflect this tuning bias. **Severity: Major. Location: Page 1 — Section 6.3 (line 127).**

### Moderate Issues

**W9. Incomplete introduction narrative.** The introduction jumps from problem description to proposed solution without a dedicated paragraph surveying existing approaches and identifying the specific gap. The Related Work discussion of Grams is imprecise — both Ano and Grams mix sign and magnitude signals, but the paper does not explain why its specific factorization is superior. **Severity: Major. Location: Page 1 — Introduction (lines 7-13) and Related Work (lines 18-19).**

**W10. Unverifiable Nesterov claim.** Limitations mention "experiments with Nesterov-style acceleration... amplified instability" but no such experiments appear anywhere in the paper. **Severity: Verification. Location: Page 1 — Limitations (line 261).**

**W11. Ablation table labeling errors.** Table 6 mislabels schedules: the row "Ano √k" uses β=1-1/k (harmonic), while "Ano log k" uses β=1-1/√k (square-root). The variant name "Analog" appears in Tables 4-6 while the text uses "Anolog". **Severity: Minor. Location: Page 1 — Table 6 (lines 242-258).**

### Minor Issues

**W12. Missing justification for ResNet-34 on CIFAR-100.** Standard CIFAR ResNet variants are 32/44/56/110; ResNet-34 is unusual and uncommented. **Severity: Minor. Location: Page 1 — Section 6.1 (line 80).**

**W13. Conclusion introduces unsubstantiated future directions.** "MARL benchmark" and "variance estimators for supervised learning" appear for the first time in the conclusion without prior context. **Severity: Suggestion. Location: Page 1 — Conclusion (line 263).**

**W14. Missing 95% CI for noise robustness experiments.** Table 1 omits confidence intervals that the footnote promises are in Appendix E, making it impossible to assess statistical significance of the reported gaps. **Severity: Minor. Location: Page 1 — Section 5.2 (lines 64-71).**

## Score
**Final Score: 4/10**

**Rationale:**

The score is driven by the interaction between novelty, research value, and validity. The conceptual contribution of direction-magnitude decoupling is interesting and the RL results are promising. However, the paper currently has multiple critical and major flaws that prevent acceptance:

- **Critical defects (W1, W2)**: The algorithm-equation discrepancy and impossible hardware specifications are fundamental credibility issues that must be resolved before the paper can be taken seriously. W1 alone potentially invalidates the core algorithmic claim.
- **Major validity concerns (W3, W4, W6, W7)**: The theory does not actually analyze the Ano being evaluated; a key claim about modifying Yogi is false; the convergence proof drops the main algorithmic feature (coordinate-wise adaptivity). These issues mean the theoretical contributions as presented are not trustworthy.
- **Experimental reliability (W5, W8, W14)**: Table errors and tuning confounds reduce confidence in the empirical results.
- **Novelty**: Deferred to manual verification (Retrieval-Disabled Mode). The core idea (sign(m_k) for direction + |g_k| for magnitude) is a natural variant within the direction-magnitude decoupling space already explored by Grams and Lion. The paper does not adequately distinguish itself from these methods. External literature comparison is needed to determine whether the specific combination is genuinely novel.

**Score breakdown (primary dimensions):**
- Research value: 5/10 — The decoupling idea is valuable but the implementation and validation have too many issues.
- Novelty strength: Deferred (tentatively 4/10 based on manuscript-grounded comparison with cited related work).
- Validity/soundness: 3/10 — Critical inconsistencies between algorithm description, theoretical analysis, and empirical claims.
- Reproducibility: 2/10 — Impossible hardware/software specs, missing experiment details for Nesterov claim, duplicate table entries.

**Post-Revision Target: [6, 7]/10** — If all critical issues (W1, W2) are resolved, theory-algorithm mismatch (W3, W6, W7) is fixed, experimental tables are corrected, and novelty is verified against external literature, the paper could reach publishable quality.