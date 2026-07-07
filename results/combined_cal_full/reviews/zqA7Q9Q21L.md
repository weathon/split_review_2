I have good calibration data. Let me now construct the final review.

## Summary

This paper addresses the problem of computing worst-case robust pursuit strategies in graph-based pursuit-evasion games (PEGs) under partial observability, where pursuers have limited sensing capabilities but face an evader who can observe globally and move asynchronously (after seeing the pursuers' actions). The paper makes three contributions: (1) a theoretical proof that a dynamic programming (DP) algorithm for Markov PEGs induces optimal strategies under asynchronous moves (Theorem 2, Corollary 1); (2) a belief preservation mechanism (Eqs 4–7) that efficiently summarizes observation histories to extend DP policies to partial observability; and (3) an integration of this mechanism into the EPG reinforcement learning framework to produce a cross-graph GNN-based pursuer policy (R2PS) that achieves strong zero-shot generalization to unseen graphs, with real-time inference speeds orders of magnitude faster than recomputing DP policies.

## Strengths

- **Theoretical extension of DP to asynchronous moves (Section 3.1, Theorem 2, Corollary 1).** The paper proves that the distance table D produced by Algorithm 1 induces strategies that are optimal for both pursuer and evader under asynchronous moves — i.e., when the evader moves after seeing the pursuers' actions. Theorem 2 is the key result: starting from state s with D(s) = d < ∞, μ* guarantees capture within d steps against any evasion strategy, and ν* guarantees evasion for at least d steps against any pursuit strategy. This is a genuine theoretical contribution that cleanly extends prior work.

- **Belief preservation mechanism (Section 3.2, Equations 4–7).** The belief-averaged policy (Equation 6) is a principled and computationally efficient (Õ(|V|) per timestep) way to handle partial observability that avoids the exponential blowup of recording full observation histories. The empirical result that DP_belief consistently outperforms DP_Pos across all 10 test graphs (Table 1) convincingly demonstrates that belief averaging adds value beyond the direct minimax position-extension.

- **Strong empirical results against a meaningful baseline (Table 2).** The R2PS policy achieves substantially higher success rates than a PSRO policy trained *directly on the test graphs* across nearly all graph/opponent combinations. Against the strongest standard opponent (DP_async), the advantage is often dramatic (e.g., Scotland-Yard: 0.76 vs 0.00; Times Square: 0.95 vs 0.04). This is a genuinely impressive demonstration of zero-shot cross-graph generalization — the R2PS policy never saw these graphs during training yet outperforms a policy that was trained on them.

- **Practical real-time inference (Table 3, Section 4.2).** The complexity analysis is clear and the empirical inference times (≤0.01 seconds on GPU for graphs with 744–2065 nodes) are orders of magnitude faster than recomputing DP policies (which takes minutes). This closes a real practical gap identified in the introduction.

## Weaknesses

### Major

- **"Worst-case robust" overclaiming relative to evidence.** The paper repeatedly uses "worst-case robust" in the title, abstract, and conclusion (e.g., lines 5, 9, 25, 170, 313: "the first approach to worst-case robust real-time pursuit strategies," "derive the first worst-case robust real-time pursuit strategies (R2PS)"). However, the method does not provide worst-case guarantees in the game-theoretic sense. The RL policy is trained against specific DP-optimal evader policies — a strong but limited subset of all possible evader strategies. The BR_async results (Table 2, rightmost column) reveal that when an evader is adversarially trained *specifically against the R2PS policy*, success rates drop substantially — to 0.10 on Hollywood Walk of Fame, 0.20 on Sagrada Familia, 0.23 on The Bund. This means a motivated adversary who studies the R2PS policy can find exploitable weaknesses. The technical contribution (zero-shot cross-graph generalization against DP-optimal evaders under partial observability) is real and valuable, and does not need the stronger claim. The paper would be better served by more precise language such as "robust against optimal DP evaders" or "adversarially robust pursuit strategies."

### Minor

- **Missing variance/confidence information.** All success rates in Tables 1–4 are reported as point estimates without standard deviations, confidence intervals, or statistical significance tests. These are averaged over 500 trials (Table 1) — ample data to compute meaningful error bars. Without this information, the reader cannot assess whether the observed differences between methods are reliable or within the noise of random initial positions and policy stochasticity.

- **Tension between belief uniformity assumption and worst-case framing.** The belief update (Equation 7) uses a uniform distribution over Neighbor(v) for the evader policy ν by default (line 157: "ν(v) is set to be a uniform distribution over Neighbor(v) by default"), justified by lack of prior knowledge. In a setting claiming worst-case robustness, the evader should be adversarial, not uniformly random. A belief that assumes random movement may systematically diverge from the true distribution when the evader is actively evading. The paper acknowledges this default and shows in Table 4 that using the actual opponent policy improves results, but does not address whether the uniform assumption could lead to pathologically wrong beliefs that undermine the policy. This tension with the "worst-case" narrative is discussed only superficially.

- **Heuristic "exponential improvement" argument (Section 4.1).** The paper states "Imagine that a half space is excluded after each single-graph division… the cross-graph policy will be improved at an exponential level" (line 195). This is explicitly framed as an ideal case and an imagination, but the language is more evocative than precise for a research paper. The argument about policy space transitivity and the claimed exponential improvement is not formally justified.

### Trivial

None.

## Nice-to-Haves

- A comparison or ablation relative to the predecessor method EPG (which operates under perfect information) could help isolate how much of R2PS's performance comes from the cross-graph RL framework versus the belief preservation mechanism. Since EPG cannot handle partial observability directly, even a perfect-information comparison would provide useful context.
- Clarify the exact initialization value for the belief function (it is stated as "0 except for the initial evader position" but the value assigned to the initial position is not specified).
- Report whether the PSRO baseline with 10 iterations had converged, or discuss how additional iterations might affect the comparison.

## Removed Points

These points from the harsh critic review were removed with justification:
- **Missing EPG baseline comparison:** EPG operates under perfect information, not partial observability. Comparing R2PS (partial observability) against EPG (perfect information) would test different settings. The PSRO baseline is the correct general game-theoretic RL baseline for this setting. Moved to Nice-to-Haves.
- **Missing appendix content / unverifiable proofs:** Removed per filtering rules — appendix sections are stripped by the parser and not part of the submission body.
- **Reproducibility concerns about redacted code URL and hyperparameters:** Removed per filtering rules about reproducibility nitpicks.
- **Notation ambiguity in Equation (7):** Trivially minor presentational point that does not affect evaluation.
- **"Game extension" complexity observation:** This is a description of the problem setting, not a weakness of the paper.
- **LLM comparison reference:** The reviewer noted the LLM comparison is "odd and unnecessary" — this is a minor stylistic preference, not a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Reframe the "worst-case robust" terminology throughout to match what is actually demonstrated. The paper's genuine contribution is a method for zero-shot cross-graph generalization against provably strong (DP-optimal) evaders under partial observability. Replacing "worst-case robust" with more precise language like "robust against optimal DP evaders" or "adversarially robust pursuit strategies" would not weaken the contribution — it would make the claims match the evidence.
- Add standard deviations or confidence intervals for all success rates in Tables 1–4. With 500 trials per condition, error bars of at most ~±2 percentage points would be expected.
- Discuss the belief uniformity assumption's impact on worst-case behavior more directly, or provide empirical analysis showing the gap between uniform-belief and true-policy-belief is small on the tested graphs.

## Score and Decision

**Bracket analysis (Round 1):** Based on calibration, the paper sits between the 5.5–7.5 band. The closest topical anchors are:
- *Beyond Worst-case Attacks* (7.00) — similar in having a gap between "worst-case" framing and actual evidence, but weaker writing. **Itemized:** that paper's strengths had weights +7.90, +8.44, +4.71 and weaknesses -5.07, -5.35, -8.06. The current paper has stronger positive weight density (four items averaging +5.60) and much weaker negative weights (none below -0.43), indicating a cleaner contribution.
- *Sample Efficient Robust Offline Self-Play* (5.60) — had strong theory but significant novelty concerns (-10.06, -9.18). The current paper has no such novelty concerns.
- *Can RL Solve Asymmetric Combinatorial-Continuous Zero-Sum Games?* (6.50) — similar structure (theory + RL), with mixed novelty concerns (-6.20, -8.46). The current paper has stronger empirical validation and no novelty concerns.
- *Structured Predictive Representations in RL* (4.80) — had GNN+RL angle but weaker empirical demonstration and limited baselines. The current paper is substantially stronger.

**Final score:** The paper's strengths (theoretical extension of DP, novel belief mechanism, strong zero-shot generalization results, practical real-time inference) are well-supported and carry heavy positive weight. The weaknesses are primarily about framing and presentation rather than technical flaws. The most significant weakness — overclaiming "worst-case robust" — is a framing issue that can be corrected without altering the technical contribution. The paper is a solid **borderline accept**: it makes genuine theoretical and practical contributions to the PEG literature, with strong empirical validation, but the claims need to be calibrated to match the evidence.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>