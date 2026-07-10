## Summary

This paper proposes **On-Demand Communication (ODC)**, which replaces FSDP's collective all-gather and reduce-scatter with point-to-point RDMA-based communication primitives, effectively reframing FSDP as a decentralized parameter server. This relaxes synchronization from once per layer to once per minibatch, eliminating per-layer straggler effects under imbalanced workloads common in LLM post-training. ODC also enables simpler minibatch-level load balancing (LB-Mini) since devices no longer need uniform microbatch counts. Across SFT and RL tasks on models up to 32B parameters and 32 GPUs, ODC achieves consistent throughput improvements — up to 36% over standard FSDP.

## Strengths

- **Elegant conceptual reframing (Section 3.1, Figure 6):** Treating FSDP as a decentralized parameter server by colocating server and worker roles within FSDP's existing sharded layout is a genuinely insightful perspective. It preserves FSDP's memory and scaling advantages while gaining the straggler tolerance of a parameter server — a clean synthesis of two paradigms.
- **Principled load-balancing simplification (Section 4):** ODC's decoupling of device progress removes the requirement for uniform microbatch counts per device, enabling minibatch-level balancing (LB-Mini). This follows directly from the communication change rather than being an add-on, making the overall method feel coherent rather than patched together.
- **Parametric study (Figure 10):** A controlled experiment isolating the effects of minibatch size, max sequence length, packing ratio, and device count provides genuine insight into *when* ODC helps. The result that acceleration grows with sequence length and device count is informative and non-obvious, especially given the inter-node bandwidth disadvantage.
- **Honest treatment of the inter-node bottleneck (Section 5.4, Figure 11):** The paper transparently benchmarks ODC primitives against collectives cross-node, acknowledges the bandwidth disadvantage, and discusses concrete mitigations (overlapping computation, hybrid sharding). This candor strengthens rather than weakens the contribution.
- **Clear problem formalization (Equation 1, Section 2.2):** The per-layer max-over-devices bottleneck is captured precisely, making the root cause of inefficiency under imbalanced workloads unambiguous.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Unexplained "Collective LB-Mini" baseline in Figure 8.** The paper states at line 179 that LB-Mini "applies only to ODC" because it produces different numbers of microbatches per device, yet Figure 8's caption lists "Collective LB-Mini (purple triangles)" as a baseline. The paper never explains what this denotes (e.g., LB-Mini's sample-to-device assignment enforced with uniform microbatch counts for collective execution). This is confusing and needs clarification. The claim is not a fatal contradiction — "Collective LB-Mini" likely uses the LB-Mini assignment with enforced uniform microbatch counts — but the paper should spell this out explicitly.

- **The "up to 36% speedup" headline is not attributed to a specific configuration.** The abstract, introduction, and Section 5.2 state "up to 36% speedup" without specifying which model size, dataset, minibatch size, or baseline yields this number. The parametric study (Figure 10) shows ~35% for ODC+LB-Mini at max length 128K and at 32 devices, but the main experiments (Figure 8) use datasets (LongAlign mean 16.5K, SWE-Smith mean 34.7K) with different length distributions. Tying the claim to an explicit setting would aid verifiability.

- **RL evaluation does not exploit ODC's key advantage.** Section 5.2 notes that implementation constraints in verl require identical samples per device, limiting LB-Mini's effectiveness. The paper states "relaxing this constraint is feasible, we did not do so, as the current solution is easier to integrate" (line 199). The RL speedup (up to 10%) is substantially smaller than the SFT speedup, and not demonstrating the heterogeneous-microbatch capability in the RL setting weakens the RL results.

- **Evaluation scale is modest for a systems paper targeting LLM post-training.** Experiments run on up to 32 A100 GPUs. The parametric study shows acceleration increasing with device count (Figure 10), but only reaches 32 devices (4 nodes). For LLM post-training at hundreds-to-thousands of GPUs, it remains unclear whether the trend continues or reverses at larger multi-node scales given the inter-node bandwidth disadvantage (Figure 11).

### Trivial

- **The "lightweight daemon" for gradient accumulation (line 143) is mentioned but its CPU/GPU overhead is not quantified.** A microbenchmark showing the daemon's overhead would help assess practicality at scale.

## Nice-to-Haves

