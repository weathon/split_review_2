Now I have sufficient calibration data. Let me write the final review.

Here is my bracket analysis:

**Round 1 bracket:** The paper sits in the 5.5–6.5 range. It is clearly stronger than the 3.8–4.4 reject-range papers (which had fundamental novelty or method issues) and weaker than the 7.0+ papers (which had comprehensive multi-backbone evaluations, formal guarantees, or large-scale benchmarks).

**Round 2 narrowing:** Comparing against C-CLIP (6.50, Accept), "Learning without Forgetting for VLMs" (5.67, Reject), and TiC-CLIP (6.25, Accept):
- NuSA-CL has *stronger* strength impact scores (+32.76 total) than any of these anchors (C-CLIP: +23.91, LwF-VLM: +14.15), driven by very high scores on efficiency (+9.81), performance (+9.93), and ablations (+9.96).
- Its dominant weakness (-10.00 for no variance) is comparable in magnitude to C-CLIP's worst weaknesses (-10.00 for typos, -9.99 for missing related works), but C-CLIP had a benchmark contribution that NuSA-CL lacks.
- Compared to LwF-VLM (5.67, Reject), NuSA-CL has stronger empirical validation (direct ablations of the mechanism) and a cleaner, more novel method.

I place the paper at **6.0**: solidly above the reject boundary, with genuine contributions, but the missing variance reporting is a meaningful gap that prevents a higher score.

---

## Summary

This paper introduces NuSA-CL, a memory-free continual learning framework for CLIP that constrains task-specific LoRA updates to an approximate null space of the current weights (identified via SVD). The method operates in a three-stage cycle—null space identification, constrained adaptation, weight merging—with zero storage overhead, no parameter growth, and no replay buffers. Experiments on MTIL and CIFAR-100 benchmarks show strong performance in the storage-free setting, with dramatic efficiency gains (1.5M parameters, 1.21 GPU-hours) relative to storage-based competitors.

## Strengths

- **Clean, well-motivated methodological idea (Sections 3.1–3.3).** The three-stage cycle—SVD-based null space identification, persistent constrained adaptation within that subspace, and weight merging—is conceptually elegant. The paper clearly distinguishes its *persistent* constraint from prior work that uses low-energy subspaces only for initialization and allows updates to drift.

