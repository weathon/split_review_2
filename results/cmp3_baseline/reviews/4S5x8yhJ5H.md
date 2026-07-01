## Summary

VIBEFACE is a new multimodal facial biometric dataset comprising 2,250 still images and 1,550 short videos from 50 participants, designed specifically for evaluating face verification in eKYC (electronic Know Your Client) scenarios. The dataset is balanced across gender, four racial categories, and three age groups, collected under five environmental conditions using multiple consumer smartphones, with full ethical compliance (GDPR, informed consent). The authors present benchmark results for face detection (MTCNN, RetinaFace, MediaPipe) and face verification (ArcFace, MagFace), demonstrating expected performance variations across conditions and demographics.

## Strengths

- **Novel scenario focus**: The dataset is the first publicly available resource to specifically include video sequences that mimic real eKYC procedures (e.g., head rotation, blinking, expression changes, partial occlusions), addressing an important gap for financial and regulatory compliance applications.
- **Strong ethical and legal grounding**: Collection followed GDPR and the EU AI Act, with informed consent, controlled-access licensing, and explicit prohibition of commercial use and re-identification. This sets a responsible standard that many older datasets (e.g., VGGFace2, MS-Celeb-1M) lacked.
- **Demographic balance by design**: Gender is exactly 50:50, four racial groups are approximately equal (13/13/12/12), and ages span 18–69 across three bands. This enables meaningful demographic analysis, though statistical power is limited by total sample size.

## Weaknesses

### Fatal
None.

### Major
- **Very small sample size (N=50)**: For a dataset intended to serve as a fairness benchmark and support generalizable conclusions, 50 subjects is severely limiting. Per-group analysis—e.g., 12–13 subjects per racial category, 25 per gender—cannot support statistically robust claims about demographic performance differences. Many existing facial datasets (e.g., MOBIO, OULU-NPU, SOTERIA) have comparable or larger subject counts, and the paper does not justify why 50 is sufficient for the claimed "new benchmark."
- **Simplistic benchmark evaluation**: Face verification is evaluated using only a fixed similarity threshold (0.5) and a single success-rate metric. No ROC/DET curves, no FMR/FNMR trade-off analysis, no cross-validation or explicit train/test splits. The detection benchmark only reports frame-level detection rates without bounding box accuracy. These minimal experiments do not demonstrate the dataset's utility for rigorous algorithm development or fairness assessment.
- **Insufficient practical impact demonstration**: The paper claims VIBEFACE can be used for PAD, deepfake detection, and fairness analysis, but provides no experiments or analysis on these tasks. The core contribution (the dataset) is not accompanied by a standard evaluation protocol or baseline model releases that would enable the community to use it effectively.

### Minor
- The claim of being "the first" to include eKYC-style videos is weakened by the SOTERIA dataset (2024), which also contains videos and demographic metadata, and is cited. The paper should more precisely delineate what eKYC-specific content is absent from SOTERIA.
- Video frame counts, total data volume, and per-scenario duration are not reported, which are important for potential users assessing dataset scale.

### Trivial
None.

## Nice-to-Haves

- Increase the number of subjects to at least 200–300 to make demographic fairness analyses statistically meaningful and position the dataset as a serious benchmark.
- Release a standard evaluation protocol (e.g., fixed train/validation/test splits, evaluation code) and baseline model checkpoints to lower the barrier for adoption.
- Provide more comprehensive fairness metrics (e.g., equal opportunity, demographic parity differences) on the benchmark tasks.
- Compare dataset difficulty against established benchmarks (LFW, CFP-FP, AgeDB) by evaluating the same models on VIBEFACE and those datasets.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Address the sample size limitation either by expanding the dataset or by tempering the claims about serving as a "benchmark for fairness" given the current N=50. The dataset can still be valuable as a focused eKYC evaluation resource, but it is not a large-scale fairness benchmark.
- Replace the binary success-rate verification metric with standard ISO/IEC 19795-1 compliant metrics (FMR, FNMR, EER) and report full ROC/DET curves. This would substantially increase the paper's value to the biometrics community.
- Provide a statistical analysis (confidence intervals, effect sizes) for the reported demographic performance gaps to help readers assess the reliability of those observations.

## Score and Decision

The paper addresses a genuine gap with a well-constructed, ethically-sourced dataset focused on eKYC scenarios. However, the extremely limited subject count (N=50) and the simplistic benchmark evaluation severely undercut its claims of being a comprehensive fairness benchmark. The contribution is a modest, useful resource but does not meet the significance bar for ICLR acceptance given these limitations.

MY FINAL SCORE: <score>4.0</score>  
MY FINAL DECISION: <decision>Reject</decision>