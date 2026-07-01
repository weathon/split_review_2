Now let me re-read key sections more carefully to verify specific claims.Now I have read the full paper thoroughly. Let me draft my consolidated review.Now let me run Round 1 calibration search — bracketing across score bands.Let me read the most relevant anchor papers for calibration, especially the one on selection bias in interventional studies which seems very closely related.Now I have strong calibration anchors. Let me compile the final review.

## Summary
This paper addresses post-treatment selection bias in interventional causal discovery—a setting where samples are selectively retained after interventions (e.g., quality control in gene perturbation studies). The authors demonstrate that existing interventional frameworks conflate selection-induced and causal dependencies, propose a new formulation via augmented DAGs with explicit selection modeling, define $\mathcal{FI}$-Markov equivalence and a richer graphical representation ($\mathcal{F}$-PAG), and develop a provably sound and complete algorithm ($\mathcal{F}$-FCI) for structure recovery from both observational and interventional data.

## Strengths

- **Concrete identifiability gap demonstrated (§2.2, Figure 1).** The paper clearly shows that post-treatment selection produces the same invariance pattern as causation—variant $p(\text{effect})$ and invariant $p(\text{effect}|\text{cause})$ after intervention—making existing frameworks unable to distinguish Figures 1(a) from 1(b). This is a specific, well-formalized gap, not a vague complaint about existing methods.

- **Clean structural insight formalized via CI pattern taxonomy (§3.2, Figure 4).** The key observation—that selection structures yield *symmetric* CI patterns (both endpoints exhibit invariance conditioned on each other) while causal relations yield *asymmetric* ones—is mapped into a six-case taxonomy (Figure 4(i)) connecting CI signatures to structural classes. This is the conceptual engine of the paper and is both elegant and well-formalized.

- **Both soundness and completeness proven (Theorems 3–4).** Unlike the closely related CDIS framework (Dai et al., 2025), which proves only soundness, this paper establishes completeness for oracle CI tests, providing stronger theoretical guarantees for the $\mathcal{FI}$-Markov equivalence class.

- **$\mathcal{F}$-PAG is a strictly more informative representation than PAG (Figure 5, Definition 5).** The new edge marks (square $\square$, filled/open triangle $\blacktriangle$/$\Delta$) distinguish cases that standard PAG collapses into a single representation, enabling finer-grained structural conclusions from the learned graph.

- **Systematic theoretical progression.** The development from augmented DAGs (Definition 1) through Markov properties (Theorem 1, Lemma 1) to graphical equivalence criteria (Lemmas 2–4, Theorem 2) is well-organized, with each component building naturally on the previous one.

## Weaknesses

### Fatal
None

### Major
1. **Step 2.3's practical scope is unquantified.** The paper's distinctive claim—going beyond traditional equivalence classes to distinguish Figures 4(a) vs. 4(b) and 4(e) vs. 4(f)—depends entirely on Step 2.3, which requires hard interventions on Type I inducing nodes along inducing paths. The authors acknowledge this dependency in §6 ("The identification of direct causal links and selection structures depends critically on the presence of Type I inducing nodes"), but the experiments never report how often Step 2.3 fires or what fraction of the improvement it accounts for. Without this ablation, the reader cannot assess whether the gains come from the selection-aware formulation (Steps 2.1–2.2) or from the novel refinement step that constitutes the paper's unique theoretical advance.

2. **Real-world evaluation lacks quantitative rigor.** Section 5.2 is a single paragraph: it describes applying $\mathcal{F}$-FCI to the Norman dataset and evaluating via Enrichr enrichment libraries, with details deferred to Appendix D.3. There is no quantitative comparison with baselines on the real data, no precision/recall numbers, and the evaluation criterion (enrichment-based prior knowledge) is indirect. For a paper that motivates its contribution through biological applications (gene perturbation quality control), this is a notable gap in the main text evidence.

### Minor
1. **No ablation without selection variables.** All synthetic experiments include 2–3 selection variables (§5.1). An experiment where selection is absent would verify that $\mathcal{F}$-FCI does not degrade when its modeling advantage is irrelevant—an important robustness check given that a practitioner may not know whether post-treatment selection is present.