- **Genuinely impressive efficiency (Table 1).** NuSA-CL uses only 1.5M trainable parameters (40× fewer than MoE-Adapters' 59.8M), 6.6 GB peak GPU memory (vs 15.5 GB), and 1.21 GPU-hours (vs 3.42). These are dramatic reductions that make the method viable for resource-constrained deployment.

- **Competitive performance in the storage-free setting (Table 1).** On the MTIL benchmark, NuSA-CL achieves 68.6 Transfer / 75.1 Avg / 82.8 Last, substantially outperforming LoRA (63.9/70.1/79.9) and MiLoRA (62.8/68.7/77.4). This ~5-point improvement supports that the null-space constraint provides genuine benefit over unconstrained LoRA.

- **Principled ablation study (Section 6, Figures 3a–3b, Table 4).** The subspace selection ablation (Tail vs Top vs Random) cleanly demonstrates that low-energy directions cause less forgetting across all tested ranks. The persistent constraint ablation (Table 4a) shows that unfreezing the null-space bases degrades performance. These directly validate the claimed mechanism rather than just comparing end-to-end numbers.

## Weaknesses

### Fatal
None.

### Major
- **No measures of variance or statistical significance reported anywhere.** Tables 1, 2, and 3 report single-point estimates with no standard deviations, confidence intervals, or multi-seed averages. Given that continual learning methods can be sensitive to task order, learning rates, and random seeds, it is impossible to determine whether reported differences (e.g., 68.6 vs 66.2 Transfer, or 71.85 vs 67.36 Last at 50-step CIFAR-100) are statistically reliable or within noise. This is a significant gap for an empirical paper whose main claims rest on comparative performance numbers. The authors should add at minimum 3-seed runs with standard deviations to all main tables.

### Minor
- **The theory section (Section 4) motivates but does not directly connect to forgetting.** Lemma 1 bounds |⟨W, ΔW⟩_F| ≤ σ_max^null · ‖M‖_F, which is a parameter-space inner product. As the paper acknowledges (Section 4.2: "should be viewed as a local stability condition rather than a full function-level guarantee"), this does not directly bound functional forgetting. The connection between parameter-space orthogonality and preserved predictions is not established. The theory is best read as motivation rather than a formal guarantee, and the paper's language ("principled mechanism for mitigating catastrophic forgetting") slightly oversells it.

- **The CIFAR-100 comparison is more nuanced than claimed (Table 3).** The paper includes non-CLIP baselines (LwF, ICaRL) that underperform CLIP zero-shot and are not informative comparisons. The relevant CLIP-based baseline (ZSCL) is present, but the picture is mixed: at 10 steps, ZSCL achieves higher Avg (82.15 vs 80.25). The claimed "large margin of over 4.4%" applies to the 50-step Last metric specifically (71.85 vs 67.36); on Avg at 50 steps the gap is a narrow 80.19 vs 79.92. The paper's claim of an "increasingly pronounced advantage" holds for Last but not for Avg.

- **The "Last" metric is described as "which measures forgetting" but is actually final average accuracy.** True forgetting is typically measured as the per-task accuracy drop from post-training to final evaluation. Final average accuracy confounds retention with plasticity for the last-learned task. Replacing or supplementing this with a direct forgetting measure would strengthen the paper.

- **InflLoRA (9 MB gradient projection memory) is classified as "storage-based" alongside methods with orders-of-magnitude larger storage (ZSCL: 10.5 GB).** While technically correct (9 MB is non-zero), the "storage-free vs storage-based" dichotomy groups InflLoRA with substantially more resource-intensive methods. The practical comparison of most interest—NuSA-CL vs the strongest parameter-efficient competitor with negligible overhead—should be foregrounded more explicitly.

### Trivial
None.

## Nice-to-Haves
- An empirical test of the theoretical bound (tracking ⟨W_{t-1}, ΔW_t⟩_F across tasks for NuSA-CL vs LoRA vs MiLoRA) would ground the theory in observable behavior.
- A direct prediction-change analysis (measuring how per-task accuracy changes as new tasks are learned) would directly test the claimed forgetting reduction.
- Adjusting the "storage-free vs storage-based" framing to acknowledge InflLoRA's minimal overhead (9 MB) more explicitly.

## Removed Points
These points were considered but removed as they do not meet the filtering criteria:

1. **"Null-space circularity concern about eventual saturation."** — The paper provides empirical evidence addressing this: 313 null directions remain after 10 tasks (more than 2× the update rank), and the 50-step CIFAR-100 analysis shows spectral stability. The concern is speculative and the paper honestly acknowledges capacity limits as a limitation.

2. **"Overstated claim about PEFT methods storing prior task info."** — The paper says "many" PEFT techniques, not all. Standard LoRA is storage-free but performs poorly in CL (63.9 Transfer). The claim is accurate as written.

3. **"Parameter count discrepancy for InflLoRA unaddressed."** — Minor clarity issue about why InflLoRA uses 7.8M vs 15.7M parameters at the same rank. Not central to the paper's claims.

4. **"No experiments on larger backbones."** — The paper discusses SVD scaling and acknowledges this as a limitation and future work. Scope creep beyond the paper's stated scope.

5. **"No evaluation of task-order sensitivity."** — Listed as future work. Scope creep.

6. **"Direct prediction-change analysis missing."** — A reasonable suggestion but not standard CL practice; the paper uses standard CL evaluation metrics.

## Novel Insights
None beyond the paper's own contributions. The reviews converge on the paper's core strengths (clean method, strong efficiency, solid ablations) and its main empirical weakness (lack of variance reporting). No reviewer identified a perspective or connection that the paper itself does not address.

## Suggestions
1. **Add multi-seed results with standard deviations to all main tables (1, 2, 3).** This is the single most impactful addition.
2. **Reframe the CIFAR-100 discussion** to explicitly acknowledge the mixed picture at shorter sequences while highlighting the long-sequence Last-accuracy advantage.
3. **Either strengthen the theory or de-emphasize it** — add an empirical validation of the bound or move it to the motivation section rather than presenting it as a formal guarantee.
4. **Supplement the "Last" metric with a direct forgetting measure** (average per-task accuracy drop).

## Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/G9Ea7mlqGO.md | 3.80 | 1 | Yes | Similar topic (CLIP continual learning) but weaker method and novelty. NuSA-CL is substantially stronger. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/gV0Moskp7k.md | 4.40 | 1 | Yes | Low-rank continual learning but only tested on T5-large; theory-algorithm mismatch. NuSA-CL has better validation. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/sb7qHFYwBc.md | 6.50 | 1 | Yes | C-CLIP: benchmark contribution + LoRA-based CL. NuSA-CL has stronger efficiency and ablations but no benchmark contribution. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/TLADT8Wrhn.md | 6.25 | 1 | Yes | TiC-CLIP: large-scale benchmark paper. Different contribution type; NuSA-CL has stronger method innovation. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/k9NYnsC4Mq.md | 5.67 | 2 | Yes | LwF-VLM: projection-based CL for VLMs. NuSA-CL has stronger ablations and efficiency evidence. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/wE1I9IGqeH.md | 6.00 | 2 | No | Complementary memory systems for open-vocab CL. Different approach. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/AZR4R3lw7y.md | 5.75 | 2 | No | Multi-view RP for pretrained-based CL. Accepted but lower score range. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/rkAqvDnnmO.md | 5.25 | 2 | No | Simple efficiency IL framework with multi-adapters. Rejected. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/9aZ2ixiYGd.md | 5.00 | 2 | No | Prompt-based rehearsal-free CL. Accepted with split reviews. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Hf54sNeeBM.md | 4.75 | 2 | No | Knowledge accumulating contrastive prompt CL. Rejected. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/9vkgAaCI3F.md | 5.25 | 2 | No | RDAC framework for stability-plasticity. Rejected. |

**Score Rationale:** NuSA-CL's strengths (+32.76 cumulative impact) are substantially higher than those of the rejected anchors in the 4.0–5.5 range, driven by very strong efficiency, performance, and ablation scores. Its dominant weakness (no variance reporting, -10.00) is a single issue that is fixable in revision rather than a fatal flaw. Compared to C-CLIP (6.50), NuSA-CL lacks a benchmark contribution but has cleaner ablations; compared to LwF-VLM (5.67, Reject), it has stronger validation and a more novel method. The score of 6.0 recognizes the genuine contribution while flagging the missing variance as a non-trivial gap that prevents a higher score.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>