Now I have solid calibration data. Let me write the final review.

## Summary

This paper presents QUOKA, a training-free and hardware-agnostic sparse attention method for chunked prefill in LLM inference. The core observation is that queries with low cosine similarity to the mean query interact more broadly with keys. QUOKA retains a small set of representative queries via this criterion, then subselects KVs via cosine-similarity scoring with a pre-aggregation trick for GQA. The method is evaluated on NIAH, RULER, LongBench, and Math500 across five model families (Llama3, Qwen3, SmollM, GPT-OSS) and three hardware platforms (A100, RTX 2080, Xeon CPU), consistently outperforming existing sparse attention methods by 10–20+ points while achieving up to 5× attention speedup.

## Strengths

- **Empirically motivated core observation (Figure 2).** The paper identifies that queries with low cosine similarity to the mean query attend more broadly to keys, validated with PCA projections and a 0.737 correlation between $S_q$ and $\max_k(A)$ (Figure 2c). This observation is concrete, falsifiable, and genuinely new — it is not a restatement of prior work and provides a principled basis for the method.

- **Clean, training-free design with genuine portability.** QUOKA relies only on standard linear algebra (cosine similarity, top-k gather) and is demonstrated on Nvidia A100, RTX 2080, and Intel Xeon CPU (Figure 5). This is a real advantage over kernel-level methods (e.g., MInference, Block-Sparse) that require custom CUDA primitives per hardware target.

- **Strong RULER results across diverse model families (Table 1).** QUOKA achieves 10–20+ point improvements over the best baseline (SampleAttn) across nearly all model/length combinations — e.g., 70.90 vs 48.31 on Llama3.2-3B at 16k, 88.57 vs 59.57 on Qwen3-4B at 16k. Evaluation spans five model families including MoE (Qwen3-30B-A3B) and NoPE variants, demonstrating broad applicability.

- **LongBench results showing minimal degradation (Table 3).** QUOKA achieves 0.945–0.995 normalized accuracy at budgets where baselines drop to 0.70–0.85, a meaningful improvement that holds across model families.

- **Pre-aggregation trick for GQA is computationally clever.** Averaging normalized queries across KV groups before the dot product (rather than averaging scores afterward) reduces scoring cost by the number of KV groups, which is non-trivial for models with large group ratios.

## Weaknesses

### Major

- **Theorem 1 does not deliver the claimed justification.** The theorem bounds $\text{CosSim}(M_Q, q^*)$ in terms of $\alpha_q = \text{CosSim}(M_Q, k)$ and $\beta_q = \text{CosSim}(k, q_0)$. However, the selection criterion $S_q = -\text{CosSim}(M_Q, q)$ depends only on the query and the mean query — not on any specific key $k$. The quantity $\alpha_q = \text{CosSim}(M_Q, k)$ is a property of the mean query and a key, not of an individual query $q$, and does not vary per query. Thus the theorem does not actually connect the selection criterion to the claim that selected queries attend broadly. The empirical evidence in Figure 2 is sufficient motivation; the theorem as presented adds formalistic language without substantive justification. The paper should either repair the theorem to state clearly what it proves and how it connects to the algorithm, or remove it and expand the empirical analysis.

- **Ambiguous labeling in Figure 4.** The figure includes a panel labeled "Full" alongside QUOKA and SampleAttention, with a caption specifying $B_{\text{SA}} = 2048$. If "Full" means dense (full) attention, a selective budget $B_{\text{SA}}$ should not apply; if it means "using all queries for scoring without query subselection" (a reasonable ablation), the label is misleading — especially since Table 2 uses "Full" to mean dense attention. The paper's main text (line 219) groups "Full" with selective attention methods without clarifying this. The ambiguity makes it impossible to interpret the NIAH comparison correctly. The authors must explicitly define "Full" in this context.

### Minor

- **Several accuracy values exceed the dense baseline without explanation.** In Table 3, QUOKA achieves normalized scores of 1.03 and 1.028 on Smollm3 (at $B_{\text{SA}} = 1024, 2048$), and the paper notes similar behavior on Math500 (Section 4.4). The paper mentions this in passing ("in some cases even surpasses the accuracy of dense attention") but offers no hypothesis (e.g., sparsity acting as a denoising mechanism, evaluation noise) and provides no variance estimates. Without error bars, the reader cannot assess whether these above-baseline values are meaningful or spurious. The paper should directly address this: are these within noise or is there a structural reason?

- **The "sub-quadratic complexity" claim is imprecise.** Line 131 states QUOKA "reduces prefill cost from $O(T^2)$ to a sub-quadratic complexity." However, the scoring step (Algorithm 1, lines 75–77) computes $\bar{Q}K^T$ for each chunk, where $K$ grows with the chunk index. Across all $T/B_{CP}$ chunks, the total scoring cost is $O(N_Q/B_{CP} \cdot T^2 \cdot d)$, which remains quadratic in $T$ with a small constant factor (~0.125 in typical settings with $N_Q=16, B_{CP}=128$). The attention itself becomes near-linear if $B_{SA}$ is constant. The paper should be precise: the method achieves near-linear attention at the cost of a heavily amortized $O(T^2)$ scoring step, not asymptotically sub-quadratic overall.

