Now I have all the information needed. Let me write the final consolidated review.

## Summary

TrojanTO proposes the first action-level backdoor attack against trajectory optimization (TO) models in offline RL (Decision Transformer, GDT, DC). The attack operates post-training (modifying a pretrained model rather than poisoning the training data), using three components: trajectory filtering to preserve benign performance, batch poisoning for trigger consistency, and alternating training (trigger + model co-optimization) to forge strong trigger–action associations. Evaluated across 6 D4RL environments × 3 TO models × 3 target action types, the attack achieves high ASR and CP at a very low budget (0.3% of trajectories).

## Strengths

- **Genuinely novel problem.** The paper correctly identifies that existing RL backdoor attacks (reward-manipulation-based, Bellman-equation-reliant) do not transfer to TO models, which use sequence modeling with reconstruction loss. This gap is real and underexplored. **(Section 4.3, Section 2)**

- **Informative factor analysis.** Section 4's systematic exploration of what matters for backdooring TO models—target action selection, trigger dimensions, trigger values, and the (non-)role of reward—provides useful grounding. The honest finding that boundary target actions yield ~1.0 ASR while interior actions can give as low as 0.11 (Table 1, Walker2d) is a strength, as is the decision to evaluate across multiple target types rather than cherry-picking the easiest one.

- **Practical threat model and impressive attack budget.** The post-training supply-chain scenario (adversary modifies a pretrained model without access to the original training pipeline) is well-motivated and underexplored in RL. Achieving the reported CP values using only 0.3% of trajectories is a legitimate engineering achievement. **(Section 3.3, Abstract)**

- **Broad evaluation scope.** Testing on 3 model architectures (DT, GDT, DC) × 6 environments (locomotion, navigation, manipulation) × 3 target action types gives the results reasonable generality. The ablation study (Table 5) cleanly isolates each component's contribution.

## Weaknesses

### Major
None that are fatal or invalidate the core contribution.

### Minor

- **ASR threshold ε is never reported.** Equation (2) defines ASR using an element-wise tolerance ε on each action dimension, but no numerical value for ε is stated anywhere in the main paper. In high-dimensional continuous action spaces (e.g., Walker2d has 6 action dimensions), whether ε = 0.01 or ε = 0.5 dramatically changes what "ASR = 0.99" means. Without this value, the core effectiveness metric cannot be properly interpreted by the reader. **(Section 3.4, Equation 2)**

- **Baseline comparison framing mixes different threat models.** The paper presents TrojanTO against Baffle (a pre-training data poisoning attack requiring 10% poisoned trajectories) and IMC (a CV technique, not an RL backdoor method) as direct competitors in Table 4, and headlines a "105.0% improvement compared to Baffle." These operate under fundamentally different threat models (pre-training vs. post-training, RL backdoor vs. CV co-optimization). While Section 3.3 does categorize attack stages, the main comparison in Section 6.1 does not caveat these differences, making the headline superiority claim less informative than it appears. A properly controlled post-training adaptation of Baffle would be a more meaningful comparison. **(Section 6.1, Table 4)**

- **Defense evaluation lacks quantitative results in the main paper.** Section 6.5 states only: "Our results show that fine-tuning is the most effective defense, while the other tested methods proved largely ineffective." No ASR/BTP/CP values after any defense are given in the main text. For a paper that introduces a new attack, defense analysis should meet the same reporting standard as attack evaluation. **(Section 6.5)**

- **Zero variance in persistent backdoor CP results is unexplained.** Table 6 reports CP values such as 0.922±0.000, 0.972±0.000, and 0.993±0.000 across multiple conditions with 3 random seeds and 100 evaluation episodes. Zero variance across all seeds for a metric computed from stochastic evaluation is unusual and warrants an explanation (e.g., measurement granularity, saturation effects, or deterministic action selection under the trigger). **(Section 6.3, Table 6)**

- **Source of the 0.3% trajectories is unclear given the threat model.** The threat model states the adversary has "no access to the original training dataset" (Section 3.3), yet the attack uses "a minimal set of poisoned trajectories (e.g., 0.3%)." The paper does not clarify whether these trajectories come from a different public source, are generated synthetically, or represent a relaxation of the "no access" assumption. **(Section 3.3)**

