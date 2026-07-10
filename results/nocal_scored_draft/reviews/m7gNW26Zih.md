Now I have the favorability signals. The two 0.00 items (overclaimed contribution and lack of variance) are the dominant negatives. The strengths are all near-perfect (0.94–1.00), so the paper has genuine value. However, the mismatch between claimed and demonstrated contribution is severe enough to drive the score down significantly. I'll assign 4.0 (borderline reject) — the paper's experimental work has merit but its central thesis is unsupported.

---

## Summary

This paper presents a three-stage training pipeline for language-based audio retrieval combining (i) soft-label distillation from an ensemble of teacher models, (ii) LLM-based caption augmentation (back-translation + LLM mix), and (iii) cluster-guided auxiliary classification heads. Experiments on CLOTHO use three audio backbones (PaSST, EAT, BEATs) and report a best single-model mAP@16 of 46.62 and a weighted ensemble mAP@16 of 48.83.

## Strengths

- **Clear, structured system description.** The three-stage pipeline with explicit SID configurations (Table 1), hyperparameters (batch sizes, learning rates, schedulers, loss weights), and training stages is well-documented, aiding reproducibility.

- **Distillation provides a large, consistent gain.** Adding soft-label distillation from the teacher ensemble lifts mAP@16 by 4–6 points across all three backbones (Table 2, SID 1 vs. SID 2: PaSST 42.08→46.62, EAT 40.41→45.35, BEATs 38.12→43.89). This is a robust and practically meaningful improvement.

- **Solid ensemble results.** The weighted ensemble (mAP@16 48.83) meaningfully improves over the best single model, and the weighting coefficients are documented in detail (Table 3).

## Weaknesses

### Major

- **Overclaimed contribution: the novel components do not add measurable benefit over distillation alone.** The paper frames LLM-based augmentation and cluster-guided classification as core contributions that "jointly improve robustness," but Table 2 shows otherwise. For PaSST (the best backbone), SID 2 (distill only, mAP@16=46.62) outperforms SID 3 (+aug, 46.41, –0.21), SID 4 (+aug+cluster finetuned, 46.39, –0.23), and SID 5 (+aug+cluster BERTopic, 46.50, –0.12). For EAT and BEATs, augmentation provides small gains (+0.70 and +0.77), but clustering does not add further benefit. The conclusion's statement that clustering "contributed to additional performance gains" is not supported by the primary metric. Moreover, the main source of improvement (distillation) is adopted from prior work (Primus et al., DCASE 2024) and properly cited but not novel to this paper.

### Minor

- **Single-dataset evaluation.** Results are reported only on the CLOTHO development test split. The paper already uses AudioCaps for pretraining, making evaluation on it straightforward; single-dataset evaluation limits generalization claims.

- **No variance or statistical significance reported.** Results come from single runs without multiple seeds, confidence intervals, or any measure of variance. The differences between SID 2–5 for PaSST span only 0.23 mAP@16 (46.39–46.62), so it is impossible to determine whether the small effects attributed to the novel components are meaningful or noise.

- **Clustering procedure underspecified.** The paper uses BERTopic with HDBSCAN but reports no key parameters (min_cluster_size, min_samples, number of clusters produced, cluster assignment distribution). Auxiliary head classification accuracy is not reported, making it difficult to assess whether the pseudo-labels are meaningful.

- **Data augmentation mixing details missing.** The paper creates 50,000 LLM-mix audio-text pairs but does not specify how these are mixed into training (batch proportion, sampling strategy, whether original samples and augmented samples are seen equally).

### Trivial

None.

## Nice-to-Haves

- Report clustering diagnostics (number of clusters, cluster purity, auxiliary head accuracy).
- Specify the proportion of augmented data per batch.
- Include evaluation on AudioCaps (already used for pretraining, so minimal additional cost).

## Removed Points

These points were considered but removed per meta-review filtering rules. Treat them with caution:

1. **"Thorough ablations on topic granularity and teacher softness are absent"** — Removed because the parser strips appendix content from all papers. The paper's contribution list (line 18) explicitly claims these ablations, and the visible text ends with "Rest of paper (reference and Appendix) is removed." Per the rules, weaknesses about content that exists in the original submission but was stripped by the parser should not be held against the paper.

2. **"Appendix A notes LLM use for language polishing"** — Removed as a weak criticism. The paper's disclosure of LLM use for language polishing is properly handled and unrelated to technical contribution.

3. **"Batch sizes differ across backbones creating a confound"** — Removed because the paper openly acknowledges this is due to compute constraints (Section 3.4). This is a practical limitation common in multi-backbone studies, not a methodological weakness.

4. **"Single-annotation results discrepancy not discussed"** — Merged into the overclaimed-contribution weakness. The R@1 improvements for PaSST from augmentation (23.35→26.81→27.20) are small and do not rescue the central claim.

## Novel Insights

The harsh critic's most penetrating observation is that the paper's own results create a paradox: three components are presented as contributions, but the data suggest only the adopted (non-novel) component drives performance. This creates a framing-revision problem rather than a technical flaw — the system is well-built and the ensemble results are solid, but the claimed novelty attribution does not match the experimental evidence. This mismatch between claimed and demonstrated contribution is the core issue.

## Suggestions

1. Reframe the narrative to accurately reflect the evidence: distillation (adopted from prior work) provides the large gains; LLM augmentation and cluster guidance yield marginal/inconsistent benefits that need further investigation rather than being presented as clear improvements.
2. Add multiple-seed runs with variance reporting for the SID 2–5 comparisons, where effect sizes are small.
3. Report clustering diagnostics (number of clusters, cluster purity, auxiliary head accuracy) to establish that the pseudo-labels are meaningful.
4. Include evaluation on AudioCaps to strengthen generalization claims.
5. Specify the proportion of augmented data per batch and other mixing details.

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>