Now let me synthesize my findings and write the final review.

## Summary
This paper proposes On-Demand Communication (ODC), which replaces the per-layer all-gather/reduce-scatter collectives in FSDP with point-to-point gather/scatter-accumulate primitives for LLM post-training. By reframing FSDP as a decentralized parameter server, ODC relaxes synchronization from once per layer to once per minibatch, decoupling device progress and enabling minibatch-level load balancing (LB-Mini). Across SFT and RL tasks with models up to 32B on up to 32 GPUs, ODC consistently improves throughput, achieving up to 36% speedup over standard FSDP.

## Strengths
- Well-motivated problem with concrete evidence: the paper identifies that FSDP's per-layer collectives create synchronization points that amplify idle time under the workload imbalance caused by variable sequence lengths, citing device idle times up to 50% even with state-of-the-art packing (Section 1). This is a genuine and practically important bottleneck in LLM post-training.
- Clean architectural insight: reframing FSDP as a decentralized parameter server by replacing all-gather/reduce-scatter with point-to-point gather/scatter-accumulate. The observation that synchronization barriers are an artifact of the communication model, not a requirement of the training algorithm (Section 3), is a useful and clearly articulated insight.
- The load-balancing simplification (LB-Mini) is a nontrivial secondary contribution: by decoupling device progress, ODC enables minibatch-level load balancing where devices can process different numbers of microbatches. The paper correctly identifies that this removes a fundamental constraint on packing algorithms (Section 4).
- Reasonably broad evaluation covering SFT on two datasets (LongAlign, SWE-Smith) with different sequence length distributions, plus RL (GRPO on AIME). Model scales span 1.5B to 32B, device counts from 8 to 32, with a parametric study (Figure 10) systematically varying key factors. The paper is also transparent about its limitations (cross-node communication overhead, RL constraints, need for hybrid sharding).

## Weaknesses

### Fatal
None.

### Major
- **Underspecified "Collective LB-Mini" baseline in Figure 8.** Section 5.1 states that LB-Mini "can produce different number of microbatches for different devices" and therefore "applies only to ODC." Yet Figure 8 includes "Collective LB-Mini" as one of the five compared methods. The paper does not explain how a minibatch-level load-balancing algorithm that produces uneven microbatches per device is implemented with collective communication (which requires tight synchronization at each layer). If devices with fewer microbatches must idle during others' extra microbatches, or if the assignment is modified to equalize microbatches, this needs to be stated explicitly. Without clarification, the interpretation of the main result figure is ambiguous.

### Minor
- **Cross-node communication bandwidth gap lacks direct time breakdown.** Figure 11 shows ODC's point-to-point primitives lag significantly behind NCCL collectives across nodes. Section 6.1 argues this is hidden by the quadratic attention cost (O(s²) computation vs. O(1) communication per microbatch with respect to sequence length). The end-to-end throughput results in Figure 8 support this claim (ODC wins overall), but a direct computation-vs-communication wall-time breakdown for the largest multi-node configuration (e.g., 32B/32 devices) would make the argument rigorous rather than relying on a qualitative assertion.

- **RL evaluation tests only the communication benefit, not the full ODC+LB-Mini system.** Section 5.2 explains that implementation constraints in verl require identical numbers of samples per device, limiting LB-Mini's effectiveness. The RL results (up to 10% speedup) therefore isolate only the communication-side improvement, not the combined ODC+LB-Mini benefit that drives the headline 36% SFT speedup. The paper is transparent about this, but it means the paper's strongest result may not fully transfer to the RL setting as evaluated.

- **The 36% speedup claim is not tied to a specific experimental configuration.** The claim appears in the abstract, introduction, and conclusion, but the paper never states which configuration (model, dataset, minibatch size, device count) produces this maximum gain. The reader must infer it from Figure 8, which would be easier if the paper explicitly called out the winning configuration.

### Trivial
None.

## Nice-to-Haves
- A controlled microbenchmark that artificially stalls one device and measures idle time under ODC vs. collectives would directly demonstrate the decoupling benefit without the confound of different load-balancing strategies.
- A computation/communication overlap ratio measurement for the end-to-end experiments would substantiate the claim that the quadratic attention cost hides cross-node communication latency.

## Removed Points
These points from the input review are flagged to be removed; treat them with caution:
- Criticisms about Equation (1) not accounting for communication overlap: the equation is a simplified model for illustrating the synchronization barrier, not a precise performance model.
- Concern that the 50% idle time motivation is in the appendix: standard placement for detailed measurements; the main paper states the claim.
- Complaint that hybrid sharding is "pushed to the discussion section": this is standard paper organization.
- Claim about missing convergence plots in the main paper: stated to be in Appendix F, which was stripped by the parser.
- Request for ZeRO++ baseline comparison: beyond the paper's stated scope.
- Various style/presentation nitpicks and speculative criticisms lacking concrete paper evidence.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Clarify what "Collective LB-Mini" means in Figure 8 — explicitly describe how LB-Mini's minibatch-level assignment (potentially uneven microbatches) is used with collective communication, including any padding or idling required.
2. Provide a communication vs. computation time breakdown for the 32B/32-device SFT experiment to directly validate the overlap-hides-cross-node-latency argument.
3. State explicitly which experimental configuration yields the 36% speedup figure.
4. If feasible, relax the verl constraint to demonstrate ODC+LB-Mini's full benefit in the RL setting.

## Calibration Summary

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| Decentralized Training in Heterogeneous Network | bntJK4NyIW.md | 2.00 | R1 | Yes | Much weaker: unclear contributions, no formal algorithm description, limited novelty |
| From Promise to Practice (Decentralized Training) | lo3nlFHOft.md | 6.67 | R1,R2 | Yes | Similar domain (distributed communication); that paper had a runtime model + convergence proof but major related-work omissions; our paper has a cleaner contribution but less theory |
| CO2 (Communication-Computation Overlap) | ZO5cn4IfaN.md | 7.00 | R1,R2 | Yes | Most topically similar; had theoretical proof and larger-scale experiments (128 GPUs) but faced novelty concerns about the core overlap idea not being new; our paper has a more novel core idea but narrower evaluation |
| QSR (Synchronization Rule) | yroyhkhWS6.md | 6.75 | R2 | Yes | More theoretical; mixed reviews (8,6,5,8); our paper is more of a systems contribution |
| NetMoE (MoE Communication) | 1qP3lsatCR.md | 7.20 | R2 | Yes | MoE domain; similar systems-optimization style; our paper has comparable strength but smaller scale |
| BurstAttention | qDKTMjoFbC.md | 5.60 | R2 | No | Different subproblem (distributed attention); scored lower |

**Round 1 bracket**: After comparing against the calibration anchors, the paper sits between the 5.5–7.5 band, closest to the 6.67–7.00 range.

**Round 2 narrowing**: Compared to CO2 (7.00), the reviewed paper lacks a theoretical convergence proof and operates at smaller scale (32 vs. 128 GPUs), and has the confusing Collective LB-Mini baseline issue. Compared to From Promise to Practice (6.67), the reviewed paper has a cleaner contribution and no major related-work gaps. The Collective LB-Mini underspecification (favorability 3.21) is a real weakness but less severe than CO2's most damaging items (novelty concerns with favorability -0.22 to -0.38). The 36% claim not being config-tied (favorability -1.12) is the worst-rated item, but this is a presentation fix. The paper's strengths score very high (favorability 13.62 for evaluation breadth, 10.72 for motivation). Overall: borderline accept with fixable evidential gaps.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>