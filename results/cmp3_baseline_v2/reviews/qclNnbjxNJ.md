## Summary

This paper identifies a fundamental yet overlooked challenge in interventional causal discovery: *post-treatment selection*, where samples are selectively retained after interventions (e.g., quality control in gene perturbation studies). The authors show that existing frameworks cannot distinguish causal relations from post-treatment selection because both induce the same pattern of marginal distribution change and conditional distribution invariance. They propose a new formulation that explicitly models post-treatment selection via augmented DAGs, define a finer-grained equivalence class (ℱℐ-Markov equivalence) and a corresponding graphical representation (ℱ-PAG), and develop a sound and complete algorithm (ℱ-FCI) that recovers causal relations, latent confounders, and post-treatment selection up to this equivalence class. Experiments on synthetic and real-world gene perturbation data demonstrate improved precision over baselines.

## Strengths

- **Important and well-motivated problem.** Post-treatment selection is common in practice (e.g., single-cell genomics, clinical trials) but has been largely ignored in causal discovery. The paper clearly illustrates why this issue breaks existing interventional formulations and provides compelling real-world motivation.
- **Rigorous theoretical framework.** The paper formally defines augmented DAGs with selection, characterizes Markov properties via d-separation, establishes graphical criteria for ℱℐ-Markov equivalence, and proves soundness and completeness of the ℱ-FCI algorithm. The extension of PAG to ℱ-PAG with new edge types (square, triangle) is a principled way to represent the finer equivalence class.
- **Novel algorithmic contribution.** ℱ-FCI leverages interventional data to go beyond traditional equivalence classes by exploiting CI patterns involving intervention indicators and Type I inducing nodes. The algorithm is clearly structured into skeleton discovery, orientation from CI patterns, and refinement using additional interventions.
- **Empirical validation.** Synthetic experiments show consistent improvements in precision and SHD over strong baselines (GIES, IGSP, UT-IGSP, JCI-GSP, FCI-interven, CDIS) across varying sample sizes and numbers of variables. The real-world application on Norman et al. (2019) gene perturbation data demonstrates practical utility.

## Weaknesses

### Major

1. **Algorithm description is incomplete and unclear.** The pseudocode in Algorithm 1 uses placeholder conditions (e.g., `CIs == (⊥, ⊥, ⊥, ⊥)`) without specifying the actual CI patterns that map to each orientation rule. The orientation rules are only hinted at via Figure 4, but the mapping from CI test outcomes to edge types is not explicitly given. This makes the algorithm difficult to reproduce or verify. The refinement step (Step 2.3) is also described at a high level without concrete decision criteria.

2. **Experimental evaluation is limited in scope.** The synthetic experiments compare against methods that do not model post-treatment selection, so outperformance is expected. The paper does not compare against any method that explicitly handles selection bias (e.g., selection-bias-corrected FCI or methods that model selection variables). The real-world experiment is only briefly described in the main text; results are relegated to the appendix and validation relies on enrichment analysis (Enrichr), which is an indirect and noisy proxy for ground truth. No quantitative metrics (e.g., precision/recall against known regulatory interactions) are reported for the real data.

3. **Practical assumptions are not discussed.** The algorithm assumes faithfulness and oracle CI tests for theoretical guarantees, but in practice CI tests are imperfect. The paper does not analyze sensitivity to CI test parameters, sample size requirements, or the impact of violations of faithfulness. The refinement step (Step 2.3) requires interventions on Type I inducing nodes, but the paper does not discuss what happens when such interventions are unavailable or how to select which nodes to intervene on.

### Minor

- The paper is dense and notation-heavy, making it hard to follow the key ideas. Some definitions (e.g., inducing node, Type I/II) are introduced late and could be better motivated earlier.
- The distinction between hard and soft interventions is mentioned but not consistently used in the algorithm description. Step 2.3 mentions "two hard interventions" but the algorithm input only specifies intervention targets without type.
- The ℱ-PAG edge types (square, triangle) are defined but their interpretation in terms of underlying causal structure is not fully explained with examples beyond Figure 5.

### Trivial

- The paper uses non-standard symbols (e.g., `\xrightarrow{\Delta}`) that may not render correctly in all viewers.

## Nice-to-Haves

- Provide a complete lookup table mapping CI test outcomes (e.g., which of the four CI tests are true/false) to each orientation rule in Step 2.2.
- Include a sensitivity analysis on the CI test threshold and sample size to demonstrate robustness.
- Add a comparison with a baseline that explicitly models selection (e.g., by including selection variables in the graph) to isolate the benefit of the proposed formulation.
- Discuss the computational complexity of ℱ-FCI and its scalability to larger graphs.

## Novel Insights

Beyond the paper's own contributions, the key insight is that post-treatment selection and causal relations are distinguishable through the *asymmetry* of CI patterns involving intervention indicators and the use of *Type I inducing nodes*—nodes that, when intervened upon, reveal whether an inducing path contains a true causal link or a selection structure. This observation generalizes the idea that interventional data can break symmetries that are indistinguishable from purely observational data, and it provides a principled way to refine equivalence classes beyond what standard PAGs can represent.

## Suggestions

1. **Clarify the algorithm.** Replace the placeholder CI conditions in Algorithm 1 with explicit patterns (e.g., using a table or decision tree). Provide a concrete example of how Step 2.2 maps CI test results to edge orientations.
2. **Strengthen experiments.** Include a synthetic setting where post-treatment selection is absent to verify that ℱ-FCI does not overfit to selection patterns. For real data, report quantitative metrics against known ground truth (e.g., from curated databases) or at least provide a more detailed analysis of the identified selection structures.
3. **Discuss limitations of the refinement step.** Address the scenario where Type I inducing nodes are not intervened upon—can the algorithm still distinguish causal relations from selection? If not, state this limitation explicitly.
4. **Improve readability.** Move some of the dense notation to a table or glossary. Use more intuitive names for the new edge types (e.g., "selection-induced" instead of square/triangle).

## Score and Decision

**Score:** 6  
**Decision:** Accept

The paper addresses a genuinely important and underexplored problem with a rigorous theoretical framework and a novel algorithm. The main weaknesses are in presentation clarity and experimental depth, which are addressable in revision. The contribution is above the acceptance threshold for ICLR.

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>