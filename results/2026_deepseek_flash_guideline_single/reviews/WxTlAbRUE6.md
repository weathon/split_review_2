Now I have sufficient calibration data. Let me write the final review.

**Calibration anchors:**

| Paper | Avg Score | Decision | Comparison to GMD-25 |
|---|---|---|---|
| EGraFFBench (NvJxTjTQtq) | 6.00 | Reject | Most comparable — MLFF benchmark with broader evaluation but implementation issues. GMD-25 has more principled task design but less comprehensive metrics. |
| Understanding & Mitigating DS for MLFFs (Xk9Q0CrJQc) | 6.25 | Reject | MLFF OOD analysis + proposed methods; rejected despite avg >6 due to modest gains. |
| ECD (SBCMNc3Mq3) | 6.50 | Accept | Benchmark accepted due to massive dataset (140K structures) and practical utility. GMD-25's dataset is smaller (118 molecules). |
| AU-GOOD (qFZnAC4GHR) | 6.67 | Accept | Framework + metric + statistical testing; accepted for comprehensive methodology. |
| GDL-DS (LixGd92Wri) | 5.67 | Reject | Broad distribution-shift benchmark, rejected for shallow coverage. |
| MatText (ihwRfc4RNw) | 4.00 | Reject | Materials benchmark rejected for thin empirical contributions. |

**Round 1 bracket:** The paper sits between 4.50 and 6.50 — above MatText and GDL-DS in task-design quality, but below ECD and AU-GOOD in evaluation rigor and comprehensiveness. Most comparable to EGraFFBench (6.00, rejected) but with less comprehensive evaluation.

**Final score:** 5.5. The principled task design and striking finding (all models fail compositionally) are real contributions, but the lack of uncertainty quantification for comparative claims and the undiscussed limitations of GFN2-xTB as reference method prevent it from reaching the acceptance bar at ICLR.

---

## Summary

This paper introduces GMD-25, a benchmark for evaluating compositional generalisation in Machine Learning Force Fields (MLFFs). It consists of four controlled tasks (Length Extrapolation, Functional Group Composition, Functional Group Duplication, Functional Group Combination) that isolate distinct forms of compositional generalization. The dataset comprises 118 molecules and ~297k labelled geometries using GFN2-xTB as the reference method. The authors evaluate five popular MLFF architectures (SchNet, PAINN, DimeNet++, GemNet, EquiFormerV2) and find that all models fail to generalize compositionally, with OOD errors often orders of magnitude higher than ID errors.

## Strengths

- **The gap is genuine and important.** The paper correctly identifies that standard MLFF benchmarks (MD17, WS22, Transition1x, MD22) test in-distribution accuracy on held-out snapshots, not generalization to new molecules. The central question — whether current MLFFs learn physical principles or simply interpolate training labels — is timely and well-motivated (Section 1, lines 13–15).

- **Task design is principled and systematic.** The four tasks carefully isolate distinct forms of compositional generalization (Section 3.1, lines 60–82). The "controlled component coverage" design (training includes all primitive components needed for generalization, e.g., all carbon chain lengths in the augmented variant, all individual functional groups in Tasks 2–4) is more informative than simply making a larger dataset and hoping for distribution shift.

- **The finding that ID performance does not predict OOD performance is practically important.** The paper documents cases where models that excel on one metric in-distribution fail on that same metric out-of-distribution, and vice versa (e.g., EquiFormerV2 excels at OOD forces but fails at OOD energy; DimeNet++ has strong ID forces but poor OOD generalization). These observations are genuinely informative for practitioners choosing architectures (Section 4.3, lines 134–160).

## Weaknesses

### Major

- **No uncertainty quantification across training runs.** All results are reported as single MAE values with no error bars, standard deviations, or confidence intervals. The paper does not state how many random seeds or independent training runs were performed, nor does it mention any form of statistical significance testing. Since the paper draws conclusions about which architectures generalize better (e.g., "GemNet overall performs best in the OOD region for Functional Group Composition and Functional Group Duplication," lines 140, 156, 160; "EquiFormerV2 performed the best on Length Extrapolation in terms of forces MAE," line 166), the absence of any reliability measure weakens every comparative claim. MLFF training is known to be sensitive to initialization and hyperparameters; without repetition, the reported rankings could reflect noise. For a benchmark paper whose purpose is to establish reliable empirical findings, this is a significant omission.

### Minor

