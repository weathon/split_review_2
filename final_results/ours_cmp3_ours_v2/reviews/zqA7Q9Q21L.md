## Summary

This paper addresses pursuit-evasion games (PEGs) under partial observability with the goal of real-time, worst-case robust strategies. The authors: (1) prove that a DP algorithm for Markov PEGs maintains optimality under asynchronous evader moves (Theorem 2); (2) propose a belief preservation mechanism to handle partial observability, extending DP policies to observation-based policies; and (3) embed this mechanism into the EPG framework to train a GNN-based RL policy (R2PS) across diverse graphs, achieving real-time inference (O(n²m) GNN vs Õ(n^{m+1}) DP recomputation). Experiments compare against PSRO on real-world graph benchmarks.

## Strengths

1. **Well-motivated and practically relevant problem.** The paper identifies a genuine gap: existing graph-based pursuit-evasion methods either assume perfect information or are too slow for real-time use under changing graph structures. The combination of partial observability, worst-case training against optimal evaders, and real-time applicability is under-explored in the literature the paper engages with.

2. **Clean theoretical extension of DP to asynchronous moves (Section 3.1).** Lemma 1, Theorem 2, and Corollary 1 show that the distance table D from Algorithm 1 directly yields optimal strategies when the evader moves after seeing the pursuers' action. Equation (3) removes the inner minimization compared to (2) while preserving the minimax structure. This is a non-trivial extension of the prior DP analysis.

3. **Large empirical gap over the PSRO baseline on most test graphs.** In Table 2, R2PS consistently achieves substantially higher success rates than PSRO against the optimal asynchronous-move evader (DP_async) — e.g., Scotland-Yard: 0.76 vs 0.00, Downtown: 0.99 vs 0.03, Times Square: 0.95 vs 0.04. The gap is large enough across most graphs to suggest a real methodological difference.

4. **Inference-time advantage is clearly demonstrated.** The O(n²m) GNN inference vs Õ(n^{m+1}) DP recomputation complexity gap is quantified concretely in Table 3 (0.01s vs 33–139 seconds on large graphs). This directly supports the real-time applicability motivation and is convincingly shown.

## Weaknesses

### Fatal
None.

### Major

1. **No statistical uncertainty is reported for any result.** All success rates in Tables 1–4 are reported as single numbers, described as "averaged over 500 tests." No standard deviations, confidence intervals, or significance tests are provided anywhere in the paper. Several comparisons are close (e.g., Table 1 Grid Map: DP_belief 0.78 vs DP_Pos 0.59; Table 2 Ours vs PSRO on the Stay columns for several graphs). Without variance estimates it is impossible to assess whether observed differences are meaningful or within Monte Carlo noise. For a paper whose central claims rest on comparative evaluations, this is a significant evidential gap.

2. **The "worst-case robust" claim in the title, abstract, and conclusion is oversold relative to the evidence.** The paper's title and abstract claim "worst-case robust real-time pursuit strategies" without qualification. However, against the optimal asynchronous-move evader (DP_async), R2PS success rates include 0.38 (Hollywood Walk of Fame), 0.20 (Sagrada Familia), and 0.25 (The Bund) in Table 2. Against the best-responding evader (BR_async) — the closest evaluation to a true worst-case opponent — rates go even lower: 0.10, 0.20, 0.23, 0.27 on several graphs (Table 2). The paper provides no theoretical bound on the gap between the learned GNN policy and the optimal DP policy. The empirical evidence shows the policy is relatively strong compared to PSRO, not that it is robust in an absolute worst-case sense. The paper's own justification (line 268: "Since our worst-case zero-shot performance is clearly better than the PSRO policy...") defines robustness relative to a single baseline, which does not match the unqualified "worst-case robust" framing.

### Minor

3. **Missing RL-level ablation of the belief mechanism.** The belief mechanism is presented as a core contribution (contribution 2, Section 1), yet it is ablated only at the DP level (Table 1: DP_belief vs DP_Pos). No comparison is made at the RL level against an R2PS variant trained without belief (i.e., using only (s_p, Pos) as the GNN input, removing the belief entirely). Table 4 tests different belief update frequencies and known vs. unknown opponent policies, but never removes the belief mechanism entirely. Without this ablation, it is unclear how much of the RL-level gain is attributable to the belief mechanism versus other components (cross-graph training, DP guidance, GNN architecture).

4. **No comparison against EPG adapted for partial observability without the belief mechanism.** Since R2PS builds directly on EPG (Lu et al., 2025a) — embedding the belief mechanism into EPG's cross-graph training framework — a comparison against an EPG variant adapted for partial observability (without the belief mechanism) would directly isolate the marginal benefit of the paper's additions. The paper compares against PSRO, a different approach; EPG is the more direct predecessor and the comparison that would most cleanly demonstrate the paper's incremental contribution.

5. **PSRO baseline details are underspecified.** The paper states only that PSRO is trained with 10 iterations × 10,000 episodes per iteration. It does not specify the policy architecture, the RL algorithm used for best-response computation inside PSRO, or any hyperparameter choices for the baseline. Since the PSRO comparison is central to the paper's empirical claims (Tables 2–3), missing these details makes it harder to assess the fairness of the comparison.

