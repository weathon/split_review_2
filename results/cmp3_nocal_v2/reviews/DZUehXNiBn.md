Now let me produce the final consolidated review.

## Summary

This paper introduces VISTA, a modular framework for causal structure learning that decomposes the global graph into local subgraphs via Markov Blankets, aggregates them through a weighted voting mechanism with exponential decay, and enforces acyclicity via a Feedback Arc Set heuristic. The framework is model-agnostic, supports parallel execution, and is evaluated across six base learners (NOTEARS, GOLEM, DAG-GNN, GraN-DAG, SCORE, CAM) on synthetic data (up to n=300) and the Sachs protein network.

## Strengths

1. **Clean, modular, model-agnostic design.** VISTA separates MB identification, local subgraph learning, edge-level weighted voting, and acyclicity enforcement into distinct plug-in stages. The aggregation operates purely on edge counts, requiring no solver, no retraining, and no access to the base learner's internal representations (Section 3.1, Figure 2 pseudocode). This is a genuine practical advantage over ILP-based merge schemes like DCILP.

2. **Substantial and consistent runtime gains.** Table 3 shows 2–10× speedups across NOTEARS, GOLEM, DAG-GNN, GraN-DAG, and SCORE at n=50, 100, and 300. These gains follow directly from the divide-and-conquer design (smaller subgraphs → cheaper per-task learning) and are clearly a meaningful engineering contribution for practitioners.

3. **Theoretical analysis beyond heuristic merging.** Theorems 3.2, 3.4, and 3.5 provide finite-sample error bounds, a practical λ range, and asymptotic consistency — more formal grounding than prior heuristic merging schemes offer. The paper is transparent about the idealized independence assumption underlying Theorem 3.2 (line 138), and the attempt at guarantees is a step forward.

## Weaknesses

### Fatal

None.

### Major

1. **Theorem 3.5 (asymptotic consistency) assumes a scaling regime that VISTA cannot deliver.** The theorem states that consistency holds if the number of subgraphs per edge is *m = C log n* with *C > 2/min{δ_p², δ_q²}*. However, in VISTA, an edge *(X, Y)* appears only in subgraphs whose Markov Blankets contain both endpoints. For a sparse graph with bounded degree — the regime most relevant for large-scale discovery — this count is bounded by a constant (roughly the sum of the degrees of the two endpoints and their spouses). It does **not** grow with *n*. The paper does not address this disconnect; it simply states the *m ~ log n* condition without verifying whether the framework can meet it. This leaves a gap between the asymptotic claim and what the framework actually provides. The authors should either prove consistency under the realistic (bounded-*m*) regime or explicitly state the limitation.

2. **Accuracy improvements are selective and the paper overstates them.** The clearest accuracy gains occur for base learners that already perform poorly standalone (GOLEM: F1 0.35→0.60; DAG-GNN: 0.33→0.59; SCORE: 0.14→0.31; GraN-DAG: 0.06→0.17 in Table 1, ER5). For the strongest baseline, NOTEARS, the F1 gain is 0.76→0.79 — well within the baseline's own standard deviation of ±0.24. The paper's narrative of "consistently improving" accuracy (line 29, line 287) would be strengthened by an honest characterization of *when* VISTA helps most (weak learners) and when the gains are marginal (already-strong learners). The catastrophic FDR of the Naive Voting baseline (0.87 for NOTEARS) further underscores that much of WV's work is cleaning up false edges introduced by the decomposition itself — a dynamic the paper acknowledges implicitly but does not discuss candidly.

### Minor

3. **The MB identification algorithm used in all experiments is not named in the main paper.** The pipeline's quality depends heavily on MB identification accuracy (Figure 1), and the paper says it "implemented the MB solver used in that work" (line 174, referencing DCILP), but the main text does not specify which solver this is or how it was configured. Reproducibility requires this detail. (If it is specified in the appendix, it should be stated explicitly in the main paper.)

4. **Real-data evaluation does not match the "large-scale" framing.** The paper motivates VISTA for "high-dimensional" and "large-scale" settings (line 13, line 23), yet the only real-data experiment is on the Sachs network (11 nodes, 17 edges). Improvements on Sachs are modest (e.g., SHD 16→16 for GOLEM, 15→14 for DAG-GNN) and for GraN-DAG, TPR drops from 0.53 to 0.29. An evaluation on a genuinely large real dataset (e.g., a gene regulatory network with 100+ variables) would substantially strengthen the central claim.

5. **Theorem 3.2's independence assumption.** The paper correctly acknowledges (line 138) that subgraphs learned from the same dataset induce correlated votes, and states the bound should be interpreted as a "qualitative guide." This is transparent but means the theorem does not directly apply to the actual setting. No attempt is made to bound how much correlation inflates the required *m*, weakening the theoretical contribution.

