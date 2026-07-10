## Summary

This paper addresses replay-free continual learning for vision-language models by reframing forgetting as alignment-geometry drift. It introduces Pi-CCA, which summarizes image-text alignment via a compact CCA certificate (top-k canonical correlations and sketched subspaces) and preserves it during adaptation through spectral and subspace-angle losses, plus a prompt-invariance mechanism. The method achieves state-of-the-art among replay-free methods across four benchmarks (MTIL, X-TAIL, VLCL, ConStruct-VL) and is supported by thorough ablations and analyses.

## Strengths

- **Genuinely novel conceptual framing.** The paper reframes forgetting in VL-CL as alignment-geometry drift and proposes directly preserving the canonical correlation structure of image-text alignment via a compact CCA certificate, rather than optimizing proxy signals (logits, similarities, parameters). Section 1 convincingly argues that existing methods "regularize outcomes" rather than controlling the alignment object itself. This is the paper's strongest intellectual contribution.

- **Technically coherent and well-justified method design.** The combination of (i) random sketching for constant-memory storage of canonical subspaces (Eq. 4), (ii) the permutation-stable spectral loss (Eq. 8), (iii) the subspace-angle surrogate loss via sketched projectors (Eq. 10), and (iv) prompt-invariance via projector averaging (Eq. 5-6, 11) forms a self-contained, principled framework. Design choices such as the sorted-pairing surrogate (avoiding O(k³) Hungarian matching with negligible cost, confirmed in Table 3) and spectral clipping with orthonormalization are well-motivated.

- **Consistent empirical advantage.** The method achieves state-of-the-art among replay-free methods across all four benchmarks (Tables 1-2). On MTIL, the gap over the next-best replay-free method (C-CLIP, 75.2) is ~1.6 pp on Avg (76.8). On VLCL I2T R@1, Pi-CCA (48.6) surpasses GIFT (47.3), a synthetic-replay method that uses diffusion-generated data. The improvements on ConStruct-VL in both FA and AF are clear.

- **Thorough analysis suite.** The ablation study (Table 3) cleanly isolates each component's contribution, showing that both spectral and subspace terms matter most and that each component contributes positively. The geometry→performance correlation analysis (Fig 3), prompt invariance stress test (Fig 4 across ID/OOD templates), task-order sensitivity (Fig 5 across 20 random orders), and certificate capacity Pareto study (Fig 2) provide the right kinds of supporting evidence.

## Weaknesses

### Major

- **Figure 3 reports implausibly perfect correlations.** The figure states Pearson r=1.00 and Spearman ρ=1.00 for subspace-angle drift vs. ΔAvg, and r=0.99, ρ=1.00 for spectral drift vs. ΔAvg. These values imply perfect (or near-perfect) monotonic ordering across a sweep that varies diverse hyperparameters (certificate size, EMAs, invariance strength, whitening, pairing, LoRA capacity/LR, sketch type). The paper's own caption simultaneously describes the data as having "realistic scatter" (line 232), which contradicts the notion of perfect linear/rank correlation. This internal inconsistency undermines confidence in the geometry→performance analysis, which is meant to be direct evidence for the paper's central thesis. The authors should clarify the sweep methodology — if the points come from deterministic hyperparameter grids where geometry drift and performance are effectively functions of the same knobs, the correlation is a tautology rather than independent evidence of a causal mechanism. Re-running with independent seeds or random orders to produce realistic scatter would be more convincing.

- **Missing variance estimates on the main classification results.** Table 1 (MTIL, X-TAIL) reports only point estimates without standard deviations or confidence intervals. By contrast, Table 2 (VLCL, ConStruct-VL) does include ± ranges. The improvements on X-TAIL are modest — e.g., Pi-CCA's Avg of 68.1 vs. RAIL's 67.4 (0.7 pp gap), with many baselines clustered within ~1 pp. Without any measure of variability, it is impossible to assess whether Pi-CCA's advantage is statistically significant. Reporting results across 3 seeds (as is done for Table 2) would be minimally sufficient and is standard practice in the field.

### Minor

- **The EMA-updated certificate creates a conceptual tension with the "preservation" framing.** The certificate is introduced as a reference derived from the pre-continual model (Sec 3.2), but Eq. 13 continuously updates it via EMA: ρ* ← (1-α)ρ* + αρ̂, and similarly for subspace sketches. This means the "reference" drifts with training rather than being fixed to the pre-trained alignment geometry. The paper frames the method as "preserving pre-trained cross-modal generalization" (abstract) yet the actual mechanism is a self-smoothing trajectory. Table 3 shows that α=0 (fixed certificate) causes a 1.2 pp drop on MTIL Avg and 0.9 pp on VLCL I2T R@1, so the EMA update is empirically beneficial. The authors should explicitly own this trade-off, explaining that α controls a stability-plasticity trade-off, and ideally show how the fixed-certificate variant compares on zero-shot retention (PD) vs. forward transfer.

- **Missing joint-training / full-replay upper bound.** The paper honestly reports "state-of-the-art among replay-free methods," but it does not report what performance would be if all past data were available (e.g., joint training or experience replay with a large buffer). Adding a single row to Tables 1-2 would calibrate how much of the retention gap Pi-CCA closes relative to the ideal case, strengthening the paper's claims.

