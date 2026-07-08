Now let me produce the final consolidated review.

## Summary

This paper presents VIBEFACE, a video and image biometric dataset designed specifically for electronic Know Your Client (eKYC) face verification scenarios. The dataset comprises 2,250 images and 1,550 videos from 50 subjects, balanced across gender, race, and age, captured under five lighting/occlusion conditions using three consumer smartphones. The authors evaluate two benchmark tasks (face detection and face verification) using pre-trained models and report demographic performance analyses.

## Strengths

- **Genuine gap targeted.** The paper identifies a real blind spot in existing face datasets: eKYC workflows with specific actions (head turning, blinking, mouth opening, face touching). No earlier dataset in the comparison table (Table 1) includes an "eKYC" column checked, and the scenario design (Section 3.2, scenarios 12–18) is clearly motivated by real authentication procedures used in financial and regulatory settings.

- **Ethically rigorous collection.** The dataset was collected with informed consent, GDPR compliance, anonymized identifiers, controlled-access licensing, and the right to withdraw (Section 3.4). This stands in genuine contrast to large-scale datasets like MS-Celeb-1M and VGGFace2 that were web-scraped without consent and have been withdrawn.

- **Deliberate demographic balance.** The dataset achieves 50:50 gender balance (25M, 25F), near-uniform racial distribution (~25% per group across four categories), and coverage across three age bands (18–30, 31–50, 51–70). This is documented in Figure 1 and Section 3.1, and it is better than most existing biometric datasets of comparable size.

- **Multi-condition acquisition.** Five sessions (artificial light, flash, glasses, natural light, weak natural light) with three camera devices and multiple pose/angle variations (Section 3.3, Table 2) create genuine diversity in capture conditions.

## Weaknesses

### Fatal
None.

### Major

- **50 subjects is insufficient for the fairness-and-benchmark claims the paper makes.** With 13 African, 13 Caucasian, 12 East Asian, and 12 South Asian participants (Section 3.1), any demographic comparison—for example, "MTCNN showed reduced detection performance among…individuals of African descent" (Section 4.1)—rests on 12–13 subjects per group. No confidence intervals, standard deviations, or statistical tests are reported anywhere in Tables 3 or 4. A single participant's characteristics can shift a group's average by several percentage points. The Abstract and Introduction frame VIBEFACE as "a new benchmark for evaluating the robustness and fairness of biometric verification systems," but the dataset can support exploratory demographic analysis at best, not conclusive fairness benchmarking. This is a structural issue: the data have already been collected. The paper could be recast as a specialized eKYC dataset without fairness claims, but as written, the scope of claims exceeds what the evidence supports.

- **No cross-dataset comparison.** The benchmark experiments (Sections 4.1, 4.2) evaluate face detection and verification only on VIBEFACE. To assess whether VIBEFACE is more challenging, more realistic, or more informative than existing alternatives (e.g., MOBIO, SOTERIA, Replay-Mobile), the same models should be run on at least one comparable dataset. Without this, the claim that VIBEFACE fills a gap remains an assertion rather than a demonstrated finding. For a dataset paper, cross-dataset comparisons are standard evidence of added value.

- **Verification evaluation uses a single fixed threshold without justification.** The verification task (Section 4.2, lines 336–340) applies a threshold of 0.5 to both ArcFace and MagFace, with no indication of calibration or Equal Error Rate (EER) computation. ArcFace and MagFace output scores on different scales, so a fixed threshold conflates model accuracy with model calibration. An EER or AUC-based evaluation is standard for biometric verification and would be more informative.

### Minor

- **No variance or uncertainty reporting.** All results in Tables 3 and 4 are point estimates—no standard deviations, confidence intervals, or per-subject variance. With only 50 subjects and small demographic subgroups (n≈12–13), within-cell variance is potentially large but cannot be assessed.

- **Verification uses frame-level rather than subject-level aggregation.** Performance is measured as "the percentage of frames in which the face was correctly authenticated" (Section 4.2). Frame-level reporting inflates the effective sample size; the statistical unit should be the subject, with per-subject means and variance reported across subjects.

