Now I have all the information needed. Here is the final consolidated review.

## Summary

The paper introduces XBIC, a score-based causal discovery method for discrete Bayesian networks that augments the BIC complexity penalty with edge-specific Shapley values computed from per-node XGBoost classifiers. When a candidate parent contributes strongly to predicting its child, XBIC reduces the penalty proportionally, providing directional signal to break Markov-equivalence ambiguity. Evaluated on 10 benchmark networks (6–76 nodes) across 7 sample-size regimes, XBIC achieves oriented-edge F₁ improvements of 5.6% over hill-climbing BIC, with larger nominal gains over PC (20.9%) and GES (9.6%).

## Strengths

1. **Novel and principled integration of Shapley values into score-based causal discovery for discrete data.** The core idea — using predictive importance asymmetry from per-node classifiers to softly modulate BIC's complexity penalty — is genuinely novel and conceptually elegant. It bridges explainable AI and causal discovery in a way that has not been done for discrete Bayesian networks (Sections 2.2–3). The mechanism is well-motivated: Shapley values provide asymmetric directional signal that can help resolve Markov-equivalence ambiguity, which is a recognized limitation of BIC-based search.

2. **Evaluation across 10 networks and 7 sample-size regimes (700 runs) is reasonably extensive.** The study covers 6–76 node networks from diverse domains (medicine, insurance, weather, software) across data quantities from 0.125M² to 8M². This breadth exceeds many causal discovery papers and captures how discrete-data behavior changes with sample size.

3. **Transparent hyperparameter handling.** The paper sweeps w over {1, 2, 3} and reports the precision–recall tradeoff (Figure 2), and demonstrates the confidence threshold τ has <1% impact on F₁ (line 194). This gives a credible sense of the method's robustness to its hyperparameters.

4. **Graceful degradation to standard BIC.** When Shapley evidence is weak (small samples, low-confidence predictions), the SHAP(G) term approaches zero and XBIC reduces to BIC. This means XBIC does not actively harm performance in data-poor regimes where the classifiers cannot produce reliable attributions (lines 113, 159, 206–207).

5. **Code, data splits, and scripts are released,** supporting reproducibility.

## Weaknesses

### Fatal
None.

### Major

1. **The PC comparison is not apples-to-apples for oriented-edge metrics, inflating the headline 20.9% claim.** PC returns a CPDAG that by design leaves genuinely ambiguous edges undirected. The paper states: "For baselines that return a PDAG, we complete it to a DAG by randomly orienting undirected edges (while preserving acyclicity) before computing directed-edge metrics" (line 190). Randomly orienting the very edges that PC was designed to leave undirected mechanically lowers its oriented-edge precision, recall, and F₁ — PC never makes a claim about those edges' directions. XBIC, by contrast, produces a fully directed DAG using additional Shapley signal, so it *must* appear to beat PC on these metrics. The 20.9% figure in the abstract (line 9) and Table 4 is not interpretable as a fair comparison. To fix this, the authors should compare at the CPDAG level (using structural Hamming distance on the CPDAG, or reporting skeleton and orientation metrics separately), or use the same principled orientation method for both PC's undirected edges and XBIC's output. As it stands, this is the paper's most serious weakness because it drives the strongest headline claim.

### Minor

2. **GES comparison is computed on a systematically biased subset.** GES exceeded the 7-day time limit on many settings, particularly larger and denser networks (Table 2 shows many "—" entries). The authors retain "only repetitions where GES completed" and compute statistics on that subset (lines 277–278). This subset skews toward smaller networks and smaller sample sizes — easier problems — and the paper acknowledges this filtering is "favorable for GES." Nonetheless, the 9.6% improvement claim rests on a non-representative sample and should be interpreted with caution or de-emphasized.

3. **Insufficient theoretical support for the consistency claim.** The paper states XBIC "preserves large-sample consistency" (line 159) because the penalty still scales as O(log N). However, the Shapley-weighted factor c(G) ∈ (0,1] varies non-uniformly across candidate graphs. BIC consistency proofs (e.g., Haughton 1988) rely on the exact penalty form and the Laplace approximation's validity; a graph-dependent factor that systematically shifts the relative ranking of graphs could, in principle, affect asymptotic selection. The paper offers no formal analysis. This claim should either be substantiated with a proper argument or removed.

4. **No discussion of whether Shapley evidence distinguishes direct causal edges from indirect or confounded relationships.** The Shapley values φ̄_{j→i} are computed from a classifier that predicts X_i from *all other variables* X_{\i}. Predictive importance conditional on all other features can be nonzero for indirect or confounded associations, not just direct edges. The confidence filter (τ) and averaging mitigate noise, but the paper does not analyze whether the signal reliably targets direct edges or how the method handles this confounding.

