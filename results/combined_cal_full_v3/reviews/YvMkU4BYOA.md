Now I have sufficient information for calibration. Let me compile my final review.

**Calibration Summary:**

| Anchor | Score | Decision | Comparison |
|--------|-------|----------|-----------|
| ExDBN (eqQFBnjjPP) | 4.00 | Reject | Incremental score-based BN method; XBIC has stronger novelty and empirical scope |
| PIT (orD5t7blqV) | 4.25 | Reject | Incremental PC improvement; XBIC has more novel contribution |
| D^3PM (TRHyAnInUC) | 3.25 | Reject | Weak theory, unclear benefits; XBIC is clearly stronger |
| DrBO (8muemqlnG3) | 6.50 | Accept | Score-based with BO; XBIC is weaker — DrBO has no fairness issues and stronger results |
| DAG-SHAP (ljZFM2mhbR) | 5.00 | Reject | Shapley+graphs (different problem); XBIC has similar-level flaws (lack of theory, limited analysis) |
| Optimal Kernel (i5JfdnCob7) | 4.40 | Reject | Highly incremental; XBIC is more novel |

**Round-1 bracket:** 4.0–5.5

Comparing my draft's items to anchors: My draft's two low-favorability weaknesses (PC comparison at 2.66, cost/benefit at 1.92) are comparable in severity to ExDBN's "limited comparison" (-1.76) and "marginal novelty" (-4.17), but my paper's strengths (favorability 8.50–10.07) are notably stronger than ExDBN's (7.28–8.33). DrBO at 6.50 had no structural evaluation flaws — my paper's PC comparison issue is a more serious problem than any DrBO weakness. This places the paper between ExDBN (4.00) and DrBO (6.50), around 4.5–5.5. The PC issue is the decisive factor: it undermines the headline claim but doesn't invalidate the core contribution. Final score: **5.0**.

## Summary

This paper proposes XBIC, a score-based causal discovery method for discrete Bayesian networks that augments the BIC score with Shapley-value-based directional evidence. For each variable, a classifier is trained to predict it from all others, and TreeExplainer computes feature attributions that are aggregated into an edge-specific signal. This signal soft-weights BIC's complexity penalty — edges with strong directional support are penalized less, while the score defaults to BIC when evidence is weak. Experiments on 10 benchmark networks (6–76 nodes) across 7 sample-size regimes (700 runs) show consistent F1 improvements over BIC-HC (5.6%), a GES variant (9.6%), and PC (20.9%), at substantial computational cost.

## Strengths

- **Clear, well-motivated targeted gap.** The paper correctly identifies that orienting edges within Markov equivalence classes is a persistent limitation of score-based discrete causal discovery (Section 2.1). Augmenting a score with asymmetric directional evidence is a natural strategy, and the method is designed around this motivation.
- **Principled design choices in the score modification.** The XBIC score (Eq. 2) is structured so that (i) when no directional signal is present (SHAP(G) ≈ 0) or the weight w = 0, XBIC reduces exactly to BIC; (ii) the penalty remains O(log N) in sample size, preserving BIC's asymptotic order. These are sensible properties that make the modification a genuine extension of BIC rather than an unrelated heuristic.
- **Thorough empirical scope.** The evaluation covers 10 benchmark networks (6–76 nodes), 7 sample-size regimes, 700 total runs, and three baselines (BIC-HC, PC, GES). This is a substantial and careful empirical study. The networks span multiple domains with varying structure, and the sample-size grid is well-chosen to probe data-limited and data-rich regimes.
- **Reproducibility commitment.** Code, data splits, and scripts are released. The hyperparameter search space for XGBoost is enumerated (Table 3), and the confidence threshold's sensitivity is examined.

## Weaknesses

### Major

- **The comparison against PC on oriented-edge F1 is unfair due to the random PDAG-to-DAG completion protocol.** The evaluation protocol (Section 4.1, line 190) states: *"For baselines that return a PDAG, we complete it to a DAG by randomly orienting undirected edges (while preserving acyclicity) before computing directed-edge metrics."* PC is designed to return a CPDAG that honestly represents ambiguity within a Markov equivalence class — the undirected edges are a feature, not a bug. Randomly orienting those edges injects noise into PC's directed-edge precision and recall. Since XBIC always outputs a fully directed DAG, it faces no such penalty. Consequently, the **20.9% average improvement over PC (Table 4) cannot be interpreted as a fair comparison**; a substantial fraction of this gap likely reflects the noise from random orientation. A fairer evaluation would use CPDAG-level metrics (adjacency F1, orientation F1 on oriented edges only, or SID) or a principled method to complete the PDAG. The paper's strongest headline number is unreliable.

