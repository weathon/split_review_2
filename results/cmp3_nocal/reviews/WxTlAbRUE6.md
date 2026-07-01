## Summary

This paper introduces GMD-25, a benchmark for evaluating compositional generalization in machine learning force fields (MLFFs). It consists of four tasks—Length Extrapolation, Functional Group Composition, Functional Group Duplication, and Functional Group Combination—designed to test whether MLFFs can generalize to unseen molecular structures formed from known components. Five models (SchNet, PAINN, DimeNet++, GemNet, EquiFormerV2) are evaluated, and the key finding is that all models fail dramatically on out-of-distribution examples, with errors often orders of magnitude higher than on in-distribution data, and that in-distribution performance does not predict out-of-distribution performance.

## Strengths

1. **Well-motivated gap.** The paper correctly identifies that existing MLFF benchmarks (MD17, MD22, Transition1x, ANI-1) primarily test interpolation to unseen configurations of known molecules, not generalization to genuinely novel molecular structures. This is articulated clearly in Section 1 and Section 2.3.

2. **Principled task design.** The four tasks are adapted from the compositional generalization literature (Hupkes et al., 2020) and map cleanly onto chemical concepts. Task 4 (Functional Group Combination) is particularly crisp: training on symmetrically functionalized molecules and testing on asymmetrically functionalized ones, holding the scaffold constant, isolates whether a model treats functional groups as independent, recombinable features (Section 3.1).

3. **Non-obvious empirical finding.** The result that ID performance does not predict OOD performance—e.g., EquiFormerV2 excels on OOD forces but collapses on OOD energy for Length Extrapolation, while simpler models like SchNet show the opposite pattern (Section 4.3)—is a genuine discovery that justifies the benchmark's existence.

## Weaknesses

### Fatal

None.

### Major

1. **Unexplained models in figure captions.** Figure 2 lists "PBE0" as one of the five compared models, but Section 4.1 (Models) only describes SchNet, PAINN, DimeNet++, GemNet, and EquiFormerV2. PAINN is missing from Figure 2's caption, while PBE0 is absent from Section 4.1. Figure 3 lists "m4s" as a model, also absent from Section 4.1. Neither PBE0 nor m4s is described anywhere in the paper body. The reader cannot determine whether PBE0 is a DFT reference calculation, another MLFF, or something else. For a benchmarking paper whose central activity is model comparison, this is a transparency failure that must be corrected.

2. **No statistical uncertainty.** All results are reported as point estimates. No error bars, confidence intervals, standard deviations, or indications of multiple random seeds appear anywhere. For a paper that makes comparative claims ("EquiFormerV2 consistently exhibits the lowest Forces MAE," "GemNet overall performs best"), the absence of any variance information makes it impossible to assess whether the reported rankings are reliable. Even a small number of repeated runs (3–5 seeds) would substantially strengthen the claims.

### Minor

3. **ID-only hyperparameter tuning.** The paper states that Bayesian hyperparameter optimization was conducted "to ensure that each model achieved its best possible performance on the in-distribution data" (Section 4.2). While this is standard practice for OOD benchmarks, it means architectures that might trade some interpolation accuracy for better extrapolation could be systematically disadvantaged. The paper should acknowledge this as a limitation.

4. **No reference baselines.** The five MLFFs are compared only against each other. Including a simple classical force field (e.g., UFF or GAFF) would help calibrate whether the reported failures indicate limitations specific to neural-network-based approaches or reflect intrinsic difficulty of the tasks at the GFN2-xTB level of theory.

5. **Descriptive analysis without diagnostic depth.** The results section reports which model performed best but does not analyze *why* different architectures show different failure patterns. For example, why does EquiFormerV2 generalize well on forces but not energy for Length Extrapolation? The paper aspires to be a "diagnostic tool" (Section 5) but does not deliver diagnostic analysis of this kind.

6. **Minor inconsistency in method description.** The introduction calls the trajectories "ab initio molecular dynamics (AIMD) trajectories" (Section 1), while Section 3 correctly identifies GFN2-xTB as a "semi-empirical tight-binding approach." Semi-empirical methods are parameterized, not ab initio. This should be corrected for consistency.

### Trivial

None.

## Nice-to-Haves

- **Task calibration.** For Task 2 (Functional Group Composition), a sanity check verifying that the GFN2-xTB reference labels for carboxylic acids are approximately additive combinations of alcohol and aldehyde contributions on the same scaffold would strengthen the task's rationale.
- **Limitations section.** The paper lacks an explicit discussion of limitations (modest dataset size of 118 molecules, reliance on GFN2-xTB-level theory, exclusion of foundation models). Adding one would improve transparency.
- **Diagnostic extensions.** Analyzing error patterns per atom type, per distance range, or per functional group would turn the benchmark into a richer diagnostic tool, which the paper already claims to be.

## Removed Points

These points are flagged to be removed, treat them with caution:

1. **Abstract overstates existing practice.** The critic claimed the abstract's statement that models are "typically trained and tested on the same molecules" overstates the case because MD22 and Transition1x involve different molecules. The word "typically" makes this characterization reasonable, and the Related Work (Section 2.3) provides a nuanced discussion. *Removed: strawman weakness; the paper's claim is qualified with "typically."*

2. **Task 1 augmented variant design conflates two types of generalization.** The critic argued the task design conflates interpolation and extrapolation. The paper's own analysis (Section 4.3, Figure 3 panels a–d) already separates alcohols and carboxylic acids, and the task design is clearly motivated. *Removed: the paper already addresses this in its analysis.*

3. **Request for GFN2-xTB as a reference baseline.** Running GFN2-xTB on the OOD molecules would trivially reproduce the labels (since GFN2-xTB is the label-generation method). This is not a meaningful baseline. *Removed: factually not useful as a baseline against MLFFs.*

4. **Exclusion of foundation models is a significant limitation.** The paper gives a clear, defensible methodological reason for excluding foundation models (to avoid confounding memorization with generalization). *Removed: the choice is justified within the paper's stated scope; criticizing it is scope creep.*

5. **Reproducibility statement.** The critic noted code/dataset are promised "upon acceptance" rather than available at submission. This is standard ICLR policy. *Removed: violates the hard rule about availability concerns.*

6. **PBE0/m4s might be in the appendix.** Even if they are, a figure caption should be interpretable from the main paper without consulting the appendix. The core criticism (missing from Section 4.1) is retained in Major weakness #1. *Removed: already captured in the main weakness.*

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add model descriptions for PBE0 and m4s to Section 4.1, or remove them from figures if they are not part of the controlled comparison.
2. Run at least 3–5 random seeds per model and report mean ± std (or similar) for all results.
3. Add at least one classical force field baseline to calibrate result severity.
4. Add a brief limitations paragraph to the conclusion.
5. Correct the "AIMD" characterization in the introduction to match the "semi-empirical" designation used in Section 3.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>