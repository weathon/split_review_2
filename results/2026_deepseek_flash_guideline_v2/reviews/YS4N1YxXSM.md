I cannot access the calibration corpus. Proceeding without calibration anchors and scoring based on my own judgment of the paper.

## Summary

QUOKA proposes a training-free, hardware-agnostic sparse attention method for chunked prefill. Its key insight is that queries with low cosine similarity to the mean query contribute most to attention, so it first selects a small set of representative queries by cosine dissimilarity from the mean query, then subselects keys via cosine similarity to those queries. The method is validated across six model families (including MoE and NoPE variants) on RULER, LongBench, NIAH, and Math500, consistently outperforming five competing sparse attention methods by large margins.

## Strengths

- **Consistent and large accuracy margins over baselines on RULER (Table 1).** QUOKA outperforms all five competing methods (SnapKV, KeyDif, LessIsMore, LoLi, SparQ, SampleAttn) across five model families at 4k–32k sequence lengths. The gaps are not incremental: on Llama3.2-3B at 16k, QUOKA scores 70.90 vs. the next-best method (SparQ) at 48.59. On Qwen3-4B at 32k, QUOKA scores 74.83 vs. SampleAttn at 40.72. These margins directly support the claim that query-oriented subselection preserves accuracy under sparsity better than prior approaches.

- **Near-baseline accuracy at a constant 25% compression ratio (Table 2).** When the selective budget scales dynamically with context (25% of cache length), QUOKA incurs ≤3-point accuracy drop on RULER across all five model families at all sequence lengths. On Qwen3-30B-A3B (MoE) at 32k: 91.08 vs. full-attention 91.87 (0.79 drop). This is stronger evidence than a fixed-budget experiment because it demonstrates graceful scaling with context.

- **Hardware portability validated across three device classes (Figure 5).** QUOKA achieves the highest relative attention speedup on an NVIDIA A100 (enterprise GPU), an NVIDIA RTX 2080 (consumer GPU), and an Intel Xeon CPU. Most competing methods (e.g., those relying on custom CUDA kernels) cannot run on CPUs. This directly supports the hardware-agnosticism claim and the design choice of building on standard linear algebra operations.

- **Clean pre-aggregation trick for GQA compatibility (Section 3.3).** Because mean and outer-product commute, averaging normalized queries across KV groups can be done *before* computing the score matrix, reducing memory and computation by a factor equal to the number of KV groups. This explains why QUOKA avoids overhead from multi-head attention and is empirically supported by ablations.

- **Architecture coverage beyond the usual scope.** The method is evaluated on six model families covering RoPE (Llama3, Qwen2.5), NoPE (SmollM3), and MoE (Qwen3-30B-A3B). Few sparse attention papers test on MoE or NoPE models, and the consistent results support generalization of the geometric observation.

## Weaknesses

### Major

- **Latency measurements lack the selective budget B_SA (Section 4.6).** The speedup claims ("5× attention speedup", "3× TTFT reduction") are reported without stating which B_SA was used. Since accuracy results (Tables 1–3) use specific B_SA values (512, 1024, 2048), the reader cannot determine whether the speedup was measured at the same budget that produced near-baseline accuracy or at a more aggressive setting. The paper must explicitly state the B_SA used in the latency experiments, ideally for each sequence length, and preferably report speedups at multiple budget levels to show the accuracy–latency Pareto frontier.

### Minor

- **Theorem 1 uses an undefined variable q^*.** The theorem states a bound on CosSim(M_Q, q^*) and defines S_q = -CosSim(M_Q, q^*), but q^* is never introduced. From context it should be q (the query under consideration), but the notation error makes the theorem mathematically incoherent as written. This matters because the theorem is presented as the "formal justification" for query subselection. However, the empirical evidence (Figures 2b, 2c) independently supports the design choice, so this is a presentation failure rather than a fatal methodological flaw. The authors should either fix the notation or replace the theorem with a clear geometric/empirical statement.

