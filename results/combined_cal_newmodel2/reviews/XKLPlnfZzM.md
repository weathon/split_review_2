Now I'll produce the final consolidated review.

## Summary

This paper introduces the Temporal Deaggregation Diffusion Model (TDDM), which factorizes trajectory generation into two components: *where* people go (encoded as a spatial marginal distribution over geographic occupancy) and *how* they move temporally. The model conditions a transformer-based diffusion backbone on aggregate spatial priors rather than trajectory-level statistics, and achieves rotation/translation invariance through canonicalization via similarity transforms. The paper evaluates across three cities (Beijing, Porto, San Francisco) on multiple metrics and demonstrates zero-shot generalization to unseen cities using only the target city's aggregate spatial statistics.

## Strengths

- **Spatial-temporal factorization is a genuinely useful design insight.** The idea of decoupling where people go from how they get there is well-motivated and cleanly operationalized. Conditioning on aggregate spatial priors (rather than unconditional generation or sample-specific conditioning) splits the difference between controllability and generalization — a real conceptual contribution.

- **Canonicalization via similarity transforms is a practical engineering choice.** Rather than building group-equivariant architectures, the paper achieves rotation/translation invariance through input-output transformations (Section 3, lines 119–123). This keeps the architecture lightweight and cleanly separates invariance from the generative model.

- **The cross-city benchmark is thoughtfully constructed.** Three cities on three continents (Beijing, Porto, San Francisco) with standardized preprocessing, a diverse set of metrics spanning different quality axes (TSTR for usefulness, KL divergences for coverage/proportionality, Density/Trip/Length/Pattern for structural properties), and a shared data pipeline for all methods. This goes well beyond single-dataset evaluations common in this area.

- **The zero-shot generalization experiments test a genuinely important capability.** Demonstrating that a model trained on Porto can generate reasonable trajectories in Beijing or San Francisco without retraining — conditioned only on aggregate spatial statistics — is practically meaningful. The finding that Porto-trained models sometimes outperform partial-local training is a genuinely interesting empirical observation (lines 305–306).

## Weaknesses

### Fatal

None.

### Major

1. **The headline comparison (Table 1) frames TDDM as performing "unconditional trajectory generation" (Section 4.1, line 247), but TDDM receives the spatial marginal H of the target data during sampling (Algorithm 2, line 3).** The baselines (Diffusion-TS, DiffTraj, TimeGAN, etc.) are genuinely unconditional. The metrics on which TDDM shows the most dramatic gains — KL(R‖S), KL(S‖R), KL_sym, JS — all measure the spatial marginal distribution, which is exactly what TDDM receives as conditioning. The ablation confirms this interpretation: removing spatial priors causes KL_sym to jump from 0.277 to 1.334 (Table 2), comparable to Diffusion-TS at 1.153. This means the 4× KL improvement in Table 1 is largely attributable to the conditioning information, not to superior trajectory modeling per se. The paper should either (a) compare against baselines that also receive H as conditioning, or (b) substantially reframe the claims to acknowledge that TDDM operates with strictly more information. The current framing ("TDDM achieves the strongest overall performance, reducing distributional divergences by a large margin," line 249) overstates what is demonstrated.

2. **No comparison against a diffusion baseline that also receives H as conditioning.** Without this, the paper cannot separate the claim "H contains useful spatial information" (unsurprising and not architecture-specific) from the claim "TDDM's architecture uses H more effectively than alternatives would." The ablation shows that most of the KL improvement comes from H itself, not from TDDM's specific modeling of trajectories conditioned on H. A controlled comparison (e.g., feeding H into Diffusion-TS via a simple conditioning mechanism) would directly test whether TDDM's architecture-level design is superior.

3. **Across Tables 1–3, only TSTR is reported with ± values.** All KL divergences, Density, Trip, Length, and Pattern scores are reported as point estimates with no variance information. The paper states that models are "trained, sampled and evaluated once per dataset" (Table 1 caption). For metrics where margins are small (e.g., Pattern: 0.917 vs. 0.907; Length: 0.004 vs. 0.003), variance could reverse the ranking. Without uncertainty quantification, the significance of these differences cannot be assessed.

### Minor

4. **DiffTraj's conditioning configuration is not explained.** The paper describes DiffTraj as relying on "strong sample-specific conditioning" (line 19), but in Table 1 it is evaluated as an unconditional baseline. The paper does not explain how DiffTraj was configured for unconditional evaluation or what effect disabling its conditioning mechanism had on its performance. This is a comparison fairness concern.

5. **The canonicalization range is inconsistent between text and algorithms.** The similarity transform description (line 121) and Equation (2) state normalization to [-1, 1]^D. However, Algorithm 1 line 6, Algorithm 2 line 11, and the explanatory text on line 169 specify [0, 1]^D. This discrepancy affects reproducibility.

