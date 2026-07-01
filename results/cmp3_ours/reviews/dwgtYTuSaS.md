Now I have sufficient calibration. Let me write the final review.

## Summary

This paper introduces Continuous Online Action Detection (COAD), a new task formulation where OAD models not only perform online detection but also continuously adapt from streaming video in a single pass without storing training data. The authors curate Ego-OAD, a large-scale egocentric OAD benchmark (87 classes, 22,991 instances, 263h of video) from Ego4D Moment Queries, and propose training strategies (state continuity, orthogonal gradient projection, non-uniform loss) adapted to the streaming setting. Results show modest out-of-stream generalization gains but mixed in-stream adaptation performance.

## Strengths

1. **Well-motivated task formulation (Sections 1, 4).** The COAD problem — online action detection combined with continuous on-the-fly adaptation — is genuinely useful and timely. The paper correctly identifies that offline-trained OAD models will struggle in deployment on wearable devices and connects this to the emerging on-device training paradigm (Zhu et al., 2024; Carreira et al., 2024a).

2. **Ego-OAD fills a genuine gap (Section 3).** No large-scale egocentric OAD benchmark existed previously. The curation is reasonable: 87 classes, 22,991 instances, 263h of video from Ego4D's Moment Queries, with multi-label temporally-grounded annotations, and manual grouping of semantically similar free-form descriptions into unified classes.

3. **Clean experimental protocol (Section 5.1).** The three-way split (pretraining / in-stream / out-of-stream) following Carreira et al. (2024a) cleanly separates initial offline learning from continuous adaptation and held-out generalization evaluation.

4. **Transparent ablation study (Table 3).** The paper systematically ablates each component and reports both in-stream and out-of-stream metrics, allowing readers to assess each component's contribution honestly.

## Weaknesses

### Major

1. **Mixed results on the primary metric (mAP) weaken the headline claims.** On Ego-OAD with egocentric pretraining, COAD loses on in-stream mAP (36.8 vs 39.0 for w/o COAD) while the out-of-stream mAP advantage is only 0.5 points (26.0 vs 25.5). The paper's headline "up to 7% generalization improvement" refers to Top-5 Recall, not mAP — the community-standard metric the paper itself adopts (it cites prior OAD work using per-frame mAP). The abstract claims improvements in both adaptation and generalization, but the adaptation improvement is on Top-5 accuracy while mAP shows COAD underperforms on in-stream data. The paper acknowledges this trade-off (line 186), but the abstract and contributions list frame the results more favorably than the mAP numbers warrant.

2. **IID Training upper bound only appears visually, not numerically in main tables.** The paper mentions an "IID Training" baseline (offline training with multiple passes over pretraining + in-stream data) and shows it in Figure 4, but does not report explicit numerical values in the main results tables (Table 1, Table 2). Without knowing the gap between COAD (26.0 out-of-stream mAP) and this upper bound, the reader cannot assess whether the continuous learning approach is competitive with standard offline training. This is the single most informative reference point for the paper's central claim.

3. **Weak results on EPIC-KITCHENS limit claimed generality.** On EPIC-KITCHENS (Table 2), COAD's out-of-stream Action mAP (9.9) barely improves over Pretrained Only (8.6), and its in-stream Action mAP (7.9) is *worse* than Pretrained Only (9.6). The w/o COAD baseline also underperforms Pretrained Only on most metrics, suggesting the dataset itself may be poorly suited for continuous adaptation. The paper attributes this to "the fine-grained nature of the actions and annotations" in a single sentence at the end of Section 5.3 — a real limitation that deserves more prominent discussion and analysis.

### Minor

4. **Method novelty is primarily in the task formulation and benchmark, not the training strategies.** The three proposed components are directly adapted from prior work: orthogonal gradient projection from Han et al. (2025, Eq. 3), non-uniform loss weighting from An et al. (2023), and state continuity is a standard RNN property. The paper frames these as "effective training strategies tailored to COAD" (contributions), which is reasonable for a task-and-benchmark paper but overstates algorithmic novelty.

5. **"Without storing data" claim (abstract, line 9) is slightly overstated.** The orthogonal gradient projection requires storing the previous gradient vector g_{t-1}, and the RNN hidden state is retained across windows. While small and the intent refers to not storing training data, the phrasing could mislead.

