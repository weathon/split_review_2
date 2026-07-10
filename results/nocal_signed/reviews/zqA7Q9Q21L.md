## Summary

This paper presents R2PS, the first approach to worst-case robust real-time pursuit strategies in graph-based pursuit-evasion games (PEGs) under partial observability. The contributions are threefold: (1) proving that a DP algorithm for Markov PEGs maintains optimality under asynchronous moves by the evader; (2) proposing a belief preservation mechanism to extend DP policies to partial observability; (3) embedding this mechanism into the EPG cross-graph RL framework to train a GNN policy that generalizes zero-shot to unseen graphs with real-time inference.

## Strengths

- **Clearly identified gap.** The paper correctly identifies that prior graph-based PEG methods (EPG, Grasper) assume perfect information, and that partial observability with asynchronous adversarial evaders is both practically important and theoretically underexplored (Section 1, lines 23-24). This problem framing is well-motivated and sets up a genuine contribution.

- **Theoretical extension of DP to asynchronous moves (Section 3.1).** The proof that the distance table \(D\) from Algorithm 1 induces strictly optimal policies under asynchronous moves (Theorem 2, Corollary 1) is a nontrivial extension of the synchronous case. Lemma 1's minimax formulation clarifies why the same \(D\) table remains valid when the evader moves second — this is not obvious a priori.

- **Real-time inference advantage is convincingly demonstrated.** Table 3 shows RL inference at 0.007–0.01 seconds vs DP at 6–139 seconds on large graphs. The complexity gap (\(O(n^2 m)\) vs \(\tilde{O}(n^{m+1})\)) is analytically clear and the practical numbers confirm it. For dynamically changing graphs, this speed difference is decisive.

- **Consistent outperformance over PSRO.** In Table 2, R2PS beats PSRO on every test graph against every evader type, often by wide margins (e.g., against DP_async: 0.95 vs 0.04 on Times Square, 0.95 vs 0.11 on Sydney Opera House). Since R2PS is zero-shot and PSRO is directly trained on the test graphs, this is a genuinely competitive result.

## Weaknesses

### Fatal
None.

### Major

- **Missing EPG baseline.** The paper positions EPG (Lu et al., 2025a) as the SOTA for cross-graph PEG generalization and explicitly states it aims to extend EPG to partial observability (lines 23-25, 169). Yet the experimental comparison (Table 2) is against PSRO — a general game-theoretic RL method that, as the paper itself notes, "focuses more on its scalability rather than generalization capability" (line 23). An EPG-based baseline adapted with the same belief-preservation input would directly validate whether the proposed mechanisms (belief preservation + async-DP adversarial training) add value over EPG's base cross-graph framework. Without this comparison, the paper's claim to extend the SOTA is not directly supported by the experiments.

### Minor

- **Belief mechanism's uniform-prior assumption not critically examined.** The paper acknowledges (line 157) that the belief update uses a uniform prior over neighbors because the evader's policy is unknown, and Table 4 shows that using the true evader policy ("Known Opponent") substantially improves success rates (e.g., 0.82 vs 0.65 on Big Ben). However, the paper frames belief preservation as a principled abstraction mechanism (line 25) without analyzing how the uniform-prior assumption systematically degrades belief fidelity against the adversarial DP_async evader. Since the evader is provably optimal at escaping, the belief is systematically wrong at most timesteps. This limitation deserves more critical discussion rather than being treated as a bonus finding.

- **PSRO baseline tuning is unclear.** PSRO is trained for 10 iterations (10K episodes per iteration), which is a relatively shallow run. Against the DP_async evader, PSRO achieves exactly 0.00 success rate on 4 of 10 test graphs (Scotland-Yard, Hollywood, Sagrada Familia) and nearly 0.00 on Times Square (0.04) and The Bund (0.04) — see Table 2. A 0.00 rate across 500 tests suggests very weak learning, raising the question of whether PSRO's hyperparameters were tuned or a default configuration was used. Without convergence analysis or evidence of tuning, the headline "consistently outperforms PSRO" loses some force.

