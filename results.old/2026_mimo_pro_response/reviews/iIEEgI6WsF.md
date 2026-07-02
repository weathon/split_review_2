Now I have enough information to calibrate. Let me write the final review.

## Summary

This paper proposes On-Demand Communication (ODC), which replaces FSDP's per-layer collective communication with point-to-point gather/scatter-accumulate primitives, relaxing synchronization from per-layer to per-minibatch granularity. This reframes FSDP as a decentralized parameter server and enables simpler minibatch-level load balancing (LB-Mini). The evaluation demonstrates up to 36% throughput improvement on SFT tasks across model scales 1.5B–32B, multiple datasets (LongAlign, SWE-Smith, AIME), and both SFT and RL tasks.

## Strengths

- **Well-motivated and practically relevant problem**: The paper provides concrete evidence that imbalanced sequence lengths in LLM post-training cause up to 50% device idle times even with state-of-the-art packing (Table 6, Appendix G). The theoretical motivation is sound: O(s) memory vs O(s²) compute scaling for sequence length s explains why microbatch-level packing has fundamental limits (Section 4, lines 151–155).
- **Clean architectural design preserving FSDP benefits**: ODC preserves FSDP's memory layout and sharding while replacing collectives with targeted gather/scatter-accumulate operations (Section 3, Figure 5). The reframing as a decentralized PS with co-located server/worker roles (Section 3.1, Figure 6) is well-articulated. The RDMA-based implementation (CUDA IPC intra-node, NVSHMEM inter-node, Triton-Distributed kernel) is practical and the paper commits to open-sourcing.
- **Comprehensive evaluation with controlled parametric study**: Results span SFT and RL tasks, three datasets, model scales 1.5B–32B, and multiple load-balancing strategies (Figures 8–9). The parametric study (Section 5.3, Figure 10) systematically varies one factor at a time from a golden setting, showing acceleration increases with sequence length and device count and decreases with packing ratio — all consistent with the paper's thesis.
- **Practical load-balancing simplification validated empirically**: LB-Mini outperforms LB-Micro at small minibatch sizes (Figure 8), validating the theoretical argument that minibatch-level balancing is more effective when devices can have different microbatch counts. As minibatch size increases, LB-Micro catches up — a natural and consistent pattern.

## Weaknesses

### Fatal
None.

### Major

