## Summary

This paper identifies a real limitation in prior alternating training methods for multimodal learning: while encoder-level gradient interference is reduced, the *classifier* becomes biased toward the dominant modality early in training, and this bias persists. The authors propose CCAT, a two-stage framework that (1) pre-trains a shared classifier with a regularization term penalizing modality contribution disparities, then (2) freezes that classifier during alternating training while adding lightweight modality-specific LoRA adapters and targeted secondary updates for severely imbalanced samples. CCAT achieves consistent gains (+1.35% on CREMA-D, +6.76% on Kinetic-Sound, +1.92% on MVSA) over prior state-of-the-art methods across three diverse multimodal benchmarks.

## Strengths

1. **Clear problem diagnosis with genuine insight.** The paper convincingly argues (Section 1, Figure 1) that alternating training methods (MLA, ReconBoost) address encoder-level interference but leave *classifier-level* bias untouched — dominant modalities bias the classifier early on, and that bias persists even as weaker modalities' encoders improve. Figure 1's tracking showing MLA's modality contributions plateau at 0.90/0.10 while CCAT reaches ~0.65/0.35 provides concrete evidence of this diagnosis.

2. **Coherent architectural response to the diagnosed problem.** The two-stage design — pretrain an unbiased classifier, freeze it as a stable decision anchor, then use LoRA adapters to reconcile the train/test distribution mismatch (unimodal vs. fused features during alternating training) — follows directly from the identified bottleneck. The design has clear internal logic rather than being a collection of unrelated tricks.

3. **Consistent empirical gains across three diverse benchmarks.** Table 1 shows CCAT outperforms the best baseline on every dataset's multimodal accuracy: +1.35% on CREMA-D (85.89 vs. LFM 83.62), +6.76% on Kinetic-Sound (79.29 vs. LFM 72.53), and +1.92% on MVSA (80.73 vs. MMPareto 78.81). Gains hold across audio-visual (CREMA-D, KS) and text-image (MVSA) settings, strengthening generalizability.

4. **Clean, interpretable ablation study.** Table 2 systematically removes each component, and every component contributes positively with monotonic improvement from worst configuration (82.80) to full method (85.89). The deltas are interpretable: freezing the classifier adds ~3%, LoRA adds ~1.2%, secondary updates add ~0.8%.

## Weaknesses

### Fatal
None.

### Major
None. The weaknesses below are all addressable and none invalidate the paper's core contribution.

### Minor

1. **The "mutual information" estimator (Eq. 5) is misnamed and its properties are unclear.** Equation 5 computes `log(N) + E[log(exp((f_i, z_i^m)) / Σ_l exp((f_i, z_i^l)))]`, where the denominator sums over modalities *l*, not over negative samples. This is **not** a standard mutual information estimator (InfoNCE or otherwise) — it is a normalized similarity score that measures relative agreement between each modality's features and the fused representation. The paper calls it "mutual information" (lines 99, 113, 115), cites Zhou et al. (2025b), and uses it to drive the regularization term (Eq. 7), sample selection (Algorithm 1, line 12), and quantitative analysis (Figure 1). While the quantity may be a reasonable heuristic for modality contribution, the information-theoretic framing implies a rigor the quantity does not deliver. The paper should either (a) rename it to something like "modality contribution score" and justify why the heuristic is meaningful, or (b) validate it against a principled estimator on synthetic data where ground-truth contributions are known.

