Now I have enough information for calibration. Let me finalize the review.

## Summary
This paper proposes On-Demand Communication (ODC), which reframes FSDP as a decentralized parameter server by replacing per-layer collective all-gather/reduce-scatter with point-to-point RDMA-based gather and scatter-accumulate operations. ODC relaxes synchronization from layer-level to minibatch-level, enabling devices to progress independently under imbalanced workloads and unlocking simpler minibatch-level load balancing (LB-Mini). Evaluated on SFT (LongAlign, SWE-Smith) and RL (GRPO on AIME) tasks with models up to 32B on up to 32 GPUs, ODC achieves up to 36% throughput improvement over standard FSDP.

## Strengths
1. **Well-motivated and architecturally clean insight.** The paper correctly identifies that FSDP's per-layer collectives create synchronization barriers ill-suited to LLM post-training's variable-length sequences. The core idea — replacing collectives with point-to-point operations and reframing FSDP as a decentralized parameter server — is crisp and principled (lines 101-119). Equation (1) cleanly formalizes the FSDP synchronization bottleneck.

2. **Honest disclosure of limitations.** Section 5.4 (Figure 11) openly benchmarks that ODC's primitives are significantly slower than NCCL collectives in cross-node settings. The paper discusses mitigations (communication-computation overlap, hybrid sharding) rather than hiding this weakness. This transparency is commendable for a systems paper.

3. **Reasonably broad evaluation scope.** The paper tests SFT on two datasets and RL (GRPO) across four model sizes (1.5B-32B), device counts (8-32), and minibatch sizes. The parametric study (Section 5.3, Figure 10) systematically examines how sequence length, packing ratio, and device count affect speedup, providing useful guidance for practitioners.

4. **The evaluation includes ODC+LB-Micro vs Collective+LB-Micro** (Figure 8), giving readers data to partially isolate the pure communication effect from the combined system effect, even though the headline presentation does not cleanly separate them.

## Weaknesses

### Major
1. **The 1-device data point in Figure 10 reveals an unexplained artifact that undermines the parametric study's interpretation.** At 1 device there is no inter-device communication, yet ODC+LB-Micro shows ~10% acceleration vs Collective+LB-Micro, and ODC+LB-Mini shows ~25%. Since the communication scheme cannot produce any effect at 1 device, these gaps must come from implementation-level differences in local data handling or measurement artifacts — not from the paper's central thesis about synchronization barriers. This contaminates the interpretation of every other data point in Figure 10, because the reader cannot separate how much of the acceleration at larger device counts is due to communication decoupling vs. baseline-comparison artifacts. For example, at the golden setting (8 devices), ODC+LB-Micro shows ~15% acceleration, but with a ~10% artifact baseline at 1 device, the true communication-driven gain may be only ~5%. The paper must explain this artifact and adjust the interpretation accordingly.

2. **The cross-node primitive weakness is acknowledged but not adequately reconciled with the headline speedups.** Figure 11 shows ODC's gather and scatter-accumulate achieve substantially lower bandwidth than NCCL collectives at 16 and 32 devices — precisely the settings where the headline 36% speedups are reported (14B model on 16 devices, 32B model on 32 devices). The paper's main mitigation argument — communication-computation overlap — is equally available to FSDP (Section 2.2 explicitly notes modern FSDP already overlaps communication with computation). The claim that ODC overlaps "particularly effectively" (line 243) because computation scales as O(s²) while communication is constant is not specific to ODC; the same arithmetic applies to FSDP. The paper never provides a runtime decomposition (profiled time in communication vs. idle vs. computation) to substantiate that the load-balancing benefit outweighs the communication penalty at these scales, leaving a gap in the evidence chain for the headline results.

3. **The headline "up to 36% speedup" conflates communication decoupling and load-balancing effects without clean separation.** The 36% number comes from ODC+LB-Mini vs a collective baseline (Figure 8). LB-Mini is only compatible with ODC, so the comparison combines the effect of eliminating per-layer synchronization barriers AND using a more effective load-balancing algorithm. While the paper does include ODC+LB-Micro vs Collective+LB-Micro (isolating the communication effect), the abstract and introduction present the 36% figure as a property of ODC's communication scheme without clarifying the decomposition. The paper would be stronger if it explicitly stated: "ODC's communication scheme alone provides X% speedup; the additional Y% comes from LB-Mini load balancing enabled by ODC."

### Minor
4. **RL gains are modest (up to 10%) and context is not fully discussed.** The paper candidly explains this is due to implementation constraints in verl and less long-tailed sequence length distributions. However, the paper does not estimate what fraction of realistic LLM post-training workloads fall into the high-benefit regime (long-tail, long-sequence SFT) vs. the low-benefit regime (RL with bounded sequence lengths). This limits practical guidance.

