Now I have all the information I need. Let me write the final consolidated review.

---

## Summary

This paper proposes a dual-encoder system for language-based audio retrieval on the CLOTHO benchmark. The system combines three components: (i) soft-label distillation from an ensemble of retrieval teachers (adopted from Primus et al., 2024), (ii) LLM-driven caption augmentation via back-translation and caption mixing, and (iii) cluster-guided auxiliary classification. The best ensemble achieves 48.83 mAP@16 on the CLOTHO development test split. The paper presents ablations across three audio backbones (PaSST, EAT, BEATs).

## Strengths

- **Ensemble results are competitive.** The best weighted ensemble (E1) reaches mAP@16 of 48.83 on the CLOTHO development test split. For a competition-oriented benchmark, this is a strong number, and the ensemble construction (system-level then model-level weighting) is clearly documented.

- **Clean ablation structure.** The five system configurations (S1–S5) in Table 1 isolate each component systematically, and results are reported across three different audio backbones (PaSST, EAT, BEATs), giving a good picture of backbone sensitivity.

- **Addresses a genuine problem.** The non-binary nature of audio-caption correspondences in CLOTHO (multiple recordings can match a single caption) is a real limitation of standard contrastive learning, and the paper's motivation for using soft targets is well-founded.

## Weaknesses

### Major

- **No comparison to any prior published results on CLOTHO.** Table 2 contains no row for any previously published method. The reader cannot determine whether the proposed system advances the state of the art, matches it, or trails it. The paper cites the top-ranked DCASE 2024 Task 8 system (Primus et al., 2024) as the source of the distillation method, but never reports that system's CLOTHO performance or any other published CLOTHO result. Without external context, the contribution cannot be assessed — a competitive ensemble number on a private validation split is not sufficient for a conference submission. This is the most significant gap in the paper.

- **The core claim is not fully supported by the ablation results.** The abstract states that the three components "jointly improve robustness," and the conclusion claims clustering "contributed to additional performance gains." However, Table 2 shows that:
  - **Distillation** (S1→S2) is the clear driver: ~+4–5 mAP@16 across all backbones.
  - **Augmentation** (S2→S3): helps EAT (+0.70) and BEATs (+0.77), but slightly hurts PaSST (–0.21).
  - **Clustering** (S3→S4/S5): for PaSST, S5 (46.50) is only +0.09 over S3 (46.41) while S4 (46.39) is slightly worse; for EAT and BEATs, clustering produces *consistent decreases* (e.g., EAT S3=46.05 → S4=45.34, S5=45.34).
  
  Two of the three claimed contributions do not reliably improve single-model performance. The paper acknowledges this in passing ("mixed gains across backbones") but the abstract and conclusion present a stronger narrative than the evidence supports. The sentence in the abstract claiming "consistent improvements under high correspondence ambiguity" is also not supported by any experiment shown in the paper (no breakdown by ambiguity level is presented).

### Minor

- **The distillation method is adopted, not proposed, and its framing as a contribution is overstated.** Section 2.2 explicitly states the distillation loss is "adopted" from Primus et al. (2024), with no modification, analysis, or extension. Listing "Soft-label distillation that targets non-binary audio-caption correspondences" as a stand-alone contribution without distinguishing what is inherited versus new is misleading.

- **The evaluation-set result is reported without analysis or context.** The paper states that the approach achieved mAP@16 of 0.421 on the evaluation set — a ~14% relative drop from the 0.488 development test result. No explanation, analysis, or comparison to any prior evaluation-set result is provided. The reader cannot interpret whether 0.421 is strong, weak, or expected.

- **No variance or statistical significance is reported.** All results in Table 2 are single-point estimates. Differences between configurations are often tiny (e.g., PaSST S2=46.62 vs. S5=46.50, a 0.12 gap) and, without confidence intervals or multiple runs, it is impossible to know whether they are meaningful. This weakens every comparative claim.

- **Missing details about the clustering procedure.** Several design choices are underspecified: (i) the number of clusters produced by BERTopic/HDBSCAN is not reported; (ii) the outlier reassignment procedure ("reassigned based on topic probabilities") is described only vaguely; (iii) the motivation for applying classification heads to both audio and text encoders when clusters are derived from captions alone is not discussed; (iv) the embedding model used for initial caption embeddings (e5-large-v2) is mentioned only in the training section rather than in the method description.

- **Cross-backbone comparisons are confounded by hyperparameter differences.** PaSST uses batch size 64 and 32 kHz sampling, while EAT and BEATs use batch sizes 24/16 and 16 kHz. Since batch size directly affects the number of negatives in the contrastive loss, observed differences between backbones cannot be cleanly attributed to the backbone architecture alone.

- **Ensemble weights are tuned on the validation set but their generalization is not examined.** The ensemble weights (Table 3) are selected via grid search on the validation split. The paper does not analyze whether these weights generalize to the test set or if the near-identical ensemble results (48.78–48.83 across E1–E4) indicate that the weight tuning is robust or simply insensitive.

### Trivial

- None.

## Nice-to-Haves

- **Break down results by correspondence ambiguity level.** The abstract claims "consistent improvements under high correspondence ambiguity," but no such experiment is shown. An analysis of whether clustering helps more for ambiguous captions would directly support (or refute) the paper's thesis.
- **Analyze soft-label quality.** The paper could strengthen its motivation by showing example soft-label distributions from the ensemble teacher, demonstrating that the teacher meaningfully captures non-binary correspondences beyond what one-hot labels provide.
- **Test LLM augmentation with an open-source model.** The paper acknowledges the reliance on GPT-4o as a limitation but does not experiment with an alternative (e.g., Llama, Mistral) to demonstrate that the pipeline is reproducible without proprietary APIs.
- **Specify audio mixing details** (e.g., equal gain, random SNR) for the LLM-mix augmentation.

## Removed Points

These points were removed from the input review under the filtering rules:

- **"Section 2.2 does not cite the original soft-label distillation for retrieval literature"** — This is a minor citation breadth concern, not a substantive flaw. Removed as a nitpick that does not affect the paper's validity.
- **"The LLM augmentation pipeline is non-reproducible due to reliance on GPT-4o"** — The paper acknowledges this as a limitation. Removed as a point already addressed by the authors.
- **"The paper does not analyze whether LLM augmentation improves alignment or simply adds noise"** — This is a reasonable suggestion but not a weakness; it belongs in Nice-to-Haves.
- **"The paper does not specify how the audio mixing is done"** — Similarly moved to Nice-to-Haves.
- **Strengths about "core motivation is valid" and "evaluation metrics are standard"** — Removed as generic statements that lack specific, concrete evidence tied to this paper's accomplishments.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add external comparisons.** Include at least one prior published CLOTHO result in Table 2. If none is directly comparable, re-implement a baseline or cite the best known published number and explain the methodological differences.
2. **Reframe the contributions around what the evidence actually supports.** Distillation is the clear driver; the paper would be more credible by treating it as the main result and honestly reporting that clustering provides mixed or negative gains.
3. **Report variance estimates.** Run each configuration with multiple seeds and report standard deviations, especially for configurations where differences are small.
4. **Provide context for the evaluation-set result.** Compare the 0.421 mAP@16 to any known evaluation-set numbers, or at minimum analyze the drop from the development test split (e.g., distribution shift, different data sources).
5. **Specify the clustering procedure details** (number of clusters, outlier handling) and motivate the design choices.

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>