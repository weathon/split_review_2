Now I have all the information I need. Let me compile the final consolidated review.

## Summary

This paper introduces XBIC, a score-based causal discovery method for discrete data that modulates BIC's complexity penalty using Shapley values from per-node XGBoost classifiers. The key idea is that asymmetric Shapley attributions between variable pairs provide directional signal for edge orientation within Markov equivalence classes. The paper evaluates on 10 benchmark networks (6–76 nodes) across 7 sample-size regimes (700 runs).

## Strengths

- **Creative and novel idea.** Using Shapley values from predictive models to modulate BIC's complexity penalty for edge orientation is genuinely novel. Prior work at the causality-XAI interface mostly goes in the opposite direction (Section 2.3); this paper inverts that relationship. This is the paper's strongest asset.

- **Broad empirical scope.** The evaluation covers 10 benchmark networks (6–76 nodes), 7 sample-size regimes, and 700 total runs — substantially more comprehensive than many causal discovery papers. The systematic variation of sample sizes from 0.125M² to 8M² gives a reasonable picture of where the method works and where it does not.

- **Clean default behavior.** XBIC reverts to standard BIC when SHAP(G) ≈ 0 (lines 113–114), gracefully degrading rather than failing catastrophically when the Shapley signal is absent.

## Weaknesses

### Major

- **Core directional signal unvalidated.** The paper asserts (line 127) that if |φ̄_{1→2}| ≫ |φ̄_{2→1}| then edge X₁→X₂ has "stronger directional support," but provides no argument or controlled experiment showing that Shapley-value asymmetry systematically encodes causal direction. Correlation is symmetric; the paper does not explain why asymmetries from tree-based classifiers should point toward true causal direction rather than reflecting arbitrary modeling choices (feature cardinality, split order, noise levels). Without isolated validation of this premise — e.g., testing whether the Shapley asymmetry itself points in the correct direction on known ground-truth networks — the reader cannot distinguish whether XBIC works because of its Shapley mechanism or despite it (e.g., because the added penalty flexibility happens to help).

- **PC comparison uses non-standard evaluation that inflates the headline 20.9% improvement.** PC returns a CPDAG with undirected edges by design. The paper (line 190) randomly orients these undirected edges before computing directed-edge metrics, which on average misorients half of them. Standard practice evaluates at the CPDAG level or on only the subset of edges PC actually orients. This makes the 20.9% F₁ gain — the paper's most prominent result — largely an artifact of evaluation choice. When only PC's actually-oriented edges are considered, the gap would likely shrink dramatically.

### Minor

- **Global penalty contradicts "edge-specific" framing.** The penalty modification (Equation 2) uses SHAP(G) = Σ|φ̄_{j→i}| summed over all edges, so the reduction is global. Edges with strong Shapley support reduce the penalty for all edges, including weak ones. This undermines the claimed "edge-specific" weighting (abstract, line 29) — an edge-specific formulation (per-node or per-edge) would better match the paper's framing.

- **GES comparison uses a filtered subset that limits interpretability.** The paper (line 278) retains only repetitions where GES completed within 7 days and acknowledges this as "favorable filtering for GES," reporting SHD improvements (6%–32%) only on this subset. Since GES may fail on the hardest cases, the reported advantage may not generalize.

- **Absolute gains over BIC are modest (0.04 absolute F₁, Table 4),** and the method underperforms BIC on several large-network/large-sample settings (Win95pts at 8M²: −0.09; Hepar2: ≈0.00 across all sizes). This degradation pattern on larger networks with more data is unexplained and concerning since directional evidence should be more reliable with more data.

- **Computational cost is substantial** (74.78s vs 0.39s for Asia, ~190×; Table 5), which contrasts with the "drop-in upgrade" framing (abstract, line 311). The paper acknowledges this limitation but does not measure parallel speedups.

### Trivial

- **Notation inconsistency:** X_{V_i} in Section 4.1 (line 194) vs X_{\setminus i} in the method (lines 19, 83, 117).

## Nice-to-Haves

- Validate the core directional signal in isolation: on each benchmark, compute |φ̄_{j→i}| and |φ̄_{i→j}| for all pairs and compare which direction the Shapley asymmetry favors against the ground truth. This would directly test the paper's central premise.
- Report absolute F₁ values (not just deltas) alongside Table 2 so that the delta values are interpretable.
- Report variance or confidence intervals for Table 2 entries.
- The consistency argument (lines 155–159) is informal — a formal treatment would strengthen the paper.

## Removed Points

- "Missing baselines (NOTEARS-discrete, DAG-GNN)" — removed: the paper's focus is score-based discrete discovery with standard baselines (BIC-HC, PC, GES); demanding methods outside this scope is not a valid weakness.
- "MMHC comparison" — removed because the paper explicitly scopes this out (line 190).
- "Explanation of Win95pts/Hepar2 failures needed" — moved to Nice-to-Haves; this is a suggestion, not a demonstrated error.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Fix the PC evaluation: report CPDAG-level SHD (which does not require random orientation) and report directed-edge metrics only on edges PC actually orients.
- Add a controlled experiment validating that Shapley asymmetry alone points toward true causal direction, independent of the BIC penalty modulation.
- Replace the global SHAP(G) aggregation with a per-edge or per-family penalty modifier that more faithfully reflects the paper's "edge-specific" framing.
- Report absolute F₁ values alongside the deltas in Table 2 and include variance estimates.

## Score and Decision

The paper introduces a genuinely novel and creative idea, backed by an impressively broad empirical evaluation. However, two major issues substantially weaken the evidence: (1) the core claim that Shapley asymmetry encodes causal direction is asserted without justification or isolated validation, and (2) the headline 20.9% improvement over PC is largely an artifact of a non-standard evaluation protocol (randomly orienting undirected CPDAG edges). The absolute gains over BIC are modest (0.04 F₁), and the method degrades on several important cases without explanation. The idea has clear potential, but the current evidence does not convincingly demonstrate that the Shapley mechanism is responsible for the reported improvements.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>