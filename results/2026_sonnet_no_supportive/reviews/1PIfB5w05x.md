Now I have enough to draft the review. Let me submit the draft and then run calibration.## Final Review

---

## Summary
This paper studies sparse signal recovery under heterogeneous (mixed-quality) noise, where $n_1$ high-quality ($\sigma_1^2$) and $n_2$ low-quality ($\sigma_2^2 > \sigma_1^2$) observations are available. It establishes sufficient conditions for information-theoretic recovery in agnostic and informed settings (Theorems 1 & 2), introduces the "Price of Quality" as the trade-off rate between sample types, and provides necessary-and-sufficient conditions for LASSO recovery in the agnostic setting (Theorem 3). The central surprise is that LASSO is completely blind to noise heterogeneity, depending only on total sample count and average noise—in sharp contrast to the IT regime where the informed decoder can exploit heterogeneity to achieve an unbounded Price of Quality.

---

## Strengths

- **Theorem 3 is a technically substantial sharp result.** It establishes both necessary and sufficient conditions showing LASSO's recovery threshold under heterogeneous noise equals the homogeneous threshold, governed by $n = n_1 + n_2$ and $\sigma_{\text{avg}}^2 = (n_1\sigma_1^2 + n_2\sigma_2^2)/n$ (eqs. 26–28). The proof adapts Wainwright (2009) to a setting where $\Sigma$ is not a scalar multiple of the identity, destroying Wishart structure; this is resolved via QR/Haar-measure analysis (eq. 49, Lemma D.6). The result is clean, interpretable, and proven in both directions.
- **The IT/algorithmic dichotomy is genuinely illuminating.** In the informed IT setting (low-SNR₂, high-SNR₁, eq. 20), the Price of Quality grows as $\Theta(\log\text{SNR}_1 / \text{SNR}_2) \to \infty$. Yet for LASSO, both sample types contribute identically. This is the paper's core conceptual finding, and it is well supported by the evidence—one proven sharp threshold (Theorem 3) and one rigorously analyzed sufficient condition (Theorem 2 with exact Chernoff optimization).
- **Generalization to arbitrary non-singular noise covariance** (Remark 3.4, eqs. 22–23) cleanly extends the two-group framework to per-sample noise levels without additional proof machinery.
- **Honest acknowledgement of limitations.** Remark 3.2 explicitly identifies that condition (9) is sufficient (not tight) due to a Chernoff relaxation, and that estimator (8) may be suboptimal. Remark 3.3 acknowledges necessity for the IT bounds remains open.

---

## Weaknesses

### Fatal
None.

### Major
- **The "Price of Quality ≤ 2" headline claim is for a sufficient condition on a potentially suboptimal estimator, but is presented too definitively.** Theorem 1 establishes condition (9) for the unweighted $\ell_2$ estimator (8). As Remark 3.2 acknowledges: (i) the Chernoff relaxation introduces unknown looseness (the exact optimum requires solving a cubic, eq. 37), and (ii) a reweighted estimator may perform strictly better in the low-SNR regime. The "≤ 2" bound is thus doubly conservative—sufficient (not tight) for an estimator that may itself be suboptimal. The abstract states "one high-quality sample is never worth more than two low-quality samples" and §1.2.1 calls this a property of the Price of Quality without adequately qualifying it as a property of a specific sufficient condition. This framing overstates the evidential strength of Theorem 1 and could mislead readers about the actual IT limit of high-quality data.

### Minor
- **The sharpness claim for the informed IT threshold in the conclusion (§5, line 340) is unsupported by a necessity theorem.** The paper states "the informed information-theoretic threshold and the LASSO threshold are sharp." But Remark 3.3 explicitly acknowledges that "establishing full necessity in the heterogeneous setting remains an interesting direction for future work." The LASSO threshold is proven sharp in both directions (Theorem 3). The informed IT condition (Theorem 2) uses a tight Chernoff exponent analogous to known homogeneous results, making the conjecture reasonable—but claiming "sharp" in the conclusion without a necessity proof is misleading, and treats a conjectured property as established. The distinction should be made explicit in the main body.
- **The necessity direction of Theorem 3 (eq. 26) does not require the noise-scaling condition of Proposition 4.1**, while the sufficiency direction (eq. 27–28) does require (30). The paper does not comment on whether the failure regime analysis extends to noise scaling beyond the sufficiency regime. A brief remark on this asymmetry would clarify scope.

### Trivial
- Equation (12) lists $2\sigma_1^4$ in the denominator of the first argument, while the corresponding term in condition (9) uses $2\sigma_2^2$. This is very likely a PDF parser artifact, but authors should verify the formula is consistent with (9) in the original submission.

---

## Nice-to-Haves
- A lower bound / necessity result for Theorem 1 (agnostic IT) would convert the agnostic Price-of-Quality analysis from a bound on a sufficient condition into a true threshold. Even a Fano-type converse in specific SNR regimes would strengthen the paper considerably.
- For Theorem 2, even a partial necessity argument (e.g., a Fano lower bound in the informed setting) would allow the IT/algorithmic comparison to rest on two rigorous phase transitions rather than one.
- A partial result on the GLS-LASSO in the informed setting (e.g., a sufficient condition showing it achieves a lower sample threshold than agnostic LASSO in some regime) would close the loop on the algorithmic analysis.

