## Summary

The paper introduces *Continuous Online Action Detection* (COAD), a new task formulation where models not only perform online action detection but also continuously adapt from streaming video in a single pass without storing data. To support this task, the authors curate Ego-OAD, a large-scale egocentric OAD benchmark derived from Ego4D Moment Queries. They propose training strategies—state continuity, orthogonal gradient projection, and non-uniform loss weighting—that improve both adaptation to the current video stream and generalization to unseen scenarios. Experiments on Ego-OAD and EPIC-KITCHENS show that COAD boosts top-5 recall on in-stream data by up to 22.5% and on out-of-stream data by up to 6.9% relative to a pretrained-only baseline.

## Strengths

- **Novel and well-motivated problem formulation.** COAD bridges a clear gap between offline-trained OAD models and the real-world requirement for on-device, post-deployment adaptation on wearable devices. The motivation from egocentric video dynamics and hardware constraints is compelling.
- **New large-scale benchmark.** Ego-OAD provides 263 hours of egocentric video with multi-label, temporally grounded annotations across 87 classes, derived from Ego4D. This fills the lack of egocentric OAD datasets and supports future research.
- **Clean experimental protocol and analysis.** The evaluation follows a principled three-way split (pretraining, in-stream, out-of-stream) to disentangle adaptation and generalization. Ablation studies on each component (state continuity, orthogonal gradient, non-uniform loss) are thorough and informative.
- **Meaningful quantitative gains on out-of-stream generalization.** COAD consistently improves out-of-stream top-5 recall over the w/o COAD baseline (e.g., +4.4% on Ego-OAD with egocentric pretraining), indicating better generalization to unseen data.

## Weaknesses

### Major

- **Missing comparison to standard OAD models.** The paper compares only to its own baselines (pretrained only and w/o COAD). It does not evaluate whether a strong, offline-trained OAD model (e.g., LSTR, TeSTra, MiniROD) applied online without adaptation would already achieve better performance than COAD. Without this comparison, it is unclear whether the adaptation gains are significant relative to the existing state of the art in OAD, or simply reflect a weak base model.
- **In-stream mAP degradation for COAD.** On Ego-OAD with egocentric pretraining, COAD achieves lower in-stream mAP (36.8) than the w/o COAD baseline (39.0), despite higher top-5 recall. This suggests a precision-recall tradeoff or over-regularization that is not adequately discussed or explained. The claim that COAD “maintains robust performance across both domains” is weakened by this mAP drop.
- **Limited effectiveness on EPIC-KITCHENS.** Results on EPIC-KITCHENS are mixed: in several cases COAD underperforms the pretrained-only baseline (e.g., Action mAP out-of-stream: 7.9 vs 9.6). The paper attributes this to fine-grained annotations, but it raises questions about the general applicability of COAD to domains with less recurring patterns. A deeper analysis or failure case study is needed.

### Minor

- **Orthogonal gradient projection is short-sighted.** The projection only uses the immediately preceding gradient, ignoring longer-range decorrelation. While this is stated, the paper does not discuss why this choice is sufficient or whether longer sequences would help.
- **Storage claim is slightly overstated.** The method requires storing the previous gradient vector for orthogonal projection, which has memory equal to the model parameter count. This is acceptable but should be acknowledged as a mild deviation from “without storing data.”
- **Inconsistency in abbreviation.** Section 4.5 introduces “Continuous OAD (CODA)” but the rest of the paper uses “COAD.” This is a minor editorial issue.

### Trivial

- Figure 2’s caption in the extracted PDF appears duplicated and could be cleaner in the final version.

## Nice-to-Haves

- Compare against at least one strong offline OAD model (e.g., LSTR or TeSTra) applied without adaptation on the out-of-stream split, to contextualize the gains.
- Provide a more detailed analysis of the in-stream mAP drop, including per-class precision and recall changes, to clarify whether the tradeoff is systematic.
- Evaluate the orthogonal gradient with a longer history (e.g., projection onto the span of the last $k$ gradients) to test whether short-sightedness limits adaptation.
- Report confidence intervals or variance over multiple runs with different random seeds, as some results (e.g., EPIC-KITCHENS) show substantial variability.

## Novel Insights

None beyond the paper’s own contributions. The key observations—that continuous adaptation on a stream can improve generalization without catastrophic forgetting, that state continuity matters, and that gradient decorrelation helps—are reasonable but individually known from the continuous learning literature; the novelty lies in combining them for OAD and in the specific training strategies.

## Suggestions

1. Add standard OAD baselines (e.g., LSTR, TeSTra, MiniROD offline) on Ego-OAD for out-of-stream evaluation to demonstrate that COAD adds value beyond strong offline models.
2. Investigate and explain the in-stream mAP drop—report mAP@k or analyze class-level precision/recall to determine whether the non-uniform loss or orthogonal projection biases predictions.
3. On EPIC-KITCHENS, consider whether the COAD training hyperparameters (learning rate, stride) need tuning for fine-grained actions; a sensitivity analysis would strengthen the claims.

## Score and Decision

MY FINAL SCORE: 4.0score>
MY FINAL DECISION: Rejectdecision>