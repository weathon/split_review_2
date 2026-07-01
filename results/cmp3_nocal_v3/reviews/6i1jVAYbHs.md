Here is the final consolidated review.

---

## Summary

This paper proposes AtlasKV, a parametric method for augmenting LLMs with knowledge graphs. It introduces two components: KG2KV, which converts KG triples (h, r, t) into query-key-value training data by leveraging the natural structural alignment between triples and attention mechanisms, and HiKVP (hierarchical key-value pruning), which organizes key embeddings into a three-level hierarchy to reduce inference memory and time to sub-linear complexity. Experiments on OOD datasets show strong knowledge grounding accuracy improvements over KBLaM, and memory projections suggest the method can handle billion-scale KGs with under 20GB VRAM at inference time.

## Strengths

1. **KG2KV is a principled and well-motivated data construction method.** Converting KG triples into Q-K-V data by masking the head or tail entity and rewriting the relation as a key attribute is elegant. The diversity comparison in Table 1 (7.864% unique enquiry attributes vs. 0.003% for the synthetic baseline) is striking and concretely demonstrates the data quality improvement — a 2600× gain that directly correlates with the OOD generalization improvements seen in Table 3.

2. **HiKVP's sub-linear complexity is theoretically sound.** The three-level hierarchy (root: ∛M keys, intermediate: M^(2/3), leaf: M) paired with top-K pruning (k_R=128, k_I=64, k_L=16) provides a clean path from O(M) to O(∛M) complexity. The idea of keeping only root keys on GPU and fetching lower levels on demand is the right engineering intuition for the problem.

3. **The ablation in Table 4 is informative and honest.** Showing that removing either named entities or event entities from KG2KV hurts performance, with differential effects across datasets (event entities matter more on ATLAS-Pes2o-QKV, named entities matter more on Enron), provides genuine insight into the data design choices.

## Weaknesses

### Fatal
None.

### Major

1. **Accuracy is not evaluated at the claimed billion-scale.** The paper's title and framing emphasize "billion-scale KGs (e.g. 1B triples)" and "less than 20GB VRAM," yet the knowledge grounding evaluation (Table 3, Figure 5) uses KG sizes of at most 10³–10⁴ triples — six orders of magnitude below the claimed operating range. The memory experiment (Figure 4) projects VRAM usage at billion-scale, but there is no accuracy evaluation showing whether grounding performance survives when the KG grows to 10⁵ or 10⁶ triples. At those scales, HiKVP's pruning (keeping 16 leaf keys from potentially millions) is far more aggressive than at the evaluated 10¹–10³ scale, where pruning barely activates. Without evidence that the hierarchical retrieval reliably identifies the correct KV pair under realistic pruning ratios, the central claim that AtlasKV "maintains strong knowledge grounding... at scale" is only partially supported.

2. **The contribution of the architecture vs. the data is not cleanly isolated.** The headline comparison (Table 3) pits AtlasKV (trained on KG2KV data with trained heads and HiKVP pruning) against KBLaM (trained on Synthetic data). The "AtlasKV w/o HiKVP" variant partially addresses this by removing the pruning component, but it still uses AtlasKV's trained heads rather than KBLaM's architecture. The dramatic gains of AtlasKV w/o HiKVP over KBLaM (e.g., 92.7% vs. 16.4% ACC@1 on ATLAS-Pes2o-QKV at 10² triples) strongly suggest that KG2KV data is the primary driver of improvement, but without running KBLaM on the same KG2KV data, the independent contribution of the AtlasKV architecture (the trained heads and attention formulation) cannot be assessed.

### Minor

