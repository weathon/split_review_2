Now let me write the final review:

## Summary
This paper introduces Proper Velocity Neural Networks (PVNNs), which use the unconstrained Proper Velocity (PV) model from special relativity as an alternative coordinate system for hyperbolic neural networks. The paper derives the complete Riemannian toolkit for PV space via an isometry with the Poincaré ball, builds neural network layers (MLR, FC, convolution, activation, batch normalization), and evaluates them across four tasks: numerical stability, image classification, graph learning, and genomic sequence learning.

## Strengths
- **Compelling numerical stability evidence (Tables 1-3):** PV maintains zero failure rate up to r=1000 in FP32 while the hyperboloid reaches 100% failure (Table 1); PV round-trip error is 2.1×10⁻⁷ vs Poincaré's 2.1×10⁻⁴ and hyperboloid's 1.0 (Table 2); PV gradients stay in [10⁻⁶, 10⁻⁴] while Poincaré vanishes to [10⁻¹³, 10⁻¹¹] and hyperboloid explodes to NaN (Table 3). This multi-faceted stability evaluation directly validates the core motivation.

- **First complete Riemannian toolkit for PV space:** Theorem 4.2 proves Riemannian isometry with the Poincaré ball; Theorems 4.3 and 5.1 derive all essential operators (exponential map, logarithmic map, parallel transport, geodesic distance, point-to-hyperplane distance) in closed form, extending the PV model from algebraic (gyrovector) to full Riemannian treatment.

- **Efficient MLR parameterization (Theorem 5.2):** The reformulation in Eq. 19 reduces computation from explicit gyroaddition (producing b×C×n intermediate tensors) to standard matrix multiplication via inner products ⟨x, z_k⟩, with a clear Euclidean limit as K→0⁻.

- **Competitive results across four diverse tasks:** PVNN achieves best or near-best results on image classification (Table 4), graph learning (Table 5, best on 3/4 datasets with +5.86% on Airport), and genomic sequence learning (Table 10, best on all 5 TEB tasks including ~9 MCC point improvement over HCNN-S on SINEs).

- **Comprehensive ablation studies (Tables 6-9):** Systematic ablations on tangent vs Riemannian FC/BN, Fréchet iteration count, Exp₀ lifting, and activation type provide useful practical insights.

- **GyroBN theoretical guarantees (Theorem 5.4):** Proves translational homogeneity of the Fréchet mean and scaling homogeneity of dispersion, guaranteeing correct normalization — a theoretical grounding that many prior Riemannian normalization methods lack.

## Weaknesses

### Fatal
None.

### Major
- **Framing conflates isometric geometry with computational representation:** Theorem 4.2 proves PV and Poincaré spaces are Riemannian isometric — same distances, geodesics, curvature, and expressiveness. Yet the paper oscillates between calling PV "an alternative representation of hyperbolic geometry" (line 44) and "a stable alternative geometry for HNNs" (line 15), and claims "PV geometry is more effective on strongly hyperbolic graphs" (line 307). Since PV and Poincaré are isometric, performance differences arise from finite-precision optimization dynamics in different coordinate systems, not geometric expressiveness. The paper should explicitly frame the contribution as a superior computational/numerical representation of the same geometry.

- **Large performance gaps on graph learning are unexplained:** On Airport, PVNN achieves 97.96% vs HNN++'s 88.40% (Table 5) — a ~10-point gap between mathematically isometric models. The paper states "all models share the same architecture" and "differ only in the underlying hyperbolic model" (line 305), but offers no analysis of why this gap exists. Without training loss curves, gradient norm analysis, or hyperparameter sensitivity studies, the reader cannot assess whether this gain is robust or an artifact of implementation/tuning differences.

### Minor
- **Tangent-space ablations show mixed results for Riemannian construction:** Table 6 shows PV FC does not consistently outperform tangent-space FC (TFC): TFC beats PV FC on Cora (53.58 vs 52.26) and PubMed (74.40 vs 74.16). The claim that Riemannian PV layers are "especially" effective "in strongly hyperbolic settings" (line 309) doesn't cleanly map to δ-hyperbolicity scores — PubMed (δ=3.5) shows essentially no advantage while Disease (δ=0) and Airport (δ=1) do.

