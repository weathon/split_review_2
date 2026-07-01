Now I have all the calibration context I need. Let me write the final review.

**Calibration summary:**

**Band 1 (score < 1.5):** Papers like "Analyzing Complex Interdependencies..." (1.0) — not proper research. Our paper is clearly not in this band.

**Band 2 (1.5–3.5):** "Weak Correlations" (2.33) — missing content, unsupported claims; "NTK with Derivative Labels" (3.0) — limited scope, synthetic-only. Our paper has a fatal mathematical error but better writing and more substance.

**Band 3 (3.5–5.5):** "Understanding NTK Trace" (3.75) — questionable methodology; "How many samples" (4.67) — solid theory with flaws. Our paper's fatal error pushes it below this band.

**Band 4 (5.5–7.5):** "Divergence of NTK" (5.75, accepted) — novel rigorous proof; "Connecting NTK and NNGP" (6.0) — interesting but incomplete. Our paper lacks the proof rigor for this band.

**Bracket:** The paper sits between 2.33 and 3.75. The fatal mathematical error in the central proof (Property (4) is demonstrably false) prevents it from rising above 3.5, but the well-motivated problem and some correct supporting results prevent it from falling below 2.0. Final score: **3.0 (reject)**.

---

## Summary

This paper studies the behavior of the deterministic Neural Tangent Kernel (NTK) for infinitely wide ReLU networks as depth \(L \to \infty\), under the scaling condition \(L \in o(\min n_i)\) so the NTK remains deterministic. The paper claims: (1) the normalized NTK converges entrywise to 1 (Theorem 2); and (2) even though the kernel becomes singular, the NTK predictor quantity \(\tilde{\Theta}_\infty^{(L)}(x^\top X)^\top (\tilde{\Theta}_\infty^{(L)}(XX^\top))^{-1}\) converges to a well-defined limit (Theorem 3), proved via rough differential equations.

## Strengths

1. **Addresses a genuine gap in NTK literature.** The regime where depth \(\to \infty\) while width grows much faster (deterministic yet singular NTK) is underexplored. Most prior work treats depth as fixed (Jacot et al.) or studies depth-to-width \(\to \infty\) where the NTK becomes stochastic (Hanin & Nica). The intermediate regime is worth analyzing.

2. **Lemma 1 and Theorem 2 are non-trivial and appear correct.** The recurrence for \(\rho^{(L)}\) (arcsin kernel) is well-known, and the claim that \(\rho^{(L)} \to 1\) from any starting value in \(]-1,1[\) is consistent with known contraction properties. Theorem 2's claim that the normalized kernel strictly increases to 1 follows naturally from the recurrence in Proposition 4.

## Weaknesses

### Fatal

1. **Property (4) of Proposition 5 is mathematically incorrect, invalidating Theorem 3's proof.** Property (4) states
   \[
   \lim_{d \to 0^+} \frac{d^k}{dz^k}\psi_d(z) = 0 \quad \forall j,k \in \mathbb{N}_0.
   \]
   The function is \(\psi_d(z) = 1/(1+\exp(-2z/(d(1-z^2))))\) for \(z \in (-1,1)\). Computing the first derivative at \(z=0\):
   \[
   \psi_d'(0) = \frac{1}{2d} \;\longrightarrow\; \infty \quad\text{as } d \to 0^+.
   \]
   Therefore \(\lim_{d\to 0^+} \psi_d'(0) \neq 0\), directly contradicting Property (4) for \(k=1\) at \(z=0\). This is not a subtle point — the derivative blows up, it does not vanish.

   The proof of Theorem 3 (lines 217–225) explicitly relies on Property (4) to argue that the numerator terms \(v_{(i,j)}\) converge to 0 and that the rough path lift has the required convergence properties ("By property (4) of \(\psi_{\mathcal{D}}\)... using (4), we have that the \(v_{(i,j)}\) converge to 0 in the 1-variation metric"). Since Theorem 3 is the paper's headline contribution and its proof depends on a false claim, **the paper's central result is unsupported.** This is a structural error, not a missing detail that could be filled by the appendix.

### Major

2. **Theorem 3's proof has additional gaps beyond the Property (4) error.** Even setting aside the mathematical error above, the proof sketch (lines 193–225) does not convincingly connect to rough path theory:
   - The interpolation \(A_n^{(L+1)}(t) = \tilde{\Theta}_\infty^{(L)} + \psi_{\mathcal{D}}(2t-1)(\tilde{\Theta}_\infty^{(L+1)}-\tilde{\Theta}_\infty^{(L)})\) applies the same scalar weight \(\psi_{\mathcal{D}}(2t-1)\) uniformly to all matrix entries. The justification that the resulting path has a rough path lift with controlled \(p\)-variation that converges appropriately is asserted without verification.
   - The invocation of the Lyons Universal Limit theorem requires verifying specific conditions (existence of a continuous lift with controlled \(p\)-variation, convergence in the appropriate topology) that are not checked in the text. The proof states that \(v_{(i,j)}\) are "of bounded total variation" and converge "in the 1-variation metric" without constructing the lift or demonstrating that these properties suffice.
   - The step from "\(v_{(i,j)} \to 0\)" to "the solution \(u^{(L+1)}(t)\) converges to \(u_\infty(t)\) solving \(u'_\infty(t) = \mathbf{0}_n\)" is asserted without showing how the Lyons theorem applies to this specific construction.

   These gaps, combined with the fatal error in Property (4), mean Theorem 3 is not established.

### Minor

3. **Proposition 4's \([0,1]\) range claim is incorrect.** Proposition 4 states "Moreover, the values in the normalized kernel are all found in the interval \([0,1]\)." From Definition 4, \(\bar{\Theta}_\infty^{(1)}(x,x') = x^\top x'\) for \(x,x' \in S^{n_0-1}\). This is the cosine similarity, which can be negative (e.g., \(-1\) for antipodal points). The claim should be qualified (e.g., "for \(L\) sufficiently large") or corrected. However, this error does not propagate to Theorem 2, whose "strictly increases to 1" claim does not require non-negativity.

