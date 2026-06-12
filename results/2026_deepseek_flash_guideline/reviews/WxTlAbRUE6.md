## Summary

GMD-25 is a benchmark for evaluating compositional generalization in machine learning force fields (MLFFs). It comprises four tasks (Length Extrapolation, Functional Group Composition, Functional Group Duplication, Functional Group Combination) that separate training and test molecules while ensuring generalization should be feasible for models that learn physical principles. The paper evaluates five popular MLFFs (SchNet, PAINN, DimeNet++, GemNet, EquiFormerV2) and finds that all models show OOD errors one to two orders of magnitude higher than ID errors, with the best ID models often not being the best OOD models.

## Strengths

- **First systematic benchmark targeting compositional generalization in MLFFs.** The four tasks isolate specific generalization failures (length extrapolation, functional group composition, duplication, and asymmetric combination) that prior benchmarks such as MD17, WS22, and Transition1x cannot detect because they train and test on the same molecules (Section 2.3, last paragraph). The training molecules are explicitly chosen so that generalization should be feasible if the model learns underlying physical principles (Section 1, paragraph 1).

- **Base/augmented task variants provide a diagnostic for failure modes.** Tasks 1 and 2 each include a base and an augmented variant (Section 3.1). The augmented variants supply additional training data that should theoretically help (e.g., showing all chain lengths but not the test-set length–group combinations), yet models still show substantial generalization gaps. This design distinguishes whether failures stem from missing component knowledge vs. inability to recombine components.

- **Diverse architectural evaluation reveals divergent ID/OOD rankings.** Five models spanning invariant GNNs (SchNet), equivariant MPNNs (PAINN), geometric-feature models (DimeNet++, GemNet), and transformers (EquiFormerV2) are evaluated (Section 4.1). The benchmark reveals that "the models that perform best on ID examples are not always the models that generalise best to OOD examples" (Section 1, paragraph 2). For instance, EquiFormerV2 has the best forces MAE on Length Extrapolation but fails on energy MAE in the OOD region, while SchNet and DimeNet++ show the opposite pattern (Section 4.3, paragraph 1). This demonstrates the benchmark's diagnostic utility beyond standard ID-only evaluation.

## Weaknesses

### Fatal

None.

### Major

- **Figure captions inconsistent with the model description.** The text (Sections 1 and 4.1) consistently lists five models: SchNet, PAINN, DimeNet++, GemNet, EquiFormerV2. However, Figure 2's caption lists "PBE0" (a DFT functional — never mentioned as an evaluated model) instead of PAINN, and attributes results to "PBE0" throughout the caption text. Figure 3's caption lists "m4s" (never mentioned or defined anywhere in the paper) alongside six models instead of five. Figure 4's caption correctly lists the five models from Section 4.1. A reader cannot determine from the captions alone whether "PBE0" in Figure 2 is a labeling error that should be PAINN, or whether PBE0 was actually evaluated (contradicting the text). The same ambiguity applies to "m4s" in Figure 3. Because the figures are the primary evidence for the paper's central claim, this inconsistency undermines trust in the results as presented. The authors must clarify whether these are parsing artifacts or actual figure content errors.

- **No statistical analysis reported for any experimental result.** All results are single point estimates (one MAE per model per task) with no mention of multiple random seeds, standard deviations, or confidence intervals. The paper makes comparative claims — "GemNet overall performed best" on Task 3, "EquiFormerV2 performed the best on Length Extrapolation in terms of forces MAE" (Sections 4.3 and 5) — but the reader cannot assess whether these differences are reliable or within the noise of training. For a benchmark paper whose value depends on establishing reliable baselines, this is a significant omission.

### Minor

- **No baseline to calibrate OOD error severity.** The paper reports MAE values without reference points (e.g., a mean predictor or linear regression on atomic descriptors). This makes it hard to interpret whether OOD errors are close to random guessing or reflect meaningful (if degraded) learning.

