Now I have strong calibration data. Let me produce the final consolidated review.

## Summary

This paper proposes MadDist and TDMadDist, two algorithms for learning the Minimum Action Distance (MAD) from state trajectories. The core innovation is using quasimetric (asymmetric) distance functions to capture the inherent asymmetry of MAD in environments with irreversible dynamics, coupled with a scale-invariant loss. The paper also introduces a simple quasimetric (d_simple) and a suite of benchmark environments with known ground-truth MAD.

## Strengths

1. **Well-motivated methodological gap (Section 4–5).** The paper correctly identifies that existing MAD methods (Steccanella & Jonsson, 2022; Park et al., 2024b) use symmetric distance metrics that cannot capture asymmetry in environments with irreversible dynamics (CliffWalking, KeyDoorGridWorld). This is a genuine limitation that the paper directly addresses.

2. **Principled scale-invariant loss (Eq. 5, Section 6.1).** The modification dividing squared error by `(j−i)²` is a clean, well-justified fix to the problem of long-horizon pairs dominating the loss in prior work. This is a clear improvement over the unnormalized loss in Steccanella & Jonsson (2022).

3. **Comprehensive evaluation suite with ground-truth MAD.** The environments span discrete/continuous state spaces, deterministic/stochastic dynamics, symmetric/asymmetric transitions, and noisy observations — enabling quantitative evaluation that is rare in this literature. The OGBench PointMaze evaluations (Table 1) at scale are a strength.

4. **Downstream planning evaluation (Table 1).** Going beyond correlation metrics to evaluate whether learned distances support goal-oriented planning is the right experimental design, and the strong results there add credibility.

## Weaknesses

### Major

1. **Missing most directly comparable baseline (Steccanella & Jonsson, 2022).** The paper explicitly states MadDist is "similar to prior work (Steccanella & Jonsson, 2022), but differs in the use of a quasimetric distance function and a scale-invariant loss" (line 137), and describes this prior method's loss in detail (Eq. 2). Yet this prior work is **not included as a baseline**. The baselines used (QRL, Hilbert) differ in multiple design dimensions simultaneously (learning signal, architecture, symmetries). Without a reimplementation of Steccanella & Jonsson (2022) with symmetric Euclidean distance, the paper cannot isolate whether improvements come from the quasimetric, the scale-invariant loss, or both. This undermines the paper's central thesis about the importance of asymmetry.

2. **Seed count inconsistency.** The experimental setup states "All reported results are means over five independent runs (random seeds)" (line 220), but Figure 3 and its captions repeatedly state "minimum and maximum values across three random seeds" (lines 232, 238, 240). This is a concrete discrepancy that undermines confidence in the reported statistics. The reader cannot determine whether the results reflect 3 or 5 seeds.

3. **Overclaimed quasimetric novelty.** The abstract claims d_simple "outperforms more elaborate quasimetrics in the existing literature" (line 19), and the conclusion repeats this (line 259). However, the main paper's only reference to the quasimetric comparison (Appendix E) is described as showing "robustness to... the choice of quasimetric" (line 222), not outperformance. No evidence for the outperformance claim is presented in the main paper. This claim should be retracted or supported with explicit evidence.

### Minor

4. **Ceiling effects in Table 1 undiscussed.** MadDist achieves 1.00 ± 0.00 success rate in 4/6 PointMaze environments. Zero variance across random seeds strongly suggests the planning task is at ceiling for these environments, making the results uninformative for method discrimination. The paper does not acknowledge this limitation.

5. **TDMadDist underperformance without analysis.** The paper acknowledges TDMadDist "underperforms the MadDist and QRL algorithm" (line 226) but does not extract any insight from this failure (e.g., why bootstrapping propagates errors, role of underestimation bias). Including a non-competitive algorithm as a co-equal contribution without analysis weakens the exposition.

6. **Behavior policy coverage not discussed.** All data uses a random policy (line 220); the paper does not address how coverage affects learning (state pairs never visited cannot have their MAD learned). This limits the reader's understanding of when the method will work.

### Trivial

7. **Selective framing in Table 1 discussion.** The paper claims MadDist "decisively outperforms all baselines across all PointMaze environments" (line 253), but in PM Giant Navigate, TDMadDist (0.99±0.05) has a higher mean than MadDist (0.93±0.17). While MadDist does beat the actual baselines (QRL 0.87, Hilbert 0.16), the framing glosses over the fact that the TD variant outperforms the direct variant in this case.

