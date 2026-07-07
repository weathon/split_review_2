## Summary

This paper identifies and formalizes the problem of **post-treatment selection** in interventional causal discovery — a setting where samples are selectively included after interventions (e.g., quality control in gene perturbation studies). The authors show that post-treatment selection produces the same statistical patterns (variant marginal, invariant conditional) as true causal relations, making them indistinguishable under existing frameworks. They introduce a new graphical formulation (augmented DAG with selection), define a finer equivalence class (ℱℐ-Markov equivalence) and a corresponding graph (ℱ-PAG), and propose ℱ-FCI, a sound and complete algorithm for recovering this class. The method exploits Type I inducing nodes — intermediate variables with their own intervention data — to disambiguate causation from selection.

## Strengths

- **The non-identifiability argument is clearly articulated.** The paper correctly identifies that post-treatment selection produces the same pattern (variant marginal, invariant conditional given the putative cause) as a true causal relation, and that existing interventional equivalence classes therefore conflate the two. This is crisply illustrated in Figures 1 and 2, making the problem tangible.

- **The theoretical framing is rigorous.** The paper situates its contribution within the established augmented DAG/MAG/PAG hierarchy, provides formal definitions (augmented DAG with selection, ℱℐ-Markov equivalence, ℱ-PAG), and states soundness and completeness theorems (Theorem 3 and Theorem 4). The characterization of CI patterns in Figure 4 and the table mapping CI tuples to structures is the intellectual core of the paper and is well-conceived.

- **The paper identifies a genuine, practically relevant problem** — post-treatment selection in interventional causal discovery — that has been overlooked. The motivating examples (gene perturbation quality control, clinical trial per-protocol analysis) are concrete and demonstrate why this matters beyond a purely theoretical exercise.

## Weaknesses

### Major

- **The method's distinguishing power depends on Type I inducing nodes with their own intervention data, and the practical restrictiveness of this condition is under-explored.** The paper acknowledges this limitation in the conclusion ("depends critically on the presence of Type I inducing nodes") but does not characterize how restrictive it is in practice. In the simplest motivating scenario — a pair of variables with post-treatment selection and no suitable third variable that (a) lies on the inducing path and (b) has its own intervention data — the method provides no resolving power over existing frameworks. The paper's framing in the abstract and introduction says the method allows "going beyond traditional equivalence classes toward the underlying true causal structure" and distinguishes "causal relations from selection patterns" without qualifying that this distinguishability is conditional on the availability of auxiliary interventions on Type I inducing nodes. A formal characterization of when the ℱℐ-Markov equivalence class strictly refines versus collapses to the standard interventional equivalence class would significantly strengthen the paper.

- **The experimental evaluation does not provide strong evidence for the method's practical value.** The claimed improvement ("average precision of over 5% in most configurations") is modest for a method claiming a fundamentally new capability, and it is unclear whether this is 5 percentage points or 5% relative. The real-world evaluation on the Norman dataset is a single paragraph in the main text with all quantitative detail deferred to the appendix — no numerical results, metrics, or baseline comparisons are provided in the main paper. An ablation experiment comparing ℱ-FCI against ℱ-FCI without the Type I node refinement (Step 2.3) would isolate what the key innovation contributes, but no such ablation is reported.

### Minor

- **The completeness theorem (Theorem 4) has an imprecise scope.** It states that each substructure "can be identified by different types of CI patterns," which essentially restates that what the algorithm identifies is identifiable. The more meaningful completeness question — whether the ℱℐ-Markov equivalence class is the finest partition of graphs given the data type (i.e., whether any two graphs in the same class are distributionally equivalent) — is not formally proven. The theorem also does not address the Type I inducing node limitation: it is unclear whether the algorithm is "complete" for pairs of variables with only Type II inducing nodes on their paths.

- **Step 2.3 of the algorithm appears to assume that interventions are available on all Type I inducing nodes.** The algorithm checks CI conditions involving ψₙ for each Type I inducing node Xₙ, but the input only specifies intervention targets ℐ. If a Type I inducing node on an inducing path has not been intervened on, ψₙ does not exist, and the refinement step cannot execute. The paper does not discuss how the algorithm handles this case.

### Trivial

None.

## Nice-to-Haves

- An ablation experiment comparing ℱ-FCI with and without the Type I node refinement (Step 2.3) would help quantify the contribution of the paper's key innovation.
- A discussion of suitable CI tests for finite-sample settings (beyond oracle tests) would be helpful for practitioners.
- A brief discussion of runtime/scaling, beyond the appendix figure.

## Removed Points

These points from the input review were flagged for removal; treat them with caution:

1. **"Algorithm pseudocode has all six branches with identical CIs condition"** — REMOVED because this is a PDF parsing artifact; the original submission does not have this issue (per Hard Rules: formatting artifacts are not author errors).

2. **"No discussion of CI test selection"** — REMOVED as standard in this literature (oracle CI tests are the norm for theoretical claims). Moved to Nice-to-Haves.

