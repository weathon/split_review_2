Here is the final consolidated review:

---

## Summary

This paper proposes learning the Minimum Action Distance (MAD) — the minimum number of actions to transition between states — from state-only trajectories, without rewards or action labels. It introduces two algorithms: **MadDist** (direct distance regression with a relative-error loss and contrastive regularization) and **TDMadDist** (TD-style bootstrapping with a target network). Both support asymmetric distance functions (quasimetrics), and the paper proposes a lightweight quasimetric, $d_{\text{simple}}$. A new benchmark suite with known ground-truth MAD is introduced to enable systematic evaluation. Experiments show MadDist outperforming prior methods (QRL, Hilbert) across several environments.

## Strengths

- **Two clearly motivated algorithmic variants.** MadDist and TDMadDist are well-differentiated: MadDist uses direct regression with a scale-normalized loss $\mathcal{L}_o = ((d_\theta/(j-i))-1)^2$ plus a contrastive regularizer; TDMadDist incorporates TD bootstrapping. The composite loss design is principled and the motivation for each term is clear.

- **Benchmark suite with known ground-truth MAD.** The paper constructs environments spanning discrete/continuous states, deterministic/stochastic dynamics, and symmetric/asymmetric transitions — all with computable ground-truth MAD. This is a genuine contribution that enables controlled evaluation, something prior work lacked.

- **Careful treatment of asymmetric structure.** The paper reviews several quasimetrics (simple, Wide Norm, IQE), proposes $d_{\text{simple}}$ (a convex combination of max and mean of relu differences), and appropriately defers the quasimetric ablation to the appendix. This attention to a core design dimension is a strength.

## Weaknesses

### Major

- **Seed count inconsistency between text and Figure 3.** Line 220 states: *"All reported results are means over five independent runs (random seeds) to ensure statistical robustness."* However, the captions of Figure 3 (lines 230, 232, 238, 240) repeatedly describe shaded regions as showing *"minimum and maximum values across three random seeds."* This is an explicit internal contradiction. If Table 1 uses 5 seeds and Figure 3 uses 3 seeds, this should be stated with justification; if both should be the same, one description is incorrect. Combined with the fact that only min-max bands (not standard deviation) are shown in Figure 3, the uncertainty characterization is weaker than the text claims. This must be resolved for the quantitative claims to be credible.

### Minor

- **Missing within-method symmetric ablation to isolate the value of asymmetry.** The paper's central motivation is that asymmetry matters, and it claims the algorithm "naturally supports both symmetric and asymmetric distances" (line 19). However, the main experiments compare MadDist (with quasimetrics) against QRL (also quasimetric) and Hilbert (symmetric but with a different loss and architecture). There is no MadDist-Symmetric variant that keeps all MadDist algorithmic components (relative-error loss, contrastive loss, constraint loss) while forcing a symmetric distance metric. Such an ablation would cleanly separate whether gains over Hilbert come from (a) the algorithmic improvements or (b) the specific choice of asymmetric metric. Since QRL also uses a quasimetric, the comparison to QRL does not fill this gap.

- **TDMadDist underperforms without diagnostic analysis.** The paper acknowledges TDMadDist "underperforms the MadDist and QRL algorithm" (line 226) but offers no investigation into *why* bootstrapping hurts. Possible causes — instability from noisy bootstrapped targets using random $s_r$, the target update rate $\beta$, or bias from TD targets — are not explored. Without analysis or diagnostics (e.g., varying $\beta$, comparing TD vs. Monte Carlo targets), TDMadDist's inclusion as a co-equal contribution is confusing rather than informative.

- **Unsupported claim about $d_{\text{simple}}$ outperforming more elaborate quasimetrics.** Lines 19-20 claim $d_{\text{simple}}$ "outperforms more elaborate quasimetrics in the existing literature," but all supporting evidence is deferred to Appendix E (stripped from the submission). A claim of this specificity should be supported with at least a summary statistic in the main text.

- **NoisyGridWorld results absent from main paper.** NoisyGridWorld is listed as a test environment (line 214) and included in the training setup (line 220), but does not appear in Figure 3 (which shows only KeyDoorGridWorld, CliffWalking, and OGBench Giant Maze). The paper states full results are in Appendix F, but an environment listed as part of the evaluation suite should appear in the main results.

- **Zero-variance perfect success rates without discussion.** Table 1 shows MadDist achieving $1.00 \pm 0.00$ success rates across 5 seeds on four OGBench environments (PM Large Navigate, PM Large Stitch, PM Medium Navigate, PM Medium Stitch). While not impossible, zero variance from a learned neural embedding on these tasks merits some discussion — e.g., whether the planning metric saturates, or additional per-seed disaggregation.

