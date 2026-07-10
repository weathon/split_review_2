Now let me produce the final consolidated review.

---

## Summary

VIBEFACE is a dataset paper releasing a multimodal (images + videos) facial dataset of 50 subjects, designed specifically to capture eKYC (electronic Know Your Client) verification scenarios—head rotations, blinking, mouth opening, face-touching—that existing public datasets do not cover. The dataset is ethically sourced (GDPR-compliant, informed consent, controlled access) and demographically balanced across gender, race, and age. Benchmark experiments for face detection (MTCNN, RetinaFace, MediaPipe) and face verification (ArcFace, MagFace) are presented.

## Strengths

- **Genuinely novel gap-filling (Section 1, Table 1).** The paper correctly identifies that no existing public dataset includes eKYC-style video recordings mimicking real identity-verification workflows. This is a real and timely gap given the growing regulatory importance of eKYC in banking and fintech. The dataset fills a clearly defined void.

- **Exemplary ethical sourcing (Section 3.4).** The dataset was collected with informed consent, full GDPR compliance, anonymized identifiers, and a controlled-access license that prohibits re-identification and commercial use. This stands in sharp contrast to crawled datasets (VGGFace2, MS-Celeb-1M, MegaFace) that have been withdrawn over ethical concerns, and provides a positive template for future facial dataset collection.

- **Demographic balance across multiple axes (Section 3.1, Figure 1).** The dataset achieves 50:50 gender balance (25M/25F), near-equal distribution across four self-identified racial categories (~25% each), and coverage across three age brackets (18–30, 31–50, 51–70). This is meaningfully better than most prior datasets that lack demographic metadata or are strongly skewed.

- **Multi-condition capture design (Section 3.3, Table 2).** Five sessions (artificial light, flash, artificial+glasses, natural light, weak natural light) with three different smartphone models, across standardized poses and selfie angles. This is a carefully designed acquisition protocol that reflects real-world variability.

## Weaknesses

### Major

- **N=50 is too small to support the paper's fairness/demographic-bias claims.** The abstract and introduction frame the dataset as enabling "fair and generalizable verification systems" and detecting "biased outcomes for under-represented groups." However, with 50 subjects total—split into 12–13 per racial group and 14–19 per age/gender cell—the statistical power to detect meaningful demographic differences is essentially zero. The differences reported in Tables 3 and 4 (e.g., ArcFace OAV: African 0.490 vs. Caucasian 0.468 vs. East Asian 0.460 vs. South Asian 0.509) are never tested for statistical significance, and with these sample sizes even fairly large disparities would not be reliable. The paper's fairness framing needs to be scaled back to match what 50 subjects can support (demonstrating the eKYC scenario design works), and demographic breakdowns should include variance estimates. This is not a flaw in the dataset itself but a substantial mismatch between claims and evidence.

- **The face verification evaluation uses a non-standard, unvalidated protocol that makes results incomparable to existing literature.** Three specific problems: (a) **Fixed threshold of 0.5 (Section 4.2)** — face verification is universally evaluated using TAR@FAR, EER, or ROC curves, not a single arbitrary threshold whose choice is never justified. (b) **Per-frame verification accuracy (Section 4.2)** — treating each video frame as an independent verification trial is not how video verification works in practice or in the literature; real systems aggregate across frames. Frame-level matching inflates apparent difficulty and produces numbers with no practical interpretation (e.g., ArcFace at only 50.9% for off-angle views). (c) **Single reference image from flash session (Section 4.2)** — using one frontal flash image as the enrollment template means off-angle/poorly-lit queries are matched against a very different-looking reference; the low OAV rates (0.274–0.509) primarily reflect pose mismatch. Together these issues mean the benchmark conclusions ("ArcFace consistently outperformed MagFace across scenarios...") may be true but the evidence is methodologically too weak to be relied upon.

### Minor

- **The face detection benchmark saturates on modern detectors and is not informative.** RetinaFace achieves 1.000 detection rate in almost all scenarios and demographic groups (Table 3). MediaPipe is close behind (0.924–1.000). Only MTCNN (a 2016 model) shows meaningful variation. A detection benchmark where modern detectors saturate does not demonstrate that the dataset presents challenging conditions or differentiates detector performance.

- **No training or fine-tuning experiments.** The paper only runs inference with off-the-shelf models. For a dataset paper, the most convincing demonstration of value would be to show that training/fine-tuning on this data reveals new insights or improves eKYC-style task performance. Without at least one experiment that *uses* the dataset beyond testing, the contribution feels incomplete.

- **Missing dataset details needed for reproducibility.** Video durations, frame counts per scenario, and image quality distributions are not reported. These matter for researchers wanting to adopt the dataset.

### Trivial

- The ISO standard reference (Section 3.1) says "ISO Central Secretary (2011) standard" but does not specify the standard number or how compliance was ensured. This should be clarified or removed.

## Nice-to-Haves

- A qualitative analysis of verification failure cases (e.g., which eKYC scenarios cause the most failures) would be far more informative than aggregate accuracy numbers.
- Verification results broken down by capture device would be a natural analysis given the multi-device design.

## Removed Points

These points were flagged for removal; treat them with caution:
- Criticism about Table 1 accuracy for MOBIO (claimed MOBIO collects demographic data contrary to the paper's table)—cannot be verified without external sources; removed per rules.
- Criticisms about "no error analysis or qualitative failure cases"—a nice-to-have, not a core weakness.
- Section-by-section speculations about what "may" be true about competitor datasets.
- Formatting/style nitpicks.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the verification protocol.** Use standard metrics (EER, TAR@FAR=1e-3, 1e-4) from continuous similarity scores. Aggregate video frames via mean/max similarity or quality-based selection. Add multiple enrollment images or at minimum report verification at multiple operating points.
2. **Acknowledge the N=50 limitation explicitly.** Frame the demographic reporting as descriptive, add confidence intervals or variance estimates, and substantially scale back the fairness/generalizability claims to match what the sample size supports.
3. **Add at least one training or analysis experiment** that demonstrates what the dataset enables (e.g., analyzing which eKYC scenario properties cause verification failures, or fine-tuning a model and measuring improvement on eKYC-specific challenges).

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>