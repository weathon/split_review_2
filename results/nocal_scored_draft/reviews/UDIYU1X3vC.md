Now let me compose the final review based on the calibrated signals.

## Summary

This paper introduces Proper Velocity Neural Networks (PVNNs), a new framework for hyperbolic deep learning based on the Proper Velocity (PV) model from special relativity. The authors derive the complete Riemannian toolkit (exponential/logarithmic maps, geodesic distance, parallel transport) for PV space via its isometry to the Poincaré ball, and develop practical neural layers (MLR, FC, convolution, activation, batch normalization) that operate entirely in PV space. Unlike the bounded Poincaré ball and constrained hyperboloid, PV space is unconstrained ($\mathbb{R}^n$ as a set), which the paper argues offers better numerical stability. Experiments across numerical stability, image classification, graph node classification, and genomic sequence learning demonstrate that PVNNs are competitive with or outperform existing hyperbolic models.

## Strengths

- **Complete Riemannian toolkit for a new hyperbolic model:** The paper derives closed-form expressions for the exponential map, logarithmic map, geodesic distance, and parallel transport on PV space (Theorem 4.3), and proves the isometry between PV and the Poincaré ball (Theorem 4.2). The derivation via isometry (Sec 4.1–4.2) is mathematically clean and provides a foundation that did not previously exist in the ML literature.

- **Practical layer designs with efficient parametrizations:** The MLR (Theorem 5.2) and FC layer (Theorem 5.3) are reduced to inner-product forms (Eq. 19, 22) that avoid expensive per-class gyroaddition and can be implemented as standard matrix multiplications. The contrast between the naive gyro-vector form (Eq. 18) and the closed-form (Eq. 19) demonstrates real practical thinking.

- **Thorough evaluation breadth:** The paper evaluates across four distinct tasks (numerical stability, vision, graphs, genomics) with ablations for activations, normalization strategies, tangent-space alternatives, and the Exp₀ lifting. This goes beyond what is typical for hyperbolic method papers.

- **Honest about the isometry:** The paper transparently establishes that PV is isometric to the Poincaré ball (Theorem 4.2) and frames the contribution around numerical stability rather than representational superiority. This is the correct framing and avoids overclaiming.

## Weaknesses

### Fatal
None.

### Major

- **The central narrative — that PV's numerical stability drives downstream accuracy gains — is only partially supported by the evidence.** In the gyro operator experiment (Tab. 1), the Poincaré ball shows zero failure rate and zero violation rate at all radii up to 1000, which undercuts the claim that PV primarily addresses instabilities that plague the Poincaré ball. The large downstream gap on Airport (PVNN 97.96% vs HNN++ 88.40%, a 9.56-point gap) lacks a direct mechanistic explanation linking gradient stability (Tab. 3) to accuracy — e.g., monitoring gradient/feature norms during training or showing training collapse in Poincaré baselines. The paper would be strengthened by either tempering the numerical-stability→accuracy narrative or providing mechanistic evidence for it.

- **No computational cost comparison for the main experiments.** PV operations involve `sinh`, `sinh⁻¹`, and `tanh⁻¹` — transcendental functions that differ from the Poincaré ball's equivalents. Tab. 7 reports timing only for PV GyroBN variants, but there is no end-to-end training/inference time comparison for PVNN vs HNN/LNN/KNN on the graph tasks (Tab. 5) or PVCNN vs HCNN-S on genomics (Tab. 10). Given the paper frames PV as a practical alternative, this is a gap.

### Minor

- **The genomic sequence learning comparison (Tab. 10) states PVCNN uses a single curvature shared for all layers, but does not specify whether the HCNN-S baseline uses per-layer curvatures.** If HCNN-S uses a more flexible per-layer curvature setup, this asymmetry could affect the comparison. This detail should be clarified.

- **The paper lacks an explicit limitations section.** Important limitations worth acknowledging include: (a) PV is isometric to the Poincaré ball, so there is no representational advantage — the practical benefit is limited to numerical stability; (b) Tab. 1 shows the numerical stability advantage is primarily vs the hyperboloid, not vs the Poincaré ball; (c) PV gyro formulas still involve `sinh`/`sinh⁻¹` which can overflow for extreme values.

### Trivial
None.

## Nice-to-Haves
- Provide mechanistic evidence for the Airport result: monitor gradient norms or feature norms during PVNN vs baseline training, or show that Poincaré baselines suffer training collapse that PV avoids.
- Add a limitations paragraph to the conclusion.

## Removed Points
These points were considered but removed with justification:
- **No code release:** Removed per guidelines — criticisms questioning the release status of cited entities should not be included.
- **KLMN baseline needs more description:** Minor presentation point; the Klein ball baseline is cited with a reference, sufficient for a main conference paper.
- **Hyperparameter fairness concern about missing appendix details:** The paper defers experimental details to App. C (stripped by the parser). Per guidelines, missing appendix content should not be held against the paper.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Provide mechanistic evidence linking PV's numerical stability to the large downstream gains on Airport — e.g., monitoring gradient norms or feature norms during training across hyperbolic models.
2. Add an end-to-end timing comparison (training time per epoch or total) for PVNN vs baseline hyperbolic models on at least one task.
3. Add a limitations paragraph to the conclusion, acknowledging the points listed in Minor weaknesses above.
4. Clarify the curvature setup (per-layer vs single curvature) of the HCNN-S baseline in the genomics experiments.

## Score and Decision

The paper makes a genuine contribution: a complete Riemannian toolkit for an underexplored hyperbolic model, practical layer designs that are genuinely more efficient than naive gyro-vector implementations, and broad experimental coverage. The theoretical foundation is clean and the framing is appropriately honest about the isometry to the Poincaré ball. However, the central empirical narrative — that numerical stability drives large downstream accuracy gains — is not as cleanly supported as the paper suggests; Tab. 1 shows Poincaré is equally stable in gyro operators, and the large Airport gap lacks mechanistic evidence. The missing computational cost comparison also weakens the "practical alternative" claim. Nevertheless, these are issues of narrative framing and missing supplementary analysis, not fundamental methodological flaws. The core contribution — a usable, well-derived new geometry for hyperbolic neural networks — is solid and will be of interest to the community.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>