- **Missing computational cost comparison against baselines.** The Pareto analysis (Fig 2) sweeps Pi-CCA's own (k, h) but does not compare Pi-CCA's GPU memory or step time against baselines (e.g., ZSCL, C-CLIP, RAIL). Including such a comparison would clarify the efficiency-accuracy trade-off relative to existing methods, which is important for practitioners.

- **"Constant-memory" claim needs clarification.** The abstract and contributions section describe the method as "constant-memory," but the streaming covariances (Σ_vv, Σ_tt, Σ_vt in Eq. 12) consume O(d²) memory in the embedding dimension. The "constant" refers to the sketch dimension h being independent of the number of tasks or classes — which is the correct and meaningful claim. The paper should explicitly distinguish these two aspects to avoid confusion.

### Trivial

None.

## Nice-to-Haves

- A comparison of fixed-certificate vs. EMA-updated certificate on the zero-shot performance drop (PD) vs. forward transfer axes, to explicitly demonstrate the stability-plasticity trade-off controlled by α.
- A computational cost table (GPU memory, step time) comparing Pi-CCA against key baselines, alongside Fig 2's internal Pareto analysis.
- Clarification in the abstract/contributions about what "constant-memory" means (independent of tasks/classes) vs. O(d²) dependence on embedding dimension.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **Theoretical guarantee for prompt-invariant certificate (Sec 3.2).** The harsh critic noted the paper lacks a theoretical guarantee that averaging projectors over prompt perturbations yields invariance. This is scope creep — the paper presents it as a procedure validated empirically, not as a theorem. REMOVED.
- **Garbled expression on line 129.** The reviewer flagged a parser artifact in the M^{(t)} expression. Per instructions, parser artifacts are not paper flaws. REMOVED.
- **Notation overload on lines 51-52.** Minor exposition issue about θ used for both the full parameter set and the frozen backbone. This is a presentation nitpick. REMOVED.

## Novel Insights

The harsh critic correctly identified the tension between the "preservation of pre-trained alignment" framing and the EMA-updated certificate as a deeper conceptual point than the paper itself acknowledges. Rather than treating this as a bug, the paper could reframe it as a stability-plasticity trade-off controlled by α, which would ground the method in a more precise theoretical claim. This reframing would make the paper's narrative more coherent without changing any equations.

## Suggestions

1. **Resolve the Fig 3 correlation issue.** Clearly describe the sweep methodology that produced the data points. If the sweep is over hyperparameter grids where geometry drift and performance are deterministically coupled (e.g., different k values directly control both drift and performance), acknowledge this and supplement with independent-seed runs that produce realistic scatter.
2. **Add error bars to Table 1** (minimum 3 seeds) so the modest gaps on X-TAIL can be assessed for significance.
3. **Acknowledge the EMA certificate tension explicitly** and reframe α as a stability-plasticity control parameter. Provide the fixed-certificate baseline (α=0, already in Table 3) with zero-shot PD and forward transfer metrics.
4. **Add a joint-training upper bound row** to Tables 1-2.
5. **Add a lightweight computational cost comparison** against 2-3 key baselines alongside the Pareto analysis.

---

**Calibration Anchors (retrieved across all rounds):**

| Path | Avg Human Score | Round | Itemized | Comparison |
|------|----------------|-------|----------|------------|
| `sb7qHFYwBc.md` (C-CLIP) | 6.50 | 1, 2 | Yes | Direct baseline; Pi-CCA has higher conceptual novelty and broader evaluation, but more concerning evidential weaknesses (Fig 3 correlations) |
| `k9NYnsC4Mq.md` (PROOF) | 5.67 | 1, 2 | Yes | Task-specific projection method with more severe structural issues (inference mismatch); Pi-CCA is cleaner methodologically |
| `TLADT8Wrhn.md` (TiC-CLIP) | 6.25 | 1, 2 | Yes | Web-scale CL continual pre-training benchmark; different focus but similar overall quality tier |
| `9aZ2ixiYGd.md` (LEAPGen) | 5.00 | 1 | Yes | Prompt-based CL with external LLM dependency; lower quality tier than Pi-CCA |
| `JIlIYIHMuv.md` | 2.50 | 1 | No | Strong reject; Pi-CCA is far more rigorous |
| `G9Ea7mlqGO.md` (CLIP Efficient OCL) | 3.80 | 1 | No | Reject range; Pi-CCA is more thorough |
| `EKfcngSxwD.md` (Task Codebook) | 4.67 | 1 | No | Borderline reject; Pi-CCA has stronger empirical support |

**Bracket rationale:** Round 1 bracketing placed the paper in the [5.5, 7.5] range. Round 2 narrowed by comparing against C-CLIP (6.50), the most directly comparable anchor (direct baseline in Pi-CCA's tables). Pi-CCA's highest-favorability strength items (13.28-14.98) exceed C-CLIP's best (13.54), reflecting its genuinely novel geometry-first framing. However, Pi-CCA also has two low-favorability items (Fig 3 at 1.82, missing error bars at -0.21) that C-CLIP does not have — C-CLIP's lowest items are around 0-2 favorability and are presentation issues, not evidential ones. The trade-off between higher strengths and more concerning weaknesses places Pi-CCA at the same tier as C-CLIP but slightly above, given that the Fig 3 and error bar issues are fixable and the core contribution is stronger.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>