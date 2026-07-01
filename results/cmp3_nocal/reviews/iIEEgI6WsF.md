## Summary

This paper identifies that FSDP's per-layer collective communication (all-gather/reduce-scatter) creates synchronization barriers that are problematic under the imbalanced workloads characteristic of LLM post-training (due to high sequence-length variance). The authors propose On-Demand Communication (ODC), which replaces per-layer collectives with point-to-point RDMA primitives, relaxing synchronization from per-layer to minibatch-level while preserving FSDP's memory layout and synchronous training semantics. ODC also enables minibatch-level load balancing (LB-Mini) that allows different numbers of microbatches per device. Experiments on SFT and RL tasks with models up to 32B and 32 GPUs show up to 36% throughput improvement over standard FSDP.

## Strengths

- **Clean, principled design that follows directly from problem analysis.** The paper correctly identifies the root cause (per-layer synchronization barriers from collectives under imbalanced workloads) and proposes a targeted remedy (replace collectives with point-to-point ops, relaxing synchronization to the minibatch boundary). The reframing of FSDP as a decentralized parameter server (Section 3.1, Figure 6) is conceptually elegant, colocating server/worker roles to preserve FSDP's memory and scaling benefits while gaining imbalance tolerance.

- **Minibatch-level load balancing (LB-Mini) is a genuine secondary contribution.** By eliminating the requirement for uniform microbatch counts across devices (Section 4), ODC enables a simpler and, as shown in the parametric study (Figure 10), often more effective load balancing strategy. This is not merely a consequence of ODC but a practical advantage that follows from removing per-layer synchronization constraints.

- **Informative parametric study and honest limitation disclosure.** The parametric study (Figure 10) is well-designed, varying one factor at a time from a golden setting, and shows clearly when ODC helps most (longer sequences, more devices, moderate minibatch sizes). The paper consistently acknowledges limitations: inter-node communication overhead (Figure 11, Section 6.1), the RL implementation constraint that limits LB-Mini effectiveness (line 199), and the narrowing gap at larger minibatch sizes (line 201).

## Weaknesses

### Fatal
None.

### Major

- **"Collective LB-Mini" baseline in Figure 8 is unexplained and appears to contradict the paper's own setup.** The paper states (line 179): *"As LB-Mini can produce different number of microbatches for different devices, it applies only to ODC."* Yet Figure 8's legend includes "Collective LB-Mini (purple triangles)" as one of five compared methods. The paper provides no explanation of what this baseline is. If LB-Mini truly requires variable microbatch counts, it cannot be combined with collective communication (which forces uniform per-layer synchronization). This is not a minor labeling issue — without clarification, readers cannot determine whether the comparison is fair. The paper should either (a) explain what "Collective LB-Mini" means and how it was implemented despite the stated incompatibility, or (b) remove it from the figure if it was included in error. The core claim about ODC's advantage does not depend on this one baseline (ODC+LB-Micro vs. Collective+LB-Micro and ODC+LB-Mini vs. Collective+LB-Micro both support the paper's conclusion), but the inconsistency undermines confidence in the presentation.

### Minor

- **RL evaluation cannot exercise ODC's primary load-balancing advantage.** The paper acknowledges (line 199) that implementation constraints in verl require identical sample counts per device, which prevents LB-Mini from being used effectively. The up-to-10% RL speedup therefore comes only from ODC's synchronization-benefit (effect a: eliminating per-layer barriers), not from load balancing (effect b). The paper does not isolate these two contributions, so it is unclear how much of the SFT speedup (up to 36%) comes from each mechanism. A controlled experiment comparing ODC+uniform microbatch counts vs. ODC+LB-Mini would cleanly separate the two effects.

- **The tension between growing acceleration with device count and cross-node communication overhead is not explicitly addressed.** The parametric study (Figure 10) shows ODC's acceleration increasing with the number of devices (~25% at 1 device to ~35% at 32 devices for ODC+LB-Mini). Yet the communication benchmark (Figure 11) shows ODC's point-to-point primitives are significantly slower than NCCL collectives when communication spans multiple nodes (16–32 GPUs). The paper discusses both results separately but does not reconcile why the acceleration still grows despite the widening raw bandwidth gap. The likely explanation (imbalance-mitigation benefits dominate) should be stated explicitly.

- **Memory implications of the hybrid sharding mitigation are not quantified in the main text.** The paper proposes hybrid sharding (Section 6.1) as a mitigation for cross-node overhead, noting it increases per-node memory usage. The text calls this "manageable" and references Appendix E, but the main evaluation does not report the resulting memory footprint. Since FSDP's memory efficiency is core to its value, the trade-off between memory cost and communication benefit should be stated quantitatively.

### Trivial

- The paper claims the PS architecture is "naturally better suited" for LLM post-training (line 27). This is slightly overstated — ODC borrows the communication pattern of PS (point-to-point) but discards its key architectural properties (asynchrony, dedicated servers, fault tolerance). The framing could be more precise.

## Nice-to-Haves

- **Separate and measure the two sources of ODC's speedup.** A controlled experiment isolating (a) synchronization barrier removal from (b) minibatch-level load balancing would strengthen the analysis.
- **Include a memory comparison** (peak activation memory, parameter buffer memory) between ODC and FSDP, given that ODC's gather operations may have different memory dynamics.
- **Results at larger scales** (64–128 GPUs) would strengthen the claims about scalability, particularly given the cross-node communication concerns.
- **Comparison to ZeRO++** or similarly optimized hierarchical sharding strategies would be a natural and informative additional baseline, though this is beyond the paper's stated scope.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Questioning existence/availability of cited models or benchmarks** — REMOVED per hard rules.
- **Demand for a ZeRO++ baseline comparison** — REMOVED as scope creep; the paper discusses ZeRO++ in the future work/hybrid sharding context but does not claim to beat it.
- **Generic criticisms about missing convergence proofs, reproducibility, or "could be a proxy metric" speculation** — REMOVED as they either misunderstand the paper or are not grounded in specific paper content.
- **Request for larger datasets or more models** — REMOVED as the current evaluation is already adequate for the claims (1.5B–32B, three datasets, two training paradigms).
- **Style/formatting nitpicks** — REMOVED per hard rules (these are parser artifacts, not author errors).
- **Criticism that the overlap argument depends on long sequences despite small minibatch sizes** — REMOVED because the datasets used (LongAlign mean 16K tokens, SWE-Smith mean 34K tokens) are indeed long-context, so the concern is not grounded in the paper's actual data.

## Novel Insights

None beyond the paper's own contributions. The harsh review correctly identifies the "Collective LB-Mini" inconsistency but does not surface any deeper flaw in the method's soundness or evaluation beyond what the paper already addresses or acknowledges.

## Suggestions

1. **Clarify the "Collective LB-Mini" baseline immediately.** Explain what it is, how it was implemented given the stated incompatibility, and whether it should be interpreted differently. If it was an error, remove it.
2. **Add an ablation experiment** comparing ODC with uniform microbatch counts vs. ODC + LB-Mini to decompose the speedup into synchronization benefit and load-balancing benefit.
3. **Explicitly reconcile** the growing acceleration with device count (Figure 10) against the cross-node communication overhead (Figure 11) in the main text.
4. **State the memory overhead of hybrid sharding** quantitatively (e.g., parameter memory increase vs. activation memory savings) to substantiate the claim that it is "manageable."
5. **In the RL results**, either implement LB-Mini within the verl framework or clearly state that the reported speedup represents only the synchronization-removal benefit of ODC.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>