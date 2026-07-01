## Summary

This paper proposes Classifier-Constrained Alternating Training (CCAT), a two-stage framework that addresses modality imbalance in multimodal learning. The key idea is to (1) pretrain a shared classifier using bidirectional cross-attention with a regularization term that penalizes modality contribution disparities, then (2) freeze this classifier during modality-alternating training while introducing modality-specific LoRA modules to enable feature adaptation and sample-level secondary updates for severely imbalanced samples. CCAT achieves SOTA accuracy on CREMA-D (+1.35%), Kinetic-Sound (+6.76%), and MVSA (+1.92%) over prior methods.

## Strengths

- **Well-motivated architectural insight with clear empirical validation.** The paper identifies that prior alternating-training methods (MLA, Reconboost) reduce encoder-level interference but leave the shared classifier vulnerable to bias from faster-converging modalities. Freezing a pretrained classifier as a "decision anchor" while adapting features via LoRA is a clean, principled response to this specific problem. The ablation study (Table 2) confirms that removing classifier freezing degrades CREMA-D multimodal accuracy from 85.89 to 82.80 (−3.09), establishing it as the single most important component.

- **Thorough and informative ablation study.** Table 2 systematically ablates each of the four components (classifier freezing, alternating training, secondary updates, LoRA) across all three datasets and all per-modality columns. The grid searches over LoRA rank *r* (Table 3) and threshold *β* (Figure 4) add further rigor.

- **Consistent SOTA results across three diverse benchmarks.** CCAT achieves the best multimodal accuracy on all three datasets: CREMA-D (+2.27% over LFM), Kinetic-Sound (+6.76% over LFM), and MVSA (+1.92% over MMPareto). The margin on Kinetic-Sound is particularly large, suggesting the method addresses a real bottleneck on that dataset.

## Weaknesses

### Fatal

None.

### Major

- **The "mutual information" estimator (Eq. 5) is mislabeled and its properties are unexamined given its central role.** Equation (5) defines a quantity labeled as "estimated mutual information," but its form is an InfoNCE-style score (Oord et al., 2018). The paper uses this quantity for three critical purposes: (i) the Stage 1 regularization loss (Eq. 7–8), (ii) the sample-level imbalance detection in Algorithm 1 (line 10), and (iii) the motivating empirical claim in Figure 1. The paper neither justifies why this particular formulation is a valid MI estimator (the denominator sums over all samples, not a negative-sample distribution), nor does it validate that the resulting contribution scores correspond meaningfully to modality importance. The paper cites Zhou et al. (2025b) for the formula, but it remains the authors' responsibility to either defend it as a contribution metric or relabel it appropriately. Since the regularization and sample-detection mechanisms depend on this quantity, the authors should at minimum provide a post-hoc validation (e.g., correlation with leave-one-modality-out performance drop).

- **Figure 1 reports contribution values (exactly 1.00 / 0.00 at epoch 0) that demand explanation.** The table in Figure 1 shows both MLA and CCAT yielding Modality A = 1.00 and Modality B = 0.00 at epoch 0. The paper does not specify whether "epoch 0" refers to random initialization or the start of alternating training after Stage 1 pretraining. In either case, exact 1.00/0.00 values from a softmax-normalized metric require explanation—whether this is a softmax artifact from feature-norm differences, a consequence of cross-attention initialization, or some other mechanism. Without this clarification, the reader cannot assess whether Figure 1 measures genuine modality imbalance evolution or simply a built-in bias of the metric decaying during training. This matters because Figure 1 is the paper's central motivating observation.

### Minor

- **Section 3.1 overclaims a "theoretical isomorphism" and "proof."** The paper states it "provides a proof of their underlying similar" (line 59) and asserts a "profound theoretical isomorphism" (line 87), but Section 3.1 contains only two gradient approximations (Eq. 2 and Eq. 3) and a qualitative analogy. The *γ* coefficients are introduced as "implicitly learned modality utilization coefficients" without deriving them from any specific architecture. Reframing this section as motivation-by-analogy rather than formal theory would be more accurate and would not diminish the method's empirical contribution.

- **Inference-pretraining distribution mismatch is acknowledged but not directly validated.** The classifier is pretrained on cross-attention-fused features but used on unimodal features (plus LoRA correction) during alternating training and inference. The paper acknowledges this mismatch (Section 3.3) and introduces LoRA modules as the remedy, but no experiment directly measures whether LoRA bridges the distribution gap (e.g., feature-space similarity before/after LoRA). The ablation shows LoRA removal costs only 1.21% on CREMA-D multimodal accuracy (84.68 vs. 85.89), suggesting the mismatch may be manageable—but the paper does not discuss this.

- **Notable ablation patterns on Kinetic-Sound are left unexplained.** In Table 2: (a) On KS Audio, removing alternating training (*Fix ✓, Alt ✗, Sec ✓, LoRA ✓*) achieves 63.01, *higher* than the full model's 61.65. (b) On KS Video, removing classifier freezing (*Fix ✗, Alt ✓, Sec ✓, LoRA ✓*) achieves 54.32, *higher* than the full model's 53.75. These cross-modal patterns—where a component the paper argues is essential *hurts* a specific modality—deserve discussion.

- **No standard deviations or significance tests reported.** Results are stated as averages over three random seeds without any variance measure. For the modest gains on CREMA-D (+1.35%) and MVSA (+1.92%), it is unclear whether these improvements are statistically significant.

### Trivial

None.

## Nice-to-Haves

- **Sensitivity analysis for the regularization coefficient *λ* (fixed at 0.001).** Given that the regularization term is central to Stage 1, a brief ablation would strengthen confidence that the chosen value is reasonable.
- **Computational cost comparison** (training time vs. baselines), since alternating training processes modalities sequentially and adds secondary updates for imbalanced samples.
- **A brief architectural description of the bidirectional cross-attention in the main text** (rather than only in the figure caption and Appendix).
- **Direct measurement of classifier bias** (e.g., weight norms or decision-boundary drift per modality during training) to more directly support the paper's central narrative.

## Removed Points

These points from the input review were removed after verification against the paper:

- *Typos/grammar issues* (e.g., "faithfully" stray word, "underlying similar," "using" → "used"): Removed as parser artifacts per policy—these are not present in the actual submission.
- *Missing appendix content (A.1):* Removed—the parser strips appendix sections; they exist in the original submission.
- *Criticism that the bidirectional cross-attention description is only in the appendix/figure caption:* Partially removed and demoted to Nice-to-Have—the main text references the figure which provides architectural detail.
- *Inference-time MI computation not specified:* The paper does address this (line 179: "unlike the cross-attention fusion adopted in the first-stage training, here the computation of c follows the same decision-level fusion used in the inference stage"). The concern about how decision-level fusion maps to Eq. (5) remains, so the MI estimator criticism is kept in Major.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Relabel or properly defend the contribution metric.** Either rename it (e.g., "modality contribution score based on normalized feature alignment") and remove the "mutual information" claim, or provide theoretical/empirical validation that it behaves as a meaningful measure of modality influence.
2. **Clarify Figure 1.** Specify what "epoch 0" corresponds to (random initialization vs. post-Stage-1) and explain how the exact 1.00/0.00 values arise from the softmax normalization of the MI scores.
3. **Discuss the anomalous ablation patterns on KS** where removing components improves per-modality performance.
4. **Add standard deviations** to the main results table.
5. **Tone down the theoretical claims in Section 3.1** from "proof" and "profound theoretical isomorphism" to a motivating analogy, which would better match the mathematical content.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>