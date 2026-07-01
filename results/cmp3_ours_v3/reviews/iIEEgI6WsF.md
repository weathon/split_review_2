Now I have enough calibration data. Let me produce the final review.

## Summary

This paper proposes On-Demand Communication (ODC), which replaces collective all-gather and reduce-scatter operations in FSDP with point-to-point communication primitives inspired by the parameter server architecture. The key insight is that LLM post-training workloads have imbalanced sequence lengths, creating straggler effects under FSDP's per-layer synchronization barriers. ODC relaxes synchronization from per-layer to per-minibatch, decouples device progress, and enables a simpler load-balancing scheme (LB-Mini) that operates at the minibatch rather than microbatch level. Experiments on SFT (LongAlign, SWE-Smith) and RL (GRPO/AIME) tasks with 1.5B–32B models show consistent throughput improvements, up to 36%.

## Strengths

1. **Well-motivated problem identification (Section 1, Section 2.2).** The paper identifies a concrete and consequential tension: FSDP's per-layer collectives create synchronization barriers that are harmless under balanced workloads but costly in LLM post-training, where sequence lengths vary dramatically. The formalization in Eq. (1) — minibatch runtime as Σ_m Σ_l max_d T_{m,d,l} — cleanly captures why per-layer barriers compound imbalance.

2. **Clean conceptual reframing (Section 3.1, Figure 6).** The idea of recasting FSDP as a decentralized parameter server — where each device is simultaneously a server (owning a parameter/gradient shard) and a worker (executing forward/backward) — is genuinely novel and well-articulated. It explains why PS-style tolerance for imbalance can be obtained without dedicated server nodes and without losing FSDP's memory efficiency. This conceptual framing is the paper's most distinctive contribution.

3. **Principled load-balancing simplification (Section 4).** The decoupling of device progress enabled by ODC allows load balancing to shift from the microbatch level (constrained by device memory and forced equal microbatch counts) to the minibatch level (where devices can process different numbers of microbatches). This is a qualitatively different design space, not merely an incremental improvement.

4. **Consistent throughput gains across diverse settings (Figures 8, 9, 10).** The empirical evaluation covers SFT and RL, 1.5B–32B models, 8–32 GPUs, multiple datasets, and both unpacked and packed settings. The trend is consistent — ODC wins in every subplot — giving confidence the effect is real. The parametric study (Figure 10) is particularly informative, showing how the benefit varies with minibatch size, sequence length, packing ratio, and device count.

## Weaknesses

### Fatal
None.

### Major

1. **"Collective LB-Mini" in Figure 8 is undefined.** Section 5.1 (line 179) states: "As LB-Mini can produce different number of microbatches for different devices, it applies only to ODC." Yet Figure 8 plots a method labeled **"Collective LB-Mini"** (purple triangles) in all eight subplots, and the caption and body text (lines 183, 197) describe it as one of the five compared methods. The paper never explains how this configuration is implemented. If it uses LB-Mini's sample-to-device assignment but forces equal microbatch counts (via padding or repacking) to work with collectives, that is a reasonable baseline — but the paper owes the reader an explicit description. If the labeling is a mistake, it must be corrected. This ambiguity directly affects the interpretability of the main results figure. (Note: the core claim that ODC outperforms collectives does not hinge exclusively on this single comparison — it is also supported by ODC+LB-Micro vs Collective+LB-Micro and ODC+LocalSort vs Collective+LocalSort — but the ambiguity is nevertheless a significant presentation gap that must be resolved.)

### Minor

2. **Cross-node communication overhead is acknowledged but insufficiently characterized.** The microbenchmark (Figure 11) shows ODC primitives are significantly slower than collectives across nodes (roughly 2× bandwidth gap at 16–32 devices). The paper offers two mitigations (Section 6.1): overlapping communication with computation and hybrid sharding. However, it does not provide a direct measurement of how much communication is actually overlapped vs. exposed in the end-to-end experiments. The argument that "computation scales as O(s²)" while communication is O(1) in sequence length is reasonable for attention layers but does not cleanly extend to MLP layers (which scale O(s) in sequence length). A simple wall-time breakdown (communication vs. computation vs. idle for ODC vs. collective) would strengthen the analysis. The results as presented already account for this overhead, so the concern is about depth of explanation, not validity.

3. **RL evaluation does not test LB-Mini's core mechanism.** The paper acknowledges (line 199) that implementation constraints in verl require identical numbers of samples per device, limiting LB-Mini's effectiveness in RL. The RL results (up to 10% speedup) are notably smaller than SFT (up to 36%). The paper states that relaxing this constraint "is feasible" but was not done because "the current solution is easier to integrate." Since one of ODC's key claimed advantages is enabling per-device microbatch count variation, disabling this in the RL experiments means the RL evaluation does not fully test the claimed mechanism. The paper's own hedging here weakens an otherwise clean empirical narrative.

