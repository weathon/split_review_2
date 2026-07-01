Now I have sufficient calibration context. Let me write the final consolidated review.

**Bracket determination:** After comparing against anchors, the paper sits between the State Chrono Representation (4.75, rejected — weaker on theory and empirical rigor) and the Physics-informed TD Metric Learning / Distributional Distance Classifiers (6.00, mixed decisions — similar quality but with different issues). I estimate the narrow plausible range is **5.0–6.0**. The paper has clear contributions but a significant gap in testing its core asymmetry claim. I place it at **5.5**.

---

## Summary

This paper proposes learning the Minimum Action Distance (MAD) — the minimum number of actions to transition between states — from state trajectories alone, using asymmetric distance metrics (quasimetrics). It introduces two algorithms: MadDist (direct distance learning with a scale-invariant loss) and TDMadDist (a temporal-difference variant), along with a simple quasimetric and a benchmark suite of environments with known ground-truth MAD. Experiments show MadDist achieving high correlation with true MAD and near-perfect downstream planning success rates on OGBench PointMaze tasks, outperforming QRL and a Hilbert-space baseline.

## Strengths

1. **Well-motivated problem with clean theoretical formulation.** The constrained optimization formulation of MAD (Eq. 1) cleanly connects to the all-pairs shortest-path problem, and Section 4 provides a sound foundation for what is being learned.

2. **Scale-invariant loss is a genuine practical improvement.** The main objective `(d_θ/(j-i) - 1)^2` (Eq. 5) replaces the unscaled squared difference used in prior work (Steccanella & Jonsson, 2022). Without scaling, longer trajectory segments would dominate the loss simply because absolute error grows with distance, not because they carry more structural information. The paper correctly identifies and addresses this.

3. **Strong downstream planning results.** MadDist achieves near-perfect or perfect success rates across all six OGBench PointMaze variants (Table 1), including the challenging Stitch datasets (which require composing information from disconnected trajectories) and Giant environments (long-horizon reasoning). The contrast with the Hilbert baseline (0.05–0.67) makes the advantage concrete.

4. **Benchmark suite with known ground-truth MAD is a useful contribution.** Five environments spanning discrete/continuous state spaces, deterministic/stochastic dynamics, symmetric/asymmetric transitions, and noise — all with known ground-truth MAD — provide a controlled testbed that has been missing from the literature. This alone is a meaningful methodological contribution.

## Weaknesses

### Major

- **The central claim about asymmetry is not directly tested.** The paper's key distinguishing claim is that supporting asymmetric distances is necessary because "the true MAD is inherently asymmetric" (line 17). Yet the three evaluation metrics (Spearman ρ, Pearson r, Ratio CV) aggregate over all state pairs and do not distinguish between `d(s,s')` and `d(s',s)`. A method that learns a symmetric distance that happens to be well-correlated with the true asymmetric distances could score well while still failing to capture directionality. In environments with clear asymmetry (e.g., CliffWalking, KeyDoorGridWorld), the paper could compute separate metrics for forward vs. backward pairs to show that quasimetric methods correctly assign different values while symmetric methods cannot. Without this analysis, the paper's core motivating claim is asserted but not supported by the evidence presented.

### Minor

- **Internal inconsistency in number of random seeds.** The Empirical Setup section (line 220) states: "All reported results are means over five independent runs (random seeds)." However, Figure 3 and all its captions (lines 230, 232, 238, 240) consistently state: "Shaded regions indicate minimum and maximum values across three random seeds." This is a direct internal contradiction about a basic experimental-design detail that must be resolved for the results to be reliably interpreted.

- **TDMadDist underperformance is not meaningfully analyzed.** TDMadDist is presented as a natural extension using bootstrapping (Section 6.2), yet it consistently underperforms the simpler MadDist across all settings. The paper's explanation (line 226: "its strong performance relative to Hilbert highlights the advantages of our quasimetric approach even when paired with a TD-based objective") is tautological and offers no insight into *why* bootstrapping hurts. An analysis isolating the TD component — whether the bootstrapping targets are unstable, whether the formulation (Eq. 8) is fundamentally mismatched, or whether hyperparameters are poorly tuned — would significantly strengthen the paper.

- **Characterization of the Hilbert baseline.** The paper frames Park et al. (2024b) as learning MAD-approximating distances (line 206). A brief acknowledgment that this is a *derived* use of the representation (rather than a method explicitly designed for MAD approximation) would improve the fairness of the comparison and clarify what conclusions can be drawn from the large performance gap.

### Trivial

- **"Decisively outperforming all baselines" is slightly overstated for one case.** On PM Giant Navigate (Table 1), MadDist achieves 0.93±0.17 vs. QRL's 0.87±0.21 — these error bars overlap. The overall claim is well-supported across the other five environments, but the phrasing is stronger than this single result warrants.

## Nice-to-Haves

- An ablation in the main paper for the contrastive loss term (Eq. 6) would help assess its contribution.
- A table of key hyperparameter values (w_r, w_c, d_max, H_c, α, β) in the main text would aid reproducibility.

## Removed Points

- **Garbled Eq. (9) / `12(9)` fragment:** Parser artifact; the original submission does not have this issue.
- **NoisyGridWorld results deferred to appendix / Spearman results in appendix:** The appendix is stripped by the parser; these exist in the original submission.
- **Missing hyperparameters / missing ablation:** Instructions specify removing nitpicks about reproducibility details and appendix content.
- **`d_simple` "novelty" overstatement:** Subjective opinion about terminology, not a substantive weakness.
- **Hilbert baseline compared unfairly:** The asymmetry in results favors the baselines (symmetric methods are disadvantaged), which is allowed per guidelines.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add a targeted analysis of asymmetry capture.** For CliffWalking or KeyDoorGridWorld, separately report correlation metrics for `d(s,s')` vs. `d(s',s)` on pairs where the true MAD is asymmetric. This would directly substantiate the paper's core claim.

2. **Resolve the 3 vs. 5 seed inconsistency.** Ensure the text and figure captions agree.

3. **Analyze why TDMadDist underperforms MadDist.** Even a short ablation isolating the bootstrapping component (e.g., comparing MadDist with and without a target network) would provide useful insight.

4. **Clarify the Hilbert baseline's relationship to MAD approximation.** A sentence acknowledging that this is a derived use of the representation (not a method explicitly trained for MAD) would make the comparison more precise.

## Score and Decision

**Round 1 bracket:** 5.0–6.0, based on comparison with calibration anchors: State Chrono Representation (4.75, rejected), Physics-informed TD Metric Learning (6.00, mixed accept/reject), Distributional Distance Classifiers (6.00, rejected), Disentangled Rep Learning with Gromov-Monge Gap (5.50, accepted).

**Final:** The paper has clear, well-motivated contributions (MAD formulation, scale-invariant loss, benchmark suite, strong planning results). However, the central motivating claim about the necessity of asymmetry for MAD approximation is never directly tested — the evaluation metrics cannot distinguish between methods that capture asymmetry and those that do not. This gap, combined with a reporting inconsistency and a dangling underperforming method, prevents full endorsement of the paper's strongest claims in its current form. With a targeted asymmetry analysis and corrections to the experimental reporting, this would be a solid contribution.

**Score:** 5.5
**Decision:** Reject

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>