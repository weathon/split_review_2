## Summary

AtlasKV proposes a parametric method for augmenting LLMs with knowledge graphs, building on the KBLaM paradigm. It introduces two main components: (1) **KG2KV**, a pipeline that converts KG triples (h, r, t) into Q-K-V training data by masking entities and rewriting relations into noun phrases, and (2) **HiKVP**, a hierarchical key-value pruning algorithm (three-layer clustering with cube-root scaling, S = ⌈∛M⌉) that aims for sub-linear time and memory complexity during inference. The paper claims this enables billion-scale KG augmentation in under 20GB VRAM.

## Strengths

1. **The KG2KV data construction is well-motivated and shows clear benefits.** The observation that a KG triple (h, r, t) can be decomposed into query (question prefix), key (unmasked entity + rewritten relation), and value (masked entity) is clean and natural. Table 1 reports 7.864% query diversity ratio vs. 0.003% for KBLaM's synthetic data, demonstrating a meaningful improvement. (Section 4.1, Table 1)

2. **The hierarchical pruning structure is soundly designed.** The cube-root cluster size (S = ⌈∛M⌉ with three layers) gives a concrete sub-linear complexity mechanism. The step-by-step description of HiKVP (Section 4.2, Steps 1–3) and the CPU-GPU memory offloading strategy are clearly explained and reasonable.

3. **Accuracy improvements over KBLaM on OOD datasets are large and consistent.** In Table 3, on ATLAS-Pes2o-QKV with 10² triples, AtlasKV w/o HiKVP achieves 92.7% ACC@1 vs. KBLaM's 25.5% (at 2e4 steps). Even with HiKVP pruning (128-64-16 top-k), AtlasKV achieves 82.3% vs. 25.5%. These gaps are substantial and suggest the overall approach (data + method) is genuinely effective at the tested scales. (Table 3)

## Weaknesses

### Fatal
None.

### Major

1. **The billion-scale accuracy claim is not empirically validated — experiments max out at 1,000 triples.** The title, abstract, and introduction repeatedly claim scaling to 1B triples. However, the accuracy experiments (Table 3) stop at 10³ (1,000) triples — six orders of magnitude below 1B. The GPTScore experiments (Figure 5) go only to 10⁴ triples. While Figure 4 projects sub-linear memory via complexity analysis, the paper provides no evidence that accuracy holds at scales beyond 1K triples. The hierarchical clustering preprocessing (UMAP+GMM on M keys) itself has significant computational cost that is not discussed or measured for billion-scale scenarios. A method validated only at 1K triples does not automatically generalize to 1B.

2. **The two main evaluation metrics are disconnected, leaving the core claim untested as a whole.** The accuracy metric (Table 3) extracts post-softmax attention scores from layer 15 to check whether the model *attends to* the correct KG triple — a proxy that does not directly measure whether the model generates the correct answer. The GPTScore metric (Figure 5) does measure actual generation quality, but it only evaluates AtlasKV **without HiKVP**. This creates a gap: (a) accuracy numbers include HiKVP but evaluate a proxy, and (b) generation-quality numbers measure what we actually care about but omit the pruning mechanism. No single experiment validates that AtlasKV with HiKVP produces correct generated answers at scale. (Section 5.2, Table 3, Figure 5)

### Minor

3. **The comparison with KBLaM is confounded by training data differences.** In Table 3, AtlasKV is trained on ATLAS-Wiki-QKV (constructed via KG2KV) while KBLaM is evaluated with its original Synthetic training data. The paper attributes AtlasKV's better performance to its method, but the improvement could partially stem from having higher-quality training data. A controlled experiment — KBLaM trained on ATLAS-Wiki-QKV, or AtlasKV trained on Synthetic data — would isolate the effect of the method from the data. The ablation study (Table 4) only investigates entity-type composition, not data source. (Table 3, Section 5.3)

4. **No empirical RAG baseline is included.** The paper's motivation criticizes RAG methods (Lines 30–33), and the introduction claims comparison with "RAG methods" (Line 47). Yet the experiments compare only with KBLaM, ICL, and zero-shot. Table 2 provides complexity analysis for RAG, but no empirical results. Given the paper's framing, an actual RAG comparison with a retriever would substantially strengthen the evaluation. (Section 5.1)

5. **The "training-free adaptation" claim is narrow.** AtlasKV requires training KG-specific projection heads (θ = {𝐖̃_Q, 𝐖̃_K, 𝐖̃_V}). The paper claims "training-free" adaptation to new KGs (Lines 34, 271), but new KGs still require running the KG2KV pipeline (which consumes LLM tokens per triple) and building the hierarchical clustering structure (UMAP+GMM). These are non-trivial preprocessing steps.

