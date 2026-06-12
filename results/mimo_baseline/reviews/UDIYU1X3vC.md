## Summary

This paper introduces Proper Velocity Neural Networks (PVNNs), which leverage the Proper Velocity (PV) model from special relativity as an unconstrained alternative to the commonly used Poincaré ball and hyperboloid models for hyperbolic neural networks. The authors derive the complete Riemannian geometric toolkit for PV space (exponential/logarithmic maps, parallel transport, geodesic distance) and build fundamental neural network layers (MLR, FC, convolution, activation, batch normalization) in this geometry. Experiments across numerical stability, image classification, graph node classification, and genomic sequence learning demonstrate improved numerical stability and competitive or superior performance.

## Strengths

- **Complete and principled theoretical framework.** The paper systematically derives all Riemannian operators for PV space, establishing the full geometric toolkit needed for deep learning. The approach of leveraging the isometry between PV and Poincaré ball (Theorem 4.2) to transfer known results is elegant and mathematically sound. The connection between gyro operations and Riemannian operators (Theorem 4.4) further enriches the theoretical understanding.

- **Comprehensive neural layer design.** All major building blocks—MLR, FC, convolution, activation, and batch normalization—are carefully designed for PV space. The MLR formulation (Theorem 5.2) is particularly well-motivated: the authors show how a naive parameterization would require expensive gyroaddition producing large intermediate tensors, and their efficient parameterization via $(z_k, r_k)$ reduces this to matrix multiplication. The FC layer (Theorem 5.3) and GyroBN with homogeneity guarantees (Theorem 5.4) are similarly well-developed.

- **Thorough experimental evaluation with strong ablations.** The paper evaluates across four distinct tasks (numerical stability, vision, graphs, genomics), providing breadth. The graph learning ablations are especially thorough, comparing tangent vs. Riemannian constructions (Table 6), different batch statistics methods (Table 7), input embedding choices (Table 8), and activation strategies (Table 9). The numerical stability experiments (Tables 1-3) convincingly demonstrate PV's advantages: zero failure rates up to $r=1000$ in FP32, stable gradients, and negligible round-trip errors.

- **Strong practical performance on relevant benchmarks.** On strongly hyperbolic graph datasets, PVNN achieves significant improvements: Disease (81.15% vs. 80.57%), Airport (97.96% vs. 92.10%), and PubMed (74.33% vs. 73.68%). Genomic sequence learning shows substantial gains, with ~8 MCC point improvements on SINEs.

## Weaknesses

### Fatal

None.

### Major

- **The isometry result raises a fundamental question about the contribution's depth.** Theorem 4.2 establishes that PV space is Riemannian isometric to the Poincaré ball. This means the two models have identical representational capacity—the geometric information content is the same. The primary differentiator then becomes numerical stability from the unconstrained representation. While the stability evidence in Section 6.1 is compelling for individual operators, the paper does not demonstrate that this translates to better *training dynamics* in practice—e.g., showing training loss curves with fewer NaN occurrences, demonstrating that PVNNs are more robust to hyperparameter/learning rate choices, or reporting training stability rates across multiple runs. This is a missed opportunity to make the practical case more compelling.

- **Marginal improvements in image classification.** Table 4 shows improvements of roughly 0.2-0.4% on CIFAR-10 and CIFAR-100 over the best baseline (Lorentz MLR). Given that the PV and Poincaré models are isometric, these small differences likely arise from optimization dynamics rather than representational advantages. More discussion on why PV MLR would be easier to optimize would strengthen the argument.

### Minor

- **PV concatenation for convolution is defined as standard Euclidean concatenation.** While this is pragmatically sensible since PV space is unconstrained, it means the convolutional layer's receptive field construction doesn't respect the hyperbolic geometry in any meaningful way. The convolution operation is essentially Euclidean with a hyperbolic FC layer applied afterward. This somewhat limits the geometric novelty of the convolutional layer.

- **The Fréchet mean computation requires iterative solvers with tunable iterations.** Table 7 shows that performance on Cora varies substantially with the number of iterations (from 33.10% with tangent to 49.50% with 5 iterations), suggesting sensitivity to this hyperparameter. The paper acknowledges the computational overhead but doesn't provide guidance on how to choose this in practice.

- **Only one dataset in genomic learning and relatively simple architectures are evaluated.** The genomic experiments follow a prior work's setup exactly. While results are strong, evaluating on additional genomic tasks or with more complex architectures would strengthen the generality of the claims.

### Trivial

None.

## Nice-to-Haves

- Training stability experiments showing NaN/Inf occurrences during actual end-to-end training of Poincaré vs. Hyperboloid vs. PV networks, with varying learning rates and initializations, would powerfully demonstrate the practical advantage of the unconstrained representation.
- Wall-clock time comparisons between PVNN and competing hyperbolic networks across all tasks would help practitioners understand the practical tradeoffs.
- Analysis of how the curvature parameter $K$ affects PVNN performance would be valuable, especially given the physical interpretation of $1/\sqrt{-K}$ as a "speed of light" analog.

## Novel Insights

The paper's central novel insight is that the PV model from special relativity, despite being algebraically isomorphic and geometrically isometric to the Poincaré ball, offers a practically superior platform for hyperbolic neural networks due to its unconstrained representation. This is a genuine insight: the isometry means nothing is lost representationally, but the unconstrained parameterization eliminates boundary-related numerical issues. The demonstration that this property preserves stable gradients even under extreme operations (scalar multiplication up to $r=1000$) while both Poincaré and hyperboloid models fail is a compelling practical argument. Beyond the paper's own contributions, no additional novel insights emerge—the insight that geometric reparameterization can yield computational advantages while preserving mathematical structure is well-established, but the specific application to PV space and the thorough experimental validation are the paper's distinctive contributions.

## Suggestions

- Add training stability experiments: track and report NaN/Inf occurrences, gradient norms over training iterations, and convergence rates across multiple seeds for all three hyperbolic models on at least one task.
- Discuss the implications of the isometry more explicitly: clarify that the contribution is about *computational and optimization advantages* of the PV parameterization rather than new representational capacity, and frame this within the broader literature on reparameterizations that improve optimization (e.g., weight normalization, spectral parameterization).
- Provide practical guidance on choosing the number of Fréchet mean iterations, possibly by relating it to the dataset's hyperbolicity or by proposing an adaptive stopping criterion.
- Consider evaluating on larger-scale benchmarks (e.g., larger graph datasets, ImageNet) to demonstrate scalability of the unconstrained formulation.

## Score and Decision

The paper makes a solid contribution by introducing a new geometric model to hyperbolic deep learning with a complete theoretical toolkit and reasonable experimental validation. The theoretical framework is rigorous, the layer designs are well-motivated, and the experiments span diverse domains. The main concern is that the isometry to Poincaré ball means the representational contribution is fundamentally about numerical stability and optimization ease rather than new geometric expressiveness, and the paper could do more to demonstrate these practical benefits in training dynamics. The image classification improvements are marginal, though graph and genomic results are more convincing. Overall, this is a well-executed paper with clear utility for the hyperbolic deep learning community.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept