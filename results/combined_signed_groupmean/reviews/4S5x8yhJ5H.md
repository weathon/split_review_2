Now I have all the calibration data needed. Let me compile the final review.

**Round 1 bracket**: 3.0–4.5. The paper has genuine strengths (novel niche, ethical compliance, structured protocol) that place it well above strong rejects (~1-2), but the two severe weaknesses (verification benchmark is not proper verification, scale too small for demographic claims) prevent it from reaching the borderline-accept range (~5+). Anchors HiDF (4.25, Reject) and the CNN-vs-ViT comparison (4.25, Reject) show that rejected dataset/survey papers at this level have meaningful contributions but fatal methodological gaps.

**Round 2 narrowing**: Comparing against FIUBench (5.40, Accept), which had a small dataset but sound evaluation, VIBEFACE has a more fundamental error — the verification benchmark simply does not measure what it claims to measure (no impostor pairs). Compared to HiDF (4.25, Reject), VIBEFACE's verification evaluation error is more severe than HiDF's single-tool limitation. The final score of **3.5** reflects a paper whose dataset contribution is real and whose ethical framework is exemplary, but whose core evaluation methodology contains a verifiable error that undermines the stated claims, and whose scale is insufficient for the fairness analysis presented.

---

## Summary

VIBEFACE introduces a new facial biometric dataset (2,250 images + 1,550 videos from 50 subjects) targeting eKYC-style video verification scenarios — head rotations, blinks, mouth movements, face-touching, partial occlusions — that are absent from existing public datasets. The data collection emphasizes demographic balance (50:50 gender, ~25% per racial group, ages 18–69) and full GDPR/EU AI Act compliance. Benchmark experiments with standard face detectors and verification models demonstrate basic dataset utility.

## Strengths

- **Genuinely underexplored niche in an area of practical importance.** No existing public dataset specifically captures eKYC-style video sequences with head rotations, blinks, mouth movements, face-touching, and partial occlusions. The 18 scenarios (especially 12–18) are well-motivated by actual eKYC procedures. This is the paper's clearest contribution and is not overstated.

- **Exemplary demographic balance and ethical compliance.** The dataset is explicitly balanced 50:50 across gender, ~25% per racial group across four categories, and across three age bands (18–69). Informed consent, GDPR compliance, EU AI Act compliance, controlled-access licensing, anonymization, and right-to-withdraw are all documented. This sets a strong positive standard, especially in contrast to the many web-scraped face datasets that have been withdrawn due to ethical failures.

- **Well-structured acquisition protocol.** The five sessions (four lighting conditions + eyeglasses), use of three consumer smartphones, and the distinction between operator-captured standardized photos and participant-captured selfie photos/videos are thoughtfully designed and clearly documented. Combining back-camera and front-camera capture across different scenarios reflects real operational conditions.

## Weaknesses

### Fatal

- **The face verification evaluation does not actually measure verification.** Section 4.2 uses a single reference image per subject and a fixed threshold of 0.5, reporting the percentage of query frames where similarity exceeds the threshold. **There is no mention of impostor pairs, no cross-subject comparisons, no false accept rate, no false reject rate, no ROC curves, no AUC, no EER.** The reported metric is at best a genuine match rate, not a verification accuracy. A system could achieve 100% on this metric while accepting every impostor. Table 4 is fundamentally uninterpretable as verification performance. This is not a minor methodological gap — it means the paper's second benchmark task does not measure what it claims to measure. (Section 4.2, lines 335–341; Table 4)

### Major

- **At 50 subjects (~12–13 per racial group, 14–19 per age band), the dataset is too small to support the demographic fairness and robustness analyses presented as findings.** The demographic breakdowns in Tables 3 and 4 report performance differences across minuscule groups with no confidence intervals, error bars, or significance tests. Claims such as "MTCNN showed reduced detection performance among individuals of African descent" (Section 4.1) are drawn from ~13-person subgroups and are statistically uninterpretable. The paper itself lists MOBIO (150 subjects), WMCA (72), and SOTERIA (70) as prior work — VIBEFACE has fewer subjects than all of them. Balance at n=50 does not compensate for lack of scale. (Section 3.1, Tables 3–4)

### Minor