3. **"No discussion of computational complexity"** — REMOVED because the paper references a scalability figure in Appendix D and this is not a standard requirement for formal identifiability papers. Moved to Nice-to-Haves.

4. **"Comparison is stacked by design"** — STRIPPED of accusatory framing. The paper compares against relevant state-of-the-art methods. Showing that methods not designed for post-treatment selection perform worse is a meaningful validation. The useful part (need for ablation) is merged into the Major weakness.

5. **"Section 2 preliminaries are too long"** — REMOVED as a presentation preference.

6. **"Definition 5 lists ten edges but says eight types"** — REMOVED as a formatting artifact (○---○ appears three times due to parsing duplication).

7. **Strength "The problem is genuine and important"** — REMOVED per filtering rules: strengths about whether a problem is important are generic unless paired with specific content about what the paper contributes. The concrete motivating examples are already noted in the second strength.

## Novel Insights

The sharpest insight across the reviews is that the paper's core limitation is structural: the Type I inducing node requirement means the method cannot resolve the simplest post-treatment selection scenarios (a pair of variables with no third intervention-accessible node on the inducing path). This is a genuine boundary on what the ℱℐ-Markov equivalence class can distinguish. The paper acknowledges this but does not formally characterize *when* the class collapses to standard interventional equivalence — arguably the most important open question for a reader considering whether to apply the method. The step from "we found a new phenomenon" to "here is a complete characterization of its identifiability boundary" is not fully bridged.

## Suggestions

1. Formally characterize the conditions under which the ℱℐ-Markov equivalence class strictly refines the standard interventional equivalence class versus collapses to it.
2. Add an ablation comparing ℱ-FCI with and without the Type I node refinement (Step 2.3).
3. Provide concrete numerical metrics (precision, recall, F1) for the Norman dataset experiment in the main text.
4. Clarify in the abstract and introduction that distinguishing causation from post-treatment selection is conditional on having Type I inducing nodes with intervention data.

## Score and Decision

**Calibration anchors used (6 total):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| xByvdb3DCm.md — "When Selection meets Intervention: Additional Complexities in Causal Discovery" | 8.00 | R1 | Yes | Very similar topic (selection in interventional discovery), but this anchor has stronger experiments, cleaner presentation, and no structural limitation comparable to the Type I node dependency. |
| G5KbDVAlI6.md — "Gene Regulatory Network Inference in the Presence of Selection Bias and Latent Confounders" | 4.00 | R1 | Yes | Similar domain (selection + latents in GRN), but much weaker theoretical framework and severe scalability concerns (5 genes tested). Our paper has superior theory but shares the thin real-world validation. |
| u63OVngeSp.md — "Deriving Causal Order from Single-Variable Interventions" | 7.00 | R1 | Yes | Strong interventional causal discovery paper with good theory and experiments. More restrictive assumptions (all variables intervened on). |
| ZXs3pkmrRG.md — "Test-Time Learning of Causal Structure from Interventional Data" | 5.50 | R2 | Yes | Different approach (learning-based), not directly comparable on selection bias. |
| cbFqqtJGtA.md — "Predicting perturbation targets with causal differential networks" | 4.25 | R1/R2 | No | Tangential topic (perturbation target prediction). |
| SKulT2VX9p.md — "Interventional Fairness on Partially Known Causal Graphs" | 6.67 | R1/R2 | No | Uses causal graphs but different application (fairness). |

**Round 1 bracket:** ~4.0 to ~6.5, based on comparison with the 8.00 anchor (stronger execution on similar topic) and the 4.00 anchor (weaker theory, similar validation gaps).

**Narrowing to final score:** The paper's weighted items show strong positive weights for theory (+5.84, +4.40) balanced against a heavy negative on experiments (-6.89). Compared to the 8.00 anchor (where the heaviest negative item was -3.27, a completeness concern), our paper's -6.89 experimental deficit is substantially worse — placing it well below 8.00. Compared to the 4.00 anchor (negatives as low as -7.62 and -8.21 for vague theorems and tiny experiments), our paper has stronger theory (+5.84 vs that anchor's +4.89 max theoretical strength) and better experiments (10–25 vs 5 variables), placing it above 4.00. The net weighted score (-1.19, slightly negative) combined with these anchor comparisons supports a score of 5.0.

**Final assessment:** The paper makes a genuine theoretical contribution — identifying post-treatment selection as a distinct source of non-identifiability and providing a formal framework to address it. However, the Type I node dependency narrows the method's scope in a way that is under-characterized, the experimental validation is modest (5% improvement, thin real-world results), and the framing somewhat overstates what the method achieves. The paper has solid theoretical foundations but needs stronger empirical evidence and a more precise characterization of its limits to be fully convincing.

### MY FINAL SCORE: <score>5.0</score>
### MY FINAL DECISION: <decision>Reject</decision>