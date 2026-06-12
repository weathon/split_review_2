## Summary
This paper proposes a unified Dimension Domain Co-Decomposition (3D) framework that integrates dimension decomposition with Mixture-of-Experts (MoE) based domain decomposition for solving PDEs with PINNs. The contributions include: a shared-MLP architecture with indexed inputs for efficient per-dimension processing, a quantitative Variable Interpretability (VI) metric to measure alignment between learned latent representations and exact solution components, and an MoE-driven approach that automatically partitions the domain without predefined subdomains or interface conditions. Experiments on Poisson, Wave, Viscous Burgers, and Linear Transport equations demonstrate improved efficiency and accuracy over vanilla PINNs and independent MLP baselines.

## Strengths
- **Novel integration of dimension decomposition and adaptive domain decomposition** – Combining a shared-MLP per-index representation with MoE gating is a fresh and sensible design that addresses two separate limitations of PINNs in a single framework.
- **Parameter efficiency via shared MLP** – Processing all dimensions with one small MLP (by indexing coordinates) significantly reduces model size compared to independent per-dimension networks, with the advantage growing with dimensionality (e.g., 50% memory reduction for 5d Poisson, 30.4% for 10d).
- **Introduction of a quantitative interpretability metric (VI)** – The paper proposes a principled, scale-invariant metric based on subspace alignment to quantify how well learned per-dimension components match ground-truth factors, filling a gap in existing dimension decomposition methods that only provide qualitative inspection.
- **Automatic domain decomposition without manual partitions** – The MoE router learns soft domain boundaries automatically, eliminating the need for predefined subdomains, explicit interface penalties, or problem-specific tuning that plagues methods like XPINNs.
- **Good empirical accuracy on tested benchmarks** – Shared MLP achieves relative l2 errors of ~10⁻⁴ on 5d Poisson and ~10⁻³ on 10d Poisson, substantially outperforming vanilla PINNs (~10⁻²–10⁻¹). The viscous Burgers error drops from 0.21 (K=1) to 0.001 (K=2) when MoE is added.

## Weaknesses

### Fatal
None.

### Major
- **VI metric is only demonstrated on separable (product-form) PDE solutions**, where ground-truth factors are known analytically. The paper acknowledges this limitation and suggests using truncated Fourier approximations for non-separable cases, but no such experiment is performed. This severely limits the practical applicability of VI until its extension beyond separable problems is validated.
- **Lack of comparison to state-of-the-art domain decomposition and dimension decomposition methods** – No quantitative comparisons with SPINNs (for dimension decomposition) or XPINNs/APINNs (for domain decomposition) on the same benchmarks. The paper claims advantages over SPINNs (memory, MoE compatibility) but provides no direct accuracy or efficiency comparison. For Burgers, the improvement from K=1 to K=2 is shown, but how does this compare to XPINNs with a manual split at the shock? Without such baselines, the relative contribution of MoE over existing domain decomposition is unclear.
- **VI metric interpretation when s < r is incompletely discussed** – When the exact subspace has lower dimension than the predicted subspace (e.g., exact factor is 1D, predicted rank r>1), VI=1 only guarantees containment, not that the predicted components are individually aligned with the exact factor. The predicted components could be arbitrary linear combinations that still span the exact subspace, which undermines the claim of “interpretable per-dimension representations.” The paper should discuss whether additional constraints (e.g., orthogonality, positivity) are needed for true per-variable interpretability.
- **Experiments are limited to relatively simple, separable or quasi-1D PDEs** – Poisson (product of sines), Wave (product of sinusoidal functions), Burgers (one shock), Transport (diagonal stripes). Performance on genuinely high-dimensional, non-separable, or strongly coupled PDEs (e.g., Navier–Stokes, turbulence, diffusion-reaction with complex interactions) is not evaluated. It is unclear whether the dimension decomposition remains effective when solutions do not admit an approximate separable representation.

### Minor
- **No ablation on the router architecture or number of layers/width** – The router is a 5-layer MLP with width 64, but no study shows how router capacity affects domain partition quality or accuracy. Similarly, the shared MLP width and depth are fixed; no sensitivity analysis is provided.
- **Consistency across seeds is only qualitatively assessed** – Five seeds are used, and representative visualizations are shown in the appendix, but there is no quantitative metric (e.g., overlap of high-weight regions, variation of expert boundaries) to measure partition stability.
- **The claim that dense MoE avoids expert collapse and is more stable than sparse MoE is not supported** – No experiments or theoretical analysis compare dense vs sparse gating in this context. The statement about top-k gating causing instability near shocks is speculation.
- **No study on the sensitivity to the number of collocation points** – All experiments use fixed point counts; it is unclear how performance scales with data availability.
- **The paper states that the shared MLP “requires on average 77.8% of the memory compared to independent MLPs”** – This number is mentioned in the text but not shown in a table; the parameter counts in Table 1 already illustrate the trend, but memory reduction is a separate (and more relevant) metric and should be reported systematically.

### Trivial
- Minor wording: “Dense MoE” vs “dense MoE” is used inconsistently.
- Figure captions are duplicated (the LaTeX alt text appears twice in the extracted PDF).

## Nice-to-Haves
- Compare against XPINNs and SPINNs on the same benchmarks to establish relative performance.
- Demonstrate VI on a non-separable PDE solution using the proposed truncated Fourier approximation, validating its practical utility.
- Provide a quantitative measure of partition consistency across runs (e.g., pairwise intersection over union of high-weight regions for each expert).
- Ablate the number of experts K more systematically, showing error vs K curves with confidence intervals for all benchmarks.
- Test on a higher-dimensional problem with a solution that is not product-separable (e.g., 10D diffusion-reaction with nonlinear reaction term).

## Novel Insights
The core insight is that dimension decomposition (via a shared-MLP with index inputs) and adaptive domain decomposition (via MoE) can be combined into a single end-to-end framework, each solving a different limitation of PINNs. The variable interpretability metric offers a way to probe what each latent dimension has learned, moving beyond pure prediction accuracy toward model understanding. The automatic discovery of domain boundaries (e.g., the shock at x=0 in Burgers) without manual intervention is a particularly appealing property for problems where the solution structure is not known a priori.

## Suggestions
- Replicate the Burgers and Transport experiments with XPINNs (using the same network capacity and collocation points) and report the error before and after adding interface conditions, to isolate the benefit of the MoE-based automatic partitioning.
- Report VI for a non-separable test case by constructing ground-truth factors via truncated SVD or Fourier expansion of the reference solution, and discuss any degradation in interpretability.
- Include an ablation study on the effect of the number of collocation points (e.g., 2048, 8192, 32768) on the 5d Poisson problem to show robustness.
- Clarify in the paper why VI=1 with s<r is sufficient for interpretability—does it guarantee that each predicted dimension component can be associated with a unique physical factor (e.g., after some rotation or scaling)?
- Add a table showing memory (GPU RAM) and training time for shared MLP vs independent MLPs across all benchmarks.

## Score and Decision
The paper presents a novel, well-motivated framework that addresses real limitations of current PINN-based methods. The shared-MLP design and VI metric are useful technical contributions. However, the experimental evaluation lacks comparisons to existing specialized methods (SPINNs, XPINNs) and relies on PDE benchmarks that are either separable or have simple structure, leaving the generality of the approach unproven. The interpretability metric is only validated on separable solutions. Given these gaps, the paper makes a compelling but not yet fully supported case for broad adoption.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>