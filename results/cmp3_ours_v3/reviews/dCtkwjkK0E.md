## Summary

This paper proposes an active learning framework for flow matching models in continuous-condition shape design tasks. The authors attempt to derive query strategies from a theoretical analysis based on piecewise-linear (CPWL) neural networks, proposing Q_D (diversity-oriented), Q_A (accuracy-oriented), and a hybrid Q_hybrid strategy. The method is evaluated on a synthetic dataset and three real-world shape design datasets (airfoil, flying wing, starship-like). The problem direction is well-motivated — active learning for generative models is underexplored — but the paper has significant gaps in both its theoretical justification and experimental execution.

## Strengths

- **Well-motivated problem direction.** Active learning for generative models (specifically flow matching) is far less developed than active learning for discriminative models. The shape-design application with expensive numerical simulation is a genuine use case where reducing annotation cost matters. The paper identifies a real gap.

- **Attempt at theoretical grounding.** Most active learning methods are heuristic-driven. The paper tries to derive query strategies from an explicit model of how training data affects flow matching generation behavior. Even though the derivation has gaps, attempting this kind of analysis is the right instinct and distinguishes the paper from purely empirical work.

- **Ablation study on Q_D components (Fig 9).** The ablation tests the contribution of each of the three terms in Eq4, providing diagnostic insight into which factor drives diversity (distance(x, X) is most important, Δentropy is minor).

## Weaknesses

### Major

- **Theoretical derivation from CPWL to the query strategy has significant gaps.** The paper claims that the CPWL assumption implies Eq2 (interpolation at unseen conditions), but does not justify why the linear regions of the network should correspond to a triangulation whose vertices are the training labels. This is a strong assumption about the trained network's geometry that is neither justified theoretically nor verified experimentally. Additionally, the counting argument motivating Q_D (Section 2.3) is explicitly done only for 1D labels (c ∈ ℝ¹, line 79), yet the method is deployed on datasets with label dimensions 3 and 4 without showing how the argument extends. The paper does not claim a formal generalization — it presents Eq4 as motivated by the 1D insight — but the gap between a 1D counting argument and a general high-dimensional query strategy is large and unaddressed.

- **Experimental results lack statistical depth.** All results are shown as single trajectories over 5 active learning rounds with no error bars, confidence intervals, or indication of variance across runs (Fig 4, Fig 7, Fig 9). With only one run per method, it is impossible to assess whether the observed ranking of methods is reliable or due to stochastic variation. This is a significant weakness for an empirical paper making comparative claims.

- **Active learning loop is critically underspecified.** The paper states that the method "avoid[s] the need for repeated training of the flow matching model" (line 103), yet reports results over 5 iterations where "6% of the data is selected" each round (line 143). The paper never clarifies whether the flow matching model is retrained on the newly selected data between rounds:
  - If it IS retrained, the efficiency claim needs qualification (the flow matching model is still trained — the saving is in the query computation, using the cheaper RBF network instead).
  - If it is NOT retrained, then the model never learns from the newly selected data, making the comparison with baselines uninterpretable.
  
  This ambiguity undermines the entire experimental evaluation. An active learning paper must specify the training loop precisely.

### Minor

- **Reporting inconsistency in Figure 4.** The Figure 4 caption explicitly lists the methods shown as "Random, Coreset, Committe, Anchor, and Q_D methods" and states "Random achieves the highest accuracy." However, the body text (line 163) states: "In contrast, Q_A yields the highest accuracy." Q_A is not listed in the caption, so the reader cannot verify the claim from the figure being discussed. This needs resolution.

- **Q_D hyperparameters unreported.** The weighting coefficients α, β, γ in Eq4 are never specified. The paper does not explain how these are set, whether they are dataset-dependent, or how sensitive results are to their values. The Δentropy term requires clustering continuous labels with a threshold that is not stated.

- **Diversity-accuracy trade-off framing is partially overstated.** Q_D is constructed to minimize distance(y, Y) while Q_A maximizes it — these are definitionally opposing objectives. The paper presents the conflict between them as a discovered insight, but the trade-off is partly by construction. This does not invalidate the contribution, but the framing should be more measured.

