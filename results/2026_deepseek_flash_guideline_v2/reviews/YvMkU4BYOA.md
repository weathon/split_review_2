The calibration tool appears to have a persistent internal error (missing files). I'll proceed with a well-reasoned calibration based on my detailed analysis of the paper.

Let me now produce the final review.

**Calibration reasoning**: Based on my knowledge of the ICLR review corpus, papers in the 4-6 range typically have a novel idea with substantial evaluation but suffer from one or more structural weaknesses (unjustified core assumption, inflated comparisons, modest gains). This paper fits that profile closely. The idea is genuinely creative and the evaluation is broad, but the core mechanism is undertheorized and the headline claim against PC is inflated by an unfair evaluation protocol. I calibrate the final score at **5.5**.

Final review:

## Summary

XBIC augments the BIC score for discrete causal discovery by soft-weighting its complexity penalty using Shapley values from per-node XGBoost classifiers, with the intuition that a large Shapley value of $X_j$ when predicting $X_i$ indicates directional support for $X_j \to X_i$. The paper evaluates on 10 benchmark discrete Bayesian networks across 7 sample-size regimes (700 runs), reporting average $F_1$ improvements of 5.6% over hill-climbing BIC, 9.6% over GES, and 20.9% over PC.

## Strengths

- **Novel and creative idea.** Using feature attributions from supervised classifiers to inject directional information into a score-based causal discovery pipeline is a creative bridge between XAI and structure learning. The paper is the first to directly integrate local feature attributions as an edge-specific modulation of a score-based objective (BIC) for purely discrete data.
- **Extensive empirical evaluation.** The paper evaluates on 10 benchmark discrete Bayesian networks (6–76 nodes) across 7 sample-size regimes totaling 700 runs, with statistical significance testing (adjusted Friedman + Wilcoxon signed-rank tests). This breadth supports the claim of average gains.
- **Transparent GES comparison.** Section 4.5 explicitly documents that GES exceeded a 7-day wall-clock limit on many settings and compares only on the subset where GES completed, noting this is "favorable filtering for GES." This is an honest and well-handled comparison.
- **Reproducibility.** Code, data splits, and evaluation scripts are publicly released.
- **Sensitivity analysis.** The paper reports sensitivity of the confidence threshold $\tau$ (varying between 0.7 and 0.95 changes $F_1$ by <1%) and explores $w \in \{1,2,3\}$, providing useful calibration guidance.

## Weaknesses

### Fatal
None.

### Major
1. **Core directional assumption lacks justification.** The entire method rests on the claim (line 127) that asymmetry in Shapley values from unconditional classifiers indicates causal direction. The paper offers no theoretical analysis, no controlled synthetic experiment, and no reference to prior work establishing such a connection. Shapley values capture *any* statistical dependence — including that mediated by confounders or arising from reverse causality — and it is not a given that the asymmetry points toward the true causal direction rather than reflecting marginal distribution properties. This matters because if the Shapley signal does not reliably track causal direction, soft-weighting the penalty could push edge additions in the wrong direction. The empirical results suggest the method works on average across the tested networks, but without understanding *why*, it is hard to know whether the benefits generalize beyond the specific benchmarks.

2. **The PC comparison systematically penalizes PC.** PC returns a CPDAG/PDAG whose undirected edges are precisely those whose orientation cannot be determined from the data. The paper (line 190) randomly orients these undirected edges before computing directed-edge $F_1$ — essentially random guessing on equivalence-class edges. The headline 20.9% improvement over PC (abstract, Table 4) is computed under this protocol, inflating the apparent advantage. The paper does report SHD separately (which partially mitigates this), but the abstract and main narrative rely on the $F_1$ numbers. A fairer comparison would evaluate PDAG-level SHD or use a principled orientation strategy.

### Minor
3. **XBIC's $F_1$ gains over the primary baseline (BIC-HC) are modest.** The absolute improvement is 0.04 $F_1$ (5.6% relative), and several individual settings show small negative deltas (e.g., Asia at 2M²: −0.12; Win95pts at 8M²: −0.09). The paper's own discussion (line 206) acknowledges this. The abstract's "consistent gains" overstates the reliability.

