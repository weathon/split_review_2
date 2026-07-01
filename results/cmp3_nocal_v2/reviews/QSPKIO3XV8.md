## Summary

This paper proposes 3D (Dimension Domain Co-Decomposition), a PINNs-based framework that combines (i) a shared-MLP dimension decomposition that processes coordinate-index pairs to reduce parameters compared to per-dimension MLPs, (ii) a Variable Interpretability (VI) metric that quantifies alignment between learned per-dimension representations and ground-truth factors, and (iii) a MoE-driven domain decomposition that automatically partitions the domain without predefined subdomains or interface conditions. Experiments on Poisson, Wave, Viscous Burgers, and Linear Transport equations demonstrate parameter savings and accuracy improvements, with the 10d Poisson result being a standout.

## Strengths

- **Parameter efficiency of the shared MLP architecture (Table 1).** The shared MLP with indexed inputs reduces parameters from 53,280 to 5,392 in the 10d Poisson case (~10× reduction). This is cleanly documented, scales with dimensionality, and is supported by memory measurements (30.4% of baseline memory for 10d).

- **The 10d Poisson result is genuinely strong.** With matched parameter counts (5,392 for shared MLP vs. 4,929 for vanilla PINN), the shared MLP achieves ℓ2 error of 1.25×10⁻³ in 11,500 epochs vs. 1.29×10⁻¹ in 31,500 epochs — an order-of-magnitude improvement. This convincingly demonstrates that the separable inductive bias helps in high dimensions.

- **Domain decomposition visualizations are informative.** Figures 4 and 5 show that the MoE router learns domain partitions aligned with physical features (the shock at x=0 in Burgers, diagonal stripes in Transport) without manual guidance. This qualitatively validates the automatic decomposition claim.

## Weaknesses

### Major

- **No quantitative comparison against existing domain decomposition PINNs.** The paper's narrative in Section 2.2 explicitly contrasts 3D with XPINNs, cPINNs, APINNs, and BPINNs, arguing that these methods require manual partitions and interface conditions. Yet the evaluation never compares 3D's accuracy against *any* of these methods on the same problems. For Burgers, the paper reports ℓ2 of 0.0011 (K=2) and 0.0008 (K=3) but gives no reference point from XPINNs with a manual partition at x=0. Without this comparison, the central claimed advantage of "automatic vs. manual decomposition" cannot be evaluated — the reader cannot tell whether the automatic approach is an improvement, a regression, or roughly equivalent. This is not a missing baseline among many; it is a gap in the evidence chain for a core claim.

### Minor

- **VI metric demonstrated only on trivially separable problems.** The paper presents VI as "a novel, quantitative, scale-invariant metric to evaluate dimension-wise interpretability" and lists it as one of three key innovations. However, VI is only computed on problems whose analytical solutions are products of univariate functions (Poisson: ∏ sin(πxᵢ); Wave: sin(πx)cos(cπt)). For Burgers and Transport — the problems with the most interesting solution structure — VI is not reported. The Conclusion acknowledges the limitation, but the metric's practical value as a general interpretability tool for PDE solving is limited to cases where a separable reference solution is available. This narrow scope should be reflected earlier in the paper (abstract/intro) rather than only in the conclusion.

- **Burgers and Transport results lack external baselines.** For Burgers (the primary domain decomposition showcase), there is no comparison against a standard PINN baseline or any other numerical method. The K=1 (ℓ2=0.2108) vs. K=2 (ℓ2=0.0011) within-method comparison shows that MoE helps, but it does not show how 3D compares to existing approaches. Similarly, the Transport results focus on qualitative visualizations with no reported error numbers or baselines.

- **Incomplete argument for SPINNs incompatibility with MoE.** The paper states (line 80) that SPINNs' forward-mode AD is "not directly compatible with MoE because the router breaks the…" — and the argument is cut off by a page break. This is a central technical differentiator that should be argued clearly in the main text rather than truncated.

- **Inconsistency in expert width across problems.** Burgers uses hidden layer width 32 while Poisson/Wave use width 64 (line 119 vs. line 174). The paper does not explain or justify this discrepancy, leaving it unclear whether the Burgers results could be improved with a wider configuration.

- **Transport uses different rank r for different K.** For Transport, r=4 with K=3 and r=8 with K=4. This confounds the effect of increasing experts with the effect of increasing rank.

### Trivial

- **Scalar index encoding for high dimensions.** The shared MLP uses scalar indices (0, 1, …, d−1) to distinguish dimensions. For d=10, these span less than a decade numerically. The paper does not discuss whether this encoding is sufficient or whether higher-dimensional embeddings would be beneficial. (Empirically it works, making this a presentation gap rather than a substantive one.)

- **VI normalization sensitivity (Eq. 5).** The normalization divides by max(√(Σ(F_{qk}−μ_k)²), ε) with ε=10⁻¹². The paper does not discuss numerical stability when columns have very small but non-zero variance.

## Nice-to-Haves

- An ablation of MoE with a standard dense MLP (no dimension decomposition) on Burgers would isolate the benefit of the "co-decomposition" claim beyond the K=1 vs. K=2 comparison already present.
- Comparing against SPINNs' accuracy on problems beyond Poisson (e.g., the 2d Wave equation) would strengthen the dimension decomposition evaluation.
- A discussion or brief experiment comparing dense vs. sparse MoE routing would substantiate the claim that dense MoE avoids expert collapse near shocks.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"No ablation isolating the combined framework"** (partial overstatement). The Burgers experiments already provide an ablation: K=1 (dimension decomposition without MoE, ℓ2=0.2108) vs. K=2 (combined, ℓ2=0.0011). The missing reverse ablation (MoE with standard MLP) is captured above as a Nice-to-Have.
- **"No comparison to SPINNs on accuracy"** (partially inaccurate). Figure 2 and the 5d/10d Poisson experiments do compare the shared MLP against independent per-dimension MLPs (the SPINNs architecture) on accuracy. The paper could extend this to more problems, but it is not entirely absent.
- **"5d Poisson parameter mismatch of roughly 8×"** (overstated). The 10d Poisson comparison uses matched parameter counts (4,929 vs. 5,392) and shows the same qualitative result, demonstrating that the advantage is not an artifact of capacity mismatch.
- **"VI interpretation of intermediate values unclear"** (partially addressed by the paper). The paper explains the subspace-containment interpretation and that VI=1 means the predicted subspace contains the exact subspace. Intermediate values follow naturally from this framing.
- Formatting/style nitpicks and speculative reproducibility concerns.

## Novel Insights

None beyond the paper's own contributions. The reviewer correctly identifies the shared-MLP parameter efficiency and the 10d Poisson result as the strongest elements, and the lack of comparison to prior domain decomposition methods as the most significant gap — these observations align with a careful reading of the paper rather than introducing new analytical angles.

## Suggestions

1. **Compare against XPINNs (or APINNs) on Burgers.** This is the single most impactful experiment the paper could add. If 3D (K=2, automatic) matches or exceeds XPINNs (2 subdomains, manual partition at x=0) in accuracy, the "automatic decomposition" claim is substantially validated.
2. **Report a vanilla PINN baseline for Burgers and Transport** so readers have an external reference point.
3. **Complete the SPINNs forward-mode AD argument in the main text** — this is a short technical paragraph and should not be deferred.
4. **Acknowledge VI's scope earlier** (abstract or introduction) rather than only in the conclusion, to align claims with demonstrated evidence.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>