- **RL policy vs DP reference gap undiscussed.** On 3 of 10 test graphs (Sagrada Familia, The Bund, Hollywood Walk of Fame), R2PS underperforms its own DP_belief reference policy — e.g., 0.20 vs 0.36 on Sagrada Familia, 0.25 vs 0.57 on The Bund (compare Table 1 and Table 2). (On the other 7 graphs, R2PS outperforms DP_belief.) This mixed result is not discussed. Understanding whether the gap stems from GNN capacity, training convergence, or exploration noise would strengthen the paper's analysis.

- **No confidence intervals or variance reporting.** Success rates from 500 trials are reported without any measure of uncertainty in Tables 1, 2, and 4. While single-run evaluation is common in RL, variance information would help readers assess the stability of results — particularly for rates in the 0.20–0.50 range.

### Trivial

- **"Worst-case robust" framing.** Despite the title and abstract, success rates as low as 0.20 against the strongest evader (Sagrada Familia, Table 2) and 0.25 (The Bund) qualify what "robust" means in practice. The language is somewhat stronger than the evidence supports.

## Nice-to-Haves

- A behavioral cloning baseline (\(\beta=\infty\), pure imitation of the DP reference) would help isolate whether the adversarial RL component adds value beyond imitating the DP policy. The paper already compares \(\beta=0\) (pure RL) vs \(\beta=0.1\) (guided) in the learning curves (Appendix C.4), partially addressing this, but a pure-imitation baseline would make the comparison cleaner.
- Scalability tests (Table 3) with variance or multiple runs would strengthen the timing claims.
- Analyzing the DP_belief vs R2PS gap more systematically (capacity, convergence, or architectural limitations of the GNN) would be informative.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Training/test graph overlap concern.** REMOVED. The paper explicitly states at line 260: "Since our training process never comes across the test graphs." The critic's speculation that "Downtown Map" from Google Maps might overlap with the 150 random Google Maps training samples is directly contradicted by this statement.
- **Behavioral cloning as a "missing" baseline.** REMOVED as stand-alone weakness. The paper already compares \(\beta=0\) vs \(\beta=0.1\) in Appendix C.4, partially addressing this. Retained as a nice-to-have.
- **One-sided framing of R2PS vs DP_belief gap.** The critic noted only the 3 graphs where R2PS underperforms DP_belief, omitting the 7 graphs where R2PS outperforms it. The underlying concern (that the gap is undiscussed) is kept in Minor weaknesses above.

## Novel Insights

None beyond the paper's own contributions. The key insight — that the DP distance table remains optimal for asynchronous-move evasion, and that combining belief preservation with cross-graph RL produces real-time policies that generalize — is well articulated in the paper itself.

## Suggestions

1. **Add an EPG baseline.** Adapt EPG for partial observability (using the same belief-preservation input) and compare directly against R2PS. This is the single highest-leverage improvement and would directly validate the claimed extension of the SOTA.
2. **Report confidence intervals** for all success rates from the 500-trial evaluations.
3. **Discuss the R2PS vs DP_belief performance gap.** Analyze whether the gap on specific graphs is due to GNN capacity, training convergence, or exploration-exploitation trade-offs.
4. **Report PSRO convergence analysis.** Show learning curves or verify that increasing iterations does not significantly improve PSRO's performance.
5. **Qualify the "worst-case robust" language** to reflect the observed success rate range (0.20–1.00 against the strongest evader).

## Score and Decision

The paper makes a genuine contribution: it provides the first demonstration of zero-shot cross-graph generalization for pursuit-evasion under partial observability, with sound theoretical extensions and a convincing real-time inference advantage. The main experimental weakness — the absence of an EPG baseline — is significant but fixable, and does not invalidate the core contributions. The other concerns are minor or addressable. On balance, the paper merits acceptance with room for improvement in experimental validation.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>