- **QUOKA exceeds the dense baseline on LongBench for Smollm3 without explanation (Table 3).** Normalized scores of 1.03 (B_SA=1024) and 1.028 (B_SA=2048) mean sparse attention with ~6–12% of KVs outperforms full attention. The paper mentions this only in passing ("in some cases even surpasses the accuracy of dense attention"). This could be a genuine regularization effect or an evaluation artifact (e.g., the dense baseline is implemented suboptimally for this model, or benchmark noise). Either way, it deserves a brief discussion — not because it undermines the method, but because it is an unusual and interesting finding that readers will question.

- **The GPT-OSS-20B column in Table 1 has an empty cell for QUOKA at 32k.** All other methods have values filled for this cell. If the experiment OOM'd or was not run, this should be explicitly footnoted. As presented, it looks like a data omission.

### Trivial

- No confidence intervals or error bars for accuracy benchmarks. While standard practice for LLM benchmarks of this type, adding them where feasible would improve rigor. The latency measurements are "averaged over 100 trials" but no variance is reported.

- The "88% fewer key-value pairs" claim in the abstract is stated without tying it to a specific B_SA/T ratio or model; it is clarified later (Section 4.5 reports "less than 12% of original tokens") but stating the budget up front would help.

## Nice-to-Haves

- Quantify the overhead of the subselection step separately from the attention kernel latency. This would clarify where the speedup comes from.
- Report speedups at multiple B_SA values for a given sequence length to show the accuracy–latency trade-off explicitly.
- Add a brief discussion of why QUOKA sometimes exceeds dense attention on LongBench for Smollm3.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Harsh critic: "Theorem 1 is circular reasoning."** The theorem is notationally broken but not circular. The empirical evidence (Figures 2b, 2c) stands independently of the theorem. The paper's argument does not collapse without the theorem. (Removed — overstatement.)

- **Harsh critic: mean(Q, dim=2) dimension ambiguity.** The shapes in Algorithm 1 (lines 83–84) show Q has shape (b, n_Q, N_Q, d); dim=2 is the sequence/chunk dimension, which is correct for computing the mean query. (Removed — factually incorrect critique.)

- **Harsh critic: "Subselection overhead not separately quantified."** This is a nice-to-have breakdown, not a weakness. The paper reports end-to-end speedups which inherently include overhead. (Demoted to nice-to-have.)

- **Strength Finder: Generic praise about "importance of the problem" or "this paper addresses an important topic."** These are generic and do not specifically support the paper's contribution. (Removed.)

- **Harsh critic: "No error bars" as a major issue.** This is standard for LLM benchmarks; demoted to trivial. (Demoted.)

## Novel Insights

The most revealing observation from the review process is the structure of the paper's evidence: the strongest support for the method (Table 1's decisive RULER margins) comes from the full method — query subselection + cosine similarity scoring + max aggregation — not from Theorem 1, which is presented as the formal justification but is notationally broken. The geometric intuition and empirical correlations (Figures 2b, 2c) are independently convincing; the PCA visualization showing that high-S_q queries lie closer to the key cluster is the real evidence. If the authors fix or drop the theorem and lean on these empirical observations, the paper's argument would be cleaner and equally strong.

## Suggestions

1. **State B_SA for latency experiments explicitly** in Section 4.6, ideally for each sequence length, and report latency at multiple budget settings to connect speedup to accuracy.
2. **Fix the undefined q^* in Theorem 1** (replace with q or q_0) or replace the theorem with a clear geometric argument supported by Figures 2b/2c.
3. **Footnote the empty GPT-OSS-20B cell** in Table 1 (OOM / not run).
4. **Add a sentence discussing the >1.0 normalized accuracy** on LongBench for Smollm3 — is it within noise, a regularization effect, or an implementation detail?
5. **Clarify in the abstract** the specific B_SA/T ratio or compression percentage that yields the "88% fewer" claim.

## Score and Decision

This is a solid method paper with a clean idea, strong empirical validation across multiple benchmarks, models, and hardware platforms, and decisive accuracy advantages over competing sparse attention methods. The weaknesses are presentation-level, not methodological. The missing B_SA in the latency section is the most impactful issue and must be addressed, but it is easily fixable. The notational error in Theorem 1 does not affect the validity of the empirical results.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>