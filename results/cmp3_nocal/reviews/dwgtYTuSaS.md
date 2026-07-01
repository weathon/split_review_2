I have verified the key claims against the paper. Let me now write the final consolidated review.

## Summary

This paper introduces Continuous Online Action Detection (COAD), a task formulation where OAD models continue to learn from streaming video after deployment, without storing data or requiring multiple passes. The authors curate Ego-OAD, a large-scale egocentric OAD benchmark (87 classes, ~23K instances, 263 hours) derived from Ego4D Moment Queries. The method combines state-continuous RNN training, orthogonal gradient projection (Han et al., 2025), and non-uniform loss weighting (An et al., 2023). Results show improved out-of-stream generalization but a drop in in-stream mAP relative to a simple adaptation baseline.

## Strengths

1. **Ego-OAD dataset fills a genuine gap.** There is a shortage of egocentric OAD benchmarks. Repurposing Ego4D's Moment Queries split into a 263-hour, 87-class, multi-label, temporally grounded OAD benchmark with overlapping actions (36% of instances) is a concrete contribution that the community can build on regardless of the method's outcome.

2. **Problem framing is timely and well-motivated.** Standard OAD models are trained offline on IID data but deployed in streaming environments with shifting user behaviors. The paper clearly articulates why this gap matters for wearable/egocentric AI and why continuous adaptation is the natural direction.

3. **Clean, systematic ablation study.** Table 3 tests each proposed component alone and in combination, honestly revealing trade-offs (e.g., uniform loss yields the highest in-stream mAP but hurts out-of-stream generalization). The ablation enables readers to understand what each component contributes and at what cost.

## Weaknesses

### Fatal
None.

### Major

1. **In-stream mAP degradation is not adequately addressed.** On Ego-OAD with egocentric pretraining, the full COAD method achieves **36.8** in-stream mAP, while the simpler w/o COAD baseline (same model, trained on the stream without the three proposed components) achieves **39.0**. The ablation deepens this concern: the "w/o COAD + uniform loss" variant (state cont. ✓, orth. grad. ✓, non-uniform loss ✗) hits **42.4** in-stream mAP — the highest in the table. The paper acknowledges this obliquely ("the baseline achieves competitive results") and frames it as a desirable trade-off, but does not squarely confront the implication: the proposed components, especially the non-uniform loss, actively suppress in-stream adaptation. Since adaptation to the user's own stream is a core part of the COAD framing, this trade-off needs far more rigorous justification than the paper provides.

2. **No variance or statistical significance reporting.** The main out-of-stream mAP gap between COAD and w/o COAD on Ego-OAD is **0.5 points** (26.0 vs 25.5). This is reported from what appears to be a single run with no standard deviations, confidence intervals, or multi-seed experiments. A 0.5 mAP difference at this scale could easily be noise. Every table in the paper has this problem. This is the single most important missing piece for evaluating the method claims.

3. **EPIC-KITCHENS results are mixed and the explanation is insufficient.** On several in-stream metrics, COAD underperforms simple "Pretrained Only" (no adaptation at all). For example, in-stream Action mAP: Pretrained Only 9.6 > COAD 7.9. On in-stream Verb mAP, COAD (29.0) merely ties Pretrained Only (29.0). The paper attributes this to "the fine-grained nature of the actions and annotations in EPIC-KITCHENS," but this post-hoc explanation does not establish whether the method's design is fundamentally limited on fine-grained action hierarchies — a common property of real-world action detection. The results do not provide supporting evidence for the method's effectiveness.

### Minor

1. **Limited technical novelty in the method components.** The three training strategies are each drawn directly from prior work with no reported modification: orthogonal gradient projection from Han et al. (2025) (Eq. 1 is a direct citation), non-uniform loss from An et al. (2023), and the evaluation protocol from Carreira et al. (2024a). State continuity is standard RNN behavior applied during training rather than only at inference. The contribution is primarily *integrative* — applying a known combination to a new OAD setting. This is legitimate but should be framed more precisely rather than as a "novel task formulation."

2. **Missing comparisons to standard continual learning baselines.** The paper compares only against "Pretrained Only" and "w/o COAD" (the method minus its three components). It does not compare against established continual learning approaches compatible with the setting (e.g., EWC, SI, weight regularization methods that do not require replay or data storage). Without these, it is unclear whether the specific COAD components drive the generalization improvements, or whether any regularized continued training procedure would yield similar results.

