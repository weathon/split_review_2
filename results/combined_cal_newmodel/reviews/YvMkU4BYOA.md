Now I have all the information needed. Let me compile the final review.

**Round 1 bracket:** The paper sits between the 3.0–3.25 papers (weaker, vague methods) and the 4.0–4.5 papers (comparable, clear contributions but with methodological concerns). No comparable papers exist in the >8.5 band. The paper's strengths (clean idea, 700-run evaluation) favor the upper end of this range, but the PDAG evaluation flaw and modest BIC-HC gain pull it downward.

**Narrowing (Round 2):** Comparing itemized favorability ratings, our paper's weaknesses are less severe in magnitude than those of ExDBN (score 4.00) and PIT (score 4.25), whose most critical items reach favorability -4.57 and -4.69. Our paper's most negative items (2.71 and 2.29) are milder, but the number of weaknesses is larger. Compared to the 3.0-level anchors (fSxiromxAq, TRHyAnInUC), our paper is clearly stronger in evaluation scope, method clarity, and empirical grounding. The PDAG evaluation issue is the main factor preventing a higher score.

**Final score:** 4.0 — comparable to ExDBN (4.00) and below Optimal Kernel (4.40) and PIT (4.25), but clearly above Sparse Causal Model (3.00) and D3PM (3.25). Decision: Reject at ICLR standards.

---

## Summary

This paper proposes XBIC, a modification of the Bayesian Information Criterion (BIC) for score-based causal discovery in discrete Bayesian networks. The key idea is to soft-weight BIC's complexity penalty using aggregated Shapley values from per-node XGBoost classifiers: edges whose candidate parent contributes strongly to predicting the child face a reduced penalty, biasing the hill-climbing search toward orientations consistent with the data's predictive structure. The method reverts to standard BIC when the attribution signal is absent.

## Strengths

- **Clean and intuitive idea.** The core proposal — augmenting BIC's complexity penalty with Shapley-derived directional weights (Equation 2) — is formally simple and reverts exactly to BIC when the attribution signal is absent ($\text{SHAP}(G)=0$ or $w=0$), making it a drop-in modification. [favorability=12.69]

- **Reasonably extensive evaluation.** Testing on 10 benchmark networks (6–76 nodes) × 7 sample-size regimes × 10 repetitions = 700 runs provides a broad empirical scope for a discrete causal discovery paper. [favorability=10.71]

- **Open-source release.** The paper states that code, data splits, and evaluation scripts are publicly available, supporting reproducibility. [favorability=11.97]

## Weaknesses

### Major

- **PDAG-to-DAG completion via random orientation invalidates PC and GES comparisons.** The paper states (line 190): "For baselines that return a PDAG, we complete it to a DAG by randomly orienting undirected edges (while preserving acyclicity) before computing directed-edge metrics." PC and GES correctly return CPDAGs encoding Markov equivalence classes; undirected edges are precisely those whose orientation cannot be determined from observational data. Randomly orienting them penalizes baselines for honestly reporting uncertainty and inflates XBIC's apparent advantage. The headline claims of 20.9% improvement over PC and 9.6% over GES cannot be taken at face value. The only fair F₁ comparison is XBIC vs. BIC-HC, since both output fully directed DAGs. [favorability=2.71]

- **Modest gain over the only fairly-compared baseline at extreme computational cost.** From Table 4, XBIC($w$=2) achieves an absolute F₁ improvement of only 0.04 (5.6% relative) over BIC-HC. From Table 5, XBIC is 100–600× slower than BIC-HC depending on the network (e.g., 523s vs 9.3s on Alarm, 2139s vs 75s on Win95pts). A 0.04 F₁ gain at two orders of magnitude more computation is a weak trade-off that the paper does not adequately justify. [favorability=2.29]

### Minor

- **Core assumption lacks direct validation.** The method's foundation (line 127) is that $|\bar{\phi}_{1 \to 2}| \gg |\bar{\phi}_{2 \to 1}|$ supports $X_1 \to X_2$ over $X_2 \to X_1$. However, since the Shapley values come from a full predictive model $f_i: X_{\setminus i} \to X_i$, both directions can yield large absolute attributions (children predict parents via backward inference). The paper provides no theoretical analysis or controlled experiment (e.g., on known bivariate/trivariate structures) to validate that the Shapley asymmetry reliably tracks causal direction rather than some other statistical asymmetry. [favorability=0.63]

- **Consistency argument is superficial.** The claim (lines 155–159) that XBIC preserves BIC's large-sample consistency is asserted with only a brief argument about the penalty still growing as $O(\log N)$. The paper does not discuss what population value $\text{SHAP}(G)$ converges to, or whether it remains bounded away from zero for incorrect graphs — both are needed for a proper consistency argument when the penalty is data-dependent. [favorability=2.01]

- **The confidence threshold $\tau$ used in the main results is not reported.** The paper states (line 194) that varying $\tau$ between 0.7 and 0.95 changes $F_1$ by $<1\%$ on average, but never states what value was used for the primary experiments. [favorability=0.19]

