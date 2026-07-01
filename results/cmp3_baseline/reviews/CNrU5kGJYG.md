## Summary

This paper proposes TrojanTO, the first post-training action-level backdoor attack against trajectory optimization (TO) models in offline reinforcement learning. The attack employs alternating training to co-optimize a trigger and model parameters, trajectory filtering to preserve benign performance, and batch poisoning for consistent trigger association. Experiments across six D4RL tasks and three TO architectures (DT, GDT, DC) demonstrate high attack success rates with a very low poisoning rate (0.3%), significantly outperforming existing baselines.

## Strengths

- **Novel and timely problem formulation**: The paper systematically studies action-level backdoors for TO models, an underexplored yet important security concern as these models scale and are deployed in safety-critical applications. The post-training threat model is practical and increasingly relevant.
- **Comprehensive empirical evaluation**: Extensive experiments across six diverse D4RL environments, three TO architectures, multiple target actions, with ablations, persistent attacks, trigger perturbations, and defense analysis. Results show consistent improvements over baselines (27.2% CP gain over IMC, 105% over Baffle) while using only 0.3% poisoned trajectories.
- **Careful analysis of key factors**: The paper provides a dedicated study (Section 4) identifying that target action and trigger design are critical while reward manipulation is ineffective for TO models. This insight directly motivates the attack design and is well-supported empirically.
- **Ablation and sensitivity analysis**: Clear component-level ablation (Table 5) and parameter studies in the appendix demonstrate the contribution of trajectory filtering, batch poisoning, and alternating training, strengthening the methodological claims.

## Weaknesses

### Fatal
None.

### Major
- **Threat model inconsistency**: Section 3.3 states the adversary operates "without access to the original training dataset," yet the methodology (Section 5) requires trajectory data from the environment (for filtering, batch poisoning, and trigger learning). The source of these trajectories is not clarified. If the adversary needs a substitute dataset, the practical feasibility and assumptions of the attack are incomplete. This discrepancy must be resolved.
- **Baseline comparison fairness**: Baffle is a pre-training data poisoning attack (different threat model), and IMC is a supervised learning method not originally designed for RL backdoors. While the comparison is informative, the paper does not sufficiently discuss the mismatch in attack budgets, threat models, or design assumptions. A dedicated online RL or model-poisoning baseline would strengthen the evaluation.
- **Trigger dimension selection**: The paper selects trigger dimensions (1,2,3) based on empirical best performance among a few random triplets. This choice is not principled and may overfit to these specific environments. The sensitivity analysis in Table 2 shows extreme variance (0.000 to 0.915 ASR depending on dimensions), indicating that the attack's success is highly contingent on this choice, which may not generalize without prior knowledge.

### Minor
- **Stealthiness evaluation**: BTP (normalized return) is the only stealthiness metric. It does not evaluate whether the backdoored model's state-action distribution or other behavioral statistics differ from the clean model on benign inputs, which could reveal the attack to more advanced detectors.
- **Defense analysis limited**: The defense study is relegated to the appendix and only tests a few baseline methods. The most effective defense (fine-tuning) is not deeply analyzed—e.g., how much fine-tuning data is needed, or whether the attack can evade fine-tuning with stronger optimization.
- **Persistent attack bound**: The persistent attack duration is intrinsically limited by the model's context window (＜20 steps). While acknowledged, this severely constrains the practical impact for long-horizon tasks.

### Trivial
- The target type "0.5staggered" in Table 1 is not defined (appendix reference but unclear).

## Nice-to-Haves

- Provide theoretical analysis explaining why TO models are more sensitive to trigger-state perturbations than reward manipulation, beyond empirical observation.
- Investigate transferability of the backdoor across different environments or model checkpoints.
- Design a principled method for selecting trigger dimensions (e.g., based on state variance or saliency) rather than brute-force search over random subsets.

## Novel Insights

Beyond the proposed attack, the paper's key insight is that backdoor design for TO models must pivot from reward-centric approaches (dominant in traditional RL) to trigger–target action coupling via alternating optimization. The finding that trigger dimension choice dominates ASR variance (Table 2) is non-trivial and suggests that TO models have highly structured state representations that can be exploited with carefully placed perturbations. The demonstration that a 0.3% poisoning rate suffices is also notable, as it highlights a stark vulnerability–stealthiness trade-off in these models.

## Suggestions

1. **Resolve the threat model inconsistency**: Clarify whether the adversary requires any trajectory data for post-training, and if so, specify the assumptions (e.g., access to public offline datasets, or a small validation set). If no data is needed, explain how the modules operate without it.
2. **Add stronger baselines**: Include a version of Baffle adapted to post-training (e.g., fine-tuning with poisoned data) or a simple fine-tuning baseline that only uses clean data, to isolate the effect of the backdoor.
3. **Provide a method for trigger dimension selection**: Even a heuristic based on state gradient magnitude or feature importance would improve reproducibility and generalizability.
4. **Expand stealthiness evaluation**: Include metrics such as KL divergence of action distributions or state-visitation frequency between clean and backdoored policies on benign inputs.

## Score and Decision

**Score**: 6  
**Decision**: Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>