The calibration search tool is encountering a persistent file-access error in its index. I will proceed with calibration using my own judgment, drawing on knowledge of comparable papers.

Let me now produce the final review.

---

## Summary

This paper proposes On-Demand Communication (ODC), a scheme that replaces FSDP's collective all-gather and reduce-scatter with point-to-point RDMA transfers for LLM post-training. ODC relaxes synchronization from per-layer to per-minibatch, eliminating idle time from workload imbalance across devices. It also introduces LB-Mini, a load-balancing strategy enabled by ODC's decoupled execution. Evaluations on SFT and RL tasks show consistent throughput improvements (up to 36%) over standard FSDP.

## Strengths

1. **Identifies a genuine and well-motivated problem.** The paper correctly pinpoints the mismatch between FSDP's per-layer collective synchronization and the imbalanced workloads characteristic of LLM post-training (Section 3, line 101). Equation 1 formalizes the minibatch runtime bound as a sum over layer-level maxes, and the paper reports device idle time reaching 50% even with state-of-the-art packing (Section 1, referencing Table 6 in the appendix).

2. **Clean, principled solution with an insightful framing.** Replacing per-layer collectives with point-to-point communication is conceptually simple. The decentralized parameter server framing (Section 3.1, Figure 6) connects the solution to a well-understood architecture while preserving FSDP's memory and scaling benefits.

3. **Consistent empirical results across diverse settings.** Figure 8 shows ODC outperforming collective baselines across all 8 SFT configurations (2 datasets × 4 model scales), and Figure 9 shows similar gains in RL. The parametric study (Figure 10) systematically characterizes how the advantage varies with minibatch size, sequence length, packing ratio, and device count — going beyond a single benchmark result.

4. **Honest treatment of the method's primary limitation.** Section 5.4 (Figure 11) directly benchmarks ODC primitives against NCCL collectives and shows ODC is significantly slower in cross-node settings. Section 6.1 discusses this openly and proposes concrete mitigations (overlap with computation, hybrid sharding). Papers that place their method's main weakness front-and-center strengthen the overall contribution.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Missing compute/communication/idle time decomposition in multi-node settings.** Figure 11 shows ODC's cross-node primitives are slower than NCCL collectives, but the paper does not provide a wall-time breakdown into compute, communication, and idle components for the multi-node (32-device) experiments. Without this decomposition, it is difficult to assess how much of the observed speedup comes from reduced synchronization vs. how much is lost to slower cross-node transfers. The paper mentions bubble rate in Appendix G, but this should be analyzed in the main results. The parametric study does vary device count (Figure 10, bottom-right panel) and shows acceleration ratio *growing* with device count, which is encouraging, but a direct decomposition would make the evidence chain complete.

2. **Inconsistency between the text and Figure 8 regarding "Collective LB-Mini."** Section 5.1 (line 179) states: "As LB-Mini can produce different number of microbatches for different devices, it applies only to ODC." Yet Figure 8 lists "Collective LB-Mini" as one of the compared methods. If this means the same sample-to-device assignment as LB-Mini but executed with collective communication, the paper should explain how this is possible given that collectives force equal microbatches per device. This inconsistency undermines confidence in the experimental design and needs clarification.

3. **Baseline comparison relies heavily on the authors' own packing heuristics.** The primary packing baseline (LB-Micro) is the authors' own heuristic. While LocalSort is adapted from prior work (Bai et al. 2024), and the paper shows LB-Micro is substantially faster than verl's Native implementation in RL (Figure 9), the headline 36% speedup is relative to baselines largely of the authors' own design. A direct comparison against the full packing strategy from Bai et al. (2024) or another published method would make the claimed advantage more defensible.

4. **Empty reproducibility statement.** The reproducibility statement heading exists (Section 7) but contains no content. For a systems paper where implementation details (buffer management, deadlock avoidance, gradient accumulation protocol) are important, this is a meaningful gap.

5. **Limited discussion of gradient accumulation semantics.** The paper does not clarify whether ODC increases communication volume compared to FSDP. FSDP may defer reduce-scatter to after all microbatches, while ODC's scatter-accumulate presumably sends gradients per microbatch. If this increases communication volume, it should be accounted for in the analysis.

### Trivial
- Section 3.2's implementation description is brief for a systems paper. The paper defers to Appendix B (which is assumed to exist in the original submission), but a slightly more detailed sketch of the synchronization protocol in the main text would help readers.

## Nice-to-Haves
- Provide a compute/communication/idle time breakdown for the multi-node (32-device) setting.
- Run the parametric study with a multi-node golden setting to confirm trends hold when cross-node communication inefficiency is present.
- Compare against a prior published packing method in addition to LB-Micro.

## Removed Points

These points were flagged during review filtering but are retained here for reference; they should not be treated as substantive weaknesses.

1. **"RL experiment measures only training time" (removed).** The paper transparently acknowledges this at Section 5.1, line 163: "we only record the model training time in RL, ignoring forward-only parts like actor rollout." The critic correctly noted this is a reasonable choice.
2. **"Implementation details absent from main text" (demoted to Trivial, above).** The paper defers to Appendix B, which exists in the original submission. This level of detail is standard for page-limited main text.
3. **"Parametric study at single-node misses cross-node behavior" (partially addressed by Figure 10's device-count variation).** The remaining substantive gap (no decomposition) is captured in Minor weakness #1.

## Novel Insights

The reviews surface a productive framing: the paper's central tension — slower cross-node primitives vs. reduced idle time — is a classic systems trade-off that would benefit from an analytical break-even model. The paper currently relies on empirical results and qualitative arguments, but a quantitative characterization of "at what imbalance level does ODC's benefit overcome its slower cross-node communication?" would substantially strengthen the contribution.

## Suggestions

1. **Clarify the "Collective LB-Mini" label in Figure 8.** Either correct the label or explain how LB-Mini packing was applied with collectives. If it is simply "same packing as LB-Mini but with collectives," explain the implementation.
2. **Add a compute/communication/idle time breakdown** to the main evaluation, especially for the 32-device (4-node) setting.
3. **Fill in the reproducibility statement** with concrete implementation details.
4. **Compare against at least one prior published packing method** (e.g., the packing method from Bai et al. 2024 directly, not just LocalSort) to strengthen baseline fairness.
5. **Clarify the gradient accumulation protocol** — does ODC increase communication volume compared to deferred reduce-scatter in FSDP?

## Score and Decision

Based on my analysis: the paper identifies a genuine, important problem; proposes a clean, well-motivated solution; and provides largely positive empirical results across diverse settings. The weaknesses are real but not structural — the inconsistent figure labeling, missing decomposition analysis, limited baseline comparison, and empty reproducibility statement are all addressable. The contribution is solid and the paper is transparent about its limitations.

I calibrate this paper as follows:

- **Contribution:** A new communication primitive that adapts parameter-server ideas to FSDP for imbalanced workloads. This is a novel and practical contribution to distributed LLM training.
- **Evaluation quality:** Broad (SFT + RL, 1.5B–32B, up to 32 GPUs) but with noted gaps (no multi-node decomposition, baseline limitations).
- **Presentation:** Generally clear, but the "Collective LB-Mini" inconsistency and empty reproducibility statement are notable issues.
- **Severity of weaknesses:** All minor to trivial; none threaten the core contribution.

The paper sits in the borderline-accept range. With the identified issues addressed (particularly the decomposition analysis and figure clarification), it would be a solid accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>