5. **Equation (1) formalizes FSDP's runtime but no ODC equivalent is provided.** Providing the analogous equation for ODC (where the max is over all layers and microbatches within a minibatch rather than per-layer) would sharpen the formal comparison and make the theoretical advantage precise. As written, the paper claims ODC removes layer-level sync but doesn't model the consequence.

### Trivial
6. **The paper claims "ODC is open-sourced" (line 9, line 145) but the URL is empty in the extracted text.** This is a reproducibility concern if the link is genuinely missing from the submission, though the extracted text may have stripped it.

## Nice-to-Haves
- A clean runtime decomposition (profiled time in communication, computation, and idle) for ODC vs. FSDP at identical settings.
- Memory overhead analysis (RDMA buffers, gradient accumulation daemon).
- Scalability discussion beyond 32 GPUs, where the cross-node penalty would grow.
- Convergence curves in the main text rather than the appendix.

## Removed Points
These points from the input review were removed with justification:
- "ODC's point-to-point scheduling logic / deadlock avoidance is not described" — Implementation details are delegated to Appendix B (stripped by the extraction parser; exists in the original submission).
- "LB-Micro may not be equivalent to what the collective baseline would use" — LB-Micro is a strong baseline the authors designed; the paper also includes LocalSort (no packing) as a simpler baseline; RL results show LB-Micro substantially outperforms verl's native implementation, confirming its strength.
- "Missing convergence curves in main text / correctness validation" — The paper states ODC preserves synchronous optimization semantics (line 25); if gradients are identical, convergence follows by construction. Empirical verification in the appendix is supplementary, not a main-text requirement for a systems paper.
- "Equation (1) notation is imprecise" — The equation cleanly captures the synchronization bottleneck motivating the paper; not imprecise for its purpose.
- "Missing related work" — Cannot be verified without external sources.
- Formatting nitpicks, grammar, and parser artifacts.

## Novel Insights
None beyond the paper's own contributions. The key observation — that FSDP's per-layer collectives are an artifact of the communication model rather than a training requirement and can be replaced by point-to-point operations without altering training semantics — is the paper's own contribution, not something surfaced by the reviews.

## Suggestions
1. **Address the 1-device artifact**: Explain why ODC+LB-Micro vs Collective+LB-Micro shows ~10% at 1 device in Figure 10. If this is measurement noise or a local-implementation difference, quantify it and adjust the interpretation of all other data points by subtracting this baseline artifact.
2. **Provide a profiled runtime decomposition**: Show wall-clock time broken into communication, computation, and idle for ODC vs. FSDP at a representative setting (e.g., 14B model, 16 devices, LongAlign). This would directly answer whether the load-balancing benefit outweighs the cross-node communication penalty.
3. **Separate communication and load-balancing effects in the headline claims**: State explicitly what speedup is attributable to ODC's communication scheme alone vs. the combined ODC+LB-Mini system.

### Calibration

**Calibration anchors consulted:**
| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| SPD (sync-point drop for TP inference) | 4.00 | 1 | Similar sync-reduction idea but for inference, weaker evaluation; our paper is stronger |
| ACCO (communication hiding in LLM training) | 5.00 | 1, 2 | Similar distributed training efficiency problem; our paper has more novel core idea |
| "From Promise to Practice" (decentralized training) | 6.67 | 1 | More thorough theory/runtime model but different focus; comparable quality |
| CO2 (full comm-computation overlap) | 7.00 | 1 | Extensive evaluation (128 GPUs), convergence proofs; our paper is weaker on theory/scale |
| Decentralized Training in Heterogeneous Network | 2.00 | 1 | Limited novelty; our paper is significantly stronger |
| OMNIBAL (computation balance in VL) | 5.00 | 2 | Similar load-balancing focus, weaker evaluation |
| SEPARATE (gradient compression) | 6.00 | 2 | Solid theory and evaluation; comparable quality |
| DynMo (dynamic load balancing) | 5.25 | 2 | Similar problem, different domain |
| LASP (sequence parallelism) | 4.75 | 2 | Point-to-point communication for SP; our paper addresses a different problem |

**Round 1 bracket:** I initially identified the paper as plausibly sitting between 4.5 and 6.5 based on its contributions (novel core idea, decent evaluation, but significant interpretive issues).

**Narrowing:** After reading full reviews of anchors in the 4-7 range and comparing specifics: the paper has a more novel core insight than ACCO (5.00) and a broader evaluation than SPD (4.00) or LASP (4.75), but lacks the theoretical rigor and scale of "From Promise to Practice" (6.67) or CO2 (7.00). The strengths (clean architectural insight, honest limitations, broad evaluation) are balanced by the weaknesses (1-device artifact, cross-node reconciliation gap, conflation of effects). This places the paper above reject-quality but below the stronger systems papers that also provide theoretical analysis or larger-scale validation.

**Final score:** 5.5 — a borderline accept with a solid core contribution that is undermined by presentation and interpretive issues that are fixable.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>