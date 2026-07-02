Now I have sufficient calibration context. Let me write the final consolidated review.

## Summary

VIBEFACE is a dataset of 2,250 images and 1,550 videos from 50 subjects, designed to fill the gap in publicly available face data that mimics eKYC (electronic Know Your Client) workflows — head rotations, blinking, mouth movements, hand occlusions, etc. The dataset is collected across three smartphones, five sessions varying lighting and eyewear, and is balanced 50:50 by gender with roughly 25% per racial group (African, Caucasian, East Asian, South Asian). Collection was conducted with informed consent under GDPR and the EU AI Act.

## Strengths

- **Genuine gap in existing datasets.** Table 1 and Section 3.2 make clear that no publicly available dataset includes video sequences mimicking the specific action protocols used in eKYC identity verification (scenarios 12–18). This is a real, practically motivated gap.

- **Deliberate and well-documented demographic balance.** 50:50 gender split, ~25% per racial category, and reasonable age spread (Figure 1, Section 3.1). Metadata provided enables fairness auditing — a genuine advantage over most existing face datasets.

- **Exemplary ethical and legal compliance.** Data collected with informed consent, under GDPR and the EU AI Act, with controlled-access licensing and anonymization (Sections 3.4, 3.5). This is a significant positive against the backdrop of withdrawn web-crawled datasets (MS-Celeb-1M, VGGFace2).

- **Multi-device, multi-condition acquisition.** Three consumer smartphones (Xiaomi Redmi Note 13, iPhone 13, Samsung Galaxy A35) and five sessions combining lighting conditions and eyewear (Table 2) provide useful cross-device and cross-condition variability.

## Weaknesses

### Major

- **Verification protocol uses a fixed threshold of 0.5 for both models** (Section 4.2, line 340). ArcFace and MagFace produce different similarity score distributions. Evaluating both at the same fixed threshold means the claim "ArcFace consistently outperformed MagFace" (line 342) may simply reflect that 0.5 is closer to ArcFace's typical operating point. Standard verification benchmarking evaluates across thresholds (ROC curves, EER, AUC) or at each model's own optimal operating point. The paper does neither, so the comparative claim is not supported by the evidence as presented.

- **Frame-level accuracy as the primary verification metric** (Section 4.2, lines 340–341). Measuring "the percentage of frames in which the face was correctly authenticated" is problematic because (a) frames within a video are highly correlated — a 6-second video at 30 fps yields 180 non-independent observations, inflating the effective sample size, and (b) verification is inherently a per-video (or per-pair) binary decision; the paper does not define how a video is judged authenticated (majority of frames? any frame?).

- **Studio collection contradicts the "unconstrained" framing.** The Introduction motivates the dataset for "unconstrained conditions — at home, in variable lighting" (Section 1, line 15), and the Conclusion highlights "the need for robust solutions in unconstrained settings" (line 346). However, Section 3 (lines 73–75) states data was collected "in a controlled studio environment" with "standardized instructions" and "continuous supervision by trained operators." The dataset captures studio simulations of eKYC actions, not genuine unconstrained captures. This direct tension between framing and execution is never acknowledged in the paper.

### Minor

- **Small subject count limits subgroup analysis.** With 50 subjects (12–13 per racial group, 14–19 per age group), the dataset's utility as a *benchmark* for demographic fairness is severely constrained. Claims about "minimal demographic variation" or "modest performance disparities" (lines 300, 344) are not statistically grounded at these subgroup sizes.

- **No model provenance specified** (Section 4.2). The paper does not state which pre-trained ArcFace/MagFace weights were used, what training data those models were originally trained on, or whether any fine-tuning was performed on VIBEFACE.

- **No limitations discussion** (Section 5). The Conclusions do not address the controlled studio environment, small N, proxy nature of the eKYC simulations (participants following instructions rather than acting naturally), or the lack of impostor/attack samples.

- **No statistical significance for demographic comparisons** (Tables 3, 4). Numerical differences across racial groups (e.g., MTCNN frontal: African 0.812 vs. East Asian 0.984, Table 3) are reported without confidence intervals or significance tests, despite only 12–13 subjects per group.

### Trivial

- The claim of "authentic eKYC-style facial videos" (line 24) overstates what the dataset contains — these are studio simulations, not real eKYC recordings. The wording should be qualified.

- The claim that the dataset is "well-suited for advancing research in presentation attack detection (PAD)" (line 374) is unsupported, as the dataset contains only bona fide samples with no attacks.

