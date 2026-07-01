## Summary

VIBEFACE is a dataset paper introducing a facial image and video dataset (50 subjects, 2,250 images, 1,550 videos) designed to support eKYC (electronic Know Your Client) face verification research. The dataset includes structured eKYC-style video sequences (head rotation, blinking, mouth opening, face touching) alongside still images across five lighting/condition sessions and three mobile devices, with deliberate demographic balancing and GDPR-compliant ethical sourcing. Two benchmark experiments (face detection with MTCNN/RetinaFace/MediaPipe and face verification with ArcFace/MagFace) demonstrate dataset usability.

## Strengths

- **Addresses a genuine gap**: No existing public dataset provides structured eKYC-style video sequences alongside still images. Table 1 shows VIBEFACE is alone among 7 comparison datasets in covering eKYC scenarios—this is a real and well-motivated gap for researchers working on liveness detection and remote identity verification (Abstract, Sec 1, Sec 2, Table 1).

- **Ethically and legally sound collection**: The dataset was collected with informed consent, GDPR compliance, controlled-access licensing, and anonymized identifiers (Sec 3.4, 3.5). Given that MS-Celeb-1M, VGGFace2, and MegaFace were withdrawn over ethical concerns, this is a structural advantage that makes the dataset usable where many prior resources are not.

- **Careful demographic design**: 50:50 gender split, roughly equal racial distribution (26/26/24/24 across 4 groups), three age bands (18–30, 31–50, 51–70), and Fitzpatrick skin type coverage with systematic demographic metadata (facial hair, piercings, hair color) enable fairness analyses that many prior datasets cannot support (Sec 3.1, Figure 1).

- **Multi-session, multi-condition, multi-device design**: Five sessions (artificial light, flash, glasses, natural light, weak natural light) with three consumer smartphones provide systematic and documented variation in conditions that matter for verification (Sec 3.3, Table 2).

## Weaknesses

### Major

- **50 subjects is too few for the fairness/robustness claims the paper makes**: The paper positions VIBEFACE as "a new benchmark for evaluating the robustness and fairness of biometric verification systems" (Abstract). With 50 subjects, the demographic subgroups are tiny (African ~13, Caucasian ~13, East Asian ~12, South Asian ~12; age 51–70: 14 subjects). The claim in Sec 4.1 that "demographic analysis revealed minimal variation in detection rates across gender and age groups" carries no statistical weight — no confidence intervals, significance tests, or error bounds are reported anywhere. Tables 3 and 4 report values to the 3rd–4th decimal place (e.g., 0.999 vs 1.000) as if these differences are meaningful. The dataset may still be a useful resource, but the fairness/benchmark framing is mismatched to what the sample size can support. No limitations section acknowledges this.

- **Verification protocol has significant methodological problems**: (a) Performance is measured as frame-level pass rate ("percentage of frames in which the face was correctly authenticated") rather than video-level accept/reject — frames within a video are highly correlated, making this metric difficult to interpret for real verification use. (b) A single fixed similarity threshold of 0.5 is used across both ArcFace and MagFace, across all sessions and scenarios; these models produce different score distributions, so threshold effects could drive reported differences. (c) No standard verification metrics (EER, TAR@FAR, AUC, ROC curves) are reported. (d) The reference image is a rear-camera flash photo (Session B), while queries are front-camera selfies under different lighting — a domain shift not discussed or controlled for (Sec 4.2, Table 4).

- **Benchmark experiments do not demonstrate the dataset's unique value**: The experiments apply off-the-shelf models and report that RetinaFace/MediaPipe outperform MTCNN (known) and ArcFace outperforms MagFace (known), with off-angle poses and poor lighting reducing accuracy (expected). No experiment isolates what the eKYC-specific video content contributes beyond what still images capture. No comparison is run on existing datasets (MOBIO, SOTERIA, OULU-NPU) using the same protocol to show VIBEFACE reveals different or deeper insights. The paper does not answer the core question a dataset paper must answer: *What does this dataset enable that existing datasets do not?* (Sec 4).

- **Controlled studio collection contradicts the "realistic/unconstrained" motivation**: The paper motivates the dataset through "unconstrained conditions — at home, in variable lighting" (Sec 1). However, collection was "in a controlled studio environment" with "trained operators" and participants performing scripted actions "continuously supervised" (Sec 3). Lighting conditions, while varied, were studio-controlled. Real eKYC sessions involve a single individual alone at home with unpredictable lighting, background clutter, camera shake, and natural (not scripted) facial movements. The paper presents studio recordings as a proxy for natural eKYC behavior without validating this proxy or discussing its limitations.

### Minor

- **No training or fine-tuning experiments**: All models are used off-the-shelf pre-trained; none is trained or fine-tuned on VIBEFACE data. For a dataset paper at a top venue, this limits the demonstration that the dataset provides useful training signal for eKYC scenarios. (Partially mitigated if the dataset is primarily an evaluation benchmark, but the paper claims both uses.)

- **No standardized evaluation protocol or data splits**: The paper does not define train/val/test splits, specify a reusable evaluation protocol with standard metrics, or provide a reference implementation. Without these, the dataset cannot function as a shared benchmark where results are comparable across groups.

