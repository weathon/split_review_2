## Summary
This paper presents VIBEFACE, a multimodal dataset of 2,250 facial images and 1,550 short videos collected from 50 demographically balanced participants using consumer smartphones under five environmental conditions. The dataset is designed to support face verification evaluation in electronic Know Your Client (eKYC) scenarios. VIBEFACE includes standardized photos, selfie images, and video sequences that mimic eKYC workflows (head rotations, expression changes, blinking, occlusions). The authors evaluate the dataset through face detection (MTCNN, RetinaFace, MediaPipe) and face verification (ArcFace, MagFace) benchmarks, reporting performance across demographic subgroups.

The primary contribution is the dataset itself, which uniquely combines: (a) eKYC-mimicking video scenarios, (b) demographic balance across gender (50:50), four racial groups, and three age groups, (c) five acquisition sessions with varying lighting and eyeglasses, and (d) strict ethical compliance (GDPR, informed consent, controlled access). The dataset addresses an important gap in biometric fairness research by providing a legally sourced, demographically diverse resource with explicit eKYC relevance.

**Novelty note:** The paper claims to be the first publicly available dataset with eKYC-style videos alongside still images. External literature verification was not available in this review run (Retrieval-Disabled Mode), so novelty claims should be treated as provisional pending manual verification.

```text
ASCII Diagram — Paper Structure & Evidence Map

[Problem: Existing face datasets lack eKYC scenarios & demographic balance]
        |
        v
[Gap: No public dataset with eKYC-style videos + still images + demographic balance]
        |
        v
[Solution: VIBEFACE — 50 subjects, 2250 images, 1550 videos, 5 sessions, 18 scenarios]
        |
        v
[Benchmark Task 1: Face Detection — MTCNN/RetinaFace/MediaPipe, Table 3]
        |
        v
[Benchmark Task 2: Face Verification — ArcFace/MagFace, Table 4]
        |
        v
[Claim: First eKYC-focused dataset with demographic balance]
        |
        v
[Limitations: N=50 limits subgroup power; no variance reporting; fixed-threshold eval]
```

## Strengths
1. **Addresses a genuine gap in biometric datasets.** The focus on eKYC-mimicking video scenarios is timely and practically relevant. As digital identity verification becomes mandatory in financial and regulatory contexts, datasets that simulate real eKYC workflows (head rotations, expression changes, occlusions, blinking) provide a needed evaluation resource that most existing face datasets do not offer.

2. **Demographic balance and transparency.** The dataset achieves near-equal representation across gender (25F/25M), four racial categories (13/13/12/12), and three age groups (18-30: 19, 31-50: 17, 51-70: 14). The inclusion of Fitzpatrick skin tone variation further supports fairness research. Many larger datasets lack this level of demographic metadata and balance.

3. **Strong ethical and legal compliance.** The data collection follows GDPR and EU AI Act requirements, with informed consent, anonymization, withdrawal rights, and controlled-access licensing. This sets a commendable standard compared to web-crawled datasets (VGGFace2, MS-Celeb-1M) that have been withdrawn due to consent issues. The explicit commitment to non-commercial, research-only use with prohibition of re-identification is appropriate for biometric data.

4. **Systematic acquisition design.** Five acquisition sessions with controlled variations (artificial light, flash, natural light, weak natural light, glasses) across three smartphone models provide thoughtful coverage of real-world capture conditions. The scenario numbering system (scenarios 1-18) is clear and well-documented.

5. **Detailed scenario documentation.** The 18 scenarios (5 standardized photos, 5 selfie photos, 1 selfie video, 7 eKYC verification videos) are thoroughly described with visual examples in Figures 2 and 3, making replication and extension feasible. The inclusion of both operator-captured (back camera) and participant-captured (front camera) images adds practical value.

6. **Utility demonstrated through benchmarks.** The face detection and verification benchmarks provide initial baselines that other researchers can directly compare against, using widely adopted models (MTCNN, RetinaFace, MediaPipe, ArcFace, MagFace). The per-demographic-group breakdown in Tables 3 and 4 offers useful reference points for fairness analysis.

## Weaknesses
### Major Weaknesses

