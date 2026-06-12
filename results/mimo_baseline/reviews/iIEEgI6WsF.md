## Summary

This paper proposes On-Demand Communication (ODC), a scheme that replaces FSDP's per-layer collective communication primitives (all-gather, reduce-scatter) with point-to-point gather and scatter-accumulate operations, relaxing synchronization from layer-level to minibatch-level. This reframes FSDP as a decentralized parameter server, decoupling device execution to mitigate straggler effects under the imbalanced workloads characteristic of LLM post-training with variable-length sequences. ODC demonstrates up to 36% throughput improvement over standard FSDP on SFT and RL tasks across model sizes from 1.5B to 32B.

## Strengths

- **Clear and well-motivated problem identification**: The paper convincingly argues that the balanced workload assumption underlying collective communication is systematically violated in LLM post-training due to high variance in sequence lengths. The formalization of minibatch runtime (Eq. 1) and the quantification of up to 50% device idle time (mentioned in introduction, Table 6 reference) ground the problem empirically.

- **Clean architectural insight**: The key contribution—decomposing collective calls into on-demand point-to-point primitives that preserve FSDP's memory layout while eliminating per-layer synchronization—is elegant and practical. The mapping to a "decentralized parameter server" (Figure 6) provides a clear conceptual framework. The implementation leverages RDMA (CUDA IPC intra-node, NVSHMEM inter-node) and Triton-Distributed, making it practically feasible.

- **Comprehensive evaluation design**: The evaluation spans two important post-training tasks (SFT and RL), three datasets with genuinely different sequence length distributions (Figure 7), model scales from 1.5B to 32B, and systematic combination of communication schemes with load balancing algorithms. The parametric study (Section 5.3) isolates the effect of minibatch size, max length, packing ratio, and device count, providing actionable insights for practitioners.

- **Honest treatment of limitations**: The communication benchmark (Figure 11) transparently reveals ODC's inter-node bandwidth disadvantage, and Section 6 provides a substantive discussion of mitigations (overlapping, hybrid sharding) and future directions. The RL results are presented without inflation despite being more modest (~10%).

## Weaknesses

### Fatal
None.

### Major

- **Cross-node communication efficiency gap**: Figure 11 shows ODC achieves significantly lower bandwidth than collectives when communication spans multiple nodes (16 and 32 devices). This is a fundamental architectural limitation of point-to-point RDMA versus optimized hierarchical collectives. The paper proposes hybrid sharding (Section 6.1) as mitigation, but this trades off memory efficiency and is only shown in Appendix E. Given that large-scale LLM post-training increasingly uses multi-node setups, this limitation directly constrains the practical applicability of ODC. The paper would benefit from a more rigorous analysis of the breakeven point where ODC's imbalance tolerance outweighs its communication overhead.

- **Limited scale of evaluation**: Experiments top out at 32 GPUs and 32B parameters. Modern LLM post-training routinely uses hundreds to thousands of GPUs. The parametric study (Figure 10) suggests benefits grow with device count, but this extrapolation remains undemonstrated. With more devices, both the straggler effect (favoring ODC) and inter-node communication volume (hurting ODC) increase, making the net effect unclear without empirical validation.

### Minor

- **RL results constrained by external factors**: The 10% RL speedup is partly attributed to verl's constraint of identical samples per device, which limits LB-Mini's effectiveness. This makes the RL evaluation less informative about ODC's true potential in RL settings, which are arguably the most important application area for LLM post-training.

- **Microbatch count variability with LB-Mini**: Since LB-Mini can produce different numbers of microbatches per device, the gradient accumulation semantics require careful treatment. The paper states correctness is verified via convergence (Appendix F), but a brief discussion of how gradient averaging/weighting is handled when devices accumulate different numbers of microbatches would strengthen the paper.

### Trivial
None.

## Nice-to-Haves

- A roofline analysis or communication-computation overlap measurement showing what fraction of ODC's inter-node overhead is actually hidden by computation for typical LLM layer sizes.
- Comparison against asynchronous or semi-synchronous baselines (e.g., local SGD variants) that also relax synchronization, to contextualize ODC's position in the broader design space.
- Wall-clock breakdown showing how much of the total speedup comes from communication relaxation vs. improved load balancing (LB-Mini), since these are orthogonal contributions.

## Novel Insights

The paper's most genuinely novel observation is that FSDP's fine-grained synchronization is an artifact of the communication model rather than a requirement of the training algorithm, and that this artifact becomes a dominant bottleneck specifically in LLM post-training due to the intersection of quadratic attention costs with variable-length sequences. The reframing of FSDP as a decentralized parameter server is a useful conceptual contribution that bridges old and new paradigms. The demonstration that even state-of-the-art packing strategies cannot fully compensate for collective communication's synchronization overhead (leaving up to 50% idle time) is a valuable empirical finding that shifts attention from the packing subproblem to the communication architecture itself.

## Suggestions

- Provide a scaling study to at least 128-256 GPUs to validate ODC's applicability at practical LLM training scale, or explicitly characterize the regimes where ODC is beneficial vs. where inter-node overhead dominates.
- Quantify the relative contribution of communication relaxation versus improved load balancing by testing ODC+LB-Micro (same packing, different communication) against Collective+LB-Mini (different packing, same communication) to disentangle the two orthogonal improvements.
- Include a microbenchmark measuring actual device idle time (bubble rate) under ODC vs. Collective, not just end-to-end throughput, to directly validate the mechanism claimed in Figures 1 and 2.

## Score and Decision

This paper presents a well-motivated and practically valuable contribution to distributed LLM training. The core insight is clean, the implementation is real and open-sourced, and the evaluation demonstrates consistent improvements. However, the cross-node communication bottleneck is a significant concern that limits generalizability, and the evaluation scale (≤32 GPUs) falls short of demonstrating the approach at the scales where LLM post-training is actually conducted. The paper is honest about these limitations and proposes reasonable mitigations, but the gap between the demonstrated setting and practical deployment reduces my confidence in the reported results' broader impact.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept