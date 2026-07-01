Now let me write the final review.

## Summary

This paper introduces TDDM, a diffusion-based generative model that factorizes trajectory generation into spatial occupancy priors (where people move) and temporal dynamics (how they move). The model first computes aggregate spatial marginals over geographic regions, then conditions a transformer-based diffusion model on these priors to generate trajectories. A canonicalization step via similarity transforms enables a single model to generalize across regions and cities. The method is evaluated on three large-scale urban trajectory datasets (Beijing, Porto, San Francisco) with a comprehensive suite of metrics.

## Strengths

- **Well-motivated factorization of spatial priors from temporal dynamics (lines 15–19, 29–31, 97).** The observation that sample-specific conditioning (DiffTraj, ControlTraj) limits generalization while aggregate spatial priors avoid this is insightful and correctly identified. Separating *where* from *how* people move is a practically motivated design improvement over prior work.

- **Clean technical design matching the motivation (lines 119–123).** The three-step pipeline—partition into regions, canonicalize via similarity transform, condition diffusion on spatial priors—is internally consistent. The canonicalization achieves location-invariance without group-equivariant architectures, making cross-city transfer mechanically plausible.

- **Generalization experiments are the most compelling contribution (Table 3, lines 265–306).** The intra-city (25%→75%) and city-to-city transfer setups directly address a practical problem: generating trajectories for regions without per-trajectory training data. The finding that "Porto-trained models generalize better than 25%-local-trained models on most metrics" (lines 305–306) is a genuinely interesting empirical result that most directly supports the paper's claimed contribution.

- **Comprehensive and standardized evaluation framework (lines 234–241).** The five qualities of synthetic data (fidelity, diversity, proportionality, usefulness, generalization) provide a principled basis for metric selection. Using TSTR, multiple KL variants, and domain-specific measures (Density, Trip, Length, Pattern) is more thorough than most trajectory generation papers.

## Weaknesses

### Major

- **Asymmetric comparison in Table 1 (conditioned vs. unconditioned methods) conflates two effects.** TDDM conditions on spatial priors $H$ computed from the *target data itself* during evaluation (lines 247–248: "spatial priors $H_{r_c}$ for each region partitioned on a grid covering the city in question"). The baselines receive no such spatial conditioning. The ablation study (Table 2) reveals what drives the headline 4× KL improvement: TDDM *without* spatial priors produces $KL_{sym}=1.334$, which is *worse* than Diffusion-TS (1.153). The architecture alone (without the conditioning signal) performs no better than existing baselines. This means the large KL improvements in Table 1 primarily reflect the information content of the conditioning signal, not superior architecture or temporal modeling. The paper frames Section 4.1 as "unconditional trajectory generation" but evaluates a conditioned model. This asymmetry should be clearly acknowledged, and the evaluation should separate (a) a fair comparison where baselines also receive spatial information from (b) the controlled ablation already in Table 2.

### Minor

- **"Zero-shot" framing is imprecise (lines 38, 167, 173, 265).** Algorithm 2 (line 3) requires $\mathbb{X}_{\text{target}}$ as input to compute the spatial prior $H$. The method still requires target-domain data—aggregate occupancy counts rather than full trajectories, which is a meaningful practical advantage—but this is not "zero-shot" in the standard sense of requiring no target-domain data. The paper is transparent about what data is needed (lines 173, 265–266), so the term itself is the problem, not any hidden assumption.

- **Single-run evaluation without variance for most metrics (line 267, Table 1).** Only TSTR reports standard deviations. All KL divergences, JS, Density, Trip, Length, and Pattern are point estimates from a single run per dataset. Without variance estimates, it is impossible to assess whether observed differences are statistically significant. For TSTR specifically, differences (0.011 vs. 0.013 vs. 0.014) are within one standard deviation and likely not significant. The paper acknowledges this ("Models are trained, sampled and evaluated once per dataset") but does not discuss the implications.

- **Normalization inconsistency between algorithms and text.** Algorithm 1 line 6 and Algorithm 2 line 11 normalize to $[0, 1]^D$, while the main text (line 121) and Equation (2) use $[-1, 1]^D$. This appears to be a minor oversight but should be harmonized.

### Trivial

- None beyond the normalization inconsistency noted above.

## Nice-to-Haves

