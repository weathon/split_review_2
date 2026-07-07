Now let me draft the review and do calibration.**Round 1 Bracket:** Based on the calibration, the paper sits between 6.0 and 7.0. CO2 (7.0, Accept) is a peer — broader scale experiments (128 GPUs) and convergence proofs, but targets bandwidth-constrained clusters, not imbalanced workloads. ACCO (5.0, Reject) was rejected for novelty and thin baselines. ODC is notably stronger than ACCO in novelty, motivation, and evaluation quality. `lo3nlFHOft` (6.67, Accept, decentralized training vs. All-Reduce) is the closest thematic match and represents a comparable contribution. The inter-node scalability gap and missing gradient weighting derivation in the main text pull this slightly below CO2. **Bracket: 6.0–7.0, landing at 6.5.**

---

## Summary
The paper proposes On-Demand Communication (ODC), which replaces FSDP's per-layer collective all-gather/reduce-scatter with RDMA point-to-point primitives, relaxing synchronization from per-layer to per-minibatch. This reframes FSDP as a decentralized parameter server and directly addresses workload imbalance in LLM post-training (due to variable sequence lengths), which can cause up to 50% device idle time under existing packing strategies. ODC also enables a simpler, more effective minibatch-level load balancing algorithm (LB-Mini). Empirically, ODC achieves up to 36% speedup across SFT and RL tasks on 1.5B–32B models.

## Strengths
- **Concrete problem characterization with empirical grounding.** The paper formalizes FSDP's synchronization bottleneck in Eq. (1), and grounds motivation empirically with up-to-50% device idle times (Table 6), making the case without overstating it.
- **Clean conceptual framing.** Reframing FSDP as a decentralized PS (Section 3.1) is an insightful unification that explains *why* ODC helps through a well-understood design space, not just empirical observation.
- **Broad, multi-axis evaluation.** Figure 8 covers four model sizes (1.5B–32B), two datasets with distinct length distributions, and five method configurations. The parametric study (Section 5.3, Figure 10) systematically isolates effects of minibatch size, sequence length, packing ratio, and device count — rare rigor for a systems paper.
- **Intellectual honesty on inter-node bandwidth.** Figure 11 openly shows ODC's substantially lower bandwidth vs. NCCL collectives at 16 and 32 devices, and Section 6.1 directly addresses the limitation with mechanistic explanation rather than burying it.

## Weaknesses

### Fatal
None.

### Major

- **Inter-node scalability is argued, not measured.** Figure 11 shows ODC's inter-node bandwidth is significantly below NCCL collectives at 16 and 32 devices (two- and four-node configurations). The authors argue the gap is masked by computation hiding communication (Section 6.1: "communication volume per microbatch is constant with sequence length s, whereas computation scales as O(s²)") and by hybrid sharding (Appendix E), and end-to-end results at 32 devices do show speedups. However, no profiling separates "time saved from removing stalls" from "time lost to slower communication" at multi-node scale. The device-count curve in Figure 10 varies model parameters on a *single cluster* rather than spanning additional nodes, so the claim that "larger DP scale amplifies ODC's benefit" rests on a scaling argument extrapolated from a fixed topology. Practitioners deploying at 64–256 GPUs (typical production scale for 32B+ models) cannot reliably predict ODC's behavior from this evidence.

- **Gradient weighting semantics for LB-Mini deferred without derivation.** Section 2.1 introduces per-microbatch weights $w_m$ (Eq. shown), and under LB-Mini, different devices process different numbers of microbatches and different total token counts. The paper notes "we verify convergence in Appendix F" but provides no derivation in the main text of what weighting rule is used or how it maintains equivalence to standard data-parallel averaging. This is part of the method, not a reproducibility detail — especially for RL where reward normalization interacts with gradient weighting.

### Minor

- **36% headline speedup conflates two contributions.** The 36% figure (Figure 8, SFT-SWE-Smith, 1.5B, 8 devices) compares ODC+LB-Mini against Collective+LocalSort, bundling a new communication scheme with a new load-balancing algorithm against a weak baseline. The pure communication benefit (ODC+LB-Micro vs. Collective+LB-Micro per Figure 10) is roughly 10–15%. The result is not fabricated — Collective LB-Mini is plotted and consistently underperforms — but the abstract leads with 36% without equally prominent framing of the decomposed numbers.

