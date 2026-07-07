Now I have enough to produce the draft review and calibrate. Let me draft it first.I found the same paper in the calibration set (earlier version). Let me compile the final review.

---

## Summary
This paper formalizes KV cache entry criticality in LLM inference as an output perturbation minimization problem. The key theoretical finding is that attention weights alone are insufficient—projected value state norms (||V_i W^O||_1) must jointly govern entry selection—formalized in Theorem 3.3 (Eq. 5) and Theorem 3.5. The authors propose a two-stage greedy algorithm (Algorithm 1) and demonstrate it as a plug-and-play enhancement to SnapKV, AdaKV, and HeadKV across 3 LLMs and 29 datasets.

## Strengths

- **Novel theoretical framing with actionable result (Section 3)**: The joint A_i × ||V_i W^O||_1 criticality criterion is non-obvious and theoretically derived. Theorem 3.5 shows that Stage 2 directly minimizes the perturbation upper bound (Eq. 6), connecting KV cache selection to Wanda-style perturbation analysis for pruning.

- **Unusually broad empirical validation (Tables 1–2, Figure 2, Table 3)**: Three model families (Llama-3.1-8B, Mistral-7B, Qwen2.5-32B), three integration targets (SnapKV, AdaKV, HeadKV), Ruler (13 tasks), LongBench (16 datasets), multi-turn SCBench, and multiple cache sizes (20–80%). This breadth makes the universality claim credible rather than cherry-picked.

- **Large, decisive gains on Ruler (Table 1)**: On Qwen2.5-32B at 40% cache, AdaKV's loss drops from 24.3% to 0.7%; HeadKV's from 13.7% to 3.4%. On Llama-3.1-8B with HeadKV, loss drops from 12.2% to 1.9%. These are qualitative improvements, not marginal ones.

- **Mechanistic validation closes the loop (Section 4.7, Figures 4–6)**: The paper directly validates that the algorithm reduces head-wise L1 perturbation in 92%/86% of heads for Llama/Mistral, and that reductions accumulate across layers. This explains *why* the algorithm works, not just that it does.

- **Practical overhead correctly quantified (Section 4.6, Figure 3)**: TTFT increases by only 0.06s per request at 32K context; decoding speedup is unchanged from the base method. This is precisely what practitioners need to evaluate deployability.

## Weaknesses

### Fatal
None.

### Major

- **Algorithm 1 pseudocode ambiguity undermines the two-stage theoretical argument**: In the pseudocode, Line 2 computes `A = softmax(qK^T)` and Line 3 appears to overwrite `A` with the joint score `(A+ε) ⊙ (L1 norms of V rows)`. Both Stage 1 (Line 5: `A_i ∈ Top_k(A, b')`) and Stage 2 (Line 8: `A_i ∈ Top_k(A, b'')`) then index the same variable. If both stages use the joint score, Stage 1 no longer guarantees the cumulative attention weight σ > 0.5 required by Assumption 3.4, and Theorem 3.5's bound may not follow.

  The Table 4 ablation provides indirect evidence that the pseudocode is misleading rather than the implementation being wrong: setting α=0 (Stage 1 selects nothing, Stage 2 selects all b by joint score) causes Mistral to collapse from 42.85 to 31.94—well below even the base AdaKV of 41.18. If both stages already used joint scores at α>0, the combined result would reduce to "select top-b by joint score" and α=0 should behave identically. The fact that it doesn't proves Stage 1 actually uses raw attention weights. This is most likely a rendering artifact where distinct typographic symbols (𝒜 for joint score vs A for attention weights) are conflated by the parser—but as presented, readers cannot reproduce the algorithm unambiguously. The algorithm box needs distinct variable names distinguishing raw attention weights from the joint score.

### Minor

- **Direct α inconsistency**: Algorithm 1's header (Line 132) specifies `α = 0.25` as the default, but Section 3.5 and Section 4.1 both state `α = 0.5` for all theory and experiments. These cannot both be correct; one must be wrong.

- **"More than half" headline overstated for individual results**: The abstract claims compression loss is reduced "more than half on average." This holds in aggregate (Figure 1), but individual cases fall short—e.g., HeadKV on Llama-3.1-8B LongBench: 4.00% → 2.87% (28% relative reduction). The claim is accurate in the aggregate sense but should be more carefully scoped.

### Trivial

- The 8–14% of attention heads where the algorithm does *not* reduce perturbation (Figure 4) is not acknowledged. A brief note would strengthen the mechanistic account and set accurate expectations.