6. **The preprocessing states that "GPS noise is added back" after map matching (line 261) but does not specify the noise model, parameters, or whether this process is deterministic or stochastic.** This affects reproducibility and raises questions about data leakage between train and evaluation.

7. **The ablation condition "w/o spatial prior + rejection" (Table 2) is not explained.** If rejection simply discards samples that don't match H, this would artificially inflate quality metrics and the comparison may be uninformative.

### Trivial

8. The "zero-shot" terminology, while the paper is transparent about what it means, could be more precise. The model receives H from the target city (aggregate statistics of target trajectories), so "zero-shot" without qualification could mislead readers into thinking no target data is used at all.

## Nice-to-Haves

- A computational cost comparison (model size, training/inference time) relative to baselines would help practitioners assess practical trade-offs.
- The paper could strengthen the factorization claim by demonstrating that the same model generates different trajectories when given different spatial priors with the same noise seed.
- Analysis of what aspects of Porto make it a good universal source dataset (beyond the length distribution observation already present) would deepen the generalization findings.

## Removed Points

These points from the input review were removed with justifications:

- *"Sum to infinity in Algorithm 2 equation for N_{r_c}"* — PDF parser artifact; the original submission does not contain this error (per parser-artifact rule).
- *"Porto generalization observation lacks analysis"* — The paper *does* discuss this (lines 305–306), noting city-specific length distribution differences and suggesting Porto captures broadly representative dynamics. Factually incorrect as a weakness.
- *"Missing failure case analysis for intra-city transfer"* — Scope-expansion request, not a concrete weakness. The paper acknowledges the degradation and presents results.
- *Missing related works* — Cannot verify existence of missing references from external sources.
- *Formatting/style nitpicks* — Parser artifacts (typos, symbols, whitespace).

## Novel Insights

The harsh critic's decomposition of the conditioning asymmetry is the most valuable analytical contribution: it correctly identifies that the headline KL improvements are largely attributable to the spatial prior information rather than the generation architecture, and correctly notes that the ablation study accidentally serves as a confound check. The insight that the comparison should be restructured as "TDDM with H vs. baselines with H" (instead of "TDDM with H vs. baselines without H") is a genuinely useful framing that would substantially strengthen the paper's evidence.

## Suggestions

1. Restructure the main experiment to include a diffusion baseline (e.g., Diffusion-TS) that also receives H as conditioning — this directly tests whether TDDM's architecture uses H more effectively than alternatives.
2. Report uncertainty (mean ± std over multiple seeds) for all metrics in Tables 1–3, not just TSTR.
3. Clarify the canonicalization range inconsistency between text ([-1,1]^D) and algorithms ([0,1]^D).
4. Explain how DiffTraj was configured for the unconditional evaluation setting.
5. Explain the "rejection" mechanism in the ablation study.
6. Specify the noise model used when adding GPS noise back after map matching.
7. Qualify "zero-shot" as "aggregate-conditioned generation" to avoid potential misinterpretation.

**Calibration anchors used:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `dDdxbdhMsY` (Deep Temporal Deaggregation) | 5.00 | 1 → 2 | Yes | Precursor version of same work; current paper is stronger (adds metrics, ablation, baselines) but retains conditioning comparison gap |
| `VRFotuGLfM` (DiffMove) | 6.20 | 1 | Yes | Trajectory + diffusion + Geolife; milder weaknesses (datasets, efficiency); current paper has more fundamental conditioning asymmetry |
| `2whSvqwemU` (FM-TS) | 3.00 | 1 | Yes | Time series generation; weaker paper (novelty concerns, reproducibility) |
| `2orBSi7pvi` (STDM) | 3.00 | 1 | Yes | Spatio-temporal diffusion; weaker paper (unclear motivation, weak experiments) |
| `UapxTvxB3N` (Trajectory-LLM) | 5.75 | 2 | Yes | Different type of weaknesses (clarity, dataset realism); accepted |
| `r125wFo0L3` (STR) | 5.00 | 2 | Yes | Different task (prediction/planning); similar score level |

**Favorability comparison**: My draft's two most damaging weaknesses (conditioning asymmetry at -1.38, missing conditioned baseline at -1.31) are comparable in severity to the most critical weaknesses in the 5.00 anchor ("no conditioned baseline" and "missing error bars"), but the current paper lacks the strong controlled comparison that would push it above 5.5. The strengths (favorability 10–13 range) are comparable to DiffMove (6.20), but the more fundamental nature of the conditioning gap pulls the score down.

**Round 1 bracket: 4.0–5.5.** Narrowed from itemized comparison against the most similar anchor (dDdxbdhMsY, avg 5.00) which is a precursor version with fewer metrics and no ablation — the current paper is improved but the conditioning asymmetry remains.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>