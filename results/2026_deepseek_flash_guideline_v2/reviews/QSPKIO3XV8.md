## Summary

This paper proposes "Dimension Domain Co-Decomposition (3D)", a PINNs framework that integrates dimension decomposition (using a shared MLP with indexed inputs to model per-coordinate factors) with MoE-based adaptive domain decomposition. It also introduces Variable Interpretability (VI), a subspace-alignment metric to quantify how well learned per-dimension components match ground-truth factors. Experiments on Poisson, Wave, Viscous Burgers, and Linear Transport equations show parameter efficiency and automatic shock detection.

---

## Strengths

- **Shared-MLP architecture yields substantial parameter savings in high dimensions (Table 1).** The shared MLP uses 5,392 parameters regardless of input dimensionality, while independent per-dimension MLPs grow linearly (e.g., 53,280 for 10d Poisson). This is a concrete architectural improvement over prior dimension-decomposition methods that assign separate networks per dimension. The advantage becomes more pronounced as dimensionality increases.

- **MoE-driven domain decomposition automatically identifies physical shock locations without predefined partitions (Section 4.3, Figure 4).** For Viscous Burgers, K=2 achieves ℓ₂ error 0.0011 versus 0.2108 for K=1 (no decomposition), and the router consistently places the partition boundary at the shock x=0. Consistency across five random seeds confirms the decomposition is driven by intrinsic PDE features rather than initialization artifacts.

- **VI metric provides a principled, quantitative subspace-alignment measure (Section 3.2).** VI uses column-wise normalization, QR decomposition, and singular-value-based subspace comparison to measure alignment between learned factor subspaces and ground-truth components. The metric is scale-invariant, bounded in [0,1], and goes beyond the qualitative visual inspection used in prior dimension-decomposition works.

- **Dimension expansion via fine-tuning (Section 4.2).** Because the separable (coordinate, index) parameterization does not depend on input dimensionality, a model trained on 5d Poisson can be fine-tuned on 8d Poisson. Standard MLP-based PINNs cannot do this due to mismatched input sizes.

---

## Weaknesses

### Major

- **No experimental comparison against the most directly relevant baselines.** SPINNs (Cho et al., 2023) is acknowledged in Section 3.1 as the closest predecessor for dimension decomposition but never compared experimentally — not on parameter count, accuracy, or training cost. Since SPINNs is the natural baseline for the dimension decomposition component, this omission makes it impossible to assess whether the shared-MLP indexing trick is actually beneficial or just trading one inductive bias for another. Similarly, XPINNs (Jagtap et al., 2020c) and APINNs (Hu et al., 2023) are discussed as related work for domain decomposition but are absent from the evaluation on Burgers and Transport. A comparison against "vanilla PINNs" and internal ablated variants (independent MLPs) is insufficient to establish that the proposed design constitutes an advance over existing specialized methods.

- **VI metric is only demonstrated on separable problems, leaving the "interpretability" claim only partially supported.** All test cases used for VI (Poisson, Wave equations) have fully separable analytical solutions where ground-truth factors are known analytically. The conclusion acknowledges that non-separable solutions would require constructing separable approximations (e.g., truncated Fourier series), but this procedure is never demonstrated or validated. For the non-separable Burgers and Transport problems, VI is not reported at all. The paper's headline claim of "solving PDEs with interpretability" is therefore only supported for the subset of PDEs with known separable structure. The paper also acknowledges (Section 3.2) that VI measures subspace *containment* (whether the predicted r-dimensional space contains the true s-dimensional subspace) rather than whether the model has identified the correct per-dimension functional forms — so VI=1 can be achieved with irrelevant extra dimensions when r > s.

### Minor

- **The high-frequency Wave equation case (c=10, Table 2) shows VI stagnates at 84.59% even with r=5**, with a standard deviation of 3.42%. The paper attributes this to known PINNs difficulty with high frequencies. This is an honest acknowledgement, but it implies that the interpretability the method promises degrades precisely when the PDE is hardest — a limitation that deserves more discussion about when the method can be relied upon.

