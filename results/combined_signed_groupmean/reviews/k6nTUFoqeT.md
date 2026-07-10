## Summary

This paper introduces FASTer, a unified framework for autoregressive Vision-Language-Action (VLA) models that combines a neural action tokenizer (FASTerVQ) with a block-wise autoregressive decoding policy (FASTerVLA). The tokenizer uses non-uniform patching of action dimensions (grouping by physical characteristic), residual vector quantization (RVQ) inspired by audio codecs, and a DCT-based frequency-domain reconstruction loss. The policy leverages block-wise autoregressive decoding to reduce inference steps. The paper evaluates across a broad range of simulated and real-world benchmarks, demonstrating strong task performance and generalization across embodiments.

## Strengths

- **Well-motivated tokenizer design.** The observation that action dimensions have highly non-uniform distributions (binary gripper, zero base movement during arm manipulation) is a genuine insight, and the non-uniform patching directly addresses it. The audio-codec-inspired RVQ with DCT-based frequency-domain L1 loss (Equation 1) is creative and well-justified for action sequences with both local dynamics and global trends. [impact=+8.13]

- **Genuinely broad evaluation.** The paper evaluates across LIBERO, VLABench, Simpler-Bridge, GalaxeaManisim (sim), plus xArm, R1Lite bimanual, and R1Lite whole-body (real) — spanning at least five distinct embodiments and both simulated and real settings. This breadth exceeds most prior VLA papers and is the paper's strongest empirical asset. [impact=+9.84]

- **Clear tokenizer-level improvements.** Figure 5 consistently shows FASTerVQ outperforming prior tokenizers across tolerance thresholds, and the data-scaling trend (FASTer(S) → FASTer(L) → FASTer(XL)) suggests the tokenizer benefits meaningfully from more data. [impact=+9.99]

- **Cross-backbone results are striking.** InternVL3.5-2B jumped from 79.35% (with FAST) to 96.65% (with FASTer), demonstrating that tokenizer quality can matter more than backbone choice. [impact=+9.98]

- **The paper honestly acknowledges its own limitations**, explicitly stating that "FASTer's improvement is driven primarily by its neural VQ tokenizer... with BAR adding only a smaller incremental boost." This transparency is commendable. [impact=+2.81]

## Weaknesses

### Fatal
None.

### Major

- **The VRR evaluation metric (Equation 4) is ambiguously defined for mixed-unit action vectors.** The equation computes an unweighted L1 norm over the full action vector with a single threshold σ, but robot actions simultaneously contain translation (meters), rotation (radians), joint positions (radians), and gripper state (binary). Summing absolute differences across these heterogeneous units with a single threshold is physically uninterpretable. The paper attempts to clarify ("For robot end-effector translation, σ corresponds to the Euclidean distance error measured in meters, whereas for end-effector rotation and joint positions, σ represents an angular error in radians"), but this description does not match the equation as written. Without specifying whether actions are normalized per-dimension, or whether VRR is computed per group of dimensions, the central tokenizer evaluation in Figures 5 and 8 cannot be reliably interpreted. [impact=-9.99]

### Minor

- **The claimed "3× reduction in inference latency compared to π₀" (Section 3.2) is overstated.** From the actual timing data (Table 2 and surrounding text): FASTerVLA takes 112ms total vs π₀ at 176ms on LIBERO — a ~1.57× speedup, not 3×. The 3× figure appears to refer to the action-decoding subcomponent specifically, but the sentence directly compares to π₀'s overall latency. On the WBC setting, FASTerVLA and π₀ converge to similar runtimes (~230ms), so there is no meaningful speedup there. [impact=-9.79]

- **No variance or statistical significance is reported for any experimental result.** Tables 1, Figure 7, and other results report single point estimates without error bars, standard deviations, or confidence intervals. Robotics benchmarks have substantial variance from initial conditions and policy stochasticity. Without this information, the reader cannot assess which reported differences are reliable. [impact=-9.17]

- **Inconsistency between Table 1 and Figure 7 regarding BAR's contribution.** Table 1 shows FASTer w/o BAR at 95.4% and FASTer at 97.9% on LIBERO (+2.5%), while Figure 7 per-backbone results show BAR adding at most +0.8%. The backbone used for Table 1 is not specified, making it impossible to reconcile the 2.5% gap with the per-backbone ablation data. [impact=-7.37]

