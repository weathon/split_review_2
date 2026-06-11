## Summary
This paper introduces the Temporal Deaggregation Diffusion Model (TDDM), a generative framework for large-scale human mobility trajectory data. The core idea is to factorize trajectory generation into two components: spatial occupancy priors (marginal distributions over geographical area, marginalized over time) and temporal dynamics (how individual trajectories realize those occupancy patterns). The model partitions the spatial domain into regions, canonicalizes each region via a similarity transform, computes a discrete spatial prior for each region, and conditions a transformer-based diffusion model on these priors to generate realistic trajectories. This design enables zero-shot generalization to new cities by estimating spatial priors from target regions without retraining.

The paper makes several contributions: (1) a spatial-temporal factorization approach that separates "where" people move from "how" they move; (2) a standardized evaluation benchmark across three cities on different continents (Beijing, Porto, San Francisco) with trajectory-specific metrics; (3) empirical results showing TDDM outperforms five baselines (TimeGAN, TimeVAE, COSCI-GAN, Diffusion-TS, DiffTraj) across KL-divergence-based distributional measures, density/trip/pattern scores, and TSTR fidelity; and (4) demonstration of zero-shot intra-city and city-to-city generalization.

**Novelty assessment (deferred — external literature verification unavailable in this run):** The conceptual contribution of decoupling spatial occupancy from temporal dynamics for trajectory generation appears well-motivated. However, because external paper search was not available in this review run, novelty claims (including comparisons to DiffTraj, ControlTraj, TrajGen, and COLA) cannot be independently verified against the latest literature. A manual literature survey is needed to confirm whether the specific formulation of spatial priors as discrete occupancy grids for conditional diffusion is genuinely novel or overlaps with existing conditional trajectory generation frameworks.

## Strengths
1. **Well-motivated factorization idea.** The core insight—separating spatial occupancy (where people go) from temporal dynamics (how they move through that space)—is conceptually clean and directly addresses the cross-region generalization challenge. This is a genuinely useful framing that goes beyond generic time-series generation.

2. **Strong empirical results on standardized benchmarks.** Across three diverse real-world GPS datasets (Geolife, Porto, Cabspotting), TDDM achieves substantially lower KL divergences (KL_sym 0.277 vs. 1.153 for the best baseline) and JS divergence (0.059 vs. 0.198), indicating both improved coverage and fidelity. These improvements are consistent and large in magnitude, suggesting the approach is robustly beneficial.

3. **Thoughtful evaluation framework.** The paper proposes to harmonize five synthetic data quality dimensions (fidelity, diversity, proportionality, usefulness, generalization) and employs multiple complementary metrics (TSTR, KL divergences, JS divergence, density/trip/length errors, pattern score) that together provide a more complete picture than any single metric. This multi-metric approach raises the bar for trajectory generation evaluation.

4. **Zero-shot generalization demonstration.** The intra-city and city-to-city transfer experiments are well-designed and convincingly show that spatial priors enable generalization without retraining. The comparison between training on 25% of a city vs. training on Porto and transferring is particularly informative, revealing interesting tradeoffs about data efficiency.

5. **Architecture design appropriate for the task.** Using a transformer encoder with three token types (trajectory, marginal distribution, denoising step) is a practical and well-justified design. The decision to avoid group-equivariant architectures in favor of input-output canonicalization keeps the model lightweight and clean.

6. **Reproducibility awareness.** The paper provides explicit training and sampling algorithms (Algorithms 1 and 2), specifies the preprocessing pipeline (map matching, resampling to 1Hz), and commits to public datasets and standardized preprocessing. These details support reproducibility.

## Weaknesses
### W1 (Major) — Critical normalization inconsistency between theoretical formulation and algorithms
The canonicalization section (Page 3) states that the similarity transform maps trajectories into $[-1, 1]^D$ with scaling factor $s = 2/\text{width}(r_c)$, and Equation (2) checks $T_{r_c} x[n] \in [-1, 1]^D$. However, Algorithm 1 line 6 normalizes to $[0, 1]^D$, and Algorithm 2 line 11 transforms back from $[0, 1]^D$. This is a numerical contradiction: $[-1,1]$ and $[0,1]$ require different scaling factors and offset corrections. If the implementation follows $[0,1]$, then Equations (2) and the similarity transform definition are incorrect. If the implementation follows $[-1,1]$, then the algorithms are wrong. This directly threatens reproducibility and must be resolved before publication. **Fix:** Adopt one consistent range throughout; update all equations, algorithms, and text to match.

