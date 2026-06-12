Now I have sufficient calibration data. Let me finalize the review.

**Calibration Summary:**

**Round 1 bracket:** 4.5–5.5

**Round 2 narrowing:** 4.5–5.5 confirmed. 

Key comparisons:
- "The best of both worlds" (3.0, rejected) — XBIC is clearly superior: more novel, better evaluation, more rigorous
- "Optimal Kernel Choice for Score-based Causal Discovery" (4.4, rejected) — XBIC has more extensive evaluation and more creative idea
- "DAG-SHAP" (5.0, rejected) — Most comparable: both use SHAP creatively in causal tasks, both lack theoretical justification for core claims, XBIC has more extensive evaluation
- "Exact Distributed BN Learning" (5.25, rejected) — XBIC has better empirical evaluation but less theoretical contribution
- "Extendable BN Structure Learning" (5.6, accepted) — XBIC is comparable in evaluation but has a more serious methodological issue (CPDAG evaluation)
- "Meta-Learning Bayesian Causal Discovery" (6.0, accepted) — Cleaner methodology, better theoretical framing; XBIC is below this
- "Causal Discovery via Bayesian Optimization" (6.5, accepted) — Stronger results, more principled; XBIC is below this

**Final score: 5.0** — The paper has a genuinely novel idea and very extensive evaluation, but the headline claims are substantially inflated by the CPDAG evaluation artifact, the core mechanism (SHAP asymmetry → causal direction) is unexplained, and the real improvement over the fair baseline (BIC-HC) is modest (+0.04 absolute F1) at 50–200× computational cost.

---

## Summary

The paper introduces XBIC, a modification to BIC for discrete Bayesian network structure learning that soft-weights BIC's complexity penalty using edge-specific Shapley values from per-node XGBoost classifiers. Evaluated on 10 benchmark networks across 7 sample-size regimes (700 runs), it claims +5.6% F1 over BIC-HC, +20.9% over PC, and +9.6% over GES.

## Strengths

- **Novel reversal of the causality-XAI pipeline.** XBIC uses feature attributions to improve structure learning when the graph is unknown, rather than the other way around (Section 2.2–2.3, Eq. 2). This is a genuinely creative idea.
- **Drop-in compatibility.** XBIC modifies only the score function; the search algorithm remains standard hill-climbing with add/delete/reverse moves (Algorithm 2). Adoption cost is minimal.
- **Extensive evaluation with proper statistical testing.** 10 discrete BNs (6–76 nodes), 7 sample sizes, 700 total runs, tested with adjusted Friedman + Wilcoxon signed-rank post-hoc tests (Section 4.3, Table 4).
- **Honest handling of GES limitations.** GES exceeded 7-day limits; authors compare head-to-head on the same completed repetitions (Section 4.5), avoiding cherry-picking.
- **Robustness to confidence threshold.** Varying τ from 0.7 to 0.95 changes F1 by <1% (Section 4.1), showing the method is not brittle to this design choice.

## Weaknesses

### Fatal
None

### Major

1. **Unfair evaluation of CPDAG-producing baselines (PC, GES).** The paper states: "For baselines that return a PDAG, we complete it to a DAG by randomly orienting undirected edges (while preserving acyclicity) before computing directed-edge metrics" (line 190). This systematically penalizes PC and GES: edges these algorithms correctly identify as non-orientable from the data get ~50% precision by random assignment. The standard practice is CPDAG-aware metrics (skeleton accuracy, orientation accuracy on orientable edges). The headline claims of +20.9% over PC and +9.6% over GES are substantially inflated by this artifact. The only fair comparison (XBIC vs. BIC-HC, both DAG-producing) yields +0.04 absolute F1 improvement.

2. **No justification for why SHAP asymmetry prefers causal direction.** The paper's central mechanism — that among Markov-equivalent DAGs, the true DAG will have higher aggregate |SHAP| on its edges — is the load-bearing claim but is never justified. Line 127 asserts "if |φ̄_{1→2}| ≫ |φ̄_{2→1}|, the edge X₁ → X₂ has stronger directional support," but no theoretical analysis, illustrative example, or empirical decomposition is provided showing this holds. The consistency remark (lines 155–159) addresses penalty growth rate, not the validity of the SHAP signal itself. The paper acknowledges this gap in its Limitations section ("formal analysis of the weighting mechanism... is an important direction"), but without even a toy example or empirical analysis of SHAP asymmetry on the benchmarks, the reader cannot assess when or why the method works.

### Minor

3. **Hyperparameter w selected on test set.** The headline result ("5.6% over BIC") uses w=2, chosen from {1, 2, 3} by inspecting performance across the benchmark suite (Table 4). w=1 gives 5.1% and w=3 gives 2.5%, so the practical impact is limited, but the reporting convention is not principled.

4. **Inconsistent gains across networks.** Table 2 shows XBIC vs. BIC improvements near zero for Asia and Survey across all sample sizes, while other networks (Insurance, Hailfinder) show consistent positive gains. The paper does not analyze which network properties predict XBIC's effectiveness, which would help practitioners assess when to apply the method.

5. **No budget-matched comparison.** XBIC is 50–200× slower than BIC-HC (Table 5). The paper does not compare to BIC-HC with the same wall-clock budget (e.g., multiple random restarts, tabu search). Without this, it is unclear whether XBIC's gains come from better scoring or simply more thorough search.

### Trivial
None

## Nice-to-Haves

