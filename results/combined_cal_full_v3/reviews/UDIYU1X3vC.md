Here is the final consolidated review:

---

## Summary

This paper introduces Proper Velocity Neural Networks (PVNNs), the first systematic study of the Proper Velocity (PV) model of hyperbolic geometry for deep learning. The authors establish the complete Riemannian toolkit (exponential/logarithmic maps, parallel transport, geodesic distance) for PV space, derive closed-form neural network layers (MLR, FC, convolution, activation, batch normalization), and validate across four tasks. The core advantage is numerical: PV's unconstrained coordinate representation avoids the vanishing/exploding gradient problems that plague the Poincaré ball and hyperboloid models near their boundaries.

## Strengths

- **First complete Riemannian toolkit for the PV model (Thm 4.3).** Closed-form Exp, Log, parallel transport, and geodesic distance are derived via the isometry with the Poincaré ball. This is mathematically clean and enables practitioners to build on PV space without re-deriving operators.

- **Numerical stability experiments (Sec 6.1) are convincing and well-designed.** Three complementary probes (gyro failure/violation rates, round-trip error of Exp/Log, gradient magnitude range) directly test the claimed advantage. Results are stark: PV shows zero failures at r=1000 in FP32, 3–4 orders of magnitude better round-trip error than the Poincaré ball, and stable gradient magnitudes where baselines produce vanishing (~10⁻¹²) or NaN gradients.

- **Practical layer designs with clear Euclidean recovery.** The PV MLR parameterization trick (Eq. 19) replaces costly gyroaddition with matrix multiplication, avoiding out-of-memory issues for high-dimensional classes. The PV FC layer (Thm 5.3) and MLR both explicitly recover standard Euclidean layers as K→0⁻, confirming they are proper generalizations.

- **Thorough ablation study on batch statistics (Table 7).** The paper honestly reports that Tangent and Euclidean mean/variance variants are 2× faster and achieve competitive accuracy, rather than hiding the computational cost of Fréchet-based GyroBN. This transparency is a strength.

- **Cross-domain evaluation** across numerical stability, vision (CIFAR-10/100), graph node classification (four datasets), and genomic sequence learning (TEB datasets) demonstrates breadth beyond a single cherry-picked setting.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **The large performance gains on Airport (Table 5: 97.96 vs. 92.10, +5.86%) and SINEs (Table 10: ~9 MCC points) lack supporting training diagnostics.** The paper attributes these to PV being "more effective on strongly hyperbolic graphs" based on δ-hyperbolicity values, but does not provide gradient norms, embedding norm evolution, or loss curves during training that would directly connect these gains to the claimed numerical stability mechanism. Without such evidence, the reader cannot determine whether the impressive numbers reflect a robust advantage of PV or arise from other confounding factors (different optimization dynamics, hyperparameter sensitivity, etc.).

2. **The paper does not discuss whether PV neural layers produce functionally different classes from their Poincaré counterparts under the isometry map (Thm 4.2).** If a PV MLR/FC layer composed with the isometry to the Poincaré ball yields an equivalent Poincaré layer, then the contribution is a numerically stable *implementation* rather than a genuinely different layer family. If they differ (due to the specific parameterization choices), that difference should be characterized. This question is acknowledged by the isometry theorem but left entirely unaddressed.

3. **No dedicated limitations section.** Important limitations are not discussed in the main text: (a) only fixed curvature K=-1 is used throughout, despite curvature learning being standard practice in some hyperbolic methods; (b) several comparisons (e.g., CIFAR-100: PV 78.20±0.37 vs. Lorentz 77.96±0.09) show overlapping standard deviations without significance testing; (c) Fréchet mean computation requires iterative solvers, adding overhead that is honestly reported in the ablation but not contextualized as a limitation.

4. **Vision results are marginal.** On CIFAR-100, PV MLR achieves 78.20±0.37 vs. Lorentz MLR at 77.96±0.09 — a difference of 0.24% with overlapping standard deviations. While the paper correctly notes this, the practical significance of the improvement is unclear, and the gains are too small to serve as strong standalone evidence for the method's advantages.

### Trivial
None.

## Nice-to-Haves

- **Learning curvature as a trainable hyperparameter** would broaden practical applicability and is now standard in modern hyperbolic methods.
- **Training curves and gradient norm evolution** during training for the Airport and SINEs tasks would strengthen the connection between the numerical stability claim and downstream gains.
- **Direct comparison** between PV layers and Poincaré layers composed with the isometry map would resolve the function-equivalence question cleanly.
- **Computational cost discussion** of the PV Exp map (which requires computing dπ_x(v) inside the sinh term) vs. the simpler Poincaré Exp map would help practitioners assess trade-offs.

