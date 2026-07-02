## Summary

This paper studies language-based audio retrieval with a dual encoder architecture enhanced by three techniques: soft-label distillation from an ensemble of retrieval teachers, LLM-driven caption augmentation (back-translation and caption mix), and cluster-guided auxiliary classification. On the CLOTHO dataset, the best single model achieves mAP@16 of 46.6 and a weighted ensemble reaches 48.8 on the development test split.

## Strengths

- **Well-motivated problem framing.** The paper correctly identifies that binary correspondence assumptions in audio retrieval datasets are a limitation, since captions can describe multiple recordings due to overlapping acoustic concepts. This framing around "non-binary audio-text correspondences" is accurate and provides a clear rationale for the soft-label distillation approach.

- **Multi-backbone evaluation.** The paper evaluates PaSST, EAT, and BEATs across all configurations (Table 2), showing that observed patterns are not specific to a single architecture. The ensemble strategies are also explored systematically.

- **Reproducible training protocol.** The three-stage pipeline (pretrain → finetune → re-finetune with clustering) is described with sufficient hyperparameter detail (learning rates, schedulers, batch sizes, loss weights, augmentation probabilities) to enable approximate reproduction.

## Weaknesses

### Fatal
None.

### Major

1. **The only novel component (cluster-guided classification) does not improve results, contradicting the paper's central claims.** Examining Table 2, the best mAP@16 for the strongest backbone (PaSST) is achieved by SID 2 (distillation alone, **46.62**) — the simplest configuration. Adding clustering (SID 4: 46.39, SID 5: 46.50) yields no improvement. The same pattern holds for EAT and BEATs. The paper's conclusion states "by utilizing clustering, we introduced an auxiliary classification task…which contributed to additional performance gains" — this is directly contradicted by Table 2. The abstract acknowledges "mixed gains" but the introduction and conclusion present clustering as a positive contribution without support from the data.

2. **No error bars or statistical significance reported.** Every result in Table 2 is a single point estimate. The differences between SID 3, 4, and 5 for PaSST mAP@16 span only 0.11 (46.41–46.50). Without multiple seeds or confidence intervals, there is no way to determine whether any configuration difference is meaningful. The paper draws conclusions about "improvements under high correspondence ambiguity" (abstract) and "mixed gains" without any statistical grounding. This prevents readers from evaluating whether the empirical claims have support.

3. **Ablation design does not isolate individual contributions.** Table 1 shows that no configuration includes clustering *without* augmentation, or clustering *without* distillation. There is no way to evaluate what clustering contributes independently of the other two components. The comparison of SID 2 vs. SID 3 (with vs. without augmentation) is available and shows negligible differences (PaSST mAP@16: 46.62 vs. 46.41), suggesting even augmentation provides marginal benefit. But the core question — "does clustering help when added to a system that does not already include augmentation?" — is left unanswered because the experimental design does not include this configuration.

### Minor

1. **Significant evaluation-to-test performance drop is unexplained.** On the development test split, the best ensemble achieves mAP@16 of 48.83. On the evaluation dataset (line 198), the same approach yields mAP@16 of 42.1 — a ~6.7 point drop. While some gap is expected when retraining on the full development split, the paper offers no analysis or discussion of this degradation. This raises questions about generalization and possible overfitting to the development split.

2. **The evaluation set result is reported as a single number without per-system breakdown.** Line 198 reports only one mAP@16 (0.421) for the evaluation dataset, making it impossible to assess which of the five system variants generalizes best. Per-system evaluation results would be informative.

3. **Framing overstates novelty.** The three contributions listed in the introduction are: (i) soft-label distillation — explicitly adopted from Primus et al. (2024) with Eqs. 5–8 being a direct reproduction; (ii) LLM-based augmentation — combining back-translation (Sennrich et al., 2015) and LLM mix (Wu et al., 2024); and (iii) cluster-guided classification — the only proposed novelty, which does not improve results. The paper would benefit from more clearly delineating what is adapted vs. novel, and honestly reporting that the novel component did not yield gains.

4. **Cluster motivation is not fully discussed.** Section 2.3 introduces clustering as a way to "learn representations that are aligned with the semantic clusters of the captions." However, if captions from very different audio clips end up in the same cluster, the classification head would push their audio representations toward the same centroid, potentially *harming* discriminative power. This tension is not acknowledged or discussed.

