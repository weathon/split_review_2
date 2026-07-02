Now I have strong calibration context. Let me compose the final review.

## Summary

This paper proposes On-Demand Communication (ODC), which replaces FSDP's per-layer collective all-gather/reduce-scatter with point-to-point gather/scatter-accumulate operations for LLM post-training. By relaxing synchronization from per-layer to per-minibatch, ODC decouples device progress under the imbalanced workloads characteristic of LLM post-training (SFT and RL with variable-length sequences). ODC also enables minibatch-level load balancing (LB-Mini) that lets devices process different numbers of microbatches. Experiments on 1.5B–32B models with up to 32 GPUs show consistent throughput improvements.

## Strengths

1. **Well-motivated diagnosis with a concrete formalization.** Section 2.2 pinpoints the root cause of inefficiency: FSDP's per-layer collectives create fine-grained synchronization barriers that force all devices to wait for the slowest one at every layer. Equation (1) formalizes this — the minibatch runtime equals the sum over layers of the max over devices — converting an intuitive observation into a precise, actionable target. This diagnosis is specific and correct.

2. **Clean, minimally invasive system design.** ODC replaces FSDP's collective calls with p2p gather and scatter-accumulate operations while preserving FSDP's memory layout, sharding scheme, and synchronous optimization semantics. The abstraction boundary is clean: integration requires only swapping collective calls for ODC primitives (Section 3.2). The use of RDMA (CUDA IPC intra-node, NVSHMEM inter-node) via Triton-Distributed ensures data transfers are non-intrusive — they do not interrupt computation on the target device. This is well-engineered.

3. **Consistent empirical gains across diverse settings.** Figures 8 and 9 show throughput improvements for all evaluated configurations: two SFT datasets (LongAlign, SWE-Smith), RL (GRPO on AIME), model sizes from 1.5B to 32B, device counts from 8 to 32, and across minibatch sizes and packing ratios. The gains are not conditional on a narrow configuration. The parametric study (Figure 10) further shows that acceleration grows with factors that exacerbate imbalance (longer sequences, more devices).

4. **Honest treatment of limitations.** The paper explicitly discusses that ODC's p2p primitives have significantly lower bandwidth than NCCL collectives in multi-node settings (Section 5.4, Figure 11), that RL gains are smaller (10% vs 36%) due to verl's uniform-samples-per-device constraint (Section 5.2), and that hybrid sharding (Section 6.1) is presented as a future direction rather than a resolved result. This candor strengthens credibility.

## Weaknesses

### Fatal
None.

### Major

1. **"Collective LB-Mini" in Figure 8 is contradictory and unexplained.** Section 5.1 states: *"As LB-Mini can produce different number of microbatches for different devices, it applies only to ODC."* Yet Figure 8 (the main results figure) reports results for "Collective LB-Mini" (purple triangles) without any explanation of how this method operates. If LB-Mini assigns different numbers of microbatches per device — its defining feature — it fundamentally cannot run with collective communication (which requires all devices to participate in every all-gather/reduce-scatter). If "Collective LB-Mini" instead uses the same sample-to-device assignment but forces uniform microbatch counts (e.g., by padding), that is a different algorithm and must be described. This ambiguity undermines the reader's ability to interpret the paper's central comparison figure. The paper's conclusion may still be correct, but a key comparison arm is currently uninterpretable.

### Minor

2. **The "up to 36% speedup" headline is not precisely attributed.** The abstract says "over standard FSDP" and Section 5.2 says "the most pronounced gains observed under packing, reaching up to a 36% speedup." The reader cannot determine from the text whether 36% comes from ODC+LB-Mini vs Collective+LocalSort, ODC+LB-Mini vs Collective+LB-Micro, or another specific pair. The 36% likely conflates two distinct sources of gain — communication decoupling (ODC alone) and improved load balancing (LB-Mini). The paper should specify the exact comparison pair and ideally decompose the gain into these two components.

3. **Inter-node communication overhead at scale is discussed but not bounded.** Figure 11 shows ODC primitives are significantly slower than NCCL collectives in multi-node settings (the bandwidth gap at 32 devices appears substantial). The paper argues this overhead is hidden by computation scaling as O(s²) while communication scales as O(s), and proposes hybrid sharding as a mitigation. However, no analysis or evidence characterizes the crossover point where this overhead could erase the synchronization benefit. The parametric study (Figure 10) varies devices up to 32 but only with a 1.5B model; the interaction of model scale with device count at larger scales is unexplored. The paper's claim that ODC is "a superior fit" could potentially be qualified by the scale regime where this holds.

4. **RL evaluation tests only the communication-decoupling component, not the full system.** The paper acknowledges that verl's constraints require identical numbers of samples per device, limiting LB-Mini's effectiveness in RL. This means the reported 10% RL speedup comes solely from replacing collectives with p2p, not from minibatch-level load balancing. The paper should explicitly separate these two sources of gain when discussing RL results.

