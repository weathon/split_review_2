Now I have sufficient calibration data. Let me write the final review.

## Summary

This paper identifies post-treatment selection as a key challenge in interventional causal discovery and develops a theoretical framework to address it. The authors extend the augmented DAG framework to include selection, define a fine-grained interventional Markov equivalence class (ℱℐ-Markov equivalence), introduce a new graphical representation (ℱ-PAG) with novel edge marks, and propose the ℱ-FCI algorithm with soundness and completeness guarantees. Synthetic experiments show improved precision and SHD over baselines.

## Strengths

1. **Problem identification is genuinely important and well-motivated.** The paper correctly identifies post-treatment selection as a real and underappreciated challenge in interventional causal discovery. The core observation — that post-treatment selection produces the same pattern of marginal-change-and-conditional-invariance as genuine causation (Section 2.2, Figure 1) — is clearly explained with concrete examples from gene expression analysis and clinical trials (Introduction, Section 2). This gap in existing frameworks is well-demonstrated.

2. **The theoretical extension is technically sound and novel.** The paper extends the augmented DAG framework to include post-treatment selection (Definition 1), characterizes Markov properties (Theorem 1), defines ℱℐ-Markov equivalence (Definition 2), and proposes ℱ-PAG as a more expressive graphical representation (Definition 5) with new edge marks (square, Δ, ▲). The theoretical machinery — inducing paths, Lemmas 2–4, Theorem 2 — is a natural and principled extension of prior work (Zhang, 2008b; Kocaoglu et al., 2019). The soundness and completeness guarantees (Theorems 3 and 4) provide theoretical grounding for the algorithm.

## Weaknesses

### Major

1. **The experimental evaluation does not adequately support the paper's central claims.** Several specific issues stand out:

   **(a) The core claim — distinguishing causation from post-treatment selection — is never directly evaluated with appropriate metrics.** The paper reports DAG Precision and DAG SHD (comparing estimated vs. true DAG), but these are coarse metrics that do not isolate whether ℱ-FCI correctly identifies which dependencies are causal versus selection-induced. A direct evaluation would measure edge-type classification accuracy (e.g., how often ℱ-FCI correctly distinguishes a causal edge from a selection path). Table 1 — which purportedly assesses this capability — is mentioned only in passing (line 277) and relegated to the appendix with no discussion in the main text.

   **(b) The real-world evaluation (Section 5.2) is essentially absent from the main paper.** It consists of only two sentences describing the Norman dataset application, with no quantitative results — no precision, recall, or F1 numbers. Results are deferred entirely to Figure 13 and Appendix D.3. For a paper whose claimed contribution includes "demonstrating effectiveness on real-world datasets," this is a significant omission.

   **(c) No ablation study is provided.** The algorithm has multiple components (skeleton discovery from observational data, CI pattern collection, orientation rules with six conditionals, Type I inducing node detection, standard FCI orientation rules). Without ablation, it is impossible to determine which components drive the reported improvements or whether the gains come primarily from the novel ℱ-specific machinery versus the basic advantage of having interventional data.

2. **Algorithm specification gaps hinder reproducibility and assessment.** 

   **(a) The "AllPaths" function in Step 2.1 (line 211) is undefined.** Path enumeration is #P-hard in general; without specifying how conditioning sets are enumerated and bounded, the algorithm's computational practicality is unclear.

   **(b) The type of CI test used in experiments is never stated.** This is critical because the data is generated using nonlinear functions (sin, tanh, square) — a linear partial correlation test would behave very differently from a kernel-based or discretization-based test.

   **(c) The loop structure of Step 2 (line 207) iterates over intervention target pairs (i,j), but the orientation rules in Step 2.2 are described as operating on pairs of variables X_{ℐ^{(i)}} and X_{ℐ^{(j)}}. It is unclear how this works for multi-node intervention targets or for variables that are not intervention targets.**

3. **The Type I inducing node dependency is a severe practical limitation that is acknowledged but not quantified.** The method can only disambiguate causation from selection when intermediate nodes on inducing paths happen to be intervention targets (Step 2.3, lines 230–240). For paths composed solely of Type II inducing nodes, the method cannot distinguish causation from selection. The paper does not report what fraction of edges in the synthetic experiments have the favorable Type I structure, so the reported average performance may overstate general applicability. This limitation is mentioned in Section 6 but not used to qualify any experimental claims.

### Minor

4. **The pre-treatment vs. post-treatment distinction is underspecified in the graph model.** The paper states it "specializes in post-treatment selection" (line 60) but the selection variable S in the graph model simply has parents from X, which could represent either pre- or post-treatment selection. The data generation procedure (Section 5.1) samples selection variables "with two randomly chosen parents from X_i" without constraining temporal ordering relative to interventions. The crucial distinction that makes post-treatment selection specifically challenging — selection occurring after intervention — is not enforced in the model or experiments.

5. **Data generation details affect reproducibility.** The noise distribution uses $\text{Unif}([0,2] \cup [2,4])$ — an unusual choice with a gap at 2 — and the selection threshold is simply "a predefined interval" without specification. Both choices directly determine the difficulty of the selection problem and should be reported precisely.

