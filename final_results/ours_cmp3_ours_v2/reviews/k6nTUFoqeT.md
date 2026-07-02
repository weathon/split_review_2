## Summary

This paper introduces FASTer, a framework for efficient autoregressive Vision-Language-Action (VLA) modeling. FASTerVQ is a neural action tokenizer that uses structured action patchification (non-uniform grouping by physical semantics), transformer-based residual vector quantization (RVQ), and a DCT-based frequency-domain reconstruction loss. FASTerVLA builds on this with block-wise autoregressive (BAR) decoding that predicts groups of action tokens in parallel. The framework is evaluated across 9 benchmarks spanning 5 embodiments (single-arm, bimanual, whole-body) in both simulation and real-world settings, consistently outperforming strong baselines like π0 and π0-FAST.

## Strengths

1. **Well-motivated technical design grounded in real-world constraints.** The four requirements for action tokenization (high compression, robust reconstruction, 2D structural modeling, flexibility) directly shape the architecture. The action patchifier that non-uniformly groups dimensions by physical semantics (gripper vs. arm vs. torso) is a simple but genuinely useful idea addressing the real problem that binary gripper states and continuous joint positions have radically different distributions. The DCT-based frequency-domain loss for capturing global temporal trends is similarly well-motivated.

2. **Very strong and consistent empirical results across diverse settings.** FASTer achieves 97.9% vs. 94.2% (π0) on LIBERO and 87.9% vs. 76.5% (π0-FAST-D) on Simpler-Bridge. Crucially, gains are consistent across three VLM backbones (PaliGemma2, Qwen2.5, InternVL3.5 — the last improving from 79.35% to 96.65%), across in-distribution and OOD settings, across simulated and real environments, and across three distinct control modalities. The cross-embodiment generalization (Figure 8: training on single-arm delta-EEF, testing on joint-velocity, absolute joint-position, and delta joint-position) is compelling evidence that FASTerVQ captures a transferable action prior.

3. **Clean ablation design.** The "FASTer w/o BAR" variant cleanly separates tokenizer contribution from decoding strategy. Figure 7 shows the tokenizer alone lifts InternVL3.5-2B from 79.35% to 96.30%, demonstrating that representation quality has first-order effects independent of decoding strategy.

4. **Detailed inference efficiency analysis.** Table 2 breaks down latency contributions, identifying observation encoding as the dominant bottleneck (~88–127ms) vs. tokenization (~2.7–7ms), which is useful both for validating claims and guiding future work.

## Weaknesses

### Fatal
None.

### Major

1. **No variance or uncertainty reporting across any experiment.** Every success rate in every table and figure is reported as a point estimate without standard deviations, confidence intervals, or the number of trials per condition. This matters because several comparative gaps are small: ~1–2 percentage point differences on VLABench generalization (Figure 9), sub-task gaps like 99.4% vs. 98.0% on LIBERO Spatial (Table 1), and real-world evaluations (Figures 4, 10) that are particularly susceptible to variance given practical constraints on trial counts. The paper's core comparative claims would be significantly strengthened by variance estimates. This is the most impactful evidential gap.

2. **VRR (Valid Reconstruction Rate) is introduced but never validated against downstream task performance.** The paper proposes VRR as a more functionally meaningful metric (Equation 4) and uses it as the primary tokenizer quality measure (Figures 5, 8). It claims "a reconstruction error on the order of 10⁻² is sufficient to cause a noticeable degradation in task execution accuracy" (line 222) without supporting evidence. The paper never demonstrates that VRR scores correlate with policy success rate. Without this validation, VRR remains a different transformation of reconstruction error whose superiority over L1/L2 is asserted rather than demonstrated.

### Minor

1. **Codebook utilization comparison uses different codebook sizes.** The paper states "Fast+ (57% of 2048) and FASTerVQ (100% of 4096) exhibit markedly higher codebook utilization than Fast (48% of 2048)" (line 264). FASTerVQ uses 4096 codes while Fast and Fast+ use 2048. Achieving 100% utilization of 4096 codes is mechanically easier — more codes spread over the same data reduces specialization pressure and dead-code likelihood. The normalized entropy comparison partially addresses this, but the utilization claims should be qualified with this confound acknowledged.

2. **VLABench absolute performance not discussed.** All methods achieve low success rates on VLABench (ID ~12–14%, OOD ~5–11%, Figure 9). The paper mentions "only a marginal gap to π0 on VLABench" (line 260) but does not explain why all methods perform poorly or how the small reported gaps should be interpreted in this low-success regime. Whether this reflects a ceiling/floor effect or a meaningfully harder benchmark is left unclear.

