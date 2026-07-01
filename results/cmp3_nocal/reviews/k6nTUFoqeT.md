## Summary

This paper proposes FASTer, a framework for efficient autoregressive vision-language-action (VLA) modeling. FASTerVQ is a neural action tokenizer that non-uniformly patches action sequences by physical semantics, applies residual vector quantization with both time-domain and DCT frequency-domain reconstruction losses, and achieves high compression with strong fidelity. FASTerVLA builds on this tokenizer with block-wise autoregressive (BAR) decoding and a lightweight action expert, enabling faster inference than prior autoregressive VLAs while matching or exceeding diffusion-based methods. The framework is evaluated across nine benchmarks spanning five embodiments in simulation and on real robots.

## Strengths

- **Well-motivated problem framing.** The paper articulates four concrete requirements for action tokenization (high compression, robust reconstruction, 2D structural modeling, flexibility) and uses them to motivate design decisions. This provides a principled evaluative lens that goes beyond ad-hoc tokenizer comparisons.

- **Broad evaluation scope.** Experiments cover nine benchmarks across five embodiments (single-arm, bimanual, whole-body), in both simulation and real-world settings. This is substantially more comprehensive than prior work on action tokenization and allows the paper to demonstrate generalization across diverse action spaces.

- **Cross-backbone results are genuinely striking.** On InternVL3.5-2B, FASTerVLA raises success rate from 79.35% (with the FAST tokenizer) to 96.65% — a 17.3% absolute improvement that turns the weakest backbone into the strongest (Figure 7). The controlled comparison (same backbone, different tokenizer) cleanly isolates the tokenizer's effect.

- **Honest inference speed analysis.** Table 2 breaks down latency per component and candidly identifies observation encoding (88–127ms), not token generation, as the dominant bottleneck. This prevents overclaiming about speed gains and provides useful context for practitioners.

## Weaknesses

### Fatal
None.

### Major

- **No statistical reporting on any experimental result.** Every success rate, VRR value, and comparison in the paper is reported as a point estimate with no standard deviation, confidence interval, or trial count. In robotics evaluations where results vary across seeds, object initializations, and policy rollouts, single-number results are uninterpretable. For example, in Table 1, FASTer achieves 97.9% vs. π0 FAST-D at 94.2% on LIBERO — a 3.7% gap that could be meaningful or within noise, and the reader cannot tell. The same issue affects every figure and table. While single-run evaluations are common in large-scale robotics benchmarks, the paper's central claims (SOTA performance, strong generalization) require the reader to trust that these point estimates reflect consistent advantages. This is a significant evidentiary gap that should be addressed with multi-seed reporting or at minimum explicit trial counts.

- **Table 1 mixes evaluation protocols from different sources.** The table aggregates numbers from OpenVLA, SpatialVLA, π0, VQ-VLA, and others alongside the authors' runs. Only the π0 FAST-D row (94.2%), the "FASTER w/o BAR" row, and the "FASTER" row are explicitly acknowledged as run under controlled conditions by the authors. The paper states baselines use "checkpoints pretrained on large-scale robotics data" but does not clearly specify which rows were reproduced in-house vs. cited from prior papers. The "state-of-the-art" claim should be qualified: the strongest controlled comparison is against π0 FAST-D (94.2% → 97.9%), which is a meaningful improvement, but the broader table obscures which comparisons are apples-to-apples.

### Minor

- **"FAST+" is never explicitly defined.** This method variant appears in Figures 5, 9, and 10 and in the text ("Fast+ (57% of 2048) and FASTerVQ (100% of 4096)"), but the paper never explains what FAST+ is — whether it is a larger variant of FAST, a different method, or an in-house baseline. This is a clarity issue that makes the figures harder to interpret.