### Trivial

None.

## Nice-to-Haves

- Report dataset sizes, initial labeled set size, and total annotation budget.
- Evaluate RBF label prediction quality and its impact on data selection.
- Compare the hybrid strategy's Pareto front against baselines (e.g., show that for any desired trade-off level, Q_hybrid achieves higher diversity at same accuracy or higher accuracy at same diversity than Random, Coreset, Committee, Anchor).
- Validate the CPWL interpolation assumption experimentally by testing whether generated samples at novel conditions actually follow Eq3.

## Removed Points

- **Q_A as an acknowledged adaptation of an existing method.** The paper openly states (line 99) that Q_A "performs the coresets algorithm in the label space." This is transparent, not a weakness. The paper's claimed novelty rests on Q_D and the hybrid combination. *Removed because the paper does not conceal this.*

- **Dated baselines.** The choice of baselines (Coreset, Committee, Random, Anchor) is reasonable for a pilot study in a new sub-area. Demanding newer AL baselines designed for discriminative models would not change the core comparison since the paper's methods are designed for a different setting (generative models, continuous conditions). *Removed per scope rules.*

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Specify the active learning loop precisely.** State clearly: (a) Is the flow matching model retrained between rounds? (b) If so, clarify that the efficiency advantage is confined to the query computation step (RBF network vs. full model training). (c) Report all experimental parameters including dataset sizes, initial labeled set size, and budget per round.

2. **Add statistical rigor.** Run each method with multiple seeds (at least 5) and report mean ± std for all metrics. Without this, the claimed rankings are not reliable.

3. **Report hyperparameter values.** State α, β, γ for Q_D and include a sensitivity analysis. Report the clustering threshold used for the Δentropy term.

4. **Resolve the Fig 4 caption/text discrepancy.** Clarify whether Q_A is present in the figure and what the actual accuracy ordering is.

5. **Strengthen theoretical grounding.** Either validate the CPWL interpolation assumption experimentally (test whether generated samples at novel conditions follow Eq3) or weaken the claims to match what is actually proven.

## Score and Decision

**Bracket (Round 1):** 3.0–4.5
**Narrowing (Round 2):** Papers on active learning with comparable experimental rigor — "Direct Acquisition Optimization" (3.67), "Does Deep Active Learning Work in the Wild?" (3.40), "Bayesian Active Learning by Distribution Disagreement" (3.40) — sit in the 3–4 range with more solid experimental methodology than the present paper. Papers above 5.0 ("Diffusion Active Learning" at 6.00, "Querying Easily Flip-flopped Samples" at 5.25) have stronger empirical validation (multiple runs, clear protocols) that this paper lacks.

**Calibration Anchors (all rounds):**
- YiyG1tHDxq.md — 3.40 — Bayesian AL for normalizing flows; similar topic, stronger experimental rigor
- GbXn0Dgf7f.md — 3.40 — Deep AL evaluation; solid negative-result methodology  
- NK09Bcvuxl.md — 3.67 — AL with influence functions; stronger theory and experiments
- WxLwXyBJLw.md — 3.25 — Flow matching one-step sampling; limited experiments
- SEvJfuCtPY.md — 3.00 — Phase-aware training; limited experiments beyond theory
- MM197t8WlM.md — 4.25 — Local flow matching; solid theory but mixed results
- 73Q9U0vcja.md — 6.00 — Diffusion AL for CT; clear protocol, multiple runs

The paper tackles a worthwhile problem and attempts a principled approach, but the combination of: (i) theoretically under-justified derivation of the core insight, (ii) absence of any statistical variance measures, and (iii) an underspecified active learning loop that makes the experimental results uninterpretable, places it below the bar for acceptance. The paper would need a substantially strengthened experimental protocol, resolution of the reporting inconsistencies, and either a validated theoretical claim or a clearer separation of the theory from the heuristic to be reconsidered.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>