Now let me produce the final review.

**Round 1 bracket: [3.5, 5.0]**

The most similar anchor is "Achieving Dimension-Free Communication in Federated Learning via Zeroth-Order Optimization" (DeComFL, avg score 6.25, accept). Both papers use random projections to achieve dimension-free communication in FL. DeComFL scored higher because its claims were more modest (no privacy claims) and its experiments included large models (OPT-1.3B). FedMPDD has a more complex method (m projections vs 1), weaker experiments (only LeNet and small CNN), and overclaims privacy — a significant liability that pushes its score below DeComFL.

The DINAR paper (privacy-preserving FL, avg 5.00, reject) was criticized for lacking privacy guarantees despite claiming privacy protection. FedMPDD has a similar vulnerability — its privacy claims outrun its evidence. Combined with missing baselines and no non-IID results, FedMPDD falls below DINAR's score.

FedComLoc (avg 3.00, reject) is incremental and was scored lower. FedMPDD is more novel algorithmically, placing it above FedComLoc.

**Final score: 4.0 — borderline reject.** The novel algorithmic core is real, but the privacy overclaiming and experimental gaps prevent acceptance in the current form.

---

## Summary

This paper proposes FedMPDD, a federated learning method that compresses client gradients via multi-projected directional derivatives. Each client computes m directional derivatives along random Rademacher vectors instead of transmitting the full d-dimensional gradient, reducing uplink cost from O(d) to O(m). The method is unbiased and the paper provides an O(1/√K) convergence analysis. The paper also claims that the rank-deficient projection provides inherent privacy against gradient inversion attacks.

## Strengths

- **Novel gradient compression mechanism with clean theoretical motivation.** The connection between directional derivatives, the JL lemma, and FL gradient compression is well-motivated. The insight that averaging m independent rank-1 projections overcomes the √d variance scaling of a single projection (Section 2) is technically sound, and the use of the JL lemma to argue m = O(log d) directions suffice is a principled framing (equation 4, lines 108-112). This contrasts favorably with heuristic compression schemes.

- **Unbiasedness is a genuine technical advantage.** The paper correctly observes that ĝ(x_k) = (1/m)Σ_j u_j(u_jᵀg) satisfies E[ĝ] = g (line 106), differentiating the method from many biased compression schemes where E[ĝ] ≠ g, which can violate the descent condition.

- **Communication reduction is cleanly parameterized and practical.** The per-client per-round uplink cost of m+1 scalars (m directional derivatives + 1 seed) is precise and tunable. The seed-based reconstruction (line 88) is an elegant engineering detail that eliminates the need to transmit projection matrices.

## Weaknesses

### Major

- **Privacy claims are overclaimed relative to the evidence presented.** The paper's central selling point is "inherent privacy" against gradient inversion attacks (lines 29, 31), but the support has several gaps:

  - **Lemma 2's bound can be vacuous.** The lower bound on data reconstruction error (line 140-142) is E[||v - v̂*||²] ≥ (d-1)/(m·L_v(x)²)||g_i||², where L_v(x) is the Lipschitz constant of the gradient w.r.t. the input. For deep neural networks, L_v(x) can be very large, making the right-hand side arbitrarily close to zero. A bound that can be made vacuous by the model's own properties does not constitute a meaningful guarantee.

  - **No formal privacy definition is provided.** The paper contrasts FedMPDD with LDP (line 31: "uniform privacy protection regardless of the magnitude of the clients' gradients") but does not offer any comparable formal privacy definition. Gradient reconstruction error (Lemma 1) is a property of any lossy compression scheme, not a privacy definition. The leap from "gradient reconstruction is difficult" to "data is protected against gradient inversion attacks" is not formally bridged.

  - **Missing controlled empirical comparison.** The empirical evaluation (Tables 1-2) shows FedMPDD achieving SSIM ≤ 0.03 (Table 1) or 0.14-0.22 (Table 2), but the only LDP baselines achieve SSIM << 0.03 only at very low accuracy (~11% in Table 1) or with noise that "severely degrades model accuracy" (Table 2, Laplace var=10). The critical comparison is missing: **LDP with noise calibrated to achieve the same SSIM as FedMPDD (0.14-0.22), then compare accuracy.** Without this, one cannot distinguish "FedMPDD provides genuine privacy" from "FedMPDD's compression destroys enough gradient information to also hurt utility."

  - **Remark 2's multi-round bound is restrictive and unaddressed.** The bound T×m < d (line 148) allows at most ~100 rounds for LeNet (d≈60,000, m=600). The paper does not discuss what happens when this is violated in practical training, nor provides empirical evaluation of multi-round privacy erosion.

