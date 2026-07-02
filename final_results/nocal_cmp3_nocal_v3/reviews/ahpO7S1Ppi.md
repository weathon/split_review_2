## Summary

This paper proposes Pctx, a personalized context-aware tokenizer for generative recommendation (GR). Existing GR methods tokenize each item into a fixed semantic ID, enforcing a universal similarity standard across all users. Pctx conditions tokenization on a user's entire interaction history: an auxiliary model (DuoRec) encodes the user context, which is clustered into centroids, fused with item features, and quantized into semantic IDs via RQ-VAE, so the same item can map to different IDs under different user histories. Experiments on three Amazon Review datasets show consistent improvements over non-personalized baselines (up to 8.9% NDCG@10).

## Strengths

1. **Genuinely novel problem framing and solution.** This is the first paper to argue that GR tokenization should be *user-dependent*, not just context-aware. The distinction from multi-identifier tokenizers (MTGRec, which samples IDs from different RQ-VAE epochs without personalization) and from adjacent-context tokenizers (ActionPiece, which uses a narrow context window) is clearly drawn in Sections 1 and 2.4, with concrete examples (the watch illustration in Figure 1).

2. **Thorough ablation study with informative controls.** Table 3 tests 9 variants across three categories. Variant (3.4) w/ Random Target is particularly well-designed: it matches Pctx in token diversity but assigns IDs randomly, and performs worse — demonstrating that the personalization mechanism itself (not just having more IDs) drives the gains. The ensemble analysis in Table 4 further rules out the concern that Pctx is simply combining DuoRec and TIGER.

3. **Statistically significant and consistent improvements.** Table 2 shows Pctx outperforming all 13 baselines on all 12 metric–dataset combinations, with * markers (p<0.05 paired t-test vs. best baseline). The improvements are consistent across three datasets with different characteristics.

## Weaknesses

### Fatal

None.

### Major

1. **The personalization vs. longer-context confound is not experimentally separated.** The primary baseline ActionPiece uses *adjacent* action context; Pctx uses the *entire* user history. The paper (Section 2.4, line 208) explicitly notes this difference: "it extends the perceived context window beyond adjacent actions." Yet there is no ablation that holds the context window fixed while isolating the personalization mechanism. A variant such as "Pctx with adjacent-only context" (matching ActionPiece's window but retaining clustering, merging, and multi-facet generation) or "ActionPiece with full history" would distinguish whether the gains come from the personalization mechanism or simply from feeding a longer context window. The ablation in Table 3 does not include this control, so the evidence for the *specific mechanism* (diverse user interpretations) is weaker than the evidence that the overall pipeline works. This is an evidential gap, not a structural flaw — the core contribution remains valid, but the causal explanation is under-supported.

### Minor

2. **No variance or multi-run statistics reported.** Table 2 reports a single number per method per metric with a * for statistical significance (paired t-test, p<0.05), but the paper never states how many seeds/runs were used, nor reports standard deviations or confidence intervals. Given that the absolute improvements are small (e.g., NDCG@10 increases from 0.0236 to 0.0257 on Scientific — a difference of 0.0021), readers need to assess stability. The authors should report standard deviations over multiple seeds in a revised version.

3. **Tight coupling with the auxiliary DuoRec model is acknowledged but not critically examined.** The pipeline requires: (i) train DuoRec on the same data, (ii) encode all (context, item) pairs, (iii) cluster per-item, (iv) quantize, (v) merge, (vi) train GR model. The ablation (1.1) w/ SASRec in Table 3 confirms that performance degrades substantially with a weaker context encoder. The conclusion mentions "end-to-end personalized action tokenizers" as future work, but the paper does not discuss this dependency as a current limitation — e.g., the method inherits all biases and failure modes of the auxiliary model, and is not a standalone tokenizer. Since this is standard practice in the GR literature (separate tokenization and generation phases), it is a minor concern rather than a major one.

### Trivial

None.

## Nice-to-Haves

- **Separate ablation of the two merging strategies** (duplicate vs. infrequent) in "w/o Redundant SID Merging." The current ablation disables both together; ablating them separately would clarify which intervention drives the large degradation (NDCG@10 drop from 0.0341 to 0.0221 on Instrument).
- **Computational cost analysis.** The pipeline involves multiple stages (train DuoRec → encode all instances → cluster per-item → RQ-VAE → merge → train GR). Providing runtime or FLOPs would help practitioners assess the practical trade-off.
- **Quantitative validation of the "interpretation" claim.** The single case study (StarCraft II) is illustrative but could be strengthened by analyzing whether users assigned different semantic IDs for the same item exhibit systematically different future behavior.

## Removed Points

These points were raised by the reviewer but are removed per the filtering guidelines. Treat them with caution.

- **K-means++ and τ under-specified / γ value not stated:** Removed because the parser strips appendices, where these details are referenced. (Hard Rule: missing appendix content.)
- **Model capacity not controlled when comparing GR to ID-based models:** The reviewer noted this is standard practice in the GR literature and not a flaw of this paper specifically.
- **Case study is cherry-picked:** Standard practice for qualitative illustrations; not a valid weakness of an empirical systems paper.
- **Game dataset shows smaller gains without discussion:** A useful observation but a suggestion for improvement, not a weakness.

## Novel Insights

Beyond the paper's own contributions, the most notable finding from the analysis is the *inverse* relationship between a model's next-item prediction performance as a standalone recommender and its effectiveness as a context encoder within Pctx: DuoRec underperforms SASRec in Table 2 but yields substantially better tokenization quality (Table 3, variant 1.1 vs. full Pctx). This suggests that representation *distinguishability* (via contrastive learning) matters more than predictive accuracy for producing useful personalized IDs — a non-obvious insight that could inform future work on tokenizer encoders.

## Suggestions

1. Add a controlled ablation that varies only the context window length (e.g., "Pctx with adjacent-only context" or "ActionPiece with full history") to disentangle personalization from longer context.
2. Report standard deviations and number of seeds for all main results.
3. Frame the DuoRec dependency explicitly as a limitation (not just future work) given its strong impact on final performance.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>