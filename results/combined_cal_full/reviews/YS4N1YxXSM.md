## Summary

QUOKA proposes a training-free, hardware-agnostic sparse attention method specifically designed for the *chunked prefill* stage of LLM inference. The key insight — that queries with low cosine similarity to the mean query contribute most strongly to the attention distribution — is operationalized through three steps: query subselection (retaining the most informative queries), cosine-similarity scoring, and group-aware aggregation. Tested across 5 model families, 4 benchmarks (RULER, LongBench, NIAH, Math500), and 3 hardware platforms (A100, RTX 2080, Xeon CPU), QUOKA consistently outperforms competing sparse attention methods (SampleAttn, SparQ, Loki, LessIsMore) by large margins (10–20+ points on RULER, 10–20% on LongBench) while achieving meaningful speedups (3× TTFT, 5× attention on GPU, 7× on CPU).

## Strengths

- **Clear problem identification with strong empirical grounding.** The paper correctly identifies that extending generation-time KV selection to multiple queries (as in prefill) by naively averaging over queries degrades performance. The core observation (Figure 2) provides clear evidence: (a) attention maps show structured sparsity, (b) queries with high $S_q$ lie closer to keys in PCA space, and (c) there is a 0.737 correlation between $S_q$ and $\max_k(A)$. The query-subselection mechanism is a natural operationalization of this observation. (Sections 1–2, Figure 2)

- **Strong, consistent empirical results across extensive evaluations.** On RULER (Table 1), QUOKA outperforms the next-best baseline by 10–20+ points across nearly every model and sequence length. On LongBench (Table 3), QUOKA achieves relative scores of 0.94–1.03 vs. dense attention, while the best baseline (SampleAttn) reaches only 0.74–0.97. These gaps are large enough not to be attributable to implementation noise. The evaluation covers 5 model families (Llama3, Qwen3, SmollM, GPT-OSS, Qwen3-30B-MoE) with diverse architectures (RoPE, NoPE, MoE).

- **Hardware-agnostic design is a genuine practical advantage.** Unlike kernel-level sparse attention methods that require custom CUDA kernels, QUOKA uses standard linear algebra primitives, enabling deployment on CPUs, consumer GPUs, and edge devices without reimplementation. The CPU and RTX 2080 latency results (Figures 5c, 5d) concretely validate that this design choice translates to real speedups (5–6× on consumer hardware).

- **Method is clean, well-structured, and easy to implement.** The three-stage design (query subselection → cosine-similarity scoring → group-aware aggregation) is clearly described in Algorithm 1. The pre-aggregation trick for GQA (averaging normalized queries before computing the score) is an elegant efficiency optimization. The paper is explicit about hyperparameters and design choices.

## Weaknesses

### Fatal
None.

### Major

- **QUOKA exceeding dense full attention on accuracy is acknowledged but not explained, undermining evaluation interpretability.** In Table 3 (LongBench), QUOKA achieves relative scores of **1.03** and **1.028** on Smollm3 at $B_{\text{SA}} = 1024$ and $2048$ — i.e., *surpassing* the dense full-attention baseline. The paper acknowledges this briefly (Sections 4.4, 6) with "in some cases even surpasses the accuracy of dense attention" but provides no analysis of why. Reasonable hypotheses include: chunked-prefill artifacts degrading the dense baseline, the sparsity acting as a beneficial regularizer, or numerical differences from the dimensionality reduction. Without disambiguation, it is difficult to interpret whether the comparison measures "preserving accuracy" or "winning due to an artifact." This is especially relevant because the paper's framing claims "near-baseline accuracy" — if the baseline is not a clean upper bound, that claim becomes ambiguous. This issue should be addressed in the main text, not relegated to a footnote.

### Minor

- **The theoretical justification (Theorem 1) is not coherent as stated.** The symbol $q^*$ appears in the theorem statement (Eq. 5) and in the definition $S_q = -\text{CosSim}(M_Q, q^*)$ but is **never defined**. The theorem's premise involves $q_0$, not $q^*$, and there is no stated relationship between them. The bound itself may be correct (the proof is in the appendix), but in the main text it does not clearly connect to the claimed conclusion. The empirical evidence in Figure 2 is sufficient motivation on its own; the theorem as presented adds confusion rather than clarity and should be rewritten or moved to the appendix.

- **A data point is missing from the primary RULER results table (Table 1).** The QUOKA column for GPT-OSS-20B at 32k sequence length is empty — the only empty cell in the table. It is unclear whether the experiment was not run, failed, or produced a result that was excluded. A primary results table should not have missing entries without explanation.

### Trivial

- **No variance or confidence reporting for any accuracy benchmark.** For latency, the paper properly states "each data point is averaged over 100 trials." For all accuracy benchmarks (RULER, LongBench, NIAH, Math500), there are no standard deviations, confidence intervals, or indication of how many runs were averaged. Given the large margins over baselines, the results are likely robust, but the paper should at minimum state this explicitly.

