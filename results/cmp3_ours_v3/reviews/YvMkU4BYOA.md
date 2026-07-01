Now I'll produce the final review.

## Summary

XBIC modifies the BIC score for score-based causal discovery on discrete data by using Shapley values from per-node XGBoost classifiers to compute directional edge signals, then soft-weighting BIC's complexity penalty so that edges with strong attribution support face a reduced penalty. On 10 benchmark discrete Bayesian networks across 7 sample-size regimes (700 runs), XBIC reports +5.6% oriented-edge F₁ over BIC-HC, +9.6% over a generalized-score GES variant, and +20.9% over PC.

## Strengths

- **Novel direction: using explanations to inform structure learning rather than the reverse.** Most work at the causality-XAI interface injects known causal structure into explanations; XBIC does the opposite — using feature attributions (computed when the graph is unknown) to improve structure learning itself (Section 2.2, lines 48–53). This is a genuinely underexplored direction with strong potential.

- **Clean degradation to BIC.** XBIC reduces to standard BIC when w=0 or SHAP(G)=0, and the penalty retains O(log N) growth (Section 3, lines 113–114, 159). This graceful fallback to the standard score when directional signal is absent reflects careful engineering design.

- **Substantial evaluation scope.** Ten networks (6–76 nodes), seven sample-size regimes, 700 total runs, with adjusted Friedman + Wilcoxon significance testing. This is more extensive than many empirical papers in this space.

- **Reproducibility commitment.** Code, data splits, and evaluation scripts are publicly released.

## Weaknesses

### Fatal

None.

### Major

- **Central premise — that Shapley asymmetry from predictive classifiers provides reliable directional evidence for discrete causal discovery — is asserted without isolated validation.** The method's operational claim is that |φ̄ⱼ→ᵢ| >> |φ̄ᵢ→ⱼ| favors Xⱼ→Xᵢ over Xᵢ→Xⱼ (line 127). The paper provides no theoretical analysis, no synthetic two-variable controlled experiment isolating this property, and no reference to prior work establishing that predictive Shapley asymmetry in tree-based models on discrete data tracks causal direction. Without this foundation, the reader cannot determine whether the observed F₁ improvements reflect a genuine directional signal or a correlate (e.g., a heuristic that happens to work on these particular benchmarks). The paper explicitly acknowledges that theory is future work (line 313), but the method is presented operationally as if the directional link is reliable. This gap undermines the paper's claim to be "principled" (abstract, line 9) and limits the interpretability of the empirical results.

- **The PC (and GES) baseline comparison is weakened by random DAG completion of PDAG outputs.** The paper completes PDAG/CPDAG outputs to a DAG "by randomly orienting undirected edges (while preserving acyclicity)" (line 190) before computing directed-edge metrics. Random orientation adds noise to PC's F₁ scores — even a perfectly correct CPDAG would score poorly on directed-edge metrics under this protocol. The headline 20.9% improvement over PC should be substantially discounted; the +5.6% over BIC-HC (which naturally outputs a DAG) is the more relevant comparison. The GES results also suffer from this protocol and, additionally, from massive data loss due to the 7-day time limit (lines 277–279).

### Minor

- **Modest effect size relative to computational cost.** XBIC is 28–192× slower than BIC (Table 5: Asia 0.39s → 74.78s, Alarm 9.30s → 523.52s, Win95pts 75.33s → 2139.27s), while the absolute F₁ improvement over BIC is 0.04 (Table 4). The gains are statistically significant and larger on some individual settings, but the cost-benefit ratio deserves more prominent discussion.

- **The penalty formulation creates an unanalyzed density-favoring bias.** SHAP(G) = Σ|φ̄ⱼ→ᵢ| over all edges in G (Equation 3). Since the denominator exp(w·SHAP(G)) grows with the number of edges, the marginal penalty for adding an edge shrinks as the graph becomes denser. A dense graph with many weak Shapley values could accumulate a larger SHAP(G) than a sparse but correct graph, making it harder for XBIC to penalize spurious edges in dense candidates. This interaction is not discussed or controlled for.

- **The consistency claim is informal.** The paper argues (lines 155–159) that because the penalty scales as c(G)·(log N)/2·dim(G), it "preserves large-sample consistency" under standard BIC regularity conditions. However, BIC's consistency proof relies specifically on the penalty being (log N)/2 per parameter; reducing the effective penalty (c(G) < 1) changes the threshold and may not satisfy the same consistency properties.

- **The GES baseline uses a generalized-score variant (Huang et al., 2018) rather than standard GES with BIC (Chickering, 2002).** Standard GES with BIC is a natural, widely-used baseline that is absent.

### Trivial

- **Imprecise phrasing in the abstract.** The abstract says XBIC reduces the penalty "when a candidate parent contributes strongly to its child's likelihood" (line 9), but XBIC measures Shapley values from a separately trained classifier, not the likelihood contribution in the BIC sense.