- For the RL experiments, consider relaxing the verl constraint that requires identical samples per device — this would let LB-Mini run fully and likely improve the RL speedup substantially.
- Consider bringing the hybrid sharding evaluation (currently Appendix E) into the main paper as a table or figure showing ODC vs. ODC+hybrid vs. collective at 32 devices, to directly address the inter-node bandwidth concern.
- A brief discussion of whether the nondeterministic accumulation order in scatter-accumulate (due to floating-point non-associativity) could cause numerical differences compared to FSDP's reduce-scatter would be thorough.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Criticism about Table 6 / 50% idle time claim being in appendix:** The paper references Table 6 (in appendix) for the 50% idle time claim. The parser strips appendix content from all papers; this existed in the original submission. **REMOVED per hard rules.**
- **Criticism about packing algorithms deferred to Appendix C:** The paper states detailed packing algorithms are in Appendix C. Appendix content is stripped by the parser. **REMOVED per hard rules.**
- **Criticism about convergence/loss curves not in main paper:** Convergence validation is in Appendix F, which is stripped. **REMOVED per hard rules.**
- **Criticism about "Collective LB-Mini" being an infeasible method:** The harsh critic called this a contradiction that "undermines the reader's confidence." This overstates the issue — the more likely interpretation is that LB-Mini's sample assignment is used with enforced uniform microbatch counts for collective execution. Kept as a minor weakness (naming confusion), not a fatal contradiction.
- **Criticism about hybrid sharding evaluation being in Appendix E:** The paper presents hybrid sharding as a mitigation in Section 6.1 and cites Appendix E for results. Appendix content is stripped. The end-to-end results at 32 devices (Figure 8, multi-node) already demonstrate ODC works despite the cross-node bandwidth disadvantage. **REMOVED per hard rules.**
- **Criticism about the synchronous launch benchmark understating ODC's advantage:** The reviewer correctly notes this works in ODC's favor (actual performance is better than the benchmark suggests). This is a positive observation, not a weakness. **REMOVED.**
- **Training semantics equivalence question:** The reviewer questions whether gradients are mathematically identical. The paper asserts identical semantics (line 103) and validates convergence. This is a reasonable question but not a demonstrated weakness. **REMOVED.**
- **Missing related works / baseline demands:** The reviewer demands specific additional baselines and comparisons. These reflect reviewer preferences rather than identified flaws in the paper's coverage. **REMOVED.**

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Clarify what "Collective LB-Mini" means in Figure 8: does it use LB-Mini's sample-to-device assignment with enforced uniform microbatch counts under collective communication? The current text says LB-Mini "applies only to ODC," which directly contradicts the figure.
2. Attribute the specific configuration that yields the "36% speedup" (model, dataset, minibatch size, baseline) explicitly in the text.
3. For the RL experiments, relax the verl constraint that requires identical samples per device to demonstrate ODC's heterogeneous-microbatch capability in the RL setting.
4. Consider adding a microbenchmark quantifying the overhead of the gradient accumulation daemon.

## Score and Decision

**Calibration summary:** The paper was compared against anchors retrieved across all score bands. The most topically relevant were: *Decentralized Training of Transformer Models in Heterogeneous Network* (avg 2.00, weak novelty and unrealistic assumptions — current paper is far stronger), *Elastic Load Balancing for Dynamic LLMs* (avg 3.67, limited novelty — current paper has stronger novelty), *From Promise to Practice: Decentralized Training* (avg 6.67, accepted, has a -10.00 impact weakness on missing related work), *CO2* (avg 7.00, accepted, has multiple -8 to -10 impact weaknesses), *NetMoE* (avg 7.20, accepted, has -7 to -10 impact weaknesses), *Smalltalk* (avg 7.33, accepted, has -5.84 and -9.85 impact weaknesses). The current paper's itemized impact scores show strengths at +9.56 to +9.99 and weaknesses at -1.62 to -0.00 — a much cleaner profile than any anchor in the 6.5–7.5 range. The strongest weakness (-1.62 for the "Collective LB-Mini" naming confusion) is an order of magnitude smaller than the decisive weaknesses that pull the anchors down. The evaluation scale (32 GPUs) is the main limitation relative to CO2 (128 GPUs) and NetMoE (32 GPUs, comparable). Overall the paper is stronger than the 7.0–7.3 anchors due to its cleaner weakness profile and more novel conceptual contribution, but falls short of the 8.0+ band due to modest scale and the RL evaluation gap.

**Round 1 bracket:** 6.5–8.0. **Round 2 narrowing:** 7.0–8.0. **Final score anchoring:** Between CO2 (7.00, with high-impact weaknesses) and the 8.0 anchors (no topically similar 8.0+ systems paper was retrieved). The paper shares CO2's high-impact empirical strengths but lacks CO2's high-magnitude weaknesses; it has a genuinely novel conceptual contribution that CO2 and NetMoE lack but a less extensive evaluation than CO2.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>