Based on the calibrated scores, let me produce the final review.

The strengths are uniformly very strong (+8.8 to +10.0), confirming the theoretical contribution is genuine and novel. The main weaknesses are the thin experimental presentation in the main text (-9.5) and the missing ablation (-8.5). The theoretical core is sound but the empirical validation needs to be brought to the main text at a level commensurate with the paper's claims. I assess this as a borderline accept — the contribution is real but the presentation of experimental evidence needs significant strengthening.

---

## Summary

This paper addresses an important and underappreciated problem: post-treatment selection in interventional causal discovery. The authors show that standard frameworks cannot distinguish post-treatment selection from direct causation (Figure 1), build a theoretical framework (augmented DAGs with selection, FI-Markov equivalence, F-PAG representation), and propose the F-FCI algorithm with formal soundness and completeness guarantees. The core technical insight — using hard interventions on Type I inducing nodes to disambiguate causation from selection — is genuinely novel.

## Strengths

- **Important and well-motivated problem.** The paper identifies post-treatment selection as a distinct challenge that existing causal discovery frameworks cannot handle, clearly illustrated in Figure 1 where selection and causation produce identical cross-intervention CI patterns. The motivation via gene perturbation studies and clinical trials is concrete and compelling.

- **Non-trivial theoretical extension of the causal discovery framework.** The paper systematically builds augmented DAGs with explicit selection variables (Section 3.1), characterizes Markov properties (Section 3.2), defines the FI-Markov equivalence class (Definition 2) and the F-PAG graphical representation (Definition 5). The lemmas connecting inducing paths to MAG tail/arrowhead marks (Lemmas 2–4) and the graphical criteria for FI-Markov equivalence (Theorem 2) are technically sound extensions of existing MAG/PAG theory.

- **Novel insight for disambiguating causation from selection.** The core idea — using hard interventions on Type I inducing nodes to distinguish whether a dependence between two intervened variables is due to direct causation, indirect causation, or selection (lines 132, 251) — is genuinely novel and goes beyond existing equivalence classes. The examples in Figure 4(b) vs. 4(f) illustrate this concretely.

- **Formal soundness and completeness guarantees.** Theorems 3 and 4 provide formal guarantees for the F-FCI algorithm, which is non-trivial given the complexity of simultaneously handling latent confounders, selection, and multiple interventional environments.

## Weaknesses

### Major

- **Thin experimental evidence in the main text for the paper's central claim.** The paper's raison d'être is distinguishing causal relations from post-treatment selection, yet the main text contains no quantitative evidence of this specific capability. The critical Table 1 (assessing selection-detection ability) is only referenced as being in the appendix (line 278). The real-world evaluation (Section 5.2) describes a procedure using Enrichr but reports zero quantitative outcomes — no hit rate, precision/recall against known regulatory interactions, or overlap counts. While Precision and SHD comparisons against baselines on synthetic data are reported in Figure 6 and show F-FCI outperforming, a reader of the main text alone cannot evaluate whether the method actually achieves its advertised purpose of distinguishing selection-induced dependencies from causal ones.

- **No ablation study isolating the core contribution.** The paper compares F-FCI against baselines that do not model post-treatment selection. Two critical controls are absent: (a) performance on data **without** post-treatment selection — the richer F-PAG representation (square marks, Δ/▲ edges) could introduce false positives when no selection exists; (b) an ablation removing Step 2.3 (Type I inducing node detection) would directly quantify the value of the paper's central technical insight versus simply running FCI with interventional data. Without these, it is unclear whether improvements reflect genuine identification or the flexibility of a more expressive output representation.

### Minor

- **Overstated completeness claim.** The abstract and introduction repeatedly claim a "sound and complete algorithm" (lines 9, 33, 289) without qualification. The conclusion (line 291) reveals that identification depends critically on the presence of Type I inducing nodes and that structures involving only Type II inducing nodes are left as future work. This means the method is provably incomplete for an important class of structures. This limitation should be stated more prominently in the abstract and contributions.

- **Unjustified assumption about selection scope.** The paper states that selection works "on at least two observed variables" (line 60) without justification. It is unclear whether the method degrades, fails, or is undefined with only one selected variable, and why this boundary case is excluded.

### Trivial

None.

## Nice-to-Haves

- A runtime/scalability comparison with baselines would be useful for practical deployment, especially on biological datasets with many variables.
- Sensitivity analysis to CI test significance thresholds and sample sizes would strengthen the empirical evaluation.
- A concrete quantitative real-world result (e.g., edge overlap counts against known regulatory interactions from Enrichr) would substantially strengthen the real-world evaluation.

## Removed Points

- **Algorithm reproducibility complaint about CI tuples being identical (lines 216–226):** Parser artifact — the original PDF would have had different CI patterns. Removed per formatting-artifact hard rule.
- **Complaint about "hat{X}_{pag(i)} never defined":** It is defined on line 86 as indicating the parents of X_i. The critic missed this.
- **Complaint about self-loop notation in Step 2.3:** The specific rendering is a parser artifact; the notation represents edge marks on a path, not a graph-theoretic self-loop.
- **Complaint about 8 vs. 10 edge types in Definition 5:** Duplication is a parser artifact from PDF extraction.
- **Complaint about CDIS baseline selection:** CDIS is a relevant baseline for selection-aware causal discovery; the comparison set is reasonable.
- **General readability complaints that are standard for theory papers:** Dense prose and deferred proofs are typical for the target venue.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the paper's stated contributions (motivation, theoretical framework, Type I inducing node insight) and surface the key gap: the experimental validation is not presented at a level commensurate with the strength of the claims.

## Suggestions

1. Move the selection-detection evaluation (Table 1 or equivalent) from the appendix into the main text, since distinguishing selection from causation is the paper's central claim.
2. Add an ablation removing Step 2.3 to isolate the value of the Type I inducing node detection.
3. Add a control experiment on data without post-treatment selection to verify F-PAG does not introduce false positives.
4. Qualify the "sound and complete" claim in the abstract to reflect the Type I inducing node requirement.
5. Provide at least one quantitative real-world metric (e.g., precision/recall against known regulatory edges from Enrichr).

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>