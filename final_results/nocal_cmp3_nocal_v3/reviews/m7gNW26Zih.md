## Summary

This paper presents a dual-encoder system for language-based audio retrieval on the CLOTHO dataset, combining: (i) soft-label distillation from an ensemble of pretrained retrieval teachers (adopted from Primus et al., 2024), (ii) LLM-based caption augmentation (back-translation and LLM-mix), and (iii) a cluster-guided auxiliary classification task. The best ensemble achieves 48.8 mAP@16 on the development test split. The systematic five-configuration ablation across three audio backbones (PaSST, EAT, BEATs) is the paper's strongest structural feature.

---

## Strengths

- **Systematic and reproducible ablation framework.** Tables 1 and 2 trace the incremental contribution of each component (distillation, augmentation, cluster guidance) across three backbones, making it possible to isolate the effect of each design decision. The augmentation pipeline (back-translation, LLM-mix) and the three-stage training protocol are clearly specified.

- **Distillation produces a clear, substantial gain.** Moving from SID 1 (contrastive only) to SID 2 (+distillation) yields a +4.5 mAP@16 improvement for PaSST (42.08 → 46.62). This gain is consistent across all three backbones and is the largest single improvement in the paper.

- **The weighted ensemble strategy is well-motivated and effective.** The ensemble (E1–E4) reaches ~48.8 mAP@16, a meaningful lift over any individual model (~46.6). The two-stage weighting procedure and grid search on the validation set are clearly described.

---

## Weaknesses

### Fatal

None.

### Major

1. **The paper's claimed novel contribution — cluster-guided auxiliary classification — is not supported by its own evidence.**  
   The abstract and introduction present cluster guidance as a core contribution ("cluster-guided auxiliary classification," third bullet). Table 2 shows the opposite:  
   - **PaSST** (best backbone): SID 5 (+cluster) = 46.50 vs. SID 3 (no cluster) = 46.41 → +0.09 mAP@16, well within noise range. SID 2 (distill only, no cluster, no aug) at 46.62 *outperforms* every configuration that includes clustering.  
   - **EAT**: SID 4/5 (+cluster) = 45.34 vs. SID 3 (no cluster) = 46.05 → clustering *hurts* by 0.71.  
   - **BEATs**: SID 5 (+cluster) = 43.88 vs. SID 3 (no cluster) = 44.66 → clustering *hurts* by 0.78.  

   Across three backbones, cluster guidance provides a negligible effect on one and actively degrades performance on the other two. The abstract further claims "ablations indicate consistent improvements under high correspondence ambiguity" — but no experiment in the paper isolates or analyzes high-ambiguity subsets, defines "high correspondence ambiguity," or tests this claim. This is not a limitation the paper acknowledges; it is a claimed contribution that the evidence contradicts.

2. **No comparison to prior published work on CLOTHO.**  
   The paper evaluates on a well-established benchmark (CLOTHO) with published results spanning several years. It cites Primus et al. (2024) as the top-ranked DCASE 2024 Task 8 system and draws its distillation method from that work, but never states what prior systems achieve on this dataset, never compares its numbers to any published result, and never explains whether its system (which also uses AudioCaps + WavCaps pretraining) surpasses prior work. Without this context, the reader cannot determine whether the proposed techniques constitute an advance. The evaluation reads as a self-contained technical report rather than a research paper situating its contribution.

### Minor

3. **Evaluation set result reported without explanation or per-system breakdown.**  
   Line 198 reports mAP@16 of 0.421 on the evaluation dataset — a ~14% relative drop from the 0.488 on the development test split. No per-system breakdown, no baseline numbers, and no discussion of why this drop occurs (distribution shift? overfitting to the dev-test via validation-set grid search? different annotation quality?). The reader cannot assess whether the proposed methods generalize.

4. **No variance or significance reporting.**  
   No standard deviations, confidence intervals, or significance tests are reported anywhere. Given that many system differences are within ~0.1–0.2 mAP@16, the reader cannot determine whether observed differences are meaningful.

5. **Data augmentation's negative effect on the best backbone is not discussed.**  
   For PaSST, adding augmentation (SID 2 → SID 3) *decreases* mAP@16 from 46.62 to 46.41. The paper presents augmentation as a contribution but does not acknowledge this pattern.

