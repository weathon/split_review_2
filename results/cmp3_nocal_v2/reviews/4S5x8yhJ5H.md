## Summary

VIBEFACE is a facial biometric dataset comprising 2,250 still images and 1,550 short videos from 50 subjects, designed to support face verification in eKYC-style scenarios. The dataset is notable for its deliberate demographic balancing (50:50 gender split, ~25% per racial group across four categories, ISO 19795-compliant age stratification), ethical sourcing with GDPR/AI Act compliance, and multi-session capture varying lighting, device, and occlusion conditions. Benchmark evaluations of face detection (MTCNN, RetinaFace, MediaPipe) and face verification (ArcFace, MagFace) are provided as demonstration tasks.

## Strengths

- **Ethical and legal compliance throughout.** The paper documents GDPR compliance, AI Act alignment, informed consent, anonymization via randomized identifiers, and the right to withdraw (Section 3.4). This stands in stark contrast to predecessors (VGGFace2, MS-Celeb-1M, MegaFace) that were withdrawn due to consent violations, making this a genuine and significant contribution.
- **Deliberate demographic balance at the design stage.** The 50:50 gender split and approximately uniform distribution across four racial groups (~24–26% each) surpass what comparable datasets offer — Table 1 shows no prior dataset ticks all of gender balance, race balance, and age balance. The ISO 19795-compliant age stratification also improves over SOTERIA's underrepresentation of older adults.
- **Multi-session, multi-condition capture design.** The five sessions varying lighting conditions (artificial, flash, natural, weak natural) and including a dedicated glasses-occlusion session (Section 3.3, Table 2) capture real-world nuisance factors. Using three consumer-grade phones (Xiaomi, iPhone, Samsung) with random device assignment per session adds useful cross-device variability.
- **Novelty of eKYC-style video scenarios.** While individual actions (blinking, head rotation, expression changes) appear in other PAD datasets, their combination in a single, ethically-sourced, publicly-accessible dataset with balanced demographic metadata and per-subject attributes is not available elsewhere. Scenarios 17–18 (partial occlusions, face touching) are practically useful for liveness and PAD research.

## Weaknesses

### Fatal
None.

### Major

1. **50 subjects is too few for the demographic fairness analysis the paper presents.** The dataset contains 50 subjects total, with racial subgroups of 12–13 people and age-gender cells as small as 6–8 (e.g., females 51–70: 6 subjects; see Figure 1). Throughout Section 4, the paper makes claims such as "minimal variation in detection rates across gender and age groups" (line 299–300) and describes performance differences across racial categories. With 12–13 subjects per racial group, these claims have no statistical basis. The paper reports **no confidence intervals, error bars, or significance tests** — not once (confirmed by grep). Observed differences — e.g., MTCNN scoring 0.812 for African subjects vs. 0.984 for East Asian on frontal views, a 17-percentage-point gap (Table 3) — could be driven by the specific 12–13 individuals in each group rather than reflecting systematic bias. Proper demographic bias studies in face recognition typically require hundreds of subjects per group. The paper also does not acknowledge this limitation. The dataset can document performance disparities across *subjects and conditions* but cannot support the general claims about demographic bias that the paper's framing invokes.

2. **Verification evaluation uses a single arbitrary threshold.** A fixed similarity threshold of 0.5 is used throughout (line 340) with no justification of how this value was chosen. Verification accuracy as a percentage of frames exceeding this threshold conflates model discrimination with threshold calibration. Standard biometric evaluation practice is to report ROC curves with FMR/FNMR tradeoffs, or metrics such as TAR@FAR=0.001 or EER. Without these, the numbers in Table 4 are uninformative for comparison with any existing benchmark. For example, ArcFace's 50.9% on OAV in Session A could mean the model is barely above chance at that threshold, or it could mean a different threshold would yield very different results — the reader cannot tell.

