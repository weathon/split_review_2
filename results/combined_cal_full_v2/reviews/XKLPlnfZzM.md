Now I have all the information I need. Let me construct the final consolidated review.

---

## Summary

This paper introduces the Temporal Deaggregation Diffusion Model (TDDM), which factorizes trajectory generation into spatial occupancy priors (marginal distributions over geographic occupancy) and temporal dynamics (learned by a diffusion model). Per-region canonicalization via similarity transforms achieves location/rotation invariance without architectural complexity. The method is evaluated on three city-scale GPS datasets (Beijing, Porto, San Francisco) against five baselines, showing strong performance on distributional metrics and interesting cross-city generalization (e.g., Porto-trained models transferring competitively to other cities). The core idea — separating *where* from *how* — is clean and well-motivated.

## Strengths

- **Conceptually clean factorization (Section 3, Eq. 5).** Separating spatial occupancy priors from temporal dynamics is well-motivated and clearly presented. Formulating generation as a mixture model over region partitions is mathematically natural. [weight=11.10]

- **Canonicalization via similarity transforms (Section 3).** Per-region translation, rotation, and scaling to normalize trajectories into $[-1,1]^D$ is a pragmatic design choice that avoids group-equivariant architectural complexity while achieving location/rotation invariance. The ablation shows it contributes to transfer performance. [weight=9.41]

- **Cross-city generalization finding (Section 4.3, Table 3).** The result that models trained on Porto transfer better to other cities than models trained on 25% of the target city is genuinely interesting and non-obvious. This suggests some cities encode more transferable temporal dynamics — a meaningful empirical contribution beyond the method itself. [weight=7.55]

- **Thorough evaluation framework.** The paper identifies five desired properties of synthetic trajectories (fidelity, diversity, proportionality, usefulness, generalization) and evaluates across a corresponding set of metrics using three cities across three continents. [weight=8.29]

## Weaknesses

### Major

1. **The "zero-shot" claim is overstated given the method's requirements (Algorithm 2).** The paper defines "zero-shot" as meaning no gradient updates on target data, but standard usage implies no target-domain data of any kind. Algorithm 2 (line 3) explicitly takes $\mathbb{X}_{\text{target}}$ — trajectory data from the target region — and computes $H = f(r_c, \mathbb{X}_{\text{target}})$ directly from it. The paper's motivation is that trajectory data is "scarce" (Introduction), yet the method requires enough trajectories from the target region to estimate a $64\times 64$ grid of occupancy probabilities. The practical scenario where aggregate occupancy counts are available but individual trajectories are not is left implicit. The contribution is better characterized as *training-free spatial adaptation using aggregate target statistics*, which is still valuable but a different claim. [Relevant section: Algorithm 2, lines 2–3; paper states "the model never receives individual target trajectories, only their aggregate spatial distribution" (line 171-173), but aggregate statistics must still be computed from target trajectories.]

2. **Unfair advantage on distributional metrics against baselines (Tables 1, 3).** TDDM conditions on the spatial prior $H$, which is a discretized version of the *target marginal distribution*. For KL divergence, JS divergence, Density error, and Trip error — the metrics where TDDM shows the largest improvements (~4× lower KL) — this provides a fundamental information advantage. Baselines (Diffusion-TS, DiffTraj, TimeGAN) receive no such conditioning and must infer the full spatial distribution from training data alone. The ablation (Table 2) confirms this: removing the spatial prior causes KL divergences to degrade ~5× while TSTR (per-timestep prediction accuracy) is unchanged. This shows the spatial prior drives distributional improvements, not better temporal dynamics learning. A controlled comparison (giving baselines access to the same spatial prior, or evaluating on metrics that control for spatial information) would be needed to substantiate the headline claims. [Relevant sections: Table 1 vs. Table 2 ablation; Eq. 3-5 showing $H$ encodes the target marginal distribution.]

3. **Missing error bars on most metrics (Tables 1-3).** Standard deviations are reported only for TSTR. For KL divergences, JS, Density, Trip, Length, and Pattern — nine out of ten metrics in Table 1 — no variance is reported. These metrics are computed from finite samples of a stochastic generative process and would vary across runs. This is especially problematic for metrics where the margin over the second-best is small (Density: 0.019 vs. 0.029; Trip: 0.031 vs. 0.041; Length: 0.004 vs. 0.003). Without confidence intervals, readers cannot assess statistical reliability. [Relevant sections: Table 1 columns for KL(S∥R), KL(R∥S), KL_sym, JS, Density, Trip, Length, Pattern.]

### Minor

4. **Training/inference mismatch in region partitioning (Section 3).** Training uses regions with randomized translation and rotation (arbitrary overlap), while inference uses a fixed grid partition with border overlap. The paper mentions this in passing (line 115) but provides no analysis of how the mismatch affects generation quality or how the model handles boundary conditions between adjacent grid cells. [Relevant section: Section 3, paragraph on partitioning: "For training, the partitioning is into regions... with randomized translation and rotation... For sampling... the partitioning can be on a grid."]

5. **No ablation of the canonicalization transform's individual components.** The paper ablates region size and the spatial prior but does not test the separate effects of removing rotation invariance, scaling, or translation within the canonicalization. This leaves it unclear which component drives transfer performance. [Relevant section: Section 4.2 ablation study.]

