## Summary
This paper identifies a fundamental yet overlooked challenge in interventional causal discovery: post-treatment selection, where samples are selectively included after interventions (e.g., quality control in gene perturbation studies). The authors show that existing frameworks cannot distinguish causal relations from selection-induced dependencies, propose a new causal formulation with explicit post-treatment selection modeling, define a finer-grained interventional Markov equivalence class (FI-Markov equivalence), introduce a novel graphical representation (F-PAG), and develop a sound and complete algorithm (F-FCI) that recovers causal structure from both observational and interventional data.

## Strengths
- **Novel and practically important problem formulation.** Post-treatment selection is genuinely underexplored in causal discovery, and the motivating examples (gene perturbation studies, clinical trials) clearly demonstrate its real-world relevance. The distinction between Figures 1(a) vs (b) and (c) vs (d) precisely identifies a gap in existing interventional frameworks that no prior work addresses.
- **Sound and complete theoretical framework.** The paper builds logically on established foundations (augmented DAGs, MAGs, PAGs) to characterize Markov properties under post-treatment selection, define a novel equivalence class, and provide graphical criteria for equivalence (Theorem 2). The soundness (Theorem 3) and completeness (Theorem 4) guarantees are formally stated.
- **Principled algorithmic contribution.** F-FCI extends the FCI framework in a principled way by exploiting CI patterns between intervention indicators and observed variables across environments. The three-step structure (skeleton discovery, orientation via interventional CI patterns, refinement via inducing node detection) is well-motivated and clearly described.
- **Strong experimental comparison.** The paper compares against six strong baselines (GIES, IGSP, UT-IGSP, JCI-GSP, FCI-interven, CDIS) across varying numbers of variables, sample sizes, and hard/soft intervention settings, with results showing consistent improvements in precision and SHD.

## Weaknesses
### Fatal
None.

### Major
- **Sensitivity to structural assumptions.** The identification of direct causal links and selection structures depends critically on the presence of Type I inducing nodes (acknowledged in the limitations). When inducing paths consist solely of Type II inducing nodes, the approach cannot disambiguate causal relations from selection. The paper does not quantify how frequently this limitation arises in practice or how performance degrades when Type I nodes are absent, which affects the general applicability of the method.
- **Thin real-world evaluation.** The real-world application (Section 5.2) presents qualitative results on gene regulatory networks evaluated against Enrichr prior knowledge, but lacks rigorous quantitative evaluation. Given that the practical motivation (gene perturbation studies) is a central selling point, a more thorough quantitative analysis with ground-truth biological benchmarks would substantially strengthen the empirical case.

### Minor
- **Theorem statements are somewhat high-level.** The soundness and completeness theorems (Theorems 3 and 4) are stated with relatively broad language ("consistent with," "can be identified by different types of CI patterns"). More precise formal statements would enhance the theoretical contribution, though this may be partly a presentation issue.
- **Limited analysis of failure modes.** The paper does not provide detailed analysis of when and why F-FCI fails to outperform baselines (e.g., for certain graph topologies or intervention configurations), which would be valuable for practitioners deciding when to apply this method.

### Trivial
None.

## Nice-to-Haves
- A characterization of the minimum number and type of interventions needed for F-FCI to distinguish post-treatment selection from causal relations, providing practical guidance for experimental design.
- Analysis of robustness when the faithfulness assumption is approximately rather than exactly satisfied.

## Novel Insights
The paper's central insight—that post-treatment selection induces the same invariance pattern (variant marginal, invariant conditional) as causal relations under interventions—is genuinely novel and identifies a fundamental blind spot in existing interventional causal discovery frameworks. The further observation that hard interventions on Type I inducing nodes along paths between intervened variables can break this non-identifiability, enabling fine-grained structural distinction beyond traditional equivalence classes, represents a meaningful advance. The proposed F-PAG graphical representation with novel edge marks (triangle, square) provides an expressive language for encoding these finer distinctions that goes beyond the standard PAG framework.

## Suggestions
- Quantify the prevalence of Type I vs. Type II inducing nodes in typical graph structures (e.g., Erdős–Rényi, scale-free) to assess the practical scope of the approach's identifiability guarantees.
- Add a controlled real-world benchmark with known ground truth (e.g., simulated single-cell perturbation data following realistic generative processes) to provide rigorous quantitative validation of the biological application.
- Provide a sensitivity analysis showing how F-FCI performance varies with the number of available interventions, which would help practitioners plan data collection.

## Score and Decision
The paper makes a genuine and well-argued contribution by identifying post-treatment selection as a fundamental challenge in causal discovery, developing a complete theoretical framework with novel equivalence classes and graphical representations, and providing a sound and complete algorithm. The theoretical contribution is solid and the problem is practically relevant. The main weaknesses are in the empirical evaluation, which could be more thorough, particularly for the real-world application. Overall, the paper advances the field in a meaningful way.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>