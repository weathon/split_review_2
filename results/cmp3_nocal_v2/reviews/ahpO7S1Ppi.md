## Summary

This paper proposes Pctx, a personalized context-aware tokenizer for generative recommendation. Unlike existing static tokenization approaches that assign fixed semantic IDs to items, Pctx generates different semantic IDs for the same item conditioned on the user's full interaction history. The method uses an auxiliary model (DuoRec) to encode user context, clusters these representations, merges redundant/infrequent semantic IDs, and uses data augmentation to balance personalization against sparsity. Experiments on three Amazon Review datasets show consistent improvements over non-personalized tokenization baselines (up to 8.9% NDCG@10).

## Strengths

- **A well-identified and genuine problem.** The paper clearly articulates a structural limitation of static semantic IDs in autoregressive generative recommendation: tokens sharing prefixes inevitably receive similar probabilities, imposing a universal similarity standard across all users. This insight (Section 1, Figure 1) correctly identifies a fundamental constraint of the paradigm, not an incremental weakness.

- **A thoughtful treatment of the personalization-generalization tradeoff.** Rather than naive per-user tokenization, the method couples adaptive clustering (Section 2.2.1), merging of duplicated and infrequent semantic IDs (Section 2.2.2), and data augmentation (Section 2.3) to control sparsity. The ablation study (Table 3) confirms each component contributes, with redundant SID merging causing the sharpest degradation when removed (0.0341→0.0221 NDCG@10 on Instrument), validating the design logic.

- **Consistent and non-trivial empirical gains.** Pctx outperforms all baselines across all three datasets and all four metrics in Table 2. Improvements over ActionPiece—the best prior context-aware tokenizer—are meaningful (e.g., NDCG@10 +7.23% on Instrument, +8.90% on Scientific), and all results are statistically significant (paired t-test, p<0.05).

- **Model ensemble analysis that addresses a natural concern.** Table 4 shows that naively ensembling DuoRec or SASRec with TIGER falls far short of Pctx's performance. This goes beyond what most GR papers provide by demonstrating that the gains come from the personalized tokenization mechanism rather than from simply combining complementary models.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Limited dataset diversity.** All three datasets are drawn from the same source (Amazon Reviews, Hou et al., 2024), share the same data distribution characteristics (~99.96% sparsity, 8–9 average sequence length), and come from a single collection pipeline. While the paper's claims are stated relative to these datasets (not universally), the absence of results on alternative domains (e.g., MovieLens, Steam, news recommendation) makes it difficult to assess how broadly the conclusions hold.

- **No multi-run variance reporting.** The paper reports statistical significance via a paired t-test on per-user results but does not report standard deviations, confidence intervals, or results across multiple random seeds. Since the pipeline involves k-means++ clustering (initialization-dependent) and RQ-VAE training, some variability across runs is expected. This is common practice in the recommendation literature, so it does not invalidate the results, but reporting variance would improve confidence in the stability of the improvements.

- **Incomplete disentanglement of personalized tokenization from additional context.** The method introduces both (a) richer user context (full history via DuoRec) and (b) a personalized tokenization mechanism (clustering, merging, augmentation). While ActionPiece already uses local context as a baseline, a cleaner comparison would be to give a non-personalized tokenizer (e.g., ActionPiece or TIGER) the same DuoRec context representations as additional input features, to verify that it is the *personalized tokenization process itself*—not merely having access to richer context features—that drives the gains. The ablation study (Table 3, variants 1.1–1.3) and ensemble analysis (Table 4) partially address this, but a direct controlled comparison would strengthen the causal claim.

- **No validation of the facet interpretability claim.** The paper asserts that multi-facet generation "reveals the likelihoods of different user interpretations, thereby enhancing the explainability" (line 198) and that different semantic ID paths for the same item correspond to interpretable facets (e.g., StarCraft II as story-driven vs. RTS in Figure 4). However, this is supported only by a single case study. The paper references a GPT-4o-based experiment in the appendix (stripped by the parser), but the main text provides no quantitative or human evaluation of whether the different semantic ID paths reliably correspond to semantically meaningful facets.

- **Several design details deferred to the appendix.** The values of key hyperparameters (α, γ, τ), the exact rule for determining the number of clusters C_{v_i} proportionally, and the replacement distribution for data augmentation are described as "in Appendix B" (line 158) or "Appendix C.3" (line 245), which the parser has stripped. While this is a presentation issue rather than a methodological flaw, the main text would benefit from stating at least the ranges or default values of these parameters.

### Trivial

- The method of selecting alternative semantic IDs during data augmentation ("randomly replaces...with probability γ," line 196) does not specify whether the replacement is uniform over alternatives or weighted. Clarifying this would aid reproducibility.

## Nice-to-Haves

- A sensitivity analysis for the most important hyperparameters (especially α, which controls the context-feature tradeoff, and τ, the frequency threshold for merging) would help assess robustness.
- An analysis of computational cost (training time, inference time, model size) relative to baselines would help practitioners understand practical tradeoffs introduced by the auxiliary DuoRec model and the additional tokenization pipeline.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Clustering proportionality factor details unclear"** — The critic flagged the determination of C_{v_i} as deferred to Appendix B. Per the filtering rules, appendix-deferred details that were stripped by the parser should not be treated as a weakness; they exist in the original submission.
- **"Single scalar α may be overly simplistic"** — The critic speculated that a single α for all items and users may be oversimplified. This is a design choice, not a confirmed weakness; no evidence is presented that a more complex scheme would improve results.
- **"No analysis of computational cost"** and **"Hyperparameter sensitivity study requested"** — These are reasonable suggestions but do not constitute weaknesses; they have been moved to Nice-to-Haves.
- **"The frequency threshold τ is not given in the main text"** — Overlaps with the weakness above about deferred details; the appendix contains this information.

## Novel Insights

The reviews do not surface insights beyond the paper's own contributions. The most useful observation is the need for a cleaner baseline that equips a non-personalized tokenizer with the same DuoRec context representations, which the paper's evaluation framework could support.

## Suggestions

- Add results from 3–5 random seeds with standard deviations to the main results table.
- Include at least one evaluation on a non-Amazon dataset (e.g., MovieLens, Steam) to broaden the empirical scope.
- Add a controlled comparison where ActionPiece or TIGER receives the same DuoRec context representations as additional input features.
- Provide a quantitative or human evaluation of whether different semantic ID paths correspond to interpretable facets, beyond the single case study.
- State the values or ranges of α, γ, and τ in the main text rather than deferring entirely to the appendix.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>