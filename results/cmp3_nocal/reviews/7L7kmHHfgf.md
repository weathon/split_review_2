Now I have all the information I need. Let me produce the final consolidated review.

## Summary

This paper proposes PIRN, a prototype-based intra-modal reconstruction framework with cross-modal normality communication for few-shot multimodal anomaly detection (MAD). It introduces three components: Balanced Prototype Assignment (BPA) using optimal transport to prevent codebook collapse, Adaptive Prototype Refinement (APR) to expand prototype coverage at inference, and Multimodal Normality Communication (MNC) for cross-modal knowledge transfer. Experiments on MVTec-3D-AD, Eyecandies, and Real-IAD demonstrate strong results with substantially lower computational cost than comparable methods.

## Strengths

1. **Clear motivation grounded in specific failure modes of existing methods.** The introduction (Section 1) correctly identifies why cross-modal alignment methods (CFM, LSFA) overfit narrow correspondences and memory-bank methods (M3DM, SG-DM) misclassify unseen normal variations in few-shot settings. This directly motivates the three design choices.

2. **Each component addresses a precisely stated gap.** BPA targets codebook collapse via balanced optimal transport (§3.2), APR bridges the train-test distribution gap via gated prototype updates (§3.3), and MNC enables cross-modal collaboration that existing prototype-based AD methods lack (§3.4). The motivation-to-method mapping is explicit for all three.

3. **Consistent empirical margins over the baselines reported in Table 1.** On MVTec-3D-AD, PIRN improves AUROC_I over the strongest baseline in Table 1 by +3.9 (5-shot), +3.7 (10-shot), and +2.4 (50-shot). On Eyecandies, improvements are +3.6, +4.0, and +2.2 respectively. These gains are meaningful in the anomaly detection context.

4. **Genuinely impressive computational efficiency.** Table 4 shows PIRN requires 103.36G FLOPs versus FIND's 728.46G (85% fewer) and 17.49ms latency versus FIND's 76.09ms (4.35× faster), while achieving comparable accuracy (0.922 vs. 0.921 AUROC_I). This is a practically relevant result.

5. **Diagnostic analysis that validates design decisions.** The t-SNE visualization (Fig. 1 right) demonstrates BPA produces more uniform prototype distributions than softmax assignment. The feature displacement analysis (Fig. 4) provides interpretable evidence that the information bottleneck induces larger displacements for anomalous tokens than normal ones. Ablations on prototype count K and decoder depth L (Tables 5-6) show the expected performance peaks and degradation patterns.

## Weaknesses

### Fatal

None.

### Major

1. **FIND, the closest accuracy competitor, is excluded from the main accuracy comparison (Table 1).** Table 4 reports FIND (Li et al., 2025) achieves 0.921 AUROC_I on the 10-shot MVTec-3D-AD setting — essentially tied with PIRN's 0.922. Yet FIND does not appear in the main results Table 1. The paper's abstract claims "consistently achieves superior performance compared to existing baselines," and the "Main Results" paragraph (p. 7) highlights gains of +3.7–4.0 points over the *strongest baseline* — but this framing depends on having excluded the closest competitor from that table. A reader of Table 1 would assume PIRN's accuracy lead over existing methods is large; the efficiency table tells a different story where accuracy is essentially matched. This is selective reporting. The paper's contribution is better described as *comparable accuracy with dramatically better efficiency*, which is still a solid contribution but should be framed as such.

2. **No variance or statistical significance is reported for any few-shot experiment.** Few-shot results depend heavily on which specific training samples are selected. The paper reports no standard deviations, confidence intervals, number of random seeds, or even how the few-shot samples were selected (random seed, fixed split, etc.). With margins of +2–4 AUROC points and known few-shot variance in anomaly detection reaching 2–5 points depending on sample selection, the reader cannot assess whether the reported improvements are statistically reliable. This is especially concerning for the 5-shot setting where sample variance is highest.

