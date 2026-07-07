Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper proposes TrojanTO, a post-training, action-level backdoor attack against Trajectory Optimization (TO) models in offline reinforcement learning. The attack uses trajectory filtering, batch poisoning, and alternating training to implant backdoors with only 0.3% poisoned trajectories. Extensive experiments across 3 TO architectures (DT, GDT, DC) and 6 D4RL environments demonstrate strong attack success while maintaining benign performance.

## Strengths

- **Identifies a genuine underexplored gap.** The paper correctly observes that existing RL backdoor attacks are designed for Bellman-equation-based agents and are ill-suited to TO models, which use sequence modeling and reconstruction loss. The post-training threat model is well motivated (Sections 1, 3.3).

- **Low poisoning rate (0.3% of trajectories) is a meaningful practical advantage** over prior work (e.g., Baffle's 10%), and the trajectory filtering and batch poisoning components that enable this are clearly described.

- **Useful empirical decomposition in Section 4.** The systematic investigation of target action types (Table 1), trigger dimensions (Table 2), and trigger values (Table 3) provides actionable guidance. The finding that reward manipulation is largely irrelevant for TO models (Figure 1) is a genuine empirical insight.

- **Broad model coverage.** The evaluation spans three distinct TO architectures (DT, GDT, DC) across six D4RL environments, giving reasonable breadth of evidence.

## Weaknesses

### Major

- **The ASR epsilon threshold is never specified.** Equation (2) defines attack success as the model's output being within $\varepsilon$ of the target action in every dimension, but no value for $\varepsilon$ is given anywhere in the paper. Since ASR is central to the evaluation (Table 4), the reader cannot interpret what ASR values mean — e.g., whether 0.99 ASR represents precise targeting or loose approximation. Without this, the core quantitative results are not interpretable or reproducible.

- **The primary baseline comparison with Baffle is on mismatched metrics.** The paper acknowledges Baffle as a "policy-level backdoor" (Section 2) that targets long-term reward manipulation, but evaluates it on action-level metrics (ASR and CP) that it was never designed to optimize. The claim of "105.0% improvement" over Baffle (Section 6.1) is therefore misleading. The paper would benefit from a fairer comparison or a clearer separation of baseline categories.

### Minor

- **No error bars in the main results.** Table 4 reports averages across 3 seeds and 3 target actions without standard deviations or confidence intervals. Given known variance in RL (cited by the paper), this makes it difficult to assess the reliability of the reported improvements.

- **The IMC baseline adaptation is not described.** The paper lists IMC (Pang et al., 2020) as a baseline in Table 4 but never explains how IMC was adapted from vision to the TO setting. Without this, the IMC results (e.g., CP of 0.013 on DT/Hopp) cannot be interpreted as inherent limitations vs. poor adaptation.

- **Tables 6 and 7 report zero standard deviations** across three random seeds for many entries (e.g., $0.922 \pm 0.000$, $0.972 \pm 0.000$, $0.993 \pm 0.000$). Exactly zero variance in RL is surprising and warrants explanation — e.g., whether this is due to a deterministic evaluation protocol or a threshold effect.

- **The trigger value experiment (Table 3) uses suboptimal dimensions.** The trigger dimension study (Table 2) found (1,2,3) to be optimal, but the trigger value comparison uses dimensions (8,9,10) without justification. This makes the comparison less informative than it could have been.

- **Defense results are deferred to the appendix.** Section 6.5 states that fine-tuning is the most effective defense, but all quantitative defense results are in Appendix B.1. Since fine-tuning is a standard defense, the main paper should at minimum summarize the key numbers.

### Trivial

None.

## Nice-to-Haves

- The paper could benefit from an ablation study comparing different batch poisoning strategies (e.g., poisoning all transitions vs. poisoning a random transition) to empirically validate the design choice in Section 5.2.
- Analyzing attack computational cost (epochs/iterations needed) would be useful for practical deployment assessment.

## Removed Points

These points from the input review were removed with justification:
- "Baffle comparison is uninformative" — Kept but downgraded from "fatal" to "Major" because the paper does acknowledge Baffle is policy-level (Section 2); the issue is the framing, not the inclusion.
- "IMC shows pathologic instability" — This is a valid observation about IMC results, not a weakness of the paper.
- "No analysis of attack cost" — Nice-to-have, not a core omission.
- "Persistent backdoor bounded by context window" — The paper acknowledges this limitation (Section 6.3).
- "Trajectory filtering assumption not validated" — A reasonable heuristic that does not require full validation.
- "First action-level claim overclaimed" — The paper says "first systematic study," which is defensible.
- Formatting/style nitpicks and grammar concerns — These are parser artifacts, not author errors.
- Missing related works — Cannot verify external references.

## Novel Insights

None beyond the paper's own contributions. The reviewer analysis primarily identifies gaps in the evaluation (missing epsilon, baseline framing, missing error bars) rather than offering new interpretations of the method itself.

## Suggestions

1. **Specify $\varepsilon$** for the ASR computation across all environments and justify the choice. Consider showing ASR as a function of $\varepsilon$ so readers can calibrate.
2. **Reframe the Baffle comparison** — either separate it into a different category ("prior methods not designed for action-level attacks") or add a proper action-level baseline.
3. **Add error bars to Table 4** — standard deviations or confidence intervals over the 3 seeds.
4. **Explain the IMC adaptation** protocol used for TO models.
5. **Address the zero-variance entries** in Tables 6 and 7.
6. **Move defense quantitative results** to the main paper or add a summary table in Section 6.5.
7. **Justify** why the trigger value experiments (Table 3) use dimensions (8,9,10) instead of (1,2,3).

## Score and Decision

**Calibration Anchors Considered:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| em0gAL8fbK.md (Backdoor attacks against offline RL in AD) | 4.00 | R1 | Yes | Similar topic; had more severe structural weaknesses (-7.99 about insufficient motivation) than this paper |
| rp5vfyp5Np.md (BATTLE, adversarial attacks on DRL) | 4.25 | R1 | Yes | Had a fatal-level novelty concern (-10.57); this paper's weaknesses are less severe |
| AKAlVyunxA.md (SHINE, backdoor shielding in DRL) | 5.75 | R1 | Yes | Stronger theoretical component and more comprehensive defense evaluation |
| ZyPRwskBli.md (Backdoor via model editing on pre-trained models) | 4.75 | R2 | Yes | Comparable quality; had overclaimed contribution (-6.15) and missing baseline issues |

**Weighted-item comparison:** My draft's strongest negative items (ASR epsilon at -4.43, Baffle comparison at -4.46) are less severe than the worst negatives in the 4.00-4.25 anchors (-7.99, -10.57) but more meaningful than the 4.75 anchor's minor negatives. My draft's strongest positives (+4.46, +4.42, +4.07) are comparable to the anchor papers' positive weights. The paper's method and problem framing are solid, but the two major evaluation issues (unspecified $\varepsilon$, Baffle comparison framing) prevent it from reaching the 5.75 level.

**Initial bracket (Round 1):** 4.0 – 5.75. **Narrowed to (Round 2):** 4.75 – 5.5.

**Final score:** 5.0 — The paper has a genuine contribution (a well-motivated post-training attack against TO models with an impressively low 0.3% poisoning rate) but the evaluation has two significant gaps (unspecified ASR epsilon making results uninterpretable, and a misleading primary baseline comparison) that prevent acceptance in current form. The weaknesses are fixable, and the underlying contribution is solid.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>