## Nice-to-Haves

- Provide exact speedup numbers in a small table (e.g., at 10k, 30k, 50k tokens) rather than only in figures, so readers can verify the headline 3×/5×/7× claims from the abstract without reading figures.
- The ablation of $N_Q$ (query-subselection budget) reportedly shows only ~3% accuracy drop even at $N_Q = \frac{1}{16} B_{\text{CP}}$ (Table 12, appendix). This is interesting and deserves more prominence in the main text, since query subselection is the most novel component.
- A brief discussion of whether baseline hyperparameters were re-tuned for the prefill setting (rather than using generation-optimized defaults) would address a natural fairness concern.

## Removed Points

These points from the input review are excluded with justification:
- *Criticism that the claim "prior work generally focused on generation phase" is overstated:* The paper itself acknowledges recent work targeting prefill ("While recent work…attempt to address this," line 121). This is already addressed in the paper.
- *Question about whether SparQ, Loki, etc. were run for NIAH:* The paper references Figure 7 in the appendix for those results. The concern is speculative given the stripped appendix.
- *Assessment that "Math500 section reads as an afterthought":* Subjective assessment, not a verifiable weakness.
- *Formatting/style nitpicks:* parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions. The reviewer observations about the Theorem 1 incoherence and the unexplained >1.0 baseline issue are valid critiques that the authors can readily address, but they do not constitute independent discoveries.

## Suggestions

1. **Explain the >1.0 baseline result.** Dedicate a paragraph (or a brief subsection) to analyzing why QUOKA occasionally exceeds dense full attention. The most productive approach would be to compare against a non-chunked dense baseline to isolate whether chunking artifacts are responsible.
2. **Clarify or remove Theorem 1 from the main text.** If kept, define $q^*$ explicitly and state the relationship between $q_0$ and $q^*$. Alternatively, treat the method as empirically motivated (Figure 2 is sufficient) and move the theorem to the appendix.
3. **Provide the missing GPT-OSS-20B 32k data point** or explain its absence.
4. **Add a brief variance statement** for accuracy results, e.g., "all results are single-run; margins over baselines are large enough that variance does not affect conclusions."
5. **Report headline speedup numbers in a table** to complement Figure 5.

## Score and Decision

**Calibration anchors used:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| OfjIlbelrT.md (FlexPrefill) | 8.00 | R1 | Yes | Most directly comparable: sparse attention for prefill. QUOKA has stronger empirical margins but the unexplained >1.0 baseline issue keeps it below this anchor. |
| 4QWPCTLq20.md (IntelLLM) | 3.00 | R1 | Yes | KV cache compression with weaker evaluation and unclear writing. QUOKA is substantially stronger. |
| am5Z8dXoaV.md (LazyLLM) | 5.00 | R1 | Yes | Dynamic token pruning for TTFT with baseline comparison gaps. QUOKA has broader evaluation and cleaner methodology. |
| pG820nmDvy.md (Running Huge Context Windows) | 4.67 | R1 | Yes | Top-k sparse attention lacking latency benchmarks. QUOKA is more rigorous. |
| PTcMzQgKmn.md (HiP) | 6.25 | R2 | Yes | Training-free sparse attention with thorough complexity analysis but limited model scope. QUOKA has stronger empirical breadth. |
| Tb5PY5vwp6.md (HShare) | 6.80 | R2 | Yes | KV cache sharing with comprehensive evaluation. QUOKA's method is cleaner and more original. |

**Round 1 bracket:** 6.5–7.5

**Weighted-item comparison:** The strongest positive weights in my draft are the empirical results (+6.34) and the empirically grounded observation (+5.59), both of which are shared with strong anchors like FlexPrefill (8.0) and HiP (6.25). The key negative weights are the >1.0 baseline issue (−2.69) and the unclear Theorem 1 (−3.15). Compared to FlexPrefill (8.0), whose negatives included −4.76 and −4.48 from missing baselines and methodology gaps, QUOKA's negatives are less severe in magnitude but the >1.0 issue is conceptually more central. Compared to HiP (6.25), whose negatives were mostly small positive weights (suggestions), QUOKA's negatives are stronger but its strengths (especially empirical breadth) are also stronger. The balance places QUOKA above HiP (6.25) and HShare (6.80) but below FlexPrefill (8.0), converging to 7.0.

This is a strong paper with a clean, well-motivated method and comprehensive evaluations. The main issues requiring attention are the unexplained >1.0 baseline results and the unclear Theorem 1. Neither undermines the core contribution, but both reduce the polish. I recommend acceptance conditional on the authors explaining the >1.0 baseline behavior in the final version.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>