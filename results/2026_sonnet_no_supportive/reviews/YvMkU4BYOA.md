Now I have enough to draft the review.Based on the calibration results, I can now form my bracket. Papers scoring 3-5 in causal discovery typically have incremental contributions with missing critical baselines or unverified mechanisms. Papers scoring 7-8 have strong novel theoretical or empirical contributions. XBIC has a genuine novel idea but: (1) the core mechanism claim is unverified, (2) comparison against PC/GES is biased by random PDAG completion, (3) in-sample w selection. The BIC-HC comparison is the cleanest (both return DAGs), and the +5.6% F1 gain there is real but modest. I bracket this at **4–5**, leaning toward 4.5.

---

## Summary
XBIC augments the standard BIC score for discrete Bayesian network structure learning by soft-weighting BIC's complexity penalty using edge-specific Shapley attributions derived from per-node XGBoost classifiers. When per-node classifiers confidently attribute predictive importance from X_j to X_i, the penalty on that edge is reduced, steering hill-climbing toward better-oriented DAGs. Experiments cover 10 bnlearn benchmark networks across 7 sample-size regimes (700 runs), reporting aggregate F1 improvements of +5.6% vs. BIC-HC, +9.6% vs. GES, and +20.9% vs. PC.

## Strengths
- **Novel integration of XAI into discrete score-based causal discovery.** No prior work uses local Shapley attributions as a directional modulation of a BIC score in discrete structure learning. The distinction from existing causality→explanation work (Sections 2.2–2.3) is accurate and well-articulated.
- **Thorough empirical evaluation.** Ten benchmark networks, seven sample-size regimes, 10 repeats each (700 runs total), using appropriate Friedman + Wilcoxon statistical tests. Per-network per-regime deltas (Table 2) and aggregate summary (Table 4) together allow granular inspection.
- **Honest reporting of failures.** Table 2 explicitly shows regressions (Win95pts at large samples: −0.09 vs. BIC; small-sample, small-network: 0.00 improvement), and the paper provides a mechanistic explanation (confidence filter → SHAP(G) ≈ 0 → XBIC reverts to BIC).

## Weaknesses

### Fatal
None.

### Major

1. **The claimed directional mechanism is intuitive but unverified, and the score formula does not cleanly implement it.** Section 3.2 states: "Intuitively, if |φ̄_{1→2}| >> |φ̄_{2→1}|, the edge X₁→X₂ has stronger directional support than X₂→X₁." However, SHAP(G) (Eq. 3) is defined as a *sum* over all edges in G: SHAP(G) = Σ_{j→i ∈ E(G)} |φ̄_{j→i}|. Because attributions are absolute values, adding *any* edge to G increases SHAP(G), uniformly reducing the complexity penalty. The formula does not distinguish between X_j→X_i vs. X_i→X_j; it encodes "prefer graphs with more or stronger attributed edges overall." The paper provides no experiment that actually measures |φ̄_{j→i}| vs. |φ̄_{i→j}| for true-direction edges to check whether the attribution magnitudes are asymmetric in the claimed direction. Without this, the empirical gains (absolute F1 ≈ 0.03–0.04 vs. BIC) are consistent with a simpler explanation: softer penalization improves recall without carrying directional information. The motivating claim — that XBIC resolves edge directions within Markov equivalence classes — is a hypothesis, not a demonstrated fact.

2. **PDAG completion via random orientation systematically biases comparisons against PC and GES.** Section 4.1: "For baselines that return a PDAG, we complete it to a DAG by randomly orienting undirected edges (while preserving acyclicity) before computing directed-edge metrics." Random completion correctly orients ~50% of undirected edges by chance. The standard protocol is to use Meek's rules to maximally orient the PDAG before any random fallback. Using random orientation inflates apparent weakness for PC (which always returns a PDAG) and partially for GES, making the +20.9% vs. PC and +9.6% vs. GES gains in Table 4 difficult to interpret.

3. **In-sample hyperparameter selection for w.** The paper sweeps w ∈ {1, 2, 3} and reports w=2 as the best configuration in Table 4, based on the same 700-run evaluation set. No held-out or cross-validated protocol for selecting w is described. If w was identified by inspecting Table 4, the reported +5.6% vs. BIC is optimistically biased.

### Minor

1. **Win95pts regression at large samples is unexplained.** Table 2 shows XBIC δF1 = −0.09 vs. BIC at 8M² on Win95pts. 8M² = 8 × 76² ≈ 46,000 samples — this is not a small-data regime. The paper's low-confidence explanation does not apply here, and no alternative is offered.

2. **GES comparison denominator ambiguity.** Section 4.5 states GES statistics are computed only over runs where GES completed. Yet Table 4 reports a "+9.6% vs. GES across 700 runs" headline. It is unclear how GES's 700-run aggregate is computed given many "-" entries in Table 2. If GES averages only over its completions, denominators differ across methods and the relative gain is not directly comparable.

