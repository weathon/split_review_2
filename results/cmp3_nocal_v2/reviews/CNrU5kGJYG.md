## Summary

This paper proposes TrojanTO, the first action-level backdoor attack against trajectory optimization (TO) models in offline RL. It identifies that existing RL backdoor attacks relying on reward manipulation are ineffective against TO models, and introduces a post-training attack framework combining trajectory filtering, batch poisoning, and alternating training to implant triggers with only 0.3% poisoned trajectories. The method is evaluated across DT, GDT, and DC on 6 D4RL environments.

## Strengths

1. **Novel problem identification (Sections 1, 2, 4.3).** The paper correctly identifies that existing RL backdoor attacks rely on reward manipulation, which is ineffective against TO models because TO models are conditioned behavior cloners minimizing reconstruction loss, not reward-maximizing Bellman agents. The empirical confirmation in Section 4.3 (Figure 1) convincingly demonstrates this gap. This is the most solid part of the contribution.

2. **Systematic empirical investigation of key factors (Section 4, Tables 1–3, Figure 1).** The study of target action selection, trigger dimensions, trigger values, and reward manipulation is thorough and produces actionable design guidance. The finding that boundary target actions yield near-perfect ASR while interior actions yield much lower ASR (e.g., 0.11 for action type '0' in Walker2d) is an important empirical observation for anyone working on this problem.

3. **Low poisoning rate (0.3% vs. Baffle's 10%).** A 33× reduction in required poisoned data while achieving competitive or superior attack success rates is a meaningful practical improvement.

4. **Broad coverage of model architectures and environments.** Testing across DT, GDT, and DC on 6 D4RL environments provides good empirical grounding for an attack paper.

5. **Component-level ablation (Table 5).** The ablation cleanly isolates the contribution of each component. The results show that BP and AT matter most for ASR, while TF and BP matter most for BTP, providing clear design insight.

## Weaknesses

### Fatal
None.

### Major
- **Unclear source of trajectories for backdoor training given the stated threat model.** Section 3.3 states the adversary operates "without access to the original training dataset" (line 60). Yet the method requires an "initial set of N trajectories" (Section 5.1, line 174) for trajectory filtering and samples "trajectories from the dataset" (Section 5.2, line 193) for batch poisoning. The paper never explains where these trajectories come from given the stated constraint. Possible resolutions (collecting proxy trajectories by running the pretrained model, using a public dataset, or revising the threat model) are not mentioned, evaluated, or acknowledged as a limitation. This gap between the stated threat model and the implemented method needs to be resolved.

### Minor
- **The ASR threshold ε is not specified in the main text.** Equation (2) defines ASR using a threshold ε, but its numerical value is never stated in the main paper. Since ε directly determines what counts as a successful attack (a tight threshold makes ASR strict, a loose one makes it trivial), the reader cannot assess how precise the claimed action control actually is. The paper should state ε where ASR is defined, not defer it entirely to the appendix.

- **No variance or confidence intervals on the main results (Table 4).** Table 4 reports only point estimates (means over 3 seeds and 3 target actions) with no error bars. Several individual settings show TrojanTO losing to baselines (e.g., DT/Pen: TrojanTO CP=0.664 vs. IMC CP=0.667; DT/Kit: TrojanTO CP=0.614 vs. Baffle CP=0.766), and without variance information it is unclear whether the overall average advantage is robust or driven by a few favorable runs. Tables 6 and 7 do report standard deviations, suggesting the machinery exists; its absence from the central result table is conspicuous.

- **The comparison with Baffle conflates two different advantages.** Baffle is a pre-training attack at 10% poisoning; TrojanTO is a post-training attack at 0.3% poisoning. The paper's framing of "105% improvement" and direct juxtaposition of CP values (lines 268–271) mixes the benefit of a different threat model with the benefit of the method itself. The paper should acknowledge this more transparently and ideally provide an apples-to-apples comparison (e.g., adapting Baffle to the post-training setting at the same 0.3% rate) to isolate whether TrojanTO's advantage stems from the method or the reduced poisoning rate.

### Trivial
- **Notational inconsistency in loss formulation.** Line 203 defines the final objective as L = L_p + λL_c, where λ weights the clean loss. Equation (7) instead uses λL_p + (1-λ)L_c, where λ weights the backdoor loss. These are opposite conventions for the same symbol λ. While mathematically equivalent up to reparameterization, this inconsistency is confusing.

## Nice-to-Haves
- The trigger dimension analysis (Table 2) is conducted on only two environments (HalfCheetah, Walker2d). Extending this analysis to more environments would strengthen confidence that the chosen dimensions (1,2,3) are generally effective.
- The defense section (Section 6.5) reports that fine-tuning is an effective defense. Since an effective defense would significantly reduce the real-world threat, this finding merits more discussion — in particular the conditions under which fine-tuning succeeds or fails, and whether a defender with limited clean data could mount an effective defense.
- A persistent backdoor attack experiment showing the effect beyond context-window bounds on more diverse tasks would better characterize the limitation stated in Section 6.3.

## Removed Points
These points were flagged by the reviewer but are removed after verification against the paper:

1. **IMC as a poorly matched baseline.** The reviewer claimed IMC is "an adversarial perturbation method for computer vision, not a backdoor attack." However, the paper adapts IMC's co-optimization framework as a reasonable baseline for trigger-model co-optimization. IMC's poor performance on some settings (e.g., CP=0.013 on DT/Hopper) may reflect genuine difficulty, not just method mismatch, and the paper does not claim IMC is a backdoor attack by design.
2. **"Post-training attack" framing overreaches.** The reviewer argued the method is indistinguishable from training-time fine-tuning. The paper clearly defines three stages of intervention (pre-training, during-training, post-training) in Section 3.3, and the post-training threat model is a genuinely different and practically relevant setting. This framing is defensible.
3. **Defense section too brief.** The paper states detailed results are in Appendix B.1, which is stripped by the parser. Per the hard rules, criticisms about missing appendix content are removed.
4. **Abstract claim about being "first."** The reviewer noted this claim is supportable if properly established. This is a positive observation, not a weakness.
5. **Trigger dimension generalizability.** The criticism that trigger dimension experiments use only two environments is a reasonable request but falls under "nice-to-have" rather than a weakness — the paper is transparent about the choice.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Clarify the source of the trajectories used for backdoor training and how this relates to the "no access to original training dataset" constraint in the threat model. If proxy trajectories are used, state this explicitly and evaluate its impact.
2. State the numerical value of ε in the main text where ASR is defined (Section 3.4).
3. Add standard deviations or confidence intervals to Table 4, or at minimum note when individual seeds show variation that changes the qualitative comparison.
4. Acknowledge the threat-model difference with Baffle more transparently when presenting the CP comparison, and consider adding an adapted-Baffle experiment at 0.3% poisoning rate in the post-training setting.
5. Fix the λ convention inconsistency between line 203 and Equation (7).

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>