6. **No runtime or complexity analysis.** Given the undefined AllPaths function, the algorithm's scaling behavior is completely opaque. The synthetic experiments with up to 25 variables provide no evidence of practical scalability.

### Trivial

None.

## Nice-to-Haves

- A direct edge-type classification experiment evaluating how often ℱ-FCI correctly labels a dependency as causal vs. selection-induced, with confusion matrices.
- Quantification of the fraction of edges in synthetic data that are resolvable via Type I inducing nodes, stratified by experimental configuration.
- Specification of the CI test used (kernel-based, partial correlation, etc.) and justification for its choice given nonlinear data.
- Move Table 1 (distinguishing post-treatment selection) into the main text with explicit discussion.
- Runtime measurements and complexity analysis of the AllPaths procedure.

## Removed Points

These points were identified by reviewers but removed from the main review per the filtering rules. Treat them with caution:

- **"ℱ-FCL" vs "ℱ-FCI" typo in abstract**: Removed — parser/formatting artifact, not an author error.
- **Step 2.2 orientation rules all showing identical CI patterns**: Removed — parser corruption of the PDF content.
- **Step 2.3 notation issues (cycling edges, unclear arrow notation)**: Removed — parser artifact, the original submission would render these correctly.
- **Missing code URL**: Removed — per hard rules, reproducibility nitpicks about artifacts not included in the submission.
- **Missing appendix content (proofs, figures, Table 1 details)**: Removed — the parser strips appendix content from all papers; these exist in the original submission.
- **"Comparisons are staged — baselines cannot handle selection"**: Partially removed. The critic claimed that "no comparison against a method that handles selection (e.g., CDIS)" was missing, but CDIS (Dai et al., 2025, handling pre-treatment selection) IS included as a baseline. However, the broader point about the evaluation lacking proper controls (no ablation, no direct metric for the core claim) is retained in Major weakness 1.
- **"Theorem 1 states standard results, not novel"**: Removed — the paper frames this as characterizing Markov properties in the new setting, not claiming Theorem 1 itself as a novel result. The novelty resides in the overall framework.
- **"Definition 2 seems to collapse to a smaller equivalence class"**: Removed — speculative and cannot be verified from the main text without the full formal development in the appendix.
- **Criticism about missing related work**: Removed per hard rules (cannot verify from external sources).

## Novel Insights

None beyond the paper's own contributions. The harsh critic's review primarily surfaced issues with the experimental validation and algorithm specification but did not generate genuinely novel insights about the problem or solution that the paper itself had not already articulated.

## Suggestions

1. **Restructure the experimental section to directly test the core claim.** Design experiments where ground truth distinguishes causal edges from selection-induced dependencies and report per-edge-type classification accuracy (precision/recall for causal edges, selection edges, latent confounder edges). Move Table 1 into the main paper with explicit discussion.

2. **Provide a quantitative real-world evaluation.** At minimum, report precision/recall/F1 against known regulatory relationships (e.g., from Enrichr or other databases) for the Norman dataset, and compare against at least one baseline method on the same data.

3. **Run an ablation study** removing or varying each major component of the algorithm (CI pattern orientation rules, Type I inducing node detection, standard FCI post-processing) to isolate what drives performance gains.

4. **Specify the AllPaths procedure** and its computational complexity, or replace it with a practical bounded approximation. Report the type of CI test used and justify its suitability for nonlinear data.

5. **Disambiguate the pre-treatment/post-treatment distinction** by specifying temporal constraints in the data generation and clarifying whether the graph model enforces that S is a descendant of intervened variables.

## Score and Decision

### Calibration

Round 1 (bracketing) retrieved the following anchor papers:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| xByvdb3DCm.md ("When Selection meets Intervention") | 8.00 | 1 | Very similar topic (selection bias + intervention). Accepted with 8/10. Stronger experiments (quantitative real-world eval). Our theory is comparable but experiments weaker. |
| G5KbDVAlI6.md ("GRN Inference with Selection Bias") | 4.00 | 1 | Similar topic (selection + latent confounders). Rejected. Weaker theory, similar experiment scale. Our paper has stronger theoretical foundation. |
| cbFqqtJGtA.md ("Predicting perturbation targets") | 4.25 | 1 | Causal discovery + biology domain. Rejected. Different problem focus. |
| ZXs3pkmrRG.md ("Test-Time Learning of Causal Structure") | 5.50 | 2 | Interventional causal discovery. Rejected with mixed scores (8,3,6,5). Stronger experiments than our paper but weaker theory. |

Round 1 bracket: [4.0, 6.5]

Narrowing: Our paper's theoretical contribution is stronger than the 4.0–5.5 anchors (which were rejected) but its experimental validation is notably weaker than the 8.0 anchor (which was accepted). The soundness + completeness proofs and the novel ℱℐ-Markov equivalence / ℱ-PAG framework represent a genuine theoretical advance. However, the experimental evaluation falls short of ICLR standards for an algorithmic paper: the core claim is never directly tested, the real-world evaluation is absent from the main text, and there is no ablation. Given the gap between the strength of the theoretical contribution and the weakness of the empirical validation, the paper is borderline but tilts toward rejection in its current form.

### Final Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>