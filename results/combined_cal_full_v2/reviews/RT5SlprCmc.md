Now I have all the calibration data I need. Let me compile the final review.

## Summary

This paper proposes learning the Minimum Action Distance (MAD) — the minimum number of steps to transition between states — from state-only trajectories, without requiring reward signals or action labels. It introduces two algorithms (MadDist and TDMadDist), a simple quasimetric (d_simple), and a benchmark suite of environments with known ground-truth MAD. MadDist uses a scale-invariant loss and contrastive term within a quasimetric embedding framework, achieving strong results on OGBench PointMaze planning tasks. The clean constrained-optimization formulation of MAD and the principled scale-invariant loss are notable contributions.

## Strengths

- **Clear problem framing and useful formalism.** The constrained optimization characterization of MAD in Eq. 1 (all-pairs shortest path with unit edge costs) is presented cleanly, and the distinction between MAD and the stochastic shortest path is well-drawn (Section 4).

- **Scale-invariant loss is a principled fix to a real problem.** The main objective in Eq. 5 — scaling the squared error by `(j-i)^2` — directly addresses an issue with prior work (Steccanella & Jonsson, 2022): naive MSE over raw distances causes long-horizon pairs to dominate the gradient. This is a concrete, well-motivated design choice.

- **Strong downstream planning results on OGBench PointMaze (Table 1).** MadDist achieves near-perfect or perfect success rates across all six OGBench PointMaze tasks (Navigate and Stitch variants at Medium, Large, and Giant scales), with tight standard deviations and large gaps over QRL and Hilbert baselines, especially on the Stitch tasks.

## Weaknesses

### Major

- **The most direct predecessor (Steccanella & Jonsson, 2022) is not included as a baseline.** MadDist is explicitly derived from this prior work — sharing the same loss structure, same use of trajectory step counts as supervision, and same embedding-based distance formulation. The claimed improvements are (a) replacing the symmetric distance with a quasimetric, (b) adding the scale-invariant loss (Eq. 5), and (c) adding the contrastive term (Eq. 6). Yet the experiments compare against QRL and Hilbert, neither of which is the direct predecessor. QRL uses a fundamentally different Lagrangian constrained-optimization framework, and the Hilbert method is an offline RL approach. Without isolating the effect of the specific changes, the reader cannot determine whether the gains come from the quasimetric, the scale-invariant loss, the contrastive term, or their combination. The most controlled comparison would be: Steccanella & Jonsson's original symmetric method → plus scale-invariant loss → plus quasimetric → full MadDist.

- **The claim about d_simple outperforming more elaborate quasimetrics is not evidenced in the main paper.** The abstract and introduction advertise a "novel quasimetric distance function that … outperforms more elaborate quasimetrics in the existing literature." However, the main experiments compare *algorithms* (MadDist, TDMadDist, QRL, Hilbert) rather than isolating the quasimetric choice. The quasimetric ablation is relegated to Appendix E, and the main text (line 222) describes it only as showing "robustness" to the choice of quasimetric, not superiority. A reader of the main paper cannot verify the headline claim about d_simple because the quasimetric choice is confounded with all other algorithmic differences.

### Minor

- **Inconsistency in variance reporting.** The empirical setup text (line 220) states results are means over *five* independent runs, while the Figure 3 caption (lines 232, 238, 240) states shaded regions show min/max over *three* random seeds. It is unclear which is correct, and three seeds is too few for reliable variance estimation.

- **Narrow set of environments in the main paper.** Of the seven environments described (NoisyGridWorld, KeyDoorGridWorld, CliffWalking, PointMaze UMaze, MediumMaze, OGBench variants), only three appear in Figure 3 and only OGBench variants appear in Table 1. Results for the stochastic (NoisyGridWorld) and additional discrete environments are deferred to the appendix, narrowing the main paper's evidence for the claimed comprehensive evaluation across stochastic/noisy settings.

- **Ceiling effects in Table 1.** Multiple entries show `1.00 ± 0.00` for MadDist (4 of 6 environments). This may indicate the downstream planning task is saturated rather than demonstrating genuine superiority. Without harder evaluation (e.g., generalization to unseen goal locations, actual RL usage), the practical significance of these perfect scores is unclear.

- **The novelty of d_simple is not clearly articulated.** Equation 3 is a convex combination of the max and mean of the positive part of the difference vector — a natural construction whose distinction from existing quasimetrics (e.g., L1 norm of the positive part) is not substantiated beyond satisfying the quasimetric axioms.

- **The framing "requiring neither reward signals nor the actions executed by the agent" (Abstract) is somewhat overstated.** The method relies on the step structure of trajectories, and the step count is meaningful only because each step corresponds to a sequential decision. This is a modest convenience rather than a fundamentally different learning paradigm.

