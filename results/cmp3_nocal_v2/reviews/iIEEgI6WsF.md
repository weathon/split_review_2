## Summary

This paper identifies that FSDP's per-layer collective communication (all-gather/reduce-scatter) creates synchronization barriers that are problematic under the imbalanced workloads of LLM post-training (where sequence length varies substantially). The authors propose On-Demand Communication (ODC), which replaces collectives with point-to-point gather and scatter-accumulate primitives, relaxing synchronization from per-layer to per-minibatch. This reframes FSDP as a decentralized parameter server. ODC is evaluated on SFT and RL tasks using models from 1.5B to 32B parameters on up to 32 GPUs, demonstrating consistent throughput improvements with up to 36% speedup over standard FSDP.

## Strengths

- **Precise root-cause diagnosis.** Section 2.2 (Equation 1) formalizes how per-layer collectives create `max_d T_{m,d,l}` barriers, correctly identifying these as a communication-model artifact rather than a training-semantics requirement. This goes beyond the typical "packing is hard" narrative.

- **Minimal, clean design.** ODC replaces only the communication primitives (all-gather → gather; reduce-scatter → scatter-accumulate) while preserving FSDP's memory layout, scalability, and ease of use. As stated in Section 3.2, integration "only requires replacing collective communication calls with ODC primitives," which is credibly simple.

- **Sound parametric study (Figure 10).** The controlled experiments varying one factor at a time from a golden setting provide actionable insight: speedup increases with sequence length and device count, and decreases with packing ratio — all internally consistent with the paper's thesis.

- **Honest about limitations.** The paper openly discusses the inter-node bandwidth gap (Figure 11), the modest RL gains (Section 5.2), and implementation constraints in verl that limit LB-Mini's effectiveness.

## Weaknesses

### Fatal

None.

### Major

None that threaten the paper's core claims. The following issues are substantive but addressable.

### Minor

- **Inconsistency between "LB-Mini applies only to ODC" and the "Collective LB-Mini" baseline.** Line 179 states that LB-Mini produces variable microbatch counts per device and therefore "applies only to ODC." Yet Figure 8 includes a "Collective LB-Mini" curve (purple triangles). The paper does not explain how minibatch-level balancing that permits variable microbatch counts can be implemented under collective communication (which requires uniform microbatch counts). This makes the "Collective LB-Mini" condition ambiguous and undermines interpretability of that specific comparison. The authors should clarify whether this is a labeling issue, an approximation, or whether some adaptation was used.

- **Headline speedup not decomposed by source.** The paper reports "up to 36% speedup over standard FSDP" (abstract, line 197) but never explicitly separates the contribution of the communication change (ODC) from the contribution of the improved load balancing (LB-Mini). The data in Figure 8 does allow readers to infer the isolated communication effect — ODC+LocalSort vs Collective+LocalSort, and ODC+LB-Micro vs Collective+LB-Micro — but the paper never states these isolated numbers. Explicitly reporting the communication-only speedup and the combined speedup as separate figures would sharpen the attribution.

- **Inter-node bandwidth gap acknowledged but not empirically resolved.** Figure 11 shows ODC primitives are 3–6× slower than collectives cross-node. The paper discusses two mitigations (overlap with O(s²) computation, hybrid sharding) and points to end-to-end speedups at 32 devices as evidence, but does not provide per-layer timing breakdowns or hybrid-sharding experiments in the main paper that would demonstrate whether the mitigations close the gap. The end-to-end results are encouraging but leave the question of how much inter-node overhead remains at larger scales (64+ GPUs).

- **RL evaluation is limited in scope.** RL experiments run only up to 14B/16 GPUs with modest gains (up to 10%), while the abstract claims "diverse LLM post-training tasks." The paper candidly acknowledges the limitations, and RL is not the primary contribution — but the evidence is thin relative to the generality claim.

### Trivial

None.

## Nice-to-Haves

- **Per-miniblock timing breakdown:** Reporting compute time, communication time (overlapped vs. non-overlapped), and idle time for ODC vs. collective would directly validate the paper's core claim that ODC reduces straggler-induced idle time. The paper references bubble rate in Appendix G (removed), so this may already exist.
- **Memory overhead:** A brief note on whether ODC's point-to-point gathers increase peak memory due to multiple outstanding communication buffers.
- **Convergence note:** A short statement in the main text (e.g., "loss curves match exactly between ODC and FSDP") would be reassuring even if Appendix F already covers this.
- **Larger-scale discussion:** The paper targets LLM post-training but evaluates only up to 32 GPUs. A qualitative discussion of how ODC would scale to 64+ GPUs would strengthen the submission.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

- *"ODC preserves synchronous optimization semantics is underspecified / lacks formal argument about data races."* — Removed because the paper addresses this: gradient accumulation is "handled by a lightweight daemon" (line 143), and the minibatch barrier ensures all gradients arrive before the optimizer step. The critic's concern about data races during scatter-accumulate is resolved by the paper's stated design. The paper's reasoning is standard and correct.
- *"Missing wall-clock time breakdown"* and *"Convergence validation"* — Referenced as deferred to appendices (Appendices G and F, respectively). The parser strips appendices, so these are not absent from the original submission.
- *Larger-scale extrapolation* — Scope creep; the paper evaluates at the scale appropriate for its claims.
- Several formatting/style nitpicks about presentation, absence of appendices, etc., which are parser artifacts or outside-scope demands.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Clarify the "Collective LB-Mini" baseline** — Either explain how minibatch-level packing is approximated under collective constraints, or correct the figure labeling.
2. **Explicitly decompose the speedup** in Section 5.2 — report the isolated communication-only speedup (e.g., "ODC+LB-Micro vs Collective+LB-Micro yields X%") alongside the combined speedup (ODC+LB-Mini vs best collective baseline).
3. **Add a brief per-layer timing breakdown** (or reference the appendix more prominently) to empirically validate that the inter-node bandwidth gap is effectively hidden by computation overlap in the tested settings.
4. **Tone down the "diverse LLM post-training" generality claim** in the abstract given the limited RL evaluation.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>