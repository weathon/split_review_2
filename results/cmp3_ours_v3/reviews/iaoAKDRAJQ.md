## Summary

This theory paper studies the relationship between adaptive optimizers (Adam, AdaGrad, Shampoo) and Normalized Steepest Descent (NSD) methods (SignGD, Muon) through the lens of smoothness assumptions. It extends adaptive smoothness analysis to the nonconvex setting for general well-structured preconditioner sets (beyond the diagonal case), proves a novel matrix inequality (Lemma 3.3) to handle noncommutativity, shows that adaptive smoothness enables an accelerated O(T⁻²) rate for adaptive optimizers with Nesterov momentum (contrasted with an Ω(T⁻¹) lower bound under standard ℓ∞ smoothness), and introduces an adaptive variance framework that yields dimension-free NSD rates unattainable under standard variance for the studied algorithm.

## Strengths

1. **Unified nonconvex analysis beyond diagonal preconditioners (Section 3, Lemma 3.3).** Prior nonconvex analysis of adaptive optimizers was limited to diagonal preconditioners. This paper extends the analysis to any well-structured preconditioner set — covering AdaGrad-Norm, full-matrix AdaGrad, and one-sided Shampoo — and identifies adaptive smoothness Λ_ℋ(f) as the governing quantity. Lemma 3.3 provides a bound on Σ||V_t^{-1}g_t||²_H for arbitrary well-structured ℋ with a clean characterization of the extra log d factor that noncommutativity introduces. This lemma is a genuine technical contribution with reuse potential beyond this paper.

2. **Clean acceleration separation result (Section 4.2, Theorem 4.3).** The accelerated Õ(Λ_ℋ(f)D²/T²) rate for adaptive optimizers with Nesterov momentum, contrasted with the Ω(T⁻¹) lower bound under ℓ∞ smoothness (Guzmán & Nemirovski, 2015), directly answers Q2 and establishes a concrete optimization benefit of the stronger adaptive smoothness assumption. This is the paper's sharpest finding.

3. **Principled adaptive variance framework with dimension-free NSD rate (Section 4.3, Theorems 4.5–4.7).** The adaptive variance definition parallels adaptive smoothness in an internally consistent way. Theorem 4.5 achieves a dimension-free rate for NSD under adaptive variance using *standard* (not adaptive) smoothness, strictly improving over concurrent work by Kovalev & Borodich (2025). The lower bound (Theorem 4.7) confirms that for NSD with momentum, dimension dependence is unavoidable under standard variance.

4. **Well-motivated narrative.** The two questions (Q1, Q2) in Section 1 directly frame the paper's contributions, and Section 2's walkthrough of Adam and SignGD under ℓ∞ geometry is an effective pedagogical device that clearly reveals the distinction between standard and adaptive smoothness.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **The "optimal Õ(T^{-1/4}) rate" claim (line 40) is not supported by the main text.** The contribution bullet states that the nonconvex convergence rate "matches optimal Õ(T^{-1/4}) rate," referencing appendix theorems (D.2, D.7, D.8). However, the main text (Theorems 3.1–3.2) only presents deterministic results with O(1/√T) rates. While the stochastic results exist in the original submission's appendix, the main text does not explain the relationship between the deterministic O(1/√T) bounds shown and the claimed optimal stochastic rate, making the claim hard to evaluate from the main text alone.

2. **The answer to Q1 is underspecified.** The paper asks "Do adaptive methods and their corresponding non-Euclidean descent exploit the non-Euclidean geometry in the same way?" and answers that they rely on different smoothness assumptions. This is accurate but is largely a statement about analysis frameworks rather than algorithm behavior. Given how prominently Q1 is motivated, a more substantive discussion of what this distinction implies algorithmically would strengthen the paper.

3. **The lower bound's scope could be more precisely qualified.** Theorem 4.7 explicitly studies Algorithm 3 (NSD with momentum), and the text correctly states that "the d-dependent rate in Theorem 4.6 is unavoidable" in that context. However, the abstract's phrasing ("cannot be achieved under standard gradient variance for certain non-Euclidean geometry") and the term "fundamental gap" (line 339) could be read by some readers as an information-theoretic claim about all possible algorithms rather than about the specific NSD-with-momentum algorithm studied. A brief qualification would preempt this misinterpretation.

### Trivial