- **The claim that dense MoE "avoids expert collapse and provides more stable training" (Section 3.3) is stated without supporting evidence.** No experimental comparison between dense and sparse gating is provided. Since this claim justifies a structural design decision, it should be empirically supported.

- **No hyperparameter sensitivity analysis** for the key knobs (rank r, number of experts K, shared MLP architecture, router architecture). Results use fixed settings; it is unclear how robust performance is to these choices, which matters for practical use of the method.

- **Training/inference cost comparison is limited.** Only one wall-clock time comparison is reported (10d Poisson: 1579s vs 1184s). For a method whose selling points include efficiency, runtime comparisons across multiple benchmarks would be informative.

### Trivial

None.

---

## Nice-to-Haves

- A comparison between dense and sparse MoE gating to validate the design choice.
- Hyperparameter sensitivity study for r and K across benchmarks.
- Demonstrate VI on at least one non-separable problem using the Fourier-series approximation mentioned in the conclusion.
- Wall-clock training times for additional benchmarks.

---

## Removed Points

These points from the Harsh Critic were removed with justification:

- **"APINNs already uses soft gating for domain decomposition — the paper's claimed benefit is what APINNs already offers."** Cannot be verified from the paper alone. The paper states APINNs uses soft gating but claims all existing approaches require predefined partitions. The core point about missing experimental comparison with APINNs is already covered under Major weakness 1.
- **"The 5d Poisson comparison stacks the deck (10-layer MLP vs 2-layer shared MLP)."** The 10d Poisson comparison uses comparable parameter counts (4,929 vs 5,392) and shows the same trends. The 5d comparison is a standard baseline demonstrating parameter efficiency, not a misleading comparison.
- **"The claim that shared MLP provides 'far more expressive representation' is imprecise."** Language nitpick that does not affect the paper's technical validity.
- **"The discussion of GAMs/NAMs/SINDy is tangential."** Organizational preference, not a substantive weakness.
- **"No discussion of training stability."** The paper does provide consistency analysis across seeds and robustness to noise.
- **"No justification for column-wise normalization in VI."** The normalization is defined; alternative choices could be explored but this is standard practice.
- **"The paper does not discuss expressivity implications of the shared MLP coupling."** A valid observation but more of a discussion suggestion than a weakness.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. Add SPINNs as a baseline for all Poisson and Wave experiments. This is the single most impactful addition — without it, the dimension decomposition contribution cannot be properly benchmarked.
2. Add APINNs or XPINNs as a baseline for the Burgers and Transport domain decomposition experiments.
3. Either demonstrate VI on a non-separable problem using the Fourier-series approximation mentioned in the conclusion, or explicitly scope the interpretability claim to separable solutions.
4. Report wall-clock training times for additional benchmarks beyond 10d Poisson.
5. Include a brief hyperparameter sensitivity analysis (varying r and K) for at least one benchmark.
6. Provide an ablation comparing dense vs. sparse MoE gating to support the claim that dense gating avoids expert collapse.

---

## Score and Decision

The paper presents a reasonable engineering contribution — a shared-MLP indexing trick for dimension decomposition, integration with MoE-based domain decomposition, and a new metric (VI) for factor interpretability. The individual components are sensible and the parameter efficiency advantage is clearly demonstrated.

However, the experimental evaluation has significant gaps. The most critical baselines (SPINNs for dimension decomposition, XPINNs/APINNs for domain decomposition) are absent, making it impossible to assess whether the proposed design advances over the state of the art. The VI metric's interpretability claim is only supported for separable solutions. These gaps mean the paper's core claims are not fully substantiated by the evidence presented.

The method's ideas are worth pursuing, but the paper in its current form does not provide sufficient evidence that they constitute a demonstrated advance over existing specialized methods. Major revision with proper baselines and a more complete evaluation would be needed.

**Calibration note:** The calibration search tool was unavailable due to a data path issue, so scoring is based on direct assessment of the paper's content and the severity of its evaluation gaps relative to standard ICLR quality expectations.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>