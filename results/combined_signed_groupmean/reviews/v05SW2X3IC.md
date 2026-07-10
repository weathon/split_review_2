Now let me write the final consolidated review.

**Bracket from Round 1:** The most relevant anchor is "Which Tasks Should Be Compressed Together?" (avg 5.33, accepted) which has strong quantitative results but clarity/presentation weaknesses. Our paper has stronger theoretical framing but more fundamental weaknesses (architecture-theory gap, no evidence of information separation, no comparison to existing multitask codecs). The DVSIB paper (avg 5.25, rejected) was rejected for limited experiments/novelty despite a similar score — our paper faces analogous structural validity concerns. Compression papers at ~3.4-3.5 (CoINR, NCA compression) were rejected for insufficient evidence supporting claims. Our paper falls between these: stronger than 3.5-level papers but with more fundamental issues than the 5.33 accepted paper. I place the paper at **4.0**.

## Summary

This paper proposes a learnable three-channel codec inspired by the Gray-Wyner network from information theory for multi-task compression. The architecture separates a representation into a common channel (Y₀) and two private channels (Y₁, Y₂), and the loss function (Eq. 12) uses a single hyperparameter β to trade off between transmit-rate efficiency (all tasks jointly) and receive-rate efficiency (tasks independently). Experiments on synthetic data, colored MNIST, and real vision benchmarks (Cityscapes, COCO) show the method outperforms independent coding and the common-channel rate responds to task information structure.

## Strengths

- **Principled theoretical framing of the transmit-receive tradeoff.** The loss function (Eq. 12) with β as a single dial interpolating between transmit-rate and receive-rate optimization is clean and well-motivated, connecting information-theoretic source coding (Gray-Wyner) with learned compression in a way that is novel and practically useful. The connection to Wyner's and Gács-Körner common information gives the problem a rigorous theoretical anchoring.

- **Well-designed edge-case experiment (colored MNIST, Section 4.2).** Using three PMFs with known mutual information (Dependent: full MI, Independent: zero MI, Mixture: intermediate) validates that the common-channel rate responds predictably to the information structure — higher common-channel utilization when tasks share more information and lower when they do not. This is the cleanest evidence that the method is doing something meaningful.

- **Useful ablation study (Section 4.1).** The comparison of Shared, Separated, and Combined encoder architectures on synthetic data demonstrates that the proposed design outperforms intuitive alternatives, providing evidence that the architectural choices matter beyond simply having more capacity.

- **Demonstrated gains over independent coding on real benchmarks.** On Cityscapes (segmentation + depth) and COCO (detection + keypoint), the proposed method consistently outperforms independent single-task codecs, showing that sharing a learned common channel yields practical rate savings.

## Weaknesses

### Major

- **Architecture-theory gap.** The theoretical framework (Gray-Wyner network, Theorem 2) assumes distinct sources X₁, X₂ with private channels Y₁ = f₁(X₁), Y₂ = f₂(X₂) and Markov conditions (Eq. 1). The actual architecture gives each branch access to both sources, and in all experiments (X₁, X₂) = X — a single source. The paper states this "effectively removes the requirement for the conditions in 1" (line 167) but does not examine whether Theorem 2's guarantees still apply or what the theoretical consequences are. The mask mechanism (Eq. 14) is a representation-alignment heuristic (forcing two feature extractors' outputs to agree via L₂ penalty), not a principled way to isolate information-theoretic common information. The paper is better understood as proposing an architecture *inspired by* Gray-Wyner theory rather than implementing it.

- **No direct evidence that the method isolates common information.** The paper's central claim is that the method "separates common information between two tasks." Yet no experiment analyzes or visualizes what information actually resides in Y₀ vs. Y₁ vs. Y₂. It is unknown whether Y₀ captures task-relevant shared information or merely residual information that the private channels cannot efficiently encode. The paper would be substantially strengthened by, e.g., decoding Y₀ alone through both task models and measuring performance — if Y₀ truly contains common information, it should support both tasks.

- **No comparison against existing multitask codecs.** The paper cites Chamain et al. (2021), Feng et al. (2022), and Guo et al. (2024) as prior multitask learnable codecs but does not compare against them experimentally. The Independent baseline (no common channel) is a weak comparator — any architecture with a shared channel should trivially beat it. Comparison against the most directly related prior work is essential to establish the method's relative merits.

- **Theorem 1 is stated but disconnected from the experiments.** The bounds relating K and C through interaction information (Theorem 1) are positioned as a contribution but are never computed empirically, never used to interpret experimental results, and never checked for whether the conditions for equality hold. This leaves a disconnect between the theoretical and empirical halves of the paper.

### Minor

- **No statistical uncertainty reported.** Rate-distortion curves and BD-rates are presented without error bars, standard deviations, or multiple seeds. Given the known variance in neural compression training, single-run results weaken the reliability of quantitative claims (e.g., the -81.58% average BD-rate advantage).

