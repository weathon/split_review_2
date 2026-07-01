Now let me produce the final review.

## Summary

The paper presents TDDM (Temporal Deaggregation Diffusion Model), a hierarchical framework for trajectory generation that factorizes the problem into spatial occupancy priors (marginal distributions over where people move) and temporal dynamics (how people move). The spatial prior is used to condition a diffusion transformer, and canonicalization via similarity transform enables parameter sharing across regions. The method is evaluated on three city-scale datasets (Geolife, Porto, Cabspotting) and shows improvements over unconditional baselines on distributional metrics, with additional experiments on intra-city and cross-city generalization.

## Strengths

1. **Well-motivated spatial-temporal factorization.** The insight that trajectory generation can be separated into *where* people move (occupancy prior H) and *how* they move (temporal dynamics) directly addresses a real limitation of existing models that either provide no spatial control or condition on full trajectory samples. The pipeline (partition → canonicalize → compute prior → conditionally generate) is architecturally clean and changes how the problem is set up, not just which optimizer is used.

2. **Canonicalization via similarity transform is a practical contribution.** Rather than building group-equivariant architectures, normalizing each region via translation, rotation, and scaling (Section 3, lines 119–123) lets a single transformer learn dynamics invariant to absolute position and orientation, keeping the architecture lightweight.

3. **Cross-city generalization experiments produce novel findings.** The observation that training on Porto generalizes *better* to other cities than training on 25% of the target city itself (lines 305–306) is genuinely non-obvious and scientifically valuable. The intra-city quadrant setup cleanly tests whether the model learns transferable dynamics rather than memorizing local patterns.

## Weaknesses

### Major

1. **Asymmetric comparison in the main unconditional generation experiment (Table 1).** TDDM receives the spatial prior H — a 64×64 grid of occupancy probabilities computed *from the real target data* — while the baselines (Diffusion-TS, DiffTraj, TimeGAN, etc.) receive no equivalent conditioning signal. The ablation study (Table 2) confirms that removing H causes TDDM's KL_sym to jump from 0.277 to 1.334, which is *worse* than Diffusion-TS (1.153) and DiffTraj (1.232). This means the temporal dynamics model (the diffusion transformer) is weaker than standard diffusion baselines at the generative task when H is removed, and the headline performance is substantially attributable to the conditioning signal.

   The paper calls this "unconditional trajectory generation" (Section 4.1) despite TDDM conditioning on aggregate target statistics. The central comparison conflates the benefit of the conditioning framework with superior temporal dynamics. The authors should either (a) give baselines access to the same spatial prior H as a conditioning input, or (b) clearly frame the comparison as conditioned vs. unconditioned and acknowledge that the improvement comes from the factorization framework itself, not from a better temporal dynamics model.

2. **The "zero-shot" claim requires qualification.** Algorithm 2 (line 3) computes H = f(r_c, X_target) — the spatial prior is estimated from the *target city's real trajectories*. The model does not see individual target trajectories, but it receives an aggregate summary statistic derived from them. In many real-world applications where one wants to generate trajectories for a new city, no trajectory data from that city may be available at all. The paper discusses computing H from "X_target trajectories" without addressing the scenario where no target trajectories exist. The framing should be "few-shot" or "aggregate-shot" — the model requires no gradient updates on target data but does require target aggregate statistics.

### Minor

3. **No statistical significance or variance for most metrics.** Across Tables 1–3, standard deviations are only reported for TSTR. For KL_sym, JS, Density, Trip, Length, and Pattern, no variance or confidence intervals are given. The KL differences between TDDM and baselines are large, but without multiple-seed variance the reader cannot assess stability. For TSTR (where std dev *is* reported), the difference between TDDM (0.011 ± 0.006) and DiffTraj (0.013 ± 0.005) is within one standard deviation.

4. **KL divergence computation is underspecified.** KL divergence on continuous 2D trajectories requires binning or density estimation. The paper uses a 64×64 grid for H but does not specify whether the KL divergences in Tables 1–3 are computed on that same grid, a different resolution, or via KDE. KL is sensitive to bin resolution and boundary handling; this information is needed for reproducibility.

5. **Trajectories crossing region boundaries are not addressed.** The method generates within fixed-size (3×3 km) regions, with only a brief mention of "partial border overlap" (line 115). The paper does not explain how trajectories that span multiple regions are handled — whether they are stitched, whether independent per-region trajectories are treated as separate samples, or how the system produces coherent long-range trajectories that cross region boundaries.

