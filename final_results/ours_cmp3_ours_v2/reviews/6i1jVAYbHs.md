Now I'll produce the final consolidated review.

## Summary

AtlasKV proposes a parametric method for augmenting LLMs with large knowledge graphs, combining two components: (1) **KG2KV**, a pipeline that converts KG triples (h, r, t) into Q-K-V training data by exploiting the natural decomposition of triples, achieving substantially higher diversity than synthetic alternatives (7.864% vs 0.003%), and (2) **HiKVP**, a hierarchical key-value pruning algorithm that reduces inference-time time and memory complexity to sub-linear (∛M). The paper demonstrates memory scaling up to 1B triples with <20GB VRAM and reports accuracy/generation improvements over KBLaM at up to 1K triples, alongside informative ablations on entity types.

## Strengths

1. **Well-motivated problem framing.** Sections 3.2 and 1 clearly identify KBLaM's linear complexity in M as a bottleneck for large-scale KG augmentation, and correctly diagnose the lack of diverse training data as a second critical limitation. Addressing both simultaneously is a worthwhile and timely goal.

2. **KG2KV data construction is a clean, well-evidenced idea.** The observation that KG triples (h, r, t) decompose naturally into Q-K-V form (Section 4.1, Figure 2) is elegant. Table 1 convincingly shows KG2KV achieves 7.864% diversity ratio vs 0.003% for the synthetic baseline, with lower average token cost (165.7 vs 349.9). This is a genuine contribution independent of the architectural changes.

3. **Clean complexity analysis.** Table 2 provides a clear head-to-head complexity comparison across ICL, RAG, CAG, KBLaM, and AtlasKV. The sub-linear ∛M scaling claim is explicit and the derivation is referenced.

4. **Informative entity-type ablation.** Table 4 shows that both named and event entities contribute to performance, with the full combination working best. This provides practical guidance for practitioners using KG2KV.

## Weaknesses

### Fatal
None.

### Major

1. **Billion-scale performance claim is not empirically tested.** The paper's title, abstract (line 9), and contribution list (line 42) claim AtlasKV "enables end-to-end augmentation of LLMs with billion-scale KGs... while achieving superior knowledge grounding performance." However, task performance (ACC@1/ACC@5) is evaluated at a maximum of **1,000 triples** (Table 3). Figure 5 (GPTScore) evaluates up to **10,000 triples**. There is no accuracy or generation-quality evidence at 1M, 10M, or 1B triples. The memory advantage at billion-scale is demonstrated (Figure 4), but whether accuracy holds under the extreme compression required at that scale (1B → 16 leaf candidates via HiKVP) remains an unanswered empirical question. The paper's central headline is not supported by the experiments reported.

2. **Confounded comparison against KBLaM.** AtlasKV is trained on ATLAS-Wiki-QKV (KG2KV-format data) while KBLaM is trained on the Synthetic dataset. The evaluation datasets ATLAS-CC-QKV and ATLAS-Pes2o-QKV are also constructed via KG2KV, meaning AtlasKV is evaluated in-distribution on data format while KBLaM is evaluated out-of-distribution. The large performance gap (e.g., 82.3% vs 16.4% ACC@1 on ATLAS-Pes2o-QKV at 100 triples, Table 3) could be primarily driven by the training-data format mismatch rather than architectural superiority. A controlled experiment — training KBLaM on ATLAS-Wiki-QKV or AtlasKV on Synthetic — is needed to separate the effect of training data from the effect of the method architecture. The paper's claim that this demonstrates AtlasKV's "superior generalization" is confounded.

3. **Full method absent from generation-quality evaluation.** Figure 5 reports GPTScore for "AtlasKV w/o HiKVP" but **not** for AtlasKV with HiKVP (the full proposed method). Table 3 shows that HiKVP causes non-trivial accuracy drops — on ATLAS-CC-QKV at 10 triples, ACC@1 drops from 83.6% (w/o HiKVP) to 61.8% (with HiKVP), a 21.8-point drop. Without GPTScore for the full method, readers cannot assess how HiKVP affects generation quality, leaving a critical gap in the evaluation of the complete system.

### Minor

4. **No empirical RAG or graph-RAG baselines despite claiming comparison.** The contribution list (line 47) claims comparison with "ICL, KBLaM, and RAG methods," but no RAG system is empirically benchmarked. Only ICL (used as a proxy), KBLaM, and zero-shot are evaluated. While the complexity table (Table 2) includes RAG and CAG for theoretical comparison, the empirical evaluation would benefit from at least one representative RAG or graph-RAG baseline to contextualize the reported gains.

5. **No variance estimates for accuracy results.** Table 3 reports single-point accuracy numbers without confidence intervals or multiple-run statistics. Given the small evaluation sizes (55 queries per KG-size condition), a few misclassifications could swing percentages by several points. The GPTScore evaluation (Figure 5) reports standard error over 5 seeds, but the accuracy evaluation does not.

