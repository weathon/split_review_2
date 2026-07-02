## Summary
# Final Review Report

## Summary

This paper proposes TrojanTO, a post-training action-level backdoor attack framework targeting Trajectory Optimization (TO) models in offline reinforcement learning. The key technical insight is that existing RL backdoors rely on reward manipulation during training, which is ineffective against TO models because they minimize reconstruction loss rather than maximizing reward. TrojanTO instead operates by modifying a pretrained TO model through three components: (1) trajectory filtering to select high-quality trajectories for poisoning, (2) batch poisoning that perturbs a single transition per batch for trigger consistency, and (3) alternating training that jointly optimizes the trigger perturbation and model parameters. The attack achieves high success rates (avg ASR 0.719) with only 0.3% poisoned trajectories and maintains benign task performance (avg BTP 0.914) across six D4RL environments and three TO architectures (DT, GDT, DC). The paper also investigates key factors influencing backdoor efficacy, finding that target action selection and trigger design are critical while reward manipulation is unnecessary.

**Novelty assessment (deferred):** Since external literature search was unavailable in this review run, novelty and comparison claims (particularly the "first action-level backdoor attack against TO models" claim) cannot be independently verified. The assessment above is grounded solely on manuscript evidence.

## Strengths
**1. Timely and relevant problem formulation.** The paper identifies a genuine security gap: TO models (Decision Transformer, Decision ConvFormer, GDT) are increasingly used in offline RL for robotic control and embodied intelligence, yet their vulnerability to backdoor attacks has not been systematically studied. The motivation that existing reward-based backdoor attacks are incompatible with TO models' reconstruction-based training is technically sound and practically important.

**2. Clean, three-component method design.** TrojanTO decomposes the backdoor injection problem into trajectory filtering, batch poisoning, and alternating training. Each component has a clear role: TF mitigates distribution shift, BP ensures trigger consistency, and AT strengthens the trigger-action coupling. The modular design makes the method easy to understand, ablate, and extend.

**3. Strong empirical results on locomotion tasks.** On locomotion environments (HalfCheetah, Walker2d, Hopper), TrojanTO achieves consistently high CP values (often >0.95 for DC and DT), demonstrating that the attack is highly effective and stealthy on these tasks. The 0.3% poisoning rate is a genuine improvement over Baffle's 10%, making the attack more practical and harder to detect.

**4. Comprehensive factor analysis (Section 4).** The systematic investigation of target action types, trigger dimensions, and trigger values provides useful design insights for the backdoor community. The finding that reward manipulation is unnecessary for TO model backdoors is a non-trivial insight that clarifies the attack surface for future work.

**5. Broad architectural evaluation.** Testing across three TO architectures (DT, GDT, DC) and six diverse D4RL environments (locomotion, navigation, manipulation) is more comprehensive than typical backdoor papers, which often evaluate on a single task family. This breadth strengthens the generalizability claims.

## Weaknesses
**W1 (Major). Defense analysis critically underdeveloped (Section 6.5).**
The defense evaluation is the weakest part of the experimental section. The paper states that four baseline defenses (weight pruning, provable defense, spectral analysis, activation clustering) are "largely ineffective" and fine-tuning is "the most effective," but provides zero numerical results, no defense hyperparameters, no post-defense ASR/BTP values, and no comparison across environments. This is not a reproducible defense analysis. Without quantitative evidence, the reader cannot assess the practical threat level of TrojanTO or the conditions under which it can be mitigated. *Required action:* Add a full defense table with ASR and BTP after each defense method, with key parameters (pruning ratio, fine-tuning epochs, clustering threshold), across at least 3 representative environments.

**W2 (Major). Claim-evidence mismatch in attack performance reporting (Section 6.1).**
The narrative claims "consistent robustness and stability across varied tasks and TO model architectures," but Table 4 shows substantial task- and architecture-specific failures: TrojanTO achieves CP=0.302 on Ant with DT (only marginally above Baffle's 0.208), CP=0.477 on Pen with DC (worse than IMC's 0.655 and Baffle's 0.542), and BTP=0.455 on Kitchen with DT (benign performance drops to 45% of clean, undermining stealth). The paper should explicitly discuss these failure cases and their causes rather than averaging over them. Overclaiming consistency reduces credibility. *Required action:* Add a paragraph analyzing the task-architecture conditions where TrojanTO underperforms, with hypotheses about why (e.g., navigation tasks may be less sensitive to state perturbation; DC's convolutional architecture may process triggers differently than transformer attention).