**1. Sample size (N=50) limits statistical reliability of demographic subgroup analysis.**
While 50 subjects with balanced demographics is a valuable starting point, the subgroup analyses in Tables 3 and 4 are based on very small per-cell sample sizes (e.g., 12-13 subjects per racial group, ~8-10 per age-gender cell). Claims such as "Both models performed slightly worse on the Caucasian subgroup" or "MTCNN showed reduced detection performance...particularly among individuals of African descent" are not accompanied by confidence intervals, standard deviations, or statistical significance tests. With per-group sample sizes this small, observed differences may not be statistically reliable. This is a major methodological concern because fairness conclusions drawn from such underpowered subgroup analyses could be misleading. (See annotations on Page 1 - Demographics paragraph and Page 1 - Detection results narrative.)

**2. Verification evaluation uses a fixed threshold of 0.5 without calibration justification.**
The face verification benchmark (Section 4.2) reports accuracy based on a fixed similarity threshold of 0.5 for all models, sessions, and demographic groups. This is a non-standard evaluation protocol that conflates model discrimination ability with threshold calibration. Standard face verification evaluation uses ROC curves reporting TAR@FAR (e.g., TAR@FAR=1e-3) or at minimum reports FMR/FNMR trade-offs. A fixed threshold of 0.5 may systematically disadvantage models or groups with different score distributions. The reported "1.000" verification rates for frontal views may also mask meaningful performance differences at more stringent FAR levels. (See annotation on Page 1 - Face verification paragraph.)

**3. Unsupported novelty claim about "first publicly available eKYC dataset."**
The manuscript repeatedly claims to be the "first publicly available database to include diverse video-based eKYC verification scenarios." Since external literature verification is unavailable in this review run, this strong claim cannot be validated. Even within the manuscript's own references, several datasets (MOBIO, SOTERIA, WMCA) include video data under mobile conditions. Whether any prior dataset contains eKYC-specific sequences is an empirical question requiring thorough literature review. The authors should use more cautious framing (e.g., "to our knowledge, among the first specifically targeting eKYC workflows") and explicitly discuss the differentiating features from the closest video-based datasets. (See annotations on Page 1 - Gap paragraph and Page 1 - Conclusion paragraph.)

**4. Absence of variance reporting for all benchmark results.**
Tables 3 and 4 report only point estimates (single proportions) without any measure of uncertainty. For a dataset of only 50 subjects, per-subject variation is expected to be substantial. Without standard deviations, confidence intervals, or per-subject breakdowns, the reader cannot assess the reliability of reported differences across sessions, demographics, or models. This is a reproducibility concern that affects all quantitative conclusions in the paper. (See annotations on Page 1 - Face detection evaluation paragraph.)

**5. Introduction includes unsupported future application claims in the conclusion.**
The final paragraph of the conclusion claims VIBEFACE is "well-suited for advancing research in presentation attack detection (PAD), as well as in emerging areas such as detecting injection attacks involving deepfakes." However, the dataset contains only bona fide samples — no presentation attacks, deepfakes, or injection attacks are included. While the dataset could serve as a source of genuine samples for PAD research, claiming it advances PAD without any attack data is an overstatement. This claim should be either removed or explicitly qualified. (See annotation on Page 1 - Future applications paragraph.)

**6. Studio-controlled acquisition limits ecological validity for unconstrained eKYC.**
The paper emphasizes that VIBEFACE supports evaluation in "realistic operational settings" and "unconstrained conditions," but data were collected in a controlled studio environment with operator supervision, standardized instructions, and consistent backgrounds. Real eKYC sessions occur in unpredictable home environments with variable backgrounds, clothing, lighting, and user behavior. The controlled studio setting is appropriate for controlled experiments but does not fully represent unconstrained eKYC conditions. This should be acknowledged as a limitation. (See annotation on Page 1 - Data acquisition paragraph.)

### Minor Weaknesses

**7. Related Work reads as a paper-by-paper list rather than thematic comparison.**
The Related Work section (Section 2) catalogs datasets chronologically (MOBIO, Replay-Mobile, OULU-NPU, WMCA, etc.) without organizing them around analytical comparison axes. A thematic structure (e.g., ethical provenance, mobile-specific datasets, demographic balance, eKYC relevance) would better highlight where VIBEFACE fits and what its specific advantages are relative to each prior dataset. (See annotation on Page 1 - Related Work paragraph.)

