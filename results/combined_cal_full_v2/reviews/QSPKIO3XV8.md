## Summary

This paper proposes Dimension Domain Co-Decomposition (3D), a unified PINNs-based framework that combines (1) a shared-MLP dimension decomposition that processes coordinate-index pairs to decouple high-dimensional inputs, (2) a Variable Interpretability (VI) metric that quantifies alignment between learned per-dimension components and ground-truth factors via subspace alignment, and (3) an MoE-driven adaptive domain decomposition that automatically partitions the solution domain without predefined subdomains or interface conditions. Experiments on Poisson, Wave, Viscous Burgers, and Linear Transport equations demonstrate parameter efficiency and accuracy improvements.

## Strengths

- **Shared-MLP with indexed inputs (Section 3.1, Table 1).** Collapsing per-dimension MLPs into a single shared MLP by appending a dimension index is clean and practical. Parameter counts independent of input dimension (5,392 for both 5D and 10D Poisson) are a real improvement over naive per-dimension approaches, well-demonstrated in Table 1. This design is genuinely more parameter-efficient than the per-dimension MLP architectures used in prior separable PINN methods.

- **Variable Interpretability metric (Section 3.2, Equations 5–6).** The subspace-alignment formulation (QR decomposition followed by SVD of Q_F^T Q_G, with VI defined as mean squared singular value) is mathematically principled — scale-invariant, bounded in [0,1], and correctly handles cases where the learned rank r exceeds the ground-truth rank s. The metric fills a genuine gap in the literature, as prior dimension decomposition methods (SPINNs, etc.) lacked any quantitative interpretability measure for per-dimension components.

- **MoE-driven automatic domain decomposition (Section 3.3, Figures 4–5).** The router cleanly separates the Viscous Burgers domain along the shock at x=0 without predefined partitions or interface conditions. The ℓ2 error drops from 0.2108 (K=1, no decomposition) to 0.0011 (K=2), convincingly demonstrating the benefit of adaptive domain decomposition. The visual results (Figure 4) show that the learned partitions align with physically meaningful features.

- **Consistency and robustness evaluation (Section 4.3).** The paper tests the MoE domain decomposition across five random seeds and under up to 5% Gaussian noise, showing that the learned partitions are driven by intrinsic geometric features rather than initialization artifacts. This is good experimental practice that strengthens confidence in the method.

## Weaknesses

### Fatal
None.

### Major

- **Missing domain decomposition baselines (XPINNs, APINNs).** The paper discusses XPINNs, APINNs, and related methods at length in Section 2.2, criticizing their reliance on predefined subdomains and interface conditions. Yet the MoE experiments (Viscous Burgers, Linear Transport) compare only against K=1 (no decomposition). Without knowing what accuracy XPINNs or APINNs achieve on the same problems — especially on Viscous Burgers where the shock location is known a priori — the claim that the MoE approach is "better" or "more effective" is unsupported. A single quantitative table comparing ℓ2 errors of XPINNs or APINNs against 3D on the Burgers problem would substantiate the claimed advantage.

- **VI metric's limited practical utility is not demonstrated beyond toy problems.** The paper acknowledges (lines 208–209) that VI "relies on reference solutions that are dimension-separable" and suggests truncated Fourier series as a workaround for non-separable solutions. However, this workaround is never demonstrated on any problem where the solution is genuinely unknown — the very setting where interpretability is most needed. As presented, VI functions as a diagnostic for problems with known closed-form separable solutions, which is a narrower contribution than the abstract and introduction suggest. Demonstrating VI on even one problem without a known closed-form solution (using the suggested Fourier-series approximation) would substantially strengthen the claimed utility.

- **The "co-decomposition" claim is not validated on any problem requiring both mechanisms simultaneously.** The paper separates its evaluation: dimension decomposition is tested on Poisson/Wave (high-dim, smooth solutions, single expert, no MoE), while MoE domain decomposition is tested on Burgers/Transport (2D problems where dimension decomposition is not the primary challenge). No experiment combines high dimensionality (e.g., ≥5D) with sharp features (shocks, discontinuities) that would exercise both components jointly. The unified framework is presented as a key contribution (title, abstract, contribution list), yet the experiments never test it as a unified whole under conditions where both mechanisms are needed.

### Minor

- **SPINNs comparison is acknowledged but not directly engaged.** The paper states (line 80) that the architecture is "related to" SPINNs and claims advantages. The "independent MLPs" baseline tested in Table 1 and Figure 2 is architecturally equivalent to SPINNs' per-dimension MLP approach, and the shared MLP shows competitive accuracy with fewer parameters. However, the paper does not engage with SPINNs' forward-mode AD strategy or discuss whether the claimed advantages hold against the full SPINNs method. Explicitly labeling the independent-MLPs baseline as "SPINNs-style per-dimension decomposition" and addressing the forward-mode AD difference would clarify the comparison.

