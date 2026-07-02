## Summary

This paper proposes TrojanTO, the first action-level backdoor attack specifically designed for trajectory optimization (TO) models in offline reinforcement learning. Unlike prior RL backdoors that rely on reward manipulation during training, TrojanTO is a post-training attack that uses alternating training, trajectory filtering, and batch poisoning to forge a strong trigger–target-action connection with a very low poisoning rate (0.3% of trajectories). Extensive experiments across multiple D4RL environments and TO architectures (DT, GDT, DC) demonstrate that TrojanTO achieves high attack success rates while maintaining benign task performance, significantly outperforming existing baselines.

## Strengths

- **Timely and underexplored problem**: The paper identifies a realistic security vulnerability in TO models, which are increasingly used in robotics and embodied AI. The post-training attack paradigm is practical given the growing scale and training cost of these models.
- **Systematic factor analysis**: The paper provides a clear empirical investigation of how target action selection, trigger design, and reward manipulation affect backdoor efficacy in TO models. This analysis is valuable for understanding the attack surface and informs the design of TrojanTO.
- **Strong empirical results**: TrojanTO achieves an average CP of 0.701 across six environments and three TO models, with a 105% improvement over Baffle and 27% over IMC. The attack maintains high BTP (0.914) while using only 0.3% poisoned trajectories, demonstrating both effectiveness and stealthiness.
- **Thorough evaluation**: The paper includes ablation studies, persistent attack analysis, trigger perturbation robustness, and defense evaluation, providing a comprehensive understanding of the method’s behavior and limitations.
- **Generality across architectures**: TrojanTO is evaluated on DT, GDT, and DC, showing consistent performance and broad applicability to different TO model designs.

## Weaknesses

### Major

- **Strong threat model assumptions**: The post-training attack assumes the adversary has full access to the pretrained model parameters and a representative dataset for fine-tuning. While plausible in a supply-chain scenario, the paper does not discuss the realism of these assumptions or potential constraints (e.g., how the adversary obtains a suitable dataset without the original training data). This limits the practical threat assessment.
- **Trigger dimension selection is ad hoc**: The paper fixes trigger dimensions to (1,2,3) based on empirical observation for specific environments. No principled method is provided for selecting trigger dimensions in new environments, which could limit the attack’s transferability and reproducibility.
- **Limited defense analysis**: The defense evaluation is relegated to the appendix and only tests a few baseline methods. The paper claims fine-tuning is effective but does not explore adaptive defenses, detection methods, or the robustness of TrojanTO against stronger countermeasures. This weakens the security analysis.

### Minor

- **Comparison with Baffle is somewhat misaligned**: Baffle is a policy-level backdoor with a different objective (long-term return degradation), while TrojanTO is action-level. The paper acknowledges this but still uses CP as a common metric. The comparison would be stronger if the paper also compared against an action-level baseline adapted for TO models.
- **Average CP across target actions may hide variability**: The main results (Table 4) report averages over three target actions. Individual results per target action are in the appendix, but the main text could benefit from showing the range or standard deviation to give a clearer picture of robustness.
- **Persistent attack duration is limited by context window**: The paper notes that the persistent backdoor deactivates when the trigger leaves the context window (fewer than 20 steps). This is a fundamental limitation that should be discussed more explicitly in the main text.

### Trivial

- None beyond parser artifacts, which are ignored.

## Nice-to-Haves

- A discussion on how the adversary could obtain a representative dataset for fine-tuning without access to the original training data (e.g., using publicly available datasets or generating trajectories from the clean model).
- A more principled approach for trigger dimension selection, perhaps based on sensitivity analysis or gradient-based importance.
- An exploration of adaptive defenses, such as trigger detection via anomaly detection in the state space.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that TO models, due to their sequence modeling and reconstruction loss objective, are fundamentally insensitive to reward manipulation—a primary attack vector in traditional RL backdoors. This shifts the focus to trigger design and action-level control, revealing a new threat landscape for offline RL. The finding that trigger dimensions and values must be carefully optimized, and that boundary target actions are more easily implanted, provides actionable knowledge for both attackers and defenders.

## Suggestions

- Clarify the source and size of the dataset used for backdoor fine-tuning. Specify how the 0.3% poisoning rate is computed (e.g., fraction of trajectories in the filtered set vs. the full dataset).
- Include a table or figure showing the per-target-action results for the main experiments to give readers a sense of variability.
- Discuss the computational cost of trigger optimization (MI-FGSM iterations) and how it scales with model size.
- Add a brief discussion on the limitations of the post-training assumption and potential scenarios where it might not hold.

## Score and Decision

**Score**: 6  
**Decision**: Accept

The paper makes a solid contribution by identifying and addressing a realistic security threat in an important class of models. The method is well-motivated, empirically validated, and outperforms baselines. The major weaknesses (threat model assumptions, ad hoc trigger selection, limited defense analysis) are significant but do not invalidate the core contribution. The paper is likely to stimulate further research on TO model security and is suitable for acceptance at ICLR.

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>