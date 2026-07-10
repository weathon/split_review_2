Now I have all the information I need. Let me compile the final review.

## Summary

The paper introduces TDDM, a diffusion model that factorizes trajectory generation into spatial occupancy priors (marginal distributions over where people go) and temporal dynamics (how they move), using coordinate canonicalization (similarity transforms) to share parameters across geographic regions. Evaluated on three cities (Beijing, Porto, San Francisco) against GAN, VAE, and diffusion baselines, TDDM shows strong qualitative results and the ablation convincingly demonstrates the spatial prior's role.

## Strengths

- **Principled factorization of spatial and temporal dynamics.** The central idea — separating *where* people move (spatial occupancy marginal) from *how* they move temporally — is intuitive and well-motivated. The canonicalization via similarity transform (Section 3, lines 119–123) is a clean mechanism for achieving location-invariance without requiring group-equivariant architectural modifications, enabling parameter sharing across geographic regions.

- **Visually convincing results.** Figure 2 (Porto dataset) shows a striking qualitative gap. TDDM generates trajectories that clearly follow road structure, with coherent density patterns, while baselines produce diffuse, road-oblivious blobs.

- **Informative ablation study.** Table 2 systematically isolates the contribution of the spatial prior and the effect of region size. The "w/o spatial prior" condition degrades KL_sym from 0.277 to 1.334 (nearly 5×), confirming the spatial prior is doing substantive work. The 1×1 km vs. 3×3 km comparison reveals a real tradeoff between local coherence (Pattern score) and global realism (Length error).

- **Cross-city transfer analysis.** The finding that training on Porto generalizes better on average than training on 25% of the target city (Section 4.3, lines 305–306) is non-obvious and empirically grounded. The honest discussion of the tradeoff between path-length accuracy and distributional coverage is useful.

## Weaknesses

### Major

- **The headline KL/JS metrics conflate conditioning with generative quality.** The KL and JS divergences (Table 1) are computed on spatial marginal distributions, which is exactly the quantity TDDM conditions on (the spatial prior *H*, line 149: $\epsilon_\theta(x_t, t, H)$). None of the baselines (TimeGAN, Diffusion-TS, DiffTraj) receive this conditioning. The claim of "up to 4 times lower KL divergences" (line 327) therefore partly reflects a structural advantage — the metric measures how well TDDM reproduces information it was explicitly given. The metrics that provide a more level playing field — TSTR (0.011 vs. 0.013, overlapping standard deviations ±0.006 vs. ±0.005), Pattern (0.917 vs. 0.907) — show only modest advantages. The paper should explicitly separate metrics that test spatial marginal matching from those that test temporal dynamics and discuss the different conclusions each supports.

### Minor

- **"Zero-shot" framing is imprecise.** In Algorithm 2 (line 3), the spatial prior *H* is computed from $\mathbb{X}_{\text{target}}$ — the target city's trajectories. The paper defines "zero-shot" as "no gradient updates or fine-tuning on target data" (line 173), but the standard ML connotation of "zero-shot" implies no target-domain data at all. The method requires aggregate marginal statistics from the target, just not individual trajectories. A clearer framing would strengthen reproducibility of claims without diminishing the genuine contribution.

- **Missing uncertainty quantification on headline results.** KL, JS, Density, Trip, Length, and Pattern metrics in Tables 1–3 are reported as point estimates without error bars or variance information. Only TSTR includes ± values. It is unclear whether TDDM's advantages on these metrics are statistically robust or reflect a single favorable run.

- **Quality (V) "Generalization" (avoiding memorization) is listed but not measured.** The paper defines five evaluation qualities (line 234), including "Generalization: synthetic samples should not be mere copies of the training data." However, no memorization metric (nearest-neighbor distance, membership inference, etc.) is reported. While the paper scopes out privacy (line 17), listing this quality without measurement creates a gap between the evaluation framework and its implementation.

## Nice-to-Haves

- Include a conditioned-baseline comparison (giving baselines access to the same spatial prior *H* as conditioning) to disentangle the benefit of the prior from architectural differences.
- Compute KL or related metrics on step-velocity distributions or path curvatures to directly test temporal dynamics independently of the spatial marginal.
- Report computational cost (training/sampling time, parameter count) to help practitioners choose between methods.
- For a truly demanding zero-shot test, derive *H* from non-trajectory sources (e.g., road network density, population estimates).

## Removed Points

- **Rejection sampling procedure not described**: The "w/o spatial prior + rejection" ablation in Table 2 mentions a rejection procedure but the procedure is not described in the visible main text. Since the appendix is stripped by the parser, this concern cannot be verified and is removed per guidelines.
- **"Equations (1) and (5) are never used in evaluation"**: These are theoretical framing equations for formal grounding. Not a weakness.
- **"Model never learns full trajectories, only region fragments"**: The model generates trajectories region by region (Algorithm 2). This is an explicit design choice, not a flaw.
- **Speculative confounds without paper evidence**: Removed per filtering guidelines.
- **Formatting/stylistic/missing-appendix criticisms**: Removed per guidelines.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Reframe the narrative around the KL metrics to acknowledge the conditioning advantage and let the fairer metrics (TSTR, Pattern, Length), the ablation study, and visual quality carry the main evidence.
- Provide error bars on all metrics, or at minimum on KL/JS where the strongest claims are made.
- Clarify the "zero-shot" terminology — e.g., "aggregate-statistics generalization" more precisely describes what is demonstrated.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>