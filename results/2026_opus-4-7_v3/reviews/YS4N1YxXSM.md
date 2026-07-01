Now let me check the ablation tables and additional details referenced in the paper:Now I have thoroughly read the paper. Let me submit the draft review and then proceed with calibration.Now let me run the calibration search — Round 1 Bracketing:Let me read the most relevant anchor papers in detail for calibration:Now I have sufficient calibration data. Let me form my Round 1 bracket and write the final review.

**Round 1 Bracket Analysis:**

- **Score 1-3 (reject)**: Papers like IntelLLM (3.0) have weak novelty, poor writing, missing baselines. QUOKA is clearly far above these.
- **Score 4-5 (borderline reject)**: Papers like LazyLLM (5.0), DynamicKV (4.4), KV Prediction (4.5). These have decent ideas but limited evaluation or methodological gaps. QUOKA's evaluation is much broader and results stronger.
- **Score 6 (borderline accept)**: Cascading KV Cache (6.0), OmniKV (6.0). These are solid but had limited baselines or evaluation scope. QUOKA exceeds these in evaluation breadth, hardware diversity, and magnitude of empirical gains.
- **Score 8 (accept)**: FlexPrefill (8.0) — the most directly comparable paper (sparse attention for prefill). FlexPrefill received unanimous 8s but with similar reviewer concerns (missing baselines, mixed performance). QUOKA tests more models (6 vs 4) and hardware platforms (3 vs 1), but FlexPrefill has stronger per-head analysis and compares against MInference.

**Initial bracket: 6.5–7.5**

QUOKA sits above the borderline-accept papers (6.0) due to its broader evaluation and stronger empirical gains, but below FlexPrefill (8.0) due to the single-head motivation and missing dense baseline in the main table. 

Now let me write the final consolidated review:## Summary
QUOKA proposes a training-free, hardware-agnostic sparse attention algorithm specifically designed for the chunked prefill setting in LLM inference. Its core contribution is a three-stage pipeline: (1) query subselection via cosine dissimilarity from the mean query, (2) cosine-similarity-based key scoring, and (3) group-aware aggregation compatible with GQA architectures. The method uses only standard linear algebra operations (no custom CUDA kernels), achieving up to 5× attention speedup and 3× TTFT reduction with minimal accuracy degradation across six model families and four benchmarks.

## Strengths
- **Algorithmic simplicity and hardware portability.** The entire method (Algorithm 1) consists of cosine similarities, top-k, gather, and mean operations. Speedups are demonstrated concretely on three distinct hardware platforms — A100, RTX 2080, and Intel Xeon CPU (Figure 5) — which is unusually comprehensive for this area.

- **Geometrically motivated query subselection.** The insight that queries dissimilar to the mean query attend more broadly across keys is clean and supported by Figure 2's PCA visualization and S_q–max_k(A) correlation (r=0.737). The three-stage design follows logically from this observation, and each component is individually ablated (Tables 9, 10, 12), confirming that cosine similarity scoring improves selection by >10% over dot product (Table 9) and max aggregation outperforms mean (Table 10).

- **Broad and rigorous evaluation grid.** Six model families spanning standard (Llama3.2-3B, Qwen2.5-3B, Qwen3-4B), MoE (Qwen3-30B-A3B), NoPE (SmolLM3), and large-scale (GPT-OSS-20B) architectures are tested across four benchmarks (NIAH, RULER, LongBench, Math500). This breadth exceeds most comparable sparse attention papers.

- **Large empirical margins.** On RULER at B_SA=1024 (Table 1), QUOKA leads the strongest baseline (SampleAttention) by 8–33 points across models and lengths. On LongBench (Table 3), QUOKA at B_SA=512 consistently matches or exceeds baselines at B_SA=2048 — a 4× budget advantage. These margins are large enough to be robust to noise.

- **Practical pre-aggregation trick.** Averaging normalized queries across GQA groups before scoring (Section 3.3) reduces computation by the GQA group factor, a useful efficiency contribution justified by the concentrated head-level distribution (Figure 3).

## Weaknesses

### Fatal
None

### Major
- **Motivating observation shown on a single attention head.** Figure 2, which underpins the entire query subselection strategy, is demonstrated only for Llama 3.2-3B layer 0, head 11 (confirmed at line 113: "Empirical observations from Llama 3.2-3B-Instruct, layer 0 head 11"). The reported correlation of 0.737 is moderate. Given the well-known diversity of attention head behaviors (local, global, sink-attending), it is unclear whether this geometric property holds uniformly. A per-head, per-layer analysis across multiple models would transform this anecdote into a generalizable finding. The downstream results suggest the method works despite possible per-head variation, but the mechanistic story that the paper builds its narrative around remains under-supported.

