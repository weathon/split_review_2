## Summary
The paper addresses post-treatment selection in interventional causal discovery, a problem where samples are selectively included after interventions, leading to spurious dependencies that mimic causal relations. The authors propose a new causal formulation that explicitly models post-treatment selection alongside latent confounders, define a fine-grained interventional Markov equivalence (FI-Markov) and a new graphical representation (F-PAG), and develop an algorithm F-FCI that is provably sound and complete for recovering the equivalence class. Empirical results on synthetic data demonstrate the method's effectiveness, and real-world results are described (though relegated to the appendix).

## Strengths
- **Original and important problem**: Post-treatment selection is often overlooked in causal discovery despite being common in practice (e.g., single-cell genomics, clinical trials). The paper clearly motivates the gap and shows rigorously that existing interventional frameworks cannot distinguish post-treatment selection from true causal relations.
- **Strong theoretical contributions**: Formal modeling of post-treatment selection, characterization of Markov properties under the augmented DAG framework, definition of FI-Markov equivalence, and proofs of soundness and completeness for the proposed algorithm. The graphical criteria (Lemmas 2–4, Theorem 2) are well grounded.
- **Sound algorithmic design**: The algorithm extends FCI with novel orientation rules that leverage invariance patterns across interventions (e.g., patterns in Figure 4) and uses hard interventions on Type I inducing nodes to resolve ambiguities that prior methods cannot.
- **Convincing empirical validation**: Synthetic experiments show consistent improvements over strong baselines (GIES, IGSP, UT-IGSP, FCI-interven, CDIS) in precision and SHD across multiple sample sizes, numbers of variables, and both hard/soft intervention settings. The improvements are non-trivial (e.g., 5+% precision gains) and robust.

## Weaknesses
### Major
- **Incomplete real-world validation in main text**: The real-world application to gene regulatory networks (Norman dataset) is described only in text and Appendix D.3, which is stripped. Without access to the appendix, reviewers cannot evaluate the real-data claims or the quality of the biological validation. While synthetic experiments alone can support a paper, the paper explicitly touts real-world applicability, making this omission harmful.
- **Algorithm pseudocode is underspecified**: Step 2.2 of Algorithm 1 uses generic conditions like "if CIs == (⊥, ⊥, ⊥, ⊥)" without indicating which CI test corresponds to each entry. The reader is forced to infer from Figure 4(i), which itself contains a truncated table. This obscures the correctness of the orientation rules and makes reproducibility harder.

### Minor
- **Completeness theorem is vaguely stated**: Theorem 4 says "each type of substructures... can be identified by different types of CI patterns" without specifying the mapping. A more precise statement (e.g., listing the CI patterns and the resulting edge marks) would strengthen the contribution.
- **Faithfulness and finite-sample issues**: The paper assumes faithfulness and oracle CI tests; practical deployment would require handling finite-sample errors, which is only briefly touched upon in the robustness experiments (appendix). A discussion of limitations under realistic CI testing would improve practical guidance.
- **Scalability assessment limited**: Synthetic experiments go up to 25 variables. Real-world gene networks can be much larger; scalability is mentioned in the appendix but not accessible here.

### Trivial
- Some notation (e.g., "Type I inducing node") is defined late (Definition 6) and could be introduced earlier with a concrete example to aid intuition.

## Nice-to-Haves
- A summary table mapping CI patterns (six rows) to the resulting edge marks in F-PAG would greatly improve clarity.
- Discussion of how to distinguish post-treatment selection from other forms of selection bias (pre-treatment selection) or from biological constraints, as mentioned in the conclusion, would be a valuable extension.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Move at least a summary of the real-world results (e.g., a table of recovered edges vs. prior knowledge) into the main paper, even if detailed analysis stays in the appendix.
- Replace the generic "if CIs == (⊥, ⊥, ⊥, ⊥)" in Algorithm 1 with explicit tuples (e.g., (⊥, ⊥, ⊥, ⊥) → X_i → X_j) and reference the corresponding row in Figure 4.
- Strengthen completeness theorem with an explicit list of identifiable CI patterns and the resulting edge marks.

## Score and Decision
MY FINAL SCORE: 8.0
MY FINAL DECISION: Accept