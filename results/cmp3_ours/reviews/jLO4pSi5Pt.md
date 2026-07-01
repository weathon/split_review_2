Now I have enough calibration context. Let me write the final review.

## Summary

This paper introduces L-TTA, the first method to address Test-Time Adaptation (TTA) for Vision-Language Models (VLMs) under long-tailed test distributions. It proposes three co-designed components: Synergistic Prototypes (SyPs) to enrich tail-class representations via two types of prototypes, Rebalancing Shortcuts (RSs) for learnable class-rebalancing via cross-attention with hyper-class vectors, and Balanced Entropy Minimization (BEM) to counter head-class bias in standard entropy minimization. Experiments across 15 datasets, 3 imbalance ratios, 6 backbones, and 11 baselines show consistent improvements in both accuracy and macro-F1.

## Strengths

- **Well-motivated problem.** Long-tailed test distributions are a realistic scenario that existing VLM-based TTA methods do not address. The paper correctly identifies that TTA's online/one-epoch nature precludes standard long-tailed remedies like up-sampling, and that VLM-specific issues (text-prior bias, modality mismatch) add complexity beyond what unimodal LT-TTA methods handle.

- **Extensive experimental scope.** The evaluation covers 15 datasets across three benchmarks (OOD, cross-domain, corruption), three imbalance ratios (10, 20, 50), six backbones (RN50, ViT-B/16, ViT-L/14, ViT-H/14, SigLIP-L/16, MetaCLIP-BigG), and 11 baselines. Few papers in this area run this many configurations.

- **Consistent improvements.** L-TTA outperforms prior methods on nearly every dataset × imbalance-ratio combination. The macro-F1 gains (typically larger than accuracy gains) verify that the method helps tail classes rather than just boosting head-class accuracy. For example, on the cross-domain benchmark the macro-F1 improvement over the next best method is +2.20% vs. +1.02% for accuracy.

- **Reasonable computational cost.** At 1.45h on a single A100, L-TTA is faster than prompt-learning baselines (TPT: 3.80h) and far faster than methods that backpropagate through the visual encoder (WATT: 27.7h, RLCF: 18.3h), while achieving the best harmonic mean of accuracy and macro-F1.

## Weaknesses

### Major

- **Overstated novelty claims.** The abstract states "As the first attempt to solve this problem" and Contribution ➋ says "the first TTA for long-tailed settings." However, the paper itself acknowledges in Section 2.1 (line 58) that prior work (SAR, DELTA) addresses non-i.i.d. and class-imbalance issues in TTA. The paper's genuine contribution — and what distinguishes it — is being the first method to address LT-TTA **for VLMs**, where cross-modal misalignment and text-prior bias introduce unique problems. The unqualified "first" claims are broader than what the paper demonstrates and should be precisely scoped. This is a framing error that can mislead readers but does not diminish the technical contribution.

- **The two motivating failure modes are asserted without dedicated empirical validation.** The paper motivates its entire method around "Text-induced Tail Erosion" and "Modality-bias Amplification" (Section 1, line 38), but neither is experimentally validated. Figure 1(b) is an illustration rather than a data plot. There is no experiment measuring whether text embeddings carry pre-training biases that correlate with head/tail status, and no quantification of the claimed performance drop from applying unimodal SAR on a VLM backbone. Since all three proposed components (SyPs, RSs, BEM) are explicitly motivated by these failure modes, the absence of empirical grounding weakens the motivation-to-design chain. The paper would be strengthened by including controlled experiments demonstrating these phenomena.

### Minor

- **Ablation study does not cleanly isolate BEM from standard EM.** Table 6 compares combinations of components, but it is unclear what loss the "SyP(DP+EP)+RS" row uses — standard EM or no optimization loss at all. If it uses no loss, the comparison conflates adding BEM with adding any loss. The marginal gain of BEM over SyP+RS is modest (+0.36% accuracy, +0.66% macro-F1 on ViT-B/16), and without a direct comparison of SyP+RS+standard EM vs. SyP+RS+BEM, the specific contribution of the balanced loss term cannot be cleanly assessed. The paper should explicitly clarify what loss is used in the ablated variants.

- **Class prior estimation creates a potential circular dependency.** The class prior π in BEM (Eq. 9, line 138) is "continually updated based on the current predicted pseudo-labels." Early in the test stream, pseudo-labels for tail classes will be unreliable. Using these unreliable predictions to estimate the prior could compound errors: the model underestimates tail-class frequency → BEM allocates less correction to tail classes → tail classes remain under-adapted. The paper does not discuss this risk. While the empirical results suggest it is not fatal in practice, the concern should be acknowledged and ideally tested (e.g., by comparing with ground-truth priors on synthetic settings).

- **EP update rule updates all C class prototypes per sample but the impact is not analyzed.** Equation 5 (line 108) updates every class prototype for each view with weight φ_c determined by prediction probability differences. The paper claims this "captures more refined inter-class associations" (line 110), but the mechanism is not ablated. It is equally plausible that this introduces noise into tail-class prototypes by overwriting them with features from unrelated classes. An ablation comparing (a) all-class update, (b) top-k update, and (c) predicted-class-only update would clarify whether the all-class design is beneficial.

### Trivial

- **The "theoretical propositions" are descriptive rather than providing non-trivial insight.** Proposition 1 restates a known behavior of entropy minimization under class imbalance — head-class gradients push toward higher confidence, tail-class gradients push the opposite way. Proposition 2 states that BEM reduces the gradient gap between head and tail classes, which follows directly from BEM's design (the penalty term dampens confident-class gradients). These are valid formalizations of the method's properties but do not constitute a genuine theoretical contribution. The paper should describe them as "empirical properties" or "design justifications" rather than "theoretical propositions with theoretical capabilities" (line 44).

