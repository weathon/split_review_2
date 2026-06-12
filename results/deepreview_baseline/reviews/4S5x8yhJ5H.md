## Summary
The paper introduces VIBEFACE, a face verification dataset designed specifically for electronic Know Your Client (eKYC) scenarios. It consists of 2,250 images and 1,550 videos from 50 subjects, with balanced demographics across gender, age, and four racial groups, collected under varying lighting conditions and glasses. Benchmark experiments with standard face detectors and verification models demonstrate basic dataset usability.

## Strengths
- **Ethical collection and informed consent:** All data was collected with participant consent and compliance with GDPR, addressing growing privacy concerns with many existing large-scale face datasets that have been withdrawn.
- **Demographic balance:** The dataset is explicitly balanced across gender (50:50), four racial groups (approximately 25% each), and three age groups, which is rare among publicly available face datasets and supports fairness evaluation.
- **eKYC-specific video scenarios:** The inclusion of short videos with actions such as head rotation, blinking, expression changes, and partial occlusions directly mimics real eKYC workflows, filling a gap not covered by most existing datasets.
- **Multiple controlled acquisition conditions:** Five sessions varying artificial/natural/weak/flash lighting and the presence of eyeglasses provide structured variability for robustness testing.

## Weaknesses
### Fatal
None identified that invalidate the paper’s core claims.

### Major
- **Small subject count (50) severely limits statistical reliability for its primary claimed use case: demographic fairness evaluation.** With only 12–13 subjects per racial group and 14–19 per age group, observed performance differences across subgroups cannot be reliably attributed to demographic factors rather than individual variation. A power analysis or bootstrap uncertainty estimates are absent. This undermines the paper’s main value proposition.
- **The dataset is too small to support training of modern deep face verification models, restricting its utility to evaluation.** For evaluation, existing datasets such as LFW (13,000 images, 5,749 subjects), IJB-C (3,500 subjects), or AgeDB (16,000 images, 568 subjects) already offer larger, publicly available evaluation benchmarks. The paper does not provide a comparative analysis showing why 50 subjects provide a meaningful or complementary evaluation signal that these larger datasets lack.
- **The eKYC scenarios were collected in a controlled studio environment, not in the unconstrained home settings that characterize real eKYC usage.** This limits the realism of the dataset relative to its stated motivation. Existing datasets such as OULU-NPU and Replay-Mobile already include mobile-captured videos under varying lighting, and the paper does not clearly quantify what new challenges VIBEFACE adds beyond those.
- **No comparison to existing evaluation datasets** (e.g., LFW, IJB-C, AgeDB, MOBIO) in terms of task difficulty, demographic coverage, or verification performance. Without such baselines, it is impossible to assess whether VIBEFACE offers a stricter or more informative benchmark for eKYC scenarios.

### Minor
- **Verification evaluation uses a single fixed threshold (0.5) and does not report ROC curves, AUC, or EER**, which are standard metrics in the face verification literature. This makes it difficult to compare results with other benchmarks or to assess calibration.
- **Only one reference image (frontal flash session) is used per subject** for verification, whereas real eKYC often compares against a document photo taken under different conditions. The impact of reference-to-query domain gap is unexplored.
- **The detection benchmark includes only three detectors (MTCNN, RetinaFace, MediaPipe).** Adding more recent or lightweight detectors (e.g., YOLOv8-face) would strengthen the analysis.
- **Cross-device variation is not analyzed**, despite using three smartphone models. The assignment of device per session is described as random, but device-specific performance is not reported.

### Trivial
- Minor formatting artifacts in table captions are present in the extracted text but are ignored per instructions.

## Nice-to-Haves
- Include per-subject performance distributions to illustrate within-group variability.
- Provide ROC curves with AUC/EER for the verification task.
- Compare verification accuracy against existing datasets (e.g., LFW, IJB-C, AgeDB) on the same models to contextualize difficulty.
- Increase the number of subjects to at least 200–300 to improve statistical power for subgroup analysis.
- Collect a subset of samples in fully unconstrained home environments to better approximate real eKYC.
- Analyze performance differences across the three phone models.

## Novel Insights
None beyond the paper’s own contributions.

## Suggestions
- **Substantially increase the number of subjects** (target at least 200) to make demographic fairness evaluation statistically meaningful and to provide a training set usable for modern models.
- **Provide ROC/AUC/EER metrics** for verification and compare against standard evaluation datasets (LFW, IJB-C, AgeDB) to demonstrate the unique difficulty of VIBEFACE’s eKYC scenarios.
- **Include uncertainty quantification** (e.g., confidence intervals or bootstrap estimates) for all subgroup metrics to support claims about fairness.
- **Extend data collection to unconstrained environments** (e.g., participants’ homes) to better match real eKYC conditions, or clearly limit claims to controlled-benchmark scenarios.
- **Release baselines** with more recent verification models (e.g., AdaFace, ElasticFace) and provide protocol definitions for cross-device and cross-session evaluation.

## Score and Decision
MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>