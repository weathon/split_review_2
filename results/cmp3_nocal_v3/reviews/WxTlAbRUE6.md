Now let me write the final consolidated review.

## Summary

This paper introduces GMD-25, a benchmark for evaluating compositional generalization of machine learning force fields (MLFFs). It comprises four systematic tasks — length extrapolation, functional group composition, functional group duplication, and functional group combination — each designed so that training data contains the necessary atomic/motif-level building blocks for test molecules. The paper evaluates five state-of-the-art MLFF architectures and finds that all models show dramatically worse out-of-distribution performance, often by 1–2 orders of magnitude, with in-distribution accuracy failing to predict OOD accuracy.

## Strengths

1. **Well-motivated gap in existing benchmarks.** (§1, §2.3) Standard MLFF benchmarks (MD17, MD22, Transition1x) train and test on different configurations of the *same* molecules. The paper correctly identifies that this conflates interpolation with genuine transferable learning. This is a genuine blind spot that the paper systematically addresses.

2. **Thoughtful task design.** (§3.1) The four tasks systematically probe different dimensions of compositional generalization — length, composition, duplication, and combination. Each task ensures that the training data contains the atomic/motif-level building blocks needed for the test molecules, making failure informative. The "base vs. augmented" variants for Tasks 1 and 2 are a nice design choice that probes how additional supporting data affects generalization.

3. **Clean experimental setup.** (§4.1–4.2) The two-stage hyperparameter tuning (defaults → Bayesian optimization on ID data) is appropriate. Model selection spans a useful range of architectural families (invariant GNN: SchNet; equivariant GNN with directional features: DimeNet++, GemNet; equivariant GNN with vector features: PAINN; equivariant Transformer: EquiFormerV2). Excluding foundation models is a defensible choice for isolating architectural generalization properties.

4. **Clear and important empirical finding.** (§4.3) The central result — that all evaluated models show dramatically worse OOD performance, often by 1–2 orders of magnitude — is robustly demonstrated across four different tasks and five model families. The observation that ID accuracy does not predict OOD accuracy (e.g., EquiFormerV2 best on forces but worst on energy for Length Extrapolation) is interesting and non-obvious, and has practical implications for model selection.

## Weaknesses

### Fatal
None.

### Major

1. **No uncertainty quantification across runs.** (§4.3, Figures 2–4) Every result in the paper is reported as a single-point estimate with no error bars, no standard deviations, and no mention of how many random seeds or training runs were used. For a benchmark paper making comparative claims ("EquiFormerV2 performed the best on Length Extrapolation in terms of forces MAE"; "GemNet overall performed best in the OOD region for Functional Group Composition and Functional Group Duplication" — see §5), this is a significant omission. With as few as 5 training trajectories (Length Extrapolation base), different initializations could yield materially different rankings. The main qualitative finding (all models generalize poorly) would likely survive added noise, but the comparative rankings of models cannot be evaluated without knowing whether observed differences exceed run-to-run variance. A benchmark should establish reproducible rankings, not single-point estimates. The paper could be substantially strengthened by running each model-task combination with 3–5 random seeds and reporting means with standard deviations.

### Minor

2. **Tension between "physical principles" framing and semi-empirical reference labels.** (Abstract, §1, §3, §5) The paper repeatedly frames GMD-25 as testing whether models "capture the underlying physical principles" (Abstract) or "learn the underlying physical principles" (§1). The ground-truth labels are computed with GFN2-xTB, a semi-empirical tight-binding method that the paper itself describes as a balance between "computational efficiency and accuracy" (§3). GFN2-xTB is a useful approximation but has known systematic errors. The paper does not discuss whether GFN2-xTB's own accuracy degrades for OOD molecules (longer alkanes, novel functional group combinations), which would mean the benchmark's labels might not faithfully represent the physical quantities the paper claims to be testing. This does not invalidate the benchmark — it remains useful as a test of generalization *within the GFN2-xTB label space* — but the framing modestly overreaches. The paper should either validate a subset with higher-fidelity reference calculations or explicitly reposition the benchmark as testing generalization within a given computational level of theory.

3. **Limited analysis of observed architectural differences.** (§4.3, §5) The paper reports interesting and varied patterns across models (e.g., EquiFormerV2's decoupled energy/force errors, SchNet and DimeNet++ having stable energy but weak forces for Length Extrapolation, GemNet doing best on Functional Group Duplication). However, the paper notes these patterns descriptively without attempting to analyze *why* certain architectures exhibit certain generalization behaviors. The conclusion ( §5) states "the benchmark serves as a valuable diagnostic tool for identifying architectural biases" but provides no analysis of which architectural features (equivariance, attention, directional messages, etc.) correlate with which generalization patterns. This is a missed opportunity to move from reporting failure to providing insight.

### Trivial
None.

## Nice-to-Haves

- **Analyze the energy/force error decoupling for EquiFormerV2.** The finding that EquiFormerV2 has the best Forces MAE but the worst Energy MAE in Length Extrapolation OOD (§4.3) is intriguing and likely diagnostically meaningful. A brief analysis (e.g., checking whether the error is a constant energy shift or scales with system size) would directly serve the paper's stated diagnostic aim with minimal additional work.

- **Add classical force-field baselines.** Classical FFs (UFF, GAFF) are not MLFFs and fall outside the paper's stated scope, but they could provide a useful lower bound on OOD error and a sanity check on whether the generalization gap is a property of learned potentials or of the task/label space itself.

- **Report training and inference times.** A benchmark paper would benefit from reporting computational cost for each model, as this affects practical adoption.

## Removed Points

- **"PBE0" and "m4s" appearing in figure captions but not model list.** These are OCR/parser artifacts from figure extraction. The paper's model list (§4.1) clearly and consistently names SchNet, PAINN, DimeNet++, GemNet, and EquiFormerV2. Not a paper error.

- **Missing classical force-field baselines as a weakness.** The paper scopes itself to evaluating MLFFs (§4.1). Classical FFs are a different methodological family and demanding them goes beyond the paper's stated scope. This is a nice-to-have, not a weakness.

- **Data/code availability concern.** The paper states the data and framework "will be made open-source upon paper acceptance." This is a standard constraint of the review format.

- **Formatting, typos, or presentation nitpicks.** All such issues are parser artifacts, not author errors.

- **Criticism about missing appendix content.** The appendix is stripped by the parser; it exists in the original submission.

## Novel Insights

The input review's central insight — that the paper overreaches with its "physical principles" framing given the semi-empirical reference level — is a valid point but is itself somewhat overextended as a criticism (the paper does acknowledge the method is semi-empirical). A more novel observation is the decoupling of the two core weaknesses: the paper's *comparative* model rankings (which need error bars) are a separate issue from its *qualitative* finding (all models fail OOD, which is robust even without error bars). The harsh review conflates these two into a single "no uncertainty" criticism, but they have different severity. The qualitative finding is the paper's primary contribution and is not threatened by the lack of error bars; the comparative ranking claims are secondary and would need multiple runs to be reliable.

## Suggestions

1. Add 3–5 random seeds per model-task combination and report means with standard deviations. This is the single most impactful improvement — it would immediately establish which comparative claims are reliable.
2. Either validate a subset of OOD molecules with higher-fidelity reference calculations (e.g., DFT with a range-separated hybrid functional) or explicitly reframe the benchmark as testing generalization within the GFN2-xTB label space.
3. Add a brief analysis section discussing which architectural features appear to correlate with which generalization patterns, even if only at the level of informed speculation.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>