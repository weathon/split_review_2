Now I have enough to write a thorough review.

---

## Summary

XTalker is an audio-driven portrait animation framework that decomposes facial motion into three interpretable subspaces within LivePortrait's keypoint parameter space: lip-phoneme synchronization (driven by audio amplitude envelope), emotional expression (conditioned on discrete emotion labels), and head motion (guided by user-defined curves). Built on a flow-matching paradigm with a shared MM-DiT backbone and three lightweight prediction heads, the system runs at 28–33 FPS on a single GPU while achieving competitive lip-sync accuracy and strong emotion and motion expressivity—trained solely on the small HDTF dataset (357 videos).

## Strengths

- **Real-time performance is a genuine achievement.** XTalker runs at 28.21 FPS on an RTX 4090, more than twice the second-fastest competing method (Float at 14.17 FPS on A100 only; OOM on 4090). This is directly enabled by the compact parameter-space design and the MM-DiT network consuming only ~2% of the per-frame compute relative to LivePortrait's warping.
- **Systematic keypoint disentanglement analysis.** The paper provides quantitative evidence (Figures 1–2) that specific implicit keypoints in LivePortrait's representation correlate strongly with audio envelope dynamics, emotional state, and head pose. These empirical findings motivate the multi-head architecture and are not merely assumed.
- **Ablation study is thorough and informative.** Table 2 tests each head individually and jointly, evaluates the impact of DWA loss balancing, and examines noise initialization choices, giving a clear picture of each component's contribution.
- **Efficient training.** Competitive results on a 357-video corpus (HDTF) versus baselines trained on much larger datasets indicates the parameterized keypoint approach generalizes well in low-data regimes.
- **Identity preservation.** XTalker achieves the highest CSIM (0.9395) and lowest LPIPS (0.0432) among all baselines, demonstrating that the parameter-space approach preserves visual identity while animating.

## Weaknesses

### Fatal
None.

### Major

- **Evaluation unfairness on the two headline advantages.** XTalker's dominant margins in EmoACC and Head Motion Variance are obtained by providing *extra input modalities* (emotion labels and user-defined pose curves) that competing baselines do not receive. These baselines generate emotions and head motion purely from audio; XTalker receives an explicit emotion class and a hand-drawn or LLM-generated trajectory. Comparing raw metric scores across this input disparity conflates architectural capability with input privilege. The paper acknowledges the superiority of a "unified framework" over reference-image-based approaches, but does not caveat the table comparison accordingly. At minimum, baselines that accept analogous control inputs (SadTalker, which accepts pose parameters) should be compared under equivalent conditions, and the metric advantage attributable solely to extra conditioning should be quantified.

- **Lip-sync performance is meaningfully below the best baseline.** Float achieves Sync-C 1.0579 vs. XTalker's 0.7548—a ~38% gap—and Sync-D 8.0542 vs. 8.4644. The paper attributes this to limited training data, but this is speculative and untested (e.g., no experiment augmenting the training set or verifying performance scales with data). Given that lip-audio synchronization is the primary stated criterion for "expressivity," the gap deserves deeper analysis.

- **EmoACC metric validity is unclear.** EmoACC is measured by an off-the-shelf facial expression classifier ("Muru 2021") applied to generated frames, conditioned on XTalker's discrete emotion labels as ground truth. There is no evidence that the classifier's label space matches XTalker's emotion taxonomy, or that frame-level classifier accuracy reflects perceptual quality of emotional expressivity. A user study or at least classifier agreement rate on real emotional video would substantially strengthen this metric's credibility.

### Minor

- **LLM-guided curve-pose synthesis is underspecified in the main text.** Section 3.3 mentions that an LLM "processes predefined curves to produce Pose Expression" via a diagonal transform, but neither the LLM prompt design, the coordinate system, nor the nature of the curves are explained. Without this, the pose head cannot be understood as a standalone contribution.

- **The Emotion Expression Transformer training target acquisition is unclear.** It is stated that a pretrained Transformer converts source images into "emotion-conditioned counterparts," but where these counterpart images come from during training (text-to-image generation? manual curation?) is not explained in the main text.

- **Head Motion Variance as a metric rewards diversity uncritically.** A method that produces random, extreme head thrashing would score highly. The paper pairs it with cosine similarity in Figure 7, but Table 1 only reports variance without naturalness controls (e.g., acceleration smoothness beyond the reported Smooth metric).

### Trivial

- The training loss weights (50:1:1 for emotion:talking:pose) indicate a large imbalance; the rationale is not discussed.

## Nice-to-Haves

- Ablating the effect of training data scale (e.g., training on a subset of VFHQ or VoxCeleb2) would validate or refute the claim that good performance on HDTF reflects the parameter-space design rather than dataset-specific overfitting.
- A user study measuring perceived emotion accuracy, lip-sync naturalness, and head motion naturalness would significantly strengthen all three claimed axes of improvement.
- Reporting performance under a fair comparison where baselines are also provided emotion/pose reference signals (where possible) would make the quantitative table more credible.

## Novel Insights

The finding that the Y-axis displacement of two specific lip keypoints (K19-Y, K20-Y) in LivePortrait's implicit representation closely tracks the audio amplitude envelope—without any explicit supervision linking the two—is a genuinely useful empirical observation. It suggests that the contrastive self-supervised training of LivePortrait incidentally induces audio-correlated structure in the motion manifold, which is an interesting property that could motivate further analysis of what implicit representations in video generation models encode about physics and acoustics.

## Suggestions

- Add a controlled comparison in Table 1 where SadTalker and any other baselines that accept pose control are evaluated with equivalent pose driving signals.
- Provide a qualitative and quantitative breakdown of EmoACC using a second independent emotion classifier to test robustness.
- Clarify the LLM curve-synthesis pipeline with a concrete example (curve shape → pitch/yaw/roll sequence).
- Include failure cases—particularly for cross-lingual audio or non-frontal source images—to characterize the approach's boundary conditions.

## Score and Decision

XTalker is a practically motivated and well-engineered paper with a genuine real-time advantage and a clear disentanglement analysis. The core contributions—decomposing keypoint subspaces and building lightweight flow-matching heads on top of LivePortrait—are incremental but executed with care. The principal concern is that the two headline metric advantages (EmoACC, Head Motion Variance) involve an unacknowledged apples-to-oranges comparison, which overstates the improvement. The lip-sync gap versus the best baseline also remains unexplained. These issues reduce confidence in the paper's central quantitative claims, but do not invalidate the underlying engineering contribution or the disentanglement analysis.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>