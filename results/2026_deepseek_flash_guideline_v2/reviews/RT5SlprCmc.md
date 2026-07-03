Now I have all the evidence I need. Let me produce the final consolidated review.

## Summary

This paper proposes learning the Minimum Action Distance (MAD) — the minimum number of actions to transition between states — from state-only trajectories. It introduces two algorithms: **MadDist** (direct distance regression with a scale-invariant loss and quasimetric distances) and **TDMadDist** (a temporal-difference variant with bootstrapped targets), defines a simple quasimetric ($d_{\text{simple}}$), and contributes a benchmark suite where the ground-truth MAD is known. Experiments show MadDist consistently outperforms QRL (an existing quasimetric method) and Hilbert (symmetric Euclidean) on MAD approximation accuracy and downstream planning success rates across discrete/continuous, deterministic/stochastic, and symmetric/asymmetric environments.

## Strengths

1. **Scale-invariant loss (Eq. 5).** The paper replaces the unscaled squared error of prior work (Steccanella & Jonsson, 2022) with $(d_\theta(s_i,s_j)/(j-i) - 1)^2$, preventing long-horizon state pairs from dominating the gradient. This is a concrete, principled modification clearly motivated in Section 6.1: "states that are further apart on a trajectory do not necessarily dominate the loss simply because the magnitude of the estimation error is larger."

2. **Systematic benchmark suite with known ground-truth MAD.** Unlike prior work that evaluated on downstream proxy tasks, the paper designs environments (NoisyGridWorld, KeyDoorGridWorld, CliffWalking, PointMaze variants) where the true MAD is analytically known or computable via Floyd-Warshall. This enables three complementary metrics (Spearman, Pearson, Ratio CV) that directly measure MAD approximation quality (Section 7). This is a genuine service to the community — it allows controlled comparison that was previously missing.

3. **Quasimetrics demonstrably improve MAD approximation over symmetric distances.** The comparison against Hilbert (symmetric Euclidean) on asymmetric environments like KeyDoorGridWorld and CliffWalking shows large, unambiguous gaps (correlation ~0.9 vs. ~0.6, Ratio CV ~0.2 vs. ~0.6 in Figure 3). This provides clear evidence that modeling directional structure matters for MAD learning, independent of any other methodological choices.

4. **Downstream planning validation on OGBench PointMaze (Table 1).** MadDist achieves perfect or near-perfect success rates on all six environments and outperforms QRL particularly on the Stitch tasks that require composing information from disconnected trajectories (e.g., PM Giant Stitch: $0.99 \pm 0.07$ vs. $0.95 \pm 0.12$, PM Medium Stitch: $1.00 \pm 0.00$ vs. $0.81 \pm 0.20$). This demonstrates that improved MAD approximation translates to practically meaningful planning performance.

5. **Broad evaluation scope.** The experiments span discrete and continuous state spaces, deterministic and stochastic dynamics, noisy observations, navigate and stitch dataset compositions, and include the large-scale OGBench PointMaze environments (up to 100×100 grids).

## Weaknesses

### Fatal
None.

### Major

1. **Missing controlled ablations that isolate which component drives improvement.** MadDist differs from QRL along multiple axes: (a) trajectory-level path-length supervision, (b) scale-invariant loss, (c) contrastive loss $\mathcal{L}_r$, and (d) quasimetric choice. The ablations reported (Appendix E, referenced at line 222) test latent dimension size, quasimetric choice, and dataset size — they do **not** isolate the contribution of the scale-invariant loss, the contrastive loss, or whether the improvement comes from trajectory-level supervision rather than QRL's locality constraints. Without ablations such as (i) MadDist with a symmetric distance vs. quasimetric (holding all else constant), (ii) MadDist without $\mathcal{L}_r$, or (iii) MadDist with the non-scale-invariant loss (the original Eq. 2) vs. Eq. 5, the reader cannot tell which innovations actually matter. The paper's claim that its specific methodological choices drive the gains (Section 7 Discussion, lines 226–227 attributes improvement to "leverages the path distances between arbitrary states") is plausible but unsupported by controlled evidence. This is the paper's most significant weakness.

### Minor

2. **Seed count inconsistency.** Section 7 (line 220) states: "All reported results are means over five independent runs (random seeds)." However, the Figure 3 caption (lines 232, 240) says: "Shaded regions around the lines represent the minimum and maximum values across three random seeds." This discrepancy needs resolution — if the figure uses only 3 seeds, the variance estimates are less reliable.

3. **Asymmetry framing overstates the gap relative to QRL.** The introduction and abstract claim that "many [prior methods] rely on symmetric approximations" (line 17) and state a contribution is "naturally supporting both symmetric and asymmetric distances" (line 19). The paper does acknowledge in Related Work (line 42) that QRL already uses quasimetrics. However, the main narrative (abstract, introduction, Section 5 heading "Asymmetric Distance Metrics," line 90 "A limitation of previous work is that the chosen distance metric $d$ is symmetric") continues to frame asymmetry as the key gap, when in fact the primary baseline QRL already handles asymmetry. The real contribution is **trajectory-level path-length supervision combined with quasimetrics** — which is a legitimate and well-supported advance — but the paper would benefit from reframing this honestly.