### Trivial

- The conclusion (line 261) lists using MAD "as a heuristic in search algorithms" as future work, but Table 1 already evaluates a planning task that uses distances in exactly this way.

## Nice-to-Haves

- Compare directly against Steccanella & Jonsson (2022) to isolate the contribution of each component (symmetric baseline → plus scale-invariant loss → plus quasimetric → full MadDist).
- Show the quasimetric comparison (d_simple vs. IQE vs. Wide Norm) in the main paper with a controlled setting where only the quasimetric varies.
- Resolve the 3-seed vs. 5-seed discrepancy and use one consistent reporting standard.
- Report an absolute error metric (e.g., MAE or RMSE) alongside the correlation-based metrics to measure absolute accuracy.
- Provide analysis of why TDMadDist underperforms MadDist — is the bootstrapping introducing bias or noise?
- Consider evaluating on harder planning tasks where ceiling effects are less likely (e.g., generalization to unseen goal configurations).

## Removed Points

These points were identified in the input review but are removed per filtering rules:

- **Garbled equation in TDMadDist (Eq. 9):** The equation contains `12(9)` which is a PDF parser artifact, not an author error. Per hard rules, formatting/corruption artifacts from the extraction process are not included as weaknesses.
- **Criticism about reproducibility from the garbled equation:** Removed for the same reason — the original submission does not have this issue.
- **Generic speculation about confounders or missing controls:** Sweeping speculative concerns without concrete anchors in the paper text were removed.
- **Strength about the paper addressing an "important problem":** Removed as generic/superficial. Only strengths with specific, grounded evidence are kept.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Include the Steccanella & Jonsson (2022) method as a baseline in the main experiments. This is the single highest-leverage improvement: it would turn a confounded comparison into a clean ablation and directly support (or refute) the paper's specific claims about what matters.
2. Move the quasimetric ablation (d_simple vs. IQE vs. Wide Norm) into the main paper, at least as a table or summary, so the claim about d_simple's superiority is verifiable by the reader.
3. Resolve the seed-count inconsistency (3 vs. 5) and use a consistent, preferably larger, number of seeds with standard error shading.
4. Report an absolute error metric (MAE or RMSE) as a complement to the correlation-based metrics.

## Score and Decision

**Round 1 bracket (from calibration):** 4.5–6.5. The paper is clearly above papers at 4.75 (which had questionable theoretical foundations and non-significant results) and below papers at 6.25+ (which had stronger theoretical or ablation rigor).

**Round 2 narrowing:** Anchors at 5.75 (OMwD6pGYB4, rejected) and 6.00 (TOiageVNru, accepted) provide the tightest bracket. Compared to OMwD6pGYB4 (weaknesses at -1.98, -1.05, -0.72): our paper has stronger empirical evaluations but similar-magnitude methodological gaps (-1.90, -0.92). Compared to TOiageVNru (weaknesses at 0.78, 2.07, 1.97, 3.08): our paper's major weaknesses have more negative weights (-1.90, -0.92), reflecting more significant experimental design gaps that the authors would need to address.

**Final placement:** The paper has genuine contributions (high-weight strengths at 9.77–10.20) and the OGBench results are compelling, but the two major weaknesses — missing the direct predecessor baseline and insufficient support for the d_simple claim in the main paper — prevent the evidence from matching the scope of the claims. These are addressable in revision but meaningful as-is. The paper sits just below the accept threshold.

**Calibration anchors used (all rounds):**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Uj0h13lVrR.md` (1.00, Round 1) — Not similar; irrelevant topic.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/NRRHkJE03w.md` (3.00, Round 1) — Conservation principle discovery; weaker empirical grounding.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/oEzY6fRUMH.md` (4.75, Rounds 1&2, itemized) — State representation for RL; questionable theoretical claims and overlapping confidence intervals. Our paper is stronger.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/9SwObx9Jdn.md` (4.75, Round 2, itemized) — Geodesic generation; novelty concerns (-5.21), toy experiments. Our paper has broader evaluation.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/OMwD6pGYB4.md` (5.75, Round 2, itemized) — Distributional successor representation; limited experiments but novel theory. Comparable methodological concerns.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/TOiageVNru.md` (6.00, Rounds 1&2, itemized) — Metric learning for motion planning. Accepted; stronger ablation but similar weakness severity.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/qofh48zW3T.md` (6.00, Rounds 1&2, itemized) — Distance classifiers for GCRL. Mixed reviews; flawed formalism concerns (-5.99).
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/s9SVlWOcLt.md` (6.75, Round 1) — Proto successor measure. Stronger theoretical contribution.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/41WIgfdd5o.md` (6.25, Round 2, itemized) — Ex-BMDP representation learning. Strong theory but restrictive assumptions.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>