### Trivial
None.

## Nice-to-Haves

- **Variance estimates.** Throughput is reported as point estimates without error bars, confidence intervals, or mention of multiple runs. Since workload imbalance has a stochastic component (depending on which samples end up on which device), results from repeated runs with different data shuffles would be more convincing.
- **Memory bandwidth analysis.** ODC's point-to-point gather means a device reads parameter shards from remote memory while computing. The paper mentions using RDMA for transparent access but does not discuss whether this competes with local computation for memory bandwidth on the receiving device (where the "server" role is colocated with computation). If so, this could be a hidden cost worth characterizing.
- **Communication-computation overlap breakdown.** A direct measurement showing how much of the cross-node communication overhead is actually hidden by computation (vs. exposed as wall-clock time) would strengthen the overlapping argument in Section 6.1.

## Removed Points
- **"Missing limitations section"** — The paper has Section 6 (Discussion) which addresses challenges and future work, effectively serving as a limitations discussion. Removed as strawman.
- **Figure captions for Figures 1 and 2 are identical** — This is a parser artifact from PDF extraction; the original submission's figures are distinct. Removed as formatting nitpick.
- **Cross-node issue framed as a "methodological gap" that invalidates results** — The results already account for this overhead; the paper acknowledges and discusses mitigations. Demoted to Minor weakness #2.
- **"MLP layers not O(s²)" presented as a fatal flaw** — The paper's O(s²) claim refers to overall computation for long sequences where attention dominates. The simplification is reasonable for the intended regime. Incorporated into Minor weakness #2 but significantly reduced in severity.
- **Generic strength about "addressing an important problem"** — Too generic/superficial; not specific to this paper's content. Removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Resolve the "Collective LB-Mini" ambiguity** — This is the single highest-leverage improvement. State explicitly what this configuration is: does it use LB-Mini's sample assignment but with equal microbatch counts (via padding or repacking)? Provide implementation details.
2. **Add a wall-time breakdown** for at least one representative setting (e.g., 14B model, minibatch size 4) showing compute vs. communication vs. idle time for ODC and collective. This would directly address concerns about how much cross-node overhead is actually hidden by overlap.
3. **Run the RL experiments without the verl constraint** (allowing per-device microbatch count variation) to demonstrate LB-Mini's benefit in that domain, or clearly caveat the RL results as reflecting only the communication-side improvement of ODC, not the load-balancing improvement.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| SPD: Sync-Point Drop | uoU4ypjAmN.md | 4.00 | R1 | Same topic area (sync-point reduction for LLM distributed training) but SPD had weaker evaluation (missing end-to-end latency) and limited experiments. Our paper is notably stronger. |
| ACCO: Accumulate while Communicate | UV1jr2aJ2J.md | 5.00 | R1 | Communication-computation overlap for LLM training. Criticized for limited novelty (similar to prior work). Our paper has a stronger conceptual contribution (PS reframing). |
| LightSeq: Sequence Level Parallelism | kC5i5X9xrn.md | 5.00 | R2 | Sequence parallelism for long contexts. Criticized for limited baselines and novelty concerns. Our paper has a cleaner contribution and more diverse evaluation. |
| DSP: Dynamic Sequence Parallelism | Z3xg3hxdky.md | 5.40 | R1 | Sequence parallelism for multi-dimensional transformers. Criticized for unfair comparisons and missing analysis. Our paper is stronger in motivation and experimental consistency. |
| From Promise to Practice | lo3nlFHOft.md | 6.67 | R1 | Decentralized training with runtime model and convergence analysis. Stronger in theoretical depth (convergence proof, analytical model). Our paper has a more practical contribution but lacks theoretical analysis. |
| CO2: Efficient Distributed Training | ZO5cn4IfaN.md | 7.00 | R1 | Communication-computation overlap with convergence proof and extensive experiments. Stronger in both theory and experimental breadth. |

**Round 1 Bracket:** 5.5 – 7.0

After comparing with anchors: Our paper is clearly stronger than SPD (4.00), LightSeq (5.00), ACCO (5.00), and DSP (5.40) — all of which had novelty or evaluation weaknesses that our paper does not share. Our paper is weaker than "From Promise to Practice" (6.67) which has convergence theory and a runtime model, and weaker than CO2 (7.00) which has proof and more extensive experiments.

The paper's core contribution (reframing FSDP as a decentralized PS to eliminate per-layer barriers under imbalanced workloads) is novel and well-supported. The evaluation is diverse and consistent. The main weakness is the undefined "Collective LB-Mini" baseline, which is a presentation gap that must be fixed but does not undermine the overall thesis (supported by other comparisons). The other weaknesses (cross-node characterization, RL constraint) are minor.

**Final score: 6.0** — A solid borderline accept. The contribution is real and the idea is clean, but the ambiguous evaluation baseline and self-imposed RL constraint prevent it from being a clear accept without revision.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>