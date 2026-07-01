## Summary

QUOKA proposes a training-free, hardware-agnostic sparse attention method for accelerating transformer inference under chunked prefill. The key observation is that queries with low cosine similarity to the mean query interact more broadly with keys, so QUOKA retains a small subset of such representative queries and then subselects KV pairs via cosine similarity scoring. Experiments across 4 benchmarks, 6+ model families, and 3 hardware platforms report near-baseline accuracy with 3–7× speedups.

## Strengths

1. **Clear motivation and well-targeted problem.** The paper correctly identifies that existing query-dependent sparse methods target the generation (single-query) setting and degrade under chunked prefill (multi-query). Sections 2.3–2.4 make this case convincingly with specific citations and a clear problem formulation.

2. **Novel core observation.** The finding that queries with low cosine similarity to the mean query attend more broadly to keys (Figure 2, correlation of 0.737 between \(S_q\) and \(\max_k(A)\)) is empirically grounded and leads to a distinctive, well-motivated design that differs from uniform-sampling alternatives like SampleAttention.

3. **Broad evaluation coverage.** The paper evaluates on 4 benchmarks (NIAH, RULER, LongBench, Math500), across 6+ model families (Llama3, Qwen2.5, Qwen3, SmollM3, GPT-OSS, Qwen3-30B-A3B), and on 3 hardware platforms (A100, RTX 2080, Intel Xeon CPU). This breadth is genuinely comprehensive for a sparse attention paper.

4. **Hardware diversity with meaningful CPU results.** The 5–7× CPU speedups (Figure 5c) are notable because most sparse attention methods rely on custom CUDA kernels and are NVIDIA-only. QUOKA's portability to CPUs and consumer GPUs is a real advantage.

5. **Strong empirical results on RULER.** In Table 1, at 32k length on Llama3.2-3B, QUOKA scores 57.01 versus the next-best method at 31.73. Across all models and lengths, QUOKA consistently leads by substantial margins.

## Weaknesses

### Fatal

None.

### Major

- **QUOKA reported as outperforming dense (full) attention on NIAH, Smollm3 on LongBench, and some Math500 cases without explanation.** Figure 4's caption states that Full attention shows "lower accuracy, especially at higher document lengths and needle depths" compared to QUOKA. Table 3 shows normalized scores of 1.03 and 1.028 for Smollm3 (i.e., 2.8–3% above the dense baseline). Section 4.4 states that QUOKA "surpasses the accuracy of dense attention in some cases." A sparse method that systematically beats the baseline that has strictly *more* information is anomalous. The dense baseline uses chunked prefill (B_CP=128), and it is possible that chunking itself degrades full attention — but the paper does not isolate or discuss this effect. Until this is resolved, the credibility of the primary quantitative comparisons is weakened.

### Minor

- **Theorem 1 has a notation issue and is decorative.** The theorem states a bound on \(\text{CosSim}(M_Q, q^*)\) but the premise defines a fixed query \(q_0\) without clarifying the relationship between \(q_0\) and \(q^*\) (lines 143–145). The bound itself (\(\text{CosSim}(M_Q, q^*) \leq 1 - 0.5(\alpha_q - \beta_q)^2\)) is not vacuous, but it is stated once in Section 3.1 and never referenced again — not in experiments, ablations, or discussion. It functions as decorative formalism that adds no actual support to the method.

- **No breakdown of QUOKA's own computational overhead.** Algorithm 1 involves computing the mean query, B_CP cosine similarities, a first top-k, query/key normalization, pre-aggregation across GQA groups, an \(N_Q \times T\) score matrix, max-pooling, and a second top-k. These operations have non-trivial cost. The reported net speedups (Figure 5) do not separate selection time from attention time, making it impossible to assess scalability, especially at shorter sequence lengths (e.g., 1k–4k tokens where speedup is ~1×).

- **Core observational claim demonstrated on limited data.** Figure 2 shows the correlation between \(S_q\) and \(\max_k(A)\) for only one layer (layer 0, head 11) of one model (Llama3.2-3B). While the observation is plausible, showing summary statistics across layers/heads would strengthen confidence that the central design premise generalizes.

### Trivial

None.

## Nice-to-Haves

