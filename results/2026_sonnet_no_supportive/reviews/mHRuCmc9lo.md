## Final Review

---

## Summary
This paper studies robust (minimax) decision making when a forecaster satisfies only partial calibration—specifically H-calibration, which constrains residuals to be uncorrelated with a class of test functions H. The authors characterize the minimax-optimal decision rule via a duality argument (Theorem 3.1), and prove a sharp transition result (Theorems 4.1–4.2): once H contains the "decision calibration" test class, the minimax-optimal robust policy collapses to plug-in best response—exactly the same guarantee provided by intractable full calibration. They also derive tractable robust policies for common training-induced calibration conditions (self-orthogonality under squared loss, bin-wise calibration) and validate the framework on two regression datasets.

---

## Strengths

- **Sharp transition result (Theorems 4.1–4.2):** Prior work established that decision calibration implies no swap regret—a qualitatively weaker guarantee than full calibration's "trustworthiness" (optimal best response among all policies). This paper shows that under the minimax lens, decision calibration is the *exact* threshold at which robust decision making collapses to plug-in best response. The proof mechanism is elegant: decision-calibration constraints render the plug-in utility invariant to any adversarial tilt q ∈ Q (see the identity after Theorem 4.2, p.7), so the adversary cannot reduce the plug-in utility below its nominal value. This upgrades decision calibration's decision-theoretic status non-trivially.

- **Clean interpolating framework (Section 2, Eq. 5, Figure 1):** The formulation of Q as all conditional expectations consistent with H-calibration, and the minimax problem over Q, provides a principled bridge between fully conservative and fully aggressive decision making. The volume intuition—richer H shrinks Q—is made precise via the duality characterization.

- **Proposition 4.4 (self-orthogonality under squared loss):** Identifies an H-calibration guarantee that holds "for free" for any linear-head model trained to MSE stationarity, without any post-processing. This concretely connects the abstract framework to the most common training paradigm.

- **Corollary 4.3 (simultaneous plug-in optimality):** A practically useful byproduct—a single decision-calibrated forecaster simultaneously certifies best-response minimax optimality for multiple downstream decision makers with different utility functions.

---

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Linearity assumption (Assumption 2.1) restricts scope.** The paper motivates the framework with high-stakes domains (healthcare, finance, line 13) where risk aversion is common, yet Theorem 4.1's proof fundamentally requires u(a,v) to be linear in v—the invariance E[u(a_BR(f(X)), q(f(X)))] = E[u(a_BR(f(X)), f(X))] (p.7) depends directly on linearity. Non-linear (risk-averse, variance-penalizing) utilities are excluded. The paper is honest about this limitation (Sections 2 and 6), and notes some non-linear utilities can be linearized over appropriate bases, but acknowledges those bases are not always low-dimensional. This is a genuine scope restriction worth flagging, even though it is standard in the calibration literature.

- **Experimental section is thin relative to the abstract's framing.** The experiments test only the secondary self-orthogonality result (not the main decision-calibration theorem) on two datasets with three-action decision problems, with no variance across runs reported. Utility differences are small (∼2% for Bike Sharing, ∼7% for California Housing under adversarial evaluation). This is appropriate for a theory paper where experiments serve as a sanity check, but the abstract's promise of "an empirical evaluation" slightly overstates what Section 5 delivers.

- **Continuous action sets not discussed.** Theorem 4.1 uses |A| indicator functions (one per action), requiring finite A. Motivating domains often involve continuous actions (dosage, investment level in [0,1]), where the decision-calibration class would be infinite. Even a brief discussion of whether the result extends or breaks down in continuous-A settings would strengthen the paper.

### Trivial
- **Proposition 4.5 recovers a known heuristic.** The result that bin-wise calibration leads to best responding to the bin mean has an intuitive precedent; the contribution is deriving it systematically from Theorem 3.1, which is appropriate, but the paper could acknowledge more explicitly that this formalizes an existing practice.

---

## Nice-to-Haves

- A worked theoretical example where H is strictly below the decision-calibration threshold and the robust policy provably differs from best response by a non-trivial amount would make the "sharp transition" concrete and vivid.
- A discussion of whether the adversarial model in Eq. 5—allowing a different worst-case q(v) for each forecast value, subject only to aggregate moment constraints—is well-matched to practical distribution shifts in the stated application domains.
- A third experimental condition: a calibration-preserving distribution shift realized naturalistically (e.g., selecting test subsets where model error correlates with a specific feature consistent with H-calibration), rather than by an adversary.