### W2 (Major) — Missing variance and statistical significance for most evaluation metrics
Tables 1, 2, and 3 report only point estimates (without standard deviations or confidence intervals) for all KL-based metrics, Density, Trip, Length, and Pattern scores. Only TSTR includes $\pm$ values. For metrics where TDDM and baselines have close scores (e.g., Length error: TDDM 0.004 vs. Diffusion-TS 0.003), the absence of variance makes it impossible to determine whether the difference is meaningful. **Fix:** Report mean $\pm$ std over at least 3 independent training runs for all metrics. Add statistical significance tests (paired bootstrap or Wilcoxon signed-rank) between TDDM and the strongest baseline for each metric.

### W3 (Major) — Potential information leakage in spatial prior estimation during training
In Algorithm 1, the spatial prior $H$ is computed from $\mathbb{X}_{train}$ trajectories within region $r_c$ (line 3), and individual training trajectories $x$ are drawn from the same set $\mathcal{X}_r$ (lines 4-7). This means $H$ is estimated from the same trajectories the model is trained to generate. The paper claims to avoid "sample-specific conditioning," but this setup could allow the model to learn associations between specific trajectory shapes and their corresponding occupancy patterns in $H$—effectively a form of memorization. No discussion of how or whether this leakage is controlled. **Fix:** Either (a) clarify that $H$ is computed from all trajectories in the region (not just the chosen sample) and that $H$'s aggregated nature prevents memorization, or (b) change the algorithm to compute $H$ from a held-out subset of trajectories within each region.

### W4 (Major) — Missing ablation for canonicalization component
The ablation study (Table 2) tests removal of spatial priors and region size changes, but does not ablate the similarity transform (canonicalization). The canonicalization is presented as a key innovation ("unlike group-equivariant architectures... our approach achieves invariance via input-output transformation"), yet its contribution to overall performance is never isolated. Without this control, readers cannot tell whether TDDM's gains come from the spatial prior conditioning, the canonicalization, or both. **Fix:** Add a "TDDM w/o canonicalization" condition—train without the similarity transform so the model must learn location-specific dynamics. If this is computationally prohibitive, at minimum discuss the expected effect and provide evidence from a small-scale experiment.

### W5 (Moderate) — Overclaim of "state of the art" without verification
The conclusion states TDDM "sets new state of the art on Density, Trip, and Pattern measures." However, the paper only compares against five baselines and acknowledges additional methods (TrajGen, ControlTraj, COLA) without reproducible code. Without controlled benchmarking against all relevant methods, the SOTA claim is unsubstantiated. **Fix:** Replace "state of the art" with a bounded claim such as "consistently outperforms all tested baselines" or "achieves the best scores among evaluated methods."

### W6 (Moderate) — Generic problem definition
Section 2 defines the task as standard unconditional generative modeling without any trajectory-specific structure. This misses an opportunity to frame the problem in a way that highlights why spatial-temporal factorization is a natural solution—e.g., spatial continuity, road network constraints, multi-modal route choices, variable trajectory lengths. **Fix:** Replace with a trajectory-specific formulation that motivates the proposed decomposition.

### W7 (Moderate) — Baseline comparison fairness requires more detail
The evaluation states that baselines come from "major generative paradigms" but does not specify whether each was re-trained with hyperparameter tuning, whether the same preprocessing pipeline was used, or whether architectural differences (e.g., DiffTraj as UNet vs. TDDM as transformer) are controlled. **Fix:** Add a paragraph detailing training procedures, hyperparameter search, and a fairness analysis for each baseline.

### W8 (Minor) — Porto "universal source" claim over-extrapolated
The paper suggests Porto acts as a "universal source" dataset based on observations from three cities. This is an intriguing finding but requires broader validation across more diverse urban environments. **Fix:** Bounded wording—"Porto served as an effective source in our experiments"—and add a caveat about limited city diversity.

### W9 (Minor) — Abstract lacks explicit research gap
The abstract states "current generative models either do not offer any controllability or rely on strong sample-specific conditioning" but does not clearly articulate why this gap is harmful or how the proposed factorization specifically addresses it. **Fix:** Add a sentence linking the gap to the solution, e.g., "This prevents cross-region transfer because sample-specific conditioning ties each generated trajectory to a training instance."

