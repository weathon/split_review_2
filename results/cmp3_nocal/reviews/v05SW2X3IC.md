Now let me produce the final consolidated review.

## Summary

This paper proposes a learnable three-channel (one common + two private) neural codec inspired by the Gray-Wyner Network for multi-task compression. It derives a loss function from information-theoretic principles (Theorem 2) to trade off transmit rate vs. receive rate, and bounds the two lossy common information notions (Wyner's C and Gács-Körner K) via interaction information (Theorem 1). Experiments span synthetic data, colored MNIST, Cityscapes, and COCO.

## Strengths

1. **Novel and well-motivated connection between Gray-Wyner theory and learned multi-task compression.** The paper correctly identifies that existing "coding for humans and machines" work assumes all task information is relevant to the reconstruction task, motivating the need for three separate channels (common + two private). This framing is principled and the transmit/receive rate tradeoff is clearly explained (Section 2.1, Figure 1).

2. **Theorem 1 extends a known lossless result to the lossy setting.** The bounds relating Wyner's and Gács-Körner common information via interaction information (Eq. 6-7) represent a genuine theoretical contribution. If the proof (Appendix A) holds, this formalizes the intuition that the gap between the two common information notions can be characterized in information-theoretic terms.

3. **Breadth of evaluation settings.** The experiments span synthetic data with known ground-truth statistics (Section 4.1), a controlled MNIST edge-case where mutual information between tasks is known analytically (Section 4.2), and two real-world vision benchmarks (Cityscapes, COCO; Section 4.3). The colored MNIST experiment in particular provides meaningful insight into how the method behaves when task dependence ranges from fully dependent to fully independent.

## Weaknesses

### Fatal

None.

### Major

1. **The architecture's common-information extraction mechanism is heuristic and not demonstrably connected to the theoretical common-information concepts that motivate the paper.** The common representation Y₀ is formed by element-wise matching of quantized features (Eq. 14): an element is retained iff the two branches produce identical values after quantization. An L2 penalty (Eq. 15) encourages the two branches to produce similar values. This mechanism does not correspond to any known definition of common information — Wyner's requires a random variable U making $\hat{Z}_1$ and $\hat{Z}_2$ conditionally independent (Eq. 3), and Gács-Körner involves a refinement of the sample space (Eq. 5). The paper provides no argument — theoretical or empirical — that the Y₀ produced by this mechanism satisfies the Markov conditions that define these quantities. The statement "If Theorem 1 holds with equality, an optimal codec optimized for β ∈ (1, 2) achieves both common information measures" (Section 3.2) explicitly refers to a theoretical optimal codec, not the proposed heuristic architecture, but this distinction is easily overlooked and the architecture section (§3.3) claims to be "grounded on the proposed objective function" without bridging the gap. This creates a disconnect between the theoretical apparatus (Sections 2.1, 3.1) and the actual method.

2. **The theoretical bounds from Theorem 1 are never computed or used in the experiments.** Theorem 1 bounds K and C via interaction information. The paper does not compute K, C, or the interaction-information bounds for any experiment — not even for the synthetic dataset where the ground-truth joint distribution is known (Section 4.1). Common-channel rates are compared against mutual information I(X₁;X₂), not against C or K. The entire theoretical contribution of Theorem 1 therefore stands apart from the empirical evaluation. This makes the paper feel like two parallel contributions (a theory result and an architecture) that do not engage with each other.

3. **Comparison against existing multi-task codecs is missing.** The related work (Section 2) explicitly cites multi-task learnable codecs (Chamain et al., 2021; Feng et al., 2022; Guo et al., 2024) and "coding for humans and machines" methods (Choi & Bajic, 2022; Foroutan et al., 2023; de Andrade & Bajic, 2024). None of these are compared against in the vision experiments. The paper dismisses the multi-task codecs with "their rate is optimal only when all the tasks involved are performed jointly" — but this also describes the Joint baseline used in the paper's own evaluation. If the claim is that the proposed three-channel separation is superior for the transmit-receive tradeoff, the evaluation should include methods designed for distributed settings. Without such comparisons, it is unclear what value the three-channel separation adds over existing shared-channel approaches.

### Minor

4. **Theorem 2's bridging step is not fully rigorous.** The transition from the conditional rate-distortion function $R_{X_1|Y_0}(D_1)$ (Eq. 9) to the conditional entropy $H(Y_1|Y_0)$ (Eq. 10) requires that the deterministic encoder $Y_1 = f_1(X_1)$ achieves the conditional rate-distortion optimum. The theorem assumes this via the existence condition ("there exists a $f_0, f_1, f_2, g_1$, and $g_2$ in their respective families that achieve $T$"), but the justification for why conditioning $Y_1$ on $X_1$ alone (without $Y_0$) is without loss of generality for the conditional rate-distortion function is not argued. The connection between the theoretical infimum and the practical loss (Eq. 12, β = 1/α) is conceptually clear but the logical chain has gaps that a reader working through the math will need to fill themselves.

5. **The headline BD-rate claim conflates "sharing" with "separation."** The paper's quantitative claim of "-81.58% BD-rate advantage in transmit rate, against single-task codecs" (§5) compares the proposed method (which shares information across tasks) against Independent (which does not share). For two tasks with non-zero mutual information, any method that shares information should outperform Independent on transmit rate — this is the premise of the multi-task compression literature, not a novel finding specific to this method. The more informative comparison is against Joint (single shared channel), where the proposed method's BD-rate advantage is positive (23.32% for Cityscapes, 13.16% for COCO), meaning Joint is actually better on transmit rate. The -81.58% figure is not clearly traced to specific tabulated numbers in the paper.

6. **Interaction information sign issue not addressed.** Theorem 1 uses $I(X_1, X_2; \hat{Z}_1; \hat{Z}_2)$ as a measure of interaction information. Multi-variable interaction information can be negative. The theorem's inequalities (K ≤ max I ≤ min I ≤ C) implicitly assume the quantity is well-behaved; the paper does not discuss whether the bounds hold when interaction information is negative or what interpretation to draw in that case.

7. **Synthetic data description (Section 4.1) is too terse.** The description of $\tilde{X}$ — "We created an $\tilde{X}$ such that $H(X_1, X_2) = 3.3$ bits per element, $H(X_1) + H(X_2) = 4.62$" — does not specify the sample space, the generative process, or how the linear regression targets are derived. The observation that β = 3/2 "performs marginally better than β = 1 and β = 2" in both transmit and receive rates (Section 4.1) is interesting but counterintuitive (a tradeoff parameter should be worse than each dedicated optimizer on its own metric); this is not discussed.

### Trivial

None.

## Nice-to-Haves

- Computing the interaction-information bounds from Theorem 1 for the synthetic dataset (where the joint distribution is known) and comparing the common-channel rate achieved to C and K would substantially strengthen the paper's theoretical narrative.
- Full raw rate-distortion curves for the vision experiments (already present as figures, but explicit operating-point tables would aid reproducibility).
- A discussion of the effect of specializing to X₁ = X₂ = X (single source) — which the paper notes in passing — on the generality of the Gray-Wyner formulation.

## Removed Points

The following points were identified in the input review but are removed (with justification):

- **"Theorem 2 is not properly justified"** — The reviewer's criticism overstates the issue. The paper explicitly states the assumptions (deterministic functions, richness of function families). The bridging step is standard in information-theoretic ML papers, though it could be clearer. Demoted to Minor weakness #4 above.
- **"Only BD-rate reported, not full rate-distortion curves"** — Contradicted by the paper: Figure 5 explicitly shows rate-accuracy curves (described as "two line graphs" in the figure caption).
- **"Why are task networks frozen? Training jointly would be more convincing"** — Freezing task networks is standard practice in compression papers to evaluate the codec rather than confounding task accuracy.
- **"X₁ = X₂ = X is a limitation not discussed"** — The paper explicitly states this specialization: "the proposed architecture specializes to a single source X, so that (X₁, X₂) = X" (Section 4).
- **"The claim that β=3/2 equally optimizes for both rates deserves a derivation"** — The reasoning (midpoint of β=1 and β=2) is self-evident from the description.
- **"Missing related works"** — Hard rule: cannot flag missing references without external verification.
- **"The notation I(X₁, X₂; Z₁; Z₂) is non-standard"** — This is a minor formatting variant; the paper cites Yeung (1991) for the definition.

## Novel Insights

None beyond the paper's own contributions. The review does not surface a novel perspective that the paper itself does not articulate.

## Suggestions

1. **Bridge the theory-architecture gap.** Either (a) redesign the common-information extraction mechanism to have a provable connection to Wyner's or Gács-Körner common information (e.g., by parameterizing a variational bound on the relevant Markov conditions), or (b) honestly reposition the paper as a practical heuristic instantiation of a Gray-Wyner-like architecture and de-emphasize the theoretical apparatus that does not constrain the design. Direction (b) would also require adding comparisons against existing multi-task codecs.

2. **Compute the Theorem 1 bounds at least on the synthetic dataset** to show whether the method is operating near the information-theoretic limits, and compare R₀ against C and K rather than only against I(X₁; X₂).

3. **Add comparisons against existing multi-task codecs** (Chamain et al., 2021; Feng et al., 2022; Guo et al., 2024) on at least one vision benchmark to demonstrate that the three-channel separation yields benefits over existing shared-channel approaches.

4. **Clarify the training-time behavior of Eq. 14.** Describe how the hard equality condition $\left[Y_0^{(1)}\right]_i = \left[Y_0^{(2)}\right]_i$ is evaluated before quantization (when the straight-through estimator produces continuous values in the backward pass but discrete in the forward pass).

5. **Trace the -81.58% BD-rate claim to specific numbers** in a table, and report the comparison against Joint (not just Independent) for this aggregate claim.

## Score and Decision

The paper addresses a genuine and interesting problem — separating common from private information in learned multi-task codecs — and provides a clean theoretical framing (Theorem 1 is a non-trivial extension) with broad evaluation. However, the paper suffers from a significant disconnect between its theoretical contributions and its practical architecture: the common-information extraction mechanism is a heuristic with no provable connection to the common-information concepts that motivate the work; the Theorem 1 bounds are never computed or used; and the empirical evaluation lacks comparisons against existing multi-task compression methods that the paper itself cites. These gaps prevent the paper from delivering on the promise of its framing. The direction is promising and the ideas merit further development, but the current execution does not warrant acceptance.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>