- **Missing full-attention baseline in main comparison table.** Table 1 (the primary RULER comparison) reports only sparse attention methods. Without the dense baseline, readers cannot assess the absolute accuracy cost of QUOKA's sparsification at B_SA=1024. Table 2 partially addresses this with a 25% proportional budget showing modest drops (1–3 points), but these are different operating points. Adding the full-attention row to Table 1 is a low-effort, high-impact fix.

### Minor
- **Unexplained super-dense performance on LongBench.** SmolLM3 achieves normalized LongBench scores of 1.03 and 1.028 at B_SA=1024 and 2048 respectively (Table 3, line 266), meaning QUOKA *exceeds* full attention accuracy. This could reflect beneficial regularization from sparsification, evaluation variance, or normalization artifacts, but the paper does not discuss it. A brief explanation would add credibility.

- **TTFT measured on only one model.** Section 4.6 reports TTFT only for Qwen3-4B (line 276). Given the accuracy evaluation spans six models including a larger Qwen3-30B-A3B and GPT-OSS-20B, reporting TTFT for at least one additional model (especially at different scales) would strengthen the efficiency claims.

- **Selection overhead not separately quantified.** The latency plots (Figure 5) show net speedup but do not break down QUOKA's scoring overhead (cosine similarities, top-k) from the attention savings. This decomposition would help readers understand the method's efficiency characteristics at different operating points.

### Trivial
None

## Nice-to-Haves
- **Ablation of query selection strategies.** Table 12 ablates N_q but does not compare against alternative query selection strategies (random, highest-norm, PCA-based). If QUOKA's cosine-dissimilarity selection were swapped into SampleAttention's pipeline, this would isolate the contribution of the selection mechanism.

- **Comparison with kernel-level sparse attention methods.** The paper argues kernel-level methods (e.g., MInference) are less portable, but never benchmarks against them. Including such a comparison — even if only on A100 — would complete the picture for practitioners.

- **Failure case analysis.** The results are uniformly positive across all settings. Identifying task types, layer depths, or attention patterns where the approximation breaks down would strengthen the paper's trustworthiness.

- **Tighter theoretical contribution.** Theorem 1 provides directional geometric intuition but does not bound the attention approximation error ‖AV − ÂV̂‖. A formal error bound would elevate the theoretical contribution.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Baselines are generation-time methods forced into a setting they were not designed for, inflating QUOKA's gains."** While most baselines originate from generation settings, the paper explicitly acknowledges this (Section 2.4, line 121: "extending these methods to the multiple-query setting with by averaging over queries significantly degrades performance"). Moreover, SampleAttention explicitly targets prefill (Section 5, line 282: "SampleAttention targets prefill but treats multiple queries homogeneously"). The comparison reflects the current state of the field — there are no other chunked-prefill-specific query-dependent methods to compare against. This is a statement about the field's maturity, not a flaw in the paper's evaluation design.

- **"Introduction's claim about kernel-level methods being limited under chunked prefill is asserted but never empirically verified."** This is a framing/scope issue. The paper's explicit scope is hardware-agnostic, kernel-free operation. Not benchmarking against kernel-level methods is a scope choice, not a flaw. Moved to nice-to-have.

- **"Theorem 1 notation is garbled (q* vs q_0)."** Likely a parser artifact from PDF extraction per the rules. Removed.

- **"Math500 claim about surpassing dense attention needs scrutiny — Table 8 is in appendix."** The appendix was stripped by the parser. Cannot evaluate claims about stripped content. Removed.

- **"No kernel-level sparse attention baselines (MInference, SeerAttention)."** These are a different design family (requiring custom CUDA kernels). The paper explicitly positions itself as kernel-free for portability. This is scope, not a gap. Moved to nice-to-have.

## Novel Insights
The observation that queries far from the mean query in cosine similarity space attend broadly across keys, while near-mean queries concentrate on a shared cluster, is a geometrically clean insight connecting query-space geometry to attention sparsity structure. This suggests that query-space geometry is an underexplored axis for sparse attention design — most prior work focuses on key-space properties. The pre-aggregation trick exploiting GQA linearity to reduce scoring cost by the group factor is a practical contribution that others in the field can adopt independently of the rest of the method.

## Suggestions
- Add full-attention baselines to Table 1 to provide absolute accuracy context alongside the sparse method comparisons.
- Provide a histogram or heatmap of per-head S_q–max_k(A) correlations across layers and models (at least 2–3 models) to validate the generality of the core geometric observation.
- Report TTFT for at least one additional model at a different scale (e.g., Qwen3-30B-A3B).
- Briefly discuss the >1.0 normalized scores on LongBench SmolLM3 — whether this reflects regularization, evaluation variance, or normalization artifacts.
- Consider separating QUOKA's selection overhead from the attention savings in the latency analysis.

