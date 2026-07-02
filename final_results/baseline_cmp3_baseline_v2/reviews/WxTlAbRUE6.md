## Summary

This paper introduces GMD-25, a benchmark designed to evaluate compositional generalisation in machine learning force fields (MLFFs). It consists of four tasks—length extrapolation, functional group composition, functional group duplication, and functional group combination—each requiring models to generalise to molecular structures that are compositionally novel relative to the training set. The authors evaluate five state-of-the-art models (SchNet, PAINN, DimeNet++, GemNet, EquiFormerV2) and find that all models exhibit significant performance degradation on out-of-distribution examples, often one to two orders of magnitude worse than in-distribution performance.

## Strengths

- **Timely and important problem.** The ability of MLFFs to generalise beyond training molecules is critical for their practical utility in drug discovery and materials science, yet existing benchmarks focus almost exclusively on in-distribution accuracy. GMD-25 directly addresses this gap.
- **Well-designed benchmark tasks.** The four tasks are carefully constructed to isolate distinct aspects of compositional generalisation (length, composition, duplication, combination) and ensure that training data contains all necessary components, making the tasks theoretically feasible.
- **Rigorous empirical evaluation.** A diverse set of representative MLFFs are evaluated under a consistent protocol, including hyperparameter tuning. The results clearly demonstrate that all current models fail to generalise, establishing a strong baseline for future work.
- **Extensibility and reproducibility.** The paper describes a toolkit for generating trajectories and provides data splits and preprocessing scripts (to be released upon acceptance), which will facilitate easy adoption and extension by the community.

## Weaknesses

### Fatal

None.

### Major

- **Hyperparameter optimisation only targets in-distribution performance.** The two-stage tuning strategy optimises hyperparameters for ID test error. Because OOD generalisation may require different inductive biases (e.g., stronger regularisation or different cut-offs), this choice potentially understates the OOD performance that models could achieve if tuned for OOD tasks. While the authors acknowledge this limitation, it weakens the claim that the observed generalisation gaps are intrinsic to the architectures.

### Minor

- **Semi-empirical reference (GFN2-xTB) instead of DFT.** The benchmark labels are computed with a semi-empirical tight-binding method, which is less accurate than the DFT calculations used in most MLFF training. While this is a pragmatic choice for generating trajectories at scale, it introduces a systematic bias: models trained on DFT data in practice may not transfer directly. The paper does not discuss how this choice affects the relevance of the benchmark for the primary intended use case (replacing DFT-based methods).
- **Lack of analysis on why models fail.** The paper documents the generalisation gap extensively but provides no mechanistic analysis (e.g., failure modes per atom type, impact of cutoff radius for larger molecules, sensitivity to network depth). Such analysis would greatly increase the diagnostic value of the benchmark and guide architectural improvements.
- **Exclusion of foundation models.** The paper deliberately omits pre-trained models (e.g., MACE-MP-0) to avoid confounding memorisation with generalisation. While this is a valid design choice, it means the benchmark does not reflect the current state of the art in practice. Including a foundation model as an additional baseline, with a clear discussion of the limitations of interpreting its results, would be informative.

### Trivial

- The caption for Figure 1 contains a duplicated sentence; this appears to be a parser artefact but should be cleaned in the final version.

## Nice-to-Haves

- Provide per-atom force error breakdowns or visualisations of where errors concentrate (e.g., near functional groups vs. the backbone). This could offer clues about the source of the generalisation failure.
- Include a simple linear baseline or a classical force field (e.g., UFF) to calibrate the difficulty of the tasks.
- Add a discussion of the computational cost of generating the benchmark data and training models, to help users decide whether the benchmark is feasible for routine evaluation.

## Novel Insights

Beyond the paper’s own contributions, a noteworthy insight is that the ranking of models by OOD performance differs substantially from their ranking by ID performance across tasks. For example, EquiFormerV2 achieves the best forces MAE on length extrapolation but the worst energy MAE, while simpler models like SchNet sometimes generalise better on energy despite weaker ID accuracy. This suggests that current design priorities (e.g., full equivariance, high-capacity attention) do not automatically yield better compositional generalisation and may even hinder it in some respects.

## Suggestions

- Run an ablation where hyperparameters are tuned on OOD performance (or a combined ID+OOD objective) to separate architectural bias from hyperparameter selection effects.
- Provide a “leaderboard” style summary table that normalises results across tasks (e.g., OOD/OOD error ratio) so readers can quickly compare model strengths.

## Score and Decision

**Score:** 6

**Decision:** Accept

The paper presents a well-executed, timely benchmark that fills an important gap in the MLFF evaluation landscape. The weaknesses are not fatal and can be addressed in future work. The GMD-25 benchmark will likely become a standard tool for assessing generalisation in force field learning.

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>