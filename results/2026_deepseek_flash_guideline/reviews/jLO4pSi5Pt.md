Now I have a calibrated understanding. Let me finalize the review.

## Summary

This paper introduces L-TTA, the first method for Test-Time Adaptation (TTA) of Vision-Language Models (VLMs) under long-tailed test distributions. It proposes three co-designed components: Synergistic Prototypes (SyPs) with Deterministic and Exclusionary Prototypes to enrich tail-class representations, Rebalancing Shortcuts (RSs) for learnable class rebalancing, and Balanced Entropy Minimization (BEM) as a theoretically motivated objective that mitigates EM's bias toward head classes. Experiments across 15 datasets, three benchmarks, and multiple backbones show consistent improvements over 12 baselines.

## Strengths

- **Exclusionary Prototypes (EPs) design explicitly addresses tail-class sparsity.** The paper identifies that tail-class prototypes remain uninitialized or store inadequate semantics during the data stream, and proposes EPs that are updated for *all* classes using prediction distributions (Eq. 5). This differs from prior work like TDA's "negative cache" which only updates the predicted class. The ablation (Table 6) provides direct evidence: dropping EPs reduces macro-F1 by ~3.22% on ViT-B/16.

- **Two theoretically grounded propositions characterize the long-tailed EM bias and the corrective effect of BEM.** Proposition 1 formalizes that standard entropy minimization drives head-class logit gradients negative while tail-class gradients remain positive. Proposition 2 proves that BEM shortens the optimization gap between head and tail classes. These give the method a foundation beyond heuristic design.

- **Comprehensive evaluation across 15 datasets, 3 imbalance ratios (10, 20, 50), 3 benchmarks (OOD, Cross-Domain, Corruption), and 4 backbones (ViT-L/14, ViT-H/14, SigLIP-L/16, MetaCLIP-BigG).** L-TTA outperforms 12 prior methods in nearly every setting, with particularly strong macro-F1 gains (e.g., +3.61% over DPE at imb=10 on OOD Average) that directly support the rebalancing claim.

- **Efficiency analysis (Table 4) demonstrating a favorable accuracy–cost trade-off.** L-TTA achieves the highest harmonic mean (67.20 on LT-CDB, 46.08 on LT-CB) while using only 1.45h runtime — substantially cheaper than RLCF (18.30h) and WATT (27.70h). The authors explain this via parallel prototype updates and shortcut optimization free of backbone gradient tracking.

- **Systematic ablation isolating each component's contribution (Table 6, Figure 4).** Each component (DP, EP, RS, BEM) contributes non-trivially, and the full method consistently outperforms partial combinations.

## Weaknesses

### Major

- **Identical MTA results across different imbalance ratios in Table 1 raise data-integrity concerns.** MTA's ImageNet-A results (Acc=57.15, Mac=51.98) are identical across all three imbalance ratios (10, 20, 50). MTA's ImageNet-V2 results (Acc=63.61, Mac=62.69) are identical at imb=10 and imb=50. Since the paper states that it creates long-tailed versions of datasets by "random sampling to manipulate the cardinality distribution into an exponentially decayed curve" for each imb ratio, the test subsets should differ. Identical results to two decimal places across different data subsets is unexpected. While MTA is described as a training-free method (line 208, 299), other training-free methods like ZERO show different values across imb ratios, so this does not fully explain the pattern. This does not invalidate the paper's own method (L-TTA's own results do not exhibit this pattern), but it undermines confidence in the experimental reporting and the fairness of baseline comparisons. The authors must explain this before the results can be fully trusted.

### Minor

- **No variance or error bars reported despite claiming 5 runs per experiment.** Many of L-TTA's accuracy gains over the strongest baselines are modest — e.g., 1-2% on OOD Average — and without standard deviations it is impossible to assess whether differences are meaningful. This is especially important given the multi-component nature of the method (three components, multiple hyperparameters) where variance could be considerable.

- **The term `\tilde{\mathbb{P}}` in Eq. 9 is not explicitly defined.** The BEM formulation (Eq. 9) uses `\tilde{\mathbb{P}}` in the penalty term `(1 - \tilde{\mathbb{P}})^\beta`, but what this represents (softmax over which logits, for which class) is never stated. This makes the precise mechanism of BEM ambiguous.

- **The split criterion for head vs. tail classes in Propositions 1 and 2 is not specified** ("We split C into C_head and C_tail with certain measurements"), making the theoretical statements less precise than they could be. The proofs are deferred to an appendix that is not accessible in this version.

