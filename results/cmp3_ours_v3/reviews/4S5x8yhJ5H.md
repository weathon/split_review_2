Now let me write the final consolidated review.

## Summary

VIBEFACE is a facial biometric dataset focused on electronic Know Your Client (eKYC) scenarios, comprising 2,250 still images and 1,550 short videos from 50 subjects. It is balanced across gender (25M/25F), four racial categories, and three age bands, collected under five sessions varying lighting and glasses presence using three consumer smartphone models. Face detection and verification baselines are provided, and the dataset is released under a GDPR/EU AI Act-compliant controlled-access license.

## Strengths

1. **eKYC focus fills a genuine gap in public datasets.** Table 1 confirms VIBEFACE is the only publicly available dataset with explicit eKYC scenarios (scenarios 12–18: head rotation, blinking, expression changes, mouth opening, partial occlusions, face touching). These protocols are well-documented in Section 3.2 and meaningfully extend beyond what existing datasets offer for studying eKYC-specific facial behaviors.

2. **Careful demographic design.** The dataset achieves near-perfect balance across gender (25M/25F), four racial categories (African 13, Caucasian 13, East Asian 12, South Asian 12), and three age bands (19/17/14). The inclusion of Fitzpatrick skin tone coverage and metadata for facial hair, hair color, and piercings (Section 3.1) enables fairness analyses that many larger datasets cannot support because they lack such metadata.

3. **Ethical and legal rigor.** Data collection complies with GDPR and the EU AI Act (Section 3.4), uses informed consent with explicit opt-out rights, and is released under a controlled-access license (Section 3.5). This is a meaningful contribution at a time when large face datasets like VGGFace2 and MS-Celeb-1M have been withdrawn over ethical concerns. The paper handles this aspect properly.

4. **Multi-session, multi-device acquisition protocol.** Five sessions vary lighting conditions (artificial, flash, natural, weak natural) and glasses presence, captured across three consumer smartphone models (Xiaomi Redmi Note 13, iPhone 13, Samsung Galaxy A35) with random device assignment per session (Table 2). This is a well-structured protocol that introduces controlled variability for systematic analysis.

## Weaknesses

### Major

1. **The face verification evaluation is incomplete and does not constitute a valid verification benchmark.** Section 4.2 describes a protocol that: (a) uses only genuine (same-subject) pairs — no impostor trials are conducted; (b) applies a similarity threshold of 0.5 with no justification; and (c) reports only the percentage of query frames exceeding this threshold. Without impostor comparisons, the reported metric cannot distinguish a system that correctly rejects impostors from one that accepts everyone above threshold. Standard face verification evaluation requires ROC curves, AUC, or TAR at specified FAR operating points. Because of this, the results in Table 4 and the demographic conclusions drawn from them (lines 344–346: "both models performed slightly worse on the Caucasian subgroup") are not supported as measures of face verification performance. This is verifiable from lines 336–340.

2. **Demographic conclusions lack statistical support given the sample size.** With N=12–13 per racial category and N=14–19 per age band (lines 139, Table 3), the paper reports performance differences across demographic groups (lines 300–301: "MTCNN showed reduced detection performance… among individuals of African descent, while achieving its highest accuracy for East Asian subjects"; lines 344–346 for verification) without any confidence intervals, variance measures, or significance tests. Per-group means with N≈12 can be driven by individual subject idiosyncrasies (beard style, glasses shape, skin reflectance), making it impossible to distinguish systematic demographic bias from individual variation.

### Minor

3. **The benchmark experiments do not demonstrate what the dataset uniquely enables.** The detection benchmark (Section 4.1) confirms known results (RetinaFace/MediaPipe outperform MTCNN; glasses and weak light are hard). The verification benchmark (Section 4.2) confirms ArcFace outperforms MagFace — also expected. The experiments do not compare performance on VIBEFACE vs. existing datasets to show what VIBEFACE uniquely reveals, test eKYC-specific hypotheses (e.g., do models generalize differently to the specific eKYC movements in scenarios 12–18?), or quantify whether eKYC dynamic scenarios produce different failure modes than static images. The paper claims to "demonstrate the dataset's utility" but does not show utility for research questions that could not be answered with existing data.

4. **No discussion of the dataset's own limitations.** Section 5 describes limitations of other datasets but does not acknowledge VIBEFACE's constraints: 50 subjects from (apparently) a single geographic location; controlled studio setting rather than the "at home, in variable lighting" environment motivated in the introduction (line 15); no children or elderly subjects; only four broad racial categories; no repeated measures for within-subject variability assessment. A dataset paper that honestly discusses its limitations is more useful to downstream users.

### Trivial

5. **Frame-level video verification metric conflates temporal correlation with independent trials.** For video queries in eKYC scenarios (scenarios 12–16), treating each frame as an independent verification attempt (lines 339–340) inflates effective sample size. Video-level aggregation (majority vote, min/max similarity over a temporal window) would be more appropriate for eKYC workflows.

## Nice-to-Haves