### Trivial

- The Alternating Training module's relationship to IMC (Section 5.3: "drawing inspiration from IMC") and IMC as a separate baseline (Table 4) create some tension. The paper would benefit from explicitly stating what modifications AT introduces beyond IMC (multi-step updates, mid-training trigger freeze).

- The trigger dimension analysis (Table 2) is only shown for HalfCheetah and Walker2d, but the default choice (1,2,3) is used across all 6 environments. Showing that this choice generalizes would strengthen confidence.

## Nice-to-Haves

- **Behavioral similarity metric.** The paper uses BTP (normalized return) as the sole stealthiness metric. While this is standard in the backdoor literature, the attack's threat model involves "unsuspecting users" deploying the model. A complementary measure of behavioral divergence (e.g., action distribution KL divergence or per-step L2 distance on benign inputs) would strengthen the stealthiness case.

- **More comprehensive trigger dimension analysis across all environments** (not just HalfCheetah and Walker2d) for the default (1,2,3) choice.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"AT's novelty relative to IMC is unclear" from the harsh critic's Critical Issues #4** — The paper explicitly acknowledges IMC inspiration and uses it as a baseline; this is standard practice. Demoted to Trivial above rather than a distinct weakness.
- **"BTP conflates stealthiness with task performance preservation" from Critical Issues #3** — Maintaining benign task performance (BTP) is the standard stealthiness metric across the backdoor literature. The critic's demand for behavioral similarity is a stricter requirement than what is standard for this threat model. Kept as a Nice-to-Have rather than a weakness.
- **Various section-by-section notes (zero variance in CP, trigger dimension generalization)** — These are addressed in the Weaknesses section above where substantive; minor observations were either merged or dropped.
- **"The 0.3% attack budget is genuinely impressive" from Strengths #4** — This is a concrete, paper-grounded strength that is kept.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Report ε numerically** in Section 3.4 or in the first row of a results table.
2. **Add a post-training baseline**: adapt Baffle's trigger design to the fine-tuning setting for a direct apples-to-apples comparison within the same threat model, or explicitly caveat the cross-paradigm comparison in Section 6.1.
3. **Add a brief explanation** for the zero-variance CP entries in Table 6.
4. **Clarify the data source** for the 0.3% poisoned trajectories: does the adversary sample from a public dataset, generate synthetic trajectories, or use a held-out subset of the original data?
5. **Move key defense numbers** (ASR/BTP/CP after each defense) into the main paper or replace Section 6.5's qualitative summary with a brief results table.

## Score and Decision

**Calibration procedure:**

Round 1 bracket search retrieved papers across all score bands using queries on "backdoor attack reinforcement learning trajectory optimization" and "offline reinforcement learning backdoor attack decision transformer." Anchor papers used for comparison:

| Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| SHINE (backdoor defense, DRL) | 5.75 | R1 | Less novel; narrower evaluation; weaker ablation |
| Tree-based Action-Manipulation Attack (continuous RL) | 5.75 | R1 | Narrower evaluation (2 envs); but has theoretical guarantees |
| Temporal Logic Multi-Vehicle Backdoor (offline RL) | 4.00 | R1 | Higher poisoning rate (~15%); more domain-specific (AD) |
| BATTLE (adversarial attacks, DRL) | 4.25 | R1 | Broader attack framing but less focused contribution |
| Doctor (Transformer for offline RL) | 5.00 | R1 | Marginal gains over baselines; lower novelty |
| Multi-level Certified Defense (offline RL) | 6.75 | R2 | Stronger theoretically; broader evaluation; accepted |
| Towards Robust Offline RL (data corruption) | 7.00 | R2 | Comprehensive evaluation; accepted |

Round 1 bracket: 5.5–6.5. Round 2 narrowed comparison using higher-scoring offline RL security papers. TrojanTO's novelty (first action-level backdoor for TO models) and evaluation breadth (6 envs × 3 models × 3 targets) place it above the 4.0–5.75 papers, but the reporting omissions and cross-paradigm baseline issues prevent it from reaching the 7+ tier. Final calibrated score: **6.0**.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>