3. **APR's claimed protection against anomalous contamination during inference is asserted but not validated.** Section 3.3 argues that anomalous patches are "assigned more diffusely across prototypes" with "low affinity to any single prototype," thereby contributing weakly to prototype updates. This reasoning is not empirically tested. No experiment: (a) measures how prototype vectors change when the test sample contains varying proportions of anomalous area; (b) verifies that anomalous patches are indeed assigned with low affinity across prototypes in practice; or (c) tests a counterfactual where APR is disabled at inference on samples with known anomalies. Since APR operates at test time on unlabeled samples, undetected contamination of the prototype codebook could silently degrade detection — and the paper provides no diagnostics for this failure mode.

### Minor

1. **The baseline configuration in Table 2 is underspecified.** The paper states the first row "excludes all proposed modules" but does not describe what architecture this baseline *is* — a standard ViT decoder with MSE loss? A vanilla autoencoder? Without specifying the baseline architecture, the incremental gains from each component are partially uninterpretable.

2. **No discussion of limitations or failure cases.** The conclusion (Section 5) does not discuss any limitations. A method that adapts prototypes at test time on potentially anomalous samples (APR), uses a fixed prototype budget (K=10), and relies on a frozen DINOv2 encoder inevitably has failure modes that the paper would be strengthened by acknowledging.

3. **Real-IAD D3 results are honestly reported but merit more careful contextualization.** PIRN achieves second-best AUROC_J (0.873) behind D³M (0.890), though it achieves the best localization (AUROC_P = 0.961). The paper uses "D^3M" and "D3M" interchangeably, which should be normalized.

### Trivial

- The column header "BFA" in Table 2 should read "BPA" to match the method name used everywhere else in the paper.

## Nice-to-Haves

- Include FIND in the main accuracy comparison (Table 1) and discuss the accuracy-efficiency trade-off candidly.
- Report variance over 3–5 random few-shot splits with error bars.
- Add a simple diagnostic for APR: e.g., measure prototype vector drift (ℓ₂ norm change) when APR processes normal vs. anomalous test samples.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *Criticism that the Fig. 1 caption claim ("superior anomaly detection accuracy using less than 1% of the training data") is stated without specifying dataset or metric.* The actual caption reads "Comparison with state-of-the-art methods on the Eyecandies dataset (AUROC7 metric)." The specification IS present. **[Factually incorrect — removed.]**

- *Criticism about garbled checkmark formatting and confusing row semantics in Table 2.* The checkmark rendering is a parser artifact; the original table formatting is not recoverable from the parsed text. **[Parser artifact — removed.]**

- *Criticism about inconsistent spellings of "MVTec-3D-AD."* This is a minor formatting inconsistency with no bearing on the technical content. **[Formatting nitpick — removed.]**

## Novel Insights

The harsh review surfaces one genuinely novel insight beyond the paper's own contributions: the paper implicitly treats APR as a "safe" test-time adaptation mechanism, but the theoretical justification for why anomalous patches receive diffuse OT weights relies on the balanced transport constraints. This connection — between optimal transport's marginal constraints and anomaly robustness — is interesting but is argued rather than tested. A controlled experiment manipulating the proportion of anomalous patches in a test sample while measuring prototype drift would either validate or refute this design assumption, and would be a valuable addition to the MAD literature regardless of outcome.

## Suggestions

1. **Add FIND to Table 1 and reframe the accuracy claim.** The paper's contribution genuinely includes a massive efficiency advantage over FIND; reframing from "superior accuracy" to "comparable accuracy with dramatically better efficiency" would make the paper both more honest and more impactful.

2. **Report variance over at least 3-5 random few-shot splits.** This is the single highest-leverage change for the paper's evidential quality. Even reporting the range or interquartile range would help readers calibrate the significance of the reported margins.

3. **Add a diagnostic experiment for APR's protection mechanism.** A simple plot of prototype ℓ₂ drift on normal vs. anomalous test samples (with varying anomaly sizes) would directly validate the paper's central claim about APR's robustness. This could even replace one of the existing ablations.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>