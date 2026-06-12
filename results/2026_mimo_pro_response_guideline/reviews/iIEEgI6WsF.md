The Round 2 results confirm the bracket. The most directly comparable papers ("From Promise to Practice" at 6.67, "CO2" at 7.00, "Zero Bubble PP" at 7.00) are all accepted systems papers on distributed training communication. Our paper has comparable contribution quality: cleaner conceptual framing, comprehensive evaluation, but some presentation issues (conflated headline, LB-Mini inconsistency).

**Final calibration: 7.0.** The paper sits alongside accepted systems papers in the 6.5-7.5 range. It is clearly above rejected papers (DSP 5.40, Decentralized Training 2.00). Its weaknesses are presentation/evaluation gaps, not structural flaws.

## Summary
This paper proposes On-Demand Communication (ODC), which replaces FSDP's per-layer collective all-gather/reduce-scatter with point-to-point RDMA gather/scatter-accumulate operations for LLM post-training. By relaxing synchronization from per-layer to per-minibatch granularity, ODC decouples device execution and eliminates straggler-induced idle time under the imbalanced workloads caused by variable sequence lengths. A secondary contribution is LB-Mini, a simplified minibatch-level load balancing strategy enabled by ODC's decoupled microbatch execution. The paper reports up to 36% speedup on SFT and 10% on RL tasks.

## Strengths
- **Well-motivated problem with quantified evidence**: Table 6 and Section 1 establish that even state-of-the-art packing strategies leave up to 50% device idle time during long-sequence SFT, demonstrating a real gap that warrants a communication-level fix.
- **Comprehensive evaluation across tasks, scales, and datasets**: Evaluation covers SFT (LongAlign, SWE-Smith) and RL (AIME with GRPO), model sizes 1.5B–32B, up to 32 GPUs, multiple minibatch sizes, and both packed and unpacked settings (Figures 8, 9).
- **Well-designed parametric study**: Figure 10 and Table 1 use a controlled "golden setting" methodology that isolates individual factors (minibatch size, max sequence length, packing ratio, device count), yielding actionable and interpretable insights.
- **Honest treatment of limitations**: Section 6.1 and Figure 11 directly acknowledge that ODC's point-to-point primitives underperform NCCL collectives for inter-node communication, and propose concrete mitigations (communication-computation overlap, hybrid sharding in Appendix E).
- **Clean and practical core mechanism**: Replacing collectives with RDMA-based point-to-point operations via CUDA IPC (intra-node) and NVSHMEM (inter-node), implemented through Triton-Distributed, is a well-motivated design that preserves FSDP's memory layout while removing synchronization artifacts.

## Weaknesses

### Fatal
None

### Major
- **Headline "36% speedup" conflates two orthogonal improvements** — The abstract and introduction claim "up to 36% speedup over standard FSDP," but this figure comes from comparing ODC+LB-Mini against Collective+LocalSort (Section 5.2, line 197), which bundles both the communication scheme change (ODC vs. Collective) and the load-balancing algorithm change (LB-Mini vs. LocalSort). The fair ablation isolating ODC's communication contribution is ODC+LB-Micro vs. Collective+LB-Micro (same load balancing, different communication), where improvements appear smaller (~10–25% from Figure 8). The paper does present all necessary data for decomposition, and Figure 10 correctly uses Collective+LB-Micro as the baseline. However, the headline in the abstract, introduction, and Section 5.2 consistently highlights the most optimistic combined number without explicit decomposition. This risks overstating the contribution of the core ODC mechanism.

- **Inconsistency between text and Figure 8 on LB-Mini's applicability** — Section 5.1 states: "As LB-Mini can produce different number of microbatches for different devices, it applies only to ODC" (line 179). Yet Figure 8 explicitly shows "Collective LB-Mini" as a baseline with throughput results. This is contradictory. If Collective LB-Mini pads shorter devices to preserve synchronization (requiring uniform microbatch counts), this should be stated explicitly. If LB-Mini genuinely requires heterogeneous microbatch counts, "Collective LB-Mini" should not appear. Clarifying this would also strengthen the argument for ODC's unique benefit of enabling minibatch-level balancing.

### Minor
- **No balanced-workload ablation** — The paper does not evaluate ODC on balanced or near-balanced workloads to confirm it does not introduce overhead in the common case. While the paper notes methods "perform similarly when the minibatch size is one" (line 197), this is a degenerate single-sample case, not a balanced multi-sample workload. A brief experiment with uniform-length synthetic data would confirm ODC is a robust improvement rather than introducing a tradeoff.

- **Gradient accumulation under heterogeneous microbatch counts not fully explained** — When LB-Mini assigns different numbers of microbatches to different devices, the gradient weights w_m for cross-device averaging need careful handling. Section 2.1 describes w_m for "proportional weighting when averaging by tokens or samples" (line 49) but does not address how this works when devices have different numbers of microbatches. A brief paragraph explaining the correct normalization in this setting would strengthen confidence.

