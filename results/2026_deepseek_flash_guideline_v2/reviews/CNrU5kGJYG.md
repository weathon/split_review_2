## Summary

TrojanTO proposes the first action-level backdoor attack against Trajectory Optimization (TO) models in offline RL (DT, GDT, DC). It is a post-training attack using three components — trajectory filtering, batch poisoning, and alternating trigger-model co-optimization — to implant a backdoor that makes the model output a specific target action when a learned trigger is added to the state. Evaluated across six D4RL tasks and three model architectures, TrojanTO achieves an average CP of 0.701 using only 0.3% of trajectories for fine-tuning while preserving benign performance (avg. BTP 0.914).

## Strengths

1. **First systematic study of action-level backdoors for TO models with a rigorous factor analysis (Section 4, Tables 1–3).** The paper systematically investigates target action selection, trigger design, and reward manipulation. Key findings — that boundary vs. interior target actions dramatically affect ASR, that trigger dimensions and values are critical, and that reward manipulation has negligible impact — provide principled guidance for attack design and establish a more complete evaluation methodology than prior work.

2. **High attack effectiveness at a very low poisoning budget across diverse settings (Table 4).** Across 18 model–environment–TO architecture combinations, TrojanTO achieves an average CP of 0.701 and BTP of 0.914 using only 0.3% of trajectories. This concretely demonstrates that post-training action-level backdoors are feasible for TO models.

3. **Clean component-level ablation confirming each module's contribution (Table 5).** Removing alternating training drops ASR from 0.719 to 0.507; removing batch poisoning drops ASR to 0.528; removing trajectory filtering drops BTP from 0.914 to 0.850. These controlled comparisons validate the design rationale.

4. **Demonstrated robustness to trigger perturbations (Table 7).** Under 10% multiplicative noise on the trigger, ASR degrades gracefully (e.g., 0.980→0.777 for Walk) rather than collapsing, a practically relevant property not evaluated in prior TO backdoor work.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **The main baseline comparison is between methods designed for fundamentally different tasks, and the headline improvement claim is overstated.** The paper describes Baffle as a policy-level backdoor (Section 3.2: "focuses solely on whether the adversary's objective can be achieved and does not consider the model's specific actions") but evaluates it using ASR, an action-level metric requiring output-to-target matching within a threshold. Evaluating Baffle with ASR is expected to produce low numbers by construction because Baffle was never designed to output a precise target action. The "105% improvement over Baffle" claim should be heavily caveated, and an adapted action-level baseline (e.g., porting TrojDRL to the TO setting) would provide a fairer comparison. The ablation study partly fills this gap by comparing against TrojanTO without its components, but that is an internal baseline, not an external one.

2. **The ASR threshold ε is not specified in the main text.** Equation (2) defines ASR using a threshold ε on per-component action difference, but no value for ε is given in the main paper. Since ε directly controls the stringency of the primary effectiveness metric, this makes every ASR and CP number in the main text uninterpretable — an ASR of 0.719 with ε = 0.5 means something very different from ε = 0.001. This parameter should be stated explicitly alongside the metric definition. (If reported in the appendix, it belongs in the main text as a metric parameter, not an implementation detail.)

3. **The "0.3% vs. 10%" budget comparison conflates different pipeline stages.** TrojanTO (post-training) uses 0.3% of trajectories for fine-tuning model parameters. Baffle (pre-training data poisoning) uses 10% of trajectories injected into the training dataset. These are different stages with different cost structures and threat models; presenting them as a direct efficiency comparison is misleading without clarifying this incommensurability.

4. **Main results average over target types, masking large performance variation.** Section 4.1 shows that boundary action '1' achieves ASR near 1.0 across tasks, while interior targets like 'fixed random' and 'arithmetic' can be substantially lower (e.g., '0' type achieves only 0.110 ASR in Walk). Table 4 averages over three target types, so the reported ASR of 0.719 is likely dominated by the boundary condition. A per-target-type breakdown in the main text is needed for readers to assess where the method works and where it struggles. (Complete per-target results are deferred to the appendix.)

### Trivial

1. **Zero standard deviations in Tables 6 and 7.** Several entries report 0.000 standard deviation across three seeds (e.g., Table 6: Hopp k=0 shows 0.922 ± 0.000). For stochastic RL evaluations, three-seed variance of exactly zero is suspicious and likely reflects deterministic evaluation conditions, which should be stated explicitly.

## Nice-to-Haves

- An adapted action-level baseline from the RL backdoor literature (e.g., TrojDRL) adapted to the TO setting would provide a fairer comparison than Baffle's policy-level attack.
- A sensitivity analysis showing how ASR varies with ε would address the uninterpretability of the metric.
- The defense analysis (Section 6.5) is purely qualitative ("fine-tuning is most effective, others are ineffective") without any results or protocol details. Quantitative results would strengthen this discussion.

## Removed Points

- **Criticism that ε is missing entirely (original framing as "structural" flaw).** The ε is likely reported in the appendix (which the parser strips). However, the point that ε should be in the main text is retained as a minor weakness since it is a metric parameter, not an implementation detail.
- **Criticism that baseline comparison is "structurally invalid" / "fatal."** While the comparison between Baffle (policy-level) and ASR (action-level metric) is imperfect, the paper rightfully positions Baffle as the closest prior work in offline RL backdoors, and the comparison is informative even if not apples-to-apples. The "105% improvement" framing is the issue, not the comparison itself. Downgraded to minor.
- **Criticism about CP metric using harmonic mean without justification.** The paper cites prior work (Ma et al., 2025) for this metric choice, which is standard practice.
- **Strength Finder's generic strengths removed** (e.g., "paper addresses an important problem" — generic and not specific to this paper's evidence).

## Novel Insights

The paper's own analysis reveals an interesting asymmetry: for TO models, reward manipulation — the central attack vector in all prior RL backdoor work — is essentially irrelevant, while the connection between trigger states and target actions is the only thing that matters. This reverses a key assumption in the adversarial RL literature.

## Suggestions

1. Report ε explicitly in the main text alongside Equation (2), with a brief justification.
2. Add a per-target-type breakdown of Table 4's main results to the main text, or at minimum note the boundary/interior gap explicitly when discussing the averaged numbers.
3. Either acknowledge the Baffle comparison limitation explicitly, or include a simple adapted action-level baseline (e.g., fine-tuning with the poisoned loss alone, without alternating training — partially covered by the ablation).
4. Clarify whether evaluation is deterministic and explain entries with 0.000 standard deviation.
5. Add quantitative results to the defense analysis (Section 6.5).

---

**Calibration note:** The calibration corpus was not accessible, so anchors could not be retrieved. The score is based on assessment of the paper's content against the ICLR review criteria.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>