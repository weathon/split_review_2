Now I have all the information I need. Let me compile my final review.

## Summary

The paper introduces Continuous Online Action Detection (COAD), combining online action detection with single-pass, no-replay continual learning from streaming video — motivated by egocentric wearable device deployment. It curates Ego-OAD (87 classes, 22,991 instances, 263h) from Ego4D MQ, and proposes a method using state continuity, orthogonal gradient projection (Han et al., 2025), and non-uniform loss (An et al., 2023).

## Strengths

1. **Novel task formulation (COAD) that fills a genuine gap.** The paper identifies that standard OAD models are trained offline on shuffled data but deployed online on streaming video, and formalizes a task that enforces single-pass, causal, no-replay adaptation. This is clearly described (Sec 4) and well-motivated for egocentric/wearable AI.

2. **Ego-OAD dataset is a substantial resource.** Curated from Ego4D MQ, it offers 87 fine-grained classes, 22,991 instances, 263h of egocentric video, multi-label annotations with 36% overlap — significantly larger and more diverse than existing egocentric OAD benchmarks. The manual grouping and multi-annotator merging (Appendix A) are sound practices.

3. **Informative ablation study.** Table 3 provides a full 2×2×2 ablation isolating each component: orthogonal gradient improves out-of-stream Top-5 Recall by 4.5% over the variant without it; non-uniform loss improves out-of-stream mAP by 4.2%. This granular attribution is stronger than typical "full vs none" ablations.

4. **Systematic exploration of the adaptation-generalization trade-off.** Figure 3 varies stride and learning rate to map the Pareto frontier, and the finding that improvement is possible even at stride 128 (loss once per ~68 seconds) provides practical guidance for deployment with sparse supervision.

5. **Clean finding about egocentric vs. exocentric pretraining.** Table 1 and Table 4 consistently show egocentric pretraining dominates exocentric for egocentric OAD, a reproducible result with practical implications.

## Weaknesses

### Fatal
None.

### Major

1. **Method contribution is thin — all components explicitly attributed to prior work, with no identified novelty.** The method (Sec 4.5) has three components: non-uniform loss from An et al. (2023, MiniROD), orthogonal gradient projection from Han et al. (2025), and state continuity (the default RNN behavior when windows are not shuffled). The paper never identifies what *it* proposes algorithmically beyond assembling existing pieces. Claiming "effective training strategies tailored to COAD" (contribution list, line 29) overstates the contribution. The paper would be more honest if framed primarily as a dataset/benchmark contribution with a reasonable baseline method.

2. **Missing comparison to standard continual learning approaches.** The only baselines are "Pretrained Only" and "w/o COAD" (naive continuous training). There is no comparison to established continual learning methods — e.g., Elastic Weight Consolidation (EWC), Synaptic Intelligence, or even a small replay buffer — which are directly applicable to this setting. The orthogonal gradient projection is one specific approach to preventing catastrophic forgetting, but the paper does not show it is competitive with alternatives.

3. **Headline numbers in the abstract are misleading.** The claimed "up to 20% / 7%" improvements compare COAD (trained on 1,177 in-stream videos) against "Pretrained Only" (trained on 186 videos) — a 6:1 data ratio. The more honest comparison, COAD vs. w/o COAD (both seeing 1,177 videos), yields gains of ~3.8 percentage points (in-stream Top-5) and ~4.4 points (out-of-stream Top-5). The abstract does not acknowledge this context.

4. **In-stream (adaptation) mAP does not favor COAD.** On Ego-OAD with egocentric pretraining (Table 1), w/o COAD achieves higher in-stream mAP (39.0) than COAD (36.8). On EPIC-KITCHENS, the in-stream Action mAP results are inconsistent. The paper acknowledges the trade-off (line 186-188), but the fact that the method sometimes degrades the adaptation it claims to enable weakens the narrative.

### Minor

1. **Data scale confound not properly isolated.** The pretraining set (186 videos) is much smaller than the in-stream set (1,177 videos). An offline IID model trained on all 1,363 videos would almost certainly provide a tighter upper bound. The "IID Training" baseline appears only in Figure 4 (without numeric values) rather than as a numbered row in the main tables, making it hard to assess what fraction of offline performance the online method recovers.