3. **MMHC excluded without justification.** Section 4.1 excludes MMHC ("not the focus here") but MMHC is the natural hybrid baseline for discrete networks and directly targets the regime studied. Including it would either strengthen the contribution or reveal the performance envelope.

### Trivial
None.

## Nice-to-Haves
- **Direct verification of attribution asymmetry:** For every true causal edge j→i in each benchmark network, compute and report the ratio |φ̄_{j→i}| / |φ̄_{i→j}|. If > 1 consistently for true-direction edges, the mechanism is validated; if not, the recall-improvement explanation is more accurate — either outcome is valuable.
- **Per-edge asymmetric formulation:** Replace the global sum SHAP(G) = Σ|φ̄_{j→i}| with a per-edge signal such as (|φ̄_{j→i}| − |φ̄_{i→j}|) to make the directional intent explicit and testable as an ablation.
- **Replace random PDAG completion with Meek's rules** for PC/GES outputs and recompute Table 4. This would reveal how much of the apparent advantage is due to the evaluation protocol.
- **Report per-cell standard deviations** in Table 2; many deltas (0.01–0.04) are small relative to expected noise.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Consistency remark labeled "misleading":** The harsh critic argues the consistency remark (Section 3) does not establish convergence to the true DAG. Removed as a standalone weakness — the remark explicitly claims only that the O(log N) penalty growth is preserved (a modest, correct claim), not convergence-to-truth. Causal discovery papers routinely defer full consistency analysis.
- **Shapley attributions cannot distinguish causal from non-causal predictors (stated as "fatal/structural"):** The critic argues observational classifiers cannot provide asymmetric causal-direction information. While theoretically accurate, the paper presents this as "intuitive" motivation, not a theorem. The empirical evaluation is the claim; removing it as a standalone fatal flaw (it is already captured in the Major weakness about unverified mechanism).
- **GES comparison "compromised" due to subset filtering:** Section 4.5 explicitly ensures head-to-head comparison on the same completed runs, which is fair. The unclear denominator in Table 4 is a minor concern retained in Minor, not a contamination of headline numbers.

## Novel Insights
The most interesting open question surfaced by this review is whether XGBoost-derived Shapley attributions from observational discrete data are genuinely asymmetric with respect to causal direction. If they are, XBIC's mechanism is more principled than the theoretical gap suggests; if they are not, the gains arise purely from softer penalization (a useful but weaker contribution). The gap between the formula (density-dependent penalty reduction) and the claim (directional disambiguation) is the sharpest actionable finding of this review — resolving it with a single targeted experiment would substantially clarify the paper's standing.

## Suggestions
1. Run the attribution asymmetry check: for each ground-truth edge j→i, compute the fraction of edges where |φ̄_{j→i}| > |φ̄_{i→j}|. Report this across all networks.
2. Replace random PDAG completion with Meek's rules; recompute Table 2 and Table 4.
3. Describe a held-out or cross-validation protocol for w selection, or fix w=2 by validation and report sensitivity separately.
4. Explain the Win95pts large-sample regression mechanism.

## Score and Decision

**Calibration anchors retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| TRHyAnInUC.md (D³PM causal discovery) | 3.25 | R1 | Causal discovery with novel angle but fundamental issues; similar tier |
| fSxiromxAq.md (Sparse Causal Model) | 3.00 | R1 | Weak empirical grounding, multiple gaps |
| JzFLBOFMZ2.md (LLM-supervised CSL) | 3.20 | R1 | Novel idea, evaluation gaps; comparable |
| AvXrppAS2o.md (causal structure + outcome prediction) | 3.00 | R1 | Limited novelty, weak evaluation |
| G19piTjVYA.md (Differentiable Causal Order) | 4.00 | R1 | Incremental, some missing baselines |
| i5JfdnCob7.md (Optimal Kernel Causal Discovery) | 4.40 | R1 | Clear contribution, solid evaluation, minor gaps |
| Lxst78Rrwj.md (Causal Graph via Distributional Invariance) | 5.00 | R1 | New framework, reasonable empirical validation |
| Z756zcjNcC.md (DDCD) | 4.50 | R1 | Novel architecture, limited theoretical grounding |
| NNBAzdF7Cg.md (Spiking NNs as causal models) | 6.00 | R1 | Solid technical contribution, accepted |
| 4011PUI9vm.md (RankSHAP) | 6.50 | R1 | Novel SHAP extension, solid axioms + evaluation |
| hQ2TUZmse1.md (Counterfactual + Shapley) | 7.00 | R1 | Strong method + experiments |
| xByvdb3DCm.md (Selection + Intervention) | 8.00 | R1 | Theoretical + empirical, clearly stronger |

**Round 1 bracket:** 4–5. XBIC is more empirically complete than the 3.0–3.25 papers but has significant unresolved mechanism questions and comparison protocol issues that prevent it from reaching the 5.5+ tier. The closest anchor is i5JfdnCob7.md (4.4: clear contribution, solid evaluation, minor gaps) — XBIC has a similar profile but with a larger unverified core claim. I settle on **4.5**.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>