6. **No variance or statistical significance reported.** All results are single-run numbers. For a multi-label dataset with 87 classes, run-to-run variance could be non-trivial.

7. **No computational cost analysis despite wearable-device motivation.** The paper motivates COAD for resource-constrained wearable devices but provides no FLOPs, parameter counts, or latency measurements. The TimeSformer backbone is computationally heavy, making it unclear whether the total system is feasible for on-device deployment.

### Trivial

8. Table 2's "(out/in)" column notation is subtle and took multiple reads to parse. Figure 5 shows only the top-1 predicted class, which is not very informative for a multi-label setting with 87 classes.

## Nice-to-Haves

- Compare COAD against a strong offline-trained OAD method (e.g., LSTR, TeSTra) on Ego-OAD to benchmark the new dataset.
- Analyze why COAD loses in-stream mAP but improves Top-5 Recall — this pattern likely reveals how the method trades off rare-class recall for common-class ranking.
- Explore longer-range gradient decorrelation (beyond the immediately preceding window).

## Removed Points

These points from the harsh critic were removed after verification against the paper:

1. **"Single-pass training with overlapping windows is a form of data reuse."** — The paper states "each window is processed exactly once," which is true. Overlaps are inherent to sliding-window processing in OAD and standard in the field. REMOVED as a non-issue.

2. **"State continuity ablation shows negligible difference (0.1 mAP)."** — The paper characterizes this as "a smaller but consistent gain," which is an honest description of the measured 0.1 mAP difference. The paper does not overclaim this component. REMOVED as not a genuine weakness.

3. **"The pretraining split has only 186 videos, so gains are partly driven by having more data."** — This concern is already fully addressed by Weakness #2 (missing IID Training baseline numbers). The w/o COAD baseline also sees the same in-stream data, controlling for data quantity. MERGED into Weakness #2.

4. **"Orthogonal gradient only decorrelates from the immediately preceding window."** — This is a design choice, not a flaw. The paper could explore longer-range decorrelation, but its absence is not a weakness. MOVED to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Report the IID Training upper bound as explicit numerical values in the main results table (Table 1).
- Add variance over multiple runs for the main results.
- Include a detailed per-class breakdown analysis of the in-stream mAP degradation.
- Add latency/memory measurements for the full system on edge-relevant hardware.

## Score and Decision

**Bracketing rationale:** Round 1 calibration retrieved anchors across all score bands. In the 3.5–5.5 band (avg 4.0–4.8), papers such as *PrAViC* (4.25, Reject) and *Actions-to-Action* (4.40, Reject) had similar concerns: limited method novelty, missing baselines, overstated claims. In the 5.5–7.5 band (avg 6.0–7.0), egocentric papers such as *Test-Time Adaptation for Missing Modalities* (6.0, Accept) and *Hand-Object Dynamics* (6.0, Accept) had stronger experimental evidence and clearer contributions. Our paper sits between these bands: the task formulation and dataset are genuine contributions beyond what the 4.25–4.80 papers offer, but the mixed experimental results and modest mAP gains do not reach the evidentiary standard of the 6.0 papers.

**Anchor papers consulted:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/jawV7vhGHw.md` (PrAViC, 4.25, Round 1) — similar online-adaptation framing but weaker task contribution; our paper has stronger task-formulation novelty.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/dl34rOnbqJ.md` (Actions-to-Action, 4.40, Round 1) — similar egocentric video + method novelty concerns; our paper has a stronger dataset contribution.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/1L52bHEL5d.md` (MiDl, 6.00, Round 1) — cleaner experimental story and clearer method contribution than our paper.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/P6G1Z6jkf3.md` (Hand-Object Dynamics, 6.00, Round 1) — stronger experimental results (SOTA on multiple benchmarks) than our paper.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/AfZH9EEuRR.md` (EgoQR, 2.20, Round 1) — weaker paper on a different egocentric task; not directly comparable.

**Final score:** 5.0 — the paper introduces a worthwhile new task and a needed dataset, but the experimental evidence for the proposed method is mixed, and the method's components are largely adapted from prior work. The paper's claims would benefit from calibration to the actual mAP numbers.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>