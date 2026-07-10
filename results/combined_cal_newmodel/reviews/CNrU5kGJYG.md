Now I'll produce the final consolidated review.

## Summary

This paper introduces TrojanTO, a post-training action-level backdoor attack against trajectory optimization (TO) models (Decision Transformer, Graph Decision Transformer, and Decision ConvFormer) in offline RL. The authors first empirically demonstrate that existing reward-manipulation-based RL backdoors are ineffective against TO models due to their sequence-modeling nature. They then propose TrojanTO, which combines trajectory filtering, batch poisoning, and alternating training to inject backdoors with only 0.3% poisoned trajectories. The method achieves strong results (average ASR 0.719, BTP 0.914, CP 0.701) across six D4RL environments and three TO architectures.

## Strengths

- **Timely and underexplored problem.** The paper targets a genuine gap: backdoor attacks against TO models (DT, GDT, DC) are largely unstudied. The empirical finding (Section 4.3, Figure 1) that existing RL backdoor methods relying on reward manipulation are ineffective against TO models is a real and useful contribution that distinguishes this attack surface from standard RL backdoors.

- **Systematic decomposition of key factors.** The analysis in Section 4 into target action choice, trigger design, and reward manipulation is informative and actionable. Showing that target action selection dramatically affects ASR (Table 1: from 0.110 to 1.000 on Walk depending on target type) and that trigger dimension choice can make or break the attack (Table 2: ASR ranges from 0.000 to 0.915) provides practical guidance for anyone building on this work.

- **Strong empirical results on the paper's own terms.** Averaged across all settings, TrojanTO achieves ASR 0.719 with BTP 0.914 using only 0.3% poisoned trajectories. On several environment–model combinations (DT/Half, DT/Walk, DC/Half, DC/Walk) it reaches near-perfect ASR with negligible BTP degradation. Results are consistent across three TO architectures and six environments, which is reasonable breadth for a first paper on this problem.

- **Clean ablation study.** Table 5 clearly decomposes the contribution of each component (trajectory filtering, batch poisoning, alternating training), confirming that all three contribute positively and that the design choices are justified.

## Weaknesses

### Major

- **Baseline comparison conflates different threat models, overstating headline claims.** Baffle (Gong et al., 2024b) is a pre-training data-poisoning attack (10% poisoning rate, no model-weight access), while TrojanTO is a post-training attack with full access to pretrained model weights (0.3% poisoning rate). The paper acknowledges this distinction in Section 3.3, categorizing attacks by stage, but then presents Table 4 and the abstract as a head-to-head competition, claiming "105% improvement" over Baffle. Since the two methods operate under fundamentally different adversary capabilities (data-only vs. full-weight access), the headline superiority claims are overstated. The comparison with IMC (Pang et al., 2020) is similarly unclear — IMC was designed for image classification, and the main paper does not explain how it was adapted to the TO setting or what architectural modifications were made. This is a framing issue rather than an invalidation of the results: the core attack is credible, but the paper would be stronger if it presented TrojanTO on its own merits with a more carefully caveated comparison.

### Minor

- **The ASR threshold ε is not reported in the main text.** ASR is defined in Equation (2) using a threshold ε that determines whether each action component is "close enough" to the target. Without explicitly stating ε, the ASR numbers are not independently interpretable — a threshold of 0.01 would give very different results from 0.5 in a high-dimensional continuous action space. The main paper should report this value (or at minimum reference the specific appendix section).

- **The balancing parameter λ is not specified.** λ ∈ [0,1] balances the backdoor loss ℒₚ and clean loss ℒ_c in Equations (1), (7), and the final objective, and governs the stealthiness–effectiveness tradeoff. Its value is never stated in the main paper, and no sensitivity analysis appears in the main text (deferred to Appendix J).

- **Standard deviations are missing from the main results table (Table 4).** While Tables 6 and 7 include variance information (±), the primary comparison table lacks standard deviations, making it impossible to assess the statistical significance of TrojanTO's advantages over baselines. Given the hint of high variance (e.g., the per-run CP averaging that produces CP=0.000 for Baffle DT/Walk despite mean ASR 0.328 and BTP 0.581), variance reporting in the main table is needed.

- **The trigger dimension choice (1,2,3) may overfit to tested environments.** Table 2 shows that (1,2,3) performs best on Half and Walk, but the paper fixes this choice for all subsequent experiments without validating that it generalizes to other tasks (Ant, Kit, Pen). The "All Dimensions" row achieving ASR 0.000 is also striking and receives no discussion — it is unclear why adding more trigger dimensions completely kills the attack.

- **Trajectory filtering assumption not validated per environment.** The paper assumes "longer trajectories are more representative of successful behavior" (Section 5.1). This is environment-dependent — in tasks like AntMaze, long trajectories could indicate the agent getting lost rather than success. The paper does not empirically verify this assumption for each environment.

- **Optimized trigger values are not analyzed.** The trigger δ is optimized with clipping bounds (δ_min, δ_max) using MI-FGSM, but the paper does not report what the resulting trigger values look like, how large they are relative to state values, or whether they would be perceptible. In a supply-chain threat model, the trigger must be physically insertable into observations — a trigger requiring large perturbations may not be feasible.

- **The 0.3% poisoning rate could be clarified.** Is this 0.3% of the original dataset trajectories or 0.3% of the filtered set F_τ? Reporting absolute numbers of trajectories would help contextualize the "minimal budget" claim.

### Trivial

- None.

## Nice-to-Haves

