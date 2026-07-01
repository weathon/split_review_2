Now I have sufficient calibration. Let me produce the final review.

## Summary

This paper proposes TrojanTO, a post-training action-level backdoor attack against Trajectory Optimization (TO) models in offline RL. The attack uses trajectory filtering, batch poisoning, and alternating training to embed a trigger that forces a specific target action at inference time, using only 0.3% poisoned trajectories. Key contributions include: (1) an empirical study showing that reward manipulation is ineffective for TO model backdoors while trigger and target action design are critical (Section 4); (2) a method designed around those findings; (3) evaluation across six D4RL environments and three TO architectures (DT, GDT, DC).

## Strengths

- **Well-motivated problem with a clear gap.** The paper correctly identifies that existing RL backdoor attacks rely on reward manipulation during training, which is incompatible with TO models that use sequence modeling and reconstruction loss (Section 3.1). The argument that training-time attacks become increasingly impractical as TO models scale is sound and makes the post-training setting genuinely relevant.

- **Informative empirical study of key factors (Section 4).** The systematic investigation of target action types (Table 1), trigger dimensions (Table 2), trigger values (Table 3), and reward manipulation (Figure 1) provides concrete, practically useful findings: boundary target actions yield ASR near 1.0 while interior ones drop to 0.11; trigger dimension choice causes ASR to vary from 0.000 to 0.915; reward manipulation has negligible effect. This analysis genuinely motivates and shapes the method design.

- **Broad evaluation scope.** Evaluation spans six D4RL environments (locomotion, navigation, manipulation) and three TO model architectures (DT, GDT, DC), supporting the claim of general applicability.

## Weaknesses

### Major

- **The Baffle comparison using ASR is structurally unfair.** The paper defines Baffle as a *policy-level* attack whose objective is "to manipulate the victim agent's long-term objectives... and does not consider the model's specific actions" (Section 3.2). TrojanTO is a fundamentally different type of attack (action-level). Yet the paper evaluates Baffle primarily on ASR — whether the model outputs a specific target action — which is the wrong metric for a policy-level attack. Baffle's low ASR (0.369, Table 4) does not indicate failure at its own objective. The paper then claims "105% improvement in CP" (line 268) and states Baffle "only reached an ASR of 0.369" (line 270) as evidence of superiority, without acknowledging this mismatch. Since CP for Baffle is partly computed from an inappropriate metric, the headline comparison is misleading. The paper should either (a) evaluate Baffle on its own terms (return degradation under trigger), (b) include action-level baselines that are appropriate comparators, or (c) explicitly acknowledge the threat-model mismatch and limit the comparison to poisoning efficiency and BTP, where both methods have something meaningful to show.

### Minor

- **Trajectory provenance and the "0.3%" poisoning rate are underspecified.** The threat model states the adversary acts "without access to the original training dataset" (Section 3.3). Yet the method consumes trajectories for filtering and batch poisoning (Sections 5.1–5.2). The paper says the adversary uses "a minimal set of poisoned trajectories (e.g., 0.3%)" (Section 3.3) but never clarifies the source of these trajectories — whether they are self-collected in a simulator, drawn from a public dataset, or somehow derived from the original training data. The "0.3%" figure is ambiguous without knowing what total pool it refers to. This ambiguity directly affects the practicality assessment of the attack.

- **The IMC baseline adaptation is underspecified.** IMC (Pang et al., 2020) is an input-model co-optimization method from image classification, used as a baseline. TrojanTO's Alternating Training (AT) module is "drawing inspiration from" IMC (Section 5.3). However, no details are provided about how IMC was adapted to TO models — which loss functions, hyperparameters, trigger initialization, or TO-specific modifications were used. The results in Table 4 (IMC achieves 0.551 CP vs. TrojanTO's 0.701) are not reproducible without this specification, making it difficult to interpret whether IMC is being compared fairly.

- **No standard deviations in the main results table.** Table 4 reports only averages over 3 seeds and 3 target actions without variance, despite later tables (6, 7) including standard deviations. With only 3 seeds, observed differences between methods cannot be assessed for statistical significance. The claim that TrojanTO exhibits "consistent robustness and stability" (line 272) would be strengthened by reporting variance.

### Trivial

- **The ASR threshold ε is not stated in the main text.** Equation (2) defines ASR using a threshold ε, but its value is not given in the main paper. Since ε directly affects ASR values, this should be stated (e.g., in the caption of Table 4 or Section 3.4).

## Nice-to-Haves

- The paper could evaluate Baffle on return degradation under trigger (its own objective) and present this alongside TrojanTO's ASR/CP as complementary rather than directly comparable metrics.
- The trigger dimensions were optimized on only two environments (Half, Walk) and then fixed for all six (Table 2). Given the massive variance across dimension choices (0.000 to 0.915), testing whether the optimal dimensions generalize would strengthen the main results.
- An analysis of trigger detectability (e.g., by simple statistical tests or human inspection of the perturbed state) would complement the BTP-based stealthiness assessment.

## Removed Points

These points from the input review were removed after verification against the paper:

- **CP metric criticism (conflating ASR and BTP):** The critic argued CP "conflates two incommensurate quantities." However, the paper already reports ASR and BTP *separately* in Table 4 alongside CP. CP is an additional composite metric (harmonic mean) commonly used in the backdoor literature (Ma et al., 2025). The paper explicitly notes that "CP is computed for each run based on its specific ASR and BTP, not a derivation from the mean." Reporting all three metrics is a standard and sufficient practice. This criticism is factually incorrect — the paper does not rely on CP alone.

