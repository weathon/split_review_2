## Summary

This paper proposes MadDist (and a TD variant TDMadDist), two self-supervised algorithms for learning the Minimum Action Distance (MAD) — the minimum number of actions needed to transition between states — from state trajectories only, without rewards or actions. The MAD is formalized as a constrained optimization problem (all-pairs shortest path). Key ideas include: (1) a scale-invariant regression loss `(d/(j-i) - 1)^2` that prevents distant state pairs from dominating gradients, (2) support for asymmetric quasimetric distance functions (d_simple, Wide Norm, IQE), and (3) a benchmark suite of environments where ground-truth MAD is computable. Results show MadDist achieves strong correlation with true MAD and outperforms baselines (QRL, Hilbert embedding) on a coefficient-of-variation metric and on a downstream planning task.

## Strengths

- **Clean formal grounding of MAD as a constrained optimization problem (Section 4, Eq. 1).** The paper formulates the MAD as the solution to a linear program — identity, single-step bound, and triangle inequality — and connects it to the all-pairs shortest-path problem. This provides a principled foundation for the loss functions that follow.

- **Scale-invariant loss (Eq. 5).** The modification from `(d - (j-i))^2` to `(d/(j-i) - 1)^2` is a simple but genuinely useful idea. It prevents state pairs that are far apart on a trajectory from dominating the gradient purely because their absolute error is larger, and is likely the main reason MadDist outperforms QRL on the CV metric.

- **Benchmark suite with known ground-truth MAD.** The environments (KeyDoorGridWorld, CliffWalking, NoisyGridWorld, PointMaze variants, OGBench) are thoughtfully chosen to probe different challenges — asymmetry, stochasticity, observation noise, long horizons — and the fact that the true MAD is computable in all of them enables a controlled evaluation that most prior work in this area has lacked. This is a genuine contribution to the community.

## Weaknesses

### Fatal
None.

### Major

- **Seed inconsistency between experimental setup and figure captions (line 220 vs. lines 230–240).** The experimental setup (line 220) states "All reported results are means over five independent runs (random seeds)." But the Figure 3 caption (repeated at lines 230, 232, 238, 240) says "Shaded regions indicate minimum and maximum values across three random seeds." This makes it impossible to know whether the error bars reflect 3 or 5 seeds, and whether the reported means are over 3 or 5 runs. This ambiguity undermines confidence in the main result figure's statistics. The authors must clarify which is correct.

- **Main paper shows only a subset of the claimed evaluation environments.** The paper claims evaluation on NoisyGridWorld, KeyDoorGridWorld, CliffWalking, PointMaze (UMaze, MediumMaze), and OGBench PointMaze. Yet Figure 3 shows results for only three: KeyDoorGridWorld, CliffWalking, and OGBench PM Giant Navigate. NoisyGridWorld — the only environment with both stochastic transitions and observation noise — is entirely absent from the main paper, as are UMaze and MediumMaze. The paper tells the reader to "see Appendix F" (stripped) for full results. For a paper whose central claim is systematic evaluation, relegating more than half the environments to the appendix is selective reporting.

- **The quasimetric used to produce headline results is not specified in the main paper.** Section 5 describes three quasimetrics (d_simple, Wide Norm, IQE) and line 222 states Appendix E shows MadDist is "robust to the choice of quasimetric." But Section 7 never states which quasimetric was actually used to produce Figure 3 and Table 1. Without this, the reader cannot determine whether the improvement comes from the loss function, the quasimetric choice, or both. If d_simple was used, the claim that it "outperforms more elaborate quasimetrics" requires evidence in the main paper; if IQE was used, the comparison against QRL (which also uses IQE) becomes a head-to-head comparison of loss functions, which the paper does not frame as such.

### Minor

- **TDMadDist underperforms with no explanation (Table 1, line 226).** The paper acknowledges "TDMadDist underperforms the MadDist and QRL algorithm" (line 226) but offers no analysis of why bootstrapping hurts. Table 1 shows TDMadDist success rates of 0.74, 0.70, 0.73, 0.92 on OGBench variants vs. MadDist's 0.93, 1.00, 1.00, 1.00. If bootstrapping introduces error propagation or the target network update creates biased targets, this should be analyzed. A negative result with analysis would be more valuable than presenting TDMadDist as a contribution without understanding its failure mode.

- **Comparison framing leans too heavily on the symmetric Hilbert baseline.** The Hilbert-space embedding (Park et al., 2024b) produces symmetric distances, so its poor performance on asymmetric environments is a foregone conclusion. The informative comparison is MadDist vs. QRL (the only other asymmetric method). Against QRL, MadDist shows better CV ratios but comparable Pearson correlations (~0.9 for both). The abstract's claim of "significantly outperforms existing state representation methods" would benefit from being calibrated against the closest prior work (QRL), rather than also counting a structurally incapable baseline.