## Nice-to-Haves

- **Empirically validate the motivating failure modes** by running a controlled experiment: apply a standard VLM TTA method on a long-tailed test set and decompose errors by head vs. tail class status and by zero-shot accuracy per class. This would show whether "text-induced tail erosion" actually occurs and quantify its magnitude.

- **Ablate the all-class EP update** against simpler alternatives (EP for predicted class only; EP for top-3 classes).

- **Report standard deviations or confidence intervals** for the 5-run experiments, especially since some margins are small (0.5–1%).

- **Provide sensitivity analysis for the entropy threshold θ** (Eq. 4), which controls which samples contribute to prototype updates and could significantly affect tail-class prototype quality.

## Removed Points

The following points from the input reviews were removed with justification:

1. **Formatting criticism of Eq. 4 norm operators** — This is a parser artifact; the original submission does not have this issue. (Hard rule: formatting artifacts)
2. **Table 7 formatting as garbled** — Parser artifact affecting table rendering. (Hard rule: formatting artifacts)
3. **Missing appendix/proof details** — The appendix exists in the original submission; the parser strips it. (Hard rule: missing appendix)
4. **Missing related work** — Cannot verify without external sources. (Hard rule: do not mention missing related work)
5. **Reproducibility nitpicks about undisclosed hyperparameters** — Trivial implementation details. (Hard rule: reproducibility nitpicks)
6. **Statistical significance concern as a major weakness** — The paper reports 5 runs; lack of std dev is a nice-to-have, not a weakness that threatens the conclusions. (Soft rule: weaken)
7. **CRA loss being under-explained** — The explanation is sufficient for the intended purpose; the connection to long-tailed problem (reducing head-class dominance) is stated. The critic's request for deeper mechanism explanation exceeds what is standard for a design component. (Soft rule: weaken)
8. **"First" claim being fatal** — This is a framing error, not a methodological flaw. It does not invalidate the technical contribution. (Demoted from fatal to major)

## Novel Insights

None beyond the paper's own contributions. The harsh critic's observation that the "propositions" are descriptive rather than theoretically deep is accurate but not novel — it is evident from the paper's own content. The critic's identification of the ablation ambiguity (whether "SyP+RS" uses EM or no loss) is a genuinely useful observation for improving reproducibility.

## Suggestions

1. Qualify all "first" claims to explicitly state "first for VLMs" and acknowledge SAR/DELTA as prior LT-TTA methods.
2. Add a dedicated experiment (even in supplementary) that validates the two claimed failure modes, or soften the language to acknowledge they are reasoned hypotheses.
3. Clarify what loss "SyP+RS" uses in Table 6 and add a direct "SyP+RS+standard EM" row alongside "SyP+RS+BEM" to isolate BEM's marginal effect.
4. Discuss the pseudo-label circular dependency risk in BEM and ideally test against ground-truth priors in a controlled setting.
5. Add an ablation of the EP all-class update against simpler alternatives.

## Score and Decision

### Calibration

Retrieved anchors and comparison summary:

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| `5lUdTogEL3.md` | 1.00 | R1 (strong reject) | Unrelated topic (person ReID); far weaker paper |
| `pdzHpQbGrn.md` (Active TPT) | 2.50 | R1 (reject) | Similar VLM TTA topic; less thorough experiments, more significant framing issues |
| `lF9QXpfNHm.md` (ROSITA) | 4.67 | R1 (reject) | Similar VLM TTA topic; less comprehensive baselines, technical contribution less clear |
| `eXrUdcxfCw.md` (Prototype CTA) | 4.80 | R2 (reject) | Similar prototype-based TTA; novelty concerns more severe |
| `BUDxvMRkc4.md` (BLG) | 4.67 | R1 (reject) | VLM + long-tail, but not TTA; narrower evaluation |
| `KNtcoAM5Gy.md` (BaFTA) | 5.50 | R2 (reject) | Similar VLM TTA topic; less thorough experiments, unfair comparisons |
| `yD2JMeKumt.md` (DOTA) | 6.00 | R1 (reject) | Similar VLM TTA; more significant methodological clarity issues |
| `75PhjtbBdr.md` (Multi-label TTA BEM) | 6.25 | R1 (accept) | Shares "BEM" naming; different problem (multi-label vs. long-tail); comparable empirical quality |
| `kIP0duasBb.md` (RLCF) | 6.67 | R1 (accept) | VLM TTA, extends to multiple tasks; comparable experimental quality |
| `b20VK2GnSs.md` (Concept Drift MLLM) | 7.00 | R1 (accept) | Addresses long-tailed + OOD for MLLMs; slightly broader scope |

**Round 1 bracket:** 5.5 – 7.0. The paper is clearly stronger than the 4–5 range papers (which have novelty or fairness concerns) and is comparable to the 6–7 range papers. It does not reach the 8+ tier (which requires exceptional novelty, breadth, or theoretical depth).

**Round 2 narrowing:** The paper's experimental scope and problem formulation are on par with accepted papers in the 6.0–6.5 range (RLCF, Multi-label BEM). However, the overclaimed novelty framing and the lack of empirical validation for the motivating failure modes pull it toward the lower end of this band, preventing it from reaching 6.5+. It is clearly above the rejected 5.5 paper (BaFTA), which had more serious experimental fairness issues.

**Final score: 6.0.** This reflects a borderline accept: the paper makes a genuine contribution to an underexplored problem with thorough evaluation, but the overstated "first" claims and the gap between asserted failure modes and empirical validation prevent it from being a clear accept. The weaknesses are addressable in revision.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>