4. **Limited experimental validation.** The experiments (Figure 1) go up to depth 30, yet the paper acknowledges convergence of \(\bar{\Theta}_\infty^{(L)}\) is logarithmic, meaning depths far beyond 30 would be needed to verify convergence to 1. While the third column of Figure 1 does compute the Theorem 3 quantity (contrary to one reviewer claim — the figure caption explicitly lists \(\bar{\kappa}^{(l)}(x^\top X^\top)(\bar{\kappa}^{(l)}(XX^\top))^{-1}\)), the paper does not discuss those results in the text, missing an opportunity to numerically support the central claim. No comparison is made against actual finite-width network training.

### Trivial

5. **Confusing wording in conclusion (line 262):** "While convergence for the limiting kernel is sublinear, the convergence for the limiting kernel is experimentally fast" — "limiting kernel" appears twice with different referents.

6. **The \(j\) index in Property (4)** is a free variable that does not appear in the expression, suggesting a copy-paste error.

## Nice-to-Haves

- The paper does not provide an explicit formula or qualitative description of the limiting solution \(u_\infty\) — only existence is claimed. A concrete characterization would strengthen the contribution.
- The scaling condition \(L \in o(\min n_i)\) is mentioned but never revisited to verify that the double limit (width \(\to \infty\) first, then depth \(\to \infty\)) commutes.

## Removed Points

These points from the input review were removed after verification against the paper:

1. **Claim that the inequality \(a^\psi b^{1-\psi} \geq ab\) is "not generally true."** For \(a,b \in (0,1)\) (which the paper states holds for large \(L\)), this inequality is in fact always true. The weighted geometric mean of two numbers in \((0,1)\) is always at least their product. This criticism is factually incorrect.

2. **Claim that experiments do not compute the Theorem 3 quantity.** The reviewer stated "The experiments do not compute or approximate \(\tilde{\Theta}_\infty^{(L)}(x^\top X)^\top (\tilde{\Theta}_\infty^{(L)}(XX^\top))^{-1}\)." However, Figure 1's third column explicitly plots \(\bar{\kappa}^{(l)}(x^\top X^\top)(\bar{\kappa}^{(l)}(XX^\top))^{-1}\), which is the same quantity. This criticism is factually wrong.

3. **Various formatting/style nitpicks.** Removed per policy (parser artifacts, not author errors).

4. **Missing related work.** Removed per policy (cannot verify existence of missing references).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix Property (4) of Proposition 5.** The function \(\psi_d\) as defined does not have vanishing derivatives at \(z=0\) as \(d \to 0^+\); the first derivative at 0 blows up like \(1/(2d)\). Either define a different interpolation function whose derivatives genuinely vanish in the limit, or find an alternative approach to Theorem 3 that does not rely on this property. This is the single most critical issue.

2. **Provide a rigorous, self-contained proof of Theorem 3.** The current sketch leaves essential steps unjustified. If the rough path theory approach is pursued, all conditions for the Lyons Universal Limit theorem must be explicitly verified. Alternatively, a more elementary proof would increase confidence.

3. **Correct the \([0,1]\) range claim in Proposition 4** to reflect that \(\bar{\Theta}_\infty^{(L)}\) can be negative for small \(L\) when inputs have negative cosine similarity.

4. **Strengthen experiments** by explicitly computing and plotting the Theorem 3 quantity for larger depths and comparing against finite-width network training.

## Score and Decision

**Calibration anchors used:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/nSDOkm0SKo.md` (avg 1.00, Round 1 band 1): Not proper research — our paper is clearly above this.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/2NwHLAffZZ.md` (avg 2.33, Round 1 band 2): Unsupported claims, missing content, unclear notation. Our paper is better written and has more substance, but the fatal error is more severe than "missing content."
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/fUz6Qefe5z.md` (avg 3.00, Round 1 band 2): NTK theory paper with limited scope (synthetic data only). Similar score band.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/bWz8aOPwsJ.md` (avg 3.75, Round 1 band 3): NTK trace dynamics — empirical focus, questionable methodology.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/V6JRkfj9dU.md` (avg 4.67, Round 1 band 3): Solid theoretical result with rigorous proof — our paper lacks the proof rigor for this band.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/VEJzjAvaIy.md` (avg 5.75, Round 1 band 4): Rigorous NTK convergence proof, accepted — our paper does not meet this standard.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5EtSvYUU0v.md` (avg 6.00, Round 1 band 4): Interesting but incomplete proofs — rejected.

**Bracket:** Round 1 bracketing placed the paper between 2.33 and 3.75. The fatal mathematical error in Property (4) prevents it from reaching the 3.75+ band where papers have functional proofs, while the well-motivated problem and some correct supporting results prevent it from falling to the 1–2 range. The paper is closest to the 3.00 anchor ("NTK with Derivative Labels") in terms of overall quality level.

**Score:** 3.0 (Reject)
**Decision:** Reject

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>