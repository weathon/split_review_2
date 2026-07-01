Now let me craft the final consolidated review.

## Summary

This paper proposes Classifier-Constrained Alternating Training (CCAT) for multimodal learning. The key idea is that alternating training methods reduce encoder interference but leave a residual classifier-level bias toward the faster-converging modality. CCAT addresses this by: (1) pretraining a shared classifier with a regularization term that penalizes modality contribution disparity, (2) freezing this classifier during alternating training to serve as an unbiased anchor, with modality-specific LoRA adapters to handle distribution mismatch, and (3) a secondary update mechanism for severely imbalanced samples. Experiments on CREMA-D, Kinetic-Sound, and MVSA show improvements over several baselines.

## Strengths

1. **Clear identification of a specific mechanism.** The paper pinpoints a concrete failure mode (Section 1, Figure 1): alternating training prevents encoder interference but the shared classifier develops a structural preference for the faster-converging modality. This goes beyond generic "modality imbalance is bad" to motivate a targeted solution.

2. **Thorough benchmark coverage and ablation design.** Table 1 evaluates on three datasets (audio-visual and text-image) against nine baselines including recent SOTA (MLA, MMPareto, LFM). Table 2 systematically ablates each component (classifier freezing, alternating training, secondary updates, LoRA), with the ablation showing that the frozen classifier contributes ~3.09% on CREMA-D, separable from LoRA's ~1.21% contribution.

3. **The secondary update mechanism (Algorithm 1, lines 10–15) is a sensible engineering addition** that targets sample-level imbalance. The ablation shows it contributes ~2.83% on CREMA-D.

## Weaknesses

### Fatal

None.

### Major

1. **Numerical inconsistency in the headline quantitative claim.** The abstract states: *"accuracy gains of +1.35% on CREMA-D, +6.76% on Kinetic-Sound and +1.92% on MVSA over state-of-the-art methods."* From Table 1: Kinetic-Sound (+6.76) and MVSA (+1.92) match exactly. But on CREMA-D, the best baseline (LFM) achieves 83.62 and CCAT achieves 85.89 — a difference of **+2.27**, not +1.35. This is not a rounding issue (2.27 cannot round to 1.35). The paper provides no clue about what baseline produced +1.35. Since this is the central quantitative claim of the paper, this inconsistency undermines trust and must be resolved. The authors should either correct the abstract, correct the table, or explain which specific comparison yields +1.35.

2. **Overclaimed theoretical contribution.** Section 3.1 is titled "Similarity Between Class Imbalance and Modality Imbalance" and is presented (lines 26, 59, 87) as a "unified theoretical framework," a "proof," and a "profound theoretical isomorphism." What it actually contains is a qualitative comparison of two known gradient patterns: Eq. (2) shows the well-known cross-entropy gradient under class imbalance, and Eq. (3) shows an analogous pattern under a simplistic linear fusion model. There is no theorem, no bound, no formal equivalence proof. The analysis is a useful intuition but it does not constitute a theoretical framework. This overclaim runs through the paper's first listed contribution (line 26) and should be corrected to match what Section 3.1 actually delivers.

### Minor

3. **The MI estimator in Eq. (5) is under-specified.** The formula is:
   $$\text{MI}(\mathbf{z}_i^m, \mathbf{f}_i) = \log(N) + \mathbb{E}_{\mathcal{D}} \left[ \log \frac{\exp(\bar{\mathbf{f}}_i, \bar{\mathbf{z}}_i^m)}{\sum_l \exp(\bar{\mathbf{f}}_i, \bar{\mathbf{z}}_i^l)} \right]$$
   The inner product notation `(·,·)` is not defined (is it cosine similarity, dot product?). The denominator sum index `l` is not specified (over modalities? over samples in a batch?). This formula does not match any standard MI estimator (e.g., InfoNCE) in the literature as written. Since the regularization (Eq. 7) and the sample-level imbalance detection (Algorithm 1, line 12) both depend on this quantity, the ambiguity is a reproducibility gap.

4. **No variance reporting despite three random seeds.** Table 1 reports "average test accuracy (%) of three random seeds" but provides no standard deviations or confidence intervals. Some improvements are modest (MVSA: +1.92% over MMPareto), and without error bars the reader cannot assess statistical reliability. This should be added.

