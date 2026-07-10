Now I have all the information I need. Let me produce the final consolidated review.

## Summary

VIBEFACE is a dataset paper presenting a new facial biometric dataset with 2,250 still images and 1,550 videos from 50 subjects, designed for eKYC (electronic Know Your Client) scenarios. Its stated contributions are: (1) demographic balance across gender, race, and age; (2) eKYC-inspired action sequences (head rotation, blinking, expression changes, etc.); (3) ethical/legal compliance (GDPR, informed consent, controlled access). The paper includes benchmark experiments on face detection and verification to demonstrate the dataset's utility.

## Strengths

- **Explicit demographic balance is genuinely better than most prior datasets.** VIBEFACE achieves a 50:50 gender split, roughly 25% per ethnic group across four categories (African, Caucasian, East Asian, South Asian), and three age bands (18–30, 31–50, 51–70). As Table 1 shows, no existing comparable dataset ticks all of DD, GB, RB, and AB simultaneously. This is a meaningful improvement for fairness research that was prioritized from the design stage.

- **Ethical and legal compliance is handled seriously and thoroughly.** Data was collected with informed consent, GDPR compliance, controlled-access licensing, anonymization, and the right to withdraw (Section 3.4). This stands in contrast to Internet-scraped face datasets (MS-Celeb-1M, VGGFace2, MegaFace) that have been withdrawn.

- **The eKYC-style verification scenarios (12–18) are novel in their combination.** While individual actions (blinking, head turning) exist in other datasets, the specific set of seven verification actions mimicking eKYC workflows — circular head rotation, tilting, blinking, expression change, mouth opening, partial face occlusion, face touching — is not present together in any single public dataset surveyed (Table 1).

## Weaknesses

### Fatal
None.

### Major

- **The benchmark experiments are too thin to convincingly demonstrate the dataset's value.** The face verification experiment (Section 4.2) uses only two models (ArcFace, MagFace), a single fixed threshold of 0.5 on raw similarity scores with no calibration analysis, and a single reference image. Standard evaluation metrics for face verification — FAR, FRR, EER, ROC curves, or accuracy at a FMR-based threshold — are absent. Reporting the percentage of frames above an arbitrary threshold does not constitute a protocol that allows other researchers to produce comparable numbers. The face detection experiment (Section 4.1) mainly confirms that RetinaFace and MediaPipe achieve near-perfect detection while MTCNN degrades slightly — adding little beyond what is already known. The experiments do not use the dataset to test a hypothesis or reveal a phenomenon that could not be studied with existing datasets, which undermines the paper's thesis that VIBEFACE is a unique resource.

- **No standardized evaluation protocol is defined.** A dataset intended as a "benchmark" (abstract) should define fixed train/validation/test splits and a clear evaluation protocol supporting comparison across future work. The paper describes which data was used for its own experiments but does not codify this into a standard protocol that others must follow. Without this, different papers may use different splits, different reference images, or different frame sampling rates, making results incomparable.

- **The controlled studio environment conflicts with the claimed eKYC realism.** Section 3 states data was collected "in a controlled studio environment... continuously supervised by trained operators." Yet the paper itself acknowledges (Section 1) that "eKYC sessions often involve users recording short videos under unconstrained conditions — at home, in variable lighting." The videos simulate eKYC *actions* under controlled conditions, not eKYC *conditions* (unconstrained environments, unsupervised capture, device heterogeneity in the wild). The paper does not meaningfully acknowledge this gap, and the mismatch between the "eKYC workflow" framing and the controlled collection environment weakens the claimed niche.

### Minor

- **With only 50 subjects, the dataset's framing as a "benchmark" is overstated.** The dataset is roughly the size of OULU-NPU (55) and smaller than MOBIO (150), WMCA (72), and SOTERIA (70). The paper reports raw percentages in Tables 3 and 4 with no confidence intervals, no statistical significance tests, and no measure of variance. Claims such as "female participants consistently achieved slightly higher verification rates than males" (Section 4.2) could easily be driven by 2–3 subjects given N=50. The dataset may still be useful as a supplementary evaluation set, but the "benchmark" framing is not supported by the numbers.

- **No analysis of device-specific effects is provided** despite data being collected with three phone models (Xiaomi Redmi Note 13, Apple iPhone 13, Samsung Galaxy A35 5G). Results are not broken down by device, missing an opportunity to characterize cross-device variability.

### Trivial
None.

## Nice-to-Haves

- Frame-level annotations (e.g., which frames have eyes closed for blinking detection) would increase the dataset's utility for liveness detection research.
- Inter-subject embedding similarity analysis would provide useful dataset characterization.
- ROC curves and threshold-independent metrics would strengthen the verification analysis.
- A cross-device breakdown of results would help characterize device-specific effects.
- The paper could acknowledge the studio-environment limitation more explicitly and clarify what aspects of eKYC realism it captures vs. what it does not.

## Removed Points

- "Empty cells in Table 1 could suggest a dataset lacks a feature": REMOVED — formatting/style nitpick, not a substantive weakness.
- "Results table is over-engineered": REMOVED — subjective presentation preference.
- "No frame-level annotations for liveness": MOVED to Nice-to-Haves — not part of the paper's stated scope.
- "No inter-subject embedding similarity analysis": MOVED to Nice-to-Haves — useful characterization but not a core flaw.
- "Paper provides no evidence for PAD/deepfake claims": REMOVED — the paper explicitly says these are "beyond the scope of the experiments presented here" (Section 5), so this is not a claimed contribution.
- "Reference image from Session B is an odd choice": REMOVED — the paper justifies this as "emulating a typical document-based authentication setup" (Section 4.2), which is reasonable.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the paper's stated strengths (demographic balance, ethical sourcing, novel eKYC action scenarios) and surface well-understood limitations of small-scale dataset evaluations, but do not offer unexpected analytical perspectives that the paper itself does not contain.

## Suggestions

1. Define a fixed, replicable evaluation protocol with exact subject splits, frame sampling rates, and standard metrics (FAR, FRR, ROC-AUC, EER with threshold selection at a fixed FMR).
2. Design an experiment that uses the dataset to test a non-obvious claim — e.g., evaluate a verification model trained on a large public dataset on both VIBEFACE and an existing dataset (SOTERIA or MOBIO) to show that the eKYC scenarios in VIBEFACE produce different failure patterns.
3. Either collect more subjects (ideally 150+) to support the "benchmark" framing, or reframe the contribution as a demographically balanced, ethically collected supplementary evaluation set and lower the "benchmark" language.
4. Acknowledge the studio-environment limitation explicitly in the introduction and discuss which aspects of eKYC realism the dataset captures and which it does not.

## Score and Decision

The paper has genuine strengths in demographic balance, ethical sourcing, and the novelty of its eKYC-inspired action scenarios. However, the experiments are far too thin to demonstrate the dataset's value as a benchmark, no standardized evaluation protocol is defined, and there is a mismatch between the "eKYC realism" framing and the controlled studio collection. The core dataset has merit, but the paper as presented does not provide sufficient evidence to support its claims. The most decisive weaknesses — the thin experiments and missing protocol — would require substantial additional work to address.

**Score: 4** (borderline reject)

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>