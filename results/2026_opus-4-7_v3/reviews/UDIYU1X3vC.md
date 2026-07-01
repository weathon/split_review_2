Now let me read the remaining parts of the paper for completeness:Good, I now have a thorough understanding of the paper. Let me draft the review.Now let me run Round 1 calibration search to bracket the score:Let me read the most relevant anchor papers for calibration:Now I have sufficient calibration data. Let me form my initial bracket and write the final review.

**Round 1 Bracket Analysis:**

The most directly comparable anchor is `ekz1hN5QNh.md` — "Fully Hyperbolic Convolutional Neural Networks for Computer Vision" (HCNN, Lorentz model, avg 6.0, accepted). Both papers develop core neural network layers on a specific hyperbolic model, with modest vision improvements and stronger results on other tasks. The PV paper has stronger ablations, a specific numerical stability advantage, and larger genomic gains.

Rejected papers in the 3.0–5.0 range (`q6WtaLj8O1`, `WOopKWDWtS`, `MEnPLXJNng`) have substantially weaker experimental validation, unclear contributions, or missing ablations — the PV paper is clearly above these.

Accepted papers at 6.0 (`ekz1hN5QNh`, `bwOndfohRK`) have similar structural contributions with comparable strengths/weaknesses. Papers at 8.0 (`Xo0Q1N7CGk`, `g7ohDlTITL`) represent more fundamental contributions with stronger validation.

**Round 1 bracket: 5.5 to 7.0**

The PV paper sits at or slightly above the HCNN anchor (6.0) due to more thorough ablations, a cleaner theoretical story, and stronger genomic results, but is pulled down slightly by the isometry/reparameterization nature of the contribution and modest vision/graph gains.

---

## Summary
This paper introduces Proper Velocity Neural Networks (PVNNs), which operate in the Proper Velocity (PV) model of hyperbolic space—an unconstrained coordinate representation that is Riemannian-isometric to the Poincaré ball. The authors derive the complete Riemannian toolkit for PV via this isometry (exponential/logarithmic maps, parallel transport, geodesic distance), then build core neural network layers (MLR, FC, convolution, activation, batch normalization) in PV space. Experiments across numerical stability, image classification, graph node classification, and genomic sequence learning demonstrate PV's numerical stability advantages and competitive-to-superior downstream performance.

## Strengths
- **Systematic derivation via isometry (Section 4, Theorems 4.2–4.3).** Rather than deriving PV Riemannian operators from scratch, the paper leverages the proven isometry with the Poincaré ball (Theorem 4.2) to systematically obtain all PV operators (Theorem 4.3). This is mathematically elegant and guarantees correctness by construction. Theorem 4.4 further unifies the gyro and Riemannian viewpoints.

- **Practical MLR reparameterization (Theorem 5.2, Eq. 19).** The $(z_k, r_k)$ parameterization reduces a $b \times C \times n$ intermediate tensor from naive gyroaddition (Eq. 18) to simple inner products $\langle x, z_k \rangle$ computable via matrix multiplication. The paper explicitly explains why the original form is memory-prohibitive—a practical insight rarely made explicit in this subfield.

- **Informative numerical stability experiments (Section 6.1, Tables 1–3).** The three-axis comparison (failure rate, round-trip error, gradient behavior) directly probes the operations used during training, clearly demonstrating: (i) hyperboloid complete failure at $r \geq 200$ (Table 1), (ii) Poincaré gradient vanishing to $10^{-11}$–$10^{-13}$ (Table 3), and (iii) PV's stable behavior across all three metrics.

- **Unusually thorough ablation study (Tables 6–9).** The paper systematically ablates tangent-space vs. Riemannian FC (Table 6), tangent vs. Euclidean vs. Fréchet batch statistics with timing (Table 7), exponential map lifting (Table 8), and activation variants (Table 9). The honesty about cases where tangent/Euclidean variants are competitive (e.g., Table 6: PubMed and Cora for TFC) adds credibility.

- **Strong genomic results (Table 10).** PVCNN outperforms HCNN-S by ~8 MCC on SINEs, ~6 on LINEs and unprocessed pseudogenes, and ~3 on hAT-Ac—margins large enough to be practically meaningful in this domain.

## Weaknesses

### Fatal
None.

### Major
- **Downstream improvements on vision and graph tasks are modest and lack significance testing, partially undermining the "effectiveness" claim.** On CIFAR-10 (Table 4), PV MLR achieves 95.30±0.18 vs. 95.12±0.20 (Unidirectional MLR)—the standard deviations overlap. On CIFAR-100, 78.20±0.37 vs. 77.96±0.09 (Lorentz MLR)—a 0.24% gain. On graph learning (Table 5), PVNN loses on Cora (51.42±1.33 vs. 53.34±1.65 for LNN). The paper reports means and standard deviations but no statistical significance tests (e.g., paired t-tests). While the genomic results are convincing, the "effectiveness" claim across all domains is only partially supported. The paper would benefit from either statistical tests or a more qualified effectiveness claim.

