## Summary

This paper proposes TDDM, a diffusion-based trajectory generation model that factorizes generation into spatial occupancy priors (where people go) and temporal dynamics (how they move). By conditioning on region-level marginal distributions rather than individual trajectories, and canonicalizing coordinates via similarity transforms to enable parameter sharing, TDDM aims to generate realistic large-scale trajectory datasets that generalize across cities. The paper introduces a 3-city benchmark (Beijing, Porto, San Francisco) with standardized metrics and reports improvements over several baselines.

## Strengths

- **Clean factorization of spatial and temporal components.** The core insight — separating *where* people go (spatial occupancy marginal) from *how* they move (temporal dynamics) — is well-motivated and clearly stated (Section 3). This differs from both unconditioned generation and sample-specific conditioning.

- **Canonicalization via similarity transforms is a practical design choice.** Rather than building group-equivariant architectures, the paper normalizes coordinates into a canonical frame (Section 3, "Canonicalization"), keeping the architecture lightweight while achieving location/rotation/scale invariance. This is what enables parameter sharing across regions.

- **3-city benchmark with standardized evaluation is a useful resource.** Evaluation across Beijing (Geolife), Porto, and San Francisco (Cabspotting) with consistent preprocessing and a harmonized set of five qualities (fidelity, diversity, proportionality, usefulness, generalization — Section 4) is a meaningful contribution that the community can build on.

- **Strong spatial distributional alignment.** Table 1 shows large improvements on KL-based metrics (KL_sym 0.277 vs. best baseline 1.153), Density (0.019 vs. 0.029), Trip (0.031 vs. 0.041), and JS divergence (0.059 vs. 0.198).

- **Ablation study cleanly demonstrates the prior's role.** Table 2 shows that removing the spatial prior degrades KL-based scores by ~5× (from 0.277 to 1.334), confirming that the prior is responsible for the spatial coverage gains.

- **Generalization experiments are well-analyzed.** The finding that Porto-trained models generalize comparably to 25%-of-target-trained models is genuinely interesting, and the discussion of the tradeoff between length accuracy and distributional coverage (Section 4.3) is honest and informative.

## Weaknesses

### Fatal
None.

### Major

1. **The headline KL improvements conflate conditioning advantage with method quality.** TDDM receives the spatial marginal distribution H as conditioning input — the same quantity that the KL divergence metrics in Table 1 measure (spatial occupancy distribution). The baselines receive no such conditioning. The paper's strongest quantitative claims ("4× lower KL," "state of the art on Density, Trip, and Pattern") are dominated by these spatial metrics. On metrics less directly tied to the conditioning signal, the picture is more modest: TSTR (0.011±0.006 vs. 0.013±0.005 for DiffTraj — overlapping std), Pattern (0.917 vs. 0.907), and Length error (0.004 vs. 0.003 for Diffusion-TS, where TDDM is slightly *worse*). The paper should explicitly acknowledge that the KL metrics measure spatial marginal alignment — exactly what the conditioning provides — and weight the temporal/non-spatial metrics more heavily in its conclusions. The abstract and conclusion currently foreground the KL numbers without this caveat, which overstates the overall advantage.

2. **"Zero-shot" generalization claim is overstated.** Algorithm 2 (line 3) computes H from the target city's real trajectory data X_target. The method needs trajectory data from the target to generate. This is not "zero-shot" in the standard sense (no target data at all) — it is "no training/fine-tuning on target data." The model requires aggregate statistics rather than individual trajectories, which is a meaningful but substantially weaker form of generalization. Critically, if no trajectories exist for a target region (the scenario the Introduction motivates — "new environments lack sufficient observations"), the paper offers no concrete method to compute H. Line 145 states H "can be estimated (even in unseen cities)" but provides no procedure for doing so without trajectory data. This gap between the motivating scenario and the actual experimental setup is significant.

3. **No statistical significance for most results.** Tables 1–3 report KL, Density, Trip, Length, and Pattern scores as single numbers with no variance. The caption states "Models are trained, sampled and evaluated once per dataset." Only TSTR has standard deviations (and these already show overlap between TDDM and DiffTraj). Without multiple seeds or confidence intervals, it is impossible to assess whether the smaller advantages (on TSTR, Pattern, Length) are real or within noise.

