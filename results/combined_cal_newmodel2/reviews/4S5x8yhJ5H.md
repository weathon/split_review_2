## Summary

This paper introduces VIBEFACE, a facial biometric dataset designed to address the gap in publicly available resources for eKYC (electronic Know Your Client) scenarios. The dataset comprises 2,250 images and 1,550 videos from 50 subjects, captured across five sessions with varying lighting and devices, featuring eKYC-specific actions (head rotation, blinking, expression changes, etc.). The authors demonstrate the dataset through face detection (MTCNN, RetinaFace, MediaPipe) and face verification (ArcFace, MagFace) benchmarks, with a strong emphasis on ethical compliance (GDPR, EU AI Act, informed consent) and demographic balance across race, gender, and age.

## Strengths

- **Clearly identified and well-motivated gap — eKYC-specific video scenarios.** The paper correctly identifies that no existing publicly available dataset includes authentic eKYC verification workflows captured as videos. Table 1's comparison with MOBIO, Replay-Mobile, OULU-NPU, WMCA, HQ-WMCA, SOTERIA, and MobiBits supports this claim; none of them have an eKYC column checked. This is a genuine, well-motivated gap.

- **Ethical sourcing that sets a standard.** Full GDPR and EU AI Act compliance, informed consent with the right to withdraw, controlled-access licensing for non-commercial academic use, anonymization, and no PII stored. Given that MS-Celeb-1M, VGGFace2, and MegaFace have been withdrawn due to ethical concerns, a legally compliant, consent-based dataset is a meaningful contribution to the community.

- **Multi-session, multi-device acquisition design.** Five sessions varying lighting (artificial, flash, natural, weak natural) and eyeglasses, using three different consumer smartphones, with both standardized rear-camera shots and front-facing selfie/video captures. This produces genuine variation in capture conditions rather than synthetic augmentation.

- **Demographic balance that goes beyond most existing datasets.** The dataset achieves near-equal representation across four racial categories (24–26% each), a 50:50 gender split, and three age brackets (18–30: 19 subjects, 31–50: 17, 51–70: 14). SOTERIA, the closest comparator, underrepresents middle-aged and older individuals; VIBEFACE addresses this.

## Weaknesses

### Fatal

None.

### Major

- **Small dataset scale (50 subjects) limits the utility of demographic subgroup analysis.** With only 12–13 subjects per racial category and 14–19 per age group, differences of a few percentage points (e.g., ArcFace OAV: African 0.490, Caucasian 0.468, East Asian 0.460, South Asian 0.509) are reported without confidence intervals or statistical significance tests. The paper states findings such as "Both models performed slightly worse on the Caucasian subgroup" (page 8, lines 344), but at these sample sizes the observed disparities are essentially anecdotal. The paper should either provide rigorous statistical testing or refrain from drawing demographic conclusions at this scale.

- **No comparative evaluation against existing datasets.** The paper argues that existing datasets lack eKYC scenarios and that VIBEFACE fills this gap, but all benchmark experiments are conducted within VIBEFACE. There is no experiment comparing model behavior on VIBEFACE's eKYC videos vs. a matched sample from an existing dataset (e.g., MOBIO or SOTERIA), so the reader cannot assess whether eKYC scenarios pose distinct, practically relevant challenges not already captured by existing resources.

### Minor

- **The verification evaluation uses a fixed threshold of 0.5 instead of standard ROC/EER analysis.** As stated on page 8 (lines 340), "Verification was considered successful when the similarity score exceeded a fixed threshold of 0.5." A single accuracy point at a fixed threshold discards most information about verification performance. The very low OAV results for MagFace (0.26–0.30) compared to ArcFace (0.43–0.51) could partly reflect calibration differences rather than genuine capability gaps. No confidence intervals or variance estimates are provided.

- **The eKYC-specific evaluation does not match the eKYC framing.** The paper is motivated by eKYC video scenarios (12–18), yet no PAD/liveness detection baselines are provided. Scenarios 17–18 (hand occluding face, touching face) are excluded from the detection evaluation because occlusions "significantly reduce facial visibility" (page 6, line 288), and scenario 11 (selfie video simulating registration) is excluded for incomplete coverage. While scenarios 12–16 are evaluated for verification, the absence of PAD baselines underserves the paper's own framing, especially since the conclusion (page 9, lines 374) mentions PAD as a natural application.

- **Verification accuracy conflates detection failures with matching failures.** Verification "failure" could arise from the face not being detected, the detected face not being matched, or the similarity score being below 0.5. These qualitatively different failure modes are not disentangled in the reported results (Table 4).

### Trivial

- **The Fitzpatrick scale claim is unsubstantiated.** The paper states "we also ensured that the skin tones of participants reflect the whole spectrum of Fitzpatrick's scale" (page 3, line 139) but provides no measurements or distributions of Fitzpatrick types per subject.

- **Device randomization is confounded with session effects.** The paper states "The acquisition device was randomly chosen before each session" (page 4, line 187). Because device and session are not fully crossed, observed differences across sessions (e.g., Session C degradation) could partly reflect device artifacts rather than lighting/glasses effects.

- **No formal evaluation protocol is defined for future users.** The paper does not specify a train/test split, cross-validation recommendations, or whether videos should be sampled at frame level or sequence level, which limits the dataset's usability as a community benchmark.