5. **The frozen classifier + LoRA design has an unresolved conceptual tension.** The paper argues that a frozen classifier prevents modality-specific bias, but the LoRA adapters per-modality modify the classifier's output (Eq. 10: `Cls(z) + LoRA_m(z)`). In principle, this allows the LoRA to partially bypass the "unbiased anchor" by adding modality-specific corrections. The ablation (Table 2) shows that removing LoRA drops accuracy by only 1.21% on CREMA-D, suggesting the frozen classifier carries most of the benefit, but the paper never analyzes this trade-off conceptually. Clarifying whether the benefit comes from the frozen classifier acting as an anchor or from the extra modality-specific capacity would strengthen the paper.

### Trivial

6. **Figure 1 caption wording is ambiguous.** The caption states "The 'Ours' lines show a more pronounced imbalance" when the data actually shows Ours achieves *better* balance (MLA gap ≈ 0.80 → Ours gap ≈ 0.30). "More pronounced imbalance" could be read as "more imbalance" rather than "more movement toward balance." The caption should be reworded for clarity.

## Nice-to-Haves

- **Sensitivity analysis on the regularization weight λ** (set to 0.001 with no sweep shown) would strengthen confidence in the pretraining stage.
- **Ablation of the pretraining stage itself** (Stage 1): how much does pretraining with the regularization contribute vs. freezing a randomly initialized classifier or a classifier pretrained without regularization?
- **Clarify the baseline reproduction protocol:** Are baseline numbers taken from published papers or re-run in a unified framework? The paper uses ResNet18 for audio/visual encoders — does this apply to re-run baselines or only CCAT?
- **A controlled synthetic experiment** verifying that CCAT recovers known ground-truth modality contributions would strengthen the claimed analogy to class imbalance.

## Removed Points

- **Figure 1 contradiction claim (harsh critic, Section-by-Section Notes):** The reviewer claimed Ours shows a "larger gap" (0.30) than MLA (0.80). This is a misreading — 0.30 < 0.80, so Ours actually achieves *better* balance. Removed as factually incorrect. The caption wording is poor (moved to Trivial #6 above) but the alleged contradiction does not exist.
- **"Randomly initializing a new classifier" baseline suggestion:** The harsh critic suggested comparing to random classifier initialization. This is a reasonable suggestion but not a weakness — the paper's design choice is well-motivated (the frozen classifier preserves the unbiased decision boundary from pretraining).
- **"t-SNE is low-evidence" criticism:** 2D t-SNE limitations are well-known and the paper also provides quantitative clustering metrics (CH, SH, DB). This does not rise to the level of a weakness needing inclusion.
- **Various formatting/style nitpicks and missing appendix concerns:** Removed per instructions (parser artifacts, not author errors).

## Novel Insights

The reviews collectively identify that the paper's strongest contribution is the empirical demonstration that encoder-level alternating training leaves residual classifier-level bias, and that freezing a regularized pretrained classifier addresses this. The most novel observation from the reviews is the practitioner insight from ablation analysis: most of the benefit (~3.09% on CREMA-D) comes from the frozen classifier itself rather than the LoRA adapters (~1.21%), which suggests the core mechanism is simpler than the full pipeline implies. The reviews also highlight that the claimed theoretical "isomorphism" to class imbalance is a qualitative analogy, not a formal framework — this is a useful calibration for readers.

## Suggestions

1. **Fix the CREMA-D numerical inconsistency** in the abstract. If +2.27% (over LFM) is correct, update the abstract. If +1.35% refers to a different baseline, state it explicitly.
2. **Reframe Section 3.1** as a motivating analogy/intuition rather than a "unified theoretical framework" or "proof." The method stands on its empirical results; the current framing oversells what the analysis provides.
3. **Clarify Eq. (5):** define the inner product, specify what `l` indexes over, and state whether this is computed per-batch or over the full dataset. Even if adopted from Zhou et al. (2025b), a self-contained formula is needed.
4. **Add standard deviations** to Table 1 (and Table 2 if available) for the three random seeds.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>