- **Fréchet ∞ underperforms Fréchet 10 iterations in Table 7:** On Disease, Airport, and PubMed, the theoretically correct Fréchet ∞ row produces lower accuracy than Fréchet 10 iterations (e.g., 71.16 vs 74.34 on PubMed). This counterintuitive result may indicate convergence issues or implicit regularization from early stopping, but the paper does not discuss it.

- **No wall-clock computational cost comparison against baselines:** PV FC involves sinh⁻¹ and cosh operations (Eq. 22), and GyroBN requires a Fréchet mean solver. Table 7 provides some GyroBN timing, but a direct wall-clock comparison of PVNN vs Poincaré/Hyperboloid baselines during full training would be informative given the paper's practical efficiency argument.

## Nice-to-Haves
- Training loss curves for PVNN vs baselines on Airport to explain the large accuracy gap
- Analysis of whether baselines experience numerical issues during training (connecting Section 6.1 stability experiments to actual NN training)
- Discussion of when PV is unnecessary or harmful (e.g., on Cora where results are mediocre)
- Gradient norm monitoring during training to validate that stability advantages translate to training dynamics

## Removed Points
These points are flagged to be removed, treat them with caution:
- Any criticism about missing appendix content (parser strips appendices; they exist in original)
- Any criticism about formatting, typos, or notation artifacts (parser issues)

## Novel Insights
The paper's most novel insight is that the unconstrained PV parameterization provides dramatically better numerical stability than both the Poincaré ball and hyperboloid models (Tables 1-3), with round-trip errors 1000× lower than Poincaré and 10⁷× lower than hyperboloid in FP32. The connection between PV gyrovector algebra from special relativity and modern deep learning infrastructure, while not deeply substantive from a physics perspective, motivates a genuinely useful mathematical framework. The efficient MLR reformulation (Theorem 5.2) that reduces gyroaddition to matrix multiplication is a practical contribution that makes PV space viable for large-scale applications.

## Suggestions
- Reframe the contribution explicitly as a computational representation advantage, not a new geometry. This strengthens the paper by making claims precise and defensible.
- Add optimization dynamics analysis (training curves, gradient norms) on Airport to explain the ~10% gap vs HNN++.
- Add a direct wall-clock comparison of PVNN vs Poincaré/Hyperboloid baselines.
- Discuss the Fréchet ∞ vs Fréchet 10 underperformance in Table 7.

## Reporting

**All anchors retrieved:**
| Anchor Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| HVT (Hyperbolic Vision Transformer) | 3.40 | R1 | Weak hyperbolic vision paper; PVNN clearly stronger |
| Riemannian Optimization for Hyperbolic Prototypical Networks | 4.25 | R1 | Rejected, unclear novelty; PVNN substantially stronger |
| Optimizing Learning for Robust Hyperbolic Deep Learning | 4.40 | R1 | Rejected, weaker evidence; PVNN stronger |
| Binary Hyperbolic Embeddings | 4.50 | R1 | Less rigorous; PVNN stronger |
| Fully Hyperbolic CNN (HCNN) | 6.00 | R1 | Very similar topic, accepted; PVNN has stronger math, more tasks, better stability |
| Neural networks on Symmetric Spaces | 6.00 | R1 | Unified framework, accepted; PVNN has more compelling stability focus |
| Fast Hyperboloid Decision Trees | 6.60 | R1 | Novel algorithm, accepted; comparable contribution scope |
| Magnitude Invariant Parametrizations | 6.25 | R1 | Less directly relevant (hypernetworks) |
| Compositional Entailment Learning for Hyperbolic VL | 8.00 | R1 | Large-scale VL, stronger breadth; above PVNN |

**Round 1 bracket: 5.5–7.0.** PVNN is clearly above the 6.00 anchors (HCNN had weaker math, smaller margins, fewer tasks) but below 8.00 anchors (broader impact, no framing issues). The mathematical toolkit, numerical stability evidence, and comprehensive ablations place it above the 6.0 HCNN paper. The isometry framing issue and unexplained graph learning gaps prevent it from reaching the 7.5+ range.

**Final score: 6.5**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>