6. **ICL memory behavior in Figure 4 is internally inconsistent.** The figure shows ICL with flat memory usage below 20GB across 10⁴–10⁹ triples. However, the paper itself states that ICL with "more than 100 triples... over 48GB VRAM is required" (line 245). Showing ICL as using less memory than AtlasKV at billion-scale while simultaneously arguing ICL is infeasible at that scale is contradictory and needs clarification of the measurement conditions.

7. **Knowledge grounding metric needs clearer definition.** The paper states the metric extracts "averaged-over-heads KG part post-softmax attention scores at the 15th layer" to determine Top-1/5 accuracy (line 212-213). It is unclear how the "correct" KG triple is identified for a given query, how ties are handled, and why the 15th layer is chosen.

8. **HiKVP's dependence on clustering quality is not analyzed.** The hierarchical pruning relies on UMAP+GMM clustering, which is itself approximate. If a relevant key is assigned to the wrong cluster at the root layer, it is eliminated with no chance of recovery. The paper does not discuss the probability or consequences of this failure mode, which is critical for a method whose scalability depends on aggressive pruning.

### Trivial

9. **"128-64-16" notation in Table 3 is explained only in the caption.** The main text should define k_R, k_I, k_L explicitly when the table is first discussed.

## Nice-to-Haves
- Evaluate task performance (accuracy and/or GPTScore) at substantially larger KG sizes (e.g., 10⁵–10⁷ triples) to directly validate the billion-scale claim.
- Train KBLaM on ATLAS-Wiki-QKV (or AtlasKV on Synthetic) to disentangle data-driven vs. architecture-driven gains.
- Report GPTScore for AtlasKV with HiKVP to complete the evaluation of the full system.
- Report wall-clock inference time in addition to memory usage and complexity.
- Provide confidence intervals for the accuracy results in Table 3.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Attention equivalence proof deferred to Appendix C:** The paper states the equivalence of its attention formulation to KBLaM's rectangular attention is proven in Appendix C. Since the parser strips appendices, this is not a verifiable weakness from the main text alone. **Removed** under the rule against penalizing missing appendix content.
- **Relation rewriting LLM dependency:** The paper states that "the influence of relation rewriting process... is also analyzed in Appendix B.2" (line 103). The concern that it is "not analyzed" contradicts the paper's statement. **Removed** since the appendix exists in the original submission.
- **Complexity derivation precision (k_R × S vs ∛M):** The constants C_t and C_m are acknowledged to depend on top-k parameters. The complexity statement remains O(∛M) with constant factors that are "much smaller than M" — this is standard and acceptable precision for complexity analysis. **Removed** as the criticism does not identify a genuine error.
- **Enron OOD claim weakened:** The paper explicitly acknowledges this limitation (line 244-245: "despite having only limited training samples with enquiry attributes similar to Enron"), so the criticism adds no new information beyond what the authors already state. **Removed** as already addressed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a controlled experiment training KBLaM on ATLAS-Wiki-QKV (or AtlasKV on Synthetic) to disentangle data and architecture effects.
2. Report GPTScore for AtlasKV with full HiKVP to complete the system evaluation.
3. Add variance or confidence intervals to the accuracy results in Table 3.
4. Clarify the ICL measurement conditions in Figure 4 to resolve the apparent inconsistency.
5. Explicitly acknowledge in the abstract that task performance is evaluated at smaller scales (up to 1K triples for accuracy, 10K for GPTScore) while memory scalability is demonstrated up to 1B triples. Alternatively, add accuracy results at larger KG sizes.

---

## Calibration and Score

**Calibration anchors retrieved (all from deepreview_13k_calibration):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/aLsMzkTej9.md (KBLaM) | 5.80 | R1 | Direct predecessor; cleaner evaluation without overclaim, similar technical depth → AtlasKV is weaker |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Hw1tOjCWBZ.md (KARPA) | 4.60 | R1 | KGQA framework; similar evaluation quality, AtlasKV has stronger technical contributions |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/DOA1WSPZSi.md (OKGQA) | 4.75 | R1 | KG+LLM benchmark; comparable rigor level |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ds3Tcnrte8.md (QAP) | 3.00 | R1 | GNN+LLM prompting; much weaker, AtlasKV is clearly stronger |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/JvkuZZ04O7.md (SubgraphRAG) | 6.00 | R1 | KG-RAG with stronger evaluation; AtlasKV has comparable technical depth but weaker evaluation |

**Round 1 bracket:** 4.0 – 5.5 (between KARPA/OKGQA and KBLaM/SubgraphRAG)

**Final score rationale:** AtlasKV has genuine technical contributions (KG2KV, HiKVP, clean complexity analysis) that are well-motivated and partially well-evaluated. However, the paper's central claim — billion-scale augmentation with strong performance — is unsupported by task-performance evidence at that scale, the comparison against KBLaM is confounded by different training data, and the full method's generation quality is not evaluated. These gaps are more severe than KBLaM's weaknesses (which mainly concerned missing RAG baselines) and justify a score below KBLaM's 5.8. The paper sits above clearly weaker works like KARPA (4.6) and QAP (3.0) due to its stronger technical core. Score: **4.5**.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>