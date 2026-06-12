## Summary

This paper proposes Dimension Domain Co-Decomposition (3D), a PINNs-based framework that unifies dimension decomposition (via a shared MLP processing coordinate-index pairs) with Mixture-of-Experts-driven automatic domain decomposition. The paper also introduces Variable Interpretability (VI), a metric quantifying alignment between learned per-dimension components and ground-truth factors. Experiments on Poisson, Wave, Burgers, and Linear Transport equations demonstrate parameter efficiency, interpretability on separable solutions, and automatic domain partitioning near shocks.

## Strengths

- **Clean architectural idea with parameter efficiency**: The shared MLP with indexed inputs (coordinate value + dimension index) is a simple and effective design that reduces parameters significantly — e.g., from 53,280 to 5,392 for 10D Poisson (Table 1) — while maintaining comparable accuracy to independent MLPs. This is a practical contribution for scaling dimension decomposition.

- **Automatic domain decomposition without predefined regions**: The MoE router learns soft domain partitions end-to-end, recovering physically meaningful boundaries (e.g., the shock at x=0 in Burgers, diagonal stripes in Linear Transport) without manual specification or interface loss terms. The visualizations in Figures 4 and 5 convincingly show that the learned partitions align with solution structure.

- **Interpretable component learning demonstrated visually**: Figure 3 showing the progressive learning of f_t(t) and f_x(x) for the Wave equation provides compelling qualitative evidence that the dimension decomposition captures physically meaningful factors, with the slower learning of higher-frequency temporal components consistent with known PINN behavior.

## Weaknesses

### Fatal

None.

### Major

- **No comparison with existing methods**: The paper does not compare against any baseline dimension decomposition method (SPINNs, CP-Net, etc.) or domain decomposition method (XPINNs, cPINNs, APINNs) on the same benchmarks. The claim that 3D "improves both computational efficiency and solution accuracy" is unsupported without such comparisons. This is the most critical gap — without baselines, the reader cannot assess whether the contributions actually advance the state of the art.

- **Experiments limited to trivially separable solutions**: All benchmark solutions are dimension-separable products of single-variable functions (e.g., u = ∏ sin(πx_i) for Poisson). This is the easiest possible setting for dimension decomposition and does not test the method's ability to handle solutions with cross-dimensional interactions, which the paper itself acknowledges are "often intrinsic to PDE solutions." The 10D Poisson with a separable solution is not a convincing high-dimensional benchmark.

- **VI metric requires separable ground truth**: The authors acknowledge this limitation in the conclusion, but it is severe — for most real-world PDEs, the exact solution is not available in separable form, making VI inapplicable without constructing approximate separable factors. This undermines the paper's claim of providing "quantitative interpretability" as a general tool.

### Minor

- **Domain decomposition experiments are only 1D+time**: The Burgers and Transport equations are 2D (t, x) problems. For a paper emphasizing high-dimensional PDEs, demonstrating MoE-driven domain decomposition on at least a 2D spatial problem would be important.

- **Sensitivity analysis is limited**: The paper does not analyze sensitivity to router initialization, the effect of the number of collocation points on decomposition quality, or how the method performs when the solution structure is not cleanly separable into subdomains.

- **Wall-clock training time not reported**: While parameter counts and memory are compared, actual training times for achieving target accuracy are not systematically reported, making efficiency claims incomplete.

### Trivial

- The claim that "the shared MLP design significantly reduces the number of trainable parameters compared with independent MLPs design" is somewhat obvious since a single shared network has fewer parameters than d independent networks by construction.

## Nice-to-Haves

- Comparison with SPINNs and XPINNs/APINNs on the same benchmarks with the same collocation budgets
- Experiments on non-separable high-dimensional PDEs (e.g., 20D+ problems from the literature)
- Analysis of what happens when the solution is not separable — does the decomposition still produce useful components?
- Ablation on the router architecture complexity and its effect on decomposition quality

## Novel Insights

The observation that MoE gating weights can serve as automatic domain partitioners for PINNs — recovering physically meaningful boundaries without interface conditions — is a genuinely useful insight. The paper demonstrates this convincingly for the Burgers shock and Transport equation stripes, suggesting that the router learns to route based on solution structure rather than arbitrary spatial splits. However, this insight is somewhat limited by the simplicity of the test cases.

## Suggestions

- Add direct comparisons with SPINNs (Cho et al., 2023) and APINNs (Hu et al., 2023) on the same benchmarks to substantiate efficiency and accuracy claims.
- Test on at least one non-separable high-dimensional problem (e.g., a 20D+ parametric PDE or a PDE with cross-dimensional coupling) to demonstrate that the method goes beyond the trivially separable case.
- Report wall-clock training times alongside parameter counts to give a complete picture of computational efficiency.

## Score and Decision

The paper presents a clean framework with some appealing design choices (shared MLP, automatic MoE decomposition), but the experimental evaluation is insufficient to support the claims. The complete absence of comparisons with existing methods, combined with benchmarks limited to trivially separable solutions, makes it impossible to assess whether 3D actually advances the state of the art. The VI metric, while conceptually interesting, is limited to separable settings. These are significant gaps that prevent acceptance at a top venue.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>