- **Selfie video scenario (scenario 11) excluded from all experiments**: The most natural, unscripted recording behavior (raising the phone from below to eye level) was excluded "due to incomplete coverage across sessions" (Sec 4.1). This limitation is disclosed but not discussed in terms of what it means for coverage of naturalistic behavior.

### Trivial

- The Conclusions mention broader applications (PAD, deepfake detection) without supporting samples or experiments. These are signaled as having "potential" (Sec 5), which is fine, but the framing could more explicitly flag them as untested future directions.

## Nice-to-Haves

- Run an experiment that isolates the dataset's unique value: compare verification accuracy on eKYC video frames vs. standardized stills of the same subjects, quantifying the gap between idealized and realistic verification.
- Define train/val/test splits and provide a reference implementation with standard verification metrics (EER, TAR@FAR) so the dataset can serve as a reusable benchmark.
- Add a dedicated limitations section candidly discussing the 50-subject scale, studio setting, and scripted behavior implications.
- Train or fine-tune a verification model on VIBEFACE data and evaluate on an independent eKYC-style test set to demonstrate training value.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Missing related works (Racial Faces in the Wild, BUPT-Xface)**: Per policy, I cannot confirm these exist or require their addition. Removed.
- **"Table 1 is useful but formatted very poorly in the extracted text"**: Parser artifact, not an author issue. Removed.
- **"The claim about no datasets with eKYC-style videos is stated without a systematic survey"**: Table 1 covers 7 datasets showing VIBEFACE as the only one with eKYC ✓; the claim is sufficiently supported. Removed as overly nitpicky.
- **"SOTERIA has 70 subjects vs. VIBEFACE's 50, so 'better balance' across fewer subjects is a trade-off"**: The paper claims "better demographic balance" within the dataset's own demographics (more even race/age distribution), not overall superiority. Partially addressed by Table 1. Removed.

## Novel Insights

The reviews surface a consistent tension: the paper does several things right (ethical sourcing, demographic balance, multi-condition capture), but the central argument — that this dataset constitutes a meaningful fairness/robustness benchmark for eKYC — is undermined by the small subject pool (50), the controlled studio setting (vs. the "unconstrained at-home" framing), and the absence of experiments that isolate what the eKYC-specific videos uniquely contribute. The verification protocol compounds this with methodological issues (frame-level metrics, fixed threshold, no standard verification measures). The key takeaway is that the dataset may still be a valuable community resource, but the paper needs to either (a) retract the fairness/benchmark framing to match the scale, or (b) provide much stronger experimental evidence that the eKYC video content reveals failure modes that still-image datasets miss — and fix the verification methodology.

## Suggestions

1. Add a candid limitations section acknowledging the 50-subject scale and controlled-studio setting, with explicit discussion of what claims the dataset can and cannot support.
2. Run at least one experiment isolating the eKYC-specific value — e.g., compare verification rates on eKYC video frames vs. standardized stills of the same subjects to quantify the realism gap.
3. Replace frame-level verification with video-level metrics (EER, TAR@FAR) and report confidence intervals or bootstrap estimates for all demographic breakdowns.
4. Define and release an official evaluation protocol with train/val/test splits and a reference implementation.

---

**Calibration Anchors (retrieved from deepreview_13k_calibration):**

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| UDC-VIT (DNBwlQYA90) | 6.00 | Round 1 | Real-world UDC video dataset with novel capture system, cross-dataset comparison, model training. VIBEFACE is weaker experimentally (no training, no cross-dataset comparison, no novel capture method). |
| Face-Human-Bench (x1Bk51SCL9) | 5.75 | Round 1 | Comprehensive face/human benchmark evaluating 25 MLLMs. VIBEFACE has smaller scale and weaker empirical validation. |
| ColorCubeNet (dEGYODD6iU) | 3.67 | Round 1 | PAD fairness method with incremental contribution. VIBEFACE has similar magnitude of issues but different type (dataset vs. method paper). |
| ID-Booth (NWvsm2VxAM) | 3.00 | Round 1 | Identity-consistent generation with limited novelty. VIBEFACE has stronger motivation and ethical positioning. |
| Person Detection Bias (tC1b9DBWww) | 2.50 | Round 1 | Bias analysis with weak experimental design. VIBEFACE has genuine data contribution that this paper lacks. |
| Face Recognition Comparison (CCo8ElCT7v) | 4.25 | Round 2 | Benchmark-style paper comparing ViT vs CNN for face recognition. VIBEFACE has a stronger data contribution but weaker experiments. |
| Cross-modal Biometrics (WjxgruI6A2) | 3.67 | Round 2 | Voice-face matching with limited novelty. Comparable quality level to VIBEFACE. |

**Round 1 Bracket:** Roughly between 3.0 and 4.5, narrowed to **3.5** based on comparison to ID-Booth (3.00, weaker motivation/data contribution), ColorCubeNet (3.67, comparable quality), and Face-Human-Bench (5.75, stronger validation).

**Final Score Rationale:** The dataset fills a genuine gap and is ethically collected with careful demographic design — real merits that prevent a 1–2 score. However, the paper is not at the level expected for a top venue: the fairness/benchmark claims are unsupported by the sample size, the verification protocol has methodological flaws, the experiments do not demonstrate what the dataset uniquely enables, and the framing is contradicted by the controlled-studio collection. The paper needs substantial additional evidence before it would meet the acceptance bar.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>