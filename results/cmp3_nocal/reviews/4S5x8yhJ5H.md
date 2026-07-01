## Summary

VIBEFACE is a multimodal facial dataset (2,250 images, 1,550 videos from 50 subjects) designed specifically for eKYC (electronic Know Your Client) verification scenarios. The dataset features controlled demographic balance across gender (50:50), race (four groups, ~25% each), and three age bands, with five acquisition sessions varying lighting, eyeglasses, and camera device. The paper also presents benchmark face detection and verification experiments using off-the-shelf models.

## Strengths

- **eKYC focus fills a specific gap.** As documented in Table 1, no prior publicly available facial dataset includes video sequences that mimic eKYC workflows—head rotations, blinking, expression changes, mouth movements. The scenarios defined in Section 3.2 map directly onto real eKYC procedures used in financial and regulatory compliance.

- **Demographic balance is well-designed and honestly documented.** Figure 1 and Section 3.1 show a near-even four-way racial split (26/26/24/24%), a precise 50:50 gender split, and coverage across three age bands (18–30, 31–50, 51–70). The inclusion of Fitzpatrick skin tone annotations further supports fairness analysis. This is materially better than most datasets compared in Table 1, where demographic metadata is often missing or imbalanced.

- **Ethical and legal sourcing is a substantive contribution.** Section 3.4 documents GDPR compliance, informed consent, controlled-access licensing, and anonymization. Given that MS-Celeb-1M, VGGFace2, and MegaFace have been withdrawn over consent issues (Section 2), the paper's emphasis on ethical collection is timely and addresses a real bottleneck in the field.

- **Multi-session, multi-device acquisition protocol.** Sessions A–E (Section 3.3, Table 2) systematically vary lighting (artificial, flash, natural, weak natural), eyeglasses, and camera device (three distinct consumer smartphones). This structured variation supports controlled analysis of individual factors and is more comprehensive than many competing datasets.

## Weaknesses

### Fatal
None.

### Major

1. **The dataset's scale (50 subjects) undermines the fairness-benchmarking claims made in the paper.** With ~12–13 subjects per racial category and as few as 6 in one age-gender cell (51–70 female), the demographic analyses in Tables 3 and 4 lack statistical power. A single idiosyncratic face can dominate a group's results. The paper reports no confidence intervals, no statistical tests, and no per-subject variance, yet draws demographic conclusions (e.g., "Both models performed slightly worse on the Caucasian subgroup" from Table 4 where ArcFace OAV scores are Afr. 0.490, Cauc. 0.468, EA 0.460, SA 0.509). The differences are small and potentially noise given the sample size. The abstract frames VIBEFACE as "a new benchmark for evaluating the robustness and fairness of biometric verification systems," but 50 subjects—even if perfectly balanced—cannot support generalizable fairness conclusions without statistical rigor.

2. **No cross-dataset comparison to demonstrate the dataset's distinctive value.** The benchmark experiments (Section 4) evaluate face detectors and verification models *only on VIBEFACE*. There is no comparison to any existing dataset (e.g., LFW, MOBIO, SOTERIA). Consequently, the reader cannot determine whether VIBEFACE's eKYC scenarios stress models differently from existing resources, whether its demographic balance changes conclusions drawn from imbalanced datasets, or whether its multi-session protocol reveals new failure modes. The experiments confirm mostly obvious expectations (RetinaFace/MediaPipe outperform MTCNN; ArcFace outperforms MagFace; challenging conditions are harder). A dataset paper's benchmark section should showcase what the dataset uniquely reveals; without cross-dataset comparison, this is not demonstrated.

3. **Flawed verification evaluation protocol.** Verification accuracy (Section 4.2, Table 4) is reported using a single fixed similarity threshold of 0.5 for all models, all scenarios, and all demographic subgroups. This is not standard practice in face verification, where threshold-free metrics (AUC, EER) or at minimum a threshold tuned on a held-out set are used—because model output distributions differ. The anomalously low MagFace scores on off-angle views (0.262–0.308, Table 4) almost certainly reflect a poorly chosen threshold rather than genuine model failure. The paper's discussion of "verification success" is therefore measuring, at least in part, an artifact of the evaluation design. This does not invalidate the dataset but renders the verification benchmark results uninterpretable as evidence of model capability.

### Minor

- **No defined evaluation protocol or data splits.** The paper does not specify train/validation/test splits or a recommended evaluation protocol for future users. For a resource intended as a benchmark, defined splits are important to ensure comparability of future results.

- **First-of-its-kind claim needs sharper demarcation from PAD datasets.** The paper states it is "the first publicly available database to include diverse video-based eKYC verification scenarios" (Section 5). However, several of the scenarios (blinking, head rotation, expression changes) closely resemble challenge-response protocols used in presentation attack detection (PAD) datasets. The paper would benefit from explicitly distinguishing eKYC verification from liveness detection and discussing overlap with PAD resources.

- **Detection benchmark lacks discriminatory power for top models.** RetinaFace and MediaPipe achieve detection rates of 1.000 (or near-1.000) on off-angle and frontal views across all sessions and demographic groups (Table 3). The detection benchmark therefore cannot differentiate between these models or reveal dataset-specific challenges in basic detection.

### Trivial
None.

## Nice-to-Haves

- A cross-session verification analysis that systematically varies the reference session vs. query session would directly support the claim that VIBEFACE enables robustness evaluation across environmental conditions. The dataset is designed for this (five sessions), but the paper only uses Session B as the reference.
- Comparing the same verification models on VIBEFACE and at least one existing dataset (e.g., MOBIO or SOTERIA) under an identical protocol would concretely demonstrate what the eKYC scenarios or demographic balance add.
- Replacing the fixed threshold with AUC or EER would allow the demographic analysis to produce interpretable results.
- Defined evaluation splits should be provided for future users.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Scenarios 17–18 purpose is unclear"** — The paper clearly defines them in Section 3.2 as eKYC verification scenarios (hand covering/touching face) and explains their exclusion from benchmarks in Section 4.1 ("occlusions that significantly reduce facial visibility"). This is not a weakness.
- **"Scenario 11 incomplete coverage should be addressed"** — The paper already acknowledges this limitation in Section 4.1.
- **Table 1 formatting critique** — A formatting nitpick that does not affect scientific content.
- **Claims about speculative PAD/deepfake applications** — The conclusion states these "hold potential," which is a standard forward-looking statement, not a claimed contribution.
- **"Only one reference image" criticism** — Using the frontal flash image as reference is explicitly justified as emulating document-based authentication; this is a reasonable design choice, not a flaw.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Downscope the paper's claims from "benchmark for fairness" to "specialized resource for eKYC protocol design and pilot evaluation" to better match the 50-subject scale.
2. Add at least one cross-dataset comparison experiment to demonstrate what VIBEFACE uniquely reveals.
3. Replace the fixed-threshold verification metric with AUC or EER, and report confidence intervals or bootstrap estimates for demographic subgroup comparisons.
4. Define and publish recommended evaluation splits and a protocol to support reproducible future work.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>