- **No discussion of computational cost.** QRL uses locality constraints that may be cheaper per step. The paper does not report training time or wall-clock comparisons, making it hard to assess practical trade-offs.

- **Scale-invariant loss (Eq. 5) has a potential issue at small j-i.** When `j-i=1`, the denominator is small and noise in the distance estimate is amplified. The paper does not discuss whether this causes instability or how it is handled.

### Trivial

- Line 127: `d_q(phi_phi(s), phi_phi(s'))` — the inner function subscript should be `\theta`, not `\phi` (parser artifact).

## Nice-to-Haves

- A one-sentence description of the downstream planning task (currently deferred entirely to Appendix H) would help readers interpret the success rates in Table 1.
- Hyperparameter sensitivity (w_c, w_r, d_max, H_c) could be briefly discussed even without a full ablation.
- An analysis of when the MAD lower bound is loose enough to mislead downstream tasks in stochastic environments would strengthen the discussion of limitations.

## Removed Points

These points were raised by the harsh critic but removed or demoted after verification against the paper:

- **Garbled Eq. 9 (Critical Issue 5).** The harsh critic flagged that Eq. 9 (line 171) has mismatched parentheses and a spurious "12(9)" token. This is a PDF parser artifact; the original submission does not have this issue. Removed per formatting-artifact rule.
- **Claim that novel quasimetric "outperforms more elaborate quasimetrics" is unsupported in main paper.** This is the same underlying issue as the missing quasimetric specification (merged into Major weakness above).
- **"No analysis of failure cases or limitations of the MAD itself."** The paper already discusses this in Section 8 (lines 261–264), noting the MAD is a lower bound and that future work should explore stochastic shortest paths. Removed as inaccurate.
- **Hilbert baseline "inflates the apparent advantage" framed as structural issue.** Demoted to Minor. The paper is transparent about why it includes the Hilbert baseline (line 206: "to demonstrate the benefits of methods that explicitly model the quasimetric nature of the MAD"). MadDist also outperforms QRL, so the core claim does not rest solely on the Hilbert comparison.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Resolve the seed discrepancy.** Clarify whether Figure 3 uses 3 or 5 seeds and correct the text or caption accordingly.
2. **State the quasimetric choice.** Explicitly state in Section 7 which quasimetric was used to produce Figure 3 and Table 1.
3. **Show key missing results in the main paper.** Either include NoisyGridWorld, UMaze, and MediumMaze results (even as a summary table) in the main paper, or adjust the scope claim.
4. **Analyze TDMadDist's failure.** Add a paragraph (even speculative) on why bootstrapping hurts: e.g., error propagation from the target network, or biased TD targets in the stochastic setting.
5. **Calibrate claims.** Tone down "significantly outperforms existing state representation methods" to reflect that the main advantage over the nearest asymmetric baseline (QRL) is on the CV ratio, with comparable Pearson correlations.
6. **Describe the planning task.** Add one sentence describing the downstream planning setup so Table 1 can be interpreted without Appendix H.

## Score and Decision

**Calibration anchor papers (all rounds):**

| Path | Avg Score | Round | Comparison to this paper |
|------|-----------|-------|------------------------|
| TOiageVNru.md (Physics-informed TD Metric Learning) | 6.00 | 2 | Most topically similar; accepted despite mixed reviews. Our paper has clearer formal grounding but more presentation issues. |
| I7DeajDEx7.md (Episodic Novelty Through Temporal Distance) | 6.75 | 1 | Accepted; stronger empirical evaluation, fewer presentation issues. Our paper is slightly weaker. |
| qofh48zW3T.md (Distributional Distance Classifiers) | 6.00 | 1 | Rejected despite 6.00 avg; mixed reviews. Comparable contribution strength to our paper. |
| sEv6vHIUnu.md (Structured Predictive Representations in RL) | 4.80 | 1 | Rejected; criticized for limited evaluation. Our paper is stronger in both method and evaluation breadth. |
| G6dMvRuhFr.md (Grounding Video Models to Actions) | 7.33 | 1 | Accepted; stronger empirical work. Our paper is not at this level. |
| ms0VgzSGF2.md (Bridging State and History Representations) | 6.75 | 1 | Accepted despite one low score (3). Our paper has similar-level contributions but more clarity issues. |

**Round 1 bracket:** 4.75–6.75  
**Narrowing:** The paper sits between the 4.80 rejected paper (stronger contributions) and the 6.00–6.75 accepted papers (weaker presentation). The core ideas are sound and the contributions are real, but the seed inconsistency, missing quasimetric specification, and selective environment reporting are non-trivial presentation issues that need correction.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>