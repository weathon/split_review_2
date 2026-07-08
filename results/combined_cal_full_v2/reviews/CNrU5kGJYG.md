Now I have all the pieces. Let me compose the final consolidated review.

---

## Summary

This paper introduces TrojanTO, the first systematic study of action-level backdoor attacks against Trajectory Optimization (TO) models in offline reinforcement learning. The authors identify that existing RL backdoor attacks relying on reward manipulation are ineffective against TO models (which use sequence modeling and reconstruction loss), and propose a post-training attack framework combining trajectory filtering, batch poisoning, and alternating training to implant action-level backdoors using only 0.3% poisoned trajectories. The method is evaluated across three TO model architectures (DT, GDT, DC) and six D4RL environments.

## Strengths

- **Problem novelty and motivation** (weight: 7.32). The paper identifies a genuine gap — existing RL backdoor attacks rely on reward manipulation during training, which is fundamentally incompatible with Trajectory Optimization models that use sequence modeling and reconstruction loss rather than Bellman-style reward maximization. The paper is the first to systematically study action-level backdoors in TO models (Section 4.3, Figure 1).

- **Empirical grounding of design decisions** (weight: 8.78). Sections 4.1–4.3 provide a clean empirical investigation of three key factors (target action, trigger design, reward manipulation) before the method is introduced. The finding that reward manipulation has negligible impact on TO model backdoors (Section 4.3, Figure 1) directly motivates the design, and the demonstration that target action choice significantly affects ASR (Table 1) justifies evaluation across multiple target action types.

- **Attack efficiency** (weight: 9.77). TrojanTO achieves an average ASR of 0.719 with only a 0.3% poisoning rate, compared to Baffle's 0.369 ASR at 10% poisoning (Table 4). This two-order-of-magnitude reduction in required attack budget is a meaningful practical advance.

- **Architectural breadth** (weight: 8.36). The method is evaluated across three distinct TO model families (DT, GDT, DC) and six D4RL environments spanning locomotion, navigation, and manipulation tasks. The consistent improvement over baselines (Table 4, averaged CP of 0.701 vs. 0.551 for IMC and 0.342 for Baffle) demonstrates general applicability.

## Weaknesses

### Major

- **Baffle comparison uses action-level metrics for a policy-level method without adaptation details** (weight: 1.84). The paper labels Baffle as a "policy-level" backdoor (Section 3.2) that aims to make an agent follow a malicious policy, not output a specific target action. Yet Table 4 evaluates Baffle using the same action-level ASR metric (Equation 2) that measures whether the output action matches a predefined target action within a threshold. The paper does not explain how Baffle was adapted for action-level evaluation, if at all. This raises questions about the fairness of the comparison, and the headline claim of "105% improvement over Baffle" (Section 6.1) rests on this comparison. The paper should either (a) describe how Baffle was adapted for action-level attacks, (b) acknowledge the objective mismatch and interpret the comparison accordingly, or (c) provide a separate policy-level metric alongside the action-level comparison.

### Minor

- **CP discrepancy reveals hidden variance unacknowledged by the paper** (weight: 6.97). The paper states that CP is computed per-run and then averaged (line 98), which is transparent. However, comparing reported CP against CP computed from mean ASR and mean BTP reveals extreme discrepancies for some baselines. For example, IMC on DT+Hopp: mean ASR=0.162, mean BTP=0.576 → CP-from-means ≈ 0.253, but reported CP = 0.013 — a ~20× gap. This indicates catastrophic per-instance instability that the paper only partially acknowledges ("the CP of IMC drastically reduces to a mere 0.013"). Reporting standard deviations or discussing what the CP discrepancy reveals about method stability would strengthen the paper — and would actually support TrojanTO's robustness claim.

- **Ambiguity in threat model regarding trajectory source** (weight: 3.91). Section 3.3 states "the adversary aims to implant a backdoor into the pretrained TO model without access to the original training dataset." Yet TrojanTO's trajectory filtering (Section 5.1) and batch poisoning (Section 5.2) operate on a dataset of trajectories at a 0.3% poisoning rate. The paper never clarifies where these trajectories come from — whether the attacker uses a public dataset (e.g., D4RL) as a proxy or collects their own task-specific data. This ambiguity weakens the threat model characterization and should be clarified.

- **Trigger dimension selection validated in only two environments** (weight: 4.67). Table 2 shows the trigger dimension ablation for only Half and Walk environments. The choice of dimensions (1,2,3) is fixed for all subsequent experiments, but its optimality in other environments (Ant, Kit, Pen, Hopp) is not demonstrated in the main text.

- **Table 4 lacks error bars while other tables include them** (weight: 6.66). Tables 6 and 7 report ± standard deviations, but Table 4 (the main results table) shows only point estimates averaged over three seeds. Reporting variance would help assess the reliability of the claimed improvements, especially given the CP discrepancies noted above.

