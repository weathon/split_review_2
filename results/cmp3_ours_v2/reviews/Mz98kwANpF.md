## Summary

This paper revisits multi-task learning with LoRA, challenging the dominant trend toward multi-component architectures (multi-adapter/multi-head designs with routing). It presents three contributions: (1) showing that a simplified multi-head variant (M-LoRA) with high inter-head similarity outperforms diversity-enforcing variants like R-LoRA; (2) demonstrating that a high-rank single LoRA is competitive with multi-component architectures; and (3) proposing Align-LoRA, which augments a single LoRA with KL-based representation alignment and achieves strong results with zero inference overhead.

## Strengths

- **Empirical challenge to the diversity assumption (Sections 3–4).** The finding that M-LoRA — which removes the router and sums heads — achieves higher inter-head similarity yet better performance than R-LoRA (Table 1, Figure 2) directly contradicts the prevailing assumption that head diversity is necessary. This is a concrete, reproducible counterexample to an established trend.

- **Rank-scaling experiment (Section 4, Tables 2–3).** Showing that a standard single-adapter LoRA with rank scaled to match the parameter budget of multi-component designs is competitive (and occasionally superior — e.g., Qwen2.5-14B: LoRA rank=10 at 54.23 vs M-LoRA at 54.18) is a clean and persuasive result that questions whether multi-component architectures provide benefits beyond additional parameters.

- **Align-LoRA is simple, principled, and adds zero inference overhead (Section 5.1).** The method applies KL-based alignment to the down-projection A's output and, unlike multi-component variants, can be merged into the backbone. Results in Tables 4–5 show meaningful gains (e.g., Qwen2.5-7B BBH: A-LoRA-K 50.28 vs LoRA rank=10 at 48.36) with fewer parameters.

- **Well-structured narrative.** The paper is clearly written, and the arc from "challenge an assumption" → "isolate the simplest case" → "propose a method" is effective.

## Weaknesses

### Major

1. **Factually incorrect claim about the MMD variant's performance (Table 4, line 225).** The paper states "both A-LoRA-K and A-LoRA-M significantly outperform the baselines" when describing Table 4. However, A-LoRA-M underperforms the simple LoRA baseline on 2 of 3 model scales in that table (Qwen2.5-7B: 47.53 vs 48.36; Qwen2.5-14B: 52.24 vs 52.93). The paper neither acknowledges this underperformance nor discusses why MMD alignment hurts in these settings. This undermines the claim that "the principle of aligning representations is broadly applicable and not contingent on a single metric" and leaves a significant explanatory gap. The paper's assertion that both KL and MMD alignment "elevate performance above the standard LoRA baseline" (line 251) is contradicted by the paper's own data.

2. **No statistical significance or variance reported for any result.** None of the five tables include error bars, standard deviations, or any indication of run-to-run variance. This is a serious omission for an empirical paper where several key comparisons involve small differences (e.g., Table 1: M-LoRA 75.45 vs R-LoRA 74.67 = 0.78 gap; Table 2 LLaMA2-7B: LoRA† 42.21 vs R-LoRA 42.24 are essentially tied). Without knowing whether these differences are stable across random seeds, the reliability of the conclusions — especially the central claim that simplified architectures "significantly outperform" complex ones — cannot be assessed.

3. **The effect of alignment is not isolated from rank.** Table 4 compares A-LoRA-K (rank=8) against LoRA (rank=10), conflating the alignment loss with a rank difference. A LoRA rank=8 baseline is not provided, so the reader cannot determine how much of A-LoRA-K's gain comes from representation alignment versus from a different rank/hyperparameter combination. A clean head-to-head (LoRA rank=8 vs A-LoRA-K rank=8) is needed to isolate the effect.

4. **The theoretical analysis (Section 5.3) is generic and overclaims novelty.** The generalization bound presented is a standard multi-task/domain adaptation bound (closely resembling Ben-David et al., 2006) that contains no LoRA-specific structure, no rank dependence, and no dependence on Align-LoRA's specific design choices (Gaussian modeling, KL on down-projection output). The paper calls this "a novel generalization bound" (line 255), but the bound would apply identically to any MTL method that reduces distribution discrepancy. While a connection is stated via the Δ(Dᵢ, Dⱼ) term, no chain of reasoning links the empirical KL/MMD alignment loss to a reduction in true distribution discrepancy. This section should be removed or replaced with method-specific analysis.

### Minor

5. **The claim that "multi-head dropout is the critical factor" (line 113) is not fully supported by the presented ablation.** The paper compares HydraLoRA to HydraLoRA "w/o Router" (which drops performance) to argue that dropout is critical. But HydraLoRA does not use the same dropout mechanism as R-LoRA/M-LoRA, so the comparison conflates architectural differences between model families with the effect of dropout. A direct ablation (M-LoRA without dropout) would cleanly substantiate this claim.

