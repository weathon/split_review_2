## Summary

VIBEFACE is a multimodal facial biometric dataset designed specifically for electronic Know Your Client (eKYC) scenarios. It contains 2,250 still images and 1,550 short videos from 50 subjects, balanced across gender, race, and age, captured under five lighting conditions with and without eyeglasses using consumer smartphones. The paper also presents benchmark results for face detection (MTCNN, RetinaFace, MediaPipe) and face verification (ArcFace, MagFace) to demonstrate the dataset's utility.

## Strengths

- **Targeted real-world gap**: The dataset explicitly addresses eKYC verification scenarios, which are increasingly important for financial and regulatory compliance but are not covered by existing public datasets. The inclusion of specific eKYC-style video actions (head rotation, blinking, expression changes, etc.) is a clear and valuable contribution.
- **Strong ethical and legal compliance**: Data collection followed informed consent, GDPR, and the EU AI Act. Participants could withdraw at any time, and data is anonymized with randomized identifiers. The controlled-access license for non-commercial research use is appropriate for sensitive biometric data.
- **Demographic balance**: The dataset achieves near-equal representation across gender (50:50), four racial categories (≈25% each), and three age groups (18–30, 31–50, 51–70), which is rare among existing biometric datasets and enables meaningful fairness analysis.
- **Multiple acquisition conditions**: Five sessions varying lighting (artificial, flash, natural, weak natural) and the presence of eyeglasses, combined with three different smartphone models, provide realistic variability for robustness evaluation.

## Weaknesses

### Fatal
None.

### Major

- **Small subject count (N=50) severely limits statistical reliability**: With only 50 subjects, each demographic subgroup contains 12–13 individuals. The benchmark results reporting performance differences across race, age, and gender are therefore based on very small samples and may reflect noise rather than true demographic bias. This undermines the dataset's primary selling point for fairness evaluation. For a dataset intended as a benchmark, the subject pool is too small to draw robust conclusions about model fairness or generalization.
- **Benchmark evaluation is overly simplistic and not aligned with eKYC practice**: Verification is evaluated at the frame level using a fixed similarity threshold of 0.5, without proper metrics such as FAR/FRR, ROC curves, or Equal Error Rate. Video-based verification in real eKYC systems typically aggregates temporal information or uses video-specific models; frame-level thresholding does not reflect practical usage. The absence of a liveness detection benchmark is a notable omission given the dataset's eKYC focus.
- **Controlled studio environment limits realism**: Despite claims of "realistic operational settings," all data was collected in a studio with standardized instructions and operator supervision. True eKYC sessions occur in unconstrained home environments with variable backgrounds, unpredictable lighting, and user-driven behavior. The controlled setup reduces the dataset's ability to test generalization to genuine eKYC conditions.

### Minor

- **No analysis of video quality or temporal characteristics**: The paper does not report video duration, frame counts, or temporal consistency of the recorded actions. This information is important for researchers planning to use the videos.
- **Fitzpatrick skin tone distribution mentioned but not provided**: The paper states that skin tones reflect the full Fitzpatrick scale but does not present the actual distribution, which would be useful for fairness analysis.
- **Single reference image for verification**: Using only one frontal flash image as the reference template may not be representative; multiple reference images or a gallery-based protocol would be more standard.

### Trivial
None.

## Nice-to-Haves

- Include a larger subject pool (e.g., 200+) to make demographic analyses statistically meaningful.
- Provide a proper evaluation protocol with cross-validation, AUC/EER metrics, and video-level verification.
- Add a liveness detection benchmark using the eKYC video scenarios.
- Collect additional data in uncontrolled home environments to increase realism.
- Release the dataset with pre-computed face embeddings and standardized train/validation/test splits.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Increase the number of subjects to at least 200 to enable reliable subgroup analysis and improve the dataset's value as a fairness benchmark.
- Replace the frame-level verification benchmark with a video-level protocol (e.g., average similarity over frames or a temporal model) and report standard metrics (AUC, EER, TAR@FAR).
- Include a presentation attack detection (PAD) benchmark using the existing bona fide videos, as the paper itself suggests this as a future application.
- Provide detailed metadata on video duration, frame rate, and resolution for each recording.

## Score and Decision

The dataset fills a genuine gap by focusing on eKYC scenarios with demographic balance and ethical rigor. However, the very small subject pool (N=50) and simplistic benchmark evaluation significantly limit its practical utility for drawing reliable conclusions about fairness or robustness. The contribution is valuable but not yet mature enough for a top venue.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>