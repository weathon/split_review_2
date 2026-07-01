## Summary

This paper introduces *Continuous Online Action Detection (COAD)*, a new task formulation where models not only detect actions in real-time but also continuously learn on-the-fly from streaming video without storing data or using multiple training passes. The authors curate Ego-OAD, a large-scale egocentric benchmark derived from Ego4D that provides 263 hours of video with 87 action classes and multi-label annotations. They propose a training strategy combining state continuity, orthogonal gradient projection, and non-uniform loss weighting, showing that COAD improves out-of-stream generalization by up to 7% Top-5 Recall and in-stream adaptation by up to 20% compared to a model without adaptation.

## Strengths

- **Novel task formulation**: COAD addresses an important gap in the OAD literature by enabling models to adapt during deployment on streaming video, which is crucial for real-world wearable devices. The formulation of single-pass, causal training with no data storage is well-motivated.
- **Large-scale benchmark contribution**: Ego-OAD fills a clear void—there is no existing large-scale egocentric OAD benchmark. The dataset is derived from Ego4D Moment Queries, is sizable (263h, 87 classes), and includes realistic multi-label overlap.
- **Thorough ablation study**: The paper systematically ablates each component of COAD (state continuity, orthogonal gradient, non-uniform loss) on the new benchmark, providing clear insight into their individual contributions and the trade-off between in-stream and out-of-stream performance.

## Weaknesses

### Major

1. **Lack of comparison to relevant single-pass continual learning methods**: The orthogonal gradient projection is compared only against a "w/o COAD" baseline that uses none of the proposed strategies. No comparisons are made to other single-pass continual learning techniques that do not require replay (e.g., online EWC, MAS, SI). Without these baselines, it is unclear whether the specific gradient projection is necessary or if any simple regularization would suffice.

2. **Unclear trade-off between in-stream and out-of-stream performance**: In Table 1 (Ego pretrain, in-stream), the full COAD achieves lower mAP (36.8) than the simpler "w/o COAD" baseline (39.0), while gaining in Top-5 Recall (89.3 vs 86.7). The paper frames this as "robust performance across domains," but in a personalized setting where adaptation to the user’s own stream is critical, losing 2.2 mAP is a concern. The analysis of stride/learning rate (Figure 3) does not resolve whether the optimal operating point for the user would favor the w/o COAD variant.

3. **Limited evaluation against state-of-the-art OAD architectures**: Only an RNN-based (GRU) detection head is evaluated. While the paper argues RNNs are suited for continuous learning, no experiment compares COAD to, for example, a lightweight Transformer adapted for continuous training. The claim that Transformers are unsuitable due to compute cost is not backed by any on-device measurement, and the community standard for OAD includes stronger Transformer models (LSTR, TeSTra). Without such comparisons, it is difficult to gauge the practical significance of the COAD formulation over simply retraining a stronger backbone.

### Minor

- EPIC-KITCHENS results are weak: COAD shows only marginal gains over Pretrained Only (e.g., Action mAP in-stream: 9.9 vs 8.6), and the w/o COAD baseline often underperforms the Pretrained Only. The paper attributes this to fine-grained labels, but this suggests the method may not generalize beyond coarse action classes. Additional analysis (e.g., class-wise performance) would help.
- The derivation of 87 unified action classes from free-form descriptions is described only briefly and the appendix containing grouping details is stripped from the main paper. The quality of these merges is not validated (no inter-annotator agreement or consistency metric).
- No computational profiling: The paper motivates COAD for resource-constrained devices but does not report FLOPs, peak memory, or inference latency, even on a simulated embedded setup.
- The orthogonal gradient projection uses only the immediately preceding gradient; more recent or a larger history could be considered, and the sensitivity to this choice is not explored.

### Trivial
- The section heading uses "CODA" (Section 4) while the paper otherwise uses "COAD"; minor inconsistency.

## Nice-to-Haves

- Comparison to single-pass continual learning baselines (online EWC, MAS, etc.) would strengthen the claim that orthogonal gradient projection is the right choice.
- A small experiment with a lightweight Transformer detection head under the COAD setting would broaden the contribution.
- On-device latency and memory measurements (even simulated) would make the deployment motivation more concrete.
- An analysis of annotation reliability on Ego-OAD (e.g., average number of annotators per video, label ambiguity rates) would build confidence in the benchmark.

## Novel Insights

The key insight is that **aligning the training dynamics with the inference dynamics**—maintaining hidden state continuity, performing single-pass updates, and decorrelating consecutive gradients—enables effective online adaptation from a weak offline pretrained model. The orthogonal gradient projection acts as a streaming-friendly regularizer that improves generalization without replay, and the non-uniform loss reduces the need for dense supervision. The paper also empirically demonstrates that egocentric pretraining (EgoVLP) provides a large advantage over exocentric pretraining for online egocentric action detection, which is not surprising but is now quantified on a large-scale benchmark.

## Suggestions

- Add comparisons to memory-free continual learning methods (e.g., online EWC, SI) as baselines to isolate the benefit of the orthogonal gradient projection.
- Provide a more detailed analysis of the in-stream vs. out-of-stream trade-off, perhaps by reporting a joint metric (e.g., harmonic mean) or by showing that the drop in in-stream mAP is accompanied by a reduction in overfitting (e.g., lower variance across runs).
- Include an evaluation of a state-of-the-art OAD Transformer backbone (e.g., LSTR) under the COAD setting, even if only on a smaller subset, to show the paradigm is not architecture-specific.
- Validate the Ego-OAD action-class grouping with a small human agreement study or by reporting the number of original free-form descriptions merged per class.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>