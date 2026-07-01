## Summary

This paper proposes Pctx, a personalized context-aware tokenizer for generative recommendation (GR). The key insight is that existing GR methods assign *static* semantic IDs to items based solely on item features, which under autoregressive decoding forces a universal similarity standard across all users. Pctx addresses this by conditioning tokenization on the user's interaction history: it uses DuoRec to encode user context, applies per-item k-means++ clustering to condense context representations, fuses these with item features, quantizes via RQ-VAE, and employs redundant ID merging, data augmentation, and multi-facet generation to balance personalization with generalizability. Experiments on three Amazon Review datasets show consistent improvements over GR baselines (TIGER, LETTER, ActionPiece) across all 12 metric×dataset combinations, with up to 8.9% improvement in NDCG@10.

## Strengths

1. **Clear, well-motivated problem.** The paper identifies a genuine limitation of static semantic IDs in GR — that the prefix-sharing property of autoregressive decoding forces a universal similarity standard — that prior work (TIGER, LETTER, ActionPiece) has not addressed. This observation is non-trivial and correctly identifies a representational restriction.

2. **Methodological coherence.** The pipeline is well-constructed: each component (context encoding via DuoRec, k-means++ condensation, fusion with item features in Equation 2, RQ-VAE quantization, redundant ID merging, data augmentation, multi-facet generation) addresses a specific subproblem articulated in challenges C1 and C2.

3. **Strong, consistent empirical results.** Table 2 shows Pctx outperforming all baselines across all 12 metric×dataset combinations with statistical significance (paired t-test, p<0.05). Improvements over the best GR baseline (ActionPiece) reach +7.2% N@10 on Instrument and +8.9% N@10 on Scientific, and the gains are consistent across all three datasets.

4. **Thorough ablation study (Table 3).** Ten variants systematically test different components: context encoders (SASRec vs. DuoRec), static vs. contextualized representations, removal of clustering, removal of SID merging, removal of data augmentation, removal of multi-facet generation, and random target assignment. The severe degradation of "w/o Redundant SID Merging" (e.g., N@5 dropping from 0.0270 to 0.0175 on Instrument) convincingly demonstrates that controlling over-personalization is essential.

5. **Model ensemble analysis (Table 4).** Showing that Pctx outperforms TIGER+DuoRec and TIGER+SASRec ensembles rules out the trivial explanation that Pctx is simply "a sequential model's predictions plus a GR model's predictions."

6. **Concrete case study (Figure 4).** The StarCraft II example — where the same game receives different semantic IDs depending on whether the user's history is story-driven or RTS-focused — provides direct, interpretable evidence that personalization is actually happening, not just an artifact of metric improvements.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **No variance reporting.** Tables 2, 3, and 4 report single numbers without standard deviations or confidence intervals. While Table 2 includes a paired t-test (p<0.05) against the best baseline, the ablation comparisons lack any significance indicators. Some differences are small in absolute terms (e.g., Pctx 0.0409 vs. variant 3.4 at 0.0398 R@5 on Instrument — a difference of 0.0026), and without error bars the stability of these differences across random seeds is unknown. This is a clear gap in reporting standards.