### Trivial
- The non-uniform grouping of action dimensions (Section 3.1) is described as determined "based on their physical characteristic" (e.g., end-effector position, orientation, gripper grouped separately) but no specific procedure is given — whether by manual inspection, clustering, or a learned method. This matters for reproducibility and for the claimed flexibility to new embodiments. [impact=-3.45]

## Nice-to-Haves
- Include a limitations section discussing settings where the tokenizer might struggle (e.g., high-frequency oscillatory actions, very high-dimensional control beyond 21 DoF).
- Report the compute cost of tokenizer training (GPU-hours, data requirements).
- Analyze which action dimensions or temporal patterns are reconstructed poorly by the tokenizer.

## Removed Points
These points are flagged to be removed, treat them with caution:
- Criticism that VRR is a "structural issue" (fatal): downgraded to Major. The VRR issue is a clarity/ambiguity problem, not a fundamental flaw — the paper mentions "normalized action space" in Section 4.2, but the equation and description remain genuinely ambiguous as written.
- Criticism that "BAR contribution is marginal/nonexistent yet treated as core contribution": mostly removed. The paper explicitly acknowledges BAR's incremental contribution. The Table 1 vs Figure 7 inconsistency is the real concern and kept as Minor.
- "Figure 1 not preserved": parser artifact — removed.
- "No limitations section / no tokenizer failure mode analysis / compute cost not reported": nice-to-haves — removed from weaknesses.
- "Missing related works": removed per instructions.
- Formatting/style nitpicks: removed.
- Training initialization confound concern: weakened; the paper tests with Bridge/Droid starting from VLM weights as a control.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Clarify the VRR metric**: specify whether actions are normalized per-dimension before computing the L1 norm, or compute VRR per dimension-group with group-appropriate σ values. The current equation and description are contradictory.
2. **Specify the backbone used in Table 1** and explain why those results differ from the per-backbone analysis in Figure 7.
3. **Re-frame the speedup claim** to reflect total system latency (~1.57× on LIBERO, ~1× on WBC) and clarify that the 3× figure refers to the action-decoding subcomponent only.
4. **Add variance information** (standard deviations or confidence intervals) for at least the main results in Table 1.
5. **Provide more detail** on how the non-uniform grouping of action dimensions is determined.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `/home/.../VYOe2eBQeh.md` (LAPA) | 5.83 | R1+R2 | Yes | Data consistency errors (-10.00) vs. paper's VRR ambiguity (-9.99); paper has cleaner data but ambiguous metric |
| `/home/.../PPDheO2z5v.md` (Actra) | 3.67 | R1 | Yes | Weak novelty and evaluation; paper is clearly stronger |
| `/home/.../Lr8IIc1rB8.md` (Autoregressive Action) | 4.00 | R1 | Yes | Limited evaluation, incremental contribution; paper is stronger |
| `/home/.../b1CVu9l5GO.md` (TraceVLA) | 7.00 | R1+R2 | Yes | Cleaner evaluation but simpler contribution; paper is less clean but more fundamental |
| `/home/.../yGnsH3gQ6U.md` (BSQ-ViT) | 5.75 | R2 | Yes | Visual tokenization; comparable technical depth but different domain |
| `/home/.../lFYj0oibGR.md` (RoboFlamingo) | 6.50 | R2 | Yes | Single-benchmark evaluation; paper has broader evaluation but messier metrics |

**Round 1 bracket:** 5.5–7.5 (papers with similar topic in this range: LAPA 5.83, BSQ-ViT 5.75, RoboFlamingo 6.50, TraceVLA 7.00).

**Narrowing:** The paper's strongest weakness (VRR metric ambiguity, -9.99) is comparable in impact magnitude to LAPA's data consistency issues (-10.00) and RoboFlamingo's finetuning claim (-9.90). However, the paper under review has broader evaluation than RoboFlamingo (multiple embodiments vs. single benchmark) and cleaner data than LAPA (no numerical errors). The VRR ambiguity, while impactful, is a clarity issue that can be resolved in writing — unlike LAPA's swapped-table-values error. The speed claim overstatement (-9.79) and missing variance (-9.17) are genuine but common concerns in robotics papers at this tier. On balance, the paper sits above LAPA (5.83) and BSQ-ViT (5.75) due to cleaner data and broader evaluation, but below TraceVLA (7.00) due to the unresolved metric ambiguity and missing variance information. It is most comparable to RoboFlamingo (6.50) — both have significant weaknesses but genuine contributions.

**Final calibrated score: 6.0**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>