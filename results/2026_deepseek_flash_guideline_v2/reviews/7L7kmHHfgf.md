Now I have all the information I need. Let me construct the final review.

## Summary

PIRN proposes a prototype-based intra-modal reconstruction framework for few-shot multimodal anomaly detection, combining three components: Balanced Prototype Assignment (BPA) via optimal transport to prevent codebook collapse, Adaptive Prototype Refinement (APR) for test-time prototype expansion, and Multimodal Normality Communication (MNC) for cross-modal knowledge exchange. The method achieves consistent improvements over baselines on MVTec-3D-AD, Eyecandies, and Real-IAD while using substantially fewer FLOPs than comparable approaches.

## Strengths

1. **Consistent few-shot gains across multiple benchmarks and shot settings.** Table 1 shows PIRN outperforms the strongest baseline (INP-Former) on MVTec-3D-AD by +3.9, +3.7, and +2.4 AUROC_I in 5-shot, 10-shot, and 50-shot settings respectively, and on Eyecandies by +3.6, +4.0, and +2.2. The pattern holds across both datasets and all three few-shot regimes, not a single lucky configuration.

2. **Order-of-magnitude efficiency improvement at comparable accuracy.** Table 4 reports PIRN achieves the best AUROC_I (0.922) with 103.36G FLOPs and 17.49ms latency, compared to FIND (0.921, 728.46G, 76.09ms) — an 85% reduction in FLOPs and 4.35× lower latency. This is a practically important result that few-shot MAD methods typically do not report.

3. **Component ablation quantifies each module's contribution.** The text describes that removing BPA drops AUROC_I from 0.922 to 0.828 (−9.4%), removing APR drops to 0.883 (−3.9%), and removing MNC drops to 0.916 (−0.6%). Each of the three mechanisms provides a measurable benefit.

4. **Stronger localization on Real-IAD D3 despite using fewer modalities.** Table 8 shows PIRN achieves AUROC_P of 0.961, outperforming D³M (0.922) which uses a tri-modal representation (RGB+Pseudo-3D+3D) compared to PIRN's two modalities (RGB+surface normals). This demonstrates that the cross-modal communication design extracts more discriminative signal per modality.

## Weaknesses

### Fatal
None.

### Major

1. **No variance estimates for the central few-shot results.** Table 1 reports only point estimates for all few-shot settings (5-shot, 10-shot, 50-shot) with no standard deviations, confidence intervals, or information about the number of random seeds or split instantiations. With only 5 or 10 training samples per class, different draws from the normal pool can produce meaningfully different models. The paper's own ablation (Table 6) shows AUROC_I can swing from 0.924 to 0.869 (a 5.5-point gap) just by changing decoder depth — larger than many claimed improvements over baselines. Without repeated trials, the reader cannot assess whether the reported gains are robust or within the experimental noise floor. This does **not** invalidate the approach — the trends are consistent across settings — but it weakens the evidential strength of the paper's central claim.

2. **APR's core inference assumption is insufficiently validated.** APR relies on the premise that anomalous patches will be "assigned more diffusely across prototypes (i.e., with low affinity to any single prototype)" under balanced OT, thereby contributing weakly to each prototype's context vector. This depends on assumptions about anomaly distinctiveness, coverage, and the OT balanced constraint. The paper provides displacement analysis (Fig. 4) for two categories as indirect evidence, but does not directly validate that anomalous patches consistently receive low/diffuse OT weights in APR's context computation. The mechanism could fail for large-surface anomalies or defects resembling normal patterns in one modality, and this is not analyzed.

### Minor

3. **Missing experimental details.** (a) The paper does not specify how few-shot samples are selected (random draw? fixed splits from prior work? shared across methods?). (b) The GPU used for latency measurements in Table 4 is not reported, making the timing comparison less reproducible. (c) The PRO curve integration range for AUPRO is not specified, which hinders cross-paper comparison.

4. **FIND is excluded from the main few-shot comparison (Table 1).** FIND (Li et al., 2025) is cited as a recent SOTA in the efficiency comparison (Table 4) but does not appear alongside M3DM, CFM, etc. in the primary few-shot accuracy table. Including it would give a more complete accuracy-versus-efficiency picture.

5. **The equal-mass constraint in BPA (§3.2, Eq. 1) is a strong prior.** It forces each prototype to receive exactly N/K mass from the patches. If some prototypes correspond to rarer normal patterns, this constraint could force unnatural assignments. The paper does not discuss or ablate softer marginal constraints.

### Trivial

6. Table 2 column header reads "BFA" instead of "BPA" (likely a parser artifact; should be cleaned up).

## Nice-to-Haves

- A direct validation of APR's OT weight distribution for anomalous vs. normal patches across multiple categories, ideally including a failure case analysis (e.g., large-surface anomalies).
- An ablation of the equal-mass constraint in BPA vs. a softer regularization.
- Analysis of whether the sigmoid-based purification in MNC (`z_n · σ(z_n^{bpa})`) ever suppresses useful normal information when the BPA reconstruction is poor.

## Removed Points

These points were raised by reviewers but are removed per the filtering rules:

1. **Table 2 is "uninterpretable" / all checkmarks identical** — REMOVED as a PDF parsing artifact. The text explicitly describes the ablation logic, and the garbled checkmark patterns are a rendering issue, not an author error. The numerical values in the table are consistent with the text's description.

2. **Criticism about INP-Former adaptation fairness** — REMOVED as speculative. The paper describes a specific adaptation procedure (two-stream, same backbone, element-wise fusion) and follows the same post-processing. Doubting its fairness without evidence is not a verified weakness.

3. **Criticism about missing related work nuance with INP-Former** — REMOVED because the paper adequately positions itself relative to prior work.

4. **Criticism about the BPA→APR ordering being "computationally redundant"** — REMOVED. The two OT computations serve different purposes (APR computes context vectors for refinement; BPA computes assignments for reconstruction). The paper does not claim computational optimality, and this is a design choice.

5. **Claim that "+3.7 AUROC_I at 10-shot on MVTec-3D-AD" cannot be distinguished from noise** — WEAKENED from "invalidates claims" to Major weakness #1. The consistency across 6 few-shot settings (2 datasets × 3 shot levels) makes it unlikely these are all noise, but variance estimates are still needed.

6. **Strength about Figure 1 t-SNE visualization** — REMOVED as a qualitative auxiliary visualization rather than a quantitative strength.

7. **"BPA typo in the method name"** — REMOVED as a trivial parser artifact.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add variance estimates.** Run each few-shot setting with 3-5 random draws/splits and report mean ± std. This single change would substantially strengthen the paper's evidential quality.

2. **Validate APR's assumption directly.** Measure OT weight distributions for anomalous vs. normal patches in APR's context computation across multiple categories and anomaly types.

3. **Include FIND in the main few-shot comparison** (Table 1) to provide a complete accuracy picture alongside the efficiency comparison.

4. **Report GPU hardware, few-shot split construction method, and AUPRO integration range** in the experimental setup.

5. **Discuss the equal-mass constraint** in BPA and consider an ablation comparing it to a softer marginal constraint.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>