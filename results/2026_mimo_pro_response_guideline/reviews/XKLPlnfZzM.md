Now I have enough data. Let me finalize the review with calibration.

**Calibration Analysis:**

Key anchors retrieved:
1. **dDdxbdhMsY** (avg 5.0, Reject) — Earlier version of essentially the same paper (TDDPM / "Deep Temporal Deaggregation"). Lacked ablation, more metrics, clear contributions.
2. **1o3fKLQPRA** (avg 4.5, Reject) — DiffPath, path generation with LDM. Limited novelty, insufficient experiments.
3. **kKXIYUi8ff** (avg 3.0, Reject) — DynamicsDiffusion for molecular trajectories. Novel idea but major issues.
4. **VRFotuGLfM** (avg 6.2, Reject) — DiffMove, trajectory recovery via conditional diffusion. Good but incremental.
5. **4anfpHj0wf** (avg 7.0, Accept) — Point Set Diffusion. Novel method, strong results, good writing.
6. **H8hO3T3DYe** (avg 5.67, Accept) — Partially Observed Trajectory Inference with OT.
7. **VRFotuGLfM** (avg 6.2, Reject) — Graph generation with diffusion mixture.

**Round 1 Bracket:** The paper under review is substantially improved from the earlier rejected version (dDdxbdhMsY, score 5.0) — it addresses nearly all reviewer concerns (added ablation, more metrics, better framing, city-to-city transfer). Compared to DiffMove (6.2, Reject), TDDM has more novel factorization and broader evaluation. It is close to but slightly below Point Set Diffusion (7.0, Accept), which had more methodological novelty in the generative modeling itself. The informational asymmetry issue is the main ceiling factor. Bracket: **6.5 – 7.0**.

Given that the in-distribution results are strong on their own (Table 1), the ablation is clean, and the cross-city generalization mechanism is genuinely novel even with the framing caveat, I settle on **7.0**.

---

## Summary

This paper introduces TDDM (Temporal Deaggregation Diffusion Model), a trajectory generation framework that factorizes generation into spatial priors (marginal occupancy distributions over regions) and temporal dynamics (a conditional diffusion model). Each spatial region is canonicalized via a similarity transform, enabling a single model to generalize across geographic locations. Evaluated on three datasets across three continents, TDDM achieves ~4× improvement in KL divergence over the best baselines and demonstrates cross-city generalization.

## Strengths

- **Clean, principled spatial-temporal factorization**: The core idea — decomposing trajectory generation into *where* (spatial priors) and *how* (temporal dynamics) people move — is formalized as a mixture model over region partitions (Eqs. 1–5). The canonicalization via similarity transform is elegant, achieving location/rotation invariance without requiring equivariant architectures. This is a genuinely different approach from prior work (unconditional models like Diffusion-TS, sample-specific conditioning like DiffTraj).

- **Large, consistent distributional improvements**: Table 1 shows TDDM achieves KL_sym of 0.277 vs. 1.153 for Diffusion-TS (next best), JS of 0.059 vs. 0.198, and Density/Trip errors of 0.019/0.031 vs. 0.029/0.041. These ~4× improvements hold consistently across all three datasets spanning Beijing, Porto, and San Francisco.

- **Novel cross-city generalization capability**: Table 3 shows training on Porto yields KL_sym of 0.335 for unseen cities, better than training on 25% of the target city's own data (0.545). The finding that Porto acts as an unexpectedly strong "universal source dataset" is a novel and practically useful empirical insight.

- **Well-designed ablation isolating spatial prior contribution**: Table 2 cleanly shows that removing spatial priors degrades KL_sym by ~5× (0.277 → 1.334) while TSTR stays constant (0.011), directly evidencing that spatial priors drive coverage/proportionality rather than temporal fidelity. The region-size ablation (1×1 vs. 3×3 km) reveals a meaningful tradeoff between local coherence and global realism.

- **Comprehensive evaluation framework**: Six metrics spanning five quality dimensions (fidelity, diversity, proportionality, usefulness, generalization) across three geographically diverse datasets on three continents, with five baselines spanning GAN, VAE, and diffusion paradigms plus multi-channel approaches.

## Weaknesses

### Fatal
None

### Major
- **Informational asymmetry in OOD evaluation needs clearer framing**: In city-to-city and intra-city experiments (Table 3), TDDM computes spatial priors from the target region's real data (Algorithm 2, line 3: `H = f(r_c, X_target)`), while all baselines have no mechanism to incorporate any target information. The paper states it is "zero-shot" because "no gradient updates occur on target trajectories" (Section 4.3) and is transparent about using X_target, but the results are presented without discussing this asymmetry relative to baselines. A reader expecting "zero-shot" to mean "no access to target data" would be misled. The contribution — generalizing via aggregate statistics alone — is genuinely valuable, but the framing should be explicit: TDDM is zero-shot in the parameter-update sense, but does condition on the target region's spatial distribution. This matters because the headline generalization claims (contributions 4, abstract, conclusion) are the paper's most novel selling point.

