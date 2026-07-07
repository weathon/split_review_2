Now I have all the information I need. Here is my final consolidated review.

## Summary

This paper introduces GMD-25, a benchmark designed to evaluate whether Machine Learning Force Fields (MLFFs) can compositionally generalise to molecules unseen during training. The benchmark comprises four tasks (Length Extrapolation, Functional Group Composition, Functional Group Duplication, and Functional Group Combination), each isolating a different facet of compositional generalisation. Results across five models (SchNet, PAINN, DimeNet++, GemNet, EquiFormerV2) show consistent and often dramatic OOD performance degradation, with errors one to two orders of magnitude above ID errors, and importantly, the best ID-performing model is not the best OOD performer — a finding with practical implications for model selection.

## Strengths

- **The four-task benchmark design is thoughtful and systematically probes distinct facets of compositional generalisation.** Length extrapolation, functional group composition, duplication, and recombination each isolate a different combinatorial challenge (Section 3.1). The augmented variants for Tasks 1 and 2 provide controlled analysis of what training signal helps. This task structure is the paper's primary intellectual contribution. [weight: +3.67]

- **The finding that best ID performance does not predict best OOD performance is non-trivial and practically important.** For instance, EquiFormerV2 leads on forces MAE in Length Extrapolation but collapses on energy MAE, while SchNet and DimeNet++ show the opposite pattern (Section 4.3, Figure 2). This suggests leaderboard rankings on standard benchmarks may systematically misguide architecture selection for deployment. [weight: +3.02]

- **The paper provides a useful toolkit for generating the benchmark data** (using RDKit, FlashMD, and GFN2-xTB), making the benchmark extensible. The total dataset of 118 molecules and 296,534 labelled geometries (Section 3.2) is a substantial resource for the community. [weight: +4.09]

- **The benchmark intentionally excludes foundation models** (Section 4.1), which is the right methodological choice for a controlled diagnostic. Including pretrained models would conflate memorisation from large-scale pretraining with in-architecture generalisation capacity. [weight: +2.35]

## Weaknesses

### Fatal
None.

### Major

- **No variance reporting across runs.** The paper does not report performance over multiple random seeds, confidence intervals, or any measure of run-to-run variability. For a benchmark study whose central claim involves ranking models ("GemNet overall performed best in the OOD region for Functional Group Composition and Functional Group Duplication," Section 5), this is a significant gap. Training sets are small (e.g., 5 molecules × ~2000 snapshots for Task 1 base), making single-run evaluations potentially dominated by initialisation luck or optimisation trajectory quirks. The qualitative model rankings carry no indication of whether gaps between models are reliable. [weight: -2.91]

- **The tasks may not cleanly isolate compositional generalisation from data sparsity effects.** The paper frames poor OOD performance as a failure of compositional generalisation, but training sets are very small (e.g., ~10,000 snapshots for Task 1 base; monocarboxylic acids C5–C10 for Task 3). While ID test performance (unseen snapshots of training molecules) is reported, this does not fully resolve the concern: a model can overfit to 2000 snapshots of a molecule while still doing reasonably well on unseen snapshots of that same molecule's conformational space. The paper provides no analysis (e.g., training on progressively more ID data) to separate "the model cannot compositionally generalise" from "the model did not have enough data to learn a good representation." This underdetermines the central interpretation. [weight: -3.21]

### Minor

- **Figure caption/model inconsistencies.** The alt-text for Figure 2 lists "PBE0" as one of five compared models, but PBE0 is a DFT functional, not an MLFF, and Section 4.1 lists only SchNet, PAINN, DimeNet++, GemNet, and EquiFormerV2 — with no mention of PBE0 (and PAINN omitted from the alt-text). The alt-text for Figure 3 similarly lists "m4s" as a model, which is not mentioned in Section 4.1. While these may be labeling artifacts in the image-description text, they are confusing and erode confidence in the paper's attention to detail. [weight: -1.11]

- **The "compositional" framing of Task 2 (Functional Group Composition) is chemically loose.** The paper states a carboxylic acid can be seen as a composition of an alcohol and an aldehyde (Section 3.1), but these groups are bonded to the same carbon in a specific arrangement with distinct inductive and resonance effects. The paper partially acknowledges this ("we do not expect the model to learn the chemical reaction pathway"), but the framing as compositional generalisation in a linguistically- or algorithmically-principled sense is overstated. [weight: -1.82]