### Trivial

1. **Naming confusion.** The framework is called "FASTer" in the body but "FASTER" in the title and Table 1 entries, while the prior work is "FAST" (Pertsch et al., 2025). Combined with FASTerVQ, FASTerVLA, FAST+, π0-FAST-D, π0-FAST-R, the nomenclature is difficult to track. A nomenclature table would improve readability.

## Nice-to-Haves

- Clarify whether "initialized from checkpoints pretrained on large-scale robotics data (e.g., from π0-FAST)" means FASTerVLA uses π0-FAST's *weights* as initialization. The paper states all methods share this initialization (making the comparison fair), but this should be spelled out explicitly since a comparison against π0-FAST while starting from its weights could otherwise appear circular.
- The lightweight action expert is described as "Inspired by π0" (line 72); clarifying what (if anything) is novel about this component relative to π0's design would help position the contribution precisely.

## Removed Points

These points are flagged to be removed, treat them with caution:
1. *Criticism about missing appendix content (Table 3 for tokenizer data budgets).* The parser strips appendix sections from all papers; they exist in the original submission.
2. *Criticism that the "FASTER" title spelling is a typo.* The title uses all-caps typography while the method name in the body uses mixed case — this is a stylistic choice, not a paper error.
3. *Criticism that the paper should reference missing related work.* Cannot verify without external sources; this was not included in the review.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add variance estimates to central results.** Report standard deviations or confidence intervals for at least Table 1 and Figure 4. Even running 3 seeds or stating the number of trials per condition would substantially improve the reader's ability to assess reliability.
2. **Validate VRR against downstream policy performance.** On a subset of tasks (e.g., LIBERO Spatial, LIBERO Object), show that tokenizers with different VRR scores produce correspondingly different policy success rates.
3. **Control for codebook size in utilization comparisons** or explicitly acknowledge the confound and explain why the comparison remains informative.
4. **Discuss VLABench's difficulty level** to contextualize the low absolute success rates and clarify whether the 1–2% improvements should be interpreted as meaningful.
5. **Add a nomenclature table** mapping all method variants (FAST, FAST+, FASTer, FASTerVQ, FASTerVLA, π0-FAST-D, π0-FAST-R) to their definitions.

## Score and Decision

**Calibration anchors** (all retrieved, avg human score, round):

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `gwZ90hFSL2` (Cross-Lingual Humanoid) | 1.00 | R1 | Much weaker; unserious paper |
| `5kMwiMnUip` (NEMESIS Jailbreaking) | 1.40 | R1 | Much weaker; not relevant |
| `8QTpYC4smR` (Systematic Review of LLMs) | 1.00 | R1 | Much weaker; survey paper |
| `KBSHR4h8XV` (Early Fusion VLA) | 3.33 | R1 | Weaker; limited evaluation, smaller margins |
| `Lr8IIc1rB8` (Autoregressive Action Sequence) | 4.00 | R1 | Weaker; limited environments, weaker baselines |
| `iVxxgZlXh6` (LLaRA) | 5.25 | R1 | Weaker; less thorough evaluation |
| `PPDheO2z5v` (Actra) | 3.67 | R1 | Weaker; limited scope, rejected |
| `9pKtcJcMP3` (Video Language Planning) | 7.00 | R1 | Comparable; different contribution type (planning vs. tokenization) |
| `lFYj0oibGR` (VL FMs as Robot Imitators) | 6.50 | R1 | Comparable; similar evaluation breadth |
| `b1CVu9l5GO` (TraceVLA) | 7.00 | R2 | Closest match; similar VLA evaluation, similar paper quality |
| `Wr3UuEx72f` (LARP video tokenizer) | 7.50 | R2 | Slightly stronger; more novel tokenization paradigm |

**Round-1 bracket**: 6.0–8.0 (papers with similar evaluation breadth and methodological contribution score 6.5–7.5 in this corpus).

**Final calibration**: The paper's comprehensive evaluation (9 benchmarks, 5 embodiments, multiple backbones), clean ablations, and consistent empirical improvements place it alongside accepted papers scoring 7.0. The missing variance reporting and unvalidated VRR metric are genuine evidential gaps that prevent it from reaching the 7.5+ tier, but the core contributions are clearly supported and significant.

**Score**: 7.0

**Decision**: Accept

<score>7.0</score>
<decision>Accept</decision>