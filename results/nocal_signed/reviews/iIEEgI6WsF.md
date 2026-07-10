Now I have all the information needed. Let me produce the final consolidated review.

---

## Summary

This paper identifies a genuine limitation of FSDP under the imbalanced workloads prevalent in LLM post-training: per-layer collectives (all-gather/reduce-scatter) create synchronization barriers that cause faster devices to idle. The authors propose On-Demand Communication (ODC), which replaces these collectives with point-to-point gather/scatter-accumulate primitives, relaxing synchronization from per-layer to per-minibatch while preserving FSDP's memory layout. ODC also enables a simpler minibatch-level load balancing scheme. Experiments on SFT (LongAlign, SWE-Smith) with 1.5B–32B models on up to 32 GPUs show up to 36% throughput improvement, and RL (GRPO on AIME) shows up to 10% improvement.

---

## Strengths

- **Well-motivated and precisely articulated diagnosis of a real problem.** The paper clearly explains why FSDP's per-layer collectives assume balanced workloads, a premise violated by variable sequence lengths in LLM post-training. Equation (1) — minibatch runtime as a sum over per-layer max-device times — formally captures the inefficiency. This is not a manufactured problem.

- **Clean, minimally invasive design.** ODC replaces collective all-gather/reduce-scatter with point-to-point gather/scatter-accumulate while preserving FSDP's parameter sharding and synchronous optimizer semantics. The reframing of FSDP as a decentralized parameter server (Section 3.1) is conceptually tidy. Integration requires only replacing collective communication calls with ODC primitives.

- **Minibatch-level load balancing is a genuine second-order contribution.** Because ODC decouples device progress, it allows devices to process different numbers of microbatches. This shifts the load balancing problem from the tightly memory-constrained microbatch level to the less constrained minibatch level — a clean insight that follows naturally from the communication redesign (Section 4).

- **Well-designed parametric study (Section 5.3, Figure 10).** Isolating the effects of minibatch size, max sequence length, packing ratio, and device count reveals where ODC helps most and where the advantage narrows. The trends (speedup grows with sequence length and device count, shrinks with packing ratio) align directly with the paper's stated mechanism.

---

## Weaknesses

### Major

- **Collective LB-Mini inconsistency in Figure 8.** Section 5.1 explicitly states: *"As LB-Mini can produce different number of microbatches for different devices, it applies only to ODC."* Yet Figure 8 includes a "Collective LB-Mini (purple triangles)" curve across all eight subplots of the main results. This directly contradicts the paper's own definition. The paper must clarify what this curve actually represents — whether it is a different algorithm, a labeling error, or an invalid combination — and justify whether the comparison with ODC variants is fair. Since this is the main results figure, the inconsistency undermines trust in the experimental design and must be resolved.

### Minor

- **RL evaluation scope is limited relative to claims of generality.** The RL experiments cover only one task (GRPO on AIME prompts) with up to 14B parameters on 16 GPUs, achieving at most ~10% speedup. The paper acknowledges these limitations (implementation constraints in verl, less long-tailed distributions), but the abstract's claim of "Across diverse LLM post-training tasks" overstates the evidence from a single RL task at modest scale.

- **Inter-node communication evidence is indirect.** Figure 11 shows ODC's gather and scatter-accumulate have substantially lower bandwidth than NCCL collectives at 16–32 devices. The paper argues this is mitigated by computation-communication overlap (since compute scales as O(s²) while communication is O(s)) and hybrid sharding, but provides no per-microbatch timing breakdown (compute vs. communication vs. idle time) in the main paper to directly confirm that communication is fully hidden. The parametric study's finding that speedup grows with device count is consistent with ODC's straggler-tolerance mechanism, but could also partly reflect NCCL collective overheads at scale, and this alternative explanation is not explicitly ruled out.

- **Single model family.** All experiments use DeepSeek-R1-Distill-Qwen models. While scaling from 1.5B to 32B is reasonable, testing on one additional architecture (e.g., Llama or Mistral) would strengthen claims of generality.

### Trivial

- **No wall-clock breakdown.** The paper reports samples per second but does not decompose time into compute, communication, and idle components. Such a breakdown would directly demonstrate that ODC's gains come from reduced synchronization idle time rather than other sources.

---

## Nice-to-Haves

- A per-device timeline trace (real runs, analogous to Figure 2) comparing ODC vs. collective under identical workloads would make the causal link between communication redesign and speedup directly visible.
- Clarify the overhead and behavior of the "lightweight daemon" handling gradient accumulation (Section 3.2): does accumulation happen immediately upon arrival (interrupting the target device) or is it deferred/batched?
- A brief discussion positioning ODC relative to loosely-synchronous or asynchronous training approaches would help contextualize the work.

---

## Removed Points

These points were flagged in the input review but are excluded from the main assessment per policy:

1. **"Table 6 (50% idle time) in stripped appendix cannot be verified"** — REMOVED: the appendix exists in the original submission; the parser strips appendices from all papers.
2. **"Hybrid sharding results deferred to Appendix E"** — REMOVED: same reason as above.
3. **"Bubble rate and packing algorithm details deferred to Appendices G and C"** — REMOVED: same reason as above.
4. **"No comparison with alternative async approaches (e.g., DiLoCo)"** — REMOVED: per policy, do not assert missing related works without external sources.
5. **"Lightweight daemon overhead / gradient accumulation timing underspecified"** — REMOVED: moved to Nice-to-Haves; these are implementation details that do not affect the paper's core claims.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

- In Figure 8, either clarify what "Collective LB-Mini" represents (if it is a valid algorithm, describe it; if it is a labeling error, correct it) or remove the curve and adjust the comparison accordingly.
- Add a per-microbatch timing decomposition (compute, communication, idle) for at least one representative setting to directly demonstrate the mechanism behind ODC's speedups.
- For the RL experiments, consider testing on at least one additional task or at larger scale to strengthen the generality claim, or temper the "diverse tasks" language in the abstract.

---

## Score and Decision

The paper addresses a real problem with a clean, well-motivated design. The core contribution — replacing FSDP's per-layer collectives with point-to-point communication to tolerate workload imbalance — is sound and supported by substantial empirical evidence on SFT tasks. However, the inconsistency between the paper's stated definition of LB-Mini (applicable only to ODC) and the "Collective LB-Mini" curve in the main results figure (Figure 8) is a concrete flaw that must be resolved. The RL evidence is also thinner than the paper's generality claims suggest. These are fixable issues; with clarification of the Figure 8 inconsistency, this would be a clear acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>