## Summary

This paper introduces Proper Velocity Neural Networks (PVNNs), which leverage the Proper Velocity (PV) model—an unconstrained representation of hyperbolic space derived from special relativity—as a numerically stable alternative to the Poincaré ball and hyperboloid models for hyperbolic deep learning. The authors establish the complete Riemannian geometry of PV space (exponential/logarithmic maps, parallel transport, geodesic distance), develop core neural network building blocks (MLR, FC, convolutional, activation, and batch normalization layers) in this space, and demonstrate improved numerical stability and competitive performance across four experimental settings.

## Strengths

- **Novel exploration of an underexplored hyperbolic model**: The PV model has been largely absent from the machine learning literature, and this paper provides the first systematic treatment of its Riemannian geometry for representation learning, which is a genuine contribution.
- **Theoretical grounding**: The derivation of closed-form Riemannian operators (Theorems 4.3, 5.1-5.3) and the proof that the PV space is isometric to the Poincaré ball (Theorem 4.2) are mathematically sound and provide a principled foundation for the proposed layers.
- **Numerical stability advantages are convincingly demonstrated**: Table 1-3 provide clear evidence that PV operations are robust under large scalar multipliers and in high-precision settings where competing models produce NaN/Inf, gradient vanishing, or gradient explosion.
- **Practical architectural innovations**: The simplified parameterization of PV MLR (Theorem 5.2) that reduces complexity from gyro-additions to inner products and avoids Riemannian optimization, along with the PV FC layer, represent well-motivated contributions that address real computational bottlenecks.
- **Comprehensive empirical evaluation across diverse domains**: The paper tests on numerical stability, image classification, graph node classification, and genomic sequence learning—four distinct tasks that probe different aspects of the model—with consistent competitive results.

## Weaknesses

### Fatal

None.

### Major

- **Empirical gains are not dramatic and evaluation could be sharper**: While PVNNs achieve the best results in many settings, the improvements over strong baselines on core image classification tasks (Table 4) are modest (e.g., ~0.2% on CIFAR-10, ~0.2% on CIFAR-100). Given that PV MLR is theoretically motivated by numerical stability, the paper would benefit from experiments on tasks where the stability advantage directly translates to accuracy gains (e.g., training with deeper hyperbolic networks, low-precision training, or on datasets requiring extreme curvature).
- **Discrepancy in Cora results**: On the weakly hyperbolic Cora dataset, PVNN underperforms the LNN baseline (51.42 vs. 53.34), and this gap is not sufficiently discussed. If PV geometry is primarily beneficial for strongly hyperbolic data, this should be clearly stated as a limitation rather than presented as "comparable." The paper would benefit from a hypothesis about why PVNN struggles on near-Euclidean graphs.
- **Missing details on hyperparameter sensitivity**: The paper reports results with specific settings but does not analyze sensitivity to curvature parameter \(K\) across different tasks. Given that the curvature must be chosen or learned, the paper would benefit from a discussion or ablation on how performance varies with \(K\) for different datasets.

### Minor

- **Activation ablation (Table 9) shows inconsistencies**: On the Cora dataset, Euclidean activation degrades performance dramatically (38.10) compared to tangent activation (52.26), yet the paper does not discuss why direct PV-space activation would fail so severely on one dataset but be competitive on others. This suggests the unconstrained property may introduce instability for certain activation functions.
- **Efficiency comparison is limited**: The paper notes that PV GyroBN is computationally expensive (Table 7), but does not provide comparable wall-clock time comparisons for the full model training across models (PVNN vs. HNN vs. LNN). Without such data, it is difficult to assess the practical trade-off between the modest accuracy gains and computational cost.
- **Parallel transport formula (Equation 12) is complex**: It relies on Möbius gyration through the Poincaré ball, which somewhat undercuts the claim of having a self-contained Riemannian toolkit. The paper should clarify how this dependency is resolved in practice.

### Trivial

- The paper uses both \(K\) (curvature) and \(s\) notation but mainly uses \(K\); this is clear but the connection to the speed-of-light analogy could be made slightly more explicit.

## Nice-to-Haves

- An evaluation on low-precision (FP16/INT8) training regimes would strongly validate the numerical stability claims.
- A theoretical or empirical characterization of when the unconstrained nature of PV is most beneficial (e.g., when embeddings are far from the origin) would strengthen the contributions.
- A comparison of PVNN with other unconstrained hyperbolic models (e.g., Klein model if applicable) would better contextualize the results.

## Novel Insights

Beyond the paper's own contributions, a genuinely novel observation is that the unconstrained nature of the PV model not only provides numerical stability but also allows for "skipping" the exponential map when lifting Euclidean features to hyperbolic space (as shown in Tables 4 and 8). This suggests that for some architectures, the PV coordinates can be treated as a natural parameterization of hyperbolic space that aligns well with Euclidean optimization, blurring the boundary between Euclidean and hyperbolic representations in a way that constrained models cannot.

## Suggestions

- **Add a discussion of limitations**: Explicitly state that PVNN may not be advantageous on near-Euclidean datasets (like Cora) and suggest when practitioners should choose PV over Poincaré/hyperboloid.
- **Add a "computational cost" comparison**: Even a simple table showing training time per epoch for each full model (not just the normalization layer) would help readers assess the practical trade-off.
- **Include a sensitivity analysis on curvature \(K\)**: Show performance across a range of \(K\) values for at least one dataset to guide practitioners in hyperparameter selection.

## Score and Decision

This paper presents a well-executed, theoretically grounded contribution that introduces a meaningful alternative geometry for hyperbolic neural networks. While the empirical gains are solid but not transformative, the numerical stability improvements are clear, and the opening-up of PV space to the ML community is a valuable contribution that warrants acceptance.

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>