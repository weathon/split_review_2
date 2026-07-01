**Calibration Summary:**

**Retrieved anchors (all rounds):**

| Path | Avg Human Score | Round | Comparison |
|------|----------------|-------|------------|
| lRTDMGYCpy.md (same paper, prev. version) | 5.75 | R1 | Previous version scored 5,6,6,6 with decision Reject. Current version adds 13 more datasets (Ruler), SCBench multi-turn QA, better notation |
| 4QWPCTLq20.md (IntelLLM) | 3.00 | R1 | Much weaker; no theoretical contribution. This paper is clearly stronger |
| jZVNmDiU86.md (PyramidKV) | 5.60 | R1 | Similar topic. PyramidKV criticized for limited novelty and unimpressive results. This paper has stronger theoretical grounding |
| HMrcv7Q4Ub.md (VL-Cache) | 6.00 | R1 | Accepted paper in related area. Comparable quality but this paper has stronger theoretical contribution |
| OfjIlbelrT.md (FlexPrefill) | 8.00 | R1 | Stronger paper with dynamic sparse attention. Not directly comparable in scope |
| Other low-score anchors | 1.0–3.0 | R1 | Surveys, unrelated topics; not competitive |

**Round 1 bracket**: 5.5–7.5 (based on comparison with anchors)

**Narrowing**: The previous version of this paper scored 5.75 (borderline reject). The current version substantially strengthens the empirical evaluation (29 datasets vs 16, adds Ruler and SCBench) while retaining the same theoretical contribution. The paper is stronger than PyramidKV (5.60) and comparable to VL-Cache (6.00) with a better theoretical foundation, but has addressable reproducibility gaps that prevent it from reaching the 7.5+ tier occupied by substantially more polished papers like FlexPrefill (8.00). Final score: 6.5.

---

## Summary

This paper formalizes the problem of identifying critical KV cache entries for LLM inference from an output perturbation perspective. The authors derive an upper bound on attention output perturbation (Theorem 3.3) showing that both attention weights *and* projected value states matter. Based on this, they propose a two-stage perturbation-constrained selection algorithm (Algorithm 1) that is plug-and-play with existing cache eviction methods (SnapKV, AdaKV, HeadKV). Experiments on 29 datasets across three LLMs show consistent improvements, with the average compression loss reduction across all conditions being approximately 57.5%.

## Strengths

1. **Genuinely formal theoretical treatment of a previously heuristic problem.** The paper derives Theorem 3.3, an upper bound on L1 attention output perturbation that depends on both attention weights A_i and projected value states ‖V_i W^O‖_1. Prior work (H2O, Scissorhands, SnapKV, AdaKV, HeadKV) relies on the empirical observation that attention weights follow a power-law distribution; this paper shows *why* and in what sense attention weights alone are insufficient. This is a real theoretical advance.

2. **Clean theory-to-algorithm design.** The two-stage greedy selection (Section 3.4) connects directly to the theoretical bound: Stage 1 (attention-weight safeguard, α=0.5) ensures Assumption 3.4 holds (cumulative attention > 0.5), enabling Stage 2 to minimize the derived upper bound in Theorem 3.5 by jointly considering attention weights and projected value norms. The theory justifies the algorithm, not the other way around.

3. **Consistent and substantial empirical gains.** The method improves all three base methods (SnapKV, AdaKV, HeadKV) across all three LLMs on 29 datasets. The improvements are substantial: on Ruler at 40% cache (Table 1), average score gain is ~14.6 points; on LongBench at 40% (Table 2), loss is roughly halved on average. The 97.8% success rate across 90 long-dependency test cases further confirms consistency.

4. **Practicality with negligible overhead.** TTFT increases by only ~0.06s at batch size 1 (32K context), and decoding latency is unaffected (0.0332s, 2.49× speedup over full cache). The method requires only the pretrained output projection matrix W^O and a simple L1 norm computation per cache entry.

5. **Honest and informative α ablation (Section 4.5).** The finding that α=0 causes a catastrophic 10-point drop on Mistral but not Llama validates the theoretical need for the attention-weight safeguard in Assumption 3.4 and shows the paper is not cherry-picking results.

## Weaknesses

### Fatal
None.

### Major

