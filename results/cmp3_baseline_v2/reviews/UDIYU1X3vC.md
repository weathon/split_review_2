## Summary
This paper introduces Proper Velocity Neural Networks (PVNNs), which leverage the unconstrained Proper Velocity (PV) model of hyperbolic geometry as an alternative to the widely-used but numerically unstable Poincaré ball and hyperboloid models. The authors derive the complete Riemannian geometry of PV space, develop core neural network layers (MLR, FC, convolutional, activation, and batch normalization) in this geometry, and empirically demonstrate improved numerical stability along with competitive or superior performance on image classification, graph node classification, and genomic sequence learning tasks.

## Strengths
- **Novel and timely contribution**: The PV model has been largely unexplored in machine learning. This paper provides the first systematic treatment of PV space for deep learning, including all essential Riemannian operators and neural network layers. This opens a genuinely new direction for hyperbolic representation learning.
- **Complete theoretical foundation**: The authors rigorously derive closed-form expressions for the exponential map, logarithmic map, geodesic distance, parallel transport, and prove that the PV model is isometric to the Poincaré ball (Theorem 4.2) and that gyro operations can be expressed via Riemannian operations (Theorem 4.4). The MLR and FC layers are accompanied by clean, simplified parameterizations (Theorems 5.2, 5.3) that avoid costly per-class gyroaddition.
- **Comprehensive experimental validation**: The paper evaluates PVNNs across four distinct tasks—numerical stability, image classification, graph node classification, and genomic sequence learning—with thorough ablations on tangent-space vs. Riemannian layers, activation variants, normalization strategies, and input embedding choices. The numerical stability experiments (Tables 1–3) convincingly demonstrate that PV avoids both gradient vanishing (Poincaré) and gradient explosion (hyperboloid).
- **Practical impact**: The unconstrained nature of PV space offers genuine numerical advantages, especially for FP32 training and large-radius operations, which is relevant for scaling hyperbolic networks in practice.

## Weaknesses
### Fatal
None.

### Major
None.

### Minor
- **Modest performance gains in some settings**: On image classification (CIFAR-100), PV MLR achieves 78.20% vs. 77.96% for the best baseline—a small improvement. On the weakly hyperbolic Cora graph, PVNN underperforms the hyperboloid baseline (51.42 vs. 53.34). While not invalidating the contribution, these results weaken the claim of universal superiority.
- **Practical value of GyroBN is unclear**: The Fréchet-based GyroBN requires iterative solvers and is slower than tangent or Euclidean variants, yet accuracy differences are often small (Table 7). The theoretical homogeneity guarantee is nice, but the practical advantage over faster approximations is not strongly demonstrated.
- **Limited baselines for genomic sequence learning**: Only one hyperbolic baseline (HCNN-S) and one Euclidean CNN are compared (Table 10). Additional hyperboloid or Poincaré convolutional baselines would strengthen the evidence for PVCNN’s benefits in this domain.

### Trivial
- The paper uses both "GyroBN" and "PV GyroBN" interchangeably, which is fine but could be streamlined.

## Nice-to-Haves
- Provide a discussion of when the Fréchet GyroBN is practically worth the extra cost vs. tangent/Euclidean approximations.
- Extend the numerical stability experiments to include mixed-precision training (FP16/BF16), which is increasingly common in practice.
- Include runtime comparisons of the full PV forward/backward pass against Poincaré/hyperboloid baselines across all tasks to quantify the speed-stability trade-off.

## Novel Insights
The core insight is that the Proper Velocity model—rooted in relativistic proper velocity—provides an unconstrained hyperbolic representation that maintains the algebraic structure of gyrovector spaces while avoiding the numerical pathologies of bounded or constrained models. This is not merely a technical trick: it reveals that the choice of hyperbolic model matters for numerical stability independently of the underlying curvature geometry, and that an isometrically equivalent model (PV is isometric to Poincaré) can have dramatically different practical behavior. The elegant parameterization of MLR (Theorem 5.2) that avoids explicit gyroaddition and reduces to Euclidean MLR in the limit \(K\to 0^-\) is a clean demonstration of how algebraic structure can be exploited for computational efficiency.

## Suggestions
- For the genomic sequence experiments, include additional hyperbolic convolutional baselines (e.g., from the hyperboloid model) and report statistical significance tests to better support the claim that PVCNN outperforms.
- Add a runtime comparison (forward + backward) for PV vs. Poincaré vs. hyperboloid models on a representative task to help practitioners assess the practical overhead.
- Discuss the limitations of the PV model more explicitly: e.g., the gyro formulas are more complex than Möbius operations, and the Fréchet mean requires an iterative solver even for the Poincaré ball.

## Score and Decision
The paper makes a substantial theoretical contribution by establishing the Riemannian geometry of the PV model and developing a complete set of neural network layers. The experimental evidence convincingly demonstrates the numerical stability advantage and shows competitive or superior performance on multiple tasks. The minor weaknesses do not undermine the core claims. This is a strong paper that will be of significant value to the community.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>