- **Statistical test results are reported without actual $p$-values, test statistics, or effect sizes** (line 241). For a 0.04 absolute F₁ improvement, seeing the variance across networks and sample sizes is essential to assess robustness. [favorability=1.48]

- **The design choice to use absolute Shapley values ($|\bar{\phi}_{j \to i}|$) rather than signed values is not discussed.** A negative attribution could also be causally informative (indicating that $X_j$ suppresses $X_i$), and discarding the sign may lose useful signal. [favorability=2.55]

### Trivial

None.

## Nice-to-Haves

- Include BIC-HC with random restarts as a lightweight baseline to isolate whether XBIC's advantage comes from the Shapley signal or simply from different search trajectories.
- Add a controlled synthetic experiment (bivariate or trivariate structures) to directly test whether Shapley asymmetry tracks causal direction.
- Report confidence intervals or standard deviations for the headline F₁ numbers in Table 4.
- Discuss the signed vs. absolute Shapley design choice in the method section.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **MMHC omission** (critic's note): The paper explicitly scopes out MMHC as targeting large sparse graphs. This is a defensible scoping choice, not a weakness — removed as scope creep.
- **GES selection bias** (critic's note): The paper already acknowledges and discusses this limitation explicitly (lines 277–278). The criticism adds no new information — removed as already addressed.
- **No theoretical justification for Shapley asymmetry** (framed as fatal by critic): The paper provides empirical validation through the full evaluation. While direct controlled validation would strengthen the paper, the claim that it has "no argument — theoretical or empirical" is overstated; the full-system results constitute empirical evidence, and the critic's stronger framing was demoted to Minor above.

## Novel Insights

None beyond the paper's own contributions — the reviews raise important methodological concerns about the evaluation protocol and cost-benefit trade-off, but do not identify new aspects of the work that the paper itself missed.

## Suggestions

1. **Fix the PDAG evaluation.** Compare on CPDAG-level SHD (where undirected edges are treated as correct when either orientation is consistent), or complete PDAGs via BIC-constrained search rather than random orientation. At minimum, report directed-edge metrics only on edges that each method actually orients.
2. **Calibrate the significance claims.** The 20.9% vs. PC and 9.6% vs. GES numbers should not be presented as headline results without caveating the PDAG completion issue prominently.
3. **Justify the cost.** Provide a clearer discussion of when the computational overhead is warranted — e.g., identifying conditions where the 0.04 F₁ gain would be practically meaningful.
4. **Validate the core assumption directly.** Add small-scale experiments (bivariate/trivariate systems) that isolate whether Shapley asymmetry actually tracks causal direction under controlled conditions.
5. **Report complete statistics.** Include confidence intervals or standard deviations for Table 4, and specify the default confidence threshold $\tau$.

## Score and Decision

| Round | Anchor | Path | Avg Score | Itemized | Comparison to paper under review |
|-------|--------|------|-----------|----------|----------------------------------|
| R1 | nSDOkm0SKo.md | Fin. markets news impact | 1.00 | No | Unrelated topic, not comparable |
| R1 | fSxiromxAq.md | Sparse Causal Model | 3.00 | Yes | Much weaker: vague method, limited evaluation, no theoretical grounding |
| R1 | TRHyAnInUC.md | D³PM diffusion CD | 3.25 | Yes | Similar issues with theoretical justification; splintered scores (6,1,3,3) |
| R1 | i5JfdnCob7.md | Optimal Kernel for score CD | 4.40 | Yes | Incremental over prior work; comparable evaluation quality |
| R1 | MVpvyeVeyI.md | Causal Bayesian Optimization | 3.40 | No | Tangentially related; different problem setting |
| R1 | hQ2TUZmse1.md | Shapley counterfactual | 7.00 | No | Different subfield (explanations, not discovery) |
| R2 | eqQFBnjjPP.md | ExDBN exact DBN | 4.00 | Yes | Comparable: clear method, decent evaluation, some gaps |
| R2 | orD5t7blqV.md | PIT Algorithm | 4.25 | Yes | Stronger theoretical grounding; narrower scope |
| R2 | JzFLBOFMZ2.md | LLM-supervised CSL | 3.20 | No | Weaker evaluation, mixed reviewer scores |
| R2 | G19piTjVYA.md | Diff. causal order | 4.00 | No | Comparable scope and quality |

The paper sits between the 3.0-level anchors (vague methods, poor evaluation) and the 4.0–4.5 anchors (clear contributions, some methodological gaps). Comparing itemized favorability: our paper's most negative items (PDAG issue at 2.71, cost-benefit at 2.29) are less extreme than ExDBN's most negative items (marginal novelty at −4.57, lack of grounding at −2.13), but our weakness count is higher. The paper exceeds the 3.0-level papers substantially in evaluation scope and method clarity. The PDAG evaluation flaw prevents a score above 4.5, as it undermines two of three headline claims.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>