**8. Flash session (B) limitations not discussed.**
Session B (flash) uses only the back-facing camera and operator, meaning it includes only standardized photos (scenarios 1-5) with no selfie or video content. This limits cross-session comparability for flash conditions. The paper does not discuss this design limitation or its implications for benchmark interpretation. (See annotation on Page 1 - Sessions section.)

**9. Natural daylight session (D) has uncontrolled confounds.**
Session D (natural daylight) was acquired across multiple days and times, introducing uncontrolled variation in light intensity due to weather and diurnal changes. Without documenting acquisition timestamps or weather conditions, this session's results are difficult to interpret as a consistent "condition." (See annotation on Page 1 - Sessions section.)

**10. Frame sampling rate (6 fps) not justified and not analyzed for sensitivity.**
The face detection evaluation samples video frames at 6 fps. This rate may undersample fast head movements (scenarios 12-13) and different sampling rates could change detection rates. No sensitivity analysis is provided. (See annotation on Page 1 - Face detection evaluation paragraph.)

**11. Title could better communicate contribution.**
The current title "VIBEFACE - VIDEO AND IMAGE BIOMETRIC DATASET FOR EVALUATION OF FACES" lists modalities but does not communicate the key novelty (eKYC focus, demographic balance, ethical sourcing). A more informative title might be: "VIBEFACE: A Demographically Balanced eKYC-Focused Dataset for Fair Face Verification."

**12. Dataset access logistics are not fully specified.**
The paper provides a temporary link and password for review, but the final infrastructure (stable hosting, application review process, data use agreement workflow) is described only vaguely. For a controlled-access biometric dataset, clear sustainability plans are important.

```text
ASCII Diagram — Revision Strategy Roadmap

[P0 Issues (Must Fix Before Publication)]
    |
    ├── P0.1: Add variance/confidence intervals to Tables 3 and 4
    │       -> Effect: enables statistical reliability assessment
    │
    ├── P0.2: Replace fixed-threshold verification with ROC/FMR-FNMR analysis
    │       -> Effect: standard-compliant evaluation, fairer model comparison
    │
    ├── P0.3: Soften "first eKYC dataset" claim with qualified language
    │       -> Effect: defensible novelty claim, reduced contradiction risk
    │
    └── P0.4: Remove or qualify PAD/injection attack claims in Conclusion
            -> Effect: eliminates unsupported overclaiming

[P1 Issues (Should Fix for Strong Revision)]
    |
    ├── P1.1: Acknowledge N=50 limitation for subgroup analyses
    ├── P1.2: Document Session D uncontrolled variability
    ├── P1.3: Add frame-rate sensitivity analysis
    └── P1.4: Restructure Related Work as thematic comparison

[P2 Issues (Quality Improvements)]
    |
    ├── P2.1: Improve title informativeness
    ├── P2.2: Clarify dataset hosting and access sustainability
    └── P2.3: Add per-subject variability analysis as supplementary material
```

## Score
**Final Score: 6/10**

**Rationale:** The paper addresses a timely and practically relevant problem — the lack of demographically balanced, eKYC-focused datasets for face verification research. The dataset itself is carefully designed with systematic acquisition sessions, clear ethical provenance, and useful benchmark baselines. However, the score reflects several significant methodological weaknesses in the benchmark evaluation: the absence of variance/confidence intervals, the use of a non-standard fixed-threshold verification protocol instead of ROC/FMR-FNMR analysis, and unsupported PAD-related claims in the conclusion. Additionally, the strong novelty claim ("first publicly available eKYC dataset") cannot be externally verified in this review. The sample size (N=50) limits the statistical power of subgroup fairness analyses, though this is a common limitation in controlled biometric data collection. With the major weaknesses addressed (particularly P0.1-P0.4 in the revision roadmap), the paper could become a solid contribution at 7-8/10. The core dataset value is genuine, but the evaluation methodology and claim calibration need substantial strengthening before publication.

**External literature verification unavailable in this run (Retrieval-Disabled Mode); novelty/comparison conclusions are intentionally deferred and should be treated as provisional pending manual literature review.**