1. The convergence bounds in Theorems 3.1 and 3.2 are presented with substantial detail (terms like ξ, S_T, ‖S_T‖_op) that makes the final rate hard to extract. The high-level interpretation on line 182 is helpful but appears after the theorem statements. A simplified rate in each theorem statement (as done in Theorem 4.3) would improve readability.

2. The conclusion (Section 5) is extremely brief at 3 lines after formatting. A paragraph discussing limitations or open questions would be valuable for a theory paper.

## Nice-to-Haves

- A discussion of whether adaptive smoothness Λ_ℋ(f) is ever significantly smaller than its worst-case upper bound d·L — even a simple theoretical example — would help readers gauge the practical significance of the acceleration result. This is not a weakness of the theory as presented, but would increase the paper's impact.
- A brief intuitive explanation (in the main text) of why adaptive variance is always no smaller than standard variance (currently deferred to Proposition B.11 in the appendix) would improve accessibility.

## Removed Points

- **"Adaptive smoothness practical prevalence is unexamined" (from Harsh Critic):** Asking a pure theory paper to empirically measure adaptive smoothness on neural network loss landscapes or to characterize function classes where Λ_ℋ(f) is small goes beyond the paper's stated scope. The paper already establishes the theoretical relationship L ≤ Λ ≤ d·L and cites prior work. This is a future-work direction, not a weakness of the theory presented.
- **"The derivation of Equation (4) lacks citation":** This is a standard duality fact; a missing citation for a known result is not a substantive weakness.
- **"No discussion of practical guidance for practitioners":** The paper is a theory paper; speculative practical guidance is a nice-to-have, not a requirement.
- **"Missing citation of Arjevani et al. (2023) lower bounds":** Rule: do not mention missing references as we cannot verify their existence externally.
- **Various section-by-section presentation nitpicks:** These are stylistic preferences, not substantive weaknesses, and are subsumed by the Trivial weaknesses listed above.

## Novel Insights

None beyond the paper's own contributions. The review broadly confirms the paper's self-stated contributions: the nonconvex extension of adaptive smoothness to general well-structured preconditioners (enabled by Lemma 3.3), the acceleration separation result, and the adaptive variance framework yielding dimension-free rates.

## Suggestions

1. Clarify the relationship between the deterministic O(1/√T) bounds in Theorems 3.1–3.2 and the claimed "optimal Õ(T^{-1/4})" stochastic rate in the contribution list, either by adding a brief explanation in the main text or including a clean statement of the stochastic result.
2. Provide a more substantive discussion of what the smoothness distinction implies algorithmically (responding more fully to Q1).
3. Add 1–2 sentences qualifying that the lower bound (Theorem 4.7) applies to NSD with momentum, not necessarily to all possible algorithms.
4. Include simplified rate expressions in the theorem statements of Theorems 3.1 and 3.2 for readability.

## Calibration Anchors

The following anchor papers from the calibration corpus were used:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `GQ1Tc3vHbt.md` (L0,L1-smooth optimization) | 6.50 | R1 | Similar pure-theory paper with genuine contributions and presentation issues; accepted |
| `ww3CLRhF1v.md` (SDEs for adaptive methods) | 7.00 | R1 | Theory+experiments paper; our paper lacks experiments but has cleaner theoretical separation |
| `YwJkv2YqBq.md` (Nesterov in benignly nonconvex) | 6.75 | R1 | Very similar genre (theory, convergence rates, Nesterov acceleration); accepted |
| `mEBSeSk49H.md` (Adam vs SGDM under nonuniform smoothness) | 4.25 | R1 | Had incomplete proofs; our paper is more rigorous |
| `DIAaRdL2Ra.md` (Adafactor convergence) | 5.00 | R1 | Had restrictive assumptions and impractical bounds; our paper is cleaner |
| `JslyktsKMY.md` (Reevaluating theory methods) | 5.75 | R1 | Empirical evaluation of theory assumptions; different genre |
| `5nldnvvHfw.md` (Adaptive decay for Adam) | 2.50 | R1 | Significantly weaker theory; rejected |
| `1NYhrZynvC.md` (Linear-rate gradient descent) | 2.50 | R1 | Similar theory genre but less rigorous; rejected |

**Bracket:** R1 bracketing placed the paper between 5.5 and 7.5. Narrowing against the 6.50 (accepted), 6.75 (accepted), and 7.00 (accepted) anchors confirms the paper is in the solid-accept range — it is more rigorous than the 4.25–5.00 anchors but lacks the empirical validation of the 7.00 anchor.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>