## Score and Decision

### Calibration Anchors (Round 1)

| Paper | Path | Avg Human Score | Round | Comparison to QUOKA |
|-------|------|----------------|-------|---------------------|
| Systematic Review of LLMs | 8QTpYC4smR | 1.00 | R1 | Not a research contribution; QUOKA is vastly superior |
| Efficient Implementation for Minimax Path | bEgDEyy2Yk | 1.00 | R1 | Code implementation paper with no novelty; irrelevant comparison |
| NEMESIS Jailbreaking LLMs | 5kMwiMnUip | 1.40 | R1 | Weak methodology; QUOKA is far stronger |
| Clothing-Irrelevant Lifelong ReID | 5lUdTogEL3 | 1.00 | R1 | Unrelated domain; clearly inferior in contribution |
| IntelLLM: KV Cache Compression | 4QWPCTLq20 | 3.00 | R1 | Weak novelty, poor writing, missing baselines; QUOKA is clearly better with broader evaluation and cleaner design |
| MixAttention | 2DD4AXOAZ8 | 2.00 | R1 | Limited evaluation; QUOKA far exceeds in scope |
| PrefixQuant | vw0NurJ7UX | 3.00 | R1 | Different focus (quantization); limited novelty per reviewers |
| CASD: Context-Aware Speculative Decoding | g3D27bfmrf | 3.00 | R1 | Different approach; QUOKA has stronger results |
| Running Huge Context Windows On Tiny GPUs | pG820nmDvy | 4.67 | R1 | Similar goal but simpler approach with weaker evaluation; QUOKA has broader model coverage and stronger results |
| KV Prediction for Improved TTFT | QlvL6eEOC6 | 4.50 | R1 | Requires auxiliary model training; QUOKA is training-free with broader evaluation |
| LazyLLM: Dynamic Token Pruning | am5Z8dXoaV | 5.00 | R1 | Good idea but limited evaluation and methodological concerns; QUOKA is stronger in both evaluation breadth and result magnitude |
| DynamicKV: Task-Aware KV Cache | uHkfU4TaPh | 4.40 | R1 | Decent contribution but less comprehensive evaluation; QUOKA is clearly superior |
| Cascading KV Cache | dSneEp59yX | 6.00 | R1 | Good idea with simple implementation, but limited baselines (mainly vs StreamingLLM); QUOKA has broader baselines and evaluation |
| Identify Critical KV Cache | lRTDMGYCpy | 5.75 | R1 | Formal framework for KV criticality but QUOKA has stronger empirical demonstration |
| OmniKV: Dynamic Context Selection | ulCAPXYXfa | 6.00 | R1 | Training-free like QUOKA but limited evaluation scope; QUOKA demonstrates broader model/hardware coverage |
| D2O: Dynamic Discriminative Operations | HzBfoUdjHt | 5.80 | R1 | Layer-level KV optimization; QUOKA has stronger empirical margins |
| FlexPrefill: Context-Aware Sparse Attention | OfjIlbelrT | 8.00 | R1 | Most directly comparable — also sparse attention for prefill. FlexPrefill has stronger per-head analysis, JSD-based dynamic pattern selection, and comparison against MInference. QUOKA has broader model coverage (6 vs 4) and hardware portability, but narrower mechanistic validation. |
| Retrieval Head Mechanistically Explains | EytBpUGB1Z | 8.00 | R1 | Different focus (mechanistic explanation); not directly comparable |
| Combatting Dimensional Collapse | f4gF6AIHRy | 8.00 | R1 | Different domain (pre-training data selection); not comparable |
| MoE++: Zero-Computation Experts | t7P5BUKcYv | 8.00 | R1 | Different focus (MoE efficiency); not comparable |

**Round 1 bracket: 6.5–7.5**

QUOKA is clearly above the 6.0-scored papers (Cascading KV Cache, OmniKV) in evaluation breadth, empirical margins, and method novelty. It is below FlexPrefill (8.0), which has stronger per-head analysis, dynamic adaptation, and comparison against kernel-level baselines. QUOKA's major weaknesses (single-head motivation, missing dense baseline in main table) are real but bounded — they don't threaten the core contribution. The empirical results are strong and consistent across a genuinely broad evaluation grid. The method's hardware portability and simplicity are practical strengths not matched by most competitors.

**Final calibrated score: 7.0**

The paper sits solidly between borderline accept and accept. It identifies a real gap (generation-time sparse attention methods fail under chunked prefill), provides a clean algorithmic solution, and demonstrates it works convincingly across a wide evaluation grid. The evidential gap in the motivating observation and the missing dense baseline in Table 1 prevent a higher score, but these are addressable issues that do not undermine the contribution.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>