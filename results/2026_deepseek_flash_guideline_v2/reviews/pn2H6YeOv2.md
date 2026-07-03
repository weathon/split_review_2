## Summary

PI-CCA proposes a replay-free continual learning framework for vision-language models that preserves the geometry of cross-modal alignment (canonical correlation spectrum and subspaces) rather than regularizing proxy signals like logits or similarity distributions. It maintains a compact sketched certificate of CCA invariants, enforces spectral/subspace consistency via mini-batch losses, and adds prompt robustness through projector averaging over prompt perturbations. The method achieves state-of-the-art results across four VL-CL benchmarks without storing past data.

## Strengths

1. **Novel geometry-first reframing of forgetting in VL-CL**: The paper identifies and addresses a structural limitation in prior work—methods like Mod-X, ZSCL, CTP, and DKR regularize proxy signals (similarities, logits, parameters, routing) rather than directly controlling the cross-modal alignment geometry. PI-CCA acts on the whitened cross-covariance's spectral and subspace structure, which is the actual object driving zero-shot retrieval and recognition. This reframing is principled and well-motivated (lines 20–22, 29, 69–71).

2. **State-of-the-art results across all four benchmarks among replay-free methods**: Table 1 shows PI-CCA achieving the highest MTIL Avg (76.8 vs 75.2 for C-CLIP) and X-TAIL Avg (68.1 vs 67.4 for RAIL). Table 2 shows it also tops VLCL I2T R@1 (48.6 ± 1.0) and ConStruct-VL Final Accuracy (75.2 ± 1.3), even surpassing GIFT—a method that uses diffusion-generated synthetic replay—without storing or generating any past data. The consistent margins across diverse benchmarks (classification, retrieval, structured concepts) provide strong empirical support that the geometry-preservation principle generalizes.

3. **Thorough component-wise attribution via systematic ablation**: Table 3 quantifies each term's contribution, with spectral loss removal dropping MTIL Avg by 2.5 pts, subspace loss removal by 2.2 pts, prompt invariance removal by 1.5 pts, and covariance EMA removal by 2.7 pts. The ablation covers design choices (Hungarian vs. sorted pairing: 0.1 pt gap, Gaussian vs. SRHT sketches: 0.2 pt gap) and confirms each component contributes meaningfully.

4. **Constant-memory replay-free certificate via random sketching**: The certificate stores only sketched bases of size O(h×k) with h ≪ d_v, d_t (Section 3.2, Eq. 4), giving memory independent of feature dimensionality. The Pareto analysis (Figure 2) maps the efficient frontier across k ∈ [16,128] and h ∈ [128,384], confirming robustness within a broad ridge with (k=64, h=256) as a practical knee point.

5. **Explicit prompt-invariance mechanism orthogonal to prior VL-CL work**: The ℒ_pi loss (Eq. 11) averages sketched projectors over prompt perturbations, reducing sensitivity to phrasing variation. The stress test (Figure 4) shows that at perturbation strength s=1.0, the invariance mechanism improves R@1 by +2.44 p.p. (ID) / +2.51 p.p. (OOD) and reduces forgetting by ~1.10 AF vs. the ablated variant, with benefits persisting under OOD templates.

## Weaknesses

### Fatal
None.

### Major

- **Figure 3 reports unusually perfect correlation values requiring clarification**: Two of four panels report Pearson r=1.00, and three of four report Spearman ρ=1.00, between geometry drift and performance drop across 25+ hyperparameter configurations. While these values are not strictly "impossible" (deterministic single-seed evaluation where both drift and Δ-performance are computed relative to the same reference configuration could produce near-perfect fit), Pearson r=1.00 implies zero residual variance—a phenomenon rare enough in experimental ML that the paper should explicitly explain the data generation process (e.g., number of (x,y) points per panel, whether multiple seeds were used, precision of reported values). The figure caption's mention of a "95% CI shaded area" on a perfect-fit line is also internally inconsistent. Since this figure is presented as key evidence for the paper's central conceptual claim ("preserving CCA geometry reliably predicts retention"), the reported values as stated strain credibility and require author clarification. **Crucially, the method's benchmark performance (Tables 1–3) stands entirely independently of this figure—the SOTA results do not require the correlation evidence to be valid.**

### Minor

- **No computational cost comparison against baselines**: The paper reports per-step time and peak memory for PI-CCA's own Pareto sweep (Figure 2) but does not compare wall-clock time or memory against any baseline method. Since PI-CCA requires differentiable SVD via power iteration, multiple forward passes for prompt perturbations, and EMA covariance updates, a reader cannot assess whether the ~1–2 point gains come at 2× or 10× the compute of a baseline. A brief comparison table would substantiate practicality.

- **Missing statistical reporting for Table 1**: The MTIL and X-TAIL results in Table 1 lack variance intervals (±), while Table 2 (VLCL, ConStruct-VL) includes them. Given that the margin over the next-best method on MTIL Avg is only 1.6 points (76.8 vs. 75.2) and many methods cluster within 2–3 points, it is unclear whether this lead is statistically reliable.

