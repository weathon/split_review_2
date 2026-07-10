## Summary

This paper introduces Proper Velocity Neural Networks (PVNNs), which use the Proper Velocity (PV) representation of hyperbolic space — an unconstrained coordinate system originating from special relativity — as an alternative to the commonly used Poincaré ball and hyperboloid models. The authors derive the complete Riemannian toolkit (exponential/logarithmic maps, parallel transport, geodesic distance) for PV space, build core neural network layers (MLR, FC, convolution, activation, batch normalization), and validate the framework on numerical stability, image classification, graph node classification, and genomic sequence learning. The core thesis is that PV's unconstrained nature avoids the numerical instabilities that plague constrained hyperbolic models.

## Strengths

- **First systematic treatment of the PV model for deep learning (Section 4).** The derivation of the full Riemannian toolkit (Theorems 4.2–4.4) for Proper Velocity space, which has been largely overlooked in ML despite its attractive unconstrained property, is a genuine and competently executed mathematical contribution.

- **Clean and decisive numerical stability demonstration (Section 6.1, Tables 1–3).** Three well-designed tests — gyro operator failure/violation rates, round-trip error of exponential/log maps, and gradient magnitude across radii — cleanly isolate the numerical advantage of an unconstrained representation. PV maintains stable behavior in FP32 where Poincaré shows round-trip errors of ~2e-4 and hyperboloid produces NaN. This is the paper's clearest and most convincing result.

- **Strong graph learning results on highly hyperbolic datasets (Table 5).** PVNN achieves substantial gains on Airport (97.96% vs. 88.40% for HNN++, a ~9.5 pp improvement) and PubMed (74.33% vs. 73.68% for HNN++), with consistent improvements on Disease (+0.58 pp over HNN++). These are the most impressive empirical results in the paper.

- **Comprehensive ablation studies (Tables 6–9).** The paper systematically covers tangent vs. Riemannian FC, tangent vs. GyroBN, multiple batch statistics computation methods (tangent, Euclidean, Fréchet at varying iterations), Exp₀ lifting, and four activation strategies. This thoroughness gives the reader a clear picture of where each design choice matters.

- **Successful real-world application (Table 10).** PVCNN achieves consistent gains over both Euclidean CNN and hyperboloid HCNN-S across all five TEB genomic sequence classification tasks, with particularly strong improvements on SINEs (~9 MCC points) and LINEs (~5.7 MCC points).

## Weaknesses

### Major

1. **The paper claims "competitive or superior performance" (Conclusion) but the evidence for superior performance beyond numerical stability is uneven, and the causal link to numerical stability is not established.** On image classification (Table 4), all PV MLR gains are within 1 standard deviation of baselines (e.g., PV MLR 78.20±0.37 vs. Lorentz MLR 77.96±0.09 on CIFAR-100). The paper does not provide analysis connecting the numerical stability advantage to the large accuracy gains on Airport and genome datasets — e.g., measuring whether Poincaré baselines push embeddings near the boundary where gradients vanish, or comparing gradient magnitudes during training. Without this link, the reader cannot distinguish between "PV provides genuinely better optimization" and "baselines were not optimally tuned." Furthermore, the genome experiments (Table 10) compare only against Euclidean CNN and hyperboloid HCNN-S but lack a Poincaré-based CNN baseline, which would be the most informative comparison given the isometry between PV and Poincaré.

2. **The paper's framing overstates the contribution relative to what the isometry (Theorem 4.2) supports.** Since PV space is Riemannian isometric to the Poincaré ball, the contribution is fundamentally a numerically advantageous *reparameterization* of hyperbolic space, not a new geometric framework. The paper transparently states the isometry in Section 4 but characterizes the contribution as a "new alternative to classical hyperbolic models" (Contribution 1) and does not discuss the isometry as a caveat in the Conclusions. Readers could come away thinking PV is a meaningfully different geometry rather than a reparameterization whose practical value lies in numerical stability during optimization.

### Minor

3. **Table 7 shows Fréchet ∞ (full convergence) performing worse than Fréchet 10 iterations on several datasets** (Airport: 98.46 vs. 99.03; PubMed: 71.16 vs. 74.34). Running the Fréchet mean computation to higher precision should not degrade accuracy. The paper offers no explanation for this unexpected behavior.

