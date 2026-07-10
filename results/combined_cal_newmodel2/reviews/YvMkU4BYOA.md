Now I have all the evidence I need. Let me write the final consolidated review.

## Summary

XBIC augments the BIC score for discrete Bayesian network structure learning by using Shapley values from per-node classifiers to soft-weight the complexity penalty. The idea is that asymmetric Shapley attributions (|φ̄₁→₂| vs |φ̄₂→₁|) provide directional evidence to help break ties within Markov-equivalence classes during hill-climbing search. The paper evaluates on 10 benchmark networks (6–76 nodes) across 7 sample-size regimes (700 runs), reporting 5.6% F₁ improvement over BIC-HC, 9.6% over GES, and 20.9% over PC.

## Strengths

- **Genuinely novel and well-motivated idea.** Using local feature attributions (Shapley values) from a separate prediction task to modulate BIC's complexity penalty for score-based discrete causal discovery is novel. The pipeline—train per-node classifiers → compute TreeSHAP values → soft-weight BIC penalty (Algorithm 1, Figure 1)—is clearly laid out. The contribution is distinct from prior work that injects causal knowledge *into* explanations (Frye et al. 2020, Heskes et al. 2020), as XBIC uses explanations to improve structure learning itself. [favorability=15.67]

- **Extensive evaluation.** 10 benchmark networks (6–76 nodes, Table 1), 7 sample-size regimes per network, 10 replicates each = 700 runs. Baselines include BIC-HC, PC, and GES. Statistical testing (adjusted Friedman + Wilcoxon) is appropriate. [favorability=14.16]

- **Full reproducibility commitment.** Code, data splits, and scripts are publicly released with clear documentation. [favorability=12.44]

- **Honest about limitations.** The paper explicitly discusses small-sample weakness (classifier confidence threshold), the precision–recall tradeoff with different w values (Figure 2), and runtime costs (Table 5), with specific and actionable limitations in the conclusions. [favorability=10.79]

## Weaknesses

### Fatal
None.

### Major

1. **PC comparison randomly orients undirected edges, inflating the headline 20.9% claim.** Line 190 states: *"For baselines that return a PDAG, we complete it to a DAG by randomly orienting undirected edges (while preserving acyclicity) before computing directed-edge metrics."* PC's CPDAG output explicitly encodes ambiguity—its undirected edges represent genuine uncertainty within the Markov equivalence class. Randomly orienting them before computing directed-edge F₁ systematically disadvantages PC and inflates any reported improvement. The "20.9% over PC" headline in the abstract and introduction depends directly on this choice. This is not a minor experimental detail; it affects the paper's central quantitative claim against a standard baseline. [favorability=2.05]

2. **No justification that Shapley asymmetry encodes causal direction.** The paper asserts at line 127: *"Intuitively, if |φ̄₁→₂| ≫ |φ̄₂→₁|, the edge X₁→X₂ has stronger directional support than X₂→X₁."* This connection between predictive importance (Shapley value magnitude) and causal direction is neither theoretically nor empirically justified. A predictor's feature importance can arise from reverse causation, confounding, or mediation just as easily as from the true causal direction. The paper frames XBIC as a *"principled enhancement"* (abstract), which overstates the theoretical grounding. The method works empirically on these benchmarks, but the mechanism by which Shapley asymmetry should correlate with causal direction is assumed rather than supported. [favorability=-1.13]