- An empirical analysis of |φ̄_{j→i}| vs. |φ̄_{i→j}| for true edges vs. reversed edges on 1–2 benchmark networks — this would provide the strongest evidence for the method's core mechanism.
- Ablation of SHAP vs. simpler attribution measures (mutual information, correlation weights) to justify the computational cost of TreeSHAP.
- A 3–5 node toy BN demonstrating that SHAP asymmetry aligns with causal direction.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **"Consistency remark is hand-wavy"**: The remark (lines 155–159) is mathematically correct for fixed w and bounded SHAP(G). While the asymptotic behavior of SHAP(G) itself is not analyzed, this is acknowledged in the Limitations section and does not invalidate the core claims.
- **Missing related works**: Not verifiable from external sources; not included.

## Novel Insights

The paper's genuinely novel contribution is reversing the typical causality-XAI pipeline: rather than using known causal structure to constrain explanations (Frye et al., 2020; Heskes et al., 2020; Wang et al., 2021), XBIC uses explanations to improve structure learning when the graph is unknown. This is a creative idea with practical appeal, positioned clearly in Section 2.3.

## Suggestions

1. **Add CPDAG-aware metrics** for PC and GES comparisons, or replace them with DAG-producing baselines (e.g., MMHC, BIC-HC with random restarts). This would make headline claims credible.
2. **Analyze SHAP asymmetry on benchmarks.** Report |φ̄_{j→i}| vs. |φ̄_{i→j}| for true edges vs. reversed/fake edges on 1–2 networks. This single analysis would be the highest-leverage addition.
3. **Include budget-matched comparison** to BIC-HC with many random restarts or tabu search at equal computational budget.

## Reporting

Anchors retrieved across all rounds:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Uj0h13lVrR | 1.0 | R1 | Much weaker; XBIC is clearly superior |
| nSDOkm0SKo | 1.0 | R1 | Much weaker; XBIC is clearly superior |
| bEgDEyy2Yk | 1.0 | R1 | Code implementation only; XBIC far above |
| P49gSPmrvN | 1.0 | R1 | Unrelated visualization; XBIC far above |
| AvXrppAS2o | 3.0 | R1 | Causal structure + prediction; marginal improvements, only 2 baselines. XBIC clearly better |
| MVpvyeVeyI | 3.4 | R1 | Causal BO with unknown graphs; highly variable scores. XBIC above |
| JzFLBOFMZ2 | 3.2 | R1 | LLM for causal discovery; XBIC more rigorous |
| TRHyAnInUC | 3.25 | R1 | Diffusion for causal discovery; XBIC more grounded |
| ljZFM2mhbR | 5.0 | R1/R2 | **Most comparable**: DAG-SHAP uses SHAP in DAG context, lacks theory, assumes known graph. XBIC has better evaluation but similar novelty level |
| DUfwD5yiN4 | 5.25 | R1 | Distributed BN learning; XBIC has better experiments but less theory |
| lnMQGBHYRt | 5.33 | R1 | Scalable do-SHAP; different focus but comparable novelty |
| lLzeKG6t52 | 4.0 | R1 | SHAP approximation; different problem |
| 3n6DYH3cIP | 5.6 | R1 | Extendable BN learning (accepted); XBIC comparable in evaluation |
| eeJz7eDWKO | 6.0 | R1 | Meta-Learning BC (accepted); cleaner methodology, better theory. XBIC below |
| 8muemqlnG3 | 6.5 | R1 | DrBO (accepted); stronger results, more principled. XBIC below |
| 8X74NZpARg | 6.25 | R1 | Shapley-Guided Utility Learning (accepted); different domain |
| xByvdb3DCm | 8.0 | R1 | Selection+Intervention (accepted); much stronger theoretical contribution |
| 3cuJwmPxXj | 8.0 | R1 | Intervention extrapolation; different focus |
| k38Th3x4d9 | 8.0 | R1 | Root cause analysis; different focus |
| i5JfdnCob7 | 4.4 | R2 | Kernel choice for score-based CD (rejected); XBIC has more extensive evaluation |
| orD5t7blqV | 4.25 | R2 | PIT Algorithm; XBIC above |
| 2pEqXce0um | 4.5 | R2 | Root cause analysis; XBIC comparable |
| eqQFBnjjPP | 4.0 | R2 | ExDBN; XBIC above |
| Lxst78Rrwj | 5.0 | R2 | Causal graph via distributional invariance; comparable to XBIC |
| jE6VXUhxq9 | 6.25 | R2 | Deterministic relations in CD (rejected); stronger theoretical insight |
| HBf6HFnpmH | 5.5 | R2 | Scalability evaluation; XBIC comparable |

**Round 1 bracket:** 4.5–5.5. XBIC is clearly above the 3.0–4.4 range (papers with weak contributions/evaluation) and below the 6.0+ range (papers with cleaner methodology and stronger claims). Most comparable anchor is DAG-SHAP (5.0, rejected).

**Round 2:** Confirmed 4.5–5.5. The "Optimal Kernel Choice" paper (4.4, rejected) has similar issues (weak novelty over prior work, limited evaluation) but XBIC is somewhat better. The 5.0 DAG-SHAP anchor remains the best match.

**Final score: 5.0** — Creative idea and extensive evaluation, but headline claims inflated by CPDAG evaluation artifact, core mechanism unexplained, and real improvement over fair baseline is +0.04 absolute F1 at 50–200× cost.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>