- **Missing baselines for joint privacy+communication.** The paper compares against communication-only methods (QSGD, Top-k, lp-proj) and FedSGD+Laplace, but not against methods that jointly address communication and privacy (e.g., DP-SGD with compression, DP-FedAvg, or the compressive DP methods cited in related work: Amiri et al. 2021, Agarwal et al. 2018). Since the paper's central claim is joint communication efficiency and privacy, these baselines are essential to establish the method's position.

- **Non-IID results are mentioned but absent from the main text.** The experimental setup (line 168) states "considering both IID and non-IID data distributions," but Tables 1 and 2 are labeled IID, and no non-IID results appear in any main-text table or figure. Non-IID data is a central challenge in FL, and there is no a priori reason to assume gradient compression via random projections behaves identically under heterogeneous data.

### Minor

- **Computational cost is not adequately addressed.** Remark 1 (line 120) suggests using Jacobian-vector products to avoid computing the full gradient, but explicitly states this strategy "is evaluated in our follow-up study" — meaning it was not implemented here. Server-side computation (Algorithm 2, lines 14-18) requires O(d × m × βN) operations per round, a factor of m more than FedSGD, but this cost is not reported or acknowledged.

- **The method uses single-step SGD (FedSGD-style), not local SGD (FedAvg-style).** The paper does not support multiple local steps, which is the primary mechanism for communication reduction in many practical FL deployments. The per-round communication savings are therefore compared without accounting for the fact that local-SGD methods need far fewer rounds.

- **The binary "Defendability" criterion is never defined.** Tables 1-2 use a ✓/✗ label (lines 184-194, 207-218), but the threshold or criterion for this label is not explained in the main text.

- **The fixed-budget scenario strongly favors compression methods by design.** While this is a legitimate evaluation strategy, the paper frames FedSGD's inability to operate under the budget as a method failure rather than a design choice. The budget of 0.9 GB (Table 2) is below what FedSGD requires for even a single round with the CNN model, as the paper itself acknowledges ("* indicates budget exceeded in the first iteration," Table 2 caption).

### Trivial

None.

## Nice-to-Haves

- A formal DP analysis of FedMPDD (even a crude bound showing that adding DP noise on top of the projection yields a combined guarantee) would substantially strengthen the privacy framing.
- An ablation separating the effect of m on per-round gradient quality from the budget effect.
- Reporting server computation time.
- Discussion of what happens when the T×m < d bound is violated in practical training.

## Removed Points

The following criticisms from the input review were removed after verification against the paper:

- **"Equation (3) dimension mismatch"**: The equation ĝ_i(x_k) = (u_{k,i}^T g_i(x_k)) u_{k,i} = (u_{k,i} u_{k,i}^T) g_i(x_k) is dimensionally consistent. No error exists.
- **"Fixed budget is a straw man — FedSGD allows 38 rounds for 0.09 GB"**: The reviewer's specific calculation applies a quote about Table 2 ("rapidly exceed the communication budget in the very first iteration," line 200) to Table 1's 0.09 GB budget. Line 200 explicitly states "In **Table 2** FedSGD..." The paper is accurate about Table 2. The general point (budget favors compression) is retained as a Minor weakness.
- **"Convergence analysis missing link — JL norm vs. variance"**: Without access to the appendix (which contains the proof), it is speculative whether the proof bridges this gap. Cannot be verified from available material.
- **"ResNet-18 claims not backed by experiments"**: The ResNet-18 example (line 25) is a motivating illustration, not an experimental claim.
- **"Theorem 2 mixing terms with different K-dependencies"**: This is a mathematical observation, not a weakness. Common in convergence bounds.
- **"JL lemma needs union bound across changing gradients"**: Speculative without the appendix proof.