2. **Incomplete isolation of the personalization effect from richer-feature benefits.** Pctx uses DuoRec context representations fused with item features, whereas baselines like TIGER and LETTER use only item features (e.g., sentence-T5 embeddings). The paper provides indirect evidence that personalization matters (variant 1.1 replacing DuoRec with SASRec underperforms Pctx; variant 3.4 with random target assignment underperforms Pctx; Table 4's ensemble analysis). However, a cleaner control is absent: training a TIGER-style model with Pctx's fused representations (item features + DuoRec context) mapped to *fixed, non-personalized* semantic IDs would more directly separate the benefit of richer representations from the benefit of personalization itself. The existing evidence is suggestive but not fully conclusive on this point. (Variant 3.4, which keeps personalized IDs but assigns them randomly, comes closest, but still differs from the proposed control.)

3. **The central motivating claim lacks empirical validation.** The paper asserts that "semantic IDs with the same prefixes always receive similar probabilities" (Section 1). While intuitively plausible under the autoregressive paradigm, this is stated without proof or a diagnostic experiment. A simple empirical demonstration — e.g., measuring next-token distribution similarity for items sharing prefixes in a trained TIGER model, and showing that Pctx's disaggregation reduces unwanted similarity — would substantially strengthen the paper's theoretical foundation. This does not invalidate the method but leaves the motivating intuition unverified.

4. **The α hyperparameter (Equation 2) is not discussed in the main text.** The balance between context-driven personalization and item-feature generalizability (α in the fusion `concat(α·e_ctx, (1−α)·e_feat)`) is central to challenge C2. The main text neither states the value used nor provides any sensitivity analysis. (Details may be in the appendix, but this is a core hyperparameter that merits at least a brief mention in the main paper.)

### Trivial

1. **Figure 3 uses a log2-scaled y-axis**, which visually compresses differences between categories. Reporting raw counts or proportions alongside would be clearer.
2. **The variability of improvement percentages across metrics** (e.g., +2.44% R@10 vs. +11.11% N@5 on Instrument) is not discussed. The pattern is consistent with the personalization story (stronger top-ranking improvements) but the paper does not comment on it.

## Nice-to-Haves

- An ablation with shorter context windows (e.g., 2–3 items) to disentangle the benefit of longer context from personalization, addressing the claim that Pctx "captures personalities reflected in longer-term contexts."
- A computational cost comparison (training time, inference time, parameter counts) relative to simpler GR models like TIGER.
- Discussion of how Pctx handles infrequent items (beyond noting they receive 1 SID) — whether clustering degenerates and whether performance is robust to item frequency.
- Clarification of the train/test split protocol for tokenizer construction in the main text (the paper already states "pretrained on the same training data" and "from the training data" for clustering, but a more explicit statement would help).

## Removed Points

- **Train/test information flow (Issue 3 from Harsh Critic):** The reviewer flagged potential leakage from tokenizer construction using test-set information. However, the paper states that DuoRec is "pretrained on the same training data" and that k-means++ clustering is on context representations "from the training data." Further details are in the appendix (stripped by the parser). Per the rule that parser-stripped appendix content cannot be used to criticize the paper, this point is removed. The authors should clarify this in the main text (noted as a nice-to-have above).

## Novel Insights

The reviews converge on the paper's own framing: the key insight is that static semantic IDs in GR impose a universal similarity standard, and introducing context-dependent tokenization is the natural solution. The Harsh Critic's suggestion of an isolation experiment (rich features without personalization) is the most valuable constructive observation not already in the paper, but it does not constitute a fundamentally different interpretation of the work.

## Suggestions

1. **Add variance reporting** — report standard deviations or results from 3–5 random seeds to Tables 2, 3, and 4.
2. **Add a diagnostic experiment** validating the prefix-sharing claim (e.g., measuring next-token distribution similarity for items sharing prefixes in a trained TIGER model, before and after Pctx).
3. **Add the missing control experiment**: train TIGER with Pctx's fused representations but *fixed* (non-personalized, single) semantic IDs to separate representation quality from personalization.
4. **State the α value** used and briefly discuss sensitivity in the main text.
5. **Mention the train/test split handling** for the tokenizer explicitly in the main text (not just the appendix).

## Score and Decision

**Score: 7.0**  
**Decision: Accept**

This is a solid paper with a clear, well-motivated contribution. The idea of personalizing semantic IDs based on user context is novel and correctly identifies a genuine limitation of existing GR tokenization. The method is coherently designed, the ablation is thorough, and the empirical results are consistent across three datasets with statistical significance. The weaknesses (missing error bars, incomplete isolation of the personalization effect from richer features, unvalidated motivating claim, and lack of α sensitivity discussion) are real but do not undermine the core contribution. They are addressable in a rebuttal/camera-ready revision and do not rise to the level that would warrant rejection.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>