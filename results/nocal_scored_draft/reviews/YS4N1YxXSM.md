Now let me write the final consolidated review.

## Summary

QUOKA proposes a training-free, hardware-agnostic sparse attention mechanism for chunked prefill in LLM inference. The key insight is that queries with low cosine similarity to the mean query interact broadly with many keys, while near-mean queries concentrate on a shared subset. By prioritizing low-cosine-similarity queries to score and subselect keys, QUOKA reduces the KV cache size before computing attention, using only standard linear algebra operations. The method is evaluated across 6 model families, 4 benchmarks, and 3 hardware platforms, showing consistent improvements over existing sparse-attention methods.

## Strengths

- **Genuinely interesting empirical observation (Section 3.1, Figure 2).** The paper identifies that queries with low cosine similarity to the mean query attend to a broader set of keys, while near-mean queries concentrate on a shared subset. This geometric property—supported by correlation analysis (r=0.737) and PCA visualization—provides a principled basis for query subselection that is not ad-hoc sparsity.

- **Training-free and hardware-agnostic design with concrete speedup measurements.** QUOKA uses only standard linear algebra, avoiding custom CUDA kernels. Speedups are demonstrated on Intel Xeon CPUs (up to 7×) and RTX 2080 GPUs (5–6×), validating portability with actual measurements across diverse hardware.

- **Consistently strong results against sparse-attention baselines on RULER and LongBench (Tables 1, 3).** On RULER with B_SA=1024, QUOKA outperforms the best competitor (SampleAttn) by 8–25 points across configurations. On LongBench, QUOKA's normalized accuracy at B_SA=512 often exceeds competitors at B_SA=2048.

- **Broad evaluation coverage** across 6 model families (including MoE and NoPE variants), 4 benchmarks, 3 hardware platforms, and multiple sparsity budgets, strengthening generality claims.

## Weaknesses

### Fatal
None.

### Major

- **RULER main results (Table 1, B_SA=1024) omit the full/dense attention baseline.** The paper claims "near-baseline accuracy" in the abstract and conclusion, but the primary accuracy table only pits QUOKA against other sparse methods. Cross-referencing with Table 2 (which uses a different, more generous 25% proportional budget) shows QUOKA at B_SA=1024 scoring 57.01 vs full attention at 76.31 on Llama3.2-3B at 32k—a ~25% relative gap. The degradation at long contexts with a fixed budget is predictable (a fixed B_SA becomes a smaller fraction of the cache) but is not discussed. The paper would be stronger if Table 1 included full attention and this tradeoff was characterized honestly.

- **NIAH results (Figure 4) show full/dense attention performing worse than QUOKA, which is anomalous and unexplained.** The figure caption confirms that "Full (c) show[s] lower accuracy, especially at higher document lengths and needle depths" compared to QUOKA. If dense attention—the gold standard—cannot reliably retrieve needles while QUOKA can, the evaluation either has a confound (e.g., chunked prefill interacting badly with full attention in a way that QUOKA's sparsity incidentally fixes) or this is a genuine finding worth highlighting. The paper offers neither explanation nor acknowledgment. This undermines confidence in the evaluation pipeline and should be addressed.

### Minor

- **LongBench normalized scores exceeding 1.0 (Table 3: Smollm3 shows 1.03 at B_SA=1024, 1.028 at B_SA=2048)** indicate QUOKA outperforming dense attention on average. While possibly attributable to noise or regularization effects, this phenomenon is not discussed and warrants explanation.

- **Theorem 1 provides an upper bound under specific assumptions** (a key k positively correlated with one query and negatively correlated with the mean query) but does not derive the paper's selection criterion (picking low-CosSim queries to M_Q). The connection between the bound and the method is asserted rather than proven. The paper's empirical evidence (Figure 2) is much stronger than the theoretical framing, which adds formality without substance. The paper could simply rely on the empirical observation.

- **Math500 results**, including the notable claim that QUOKA "surpasses the accuracy of dense attention," are relegated entirely to the appendix (Table 8). A reader of the main paper alone cannot verify this significant claim. Space constraints partly explain this, but the claim deserves visibility in the main text.

- **No measures of variance or statistical significance** are reported. Accuracy results (Tables 1–3) are point estimates with no indication of variability across runs or seeds. While single-run evaluation is common in this area, the paper's fine-grained accuracy comparisons (e.g., "10–20% higher") would be strengthened by error bars or variance statements.

### Trivial
None.

## Nice-to-Haves
- SnapKV and KeyDif perform far worse than in their original papers (Table 1, e.g., SnapKV scoring 6.21 at 32k on Llama3.2-3B). A brief discussion of whether chunked prefill is particularly hostile to these methods would be informative.

## Removed Points
These points are flagged to be removed; treat them with caution:
- **SnapKV/KeyDif poor performance not discussed**: Removed as a discussion enhancement, not a core weakness. The paper's focus is on demonstrating QUOKA's strengths.
- **"88% fewer key-value pairs" claim is vague**: Removed as trivial; the claim is contextualized by the method description and budget tables throughout the paper.
- **GPT-OSS-20B blank entry in Table 1**: Removed as speculative; could be a formatting artifact or a timed-out experiment.
- **LoLi/Loki naming inconsistency**: Removed as a minor typographical issue.

## Novel Insights
The most valuable insight from the reviews is that the paper systematically avoids placing the full-attention baseline alongside QUOKA in the same comparison table (Table 1), and the NIAH evaluation contains an anomaly where the reference method underperforms the proposed method—the combination suggests the paper's framing may be more favorable than the data supports in every dimension. This is a meta-observation about presentation strategy rather than a novel finding about the method itself.

## Suggestions
1. **Add a "Full Attention" row to Table 1** so readers can directly assess the "near-baseline" claim against the main sparse-attention comparison.
2. **Explain the NIAH anomaly** (Figure 4) where full attention underperforms QUOKA—either as a confound to correct or a genuine finding to discuss.
3. **Add a brief discussion** of the LongBench normalized scores exceeding 1.0.
4. **Include variance measures** (e.g., std over 3 seeds) for accuracy tables where fine-grained claims are made.
5. **Move Math500 numerical results** into the main paper or temper the "surpasses dense attention" claim in the abstract.

## Score and Decision

**Score: 6**

**Decision: Accept**

The core contribution—the geometric insight about query diversity and its use for query subselection in chunked prefill—is genuinely novel, well-motivated, and validated by strong empirical results against sparse-attention baselines across diverse settings. The method is clean, training-free, and hardware-agnostic. However, the paper systematically under-reports the comparison that matters most (QUOKA vs. full attention in Table 1), contains an unexplained anomaly where full attention underperforms QUOKA on NIAH (Figure 4), and does not discuss scores exceeding 1.0 on LongBench. These are evidential gaps and framing issues rather than fatal method flaws. The method itself is sound and the contributions are real; the paper needs to calibrate its claims and fill the missing comparisons before it can be endorsed more strongly.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>