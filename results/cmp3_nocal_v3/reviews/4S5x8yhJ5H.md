**VERIFICATION NOTE:** I have read the paper in full and verified every criticism against the actual text before including it. Claims that are speculative, misread the paper, or constitute formatting nitpicks have been removed.

---

## Summary

This paper introduces VIBEFACE, a multimodal dataset of 2,250 facial images and 1,550 short videos from 50 subjects, designed to support face verification evaluation in eKYC (electronic Know Your Client) scenarios. The dataset is notable for its systematic session design (varying lighting, glasses, and camera perspectives across five sessions), its 18 scenarios including both standardized and eKYC-mimicking video sequences, its demographic balance across gender (50:50), race (≈25% per four groups), and age (three bands), and its thorough ethical/legal compliance (GDPR, AI Act, informed consent, controlled-access licensing). Benchmark evaluations of face detection (MTCNN, RetinaFace, MediaPipe) and face verification (ArcFace, MagFace) are provided to demonstrate dataset utility.

## Strengths

1. **Genuinely novel eKYC focus.** The paper correctly identifies that existing publicly available datasets (MOBIO, OULU-NPU, WMCA, SOTERIA) lack video sequences that mimic the head rotations, blinking, expression changes, and face-touching actions used in eKYC verification workflows (scenarios 12–18, Section 3.2). This is a real gap, and the dataset's scenario design is thoughtfully constructed around it.

2. **Demonstrably better demographic balance than comparable datasets.** Table 1 shows that VIBEFACE is the only dataset among its peers that explicitly reports balance across gender (50:50), four racial groups (≈25% each), and three age bands (18–30, 31–50, 51–70). Comparable datasets either lack demographic metadata entirely (MOBIO, OULU-NPU, WMCA, HQ-WMCA) or have known gaps (SOTERIA lacks age balance). The comparison in Table 1 is transparent and honest.

3. **Exemplary ethical and legal compliance.** Section 3.4 documents informed consent, GDPR compliance, AI Act compliance, the right to withdraw, anonymization via randomized identifiers, and controlled-access licensing restricting use to non-commercial academic research. This sets a high standard that contrasts favorably with Internet-crawled datasets (VGGFace2, MS-Celeb-1M, MegaFace) that have been withdrawn over privacy concerns.

4. **Systematic and well-documented dataset design.** The five-session structure (Section 3.3, Table 2) with varying lighting conditions (artificial, flash, natural daylight, weak natural light) and the presence/absence of eyeglasses is clearly described and motivated. The use of three consumer smartphones (Xiaomi Redmi Note 13, iPhone 13, Samsung Galaxy A35) and the consistent resolution specifications (1920×1080 for video, ≥2316×3088 for images) are well-documented.

## Weaknesses

### Fatal

None. The dataset itself is a genuine contribution; the flaws are in the evaluation and framing, which are fixable.

### Major

1. **Verification benchmark lacks impostor trials, making Table 4 uninterpretable as verification performance.** The protocol (Section 4.2) compares each query frame against the subject's own reference image and reports the percentage exceeding a threshold of 0.5. There are **no cross-identity comparisons** — the paper never compares queries against reference images of *different* subjects. Without impostor trials, there is no way to measure false positive rates, compute ROC curves, or determine TAR@FAR. The reported numbers in Table 4 are genuine-match rates only, and it is impossible to know whether a threshold of 0.5 produces meaningful discrimination or is trivially satisfied/failed by most pairs. The paper claims these results demonstrate "verification" performance, but the evaluation does not measure a system's ability to *distinguish between identities*. This is compounded by two undiscussed design choices: (a) the reference image is from Session B (rear-camera flash), while all query images/videos are from front-camera sessions (A, C, D, E), introducing an unanalyzed camera-domain gap; (b) the 0.5 threshold is stated without any justification, calibration, or analysis.

### Minor

2. **Demographic fairness claims rest on very small subgroups without statistical support.** The dataset has 50 subjects, with 12–13 per racial group and roughly 14–19 per age band. Tables 3 and 4 report performance breakdowns across these groups (e.g., MTCNN frontal-view detection: 0.812 for African subjects vs. 0.984 for East Asian subjects), but no confidence intervals, standard deviations, or statistical significance tests are provided. With such small samples, observed differences could be driven by a single outlier. The paper states findings like "minimal variation across gender and age groups" and characterizes racial disparities as findings, when the data supports only preliminary observations.

3. **No cross-dataset comparison demonstrating the dataset's unique value.** The paper benchmarks models on VIBEFACE but never runs the *same models* on existing datasets (MOBIO, OULU-NPU, SOTERIA, etc.). The claim that VIBEFACE surfaces challenges absent from prior datasets would be substantially strengthened by showing, for example, that models performing well on existing datasets struggle on VIBEFACE's eKYC-specific scenarios, or that demographic disparities differ. Without this, the benchmark results serve mainly as sanity checks rather than evidence of new scientific value.

