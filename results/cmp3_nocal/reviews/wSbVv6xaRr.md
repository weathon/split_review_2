Here is the final consolidated review.

---

## Summary

This paper proposes FedMPDD, a federated learning algorithm that compresses client gradients by computing directional derivatives along m random Rademacher vectors. Each client transmits only m scalars plus a seed (O(m) vs O(d) communication per round), and the server reconstructs a gradient estimate using the same random vectors. The method is unbiased, provides a tunable communication-fidelity trade-off via m, and the paper provides a convergence analysis (O(1/√K) to a stationary point) and experiments showing communication savings and protection against gradient inversion attacks.

## Strengths

1. **Clean theoretical quantification of the compression-fidelity trade-off.** Lemma 1 (line 132–134) gives an exact expression for the expected relative squared reconstruction error: (d‑1)/m. This is a precise, well-derived result that directly relates the compression ratio to gradient fidelity and provides a principled basis for choosing m.

2. **Real and straightforward communication reduction.** Transmitting m scalars (+ one seed) instead of a d-dimensional gradient is a clear savings story. The encoding/decoding mechanism is well-specified (Algorithm 2, lines 58–86): the client computes m inner products with shared-seed Rademacher vectors, the server reconstructs from the same vectors. The mechanism is implementable and the benefit is unambiguous.

3. **Unbiased estimator with JL-based convergence guarantee.** Theorem 2 (line 114) establishes an O(1/√K) convergence rate to a stationary point, using the Johnson–Lindenstrauss lemma to control the distortion from multi-projection averaging. This is a clean theoretical bridge between random projection theory and FL convergence.

4. **The tunable m parameter provides a principled three-way trade-off** among communication cost, gradient fidelity, and protection against gradient inversion, supported by the quantitative bound in Lemma 1.

## Weaknesses

### Fatal
None.

### Major

