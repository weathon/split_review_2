## Summary

This paper introduces PI-CCA, a replay-free continual learning framework for vision-language models that preserves cross-modal alignment geometry rather than proxy quantities. The core idea is to summarize the image-text alignment via a compact CCA certificate (top-*k* canonical correlations and a sketched subspace) and constrain training to match this certificate using only mini-batch statistics, with an additional prompt-invariance mechanism. The method is evaluated across four VL-CL protocols (MTIL, X-TAIL, VLCL, ConStruct-VL), achieving top mean performance among replay-free methods with constant memory and no data generators.

## Strengths

- **Principled conceptual reframing (Sections 1, 3).** The paper reconceptualizes catastrophic forgetting in VL-CL as drift in alignment geometry (canonical correlations and subspaces of the whitened cross-covariance) rather than drift in proxy quantities (logits, similarities, parameters). This is a genuinely novel perspective, well-motivated by the actual mechanism underlying CLIP's zero-shot retrieval.

- **Strong empirical breadth (Tables 1, 2).** PI-CCA is evaluated across four distinct VL-CL protocols — task-incremental classification (MTIL), task-agnostic classification (X-TAIL), image-text retrieval (VLCL), and structured concept matching (ConStruct-VL) — and achieves the top mean performance among replay-free methods on all four.

- **Clean ablation and sensitivity analysis (Table 3, Figure 2).** The component ablations in Table 3 are informative and consistent with the paper's stated motivation: removing either the spectral or subspace term causes the largest drops. The certificate capacity Pareto analysis (Figure 2) shows the method is not brittle to the choice of *k* and *h* and identifies a practical operating regime.

- **Practical advantages.** The method is replay-free, generator-free, uses constant memory (O(*hk* + *k*) for the certificate), and is compatible with parameter-efficient adapters (LoRA). These are meaningful advantages over methods requiring replay buffers, diffusion-based synthetic data, or growing model architectures.

## Weaknesses

### Fatal
None.

### Major

- **Suspicious correlation values in Figure 3.** The figure caption reports Pearson r=1.00 (two panels) and r=0.99 (two panels), with Spearman ρ=1.00 in *all four* panels, for scatter plots relating geometric drift metrics to performance drops across multiple hyperparameter sweeps. The body text (line 232) simultaneously describes "realistic scatter" in the same plots. A Pearson correlation of exactly 1.00 implies zero residual — every data point lies precisely on the regression line — which is effectively impossible for experimental data where independent hyperparameters (certificate size, EMA rates, whitening, LoRA capacity/LR, sketch type, etc.) are varied. Even Spearman ρ=1.00 across all four panels would mean perfect rank-order agreement with no ties, which is equally implausible for real data. The discrepancy between "realistic scatter" and the reported r=1.00/ρ=1.00 values must be resolved. If these are rounded or OCR artifacts, the authors should report the correct values and clarify the presentation.

### Minor

- **No variance estimates for classification results (Table 1).** Table 1 reports MTIL and X-TAIL results as point estimates without standard deviations, confidence intervals, or any indication of the number of runs. By contrast, Table 2 reports ± values for retrieval benchmarks. The margins over baselines in Table 1 are modest (e.g., PI-CCA 76.8 Avg vs. C-CLIP 75.2 on MTIL — a 1.6 point gap). Without variance estimates, it is impossible to assess whether these differences are meaningful or within run-to-run noise. The task-order sensitivity analysis uses 3 seeds (Figure 5), suggesting this information is available.

- **Overlapping error bars on retrieval benchmarks (Table 2).** PI-CCA's VLCL I2T R@1 is 48.6±1.0 vs. GIFT 47.3±1.2 and C-CLIP 46.1±1.4. On ConStruct-VL, PI-CCA FA is 75.2±1.3 vs. GIFT 73.9±1.5. While the means favor PI-CCA, the confidence intervals overlap substantially, and no statistical significance tests are reported. The headline "state-of-the-art" claim is supported by the means, but the evidence for reliable superiority over the strongest competitor (GIFT) is weaker than the prose suggests.

- **Certificate initialization is underspecified.** The certificate is defined from "reference (pre-continual) CCA quantities" (line 71), and the paper states a "diverse anchor prompt set" is used (line 89). However, the data source for computing the initial CCA — what image-text pairs are used? The first task's data? A held-out reference set? Pre-training data? — is not specified in the main text. This is a basic reproducibility detail that affects how the method is applied in practice.

