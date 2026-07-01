## Summary

This paper identifies a genuine limitation in generative recommendation (GR): static tokenization assigns the same semantic ID to an item regardless of user context, which enforces a universal similarity standard under the autoregressive paradigm. The authors propose Pctx, a personalized context-aware tokenizer that incorporates a user's historical interactions when generating semantic IDs. The tokenization pipeline uses an auxiliary contrastive learning model (DuoRec) to encode user context, clusters context representations per item via k-means++, fuses them with sentence embeddings, quantizes via RQ-VAE, and applies merging/augmentation strategies to balance personalization against sparsity. Experiments on three Amazon Review datasets show consistent improvements (up to 8.9% relative NDCG@10 gain) over static and context-aware baselines.

## Strengths

1. **Well-motivated problem with a clear technical explanation (Section 1, Figure 1).** The paper pinpoints a concrete limitation of static GR tokenization: because autoregressive models assign similar probabilities to semantic IDs sharing prefixes, a fixed ID mapping imposes a single similarity standard across all users. The watch/gift/investment example is simple but effectively illustrates why this is a real problem.

2. **Method design explicitly addresses the personalization-sparsity tradeoff (Section 2.2).** Rather than naively assigning unique IDs per user-item occurrence, the paper introduces three principled sparsity controls: (a) adaptive clustering per item to condense context representations, (b) merging infrequent semantic IDs against a threshold τ, and (c) data augmentation with random replacement (γ). The ablation (Table 3) confirms all three matter — removing the merging strategy causes a severe collapse (NDCG@10 drops from 0.0341 to 0.0221 on Instrument), demonstrating that the design choices are not decorative.

3. **Informative and honestly-reported ablation study (Table 3).** Several findings stand out: (1.1) DuoRec is *worse* than SASRec as a standalone recommender but *better* as a context encoder for Pctx — a non-obvious result that supports the method's mechanism. (3.3) "TIGER w/ Pctx IDs" (Pctx's IDs without data augmentation or multi-facet generation) performs near baseline TIGER (0.0302 vs. 0.0306 NDCG@10 on Instrument), honestly showing that the gains come from the full pipeline, not just the new IDs. (3.4) "w/ Random Target" (γ=1) underperforms Pctx, cleanly demonstrating that the context-to-ID mapping matters beyond token diversity.

4. **Ensemble analysis directly addresses the most natural skeptical argument (Table 4).** The concern that Pctx might simply combine DuoRec's representations with TIGER's GR pipeline is anticipated and countered: explicit ensembles of SASRec/DuoRec with TIGER fall well short of Pctx, confirming that the contribution is structural rather than additive.

5. **Case study makes the personalization concrete (Figure 4).** StarCraft II is tokenized as [53, 395, 576, 770] under a story-driven context vs. [53, 412, 576, 770] under an RTS context. The shared first and third tokens (53, 576) with differing second tokens (395 vs. 412) are consistent with what the method should produce — personalization manifests at later token positions within shared prefix clusters.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

1. **No hyperparameter sensitivity analysis for the pipeline's internal knobs (α, τ, γ, C_{v_i} scaling).** The method involves roughly seven design choices (DuoRec training → context clustering → fusion weight α → RQ-VAE quantization with codebook sizes → duplicate merging → infrequent ID merging τ → data augmentation rate γ), plus the GR model's own hyperparameters. The ablation study tests high-level component presence/absence but does not explore sensitivity to the quantitative parameters within them. It is therefore unclear whether the reported results require careful tuning or are robust across reasonable ranges. (The paper reports ablations for components but not for α, τ, γ, or the C_{v_i} scaling rule — these are cited observations from the paper's text and equations.)

2. **No standard deviations or confidence intervals reported for any result.** Although the main table (Table 2) uses a paired t-test (p<0.05) to indicate statistical significance versus the best baseline, no variance information is provided for any metric in any table. Since all reported numbers are in the 0.01–0.06 range, even modest variance could affect method ordering. This makes it harder for readers to assess result stability.

3. **The α scaling in Equation (2) is an unusual design with no rationale provided.** The fusion is written as concat(α·e^{ctx}, (1−α)·e^{feat}), which separately scales the context and feature dimensions before concatenation — rather than concatenating the raw vectors and letting RQ-VAE learn the weighting. The paper does not explain why this specific form was chosen instead of simpler alternatives, nor how α interacts with the subsequent quantization process.

4. **The personalization framing could be more precise about where it operates.** The abstract says "the same item to be tokenized into different semantic IDs under different user contexts," which is true of the training data construction. However, the tokenizer is applied during preprocessing to build training sequences; during inference, the GR model generates from learned probabilities in this pre-built token space. The framing in places (abstract, introduction) may suggest a more dynamic, online tokenization process than what actually occurs. This is a clarity issue rather than a methodological flaw — the method is correctly described in Section 2.3.

5. **The case study does not verify that the differing token positions reflect meaningful semantic distinctions.** The paper shows that StarCraft II gets [53, 395, 576, 770] vs. [53, 412, 576, 770] under different contexts, but does not check whether tokens 395 and 412 in the RQ-VAE codebook correspond to semantically distinguishable centroids. It is possible that nearby but distinct cluster centroids were assigned by the quantization process without a meaningful interpretive difference.

6. **The "w/ Random Target" ablation (3.4) uses γ=1 while Pctx uses a tuned (undisclosed) γ.** This variant is designed to test whether the context-to-ID mapping matters (vs. random diversity), and its conclusion is sound. However, the comparison is not perfectly balanced because the ablation uses an extreme augmentation rate. Reporting performance across a range of γ values would strengthen the analysis and is absent from the main text.

### Trivial

None.

## Nice-to-Haves

- **Analysis of where personalization helps most.** The paper would be stronger by showing whether gains concentrate on users with longer histories (more context signal) or on items with higher category ambiguity (e.g., items belonging to multiple categories). This would provide practical guidance.
- **Evidence linking personalized IDs to actual user behavior differences.** An analysis showing that users assigned to different semantic IDs for the same item exhibit measurably different downstream behavior would directly support the "diverse user interpretations" narrative.
- **Whether the modest absolute gains (0.002–0.003 NDCG@10, ~3–9% relative) justify the multi-stage pipeline complexity.** This is a judgment call that depends on the deployment context. The paper is clear about its contribution, but acknowledging the cost-benefit tradeoff explicitly would help readers calibrate expectations.

## Removed Points

- **Criticism about C_{v_i} determination deferred to the appendix:** Removed per policy — appendices are stripped by the parser and cannot be verified.
- **Criticism about absolute improvements being too small:** Moved to Nice-to-Have — the improvements are consistent across 12 metrics and statistically significant; the question of cost-benefit is a judgment call, not a verifiable weakness.
- **Criticism about inference-time personalization being indirect:** Retained in diluted form as Minor (clarity/framing issue #4) rather than the stronger "limits the framing" framing the reviewer used, since the paper's description is technically accurate.

## Novel Insights

None beyond the paper's own contributions. The reviews identify useful clarifications and minor gaps but do not surface a fundamentally different interpretation of the paper's findings.

## Suggestions

- Add a sensitivity table showing NDCG@10 across 2–3 values of α, τ, and γ to demonstrate robustness.
- Report standard deviations over at least 3 seeds or runs for the main results.
- Clarify the probability aggregation step in multi-facet generation: "within each beam search result" is ambiguous — specify whether probabilities are summed across beams or within each beam's final token.
- Add a brief rationale for the α scaling design in Equation (2) (why scale before concatenation rather than letting RQ-VAE learn the weighting).
- Disclose the tuned value of γ used for the main Pctx results.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>