5. **Base absolute F₁ values are missing.** Table 2 reports only F₁ deltas relative to baselines; Table 4 reports absolute deltas (e.g., +0.04 over BIC) but not the absolute F₁ of BIC itself. The reader cannot assess how well any method performs in absolute terms. For example, a +0.04 delta from a baseline of 0.40 is a 10% relative gain, but from 0.90 it is only 4.4%. A column with BIC's absolute F₁ should be included.

6. **Confidence threshold τ is not numerically specified for the main experiments.** The paper says τ was varied between 0.7 and 0.95 in sensitivity analysis (line 194) but does not state the value actually used in the 700-run main evaluation. This is a minor reproducibility gap.

7. **Exponential penalty reduction could risk overfitting.** XBIC uses exp(w·SHAP(G)) in the denominator of the penalty (Eq. 2). Even moderate Shapley values can massively reduce the penalty (e.g., w=2, SHAP(G)=3 → penalty reduced by factor e⁶ ≈ 403). The paper does not discuss whether this exponential form is principled or whether it could overfit by over-rewarding edges with strong predictive (but not necessarily causal) signal.

### Trivial
- Algorithm 1 (line 78) describes the data matrix as ℝ^{N×M} with "discrete columns," which is slightly inconsistent since ℝ typically implies real-valued entries.

## Nice-to-Haves
- Add variance estimates or confidence intervals to the main aggregated results (Tables 2, 4), beyond the three-network subset shown in Figure 2.
- Include absolute F₁ values for baselines alongside the deltas.
- The "drop-in upgrade" framing (line 9; line 311) overpromises on practicality given the 100–200× slowdown from the front-loaded classifier+SHAP phase. Consider softening this language to "compatible with existing BIC-based pipelines" or similar.
- Analyze which structural properties (e.g., number of Markov-equivalent alternatives, strength of conditional dependencies) predict when XBIC's Shapley signal is most beneficial.

## Removed Points
- **"Drop-in upgrade" framing inconsistent with computational cost** — Removed because "drop-in modification of a familiar score" (line 311) is technically accurate: the score function itself is a drop-in replacement within any BIC-based search. The criticism conflates the score function with the full pipeline's preprocessing cost, which the paper separately discusses (Section 4.4).
- **Pure formatting/style nitpicks** — Removed per instructions.
- **Missing appendix/supplementary content** — Removed per instructions; appendices are stripped by the parser.
- **Typos, grammar, and parser artifacts** — Removed per instructions.

## Novel Insights
None beyond the paper's own contributions. The reviews surface the core methodological concern (PC comparison validity for directed-edge metrics), the theoretical gap (consistency argument), and the missing analysis of when Shapley signal distinguishes direct from indirect relationships — all of which the paper partially acknowledges but does not fully resolve.

## Suggestions
1. **Fix the PC comparison.** Either (a) compare at the CPDAG level using appropriate metrics (SHD on CPDAG, or skeleton/orientation metrics separately), or (b) use the same principled orientation procedure (e.g., BIC scoring of the two possible orientations) for both PC's undirected edges and XBIC's output. If the comparison must be on directed-edge F₁, explain why random orientation of a CPDAG's undirected edges is considered fair, or adjust the claim accordingly.
2. **De-emphasize or contextualize the GES comparison.** The 9.6% figure should note it is computed only on the subset where GES completed.
3. **Drop or substantiate the consistency claim.** Either provide a formal argument or note that the general case is an open question.
4. **Add absolute F₁ values for BIC-HC** alongside the deltas in Tables 2 and 4 so readers can assess baseline performance.
5. **Specify the τ value used in the main experiments** (line 194).
6. **Discuss whether the Shapley signal distinguishes direct from indirect relationships**, and if not, what this implies for the method's reliability.

## Score and Decision

**Bracket determination.** Round 1 searched six bands. The paper's closest topical matches are score-based causal discovery papers in the 4.25–6.50 range:
- PIT Algorithm (4.25): Structure learning improvement. Weaker contribution than XBIC.
- Extendable BN Learning (5.60, accepted): Cleaner method, cleaner evaluation. Comparable contribution size.
- Test-Time Causal Learning (5.50, rejected): Novel approach, mixed evaluation quality. Similar tier.
- DrBO (6.50, accepted): Stronger empirical validation, clearer comparisons. Better than XBIC.
- Deterministic Relations (6.25, rejected): Solid theory + experiments. Better methodology but also rejected.

Initial bracket: **4.5–6.0**. The paper has a genuinely novel idea and broad evaluation, but the PC comparison inflates the headline claim and the theoretical support is shallow. These issues prevent it from reaching the 6.0+ range of cleaner papers, but the core idea keeps it above the 4.0 range of weaker contributions.

**Final calibration.** Comparing against the anchors: the paper is stronger than PIT Algorithm (4.25) which has a less novel contribution. It is comparable to Extendable BN Learning (5.60) in contribution scope but has more significant comparison issues. It is weaker than DrBO (6.50) and Deterministic Relations (6.25) in methodological rigor. The most appropriate score is **5.0**, reflecting a novel but incompletely validated contribution.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>