- **Collective LB-Mini baseline contradicts the paper's own design statement**: Section 5.1 explicitly states "LB-Mini can produce different number of microbatches for different devices, it applies only to ODC" (line 179). Yet Figure 8 prominently displays a "Collective LB-Mini" baseline across all SFT subplots. If LB-Mini requires ODC's variable-microbatch capability, what exactly does the Collective variant do? Does it force uniform microbatch counts (undermining LB-Mini's advantage), or is the statement about exclusivity wrong? This confusion matters because gains from "ODC LB-Mini" over "Collective LB-Mini" would conflate the communication-scheme benefit with the load-balancing benefit — precisely the decomposition the paper needs to clarify.

- **Sources of improvement not explicitly decomposed**: ODC combines two somewhat independent mechanisms: (a) point-to-point communication replacing collectives, and (b) LB-Mini replacing microbatch-level balancing. The main results present only combinations. From Figure 8 one can partially extract this: comparing ODC+LB-Micro vs. Collective+LB-Micro isolates the communication effect (~5–15%), and comparing ODC+LB-Mini vs. ODC+LB-Micro isolates LB-Mini. But the paper never discusses this decomposition. For the headline 36% speedup, understanding the relative contributions of each mechanism is important for both scientific understanding and practical adoption decisions.

### Minor

- **No error bars or variance estimates on throughput numbers**: All throughput measurements in Figures 8, 9, 10 are single-point values. For a systems paper evaluating wall-clock throughput on shared hardware, some measure of run-to-run variability would strengthen confidence in the reported differences, especially for smaller gaps (e.g., the ~5% differences in some RL settings).

- **Parametric study limited to 1.5B model**: The golden setting (Table 1) uses 1.5B on 8 devices. While the "Devices" factor scales to 32 (spanning multiple nodes, Figure 10), all other parametric variations hold model size at 1.5B. Since the main evaluation shows ODC working across 1.5B–32B, confirming that the parametric trends (minibatch size, max length, packing ratio) hold for larger models would strengthen generalizability.

### Trivial
None.

## Nice-to-Haves
- Decompose bubble-rate data into the main text (currently Appendix G); the ~50% idle time claim is a key motivating fact that would be more impactful with direct comparison.
- Characterize the compute-to-communication ratio at which ODC's cross-node bandwidth disadvantage (Figure 11) might negate its straggler-tolerance benefit, even as a simple analytical model.
- Add memory overhead analysis comparing ODC's point-to-point buffering vs. collective communication memory footprint, given LLM training's memory-bound nature.

## Removed Points
These points are flagged to be removed, treat them with caution:

- **Cross-node overhead as a central unresolved weakness**: The harsh critic claims the parametric study only tests on a single node (1.5B/8-GPU) and that the paper provides no cross-node evidence. This is inaccurate: the "Devices" parametric variation goes to 32 devices (Figure 10, line 221), spanning multiple nodes, and still shows increasing acceleration ratios. The main evaluation includes 14B/16-GPU and 32B/32-GPU configurations which necessarily span nodes with the 8-GPU NVSwitch intra-node setup. The paper is transparent about the inter-node primitive bandwidth gap (Figure 11, Section 6.1) and proposes concrete mitigations (overlap via O(s²) compute hiding communication, hybrid sharding). While cross-node remains a limitation worth future work, it is not the unstested gap the critic claims.

- **RL evaluation ignoring rollout time as a weakness**: The paper explicitly states "we only record the model training time in RL, ignoring forward-only parts like actor rollout" (Section 5.1, line 163). This is a reasonable scoping decision for evaluating the communication scheme's impact on training throughput specifically, not a missing analysis.

## Novel Insights

The paper's core insight — that FSDP's collective communication implicitly enforces balanced workloads through per-layer synchronization barriers, and that decomposing collectives into point-to-point operations can relax this to minibatch-level synchronization — is a genuine and well-executed contribution. The connection between classical PS architecture and modern FSDP's decentralized parameter management (Section 3.1) provides a clean conceptual reframing. The observation that memory-compute mismatch (O(s) vs O(s²)) creates fundamental limits for microbatch-level packing offers a principled argument for why coarser-grained balancing is structurally better, not just incrementally more convenient.

## Suggestions

- Add a table or figure explicitly decomposing throughput gains into: (1) ODC communication effect (ODC+LB-Micro vs. Collective+LB-Micro, same LB) and (2) LB-Mini effect (ODC+LB-Mini vs. ODC+LB-Micro, same communication). This is the single most informative addition.
- Clarify what "Collective LB-Mini" actually implements. If it forces uniform microbatch counts, acknowledge the comparison conflates communication and load-balancing effects.
- Include at least basic error bars (e.g., 3-run standard deviation) for the main throughput results.

## Calibration Anchors

| Anchor | Path | Avg Score | Round | Comparison |
|--------|------|-----------|-------|------------|
| Decentralized Training of Transformer Models (Heterogeneous) | bntJK4NyIW | 2.00 | 1 | Much weaker technical contribution and evaluation; ODC is significantly stronger |
| DeMo: Decoupled Momentum Optimization | b7HOhqXiZs | 2.60 | 1 | Broader but vaguer contribution; ODC has clearer problem and stronger evaluation |
| SPD: Sync-Point Drop for TP | uoU4ypjAmN | 4.00 | 1 | Narrower scope (inference-only), less comprehensive evaluation; ODC is more impactful |
| Linear Attention Sequence Parallelism | oVnfVnwh6y | 4.75 | 1 | Narrow niche (linear attention SP); ODC targets broader, more relevant problem with better evaluation |
| ACCO: Accumulate while you Communicate | UV1jr2aJ2J | 5.00 | 1 | Similar topic area but weaker novelty claims, unclear advantages; ODC is better motivated and evaluated |
| FlashDP: Memory-Efficient DP-SGD Training | cZZMC8VFZc | 5.00 | 1 | Different focus (DP-SGD); ODC addresses more fundamental synchronization issue |
| SEPARATE: Low-rank Gradient Compression | 8HuLgtjqOD | 6.00 | 1 | Solid systems contribution with 2× speedup on communication compression; comparable quality to ODC but different angle |
| From Promise to Practice: Decentralized Training | lo3nlFHOft | 6.67 | 1 | Strong decentralized training paper with runtime model and convergence proof; slightly stronger theoretical contribution than ODC |
| CO2: Full Communication-Computation Overlap | ZO5cn4IfaN | 7.00 | 1 | More theoretically grounded (convergence proof), broader scalability (128 GPUs), addresses similar communication challenge; stronger overall |

**Round 1 bracket**: Based on these anchors, the paper sits between 5.5 and 7.0. It is clearly stronger than ACCO (5.0, rejected) and comparable to SEPARATE (6.0, accepted). It is slightly weaker than "From Promise to Practice" (6.67) due to the Collective LB-Mini contradiction and lack of decomposition, and weaker than CO2 (7.0) which has stronger theoretical grounding. I place it at **6.5** — a solid systems contribution with a well-motivated problem, clean design, and comprehensive evaluation, but held back by the Collective LB-Mini inconsistency and the unanalyzed decomposition of its two intertwined contributions.

**Final score**: 6.5

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>