5. **Memory bandwidth contention from p2p RDMA is not discussed.** When multiple fast devices simultaneously gather parameters from or push gradients to the same slower device, memory bandwidth contention on the target could slow its computation, partially offsetting the decoupling benefit. This is a known concern in p2p schemes and is not addressed in the paper.

### Trivial

- The parametric study (Figure 10) uses the smallest model (1.5B) and does not include model size as a variable. Since Figure 8 shows different speedup magnitudes for different model sizes, this dimension is worth probing in the study.

## Nice-to-Haves

- **Decompose the speedup.** Separately report the two components: (a) communication-decoupling alone (ODC+LB-Micro vs Collective+LB-Micro) and (b) load-balancing improvement (ODC+LB-Mini vs ODC+LB-Micro). A table with exact numerical values would complement the figures.
- **Add a simple analytical bound** characterizing where inter-node communication overhead would erase the synchronization benefit. Even a rough back-of-envelope calculation would strengthen claims about scalability.
- **Memory bandwidth measurement.** An experiment measuring per-device memory bandwidth contention under ODC vs collectives would address the p2p concern.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Criticism about Table 6 (50% idle time claim):** The table is in the appendix, stripped by the parser. Per instructions, criticisms about missing appendix content are removed.
- **Criticism about LB-Mini algorithm not described in main text and deferred to Appendix C:** Stripped by parser; removed per instructions.
- **Criticism about hybrid sharding (Section 6.1) not evaluated:** The paper cites Appendix E, which is stripped. Removed per instructions.
- **Criticism about convergence verification in appendix:** Stripped; removed per instructions.
- **Criticism about PS framing being rhetorical:** The paper acknowledges the colocated-roles distinction and the framing does not depend on the analogy being perfect. This is an observation, not a weakness.
- **Criticism about Equation (1) not discussing M=1 edge case:** Overly nitpicky; removed.
- **Criticism about missing detailed convergence numbers in main text:** Related to appendix content; removed.
- **Criticism about communication benchmark not capturing async advantage:** The paper benchmarks synchronously "for fairness" to measure raw bandwidth. The benchmark's purpose (measuring primitive bandwidth) is clear and appropriate; the end-to-end experiments capture the async advantage.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Resolve the "Collective LB-Mini" ambiguity immediately.** Either explain how this method operates (if it uses the LB-Mini assignment but forces uniform microbatch counts through padding, describe this explicitly) or, if it cannot be meaningfully defined, remove it from the figures and discussion.

2. **Clarify the 36% speedup claim.** State explicitly: (a) which specific pair of methods produces this number, (b) what "standard FSDP" means in this context (presumably Collective+LocalSort), and (c) how much of the gain comes from switching to p2p vs. from the improved load balancing.

3. **Add at least a brief discussion of the crossover scale** where inter-node communication overhead could offset ODC's synchronization benefit. Even a paragraph analyzing the trade-off between communication volume and computation as a function of model size and device count would be valuable.

## Score and Decision

**Round 1 bracket:** 5.5–7.0 (based on comparison to similar systems papers — CO2 at 7.0, NetMoE at 7.2, From Promise to Practice at 6.67, ACCO at 5.0).

**Anchors retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| CO2 (ZO5cn4IfaN) | 7.00 | 1 | Similar systems paper on communication optimization; stronger scale (128 GPUs) and convergence proof; ODC is more novel but smaller-scale |
| NetMoE (1qP3lsatCR) | 7.20 | 1 | MoE communication optimization; comparable scale (32 GPUs) and clean formulation; ODC similarly well-engineered |
| ACCO (UV1jr2aJ2J) | 5.00 | 1 | Communication hiding for LLM training; rejected for lack of novelty; ODC is more novel but has presentation issues |
| From Promise to Practice (lo3nlFHOft) | 6.67 | 1 | Decentralized training analysis; has analytical model and 64 GPU eval; ODC has cleaner empirical results |
| BurstAttention (qDKTMjoFbC) | 5.60 | 2 | Distributed attention; rejected; ODC is stronger |
| SEPARATE (8HuLgtjqOD) | 6.00 | 2 | Gradient compression; accepted; comparable in contribution strength |
| Don't Stop Me Now (7JhGdZvW4T) | 6.00 | 2 | LLM scheduling; accepted; comparable systems contribution |

**Final score determination:** The paper's core contribution — identifying that FSDP collectives are a poor fit for imbalanced workloads and replacing them with p2p communication — is genuinely novel, well-motivated, and empirically validated. The design is clean and minimally invasive. These strengths place it clearly above papers like ACCO (5.0) and BurstAttention (5.6). However, the "Collective LB-Mini" contradiction in the main results figure is a real presentation issue that makes a key comparison uninterpretable, and the evaluation scale (up to 32 GPUs) and lack of scalability analysis are meaningful limitations. Compared to CO2 (7.0) and NetMoE (7.2), which have stronger evaluations and cleaner presentations, this paper sits slightly lower. It aligns well with papers scoring around 6.0 (SEPARATE, Don't Stop Me Now) in terms of contribution quality and presentation clarity.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>