## Novel Insights

The harsh critic correctly identifies a structural gap in the paper's privacy argument: Lemma 2's lower bound depends on the Lipschitz constant L_v(x), which can be arbitrarily large for deep networks, making the bound vacuous precisely when the model is most expressive. This is not a minor technicality — it undermines the paper's core privacy narrative. The critic also correctly identifies the absence of a controlled empirical comparison at matched SSIM levels, without which compression-induced information loss cannot be distinguished from genuine privacy protection.

## Suggestions

1. Substantially downgrade the privacy claims. Frame the gradient reconstruction error (Lemma 1) as "compression-induced gradient obfuscation" — a side benefit of the compression mechanism — rather than "inherent privacy." Remove or qualify the claim that the method is "fundamentally different from differential privacy approaches" (line 29).
2. Add the critical controlled experiment: compare FedMPDD against LDP with noise calibrated to the same SSIM level. If FedMPDD achieves higher accuracy at the same SSIM, that is a concrete, meaningful result.
3. Include at least one baseline that jointly addresses communication and privacy (e.g., DP-SGD with quantization, or Amiri et al. 2021).
4. Show non-IID results in the main text.
5. Report server-side computation time and acknowledge the O(d × m × βN) server cost.
6. Define the "Defendability" criterion.
7. Discuss what happens when the T×m < d bound is violated.
8. Consider extending the method to support multiple local steps (FedAvg-style).

## Score and Decision

**Calibration anchors:**

| Path | Avg Human Score | Round | Comparison |
|------|----------------|-------|------------|
| omrLHFzC37.md (DeComFL: zeroth-order dimension-free FL) | 6.25 | R1 | Most similar conceptually; also uses random projections for dimension-free FL communication. DeComFL has cleaner O(1) communication vs O(m), experiments on larger models, and does not overclaim privacy. FedMPDD is weaker — its privacy claims are unsupported and experiments are smaller scale. |
| BO3aRwGzq0.md (DINAR: privacy-preserving FL) | 5.00 | R1 | Also claims privacy without formal guarantees, was criticized for this and rejected (avg 5.00). FedMPDD has a similar vulnerability but a stronger algorithmic contribution, placing it slightly below. |
| ogIFNo2bQw.md (BiCompFL: bi-directional compression) | 4.80 | R1 | Compression FL paper rejected for incremental novelty. FedMPDD is more novel algorithmically, roughly comparable quality. |
| ZU42Wrcqfm.md (FedSMU: compression + generalization) | 5.75 | R2 | Rejected. Has stronger experiments than FedMPDD but less relevant method. |
| 0jmFRA64Vw.md (FedComLoc: compression + local training) | 3.00 | R1 | Incremental compression work scored low. FedMPDD is more novel. |
| LJULZNlW5d.md (Vanishing Privacy: GIA threat) | 3.00 | R2 | Gradient leakage paper, less directly comparable. |

**Round 1 bracket: [3.5, 5.0].** The paper sits between DeComFL (6.25) and FedComLoc (3.00) — more novel than FedComLoc but with weaker evidence than DeComFL due to overclaimed privacy and smaller experiments.

**Final score: 4.0 — borderline reject.**

The core algorithmic idea (multi-projected directional derivatives for FL gradient compression) is genuinely novel and the convergence theory is clean. However, the privacy claims — a central component of the paper's contribution ("Communication-Efficient and **Private** Federated Learning") — are significantly overclaimed and not well-supported. Lemma 2's bound can be vacuous for DNNs, no formal privacy definition is provided, and the empirical privacy evaluation lacks a controlled comparison at matched SSIM levels. Additionally, the experiments omit non-IID results and essential baselines for joint privacy+communication. These issues are major enough to recommend rejection in the current form, but the underlying algorithmic contribution has real merit and could be publishable with substantial revision focused on toning down the privacy claims and filling the experimental gaps.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>