---

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **Potential typo in eq. (12) ($\sigma_1^4$ vs $\sigma_2^2$):** Elevated to Trivial in the main review because it may be a genuine inconsistency—but kept only as a verification note. Per hard rules, pure parser/formatting artifacts should not count against the paper.
- **The agnostic estimator (8) may not be IT-optimal:** The harsh critic raised this as a major issue; however, the paper explicitly acknowledges this limitation in Remark 3.2. The weakness is already incorporated as part of the broader "Major" point above about overstatement, not as an independent flaw.
- **Generic calls for stronger baseline comparisons:** Not raised by the reviewer; not applicable (pure theory paper).

---

## Novel Insights
The most structurally interesting finding—beyond the paper's own framing—is that LASSO's averaging over heterogeneous noise is not an approximation or performance loss: it is exact in the sense that the threshold depends on $\sigma_{\text{avg}}^2$ through the first-order KKT conditions (eq. 29), not through any relaxation. This suggests a broader principle: polynomial-time algorithms for sparse recovery may systematically average out heterogeneity that matters information-theoretically, consistent with the growing body of evidence that the algorithmic threshold is more "robust" to problem perturbations (Gamarnik & Zadik 2022; Wang et al. 2010; Omidiran & Wainwright 2008). The Haar-measure approach used to handle the non-Wishart structure may have broader applicability in heterogeneous-design compressed sensing.

---

## Suggestions
1. Revise the abstract and §1.2.1 to explicitly qualify "Price of Quality ≤ 2" as a property of the sufficient condition for the specific agnostic estimator (8), distinguishing it from a claim about the true IT limit.
2. In §5, replace "the informed information-theoretic threshold and the LASSO threshold are sharp" with language that distinguishes the proven sharp result (Theorem 3) from the conjectured sharp result (Theorem 2), and cross-reference Remark 3.3.
3. Add a brief remark in §4 on the asymmetry between necessity (eq. 26) and sufficiency (eqs. 27–30) with respect to noise scaling.
4. Verify eq. (12) against eq. (9) to ensure the $\sigma_1^4$ denominator in the original submission matches $\sigma_2^2$ from condition (9).

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `Uj0h13lVrR.md` (GFlowNets KL divergence) | 1.0 | R1 | Unrelated, strong reject |
| `vQIVbfTMzf.md` (Finite-sample/asymptotic regimes) | 3.25 | R1 | Related theme (high-dim stats) but weaker contribution, rejected |
| `gVVoZtiQlt.md` (Phase transition shuffled regression) | 5.0 | R1 | Topically closest — phase transition in regression; paper under review is narrower but stronger technically |
| `sIcPMMhl9W.md` (Phase transition shuffled regression v2) | 5.8 | R1/R2 | Same paper, borderline reject; paper under review has a cleaner sharp result (Theorem 3) |
| `YvOq7jHT6R.md` (Hard-thresholding multi-biased) | 3.75 | R1 | Weaker: sparse optimization without sharp thresholds |
| `H8OOlBjhkU.md` (Sparse restricted convex sets) | 5.0 | R1 | Similar scope: sparse optimization theory |
| `NHhjczmJjo.md` (Transformers in-context sparse recovery) | 7.0 | R1/R2 | Accepted; more machine-learning flavor, multiple tight results |
| `sIcPMMhl9W.md` | 5.8 | R2 | Borderline reject; paper under review has comparable IT analysis + stronger algorithmic result |
| `wpXGPCBOTX.md` (Sparsistency for iOT) | 6.75 | R1/R2 | Accepted; comparable theory depth, both directions proven |
| `FT4gAPFsQd.md` (How sparse can we prune) | 6.0 | R1 | Borderline reject/accept; comparable theoretical scope |
| `nIEjY4a2Lf.md` (Misspecified Q-learning sparse linear) | 6.0 | R2 | Accepted; clean theoretical extension, all reviews 6/6/6/6 |
| `f3jySJpEFT.md` (LASSO Bandit with compatibility) | 6.33 | R2 | Accepted; clean extension of LASSO theory to new setting, close analog |
| `nxnbPPVvOG.md` (Flat minima Gauss-Markov) | 5.67 | R2 | Accepted (borderline); theoretical extension, mixed reviews |
| `fMTPkDEhLQ.md` (Tight lower bounds Hölder smooth) | 8.0 | R1 | Accepted strong; tight bounds in both directions — clearly stronger than paper under review |
| `4xWQS2z77v.md` (Loss landscape neural networks convex duality) | 8.0 | R1 | Unrelated, strong accept |

**Round 1 bracket:** Between 5 and 7. The paper has one genuinely sharp result (Theorem 3, both directions) comparable to accepted papers at 6.0–6.75, but the IT results are only sufficient conditions with a potentially overclaimed headline finding.

**Round 2 narrowing:** The closest analogs are:
- *Phase transition shuffled regression* (5.8, borderline reject): That paper studies a similar phase-transition question using message passing; it has more complex machinery but also only sufficient conditions. Reviewers gave it 5–8 range.
- *Lasso Bandit / Misspecified Q-learning* (6.0–6.33): Clean theoretical extensions of known methods to new settings, all accepted. The paper under review is comparable in scope.
- *Sparsistency for iOT* (6.75): Accepted; proves both directions for a related problem.

The paper under review is stronger than the shuffled regression papers (Theorem 3 is proven in both directions, the conceptual finding about noise averaging is clean) but weaker than sparsistency/iOT (which proves both directions throughout). The major weakness — the IT headline overclaimed — is real but addressable. I place this at **5.5**: a borderline paper that makes a real contribution (Theorem 3 is solid, the dichotomy is interesting) but the IT half is weaker than presented, and the abstract sets expectations that the proofs don't fully meet.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>