6. **Training set composition is not analyzed.** The paper mentions using the Dungeon environment (150 graphs) plus random urban locations from Google Maps (150 graphs), but does not analyze structural properties (node count range, degree distribution, how these relate to test graphs). Since "zero-shot generalization to unseen graph structures" is a core claim, understanding the relationship between training and test distributions is important for interpreting the results.

### Trivial
None.

## Nice-to-Haves

- A comparison against a simple online planning baseline (e.g., QMDP, or a lookahead using the D table with the belief state) would help situate the contribution within the broader POMDP/planning literature.
- The transitivity argument in Section 4.1 ("half space is excluded... exponential level") is presented as informal intuition. The paper already frames it appropriately ("imagine that"), so this is purely a presentation note.

## Removed Points

These points from the input review are removed; treat them with caution:

- **"Information advantage (DP guidance) is a confound"** — The DP guidance is part of the proposed method, not a confound. R2PS is designed to leverage DP tables; this is the treatment, not an uncontrolled variable. Removing it would change the method being evaluated.
- **"Training budget asymmetry favors R2PS"** — R2PS trains on 300 separate graphs (∼333 episodes/graph) while PSRO trains on the 10 test graphs directly (10,000 episodes/graph). PSRO has the advantage of training directly on test data with far more episodes per graph. If anything, the asymmetry is conservative for the paper's claims.
- **"Observation timing ambiguity in Pos update"** — The paper's description is sufficiently clear: the evader moves asynchronously after the pursuers, and the Pos update reflects the pursuers' observations before the evader's move. The timing is internally consistent.
- **"First approach claim needs qualification about POMDP-based PEG work"** — The rules prohibit criticizing missing related work. The claim may or may not be valid; it cannot be assessed without exhaustive literature knowledge.
- **"Architecture mismatch as a confound"** — R2PS uses a GNN because it is designed for graph-structured inputs; the PSRO framework is agnostic to policy representation and could in principle use any architecture. The paper does not specify PSRO's architecture, which is a separate minor oversight (captured in weakness 5), but an architecture mismatch does not inherently make the comparison unfair.

## Novel Insights

Beyond the paper's own contributions, the review surfaces a notable disconnect between absolute and relative claims. The paper's empirical evidence consistently supports "outperforms PSRO trained directly on test graphs," which is a valid and practically meaningful result. But the title/abstract language ("worst-case robust") implies an absolute guarantee that the evidence does not support — the policy demonstrably fails on several test graphs against the optimal evader. This is a recurring pattern in RL-for-games papers where "robust" is used to describe training procedure (training against worst-case opponents) rather than verified policy properties. The distinction matters for practitioners: a strategy that works 20–38% of the time against the optimal evader is useful primarily as a fast approximation to the optimal DP policy, not as a standalone worst-case guarantee.

## Suggestions

1. **Report binomial confidence intervals or standard deviations** for all success rates. With 500 Monte Carlo trials, ±2% margins are trivial to compute and would substantially strengthen reliability claims.
2. **Add an RL-level ablation** training R2PS without the belief mechanism (using only (s_p, Pos) as GNN input).
3. **Calibrate the "worst-case robust" language.** The paper should more precisely claim "policies trained against worst-case optimal opponents with cross-graph generalization" rather than claiming the learned policy itself is worst-case robust. The title and abstract should reflect this nuance.
4. **Add the missing EPG-without-belief comparison** to isolate the contribution of the belief mechanism.
5. **Specify PSRO's architecture, RL backbone, and hyperparameters** used in the comparison.
6. **Analyze training set graph properties** (node count distribution, degree range, structural similarity to test graphs) to better characterize the zero-shot generalization claim.

## Score and Decision

<score>5.0</score>
<decision>Reject</decision>

**Calibration anchors (retrieved from /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/):**

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| Uj0h13lVrR (GFlowNet) | 1.00 | 1 | Unrelated topic; strong reject; not comparable |
| 5kMwiMnUip (LLM jailbreak) | 1.40 | 1 | Unrelated; strong reject |
| VRRuYBaq9u (GPO for POMDPs) | 3.25 | 1 | Rejected for lack of novelty vs existing work; R2PS has more original content (DP extension, belief mechanism) and is clearly stronger |
| KrtGfTGaGe (Wasserstein Believer) | 4.50 | 1 | Accepted (4.50, scores 1,5,6,6) with controversial assumptions; R2PS has clearer empirical results but less rigorous theory |
| Q00CO1Tm6M (POMDP Hardness) | 5.75 | 1 | Pure theory paper (Reject despite 5.75); different genre, hard to compare directly |
| 99tKiMVJhY (Dec-POMFC) | 6.33 | 1 | Accepted; has rigorous theory + experiments; stronger overall than R2PS |
| KD5nJUgeW4 (DRDA for POSGs) | 7.00 | 1 | Accepted; rigorous convergence proofs for POSGs; stronger theoretical contribution than R2PS |
| stUKwWBuBm (Tractable MARL) | 8.00 | 1 | Strong accept; top-tier theory+experiments; not comparable in quality |

**Round 1 bracket:** 4.0–6.0. The paper has real contributions (DP extension, belief mechanism, strong speed advantage) that place it well above the 3-range reject papers, but the missing statistical rigor and claim inflation prevent it from reaching the 6+ range where papers are accepted. The 5.0 score reflects a paper with solid foundations whose evidence presentation needs significant strengthening before it can be confidently accepted.