- **Demographic disparity observations lack statistical testing.** Claims such as "female participants consistently achieved slightly higher verification rates than males" and that MTCNN showed reduced performance for certain racial groups (Section 4.1–4.2) are reported as observations without any significance test. Given the small group sizes, these patterns may not be reliable.

### Trivial
None.

## Nice-to-Haves

- Supplement fixed-threshold accuracy with EER, AUC, or ROC-based verification metrics.
- Add cross-dataset experiments (running the same models on SOTERIA, MOBIO, or Replay-Mobile).
- Report subject-level aggregated metrics with bootstrap confidence intervals.
- Add confidence intervals or bootstrapped uncertainty estimates for demographic comparisons.
- The face detection results (RetinaFace at 100% for images) are uninformative; replacing one detector with a modern model that fails on some conditions would show where the dataset is challenging.

## Removed Points

These points from the input review were removed or demoted after verification against the paper:

- **"First eKYC dataset claim overstated"**: The paper's Table 1 clearly shows no other dataset checks the eKYC column. SOTERIA has videos and demographic data but not eKYC-specific verification scenarios. The claim is accurate as stated.
- **MOBIO "Photos" formatting inconsistency**: A table rendering artifact, not an author error.
- **Face detection results being "too easy"**: RetinaFace achieving 100% on good-quality images is expected and characteristic of the dataset; this is not a valid weakness.
- **Missing appendix content/references**: Parser artifacts from the review process.
- **PAD/deepfake applications mentioned without experiments**: These appear in the Conclusion as future work, not as demonstrated contributions.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

The single highest-leverage improvement would be to **recast the paper's claims** to match what 50 subjects can actually support: a specialized dataset for eKYC-style video verification, with demographic metadata for exploratory analysis rather than conclusive fairness benchmarking. Concretely: (1) replace "fairness benchmarking" framing with "eKYC-focused dataset with demographic metadata," (2) add EER/AUC metrics and confidence intervals to the benchmark evaluation, and (3) include cross-dataset comparison experiments to demonstrate the dataset's relative difficulty and value.

## Score and Decision

**Calibration summary:** All anchors retrieved across rounds are listed below. The score is calibrated by comparing weighted item scores.

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| ID-Booth | NWvsm2VxAM.md | 3.00 | R1 | Yes | Synthetic face data paper with limited novelty; our dataset contribution is more tangible |
| HiDF | XhyCPEnlCa.md | 4.25 | R2 | Yes | Similar dataset-only contribution with stronger strengths (12.76 vs 8.68) but a severe broken-link weakness (−7.66 vs our −0.88) |
| UDC-VIT | DNBwlQYA90.md | 6.00 | R1 | Yes | First real-world UDC dataset, rejected; our sample-size limitation is more severe |
| ILLUSION | qnlG3zPQUy.md | 6.00 | R1 | Yes | Large-scale (1.3M samples) deepfake dataset, accepted; our scale is far smaller |
| Vec2Face | RoN6NnHjn4.md | 6.00 | R1 | Yes | Synthetic face generation with technical contribution, accepted; our paper lacks algorithmic novelty |

**Bracket determination (Round 1):** The paper sits clearly above ID-Booth (3.00) due to a genuine dataset contribution with ethical rigor, but below UDC-VIT (6.00) and ILLUSION (6.00) in large part because of the 50-subject limitation and lack of cross-dataset evidence. The strongest negative-weighted item (−0.88 for sample size) is a structural limitation that the other dataset papers in the 6.0 range do not share.

**Narrowing (Round 2):** Comparing against HiDF (4.25, Reject), our paper has lower peak strength weights (8.68 vs 12.76) but no catastrophic negative weights (−0.88 vs −7.66). However, the 50-subject limitation is structural in a way HiDF's single-tool limitation is not (adding more subjects requires recollecting data). The paper also lacks cross-dataset comparison that would ground its claims about the dataset's value.

**Final placement:** The paper has genuine contributions (eKYC gap, ethical collection, demographic balance, multi-condition acquisition) that support a score in the 4.0–4.5 range. However, the gap between claimed scope (fairness benchmark) and supported evidence (50 subjects, no cross-dataset comparison, no uncertainty metrics) is substantial enough to make the paper not yet ready for acceptance.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>