## Nice-to-Haves

- A diagnostic experiment for TDMadDist varying the target update rate $\beta$ or comparing TD(0) vs. Monte Carlo targets would clarify whether bootstrapping can be made competitive.
- Sensitivity analysis for hyperparameters $H_c$, $w_r$, $w_c$ in the main text (currently deferred to Appendix E) would help readers assess robustness without consulting the appendix.
- Standard deviation or confidence intervals (rather than min-max bands) in Figure 3 would provide more informative uncertainty characterization.

## Removed Points

1. **"QRL characterization oversimplified"** — The paper's statement that QRL "only uses locality constraints" (line 226) is a reasonable characterization of QRL's learning signal for the comparison at hand; it is not a misrepresentation.
2. **"Scale-invariant is imprecise"** — The term is used informally and is clear in context; this is a phrasing preference, not a substantive flaw.
3. **"Downstream RL evaluation missing"** — The paper explicitly scopes itself to representation learning and includes a downstream planning task. Requiring goal-conditioned RL experiments is scope creep.
4. **"Behavior policy coverage analysis missing"** — This asks for additional experiments beyond the paper's stated scope.
5. **"Planning task under-documented in main text"** — Appendix H (stripped) covers this; main-text space constraints are reasonable.
6. **Strength removed: "Clear motivation and well-scoped problem"** — Generic framing applicable to many papers; not specific enough to warrant retention as a distinguishing strength.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a seed-count inconsistency and a missing symmetric ablation that the paper does not discuss, but these are gaps in the paper's evidence, not novel insights.

## Suggestions

1. **Resolve the seed-count inconsistency.** State clearly how many seeds are used for each figure/table and why. Use consistent reporting throughout.
2. **Add a MadDist-Symmetric ablation.** Keep all algorithmic components identical but substitute a symmetric distance (e.g., Euclidean) for the quasimetric. This will directly isolate the value of asymmetry from the value of the algorithmic changes.
3. **Diagnose or de-emphasize TDMadDist.** Either (a) provide analysis of why bootstrapping fails (e.g., ablation of $\beta$, comparison of TD vs. Monte Carlo targets) or (b) reframe TDMadDist as a negative result with explicit discussion of the failure mode.
4. **Support the $d_{\text{simple}}$ superiority claim in the main text** with at least a summary statistic from the quasimetric ablation.
5. **Add standard deviation or confidence intervals** to Figure 3 instead of min-max bands, or increase the number of seeds for more robust min-max estimates.

---

### Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| AP0ndQloqR.md | 7.50 | 1 | Yes | Strong theoretical paper with heavy positives (+7.40). My paper lacks this level of theoretical depth. |
| GwKNdRc9Bj.md | 3.75 | 1 | Yes | Weak experimental results (-4.68, -5.31, -6.49). My paper's negatives are far milder. |
| I7DeajDEx7.md | 6.75 | 1 | Yes | Novelty concerns (-9.74) drag it down. My paper has cleaner contributions but less impact. |
| dkn9cEOQkU.md | 5.50 | 1 | Yes | Real-robot evaluation was weak (-9.05). My paper's evaluation issues are less severe. |
| TOiageVNru.md | 6.00 | 2 | Yes | Similar profile: solid method with evaluation gaps. Their negatives (-4.22, -2.93) are somewhat worse than mine. |
| qofh48zW3T.md | 6.00 | 2 | Yes | Massive proposition correctness issue (-10.99) balanced by strong positives (+7.20). My paper lacks such severe swings. |
| s9SVlWOcLt.md | 6.75 | 2 | Yes | Strong theory but severe presentation criticisms (-9.77). My weaknesses are more moderate. |

**Final score rationale:** The paper's strongest weaknesses (-2.93 for TDMadDist diagnostic gap, -1.26 for unsupported claim, -1.05 for seed inconsistency) are all significantly milder than the double-digit negatives seen in the 6.00-level anchors (TOiageVNru had -4.22, qofh48zW3T had -10.99). Conversely, the paper's strengths (+4.77, +4.53, +4.19) are solid but not exceptional compared to the +7+ items in the same anchors. The seed inconsistency is the most concerning issue as it undermines the credibility of the quantitative evaluation, but it is fixable and does not invalidate the core approach. The paper makes genuine contributions (the benchmark suite, the algorithmic framework, the attention to asymmetry) that position it appropriately for borderline acceptance pending the identified revisions.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>