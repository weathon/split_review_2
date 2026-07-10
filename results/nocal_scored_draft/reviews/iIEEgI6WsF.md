Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper proposes On-Demand Communication (ODC), which replaces FSDP's collective all-gather/reduce-scatter with point-to-point gather/scatter-accumulate operations to mitigate workload imbalance in LLM post-training. By relaxing synchronization from per-layer to per-minibatch, ODC decouples device execution and enables simpler minibatch-level load balancing (LB-Mini). Experiments on SFT and RL tasks (up to 32B-parameter models, 32 GPUs) show up to 36% throughput improvement over standard FSDP.

## Strengths

- **Well-motivated problem.** LLM post-training (SFT, RL) genuinely suffers from high variance in sequence lengths that creates workload imbalance. The paper correctly identifies per-layer FSDP synchronization barriers as the root cause, formalized in Equation (1) which cleanly captures the min-over-max bottleneck.
- **Clean and clearly communicated core idea.** Replacing collectives with point-to-point operations and reframing FSDP as a decentralized parameter server is conceptually sound. Figures 1, 2, and 6 effectively illustrate the difference.
- **Well-designed parametric study (Section 5.3, Figure 10).** Systematic variation of minibatch size, sequence length, packing ratio, and device count provides genuine insight into when ODC helps most. This is the strongest part of the evaluation.
- **Honest reporting of limitations.** The paper shows (Figure 11) that ODC's point-to-point primitives are substantially slower than NCCL collectives for inter-node communication, and discusses mitigations (overlapping, hybrid sharding) rather than glossing over the issue.
- **Consistent throughput improvements.** Across diverse SFT and RL tasks, ODC achieves up to 36% speedup over FSDP, with a meaningful baseline (Collective Native in verl) that the paper's LB-Micro packing substantially outperforms.

## Weaknesses

### Fatal
None.

### Major

- **Contradiction regarding "Collective LB-Mini" in Figure 8.** Section 5.1 states: "As *LB-Mini* can produce different number of microbatches for different devices, it applies only to ODC." Yet Figure 8 includes "Collective LB-Mini (purple triangles)" as one of five methods compared across all subplots. This is a factual inconsistency — either LB-Mini was adapted for collective communication in some way (not explained), or the figure includes a method that cannot exist by the paper's own definition. This directly undermines interpretability of the main SFT experimental results.

- **Inter-node communication gap: overlapping claim is unsubstantiated.** Figure 11 shows ODC primitives achieving substantially worse bandwidth than NCCL collectives at 16 and 32 devices (multi-node), yet Figure 10 shows ODC's acceleration ratio *increasing* with the number of devices. The paper's explanation (Section 6.1) — that computation scales as O(s²) while communication volume is constant, so overlapping hides the latency — is plausible but no runtime breakdown is provided to validate it. Without decomposing step time into computation, collective communication, ODC communication, and idle time, the reader cannot assess whether overlapping truly compensates for the bandwidth gap or whether other factors dominate.

### Minor

- **No convergence/task-quality curves in the main text.** The paper references Appendix F for convergence verification, and appendices exist in the original submission. However, for a method that changes the floating-point order of gradient accumulation, including even one loss-vs-step or loss-vs-time figure in the main text would substantially strengthen the claim that training semantics are preserved. As it stands, the main text provides no visual evidence of training quality.
  
- **RL evaluation is limited relative to the paper's scope.** Results are restricted to a 14B model on 16 GPUs with AIME prompts only, and the paper acknowledges that verl's API constraints prevented full use of LB-Mini. The observed speedup is at most 10% (vs 36% for SFT). Since "LLM Post-Training" (including RL) is central to the paper's framing, this limited evidence weakens the claim that ODC broadly benefits RL post-training.

- **"Non-intrusive" claim lacks supporting measurements.** Section 3 asserts that point-to-point transfers "do not interrupt ongoing computation" on the target device, enabled by RDMA interfaces (CUDA IPC, NVSHMEM). The mechanism description in Section 3.2 is adequate, but no latency measurements or profiling data are provided to substantiate that these transfers are indeed non-intrusive in practice.

### Trivial

- **The primitive benchmark (Section 5.4) tests ODC primitives synchronously with barriers**, which is the opposite of how ODC is designed to be used. The paper acknowledges this, but it limits what the benchmark reveals about real-world performance.

## Nice-to-Haves

- **Compare against a published SOTA packing strategy** (e.g., from the LongAlign or related literature cited in the paper) rather than only against custom baselines, to further strengthen the claim that imbalance persists even with advanced packing.
- **Provide a direct comparison against an asynchronous PS baseline** (e.g., bounded-staleness SGD) to contextualize ODC's design choice of preserving synchronous updates.

## Removed Points

The following points from the input review were removed after cross-checking against the paper. Treat them with caution if referenced:

- *"Missing baselines from cited packing literature":* The paper's contribution is about the communication scheme, not packing. LocalSort is adapted from a published method (Bai et al. 2024), and LB-Micro demonstrably outperforms the native verl implementation. This is a nice-to-have, not a weakness.
- *"Overstates the difference about synchronization barriers":* The paper already acknowledges FSDP can overlap communication with computation (line 70) but correctly notes this does not remove the synchronization points.
- *"Implementation details deferred to appendix":* Section 3.2 provides the mechanism in the main text (RDMA-based interfaces, lightweight daemon, Triton-Distributed). Adequate for a main text.
- *"LB-Mini algorithm deferred to Appendix C" / "Hybrid sharding mitigation deferred to Appendix E":* Per policy, weaknesses about appendix-deferred content are removed since appendices exist in the original submission.
- *"Scale is modest":* The paper does not claim its experiments demonstrate "large-scale" scaling for ODC; the term is only used for prior work.
- *"Parametric study compares only against LB-Micro":* This is by design to isolate the communication effect, as explicitly stated.

## Novel Insights

None beyond the paper's own contributions. The identified contradictions and evidence gaps are standard methodological concerns rather than novel observations about the paper's substance.

## Suggestions

1. **Resolve the Collective LB-Mini contradiction:** Explain how LB-Mini was adapted for collective communication (e.g., with padding to equalize microbatch counts for collectives) or remove the "Collective LB-Mini" curve from Figure 8 and adjust claims accordingly.
2. **Provide a runtime breakdown** (computation, collective communication, ODC communication, idle time) for a representative configuration to substantiate that overlapping hides ODC's inter-node communication disadvantage.
3. **Include at least one convergence/loss curve** in the main text comparing ODC and FSDP training trajectories.
4. **Add microbenchmark measurements** demonstrating that the point-to-point RDMA transfers are indeed non-intrusive (e.g., no added latency on the target device's computation stream).

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>