## Nice-to-Haves

- Adding a comparative experiment showing how model behavior differs on VIBEFACE's eKYC videos vs. a matched sample from an existing dataset like MOBIO or SOTERIA would directly substantiate the gap claim.
- Replacing the fixed-threshold verification with ROC/EER analysis and reporting confidence intervals (e.g., bootstrapped) would raise the benchmark from "illustrative demo" to "usable community reference."
- Adding at least one PAD or liveness detection baseline on the eKYC video scenarios (12–18) would demonstrate the dataset's distinctive value.

## Removed Points

These points are flagged to be removed, treat them with caution:
- "Dataset size fundamentally limits its value as a benchmark" — reduced from fatal to major: the scale is a real limitation but the primary gap (eKYC scenarios) is specific rather than scale-driven; the paper does not claim to replace LFW/IJB-C, and the data volume per subject (2,250 images + 1,550 videos) is substantial.
- "No release timeline or hosting commitment" — removed: the paper describes a controlled-access license and project website; questioning long-term hosting is speculative.
- "Camera resolution and quality metrics missing" — removed: the paper reports minimum resolution (2316×3088 for images, 1920×1080 for videos at line 131); distribution details are a minor nice-to-have.
- "Single reference image is fragile" — removed: using one enrollment image is a common protocol in face verification; this is a design choice, not a flaw.
- "The checkbox-based format in Table 1 is overly coarse" — removed: a presentation nitpick without substance.
- Table 1 "eKYC is binary" critique — removed: a checkbox table is an appropriate summary format.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a comparative experiment (e.g., does ArcFace achieve different accuracy on VIBEFACE's head-rotation videos vs. frontal video from MOBIO?) to directly substantiate the eKYC-gap claim.
2. Replace the fixed-threshold protocol with ROC/EER analysis and report bootstrapped confidence intervals.
3. Add at least one PAD/liveness baseline on scenarios 12–18 to demonstrate the eKYC-specific value.
4. Provide measured Fitzpatrick type distributions to substantiate the skin-tone claim.
5. Define a formal evaluation protocol for future users (recommended train/test split, cross-validation or evaluation procedure).

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| `5lUdTogEL3.md` | 1.00 | R1 | No | Person re-ID, not face biometrics; much weaker paper |
| `u1cQYxRI1H.md` | 0.50 | R1 | No | Illumination harmonization; not a dataset paper |
| `NWvsm2VxAM.md` (ID-Booth) | 3.00 | R1 | Yes | Synthetic face generation; similar domain but method paper; limited novelty, weak results |
| `uW3tNSx7PZ.md` | 2.50 | R1 | No | Gradient protection in FL; not a dataset paper |
| `WjxgruI6A2.md` | 3.67 | R2 | No | Voice-face matching; homogeneous dataset focused |
| `dEGYODD6iU.md` (ColorCubeNet) | 3.67 | R1/R2 | Yes | Skin tone PAD; limited novelty, weak SOTA comparison |
| `XhyCPEnlCa.md` (HiDF) | 4.25 | R1/R2 | Yes | Deepfake dataset (30K images, 4K videos); single generation method, limited diversity |
| `3iGponpukH.md` (ScalePerson) | 4.75 | R1/R2 | Yes | Person detection benchmark; dataset too easy, low discriminative power |
| `0y3hGn1wOk.md` (FIUBench) | 5.40 | R2 | Yes | Facial identity VLM unlearning benchmark with 400 synthetic faces and clear evaluation protocol; accepted |
| `DNBwlQYA90.md` (UDC-VIT) | 6.00 | R1 | Yes | UDC video dataset with cross-dataset comparison; first real-world UDC video dataset |
| `RoN6NnHjn4.md` (Vec2Face) | 6.00 | R1 | Yes | Synthetic face generation with strong experiments; accepted |
| `lAhQCHuANV.md` | 6.33 | R1 | No | Face recognition fairness assessment; not a dataset paper |

**Calibration reasoning (Round 1 bracket → Round 2 narrow):** Round 1 bracketing placed the paper between 2.5 and 5.5 by comparison with ID-Booth (3.00), HiDF (4.25), and ScalePerson (4.75). Round 2 narrowed by comparing VIBEFACE's item favorability against FIUBench (5.40, Accept) and HiDF (4.25, Reject). VIBEFACE's highest-favorability strengths (eKYC gap at 11.22, ethical sourcing at 11.30) are competitive with FIUBench's strongest items (~9.9), but its major weaknesses have strongly negative favorability (small scale at -0.70, no comparative evaluation at -2.26), whereas FIUBench's size concern had moderate favorability (~2-5). The verification protocol weakness (favorability 3.81) is notably weaker than FIUBench's evaluation protocol (favorability 8.72). VIBEFACE sits between HiDF (4.25) and ScalePerson (4.75): it has stronger ethical grounding and demographic balance than either, but the 50-subject scale is smaller than HiDF's 30K images+4K videos and the evaluation is less rigorous than ScalePerson's 231-experiment benchmark.

**Final score: 4.0.** The paper addresses a genuine gap with strong ethical and demographic design, but the small scale (50 subjects), lack of comparative evaluation, and weak verification protocol prevent it from functioning as a community benchmark. The contribution is real but narrow, more appropriate for a specialized venue at its current depth.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>