**W3 (Major). Formula inconsistency between threat model and implementation (Eq. 1 vs. Eqs. 5-6).**
The formal threat model (Eq. 1) minimizes $\|\tilde{\pi}([a],[s],[R])_t - \pi([a],[s],[R])_t\|$, forcing output similarity to the *original* model on benign inputs. However, the actual clean loss (Eq. 6) uses ground-truth action reconstruction $\frac{1}{T}\sum_t (\hat{\pi}(B_c)_t - a_t)^2$. These are not equivalent—Eq. 1 over-constrains the model by penalizing any deviation from the original policy even if the new policy is equally valid. This inconsistency means the formal objective does not match the implemented algorithm. Additionally, Eq. (6) sums over $t=0$ to $T$ but should sum over $t=0$ to $T-1$ for consistency with earlier definitions. *Required action:* (i) Revise Eq. (1) to use ground-truth action reconstruction for the clean term, aligning with Eq. (6). (ii) Fix the summation bound in Eq. (6) to $T-1$. (iii) Report the $\lambda$ value used and include sensitivity analysis.

**W4 (Major). Missing statistical rigor in factor analysis (Section 4).**
Tables 1, 2, and 3 report ASR values without any variance or confidence intervals, yet the paper states "All results are averaged over three runs with distinct random seeds" for the main experiments. The factor analysis drives critical method design decisions (MI-FGSM trigger optimization, ignoring reward manipulation). If these empirical findings are not statistically robust, the design rationale weakens. For instance, in Table 2, dimensions (5,6,7) give ASR=0.435 (Half) and 0.047 (Walk) — without variance, it is unclear whether the 10x difference across environments is meaningful or noise. *Required action:* Add standard deviations to Tables 1-3, or add a note that these are single-seed results with a verification subset reported with variance.

**W5 (Major). Missing hyperparameter reporting for core loss trade-off.** 
The final objective $\mathcal{L} = \mathcal{L}_p + \lambda \mathcal{L}_c$ relies on $\lambda$ to balance attack success and benign performance, but the paper never reports the value of $\lambda$ used in experiments, nor does it provide sensitivity analysis. Moreover, $\mathcal{L}_p$ is a single-point loss (one poisoned transition) while $\mathcal{L}_c$ averages over all $T$ timesteps, creating a scale imbalance that makes $\lambda$'s effect dependent on context length $K$ and batch size. Without this detail, the results are not independently reproducible. *Required action:* Report $\lambda$ value for all experiments, add a sensitivity table (e.g., $\lambda \in \{0.1, 0.3, 0.5, 0.7, 0.9\}$ showing ASR/BTP/CP), and renormalize $\mathcal{L}_p$ to match the per-timestep scale of $\mathcal{L}_c$.

**W6 (Moderate). Trajectory filtering heuristic lacks validation (Section 5.1).**
The paper assumes "longer trajectories are more representative of successful behavior" without empirical support. In AntMaze, longer trajectories could reflect failure (agent stuck in loops). In Kitchen, successful manipulation can vary in length. The paper does not report $\epsilon$ values, fraction of retained trajectories per dataset, or sensitivity to the threshold choice. *Required action:* Add an appendix table showing $\epsilon$ per dataset, retention percentage, and a sensitivity analysis (e.g., CP vs. $\epsilon$ at ±20% of the chosen value).