- **The motivating incremental transmission scenario is not tested.** The introduction compellingly motivates a scenario where tasks are activated sequentially (detection first, then segmentation). All experiments assume both tasks are performed simultaneously from the same coded representation, leaving the motivating use case unvalidated.

- **Training-inference mismatch in the mask mechanism.** The mask (Eq. 14) zeros out elements where Y₀⁽¹⁾ ≠ Y₀⁽²⁾ after quantization, but during training the straight-through gradient estimator means gradients flow through the averaged branch regardless of whether elements match. The auxiliary loss partially addresses this, but the mismatch is not discussed or analyzed.

### Trivial

None.

## Nice-to-Haves

- Analyze channel content: decode Y₀ alone through both task models to verify it contains task-relevant shared information.
- Compare against existing multitask codecs (Chamain et al., Feng et al., Guo et al.).
- Report results from multiple training seeds with error bars.
- Ablate the mask mechanism to separate the benefit of architectural capacity from the benefit of the common-information extraction mechanism.

## Removed Points

These points are flagged to be removed; treat them with caution:
- Criticism that "the paper does not report comparison against Joint coding" — this is factually wrong; Figure 5 tables show BD-rates explicitly computed with respect to Joint. Removed per Hard Rule 2.
- Criticism about hyperparameters relegated to appendix — the parser strips appendices from all papers; this is a format artifact. Removed per Hard Rule.
- Criticism about "compatibility" discussion relegated to Appendix C — same appendix artifact. Removed.
- Criticism that the advantage could come from network capacity rather than design — retained as it is a genuine concern about the Section 4.1 experiment; the ablation does compare Shared vs Separated vs Combined, which partially addresses this.
- Various section-by-section notes about figure clarity, notation density, etc. — these are presentation-level observations without specific actionable criticism. Removed as formatting/presentation nitpicks.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Acknowledge the architecture-theory gap transparently.** Reframe the paper as proposing an architecture *inspired by* Gray-Wyner principles rather than implementing them. This would align the claims with what is actually demonstrated.
2. **Add a channel-content analysis experiment.** Decode Y₀ alone through both task models to verify it captures task-relevant common information. Visualize what Y₀, Y₁, and Y₂ encode.
3. **Compare against at least one existing multitask codec** to ground the empirical claims relative to prior work.
4. **Report multiple seeds** or justify why single-run results are sufficient in this setting.
5. **Either connect Theorem 1 to experiments** (compute interaction information bounds on the datasets) or downplay its prominence in the paper.

## Score and Decision

**Calibration summary (all anchors retrieved):**

| Anchor Paper | Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|---|
| Which Tasks Should Be Compressed Together? | x33vSZUg0A.md | 5.33 | R1 | Yes | More thorough experiments, fewer fundamental validity concerns; accepted despite presentation issues |
| Real Time Macro-Block Rate Control | aQ7qYnY2nF.md | 4.00 | R1 | No | Task-aware compression; less theoretically ambitious, more focused empirical contribution |
| CoINR: Compressed Implicit Neural Representations | ZWi6RpT4mJ.md | 3.50 | R1 | Yes | Had mathematically incorrect statements; rejected for insufficient evidence |
| Unraveling NCA for Image Compression | gIrVoQEDQv.md | 3.40 | R1 | Yes | Novel idea but experiments too weak to support claims; rejected |
| Deep Variational Multivariate Info Bottleneck | ZhY1XSYqO4.md | 5.25 | R1 | Yes | Strong framework but limited experiments; rejected despite 5.25 avg |
| CMC-Bench | foKwWau15m.md | 6.00 | R2 | No | Different topic (cross-modal compression benchmark) |

The most informative anchor is "Which Tasks Should Be Compressed Together?" (avg 5.33, accepted). That paper's decisive strengths were strong quantitative results (+9.98) and sound principle (+9.06), while its biggest weaknesses were clarity/organization (-9.34, -9.97). Our paper has equally strong strengths but three decisive weaknesses that are **structural** rather than presentational: the architecture-theory gap (-9.99), no evidence of information separation (-9.95), and no comparison against existing multitask codecs (-10.00), plus a fourth decisive weakness in Theorem 1 not being connected to experiments (-9.89). The "Which Tasks" paper was accepted because its weaknesses were addressable via revision; ours are more fundamental to the validity of the central claims. Meanwhile, rejected papers near 3.5 (CoINR, NCA compression) had analogous problems of insufficient evidence for claimed contributions. Our paper is stronger than those but falls short of the evidence bar set by the 5.3 anchor.

**Final score: 4.0.** The paper tackles an interesting problem with a clean theoretical framing, but the gap between the claimed Gray-Wyner implementation and the actual architecture, the lack of direct evidence for information separation, and the absence of comparison against existing multitask codecs prevent acceptance in the current form. The core idea and loss function are valuable; the paper would benefit from reframing as "inspired by Gray-Wyner theory" and adding the missing evidence.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>