### Minor
- **Single-run evaluation without variance for headline metrics**: Table 1 explicitly states "Models are trained, sampled and evaluated once per dataset." While TSTR reports standard deviations, KL-based and other metrics are single-point estimates. The KL differences are large enough to be robust (0.277 vs. 1.153), but smaller improvements — Pattern (0.917 vs. 0.907), Length (0.004 vs. 0.003), Density (0.019 vs. 0.029) — could plausibly vary across seeds. The claim "TDDM matches Diffusion-TS at state of the art on Length error" (Section 4.1) cannot be established from a single run.

- **Coordinate normalization range inconsistency**: Section 3 states canonicalization maps to [-1, 1]^D (line 121), while Algorithm 1 line 6 and Algorithm 2 line 11 normalize to [0, 1]^D. This should be resolved for reproducibility.

### Trivial
None

## Nice-to-Haves
- Adding a control experiment for OOD evaluation where a baseline (e.g., DiffTraj or Diffusion-TS) is also conditioned on the target spatial prior would isolate whether the improvement comes from the factorization mechanism or simply from having target information. If no baseline can be adapted to use spatial priors, this would actually *strengthen* the paper's argument.
- Reporting compute/efficiency metrics (training time, inference time, model size) would contextualize results, given the quadratic token cost of the 64×64 spatial grid in the transformer.
- Discussion of sensitivity to spatial prior quality (e.g., sparse target data) would strengthen practical applicability.

## Removed Points
These points are flagged to be removed, treat them with caution.
- None — all points from the inputs were either verified against the paper or filtered out by the rules.

## Novel Insights
The finding that cross-city transfer from Porto yields stronger distributional alignment than training on 25% of the target city's own data (KL_sym 0.335 vs. 0.545) is a genuinely novel empirical observation revealing that certain cities may act as broadly representative source datasets. This practical insight — that a carefully chosen training city can outperform limited local data for spatial coverage tasks — is valuable for the mobility community and is not demonstrated by any baseline method.

## Suggestions
- Add explicit framing about the informational setup in OOD experiments — a single sentence in the abstract, contributions, and Section 4.3 clarifying that "zero-shot" means no gradient updates but conditioning on target aggregate spatial statistics.
- Run 3–5 seeds for the main comparison table to report variance on KL, Density, Trip, Length, and Pattern.
- Resolve the [-1,1]^D vs [0,1]^D normalization range inconsistency between the method text and algorithms.

## Calibration Report

**Round 1 anchors (all queries):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Uj0h13lVrR | 1.00 | R1 | KL divergence for GFlowNets; unrelated topic, very weak |
| u1cQYxRI1H | 0.50* | R1 | Diffusion for illumination; mislabeled, strong paper (10.0) |
| P49gSPmrvN | 1.00 | R1 | UMAP for discourse viz; rejected, not relevant |
| bEgDEyy2Yk | 1.00 | R1 | Graph algorithm implementation; rejected, not relevant |
| kKXIYUi8ff | 3.00 | R1 | DynamicsDiffusion for molecular trajectories; similar topic, rejected for major issues |
| 2orBSi7pvi | 3.00 | R1 | STDM for time series; related diffusion+time series, rejected for insufficient novelty |
| XeGSIr7z6u | 3.40 | R1 | Memorization-generalization in diffusion; theoretical, rejected |
| 46tjvA75h6 | 3.00 | R1 | EBM with diffusion; rejected, not directly relevant |
| dDdxbdhMsY | 5.00 | R1 | **Earlier version of same paper** (TDDPM); rejected for lacking ablation, metrics, clear contributions |
| 1o3fKLQPRA | 4.50 | R1 | DiffPath for path generation; limited novelty, rejected |
| r125wFo0L3 | 5.00 | R1 | Large trajectory models for autonomous driving; rejected, different setting |
| E2OAT195Le | 3.75 | R1 | Diffusion for network evolution; rejected, different domain |
| VRFotuGLfM | 6.20 | R1 | DiffMove for trajectory recovery; incremental, rejected |
| 4anfpHj0wf | 7.00 | R1 | Point Set Diffusion; novel method, accepted |
| H8hO3T3DYe | 5.67 | R1 | Trajectory inference with OT; accepted, different focus |
| UQVhOVhUi4 | 6.25 | R1 | Graph generation with diffusion; rejected |
| uKZdlihDDn | 7.60 | R1 | Diffusion for fluid simulations; accepted, strong |
| RuP17cJtZo | 8.00 | R1 | Generator Matching; theoretical framework, accepted |
| fV0t65OBUu | 8.00 | R1 | Covariance matching for diffusion; accepted, technical |
| EO8xpnW7aX | 8.00 | R1 | Discrete diffusion for permutations; accepted, novel |

**Round 1 Bracket:** 6.5 – 7.0. The paper is substantially stronger than its earlier version (dDdxbdhMsY, 5.0, Reject) which lacked ablation, more metrics, and city-to-city transfer. It is stronger than DiffMove (6.2, Reject) and DiffPath (4.5, Reject) in novelty and evaluation breadth. It is comparable to Point Set Diffusion (7.0, Accept), which had more methodological novelty but TDDM has broader practical evaluation and a unique generalization capability.

**Final score: 7.0.** The in-distribution results (Table 1) are strong independently of the OOD claims. The method is clean, the ablation is informative, and the evaluation is comprehensive. The OOD framing issue is real but does not undermine the core contribution — the mechanism of generalizing via aggregate spatial statistics is genuinely novel and useful, even if the "zero-shot" framing needs correction.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>