- **Inter-node communication overhead not profiled in main results** — Figure 11 shows ODC has significantly lower raw bandwidth than NCCL collectives for inter-node transfers. The main SFT results include multi-node configs (14B/16-GPU, 32B/32-GPU). Section 6.1 argues O(s²) computation hides O(1) communication latency for long sequences, and Appendix E shows hybrid sharding as mitigation. However, the main evaluation lacks a communication/computation time breakdown for these multi-node setups. Even a simple profiling for the 32B/32-GPU configuration would substantiate the claim that computation indeed hides the inter-node overhead.

### Trivial
None

## Nice-to-Haves
- A bar chart or table explicitly decomposing the 36% into (a) ODC communication-only improvement, (b) LB-Mini load-balancing-only improvement, and (c) combined improvement.
- Peak GPU memory measurements for ODC vs. FSDP to substantiate the claim that ODC "preserves FSDP's memory layout."
- A brief discussion of how ODC relates to sequence-parallel and dynamic-batching approaches.

## Removed Points
These points are flagged to be removed, treat them with caution:
- "Missing comparison against sequence-length-aware FSDP variants" — scope creep; the paper explicitly positions ODC as orthogonal to packing strategies.
- "LB-Mini novelty hard to evaluate since algorithms deferred to Appendix C" — Appendix content is stripped by the parser; the original paper contains the details.
- "Missing related works" — cannot verify existence of external references.

## Novel Insights
The paper's core insight — that per-layer synchronization in FSDP is an artifact of the communication model, not a requirement of the training algorithm, and can be relaxed to per-minibatch granularity using point-to-point RDMA — is genuinely novel and well-articulated. The reframing of FSDP as a decentralized parameter server provides a useful conceptual bridge between classical distributed ML and modern sharded data parallelism. The observation that O(1) communication volume vs. O(s²) compute volume means inter-node overhead becomes negligible for long sequences is a practical insight that makes the inter-node bandwidth gap less concerning than raw benchmarks suggest.

## Suggestions
- Decompose the 36% headline figure explicitly to isolate the communication contribution from the load-balancing contribution.
- Clarify what "Collective LB-Mini" means in Figure 8 given the text claims LB-Mini applies only to ODC.
- Add a brief communication/computation time breakdown for multi-node configurations.
- Add a brief explanation of how gradient averaging works correctly when devices have different numbers of microbatches.
- Consider a balanced-workload experiment to confirm ODC does not regress performance.

## Score and Decision

### Anchoring Report

**Round 1 anchors (all queries)**:
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| lo3nlFHOft.md ("From Promise to Practice") | 6.67 | 1,2 | Most directly comparable — decentralized training, 64 GPUs, convergence proofs. Our paper has broader evaluation but less theory. |
| ZO5cn4IfaN.md ("CO2") | 7.00 | 1,2 | Communication-computation overlap, 128 GPUs. Our paper has cleaner framing, comparable evaluation breadth. |
| yroyhkhWS6.md ("QSR") | 6.75 | 1 | Synchronization rule for Local SGD. Our paper is more practically focused. |
| Z3xg3hxdky.md ("DSP") | 5.40 | 1 | Sequence parallelism — rejected due to limited evaluation scope. Our paper is clearly stronger. |
| bntJK4NyIW.md ("Decentralized Training in Het. Network") | 2.00 | 1 | PS + pipeline parallelism — rejected for limited novelty. Our paper is clearly stronger. |
| tuzTN0eIO5.md ("Zero Bubble PP") | 7.00 | 2 | Pipeline parallelism scheduling — comparable contribution level. |
| 1qP3lsatCR.md ("NetMoE") | 7.20 | 2 | MoE training optimization — comparable contribution level. |
| 7JhGdZvW4T.md ("TRAIL scheduling") | 6.00 | 1 | LLM serving scheduling — less directly relevant but accept-level. |

**Round 1 bracket**: 6.5–7.0. The paper is clearly above rejected systems papers (DSP 5.40, Decentralized 2.00) and comparable to accepted papers in the 6.5–7.2 range. The conflation of the 36% headline and the LB-Mini text/figure inconsistency are real presentation issues but not structural flaws. The core contribution is sound, well-motivated, and comprehensively evaluated.

**Final score**: 7.0 — Sits alongside accepted systems papers ("From Promise to Practice" 6.67, "CO2" 7.00, "Zero Bubble PP" 7.00). The paper makes a meaningful practical contribution to an important problem, with clear conceptual framing and solid evaluation. The identified weaknesses are addressable presentation and experimental gaps.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>