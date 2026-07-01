## Summary

This paper proposes FedMPDD (Federated Learning via Multi-Projected Directional Derivatives), which compresses each client's high-dimensional gradient by computing its directional derivatives along \(m \ll d\) random Rademacher vectors, reducing uplink communication from \(O(d)\) to \(O(m)\) per client. The server reconstructs a gradient estimate using the same random vectors. The paper's key insight is that averaging \(m\) projections overcomes the dimension-dependent convergence limitation of a single projection (which converges at \(O(d/\sqrt{K})\)), achieving \(O(1/\sqrt{K})\) convergence matching FedSGD. The paper further argues that the rank-deficient projection (\(\text{rank}=m \ll d\)) creates an unavoidable ambiguity in gradient reconstruction, providing inherent privacy against gradient inversion attacks. Empirical results on MNIST and CIFAR-10 show strong communication savings and low SSIM scores under gradient inversion attacks.

## Strengths

1. **Conceptually interesting privacy-from-compression framing.** The observation that random projection to \(m \ll d\) dimensions creates an underdetermined system (\(\mathbb{R}^m\) → \(\mathbb{R}^d\)) that fundamentally prevents unique gradient recovery is a genuinely distinctive way to think about privacy in gradient compression. The connection to the nullspace of the projection, formalized in Lemma 1 (expected relative gradient reconstruction error of \(\frac{d-1}{m}\)), is the paper's most novel conceptual contribution and contrasts with the conventional "compress first, then add noise" approach.

2. **Rigorous convergence theory.** Theorem 2 provides a clean \(O(1/\sqrt{K})\) convergence bound that explicitly separates the multi-projection distortion term (\(O(\epsilon G^2/\sqrt{K})\)) from standard optimization terms, grounded in the Johnson–Lindenstrauss lemma. The analysis is appropriately matched to the non-convex setting and the logarithmic dependence of \(m\) on \(d\) is well-motivated.

3. **Substantial empirical communication savings.** The reported compression ratios are genuine and striking (e.g., 356× reduction versus FedSGD on CIFAR-10 in Table 2). The SSIM values for FedMPDD (0.14–0.22) are meaningfully lower than those of uncompressed baselines like Top-k and lp-proj (0.74–0.91), and the qualitative GIA visualizations in Figure 2 provide intuitive support.

## Weaknesses

### Fatal
None.

### Major

1. **Defendability labeling is inconsistent and conflates design intent with measured outcome.** In Table 2, FedSGD+Laplace(var=10) achieves SSIM=0.23 and is marked ✗, while FedMPDD(m=2000) achieves SSIM=0.22 and is marked ✓. An SSIM difference of 0.01 cannot justify opposite categorizations. Since the paper uses SSIM as the privacy leakage metric throughout, labeling two methods with nearly identical SSIM values differently undermines the claim that FedMPDD's privacy protection is qualitatively superior to LDP's. The criteria for "Defendability" are never defined in the paper, leaving the reader to infer that the label reflects design intent rather than measured outcome — a circular argument.

2. **No comparison against methods that jointly pursue compression and privacy.** The paper cites Amiri et al. (2021) (DP + compression via universal vector quantization) and Lyu (2021) (1-bit compressor integrating DP) in the related work as the most closely related approaches, but does not include them or any comparable joint compression+DP method in the experiments. The paper compares against compression-only methods (Top-k, lp-proj, QSGD, SA-FedLora) that are not designed for privacy, and against LDP-only methods (FedSGD+Laplace) that are not compressed. The central claim — that FedMPDD achieves a superior joint trade-off — cannot be properly evaluated without the most directly relevant baselines.

3. **Multi-round privacy erosion is acknowledged but unaddressed.** Remark 2 states that privacy is guaranteed only when \(T \times m < d\) (where \(T\) is the number of rounds). For a moderate \(d \approx 300,000\) and \(m = 600\), this allows only 500 rounds — well below typical FL training horizons. The paper responds that "the natural evolution of gradients during training provides stronger practical protection" but provides no formal analysis, no empirical measurement of SSIM as a function of round count, and no mechanism (e.g., periodic basis refresh) to address erosion. This is a structural gap that directly concerns the method's practical applicability, not a minor limitation.

4. **Privacy claims extend beyond what the formal analysis supports.** The paper states that FedMPDD provides "inherent privacy against gradient inversion attacks" and "consistent privacy" because Lemma 1 gives a gradient reconstruction error of \((d-1)/m\) that is independent of gradient magnitude. However, the quantity that matters for data privacy is Lemma 2 (data reconstruction error), which has a lower bound proportional to \(\|\mathbf{g}\|^2 / L_v^2\) — it *does* depend on gradient magnitude and on the Lipschitz constant \(L_v\). The paper provides no estimate of \(L_v\) for any model used in the experiments, so the numerical privacy bound is uncalibrated. The "consistent privacy" claim conflates gradient reconstruction (which is indeed magnitude-independent) with data reconstruction (which is not). Additionally, the paper presents the privacy protection as an absolute property rather than a relative lower bound; a lower bound on reconstruction error is not equivalent to a formal guarantee like \((\varepsilon,\delta)\)-DP.

### Minor

1. **No direct round-efficiency comparison against unconstrained FedSGD.** The paper's convergence analysis suggests FedMPDD should converge at the same rate as FedSGD per round (up to an \(\epsilon\)-distortion term), but the experiments never directly compare the two in terms of accuracy-vs-rounds without communication budget constraints. The reader cannot assess whether the \(\epsilon\)-distortion is practically negligible or whether FedMPDD trades off more rounds for lower per-round cost.

