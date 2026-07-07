Now let me write the final consolidated review.

## Summary

This paper proposes AtlasKV, a method for augmenting LLMs with billion-scale knowledge graphs under low GPU memory (<20GB VRAM). It introduces two components: (1) **KG2KV**, a pipeline that converts KG triples (h, r, t) into Q-K-V training/inference data by masking head/tail entities and rewriting relations into noun phrases, and (2) **HiKVP**, a hierarchical key-value pruning algorithm that reduces the rectangular attention complexity of KBLaM from O(M) to O(∛M) via a three-level clustering hierarchy. Experiments compare against KBLaM and ICL baselines on knowledge grounding accuracy and memory scaling.

## Strengths

- **The sub-linear complexity insight is well-motivated and technically sound.** The paper correctly identifies KBLaM's linear-M complexity as prohibitive at billion-scale, and the three-level hierarchy with cluster size S = ⌈∛M⌉ produces a meaningful cube-root reduction (O(∛M)). The derivation is coherent. (§3.2, §4.2)

- **The KG2KV data construction pipeline is a practically useful contribution.** Converting KG triples into Q-K-V form by masking entities and rewriting relations into noun phrases, then adding diverse questioning prefixes, is a clean way to generate diverse training data from structured KGs. The reported diversity improvement (7.864% vs. 0.003%) and token cost reduction (165.7 vs. 349.9) over synthetic data are striking if confirmed. (§4.1, Table 1)

- **The paper clearly articulates two specific challenges** of the KBLaM paradigm—limited training data diversity and poor scalability—and proposes separate components (KG2KV for data, HiKVP for scalability) to address each. This structured framing is a genuine strength.

## Weaknesses

### Major

**1. The main accuracy comparison (Table 3) conflates the method contribution with the data contribution.** AtlasKV is trained on its own KG2KV-derived data (ATLAS-Wiki-QKV) while KBLaM is trained on the original Synthetic data from its paper. The large accuracy gaps (e.g., 82.3% vs. 16.4% ACC@1 on ATLAS-Pes2o-QKV at 10² triples) could be driven entirely by training data quality rather than any algorithmic advantage of HiKVP or the AtlasKV projection heads. The paper does not include the controlled experiment of training AtlasKV on Synthetic data or training KBLaM on KG2KV data. Without this separation, the claimed superiority over KBLaM cannot be attributed to the method itself—it is unclear whether the gain comes from the KG2KV data, the AtlasKV heads, or both. (§5.1, Table 3)

**2. No accuracy validation at the billion-triple scale that forms the paper's headline claim.** Figure 4 shows GPU memory scaling up to 10⁹ triples (AtlasKV ~20GB, flat), which is the paper's flagship scaling result. However, Table 3—the accuracy table—only reports results up to 10⁴ triples. At 10⁹ triples, the HiKVP top-k parameters (128-64-16) select at most 16 out of 1B leaf-layer KV pairs. Whether knowledge grounding accuracy survives this extreme pruning rate is an empirical question that the paper does not answer. The central quantitative claim ("billion-scale KGs with <20GB VRAM while achieving superior knowledge grounding") is only half-supported: memory is demonstrated, accuracy is not. (Figure 4, Table 3)

### Minor

**3. The "OOD" evaluation datasets are not truly out-of-distribution relative to the training data.** AtlasKV is trained on ATLAS-Wiki-QKV and evaluated on ATLAS-CC-QKV and ATLAS-Pes2o-QKV, which are constructed from other ATLAS-family KGs using the same KG2KV pipeline. All three share the same underlying ontology, entity types, relation categories, and data-construction procedure. Only the Enron dataset is genuinely OOD. The claim that ATLAS-CC and ATLAS-Pes2o evaluate "generalization capabilities" (§5.1) overstates what these datasets measure—they primarily test transfer within the same distribution family. (§5.1)

**4. The paper claims comparison with RAG methods in its contributions and abstract but does not implement any actual RAG baseline.** The experimental section (§5.1) lists ICL as "the basic knowledge augmentation paradigm used in RAG methods" and only compares against ICL, KBLaM, and zero-shot. ICL (putting all triples in context) is not RAG—RAG uses a retriever to select a subset. E² GraphRAG and LinearRAG are discussed in related work (§2) but never compared. The paper positioned itself against RAG beyond what the experiments support. (§1, §5.1)

**5. The ICL baseline in Figure 4 operates under undisclosed conditions, making the memory comparison uninterpretable.** The figure shows ICL and zero-shot both with "much lower memory usage, staying below 20GB" at all KG sizes up to 10⁹. If ICL were putting all triples into context, its memory would grow with M. The only way ICL stays flat below 20GB at 10⁹ triples is if it uses a fixed, small subset—but then the comparison is not apples-to-apples with AtlasKV, which processes the entire KG via HiKVP. The paper does not disclose the ICL setup at each KG size. (Figure 4)

