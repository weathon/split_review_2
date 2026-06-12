## Summary

This paper proposes TrojanTO, the first action-level backdoor attack specifically designed for Trajectory Optimization (TO) models in offline reinforcement learning. The authors identify that existing RL backdoor methods fail against TO models due to their sequence modeling nature and training objective based on reconstruction loss rather than reward maximization. TrojanTO is a post-training attack that uses trajectory filtering, batch poisoning, and alternating training to embed backdoors with extremely low poisoning rates (0.3% of trajectories), achieving high attack success rates while maintaining benign task performance across multiple D4RL environments and TO architectures (DT, GDT, DC).

## Strengths

- **Novel and well-motivated problem.** This is the first systematic study of action-level backdoors in offline RL for Trajectory Optimization models. The paper clearly identifies why existing backdoor attacks (which manipulate rewards during training) are incompatible with TO models, establishing a new and practically relevant threat vector in a growing area of RL.

- **Comprehensive empirical analysis of key factors.** Section 4 provides a thorough investigation into how target action selection, trigger design (dimensions and values), and reward manipulation affect backdoor efficacy in TO models. This analysis is informative and directly motivates the design choices in TrojanTO, particularly the finding that reward manipulation is negligible (Figure 1), which is a non-obvious and important insight.

- **Strong experimental results across diverse settings.** TrojanTO achieves an average CP of 0.701 across six D4RL environments and three TO model architectures, substantially outperforming Baffle (0.342) and IMC (0.551). The attack maintains high ASR with only 0.3% poisoning rate (versus 10% for Baffle), demonstrating both effectiveness and stealth. The ablation study in Table 5 cleanly validates the contribution of each component.

- **Thorough evaluation of attack properties.** The paper goes beyond basic metrics by examining persistent backdoor attacks (Section 6.3), robustness to trigger perturbations (Section 6.4), and initial defense analysis (Section 6.5). These additional experiments strengthen the practical relevance of the threat model.

## Weaknesses

### Fatal

None.

### Major

- **Threat model ambiguity regarding dataset access.** Section 3.3 states the adversary "modifies the pretrained TO model without access to the original training dataset," yet the attack uses filtered trajectories from the same offline RL dataset (e.g., D4RL) for backdoor training. This creates a contradiction: if the adversary can access any offline RL dataset, why not the original training dataset? The paper should clarify whether the adversary uses a separate public dataset or has partial access to training data, and discuss how this affects the practical applicability of the threat model.

- **Defense analysis is too shallow for a security paper.** Section 6.5 only states that "fine-tuning is the most effective defense" and relegates all details to the appendix. Given that backdoor attacks are a security area where defenses are a standard part of evaluation, the paper should include quantitative defense results in the main paper and discuss why other defenses fail. The current treatment is insufficient to substantiate the claim that TrojanTO is robust to existing defenses.

### Minor

- **Baseline comparison fairness.** Baffle is a pre-training attack with 10% poisoning rate, while TrojanTO uses 0.3%—this is an asymmetric comparison that inflates the apparent advantage. The paper acknowledges this as demonstrating "superior stealth," but a normalized comparison (e.g., CP per unit poisoning rate or a baseline adapted to post-training) would be more informative. IMC was originally designed for image classifiers, not RL; its performance degradation may partly reflect mismatch rather than inherent weakness.

- **Trigger dimension selection is heuristic.** Section 4.2 shows that trigger dimension choice significantly affects ASR (Table 2), and the paper fixes dimensions to (1,2,3) for all main experiments. The paper attempts dimension selection methods in Appendix F but does not provide a principled way to choose effective trigger dimensions across different environments. This leaves the attack's success somewhat dependent on an ad-hoc choice.

### Trivial

- The persistent backdoor evaluation (Section 6.3) is limited to three environments and maximum k=15. The paper notes the context window constraint but does not explore whether adaptive triggers (e.g., periodic re-triggering) could overcome this limitation.

## Nice-to-Haves

- A theoretical justification for why alternating training (bi-level optimization) is effective for backdoor implantation in TO models would strengthen the methodology beyond the empirical motivation.
- Exploring whether the attack can be transferred across different TO model architectures (e.g., a trigger trained on DT that works on DC) would further demonstrate practical threat.
- An analysis of the computational cost of the post-training attack (training time, GPU hours) would help practitioners understand the attack's feasibility.

## Novel Insights

Beyond the paper's own contributions, the most novel insight is that reward manipulation—the central attack vector in traditional RL backdoors—is essentially irrelevant for TO models because their training objective is reconstruction (behavior cloning conditioned on returns-to-go) rather than policy optimization via reward maximization. This reframes the backdoor problem for sequence-modeling-based RL: triggers must be designed to hijack the autoregressive action prediction mechanism, not to corrupt value estimates. This insight could generalize to other conditional sequence models used in decision-making beyond RL.

## Suggestions

- Clarify the threat model: explicitly state whether the adversary has access to any offline dataset, and if so, what constraints exist relative to the original training data. If the adversary uses a public dataset (e.g., D4RL), mention it explicitly.

- Include a quantitative summary of defense results in the main paper (at least one table or figure showing the CP after each defense method), and discuss why weight pruning and spectral analysis fail while fine-tuning succeeds.

- Add an ablation varying the trigger dimension selection method to demonstrate that TrojanTO is robust to different dimension choices, or provide guidance on how to select effective dimensions.

## Score and Decision

This paper addresses an underexplored and timely problem (security of trajectory optimization models in offline RL), provides a well-motivated attack design with strong empirical validation, and includes informative ablation studies. The weaknesses—primarily threat model clarity and superficial defense analysis—are not fatal but should be addressed to strengthen the paper's contribution. Overall, the paper makes a solid contribution to the field.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>