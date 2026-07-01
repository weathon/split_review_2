## Summary

The paper introduces the problem of PPI candidate ranking—prioritizing novel protein-protein interactions for experimental validation—and proposes a two-stage framework. First, an interpretability-guided retrieval step uses contact-map-activated embedding regions from D-SCRIPT or Topsy-Turvy to rank candidates by cosine similarity to known interactors. Second, a re-ranking module refines the top candidates using interaction scores, structural plausibility (SpeedPPI/pDockQ), functional annotations, and LLM-based semantic similarity. Evaluated on STRING v11→v12 transitions, the method substantially improves ranking metrics over direct use of prediction probabilities from D-SCRIPT, Topsy-Turvy, and xCAPT5.

## Strengths

- **Well-motivated problem.** The paper correctly identifies that experimental PPI validation is costly and that computational methods should prioritize candidates rather than merely classify pairs. The prospective evaluation design (training on v11, testing on v12) is appropriate and practically relevant.
- **Large-scale, realistic evaluation.** Using successive STRING releases with high-confidence physical interactions provides a clean testbed for assessing whether models can anticipate future discoveries. The scale (279,568 new positives) gives statistical credibility.
- **Clear improvements over baselines.** Table 1 shows that the interpretability-guided retrieval consistently outperforms direct use of prediction probabilities across all cutoff values and metrics. For D-SCRIPT, Recall@10 rises from 1.2% to 26.4%, and MRR increases from 0.034 to 0.169.
- **Insightful re-ranking analysis.** Table 2 systematically compares ten different re-ranking signals and reveals that PubMedBERT and lightweight annotation overlaps (Token, Location, KeyTerm) provide the most consistent improvements, while pDockQ underperforms. This analysis offers practical guidance for future work.

## Weaknesses

### Fatal
None.

### Major
- **Overclaim of improvement magnitude.** The abstract and conclusions state that the method improves ranking metrics by “two orders of magnitude.” The largest observed improvement in Table 1 is Recall@5 for D-SCRIPT (0.0071 → 0.1832, a factor of ~26×), which is roughly 1.4 orders of magnitude, not two (100×). This misrepresentation undermines the paper’s credibility and should be corrected.
- **Re-ranking evaluation is limited to top-10 candidates.** The re-ranking analysis (Table 2) only considers the top 10 candidates per target protein. This is a very small set, and it is unclear whether the observed rank-shift patterns generalize to larger candidate pools. Moreover, the paper does not report overall ranking metrics (e.g., Recall@k, MAP) after re-ranking, making it impossible to assess the net benefit of the refinement stage.
- **Insufficient baseline coverage.** The main comparisons are against D-SCRIPT and Topsy-Turvy, which are several years old. xCAPT5 is included in Table 1 but is not described in the method section, and no other recent PPI predictors (e.g., structure-based methods like FoldDock, or other sequence-based models) are compared. The claim of “state-of-the-art” is not fully supported.

### Minor
- **Reliance on known interactors.** The method requires a set of known partners for each target protein. For understudied proteins with few or no known interactors, the interpretability-guided retrieval cannot be applied, and the framework reduces to using raw prediction probabilities. This limitation is acknowledged but not quantitatively analyzed.
- **No ablation study.** The paper does not isolate the contribution of individual components (e.g., using activated regions vs. full embeddings, max similarity vs. mean similarity, the effect of the contiguous segment selection). Such an ablation would strengthen the methodological justification.
- **Potential data leakage in STRING v12.** STRING v12 interactions may include computationally predicted interactions that were already inferable from v11 data, not purely novel experimental discoveries. The paper filters for experimental support > 0, but STRING’s experimental evidence includes various types; the prospective nature of the evaluation could be clarified.
- **No statistical significance tests.** The improvements in Table 1 are reported as point estimates without confidence intervals or significance tests, making it difficult to assess variability.
- **Computational cost is mentioned but not quantified.** The paper states runtimes of “hundreds of hours” (Figure 2, not provided) but does not discuss practical feasibility or compare costs across methods.

### Trivial
- The phrase “a the two-stage framework” (Section 4) is a minor grammatical issue.

## Nice-to-Haves

- Provide code and data to enable reproducibility.
- Combine the multiple re-ranking signals into a single, fused ranking (e.g., via learning-to-rank) rather than evaluating each independently.
- Include more recent PPI prediction methods (e.g., FoldDock, ESM-based predictors) as baselines.
- Analyze performance stratified by the number of known interactors to quantify the method’s robustness for understudied proteins.

## Novel Insights

The paper demonstrates that internal model representations (contact-map-activated embedding regions) are substantially more effective for ranking novel PPIs than the final prediction probabilities. This suggests that the supervised training objective may compress away information that is useful for generalization to future interactions. Additionally, the re-ranking analysis reveals that lightweight semantic signals (token overlap, key-term Jaccard) often match or exceed the gains from expensive structure-based scores (pDockQ), indicating that functional annotation similarity is a strong and underutilized signal for PPI prioritization.

## Suggestions

- Correct the “two orders of magnitude” claim to reflect the actual improvement factors (roughly 20–25×, i.e., one order of magnitude).
- Extend the re-ranking evaluation to larger candidate sets (e.g., top-100 or top-500) and report overall metrics (Recall@k, MAP) after re-ranking to quantify the net benefit.
- Add an ablation study that removes the activation-region selection and uses full embeddings, or replaces max similarity with mean similarity, to justify design choices.
- Include confidence intervals or bootstrapped standard errors for the main retrieval results.
- Discuss the computational cost of the interpretability-guided retrieval more concretely and compare it to the cost of running the baseline predictors.

## Score and Decision

**Score:** 4.0

**Decision:** Reject

The paper addresses a practically important problem and presents a well-designed evaluation with clear improvements over baselines. However, the overclaim of “two orders of magnitude” is a significant misrepresentation of the results, and the re-ranking evaluation is too limited to fully support the claimed benefits. These issues, combined with insufficient baseline coverage and lack of ablation studies, prevent the paper from meeting the acceptance threshold in its current form. The core ideas are promising, and with substantial revisions (correcting the overclaim, extending the re-ranking analysis, and adding more rigorous comparisons), the paper could become a strong contribution.

MY FINAL SCORE: 4.0<score>  
MY FINAL DECISION: Reject<decision>