- **OOD results are presented at low absolute success rates without adequate contextualization.** On VLABench OOD (Figure 9), FASTerVLA achieves roughly 8–14% across all dimensions. While the paper correctly notes the "lowest relative performance drop of 29%," this framing obscures the fact that even the best model succeeds only ~1 in 10 times in these settings. The paper would benefit from a candid discussion of when and why all methods fail, and what kinds of OOD scenarios remain challenging.

- **Codebook utilization framing inflates FASTerVQ's apparent advantage.** The paper states "Fast+ (57% of 2048) and FASTerVQ (100% of 4096) exhibit markedly higher codebook utilization." 100% utilization of 4096 slots is mechanically easier than 57% of 2048 slots because the larger codebook has more capacity. The paper does also report normalized entropy, which is the more informative comparison — the "100%" figure should be de-emphasized or replaced by the raw count and entropy values.

- **Spacing augmentation is not ablated.** The paper introduces a spacing augmentation technique (perturbing RoPE offsets during training) to mitigate position overfitting, but its contribution is never isolated. The ablation study (Section 4.4) covers tokenizer architecture, codebook size, residual depth, action expert size, and block-wise decoding, but not this component.

- **No discussion of method limitations or failure cases.** The paper would benefit from acknowledging when FASTerVLA fails, what kinds of action dimensions are hardest to reconstruct, and whether the non-uniform patching requires manual tuning for each new embodiment.

### Trivial
None.

## Nice-to-Haves

- Analyze the tokenizer's computational overhead during training (the paper reports only inference speed).
- Clarify what, if anything, distinguishes the lightweight action expert from the π0-inspired design it acknowledges.
- Provide practical guidance on setting the VRR tolerance σ for new tasks.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **Criticism about Figure 1 not being available to verify the motivating claim.** The paper's figures are stripped by the PDF parser; they exist in the original submission. This is a marking artifact, not a paper flaw. **Reason for removal:** parser artifact per hard rules.
2. **"The related work is somewhat brief" and "more detailed discussion of VQ-VLA would be appropriate."** This is a subjective scope judgment. The related work section adequately situates the paper. **Reason for removal:** scope creep per soft rules.
3. **"No guidance on setting VRR σ for new tasks."** This is a reasonable suggestion but not a weakness that harms any claim made in the paper. **Reason for removal:** moved to nice-to-have.
4. **"The paper would benefit from VRR numbers for each variant in the main text."** The VRR data is presented in Figure 5, which is a standard way to communicate functional-form comparisons across σ thresholds. **Reason for removal:** not a substantive weakness.
5. **"FASTER benefits from π0-FAST's pretraining infrastructure — the comparison against π0-FAST is not an independent cold-start comparison."** The paper explicitly states this shared initialization ("all baselines and FASTerVLA models are initialized from checkpoints pretrained on large-scale robotics data (e.g., from π0-FAST)"). Shared pretraining is standard practice; using it to compare the methods that fine-tune from the same starting point is appropriate. **Reason for removal:** the paper already acknowledges this setup and it is standard for the field.
6. **"The discrepancy between Figure 4 (P0 at ~85% on LIBERO) and Table 1 (π0 at 94.2%) cannot be resolved without error bars."** Figure 4 is labeled "Libero (Scratch)" — a different training setting (from scratch vs. pretrained) from Table 1, which likely explains the gap. The discrepancy is about experimental condition labeling, not about needing error bars specifically. **Reason for removal:** the reviewer misattributes this to a need for error bars when the actual explanation is a difference in experimental condition.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Report all success rates as means over multiple seeds (at least 3) with standard deviations or explicit trial counts.** This is the single highest-leverage improvement and would directly address the most serious weakness.
2. **Clearly distinguish in Table 1 which rows are reproduced in-house under a shared protocol vs. cited from prior papers.** Add a footnote or column indicating the source and protocol for each baseline.
3. **Define FAST+ explicitly** — indicate whether it is a larger-codebook variant of FAST or a separate method.
4. **Add a brief limitations paragraph** discussing when the tokenizer's non-uniform patching requires manual tuning, and what kinds of OOD scenarios remain challenging.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>