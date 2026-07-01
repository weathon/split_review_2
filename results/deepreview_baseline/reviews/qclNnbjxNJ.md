## Summary

This paper addresses the problem of post-treatment selection in interventional causal discovery, where samples are selectively included after interventions (e.g., quality control in gene expression studies). The authors introduce a new causal formulation that explicitly models post-treatment selection alongside latent confounders, define a novel fine-grained interventional equivalence class (ℱℐ-Markov equivalence) with a corresponding graphical representation (ℱ-PAG), and develop a sound and complete algorithm (ℱ-FCI) that can distinguish true causal relations from selection-induced dependencies using both observational and interventional data.

## Strengths

- **Important and underexplored problem**: Post-treatment selection is a genuine challenge in biological and clinical settings (e.g., single-cell perturbation studies, per-protocol clinical trial analyses), yet it has been largely overlooked by existing interventional causal discovery frameworks. The paper correctly identifies this gap and provides a principled treatment.

- **Novel theoretical contribution**: The ℱℐ-Markov equivalence class and ℱ-PAG representation are well-motivated extensions that capture more structural information than standard PAGs. The theoretical characterization of how post-treatment selection differs from causal relations in terms of structural symmetries and CI patterns is insightful.

- **Soundness and completeness proofs**: The paper provides theoretical guarantees (Theorems 3 and 4) for the proposed ℱ-FCI algorithm, which is a strong contribution for a constraint-based causal discovery method.

- **Clear motivation with concrete examples**: Figure 1 and the accompanying discussion effectively illustrate why existing methods fail to distinguish causal relations from post-treatment selection, making the problem accessible.

## Weaknesses

### Major

- **Algorithm description is incomplete and unclear**: Algorithm 1 contains placeholder notation (e.g., "CIs == (⟂, ⟂, ⟂, ⟂)" repeated with identical conditions for different orientations) that makes the orientation rules impossible to follow. The actual CI pattern conditions that distinguish different edge types are not specified. This is a critical flaw—the core algorithmic contribution is not properly described.

- **Missing experimental details for reproducibility**: The paper states that a Python implementation is available but provides no URL. The simulation setup mentions "randomly drawn from linear, square, sin and tanh" for functions, but the exact selection mechanism (predefined interval) is vague. Without these details, the experiments cannot be reproduced.

- **Limited baseline comparison**: The baselines (GIES, IGSP, UT-IGSP, JCI-GSP, FCI-interven, CDIS) are all methods that do not model post-treatment selection. The paper would benefit from comparing against a method that explicitly handles selection (e.g., FCI with selection bias modeling) to demonstrate the specific advantage of the proposed approach.

- **Real-world evaluation is superficial**: The real-world application on Norman datasets is described in one paragraph with a reference to Appendix D.3, but the appendix is not included in the provided content. The claim that results are "evaluated using prior knowledge provided by Enrichr" is vague—what specific metrics or validation criteria were used?

### Minor

- **Notation overload**: The paper introduces many new symbols (ℱ, ℱℐ, ℱ-PAG, ℱ-FCI, Type I/II inducing nodes, square marks, triangle marks) without sufficient intuitive explanation. The distinction between different edge types in ℱ-PAG (especially the triangle marks) is not clearly justified with examples.

- **Theoretical results rely on oracle CI tests**: The soundness and completeness theorems assume access to oracle CI tests. The paper does not discuss how finite-sample CI testing affects the algorithm's performance or provide guidance on CI test selection.

### Trivial

- The paper uses "Augz" and "Aug" inconsistently for the augmented DAG notation.

## Nice-to-Haves

- A table summarizing the CI pattern conditions for each orientation rule in Step 2.2 would greatly improve clarity.
- An ablation study showing performance with vs. without the Type I inducing node detection step would help validate its importance.
- Discussion of computational complexity and practical runtime would be useful for practitioners.

## Novel Insights

The key insight is that post-treatment selection and causal relations produce identical patterns of marginal variability and conditional invariance under interventions, making them indistinguishable within existing frameworks. The paper's novel observation is that by leveraging hard interventions on Type I inducing nodes (non-endpoint nodes on inducing paths), one can break this symmetry and distinguish genuine causal links from selection-induced dependencies. This insight extends beyond the specific problem setting—it suggests that multiple distinct interventions can resolve ambiguities that single interventions cannot, which has broader implications for experimental design in causal discovery.

## Suggestions

1. **Clarify Algorithm 1**: Replace the placeholder "CIs == (⟂, ⟂, ⟂, ⟂)" with the actual CI pattern conditions for each orientation rule. Provide a table mapping CI patterns to edge types, similar to Figure 4(i) but comprehensive.

2. **Provide the code URL**: Include the actual repository URL in the paper for reproducibility.

3. **Strengthen real-world evaluation**: Report quantitative metrics (e.g., precision/recall against known regulatory relationships) rather than just qualitative analysis. If the appendix contains this, ensure it is included.

4. **Add a complexity analysis**: Discuss the computational complexity of ℱ-FCI, particularly the path enumeration in Step 2.3, which could be exponential in the worst case.

5. **Discuss limitations of Type I inducing node detection**: Acknowledge that the method cannot distinguish causal relations from selection when inducing paths consist solely of Type II inducing nodes, and discuss potential workarounds.

## Score and Decision

The paper addresses a genuinely important and overlooked problem with a principled theoretical framework. The core ideas are novel and the theoretical contributions (ℱℐ-Markov equivalence, soundness/completeness) are valuable. However, the incomplete and unclear algorithm description is a major flaw that prevents proper evaluation of the method. The experimental evaluation, while showing promising results, lacks sufficient detail for reproducibility and the real-world validation is superficial. Given these issues, the paper requires substantial revision before acceptance.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>