### Trivial
None.

## Nice-to-Haves

- A train-time efficiency comparison (wall-clock time and peak memory) against baseline methods (e.g., ZSCL, Mod-X, C-CLIP) under identical hardware would strengthen the paper's practical claims. The internal Pareto analysis (Figure 2) is useful but does not calibrate the reader against competitors.
- A brief limitations discussion noting, e.g., the dependency on paired image-text data for certificate initialization, the approximation introduced by sketching, or the stability-plasticity trade-off inherent in the EMA certificate update.
- A frozen-backbone baseline would help isolate the contribution of the geometry-preservation losses from the effect of LoRA fine-tuning itself.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Efficiency comparison against baselines.** The harsh critic's point about missing train-time efficiency comparison is demoted to a Nice-to-Have. The paper provides an internal Pareto analysis (Figure 2) of Pi-CCA's own configurations, and cross-method wall-clock comparisons are often noisy due to implementation differences and unreleased baseline code.
- **Parsing artifact in Eq. (line 129).** The duplicated term "$(\sum_{v=1}^t \mathbf{S}_v^{(t)})^{-1/2} (\sum_{v=1}^t \mathbf{S}_v^{(t)})^{-1/2}$" is a parser artifact, not an author error.
- **EMA trade-off discussion.** The critic's concern about the EMA certificate being a "moving target" is noted, but the paper explicitly frames this as a stability-plasticity trade-off by design (Section 3.4, Equation 13). This is a deliberate design choice, not a flaw.
- **Missing theoretical analysis (Appendix A.4).** The appendix is not available in the parsed document, which is a known limitation of the review format, not a weakness in the paper.
- **Hyperparameter count.** The critic's concern about many hyperparameters is addressed by the ablation study (Table 3) and sensitivity analysis; most VL-CL methods in this space have comparable numbers of hyperparameters.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's most pointed observation — that the Figure 3 correlation values are suspicious — is factually correct and has been included as the primary weakness.

## Suggestions

1. **Resolve the Figure 3 correlation discrepancy.** Report the exact Pearson and Spearman values without rounding, and reconcile the claim of "realistic scatter" in the body text with the reported r=1.00/ρ=1.00 annotations. If these are figure-rendering artifacts, state this explicitly.
2. **Add variance estimates to Table 1** (standard deviations or confidence intervals), or at minimum state the number of seeds and confirm that variance was negligible.
3. **Specify the data source** used to compute the initial CCA certificate (what image-text pairs, under what conditions).
4. Consider adding a brief limitations paragraph acknowledging the stability-plasticity trade-off in the EMA certificate update and the approximation error introduced by sketching.

## Score and Decision

### Calibration Anchors

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| C-CLIP | sb7qHFYwBc.md | 6.50 | 1 | Yes | Closest comparable — VL-CL method. PI-CCA has a stronger conceptual contribution but more evidentiary gaps (Figure 3, missing variance). |
| TiC-CLIP | TLADT8Wrhn.md | 6.25 | 1 | Yes | Benchmark-focused CL continual learning paper. Less directly comparable on method novelty. |
| CLIP Efficient Online CL | G9Ea7mlqGO.md | 3.80 | 1 | Yes | Much weaker paper that was rejected. PI-CCA has substantially stronger conceptual novelty and evaluation breadth. |

**Round-1 bracket:** The paper is most comparable to C-CLIP (6.50) in the 5.5–7.5 band. It is clearly stronger than the 3.80-level papers. No comparable papers were found in the strong-reject (0–1.5) or strong-accept (8.5+) bands. **Initial bracket: 5.5–7.0.**

**Narrowing:** Compared to C-CLIP (6.50, accepted), PI-CCA has a more novel conceptual contribution (impact +10.00 vs. C-CLIP's strongest contributions at +10.00). However, PI-CCA's most impactful weakness — the Figure 3 correlation issue (impact -10.00) — is a more central evidential concern than C-CLIP's most impactful weaknesses (missing references at -10.00, poor benchmark definition at -10.00), because it directly touches the paper's core explanatory claim. The missing variance in Table 1 (impact -8.13) and underspecified certificate initialization (impact -7.88) are additional concerns absent from C-CLIP's review. The paper's strengths are genuine and substantial, but the evidentiary gaps in the correlation analysis and missing variance estimates pull the overall assessment below C-CLIP. **Final score: 6.0.**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>