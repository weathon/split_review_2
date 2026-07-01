## Summary

The paper proposes Dimension Domain Co-Decomposition (3D), a PINNs-based framework that integrates dimension decomposition (via a shared MLP with indexed inputs) with Mixture-of-Experts (MoE) driven domain decomposition. It introduces Variable Interpretability (VI), a metric that quantifies alignment between learned per-dimension latent representations and ground-truth solution factors. Experiments on Poisson, Wave, Viscous Burgers, and Linear Transport equations show that 3D improves parameter efficiency, accuracy, and provides interpretable decompositions without requiring predefined subdomains or interface conditions.

## Strengths

- **Novel combination of dimension decomposition and MoE domain decomposition.** The paper unifies two complementary strategies—coordinate-wise factorization and adaptive domain partitioning—in a single end-to-end trainable framework. This is a sensible and well-motivated design that addresses limitations of prior work (e.g., SPINNs lack domain adaptivity; XPINNs require manual partitions).
- **Shared MLP architecture for dimension decomposition.** Using a single MLP that takes coordinate-index pairs as input reduces the parameter count significantly compared to independent per-dimension MLPs, especially as the input dimension grows. The empirical parameter and memory savings (Table 1, memory reduction to 30.4% in 10d Poisson) are clear and practically valuable.
- **Variable Interpretability (VI) metric.** VI provides a principled, scale-invariant way to measure how well the learned subspace of each dimension component aligns with the ground-truth factor subspace. The use of QR decomposition and singular values of the cross-gram matrix is technically sound and yields a value in [0,1] that is easy to interpret.
- **Automatic domain decomposition via dense MoE.** The router learns soft partitions without requiring predefined subdomains or explicit interface loss terms. The visualizations for Viscous Burgers (Figure 4) and Linear Transport (Figure 5) convincingly show that the learned partitions align with salient solution features (shock location, diagonal stripes), and the error drops dramatically when going from K=1 to K=2 (from 0.21 to 0.0011).
- **Consistency and robustness experiments.** The paper reports results across multiple random seeds and under noisy initial/boundary conditions, demonstrating that the learned decompositions are driven by intrinsic solution geometry rather than initialization artifacts.

## Weaknesses

### Major

1. **VI metric is limited to dimension-separable reference solutions.** The paper acknowledges this limitation but it is a fundamental restriction. VI requires ground-truth factors that are separable per dimension (e.g., product of univariate functions). For general PDE solutions that are not separable, the authors suggest constructing separable approximations (e.g., truncated Fourier series), but this is not evaluated or validated. Without a practical way to apply VI to non-separable problems, the interpretability claim is significantly weakened for many real-world PDEs.

2. **Comparison with relevant baselines is incomplete.** The paper compares against vanilla PINNs and independent MLPs, but does not directly compare against state-of-the-art decomposition-based PINN methods such as SPINNs (Cho et al., 2023) for dimension decomposition or XPINNs/APINNs (Jagtap et al., 2020; Hu et al., 2023) for domain decomposition. The paper claims advantages over these methods (e.g., SPINNs cannot easily integrate with MoE; XPINNs require manual partitions), but without quantitative comparisons on the same benchmarks, it is unclear whether 3D actually outperforms them in accuracy or efficiency.

3. **The MoE-driven domain decomposition is not entirely novel.** Soft gating for domain decomposition in PINNs has been explored in APINNs (Hu et al., 2023), which also uses a gating network to assign weights to subdomain experts. The paper cites APINNs but does not clearly differentiate its approach beyond noting that APINNs still require predefined subdomains. However, APINNs also learn the gating weights automatically. A more detailed discussion of the differences and an empirical comparison would strengthen the novelty claim.

### Minor

- The experiments are conducted on relatively low-dimensional problems (up to 10d Poisson, 2d Wave). While the paper claims to address high-dimensional PDEs, the highest dimension tested is 10, which is still moderate. The parameter reduction advantage of the shared MLP is clear, but the scalability to truly high dimensions (e.g., 50 or 100) is not demonstrated.
- The paper uses a dense MoE (all experts are always active) rather than sparse MoE. The justification (avoiding expert collapse, stability near shocks) is reasonable, but dense MoE incurs higher computational cost as K grows. The paper does not report training time or FLOPs for the MoE experiments, making it hard to assess the trade-off.
- The VI metric is computed using the learned components from the dimension decomposition inside each expert. However, when multiple experts are used (e.g., Burgers, Transport), the final prediction is a weighted sum of expert outputs. It is unclear how VI is computed in that setting—does the paper compute VI per expert or for the aggregated prediction? The description in Section 3.2 and the experiments in Section 4.2 focus on single-expert cases (Poisson, Wave). The paper should clarify whether VI is applicable in the MoE setting and how it is computed.

### Trivial

- The paper states that the shared MLP design reduces memory to 77.8% on average, but the exact calculation of this number is not explained. It would be helpful to specify whether this refers to peak memory during training or model storage.

## Nice-to-Haves

- An ablation study on the effect of the number of experts K on both accuracy and training time would be useful. The paper shows that K=2 is sufficient for Burgers, but does not provide a systematic way to choose K_optimal.
- The paper could discuss the computational overhead of the router and whether the MoE structure introduces additional training instability (e.g., load balancing issues).
- A comparison of VI with other interpretability metrics (e.g., feature importance, sensitivity analysis) would help contextualize its value.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Provide quantitative comparisons with SPINNs and APINNs on the same benchmarks to substantiate the claimed advantages.
- Extend the VI metric to non-separable solutions by demonstrating the proposed Fourier-series approximation on a concrete example (e.g., a PDE with a known non-separable solution).
- Clarify how VI is computed when multiple experts are used, and report VI values for the MoE experiments (Burgers, Transport) if applicable.
- Include training time and memory usage for the MoE experiments to allow a fair assessment of the efficiency-accuracy trade-off.

## Score and Decision

The paper presents a well-motivated and technically sound framework that combines dimension decomposition with MoE-based domain decomposition. The shared MLP design and the VI metric are useful contributions. However, the limited applicability of VI to separable solutions and the lack of direct comparisons with relevant baselines (SPINNs, APINNs) weaken the overall impact. The paper is a solid incremental contribution but does not yet demonstrate a clear advantage over existing methods in a comprehensive evaluation.

MY FINAL SCORE: 6.0</score>  
MY FINAL DECISION: Accept</decision>