3. **No cross-dataset comparison to demonstrate the dataset's claimed value.** For a dataset paper, the most critical experiment is showing what new insights this dataset enables that existing datasets do not. The paper runs two models on its own data and reports numbers. There is no experiment comparing, for example, (i) whether demographic disparities observed on VIBEFACE differ from those on MOBIO or SOTERIA, (ii) whether eKYC scenarios reveal failure modes that standard photo-based benchmarks miss, or (iii) whether models trained on web-scraped data generalize differently to VIBEFACE's controlled-acquisition data. Without such comparisons, the paper has not demonstrated that the dataset provides value beyond being another reasonably diverse face collection.

### Minor

1. **Face detection benchmark is saturated.** RetinaFace achieves 100% or near-100% on virtually every setting (Table 3). MediaPipe is similarly at ceiling. This makes the detection benchmark uninformative — it simply confirms that modern detectors handle these conditions easily, which was predictable from prior work.

2. **"eKYC" framing is imprecise.** The paper repeatedly describes the dataset as capturing "eKYC procedures" (line 66) and "authentic eKYC-style facial videos" (line 24). The actual video scenarios (Section 3.2, scenarios 12–18) are standard liveness-detection actions: head rotation, blinking, expression changes, mouth opening, face touching. Real eKYC workflows also involve document verification (scanning an ID) and document-to-selfie matching, which the dataset does not include. A more precise framing — e.g., "liveness-detection sequences used in eKYC" — would better reflect the dataset's scope.

3. **Hardest detection cases were excluded.** Scenarios 17–18 (partial occlusions, face touching) were excluded from the detection benchmark "because they involve occlusions that significantly reduce facial visibility" (line 288). But occluded faces are precisely where detection performance matters most in real eKYC deployments. Excluding them avoids the hardest test cases and weakens the benchmark.

4. **PAD and deepfake-detection claims are speculative.** The conclusion states the dataset is "well-suited for advancing research in presentation attack detection (PAD)" and "detecting injection attacks involving deepfakes" (line 374), but all samples are bona fide — no attack presentations or deepfakes are included. This forward-looking statement should be tempered or removed.

### Trivial

1. **No standardized evaluation protocol.** The paper does not define train/test splits, cross-validation scheme, or recommended evaluation metrics. This makes it difficult for the community to adopt a common protocol, reducing comparability of future results using the dataset.

## Nice-to-Haves

- Conduct a cross-dataset comparison experiment showing what VIBEFACE uniquely reveals (e.g., compare demographic disparity magnitudes on VIBEFACE vs. MOBIO/SOTERIA, or compare whether eKYC-style videos expose failure modes that static images miss).
- Provide a specific recommended evaluation protocol with defined splits to enable reproducible benchmarking.

## Removed Points

- **Missing related work (RFW, BUPT-BalancedFace, LFW, IJB-C, FairFace):** Removed per guidelines — the reviewer cannot verify that the paper's related-work coverage is incomplete without external sources.
- **Reproducibility/access concerns about controlled-access license:** Removed. Controlled access with a signed agreement is standard practice for biometric datasets containing identifiable data; the paper provides a temporary review link. The more substantive reproducibility concern (no standardized protocol) is retained in Trivial.
- **"No discussion of dataset size limitations":** Merged into Major Weakness #1 rather than listed separately, since it is integral to that criticism.
- **"Table 1 comparison is incomplete":** Removed per guidelines — the reviewer cannot verify the completeness of a comparison table without external sources.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Reframe the paper's contribution more precisely: a controlled, ethically-sourced dataset for evaluating verification models under eKYC-style liveness-detection scenarios with balanced demographic metadata, rather than a resource for general demographic bias analysis.
- Replace the threshold-based verification metric with proper biometric evaluation (FMR/FNMR, ROC curves, or TAR at standardized FAR values).
- Acknowledge the 50-subject limitation candidly and temper demographic claims accordingly.
- Include scenarios 17–18 in the detection evaluation, or explain more compellingly why they were excluded.
- Add a standardized evaluation protocol (train/test splits, suggested metrics) to enable reproducible benchmarking.

## Score and Decision

**MY FINAL SCORE: <score>4</score>**
**MY FINAL DECISION: <decision>Reject</decision>**