## Nice-to-Haves

- Visualize the learned embedding space to show directional structure (e.g., that states without/with the key are arranged asymmetrically in KeyDoorGridWorld).
- Ablate the effect of the scale-invariant loss separately from the quasimetric: include a version of MadDist with symmetric Euclidean distance + scaled loss.
- Discuss limitations of the random-policy data collection assumption and how coverage affects the learned distances.

## Removed Points

- **Equation 12(9) corruption (line 171):** Removed as a parser/formatting artifact. The paper text at line 173 explains the intended objective clearly.
- **d_simple triangle inequality concern:** Removed because the proof is in Appendix B, which is stripped by the parser. The main text (line 105) correctly states where the proof is.
- **Missing related work:** Not included per policy (cannot confirm existence of missing references).
- **"No analysis of learned embeddings":** Carried to Nice-to-Haves; not a concrete weakness.
- **Formatting/style nitpicks, typos, missing appendix content:** Removed per policy as parser artifacts or non-substantive.

## Novel Insights

None beyond the paper's own contributions. The reviewer points largely converge on identifying concrete experimental gaps (missing baseline, seed inconsistency, overclaiming) rather than offering novel analytical perspectives.

## Suggestions

1. **Include Steccanella & Jonsson (2022)** reimplemented with symmetric Euclidean distance and the original (unscaled) loss as a baseline. This would isolate the paper's two claimed innovations: the effect of the quasimetric and the effect of the scale-invariant loss. If MadDist with symmetric distance + scaled loss outperforms Steccanella & Jonsson, the scale-invariant loss is validated. If MadDist with quasimetric + unscaled loss outperforms it, the quasimetric is validated.

2. **Resolve the seed count discrepancy.** Clarify whether results are based on 3 or 5 seeds and report all statistics consistently.

3. **Calibrate quasimetric claims to match evidence.** Either show evidence that d_simple outperforms other quasimetrics (WideNorm, IQE) in the main paper, or retract the "outperforms" language from the abstract and conclusion.

4. **Discuss ceiling effects in Table 1** and, if possible, include harder planning tasks where methods can be discriminated.

## Score and Decision

**Calibration.** I retrieved and itemized three anchor papers for comparison:

| Anchor | Avg Score | How It Compares |
|--------|-----------|-----------------|
| TOiageVNru (Physics-informed TD Metric Learning) | 6.00 | Accepted. More baselines, real robot experiments, stronger evaluation. Accepted despite ablation showing main component from prior work. MAD paper has cleaner core motivation but weaker evaluation. |
| OMwD6pGYB4 (Distributional Analogue to SR) | 5.75 | Rejected. Good idea but toy experiments and limited applicability. MAD paper is similarly sound conceptually but has broader evaluation. |
| oEzY6fRUMH (State Chrono Representation) | 4.75 | Rejected. Unconvincing results with overlapping CIs, unclear writing. MAD paper is better: clearly written, stronger empirical signal. |
| sEv6vHIUnu (Structured Predictive Representations) | 4.80 | Rejected. Limited experiments (4 MiniGrid tasks), overstated conclusions. MAD paper has more thorough evaluation. |
| qofh48zW3T (Distributional Distance Classifiers for GCRL) | 6.00 | Rejected. Poor formalism, missing proofs. MAD paper is better written and more rigorous mathematically. |

**Round 1 bracket:** 4.0–6.0. The paper is clearly above the 1–3 range (unrelated or fundamentally flawed papers) and below the 7.5+ range (exceptionally strong work with flawless execution). Within the bracket, the paper is stronger than the 4.75–4.80 papers (which had unconvincing results or limited experiments) but has evaluation gaps that keep it below the 6.00 level.

**Final Score:** 5.0. The core ideas are well-motivated and the method appears sound. However, the missing baseline (Steccanella & Jonsson, 2022) prevents the paper from isolating the effect of its claimed contributions, the seed count inconsistency undermines trust in the statistics, and the quasimetric outperformance claim is unsupported in the main paper. These issues are fixable but currently limit the paper's ability to make a clean case for its contribution.

**Decision:** Reject (borderline; could be strengthened to accept by adding the missing baseline, resolving the seed discrepancy, and calibrating claims to match evidence).

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>