6. **Preprocessing cost of the hierarchical clustering is not quantified.** Building the three-layer hierarchy requires running UMAP on the full set of M key embeddings followed by GMM clustering. For M approaching 10⁹, this is computationally intensive. The paper does not discuss the time or memory cost of this offline preprocessing step. (Section 4.2)

### Trivial
None.

## Nice-to-Haves
- Adding generation-quality results (GPTScore) for AtlasKV **with HiKVP** would connect the two halves of the evaluation.
- A controlled experiment separating the effect of KG2KV data from the effect of the architectural method.
- Wall-clock latency measurements would complement the asymptotic complexity analysis.
- Explicit qualification that the billion-scale memory figures are derived from complexity formulas unless empirically measured.

## Removed Points

These points are flagged to be removed; treat them with caution:
- **Table 4 column header typo**: The third column reads "10³" instead of "10¹" — this is likely a parser/formatting artifact, not an author error.
- **Constants C_t and C_m not bounded**: The derivation is relegated to Appendix D, which was stripped by the parser. This is a presentation choice, not a substantive flaw.
- **KG2KV requires an LLM call per triple**: The paper acknowledges and quantifies this cost (Avg. Token Cost 165.7 per triple in Table 1). The cost is inherent to the approach, not a hidden deficiency.
- **No statistical significance / error bars in Table 3**: While desirable, single-run evaluation for this type of parametric method is standard in the field (KBLaM itself does not report error bars).

## Novel Insights

The harsh critic's observation that the paper's evaluation is structurally split across two disconnected settings — accuracy (attention-score proxy with HiKVP) vs. generation quality (GPTScore without HiKVP) — is the most incisive critique. This means that a reader cannot look at any single experiment and confirm that AtlasKV with HiKVP both prunes efficiently and generates correct answers. The critic also correctly identifies that the billion-scale claim rests entirely on analytical complexity projections for memory, while accuracy is never measured at scales beyond 1K triples — a gap between claims and evidence that is larger than what comparable papers in this space typically exhibit.

## Suggestions
1. Add an accuracy experiment at a substantially larger scale (at least 10⁵ triples) to validate that the method's accuracy holds beyond 1K triples.
2. Run GPTScore for AtlasKV with HiKVP to connect accuracy and generation quality in a single evaluation.
3. Include a controlled experiment training KBLaM on ATLAS-Wiki-QKV data to separate method effects from data effects.
4. Add an empirical RAG baseline comparison to substantiate the paper's motivational framing.
5. Acknowledge and quantify the preprocessing cost of UMAP+GMM clustering at scale.
6. Calibrate the headline claims to the scales actually tested, or explicitly qualify billion-scale claims as projections.

## Score and Decision

**Calibration anchors used:**
1. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/aLsMzkTej9.md` — **KBLaM paper, avg 5.80 (Accept)**. Direct predecessor. Its claims ("more than 10K triples") were proportional to its evidence. AtlasKV has stronger methodological components but a much larger claim-evidence gap and a disconnected evaluation. AtlasKV is weaker.
2. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Hw1tOjCWBZ.md` — **KARPA, avg 4.60 (Reject)**. Training-free KGQA method. Similar level of methodological contribution but reviewers found novelty lacking. AtlasKV has more technical novelty but worse claim-evidence proportionality.
3. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/pG820nmDvy.md` — **Running Huge Context Windows, avg 4.67 (Reject)**. Claims 1M-token context on tiny GPUs and tests it. AtlasKV claims larger scale (1B vs 1M) but tests at smaller scale relative to its claim. Similar pattern of ambitious claims with incomplete validation.
4. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/DOA1WSPZSi.md` — **OKGQA, avg 4.75 (Reject)**. Benchmark paper for KG+LLM trustworthiness. Different type of contribution but similar score tier.
5. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5swfKRkCx7.md` — **Two Heads RAG, avg 3.75 (Reject)**. Lower-tier paper with weaker contributions. AtlasKV is clearly stronger.

**Round-1 bracket:** 3.5–5.5. **Narrowing:** The paper's methodological contributions (KG2KV + HiKVP) are genuine and demonstrate clear advantages over KBLaM at tested scales, placing it above the 3.5–4.0 floor. However, the gap between the headline billion-scale claim and the actual evidence (accuracy tested only to 1K triples, disconnected evaluation) is a serious structural issue that prevents acceptance at the level of KBLaM (5.80). The paper sits in the 4.0–5.0 range.

**Final score: 4.0 (Borderline Reject).** The paper has real ideas and promising small-scale results, but the central claim of billion-scale viability is unsubstantiated by the evidence presented, and the evaluation structure prevents a clean reading of the method's overall effectiveness.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>