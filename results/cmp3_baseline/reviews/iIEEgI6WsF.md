## Summary

This paper revisits the parameter server (PS) paradigm to address the inefficiency of FSDP under imbalanced workloads common in LLM post-training. It proposes **On-Demand Communication (ODC)**, which replaces collective all-gather/reduce-scatter with point-to-point gather and scatter-accumulate operations. This reduces synchronization barriers from per-layer to per-minibatch, decouples device execution, and enables simpler minibatch-level load balancing. Evaluated on SFT and RL tasks with models up to 32B parameters, ODC achieves up to 36% throughput improvement over standard FSDP.

## Strengths

- **Well-motivated problem.** The paper clearly identifies that workload imbalance (due to high variance in sequence lengths) is a fundamental and persistent issue in LLM post-training, and that FSDP’s per-layer collectives exacerbate this by creating synchronization barriers. The critique of existing packing-based solutions as insufficient under memory constraints is convincing.

- **Elegant, principled solution.** Replacing collectives with point-to-point operations addresses the root cause (synchronization overhead) rather than only mitigating symptoms. Framing ODC as a decentralized parameter server that preserves FSDP’s memory and scaling benefits is a clean conceptual contribution.

- **Thorough empirical evaluation.** Experiments cover two major post-training tasks (SFT and RL) across multiple model scales (1.5B–32B), datasets with different sequence length distributions, and various minibatch sizes. The parametric study (minibatch size, max length, packing ratio, device count) provides insight into when ODC is most beneficial.

- **Open-sourced implementation.** The code is publicly released, supporting reproducibility and community use.

## Weaknesses

### Fatal
None.

### Major
- **Inter-node communication efficiency is significantly lower than NCCL collectives (Figure 11).** ODC’s point-to-point primitives lag behind NCCL’s optimized collectives by a large margin (up to ~3× in the cross-node setting). The paper argues that this overhead is hidden by overlapping with computation (which scales as O(s²)) and that hybrid sharding mitigates it. However, the evidence for this claim relies on the specific long-context regimes tested. For applications with shorter sequences or smaller models where compute-to-communication ratio is lower, or when overlapping is less effective, the overhead could dominate and erode the benefits. The paper would be stronger if it quantified the impact of this overhead more directly (e.g., by presenting effective throughput after overlapping or by showing results under conditions where communication is not fully hidden).

### Minor
- **RL gains are modest (up to 10%) and partially attributed to implementation constraints.** The paper notes that verl requires identical numbers of samples per device, which limits the effectiveness of the minibatch-level load balancing (LB-Mini). This is a fair point, but it also means the results for RL are less comprehensive than for SFT.

- **The hybrid sharding mitigation (Section 6.1) is mentioned but not evaluated.** The paper suggests that hybrid sharding (sharding only within a node) can eliminate cross-node communication, but no experiments are provided. This leaves an important mitigation strategy unvalidated.

### Trivial
- Some figure captions are repetitive and contain excess text (likely parsing artifacts), but readability is not affected.

## Nice-to-Haves

- A detailed analysis of the effective throughput after overlapping communication with computation, comparing ODC and collectives in the cross-node setting.
- Empirical evaluation of the hybrid sharding strategy proposed in Section 6.1.
- A discussion of the expected performance on shorter sequences or smaller models where computation is less dominant.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Add an experiment or calculation that shows the impact of communication overhead after overlapping (e.g., profile the network idle time during training). This would strengthen the claim that inter-node overhead is effectively hidden.
- Include a table or figure evaluating the hybrid sharding approach (Section 6.1) to demonstrate its effectiveness in reducing cross-node communication costs.
- Consider discussing the scalability of ODC to larger clusters (e.g., 64+ GPUs) and whether the point-to-point pattern introduces congestion bottlenecks that collectives might avoid.

## Score and Decision

**Score:** 8  
**Decision:** Accept

**Reasoning:** The paper addresses a timely and important problem with a well-motivated, elegant solution. The empirical results are strong and the analysis is thorough. The primary concern (inter-node communication efficiency) is acknowledged and mitigated for the paper’s target use case (long-context post-training), but the lack of direct quantification of the mitigation’s effectiveness keeps the score from being higher. Overall, the contribution is significant and the paper is of high quality.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>