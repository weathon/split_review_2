## Summary
This paper identifies that the per-layer all-gather/reduce-scatter collectives in FSDP create synchronization barriers that amplify straggler effects under imbalanced workloads common in LLM post-training. To address this, the authors propose On-Demand Communication (ODC), which replaces collectives with point-to-point operations, effectively relaxing synchronization from layer-level to minibatch-level and reframing FSDP as a decentralized parameter server. Empirical evaluations across SFT and RL tasks show consistent throughput improvements, up to 36% over standard FSDP, demonstrating a practical and elegant solution to a real bottleneck in modern distributed training.

## Strengths
- **Clear problem identification and motivation:** The paper convincingly argues that the shift from balanced workloads (e.g., vision) to imbalanced workloads (LLM post-training with variable sequence lengths) fundamentally breaks the implicit assumption behind collective communication. This motivates the need for a paradigm shift, not just a better packing algorithm.
- **Elegant and practical solution:** ODC is a surprisingly simple modification—replacing collectives with point-to-point primitives while preserving FSDP’s memory layout and semantics. This avoids complex system engineering (no separate server nodes) and is directly integrable into existing FSDP codebases.
- **Strong empirical validation:** The evaluation covers two major post-training tasks (SFT and RL), multiple model sizes (1.5B–32B), multiple datasets with realistic length distributions (LongAlign, SWE-Smith, AIME), and up to 32 GPUs. The parametric study further isolates the effect of minibatch size, sequence length, packing ratio, and device count, providing a thorough understanding of when ODC helps most.
- **Honest discussion of limitations:** The paper openly acknowledges and analyzes the inter-node communication overhead of point-to-point vs. hierarchical collectives (Section 6.1) and suggests practical mitigations (overlap, hybrid sharding). This transparency strengthens the credibility of the work.
- **Reproducibility orientation:** The authors state they will open-source the implementation and integrate it into FSDP, which is valuable for the community.

## Weaknesses
### Fatal
None.

### Major
- **Inter-node communication inefficiency is only partially addressed:** The paper admits that ODC’s point-to-point primitives are significantly slower than NCCL collectives across nodes (Figure 11). While overlapping computation with communication works for long sequences, the parametric study shows that acceleration drops when packing ratio is high or sequences are short. The proposed hybrid sharding is mentioned but not experimentally validated in the main results; its effectiveness remains unquantified under realistic settings.
- **Limited scope to post-training only:** The paper frames ODC as a solution for LLM post-training (SFT, RL), but does not discuss applicability to pre-training, where workload is generally more balanced and collective communication is well-established. This is a reasonable scope choice, but the title and abstract may overclaim generality. The paper would benefit from clarifying whether the same imbalanced conditions arise in pre-training at scale.

### Minor
- **Lack of comparison to asynchronous training methods:** ODC preserves synchronous minibatch semantics and relaxes only per-layer barriers. The paper mentions future work on asynchronous updates, but a comparison to existing asynchronous FSDP variants or asynchronous PS systems (even if not exact fits) would help contextualize the contribution.
- **No analysis of memory overhead for gather/caching:** ODC fetches parameters on demand from peers; if multiple layers need the same shard concurrently, there might be repeated transfers or caching overhead. The paper does not discuss memory implications for the gather buffer or whether caching can help.
- **Implementation relies on specific RDMA interfaces (CUDA IPC, NVSHMEM):** While these are available on A100 clusters, not all GPU clusters have NVSwitch or NVSHMEM support. The paper could briefly discuss fallback strategies for environments with only NCCL or MPI.

### Trivial
- The phrase “Our implementation of ODC and integration with FSDP is open-sourced at .” has an empty URL in the abstract; presumably will be filled.

## Nice-to-Haves
- An ablation experiment showing the effect of overlapping computation with communication for ODC vs. collectives under varying sequence lengths.
- A practical guide or rule-of-thumb for when to use ODC vs. standard FSDP based on sequence length distribution and cluster topology.

## Novel Insights
Beyond the paper’s own technical contribution, the key insight is that the synchronization granularity in sharded data parallelism (FSDP) is an artifact of the communication primitive choice, not a requirement of the optimizer. By decoupling the per-layer barriers via point-to-point communication, the authors reveal that the entire problem of load balancing can be shifted from the microbatch level to the minibatch level, which is both simpler and more effective. This reframing of FSDP as a decentralized parameter server bridges two historically separate system designs (PS and collective communication) in a way that preserves the memory and scalability advantages of the former while adding the robustness of the latter to heterogeneous workloads.

## Suggestions
- Consider adding an experiment with hybrid sharding (parameter sharding only within nodes) to quantify the inter-node communication overhead reduction under realistic settings (e.g., medium-length sequences, 16+ GPUs).
- Clarify the scope of the contribution in the introduction: explicitly state that the paper targets post-training, where workload imbalance is most severe, and discuss briefly whether pre-training might also benefit.
- Provide a practical decision tree or heuristic: given a cluster topology and workload (sequence length distribution, minibatch size), when should a practitioner choose ODC vs. standard FSDP?

## Score and Decision
Score: 8 – accept. The paper presents a clear, well-motivated, and empirically validated improvement to a critical part of the modern LLM training stack. The solution is elegant, practical, and open-source. The weaknesses are acknowledged and do not invalidate the contribution. I expect this work to have significant impact on practitioners and to open new directions for combining PS principles with collective communication systems.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>