6. **Different batch sizes per backbone confound cross-backbone comparisons.**  
   Batch sizes are 64/24/16 for PaSST/EAT/BEATs respectively (due to computational constraints). Contrastive learning is known to be sensitive to batch size; the paper acknowledges the constraint but does not discuss whether this could explain the performance ordering across backbones.

7. **Conceptual redundancy of the auxiliary cluster task.**  
   The audio encoder is trained to predict the cluster label of the *paired caption*. Since the cluster labels are derived from caption embeddings, this auxiliary task is a coarser, discretized version of the same alignment objective the contrastive loss already optimizes. No analysis is provided showing that the cluster predictions capture semantic structure the contrastive loss misses — which would explain why the auxiliary task adds little to no benefit (as the results confirm).

### Trivial

None.

---

## Nice-to-Haves

- Provide per-system results on the evaluation set so readers can assess generalization beyond the dev-test split.
- Analyze *when* clustering might help — e.g., define a subset of queries with high ambiguity (multiple valid captions per audio), compare performance with and without cluster guidance on that subset, and report statistical significance.
- Ablate sensitivity to hyperparameters of the cluster guidance (number of clusters, auxiliary loss weight λ₂), not just the clustering method (finetuned vs. BERTopic).
- Clarify what the auxiliary classification task provides that the contrastive loss does not, either through conceptual analysis or probing experiments.

---

## Removed Points

These points were raised in the input review but are removed per the filtering rules:

1. **"Section 2.1-2.2: distillation is standard/adopted from prior work"** — The paper *explicitly* attributes the distillation method to Primus et al. (2024) (lines 56–58). Stating that a component is adopted is proper scholarship, not a weakness. **Removed: not a valid criticism.**

2. **"No held-out test set evaluation with baselines" (the "no held-out test set" part)** — Table 2 *is* on the CLOTHO development test split, which is a held-out test set. The valid concern (no SOTA comparison) is already covered in Weakness 2. **Removed: factually inaccurate.**

3. **"Section 2.4: LLM-mix augmentation quality not discussed"** — The paper describes how the 50,000 mixed samples are created and cites Wu et al. (2024) for the technique. A deeper quality analysis would be nice but is not a standard expectation for a systems paper. **Removed: scope creep.**

---

## Novel Insights

None beyond the paper's own contributions. The review's primary insight is that the paper's central claimed contribution (cluster guidance) is contradicted by its own ablation results — but this is an evaluation of the paper's internal coherence, not a novel research insight.

---

## Suggestions

1. **Reframe the contributions honestly.** Drop or substantially soften the claim that cluster guidance "improves" performance. The data supports at most that cluster guidance has negligible or inconsistent effects. The paper's value rests on the distillation + ensemble pipeline, which does produce clear gains. Frame the cluster guidance as an attempted technique that did not reliably help, and discuss why.

2. **Add a comparison to prior published results on CLOTHO.** Without this, the paper cannot demonstrate progress. Report prior SOTA numbers (including the Primus et al. 2024 system that inspired the distillation component) and discuss how the proposed system compares, controlling for differences in training data and compute.

3. **Explain the evaluation-set performance gap (0.421 vs. 0.488).** This is essential for establishing generalization.

4. **Report variance or confidence intervals** for at least the key comparisons, especially given small differences between configurations.

5. **Investigate the batch-size confound** or at minimum discuss how it might affect backbone comparisons.

---

## Score and Decision

**Score:** 4 — Borderline reject.  
**Decision:** Reject

**Rationale:** The paper's strongest claim (cluster-guided auxiliary classification as a novel contribution) is contradicted by its own ablation results across three backbones. The abstract asserts "consistent improvements under high correspondence ambiguity" with no supporting experiment. Combined with the absence of any comparison to prior published work on CLOTHO, the paper does not convincingly demonstrate a research advance. The distillation and ensemble components are well-executed but are largely adopted from prior work (Primus et al., 2024), and the paper does not establish that its overall system surpasses existing published results. The systematic ablation framework and reproducible pipeline are genuine strengths, but they do not compensate for the gap between the claimed contributions and the evidence provided.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>