3. **Missing ablation against simpler association measures.** The expensive Shapley computation (74–1900 seconds vs 0.4–75 seconds for BIC, Table 5) is the main practical cost of XBIC. Without a comparison against a cheap association measure (e.g., absolute Cramér's V, conditional mutual information, or XGBoost feature importance) used in the same penalty-modulation framework, it is unclear whether the Shapley values provide unique value or whether any dependence-weighted penalty softening would yield similar results. This ablation is essential to isolate the contribution of the Shapley machinery. [favorability=3.65]

### Minor

1. **Confidence intervals missing from main aggregate tables.** Figure 2 shows CIs for 3 networks, but Tables 2 and 4 (the headline 700-run aggregates) report only point estimates without standard deviations or confidence intervals. This makes it difficult to assess the variability and reliability of the reported improvements. [favorability=5.80]

2. **GES comparison affected by selection bias.** The paper transparently states (Section 4.5) that GES exceeded the 7-day limit on many settings and reports comparisons only on the subset where GES completed. This subset is skewed toward smaller/sparser networks and larger samples. The 9.6% improvement aggregates over this non-random subset, and the paper does not bound the potential bias. [favorability=1.42]

3. **Consistency argument is incomplete.** The brief remark (lines 155–159) argues that because the penalty still grows as O(log N), standard BIC consistency is preserved. However, the penalty includes a graph-dependent factor c(G) in the denominator that modifies the finite-sample penalty ordering. Establishing that the true graph has strictly larger XBIC than alternatives under standard regularity conditions requires more analysis than the brief note provides. [favorability=5.60]

4. **Undiscussed gap between attribution signal and score.** Shapley values are computed from models trained on *all* other variables X\_{∖i} (Algorithm 1, line 2), not candidate parent sets. BIC's likelihood term uses P(X_i | PA_i). The relationship between the full-conditional attribution signal and the parent-set-based likelihood is not discussed. [favorability=6.79]

5. **Win95pts negative results at large sample sizes not discussed.** Table 2 shows XBIC (w=2) underperforming BIC by -0.09 F₁ at 8M² and PC by -0.15 for Win95pts, contrasting with the general trend. This is not discussed in the text. [favorability=5.00]

### Trivial
None.

## Nice-to-Haves

- **Provide empirical validation of the Shapley-causal direction assumption.** On the benchmark networks with known ground truth, compute the fraction of edges where the larger |φ̄| points in the correct direction, broken down by edge type (collider, mediator, confounder). This would directly test whether the core assumption holds on these benchmarks.
- **Explore the penalty-modulation design space more thoroughly.** The current global denominator exp(w·SHAP(G)) could be replaced with per-edge penalty weights; a comparison would clarify whether the global structure is a design choice or a limitation.
- **Include CPDAG-level metrics alongside directed-edge metrics.** Reporting skeleton F₁ and oriented-edge F₁ separately on the subgraph PC can orient would provide a cleaner comparison with constraint-based methods.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"95% confidence intervals across all runs referenced in the abstract."** — Factually incorrect; the abstract does not mention confidence intervals. (The underlying concern that CI are missing from Tables 2/4 is valid and kept as a minor weakness.)
- **"Penalty modulation is global not edge-specific, inconsistent with prose."** — SHAP(G) is a sum over edges; each edge's Shapley value differentiates its marginal contribution in the hill-climbing context. The paper's descriptions are consistent with how the formula behaves during search. Removed as overreading.
- **"Runtime cost is downplayed."** — The paper provides full runtime data (Table 5), explicitly discusses the cost, and notes parallelization potential. This is not a hidden weakness.
- **"w sweep over {1,2,3} is narrow."** — This is a reasonable sensitivity range, with w=0 recovering BIC as the natural baseline.

## Novel Insights

None beyond the paper's own contributions. The core insight—using predictive-model feature attributions to modulate a score-based causal discovery objective—is well-communicated by the paper itself. The reviews do not surface any deeper analytical insight beyond what the paper already states.

## Suggestions

1. **Fix the PC comparison.** Either (a) evaluate on CPDAG-level metrics (report skeleton recovery and oriented-subgraph recovery separately, so PC is not penalized for being correctly uncertain), or (b) use an oracle orientation strategy for PC's undirected edges (e.g., orient using the ground truth to establish an upper bound, and random orientation to establish a lower bound).
2. **Add a Shapley ablation.** Replace the Shapley-based weighting with a cheap association measure (e.g., absolute Cramér's V or XGBoost feature importance from the same models) and compare. If the improvement persists, the contribution is the penalty-softening idea; if it vanishes, the Shapley computation is uniquely valuable.
3. **Provide empirical evidence for the core assumption.** On the benchmark networks, compute the accuracy with which |φ̄ⱼ→ᵢ| > |φ̄ᵢ→ⱼ| predicts the true direction Xⱼ→Xᵢ.
4. **Add variability estimates to Tables 2 and 4.**

## Score and Decision

### Calibration Anchors

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| JzFLBOFMZ2 | Causal Structure Learning Supervised by LLM | 3.20 | 1 | Yes | Core assumption (LLM knows causality) even shakier; weaker presentation; XBIC is stronger |
| eqQFBnjjPP | ExDBN: Exact learning of Dynamic Bayesian Networks | 4.00 | 1 | Yes | Marginal novelty, thin comparisons, confusing presentation; XBIC has clearer novelty and broader eval |
| i5JfdnCob7 | Optimal Kernel Choice for Score-based Causal Discovery | 4.40 | 1 | Yes | Incremental over Huang et al. 2018; XBIC has more distinct novelty |
| UAkVjK00Wv | Auto-Ensemble Structure Learning | 4.75 | 2 | Yes | More severe negative items (-4.16, -2.14) on innovation; XBIC has stronger novel contribution |
| 3n6DYH3cIP | Extendable and Iterative Structure Learning for BNs | 5.60 | 2 | Yes | Comparable strength profile; worst item -1.36 vs XBIC's -1.13; accepted |
| KWO8LSUC5W | Constraint-Free Structure Learning (COSMO) | 5.60 | 2 | Yes | Has items as negative as -4.85 but accepted; XBIC's worst item is -1.13 but has more total weaknesses |
| 8muemqlnG3 | Causal Discovery via Bayesian Optimization (DrBO) | 6.50 | 1 | Yes | Stronger profile: no negative favorability weaknesses; XBIC not at this level |
| eeJz7eDWKO | Meta-Learning Approach to Bayesian Causal Discovery | 6.00 | 2 | No | Higher-scoring paper; not itemized |

**Round 1 bracket:** Based on initial calibration, the paper sits between the 3.20–4.75 band (where papers have severe conceptual or novelty issues) and the 5.60–6.50 band (where papers have clean evaluations with minor weaknesses). The paper's strongest items (novelty favorability 15.67, evaluation favorability 14.16) are comparable to 5.60-level papers, but its weakest items (Shapley-causal justification at -1.13, PC comparison at 2.05) are more negative than typical 5.60 papers.

**Round 2 narrowing:** Comparing itemized ratings against 3n6DYH3cIP (5.60) and KWO8LSUC5W (5.60), the XBIC paper shares the pattern of strong strengths with a few negative or near-negative weaknesses. However, XBIC's negative items are about evaluation methodology and conceptual grounding (fixable in revision), while the negative items in the 5.60 anchors are about novelty/scope. The 4.75 anchor (UAkVjK00Wv) has innovation criticisms far more severe (-4.16). XBIC sits between these bands.

**Final score grounded in favorability comparison:** XBIC has two genuinely novel contributions (the Shapley-scoring idea and an extensive 700-run evaluation) that push it above papers at 4.75 and below. But the unresolved PC evaluation issue (which directly impacts a headline claim) and the conceptual gap in the Shapley-causal connection prevent it from reaching the clean 5.60+ level. The paper would need to fix the PC comparison and add the Shapley-causal analysis to be a clear accept.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>