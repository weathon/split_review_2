## Summary

This paper proposes TrojanTO, the first action-level backdoor attack against trajectory optimization (TO) models in offline RL. The key insight is that existing RL backdoor attacks rely on reward manipulation during training, which is ineffective for TO models that learn via reconstruction loss over sequences. TrojanTO is a post-training attack that uses trajectory filtering, batch poisoning, and alternating training to implant backdoors with a very low poisoning rate (0.3%). The evaluation covers three TO architectures (DT, GDT, DC) across six D4RL environments.

## Strengths

- **Novel attack paradigm for an underexplored setting.** The paper correctly identifies that existing RL backdoor attacks (which rely on reward manipulation during training) do not transfer to trajectory optimization models. The post-training attack vector is well-motivated, and the paper empirically validates this motivation by showing that reward manipulation has negligible effect on TO models (Section 4.3, Figure 1).

- **Broad evaluation across three TO architectures (DT, GDT, DC) and six D4RL environments spanning locomotion, navigation, and manipulation.** This breadth demonstrates TrojanTO is not narrowly tuned to a single architecture.

- **Low poisoning rate (0.3%) is a genuine differentiator.** Even accounting for definitional differences with pre-training attacks, achieving high ASR with very few poisoned trajectories is the paper's most practically relevant finding.

## Weaknesses

### Fatal
None.

### Major

- **The ASR threshold ε (Equation 2) is never stated.** ASR is defined as the proportion of triggered steps where every component of the output action is within ε of the target action. In continuous action spaces, this choice is decisive — ε = 0.01 means near-exact output, while ε = 0.5 means barely steering in the right direction. Without this value, the reader cannot calibrate what "ASR = 1.000" actually means, and the central comparison in Table 4 rests on an incompletely specified metric. This is the single most important omission in the paper.

- **The threat model states the adversary operates "without access to the original training dataset" (Section 3.3) but TrojanTO's trajectory filtering and batch poisoning modules rely on trajectory data from the D4RL datasets — the same datasets used to pretrain the victim models.** The paper does not explain how the adversary obtains this dataset under the stated assumptions. This needs clarification: either the threat model should acknowledge the adversary has access to representative (e.g., publicly available) trajectory data from the same distribution, or the method should explain how F_τ is obtained without violating the stated constraints.

### Minor

- **Table 4 (the primary results table) reports only point estimates averaged over three seeds, with no standard deviations or per-seed ranges.** The reader cannot assess whether TrojanTO's CP advantage over baselines is consistent across seeds or driven by outliers. Given that some baseline results show extreme values (e.g., IMC CP = 0.013 on DT Hopper, CP = 0.133 on DT Ant), variance information is needed to evaluate the comparison.

- **The paper compares TrojanTO's 0.3% poisoning rate against Baffle's 10% poisoning rate as if on the same scale.** Baffle is a pre-training data poisoning attack (10% of training trajectories are adversarial), while TrojanTO is a post-training model modification attack with a fundamentally different mechanism. The 0.3% figure is also ambiguous — it is unclear whether this is 0.3% of the original dataset trajectories or 0.3% of the filtered set F_τ. The comparison should be framed transparently as different attack paradigms with different resource requirements.

- **Trigger dimensions (1,2,3) were selected by evaluating ASR on HalfCheetah and Walker2d (Table 2) and then fixed for the main evaluation, which includes those same environments.** This is not a held-out selection. The paper should clarify whether the main results on HalfCheetah and Walker2d would be affected if trigger dimensions were chosen via a principled method or on a held-out set.

- **The defense section (Section 6.5) states qualitatively that fine-tuning is the most effective defense while other methods are ineffective, but defers all quantitative results (post-defense ASR/BTP) to Appendix B.1.** Reporting these numbers in the main text would strengthen the analysis.

### Trivial
None.

## Nice-to-Haves

- Show ASR as a function of ε (e.g., a sweep from ε = 0.001 to ε = 1.0) to calibrate the reader and demonstrate the attack's precision.
- Reframe the Baffle comparison to clearly distinguish pre-training vs. post-training paradigms rather than presenting both on a single "poisoning rate" axis.

## Removed Points

These points from the input review were removed with justification:

- **Target action '1' meaning:** The harsh critic questioned what '1' means in continuous action spaces. The paper states these are boundary actions and references Appendix Table 17 for specific values. This is adequately addressed. **Removed because the paper provides the details via an appendix reference.**
- **Trigger applied only to most recent state:** The critic questioned this design choice. This is standard in trigger-based attacks and does not require extensive justification. **Removed as a nitpick.**
- **Trajectory filtering assumption about longer trajectories:** The critic questioned whether longer trajectories are indeed better. This is a reasonable heuristic, and the ablation study (Table 5) confirms the component contributes positively. **Removed as overly nitpicky.**
- **Formatting/style issues:** None present.
- **Reproducibility nitpicks:** None applicable beyond the ε threshold which is kept as a Major weakness.

## Novel Insights

None beyond the paper's own contributions. The reviews surface standard concerns (missing metric parameter, threat model clarification, variance reporting) rather than providing new analytical insights about the method itself.

## Suggestions

1. **State the ASR threshold ε** explicitly in Section 3.4. Consider showing ASR as a function of ε to calibrate interpretation.
2. **Clarify the threat model** regarding data access: either relax the "no access to original training data" claim to acknowledge the adversary can use public or representative trajectory data, or explain how F_τ is obtained without violating the stated constraints.
3. **Add standard deviations** or per-seed ranges to Table 4.
4. **Clarify the 0.3% poisoning rate:** state whether this is relative to the original dataset or the filtered set F_τ.
5. **Report post-defense ASR and BTP numbers** in the main defense section.

## Score and Decision

The paper addresses a genuine and underexplored problem, the method is well-motivated, and the evaluation is broad. However, the unstated ASR threshold ε makes the primary metric incompletely specified, and the threat model contains an unresolved inconsistency regarding data access. These issues are fixable but must be addressed. The paper should be considered for acceptance after these clarifications.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>