- **The 5.6% improvement over BIC-HC comes at extreme computational cost that is under-discussed.** From Table 5, XBIC (w=2) is 50–602× slower than BIC-HC on small networks (Asia: 0.39s vs 74.78s, 192×; Survey: 0.09s vs 54.21s, 602×) and 28–47× slower on larger ones (Win95pts: 75.33s vs 2139.27s, 28×; Hepar2: 40.33s vs 1885.44s, 47×). For this cost, the average relative F1 improvement over BIC is 5.6% (absolute 0.04). The paper acknowledges the cost but describes it as "manageable for offline discovery," which undersells the magnitude. A 50–600× slowdown for a 0.04 absolute F1 gain is an unfavorable trade-off that limits practical adoption. The paper should discuss this more quantitatively (e.g., F1 per unit time or identifying specific regimes where gains are largest).

### Minor

- **The consistency argument (Section 3.3, lines 155–159) is heuristic, not a proof.** The paper argues that because the XBIC penalty still scales as O(log N) and reduces to BIC when SHAP(G)=0, it "preserves large-sample consistency." This requires verifying that the modified penalty satisfies specific conditions for BIC consistency theorems (e.g., the penalty difference between true and false models diverges at the right rate), which the paper does not do. The paper acknowledges this gap in Limitations, making it a minor issue rather than a fatal flaw, but the language overstates what has been established.

- **The evaluation does not cleanly separate orientation improvement from skeleton improvement.** The paper's stated goal is improving edge orientation within Markov equivalence classes, but oriented-edge F1 conflates skeleton errors with orientation errors: a missing edge is treated the same as an edge that is present but reversed. The gains in Table 2 could come partly from XBIC finding a better skeleton than BIC-HC, not from better orientation within the same skeleton. Reporting orientation F1 conditional on correct skeleton edges would directly test the core claim that Shapley evidence helps resolve Markov-equivalence-class ambiguity.

- **The confidence threshold τ used in the main experiments is never stated numerically.** Section 4.1 (line 194) mentions varying it between 0.7 and 0.95 and reports sensitivity < 1%, but the actual τ value used for the main results is not specified. This is a minor reproducibility gap.

### Trivial

None.

## Nice-to-Haves

- **Non-Shapley directional baseline.** To justify that Shapley values specifically — rather than any asymmetric predictive signal — provide the benefit, the paper could compare against a simpler measure of directional predictivity, such as asymmetric conditional mutual information or the difference in prediction error when predicting Xᵢ from Xⱼ vs. predicting Xⱼ from Xᵢ.
- **Guidance on choosing w in practice.** The paper sweeps w ∈ {1, 2, 3} and finds w=2 best on average, but provides no criterion for selecting w when ground truth is unknown. A practical recommendation (e.g., cross-validated likelihood, stability selection) would increase usability.

## Removed Points

These points are flagged to be removed; treat them with caution:

1. **Criticism about classifiers using all other variables potentially causing conditioning pathologies** — This is speculative without concrete evidence of harm. The paper uses a standard approach of predicting each variable from all others, common in causal discovery.

2. **Criticism about PC runtime on Hailfinder being suspicious** — The reviewer speculates about suboptimal CI test implementation without evidence. Removed as speculative.

3. **Criticism about GES comparison limited by 7-day cutoff** — The paper handles this transparently: it filters to runs where GES completed and compares head-to-head on identical subsets. This is reasonable.

4. **Criticism about needing broader baselines or missing related works** — Removed per hard rules.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Redesign the PC evaluation**: Use CPDAG-level metrics (adjacency F1, orientation F1 on oriented edges only, or SID) instead of randomly completing PDAGs. Honestly quantify how much of the 20.9% gain is real versus an artifact of random post-processing. If the gain over PC shrinks substantially under fair metrics, adjust the paper's claims accordingly.

2. **Report the cost-benefit trade-off quantitatively**: Compute F1 per unit wall-clock time or identify specific network/sample-size regimes where XBIC's gains are largest relative to its overhead. This would help practitioners decide when the method is worthwhile.

3. **Report orientation F1 conditional on correct skeleton edges**: This would directly test the core claim that Shapley evidence helps resolve Markov-equivalence-class ambiguity, independent of skeleton-finding ability.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>