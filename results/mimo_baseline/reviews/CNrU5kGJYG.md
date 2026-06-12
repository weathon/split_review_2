## Summary
This paper proposes TrojanTO, the first action-level backdoor attack against Trajectory Optimization (TO) models in offline RL. Unlike traditional RL backdoor attacks that manipulate rewards during training, TrojanTO is a post-training attack that modifies a pretrained model using alternating optimization between a learnable trigger and model parameters, combined with trajectory filtering and batch poisoning to maintain stealthiness at a low poisoning rate of 0.3%.

## Strengths
- **Novel and well-motivated threat model**: The paper clearly identifies that existing backdoor paradigms based on reward manipulation are fundamentally incompatible with TO models, which minimize reconstruction loss rather than maximizing returns. The post-training attack paradigm is timely given the increasing scale and cost of training TO models. This is a genuine contribution to the security literature for offline RL.

- **Systematic empirical investigation of key factors (Sections 4.1–4.3)**: The paper methodically disentangles the influence of target action selection, trigger design, and reward manipulation on backdoor efficacy. The finding that reward manipulation has negligible impact on TO models (Figure 1) is a genuinely important insight that distinguishes TO model vulnerabilities from those of traditional RL agents. The observation that boundary target actions yield higher ASR than interior actions is also practically useful.

- **Comprehensive experimental evaluation**: Experiments span 6 D4RL environments (locomotion, navigation, manipulation), 3 TO model architectures (DT, GDT, DC), and multiple target action types, with all results averaged over 3 random seeds. The comparison against Baffle and IMC baselines shows TrojanTO achieves significantly higher CP (0.701 vs. 0.342 and 0.551) while using only 0.3% poisoning rate versus Baffle's 10%.

- **Thorough ablation studies**: Table 5 provides clear evidence that all three components (TF, BP, AT) contribute meaningfully: AT primarily improves ASR while TF and BP primarily preserve BTP. Additional analyses on persistent backdoor attacks (Table 6), trigger perturbations (Table 7), and defenses are well-designed.

## Weaknesses
### Fatal
None.

### Major
- **Mixed attack effectiveness across environments**: The attack achieves high ASR on locomotion tasks (often 0.9+) but shows notably lower effectiveness on AntMaze (ASR 0.296 with DT, 0.334 with GDT) and variable performance on manipulation tasks (Pen ASR ranges from 0.428 to 0.667 depending on model). While the paper presents averages favorably, this variability suggests the attack's effectiveness is task-dependent, and the paper does not provide sufficient analysis of why certain environments resist the attack.

- **Defense analysis is underdeveloped**: The paper acknowledges that fine-tuning is the most effective defense against TrojanTO, while other defenses are "largely ineffective." However, fine-tuning is the most natural and accessible countermeasure for a post-training attack. Given that the threat model assumes the user deploys a compromised model and may fine-tune it, the practical impact of the attack is somewhat diminished. The defense analysis, relegated to Appendix B.1, deserves more thorough treatment in the main paper.

### Minor
- **Fixed trigger dimension selection**: After the initial study in Table 2, trigger dimensions are always fixed to (1,2,3). The paper does not provide a principled reason for this choice beyond empirical observation, and it remains unclear whether this choice transfers across different state spaces or environments. The paper briefly mentions additional dimension selection methods in Appendix F, but this aspect could be more rigorously motivated.

- **Bi-level optimization convergence and stability**: The alternating training procedure uses MI-FGSM for trigger learning with multi-step updates, and switches to parameter-only optimization after half the training budget. The rationale for the 50% cutoff is not clearly justified, and there is limited analysis of optimization convergence or sensitivity to the training budget split.

- **CP metric interpretation**: Some reported CP values are moderate (e.g., 0.302 for DT/Ant, 0.365 for DT/Hopp with Baffle), and the paper does not discuss what constitutes a practically meaningful CP threshold. The harmonic mean can be misleading when ASR and BTP are imbalanced.

### Trivial
None.

## Nice-to-Haves
- Analysis of whether the trigger dimensions that work well for one environment transfer to others, or whether environment-specific dimension selection is needed
- Visualization of the learned trigger values to provide intuition about what the trigger captures
- Discussion of detection methods beyond the tested defenses, such as input sanitization or anomaly detection

## Novel Insights
The paper makes two genuinely novel observations: (1) reward manipulation, the primary attack vector for traditional RL backdoors, is essentially irrelevant for TO models, which instead rely on reconstruction loss over sequences. This fundamentally reframes the backdoor threat landscape for the emerging class of sequence-modeling-based RL. (2) The choice of target action in high-dimensional continuous spaces is not innocuous—boundary actions are dramatically easier to implant as backdoors than interior actions, suggesting that prior work using fixed target actions (like '1') may have overestimated attack difficulty by not considering the full range of targets.

## Suggestions
- Include a deeper analysis of why certain environments (especially AntMaze) resist the attack—Is it the reward structure, state dimensionality, or trajectory characteristics?
- Provide more discussion of fine-tuning as a defense in the main paper, including how much fine-tuning is needed and whether the attacker could anticipate or circumvent it (e.g., by training with augmentation against fine-tuning)
- Consider analyzing the attack's transferability: if a backdoor is implanted in DT, does it transfer when the user applies a different architecture or modifies the model?

## Score and Decision
This paper presents a well-motivated and systematically executed study of a novel threat against TO models. The empirical investigation of key factors (especially the negligible role of reward manipulation) provides genuine insight into the security properties of sequence-modeling-based RL. The attack methodology is effective at low poisoning rates, and experiments are comprehensive. The main concerns are the mixed effectiveness across environments and the acknowledgment that standard fine-tuning can defend against the attack, which somewhat limits practical impact. Overall, this is a solid contribution that fills an important gap in the offline RL security literature.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>