4. **The PV convolution (Section 5.3) uses Euclidean concatenation followed by PV FC layers.** While this is a natural design given that PV space is ℝ^n, it does not encode a geometric inductive bias specific to hyperbolic convolution. The paper compares against HCNN-S (Bdeir et al., 2024), which formulates convolution within the Lorentz structure, but does not discuss what this comparison actually demonstrates given the design asymmetry.

### Trivial

None.

## Nice-to-Haves

- Explore behavior at different curvatures (currently fixed at K=-1 for all experiments).
- Add a Poincaré-based CNN baseline to the genome experiments (Table 10) to isolate the effect of numerical stability.
- Directly analyze gradient behavior and embedding norms during training of the specific tasks where PV improves accuracy (Airport, SINEs) to confirm the numerical stability mechanism.

## Removed Points

These points from the input review were removed after cross-checking against the paper:
- **"The isometry fundamentally limits the contribution"** — downgraded to the Major weakness about framing (above). The paper transparently states Theorem 4.2 and uses it throughout; the issue is about precise characterization, not hiding information.
- **"The Fréchet mean computation using the isometry undermines PV framing"** — removed. Using the isometry for computational convenience is standard practice and does not undermine the contribution.
- **"Table 6 GyroBN claim is overstated"** — removed. The paper's claim that GyroBN "improves over PVNN+TBN on all datasets" is technically correct (higher mean on all four datasets).
- **"Missing hyperparameter tuning for baselines"** — removed. Appendix (stripped by parser) likely contains these details; per rules, missing appendix content is not a valid criticism.
- **"Reproducibility statement"** — removed per rules (code to be released upon acceptance is standard for ICLR).
- **Section-by-section formatting/presentation nitpicks — removed per rules (parser artifacts).**
- **"Statistical rigor"** — merged into existing Major weakness about evidence quality.
- **"Curvature treatment gap"** — moved to Nice-to-Haves.

## Novel Insights

The key insight from the review process is that the paper's contribution should be evaluated as a *numerical reparameterization* of hyperbolic space rather than a *new geometric framework*, because the PV space and Poincaré ball are isometric (Theorem 4.2). This reframing does not diminish the practical value — the numerical stability results (Section 6.1) are genuinely compelling — but it does mean the paper's claim of "superior performance" requires a causal connection to numerical stability that the current experiments do not fully establish.

## Suggestions

1. Directly analyze the source of accuracy gains for the Airport and SINEs experiments: measure embedding norms and gradient magnitudes during training for PV vs. Poincaré baselines.
2. Add a Poincaré-based CNN baseline to the genome experiments (Table 10) to isolate the effect of numerical stability.
3. Acknowledge the isometry more prominently in the introduction, abstract, and conclusions, clarifying that PV offers a numerically advantageous reparameterization of hyperbolic space (not a new geometry).
4. Explain the discrepancy where Fréchet ∞ underperforms Fréchet 10 iterations (Table 7).
5. Consider ablating curvature values beyond K=-1 to test robustness of the numerical stability claims.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| ekz1hN5QNh.md (Fully Hyperbolic CNN for CV) | 6.00 | 1,2 | Yes | Shares "results within noise" on some tasks, but our paper has stronger wins on graph/genome |
| bwOndfohRK.md (NNs on Symmetric Spaces) | 6.00 | 1,2 | Yes | Similar mathematical derivation contribution; our empirical scope is broader |
| zbKcFZ6Dbp.md (Shadow Cones) | 6.33 | 2 | Yes | Similar structure of strong math + empirical; our experimental scope is broader |
| WOopKWDWtS.md (Robust Hyperbolic DL) | 4.40 | 1 | Yes | Our paper has clearer theoretical contribution and stronger results |
| jzneu6AO2x.md (Riemannian Hyperbolic Prototypical) | 4.25 | 1 | Yes | Our paper has stronger novelty and broader validation |

**Bracket (Round 1):** 6.0–7.0, based on comparison with the HCNN anchor (6.00) where our paper has stronger empirical wins but similar framing concerns.

**Narrowing (Round 2):** Our paper's top-scoring strengths (+10.00 numerical stability, +9.99 systematic treatment, +9.74 graph results, +9.78 ablations, +9.94 genome results) are more decisive than any single strength in the 6.0-range anchors. The framing overstatement (-9.99) and missing causal link are real but addressable in revision. The paper sits above the "borderline accept" level of the 6.0 anchors but below a solid "accept" due to these gaps. Final score: 6.5.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>