6. **The "benchmark" contribution is somewhat inflated.** The paper lists "Benchmarking at Scale" as a main contribution, but this consists of three existing datasets (Geolife, Porto, Cabspotting) with existing metrics (KL, JS, TSTR, Density/Trip/Length/Pattern), run through a common preprocessing pipeline. No release of standardized splits, code, or a reusable evaluation resource is described in the main text. The evaluation framework is a useful methodological choice for the paper's own experiments, but claiming it as a "benchmark" contribution overstates what is being offered to the community.

### Trivial

None.

## Nice-to-Haves

- Conditioning the baselines on H (or an equivalent spatial prior) to test whether TDDM's advantage comes specifically from the deaggregation architecture or simply from having access to marginal distribution information.
- Exploring whether H can be derived from non-trajectory sources (census data, land-use maps, OpenStreetMap) to truly enable generation without any target-city trajectory data.
- Reporting all metrics with multiple-seed variance.

## Removed Points

These points from the input review are removed with justification:

1. **Map-matching pipeline criticism** — The harsh critic questioned the "map matching... before GPS noise is added back" pipeline as odd, and argued the conclusion about the deaggregation framework doesn't follow from the map-matching ablation. The map-matching + noise re-addition is a standard preprocessing technique (aligning trajectories to roads then simulating realistic GPS noise). The conclusion is supported by the relative ordering holding with and without map-matching — a reasonable if imperfect argument. Removed as a misunderstanding of standard practice.

2. **"Motivation about memorization is unsupported"** — The harsh critic notes the claim that sample-specific conditioning "increases the risk of memorization and prevents cross-region generalization" (lines 28–29) is unsupported. This is a motivation statement framing the approach, not an experimental claim requiring proof. Removed as category-driven noise.

3. **Code/release availability concern** — The critic notes "no code release mentioned in the main text." Per Hard Rules, criticisms questioning the release status or availability of any cited entity must be removed. Removed.

## Novel Insights

The most distinctive finding beyond the paper's own contributions is that a model trained on Porto generalizes to other cities (KL_sym 0.335) better than a model trained on 25% of the target city itself (KL_sym 0.545), suggesting that certain cities serve as "universal" mobility sources with representative temporal dynamics. This is a genuinely non-obvious empirical pattern that could be practically exploited.

## Suggestions

1. Reframe the main comparison to acknowledge that TDDM is a conditioned method whereas the baselines are unconditioned. Clearly attribute the improvement to the factorization framework (spatial prior + temporal dynamics) rather than implying superior temporal dynamics.
2. Add multiple-seed variance estimates for KL and other distributional metrics.
3. Specify how KL divergence is computed (grid resolution, binning approach, boundary handling).
4. Qualify the "zero-shot" terminology: clarify that H requires target aggregate statistics, but the model requires no gradient updates on target data.
5. Address how cross-region trajectories are handled, or explicitly scope the method to per-region generation.

## Score and Decision

### Calibration

**Round 1 Bracket:** 4.0–6.0 (based on initial content analysis)

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/dDdxbdhMsY.md` | 5.0 | R1 | Earlier version of the same paper ("Deep Temporal Deaggregation"). Had no ablation study, no std dev — weaknesses the current version improves. Current version is better but still has the asymmetric comparison issue. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/r125wFo0L3.md` | 5.0 | R1+R2 | "Large Trajectory Models" — autonomous driving trajectory prediction. All reviewers gave 5. Cleaner evaluation but different task (prediction vs. generation). |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/VRFotuGLfM.md` | 6.2 | R1 | "DiffMove" — human trajectory recovery with conditional diffusion. Clearer task, cleaner evaluation, solid SOTA claims. Current paper is less clean methodologically. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5IvTw0qMKj.md` | 4.67 | R2 | "C²INet" — trajectory prediction with continual causal intervention. Different task. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/VaoeAi5CW8.md` | 4.25 | R2 | "DTP" — diffusion trajectory-guided policy for robot manipulation. Different domain. |

**Narrowing:** The earlier version of this paper (dDdxbdhMsY) scored 5.0 with scores [6,6,3]. The current version improves on the weaknesses that led to the 3 (adding ablation study) but still has structural issues (asymmetric comparison, zero-shot overclaiming). It is meaningfully improved from the 5.0 anchor but does not reach the clarity and evaluation quality of DiffMove (6.2). The structural issues in the main comparison prevent it from crossing the accept threshold.

**Final Score: 5.0**
**Final Decision: Reject**

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>