- **Loki baseline shows non-monotonic behavior.** In Table 3, Loki on Smollm3 achieves 0.384 at $B_{\text{SA}}=512$, 0.801 at $B_{\text{SA}}=1024$, and 0.622 at $B_{\text{SA}}=2048$. The drop from 1024 to 2048 budget is unexpected for a monotonic budget–accuracy relationship, suggesting either a bug or implementation issue with the Loki baseline. If a baseline implementation is unreliable, it compromises the comparison.

- **No error bars, confidence intervals, or multiple-run statistics** are reported for any result. Given that some values exceed the dense baseline, variance estimates are needed to assess robustness.

- **SnapKV and KeyDif appear in Table 1** but are not described in the baselines section (line 187). They perform very poorly (e.g., SnapKV scores 29.15 on 4k Llama3.2-3B vs. QUOKA's 86.71). Their inclusion without commentary on why they perform poorly in this setting makes the comparison table look more favorable to QUOKA.

- **No code release.** The reproducibility statement (lines 306–308) acknowledges this. For a methods paper at a major conference, code release is standard practice and would help verify and build upon the method.

### Trivial

- None beyond the items already listed as minor.

## Nice-to-Haves

- **Latency results on additional models.** The latency measurements (Section 4.6) are reported only for Qwen3-4B. Given the claim of generalization across architectures, measurements on at least one additional model (e.g., Llama3.2-3B) would strengthen the case.
- **Ablation of query subselection.** The paper ablates $N_Q$, $B_{SA}$, and $B_{CP}$ (Tables 11, 12 in appendix) but does not compare against a version of QUOKA without query subselection (using all queries for scoring). This would directly quantify how much the query subselection step contributes to accuracy vs. simply using more queries.
- **A breakdown of latency** showing time spent on scoring vs. attending would help assess whether the method's overhead is negligible at practical sequence lengths.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"Figure 4 shows Full attention underperforming QUOKA — this is either an error or undermines the paper's premise"** — REMOVED as fatally framed. The criticism assumes "Full" in Figure 4 means dense full attention, but the caption specifies $B_{\text{SA}}=2048$, which only applies to methods using KV selection. "Full" in this figure likely means "using all queries (no query subselection)" with the same KV budget. The labeling ambiguity is real (kept above as [Major]) but the fatal framing is based on a likely misinterpretation.
- **"Abstract/intro claim about pattern-based methods stated without evidence"** — REMOVED. This is standard positioning language, not a weakness requiring evidence.
- **"Section 3.2 cosine similarity analysis claim insufficient"** — REMOVED. The paper provides empirical support in appendix Table 9, which is reasonable.
- **"Missing GPT-OSS-20B entry in Table 1"** — REMOVED. Likely a parser artifact (the original PDF may render it).
- **"Theorem 1 is not logically wrong"** — Noted above as [Major] but reframed from the critic's fatal framing. The empirical evidence in Figure 2 stands on its own.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Clarify Figure 4:** Explicitly state what "Full" represents in the caption (e.g., "Full: using all queries for scoring without query subselection, with the same $B_{\text{SA}}=2048$ KV budget").
2. **Either substantively repair Theorem 1 or remove it:** If kept, the theorem must directly connect the selection criterion $-\text{CosSim}(M_Q, q)$ to attention output quality. If it cannot, remove it and expand the empirical analysis in Figure 2.
3. **Address above-baseline results directly:** Offer a hypothesis (e.g., sparsity filters out irrelevant context noise) and report variance estimates or multiple runs.
4. **Provide precise complexity analysis:** State the $O(N_Q/B_{CP} \cdot T^2)$ scoring cost explicitly and clarify under what conditions the overall method is sub-quadratic.
5. **Add error bars or multiple-run statistics** to the main tables (RULER, LongBench).
6. **Investigate the Loki non-monotonic values** and either fix or report with a note.

**Calibration round-1 bracket:** I examined anchors spanning 1.0–8.5. The most comparable papers were "Identify Critical KV Cache" (5.75, Reject), "OmniKV" (6.00, Accept), "Cascading KV Cache" (6.00, Accept), and "FlexPrefill" (8.00, Accept). QUOKA has stronger empirical scope than the 6.0 papers (5 model families vs. 1–2, larger improvement margins, demonstrated hardware portability) and a genuinely novel core observation. However, its presentation issues (Theorem 1 non-connection, Figure 4 ambiguity, imprecise complexity claim, absent variance, no code) are more numerous than the 6.0 anchors. FlexPrefill (8.0) is substantially cleaner in presentation and evaluation rigor. Placing QUOKA solidly in the 5.5–6.5 range, with the decisive factor being whether the presentation issues are fixable — they are — I assign **6.0**.

**Score and Decision**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>