**6. The "training-free adaptation" claim (§6) is imprecise.** The paper states AtlasKV "can be adapted to new knowledge in a training-free manner," but the method requires initial training of the KG-specific projection heads (W̃_Q, W̃_K, W̃_V). What is meant is that after those heads are trained, new KV pairs can be added without retraining the heads. This is a meaningful property but the phrasing is misleading without qualification. (§4.2, §6)

**7. The diversity ratio for synthetic data (0.003% in Table 1) lacks the denominator needed to evaluate the comparison.** At 0.003%, this implies roughly 3 unique enquiry attributes per 100,000 triples. While the paper attributes this to fixed pre-defined schemas, the total number of triples over which both the diversity ratio and average token cost are computed is not stated. More detail is needed to assess whether the comparison is controlled. (Table 1, §4.1)

## Nice-to-Haves

- **Add a genuine RAG baseline** (e.g., bi-encoder retriever + top-k context) to support the paper's positioning against RAG.
- **Discuss the cost of building the hierarchy** (UMAP + GMM at billion-scale), even if it is a one-time preprocessing cost.
- **Clarify the ICL setup** in Figure 4: what subset of triples is used per KG size, and how is it selected?

## Removed Points

- **Table 4 column header duplication (10³ listed twice):** This is a formatting artifact from PDF extraction, not a paper error. Removed per hard rules.
- **Criticisms about missing appendix content (samples, prompt templates, derivations):** The parser strips appendix sections from all papers; these exist in the original submission. Removed per hard rules.
- **UMAP/GMM scaling concern framed as a fatal limitation:** This is a one-time preprocessing cost, not an inference limitation. Moved to Nice-to-Haves.
- **Observation that the equivalent attention is a reparameterization:** This is not a concrete weakness; the paper's novelty lies in KG2KV and HiKVP, which is appropriate.

## Novel Insights

None beyond the paper's own contributions. The reviews surface familiar concerns about confounded experimental design and missing scale validation but do not add fundamentally new analytical insights about the method itself.

## Suggestions

1. **Disentangle method from data:** Conduct a 2×2 experiment—(AtlasKV heads vs KBLaM heads) × (KG2KV data vs Synthetic data)—to isolate the contribution of each.
2. **Measure accuracy at larger scales:** Report accuracy at 10⁵, 10⁶, and (if feasible via sampling) 10⁹ triples to validate that HiKVP's extreme pruning retains relevant knowledge.
3. **Clarify the ICL in Figure 4:** State what subset of triples is used, and how it is selected.
4. **Add a genuine RAG baseline** to support the paper's positioning.
5. **Qualify the "training-free" claim** to clarify that initial training of KG-specific heads is still required.
6. **State the denominator** for the diversity ratio and token cost computations in Table 1.

## Score and Decision

**Calibration Anchors (all rounds):**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/aLsMzkTej9.md` — KBLaM, avg 5.80, Round 1+2. Itemized. The direct predecessor paper; AtlasKV builds on it but has additional evaluation gaps (confounded comparison, missing accuracy at scale) that KBLaM did not have.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/nnVO1PvbTv.md` — Think-on-Graph, avg 7.00, Round 1. Itemized. A stronger KG-LLM integration paper with extensive experiments; AtlasKV is clearly weaker in evaluation scope.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Hw1tOjCWBZ.md` — KARPA, avg 4.60, Round 1. Itemized. A paper with similar "training-free" overclaim and novelty concerns; AtlasKV has stronger technical contributions but similar evaluation gaps.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/t21RmVmJrT.md` — avg 5.00, Round 2. Not itemized.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/sl4hOq9wm9.md` — avg 5.50, Round 2. Not itemized.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/aCPFCDL9QY.md` — avg 5.75, Round 2. Not itemized.

**Weighted-item comparison:** My draft's strengths (KG2KV pipeline at +5.81, sub-linear complexity at +4.33) are comparable to KBLaM's top strengths. However, my paper's major weaknesses have heavier negative weights than KBLaM's worst weaknesses: the data confound (-5.17) and missing billion-scale accuracy (-4.02) are structural evaluation gaps that KBLaM did not face. The missing RAG baseline (-6.13) and unclear ICL setup (-5.08) add further weight. Together these push the paper below KBLaM's score of 5.80, into the 4.0–5.0 range.

**Initial bracket:** [4.0, 5.5]. **Final score:** 4.5.

The core ideas (KG2KV data construction and HiKVP hierarchical pruning) are genuinely interesting and well-motivated. However, the evaluation as presented has two structural gaps: (1) the main accuracy comparison conflates method contribution with data contribution, and (2) the headline billion-scale claim has no accuracy validation at that scale. These gaps prevent the paper from being a clear accept, despite the novelty of its components.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>