### W10 (Minor) — Introduction narrative could be tightened
The introduction's first two paragraphs list applications and challenges but do not build a clear logical arc from broad motivation to specific gap to proposed solution. **Fix:** Restructure to follow: Big Picture → Concrete Gap → Key Insight → Solution Preview → Contribution List. Specific copy-edit suggestions are provided in the PDF annotations.

## Score
**Final Score: 6/10**

### Rationale

The paper presents a well-motivated and empirically promising approach to trajectory generation through spatial-temporal factorization. The core idea—separating spatial occupancy priors from temporal dynamics—is conceptually clean and directly targets the cross-region generalization problem. The empirical results show substantial improvements over five baselines across multiple metrics on three real-world datasets, and the zero-shot generalization experiments are informative.

However, the paper has several issues that reduce confidence and must be resolved before acceptance. The most critical is a normalization inconsistency (W1) between the theoretical formulation ($[-1,1]^D$) and the algorithms ($[0,1]^D$), which directly threatens reproducibility. Additionally, the evaluation lacks variance reporting for most metrics (W2), the training algorithm may contain an information leakage channel (W3), and a key component (canonicalization) is not ablated (W4). The paper also overclaims SOTA status (W5) without external verification, and several minor narrative and framing issues reduce readability. Novelty cannot be independently verified due to external retrieval being unavailable in this run, which introduces additional uncertainty.

These weaknesses are fixable with reasonable effort. The normalization inconsistency, variance reporting, and bounded claims are straightforward corrections. The information leakage and missing ablation require more thoughtful experimental design but are feasible. With these addressed, the paper would likely be a solid contribution to the trajectory generation literature.

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Problem: Cross-region trajectory generation without sample-specific conditioning]
    |
    v
[Key Insight: Factorize into spatial priors (where) + temporal dynamics (how)]
    |
    v
[TDDM Framework]
    ├── Partition spatial domain → regions
    ├── Canonicalization via similarity transform
    ├── Spatial prior H (discrete 64×64 occupancy grid)
    └── Diffusion model conditioned on H (transformer encoder)
    |
    v
[Evidence from Experiments]
    ├── Table 1: KL_sym 0.277 (TDDM) vs 1.153 (Diffusion-TS) — Strong ✓
    ├── Table 2: Ablation: w/o spatial prior → KL_sym 1.334 (5× worse) — ✓
    ├── Table 3: Zero-shot intra-city TSTR 0.010 — ✓
    └── Missing: Canonicalization ablation, variance bars, significance tests — ✗
    |
    v
[Claims Made vs Verified]
    ├── "Sets new state of the art" → Overclaim (not verified against full literature) ✗
    ├── "Spatial-temporal factorization enables generalization" → Well supported ✓
    └── "Spatial priors critical for coverage" → Well supported by ablation ✓
```

### ASCII Diagram — Revision Strategy Roadmap

```text
Priority | Issue | Fix | Expected Impact
---------|-------|-----|----------------
P0 (Must) | W1: Normalization inconsistency [-1,1] vs [0,1] | Standardize all equations/algorithms to one range | Reproducibility restored
P0 (Must) | W2: Missing variance | Add std over 3+ seeds + significance tests | Statistical credibility
P0 (Must) | W3: Information leakage in training | Clarify or redesign H computation | Trust in "no sample-specific conditioning" claim
P1 (Should) | W4: Missing ablation for canonicalization | Add w/o canonicalization control | Understanding of what drives gains
P1 (Should) | W5: SOTA overclaim | Replace with bounded wording | Scientific accuracy
P2 (Nice) | W6-W10: Narrative, abstract, problem definition | Targeted rewrites | Readability
```

### Contribution Claims Summary

| Claim ID | Claim | Evidence Strength | Status |
|----------|-------|-------------------|--------|
| C1 | Spatial-temporal factorization for trajectory generation | Strong empirical support; conceptual clarity | **Partially supported** (missing canonicalization ablation) |
| C2 | Improved fidelity and coverage over baselines | Strong across 3 datasets, 10 metrics | **Supported** (but missing variance) |
| C3 | Zero-shot generalization to new regions | Good evidence from intra-city and city-to-city | **Supported** (but length error degradation noted) |
| Novelty | (Deferred — external retrieval unavailable) | N/A | **Deferred manual verification** |