3. **The orthogonal gradient projection uses only the immediately preceding gradient.** Eq. (1) projects \(g_t\) to be orthogonal to \(g_{t-1}\) only. The paper does not justify why a single-step memory window is sufficient for decorrelation, nor whether a buffer of recent gradients would be more effective. This design choice is not ablated.

### Trivial
- Naming inconsistency: The method is introduced as "CODA" (line 66) but referred to as "COAD" everywhere else including the title and abstract.
- Typo: "Countinuous" instead of "Continuous" in the contribution list (line 27).

## Nice-to-Haves

- An analysis of gradient cosine similarity over time (with and without the orthogonal projection) would substantiate the claimed decorrelation mechanism.
- Given the wearable device motivation, a resource footprint analysis (model size, memory for gradient storage, throughput) would strengthen the framing, though it is not required for the core contribution.
- The manual grouping of Ego4D descriptions into unified classes (Appendix A) is an important curation step; a validation or inter-annotator agreement measure would increase confidence in the benchmark quality.

## Removed Points

These points were flagged in the input review but are removed with justification:

- *Criticism about the "no data storage" constraint not being enforced because of pre-extracted features / g_{t-1} storage.* **Removed:** Pre-extracted features are standard practice in OAD research. The "no data storage" constraint refers to not storing raw video for replay/multiple epochs. Storing a single gradient vector is negligible. This criticism misreads the paper's stated constraint.

- *Criticism that qualitative results (Fig. 5) showing only top-1 predictions is misleading.* **Removed:** Showing only the argmax class in qualitative visualizations is standard practice and is explicitly noted in the caption.

- *General speculation about label ambiguity in Ego-OAD and Appendix A quality.* **Removed:** The paper acknowledges the label amplification and describes its mitigation strategy. The appendix is referenced; its content cannot be judged from the main paper alone.

- *Claims about missing related works.* **Removed:** Per guidelines, I cannot verify missing related work claims.

- *The framing that "up to 20% improvement" in the abstract omits the mAP trade-off.* **Removed:** Abstracts are summaries; a 2.2-point mAP drop on one metric alongside a 16-point Top-5 Recall gain on another is a reasonable trade-off to mention selectively in a summary. The full results are transparent in the tables.

- *Strength about "timely and well-motivated problem framing" being generic.* **Kept as a strength** because the paper concretely ties the motivation to the IID-offline vs. streaming-deployment gap, which is specific and well-articulated.

## Novel Insights

The key insight from the review process is that the paper's components operate in tension with each other in ways the paper does not fully analyze: the non-uniform loss (from An et al., 2023) appears to be the primary driver of in-stream mAP degradation (compare ablation rows: removing it boosts in-stream mAP from 36.8 to 42.4 while only modestly hurting out-of-stream generalization), yet the paper highlights it as a benefit. A more nuanced analysis of this specific trade-off — and whether a Pareto-optimal configuration exists — would either strengthen or refine the method's core claim. The ablation reveals that different components serve different regimes (in-stream vs. out-of-stream), and the paper's "balancing" narrative would be stronger if it explicitly characterized this as a controllable hyperparameter rather than a fixed method.

## Suggestions

1. Report all main results with at least 3 random seeds and include standard deviations or confidence intervals. The 0.5 mAP out-of-stream gap cannot be interpreted without this.

2. Directly analyze and discuss the in-stream mAP degradation. If the trade-off is inherent and necessary for generalization, show this explicitly (e.g., a Pareto curve over component configurations). If the non-uniform loss is the culprit, consider whether a softer version or a different loss weighting can recover in-stream performance.

3. Add comparisons to at least one standard continual learning baseline compatible with the no-replay constraint (e.g., EWC, SI, or simple L2 regularization during fine-tuning).

4. Clarify in Section 4 that the components are applications of prior techniques to the OAD setting and state what, if anything, was modified. The current text ("we apply...") is accurate but undersells or overstates the novelty depending on how the reader interprets it.

## Score and Decision

The Ego-OAD dataset and the problem framing are solid contributions. The ablation study is informative and honestly presented. However, the method has a clearly documented weakness (degraded in-stream adaptation with modest out-of-stream gains), the key results lack variance estimates, and the technical novelty is primarily integrative. In its current form, the evidence does not convincingly demonstrate that the specific COAD components are beneficial relative to simpler alternatives.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>