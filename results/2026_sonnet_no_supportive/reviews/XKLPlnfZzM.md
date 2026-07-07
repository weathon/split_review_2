## Summary
TDDM (Temporal Deaggregation Diffusion Model) proposes a hierarchical framework for GPS trajectory generation that factorizes mobility into *where* (a spatial occupancy prior H) and *how* (temporal dynamics conditioned on H). Each geographic region is canonicalized via similarity transform, enabling cross-region parameter sharing. The paper introduces a three-city benchmark (Beijing/Porto/San Francisco) and demonstrates improved distributional metrics over prior generative baselines, plus city-to-city zero-shot transfer.

## Strengths
- **Spatial-temporal factorization is a genuine design insight.** Separating marginal spatial occupancy H from temporal generation is principled and mechanistically well-specified. The three-step pipeline (partition → canonicalize → condition) is internally consistent and described clearly in Section 3.
- **Canonicalization via similarity transform is an elegant architectural choice.** Rather than building equivariance into the model, the paper normalizes coordinates to [−1,1]² and inverts at generation time (Section 3). This is lightweight and makes zero-shot cross-region transfer structurally possible rather than hoped for.
- **Ablation isolates the mechanism correctly.** Table 2 shows KL_sym degrading from 0.277 to 1.334 without spatial priors (~5×), confirming the central mechanistic claim.
- **Cross-city generalization is empirically substantiated.** Table 3 shows that a model trained on Porto achieves KL_sym=0.335 and JS=0.071 on unseen cities, outperforming training on 25% local data (KL_sym=0.545, JS=0.106), a substantive finding.
- **Benchmark contribution.** Standardized evaluation across three datasets on three continents with a coherent set of metrics covering fidelity, coverage, proportionality, and usefulness is a practical community contribution.

## Weaknesses

### Fatal
None.

### Major
- **Asymmetric comparison in Table 1.** Section 2 defines the task as unconditional generation, but TDDM is a conditional model: H is computed from real training trajectories (Algorithm 1, line 3) and supplied at generation time, while all baselines are truly unconditional. The KL divergence metrics in Table 1 measure spatial distributional alignment — precisely the quantity H encodes. The 4× KL improvement over Diffusion-TS (0.277 vs. 1.153) is therefore at least partially a mechanical consequence of conditioning on the true spatial marginal, not purely a consequence of a superior architecture. The ablation (Table 2) itself confirms that removing the spatial prior collapses TDDM's KL performance to near-baseline level (1.334 vs. Diffusion-TS's 1.153). The paper provides no similarly-conditioned baseline to isolate how much of the gain comes from H vs. the architecture. The comparison should be framed explicitly as demonstrating the value of spatial conditioning as a design choice, not as an unconditional model comparison.

- **"Zero-shot" framing is softer than claimed.** Algorithm 2, line 3 explicitly reads: *"Compute heatmap H = f(r_c, X_target)"* — H is computed from actual target-city trajectories. No gradient updates occur on the model weights, but the model receives aggregate statistics derived from ground-truth target data. Section 3 acknowledges that "H can be estimated (even in unseen cities)" from other sources, but the paper never demonstrates this. As evaluated, the experiment answers "can a model trained on one city generalize if given target aggregate statistics?" — a real and useful capability, but not as strong as the "zero-shot" framing implies. The language should be calibrated accordingly, or an experiment estimating H from proxies (OpenStreetMap road density, population heatmaps) should be added.

### Minor
- **KL gains may not reflect temporal quality.** The KL metrics evaluate spatial distributional alignment — exactly what H conditions on. The temporal quality metric TSTR shows a much smaller improvement (0.011 vs. 0.013 for DiffTraj) with overlapping standard deviations (±0.006 and ±0.005), and it is unclear whether this improvement is statistically significant. A short discussion clarifying that spatial KL gains are partly mechanistic while temporal quality improvements are smaller would give a more honest picture of the overall advance.

- **"w/o spatial prior + rejection" ablation condition is unexplained.** Table 2 includes this variant but the main text provides no description of what rejection sampling scheme is used or what hypothesis it tests.

### Trivial
None.

