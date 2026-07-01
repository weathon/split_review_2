## Summary

This paper proposes MadDist and TDMadDist, two algorithms that learn the Minimum Action Distance (MAD) — the minimum number of actions needed to transition between states — from state-only trajectories. The key technical innovations are: (1) a scale-invariant loss (Eq. 5) that avoids the trajectory-length-dependent error amplification of prior work, (2) support for asymmetric quasimetrics (including a simple new one, d_simple), and (3) a benchmark suite with known ground-truth MAD across diverse settings. MadDist achieves strong downstream planning results.

## Strengths

- **Well-motivated problem and clear gap.** The paper correctly identifies that prior MAD-approximation work relies on symmetric metrics despite MAD being inherently asymmetric, and that no prior work has been systematically evaluated on MAD approximation itself. This framing is specific and accurate.

- **Scale-invariant loss (Eq. 5) is a genuine, simple improvement.** The observation that the MSE in Eq. (2) from Steccanella & Jonsson (2022) scales errors with trajectory length, and that dividing by `j-i` fixes this, is clean and directly addressable. The paper demonstrates its empirical benefit.

- **Valuable benchmark suite.** Environments with known ground-truth MAD spanning discrete/continuous, deterministic/stochastic, and symmetric/asymmetric dynamics are a useful community resource.

- **Strong downstream planning results (Table 1).** MadDist achieves near-perfect success rates across all OGBench PointMaze environments, including the challenging Stitch settings that require composing information from disconnected trajectories. This grounds the representation quality in a practical task.

## Weaknesses

### Fatal
None.

### Major

- **Unsubstantiated headline claim about d_simple.** The abstract and contribution list claim that d_simple "outperforms more elaborate quasimetrics in the existing literature." However, the main experimental section (Section 7) never specifies which quasimetric was used for the reported MadDist/TDMadDist results. The only mention in the main text (line 222) is that the methods are "robust to the choice of quasimetric" — a different claim from "outperforms." Without knowing whether d_simple, d_WN, or d_IQE produced the results, and without a main-paper comparison, the reader cannot verify this headline claim. This is the paper's stated contribution and must be supported in the main text or retracted.

### Minor

- **Statistical reporting inconsistency.** The Empirical Setup (line 220) states "means over five independent runs," but the Figure 3 caption says "Shaded regions indicate minimum and maximum values across three random seeds." This discrepancy undermines confidence in experimental rigor. Additionally, MadDist achieving "1.00 ± 0.00" in four of six environments in Table 1 is atypical and may indicate task saturation.

- **TDMadDist underperforms the simpler MadDist with weak justification.** The paper acknowledges TDMadDist underperforms MadDist (and often QRL) but justifies this only as showing "the advantages of our quasimetric approach even when paired with a TD-based objective." This does not address why the bootstrapped variant fares worse or what it contributes. Presenting an underperforming variant as a contribution without analysis weakens the paper.

- **Contrastive loss (L_r, Eq. 6) and its hyperparameter d_max are unanalyzed.** The loss pushes distances between random state pairs toward d_max. For pairs that are genuinely close in MAD (e.g., adjacent states), this may directly conflict with the supervised loss (L_o) and constraint loss (L_c). The paper provides no sensitivity analysis for d_max and no ablation showing whether L_r is needed or what its effect is.

- **Abstract overclaims downstream scope.** The abstract states that MAD "naturally enables critical downstream tasks such as goal-conditioned reinforcement learning and reward shaping," but only goal-oriented planning is evaluated. The claimed downstream benefits are asserted, not demonstrated.

- **Limited discussion of d_simple's expressiveness.** The paper does not acknowledge that d_simple can only capture coordinate-aligned asymmetry (signed differences per dimension), which may not represent more complex directional structures involving interactions between dimensions.

- **No failure-case analysis.** The paper reports aggregate correlation numbers but never examines systematic errors (e.g., long-range vs short-range pairs, specific directions in asymmetric environments).

### Trivial

- SPD is introduced in the Conclusion without prior definition or distinction from SSP discussed in Section 4, which may confuse readers.
- NoisyGridWorld, listed as an environment, has no results shown in the main paper (deferred to Appendix F).

## Nice-to-Haves

- A symmetric-MadDist ablation (e.g., using Euclidean distance) would isolate the benefit of asymmetry from the improved loss formulation, making the comparison against baselines more informative.
- Sensitivity analysis for the d_max hyperparameter and an ablation without L_r.
- Error breakdown by distance range and direction in asymmetric environments.

## Removed Points

These points are flagged to be removed; treat them with caution:
- **"Eq. (9) is garbled"** — This is a parser artifact from PDF extraction, not an author error. Per policy, formatting artifacts are removed.
- **"OGBench PM Giant Navigate not listed in environment descriptions"** — The environment IS listed: Figure 2 shows OGBenchGiantMaze, and line 218–219 describes OGBench PointMaze as including larger layouts (Giant being one). The reviewer missed this.
- **"Comparisons against QRL and Hilbert are unfair/uninformative"** — The reviewer argues QRL is not trained to predict MAD, making the comparison uninformative. However, evaluating different methods on the same metric (MAD approximation accuracy) is standard practice. The paper would be stronger with a symmetric ablation, but the existing comparison is not invalid.
- **"Planning task not described in main paper"** — The paper explicitly references Appendix H for full details (line 224). Deferring implementation details to an appendix is standard for conference papers.
- **"Section 4 observation about path lengths is standard"** — Subjective opinion about originality; not a concrete weakness.

## Novel Insights

None beyond the paper's own contributions. The reviews identify the d_simple claim-robustness discrepancy and the statistical inconsistency, but these are corrections to presentation issues, not novel analytical insights.

## Suggestions

1. Specify which quasimetric produced the main results in Section 7. If d_simple was used, either move the ablation comparison from Appendix E to the main paper, or retract the "outperforms more elaborate quasimetrics" claim from the abstract and introduction.
2. Resolve the 5-vs-3 seed inconsistency and report standard deviations or confidence intervals uniformly.
3. Either explain why TDMadDist underperforms (e.g., bootstrapping noise, target update instability) or de-emphasize it.
4. Add an ablation of the contrastive loss (L_r) with d_max sensitivity, and consider removing L_r if it is not necessary.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>