### Minor
- **The paper's framing occasionally implies a deeper geometric distinction than the isometry warrants.** Since PV is isometric to the Poincaré ball (Theorem 4.2), PV and Poincaré represent the *same* Riemannian manifold in different coordinates. The contribution is therefore a numerically superior *parameterization*, not a new geometry. The abstract's "stable alternative" and introduction's "explore the Proper Velocity space" are accurate, but the paper would be sharpened by an explicit statement that PV's advantage is one of parameterization, not geometry. This is a framing issue, not a structural flaw.

- **PV's behavior at extreme norms is not characterized.** Since $\beta_x = 1/\sqrt{1+|K|\|x\|^2} \to 0$ as $\|x\| \to \infty$, the PV metric (Eq. 1) approaches the Euclidean metric at large norms—meaning embeddings far from the origin effectively lose their hyperbolic character. Whether PV embeddings migrate to large-norm regions during training, and whether this trades stability for geometric expressivity, is not discussed. This is an insightful open question that would strengthen the paper if addressed.

- **Convolution and activation choices in PV are convenient but geometrically ad hoc (Section 5.3).** PV concatenation is defined as Euclidean concatenation because PV is unconstrained, and one activation variant applies $\sigma$ directly in PV space. While the ablations (Table 9) explore alternatives, the justification remains pragmatic rather than principled. This is acceptable for a first paper on PV networks but blurs the line between principled hyperbolic computation and Euclidean operations on an unconstrained space.

### Trivial
None.

## Nice-to-Haves
- An analysis correlating dataset hyperbolicity ($\delta$) with PV's relative gain over baselines would make the contribution more actionable. The paper notes this trend in Section 6.3 ("PV geometry is more effective on strongly hyperbolic graphs") but does not develop it quantitatively.
- A direct experiment demonstrating PV's stability advantage during training—e.g., enabling larger learning rates, deeper networks, or removing gradient clipping that Poincaré/hyperboloid require—would strengthen the connection between Section 6.1's isolation experiments and downstream performance.
- Wall-clock training time comparisons for the full models in Tables 4, 5, and 10 (Table 7 provides timing only for normalization variants).
- Analysis of PV embedding norm distributions during training to understand whether the unconstrained space is being exploited or is merely a convenience.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"No Poincaré-based convolutional baseline in genomic experiments (Table 10)"**: The paper follows the experimental setup of Khan et al. (2025), and the gains over HCNN-S (hyperboloid) are large enough (~6–9 MCC) to be meaningful regardless of whether a Poincaré CNN is included. Demanding an additional baseline beyond what the reference paper provides is scope creep.
- **"Airport performance gap may be sensitive to implementation details"**: Speculative—the paper uses a controlled setup with the same architecture across all models (Section 6.3), and no evidence of implementation artifacts is provided. The gap (97.96% vs. 92.10%) is large and consistent with PV's advantage on strongly hyperbolic data ($\delta=1$).
- **"Table 3 gradient range should be a plot"**: Pure presentation preference, not a weakness.
- **"GyroBN ordering dependence (centering before scaling)"**: The paper correctly documents this requirement in the text following Theorem 5.4. This is a correctly noted design choice, not a weakness.

## Novel Insights
The paper's central insight is that the PV model's unconstrained nature—occupying all of $\mathbb{R}^n$—simultaneously provides numerical stability (no boundary effects, no manifold constraint violations as in the hyperboloid) and practical engineering benefits (Euclidean concatenation for convolution, direct activation, optional omission of the exponential map). The systematic derivation of all PV operators via the Poincaré isometry, rather than from scratch, demonstrates a reusable methodology for bringing new coordinate systems to hyperbolic neural networks. The observation (raised in analysis but absent from the paper) that $\beta_x \to 0$ at large norms suggests a stability–expressivity trade-off unique to PV that could be a productive direction for follow-up work.

## Suggestions
- Add statistical significance tests (paired t-tests or Wilcoxon signed-rank) for Tables 4 and 5, or qualify the effectiveness claim to focus on genomic tasks where gains are clearly significant.
- Include an explicit statement (e.g., in Section 4.1 or the conclusion) that PV and Poincaré are the same Riemannian manifold in different coordinates, and frame the contribution as a numerically superior parameterization.
- Monitor PV embedding norm distributions during training across the experimental tasks to characterize whether embeddings remain in a strongly hyperbolic regime.
- Investigate whether PV enables training regimes (larger learning rates, deeper networks) that are unstable for Poincaré/hyperboloid, directly connecting the stability advantage to practice.