6. **Model size, training cost, and inference speed are not reported.** Without this information, readers cannot assess whether TDDM's improvements are cost-effective compared to simpler baselines. [Relevant section: Section 3, Algorithm descriptions mention transformer but not its parameter count or compute requirements.]

### Trivial

7. **No dedicated "Related Work" section** in the main body (references are woven into the Introduction and Appendix). While this is a presentation choice rather than a substantive flaw, a dedicated section would improve readability for a venue like ICLR.

## Nice-to-Haves

- Adding a controlled baseline that gives a diffusion model (e.g., Diffusion-TS) access to the same spatial prior $H$ as additional input features would isolate whether the advantage comes from the factorization or simply from having more information.
- Reporting variance across runs for all metrics (not just TSTR) would substantially strengthen the quantitative claims.
- Discussing practical settings where aggregate occupancy data is available without individual trajectories (e.g., census tract counts, cell tower registrations, satellite imagery) would clarify the method's real-world applicability.
- Ablating the individual components of the canonicalization transform would directly test the claimed invariance mechanism.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Map matching pre-processing creates artifacts that advantage TDDM"** — REMOVED. The paper clearly states all models (including baselines) are trained and evaluated on the same preprocessed data (line 243: "All models, including baselines and TDDM, are trained and evaluated using the same preprocessed datasets"). A map-matching ablation (Table 9) shows consistent results. The criticism is not supported by the evidence in the paper.
- **"No related work section"** — REMOVED per instructions (I cannot confirm missing external references; the paper embeds related discussion in the Introduction).
- **"Equation (2) is ambiguous"** — REMOVED. The equation is clear: the summation is over all trajectories in $\mathbb{X}$, with the indicator selecting observations that fall within the canonicalized region.
- **Typography and formatting nitpicks** — REMOVED per instructions (parser artifacts).
- Generic speculation about unsubstantiated alternative interpretations — REMOVED as not grounded in specific paper content.

## Novel Insights

The critical synthesis across reviews reveals that the paper's genuine contribution — *training-free spatial adaptation using aggregate occupancy statistics* — is distinct from what its "zero-shot" framing claims. The most striking and novel empirical result is the Porto-as-universal-source finding, which suggests some cities encode more transferable temporal dynamics than others. The main unresolved tension is between the method's practical strength (you can generate trajectories for a new region if you have its aggregate occupancy map) and the evaluation's reliance on distributional metrics that directly reward the spatial prior information that baselines lack. Resolving this tension — ideally by giving baselines the same prior information — would substantially clarify what the factorization itself contributes versus what comes from the additional conditioning signal.

## Suggestions

1. **Reframe the generalization claims.** Replace "zero-shot" with "training-free spatial adaptation using aggregate target statistics." Discuss concrete settings where aggregate occupancy data is available (census tracts, cell tower registrations, satellite imagery) without requiring individual trajectories.
2. **Add a controlled baseline experiment.** Give the best diffusion baseline (Diffusion-TS or DiffTraj) access to the spatial prior $H$ as additional input features. This isolates whether the advantage comes from the factorization framework or from having more information.
3. **Report variance across multiple seeds for all metrics.** Run each model 3-5 times and report mean ± std for all metrics, not just TSTR.
4. **Ablate canonicalization components individually.** Test the separate contributions of rotation, scaling, and translation within the canonicalization transform.

---

**Calibration summary.** All anchors retrieved across rounds:

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| Deep Temporal Deaggregation | dDdxbdhMsY | 5.00 | R1+R2 | Yes | Earlier/related version of this work. Current paper is significantly improved (more baselines, cross-city experiments, ablations, canonicalization) but shares missing-error-bars concern. |
| Large Trajectory Models | r125wFo0L3 | 5.00 | R1+R2 | No | Motion prediction (different task). Comparable score tier. |
| DiffMove | VRFotuGLfM | 6.20 | R1+R2 | Yes | Trajectory recovery (different task). Well-executed with strong baselines and error bars. |
| DiffPath | 1o3fKLQPRA | 4.50 | R1 | Yes | Path generation with LDM. Weaker evaluation than current paper. |
| Trajectory-LLM | UapxTvxB3N | 5.75 | R2 | Yes | LLM-based trajectory generation. Similar quality but different methodology (dataset contribution vs. method contribution). |
| STDM | 2orBSi7pvi | 3.00 | R1 | No | Spatio-temporal diffusion for time series. Lower quality. |
| xTED | Nh8NLlIfBv | 5.25 | R2 | Yes | Cross-domain trajectory editing. Similar score tier with different domain. |

**Round 1 bracket:** The paper clearly belongs above the 3.0–3.5 range (STDM) and below the 7.0+ range (strong accept). Initial bracket: 4.5–6.5.

**Round 2 narrowing:** Compared to dDdxbdhMsY (5.00, same line of work), the current paper has stronger strengths (peak weight 11.10 vs. 9.17) but one negative-weight weakness (-0.77 for unfair evaluation) that dDdxbdhMsY lacks. Compared to Trajectory-LLM (5.75) and xTED (5.25), the current paper is competitive in strength weights but has a more significant methodological concern (information advantage in comparison). The negative-weight weakness (-0.77) is the decisive item: it places this paper slightly below the 6.0 threshold because it signals a genuine methodological concern rather than a presentation issue. I therefore place it at **5.5**.

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>