1. **Underspecified integration with observation-window methods (reproducibility gap).** Algorithm 1 expects a single query state q to compute A = softmax(qK^T). However, in the "compression before question" setting (Section 4.1), the context is compressed independently before the question is introduced, and Algorithm 2 computes accumulated attention over an observation window (mean of softmax across multiple queries). Algorithm 2 (line 8) calls Algorithm 1 without specifying how the query state q is provided — whether it receives the accumulated attention weights Ā, the last query token, or something else. The paper states integration is "seamless" (line 190) but does not specify this critical mapping. This makes the exact procedure unreproducible from the paper alone.

### Minor

1. **Default α inconsistency between pseudocode and text.** Algorithm 1's header (line 132) lists default α = 0.25, while the text (lines 172, 200) states α = 0.5 is used throughout all experiments. Additionally, the pseudocode on line 5 checks "A_i ∈ Top_k(𝒜, b')" where 𝒜 is the product of attention weights and value norms, which conflates the Stage 1 criterion (which the text says should use attention weights alone). The text description is clear, so the intent is recoverable, but the pseudocode needs correction.

2. **No statistical uncertainty reported.** All results in Tables 1–3 and Figure 1 are point estimates with no standard deviations or confidence intervals. The Ruler benchmark runs 100 instances per task (Section 4.2), so variance estimation is feasible. Many per-task improvements are small (1–5 points), and without uncertainty quantification the reader cannot distinguish meaningful gains from noise. This is a common gap in the cache eviction literature, but addressing it would substantially strengthen the evidence.

3. **"More than half" claim would benefit from explicit computation.** The abstract claims the method "reduces the compression loss by more than half on average across 29 datasets." Computing the average reduction across all 18 model×method combinations (Figure 1 data) yields approximately 57.5%, which supports the claim. However, some individual cases show smaller reductions (e.g., SnapKV on Mistral Ruler: 20.4%; HeadKV on Llama LongBench: 28.3%). Showing the computation explicitly would be more precise than leaving the reader to verify.

4. **SCBench multi-turn evidence is thin.** Section 4.4 evaluates only AdaKV (not SnapKV or HeadKV) on only 3 tasks with no variance reported. Given the paper's claim of universal enhancement, showing at least one additional base method on SCBench would strengthen the multi-turn evidence.

### Trivial
- The theoretical bound in Theorem 3.3 is derived via triangle inequality and could be loose. The paper acknowledges this ("worst-case perturbation"), but a brief discussion of bound tightness would strengthen the theoretical contribution.
- Section 4.5 references "Table 5" but the table shown is labeled "Table 4."

## Nice-to-Haves
- Extending the SCBench evaluation to include SnapKV and HeadKV base methods.
- Adding a discussion of the tightness of the L1 upper bound in Theorem 3.3.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Harsh critic's "more than half claim is overstated"**: Removed from "Critical" and downgraded to Minor #3 because computing the average reduction across all conditions yields ~57.5%, which supports the claim. The reviewer's specific examples (SnapKV on Mistral at 20.4% reduction) are individual cases that do not contradict an average claim.
- **Harsh critic's section-by-section notes about bound tightness**: Kept only as a Trivial note, as it does not constitute a weakness.
- **Harsh critic's "the bound could be loose" without evidence of harm**: Moved to Trivial.

## Novel Insights

None beyond the paper's own contributions. The harsh reviewer raised an interesting tension: the theoretical framework is per-query (single q), but the SOTA methods operate with accumulated attention over an observation window. This gap between the clean single-query theory and the practical multi-query setting is not addressed in the paper and constitutes the primary reproducibility concern.

## Suggestions
1. **Fix the pseudocode** to match the text: set α=0.5 as default and cleanly separate the Stage 1 criterion (attention weights only) from Stage 2 (product criterion).
2. **Specify the integration with Algorithm 2** explicitly: state whether Algorithm 1 receives the accumulated attention Ā as its attention input, or whether a single query q is used.
3. **Add standard deviations or confidence intervals** to the main results tables, especially for Ruler where 100-instance sampling makes this straightforward.
4. **Show the "more than half" computation** explicitly: report the average reduction ratio across all conditions.
5. **Add at least one more base method** (SnapKV or HeadKV) to the SCBench evaluation.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>