**W7 (Moderate). Persistent backdoor mechanism unexplained (Section 6.3).**
Table 6 shows that persistent backdooring works for $k=5,10,15$ steps, but the paper offers no explanation of *why* the model continues outputting the target action after a single trigger. Is it because the trigger stays in context? Because the model enters a self-sustaining loop? The claim that "the maximum duration is fundamentally bounded by the context window" is not empirically tested (no experiment pushes $k$ beyond the context size). *Required action:* Add an analysis of the persistent mechanism (e.g., by tracking whether the model's own output action replaces the trigger as the conditioning signal for subsequent steps). Test $k$ up to the full context window and report the drop point.

**W8 (Moderate). Novelty claims cannot be verified without literature search.**
The paper claims "the first action-level backdoor attack against TO models" and "the first systematic study of action-level backdoors in offline RL." Since external literature search was unavailable in this review run, these claims cannot be independently confirmed or refuted. The authors should ensure that all "first" claims are scoped with precise qualifiers (task setting, threat model, architecture family) and that related-work coverage includes all comparable prior methods. *Required action:* Replace "first" with bounded phrasing such as "to our knowledge, the first post-training action-level backdoor for TO models under the supply-chain threat model" and verify that no concurrent or prior work meets this exact description.

**W9 (Minor). ASR threshold $\varepsilon$ not reported.**
The ASR definition (Eq. 2) depends on a threshold $\varepsilon$ that determines whether an output action matches the target. The paper never states the value of $\varepsilon$, making ASR values non-reproducible. *Required action:* Report $\varepsilon$ value (e.g., $\varepsilon=0.1$) and justify it relative to action space scale.

**W10 (Minor). BTP denominator risk and CP ceiling.**
BTP (Eq. 3) divides by $G_k(\pi)$, which could be zero or negative in sparse-reward environments. CP (harmonic mean of ASR and BTP) treats BTP as bounded [0,1], but BTP can exceed 1 if the backdoored model outperforms the clean one. The paper does not clarify how these edge cases are handled. *Required action:* Add a note clarifying handling of zero/negative denominators for BTP and whether BTP is capped at 1.0 for CP computation.

### Ranked Error Board (Top 5)

| Rank | Issue | Severity | Validity Risk | Fixability | Confidence |
|------|-------|----------|--------------|------------|------------|
| 1 | W1: Defense analysis lacks quantitative results | Major | High — defense claims unverifiable | Easy — add table | High |
| 2 | W2: Claim-evidence mismatch in robustness narrative | Major | Medium — overclaiming harms credibility | Moderate — rewrite + discuss failures | High |
| 3 | W3: Eq. (1) vs. Eqs. (5-6) inconsistency | Major | Medium — formal model mismatches implementation | Easy — correct equation and report λ | High |
| 4 | W4: Missing variance in factor analysis | Major | Medium — design choices may be noise-driven | Moderate — add seed info | High |
| 5 | W5: Missing λ reporting and scale imbalance | Major | Medium — reproducibility gap | Easy — report λ and add sensitivity | High |

## Score
**Final Score: 6/10**

**Rationale:** The paper addresses a timely and underexplored problem (backdoor attacks on TO models), proposes a clean three-component method (TrojanTO), and provides broad empirical evaluation across six environments and three architectures. The core technical contributions—the post-training attack paradigm, the finding that reward manipulation is unnecessary, and the consistency poisoning strategy—are novel within the offline RL backdoor literature. The low poisoning rate (0.3%) is a genuine practical advantage over prior work.

However, the score is constrained by several significant weaknesses:

1. **Defense analysis is critically incomplete** (W1). The paper makes strong claims about defense ineffectiveness without reporting any numerical results. This is a major empirical gap that prevents full assessment of the attack's practical threat level.

2. **Narrative overclaims robustness** (W2). While average CP is strong, several task-architecture combinations show poor performance that is not discussed. The paper presents the results as uniformly strong, which conflicts with the data.

3. **Formula inconsistency between formal threat model and implementation** (W3) and missing hyperparameter reporting (λ in W5) reduce reproducibility. These are fixable but currently prevent independent verification.

4. **Factor analysis lacks statistical rigor** (W4), weakening confidence in the design decisions derived from it.

5. **Novelty claims cannot be externally verified** in this review run due to unavailable literature search. The "first" claims should be conservatively bounded.

The paper has clear strengths in problem framing, method design, and breadth of evaluation, but the weaknesses in empirical reporting rigor, reproducibility details, and balanced narrative are substantial enough that the current version would require major revision for a top-tier venue. The core technical approach is promising and the empirical evidence is largely supportive (on locomotion tasks), giving the paper a solid foundation for revision.