- Add a simpler post-training baseline (e.g., direct fine-tuning on poisoned trajectories without TrojanTO's alternating training, trajectory filtering, or batch poisoning components) to better isolate the value of the method's specific design choices. The ablation study (Table 5) partially fills this role but a "naive fine-tuning" baseline would be cleaner.
- A brief discussion of whether weight-level access is realistic in the deployment scenarios described (e.g., API-based model serving) would strengthen the threat model discussion.
- Discuss backdoor detection (as distinct from mitigation) — e.g., whether the backdoored model can be detected through weight analysis or behavior on held-out data.

## Removed Points

These points were raised by the harsh critic but are removed or downgraded after cross-checking:

- **CP=0.000 anomaly for Baffle DT/Walk**: The reviewer calculated CP should be ~0.419 from mean ASR/BTP, but the paper explicitly states (line 98) that "CP is computed for each run based on its specific ASR and BTP, not a derivation from the mean ASR and BTP." The per-run averaging explains this; not an error.
- **Persistent backdoor limited by context window**: The paper acknowledges this limitation (line 307: "the maximum duration is fundamentally bounded by the TO model's finite context window"). This is an inherent property of the setting, not a weakness of the paper.
- **Averaging across target types inflates numbers**: The paper is fully transparent about per-type results in Table 1 and explains why diverse target actions are evaluated.
- **Defense section too brief**: Results are deferred to Appendix B.1. This is standard practice under page limits.
- **Missing appendix/proof content**: The parser strips appendix sections from all papers; they exist in the original submission.

## Novel Insights

The harsh critic's review surfaces one genuinely novel observation beyond the paper's own contributions: the paper's conceptual contribution is stronger than its empirical framing suggests. The finding that reward manipulation is ineffective against TO models (Section 4.3), combined with the systematic decomposition of which factors matter (target action > trigger design > reward), constitutes a useful conceptual framework for thinking about backdoors in sequence-modeling-based RL. The paper would benefit from foregrounding this framework more prominently rather than leading with the potentially overstated baseline comparisons.

## Suggestions

1. **Report ε and λ in the main paper** (or, if space is tight, include a clear pointer to the appendix section with a one-sentence summary of the values). Without these, the paper's quantitative claims are not independently verifiable from the main text.
2. **Reframe the baseline comparison.** Present the Baffle and IMC results as informative context rather than direct head-to-head competition. Make explicit that they operate under different (more constrained) threat models, and position TrojanTO's contribution primarily against its own design space (ablation study, varying targets, varying triggers).
3. **Add standard deviations to Table 4.** The primary results table is where readers assess the reliability of the claims.
4. **Add a brief discussion of the "All Dimensions" zero ASR result** and why trigger selection matters so dramatically.
5. **Discuss optimized trigger magnitude** to address the practical feasibility of trigger insertion in physical environments.

## Score and Decision

**Score calibration anchors** (all rounds):

| Anchor | Score | Round | Itemized | Comparison |
|--------|-------|-------|----------|------------|
| Temporal Logic Multi-Vehicle Backdoor (offline RL) | 4.0 (Reject) | R1 | Yes | Weaker than our paper: 15% vs 0.3% poisoning, more assumptions, less comprehensive evaluation. Our paper's major weakness is less severe than this anchor's (unrealistic assumptions, high poisoning rate). |
| Backdoor in Seconds (model editing) | 4.75 (Reject) | R1/R2 | Yes | Similar post-training setting but different domain. Our paper has comparable baseline-comparison concerns (favorability 0.19 vs 0.18) but stronger empirical breadth. |
| Efficient Backdoor Attacks (DNNs) | 5.75 (Accept) | R1 | Yes | Similar profile: practical attack scenario with solid results. Our strengths are comparable; our major weakness is more significant than this anchor's main weaknesses. |
| SHINE (DRL defense) | 5.75 (Reject) | R1 | Yes | Defense paper, different contribution type. Our paper has stronger specificity to TO models. |
| Less is More (clean-label backdoor) | 5.80 (Reject) | R1/R2 | Yes | Similar in having missing parameter details and baseline concerns. Our paper addresses a more novel problem domain (TO models vs image classification). |
| Multi-level Certified Defense (offline RL) | 6.75 (Accept) | R1 | Yes | Stronger than our paper: theoretical contributions with DP-based certification. Our paper doesn't reach this level of theoretical rigor. |

**Bracket determination (Round 1):** The paper falls between 4.0 (weaker anchors) and 5.75–6.75 (stronger anchors). Round 1 bracket: **5.0–6.5**.

**Narrowing (Round 2):** Comparing itemized favorability ratings: our strengths (10.09–12.11) are comparable to the 5.75 anchors (8.70–12.43) but below the 6.75 anchor (10.11–13.62). Our major weakness (favorability 0.19) is more impactful than the 5.75 anchors' weakest items (~−1.01 to −2.17) but less severe than the 4.0 anchor's worst (−2.72). Our minor weaknesses (−1.54 to 2.60) are comparable in severity to the 5.75 anchors' minor issues. The paper's core contribution (first post-training backdoor for TO models, validated reward-ineffectiveness finding, strong results across 3 architectures) is solid but the baseline framing issue pulls the score below the 6.0+ range.

**Final placement:** The paper's contribution is genuine but the headline claims are overstated relative to the evidence presented. The weaknesses are fixable through better framing and minor additions, not structural. Calibrated against the anchors, the paper sits between the 4.0–5.0 reject-level backdoor papers and the 5.75–6.0 accept-level papers, closer to the latter.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>