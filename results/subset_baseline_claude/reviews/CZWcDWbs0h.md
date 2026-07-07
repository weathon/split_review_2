## Summary

This paper proposes ALiRAS (Auto-labeled Linguistic Representations for Audio Spoofing detection), a multi-view framework for audio deepfake detection. The core idea is to fine-tune a VGGish model on 840 expert-labeled audio clips annotated with three phonetic/phonological binary features (breath presence, pitch anomaly, audio quality anomaly), then integrate these auto-labeled linguistic features into ensemble models alongside foundation model baselines (XLSR, HuBERT, WavLM). The paper claims improvements in three dimensions: effectiveness (EER reduction), scalability (31% time savings via a cascade ensemble), and explainability (SHAP values over the three features).

---

## Strengths

- **Interdisciplinary motivation is sound**: Combining sociolinguistic expertise with deep learning for ADD is a legitimate and underexplored research direction. The idea of using human-perceptual features as an auxiliary view is conceptually appealing.
- **Scalability analysis is concrete**: Table 3 and Table 4 provide actual timing measurements across different ensemble configurations, making the resource-efficiency claims falsifiable and reproducible.
- **Attack-type breakdown in Table 6**: Decomposing performance by TTS, VC, VC-TTS, and Unknown attacks adds analytical depth beyond aggregate metrics.

---

## Weaknesses

### Fatal
None that fully invalidate the approach conceptually, but the combination of major weaknesses below substantially undermines the paper's core claims.

### Major

1. **Auto-labeling performance is too weak to justify the approach**. The best AUC for auto-labeling the linguistic features is 0.71 (VGGish), while the foundation models achieve 0.57–0.59 (Table 2). A 0.71 AUC is poor for a binary classification task with expert-defined, perceptually salient features. This calls into question whether the auto-labeled features carry reliable phonetic signal at scale.

2. **Performance improvements are selective and largely not additive**. The abstract claims "at least 7% EER decrease," but this improvement holds only for XLSR-ResNet18 (0.40 → 0.27), which is itself a poor baseline approaching random detection. For HuBERT-ResNet18 (EER=0.171), the best-performing model, adding ALiRAS yields no gain—EER remains 0.171. For WavLM-MLP (EER=0.277), ALiRAS again yields no improvement. The claimed effectiveness therefore does not hold for the competitive baselines and appears to only repair a broken one.

3. **The 31% time savings is a dataset property, not an intrinsic method advantage**. The cost-efficient cascade skips foundation model processing for samples classified as spoofed by ALiRAS. The ~31% savings directly reflects the fraction of data ALiRAS labels as spoofed in this specific dataset split. This figure is not generalizable to other datasets with different spoof/genuine ratios and does not account for any real-time streaming scenario where a cascade cannot be pre-filtered.

4. **The cost-efficient ensemble introduces a latent quality trap**. When ALiRAS falsely labels a spoofed sample as genuine (its own EER is 0.319), the foundation model must process it—but this is the most important case to get right. There is no analysis of the false-negative rate of ALiRAS as the "gatekeeper," which is critical for a security-facing application.

5. **Explainability contribution is thin**. Applying SHAP to a 3-feature logistic/MLP model over expert-defined binary features is not a substantive explainability contribution. The three features were chosen by experts precisely because they are semantically interpretable; SHAP is not revealing anything beyond what the experts already knew. This does not provide explainability for the foundation model's decisions, only for the auxiliary ALiRAS component.

### Minor

- The expert-labeled dataset (840 samples, 15% held out = ~126 test samples) is small. Auto-labeling model AUCs on this tiny test set carry high variance.
- Training on ASVspoof 2019 LA and testing on ASVspoof 2021 DF mixes different challenge tracks (logical access vs. deepfake), which may favor certain attack types.

### Trivial

- The toy example in Figure 2 is overly long for what it explains.
- Ensemble weight selection via grid search on validation data is standard and needs no extended justification.

---

## Nice-to-Haves

- Ablation showing what happens when the ALiRAS threshold (0.55) is varied, especially how it trades off time savings versus EER degradation.
- Evaluation on a held-out third dataset to assess cross-corpus generalization of the auto-labeled features.
- A comparison with existing cascade/early-exit detectors to contextualize the scalability claim.

---

## Novel Insights

The paper's most interesting implicit finding is that VGGish — a comparatively lightweight, supervised audio classification model — outperforms large self-supervised speech foundation models (HuBERT, WavLM, XLSR) at capturing expert-defined perceptual phonetic features. This suggests the self-supervised SSL objectives are not aligned with human phonetic perception and raises a worthwhile question about what these models actually learn. However, this insight is not developed or highlighted by the authors.

---

## Suggestions

- Quantify ALiRAS's false-negative rate in the cascade setting separately, and report EER conditioned on ALiRAS's gating decision (i.e., what is the error rate on the "ALiRAS says genuine but foundation model must decide" subset).
- Reframe the scalability claim by reporting how the 31% reduction scales with dataset spoof ratio, or test on a dataset with a different ratio to show robustness.
- Consider a deeper explainability analysis: e.g., do the SHAP rankings of the three features correlate with known properties of specific TTS systems? That would constitute a novel finding.

---

## Score and Decision

The paper addresses a real problem (explainability and scalability in ADD) with a creative interdisciplinary angle. However, the technical execution has significant gaps: auto-labeling accuracy is mediocre (0.71 AUC), performance gains only materialize for the weakest baseline, explainability is reduced to SHAP on three hand-curated binary features, and the scalability claim is dataset-dependent. The paper does not meet the bar for acceptance as a research contribution at a top ML venue in its current form.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>