4. **Confidence interval overlap and potentially saturated evaluation.** The paper claims MadDist "decisively outperforms all baselines" (line 253), but for PM Giant Navigate, QRL's success rate ($0.87 \pm 0.21$) overlaps substantially with MadDist's ($0.93 \pm 0.17$). Additionally, MadDist achieves $1.00 \pm 0.00$ on 4 of 6 environments (Table 1). While this is impressive, perfect scores with zero variance on a planning success-rate metric can also indicate the downstream task is not sufficiently discriminating at the top end, rather than that the distance estimates are truly perfect. The paper should acknowledge this ceiling effect.

5. **$d_{\text{simple}}$ receives disproportionate emphasis relative to its technical novelty.** The abstract and conclusion list $d_{\text{simple}}$ as a main contribution ("novel quasimetric," lines 19, 259). As a convex combination of $\max(\text{relu}(x-y))$ and $\frac{1}{d}\sum \text{relu}(x_i - y_i)$, it is a straightforward construction. The framework supports any quasimetric, and the paper defers the comparison of $d_{\text{simple}}$ vs. IQE vs. Wide Norm to the appendix. If that ablation shows IQE or Wide Norm perform equally well, the claimed novelty of $d_{\text{simple}}$ as a contribution reduces to the empirical finding that a simple metric suffices — which is a different (and weaker) claim. Moving this comparison to the main paper would clarify its status.

### Trivial
None.

## Nice-to-Haves

- Report wall-clock time or sample complexity, since the methods use different loss formulations and the computational cost is relevant for practitioners.
- Provide a brief description of the downstream planning task (Table 1) in the main text rather than deferring entirely to Appendix H.
- Acknowledge the limitation that states never visited by the behavior policy cannot have their MAD learned (the paper currently does not discuss this).
- Clarify the TDMadDist $\mathcal{L}'_r$ equation (Eq. 9 appears corrupted in the PDF extract; the surrounding text provides the intended meaning but the equation needs correction).

## Removed Points

These points were raised in one or both reviews but are excluded from the main assessment:

- **TDMadDist equation garbled / logic suspect:** REMOVED. The equation artifact ("12(9)") is a PDF-parser formatting issue, not an author error. The intended objective (enforcing $d(s_i, s_r) \leq 1 + d(s_{i+1}, s_r)$ via the triangle inequality) is standard bootstrapping logic and is correctly explained in the text (line 173).
- **$d_{\text{simple}}$ novelty is "questionable" / "methodological gap":** REMOVED as a standalone criticism. The reviewer's observation that $d_{\text{simple}}$ is simple is correct, but simple≠invalid. The real issue (disproportionate emphasis) is folded into Minor #5 above.
- **Missing related works:** REMOVED per policy (cannot confirm existence of works not cited from external knowledge).
- **d_simple triangle inequality proof not in main text:** REMOVED. Proof deferral to an appendix is standard practice and not a weakness (Appendix B is explicitly noted).
- **No discussion of suboptimal behavior policy:** Moved to Nice-to-Haves. This is a legitimate limitation but the paper does not claim to solve the coverage problem, and it is not central to the paper's claims.

## Novel Insights

None beyond the paper's own contributions. The observation that the paper's real contribution is trajectory-level supervision combined with quasimetrics (rather than asymmetry per se) is worth stating explicitly, but it is already present in the paper's own discussion in Section 2 (lines 42–46, which note QRL's use of IQE and identify the key difference as "does not leverage existing distance along a trajectory as supervision").

## Suggestions

1. **Add controlled ablations** that isolate: (a) scale-invariant vs. original loss (Eq. 5 vs. Eq. 2), (b) with vs. without $\mathcal{L}_r$, (c) symmetric distance vs. quasimetric within the MadDist framework. This is the single highest-leverage improvement — it would clarify which component drives the gains over QRL.
2. **Resolve the seed-count inconsistency** (5 seeds in text vs. 3 in Figure 3 captions) and report consistently.
3. **Reframe the contribution** in the introduction: instead of "prior work relies on symmetric metrics" as the primary gap, say "while recent work has explored quasimetrics for MAD (QRL), these methods rely on locality constraints rather than direct trajectory-level path-length supervision, which we show is a more effective learning signal."
4. **Move the quasimetric ablation** ($d_{\text{simple}}$ vs. IQE vs. Wide Norm) from the appendix to the main paper, since $d_{\text{simple}}$ is listed as a main contribution.
5. **Quality claims with statistical overlap:** note cases where confidence intervals overlap with baselines (e.g., PM Giant Navigate) and acknowledge that ceiling effects may partially explain perfect scores.

## Score and Decision

**Calibration note:** The calibration database was unavailable, so I could not retrieve anchored comparisons. My score is based on a direct assessment of the paper's strengths and weaknesses against the ICLR scoring rubric.

**Reasoning:** This paper makes a meaningful contribution to state representation learning for RL. The scale-invariant loss and benchmark suite are clear positives. The empirical results are strong and consistent across diverse settings. However, the paper has a significant methodological gap (lack of controlled ablations for its core components) and several minor issues (seed inconsistency, framing overreach, potentially saturated metrics). These weaknesses prevent the paper from being a clear accept but do not invalidate its core findings. With the suggested revisions — particularly the addition of controlled ablations — the paper would be a solid accept.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>