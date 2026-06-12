## Summary

The paper introduces GMD-25, a benchmark for evaluating compositional generalization of machine learning force fields (MLFFs). It comprises four controlled tasks—length extrapolation, functional group composition, functional group duplication, and functional group combination—designed to test whether models learn underlying physical principles rather than interpolating training labels. Evaluating five state-of-the-art models (SchNet, PAINN, DimeNet++, GemNet, EquiFormerV2), the authors find that all models show severe performance degradation on out-of-distribution molecules, with errors often one to two orders of magnitude higher than on in-distribution examples, highlighting a critical gap in current MLFF evaluation and design.

## Strengths

- **Timely and important problem**: The paper addresses a central limitation of MLFFs—their ability to generalize to unseen molecular structures—which is crucial for practical applications in drug discovery and materials science. This gap is well-motivated and often overlooked in standard benchmarks.
- **Systematic and well-designed benchmark**: The four tasks are carefully constructed to probe distinct aspects of compositional generalization (length extrapolation, systematicity via composition/duplication/combination), with training sets that cover all needed sub-components. The tasks are clearly explained with molecular diagrams and practical relevance.
- **Comprehensive empirical evaluation**: A diverse set of models spanning invariant GNNs, equivariant GNNs, and equivariant transformers are evaluated under a consistent protocol with hyperparameter optimization. The results consistently demonstrate failure across all tasks, with clear visualizations and quantitative evidence.
- **Novel and actionable insights**: The paper shows that model ranking on in-distribution accuracy does not predict out-of-distribution performance (e.g., EquiFormerV2 excels on forces but fails on energy OOD), and that no single architecture dominates all generalization tasks. This suggests that current physically-informed designs are insufficient.

## Weaknesses

### Fatal
None.

### Major
- **Single quantum chemistry method**: The benchmark relies exclusively on GFN2-xTB semi-empirical labels. While internally consistent, the generalizability of the findings to higher-level methods (e.g., DFT, coupled cluster) is not addressed. The community may question whether the observed generalization failures are artifacts of the label fidelity. A small-scale validation using a more accurate method would substantially strengthen the claims.
- **Lack of analysis on why models fail**: The paper documents failure but provides limited insight into the root causes (e.g., role of cutoff radius, message-passing depth, equivariance constraints, or training distribution coverage). Without such analysis, the benchmark remains a diagnostic tool rather than a guide for improvement.

### Minor
- **Hyperparameter tuning scope**: Bayesian optimization is mentioned but the search space, budget, and selected hyperparameters are not discussed in the main text. The degree to which tuning could mitigate OOD errors is unclear, especially since some models may need task-specific adaptation.
- **Missing baseline comparisons**: No simple baselines (e.g., kernel methods, linear models on hand-crafted features, or models with explicit physical priors like cutoff-based group contributions) are included to contextualize the MLFF failures. The results would be more impactful with a lower- or upper-bound reference.

### Trivial
- **Figure 3 caption**: One model is labeled "m4s" which is not defined in the caption or text, likely an artifact from the automatic parsing but momentarily confusing.

## Nice-to-Haves

- Provide a small-scale replication of one task (e.g., length extrapolation) using DFT-level labels to verify that the generalisation gap is not an artifact of the semi-empirical method.
- Include an ablation study varying the number of training snapshots or molecular diversity to understand sensitivity to dataset size.
- Release a leaderboard or baseline results with simple non-learned potentials (e.g., classical force fields) to calibrate the difficulty of each task.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that the failure mode is pervasive across architectures and tasks, yet the relative ranking of models is task-dependent and inconsistent with in-distribution performance. This suggests that current MLFFs do not learn a physically consistent representation: they may capture local equivariant interactions but fail to compose them in novel contexts. The magnitude of the generalisation gap (orders of magnitude) underscores that interpolation-based evaluation, common in the field, is highly misleading.

## Suggestions

- Extend the benchmark to include a small set of validation calculations with a higher-accuracy method (e.g., ωB97X-D3/def2-TZVP) for a subset of molecules to check label sensitivity.
- Provide a more interpretable analysis per task, such as per-atom error maps, correlation plots, or the effect of increasing model capacity on OOD error.
- Consider adding tasks that require extrapolation to out-of-distribution conformations (e.g., non-equilibrium geometries) to further probe physical understanding.

## Score and Decision

**Score**: 8  
**Decision**: Accept  

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>