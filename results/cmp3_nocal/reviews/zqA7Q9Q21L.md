## Summary

This paper presents R2PS, a method for learning real-time pursuit policies in graph-based pursuit-evasion games under partial observability. The approach combines three components: (1) a theoretical proof that a DP algorithm for Markov PEGs maintains optimality under asynchronous evader moves, (2) a compact belief-preservation mechanism (Eq. 4-7) that tracks possible evader positions with O(|V|) per-timestep complexity, and (3) a cross-graph RL training pipeline (adapting the EPG framework) that distills DP reference policies into a GNN policy capable of zero-shot generalization to unseen graphs. The key practical result is a 10,000x-100,000x inference-time speedup over DP recomputation.

## Strengths

1. **Impressive and concretely documented inference speedup.** The paper reports specific wall-clock times: 2+ minutes for DP rescheduling vs. < 1 second (CPU) and < 0.01 seconds (GPU) on graphs with n=1000 (Section 4.2), and similar gaps on large real-world graphs (Table 3). This 10,000x-100,000x speedup is the paper's clearest practical contribution and is supported by concrete, verifiable numbers.

2. **Well-designed belief preservation mechanism.** Rather than tracking full observation histories (exponential in the horizon), the paper compactly maintains a set Pos of possible evader positions (Eq. 4) and a belief distribution over them (Eq. 7), with O(|V|) per-timestep complexity. The ablation in Table 4 (where reducing belief update frequency degrades performance) and the consistent advantage of DP_belief over DP_Pos in Table 1 provide evidence that this mechanism does useful work.

3. **Clear problem framing.** The paper correctly identifies a genuine gap: EPG handles perfect-information cross-graph generalization but not partial observability, while existing RL methods for PEGs focus on scalability rather than graph-structure generalization. The motivation for the asymmetric observability model (pursuers have limited sensors, evader has global information) is well-suited to security applications.

## Weaknesses

### Fatal

None.

### Major

1. **"Worst-case robust" claim is not supported by the empirical results.** The paper uses "worst-case robust" in its title, abstract, contribution list, and conclusion (lines 9, 25, 30, 195, 268, 311, 313). Against the optimal DP_async evader, the RL pursuer's success rates are 0.38 (Hollywood), 0.20 (Sagrada Familia), and 0.25 (The Bund) in Table 2. Against the BR_async evader (trained to counter the RL pursuer's specific policy), these drop further to 0.10, 0.20, and 0.23. A strategy that fails 60–80% of the time against the worst-case opponent is not robust in any standard sense of the term. The paper appears to mean "trained against a worst-case evader" rather than "achieves high worst-case performance," but the title and abstract claim the latter without qualification. The comparison with PSRO (which scores 0.00 on several graphs) is not sufficient to warrant "worst-case robust" — being better than a near-zero baseline does not constitute robustness.

2. **The PSRO baseline comparison is inadequately specified and configured.** The paper provides minimal detail about the PSRO implementation (lines 240–241): it does not state whether PSRO uses the same GNN architecture, the same belief mechanism, or even how partial observability is handled. PSRO scores 0.00 against DP_async on 5 of 10 graphs — suspiciously low, suggesting the baseline may be poorly configured. Additionally: (a) PSRO is a population-based meta-game method; using it as a single-policy RL baseline is misaligned with its design. (b) 10 PSRO iterations are claimed without any convergence analysis. (c) The training paradigms differ substantially — PSRO trains 100K episodes per test graph while R2PS trains 100K episodes total across 300 training graphs, yet the paper draws a strong conclusion about superiority. Better baselines would include a PPO variant with the same GNN architecture and belief input (β=0 ablation), or the DP_belief policy as a non-learned reference.

3. **Belief update uses a uniform evader model inconsistent with the evaluation opponent.** The belief update (Eq. 7) defaults to a uniform distribution over neighbors for the evader's movement policy ν (line 157: "ν(v) is set to be a uniform distribution over Neighbor(v) by default"). However, in both training and evaluation, the evader is the optimal DP_async policy (Eq. 3), which is deterministic and adversarially non-uniform. The pursuer's belief therefore tracks where the evader *would be if it moved randomly*, not where the *actual* worst-case evader is. The paper acknowledges this (line 157) and evaluates the known-opponent case (Table 4), which improves results — but the default setup means the core evaluation relies on a systematically misspecified belief. This weakens the claim that the method "handles" partial observability against worst-case opponents.

