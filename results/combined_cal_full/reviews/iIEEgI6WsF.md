Now I have all the information needed. Let me compile the final review.

## Summary
This paper identifies a genuine problem: FSDP's per-layer collective communication (all-gather/reduce-scatter) assumes balanced workloads, but LLM post-training (SFT, RL) produces highly variable sequence lengths that violate this assumption, causing up to 50% device idle time. The paper proposes On-Demand Communication (ODC), which replaces per-layer collectives with point-to-point gather/scatter-accumulate operations, relaxing synchronization from the layer level to the minibatch level while preserving synchronous optimizer semantics. ODC reframes FSDP as a decentralized parameter server. The method consistently improves throughput across SFT and RL tasks, achieving up to 36% speedup over standard FSDP.

## Strengths
- **Well-motivated problem with concrete evidence.** The paper quantifies the problem severity (up to 50% device idle time, Section 1) and identifies the root cause: FSDP's per-layer collectives create synchronization barriers that amplify workload imbalance from variable-length sequences in LLM post-training.
- **Clean conceptual intervention.** Replacing collectives with point-to-point gather and scatter-accumulate, relaxing synchronization from per-layer to per-minibatch, is a simple and principled idea. Framing ODC as a decentralized parameter server (Section 3.1) connects the approach to a well-understood architectural lineage without requiring dedicated server nodes.
- **Consistent empirical gains across diverse settings.** Speedup over collective FSDP holds across two datasets (LongAlign, SWE-Smith), two tasks (SFT and RL), four model scales (1.5B–32B), and three device counts (8–32). Even in RL where gains are weaker (up to 10%), the direction is consistent. The improvement is not a single-point artifact.
- **Parametric study (Figure 10).** The controlled analysis of how acceleration varies with minibatch size, max length, packing ratio, and device count provides useful insight into where the method works best and why. The finding that gains increase with sequence length and device count directionally supports the paper's thesis.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- **RL evaluation is narrow relative to the paper's broad claims.** The abstract states ODC is "a superior fit for LLM post-training," which includes RL. However, the RL experiments use only one dataset (AIME), one model family (DeepSeek-R1-Distill-Qwen), and are limited to 14B/16 GPUs. More importantly, implementation constraints in `verl` require identical numbers of samples per device, which prevents the best ODC configuration (LB-Mini's different-number-of-microbatches-per-device) from being applied at all. The paper acknowledges these limitations (Section 5.2), but the gap between the broad claim and the thin RL evidence remains. The SFT evaluation is strong; the RL evidence is suggestive but insufficient to support the same level of confidence.
- **The two sources of gain are not clearly disambiguated in the headline result.** The "up to 36%" speedup blends two effects: (a) ODC's communication relaxation (relaxed synchronization), and (b) LB-Mini's minibatch-level load balancing (enabled by ODC). The paper does provide the comparison ODC+LB-Micro vs Collective+LB-Micro, which isolates effect (a) and shows lower but still positive gains (10–22% depending on settings, Figure 10). A clearer decomposition — e.g., "X% from communication relaxation alone, Y% additional from minibatch-level balancing" — would make the contribution more interpretable for readers.
- **Memory overhead of ODC's point-to-point pattern is not discussed.** The paper does not address whether ODC's gather/scatter-accumulate operations require additional buffers for outstanding requests or whether memory footprint increases compared to collective operations. For memory-constrained LLM training, this is a practical concern even if the increase is small.

### Trivial
- The paper states ODC "preserves the synchronous optimization semantics" (Section 3). The optimizer step is indeed synchronous at the minibatch boundary, but gradient accumulation across microbatches within a minibatch is now asynchronous across devices, which could produce slightly different numerical values of accumulated gradients compared to standard FSDP. The convergence verification in Appendix F addresses this, but a brief note in the main text about numerical determinism would improve precision.

## Nice-to-Haves
- A controlled experiment measuring what fraction of communication latency is actually hidden by computation overlap (e.g., artificially inflating communication latency) would strengthen the cross-node communication analysis in the main text.
- Reporting median speedup across evaluated configurations (not just "up to 36%") would give practitioners a more representative expectation.

## Removed Points
These points from the input review are flagged as removed, treat them with caution:
- **Cross-node communication overhead as a critical issue:** The paper acknowledges the bandwidth degradation (Figure 11), provides two concrete mitigations in Section 6.1 (overlap with computation, hybrid sharding), and the end-to-end results (Figures 8, 10) show consistent speedups in cross-node settings (16, 32 devices). The parametric study shows speedup increases with device count. Detailed bubble-rate data exists in Appendix G (stripped by parser but present in original submission). Per the guidelines, weaknesses about missing appendix content are removed, and the end-to-end evidence already in the main text substantiates the claim.
- **Headline "up to 36%" framing concern:** "Up to X%" is standard reporting practice. The parametric study (Figure 10) shows ODC+LB-Mini reaching ~35% at large device counts and long max lengths, consistent with the 36% claim. The paper presents detailed per-configuration results allowing readers to assess typical performance.
- **Load-balancing baseline quality concern:** The paper's core comparison (ODC+LB-Micro vs Collective+LB-Micro) isolates the communication effect using the same packing method. Asking for comparison against SOTA packing methods is scope creep; the paper's contribution is about the communication scheme, not advancing packing algorithms.
- **Missing async SGD comparison:** Explicitly discussed as future work in Section 6.2.
- **Fault tolerance concern:** Discussed as future work in Section 6.2.
- **Open-source URL missing:** Stripped by parser.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Strengthen the RL evaluation by either implementing the `verl` constraint relaxation (which the paper states is feasible) to demonstrate the full ODC+LB-Mini pipeline in RL, or adding a second RL dataset to broaden the evidence base.
- Add a brief discussion of ODC's memory overhead (buffer requirements for point-to-point communication), even if the overhead is negligible.
- Consider reporting a summary statistic (e.g., median speedup across evaluated configurations) alongside the headline "up to X%" to set more calibrated expectations.

## Score and Decision

**Calibration Anchors (all anchors retrieved across rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| 8QTpYC4smR | 1.00 | R1 | No | Survey paper, not comparable |
| 5kMwiMnUip | 1.40 | R1 | No | LLM jailbreaking, not comparable |
| bEgDEyy2Yk | 1.00 | R1 | No | Graph algorithm implementation, not comparable |
| bntJK4NyIW | 2.00 | R2 | No | Decentralized training in heterogeneous network, weaker system contribution |
| 2HN97iDvHz | 3.00 | R2 | No | LLM-powered scheduling, different focus |
| ArJikvI6xo | 3.40 | R2 | No | Federated learning agent, different focus |
| b7HOhqXiZs | 2.60 | R2 | No | Decoupled momentum optimization, theoretical focus |
| yuYMJQIhEU | 4.50 | R2 | No | Decentralized learning optimizer, theoretical focus |
| 0fpLLsAynh | 3.67 | R2 | No | Decentralized federated learning, theoretical focus |
| fhJeqL1rRg | 4.50 | R2 | No | Ensemble weight averaging, different focus |
| 1qP3lsatCR (NetMoE) | 7.20 | R2n | No | MoE training system, strong experiments like this paper, but different domain |
| 7JhGdZvW4T | 6.00 | R2n | No | LLM scheduling, different focus |
| Cs6MrbFuMq | 6.00 | R2n | No | LLM inference, different focus |
| **qDKTMjoFbC (BurstAttention)** | 5.60 | R1,R2n | **Yes** | Similar systems topic; had severe novelty (-9.75) and analysis (-6.03) weaknesses absent in this paper. This paper is clearly stronger. |
| **lo3nlFHOft (Promise to Practice)** | 6.67 | R1,R2n | **Yes** | Decentralized training; had missing related work (-8.23) and limited novelty (-5.68). This paper has milder weaknesses. |
| **tuzTN0eIO5 (Zero Bubble)** | 7.00 | R1 | **Yes** | Pipeline parallelism; standout creative insight (+7.29). This paper has a less flashy but still clean contribution with milder negatives. |
| **ZO5cn4IfaN (CO2)** | 7.00 | R1 | **Yes** | Communication-computation overlap; strong experiments but had missing comparison (-7.03) and prior work differentiation (-5.66). This paper has similar-quality experiments with milder negatives. |
| vMNpv5OBGb | 5.67 | R2n | No | Automatic parallelism, different focus |
| B5Tp4WwZl8 | 6.25 | R2n | No | Error feedback, different focus |
| lsvlvWB9vz | 6.50 | R2n | No | Compression in distributed optimization, different focus |
| omrLHFzC37 | 6.25 | R2n | No | Federated learning, different focus |
| cznqgb4DNv | 7.00 | R2n | No | Decentralized federated learning, different focus |

**Round 1 Bracket:** 6.5–7.5

**Final Score Determination:** My draft's weighted items sum to ~13.7 (strengths: +2.14, +3.93, +4.92, +5.05; weaknesses: -3.87, -0.68, -0.73, +2.96). The strongest anchors in the 6.5–7.5 range — Zero Bubble (7.00) and CO2 (7.00) — had similar or stronger positive items (+7.29 for Zero Bubble's creative insight; +6.38/+4.50 for CO2's problem motivation/experiments) but also had much heavier negatives (-7.03, -5.66, -4.41 for CO2). By contrast, this paper's only non-trivial negative is -3.87 (RL evaluation narrowness), and the paper addresses this limitation transparently. Comparing directly: this paper lacks a single "wow" creative insight on the level of Zero Bubble's backward-splitting idea, but it also has no comparably severe weaknesses. The clean idea, consistent gains, and strong parametric study place it solidly at 7.0 — a clear accept with good evidence and a well-executed system contribution.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>