## Summary

This paper introduces GMD-25, a benchmark designed to evaluate compositional generalisation in Machine Learning Force Fields (MLFFs). The benchmark consists of four tasks—Length Extrapolation, Functional Group Composition, Functional Group Duplication, and Functional Group Combination—that test whether models can generalise to out-of-distribution molecules by learning underlying physical principles rather than interpolating training data. The authors evaluate several state-of-the-art MLFFs (SchNet, PAINN, DimeNet++, GemNet, EquiFormerV2) and find that all models exhibit substantial performance degradation on OOD examples, with errors often one to two orders of magnitude higher than on in-distribution examples.

## Strengths

- **Well-motivated and important research question**: The paper addresses a critical gap in MLFF evaluation—whether models learn physical principles or simply interpolate training data. This question has direct implications for the practical utility of MLFFs in molecular discovery, where generalisation to novel molecules is essential.

- **Carefully designed benchmark tasks**: The four tasks systematically probe different aspects of compositional generalisation (length extrapolation, systematicity, repetition, recombination) with clear rationales for why each task tests meaningful physical understanding. The augmented variants provide controlled comparisons to isolate the difficulty of each generalisation challenge.

- **Comprehensive evaluation of diverse architectures**: The paper evaluates five models spanning invariant GNNs (SchNet), equivariant message passing (PAINN), geometric feature-based models (DimeNet++, GemNet), and transformer-based approaches (EquiFormerV2), providing broad coverage of current architectural families.

- **Clear and informative visualisation of results**: Figures 2-4 effectively communicate the generalisation gap across tasks and models, with logarithmic scales appropriately used to show the magnitude of performance degradation.

## Weaknesses

### Major

- **Limited analysis of why models fail**: The paper documents that models fail to generalise but provides minimal analysis of *why*. For instance, does the failure stem from architectural limitations (e.g., insufficient receptive field for longer chains), training dynamics (e.g., overfitting to training distribution), or fundamental representational issues? Without such analysis, the benchmark serves primarily as a diagnostic rather than a guide for improvement.

- **No evaluation of foundation models or pre-training approaches**: The authors explicitly exclude foundation models (e.g., MACE-MP-0) from evaluation, arguing they make it "harder to untangle memorisation and generalisation effects." However, these models represent the current state of the art in practical MLFF applications, and understanding their generalisation behaviour is directly relevant to the paper's stated goal of encouraging "development of models with better generalisability."

- **Single reference method for ground truth labels**: All trajectories use GFN2-xTB semi-empirical tight-binding calculations. While the authors note this method's "balance between computational efficiency and accuracy," the benchmark's conclusions about generalisation may not transfer to higher-fidelity methods like DFT. The paper would benefit from at least a small-scale validation study comparing GFN2-xTB with DFT-level calculations for a subset of molecules.

- **Insufficient detail on hyperparameter optimisation**: The paper mentions Bayesian hyperparameter optimisation but does not report the search space, number of trials, or whether the same hyperparameters were used across all tasks. This makes it difficult to assess whether the reported performance differences reflect genuine architectural advantages or simply different degrees of hyperparameter tuning.

### Minor

- **The "augmented" variant of Length Extrapolation is not clearly motivated**: The paper states this variant "might be expected to be easier" but does not explain why this particular training set design (discontinuous chain lengths with different functional groups) was chosen over other possible augmented designs.

- **No statistical significance or confidence intervals reported**: The results are presented as point estimates without error bars or measures of variability across different random seeds or training runs. Given the small size of some test sets, this limits confidence in the relative ranking of models.

- **Limited discussion of practical implications**: While the paper convincingly demonstrates that models fail to generalise, it does not discuss what level of OOD error would be acceptable for practical applications, or whether the observed errors would render the models unusable for specific downstream tasks.

### Trivial

- The paper uses "EquiFormerV2" and "EquiFormV2" inconsistently in figure captions.

## Nice-to-Haves

- An ablation study isolating the effect of different architectural components (e.g., equivariance, attention, message-passing depth) on generalisation performance would significantly strengthen the paper's contribution.
- Including a simple baseline (e.g., linear regression on hand-crafted features) would help contextualise the difficulty of the tasks.
- Analysis of whether OOD errors correlate with specific molecular properties (e.g., chain length, functional group size) could provide actionable insights for model development.

## Novel Insights

None beyond the paper's own contributions. The finding that MLFFs fail to generalise compositionally is important but not surprising given the broader literature on neural network generalisation. The paper's main contribution is the systematic benchmark rather than novel insights about why or how to fix the problem.

## Suggestions

- Add an analysis section investigating potential causes of generalisation failure, such as examining attention patterns, receptive field limitations, or the relationship between training data coverage and OOD error.
- Include at least one foundation model (e.g., MACE-MP-0) in the evaluation, with appropriate caveats about interpreting results, to provide a practical baseline for the community.
- Report results with confidence intervals or standard deviations across multiple random seeds to increase statistical reliability.
- Provide the hyperparameter search space and number of trials in the appendix to allow reproducibility of the tuning process.

## Score and Decision

The paper addresses an important and timely problem with a well-designed benchmark. The tasks are thoughtfully constructed, the evaluation is comprehensive across architectural families, and the results clearly demonstrate a significant generalisation gap. However, the paper's impact is limited by the lack of analysis into *why* models fail and the exclusion of foundation models that represent current practical state-of-the-art. The benchmark itself is a valuable contribution, but the paper would benefit from deeper investigation of the failure modes to guide future model development.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>