## Nice-to-Haves
- Demonstrate H estimation from proxy sources (e.g., OpenStreetMap road density) rather than target trajectories — this would genuinely earn the strong "zero-shot" claim.
- Add a similarly-conditioned baseline to Table 1 (e.g., Diffusion-TS conditioned on the same H via token prepending) to isolate the architectural contribution from the conditioning signal.
- Ablate grid resolution (currently fixed at 64×64); the tradeoff argument given in Section 3 is reasonable but not experimentally verified.
- Report wall-clock training and inference times; the 64×64 grid adds quadratic transformer token cost that is relevant for practitioners.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **DiffTraj baseline degradation concern**: The reviewer speculates DiffTraj may run in a degraded mode without its original conditioning signal, making the baseline unfair. Since the asymmetry in this case would favor the baseline (DiffTraj without conditioning is weaker), the rule is to remove criticisms where the asymmetry favors the baseline rather than the author's method. Removed.
- **Privacy analysis**: The paper explicitly scopes out privacy in Section 1 ("this work focuses exclusively on improving fidelity and cross-region generalization"). Removed as out-of-scope.
- **Porto confound (density/length) in cross-city transfer**: The reviewer speculates Porto's longer/denser trajectories may inflate H informativeness. The paper already addresses this in Section 4.3 ("Porto exhibits a heavier-tailed distribution than Cabspotting") and acknowledges Length error as the main failure mode. The criticism is speculative rather than demonstrated. Removed.
- **Statistical significance of TSTR difference**: Noted in Minor above; not a separate weakness to carry at the Major level.

## Novel Insights
The paper's most useful empirical finding is that aggregate spatial occupancy H, computed at the population level, is sufficient to drive both in-distribution quality and cross-city generalization, implying a practical principle: *where* people move transfers across cities, while *how* they move at the individual level does not. The ancillary finding that Porto outperforms 25% local training data as a "universal source dataset" is an unexpected and practically actionable result — it suggests that careful source dataset selection may substitute for modest local data collection in mobility modeling deployments.

## Suggestions
1. Re-frame Section 4.1 and Table 1 explicitly: TDDM is a conditional model compared against unconditional baselines; the experiment demonstrates the value of spatial conditioning, not a head-to-head on the same task.
2. Rename "zero-shot" to "aggregate-conditioned transfer" or add a proxy-H experiment to substantiate the stronger claim.
3. Explain the "w/o spatial prior + rejection" ablation in the main text.
4. Add a simple conditional baseline to Table 1 to isolate architectural gains from conditioning gains.

---

## Calibration Anchors

| Path | Avg Score | Round | Comparison to paper |
|---|---|---|---|
| dDdxbdhMsY | 5.00 | 1 | Earlier version of same paper (TDDPM); current paper adds city-to-city transfer, richer metrics, cleaner ablation — clear improvement over the 5.0-scored prior |
| 2orBSi7pvi | 3.00 | 1 | Spatio-temporal diffusion for time series; weaker contribution and narrower evaluation than this paper |
| 1o3fKLQPRA | 4.50 | 1 | DiffPath road-network path generation; similar domain but narrower task and smaller benchmark |
| r125wFo0L3 | 5.00 | 1 | Large Trajectory Models for autonomous driving; different task (prediction) but similar spatial-temporal scope |
| VRFotuGLfM | 6.20 | 2 | DiffMove trajectory recovery; similar domain and conditional diffusion approach, comparable contribution level |
| 9aTZf71uiD | 6.00 | 2 | UniTraj, unified trajectory generation model; closest in scope and quality level |
| WeJEidTzff | 6.75 | 2 | OD flow generation benchmark; comparable benchmark contribution with solid empirical work |
| IcbC9F9xJ7 | 6.50 | 2 | Conditional diffusion for single-cell analysis; conditional modeling with asymmetric baseline issue but strong results |

**Round 1 bracket:** 5.5 – 7.0  
The paper is a clear improvement over the 5.0-scored prior version (dDdxbdhMsY). The major weaknesses (comparison framing asymmetry, zero-shot language) are substantive enough to prevent a clear-accept score. Similar papers with clean conditional baselines and well-framed comparisons score 6.0–6.75.

**Round 2 narrowing:** Anchors at 6.0 (9aTZf71uiD) and 6.2 (VRFotuGLfM) have comparable contribution depth. The TDDM paper's contribution is real, the benchmark is valuable, and the ablation is well-targeted — but the unacknowledged comparison asymmetry in the main result table is a significant presentation/framing gap. Final score: **6.0**.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>