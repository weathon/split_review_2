Now I have all the information I need. Let me produce the final consolidated review.

## Summary

AtlasKV proposes a parametric framework for augmenting LLMs with knowledge graphs, combining (1) KG2KV, a pipeline that converts KG triples into Q-K-V training data, and (2) HiKVP, a hierarchical key-value pruning algorithm that reduces inference complexity from O(M) to O(∛M). The paper demonstrates that HiKVP allows fitting 1B KG triples within ~20GB VRAM (Figure 4), and that KG2KV-derived training data substantially improves OOD generalization over schema-generated synthetic data (Table 3).

## Strengths

1. **Sub-linear complexity via HiKVP backed by empirical memory scaling**: Table 2 derives O((C_t ∛M + N)·N·D) time and O((C_m ∛M + N)·(N+D)) memory, and Figure 4 confirms AtlasKV uses ~20GB VRAM at 1B triples while KBLaM exceeds 40GB at just 10^5 triples. This is a concrete algorithmic advance — reducing the dominant term from M to ∛M — and is verified at the claimed billion-scale regime.

2. **KG2KV data quality advantage quantified in Table 1**: KG2KV achieves 7.864% diversity ratio vs. 0.003% for synthetic data (~2600× improvement) while reducing token cost from 349.9 to 165.7. This directly validates the claim that KG triples yield higher-quality training data than schema-defined generation.

3. **Large OOD generalization gains on hard datasets**: On ATLAS-Pes2o-QKV (10^2 triples), AtlasKV achieves 82.3% ACC@1 vs. KBLaM's 16.4% — a 61.8-point gap. AtlasKV trained on ATLAS-Wiki-QKV (limited overlap with Enron) still outperforms KBLaM trained on Enron-specific synthetic data, demonstrating genuine transfer from diverse query attributes.

4. **Faster convergence**: AtlasKV at 3K steps substantially outperforms KBLaM at 20K steps across all three OOD datasets (e.g., 89.1% vs. 23.6% on ATLAS-CC-QKV at 10^2 triples), showing that KG2KV data quality buys convergence speed.

5. **Systematic ablation of entity-type contributions**: Table 4 ablates named vs. event entities in KG2KV — removing event entities drops ACC@1 from 92.7% to 49.0% (ATLAS-Pes2o, 10^2 triples), while removing named entities drops it from 92.7% to 80.0%. The analysis turns an architectural choice into a tested design principle.

6. **GPT-4o-scored generation quality**: Figure 5 reports answer relevance scores (0–1, 5 seeds × 5 generations) across three datasets, providing a complementary metric beyond attention-based grounding accuracy.

## Weaknesses

### Major

1. **Accuracy evaluation does not match the billion-scale claim.** The paper's title and abstract claim augmentation with billion-scale KGs (1B triples). Memory scaling is demonstrated at that scale (Figure 4), but knowledge grounding accuracy (Table 3) maxes out at 10^3 triples and GPTScore (Figure 5) at 10^4 triples — a 6-order-of-magnitude gap. The hierarchical pruning algorithm introduces a trade-off (aggressive top-k pruning at the root could discard relevant clusters before the leaf layer), and the paper provides no experiments probing whether accuracy degrades at 10^5, 10^6, or 10^7+ triples. Without this, the paper's central claim of *effective* billion-scale augmentation is only partially supported: memory scaling works, but the accuracy at scale is unknown.

2. **Training-data confound between method and data source.** AtlasKV is trained on KG2KV-derived ATLAS-Wiki-QKV data while KBLaM is trained on Synthetic data. Table 3 attributes AtlasKV's superior OOD generalization to KG2KV, but this conflates method architecture with training data. A controlled experiment — training KBLaM on ATLAS-Wiki-QKV or training the AtlasKV architecture on Synthetic data — is necessary to isolate the source of improvement. Without it, readers cannot determine how much of the gain comes from the KG2KV data pipeline versus the AtlasKV architecture itself.

### Minor

1. **No empirical RAG baseline in accuracy evaluation.** The paper discusses RAG throughout (complexity analysis in Table 2, related work) and the contribution list claims comparison "to ICL, KBLaM, and RAG methods," but the accuracy tables (Table 3, Figure 5) include only ICL, KBLaM, and zero-shot. Graph-based RAG methods (E² GraphRAG, LinearRAG) and KGQA methods (RAR, KnowGPT) are cited in related work but omitted from empirical comparison. This weakens the experimental positioning against the most natural competitor.

2. **Primary accuracy metric is an indirect proxy.** Table 3 measures "knowledge grounding accuracy" by whether the LLM's attention scores in layer 15 align with the correct KG triple — not whether the model generates the correct answer. An LLM could attend to the right triple but generate the wrong answer, or vice versa. The GPTScore evaluation (Figure 5) partially addresses this, but it evaluates *AtlasKV w/o HiKVP* rather than the full method with pruning. Standard end-to-end KGQA metrics (exact match, F1) would calibrate what the grounding accuracy numbers mean.