### Minor

1. **Training set composition is underspecified.** The paper states the training set contains 150 synthetic graphs (from Dungeon) and 150 Google Maps urban locations, but gives no details about graph sizes, average degrees, diameters, or diversity metrics. Without understanding the training distribution relative to the test graphs, the claim of "zero-shot generalization" is difficult to evaluate (lines 238-239).

2. **No discussion of limitations.** The paper has no limitations section, and the conclusion does not acknowledge any weaknesses. The belief inconsistency (Weakness #3), the performance drop on several real-world graphs (Weakness #1), and the scalability gap (Table 3 success rates dropping to 0.33–0.56 on large graphs) are all worth explicit discussion.

3. **BR_async training procedure is not described.** The best-response evader used as the hardest test opponent is mentioned (line 266, Table 2) but no details are given about its training algorithm, architecture, or convergence criteria. This matters because BR_async results are used to argue robustness.

4. **No confidence intervals or error bars.** All success rates are reported as point estimates (500 tests for Table 1; unspecified for Table 2). Reporting variance would strengthen comparisons.

5. **The policy space transitivity intuition (lines 195–196) is hand-wavy.** The geometric analogy ("half space is excluded after each single-graph division") is not supported by formal results and does not add rigorous justification for the cross-graph approach.

### Trivial

None.

## Nice-to-Haves

- Report standard errors or confidence intervals for the main success-rate tables.
- Add a non-learned baseline: the DP_belief policy (Table 1) as a reference on the test graphs under the RL evaluation protocol (Table 2). This would isolate the contribution of RL training vs. the DP policies.
- Add the β=0 ablation (RL without DP reference guidance) as a cleaner baseline than PSRO.
- Provide more detail on the training graph distribution (sizes, degree statistics, structural diversity).

## Removed Points

- **Asymmetric observability not sufficiently motivated**: The paper does motivate this in Section 2.1 (line 49, line 37-38) by noting the worst evader can have good predictions. The motivation is adequate for the security application the paper targets. *Removed: paper already addresses this.*
- **The theoretical contribution is disconnected from the main method**: The theoretical result (Theorem 2, Corollary 1) directly justifies using the DP evader as the optimal training opponent under asynchronous moves. This is a supporting foundation, not a disconnected addition. *Downgraded: not a core weakness.*
- **Missing appendix content**: The parser strips appendix content from all papers. The original submission contains these sections. *Removed per hard rules.*

## Novel Insights

None beyond the paper's own contributions. The reviews surface two observations worth noting: (1) the belief mechanism's uniform-movement assumption is a practical approximation that could be improved by using the known DP evader policy during training; (2) the paper's use of "worst-case robust" conflates a property of the training procedure (training against an optimal opponent) with a property of the results (achieving high worst-case performance), which the empirical evidence does not fully support. These are useful diagnostic points for revision rather than novel analytical insights.

## Suggestions

1. **Reframe the core claim.** Either (a) drop "worst-case robust" from the title and replace with "real-time pursuit under partial observability with cross-graph generalization," or (b) clearly define the term to mean "trained against worst-case opponents" and acknowledge that absolute capture rates remain modest on several graphs. The current framing invites rejection that the substance of the paper does not warrant.

2. **Fix the belief inconsistency for the main results.** Since the DP evader's true policy ν* is known during training (it is computed by Algorithm 1), use it for belief propagation rather than the uniform default. Table 4's "Known Opponent" column shows this improves performance. Reporting this as the default would strengthen the method.

3. **Replace or augment the PSRO baseline.** Add (a) the DP_belief policy applied to the RL evaluation protocol, and (b) a PPO/SAC baseline with the same GNN architecture, belief input, and training budget as R2PS but without DP guidance (β=0). This would isolate the contribution of the reference-policy distillation.

4. **Add a limitations section** addressing the belief approximation, the performance ceiling on several graphs, and the scalability constraints.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>