### Trivial

6. **Figure 4 uses *t = 0.5* while all main-table results use *t = 0.7*.** The sensitivity analysis in Figure 4 is run at a different operating point than the tabulated results (line 205 vs. Figure 4 caption). While the qualitative trend shown is still informative, this disconnect makes it harder to relate the precision-recall curves directly to the numbers in Table 1.

7. **SHD values in NV rows are not contextualized.** SHD values of 3000+ for n=100 graphs (Table 1, NV rows) are extreme. The paper should clarify whether these are measured over the full edge space and provide context for what "random" SHD would be at this graph size.

## Nice-to-Haves

- **Comparisons to DCILP should appear in the main paper, not just the appendix.** DCILP is the closest prior work in the decompose-then-reconcile paradigm. The paper mentions Appendix F.2 contains this comparison, but it merits main-text treatment given its direct relevance.
- **Oracle-MB experiments.** Since MB quality is critical to the pipeline, an ablation using ground-truth MBs (on synthetic data) would establish an upper bound on how much improvement comes from the voting mechanism vs. the MB identification step.
- **Larger real dataset evaluation** (as noted in weakness 4 above) would directly support the paper's large-scale motivation.

## Removed Points

- **"m=1 degeneracy" (weighted voting rejects singleton edges):** Removed because Proposition 3.1 guarantees every true edge appears in at least 2 subgraphs (the subgraphs of both its endpoints). Singletons are necessarily spurious, so filtering them is a feature, not a flaw.
- **"FAS ordering may remove strong edges unnecessarily":** Removed because the paper provides a concrete justification (line 114 — avoids forcing cycle removal on already-sparse graphs), and the reviewer's counterpoint is speculative without empirical evidence.
- **"Normalized data makes baseline weaker, inflating VISTA gains":** Removed because this is an observation about the data regime, not a flaw in the method. VISTA improves across both normalized and unnormalized settings, which is evidence of robustness.
- **"DCILP should appear in main paper":** Demoted to Nice-to-Have. The comparison exists in the appendix, and the paper acknowledges it. A main-text placement would strengthen the paper but its absence is not a weakness.
- **Various formatting/style nitpicks and general-scope criticisms (e.g., "the evaluation lacks rigor," "evidence is weak for the claims"):** Removed per filtering rules for lacking concrete anchors.

## Novel Insights

The key insight emerging from the review is that VISTA's value proposition is more nuanced than the paper presents. The framework is best understood as a **weak-learner amplifier** — it provides the largest accuracy gains when the base learner is unreliable, and its primary mechanism (weighted voting) functions as a denoising filter on top of an MB decomposition that, left unfiltered (NV), produces catastrophic false-positive rates. This pattern suggests VISTA's most impactful use case is not replacing already-strong methods like NOTEARS, but making weaker or faster learners viable at scale. The theoretical gap in Theorem 3.5 (m ~ log n assumption vs. bounded-degree reality) further suggests the consistency guarantee needs re-derivation under the framework's actual operating constraints.

## Suggestions

1. **Address the m-scaling issue in Theorem 3.5.** Either (a) prove consistency under bounded m (where the number of subgraphs per edge is O(1) with respect to n), or (b) explicitly state the limitation and discuss its implications for finite-sample behavior.
2. **Calibrate the accuracy claims** to distinguish regimes where VISTA provides meaningful improvements (weak base learners) from regimes where gains are marginal (strong learners). The paper's current framing suggests broad improvement; a more honest characterization would strengthen the paper.
3. **Specify the MB solver used** in the main paper (name, implementation, configuration) so the experimental pipeline is reproducible.
4. **Include a large-scale real-data experiment** (100+ variables) to support the paper's central motivation.
5. **Contextualize SHD values** in Table 1 — explain the scale and what a "random" baseline would achieve.
6. **Unify the operating point** between Figure 4 and Table 1, or clearly state why t=0.5 is used for the sensitivity analysis.

## Score and Decision

**Score:** 6.0  
**Decision:** Accept (borderline)

**Rationale:** VISTA's core idea is clean, the runtime gains are real and significant, and the modular design has clear practical value. The theoretical analysis, while containing acknowledged gaps, goes beyond heuristic merging schemes. However, the paper overstates its accuracy improvements (gains are selective and most dramatic for weak learners) and Theorem 3.5's consistency guarantee relies on a scaling assumption (m ~ log n) that the framework cannot satisfy in sparse graphs. These issues are addressable in revision and do not invalidate the framework's core contribution, but they prevent a higher score.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>