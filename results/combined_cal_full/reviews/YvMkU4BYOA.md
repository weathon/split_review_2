Now I have sufficient calibration data. Let me compile the final review.

**Bracket from Round 1:** The paper sits between the reject-range anchors (3.0-4.0: AvXrppAS2o, eqQFBnjjPP) and the borderline-accept range (5.0-6.5: DAG-SHAP at 5.0, DrBO at 6.5). Against DAG-SHAP (5.0) — the most topically similar anchor — our paper's weighted items are comparable: genuine novelty (+1.57 vs DAG-SHAP's +3.88 creative approach), broad evaluation (+3.65), honest limitation reporting (+4.40), but a heavy negative on PC evaluation fairness (-5.08). DAG-SHAP's heaviest negatives were around -4.54 (lack of theoretical guarantees). Our PC evaluation issue is similarly weighty. Against the lower anchors (AvXrppAS2o at 3.0, eqQFBnjjPP at 4.0), our paper has stronger novelty and more honest reporting, placing it above them. Against DrBO (6.5), that paper had stronger empirical results and fewer methodological concerns, placing it clearly above ours. **Plausible bracket: 4.0–5.5.**

Here is the consolidated review:

## Summary

XBIC augments the BIC score for discrete causal structure learning with Shapley-value-based directional signals from per-node XGBoost classifiers. The idea is to softly reduce BIC's complexity penalty on edges where Shapley attributions indicate strong directional support, while defaulting to standard BIC when evidence is weak. The paper evaluates across 10 benchmark networks and 7 sample-size regimes.

## Strengths

- **Novel direction for combining explainability with structure learning (Section 3).** The idea of using local feature attributions (Shapley values) from predictive classifiers to inform the scoring of causal graphs is genuinely novel. Prior work typically uses causal knowledge to constrain explanations; this paper inverts that relationship by using attributions to improve structure learning when the graph is unknown.

- **Thorough evaluation scope.** The paper evaluates across 10 benchmark Bayesian networks (6–76 nodes), 7 sample-size regimes, and 700 total runs (Section 4.1). This is broader than many papers in this space and allows characterization of where XBIC helps and where it does not.

- **Honest limitation reporting.** The paper acknowledges that XBIC offers little benefit on small samples (Section 4.3, Conclusions), reports wall-clock times showing significant computational overhead (Table 5), and identifies scale limitations and the lack of formal theory (Limitations, Section Conclusions). This candor helps readers assess applicability.

## Weaknesses

### Major

1. **The PC evaluation protocol is structurally unfair, inflating the reported 20.9% improvement.** From Section 4.1 (line 190): "For baselines that return a PDAG, we complete it to a DAG by randomly orienting undirected edges (while preserving acyclicity) before computing directed-edge metrics." PC's CPDAG output correctly leaves edges whose direction cannot be determined from conditional independence tests *undirected by design*. Randomly orienting these edges before computing directed-edge precision/recall means approximately half of those edges will be assigned the wrong direction, systematically degrading PC's scores. XBIC always outputs a fully directed DAG and is evaluated on directed edges directly. An unknown but potentially large fraction of the reported 20.9% gap is an artifact of this protocol. Standard practice is to evaluate PC on its CPDAG output using SID, or to report skeleton and orientation metrics separately.

2. **Absolute F1 values for baselines are not reported, only deltas.** Table 2 shows F1 deltas of XBIC relative to BIC, PC, and GES. Table 4 reports absolute deltas (e.g., 0.04 for XBIC w=2 vs BIC) but never the baseline F1 values themselves. Without knowing whether the baseline BIC F1 is 0.30 or 0.80, a reader cannot calibrate whether a 0.04 absolute improvement is practically meaningful. This gap in reporting significantly limits interpretability of the results.

### Minor

3. **The confidence threshold τ used in the main experiments is not stated.** Section 3.1 (line 117) defines τ ∈ (0,1) but never gives its specific value. Section 4.3 (line 194) reports that varying τ between 0.7 and 0.95 changes F1 by <1%, but the actual value used remains unspecified. This is a reproducibility gap.

4. **The GES comparison (Section 4.5) filters to only runs where GES completed within 7 days**, selecting the easiest subset for GES. While described transparently, the conclusion that XBIC achieves lower SHD than GES should be caveated with this selection bias.

5. **The runtime overhead (Table 5) is 100–600× slower than BIC** (e.g., Asia: 0.39s vs 74.78s; Survey: 0.09s vs 54.21s). While acknowledged, the 5.6% relative F1 improvement over BIC at this cost receives limited discussion of the cost-benefit trade-off.

### Trivial

None.

## Nice-to-Haves

- A controlled experiment validating that Shapley-value asymmetry reliably tracks causal direction (e.g., on a synthetic graph with known ground-truth mechanisms) would strengthen the core assumption.
- Reporting orientation-specific metrics (how XBIC resolves edges that are within Markov equivalence classes) would directly test the problem the method was designed for.

## Removed Points

These points were raised but are either not verifiable from the paper as written, reflect scope creep, or are minor enough to not warrant inclusion in the final assessment:

- **Core assumption about Shapley asymmetry → causal direction:** The harsh critic claimed this is "unexamined." However, the paper presents it explicitly as intuition (Section 3.2: "Intuitively..."), evaluates the method empirically across 10 benchmarks, and the Limitations section acknowledges the lack of formal theory. This is an empirical paper, and the core mechanism is validated through benchmark performance. Demanding a theoretical proof sets a standard not required for this type of work.
- **Exponential form of penalty in Eq (2):** The functional form choice is a design decision; the paper demonstrates it works empirically. No principled reason exists to prefer linear over exponential.
- **Data matrix typed as ℝ in Algorithm 1 (line 78):** Trivial notation inconsistency with discrete data. Removed as formatting nitpick.
- **Missing MMHC baseline:** The paper explicitly addresses this ("MMHC targets large sparse graphs and is not the focus here"). Scope justification is reasonable.
- **Hyperparameter w values not justified:** The paper sweeps w ∈ {1,2,3} and reports results. The range is clearly stated and results are shown for all values.
- **Friedman/Wilcoxon without effect sizes:** Minor statistical reporting preference; p-values are reported.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Re-evaluate PC using standard metrics appropriate to its CPDAG output (e.g., SID, or report skeleton and orientation F1 separately).
2. Report absolute F1 values for all baselines in a full results table.
3. State the exact τ value used in the main experiments.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>