- **The GFN2-xTB reference method is acknowledged but its limitations for the benchmark's central claim are not discussed.** The paper uses GFN2-xTB (semi-empirical tight-binding) rather than DFT (Section 3, line 56). The paper's core framing (abstract, lines 8–9; Section 1, lines 13–15) is about whether models "learn the underlying physical principles" — but if the reference labels themselves come from an approximate method whose accuracy may degrade on OOD molecules, a model's poor OOD performance could partly reflect reference label noise rather than a pure generalization failure. The paper never discusses whether GFN2-xTB's accuracy is uniform across the test molecules (e.g., does it extrapolate to longer alkane chains or novel functional group combinations as reliably as DFT would?). A simple validation experiment comparing GFN2-xTB against DFT for a subset of representative OOD molecules would substantially strengthen the claims. This does not invalidate the benchmark but is a limitation that should be explicitly acknowledged and ideally addressed.

- **No aggregate results table in the main text.** The paper describes results qualitatively and via figures (Section 4.3, lines 132–161) but does not provide a single table in the main body with numerical MAE values for all model–task combinations. For a benchmark paper intended as a reference for the community, a summary table showing ID vs. OOD MAE for each model × task would substantially improve usability and allow readers to quickly compare results without parsing figure captions.

### Trivial

- **The "augmented variant" naming in Length Extrapolation conflates two different capabilities.** The augmented variant tests compositional interpolation (recombining seen lengths with seen functional groups in new pairings), which is qualitatively different from the base variant's test of extrapolation to unseen lengths (lines 62–64). Both are called "Length Extrapolation," which could confuse readers interpreting why some models succeed on one variant but not the other. Consider renaming or clearly differentiating.

- **Minor overstatement in the introduction.** The paper states "the benchmark's ab initio molecular dynamics (AIMD) trajectories were generated" (line 26), but GFN2-xTB is semi-empirical tight-binding, not ab initio in the DFT sense. This is a minor imprecision.

## Nice-to-Haves

- A small-scale validation experiment comparing GFN2-xTB against a DFT reference for representative OOD molecules (e.g., C13 alkane, a carboxylic acid in the composition task) would substantially strengthen the claim that poor OOD performance reflects model generalization failure rather than reference label noise.
- An analysis of failure modes — do the errors follow systematic patterns (e.g., consistent overestimation of energy for longer chains) or are they chaotic? This would deepen the benchmark's value as a diagnostic tool.
- The paper excludes foundation models (MACE-MP-0, ORB) by design to avoid conflating memorization and generalization (line 104). This is defensible but limits practical relevance; a brief acknowledgment of this limitation would help practitioners.
- The paper could acknowledge that the small training set size (e.g., ~10k training geometries for Length Extrapolation base) means that some generalization failures could be due to insufficient data rather than architectural limitations.

## Removed Points

- **Figure/model inconsistency (PBE0, m4s).** The harsh critic noted that Figure 2's caption (line 120) lists "PBE0" and Figure 3's caption (line 144) lists "m4s", neither matching the five models listed in Section 4.1 (SchNet, PAINN, DimeNet++, GemNet, EquiFormerV2). These strings appear in OCR-extracted text from embedded figure images — almost certainly parser artifacts (e.g., PAINN misread as PBE0, and m4s as garbled text). The paper's narrative text (lines 104, 134–136) consistently and correctly refers to all five models by their proper names. Per guideline: parser-originated garbled text is not an author error. Removed.

- **Conditional release ("upon acceptance") concern.** The critic flagged that the toolkit "will be made available upon acceptance" (line 116). Per guidelines: "REMOVE any criticism that questions the existence, release status, or availability of any model, tool, benchmark, dataset, or reference cited in the paper." Removed.

- **All other formatting, typo, grammar, and reproducibility nitpicks.** Pure parser artifacts or field-standard practices. Removed.

## Novel Insights

None beyond the paper's own contributions. The reviews did not surface a perspective on the paper that its authors had not already articulated.

## Suggestions

1. **Add uncertainty quantification.** Report results from at least 3–5 independent training runs per model per task with error bars. This is the single highest-leverage improvement and would transform the paper's comparative claims from suggestive to reliable.

2. **Include an aggregate results table** in the main paper showing numerical ID vs. OOD MAE for all model–task combinations. This is standard for benchmark papers and would greatly improve usability.

3. **Validate GFN2-xTB against DFT** for a small representative subset of OOD molecules, and explicitly discuss the limitations of the reference method in the paper.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>