- A breakdown of time spent in each step of Algorithm 1 vs. dense attention, for at least two sequence lengths (e.g., 5k and 30k).
- Results for the 1k–4k token regime, where selection overhead may dominate and speedup appears marginal.
- Code release to facilitate adoption and reproducibility.

## Removed Points

These points appeared in the input review but were removed with justification:

- **"Margin over baselines implausibly large with no evidence baselines were well-tuned."** The reviewer speculated that the large margins in Tables 1 and 3 might reflect suboptimal baseline configuration rather than genuine method superiority. However, the paper describes the baseline adaptation strategy (line 187–188: SampleAttention uniformly samples queries, SparQ and Loki down-project to 64 dimensions). Without specific evidence of misconfiguration, this is speculative and is removed.

- **"Theorem 1 is vacuous or incorrect (bound is trivially satisfied)."** The algebraic expansion shows RHS = \(1 - 0.5(\alpha_q - \beta_q)^2\), which IS tighter than the trivial bound of 1 (e.g., if \(\alpha_q=-0.5, \beta_q=0.5\), RHS = 0.5). The bound itself is mathematically valid, though the notation issue and decorative nature remain as kept weaknesses above.

- **Generic area-sweep concerns** (e.g., "could the metric be measuring a proxy?", "are confounders controlled?") that lack specific anchors in the paper are removed per filtering discipline.

## Novel Insights

None beyond the paper's own contributions. The input review does not surface a genuinely novel analytical angle that the paper itself does not already articulate.

## Suggestions

1. **Investigate and explain the dense-baseline anomaly.** If chunked prefill degrades full attention (e.g., through chunk-boundary effects on the causal mask or numerical precision), isolate and document this explicitly. If QUOKA genuinely compensates for chunking artifacts, provide supporting analysis. Without this, a central aspect of the quantitative evidence remains uninterpretable.

2. **Remove or substantially revise Theorem 1.** Either provide a bound that connects non-trivially to the subselection criterion and is actually used in the paper, or omit the formal theorem entirely and rely on the empirical evidence (which already provides the actual support for the method).

3. **Add an overhead breakdown.** A table or figure showing wall-clock time for each step of Algorithm 1 vs. the attention kernel would clarify where savings come from and help assess scaling behavior at diverse sequence lengths.

## Score and Decision

**Round 1 bracket (determined before final score): [5.0, 6.5]**

**Calibration anchors retrieved across all rounds** (path, avg human score, round, and how they compare):

| Anchor | Avg Score | Round | Comparison to QUOKA |
|--------|-----------|-------|---------------------|
| FlexPrefill | 8.00 | R1 | Stronger paper overall — cleaner evaluation, more rigorous baselines |
| OmniKV | 6.00 | R1 | Similar quality — narrower model/breadth evaluation but fewer unresolved concerns |
| Identify Critical KV | 5.75 | R1 | Similar ambition and has decorative theory issues too; similar score range |
| SwiftKV | 5.50 | R2 | Requires training; QUOKA is training-free and more broadly evaluated |
| ChunkKV | 5.25 | R1 | Weaker novelty — QUOKA has a more original core observation and broader hardware coverage |
| LazyLLM | 5.00 | R1 | Weaker overall — narrower evaluation, less novel method |
| Running Huge Context Windows | 4.67 | R2 | Less rigorous evaluation — QUOKA is clearly stronger |
| HShare | 6.80 | R2 | Stronger — cleaner experiments, fewer concerns |
| Radar | 6.60 | R2 | Stronger overall — theoretical justification, cleaner experiments |

QUOKA's core idea (query geometry for KV selection under chunked prefill) is genuinely novel and well-motivated. The evaluation breadth across models, benchmarks, and hardware is a real strength that places it above the 5.0-level papers. However, the unresolved dense-baseline anomaly — a sparse method outperforming full attention on multiple benchmarks without explanation — is a significant credibility concern that prevents a score in the accept (≥6.0) range. After calibration, 5.5 represents the midpoint of the plausible bracket, reflecting a paper with a solid core idea and broad evaluation but with evidence that is not fully trustworthy in its current form.

**Score: 5.5**
**Decision: Reject**

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>