## Score and Decision

### Calibration Anchors

| Anchor | Avg Score | Round | Comparison to PV paper |
|--------|-----------|-------|------------------------|
| `nSDOkm0SKo.md` (Financial Markets NN) | 1.0 | R1 | Clearly weaker—not a genuine ML contribution. |
| `Uj0h13lVrR.md` (KL Div GFlowNets) | 1.0 | R1 | Clearly weaker—fundamental methodological issues. |
| `P49gSPmrvN.md` (UMAP Scientific Discourse) | 1.0 | R1 | Clearly weaker—minimal novelty. |
| `q6WtaLj8O1.md` (Hyperbolic Hypergraph GNN) | 3.0 | R1 | Weaker—unclear model, poor presentation, mixed results. PV paper is substantially stronger. |
| `HDmmwwTIlf.md` (Characteristic NN for hyperbolic PDEs) | 2.5 | R1 | Unrelated topic; clearly weaker contribution. |
| `A1JdcLawSu.md` (Hyperspherical CL) | 3.0 | R1 | Different topic; weaker experimental validation. |
| `b2FFWnwZxl.md` (HVT) | 3.4 | R1 | Related (hyperbolic vision transformer); weaker—5 reviewers all gave 3. PV paper is clearly above. |
| `MEnPLXJNng.md` (Riemannian Transformation Layers) | 4.75 | R1 | Related—general Riemannian layers. Rejected for novelty concerns and limited manifold scope. PV paper has clearer contribution and better experiments. |
| `WOopKWDWtS.md` (Robust Hyperbolic DL) | 4.4 | R1 | Related—stability improvements for hyperbolic learning. Rejected for marginal improvements and lacking theory. PV paper has more rigorous development. |
| `jzneu6AO2x.md` (Riemannian Optimization for HPN) | 4.25 | R1 | Related—hyperbolic prototypical networks. Mixed reviews. PV paper has broader contribution. |
| `EyWKb7Ltcx.md` (Intrinsic Riemannian Classifiers SPD) | 5.0 | R1 | Related—Riemannian classifiers. Rejected despite similar theoretical depth. PV paper has stronger experimental validation. |
| `ekz1hN5QNh.md` (HCNN - Fully Hyperbolic CNN) | 6.0 | R1 | **Most directly comparable.** Also develops core layers on a specific hyperbolic model (Lorentz). Similar modest vision gains. PV paper has stronger ablations, numerical stability analysis, and larger genomic gains. Comparable or slightly above. |
| `bwOndfohRK.md` (NN on Symmetric Spaces) | 6.0 | R1 | Related—unified FC/attention on symmetric spaces. PV paper has comparable depth with more focused contribution and better ablations. |
| `30aSE3FB3L.md` (Matrix Manifold NN++) | 5.67 | R1 | Related—FC/conv layers on SPD via gyrovector calculus. Mixed reviews (3,8,6). PV paper has more coherent contribution. |
| `YcaFqY8LWD.md` (GyroAtt) | 6.25 | R1 | Related—gyro attention on matrix manifolds. Similar quality level. |
| `Xo0Q1N7CGk.md` (Conformal Isometry Grid Cells) | 8.0 | R1 | Stronger—more fundamental contribution with uniform reviewer agreement. PV paper doesn't reach this level. |
| `JWtrk7mprJ.md` (Residual Deep GPs on Manifolds) | 7.6 | R1 | Stronger—more novel methodology with broader applicability. PV paper is below this. |
| `g7ohDlTITL.md` (Flow Matching on General Geometries) | 8.0 | R1 | Stronger—foundational contribution. PV paper is below. |
| `3i13Gev2hV.md` (Compositional Entailment Hyperbolic VL) | 8.0 | R1 | Stronger—novel use of hyperbolic geometry for VL models. PV paper is below. |

**Round 1 bracket: 5.5–7.0**

**Narrowing to final score:** The PV paper is most comparable to `ekz1hN5QNh.md` (HCNN, 6.0) and `bwOndfohRK.md` (Symmetric Spaces NN, 6.0). It shares the same structural contribution type (new layers on a specific model) with comparable experimental quality. The PV paper's advantages (numerical stability analysis, stronger ablations, larger genomic gains) are balanced against its main weakness (reparameterization rather than new geometry, modest vision/graph gains). The paper sits squarely at the accept threshold—a technically sound paper with a genuine but bounded contribution.

**Final score: 6.0**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>