## Nice-to-Haves
- Analysis of which heads/layers are in the 8–14% that resist perturbation reduction — do they correspond to sparser attention patterns, specific layers, or atypical value norm distributions?
- Explanation of *why* pure joint-score selection without the attention-weight floor (α=0) fails specifically on Mistral (Table 4) while succeeding on Llama — this likely reveals something important about attention pattern structure across architectures.
- SCBench evaluation with SnapKV and HeadKV in addition to AdaKV, to maintain consistency with the main experimental design.

## Removed Points
*These points are flagged to be removed, treat them with caution.*

- **Theorem 3.3 bound tightness**: The reviewer speculates the bound may be too loose. This is not anchored to a specific flaw—the bound's purpose is to enable tractable optimization, not to be tight. Empirical validation in Section 4.7 (92%/86% improvement rates) provides adequate support. *Removed as speculative.*

- **Compression scenario comparability**: The "context compressed before question" setting (Section 4.1) is noted as limiting comparability with prior work. The paper explicitly justifies this as the more realistic setting and provides the alternative in Appendix F. *Removed as adequately addressed.*

- **SCBench statistical noise for Math.Find**: Small absolute scores (11–17/100) over 6 turns raise noise concerns. But the directional results are consistent across all budget levels, and the paper doesn't overclaim here. *Removed as insufficiently grounded.*

- **Strength: "First formal study of KV cache criticality"**: The paper's abstract and introduction claim novelty in formalization. While the *combination* of perturbation bounding and selection is novel, the individual components are incremental. *Weakened to note this is a genuine theoretical contribution, but not the first perturbation-based analysis in neural network compression.*

## Novel Insights
The paper's most genuinely novel contribution is identifying that the product A_i × ||V_i W^O||_1 is the correct criticality metric for KV cache entries—not attention weights alone. This formally explains why attention-only heuristics fail: high-norm entries that receive moderate attention can dominate the output perturbation more than high-attention, low-norm entries. The connection to Wanda-style weight pruning analysis suggests a broader paradigm: output-perturbation-guided selection applies uniformly across neural network compression problems, and future work should explore perturbation-based selection for other architectural components (e.g., attention heads, layers).

## Suggestions
- **Revise Algorithm 1** to use distinct variable names: store raw attention weights in `A`, compute joint scores in `𝒜 = (A+ε) ⊙ (L1 norms)`, and explicitly use `A` in Stage 1's Top-K condition and `𝒜` in Stage 2's. This single fix resolves the pseudocode ambiguity and makes the algorithm unambiguously reproducible.
- **Correct α in the algorithm header** from 0.25 to 0.5, or justify why the header value differs from the experimental default.
- **Add one sentence in Section 4.7** acknowledging the 8–14% of heads where perturbation is not reduced, noting whether these correspond to particular model components.

---

## Score and Decision

**Calibration anchors:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| lRTDMGYCpy.md | 5.75 | R1 | Same paper, earlier version — only LongBench (16 datasets), no Ruler, 2 models, no SCBench; Rejected |
| 0ZcQhdyI3n.md (LSH-E) | 3.83 | R1 | KV cache compression via LSH; weaker theory, narrower evaluation than this paper |
| tcq7n0m7Ml.md (EMS) | 4.60 | R1 | Head-wise KV eviction with evict-then-merge; similar scope, weaker theoretical grounding |
| QlvL6eEOC6.md | 4.50 | R1 | KV prediction auxiliary model; different approach, weaker empirics |
| p7vJ3wsm34.md (KV-Distill) | 4.00 | R1 | KV cache distillation requiring fine-tuning; narrower than this plug-and-play method |
| FJFVmeXusW.md (HeadKV) | 6.50 | R1 | Head-level KV compression (one of this paper's baselines); this paper substantially outperforms it as a meta-algorithm |
| OfjIlbelrT.md (FlexPrefill) | 8.00 | R1 | Flexible sparse attention, well-executed systems paper; broader and more polished than this paper |

**Round 1 bracket**: The earlier version of this paper received 5.75 and was rejected. The current version substantially expands the earlier work: adds the Ruler benchmark (13 tasks, where gains are decisive), a third model (Qwen2.5-32B, 32B scale), SCBench multi-turn evaluation, and detailed perturbation analysis. These additions address the earlier reviewers' primary concerns (insufficient evaluation, only 7B models, missing Ruler-like tasks). The main remaining issue is the pseudocode ambiguity (presentation, fixable) and the α inconsistency (trivial). Initial bracket: **5.5–7.0**.

**Narrowing**: Relative to HeadKV (6.50, Accept, one of this paper's baselines), the current paper makes a stronger and broader contribution—it's a theoretically grounded meta-algorithm that consistently improves HeadKV, SnapKV, and AdaKV with decisive gains. Relative to FlexPrefill (8.0), this paper is less polished (pseudocode ambiguity remains) and more narrowly focused on a single component. The pseudocode ambiguity is presentation-level and does not undermine empirical results. Settling on **6.5**.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>