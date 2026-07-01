Now I have a good calibration picture. Let me finalize the review.

**Round 1 bracket**: Based on the calibration anchors, this paper sits between the 4.0 (em0gAL8fbK.md - backdoor attack on offline RL) and 5.75 (AKAlVyunxA.md - backdoor defense in RL, and HZnnHDrBXD.md - action attack on continuous RL) anchors. The paper has a genuine problem and useful empirical findings, but the evaluation issues (metric mismatch for Baffle, ε not reported, data access tension) are meaningful. I place the narrowest plausible range at 4.5–5.5.

Let me finalize:

**Final score**: 5.0 — the paper identifies a genuine gap and presents a reasonable method with useful empirical findings, but the evaluation has meaningful weaknesses that prevent it from being clearly borderline-acceptable. Score 5 is between borderline reject and borderline accept, reflecting that the contribution is real but the current evaluation does not fully support the strength of claims made.

Now let me write the final review.## Summary

This paper proposes TrojanTO, the first action-level backdoor attack against trajectory optimization (TO) models in offline RL. It identifies that existing RL backdoor attacks relying on reward manipulation during training are incompatible with TO models (trained via behavior cloning), and introduces a post-training attack using trajectory filtering, batch poisoning, and alternating training. A key empirical contribution is the finding that reward manipulation is irrelevant for backdooring TO models, while target action and trigger design are critical. The method achieves a claimed 0.3% poisoning rate across DT, GDT, and DC architectures on six D4RL environments.

## Strengths

1. **Timely problem identification.** The paper correctly identifies that existing RL backdoor attacks (which manipulate reward signals during training) do not transfer to TO models trained via behavior cloning. This gap between the backdoor literature and modern TO architectures (Decision Transformer, Graph Decision Transformer, Decision ConvFormer) is a genuine and timely concern as TO models grow in adoption.

2. **Useful empirical findings in Section 4.** The demonstration that reward manipulation is largely ineffective for backdooring TO models (Section 4.3, Figure 1) is a non-trivial insight that meaningfully distinguishes this setting from traditional RL backdoors. The systematic investigation of target action type (boundary vs. interior) and trigger dimension selection (Tables 1–3) provides practical guidance that could inform future attack and defense work in this space.