1. **Privacy claims are substantially overstated relative to what is actually proven.** The paper repeatedly uses language such as "inherent privacy," "privacy guarantee," and "formal defense against GIAs" (lines 9, 29, 124, 136, 144). However:

   - **Lemma 1** (line 132–134) bounds the *gradient reconstruction error* — a property of any lossy compression scheme (quantization, sparsification, sketching all discard information). It is not a privacy guarantee.
   - **Lemma 2** (line 138–142) attempts to bound the data reconstruction error, but the bound depends on $L_v(\mathbf{x})$, "the Lipschitz constant of the gradient with respect to $\mathbf{v}$." This constant is stated (line 142) but never characterized, bounded, or derived for any architecture. If $L_v(\mathbf{x})$ can be large, the lower bound becomes arbitrarily weak; the lemma is essentially vacuous without further characterization.
   - No differential privacy analysis ($\epsilon,\delta$ or Rényi DP) is provided. The comparison with LDP on SSIM (an informal metric) conflates two different standards: LDP provides formal ($\epsilon,\delta$) guarantees; FedMPDD provides a heuristic "harder to reconstruct" property that any lossy compression method also possesses (as the paper's own Table 2 shows: QSGD, Top-k, and lp-proj all achieve SSIM < 1.0).

   The claim of a "concrete privacy guarantee" (line 144) is not supported by the evidence presented. The paper should either (a) provide a formal DP analysis of the mechanism, or (b) clearly re-frame what is provided as *gradient obfuscation through lossy compression*, quantified by Lemma 1's reconstruction error, and drop the "privacy guarantee" language.

2. **Abstract convergence rate ($O(1/K)$) contradicts the body's Theorem 2 ($O(1/\sqrt{K})$).** The abstract (line 9) states "FedMPDD converges at a rate of $\mathcal{O}(1/K)$, matching the performance of FedSGD." Theorem 2 (line 114) and the contributions list (line 32) both state $O(1/\sqrt{K})$, which is the standard non-convex stationary-point rate. $O(1/K)$ is a faster rate that the paper does not prove. This is a factual error in the abstract that must be corrected.

### Minor

1. **The "fundamentally new encoding paradigm" framing is overstated.** The paper (lines 28, 40) distinguishes itself from "structured and sketched updates" by claiming those use a "fixed, low-dimensional subspace" while FedMPDD uses dynamic per-client per-round random projections. However, many sketching/random-projection methods (e.g., Count‑Sketch, JL random projections) also use independently sampled random matrices. The core operation (project gradients onto random vectors, transmit coefficients, reconstruct) is a known random-projection/sketching technique. The genuine distinction — unbiasedness due to fresh randomness per client per round — is a real advantage but an incremental one, not a "fundamental departure" (line 40).

2. **Computational overhead is not fully accounted.** Remark 1 (line 120) acknowledges that the current implementation computes the full stochastic gradient $\mathbf{g}_i(\mathbf{x}_k)$ (Algorithm 2 line 6) *then* computes $m$ inner products, incurring $O(dm)$ additional work per client per round. The JVP-based alternative that avoids computing the full gradient is described as a "follow-up study" — meaning the experiments in this paper incur this extra cost. The overhead is claimed to be "negligible" but is not quantified relative to the baseline methods' compute. The paper should either justify the $O(dm)$ cost or implement the JVP approach.

3. **The multi-round composition bound (Remark 2) may be restrictive in practice.** The bound states that unique gradient recovery is impossible if $T \times m < d$ (line 148). For the CIFAR-10 experiment ($d \approx 300K$, $m=600$), this allows $T < 500$ rounds. Many FL training runs extend to thousands of rounds. The paper presents this as a "generous bound" without discussing regimes where it is violated.

4. **Communication cost specification is imprecise.** The paper describes transmitting "$m+1$ scalars" and "$O(m)$ bits" (lines 31, 122) but does not specify whether the $m$ scalar inner products $s_k^i[j]$ are quantized or transmitted at full (32-bit) precision. The seed is negligible, but the $m$ scalars are real-valued and require some precision budget. The paper should clarify the bit budget per scalar.

5. **No statistical variability reported.** Tables 1 and 2 report single numbers without variance or confidence intervals. Given the method involves random projections, results may vary across runs. Means and standard deviations over multiple trials should be reported.

### Trivial
- The estimator notation varies between equations (2)–(3) and the algorithm, making internal consistency checks harder than necessary.

## Nice-to-Haves
- A comparison against a fixed-random-matrix version of random projection (same projection across all clients/rounds) would isolate the effect of fresh randomness from the general benefit of random projection.
- Lemma 2 could be made meaningful by characterizing $L_v(\mathbf{x})$ for standard architectures or providing an explicit smoothness assumption.

## Removed Points
These points appeared in the original harsh review but are removed or downgraded:

- **Claim that the experimental comparison is "systematically unfair" and "rigged":** The paper compares FedMPDD against multiple baselines (lp-proj, Top-k, SA-FedLora, QSGD) under identical communication budgets, and FedSGD is explicitly marked when it exceeds the budget. The comparison is informative, not rigged. The critic's suggestion that baselines' hyperparameters were not tuned is speculative — the paper states "Hyperparameter tuning details for each model are in Appendix H.2" (line 168), and the appendix was stripped by the parser. **REMOVED.**
- **Claim about missing comparison to specific randomly-projected FL methods (FedSketch, Count-Sketch):** The paper does compare against lp-proj (a sketching method) and cites FedSketch in related work. Missing a specific variant from a crowded literature is not a meaningful weakness. **Moved to Nice-to-Haves.**
- **Claim that "smaller m values sometimes yielded faster convergence" contradicts Theorem 2:** Theorem 2 provides an upper bound, not a tight characterization. Claiming an empirical observation contradicts an upper bound is conceptually incorrect. **REMOVED.**
- **Criticisms about missing appendix content (proofs, related work sections):** The parser strips appendices from all papers; these exist in the original submission. **REMOVED.**
- **Formatting and notation nitpicks:** Reduced to a single trivial point. **REMOVED.**

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Fix the abstract to say $O(1/\sqrt{K})$ consistently with Theorem 2.
2. Either (a) provide a formal DP analysis of the projection mechanism, or (b) clearly re-frame the privacy claim as "protection against GIAs through lossy compression, quantified by Lemma 1's reconstruction error" and remove the "privacy guarantee" language. Characterize $L_v(\mathbf{x})$ in Lemma 2 or remove it.
3. Clarify the bit budget for the $m$ scalars (are they quantized? at what precision?).
4. Report means and standard deviations over multiple runs.
5. Either implement the JVP approach or quantify the $O(dm)$ overhead relative to the full gradient computation.

## Score and Decision

The core method is sound, the communication reduction is real, and Lemma 1 provides a clean theoretical foundation. The main issues are overclaimed privacy framing (Lemma 2's uncharacterized constant, absence of formal guarantees) and a factual error in the abstract. These are fixable with revisions. The paper makes a genuine contribution to communication-efficient FL.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>