3. **ICL memory comparison in Figure 4 is unclearly scoped.** Figure 4 shows ICL memory usage staying flat and below 20GB from 10^4 to 10^9 triples. If ICL puts all M triples in context (as implied by Table 2's O((MT+N)²·D) complexity), its memory should grow with M. This suggests the ICL baseline uses only a small fixed subset (e.g., via a retriever selecting the top-R relevant triples), but the paper does not clarify this. The comparison is not informative as presented.

4. **No accuracy variance for grounding results.** Table 3 reports single numbers without standard errors, confidence intervals, or multiple seeds for the primary grounding accuracy metric. The GPTScore evaluation uses 5 seeds, but the main results do not.

5. **Relation-rewriting cost in KG2KV not quantified.** The paper states relation rewriting via LLM is "the only part that consumes tokens" (Section 4.1) but does not estimate how many LLM calls or tokens are needed to rewrite billions of relations, which is relevant to practical feasibility at the claimed scale.

6. **Hierarchical clustering at billion scale not addressed.** Clustering 1B vectors with UMAP + GMM is itself a non-trivial engineering challenge. The paper does not discuss its time/memory cost or whether this is a one-time preprocessing step.

### Trivial

- Table 4 header says "ATLAS-Pen2o-QKV" where the correct name (consistent with Table 3 and elsewhere) is "ATLAS-Pes2o-QKV."

## Nice-to-Haves

- Report knowledge grounding accuracy at 10^5, 10^6, or 10^7 triples, even if accuracy degrades — showing the degradation curve would be informative.
- Report end-to-end KGQA accuracy (exact match, F1) on a standard benchmark to ground the proxy metric.
- Controlled experiment: train KBLaM on ATLAS-Wiki-QKV data to disentangle data quality from architecture.
- Add a RAG baseline to empirical accuracy comparisons.
- Clarify the ICL setup in Figure 4: what subset of triples is used, and is a retriever involved?

## Removed Points

These points were raised by reviewers but removed per filtering rules:

- **"Training dynamics observation deferred to Appendix E":** Removed because appendix content is stripped by the parser; it exists in the original submission. The main text states the key observation.
- **"Missing related works":** Removed per instructions — I cannot verify the existence of missing references.
- **"Method categorization is problematic":** The paper's classification of methods into parametric/non-parametric is defensible and standard in this area.
- **Pure formatting/typographical nitpicks:** Removed per filtering rules — these are parser artifacts, not author errors.
- **Strawman about "no proof at all":** The paper provides complexity derivations (Appendix D reference) and equivalence proof to rectangular attention (Appendix C reference).

## Novel Insights

The synthesis of both reviews reveals a central structural tension: the paper convincingly demonstrates two separate things — (a) that HiKVP achieves sub-linear memory scaling verified at 1B triples, and (b) that KG2KV data substantially improves OOD accuracy at small scales (≤10^3 triples) — but never bridges the gap between them. The hierarchical pruning algorithm's fundamental trade-off (aggressive root-level pruning could discard relevant clusters at coarser granularity) is theoretically acknowledged but never empirically probed at the scale where it would matter most. This creates a situation where the paper's strongest evidence (memory at 1B) and weakest evidence (accuracy at 10^3) serve different parts of the same "billion-scale effectiveness" claim without connecting. The paper would be substantially stronger if it showed a degradation curve or even a single accuracy data point at 10^5–10^6 triples.

## Suggestions

1. **(Highest leverage)** Add accuracy scaling experiments at 10^5–10^7 triples. Even a single dataset at one pruning setting would dramatically strengthen the billion-scale claim.
2. Run a controlled experiment training KBLaM on ATLAS-Wiki-QKV data to disentangle data quality from architecture.
3. Clarify the ICL setup in Figure 4 — specify what subset of triples is used and whether/which retriever is involved.
4. Report standard KGQA metrics (exact match, F1) on at least one benchmark.
5. Quantify the LLM token cost for relation rewriting at the billion-scale setting.

## Score and Decision

**Calibration note:** The calibration tool was unavailable due to an infrastructure error, so calibration is based on the paper's content and review analysis directly.

This paper makes genuine contributions: the KG2KV pipeline is a principled approach to converting KGs into training data for the rectangular-attention paradigm, and HiKVP is a well-designed hierarchical pruning algorithm with clean theoretical backing. The memory scaling result is striking and verified. The OOD generalization improvements are large and convincing at the scales tested.

However, the paper's central claim — that AtlasKV enables *effective* billion-scale KG augmentation — is only half-supported. Memory scaling is shown at 1B triples; accuracy is only shown at ≤10^3 triples (a 10^6× gap). Combined with the training-data confound, missing RAG baseline, and proxy metric concerns, the evaluation falls short of fully establishing the claimed capability. The work has clear value but needs additional experiments to match its own framing.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>