### Trivial
None.

## Nice-to-Haves

- Running experiments with multiple random seeds and reporting variance or confidence intervals for all metrics.
- Adding a configuration with clustering alone (without distillation or augmentation) to isolate its contribution.
- Reporting per-system results on the evaluation dataset.
- Analyzing whether the cluster-guided auxiliary task helps under specific conditions (e.g., high vs. low cluster purity, certain numbers of clusters).

## Removed Points

These points from the input review were removed:

1. **"Paper is more appropriate for a workshop venue"** — This is a venue assessment, not a weakness of the paper's technical content. Removed per instruction to avoid venue speculation.

2. **"The paper reads as a DCASE challenge system description"** — While not entirely inaccurate, this is a framing judgment rather than a specific, verifiable weakness. The relevant technical content (borrowed components, ineffective novelty) is already captured in the kept weaknesses.

3. **"No explanation for SID 4 vs SID 5 difference purpose"** — The reviewer noted that the paper doesn't explain what SID 4 vs SID 5 is supposed to test. This is partially correct but the contrast (finetuned embeddings vs. BERTopic/e5-large-v2 embeddings) is implicitly about clustering quality. This point was too granular to surface as a standalone weakness.

4. **Generic section-by-section notes** (e.g., "Section 2.2 is clearly and correctly described but it is a reproduction") — These are editorial observations rather than weaknesses. The substantive content (the borrowing is acknowledged) is already reflected in kept weaknesses.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's central insight — that the paper's novel component does not work and the claimed contributions are unsupported — is a critique that emerges directly from reading Table 2 against the paper's own claims, rather than a novel observation about the method or the field.

## Suggestions

1. Report results with multiple random seeds and include confidence intervals or error bars to establish whether any observed differences are meaningful beyond noise.
2. Add ablation configurations that isolate clustering without augmentation (e.g., SID 2 + clustering) to demonstrate its independent contribution.
3. Analyze why the evaluation set performance drops substantially (~6.7 points) compared to the development test set.
4. Either demonstrate a configuration where cluster-guided classification *reliably* helps (with statistical significance), or honestly reframe the paper around the negative result — a careful empirical study showing that cluster-guided auxiliary tasks do not improve audio retrieval. The latter would be a legitimate contribution if accompanied by diagnostic analysis explaining *why* the approach fails.
5. Provide per-system evaluation results so readers can assess generalization.

---

**Round 1 bracket determination:** After reading the paper and examining the anchored papers, the narrowest plausible score range was [2.5, 4.0]. The paper is a competent engineering effort with thorough multi-backbone evaluation, but its only novel component demonstrably fails to improve results, statistical rigor is absent, and the ablation design is incomplete. This places it below "Enhancing Audio-Language Models" (4.75, Reject) which at least shows partial gains on its targeted task, but above "SimO Loss" (3.00, Reject) which evaluates only on CIFAR-10 with no proper baselines. The paper's disconnect between claimed contributions and empirical evidence is the decisive factor.

**Anchors used (all rounds):**

| Paper | Score | Round | Comparison |
|-------|-------|-------|------------|
| Enhancing Audio-Language Models (nplYdpc1Pm) | 4.75 | R1 | Stronger — shows partial gains on targeted task. This paper's novel component shows no gains. |
| Contrastive Learning from Synthetic Audio Doppelgängers (XRtyVELwr6) | 6.25 | R1 | Much stronger — genuinely novel approach, competitive results, thorough experiments. |
| CompA (86NGO8qeWs) | 6.50 | R1 | Much stronger — new benchmark + new method, clear novel contributions. |
| SimO Loss (QCY1WQXTc8) | 3.00 | R1 | Comparable — limited evaluation but at least proposes a new loss function. This paper has broader evaluation but an ineffective novel component. |
| Acoustic Prompt Tuning (rAX55lDjtt) | 4.60 | R1 | Stronger — extends LLMs to audio with novel adapter method showing improvements. |
| Multi-label Cluster Discrimination (OPpqmSp0wK) | 5.00 | Narrow | Stronger — cluster discrimination that actually improves results in vision domain. |
| Utilization of Neighbor Information (n6KBvTQ10I) | 3.75 | Narrow | Comparable — mixed results, limited novelty concerns. |

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>