3. **The ICL memory curve in Figure 4 is unclear.** The figure description states that ICL stays below 20GB across KG sizes from 10⁴ to 10⁹ triples. For ICL (which places all triples in the LLM's context), 10⁴ triples at ~20 tokens each would require handling 200K+ tokens, whose KV cache alone would far exceed 20GB for LLaMA-3.1-8B. The paper itself notes that ICL with "more than 100 triples… over 48GB VRAM is required." This discrepancy suggests either the ICL curve measures something other than full-context ICL (e.g., with retrieval/subsetting) or the description is misleading. The memory comparison needs clarification.

4. **Missing KG-specific baselines.** The related work discusses KELP, KnowGPT, and RAR — methods specifically designed for KG-augmented LLMs — but none are included as experimental baselines. Since the paper's contribution is about KG augmentation, comparisons against these would strengthen the evaluation beyond the current set (KBLaM, ICL, zero-shot).

5. **No discussion of upfront preprocessing cost.** Building the three-level hierarchy requires running a sentence encoder, UMAP dimension reduction, and GMM clustering on potentially billions of key vectors. This one-time computational cost could be substantial and is not acknowledged. The "less than 20GB VRAM" framing refers only to inference, not to the cost of constructing the index.

6. **Evaluation uses only proxy metrics.** The main metric (knowledge grounding accuracy) measures whether the correct KV pair receives top attention weight, not whether the model produces correct answers. An end-to-end QA evaluation (e.g., on WebQuestions or a subset of the ATLAS datasets with natural language questions) would strengthen confidence in real-world applicability.

### Trivial

7. Table 4 header reads "ATLAS-Pen2o-QKV" — appears to be a typo for "ATLAS-Pes2o-QKV."

## Nice-to-Haves

- A KBLaM + KG2KV-data control experiment to fully isolate the architecture contribution from the data contribution.
- Accuracy or retrieval-recall measurements at KG sizes of 10⁵–10⁶ triples (even on a synthetic or sampled task) to validate HiKVP's retrieval quality under aggressive pruning ratios.
- Error analysis: when AtlasKV underperforms relative to its no-pruning variant (e.g., 52.2% vs. 72.7% ACC@1 on ATLAS-Pes2o-QKV at 10¹ triples), understanding whether the hierarchy prunes the wrong branch or the KG2KV mapping is ambiguous would help assess the method's maturity.

## Removed Points

The following points from the input review were removed with justification:

- "The paper's central claim is unsubstantiated" — overstates the issue; the paper does show systematic improvements. The variable isolation concern is real but not fatal, and is retained as Major #2.
- "7.864% diversity ratio may not be 'good'" — subjective framing critique without evidence that a higher ratio is needed; KG2KV is 2600× better than the alternative.
- "Should include CAG, LoRA as baselines" — the paper follows KBLaM's evaluation protocol; demanding every method from the related work section is scope creep.
- "ICL figure is physically impossible" — without seeing the actual figure, the strong claim of impossibility is speculative. The unclear description is a real clarity issue (retained as Minor #3).
- Missing appendix/references complaints — parser-stripped sections; not author errors.
- Reproducibility concerns about unreleased datasets/models — the paper cites ATLAS (Bai et al., 2025) and KBLaM (Wang et al., 2024); these are assumed to exist per policy.
- Grammar/formatting nitpicks — parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add the KBLaM + KG2KV-data control.** Train KBLaM on ATLAS-Wiki-QKV data and include the results in Table 3. If AtlasKV still significantly outperforms KBLaM on the same data, the architecture's independent value is confirmed. If not, the paper should reframe its claims to emphasize KG2KV's data contribution.
2. **Benchmark accuracy at larger KG sizes.** Measure grounding accuracy or retrieval recall at 10⁵–10⁶ triples to validate that HiKVP's hierarchical retrieval works under realistic pruning.
3. **Clarify Figure 4.** Explain what the ICL curve actually measures. If ICL uses retrieved subsets rather than full-context, rename it accordingly. Better yet, include a table with measured VRAM at several discrete KG sizes.
4. **Add a brief limitations paragraph** acknowledging the upfront preprocessing cost and discussing when the one-time build is acceptable vs. prohibitive.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>