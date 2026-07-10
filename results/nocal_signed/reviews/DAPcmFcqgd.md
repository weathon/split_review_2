Now I have all the information needed. Let me synthesize the final review.

---

## Summary

This paper proposes MoEP (Modular Expert Paths), an architecture that combines layer-level parallelism with MoE-style top-k routing while keeping the total parameter count fixed by reducing the hidden dimensionality of the parallel stack. The model is evaluated on the BabyLM strict-small track and compared against GPT-2 and GPT-BERT baselines. The core idea — adding sparsity without increasing parameters — is genuinely novel and well-motivated.

## Strengths

- **The core architectural idea is well-motivated and novel.** Combining layer-level parallelism (inspired by PaPaformer) with MoE-style top-k routing while scaling down dimensionality in the parallel stack to keep total parameters fixed is a genuinely interesting and underexplored design space (Sections 3.1–3.3). The problem it targets — adding sparsity without parameter growth — is a worthwhile research direction.

- **The evaluation follows a standardized, community-accepted benchmark pipeline.** Using the BabyLM strict-small track provides a reproducible evaluation framework with multiple zero-shot and fine-tuning tasks. The checkpoint selection procedure (best evaluation checkpoint) is clearly documented (Section 4, Table 1).

- **The paper candidly discusses its limitations.** Section 6 acknowledges that scaling up is uncertain and that reduced-dimensionality parallel blocks may not work on more complex data. This transparency is a genuine strength that many papers lack.

## Weaknesses

### Fatal
None.

### Major

- **Misleading headline claims about benchmark performance.** The introduction states MoEP "was able to outperform all BabyLM strict-small baseline models" (line 31) without qualification. This is only true when AoA is included in the macro average — a task on which GPT-BERT scores *negative* values (−3.90), dragging down its average. On the standard macro average **excluding AoA**, the GPT-BERT variants (54.10, 53.65, 52.40) substantially outperform MoEP (49.00) by 3.4–5.1 points. The paper's own Table 1 shows this clearly, but the narrative framing in the introduction does not reflect it. The paper *does* later qualify this claim (Section 5.1, line 166), but the initial framing remains misleading.

- **No ablation studies isolate the routing mechanism's contribution.** MoEP differs from GPT-2 in at least four simultaneous ways: (a) 2 full-size + 10 parallel layers vs. 12 full-size layers, (b) top-2 routing among 4 parallel blocks per parallel layer vs. no routing, (c) MoE shrink/grow projection blocks vs. no projections, and (d) a load-balancing auxiliary loss. The reported improvement over the authors' own GPT-2 reimplementation is only 0.9 points (49.00 vs. 48.10). Without a controlled ablation — e.g., learned routing vs. dense activation (all blocks always active) vs. random routing — the paper cannot attribute this small gap to the routing mechanism rather than to the parallel architecture, dimensionality reduction, or training procedure differences. This gap directly undermines the paper's central claim that sparsity itself is beneficial.

- **The paper claims efficiency but provides no computational efficiency measurements.** The title says "Compact and Efficient Sparsity" and the abstract claims the architecture "accelerates model learning." Yet there are no FLOP counts per token, no training throughput (tokens/sec), no inference speed comparisons, and no memory usage analysis. The only evidence for faster learning is the qualitative training dynamics discussion in Appendix A.3, which shows both MoEP and GPT-2 reaching peak performance at the same 30M-word checkpoint. Without efficiency metrics, the claimed benefit of "sparsity without parameter growth" is asserted but never demonstrated to provide any practical advantage.

### Minor

- **The load-balancing auxiliary loss is underspecified.** Equation (3) defines λ^block and λ^expert coefficients, but their values are never reported in Table 3 or anywhere else. The entropy-based balancing objective is also non-standard in the MoE literature (which typically uses importance-weighted auxiliary losses), and this design choice is not justified. This limits reproducibility.

- **No quantitative routing analysis** despite being listed as a contribution (contribution 3: "analyze expert networks routing behavior"). The paper provides no load distribution statistics, no entropy of routing assignments, and no analysis of which tokens activate which parallel blocks.

- **Single-run results** with no variance estimates (a single seed, 42). While single runs are common in the BabyLM setting, the small performance margins (0.9 points) would benefit from variance reporting to establish reliability.

### Trivial
None.

## Nice-to-Haves

- Hyperparameter sensitivity analysis exploring how the number of parallel blocks (P), top-k value, or number of parallel layers (N) affects performance would strengthen the understanding of the architecture's behavior.
- Reporting variance across multiple random seeds would help assess the reliability of the small observed improvements.

## Removed Points (treated with caution)

These points from the input review were removed after verification against the paper:
- *"Paper does not explain how top-2 outputs are combined"* — The paper states "the routed inputs are summed up together" (line 122). The combination method is stated, though whether weights from the gating mechanism are applied is unclear.
- *"Conflates PaPaformer and MoE literatures"* — The paper explicitly distinguishes PaPaformer-style parallelism from MoE-style routing and positions MoEP as building on both.
- *"Calling linear projections 'experts' overstates complexity"* — A tone/style criticism rather than a substantive flaw.
- *Grammar/writing quality complaints* — Per policy, formatting and grammatical artifacts from PDF extraction are not treated as author errors.
- *Demand for full hyperparameter sensitivity analysis* — A reasonable wish-list item but not a required standard for an exploratory architecture paper at this scale.

## Novel Insights

None beyond the paper's own contributions. The reviewer inputs converge on a consistent assessment: the paper proposes a genuinely interesting architectural idea but presents its results too aggressively and lacks the ablations and efficiency measurements necessary to substantiate its core claims about the routing mechanism and computational benefits.

## Suggestions

1. **Add ablation studies** comparing learned top-k routing against: (a) dense activation (all parallel blocks always active), and (b) random routing. This would isolate whether the routing mechanism itself contributes beyond the parallel architecture.
2. **Provide computational efficiency metrics**: FLOPs per token, training throughput (tokens/sec), and inference throughput for MoEP vs. GPT-2.
3. **Report λ^block and λ^expert values** and justify the entropy-based balancing objective.
4. **Qualify the performance claims** in the introduction to accurately reflect that the advantage over GPT-BERT depends on including AoA, and that GPT-BERT variants significantly outperform MoEP on the standard macro average excluding AoA.
5. **Run additional random seeds** to provide variance estimates, given the small performance margins.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>