4. **Learning of region weights p(r_c) is unclear.** The paper states that "both relative probability between regions, p(r_c), and spatial priors H_{r_c} for each region... are learned during training" (line 247). However, Algorithm 1 takes p(r_c) as input and never updates it during the training loop. Eq. 2 defines p(r_c) directly from empirical point counts in the data. This is estimation from data statistics, not learning via optimization. The mechanism by which p(r_c) is "learned" is never specified in the training algorithm.

### Minor

1. **Coordinate normalization inconsistency.** Section 3 (line 121) states canonicalization maps to [-1, 1]^D, but Algorithm 1 (line 6) and Algorithm 2 (line 11) use [0, 1]^D. This matters for reproducibility.

2. **"Unconditional generation" framing is imprecise.** Section 4.1 describes the task as "unconditional trajectory generation" while TDDM explicitly conditions on spatial priors H. "Region-conditional generation" or "prior-conditioned generation" would be more accurate.

3. **Proportionality metrics partially conflated with sampling design.** In Algorithm 2 (line 4), the number of samples per region N_{r_c} is set proportional to the real data's per-region point counts. This directly determines the between-region distribution that the proportionality metrics measure, partially decoupling this aspect of evaluation from TDDM's generative quality (though within-region generation is still learned).

4. **Per-city variation deferred to appendix.** Main tables 1–3 aggregate across cities. The paper notes (line 301) that per-city analysis reveals "more substantial variations" but only provides this in the appendix. Individual city results in the main text would strengthen the evaluation, especially given the datasets' heterogeneity.

### Trivial
None that warrant listing separately beyond the minor items above.

## Nice-to-Haves

- **Controlled comparison where baselines also receive the spatial prior H.** Giving Diffusion-TS or DiffTraj the same spatial prior as conditioning input would isolate whether TDDM's advantage comes from the architecture/factorization or almost entirely from the prior signal itself.
- **Additional temporal metrics independent of spatial conditioning.** Metrics such as autocorrelation of step directions, distribution of trip durations, or turning angle distributions would directly test the "temporal dynamics" half of the factorization.
- **Clarify how H can be estimated for truly unseen cities** without any trajectory data (e.g., from OpenStreetMap, census data, or land use information), if such a procedure exists.

## Removed Points

- *Criticism about DiffTraj/ControlTraj "sample-specific conditioning" needing clarification* — the paper cites these works and briefly characterizes them; this is a minor descriptive point, not a weakness of the paper.
- *Criticism about missing temporal metrics* — the paper does include temporal measures (TSTR, Length error, Pattern score, KL_speed). The claim that "there is no dedicated temporal metric" is inaccurate; the paper's temporal coverage could be expanded but is not absent.
- *Criticism about trajectory target length not being discussed* — Algorithm 1 lists "Target length" as input; detailed handling is reasonably deferred to the appendix.
- *"Aggregating across cities obscures variation" as a standalone point* — this is standard practice; the paper acknowledges per-city variation exists and provides it in the appendix.
- *Criticism about the paper not acknowledging H provides an information advantage* — this is folded into Major weakness 1 above, where it is properly contextualized and verified against the paper.

## Novel Insights

The most interesting observation from the reviews is the identification of a partial circularity in the generalization evaluation: Algorithm 2 sets per-region sample counts proportional to real data counts, which means the between-region distribution that proportionality metrics measure is directly controlled. This does not invalidate the within-region generation results but does mean the proportionality metrics in the generalization setting partly reflect the experimental design rather than generative quality. Additionally, the observation that the KL metrics implicitly measure what TDDM conditions on — while not invalidating the contribution — clarifies that the paper's quantitative claims are strongest for spatial marginal matching and more modest for trajectory-level temporal fidelity. These distinctions are useful for properly scoping the contribution.

## Suggestions

1. Acknowledge explicitly that the KL divergence metrics measure spatial marginal alignment — the same quantity TDDM conditions on — and calibrate the abstract/conclusion claims accordingly.
2. Rename "zero-shot" to "training-free generalization" or "no-fine-tuning generalization" to accurately reflect that target-region trajectory data is needed to compute the spatial prior.
3. Report all metrics with variance across 3+ random seeds or bootstrapped confidence intervals.
4. Clarify whether p(r_c) is learned via gradient updates or estimated from empirical counts, and fix the [0,1]/[-1,1] normalization inconsistency.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>