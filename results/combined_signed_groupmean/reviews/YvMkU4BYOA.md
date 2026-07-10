Now I have enough calibration data. Let me synthesize my final assessment.

Let me compare against the closest anchor — DrBO (6.50):

**DrBO's weaknesses**: code not available (-10.00), inadequate baselines (-10.00), CAM pruning concern (-9.88) — these are serious methodological flaws.
**XBIC's weaknesses**: framing overreach (-10.00), global modulation (-9.71), GES subset (-5.72) — all addressable in revision.
**XBIC's strengths**: code provided (+10.00), extensive evaluation (+9.95), clean formulation (+9.28) — all stronger than DrBO's corresponding strengths.

XBIC is comparable or slightly below DrBO due to the central framing issue being more fundamental than DrBO's missing code/baselines. Let me finalize.

Here is my final consolidated review:

## Summary

This paper proposes XBIC, a score for discrete causal discovery that modulates BIC's complexity penalty using aggregated Shapley values from per-node classifiers. When a candidate parent contributes strongly to predicting its child, the penalty is reduced; when signal is weak, XBIC reverts to standard BIC. The method is evaluated on 10 benchmark networks across 7 sample-size regimes (700 runs), showing consistent but modest improvements over BIC, PC, and a GES variant.

## Strengths

- **Well-motivated problem and clean formulation.** The paper correctly identifies that resolving orientations within Markov equivalence classes is a persistent limitation of score-based methods for discrete data. The XBIC formulation (Equation 2) is simple and elegant: divide the penalty by exp(w·SHAP(G)). The property that XBIC reverts to BIC when Shapley evidence is weak (w=0 or SHAP(G)=0) is a practical asset — it means the method cannot be worse than BIC in expectation when no directional signal exists (Section 3). [impact=+9.28]

- **Extensive, systematic evaluation.** The paper evaluates on 10 benchmark networks (6–76 nodes) across 7 sample-size regimes (0.125M² to 8M²), totaling 700 runs. The sample-size sweep is well-chosen to probe when the method helps and when it degrades. The use of adjusted Friedman + Wilcoxon tests (Section 4.3) is appropriate for the multi-network, multi-regime comparison. [impact=+9.95]

- **Reproducibility.** Code, data splits, and scripts are released. The evaluation protocol is described in sufficient detail (seeds, CV folds, Optuna search spaces) that the results can be independently verified. [impact=+10.00]

## Weaknesses

### Fatal
None.

### Major

- **Shapley-based signal is framed as "directional evidence" without theoretical justification for the discrete setting.** The paper repeatedly frames φ̄_{j→i} as providing "directional evidence" (lines 19, 97, 282) or "directional support" (line 127) for Xⱼ → Xᵢ. However, φ_{j→i} is computed from a classifier fᵢ that predicts Xᵢ from *all other variables* X_{⧹i}. This classifier exploits any statistical dependence between Xⱼ and Xᵢ regardless of causal origin. In a chain X → Y → Z, the classifier predicting Z from {X,Y} assigns nonzero Shapley to X (because X and Z are dependent through Y), potentially reducing the penalty on the spurious edge X → Z. The paper provides no theoretical justification for why predictive-power asymmetry in the full conditional should align with causal direction in arbitrary discrete CPTs. Calling XBIC a "principled enhancement" (abstract line 9) overstates what is best described as a heuristic that empirically correlates with causal direction on tested benchmarks. **This does not invalidate the empirical results** — the method still works as a heuristic — but it weakens the paper's claim to a principled contribution. [impact=-10.00]

### Minor

- **The GES comparison in the abstract is reported on a biased subset without qualification.** GES exceeded a 7-day wall-clock limit on many (network, sample-size) pairs. Section 4.5 transparently retains only runs where GES completed — acknowledged as "favorable filtering for GES" (line 278). Yet the abstract reports "+9.6% over a generalized-score GES variant" (line 9) alongside the fair comparisons (BIC, PC) without noting this filtering. The 9.6% aggregates only over the subset where both methods completed, biased toward smaller networks and fewer samples. [impact=-5.72]

- **The penalty modulation is global rather than per-edge, creating unanalyzed interactions.** In Equation 2, the penalty is divided by exp(w·SHAP(G)) where SHAP(G) sums |φ̄| over *all edges* in G. This means the effective penalty on every edge depends on the Shapley values of all other edges. Adding a single edge with large |φ̄| simultaneously reduces the penalty on all existing edges — the net penalty can even decrease if exp(w·ΔSHAP) exceeds (1 + Δdim/dim_old). This global interaction is never discussed. While the paper correctly describes the *evidence* as edge-specific (each |φ̄_{j→i}| is per-edge), the modulation is global and its consequences are unanalyzed. [impact=-9.71]

- **No analysis of which edge types XBIC orients correctly vs. incorrectly.** The evaluation reports aggregate F₁ and SHD but does not break down performance by edge type (chains vs. confounders vs. colliders). Since the method is specifically designed to resolve Markov-equivalence classes (where chains and confounders are indistinguishable), a breakdown by these motifs would directly test the central claim about orientation improvement.