2. **The assumption "selection works on at least two observed variables" (end of §2.1) is stated without justification.** The paper does not clarify whether this is required for identifiability or motivated by the application domain, nor what happens to the algorithm when a selection variable has only one observed parent.

3. **Computational complexity is not discussed in the main text.** The conditioning-set search in Step 2.1 iterates over subsets of nodes on all paths between intervention targets, which could be exponential for dense graphs. A brief complexity statement would help readers assess scalability, even though scalability results (Figure 11) are mentioned as being in the appendix.

### Trivial
None

## Nice-to-Haves
- Sensitivity analysis varying selection strength, number of selection variables, and functional form of the selection mechanism to map out when $\mathcal{F}$-FCI's advantage is decisive vs. marginal.
- Analysis of finite-sample error propagation through algorithmic steps, particularly Step 2.3 which relies on a single CI test ($\psi_n \perp X_{\mathcal{I}^{(i)}}$) for a consequential structural determination.
- Testing robustness to more complex, non-additive selection mechanisms beyond the threshold-on-sum form ($\sum f_s(X_i)$ within an interval) used in simulations.

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **Algorithm Step 2.2's CI conditions appear garbled** (all six cases show $(⊥,⊥,⊥,⊥)$ in lines 216–226). REMOVED: This is a PDF parsing artifact. Figure 4's table shows the distinct patterns, and the original submission does not have this issue.
- **Oracle CI test limitation** (Theorems 3–4 hold only for oracle tests). REMOVED: This is standard in constraint-based causal discovery—FCI itself has the same property. Not a methodology-specific weakness but a field-wide characteristic.
- **Baselines not designed for post-treatment selection.** REMOVED as standalone weakness: The paper's contribution IS about handling post-treatment selection, so the natural evaluation tests selection-aware vs. selection-unaware methods on data with selection. The specific ask for a no-selection ablation is retained as Minor weakness 1.
- **Abstract overstates by claiming the method goes "toward the underlying true causal structure."** REMOVED: The body text (§3.3) precisely defines recovery up to $\mathcal{FI}$-Markov equivalence, and the abstract uses the hedged word "toward," which is appropriate.
- **Faithfulness violation discussion missing.** REMOVED: Faithfulness is explicitly assumed (§4, line 247: "We assume faithfulness"), and discussing violations is standard future work for constraint-based methods, not a specific weakness.

## Novel Insights
The paper's central novel insight is that post-treatment selection and causation, while producing identical marginal/conditional invariance patterns under intervention, generate structurally distinguishable CI signatures when both directions of intervention are considered—selection is symmetric while causation is asymmetric. The further observation that hard interventions on Type I inducing nodes can disambiguate structures sharing identical endpoint CI patterns (e.g., direct vs. indirect causal links mediated through a selection path) represents a genuine advance in the identifiability theory of interventional causal discovery, extending beyond what the closely related CDIS framework achieves.