## Nice-to-Haves

- Define a standard evaluation protocol with explicit train/validation/test splits or cross-validation folds, so different research groups can reproduce results.
- Include per-subject performance breakdowns to check for outlier-driven aggregation effects.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Criticism about Table 1 "underselling competing datasets" / checkmark format.** REMOVED: The table is a factual feature comparison, and the paper acknowledges those datasets serve different primary purposes (lines 52–57). The checkmark format is standard for such comparisons.

- **Criticism about MTCNN demographic bias being "well-known."** REMOVED: The detection experiments serve to demonstrate the dataset can surface such issues, not to claim novelty of the finding per se. This is a standard use case for a benchmark dataset.

- **Criticism about missing quality control discussion.** REMOVED: The paper explicitly states no pre/post-processing was applied (line 131), which is a transparent design choice rather than an omission.

- **Criticism about "authentic" wording in Introduction.** MERGED into Trivial weakness #1.

- **Various formatting/style observations from Section-by-Section notes.** REMOVED per Hard Rules (parser artifacts, not paper problems).

## Novel Insights

The reviews surface one observation that goes beyond the paper's own articulation: the tension between the paper's stated ecological validity ("unconstrained, at-home conditions") and the actual collection protocol ("controlled studio, supervised operators") is not merely a minor omission but a structural feature of the dataset that the paper never reconciles. This limits the dataset's ability to support the generalization claims the paper makes. Additionally, the methodological critique of the verification protocol (fixed threshold + frame-level accuracy) reveals that the quantitative comparisons in Table 4 do not actually support the claims drawn from them — a problem the paper does not acknowledge.

## Suggestions

1. **Replace the verification metric.** Use a standard protocol: for each video, compute a single similarity score (maximum or mean over frames), then report ROC curves, EER, and AUC. Evaluate across multiple thresholds rather than a single fixed 0.5.
2. **Acknowledge the studio environment directly.** Reframe the paper to honestly describe the data as studio-simulated eKYC actions, and discuss what further work would be needed to extend to genuinely unconstrained capture.
3. **Add a limitations section** addressing the small N, studio environment, proxy nature of the recordings, and lack of statistical power for subgroup analysis.
4. **Specify model provenance** (which pretrained weights, training data, any fine-tuning) for all benchmark experiments.

## Score and Decision

**Calibration procedure:** I retrieved 24 anchor papers across 6 score bands using topical similarity queries. The most relevant anchors are dataset papers:

| Anchor | Path | Avg Score | Round | Comparison |
|--------|------|-----------|-------|------------|
| HiDF deepfake dataset | 5lUdTogEL3... (via XhyCPEnlCa) | 4.25 | 1, 2 | Dataset paper rejected due to limited diversity and baseline concerns. VIBEFACE has stronger ethical/demographic credentials but similar evaluation issues. |
| IndianRoad video dataset | 8gCgXG40Wn | 4.00 | 2 | Dataset paper rejected due to evaluation methodology gaps. Similar profile to VIBEFACE. |
| Short-video dataset | T4VK4U4aKb | 4.50 | 2 | Large-scale dataset rejected for lacking proper benchmark tasks. VIBEFACE has benchmark tasks, but they are methodologically flawed. |
| UDC-VIT video dataset | DNBwlQYA90 | 6.00 | 2 | Despite scoring 6.00, rejected for limited novelty in collection methods. VIBEFACE's evaluation issues are worse. |
| ILLUSION deepfake dataset | qnlG3zPQUy | 6.00 | 1, 2 | Accepted. Large-scale (1.3M samples), comprehensive benchmarks. VIBEFACE is much smaller with weaker evaluation. |
| Face-Human-Bench | x1Bk51SCL9 | 5.75 | 2 | Rejected despite thorough evaluation. Shows that benchmark papers need stronger justification of novelty. |

**Round-1 bracket:** 3.5–5.5. The dataset fills a genuine gap and has exemplary ethical compliance, but the evaluation methodology is flawed and the framing is inconsistent.

**Final score:** 4.5. The dataset itself is a solid contribution with several strengths (demographic balance, ethical compliance, eKYC-specific scenarios). However, the paper as written has two major issues: (1) the verification evaluation protocol is methodologically invalid for the comparative claims made, and (2) the motivating premise (unconstrained capture) directly contradicts the actual collection protocol (controlled studio), a tension that is never acknowledged. These issues are fixable with revisions, but as presented they undermine the quantitative claims and framing of the paper.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>