4. **The dataset scale (50 subjects) constrains the paper's claims more than is acknowledged.** VIBEFACE is the smallest among comparable datasets (MOBIO: 150, OULU-NPU: 55, WMCA: 72, SOTERIA: 70 — Table 1). The conclusion that the dataset is "a resource for advancing fair and robust face biometrics research" does not adequately discuss that 50 subjects (12–13 per group) sharply limits the kinds of analysis the dataset can support, especially for demographic fairness auditing. An explicit limitations section is absent.

5. **Minor overstatement about "authentic" eKYC content.** The abstract accurately describes the videos as "sequences that explicitly mimic eKYC workflows" (line 9), but line 24 claims "there are no publicly available datasets that include authentic eKYC-style facial videos alongside still images." The data was collected in a controlled studio (line 73) with scripted actions, not in actual eKYC sessions. "Authentic" moderately overstates the relationship to real-world eKYC interactions.

### Trivial

6. **Missing video statistics.** The paper states there are 1,550 videos but never provides their duration, frame count, or total runtime per subject or in aggregate. Only the 6 fps frame-sampling rate for evaluation and a "at least three seconds" note for one scenario are given.

7. **"High-quality" is asserted but not quantified.** Resolution is provided, but no quantitative quality metrics (sharpness, SNR, compression ratio) are reported.

8. **No explicit limitations section.** The paper would benefit from a dedicated discussion of the dataset's constraints (scale, controlled studio setting, scripted actions) rather than leaving them implicit.

## Nice-to-Haves

- **Cross-dataset comparison**: Running the same verification models on MOBIO or SOTERIA with a comparable protocol would demonstrate whether VIBEFACE surfaces different failure modes or demographic disparities.
- **Confidence intervals for demographic breakdowns**: Bootstrapped confidence intervals or significance tests would help readers assess whether observed group differences are meaningful.
- **Video duration metadata**: Including per-video duration and frame counts would aid reproducibility and dataset usability.
- **Training/evaluation guidance**: A brief note on whether the dataset is intended for training (unlikely at 50 subjects), evaluation, or both would clarify its intended use.

## Removed Points

These points were flagged during the review process but are removed from the main review for the following reasons:

1. **"Reference access (TinyURL/temporary password)"** — Comment about the review-access mechanism, not a paper quality issue. Removed as a review-process observation.
2. **"No discussion of whether the dataset is intended for training, evaluation, or both"** — The paper's framing as a benchmark/evaluation resource and the 50-subject scale make this sufficiently clear implicitly. Removed as overly nitpicky.
3. **"The threshold of 0.5 is uncalibrated / needs cross-validation"** — This is already included in the Major weakness about the verification benchmark; treating it as a separate point would duplicate the same criticism. Merged into Weakness 1.
4. **"Video duration and statistics are missing"** — This is retained as Trivial (point 6 above), not removed. (Kept.)
5. **Generic strengths about "important problem"** — The strengths section retains only concrete, paper-specific strengths. Generic claims about importance were dropped.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm that the dataset fills a genuine gap in eKYC-focused evaluation resources and is well-documented ethically and demographically, but do not surface additional novel observations beyond what the paper itself states.

## Suggestions

1. **Fix the verification evaluation protocol.** This is the single most important improvement. Add impostor trials (comparing query frames against reference images of *different* subjects), report ROC curves or TAR@FAR at standard operating points, and either justify the threshold or eliminate it in favor of threshold-free evaluation (e.g., AUC). Also discuss or control for the camera-domain gap between the reference image (rear-camera flash, Session B) and query images (front-camera, Sessions A/C/D/E).

2. **Temper the demographic claims.** Frame the demographic analyses as preliminary observations rather than definitive findings. Add confidence intervals or note the small sample sizes explicitly. Acknowledge that 12–13 subjects per group is insufficient for reliable fairness conclusions.

3. **Add a cross-dataset comparison.** Even a small-scale comparison — running the same verification models on MOBIO or SOTERIA with a similar reference-query protocol — would substantially strengthen the claim that VIBEFACE surfaces challenges not present in existing datasets.

4. **Add a limitations section.** Explicitly discuss the dataset's scale (50 subjects), controlled studio setting, and the scripted (rather than truly unconstrained) nature of the eKYC-style recordings.

---

## Score and Decision

The dataset itself is a genuine contribution: it fills a concrete gap (eKYC-focused evaluation with demographic balance and ethical compliance), is systematically designed, and is thoroughly documented. However, the verification benchmark in its current form is not a valid measure of verification performance due to the absence of impostor trials, and the demographic claims are overstated relative to the statistical power of the data. These issues are fixable with revisions, and the dataset's core value is not invalidated by them.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>