- **Missing action-level baselines (TrojDRL, Rathbun et al., Ma et al.):** The critic faults the paper for not adapting these training-time attacks to the post-training setting. The paper explicitly scopes its contribution as a *post-training* attack (Section 3.3) and explains (Section 2, line 34) that training-time attacks are incompatible with TO models due to computational costs and different training objectives. Criticizing the paper for also solving the adaptation of fundamentally different attack paradigms is scope creep.

- **"IMC baseline is the same core idea as TrojanTO's AT component":** The critic claimed IMC is "essentially a variant of TrojanTO without TrojanTO's trajectory filtering and batch poisoning." In fact, AT is "drawing inspiration from" IMC (Section 5.3), but IMC is an image-classification method (Pang et al., 2020) from a different domain. Applying it directly to TO models is a nontrivial adaptation. The legitimate concern is that the IMC adaptation is underspecified (kept above as a Minor weakness), not that IMC and AT are identical.

- **Trigger detectability analysis:** The critic asked for analysis of whether the trigger perturbation is detectable by human observers or statistical tests. This is a reasonable extension but not a core weakness, as the paper evaluates stealthiness through BTP (task performance preservation) and trigger perturbation analysis (Section 6.4), which are the standard metrics in this literature.

## Novel Insights

The most interesting observation from the review process is that the harsh critic identified one genuinely structural evaluation design issue (the Baffle ASR comparison) alongside several minor clarity issues, while many of the "critical" claims (CP metric misuse, missing baselines, IMC redundancy) turned out to be either inaccurate upon verification against the paper or outside the paper's stated scope. This suggests the paper's core contribution is solid but its evaluation narrative overreaches in positioning the comparison with Baffle. The empirical study in Section 4 — the paper's strongest component — received no substantive criticism and was correctly identified as a genuine strength.

## Suggestions

1. **Restructure the Baffle comparison.** Either (a) evaluate Baffle on its own terms (return degradation under trigger) as a separate analysis and report this alongside TrojanTO's ASR/CP without claiming direct superiority, or (b) acknowledge the threat-model mismatch explicitly and limit the comparison to the dimensions where both methods are comparable (poisoning efficiency, BTP preservation). Do not compute CP for Baffle from an ASR that is inappropriate for its objective.

2. **Clarify trajectory provenance.** In Section 3.3, explicitly state where the adversary's trajectories come from (e.g., self-collected using a pretrained policy in a simulator), how many are needed, and what "0.3%" refers to.

3. **Report standard deviations in Table 4** or provide per-run results in an appendix with a summary of variance in the main text.

4. **State the ε value for ASR** in the main text (Section 3.4 or Table 4 caption).

5. **Provide IMC adaptation details** — specify which layers were modified, loss functions, hyperparameters, and trigger initialization used for the IMC baseline.

---

**Calibration Anchors:** The following anchors from the deepreview_13k_calibration corpus were used to calibrate the score (rounds: bracket → narrow → final).

| Path | Avg Score | Round | Comparison to this paper |
|------|-----------|-------|-------------------------|
| `5kMwiMnUip.md` (LLM jailbreaking) | 1.40 | Bracket (high<1.5) | Much weaker; unrelated topic and rejected by all reviewers |
| `Uj0h13lVrR.md` (GFlowNets) | 1.00 | Bracket (high<1.5) | Fundamentally flawed; not comparable |
| `66e22qCU5i.md` (Certified Copy backdoor) | 3.00 | Bracket (1.5–3.5) | Weaker contribution; questionable motivation and limited applicability |
| `S5JCqTJyKj.md` (Deferred backdoor) | 3.00 | Bracket (1.5–3.5) | Weaker; weak threat model and insufficient experiments |
| `ZyPRwskBli.md` (Backdoor in Seconds) | 4.75 | Bracket (3.5–5.5) | Most similar anchor. Same general area (post-training backdoor). Weaker on empirical grounding but stronger on evaluation breadth. Both have baseline comparison issues. |
| `vRyp2dhEQp.md` (Efficient Backdoor Attacks) | 5.75 | Narrow (4.5–6.5) | Slightly stronger evaluation despite varying reviewer scores. Accepted. |
| `AKAlVyunxA.md` (SHINE RL defense) | 5.75 | Narrow (5.0–6.5) | Different task (defense vs attack) but same RL domain. Comparable quality but rejected. |
| `krx55l2A6G.md` (Hiding in Plain Sight) | 6.20 | Bracket (5.5–7.5) | Stronger execution; accepted with minor nice-to-have weaknesses |
| `Bo62NeU6VF.md` (Backtracking safety) | 8.00 | Bracket (7.5–8.5) | Significantly stronger; different subfield |

**Bracket (Round 1):** 4.5–6.5, based on comparison to "Backdoor in Seconds" (4.75) and "Efficient Backdoor Attacks" (5.75).

**Narrowing (Round 2):** The paper's evaluation issues (Baffle comparison, trajectory provenance) are significant but fixable, placing it below "Hiding in Plain Sight" (6.20) but above "Backdoor in Seconds" (4.75) due to stronger empirical grounding and clearer motivation. Narrowed to 5.0–6.0.

**Final:** 5.5 — the paper has a genuine contribution and the issues are addressable in rebuttal.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>