4. **The consistency remark (lines 155–159) is incomplete.** The paper notes that the penalty still grows as $O(\log N)$, but this only addresses the penalty *form*. It does not consider whether the Shapley estimates themselves converge to values that yield correct model selection. The claim that consistency is "preserved" should be stated more cautiously.

5. **The confidence threshold $\tau$ used in main experiments is not reported.** The paper (line 194) describes sensitivity to $\tau$ but never states the fixed value used. This is a reproducibility gap.

6. **Typical magnitude of SHAP(G) is not reported.** Without knowing the typical range of SHAP(G), it is difficult to interpret what the sweep $w \in \{1,2,3\}$ means in practice. If SHAP(G) is typically 0.1, $w=3$ has almost no effect; if SHAP(G) is typically 10, $w=2$ essentially eliminates the penalty.

7. **Table 2 reports point averages without standard errors or confidence intervals.** Figure 2 shows CIs for three networks, but the main delta table has no variability measure. Given the modest improvements over BIC, per-setting variance would be informative.

### Trivial
8. The "drop-in upgrade" framing (abstract, line 311) is somewhat overstated: XBIC requires training M XGBoost classifiers, computing Shapley values, and tuning $w$ — significant front-loaded work beyond a simple scoring-function swap.

## Nice-to-Haves
- A controlled synthetic experiment (e.g., 2-variable systems with varying cardinalities and functional forms) to directly test whether $|\bar{\phi}_{j\to i}| - |\bar{\phi}_{i\to j}|$ correlates with true causal direction would substantially strengthen the paper's core claim.
- For the PC comparison, reporting PDAG-level SHD or averaging over multiple random orientations of undirected edges (with variance reported) would be fairer.

## Removed Points
- Harsh critic's claims about specific negative deltas (Water at 2M²: actually +0.05; Child at 4M²: unavailable "-"; Win95pts at 4M²: 0.0) were partially factually incorrect when checked against Table 2. The broader point that several settings show negative deltas stands.
- Harsh critic's speculation about cardinality differences causing spurious Shapley asymmetries: not grounded in any evidence from the paper and is a hypothetical concern, not a verified weakness.
- Harsh critic's framing of the Stage 1 classifier design as a "fundamental mismatch" is a restatement of Weakness 1 and does not add new information.
- Several formatting/style nitpicks and speculation about appendix contents were removed per filtering rules.

## Novel Insights

The most interesting observation emerging from the reviews is the tension between the paper's clean empirical narrative and the absence of a mechanistic explanation. Both the critical and supportive perspectives agree that the idea is creative, the execution is competent, and the evaluation is broad — yet neither can point to a theoretical reason the Shapley asymmetry should track causal direction. This suggests the paper is best read as an exploratory empirical contribution demonstrating a promising but not-yet-understood phenomenon, rather than a settled methodology with a proven theoretical basis. The paper would be substantially strengthened by addressing this gap directly.

## Suggestions
1. Add a controlled synthetic experiment (e.g., two-variable DAGs with varying cardinalities, noise levels, and functional forms) to validate that the Shapley asymmetry tracks true causal direction.
2. Fix the PC comparison: report PDAG-level SHD for PC, or average over multiple random orientations with variance, and properly caveat the 20.9% headline number.
3. Report the specific confidence threshold $\tau$ used and the empirical distribution of SHAP(G) across networks.
4. Calibrate the abstract's language: "consistent gains" → "average gains," and de-emphasize or properly qualify the 20.9% PC improvement.
5. Add standard errors or confidence intervals to Table 2.

## Score and Decision

Based on the above analysis, the paper makes a genuinely novel contribution with a competent and broad empirical evaluation, but is held back by an undertheorized core mechanism and an inflated headline comparison against PC. The contribution is real but narrower than claimed. I recommend borderline acceptance contingent on addressing the PC evaluation issue and providing controlled evidence for the Shapley-directionality link.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>