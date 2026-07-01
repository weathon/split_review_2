##Summary

This paper identifies that the per-layer collective communication (all-gather, reduce-scatter) in FSDP creates fine-grained synchronization barriers that cause significant device idle time under the imbalanced workloads common in LLM post-training (due to high variance in sequence lengths). To address this, the authors propose On-Demand Communication (ODC), which replaces collectives with point-to-point gather and scatter-accumulate operations, effectively reframing FSDP as a decentralized parameter server. ODC relaxes synchronization from per-layer to per-minibatch, decouples device progress, and enables simpler minibatch-level load balancing. Experiments on SFT and RL tasks with models up to 32B parameters show consistent throughput improvements, achieving up to 36% speedup over standard FSDP.

## Strengths

- **Clear problem identification and motivation**: The paper convincingly demonstrates that the balanced-workload assumption underlying collective communication is violated in LLM post-training, and that this leads to substantial inefficiency in FSDP. The analysis of why existing packing strategies are insufficient under memory constraints is well-argued.
- **Novel and well-grounded solution**: Revisiting the parameter server paradigm and adapting it to modern sharded DP is a fresh perspective. ODC is elegantly simple—replacing collectives with point-to-point primitives while preserving FSDP’s memory layout and synchronous semantics—and the connection to decentralized parameter servers is clearly explained.
- **Thorough empirical evaluation**: The paper evaluates ODC across multiple model scales (1.5B–32B), datasets with different sequence length distributions (LongAlign, SWE-Smith, AIME), and tasks (SFT and RL). The parametric study (varying minibatch size, max length, packing ratio, device count) provides valuable insights into when ODC is most beneficial.
- **Honest discussion of limitations**: The paper openly acknowledges the inter-node communication bandwidth gap between ODC primitives and NCCL collectives, and discusses practical mitigations (overlapping, hybrid sharding). This transparency strengthens the paper’s credibility.

## Weaknesses

### Fatal
None.

### Major
- **Inter-node communication overhead is a significant practical concern**: Figure 11 shows that ODC primitives have substantially lower bandwidth than NCCL collectives when communication spans multiple nodes. While the paper argues that overlapping with computation and hybrid sharding can mitigate this, the experiments do not isolate the impact of this overhead. The reported speedups may not generalize to settings where computation cannot fully hide communication (e.g., small models, short sequences, or low packing ratios). A more detailed analysis or ablation on this point would strengthen the paper.
- **Hardware and software dependencies limit generalizability**: The implementation relies on RDMA (CUDA IPC, NVSHMEM) and Triton-Distributed, which may not be available in all clusters (e.g., those using InfiniBand without NVSHMEM support). The paper claims open-sourcing, but the current evaluation is tied to a specific hardware setup. The feasibility of porting ODC to other interconnects is not discussed.

### Minor
- **Load balancing baselines could be stronger**: The paper compares against LocalSort and LB-Micro, but does not include more sophisticated packing strategies from the literature (e.g., those that jointly optimize memory and compute). While LB-Micro is shown to be faster than the native verl implementation, it is a heuristic; a comparison with a more principled packing method would better contextualize the benefits of LB-Mini.
- **RL experiments are less compelling**: The speedups in RL (up to 10%) are smaller than in SFT, and the experiments are limited to 16 GPUs. The paper attributes this to implementation constraints in verl and less long-tailed distributions, but the results are less definitive. The claim that ODC is a “superior fit” for LLM post-training would be stronger with more extensive RL evaluation.
- **Gradient accumulation semantics are not fully detailed**: The scatter-accumulate operation is described as pushing gradients to the owning device, but it is not entirely clear how this interacts with gradient accumulation across microbatches (e.g., whether the accumulation happens on the server side or requires additional synchronization). A more precise description would aid reproducibility.

### Trivial
- The paper could benefit from a brief discussion of memory overhead: ODC may require additional buffers for point-to-point communication compared to in-place collectives.

## Nice-to-Haves

- An ablation study that isolates the contribution of ODC’s decoupled progress from the improved load balancing (LB-Mini) would help quantify the source of speedups.
- A comparison with asynchronous training approaches (e.g., stale synchronous parallel) would provide context for the future work section.
- A discussion of how ODC handles fault tolerance or elasticity, given the paper’s mention of these as advantages of parameter servers.

## Novel Insights

The central insight is that the per-layer synchronization barriers in FSDP are an artifact of the collective communication model, not a requirement of the training algorithm. By decomposing all-gather and reduce-scatter into point-to-point operations, the synchronization granularity can be relaxed to the minibatch level without changing training semantics. This reframing of FSDP as a decentralized parameter server is a fresh perspective that opens up new optimization opportunities (e.g., asynchronous updates, elasticity) beyond the immediate throughput gains demonstrated.

## Suggestions

- Provide experiments that isolate the effect of inter-node communication overhead, e.g., by comparing ODC with and without computation-communication overlap, or by using hybrid sharding to eliminate cross-node transfers.
- Include a comparison with a version of ODC that uses hierarchical communication (e.g., intra-node collectives + inter-node point-to-point) to address the bandwidth gap.
- Discuss the feasibility of implementing ODC on other interconnects (e.g., InfiniBand with GPUDirect RDMA) and any required changes.

## Score and Decision

**Score**: 8  
**Decision**: Accept

The paper makes a strong, well-motivated contribution to distributed training for LLMs. It identifies a real and growing problem (workload imbalance in post-training), proposes a clean and effective solution (ODC), and supports it with thorough experiments and honest discussion of limitations. The work is likely to have practical impact and to inspire further research on adapting parameter server ideas to modern training paradigms. The weaknesses are not fatal and can be addressed in future work or discussion.

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>