- **The ablation does not isolate the EP mechanism from a simpler alternative.** Replacing EPs with a vanilla negative cache (as in TDA) while keeping everything else identical would clarify whether the specific EP design drives the gain, or whether simply having more prototypes in general suffices.

### Trivial

- **Minor notation:** Eq. 7 (CRA loss) is dense and the parentheses make it difficult to parse as typeset. It would benefit from a cleaner breakdown.

## Nice-to-Haves

- A direct comparison of BEM against plugging a standard long-tailed technique (e.g., logit adjustment) into a strong TTA baseline (e.g., DPE) would strengthen the claim that a specialized objective is necessary, rather than simply applying existing LT techniques.
- Analysis of whether tail-class EPs become contaminated with actual tail-class features (since the model may not recognize tail samples as such) would address a conceptual concern about the EP design noted in the paper's own analysis.

## Removed Points

- **Criticism about "not presenting empirical evidence that failure modes occur"** — The paper provides evidence via Figure 2 and the SAR-on-VLM-backbone example (line 38). The claim that no experiment "tests whether they were actually mitigated" is excessive as the overall LT-TTA benchmark results implicitly validate the design motivation.
- **Criticism about missing related work comparisons (DELTA)** — The paper discusses DELTA in Section 2.1 (line 58) and correctly notes the distinction: DELTA addresses class bias via re-weighting for non-i.i.d. test data, while L-TTA tackles the VLM-specific long-tailed TTA problem. The existing coverage is adequate.
- **Criticism about not adapting LT methods to TTA baselines** — This is a reasonable suggestion (moved to Nice-to-Haves) but not a weakness; the paper defines a new problem and compares against existing TTA methods as-is.
- **Claim that "accuracy gains are modest"** — The accuracy gains are modest in some settings but macro-F1 gains are substantial (up to +4.35%), which is the more relevant metric for a rebalancing method. The pattern is consistent with the paper's claims.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Address the duplicate MTA values explicitly:** Clarify the experimental procedure — were the same long-tailed subsets used for all methods? Were seeds fixed across runs? Explain how MTA's results can be identical across three different data subsets, particularly given that other training-free methods (ZERO) show variation. If this is a known property of MTA, provide a citation or analysis.

2. **Report standard deviations or confidence intervals** for the main results given the 5-run experiments claimed.

3. **Define `\tilde{\mathbb{P}}` explicitly** in Eq. 9 and clarify how the penalty term applies per-class vs. per-sample.

4. **Add an ablation** comparing EPs against a simpler negative cache baseline (e.g., TDA-style cache) to isolate the benefit of the EP design specifically.

5. **Specify the head/tail split criterion** in Propositions 1 and 2 more precisely, or acknowledge that the propositions assume such a split exists.

---

**Round 1 bracket**: Based on calibration against human-reviewed anchors, the narrowest plausible score range is [5.5, 7.0].

**Anchors retrieved across rounds**:
| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| DOTA (yD2JMeKumt) | 6.00 | 1, 2 | VLM TTA method with major methodological gaps (unclear distribution estimation, weak human feedback results); our paper has clearer methodology and more comprehensive evaluation but has suspicious data issues |
| ROSITA (lF9QXpfNHm) | 4.67 | 1 | Open-world VLM TTA, limited backbones, no error bars; our paper is stronger on all dimensions |
| BLG (BUDxvMRkc4) | 4.67 | 1 | Long-tailed VLM classification (not TTA); our paper tackles a more novel problem |
| InCPL (Rc3RP9OoEJ) | 5.00 | 1 | TTA prompt learning with marginal improvements; our paper has clearer gains and broader scope |
| Concept Drift (b20VK2GnSs) | 7.00 | 2 | VLM concept drift, accepted; stronger experimental rigor than our paper |
| Active TPT (pdzHpQbGrn) | 2.50 | 1 | Very weak novelty, limited contribution; our paper is far stronger |
| Multi-modal Reliability Bias (TPZRq4FALB) | 8.00 | 1 | Top-tier TTA paper with excellent motivation, clean experiments, strong writing; our paper is below this level |
| Prototype CZSL (eE2PXlNydB) | 6.00 | 2 | Prototype-based method in different domain; comparable quality |

**Final score rationale**: L-TTA addresses a genuinely novel problem (first LT-TTA for VLMs) with a well-motivated, multi-component method and unusually comprehensive evaluation. However, the identical MTA values across different imbalance ratios in Table 1 are a concerning data-integrity issue that demands explanation, and the lack of variance reporting weakens the quantitative evidence. These issues place the paper in borderline-accept territory. Score 6.0 reflects a paper with clear contributions that needs to address specific experimental reporting concerns before the community can fully trust the results.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>