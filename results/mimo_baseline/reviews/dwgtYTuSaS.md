## Summary

This paper introduces Continuous Online Action Detection (COAD), a new task formulation where models perform online action detection while simultaneously learning from continuous video streams in a single pass, without data storage or replay. The authors curate Ego-OAD, a large-scale egocentric benchmark derived from Ego4D, and propose training strategies—state continuity, orthogonal gradient projection, and non-uniform loss—that improve both adaptation to individual users (up to 20% top-5 recall on in-stream) and generalization to unseen environments (up to 7% on out-of-stream).

## Strengths

- **Well-motivated task formulation**: COAD is a natural and practically important extension of standard OAD for wearable egocentric devices. The paper clearly articulates why existing offline-trained OAD models are insufficient for real-world deployment where environments, users, and tasks evolve. The connection to on-device, resource-constrained settings is compelling.

- **Useful benchmark contribution**: Ego-OAD provides a large-scale, diverse egocentric benchmark for online action detection with 87 action classes, 22,991 action instances, and 263 hours of video. The curation process (merging annotation passes, grouping semantically similar actions) is reasonable and the multi-label temporal annotation structure is appropriate for realistic OAD.

- **Thorough ablation study**: Table 3 provides a systematic component-level analysis, and Figure 3 offers insightful analysis of the adaptation-generalization trade-off under varying hyperparameters. The finding that COAD can improve with very sparse supervision (stride 128, ~68 seconds between updates) is particularly interesting and practically relevant.

## Weaknesses

### Fatal
None.

### Major

- **Severely limited baselines**: The paper only compares against two baselines: "Pretrained Only" (no adaptation) and "w/o COAD" (continuous training without the proposed techniques). There are no comparisons against other continual learning methods (e.g., experience replay, EWC, GEM, or other gradient projection approaches from Han et al. 2025 or beyond). This makes it impossible to determine whether the improvements stem from the specific proposed techniques or simply from any form of continual adaptation. A reader cannot assess the marginal value of orthogonal gradient projection versus, say, a simple learning rate schedule or elastic weight consolidation.

- **Mixed and concerning EPIC-KITCHENS results**: On the most important metric (Action mAP and Top-5 Recall in-stream), COAD underperforms Pretrained Only (7.9 vs 9.6 mAP, 20.5 vs 22.9 top-5). The authors attribute this to "fine-grained nature of the actions," but this is a significant weakness since EPIC-KITCHENS is the primary egocentric action benchmark in the field. If COAD cannot adapt on more complex action spaces, the generalizability of the approach is questionable. The Table 2 caption also appears to have an error where "out/in" results are reported in an unusual column format that mixes verb/noun/action.

- **In-stream improvements may reflect overfitting, not meaningful adaptation**: In Table 1, the "w/o COAD" baseline achieves higher in-stream mAP than COAD (39.0 vs 36.8 for ego; 31.0 vs 31.0 for exo), while COAD achieves better top-5 recall. This trade-off suggests that the orthogonal gradient and non-uniform loss primarily serve as regularization rather than enabling better learning, which partially undermines the narrative that COAD "learns" from the stream effectively.

### Minor

- **The "up to 20%" claim in the abstract is misleading**: This figure comes from the in-stream exocentric top-5 recall improvement (57.5 → 80.0 = 22.5 percentage points). However, the abstract says "improves adaptation to the user's environment by up to 20% in top-5 accuracy," and the more meaningful out-of-stream improvements are 6.5–6.9 percentage points. The abstract should be more precise about which setting the headline numbers come from.

- **RNN choice is under-justified**: While the paper mentions targeting resource-constrained devices, no computational cost comparisons are provided against Transformer-based OAD methods (LSTR, TeSTra). Without concrete FLOPs, memory, or latency numbers, the efficiency argument remains unsubstantiated.

- **Dataset split sizes are imbalanced**: The pretraining set has only 186 videos while in-stream has 1,177. This means the "pretrained only" baseline is trained on a very small fraction of data, which may exaggerate the benefits of any subsequent adaptation.

## Nice-to-Haves

- Comparison against at least one prior continual learning baseline (e.g., experience replay with limited memory, EWC) to validate that the specific COAD techniques provide value over generic continual learning.
- Computational cost analysis (FLOPs, memory, latency) to substantiate the efficiency claims for wearable deployment.
- Analysis of per-class performance to understand which action categories benefit most from continuous learning.

## Novel Insights

The paper's most novel observation is that a model can meaningfully improve generalization through single-pass continuous training on non-IID video streams, even with very sparse supervision (one gradient update every ~68 seconds). This finding, demonstrated in Figure 3 and the stride ablation, suggests that continuous video streams carry sufficient structural regularity for learning without the IID assumptions of standard training. Additionally, the finding that orthogonal gradient projection helps more with generalization than adaptation (Table 3) suggests that gradient decorrelation acts primarily as a regularizer against stream-specific biases rather than enabling more efficient learning.

## Suggestions

- Add at least 2-3 continual learning baselines (e.g., experience replay with small buffer, EWC, and a method from Han et al. 2025 beyond just the gradient projection) to properly contextualize COAD's contribution.
- Fix the EPIC-KITCHENS table formatting and provide per-category analysis to understand why COAD struggles on fine-grained action recognition.
- Provide concrete computational cost numbers (FLOPs, memory footprint, inference latency) to justify the RNN-based design choice for wearable devices.
- Calibrate the abstract's headline claims to accurately reflect the out-of-stream generalization improvements rather than the in-stream numbers.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: Reject