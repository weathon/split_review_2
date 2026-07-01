## Summary

This paper introduces GMD-25, a benchmark for evaluating compositional generalization in Machine Learning Force Fields (MLFFs). The benchmark comprises four tasks (length extrapolation, functional group composition, functional group duplication, and functional group combination), each with controlled train/test splits designed to test whether models learn transferable physical representations rather than interpolating training labels. Five MLFF architectures are evaluated, and the central finding is that all models fail dramatically on out-of-distribution examples, with errors often orders of magnitude higher than in-distribution errors.

## Strengths

- **The benchmark fills a genuine gap.** Existing MLFF benchmarks (MD17, MD22, WS22, Transition1x) focus on equilibrium dynamics or broad chemical coverage without systematically isolating compositional generalization via controlled compositional splits. The four tasks probe distinct generalization mechanisms, and the base/augmented variants provide graded difficulty.

- **The core empirical finding is informative.** Across all four tasks and all five models, OOD errors are one to two orders of magnitude higher than ID errors. The observation that ID performance does not correlate with OOD performance (e.g., EquiFormerV2 achieves excellent force predictions but poor energy predictions on OOD data) is a practically important signal for practitioners.

- **The benchmark design is thoughtful.** By ensuring that all atomic environments, functional groups, and chain lengths in the test molecules are composed of components seen during training, the benchmark genuinely tests compositional generalization rather than raw memorization or distribution shift of atom types.

## Weaknesses

### Fatal
None.

### Major

- **Model inconsistency between text and figures (verified).** Section 4.1 lists five models: SchNet, PAINN, DimeNet++, GemNet, EquiFormerV2. However, the Figure 2 caption includes "PBE0" (a DFT functional not mentioned in the model description section) and omits PAINN. The Figure 3 caption includes "m4s," which is never defined anywhere in the paper, and lists six models. Figure 4 is consistent with the text. These discrepancies mean the reader cannot determine which models were actually evaluated on which tasks, undermining confidence in the presented results. This is the most significant weakness and must be resolved before the paper can be relied upon.

### Minor

- **No statistical uncertainty reported (verified).** All results are reported as single values with no error bars, standard deviations, or mention of random seeds. Given the modest dataset size (~2000 snapshots per molecule), run-to-run variance could be non-negligible. The claims about which model "performs best" on a given task cannot be assessed for statistical significance.

- **MACE is not evaluated.** The paper cites MACE (Batatia et al., 2022) in the related work as a prominent equivariant architecture but excludes it from evaluation. The stated rationale—excluding "foundation models (Batatia et al., 2023)"—applies to the MACE foundation model, not to the base MACE architecture. MACE's many-body message passing represents a distinct architectural family from the pairwise message passing of the evaluated models, so this is a gap in coverage.

- **No numerical results table.** All results are conveyed through figures with log-scale axes. Including a table of numerical values would substantially increase the benchmark's utility as a reference for the community.

- **Hyperparameter tuning on ID data only (verified, Section 4.2).** Hyperparameters were optimized for ID performance. This choice could systematically disadvantage models on OOD tasks, since the hyperparameters that minimize ID error may not be those that enable generalization. This limitation is not discussed.

### Trivial
- Minor naming inconsistency: the same model is referred to as "EquiFormerv2" (intro), "EquiFormerV2" (Section 4.1), and "EquiFormV2" (Figure 3–4 captions).

## Nice-to-Haves
- Adding an analysis of how errors scale with chain length or which functional groups are disproportionately difficult would deepen the diagnostic value.
- Adding error-component analysis (e.g., force magnitude vs. direction) beyond aggregate MAE.

## Removed Points

The following points from the input review were removed per filtering rules:

1. **"Dataset release conditioned on acceptance"** — Removed per hard rule: criticisms about release status of cited datasets/tools are not permitted. Conditional release upon acceptance is standard practice.

2. **"Link to algorithmic alignment papers is slightly stretched"** — Removed: subjective framing opinion, not a substantive weakness. The paper makes a reasonable connection.

3. **"Does not address whether GMD-25 offers different insights than DrugOOD/BOOM"** — Removed: scope creep. The paper situates itself relative to these benchmarks; cross-comparison analysis is not required.

4. **"The augmented variant is not obviously compositional"** — Removed: the paper already explains this (line 64: "the model is tested on combinations of lengths and functional groups that it has not seen before"). The explanation is reasonable.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Resolve the model inconsistency as the top priority.** Either ensure all figure captions match the model list in Section 4.1, or if PBE0 and m4s are distinct evaluation conditions (e.g., DFT reference, additional method), define them explicitly and justify their inclusion.

2. **Report statistical uncertainty.** Include means and standard deviations across multiple random seeds (at least 3) for all main results, and add error bars to figures.

3. **Add a numerical results table** (at minimum in the appendix) with exact MAE values for all model-task combinations.

4. **Either add MACE to the evaluation or explicitly justify its omission** as a deliberate scope decision distinct from the foundation-model exclusion.

5. **Acknowledge the ID-only hyperparameter tuning as a limitation** and discuss potential sensitivity of OOD findings to this choice.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>