---

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Evaluation validity" (experiments don't test Theorem 4.1):** Testing "best response is optimal under decision calibration" empirically is near-tautological; the secondary result is the appropriate empirical target. Not a genuine weakness.
- **Circular adversary concern in experiments:** The paper explicitly reports the more informative cross-evaluation in Table 1; the concern that robust vs. robust adversary is "definitional" is not a meaningful weakness.
- **Proof of Theorem 3.1 not reviewable (appendix stripped):** Parser artifact, not an author error. The main body gives a complete characterization; the proof details live in a stripped appendix.
- **Approximate calibration in experiments / Appendix B:** The paper explicitly acknowledges approximate calibration and references Appendix B. Removed per hard rules on appendix content.
- **"Mild cost of robustness" discussion insufficient:** The adversarial model pessimism concern is valid in principle but the paper acknowledges conservatism and the small gaps in Table 1 provide empirical evidence. Not a meaningful weakness.

---

## Novel Insights
The sharp transition result is the genuinely novel conceptual contribution: decision calibration is not merely a tractable approximation of full calibration but is the *exact* minimax threshold at which robust decision making collapses to plug-in best response. This reframes the significance of decision calibration from a regret-bounding tool (swap-regret guarantees, which restrict comparisons to action-remapping policies) to a full trustworthiness certificate (no adversarially consistent distribution can hurt the plug-in policy's utility below its nominal value). The mechanism—that the calibration constraints render the plug-in policy's utility adversary-invariant—is elegant and may have broader applicability in other partial-information decision settings.

---

## Suggestions
- Discuss the implication of linearity for the stated high-stakes motivating domains even if extension to non-linear utilities is left for future work.
- Include confidence intervals or variance across runs for the experimental results, even if small.
- Add a brief discussion (even one paragraph) of the continuous action set case, explaining whether the proof technique for Theorem 4.1 extends or what the obstacle is.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Human Score | Round | Comparison |
|------|----------------|-------|------------|
| bEgDEyy2Yk | 1.00 | R1 | Unrelated (graph algorithms) |
| nSDOkm0SKo | 1.00 | R1 | Unrelated (financial news) |
| p79lnC36CO | 2.00 | R1 | Calibration diagnostics, applied, no theory |
| ZBL26FX0FT | 3.00 | R1 | Calibration for selective classifiers, applied |
| 7BDUTI6aS7 | 3.00 | R1 | DRO with risk quadrangle, less novel framework |
| XM7INBbvwT | 4.67 | R1 | Calibration + human decisions, HCI experiment, not theory |
| 5HpZZbgdeK | 5.00 | R1 | Efficient calibration for many classes, engineering contribution |
| nNQmZGjEVe | 4.25 | R1 | Calibrated RAG, empirical, less theoretical |
| X0epAjg0hd | 5.67 | R1 | Calibration metrics reassessment, good but methodological |
| uuPkll6i7m | 6.75 | R1 | Certified calibration under adversarial attacks, comparable scope |
| dIkpHooa2D | 6.75 | R1 | Minimax DRO in function space, similar mathematical depth |
| iOMnn1hSBO | 6.80 | R1/R2 | Decision-focused UQ via conformal, similar problem setting |
| TTrzgEZt9s | 8.00 | R1 | DRO with bias-variance reduction, stronger empirical contribution |
| TId1SHe8JG | 7.50 | R2 | Higher-order calibration with formal guarantees, most comparable |
| LqTz13JS2P | 7.25 | R2 | Principal-agent theory with regret bounds, comparable theory depth |
| i2Phucne30 | 7.00 | R2 | Bias-variance alignment theory with calibration connection |

**Round 1 bracket:** Based on comparators, this paper sits between 6.75 (uuPkll6i7m, dIkpHooa2D) and 8.0 (TTrzgEZt9s). Initial bracket: **6.5 to 8.0**.

**Round 2 narrowing:** The most topically similar paper is TId1SHe8JG (7.5: "Provable Uncertainty Decomposition via Higher-Order Calibration"), a theory paper introducing a new calibration notion and proving formal guarantees, with modestly supporting experiments. The paper under review has a comparably novel and crisp central result (the sharp transition theorem), a similarly clean framework, and a similar experimental footprint (sanity check rather than empirical contribution). The paper under review is arguably more directly applicable (does not require k-snapshots) but more restricted in scope (linearity of utility). LqTz13JS2P (7.25) is also very comparable—theory paper with formal decision-theoretic results and modest empirical validation. Placing this paper at **7.5** is appropriate: above the 6.75-7.0 range (which requires a stronger empirical contribution), and below 8.0 (which requires either a more comprehensive theory or a more complete empirical evaluation).

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>