- **Performance Drop (PD) metric mentioned but absent from main tables**: The evaluation protocol (line 147) states that PD on a held-out zero-shot suite is reported, but no PD column appears in Tables 1 or 2. PD is plotted in Figure 4 but absent from the main quantitative comparisons, creating an inconsistency between stated protocol and reported results.

- **EMA certificate update creates a framing tension**: The certificate is updated via EMA every step (Eq. 13), meaning it slowly drifts from the original pre-trained alignment. The paper acknowledges this as "controlled plasticity" (line 133), but the abstract's phrasing ("preserves pre-trained cross-modal generalization") and the "invariant" terminology could mislead a reader into thinking the reference is fixed. The method preserves a slowly-adapting reference rather than the original pre-training alignment. Clarifying what exactly is being preserved and how α controls this trade-off would strengthen the paper.

### Trivial

- The sketch isometry claim (line 109: "preserves order/angles under near-isometric sketches... Gaussian/SRHT") is stated without a formal bound or citation. A Johnson-Lindenstrauss-style argument would require specifying how h depends on k and the embedding dimension of the subspaces being compared.

## Nice-to-Haves

- Including generic CL baselines (e.g., EWC, SI, MAS applied to LoRA adapters) would strengthen the claim that geometry-based regularization is superior to simple weight-regularization approaches, but this is outside the paper's stated scope and does not weaken the existing comparison against VL-CL-specific methods.
- Adding a negative control to Figure 3—showing that changes in non-regularized geometry measures (e.g., lower spectrum components below k) do NOT correlate with performance—would demonstrate specificity and rule out spurious correlation.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Code release concern** (Harsh Critic): Removed per the hard rule that questioning the release status of cited or promised artifacts is not permitted. The paper states code will be released upon acceptance.
- **"Figure 3 correlations are impossible"** (Harsh Critic): Reframed. The claim of impossibility is too strong—deterministic single-seed evaluation with relative-to-baseline measurements could produce such values. Demoted to a Major weakness requiring clarification rather than treated as a fatal flaw.
- **Missing comparison against EWC/SI/MAS** (Harsh Critic): Demoted to Nice-to-Haves. The paper compares against standard VL-CL baselines; requesting single-modality CL methods is scope creep.
- **Missing appendix content / theoretical proofs** (Harsh Critic): Removed per the hard rule that the parser strips appendix content; these exist in the original submission.
- **Generic "the evaluation lacks rigor" framing** (Harsh Critic): Removed as unspecific. Every concrete sub-concern was either verified (missing variance, missing PD) or reframed above.
- **Strength Finder's generic strengths** (e.g., "the paper addresses an important problem"): Removed as superficial. Only concrete, evidence-grounded strengths were retained.

## Novel Insights

The reviews surface a genuine tension: the paper's strongest evidence for its central *conceptual* claim (Figure 3's geometry→performance correlation) has the weakest empirical presentation (suspiciously perfect r values), while its strongest *empirical* contribution (consistent SOTA across four benchmarks) is cleanly presented and independently convincing. This means the paper succeeds on its "capability and performance" contribution (contribution ii in Section 1) even if the "insight" contribution (contribution i) rests on imperfect correlational evidence. A reader should judge the paper primarily on the benchmark results and the novelty of the geometry-preservation principle, rather than on the correlation figure alone.

## Suggestions

1. Provide the raw data behind Figure 3 (the drift values and per-configuration performance drops) to clarify how the reported r=1.00 values arise—specifically, how many points per panel, whether multiple seeds were used, and the numerical precision of the reported correlations.
2. Add a computational cost comparison table (step time and peak memory) against 2–3 representative baselines (e.g., C-CLIP, ZSCL, Mod-X).
3. Add ± variance intervals to Table 1 for consistency with Table 2.
4. Either report the PD metric in the main tables or remove it from the protocol description to eliminate inconsistency.
5. Clarify in Section 3.4 what the certificate EMA preserves relative to pre-training, and consider an experiment comparing the EMA-updated certificate against a fixed (pre-training-only) certificate.

## Score and Decision

Based on calibration against the human-reviewed corpus (though the calibration search tool encountered an infrastructure error and could not retrieve anchors), I assign a score based on direct paper analysis:

- The paper makes a genuinely novel conceptual contribution (geometry-first reframing of VL-CL forgetting)
- Achieves consistent SOTA results across 4 benchmarks with thorough ablation
- Has one concerning figure (Figure 3) whose correlation values need clarification but does not depend on that figure for its main empirical claims
- Has several presentation/consistency issues (missing variance, missing PD metric, missing compute comparison)

This places the paper solidly in the accept range—between 7 and 8 on the ICLR scale. The core contribution is real, the experiments are well-designed, and the issues are addressable in rebuttal/revision. The paper is not a 10 (breakthrough) nor a borderline 6.

**MY FINAL SCORE: <score>7.5</score>**
**MY FINAL DECISION: <decision>Accept</decision>**