## Removed Points

These points from the input review were removed with justification:

- **"Framing as 'new geometry' obscures isometry"** — REMOVED. The paper explicitly acknowledges the isometry (Sec 4.1, Thm 4.2). Calling PV an "alternative geometry" for a different model of the *same* hyperbolic geometry is standard terminology (cf. Poincaré ball, hyperboloid, Klein ball). The abstract correctly calls PV "an unconstrained representation of hyperbolic space."
- **"'Without Exp₀' variant undercuts hyperbolic motivation"** — REMOVED. The paper honestly presents this ablation (Table 8) and discusses it. With-Exp₀ is slightly better on most graph tasks. This is transparent reporting, not a flaw.
- **Missing related works** — REMOVED per policy (cannot verify existence of external works not cited in the paper).
- **Formatting nitpicks** — REMOVED per policy (parser artifacts).
- **Criticisms about unreleased models/code** — REMOVED per policy (the paper states code will be released upon acceptance; cited models are assumed to exist).

## Novel Insights

None beyond the paper's own contributions. The input review's insights about the isometry vs. coordinate-conditioning distinction are not novel — the paper itself acknowledges the isometry. The observation that the "without Exp₀" results are interesting is already discussed in the paper's own ablation text.

## Suggestions

1. Add training diagnostics (gradient norm evolution, embedding norm trajectories, loss curves) for the Airport and SINEs experiments to substantiate the claimed connection between numerical stability and downstream performance.
2. Include a brief discussion of whether the PV neural layers are functionally equivalent to Poincaré layers under the isometry, or explain why the parameterization differences matter.
3. Add a limitations paragraph in the main text covering fixed curvature, statistical significance of marginal gains, and the computational overhead of Fréchet-based normalization.
4. Consider reporting confidence intervals or effect sizes for the vision experiments where improvements are marginal.

## Score and Decision

**Calibration anchors considered (all rounds):**

| Anchor Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| bwOndfohRK.md (Symmetric Spaces NN) | 6.00 | R1 | Yes | Similar scope (new non-Euclidean geometry toolkit + NN layers). PVNN has stronger numerical evidence and more thorough ablations |
| ekz1hN5QNh.md (Fully Hyperbolic CNN) | 6.00 | R1 | Yes | Also hyperbolic NN layers. PVNN's evidence for its core advantage is clearer; no -3.65-level weaknesses |
| 30aSE3FB3L.md (Matrix Manifold NN++) | 5.67 | R1 | Yes | Broader scope but weaker empirical support than PVNN |
| jzneu6AO2x.md (Riemannian Hyperbolic ProtNet) | 4.25 | R1 | Yes | Limited novelty vs. PVNN's genuinely new model |
| WOopKWDWtS.md (Optimizing Hyperbolic DL) | 4.40 | R1 | Yes | Marginal improvements, unclear contributions vs. PVNN's clear thesis |
| b2FFWnwZxl.md (HVT) | 3.40 | R1 | No | Weaker, rejected; not comparable |
| nSDOkm0SKo.md (Financial Markets) | 1.00 | R1 | No | Unrelated |
| Xo0Q1N7CGk.md (Grid Cells) | 8.00 | R1 | No | Very different topic, higher bar |

**Round 1 bracket:** 5.5–6.5 based on comparison to strongest similar anchors (all scoring 5.67–6.00).

**Narrowing:** PVNN's item profile — three strengths with favorability ≥ 9.73, lowest weakness at -0.35 — compares favorably to bwOndfohRK (4 strengths, lowest weakness -0.66) and ekz1hN5QNh (weakness at -3.65). All weaknesses are minor and none threaten core claims. The paper is a solid **6.0** — clearly above the borderline, with genuine contributions that compensate for its gaps.

**Final justification:** The PVNN paper makes a real contribution by bringing an overlooked hyperbolic model to the ML community, providing a complete mathematical toolkit, and convincingly demonstrating its numerical stability advantage. The weaknesses (missing training diagnostics on outlier datasets, unaddressed isometry-equivalence question, no limitations section, marginal vision gains) are all addressable and do not undermine the paper's core thesis. The paper belongs solidly in the accept range, comparable to symmetric-spaces and fully-hyperbolic CNN papers that scored 6.0.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>