- **Device is confounded with session.** Section 3.3 states "the acquisition device was randomly chosen before each session," meaning device type and session conditions (lighting, eyeglasses) are perfectly confounded. It is impossible to attribute performance differences to lighting, eyeglasses, or device hardware independently. (Section 3.3, line 187)

- **No recommended evaluation splits or protocol are provided.** For a dataset positioned as a benchmark, the lack of predefined gallery/probe splits and train/test partitions hinders comparability of future results. Different users will use the data differently, making results difficult to compare.

- **The data was collected in a controlled studio environment with scripted actions, not in genuine unconstrained eKYC conditions.** While the paper acknowledges the studio setting, it simultaneously claims "realistic eKYC sequences" and "unconstrained conditions" (lines 15, 31) without transparently discussing this gap as a limitation. The mismatch between the framing and the actual collection conditions should be acknowledged. (Section 3, line 73)

### Trivial

None.

## Nice-to-Haves

- **Cross-dataset comparative experiments** would substantiate the claim that VIBEFACE is needed. Demonstrating that models that look fair on LFW or MOBIO reveal biases on VIBEFACE would strengthen the argument that the dataset fills an empirical gap, not just a categorical one.
- **Failure case visualization** would help the community understand where and why models struggle on this data.
- **Future work on scaling** to at least 200–300 subjects would transform the dataset from a pilot into a proper fairness/robustness benchmark.

## Removed Points

- **No comparative experiments against existing datasets** — removed because cross-dataset comparison is a nice-to-have for a dataset paper, not a requirement. The primary contribution is the dataset itself; the benchmarks demonstrate basic utility. Moved to Nice-to-Haves.
- **Session B asymmetry** — removed as a presentational observation that does not affect the core contribution.
- **Statistical analysis complaint** — merged into the Major weakness about insufficient scale.
- **Table 1 comparison being misleading** — removed; Table 1 checks binary properties (gender balance, race balance, age balance), which is standard practice. The paper is transparent about actual numbers in Section 3.1.
- **No discussion of failure cases** — removed as a non-essential addition for a dataset paper. Moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the verification benchmark fundamentally.** Define a proper protocol with: (a) genuine pairs (same subject, reference vs. query) and impostor pairs (different subjects, reference vs. query); (b) report standard metrics — AUC, EER, or FAR@FRR at operating points; (c) either justify the threshold via ROC analysis or remove it. Without these, the "verification" task does not measure verification.
2. **Collect more subjects** (at least 200–300) before positioning the dataset as a fairness/robustness benchmark. At 50 subjects, demographic subgroup analyses are not meaningful.
3. **Provide recommended evaluation splits** (gallery/probe definitions, cross-validation folds) to ensure comparability across future work using the dataset.
4. **Acknowledge the studio-vs-real-world gap** transparently in a limitations paragraph rather than framing studio recordings as "realistic eKYC."

---

## Score and Decision

**Round 1 bracket**: 3.0–4.5. Anchors retrieved: HiDF (4.25, Reject), CNN-vs-ViT comparison (4.25, Reject), FIUBench (5.40, Accept). The paper's strengths (niche + ethics + protocol) are genuine, but its weaknesses are more severe than those of rejected anchors.

**Round 2 — itemized comparison**:
- vs. HiDF (4.25, Reject): HiDF had a high-quality dataset but was rejected for limited generation diversity and evaluation gaps. VIBEFACE has a more fundamental methodological error (verification without impostor pairs) and a scale problem, but compensates with stronger ethical documentation.
- vs. FIUBench (5.40, Accept): FIUBench had small scale too but its evaluation pipeline was sound for its stated task. VIBEFACE's evaluation is not sound for its stated task, which makes it clearly weaker.
- vs. ILLUSION (6.00, Accept): ILLUSION is an order of magnitude larger and had proper evaluation protocols. VIBEFACE does not compare favorably.

**Final placement**: The two decisive weaknesses (-10.00 each from the scoring model) outweigh the strong strengths (+8.97 to +9.78). The paper's dataset contribution is real and the ethical framework is exemplary, but the verification benchmark is fundamentally wrong (no impostor pairs → does not measure verification) and the scale is insufficient for the demographic claims made. These are fixable issues, but as presented, the paper does not deliver on its stated contributions.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>