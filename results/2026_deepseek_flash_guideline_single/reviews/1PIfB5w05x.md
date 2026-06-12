Now let me write the final review.

## Summary

This paper studies sparse signal support recovery when observations come from two sources of differing quality (low-noise and high-noise measurements). It establishes sufficient sample-size conditions for information-theoretic recovery in both agnostic (noise variances unknown) and informed (variances known) settings, introducing the "Price of Quality" γ — the number of low-quality samples that replace one high-quality sample in the sufficient condition. It also extends the LASSO phase transition (Wainwright 2009) to the heterogeneous-noise agnostic setting, showing the algorithmic threshold depends only on the average noise level, revealing a sharp contrast between information-theoretic and computational recovery.

## Strengths

1. **Clean conceptual contribution — the Price of Quality (γ).** The idea of quantifying the trade-off between high- and low-quality samples via a single number in a linear sufficient condition (γ = α₁/α₂) is elegantly simple and interpretable. The contrast between the agnostic setting (γ uniformly bounded, γ ≤ 2) and the informed setting (γ can blow up to infinity) yields a practical takeaway: provenance information enabling per-sample loss rescaling dramatically improves the effective value of high-quality data.

2. **Computational vs. information-theoretic gap is rigorously exposed, not just noted.** The LASSO result (Theorem 3) rigorously shows the algorithmic threshold depends only on the average noise level — so high- and low-quality samples contribute equally to computational recovery — while the information-theoretic conditions give them different weights. This contrast, backed by concrete theorems, is the paper's most valuable finding.

3. **Technically non-trivial extension of Wainwright (2009).** The LASSO analysis for heterogeneous noise requires handling a diagonal Σ that is not a scalar multiple of the identity, which breaks the standard Wishart argument. The QR decomposition + Haar measure approach in the proof of Theorem 3 is a genuine technical contribution beyond merely restating a known result.

4. **Honest handling of limitations.** Remark 3.2 explicitly acknowledges that the agnostic sufficient condition is not sharp, explains why (cubic equation relaxation), and notes that estimator (8) may not be the best approach. Remark 4.2 explains in concrete technical detail why extending to the informed LASSO setting is nontrivial. This level of transparency is uncommon and valuable.

5. **Generalizations explicitly scoped.** Remark 3.4 extends both theorems to arbitrary non-singular noise structures and signed support recovery, showing the results are not brittle to the two-source assumption.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **The headline γ ≤ 2 bound is a property of a sufficient condition whose tightness is uncalibrated.** The paper is transparent throughout — the caveat "under our sufficient condition" is consistently present in the abstract (line 9), the introduction (line 81), the low-SNR discussion (line 191), and the conclusion (line 336). Remark 3.2 explicitly acknowledges the condition is not sharp and identifies the cubic equation relaxation as the source of looseness. However, the paper's most prominent finding derives from a Chernoff-bound relaxation whose gap relative to the true threshold is entirely unquantified. The paper provides no bound on how loose this relaxation might be (factor of 1.1 vs. 10) and no calibration against a known baseline (e.g., the homogeneous-noise case σ₁² = σ₂² where the exact threshold is known). A reader cannot assess whether γ ≤ 2 is a near-sharp property of the problem or a loose artifact of the analysis. This does not invalidate the contribution — the theoretical framework, informed-setting results, and LASSO analysis stand independently — but it means the headline claim should be treated with appropriate caution.

2. **The agnostic information-theoretic estimator (8) is computationally intractable while the agnostic setting is motivated by practical scenarios.** The estimator in Theorem 1 minimizes over the space of binary s-sparse vectors — a combinatorial optimization problem that is NP-hard in general. The paper's framing contrasts the agnostic vs. informed settings, but the real practical contrast is between the computationally tractable LASSO (Theorem 3) and the intractable MLE. This is standard practice in the information-theoretic literature (e.g., Gamarnik & Zadik 2022 use the same estimator), and the paper cleanly separates sampling complexity (Section 3) from algorithmic recovery (Section 4). Nevertheless, the practical motivation for the agnostic setting (LLM annotation, citizen science) sits somewhat uneasily with an intractable estimator, and a brief acknowledgment of this mismatch would improve the framing.

### Trivial

1. **Equation (12) has a denominator discrepancy with equation (9).** In (9), the first log's inner fraction has denominator 2σ₂²; in (12), the same term has denominator 2σ₁⁴. The asymptotic expansions in (13)-(14) match the 2σ₂² version, confirming (12) contains a typo. This would confuse a reader trying to verify the derivation.