- Fundamentally revise the verification protocol to include impostor pairs and report standard metrics (ROC/AUC/TAR@FAR). This is essential to make the results interpretable and comparable to the extensive face verification literature.
- Add an eKYC-specific analysis that leverages the dataset's unique value: e.g., compare verification accuracy on eKYC dynamic scenarios (12–18) vs. static frontal images to quantify the difficulty introduced by natural facial movements, or identify which movements cause the most verification instability.
- Add statistical reporting (bootstrap confidence intervals, variance measures) for the demographic analyses.
- Provide device-level analysis since cross-device variability is a stated motivation in the introduction.
- Justify the choice of the flash session frontal image (Scenario 3, Session B) as the reference, since flash is an atypical reference condition.
- Add a "Limitations" subsection to Section 5.

## Removed Points

These points were raised in the input but are removed per filtering rules:

- **"50 subjects is a fundamental scale limitation contradicting the paper's framing"** — While scale is a legitimate concern for demographic analysis, the paper is compared to similarly-sized datasets (MOBIO 150, OULU-NPU 55, WMCA 72, SOTERIA 70; Table 1), so calling it "fundamental" overstates the issue. The sample-size criticism is retained but consolidated into Weakness #2 (demographic conclusions lack statistical support), which captures the core concern more precisely.
- **Concerns about "eKYC-style facial videos alongside still images" claim lacking a supporting survey** — The paper provides Table 1 as implicit support. This is a minor presentational point, not a weakness.
- **Table 1 comparison issue with PAD datasets** — Minor framing observation.
- **Single geographic location as a limitation** — Relevant but more speculative than other weaknesses; subsumed under Weakness #4 (no limitations discussion).
- **Controlled studio vs. "at home" mismatch** — Subsumed under Weakness #4.
- **Missing device-level analysis, reference image justification, session B coverage** — These are nice-to-haves, not weaknesses.
- **Various formatting/style observations from section-by-section notes** — Not substantive weaknesses.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Fundamentally revise the verification evaluation to include impostor pairs and report standard metrics (ROC/AUC/TAR@FAR).
2. Either remove the unqualified demographic performance claims or support them with proper statistical tests and explicit caveats about subgroup sizes.
3. Add a "Limitations" subsection to Section 5 that honestly calibrates what conclusions the dataset supports.
4. Include at least one analysis that demonstrates the eKYC-specific value of the dataset (e.g., comparing performance on eKYC dynamic scenarios vs. static images, or analyzing which eKYC movements cause the most verification instability).

## Score and Decision

**Calibration Process:**

Round 1 (bracketing) searched over six score ranges. The most informative anchors for comparison were:

| Anchor Paper | Human Score | Round | Comparison |
|---|---|---|---|
| ID-Booth (synthetic face dataset) | 3.0 | R1 | Stronger dataset contribution than VIBEFACE, but similar-level methodology concerns |
| HiDF (deepfake dataset, 30K images+4K videos) | 4.25 | R1 | Larger dataset but single-generation method; rejected with similar "limited experiments" critiques |
| IndianRoad (traffic video dataset) | 4.0 | R2 | Dataset with niche focus but limited experiments; similar level |
| AVSS (airport segmentation dataset) | 4.75 | R2 | Dataset benchmark with limited model innovation; slightly stronger evaluation |
| VideoClusterNet (face clustering) | 5.0 | R2 | Method + evaluation, not a pure dataset paper |
| **VIBeID (biometric dataset, 100 subjects)** | **5.75** | **R2** | **Most similar: biometric dataset with benchmarks; had 2× the subjects and no fundamental evaluation flaw; still rejected** |
| UDC-VIT (UDC video dataset) | 6.0 | R2 | Novel acquisition system with thorough evaluation, still rejected for limited technical depth |
| ILLUSION (deepfake dataset, 1.3M samples) | 6.0 | R2 | Much larger scale, more thorough evaluation, borderline accepted |

**Round 1 bracket:** [3.5, 5.5] — VIBEFACE has a genuine niche (eKYC) and ethical rigor that separates it from low-1.x–3.x papers (which had fundamental execution problems), but its incomplete verification evaluation and small-N demographic claims prevent it from reaching the 5.5+ tier where papers like VIBeID (5.75) and UDC-VIT (6.0) sit.

**Round 2 narrowing:** VIBeID (5.75) is the closest direct comparator: both are biometric datasets with benchmark analyses. VIBEFACE has half the subjects, a more serious evaluation flaw (no impostor trials vs. VIBeID's minor methodological concerns), and offers less technical depth in experiments. This places VIBEFACE clearly below 5.75, in the 4.0–4.5 range. Comparing upward: UDC-VIT (6.0) had a novel capture system and cross-dataset validation; VIBEFACE lacks comparable methodological rigor. Comparing downward: HiDF (4.25) had similar "limited experiments" critiques but was much larger in scale; VIBEFACE's verification flaws are more fundamental.

**Final score: 4.5** — The dataset itself has genuine value (ethical sourcing, eKYC focus, demographic balance), but the paper significantly overstates what it demonstrates. The verification evaluation is structurally incomplete, and the benchmark experiments do not exploit the dataset's unique characteristics. These issues can be addressed in revision, but as presented the gap between claims and evidence is too large for acceptance.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>