3. **Low claimed poisoning rate.** Requiring ~0.3% poisoned trajectories (versus Baffle's 10%) is a meaningful practical advantage if validated. The trajectory filtering and batch poisoning mechanisms that enable this efficiency are well-motivated design choices.

## Weaknesses

### Fatal

None.

### Major

1. **Baffle comparison uses a metric mismatch.** The paper compares Baffle (Gong et al., 2024b) — which it itself categorizes as a *policy-level* backdoor in Section 3.2 — on ASR, a metric that measures whether a *specific target action* is output at a triggered step. A policy-level attack is designed to manipulate long-term agent behavior, not to force a particular action at a particular time. The headline claim of "105.0% improvement compared to Baffle" (line 268) and the CP metric (which embeds ASR) inherit this issue: they compare fundamentally different attack objectives on a metric only one is designed to optimize. This does not invalidate the paper's contribution, but the comparison as presented is misleading. Baffle should either be adapted to an action-level setting (with the adaptation described and justified), or clearly framed as a reference point rather than a direct competitor, with the "105.0%" rhetoric removed or qualified.

2. **ASR threshold ε is never reported.** Equation (2) defines ASR using a threshold ε that determines how close the model's output must be to the target action to count as a successful attack. This ε value is never stated anywhere in the paper. Since ASR is the paper's primary effectiveness metric and the paper uses continuous action spaces, the threshold choice directly controls the stringency of the metric. A loose ε would trivially inflate ASR, especially for boundary actions (which already achieve near-100% ASR). Without knowing ε, a reader cannot assess whether "high ASR" reflects genuine precise action control or a generous tolerance. This must be reported in the main paper and justified.

3. **Unresolved tension in the threat model about data requirements.** The threat model states the adversary "aims to implant a backdoor into the pretrained TO model without access to the original training dataset" (line 60). However, TrojanTO's method operates on a filtered set of trajectories F_τ and computes both a poisoned loss L_p (Equation 5, requiring poisoned transitions) and a clean loss L_c (Equation 6, requiring ground-truth actions from clean trajectories). The paper never clarifies where these clean trajectories come from — are they the original training set (contradicting the threat model), or a separately collected set? The 0.3% poisoning rate is cited as a percentage of what reference set, and this denominator is never defined. The clean loss term implies the adversary needs substantial clean data to maintain BTP, which should be explicitly acknowledged in the threat model rather than framed as "without access to the original training dataset."

### Minor

1. **Several entries show ±0.000 standard deviation across three runs (Tables 6, 7).** In RL experiments, zero variance across multiple seeds is unusual and the paper does not explain it. While ceiling effects (ASR=1.0) could explain some cases, non-ceiling values also report zero variance (e.g., Table 6: Hopp k=5 at 0.898 ± 0.000; Walk k=0 at 0.993 ± 0.000; Table 7: Hopp η=0% through η=10% all ±0.000). The paper should clarify whether the optimization is deterministic or if there is a methodological reason for the absence of variance.

2. **The "superior reliability" claim (line 272) is overstated given individual cases where baselines match or exceed TrojanTO.** For instance: DC+Ant (IMC CP 0.752 vs. TrojanTO 0.559), DC+Pen (IMC CP 0.655 vs. TrojanTO 0.477), DT+Kit (Baffle CP 0.766 vs. TrojanTO 0.614). TrojanTO wins on average across all settings, but claiming "consistent robustness and stability across varied tasks" and "superior reliability" goes beyond what the evidence supports when baselines outperform TrojanTO in multiple individual cells of Table 4.

3. **Standard deviations are absent from Table 4**, the main results table. Given the zero-variance observations in Tables 6–7, reporting variance for the central comparison would help assess whether the reported averages are reliable.

4. **No baseline comparisons for persistent backdoor and trigger perturbation experiments (Tables 6, 7).** These tables demonstrate TrojanTO's capabilities in isolation (persistence across k steps, robustness to noise), but do not establish whether Baffle or IMC could achieve similar results. Without baseline comparisons, these results show a capability but do not demonstrate that TrojanTO is uniquely capable of it.

### Trivial

None.

## Nice-to-Haves

- Report ASR across multiple ε values to demonstrate results are not artifacts of a loose threshold.
- An analysis of whether the backdoored model leaves detectable signatures (activation pattern differences, trigger-specific gradients). Testing detection resistance would strengthen the security claims.
- A more principled approach to trigger dimension selection. The paper shows the choice dramatically affects ASR (from 0.915 to 0.000 depending on dimensions in Table 2) but fixes dimensions to (1,2,3) based on empirical success for specific environments, without a principled justification for transferability.
- Add baseline comparisons to the persistent backdoor and trigger perturbation experiments.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"IMC comparison is circular"** — REMOVED. The paper states the alternating training is "drawing inspiration from" IMC (line 207). Comparing TrojanTO (IMC + trajectory filtering + batch poisoning) against vanilla IMC is a valid ablation that quantifies the value of domain-specific adaptations. This is not circular; it is a standard comparison. The broader point about lacking a genuinely competitive action-level baseline designed for sequential decision-making is noted but is a scope issue rather than a methodological flaw.

- **Criticism about "large-scale" framing being overstated** — REMOVED. The paper's claim that retraining TO models is "prohibitively expensive" is a relative statement about fine-tuning vs. full retraining and is standard in the literature.

- **"Post-training" label ambiguity** — REMOVED. The paper clearly defines its three-way categorization (pre-, during-, post-training) and TrojanTO fits within it. Using fine-tuning data for post-training modification is standard for this attack paradigm.

- **Section 4.1 interior target actions** — REMOVED as a weakness. The paper acknowledges the limitation and explicitly evaluates against diverse target actions.

- **Defense section being perfunctory** — REMOVED as a distinct weakness. Detailed results are deferred to the appendix, which is standard practice for conference papers.

## Novel Insights

None beyond the paper's own contributions. The reviews surface verification issues about the evaluation design (metric mismatch, unreported threshold, data access tension) rather than generating new analytical insights about the method itself.

## Suggestions

1. Report the ε value for ASR in the main paper, justify the choice, and consider showing ASR across multiple ε values.
2. For the Baffle comparison: either adapt Baffle to an action-level setting (describing the adaptation) or clearly frame it as a reference point and remove/qualify the "105% improvement" claim.
3. Clarify the data-access setup: specify where the clean trajectories used for L_c come from, what the 0.3% poisoning rate denominator refers to, and adjust the threat model language to honestly reflect the data requirements.
4. Explain the zero-variance entries in Tables 6–7 or report individual seed values.
5. Add standard deviations to Table 4 or include a variance-aware summary of the main results.
6. Temper the "superior reliability" claim to acknowledge the individual cases where baselines outperform TrojanTO.

## Score and Decision

**Calibration anchors (all rounds):**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| em0gAL8fbK.md — "Temporal Logic-Based Multi-Vehicle Backdoor Attacks against Offline RL" | 4.00 | R1 | Similar domain (backdoor attack on offline RL); rejected. TrojanTO has lower poisoning rate and more environments, but comparable evaluation issues. |
| AKAlVyunxA.md — "SHINE: Shielding Backdoors in Deep RL" | 5.75 | R1 | Defense paper with theoretical guarantees and comprehensive evaluation; rejected but scored higher. TrojanTO lacks theoretical guarantees. |
| HZnnHDrBXD.md — "Tree-based Action-Manipulation Attack Against Continuous RL" | 5.75 | R1 | Attack paper with theoretical analysis on continuous RL; rejected. TrojanTO evaluates more broadly across models and environments. |
| GxCGsxiAaK.md — "Universal Jailbreak Backdoors from Poisoned Human Feedback" | 5.75 | R1 | Accepted RL backdoor paper with comprehensive experiments. TrojanTO's evaluation is less thorough by comparison. |

**Round 1 bracket:** 4.5–5.5. The paper identifies a genuine gap with useful empirical findings but has meaningful evaluation issues that prevent a clear acceptance recommendation.

**Narrowing:** Compared to the em0gAL8fbK.md anchor (score 4.0), TrojanTO has a more novel contribution (first action-level backdoor for TO models, finding about reward irrelevance) and a much lower poisoning rate (0.3% vs 15%). However, the Baffle metric-mismatch and missing ε are evaluation issues of similar severity to the calibration paper's high poisoning rate weakness. This pushes the paper above 4.0. Compared to the 5.75 anchors (SHINE, LCBT), TrojanTO lacks theoretical guarantees and has a less clean evaluation, placing it below 5.75.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>