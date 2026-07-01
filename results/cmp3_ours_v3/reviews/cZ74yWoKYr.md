Here is the final consolidated review.

## Summary

This paper formalizes critical KV cache selection from an output perturbation perspective. The authors derive an upper bound on attention output perturbation (Theorem 3.3) showing it depends on both attention weights and projected value states (VW^O), and propose a two-stage greedy algorithm that constrains worst-case perturbation. The algorithm integrates as a plug-and-play enhancement into existing cache eviction methods (SnapKV, AdaKV, HeadKV) and is evaluated across 3 LLMs and 29 datasets, achieving consistent and often substantial loss reductions (roughly halving compression loss on average).

## Strengths

1. **Clear formal framework that genuinely extends understanding.** The paper defines critical KV cache selection as output perturbation minimization (Definition 3.1), derives an upper bound (Theorem 3.3), and shows theoretically that this bound depends on both attention weights and projected value states VW^O. This is a genuine analytical contribution that identifies why attention-weight-only heuristics can miss important entries. The formal chain from Definition 3.1 through Theorem 3.3 to Algorithm 1 is logically structured.

2. **Large and consistent empirical gains across diverse settings.** On Ruler (Table 1), integrating the algorithm raises AdaKV on Mistral-7B from 34.88 to 69.17 at 40% cache — a ~34-point lift. On LongBench (Table 2), losses are roughly halved across most settings (e.g., AdaKV on Llama from 6.0% to 2.4% at 40% cache). Across 90 long-dependency test cases, improvements are observed in 88 (97.8%). These results hold across three LLMs (7B–32B), three base methods, and two cache sizes (20%, 40%).

3. **Informative α ablation that validates the two-stage design.** Table 4 shows that on Mistral, setting α=0 (pure value-weighted selection) causes a catastrophic drop from 42.85 to 31.94, while α=0.5 avoids this. On Llama, α=0 performs slightly better (44.35 vs 43.77). This asymmetry directly supports the authors' claim that stage 1 serves as a safeguard — it prevents pathological selections when value-weighted scores alone would violate the bound assumptions.

4. **Negligible computational overhead.** Figure 3 shows a TTFT increase of only 0.06s (batch 1) and 0.16s (batch 4), with the core extra computation being a single linear pass (|VW^O|). The decoding latency is identical to the base eviction methods and 2.5× faster than full cache.

## Weaknesses

### Fatal
None.