- **Potential confound in hyperparameter tuning.** Hyperparameters were optimized for ID performance (Section 4.2), then models were tested OOD. Models that overfit more aggressively to achieve better ID performance after tuning may generalize worse, creating a confound. The paper does not discuss this or analyze whether ID-optimal hyperparameters are systematically harmful for OOD performance.

- **Task 2 (Functional Group Composition) framing as "compositional" is imprecise.** Carboxylic acid (-COOH) is described as a composition of alcohol (-OH) and aldehyde (C=O), but these are directly bonded to the same carbon, creating a resonance-stabilized structure whose electronic properties are not additive. The paper acknowledges this partially ("we do not expect the model to learn the chemical reaction pathway"), but the base variant remains the most prominently discussed and the "compositional" framing overstates what the task can diagnose.

- **"Complex carbonyls" and "complex alcohols" in Task 2 are not defined.** The paper adds these to the training set (Section 3.1, Task 2 description) without specifying which molecules they refer to, which matters for reproducibility.

- **GFN2-xTB limitations not discussed.** Using a semi-empirical tight-binding method as ground truth introduces an upper bound on label fidelity that should be acknowledged.

- **Inference cost not reported.** Parameters, FLOPs, or wall time would help the community interpret accuracy-efficiency trade-offs across architectures.

### Trivial

- Training trajectory counts are not fully consistent across tasks — Task 1 specifies "one trajectory per molecule," while other tasks state "each trajectory contains around 2000 snapshots" without consistently stating trajectories per molecule.

## Nice-to-Haves

- Run all experiments with at least 5 random seeds and report mean ± std — this single change would transform the paper's evidential standing.
- Add a simple sanity-check baseline (e.g., predicting mean training energy/force) to calibrate how much of the OOD degradation reflects genuine difficulty.
- Discuss whether hyperparameters that maximize ID performance are systematically harmful for OOD.
- Rename or clarify the "extrapolation" framing for the augmented variant of Task 1, which is partially an interpolation task for alcohols.

## Removed Points

- **Benchmark not available at submission time**: Removed per hard rules — criticisms questioning release status/availability of cited entities are not appropriate for evaluation.
- **Formatting/typo concerns**: Not included as these are likely PDF parser artifacts, not author errors.
- **Comments about "missing appendix" or "missing proofs"**: Removed per hard rules — these sections exist in the original submission but are stripped by the parser.
- **Generic strength about "addressing an important problem"**: Removed as it is not specific to the paper's content.

## Novel Insights

The most striking pattern across the inputs is the gap between the paper's conceptually strong task design and its thin evidential support. The four tasks are genuinely novel as an MLFF benchmark, and the base/augmented variant design is clever — it allows distinguishing missing-component-knowledge failures from recombination failures. However, the paper stops at demonstrating that "models fail" without providing the methodological rigor (error bars, baselines, confound analysis) that would make the diagnosis actionable. The figure caption inconsistency further undermines confidence. This is not a paper whose core idea is wrong; it is a paper whose execution needs to match the ambition of its design.

## Suggestions

1. **Clarify the figure caption inconsistency.** Confirm whether Figures 2 and 3 actually display PAINN (not PBE0) and whether Figure 3 includes only the five models from Section 4.1 (not "m4s"). If the captions are PDF extraction artifacts, state this explicitly in the rebuttal and correct them in a revision.

2. **Add multiple random seeds (at least 5) and report mean ± std for all experimental results.** This is the single most impactful improvement and is expected for a benchmark paper.

3. **Add a simple baseline** (e.g., predicting the mean training energy/force) to calibrate how challenging the OOD tasks truly are.

4. **Discuss the hyperparameter confound**: analyze whether the ID-optimal hyperparameters differ systematically from OOD-optimal ones.

5. **Define "complex carbonyls" and "complex alcohols"** or remove the vague terminology and specify exact molecules.

6. **Consider a softened framing for Task 2** that acknowledges the resonance structure of carboxylic acids rather than claiming strict compositionality.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>