- **10D Poisson baseline comparison reflects inductive bias, not unique innovation.** The 10D Poisson problem has a perfectly separable product-of-sines solution. The comparison against a vanilla 4-layer MLP (1.25e-3 vs 1.29e-1, lines 139–140) primarily reflects the inductive bias that any separable architecture (including SPINNs) would have for this problem, not a unique advantage of the shared-MLP design. This does not invalidate the result, but contextualizing it against another separable baseline would make the comparison more informative.

### Trivial
None.

## Nice-to-Haves
- The "memory" savings claim (line 126: "77.8% of the memory") could be clarified as parameter count ratio vs. actual GPU memory consumption during training.
- The observation that VI for the high-frequency Wave cases (c=5, c=10) degrades with increasing frequency raises the interesting question of whether VI is measuring interpretability or simply convergence for that frequency component. The paper's spectral-bias explanation is plausible, but a brief discussion of this relationship would strengthen the presentation.

## Removed Points
- "No comparison against SPINNs invalidates the claimed advantage" (from Critical): Demoted after verifying that the independent-MLPs baseline is architecturally equivalent to SPINNs' per-dimension MLPs. The comparison does exist, just not under the SPINNs label.
- "10D Poisson comparison stacks the deck" (from Critical): Demoted to Minor because the paper fairly compares models with comparable parameter counts and is testing its own method, not claiming a universal result. The criticism about inductive bias is valid but not fatal.
- "VI measuring interpretability vs convergence" (Section 4.2 question): Removed as speculative — no evidence is provided that VI is redundant with ℓ2 error.
- Formatting/style nitpicks and section-by-section presentation notes: Removed per filtering rules.
- The paper's section notes about "memory claims unclear" and "VI ambiguity on s < r case": Removed — the paper is sufficiently clear on these points.

## Novel Insights
None beyond the paper's own contributions. The reviewer analysis does not surface a genuinely novel observation about the method or results that the paper itself does not already articulate.

## Suggestions
1. Add at least one existing domain decomposition method (XPINNs or APINNs) as a baseline on the Viscous Burgers problem to support the claimed advantage over methods requiring predefined partitions.
2. Demonstrate VI on a problem without a known closed-form separable solution using the suggested Fourier-series approximation, to show the metric works in settings where interpretability is most needed.
3. Add a single experiment combining high dimensionality (e.g., 5D or 10D) with sharp features that require domain decomposition, to substantiate the "co-decomposition" claim.
4. Label the "independent MLPs" baseline as a SPINNs-style per-dimension decomposition and briefly discuss the forward-mode AD difference.

---

**Calibration report.** All retrieval rounds:

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| DimOL | hghJJJUJJR.md | 3.00 | R1 | Yes | Weaker: negligible improvement, poor theoretical grounding. 3D has clear motivation and demonstrable gains. |
| Hybrid Numerical PINNs | R5FzCFR5yU.md | 3.33 | R1 | No | Different topic (hybrid numerical differentiation). Less relevant. |
| EPINN | SYiOxXWlKU.md | 2.50 | R1 | No | Single-layer PINN for stiff ODEs. Less relevant, lower quality. |
| In-Context Neural PDE | fzZfju8y0g.md | 3.40 | R1 | No | Transformer-based PDE adaptation. Different approach. |
| Ensemble/MoE DeepONets | BvMuyqPvk1.md | 4.33 | R1, R2 | Yes | Comparable: both use MoE for PDEs; weaknesses about missing baselines similar, but 3D has stronger empirical gains. |
| M²M | MUL7tKvNei.md | 4.00 | R1 | Yes | Weaker: unsupported claims, incorrect error dynamics. 3D has sounder theory. |
| HyResPINNs | 5rfj85bHCy.md | 5.00 | R1, R2 | Yes | Most similar in quality: comparable novelty and experimental rigor; both have limited baselines. |
| GP-PDE (high-freq) | q4AEBLHuA6.md | 5.75 | R2 | Yes | Stronger: broader experiment suite, fewer missing baselines; accepted at ICLR. |
| Connecting Solutions PINNs | Q9OGPWt0Rp.md | 5.25 | R2 | No | Meta-learning PINNs; different focus. |

**Bracket placement.** Round 1 established 4.0–6.0 as the plausible range (weaker than GP-PDE at 5.75, stronger than M²M at 4.00). Round 2 narrowed to 4.5–5.5, anchored on HyResPINNs (5.00) which has comparable strength and weakness profiles. The paper's strongest items (shared-MLP design: w=10.37, robustness evaluation: w=9.67) are competitive with HyResPINNs' top items (w≈10–12), while its weakest items (missing domain decomposition baselines: w=-2.75, VI limitation: w=-2.46) are similar in severity to HyResPINNs' weakest items (no cost comparison: w=-1.65, incremental novelty: w=-3.56). The paper sits slightly below the GP-PDE paper (5.75, accepted) because that paper's weaknesses are about missing citations and presentation, whereas this paper's weaknesses concern missing experimental baselines — a more substantive gap.

**Final score:** 5.0 — borderline reject. The paper has genuine and well-motivated contributions, but the evaluation does not yet support the level of claim made in the title and introduction. The missing baselines (domain decomposition methods, demonstration of VI in non-separable settings, unified co-decomposition experiment) are addressable in revision.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>