- **No synthesis of model-level architectural insights from the results.** The conclusion lists which model performed best on which task (Section 5) but does not connect these observations to specific inductive biases (e.g., do higher-body-order message-passing models generalise better? do invariant vs. equivariant models trade off differently on energy vs. forces?). Section 2.2 mentions algorithmic alignment (Xu et al., 2020) but this is never revisited in the results analysis. [weight: -2.26]

### Trivial
None.

## Nice-to-Haves

- Report results over 3–5 random seeds with error bars/confidence intervals in all figures. This is essential infrastructure for a benchmark paper.
- Add a data-ablation study on Task 1 (or Task 3) training models on progressively more ID data (1×, 2×, 4× the original training set) to help separate compositional generalisation failure from data-sparsity effects. The paper already has the data; this requires computational investment.
- Include one or two simple non-neural baselines (e.g., a classical force field like UFF or GAFF) to establish a floor for what compositional generalisation looks like without learned representations.
- Correct the Figure 2 and Figure 3 caption/model inconsistencies regarding "PBE0" and "m4s".
- Add verbose breakdowns for Tasks 3 and 4 by chain length, as was done for Task 1, to reveal whether the generalisation gap is uniform or concentrated in certain molecule sizes.

## Removed Points

These points were flagged by reviewers but are removed from the main review with justification:

- *"Missing models (MACE, NequIP)"*: Removed. The paper justifies its model selection (5 models covering distinct architectural families) and explains why foundation models are excluded (Section 4.1). MACE is cited in related work but omitting it as an evaluated baseline is a scope choice, not a weakness.
- *"Augmented variant tests interpolation, not extrapolation"*: Removed. The paper itself calls the augmented variant "easier" (Section 3.1, Task 1) and the main text correctly describes the task. The label "Length Extrapolation" for the overall task remains appropriate for the base variant.
- *"Abstract overstates that models are trained/tested on same molecules"*: Removed. The paper's related work (Section 2.3) acknowledges broader-coverage benchmarks like Transition1x and MD22, and the claim that models are "typically trained and tested on the same molecules" is a reasonable characterisation of standard practice.
- *"Algorithmic alignment mentioned but not revisited"*: Removed. This is a nice-to-have extension rather than a genuine weakness; the paper is a benchmark, not an architectural analysis.
- *"Missing dataset size table / computational budget / convergence criteria"*: Removed. The appendix is stripped by the parser; these details may exist there.
- *"The problem is well-motivated"* strength: Removed as generic.

## Novel Insights

None beyond the paper's own contributions. The reviews surface standard concerns about benchmarking rigor (variance reporting, confound controls) but do not reveal new scientific insights about the paper's subject matter.

## Suggestions

1. Add multi-seed evaluation with error bars to all quantitative comparisons. This is the single most impactful improvement for the paper's credibility as a benchmark.
2. Conduct a data-ablation study on at least one task (preferably Task 1 or Task 3) where training data is progressively scaled (1×, 2×, 4×, 8×) to test whether OOD gaps persist with more data — this would directly address the data-sparsity confound.
3. Correct the caption/model inconsistencies in Figures 2 and 3 regarding "PBE0" (which is not one of the evaluated models) and "m4s" (which is not defined in Section 4.1).
4. Add a brief synthesis in Section 5 connecting observed model rankings to specific architectural design choices (equivariance, body order of message passing, use of dihedral angles) to turn observations into actionable guidance.
5. Consider including a classical force field baseline to contextualise the difficulty of the tasks.

## Score and Decision
**Score**: 6.0  
**Decision**: Borderline Accept

**Calibration context**: The most directly comparable anchor is **EGraFFBench** (avg 6.00), an MLFF benchmarking paper evaluating 6 equivariant models on OOD tasks. EGraFFBench received more severe weighted weaknesses than this paper (net weighted item sum -3.51 vs. +1.82 for GMD-25), particularly around unreliable experimental results due to implementation errors. **Understanding and Mitigating Distribution Shifts for MLFFs** (avg 6.25) had weaknesses about modest performance gains (-7.06) and practical utility (-8.30) — both more serious than any weakness here. **AU-GOOD** (avg 6.67) had severe novelty concerns (-9.31). The Round 1 bracket placed this paper in the 5.5–7.5 band, and comparison of weighted item profiles against the closest anchors (shared heavy-positive items: thorough benchmark design, useful community resource; shared heavy-negative items: missing error bars, interpretational confounds) narrows the final score to 6.0. This paper's benchmark design is a genuine contribution, but the absence of variance reporting and unresolved data-sparsity confound prevent a higher score.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>