2. **EPIC-KITCHENS results are mixed and not fully explained.** While the paper attributes difficulties to "the fine-grained nature of the actions," it provides no supporting analysis. The out-of-stream Action mAP (9.9) is modestly better than Pretrained Only (8.6), but the in-stream Action mAP (7.9) is below Pretrained Only (9.6) despite the latter never seeing in-stream data. The paper's explanation is asserted, not evidenced.

3. **Missing statistical significance.** No variances, confidence intervals, or multiple-seed runs are reported. Given modest differences (e.g., 26.0 vs. 25.5 mAP, or 39.0 vs. 36.8), it is unclear whether the reported gains are within noise.

### Trivial
- Contribution list: "Countinuous" should be "Continuous" (line 27).

## Nice-to-Haves
- Report computational cost (FLOPs, runtime, memory) to support the claimed suitability for resource-constrained deployment.
- Include the IID offline upper bound as a numbered row in the main results tables.
- Discuss the limitation that only the GRU detection head is adapted (frozen backbone), which limits the scope of possible adaptation.
- Provide more details on the "w/o COAD" baseline protocol (does it reset hidden states? does it compute loss at every step?).

## Removed Points

**The following points from the Harsh Critic are removed with justification:**

- **Criticism about out-of-stream Action mAP on EPIC-KITCHENS (Harsh Critic point #5).** The critic claimed "COAD's out-of-stream result (7.9 mAP) is worse than Pretrained Only (9.6 mAP)." This is a factual error: the table format is "out/in" so 7.9 is the *in-stream* value, and COAD's *out-of-stream* Action mAP (9.9) is actually *better* than Pretrained Only (8.6). The broader point about mixed EPIC-KITCHENS results remains valid and is kept in Minor.

- **Claim that "no comparison to any existing OAD method" is a decisive weakness.** This is weakened because existing OAD methods (LSTR, TeSTra, etc.) are designed for offline training + online inference, not online adaptation. Adapting them to the COAD setting is non-trivial and the paper's scope is justified. However, the missing continual learning baselines (EWC, replay) is a genuine gap, kept in Major.

- **Criticism about "w/o COAD baseline is underspecified"** — removed as a nitpick. The baseline is described as "without applying any of the proposed strategies" which is sufficiently clear for an ablation baseline. The detail is moved to Nice-to-Haves.

- **Generic speculation about method novelty being "zero"** — softened. The combination of existing techniques applied to a new task is a modest contribution. The criticism is retained as Major (point 1) but reworded to accurately reflect that the paper does not identify what is new.

- **Strength Finder's strengths about "important problem" and "timely" framing** — removed as generic/superficial. Only concrete, specific strengths are kept.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface any observation about the paper that the authors themselves do not make. The calibration search was unavailable, so no comparative novelty assessment across the reviewer corpus is possible.

## Suggestions

1. **Reframe the paper's contribution.** The Ego-OAD dataset and COAD task formulation are the strongest contributions. The method should be presented as a reasonable baseline for the new benchmark, not as a novel algorithmic contribution. This would align the paper's claims with what it actually demonstrates.

2. **Add at least two continual learning baselines** (e.g., EWC and a small replay buffer) to the comparison tables. Without these, the claimed effectiveness of the orthogonal gradient projection cannot be assessed relative to standard alternatives.

3. **Report the IID offline upper bound as a numbered row** in the main results table, with actual numeric values. This gives readers a clear reference point for what fraction of offline performance is recovered.

4. **Reconcile the abstract's claims with the actual comparisons.** Either present the gains over w/o COAD (not Pretrained Only) in the abstract, or at minimum acknowledge that the "up to 20%" number reflects comparison against a baseline trained on 86% less data.

5. **Run experiments with multiple random seeds** and report standard deviations or confidence intervals, especially for comparisons where the differences are modest (1–5 points).

## Score and Decision

Without calibration anchors (the calibration tool was unavailable), I calibrate against my knowledge of ICLR standards and the paper's internal evidence. The paper has two genuine contributions (task formulation, dataset) that would merit consideration, but it overclaims the method contribution (all components from prior work, none identified as new) and the evaluation has significant gaps (missing continual learning baselines, misleading abstract numbers, mixed in-stream results). A score of **5** reflects a borderline paper: valuable contributions weakened by overstated claims and incomplete evaluation. The authors could realistically address the major concerns with additional baselines and reframing, but the paper in its current form does not convincingly deliver on all its claims.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>