### Trivial

None.

## Nice-to-Haves

- Specify the ε threshold for ASR in the main text alongside Equation (2), or add a cross-reference to where it is defined.
- Include a brief discussion of what the per-run CP vs. CP-from-means spread reveals about method stability.
- Add standard deviations or confidence intervals to Table 4 to match the presentation in Tables 6–7.

## Removed Points

- **ASR threshold ε not specified** — The critic noted that the ε value in Equation (2) is not stated in the main text. This information is likely present in the appendix (which the parser strips from the submission). Per the guidelines, weaknesses about content deferred to the appendix that exists in the original submission are not evaluated against the paper. If ε is absent from the full submission, it would be a legitimate fix; as presented to us, this cannot be confirmed.

- **Defense section is thin** — The defense analysis (Section 6.5) defers details to Appendix B.1 with one summary sentence in the main text. This is an acknowledged presentation choice; the concrete results exist in the appendix of the original submission.

- **Reward manipulation analysis limited to one environment (Walk)** — Figure 1 shows only Walk, but the paper states "More results are provided in Appendix K.1." This is deferred to the existing appendix.

## Novel Insights

The most insightful observation from the review process is the CP discrepancy analysis. The paper explicitly computes CP per-run before averaging, yet the extreme gap between reported CP and the CP computed from mean ASR/BTP for some baselines (e.g., IMC DT Hopp: 0.013 vs ~0.253) is a hidden signal of per-instance instability. The paper could leverage this observation more directly as evidence of TrojanTO's reliability advantage, rather than merely reporting the lower CP values as a fait accompli.

## Suggestions

1. Clarify the Baffle evaluation protocol: describe how Baffle was adapted for action-level evaluation, or explicitly acknowledge the objective mismatch and reframe the comparison (e.g., as a motivational baseline showing that prior work designed for different objectives does not translate).
2. Add standard deviations or confidence intervals to Table 4.
3. Clarify the dataset source used for backdoor training (proxy dataset or self-collected trajectories) relative to the "no access to original training data" threat model assumption.
4. Report the ε threshold value for ASR in the main text alongside Equation (2), or add a cross-reference to where it is defined.
5. Include a brief discussion of per-run variance in ASR and BTP to contextualize the large CP discrepancies observed for some baselines.

## Score and Decision

**Calibration report.** Anchors retrieved across rounds:

| Path | Avg Human Score | Round | Itemized? | Comparison |
|------|----------------|-------|-----------|------------|
| S1Bv3068Xt (BALD) | 6.25 | R1 | Yes | Backdoor attacks on embodied LLM decision-making; closest in topic. BALD has stronger novelty framing and presentation but lacks the comparison-fairness concern this paper has. |
| em0gAL8fbK (Temporal Logic Offline RL Backdoor) | 4.00 | R1 | Yes | Backdoor in offline RL with 15% poisoning rate; the current paper is clearly stronger (0.3% rate, broader evaluation). |
| AKAlVyunxA (SHINE) | 5.75 | R1 | Yes | Backdoor defense in DRL; different focus but similar topic area. |
| vRyp2dhEQp (Efficient Backdoor) | 5.75 | R1 | Yes | Data-constrained backdoor attacks; similar theme of realistic threat models. |
| HZnnHDrBXD (Tree-based Action-Manipulation) | 5.75 | R2 | Yes | Attacks on continuous RL; comparable empirical scope but adds theoretical guarantees. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/c93SBwz1Ma (BadChain) | 5.25 | R2 | Yes | Backdoor on LLMs with no training data access; similar practical threat model. |

**Round 1 bracket:** The paper sits above the Temporal Logic Offline RL Backdoor anchor (4.00, high poisoning rate, narrow evaluation) and below BALD (6.25, comprehensive but different domain). Narrowest plausible range: 4.5–6.0.

**Round 2 narrowing:** Compared to Tree-based Action-Manipulation (5.75) and BadChain (5.25), the current paper has broader empirical evaluation (more environments, more model types) but lacks theoretical guarantees (present in the 5.75 anchor) and has the Baffle comparison concern. Its weighted items: strong positive weights on strengths (7.32–9.77), highest-weighted weaknesses are CP discrepancy (6.97) and missing error bars (6.66) — both fixable. The Baffle comparison issue carries a low weight (1.84), suggesting it is more of a framing/presentation concern than a fatal flaw.

**Final score:** 5.5. The paper presents a genuinely novel attack framework with strong empirical support. The main quantitative claim is somewhat overstated due to the Baffle comparison framing, and several minor clarity issues (dataset source, ε value referencing, variance reporting) prevent a higher score. These are addressable in revision.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>