- **RL speedup scope insufficiently prominent.** Section 5.1 states RL experiments record only model training time, excluding actor rollout, which "can dominate RL training time." The 10% RL speedup should be more prominently scoped in the main text to avoid misinterpretation by practitioners interested in end-to-end RL wall-clock time.

### Trivial

- No error bars or run counts reported for main results in Figures 8–9. Given the inherent sequence-length variance in these datasets, run-to-run variance is plausibly non-trivial.

## Nice-to-Haves
- A breakdown profile at the 32-device, 32B configuration showing time saved from stall removal vs. time lost to slower inter-node communication would directly validate the key mitigation argument in Section 6.1.
- Memory overhead of ODC's gradient accumulation daemon and gather buffers is uncharacterized; an order-of-magnitude estimate would help practitioners in memory-constrained long-sequence settings.
- Report ODC+LB-Micro vs. Collective+LB-Micro speedup as a dedicated headline number alongside the 36% figure to let readers cleanly attribute gains to communication vs. load balancing.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **PCIe/NVLink bandwidth contention (Section 3.2):** The harsh critic raised that RDMA operations may slow compute kernels sharing interconnect bandwidth. This is speculative — the paper provides no evidence of such contention, and end-to-end intra-node results (Figures 11 and 8) show no significant degradation. Removed as unverified speculation.

- **"Statistical rigor" as a Major weakness:** Single-run reporting is the norm in systems papers at this scale; demoted to Trivial.

## Novel Insights
The reframing of FSDP as a decentralized parameter server (Section 3.1) is a genuinely unifying observation: it reveals that per-layer synchronization barriers are an artifact of collective communication, not an algorithmic requirement of sharded data parallelism. The parametric study further provides a principled characterization of ODC's operating regime — benefit increases with sequence length (due to O(s²) compute hiding O(1) communication) and with device count (due to increased heterogeneity across devices) — directly quantifying where the tradeoff between stall removal and lower bandwidth tips in ODC's favor.

## Suggestions
- Add a single profiling breakdown for the 32-device, 32B SFT configuration to directly demonstrate the stall-removal vs. communication-overhead tradeoff at multi-node scale.
- Move the gradient weighting derivation for LB-Mini from Appendix F to the main text (condensed form in Section 4), since it is part of the method's correctness argument.
- In the abstract, clarify that 36% includes both the communication and load-balancing improvements, and quote the communication-only gain separately.

## Score and Decision

**Anchor papers:**
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `lo3nlFHOft.md` | 6.67 | 1 | Closest thematic match — decentralized training vs. All-Reduce, accepted; ODC is similarly scoped and equally well-executed |
| `ZO5cn4IfaN.md` (CO2) | 7.00 | 1 | Distributed training with comm-compute overlap; has convergence proofs and 128 GPU experiments; ODC lacks these but is more focused and addresses a sharper problem |
| `UV1jr2aJ2J.md` (ACCO) | 5.00 | 1 | Rejected for novelty and weak baselines; ODC substantially stronger in motivation, evaluation, and clarity |
| `uoU4ypjAmN.md` (SPD) | 4.00 | 1 | Sync-point drop for inference; thinner contribution than ODC |
| `bntJK4NyIW.md` | 2.00 | 1 | Rejected decentralized training — weak evaluation, limited insight |
| `qDKTMjoFbC.md` | 5.60 | 1 | BurstAttention — distributed attention for long sequences; comparable systems paper, borderline accept |
| `oVnfVnwh6y.md` | 4.75 | 1 | Linear attention SP — related systems paper, borderline reject |
| `Cs6MrbFuMq.md` | 6.00 | 1 | HexGen-2 — disaggregated LLM inference; comparable scope, borderline accept |

**Round 1 bracket:** 6.0–7.0.  
**Round 2:** No additional search needed — the bracket is sufficiently narrow. ODC is stronger than the 6.0-tier anchors (HexGen-2, BurstAttention) due to cleaner framing, more rigorous parametric study, and a sharper, empirically-grounded contribution. It falls slightly below CO2 (7.0) which provides convergence proofs and scales to 128 GPUs. The two Major weaknesses (inter-node scalability evidence, missing gradient weighting derivation in the main text) are real but addressable in a rebuttal. **Final score: 6.5.**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>