6. **No limitations discussion.** The paper does not discuss limitations of Align-LoRA: the Gaussian (diagonal-covariance) assumption on representations, the O(M²) pairwise KL computations for many tasks, and the possibility that forced alignment could hurt on tasks requiring genuinely distinct representations.

7. **Table 5 tasks are not named in the main paper.** The eight tasks are labeled "Task1" through "Task8" without names, forcing the reader to consult the appendix for basic experimental context.

### Trivial

None.

## Nice-to-Haves

- A brief latency measurement substantiating the claimed inference overhead of multi-component variants would strengthen the practical motivation.
- An analysis of why MMD fails where KL succeeds (e.g., is the Gaussian assumption the key difference?) would significantly strengthen the paper and address the current factual gap.

## Removed Points

These points are flagged to be removed; treat them with caution:

- "Missing baselines from outside the LoRA family" — scope of the paper is LoRA-family methods; demanding non-LoRA baselines (prefix tuning, adapters) is scope creep.
- "No inference latency measurement" — nice-to-have, not central to the paper's methodological contribution.
- "The connection between observations and method is logically loose" — subsumed by Weakness 3 (missing equi-rank comparison); the paper has a coherent narrative, the gap is the missing control.
- "Line 146 overclaims by not acknowledging M-LoRA still beats high-rank LoRA" — the paper uses qualified language ("competitive with, and at times superior to") which is accurate; M-LoRA often edges ahead but by very small margins.
- "5 tasks are a thin basis for a paradigm shift" — overstated; the paper's main results (Tables 2–5) use larger benchmarks (Flanv2, BBH, 8-task set).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Correct the factual error** about A-LoRA-M's performance. Acknowledge that MMD alignment underperforms in some settings and provide analysis of why.
2. **Add variance information** (at minimum 3 seeds with standard deviation) for all main results.
3. **Add a LoRA rank=8 row** to Table 4 to cleanly isolate the effect of alignment from rank.
4. **Remove or rework the theoretical section** (Section 5.3) to either present a method-specific bound or drop the section entirely.
5. **Rename tasks in Table 5** and add a limitations paragraph discussing the Gaussian assumption, scalability to many tasks, and the MMD failure mode.
6. **Strengthen the dropout analysis** by directly ablating dropout in M-LoRA.

---

## Score and Decision

**Calibration anchors (all retrieved rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| UnoLoRA (49ti6LOUw5.md) | 3.00 | R1 | Single shared LoRA for MTL; much less rigorous, one model only, confusing method. Current paper is significantly stronger. |
| MORE (LWvgajBmNH.md) | 4.00 | R1 | MoE LoRA for MTL; limited novelty, marginal gains, only GLUE. Current paper is stronger. |
| ShareLoRA (O6QZ4W6GXt.md) | 4.20 | R2 | Sharing LoRA modules. Current paper has better experiments and clearer contributions. |
| LoTA (qOqCXEXsX4.md) | 4.25 | R2 | Sparse adaptation for MTL; current paper is comparable or slightly stronger. |
| Seeded LoRA (U3UtvOYMiw.md) | 5.00 | R2 | Collaborative fine-tuning; similar tier but current paper has more novel findings. |
| LoraHub (w8eCnnq57m.md) | 5.33 | R2 | LoRA composition for cross-task generalization; similar tier. |
| **PaLoRA (icDoYdUhRa.md)** | **5.50** | **R2** | **Pareto LoRA for MTL. Similar level — has contributions but weaknesses like missing variance and limited comparisons. Current paper is comparable.** |
| C-Poly (G1Hlubz1fR.md) | 6.00 | R1 | Composable LoRA for MTL; stronger experiments but more incremental. |
| Multi-Task Model Fusion (iynRvVVAmH.md) | 7.00 | R1 | Stronger theory and rigor across vision and language; current paper is weaker. |

**Round 1 bracket:** 4.5–6.5  
**Round 2 narrowed to:** 5.0–6.0  

This paper makes a genuine empirical contribution by challenging a trend toward increasingly complex multi-component LoRA architectures. The core findings in Sections 3–4 are clean and useful, and Align-LoRA is a practical method with zero inference overhead. However, the paper has several issues that prevent clean acceptance: a factual error about A-LoRA-M's performance, complete absence of variance reporting, no equi-rank ablation to isolate the alignment effect, and an ornamental theoretical section. These are fixable, but as presented they weaken the evidence for the paper's central claims.

**Final score: 5.5** — borderline accept. The paper has real empirical contributions but requires significant revisions (particularly correcting the factual error, adding variance, and adding the equi-rank control) before the claims can be fully trusted.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>