### Major
1. **Theory-practice gap: single-query formalism vs. observation-window implementation.** The theoretical development in Section 3 (Algorithm 1, Definition 3.1, Theorems 3.3, 3.5) assumes a concrete query q and computes A = softmax(qK^T). However, the practical deployment (Section 4.1, Algorithm 2) compresses the cache *before the question is seen*, using accumulated attention weights over an observation window (Q̂ = Q[-n':], Ā = A.mean(dim=0) + maxpooling). Algorithm 2 calls Algorithm 1 at line 8 but never specifies how — what query q is passed, or whether Ā replaces the internally computed A? If Ā is passed as "attention weights" to Algorithm 1, the internal softmax computation (line 2) would be redundant or incorrectly applied. If a single query from the window is used, the method does not leverage the accumulated signal that existing methods use. The paper contains no explanation of how the single-query Algorithm 1 is adapted to the observation-window setting where future queries are unknown. This does not invalidate the empirical results — the algorithm works — but it means the theoretical justification (Theorems 3.3, 3.5) does not directly apply to the actual deployment scenario, and the paper's narrative implying a direct correspondence is overclaimed.

### Minor
2. **No variance or confidence intervals.** Across all main results (Tables 1–4), only point estimates are reported. For smaller-margin improvements (e.g., HeadKV on Llama LongBench at 40%: 47.23→47.79, or several Single-Doc QA improvements in Table 1), it is not possible to assess robustness. Adding standard deviations or confidence intervals would substantially strengthen trust in the results.

3. **α pseudocode discrepancy.** Algorithm 1's input header (line 132) specifies α = 0.25, while the text (line 172) and all experiments (line 200) use α = 0.5. This is a clear mismatch that must be corrected.

4. **Limited SCBench evaluation.** Only AdaKV is tested, on 3 SCBench tasks (3 of 4,853 QA turns). Gains at 40% budget are modest in one case (Retr.KV: 19.40→19.80, a 2% relative improvement). The paper should more explicitly acknowledge this limited scope.

### Trivial
None.

## Nice-to-Haves
- A bound tightness analysis (the paper derives an upper bound θ but does not analyze how tight it is; the empirical validation in Section 4.7 partially addresses this, but a theoretical tightness discussion would strengthen the formal contribution).
- Specification of random seeds or precise sampling procedures for reproducibility.

## Removed Points
*(These points are flagged to be removed — treat them with caution.)*

1. **Harsh Critic mention of missing related work on perturbation-based analysis (Section 2).** This is not a concrete weakness against the paper — the paper already cites relevant work (Catformer, Admin, Wanda). The critic simply notes this is the "first analysis" for cache eviction, which is the paper's legitimate claim.

2. **"Bound tightness analysis" listed as a Missing Part.** The harsh critic raised this as a missing piece, but the empirical validation in Section 4.7 (92% and 86% head-level success rates) directly shows the bound-constrained algorithm reduces actual perturbation. This is a nice-to-have, not a weakness. Moved to Nice-to-Haves.

3. **"The integration with AdaKV/HeadKV budget allocation is not fully described."** Algorithm 2 line 1 shows budget allocation, and the text (Section 3.6) explains that "different budget allocation methods...all use the same underlying mechanism for KV cache selection." The description is adequate for the paper's scope. The harsh critic's concern that "the paper should clarify whether each head independently runs Algorithm 1" reflects a reading that is more granular than the paper needs to be at this level.

4. **"Reproducibility details — random seed"** mentioned as a Missing Part. This is a nice-to-have. The paper states 100 samples per Ruler task (line 204), which is a reasonable level of detail for a conference submission.

## Novel Insights

The most insightful observation from the reviews is that the theory-practice gap (single-query formalism vs. observation-window implementation) is a structural issue that the paper's narrative glosses over. The harsh critic correctly identified that the theoretical justification does not directly extend to the actual deployment scenario. All other synthesized points — the strength of the empirical results, the value of the α ablation, the need for variance reporting — are either directly stated in or straightforward extensions of the paper's own claims. None beyond the above.

## Suggestions
1. **Address the theory-practice gap explicitly.** Add a discussion explaining how Algorithm 1 is adapted to the observation-window setting. Options include: (a) showing that the accumulated Ā can be treated as a "smoothed query" that still satisfies the bound structure, (b) empirically comparing single-query selection (where the query is known) against observation-window selection to quantify the approximation cost, (c) analyzing whether the bound on perturbation for a single query also bounds an aggregate measure over the observation window. This would tighten the link between the formalism and the results and make the paper significantly stronger.
2. **Fix the α pseudocode** (0.25 → 0.5). This is a simple fix that affects credibility.
3. **Add variance reporting** (standard deviations or confidence intervals) to the main tables.

## Score and Decision

**Calibration anchors:**
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| lRTDMGYCpy (same paper, earlier version) | 5.75 | R1 | Previous version with 16 LongBench datasets, fewer baselines; current version is substantially expanded (29 datasets, Ruler, more baselines) |
| 4QWPCTLq20 (IntelLLM) | 3.00 | R1 | Weaker paper with unclear methodology, fewer baselines, no formal theory |
| 0ZcQhdyI3n (LSH-E) | 3.83 | R1 | Similar topic but weaker evaluation, missing key baselines |
| Q5VlpYRxGF (KVMerger) | 4.33 | R1 | KV cache merging paper, fewer baselines, less rigorous evaluation |
| FJFVmeXusW (Not All Heads Matter) | 6.50 | R1 | Accept-level KV cache paper with strong empirical results; comparable contribution level |
| EQgEMAD4kv (CAKE) | 7.00 | R1 | Accept-level paper with strong empirical results |

**Round 1 bracket:** 5.5–7.0 (the paper is clearly stronger than the previous version at 5.75, and comparable to accepted KV cache papers in the 6.5–7.0 range, but the theory-practice gap prevents it from reaching the 7+ tier).

**Reasoning for final score:** The paper represents a meaningful advance in KV cache selection with a novel theoretical framing and strong empirical results across 29 datasets, 3 models, and 3 base methods. However, the major theory-practice gap (single-query formalism not matching the observation-window implementation) is a significant issue that the paper does not address, and the α pseudocode error undermines presentation quality. Compared to accepted papers in this space (Not All Heads Matter at 6.5, CAKE at 7.0), the current paper has a stronger theoretical contribution but a more significant structural weakness. The previous version of this paper scored 5.75; the current expanded version merits a modest increase.

<score>6.0</score>
<decision>Accept</decision>