- **The "consistency remark" addresses penalty order, not structural consistency.** The remark (lines 155–159) argues only that the O(log N) penalty growth rate is preserved, concluding this "preserves large-sample consistency." However, structural consistency (recovering the true graph with probability 1 as N→∞) is stronger than preserving penalty order. A score that consistently selects a wrong DAG within an equivalence class could still have O(log N) penalty growth.

### Trivial
None.

## Nice-to-Haves

- **Controlled orientation-only experiment**: Fix the skeleton to ground truth and measure whether XBIC orients edges within equivalence classes more accurately than BIC. This would directly test the paper's core claim without confounds from skeleton recovery.
- **Compute-accuracy Pareto analysis**: Show (runtime, F₁) coordinates per network to help practitioners assess the cost-benefit trade-off more concretely.
- **Edge-type breakdown**: Analyze which graph motifs (chains, confounders, colliders) benefit most from the Shapley modulation.

## Removed Points

These points from the input review are removed per the filtering rules:

- **NOTEARS comparison suggestion** — scope creep; the paper focuses on classical score-based methods for discrete data and does not claim to cover gradient-based approaches.
- **MMHC not included** — the paper acknowledges this ("not the focus here") for the stated reason that MMHC targets large sparse graphs.
- **Table 2 "hard to parse"** — parser formatting artifact, not an author issue; the substantive observation (some entries near zero/negative) is preserved in the evaluation discussion.
- **ReX comparison insufficient** — the paper's narrow claim (first to integrate local feature attributions as edge-specific modulation of BIC for purely discrete data) is defensible; ReX targets continuous settings with constraint pruning.
- **Confidence filter lacking theoretical motivation** — the paper provides a practical justification (reducing attribution noise), which is reasonable for an empirical paper.
- **Self-limiting behavior on small samples** — insightful observation but the paper acknowledges this behavior and frames it as a design feature.
- **Pure formatting/style nitpicks** — removed per rules.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a central tension: the Shapley asymmetry is presented as causally informative when it is actually a predictive-heuristic correlation that works on benchmarks but lacks a theoretical basis for general discrete CPTs. This observation — that the heuristic's success deserves causal explanation rather than assumption — is the main novel insight from the review process.

## Suggestions

1. **Reframe the contribution**. Replace "directional evidence" and "principled enhancement" with language that honestly describes the method as using predictive-power asymmetries from the full conditional as a heuristic to modulate BIC penalties. Add a discussion of when the heuristic might fail (e.g., chains where indirect dependence creates spurious directional signals).

2. **Separate the GES comparison** in the abstract and headline results from the fair comparisons (BIC, PC). Use language like "on the subset where GES completed" or report only the BIC and PC improvements as primary.

3. **Add a controlled orientation-only experiment**: fix the skeleton to ground truth, run XBIC vs. BIC orientation, and report orientation accuracy directly.

4. **Discuss the global modulation** in the penalty and its interaction effects. Analyze the condition under which adding a high-φ edge can decrease total penalty.

5. **Add an edge-type breakdown** (chains vs. confounders vs. colliders) to directly test the orientation improvement claim.

## Score and Decision

**Round 1 bracket**: [5.0, 7.0]. The paper is clearly stronger than DAG-SHAP (5.00) and Optimal Kernel Choice (4.40) which had more serious novelty and methodological concerns. It is comparable to DrBO (6.50, Accept), DGES (6.25, Reject), and Extendable Structure Learning (5.60, Accept).

**Narrowing**: Compared to DrBO (6.50), XBIC has stronger reproducibility (code provided vs. DrBO's code not available at -10.00) and comparable experimental rigor. However, XBIC's central framing issue (-10.00 impact) — presenting predictive Shapley asymmetry as causal "directional evidence" without justification — is a more fundamental concern than DrBO's missing-code and baseline issues, which are procedural. The global modulation issue (-9.71) is also a significant unaddressed design concern. These prevent XBIC from reaching DrBO's level.

Compared to DGES (6.25), XBIC offers clearer novelty but less theoretical depth. DGES was rejected mainly due to perception of small contribution and inability to orient edges within deterministic clusters — problems arguably more limiting than XBIC's framing issue.

**Final placement**: 6.0. The paper has genuine contributions (novel integration of Shapley values into BIC scoring, extensive discrete-data evaluation, clean formulation) that are well-validated empirically. The weaknesses — primarily framing overreach and an unanalyzed global modulation — are significant but addressable in revision and do not invalidate the empirical findings.

**Anchors consulted** (all rounds):
- DAG-SHAP (5.00, Reject) — similar Shapley+causality topic; XBIC has clearer contribution and stronger evaluation
- Optimal Kernel Choice (4.40, Reject) — XBIC more novel and better evaluated
- DrBO (6.50, Accept) — XBIC comparable but weaker on framing, stronger on reproducibility
- Extendable SL (5.60, Accept) — XBIC comparable, both have strong experiments
- DGES (6.25, Reject) — XBIC has clearer contribution
- Meta-Learning BCD (6.00, Accept) — similar score, different methodology

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>