2. **The "unified theoretical framework" (contribution i) is overclaimed.** Section 3.1 presents gradient equations for class imbalance (Eq. 2: minority class gradient ≈ −f) and modality imbalance (Eq. 3: dominated modality gradient ≈ dominant modality's features). The paper calls this a "profound theoretical isomorphism" and a "unified theoretical framework" (lines 87, 59) and lists it as contribution (i) — "providing a new theoretical framework for understanding multimodal imbalance." In reality, this is a simple gradient analogy showing a superficial similarity between two different phenomena. There are no theorems, bounds, or derived conditions. The analysis also assumes a linear classifier (Eq. 1 uses W^T f), while the actual architecture uses cross-attention + MLP + normalization (Figure 2), and the paper does not discuss whether the linear-case argument carries over. The paper is stronger as an empirical method paper; the theoretical framing should be presented as motivation, not as a substantive contribution.

3. **Main results lack variance estimates.** Table 1 reports "average test accuracy (%) of three random seeds" but provides no standard deviations or confidence intervals. This matters because: (a) the +1.35% gain on CREMA-D (85.89 vs. 83.62) is modest and could lie within noise range; (b) the ablation study (Table 2) also lacks variance, so the relative contributions of each component cannot be assessed statistically; (c) grid search results (Table 3, Figure 4) do not report whether optimal hyperparameters are stable across seeds. Reporting individual seed results or standard deviations would substantially strengthen the presentation.

4. **Stage 1 (classifier pretraining) is under-specified, limiting reproducibility.** Specifically:
   - **Are encoders trained during Stage 1?** Algorithm 1 takes encoders as inputs alongside the pretrained classifier, but Section 3.2 and Figure 2 show encoders feeding into the bidirectional cross-attention fusion during pretraining, suggesting they are active. The Implementation Details (lines 231-243) discuss 150 total epochs without splitting between Stage 1 and Stage 2.
   - **Audio input representation is unspecified.** The paper states "ResNet18 encoders for both audio and visual modalities" (line 232). For ResNet18 to process audio, the signal must be converted to a 2D representation (e.g., log-mel spectrogram), but this is never specified.
   - The paper references "Appendix A.1" and "Appendix A.3" for additional details, which are stripped from this review, so some of these gaps may be addressed there. Nonetheless, the main text should include these essentials.

5. **The regularization term (Eq. 7) drives all samples toward balanced contributions, including those where imbalance may be justified.** Minimizing |c₁ − c₂| under the softmax constraint c₁ + c₂ = 1 pushes both toward 0.5. On samples where one modality is genuinely uninformative (silent audio, dark images), forced balance could harm performance. The threshold β for secondary updates partially addresses this, but the Stage 1 classifier regularization applies uniformly to all samples. The paper should at minimum acknowledge this trade-off.

6. **On MVSA, CCAT's Image unimodal accuracy (55.30%) is lower than MMPareto's (59.54%).** The paper states this is because they "prioritize liberating weak modalities' representational potential...transcending relative performance differences" (lines 268-274), which is a reasonable but undersupported explanation. Since the multimodal accuracy still wins (80.73 vs. 78.81), this is not a fatal concern, but the trade-off deserves more explicit discussion.

### Trivial
- **Minor numerical discrepancy in line 22**: The text says MLA reduces initial contribution disparity "1.00 → 0.92," but the table shows MLA Modality A going from 1.00 to 0.90 (epoch 100). The value 0.92 does not clearly match any reported number.
- **The gradient analysis (Section 3.1) assumes a linear classifier (W^T f)** but the actual architecture uses bidirectional cross-attention + MLP + normalization. The paper does not discuss whether the simplified analysis generalizes.

## Nice-to-Haves

- **Directly measure classifier bias**: The paper infers classifier bias from modality contribution scores but never directly measures it (e.g., via linear probes on classifier weights, or gradient norms with respect to each modality's features). A direct diagnostic would substantiate the core thesis.
- **Validate the contribution estimator**: On synthetic data with known modality contributions, does Eq. 5-6 recover the correct rankings? A simple validation experiment would address Concern #1 above.
- **Disentangle LoRA's role**: The LoRA modules simultaneously correct train/test distribution mismatch and enable modality-specific adaptation. Comparing against full (non-low-rank) modality-specific adapters would clarify whether the low-rank constraint is important.
- **Report training time / FLOPs**: The secondary updates (Algorithm 1, lines 11-15) effectively double per-epoch compute for underperforming modalities on a subset of samples. Reporting wall-clock time relative to MLA would help practitioners.
- **Ablation row with "Fix + Alt" only (no Sec, no LoRA)** would directly measure the incremental value of LoRA and secondary updates relative to just freezing the classifier.

## Removed Points

- **"Missing standard deviations"** — This is kept in Minor (not removed). It's a valid weakness.
- **"Missing late fusion baselines" (Section 2 note)** — Removed. The paper compares against Sum, Concat, FiLM, BiGated, OGM-GE, QMF, MLA, MMPareto, and LFM — a comprehensive set. The specific complaint about decision-level fusion baselines is not well-specified.
- **Generic "could be more thorough" criticisms** — Removed as they lack concrete anchors in the paper.
- **Speculative concerns about appendix contents** — Removed. The appendix is stripped; speculation about what it does or does not contain is not a valid criticism of the paper as presented.
- **Criticisms about model/benchmark availability** — None present in the input.

## Novel Insights

The merged review surfaces a valuable meta-observation: the paper diagnoses a real and nontrivial problem (classifier-level bias persisting after encoder-level interference is reduced), but its presentation of the solution would benefit from sharper honesty about what is rigorously established vs. what is heuristic. The mutual information estimator, the theoretical "framework," and the numerical results all serve the same core narrative, but each has a gap that is addressable without changing the method. The most constructive insight from the review process is that the paper's empirical contribution is strong enough to stand on its own once these framing issues are corrected — the weakest part of the paper is not what it does, but what it claims about what it does.

## Suggestions

1. Rename "mutual information" (Eq. 5-6) to "modality contribution score" and either validate it against a proper MI estimator or explicitly frame it as a heuristic similarity measure.
2. Add standard deviations (or individual seed results) to Tables 1, 2, and 4.
3. Clarify Stage 1 training details in the main text: whether encoders are trained, epoch allocation between stages, and the audio input representation (e.g., log-mel spectrogram parameters).
4. Downgrade contribution (i) from "theoretical framework" to "motivating analogy" — this aligns with what Section 3.1 actually delivers and avoids overclaiming.
5. Add a brief limitations paragraph acknowledging: only tested on two-modality settings, the heuristic nature of the contribution estimator, and the trade-off between forced balance and natural modality informativeness.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>