## Nice-to-Haves

1. A controlled synthetic experiment (e.g., two-variable discrete causal models with known ground truth) measuring whether Shapley asymmetry |φ̄ⱼ→ᵢ| − |φ̄ᵢ→ⱼ| correctly identifies causal direction under varying functional forms, noise levels, and sample sizes. This directly tests the central premise and is the single highest-impact addition.
2. CPDAG-level metrics (e.g., SID) for the PC comparison to avoid the random-completion issue.
3. Disclosure of the specific confidence threshold τ used in the main experiments (sensitivity is reported but the actual default value is not stated).

## Removed Points

These points are flagged to be removed; treat them with caution.

- *"The paper does not specify whether GES improvement is computed only on the subset where GES completed."* → **Removed:** The paper clearly states "XBIC was compared head-to-head on the same repetitions" (lines 278–279).
- *"No analysis of how the number of categories per variable affects the method."* → **Removed:** Scope creep — the paper acknowledges high-cardinality CPTs as a challenge (line 15) but does not claim to analyze this dimension.
- *Headline strengths lacking specific backing* → Several strengths from the input review were dropped because they were generic (e.g., "the paper addresses an important problem") or because they conflicted with verified weaknesses.

## Novel Insights

None beyond the paper's own contributions. The single most insightful observation from the review process is that the paper's core operational premise (Shapley asymmetry → causal direction for discrete data) lacks any isolated validation, making it difficult to distinguish whether the empirical gains reflect a genuine signal or a correlate. This is a specific, concrete gap — not a generic concern.

## Suggestions

1. **Add a controlled experiment validating the central premise.** This is the single highest-leverage improvement: a synthetic two-variable setup where the ground-truth direction is known, testing whether |φ̄ⱼ→ᵢ| > |φ̄ᵢ→ⱼ| reliably indicates Xⱼ→Xᵢ across different functional forms and noise levels. Include a confounded case (X←Z→Y) to test whether the asymmetry goes to zero when direction is not identifiable.
2. **Re-run PC comparison using CPDAG-level metrics** (SHD on CPDAG, SID) or average over multiple random completions and report variance.
3. **Acknowledge and analyze the density-bias** in the SHAP(G) formulation, or propose a normalized variant (e.g., average |φ̄| per edge rather than sum).
4. **Report the specific τ value used** and clarify the limitations of the consistency claim.

## Score and Decision

Calibration anchors (all papers retrieved across rounds):

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `Uj0h13lVrR.md` | 1.00 | R1 | GFlowNets paper — not comparable, strong reject |
| `5lUdTogEL3.md` | 1.00 | R1 | Person re-ID — not comparable, strong reject |
| `AvXrppAS2o.md` | 3.00 | R1 | Causal structure learning for prediction — similar topic, weaker method grounding |
| `fSxiromxAq.md` | 3.00 | R1 | Sparse causal model — vague framing, thin evaluation |
| `TRHyAnInUC.md` | 3.25 | R1 | Diffusion for causal discovery — similar topic, stronger theory but less evaluation |
| `JzFLBOFMZ2.md` | 3.20 | R1 | LLM for causal discovery — similar topic |
| `i5JfdnCob7.md` | 4.40 | R1, R2 | Kernel selection for score-based causal discovery — incremental over prior work, thin experiments |
| `G19piTjVYA.md` | 4.00 | R2 | Differentiable causal order — similar evaluation limitations |
| `Z756zcjNcC.md` | 4.50 | R2 | DDCD — comparable: interesting idea with a mechanism gap, mixed reviews |
| `Lxst78Rrwj.md` | 5.00 | R1 | Causal graph via distributional invariance — has theoretical framework but imperfect |
| `ljZFM2mhbR.md` | 5.00 | R2 | DAG-SHAP — Shapley+graphs, similar topic |
| `lmKJ1b6PaL.md` | 6.80 | R1 | Causal Concept Graphs — stronger theory + validation |
| `Q0s6kgrUMr.md` | 6.67 | R1 | Causal/anticausal direction — has both theoretical analysis and empirical validation |
| `NNBAzdF7Cg.md` | 6.00 | R1 | Spiking neural networks as causal models |
| `k03mB41vyM.md` | 6.50 | R1 | Identifiable exchangeable mechanisms — strong theory |

**Round 1 bracket:** 4.0–6.0.  
**Round 2 narrowing:** 4.5–5.5 (based on comparison to DDCD at 4.50, DAG-SHAP at 5.00, and Causal Graph via Invariance at 5.00).

**Final score:** 5.0. The paper has a genuinely novel idea and thorough empirical evaluation, which are real strengths. However, the central premise — that Shapley asymmetry from predictive classifiers reliably tracks causal direction in discrete data — is asserted without isolated validation, and the PC/GES baseline comparison is weakened by random-orientation of PDAG outputs. These are significant weaknesses that prevent the paper from meeting the ICLR bar in its current form.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>