- **Spatial prior computation for unseen regions could be clarified.** For the intra-city transfer experiment (25% training → 75% unseen), it would be helpful to explicitly state that $H$ for the unseen 75% is computed from trajectory data in those regions (rather than from auxiliary sources like population density).
- **The unconditional generation framing (Section 4.1) could be better aligned with the actual evaluation.** The paper defines the task as learning $p(x)$ but evaluates $p(x|H)$. Restructuring this section would eliminate the framing mismatch.
- **Adding multiple seeds with variance estimates** for all metrics would substantially strengthen the paper's evidentiary support.

## Removed Points

- "The main comparison is structurally unfair to baselines" — This is kept as a Major weakness but rephrased to reflect that the comparison is asymmetric and conflates effects, not that it is invalid. The ablation study does provide partial control, and the paper is transparent about its conditioning setup.
- "Several relevant recent baselines are missing" — The paper acknowledges unavailable baselines (line 224), and criticizing missing related work violates review guidelines.
- "The paper does not discuss failure cases or limitations" — This is a common but not mandatory expectation; the future work section (lines 333–335) partially addresses this.
- "Algorithm 2 line 4 has a typographical issue with ∑_{n=1}^{∞}" — This is a PDF parser formatting artifact.
- "The KL improvements are partially circular" — Replaced with the more precise "asymmetric comparison" framing above.
- Several generic strengths from the input review (e.g., "this paper addressed an important problem") removed per filtering guidelines.

## Novel Insights

The key insight that emerges from the combined reviews is that the paper's most significant contribution—cross-city zero-shot transfer via spatial-temporal factorization—is partially obscured by being placed behind a conventional unconditional generation comparison. The city-to-city results (Porto-trained models outperforming 25%-local-trained models on most metrics) are the paper's strongest and most distinctive empirical finding, yet they are presented as a secondary experiment. A restructured evaluation that foregrounds the transfer capability and clearly acknowledges the asymmetric nature of the within-city comparison would substantially strengthen the paper's case.

## Suggestions

1. **Restructure the evaluation** to foreground the generalization experiments (Table 3) as the primary evidence for the method's value, and reframe Section 4.1 as "Prior-conditioned trajectory generation" with an explicit discussion of what the comparison does and does not show.
2. **Add variance estimates** by running 3–5 seeds and reporting means and standard deviations for all metrics.
3. **Replace "zero-shot"** with a more precise term such as "gradient-free transfer" or "prior-conditioned generalization" throughout.
4. **Harmonize the normalization range** between Algorithm 1 ($[0,1]^D$) and the main text ($[-1,1]^D$).

## Score and Decision

**Score: 5.5**  
**Decision: Borderline (Reject)**

**Calibration Anchors:**   
| Anchor | Path | Avg Human Score | Round | Comparison |
|--------|------|----------------|-------|------------|
| Deep Temporal Deaggregation | dDdxbdhMsY.md | 5.00 | 1 | Nearly identical method in earlier form; this paper is more polished with better generalization experiments but shares the same asymmetric-comparison weakness |
| DiffPath | 1o3fKLQPRA.md | 4.50 | 1 | Road-network path generation with LDM; less method novelty, weaker evaluation |
| DiffMove | VRFotuGLfM.md | 6.20 | 1 | Conditional diffusion for trajectory recovery with stronger SOTA evidence and cleaner comparisons |
| Point Set Diffusion | 4anfpHj0wf.md | 7.00 | 2 | More general method with thorough experiments and clear framing; higher bar |
| Large Trajectory Models | r125wFo0L3.md | 5.00 | 1 | Trajectory prediction, not generation; less relevant but similar quality tier |
| Conditional Variational Diffusion Models | YOKnEkIuoi.md | 5.80 | 2 | Similar framing issues around conditioning; accepted despite them |
| Multidimensional Trajectory Optimization | oHbmiaeyUL.md | 5.50 | 2 | Theoretical paper on flow/diffusion trajectories; similar score tier |

**Round 1 bracket:** 4.5–6.5. The paper's core idea (spatial-temporal factorization) is genuinely interesting and the generalization experiments are strong, placing it above methods with weaker evidence (DiffPath at 4.5, Deep Temporal Deaggregation at 5.0). However, the asymmetric comparison in Table 1 and the imprecise "zero-shot" framing prevent it from reaching the level of DiffMove (6.2) or Point Set Diffusion (7.0), where the evidence more directly supports the claims. The final score of 5.5 reflects a paper with a solid methodological contribution and one genuinely compelling result (cross-city transfer), but whose main quantitative comparison is structured in a way that overstates what has been demonstrated.

<score>5.5</score>
<decision>Reject</decision>