2. **γ > 1 is asserted without proof in (12).** While the inequality is correct (σ₂² > σ₁² ensures the numerator argument exceeds the denominator argument in the corrected expression), the paper provides no brief justification.

## Nice-to-Haves

- Calibrate the agnostic sufficient condition against the known homogeneous-noise threshold (σ₁² = σ₂²). Since the cubic equation relaxation reduces to the known sharp condition in the homogeneous case, explicitly showing this would give readers confidence the relaxation is not wildly loose.
- Bound the gap between the relaxed and optimal Chernoff exponent, even with a constant-factor estimate.
- Acknowledge the computational intractability of estimator (8) explicitly in the main text rather than only implicitly in Remark 3.2.

## Removed Points

- **"Conclusion drops the 'under our sufficient condition' caveat."** Removed as factually incorrect. The conclusion (line 336) states: "under our sufficient condition, one high-quality sample is never worth more than two low-quality samples." The caveat is consistently present in the abstract (line 9), introduction (line 81), and conclusion. This criticism was based on a misreading of the paper.

- **"Proposition 4.1 creates a misleading conditional phase transition."** Removed. Theorem 3 clearly states both conditions (27) and (28) are needed for sufficiency; Proposition 4.1 characterizes when λ_p satisfying (28) exists. This is standard in the LASSO literature and is presented transparently.

- **"Pure formatting nitpicks"** and **"missing related work"** style criticisms: Removed per hard rules.

## Novel Insights

The harsh critic's observation that the gap between the relaxed sufficient condition and the true information-theoretic threshold is uncalibrated is valid but is a limitation the paper already acknowledges. Beyond the paper's own contributions, the most interesting synthesis is the broader pattern the conclusion identifies: the algorithmic threshold appears systematically more "robust" to changes in problem structure (sparse design, heterogeneous noise) than the information-theoretic threshold, which connects this paper's findings to a pattern observed across the literature (Wang et al., Omidiran & Wainwright).

## Suggestions

1. Fix the typo in equation (12) — change 2σ₁⁴ to 2σ₂² to match (9) and the asymptotic analysis.
2. Add a brief justification for γ > 1 in the agnostic setting.
3. Add a calibration remark: show that the relaxed sufficient condition recovers the known sharp threshold in the homogeneous-noise limiting case σ₁² = σ₂², to give readers some sense of the relaxation's tightness.

## Score and Decision

**Round 1 bracket:** Based on calibration search against similar theoretical papers in the ICLR corpus, the plausible range was initially set at [5.5, 7.5].

**Anchors consulted:**
- *Sparsistency for inverse optimal transport* (6.75, Round 1): Similar type of contribution — extending irrepresentability conditions to a new problem setting, with strong theory but limited experiments. Comparable technical depth and rigor.
- *On the Learn-to-Optimize Capabilities of Transformers in In-Context Sparse Recovery* (7.00, Round 1): Strong theory plus empirical validation. The current paper has a cleaner narrative but lacks the experiments of this anchor.
- *Lasso Bandit with Compatibility Condition on Optimal Arm* (6.33, Round 1): Relaxing assumptions for LASSO bandits with theoretical and experimental backing. Similar in nature to the current paper's LASSO extension.
- *Flat Minima in Linear Estimation and an Extended Gauss Markov Theorem* (5.67, Round 1): Theoretical contribution with notable presentation issues and only synthetic experiments. The current paper is better written and more rigorous.
- *The Phase Transition Phenomenon of Shuffled Regression* (5.80, Round 2): Rejected despite interesting phase transition analysis due to readability issues and unclear derivations. The current paper is clearly stronger.
- *Sparsistency for inverse optimal transport* (6.75, Round 2): Confirmed as the most directly comparable anchor — both papers extend known LASSO-style theory to new settings with clear framing.
- *Distribution-Specific Agnostic Conditional Classification With Halfspaces* (6.20, Round 2): Theory paper on agnostic classification accepted at ICLR. Similar level of theoretical rigor.

**Final assessment:** The paper is a solid theoretical contribution that extends sparse recovery theory to a practically motivated new setting (mixed-quality data). The Price of Quality concept is clean and interpretable; the LASSO extension is technically non-trivial; the writing is clear and limitations are honestly scoped. The main weakness — that the headline γ ≤ 2 result derives from an uncalibrated sufficient condition — is real but appropriately caveated and does not undermine the broader contribution. The paper is stronger than rejected theoretical papers in the 5.5–6.0 range and comparable to accepted theory papers in the 6.0–7.0 range. A score of 6.5 reflects a paper that makes a genuine, well-executed contribution but has a notable limitation (uncalibrated sufficient condition) that keeps it from the top tier.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>