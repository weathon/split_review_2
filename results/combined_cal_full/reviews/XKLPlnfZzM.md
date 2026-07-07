## Summary

This paper proposes TDDM, a hierarchical framework that factorizes trajectory generation into spatial occupancy priors (marginal distributions over geographic occupancy) and temporal dynamics learned by a diffusion model. By canonicalizing regions via similarity transforms before modeling, TDDM enables a single model to process trajectories from any geographic region and transfer across cities. Evaluated on three cities across three continents, the method shows strong distributional alignment (lower KL divergences) and demonstrates that a model trained on one city (Porto) can generalize to others using only aggregate spatial information from the target.

## Strengths

- **Well-motivated factorization of spatial from temporal dynamics.** The paper clearly explains (Section 3) why existing approaches are limited — sample-specific conditioning (DiffTraj, ControlTraj) ties each generation to a training trajectory, while unconditional methods (Diffusion-TS) provide no control. Conditioning on aggregate spatial marginal distributions is a sensible middle ground that the paper motivates and uses consistently.

- **Canonicalization via similarity transforms (Section 3) is a pragmatic design choice that demonstrably works.** Rather than imposing group-equivariant inductive biases into the architecture, TDDM canonicalizes regions before feeding them to the model. The cross-city transfer results (Table 3) provide concrete evidence: a model trained on Porto generates reasonable trajectories for San Francisco, showing that the design choice achieves its goal.

- **The cross-city transfer finding (Section 4.3) is genuinely informative and non-obvious.** Training on Porto often generalizes better to other cities than training on 25% of the target city (KL_sym 0.335 vs. 0.545). This provides practical guidance: for distributional coverage, a well-chosen source city may be preferable to limited local data.

- **Comprehensive evaluation framework.** Three cities across three continents, multiple complementary metrics (KL divergences in both directions, JS, density/trip/length errors, pattern score, TSTR with standard deviations), and both in-distribution and out-of-distribution settings.

## Weaknesses

### Major

- **The headline comparison (Table 1) is not appropriately contextualized regarding the role of the conditioning signal.** TDDM generates trajectories conditioned on spatial priors H (a 64×64 grid encoding marginal occupancy), while baselines like Diffusion-TS and DiffTraj receive no such spatial information. The paper's own ablation (Table 2, "w/o spatial prior") shows TDDM without spatial priors achieves KL_sym=1.334 — *worse* than both Diffusion-TS (1.153) and DiffTraj (1.232). This confirms that the large margins in Table 1 (KL_sym 0.277 vs. 1.153) are primarily driven by the conditioning signal, not by superior temporal dynamics modeling. The paper should make this distinction explicit in the abstract and introduction rather than framing the comparison as uniform architectural superiority.

### Minor

- **KL divergences and most metrics in Tables 1 and 2 are reported only as point estimates averaged across three datasets, without variance, confidence intervals, or statistical significance.** TSTR values include ±std, but for the metrics showing the largest improvements (KL_sym, JS, Density, Trip), the reader cannot assess whether the reported differences are robust. The per-city results are relegated to the appendix (which is stripped from the submission); the main text should at minimum show per-city variation for the headline metrics.

- **The claim of "zero-shot" generalization (abstract, contribution list) is overstated.** Algorithm 2 line 3 explicitly computes H from X_target (real trajectories from the target region). The method always needs aggregate trajectory data from any region it generates for. While the model does not need per-trajectory labels or fine-tuning — a genuine strength — describing this as "zero-shot" implies generalization with no target data at all, which is inaccurate. "Aggregate-conditioned transfer" would be more precise.

- **The ablation condition "w/o spatial prior + rejection" appears in Table 2 but is never described in the main text.** Section 4.2 only discusses "removing spatial priors" and "reducing partition size." If this is rejection sampling (generate unconditionally, then filter by the spatial prior), it is an informative baseline that should be explained.

- **The paper does not explain how trajectories that cross region boundaries are handled during generation.** It mentions "partial border overlap" (Section 3, paragraph on partitioning) but provides no mechanism for ensuring coherent trajectories across regions. Since trajectories are generated independently per region (Algorithm 2), a trajectory near a boundary would be truncated or split across two independent generations, creating discontinuities. The paper should clarify whether this is a limitation or whether there is a mechanism not described.

- **The TSTR definition (Section 4) states "The resulting model is then evaluated on the training data" — this is ambiguous.** In a "Train on Synthetic, Test on Real" protocol, the evaluation should use held-out real data. The intended meaning is likely correct, but the wording should be clarified.

### Trivial

- **Coordinate range inconsistency:** Section 3 (text) states canonicalization maps to [-1, 1]^D, while Algorithm 1 line 6 and Algorithm 2 line 11 use [0, 1]^D. This should be resolved.

## Nice-to-Haves

