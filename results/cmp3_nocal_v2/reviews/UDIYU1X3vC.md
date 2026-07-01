## Summary

This paper introduces Proper Velocity Neural Networks (PVNNs), a new framework for hyperbolic neural networks based on the Proper Velocity (PV) model — an unconstrained representation of hyperbolic space originating in special relativity. The authors derive the complete Riemannian toolkit (exponential/logarithmic maps, geodesic distance, parallel transport) for the PV space, building it through an isometry with the Poincaré ball. They then develop fundamental neural network layers (MLR, FC, convolutional, activation, and batch normalization) in PV space and evaluate across four tasks: numerical stability, image classification, graph node classification, and genomic sequence learning.

---

## Strengths

1. **Genuinely novel and practically useful representation.** Hyperbolic neural networks overwhelmingly use the Poincaré ball or hyperboloid (Lorentz) models. The PV model is genuinely underexplored in ML, and its unconstrained nature (PV space = ℝⁿ) eliminates the need to enforce manifold constraints during optimization (e.g., clipping to stay within the Poincaré ball). The paper provides the first complete Riemannian toolkit for this space (Exp, Log, parallel transport, geodesic distance), which is a nontrivial and useful contribution (Sections 3–4).

2. **Elegant theoretical derivation via isometry.** Theorem 4.2 establishes that PV and the Poincaré ball are Riemannian isometric. The paper leverages this isometry productively: instead of deriving PV Riemannian operators from scratch, it pulls them through from the known Poincaré operators. This is clean and avoids reinventing the wheel (Section 4.1–4.2).

3. **Strong empirical results on two of four tasks.** On the Airport graph dataset, PVNN outperforms the strongest baseline by 5.86 percentage points (97.96 vs. 92.10, Table 5). On the SINEs genomic dataset, PVCNN improves over HCNN-S by ~9 MCC points (Table 10). These are large, practically meaningful improvements on tasks where prior hyperbolic networks already work well.

4. **Practical MLR and FC formulations.** The final parameterization of PV MLR (Theorem 5.2, Eq. 19) avoids the expensive gyroaddition-over-classes bottleneck, reducing computation to a matrix multiplication. This is a real engineering contribution that makes the method scalable (Section 5.1).

5. **Comprehensive ablation study.** Tables 6–9 systematically ablate tangent vs. Riemannian layers, batch statistics approximations, activation choices, and the exponential map lifting. These help isolate where the PV formulation matters (Section 6.3).

---

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Framing overstates geometric novelty relative to the isometry.** The paper acknowledges the isometry between PV and the Poincaré ball (Theorem 4.2) and uses it productively to derive operators. However, the framing language — "new alternative geometry" (abstract, contributions), "stable alternative geometry" (Section 1) — could lead readers to expect a fundamentally different geometric structure with different expressive properties. PV is not a new geometry; it is a new *coordinate chart* of the same hyperbolic geometry. The genuine advantage is *numerical* (unconstrained → no boundary instabilities, better gradient behavior), which is real and practically important. The paper should make this distinction clearer in the abstract and introduction. (Evidence: Abstract, lines 9, 15, 24.)

2. **Numerical stability claims should calibrate the contrast with Poincaré more precisely.** Table 1 shows that on the gyro-operator test, PV and the Poincaré ball both achieve 0% failure at all radii — the hyperboloid model is the one that fails. The real numerical advantage of PV over Poincaré appears in Tables 2 (Exp/Log round-trip error) and 3 (gradient behavior), where PV shows smaller errors and more stable gradients. This is a genuine but more modest improvement over Poincaré. The paper's narrative ("unconstrained representation that alleviates numerical instabilities") is not wrong, but it slightly overdraws the contrast with Poincaré without distinguishing which instability affects which model. (Evidence: Tables 1–3; lines 15, 237.)

3. **The very large accuracy gap on Airport (5.86 points over KNN, ~11 points over tangent-space FC) lacks a mechanistic explanation.** Gaps of this magnitude are uncommon in graph node classification. The paper's ablations (Table 6) confirm the gap persists, showing PVNN at 97.93 vs. PVNN+TFC at 86.99. The paper attributes the gap to the effectiveness of PV geometry in strongly hyperbolic settings, but provides no training curves, convergence analysis, or controlled hyperparameter search to rule out that the tangent-space FC baseline is simply undertuned for this dataset. A dedicated analysis (e.g., demonstrating that the TFC baseline cannot close the gap with additional tuning, or that gradient behavior during training differs substantially) would significantly strengthen this result. (Evidence: Tables 5–6; lines 307–309.)

4. **PV GyroBN's practical value is unclear from the evidence.** Table 7 shows that Fréchet-based GyroBN (10 iterations) achieves the best accuracies but is 2–3× slower than Tangent or Euclidean approximations. On Disease and PubMed, the improvements over cheaper Tangent/Euclidean variants are marginal (~0.1–0.5 points), while on Cora, Fréchet 10 iter has high variance (±5.45). The paper notes the tradeoff in one sentence ("more computationally expensive," line 357) but does not contextualize whether the accuracy gains justify the cost. The practical recommendation for practitioners is ambiguous. (Evidence: Table 7; lines 357–358.)

### Trivial
- Table 5 notation: The PV column uses $\mathbb{P}V_K^n$ while Poincaré rows use $\mathbb{P}_K^R$ and hyperboloid uses $\mathbb{H}_K^R$. The $n$ vs $R$ notation is inconsistent.

---

## Nice-to-Haves

- **Test whether the performance gap between PVNN and Poincaré-based networks closes with FP64 training.** If the gap persists in FP64, it would suggest the advantage is not purely numerical, strengthening the case for a geometric/architectural benefit. If the gap closes, it would confirm that the advantage is primarily numerical stability, which is itself a valuable finding.
- **Report gradient norms during actual training** (not just on the synthetic $f_r$) to tie the theoretical stability claim directly to the empirical accuracy differences.
- **Curvature sensitivity analysis.** All experiments use $K=-1$ (standard in prior work). A brief discussion or sensitivity study would confirm robustness.
- **Variance for Tables 2–3.** Reporting standard deviations for the round-trip error and gradient magnitude would help assess whether the PV advantage over Poincaré is systematic.

---

## Removed Points

- **"Failure rate conflates two failure modes"** — Removed because the paper *does* separate them. The failure rate tracks NaN/Inf, and the violation rate (reported separately) tracks off-manifold points. The critic misread the text. (Evidence: lines 235–236.)
- **Generic framing criticisms not anchored to specific sentences** — Removed per filtering discipline.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. **In the abstract and introduction, explicitly state** that PV is isometric to the Poincaré ball and that the contribution is a new *coordinate representation* with superior numerical properties (unconstrained domain, better gradient behavior), not a fundamentally different geometric structure.
2. **Add a dedicated analysis or discussion of the Airport gap** — even a brief paragraph showing that the tangent-space baseline was reasonably tuned and cannot close the gap, or that gradient norms during training differ substantially between PV and TFC.
3. **Clarify the practical recommendation for batch normalization**: under what circumstances should practitioners use the full Fréchet-based GyroBN versus the cheaper Tangent/Euclidean approximations?

---

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>