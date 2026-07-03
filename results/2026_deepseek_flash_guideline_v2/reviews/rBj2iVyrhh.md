Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper proposes Classifier-Constrained Alternating Training (CCAT), a two-stage framework for mitigating modality imbalance in multimodal learning. The key idea is to (1) pretrain a shared classifier with a regularization term that penalizes large disparities in modality contribution scores, (2) freeze this classifier during alternating modality training to serve as a stable decision anchor, and (3) add modality-specific LoRA adapters plus sample-level secondary updates for severely imbalanced samples. Experiments on CREMA-D, Kinetic-Sound, and MVSA show consistent improvements over baselines, with particularly large gains on Kinetic-Sound (+6.76pp).

## Strengths

1. **Novel and well-motivated classifier-centric approach to modality imbalance.** The paper identifies a genuine limitation in prior alternating-training methods: while they reduce encoder-level gradient interference, the classifier still develops structural bias toward the dominant modality. Freezing a regularized pretrained classifier as a "stable decision anchor" is a sensible architectural contribution that goes beyond the gradient-modulation and encoder-decoupling strategies in prior work (MLA, OGM-GE, MMPareto).

2. **Consistent empirical gains across diverse benchmarks (Table 1).** CCAT outperforms all baselines on all three datasets. The +6.76 percentage point gain over LFM on Kinetic-Sound (79.29% vs. 72.53%) is a substantial improvement. Gains on CREMA-D (+2.27pp over LFM's 83.62) and MVSA (+1.92pp over MMPareto's 78.81) are meaningful and hold across different modality pairs (audio-visual and text-image).

3. **Thorough ablation isolating each component (Table 2).** Every ablation row shows clear degradation: removing classifier freezing (−3.09pp), alternating training (−4.44pp), secondary updates (−2.83pp), or LoRA (−1.21pp). This provides granular, quantitative evidence that each design choice in CCAT contributes positively and the framework is not reliant on a single trick.

4. **Hyperparameter sensitivity analysis (Table 3, Figure 4).** Full grid search over LoRA rank r (1–16) and imbalance threshold β (0.05–0.40) on all three datasets is reported. The method shows modest variation across hyperparameter choices (e.g., CREMA-D varies by ~1.7% across all β values), indicating it is not brittle.

## Weaknesses

### Major

1. **Numerical inconsistency in the abstract.** The abstract states "+1.35% on CREMA-D," but Table 1 shows CCAT at 85.89% vs. the next-best baseline (LFM) at 83.62% — a +2.27 percentage point gain. The KS (+6.76%) and MVSA (+1.92%) numbers in the abstract match Table 1 exactly, making this discrepancy for CREMA-D an unforced error. This must be corrected and explained.

2. **No variance or statistical significance reported for any result.** All results are reported as the average over three random seeds without standard deviations, confidence intervals, or significance tests. On CREMA-D (+2.27pp over LFM) and MVSA (+1.92pp over MMPareto), the margins are modest, and without error bars the reader cannot determine whether these gains are meaningful or within run-to-run noise. This is a standard expectation for an empirical paper at ICLR.

3. **Overclaimed theoretical contribution (Section 3.1).** The paper presents the gradient-suppression parallel between class imbalance (Eq. 2) and modality imbalance (Eq. 3) as a "profound theoretical isomorphism" and "new theoretical framework" (Contribution i). The analysis shows that in both cases one gradient term dominates the update — a mathematically clear but straightforward observation that does not constitute a novel theoretical framework. The specific mechanisms are fundamentally different (sampling frequency vs. feature-quality/gradient conflict), and the analysis does not yield new theoretical predictions. The framing should be toned down.

### Minor

4. **Mutual Information estimator needs clarification.** Equation (5) defines an InfoNCE-style quantity called "mutual information." While InfoNCE is a standard lower-bound estimator of MI, the formulation is underspecified: the denominator sum over `l` is ambiguous (does `l` index over all N samples in the dataset or within a batch? What are the positive/negative pairs?), and the `log(N)` term deviates from standard InfoNCE. Since the contribution scores (Eq. 6) and both the regularization (Eq. 7–8) and secondary update mechanism depend on this quantity, its precise definition should be clarified, and its validity as a proxy for modality contribution should be discussed.

5. **Baseline implementation disclosure.** The paper does not state whether baseline results use original implementations, official code, or re-implementations. Since all methods use ResNet18 for both audio and visual modalities (which is a shared choice, not inherently problematic), the relative fairness depends on whether baselines were properly tuned for this setting. The authors should disclose how baseline numbers were obtained.

6. **Secondary update may double-count gradients on extreme samples.** In Algorithm 1, the same batch ℬ is used for primary alternating updates (lines 7–8) and for identifying extreme samples for secondary updates (lines 10–15). Samples with c_i^m < β effectively receive two gradient steps per epoch from the same data. While the ablation suggests this helps, the paper should discuss whether this could lead to overfitting on those samples or optimization instability.

### Trivial

7. Orphaned period at the end of line 26: "faithfully."

## Nice-to-Haves

- Code release would aid reproducibility.
- Computational cost comparison (training time, parameter count) relative to baselines.
- The hyperparameter β varies across datasets (0.05–0.30); discussion of how to set it without a validation set would strengthen practical utility.

## Removed Points

The following criticisms from the inputs have been removed/moved here with justification:

1. **"MI estimator is not mutual information"** — Removed. InfoNCE is a standard lower-bound estimator of mutual information (Oord et al., 2018). Calling it "mutual information" is consistent with the contrastive learning literature. A weaker version is retained as Minor weakness 4 above (needs clarification of formulation).

2. **"LoRA is not standard LoRA"** — Removed. Eq. (9) defines LoRA_m(z_i^m) = B^m A^m z_i^m, which is exactly the standard low-rank decomposition. The addition in Eq. (10) applies this as a residual to the classifier features, consistent with LoRA's original design.

3. **"ResNet18 for audio is suboptimal / unfair comparison"** — Removed. Using ResNet18 on audio spectrograms is common in audio-visual learning (e.g., the Arandjelovic & Zisserman 2017 paper that introduced KS). All baselines share the same backbone, making comparisons fair.

4. **"t-SNE clustering metrics are invalid"** — Removed because the paper does not state that CH, SH, DB scores were computed on t-SNE coordinates. It is standard practice to compute these metrics on original features and display them alongside t-SNE visualizations.

5. **"Figure 1 comparison is unfair"** — Removed. Both MLA and Ours start from the same state (1.00, 0.00) at epoch 0, so the comparison is appropriately controlled.

6. **"Section 3.1 γ₁, γ₂ are underspecified"** — Removed. These are explicitly described as "implicitly learned modality utilization coefficients formed during optimization," which is a standard conceptual device in multimodal gradient analysis (following Huang et al., 2022 and others).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the numerical discrepancy** in the abstract for CREMA-D (+1.35% should be +2.27%, or clarify which baseline is being compared against).
2. **Add standard deviations** (or confidence intervals) to all main results in Table 1 and ablation results in Table 2.
3. **Tone down the theoretical claims** in Section 3.1 — present the gradient-parallel as design inspiration rather than a "new theoretical framework."
4. **Clarify the MI estimator formulation** in Eq. (5) (what the denominator indexes over, whether it uses batch-level or dataset-level expectations).
5. **Disclose how baseline results were obtained** (original implementations vs. re-implementations).

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>