- An ablation removing canonicalization (i.e., training on raw coordinates) would isolate the contribution of this design choice and strengthen the paper's claims about its importance for transfer.
- Providing baselines conditioned on the same spatial prior (e.g., adding H as conditioning to Diffusion-TS or DiffTraj) would enable a more direct architectural comparison. However, this is a substantial engineering effort and not required for acceptance.
- A finer-grained analysis of what temporal properties transfer poorly across cities — the length error degrades by 20-30× in cross-city transfer (0.003 → 0.06–0.11), which the paper mentions but does not deeply analyze.

## Removed Points

These points from the input reviews are flagged to be removed; treat them with caution.

- **"The comparison is structurally unfair"** (the critic's Critical Issue 1): This phrasing was too strong. Comparing the full method against unconditioned baselines is a legitimate evaluation of the proposed approach. The retained [Major] weakness above reflects only the insufficient *contextualization* of the comparison, not unfairness.
- **Suggestion that baselines should be retrofitted with spatial-prior conditioning:** This is a reasonable future direction but not a requirement for this paper's evaluation. The baselines are not designed for this conditioning, and retrofitting them is non-trivial.
- **Generic strength about the problem being important:** Every paper at this venue addresses an important problem.
- **Reproducibility nitpicks about undisclosed hyperparameters:** Hyperparameters are referenced to Appendix C, which is stripped by the parser.
- **Missing related works criticism:** Cannot be verified without external sources.

## Novel Insights

The most striking finding is that training on Porto generalizes to other cities better than training on 25% of the target city. This suggests that some cities capture temporal dynamics that are broadly representative across urban contexts, and that the spatial-prior factorization successfully decouples location-specific patterns from transferable motion dynamics. The fact that this holds across three continents and qualitatively different trajectory types (pedestrian/Geolife vs. taxi/Porto vs. taxi/Cabspotting) strengthens the claim that the factorization captures something fundamental about urban mobility.

## Suggestions

1. Reframe the abstract and introduction to describe Table 1 as an evaluation of the full TDDM system (spatial priors + temporal dynamics) vs. unconditional baselines, and clearly cite the ablation (Table 2, "w/o spatial prior") to show that the conditioning is responsible for the large margins.
2. Report per-city KL divergences in the main text or add bootstrapped confidence intervals.
3. Explain the "w/o spatial prior + rejection" ablation in the text.
4. Clarify how region-boundary trajectories are handled (or explicitly state this as a limitation).
5. Clarify the TSTR evaluation data split.
6. Resolve the [0,1]^D vs [-1,1]^D coordinate inconsistency.

## Score and Decision

**Calibration anchors consulted:**

| Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/dDdxbdhMsY.md` (Deep Temporal Deaggregation) | 5.00 | R1 | Yes | Close sibling paper with same core idea but weaker experiments and no ablation study. Current paper is substantially stronger. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/VRFotuGLfM.md` (DiffMove) | 6.20 | R1/R2 | Yes | Trajectory recovery with diffusion; had severe "lacks innovation" (-7.49) and "novelty limited" (-8.71) weaknesses that the current paper avoids. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/1o3fKLQPRA.md` (DiffPath) | 4.50 | R1 | Yes | Path generation; had multiple severe weaknesses (-7.27 core contribution, -8.93 motivation, -9.70 novelty). Current paper is clearly stronger. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/4anfpHj0wf.md` (Point Set Diffusion) | 7.00 | R2 | No | Cleaner theoretical framing and experiments; higher bar than current paper. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/MbM1BqGpZu.md` (Diff Transformer Theory) | 6.75 | R2 | No | Theory paper; different scope. |

**Round 1 bracket:** 5.5–7.0 (above dDdxbdhMsY at 5.00 and DiffPath at 4.50; comparable to DiffMove at 6.20; below Point Set Diffusion at 7.00).

**Narrowing:** Comparing weighted items, the current paper's strongest negative weights are -2.88 (comparison contextualization), -2.12 (region boundaries), and -2.10 (missing variance). DiffMove's strongest negatives were -7.49 and -8.71 (both about limited novelty/innovation) — weaknesses the current paper does not share. The current paper shares the "missing variance on KL" issue with dDdxbdhMsY (-0.70) and DiffMove's minor concerns, but lacks the fatal "no ablation" and "unclear contributions" issues of dDdxbdhMsY (-4.42, -3.04). The paper's strengths are well-grounded (factorization motivation +5.14, canonicalization +4.00) compared to the anchors' strength ranges.

**Final score: 6.0.** The paper has a clear, well-motivated contribution and solid experimental support. It is not a clear accept because: (1) the headline comparison is framed in a way that could mislead readers about the source of improvement, (2) key metrics lack variance estimates, (3) the "zero-shot" framing overstates the method's generalization capabilities, and (4) the region-boundary handling is unaddressed. All of these are fixable with reframing and additional analysis, and the core idea is sound.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>