2. **Non-standard communication cost formula.** Line 122 states that total communication cost is \(O(1/\sqrt{K} \times \beta N \times m)\). The \(1/\sqrt{K}\) factor appears to conflate the convergence rate with the number of rounds; total communication should scale with \(K\) (the number of rounds), not \(1/\sqrt{K}\). This appears to be a writing error that could mislead readers about the cost analysis.

3. **Lemma 2's Lipschitz constant \(L_v\) is not estimated.** The data reconstruction lower bound depends critically on \(L_v\) (the Lipschitz constant of the loss gradient with respect to the input). For deep neural networks, \(L_v\) can be very large, potentially making the bound vacuous. Without even a rough estimate for the models used, the privacy guarantee is uncalibrated.

### Trivial

1. **Assumption 1 is referenced in Theorem 2 but not characterized in the main text.** The step size formula uses \(L\) (suggesting \(L\)-smoothness), but a reader of the main text alone cannot determine what Assumption 1 entails, making it harder to assess the theorem's applicability.

2. **SSIM gap between MNIST (Figure 1: <0.04) and CIFAR-10 (Table 2: 0.14–0.22) is not explained.** The paper should clarify whether this reflects differences in model architecture, data complexity, or the \(m/d\) ratio.

## Nice-to-Haves

- **Accuracy-vs-communication Pareto curves** where all methods train to convergence and the x-axis is total bytes transmitted. This would show the real trade-off (accuracy per byte) without the "baselines can't start" framing.
- **SSIM as a function of training round number** to empirically characterize whether privacy erodes over time as \(T \times m\) approaches \(d\).
- **Sensitivity analysis over a wider range of \(m\) values** with practical guidance for choosing \(\varepsilon\) and \(\delta\) in the JL formula \(m = O(\ln(d/\delta)/\varepsilon^2)\).

## Removed Points

*(These points appeared in the input review but were removed for the reasons stated. They should be treated with caution.)*

- **"Fixed budget comparison is uninformative because baselines can't train."** — The comparison also includes compression baselines (Top-k, lp-proj, QSGD, SA-FedLora) that *do* train under the budget, against which FedMPDD achieves higher accuracy. The comparison is informative.
- **"Novelty overstated relative to random projection methods."** — The paper's characterization of existing methods as using "fixed, shared random matrices" cannot be reliably verified or refuted from the paper alone. The core technical contributions (privacy analysis, multi-projection averaging for convergence) retain value regardless of this positioning claim.
- **"Computational cost analysis calls JVP strategy a follow-up study."** — The appendix (removed by the parser) likely contained the evaluation; this criticism cannot be evaluated from the available main text.
- **"Unbiasedness of projected directional derivative for stochastic gradients is not addressed."** — The unbiasedness \(\mathbb{E}[\hat{\mathbf{g}}] = \mathbf{g}\) holds for any fixed gradient vector \(\mathbf{g}\) when \(\mathbb{E}[\mathbf{u}\mathbf{u}^\top] = I\) and \(\mathbf{u}\) is independent of \(\mathbf{g}\); the paper's use of independently generated Rademacher vectors satisfies this.
- **"How \(m\) was chosen is unclear."** — The paper explicitly states \(m = O(\ln(d/\delta)/\varepsilon^2)\) and refers to Table A.9 for a sensitivity range.
- **"Lemma 1 derivation of constant \((d-1)/m\) needs more detail."** — The paper explicitly chooses Rademacher vectors; the constant follows from standard variance calculations for this distribution.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Clarify Defendability criteria.** Either define the metric explicitly or apply the ✓/✗ labels consistently based on measured SSIM thresholds. Alternatively, remove the label entirely and let the SSIM values speak for themselves.
2. **Add at least one joint compression+DP baseline.** The paper itself identifies Amiri et al. (2021) and Lyu (2021) as the most relevant prior work on joint compression and privacy. Include them in the experiments under comparable communication budgets.
3. **Empirically characterize multi-round privacy.** Report SSIM as a function of training rounds (as already done in Figure 1 for MNIST, but extend to CIFAR-10 and explicitly comment on whether SSIM drifts as \(T\) approaches \(d/m\)).
4. **Calibrate the privacy claims.** Distinguish clearly between "inherent privacy" (which is a lower bound on reconstruction error) and formal differential privacy. Acknowledge that Lemma 2's bound depends on the unestimated \(L_v\). Replace absolute-sounding privacy language with relative, quantified statements.
5. **Fix the communication cost formula** on line 122 to reflect \(O(K \times \beta N \times m)\) or explain the intended derivation.
6. **Include an unconstrained accuracy-vs-rounds curve** comparing FedMPDD to FedSGD on the same architecture and task, so readers can assess the per-round convergence impact of the \(\epsilon\)-distortion term.

## Score and Decision

**Recommendation: Borderline Reject.** The core idea has genuine merit and the theoretical analysis is competently executed. However, the paper's empirical evaluation has significant gaps: the defendability labeling inconsistency, the omission of joint compression+DP baselines, the unaddressed multi-round privacy erosion, and privacy claims that overreach the formal analysis. These are structural weaknesses that affect the paper's central claims. The idea is worth developing, but in its current form the evidence does not reliably support the claimed advantages over reasonable alternatives.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>