## Suggestions
1. **Add a Step 2.3 ablation:** Report how often Step 2.3 fires across simulation settings and what fraction of the performance improvement it accounts for. This directly substantiates the paper's unique selling point.
2. **Strengthen §5.2:** Provide quantitative precision/recall against a curated ground-truth gene regulation database and include baseline comparisons on the Norman dataset in the main text.
3. **State computational complexity** of Steps 2.1 and 2.3 in the main text, even briefly.
4. **Add a no-selection experiment** to demonstrate graceful degradation when the selection-modeling advantage is unnecessary.
5. **Justify the ≥2 parents assumption** on selection variables—clarify identifiability vs. domain motivation.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| When Selection meets Intervention (CDIS) | xByvdb3DCm | 8.0 | 1 | Most closely related: addresses pre-treatment selection bias; proves only soundness (not completeness); denser notation but stronger empirical evaluation with 3 datasets. The paper under review extends to post-treatment selection and proves completeness, but has weaker empirical evidence. |
| Gene Regulatory Network Inference (GISL) | G5KbDVAlI6 | 4.0 | 1 | Related topic (GRNI with selection bias) but much weaker: scales only to 5–9 nodes, limited baselines, incomplete evaluation. The paper under review is substantially stronger in theory and evaluation. |
| Deriving Causal Order from Interventions | u63OVngeSp | 7.0 | 1 | Related interventional causal discovery; introduces interventional faithfulness. Similar tier of theoretical contribution but different problem scope. Comparable empirical evaluation quality. |
| Efficient Causal Discovery with Latent Variables | BZYIEw4mcY | 6.0 | 1 | Addresses latent variables with complex relations; polynomial-time algorithm. Less novel problem formulation than the paper under review but broader empirical validation. |
| Interventional Fairness on Partially Known Causal Graphs | SKulT2VX9p | 6.67 | 1 | Different application (fairness) but similar causal graph learning methodology. Less directly comparable. |
| Recovery of Causal Graph via Homologous Surrogates | fGhr39bqZa | 6.0 | 1 | Addresses latent variables without pure children; novel concept but different setting. |
| Causal Graph Learning via Distributional Invariance | Lxst78Rrwj | 5.0 | 1 | Observational-only invariance framework; weaker theoretical contributions than the paper under review. |
| Predicting perturbation targets with causal differential networks | cbFqqtJGtA | 4.25 | 1 | Related perturbation setting but focuses on target identification rather than full structure learning; weaker contributions. |
| Turning Challenges into Opportunities (CRL) | q07DDpu8Xb | 5.25 | 1 | Causal representation learning under distribution shifts; different subfield, less directly comparable. |
| Best of both worlds: causal structure for prediction | AvXrppAS2o | 3.0 | 1 | Weak paper combining causal discovery with prediction; not comparable in theoretical depth. |
| DFITE (ITE via diffusion) | 4u0ruVk749 | 3.0 | 1 | Treatment effect estimation, different problem; substantially weaker contributions. |
| Sparse Causal Model | fSxiromxAq | 3.0 | 1 | Sparse causal discovery on real data; limited novelty compared to paper under review. |
| Identifying Representations for Intervention Extrapolation | 3cuJwmPxXj | 8.0 | 1 | Different problem (intervention extrapolation in CRL) but similar caliber of theoretical contribution. |
| Root Cause Analysis via Granger Causality | k38Th3x4d9 | 8.0 | 1 | Time series causal discovery; different domain, not directly comparable. |
| Cross-Entropy for Inverting DGP | hrqNOxpItr | 8.0 | 1 | Representation learning theory; different subfield entirely. |

**Round 1 bracket: 6.0 to 8.0**

The paper under review is clearly above the 4.0–5.0 band (stronger theory and more novel problem than G5KbDVAlI6 at 4.0 and Lxst78Rrwj at 5.0). It shares the same problem space as xByvdb3DCm (8.0) but with weaker empirical evidence and a key practical limitation (Step 2.3). The theoretical contribution (completeness, F-PAG, CI pattern taxonomy) is comparable to or slightly stronger than the 7.0 anchor (u63OVngeSp).

**Narrowing analysis:** Compared to the most directly relevant anchor (xByvdb3DCm, 8.0—which IS the CDIS paper cited as a baseline), the paper under review: (a) extends from pre- to post-treatment selection, a distinct and complementary contribution; (b) proves completeness where CDIS only proves soundness; (c) introduces a richer F-PAG representation. However: (d) its real-world evaluation is thinner; (e) it does not demonstrate how often its unique mechanism (Step 2.3) fires; (f) the ~5% precision improvement is modest. The theoretical advance justifies a score near the 7.0 anchor, but the empirical gaps prevent reaching the 8.0 level. The combination of a genuine novel problem, clean theory with completeness, but bounded empirical validation places this paper solidly in the 6.5–7.0 range.

**Final score: 7.0**

This paper makes a genuine and well-formalized theoretical contribution to an important subproblem in causal discovery. The $\mathcal{FI}$-Markov equivalence class, $\mathcal{F}$-PAG representation, and completeness guarantee represent meaningful advances over the closely related CDIS framework. The major weaknesses—the unquantified practical scope of Step 2.3 and thin real-world evaluation—are evidential gaps rather than structural flaws: they limit confidence in the practical impact but do not undermine the theoretical contribution. The paper is above the acceptance threshold but would benefit significantly from the suggested ablations and empirical strengthening.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>