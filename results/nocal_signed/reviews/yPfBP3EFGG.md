Now I have calibrated signals from the scoring model. Let me compose the final review.

---

## Summary

This paper proposes STNAdam, an Adam variant for "nonconvex + weakly-convex" composite optimization that maintains two intertwined iteration trajectories (an extrapolation track and a regular update track). The framework accepts arbitrary variance-reduced gradient estimators (SGD, SAGA, SARAH) within a single algorithmic template. The paper establishes almost-sure convergence under the Kurdyka-Łojasiewicz property with explicit rates (Theorems 1–2) and evaluates the method on low-light image enhancement.

## Strengths

- **Ambitious and genuinely novel theoretical scope.** The paper targets "nonconvex + weakly-convex" composite optimization — a more general problem class than the "nonconvex + convex" or "nonconvex + smooth" settings typical in Adam variant analyses. Establishing almost-sure convergence under the KL property with explicit convergence rates for this class is a non-trivial theoretical contribution (Section 3, Theorems 1–2).

- **Flexible gradient-estimator-agnostic framework.** The algorithm is designed to accept arbitrary variance-reduced gradient estimators (SGD, SAGA, SARAH, SVRG, SPIDER) within a single template (Algorithm 1, Lemma 1). This is a clean design choice that future work could build on directly.

## Weaknesses

### Fatal

- **Inadequate empirical evaluation for the practical claims made.** The paper lists "favorable practical performance" as one of its three core contributions (contribution iii), yet the empirical evaluation is far too thin to support this claim. Specifically: evaluation on only one dataset (LOL), no standard deviations or confidence intervals (every reported number is a single deterministic value), no convergence plots (loss vs iteration or loss vs time), and no sensitivity analysis studying how performance varies with the hyper-parameter scheduling intervals. For an optimizer paper at a conference that values empirical validation, this level of evidence is fundamentally insufficient to substantiate the practical claims.

### Major

- **No controlled ablation to isolate the two-track mechanism.** The paper compares STNAdam-SGD, STNAdam-SAGA, and STNAdam-SARAH against baselines (SGD, Adam, SNAdam) that all use plain SGD-style gradients. There is no single-track + SARAH or single-track + SAGA baseline. Consequently, the large PSNR gap between STNAdam-SARAH (22.26) and STNAdam-SGD (18.06) — a 4.2 dB improvement — is primarily attributable to the variance-reduced SARAH estimator, not the two-track framework. The cleanest comparison for isolating the two-track contribution is STNAdam-SGD vs SNAdam (18.06 vs 17.14, a **0.9 dB** gain), which is modest. Without proper ablations, the paper cannot substantiate its central claim that the two-track framework drives improvement.

- **Implausible runtime values.** The reported "Time(s)" in Tables 2 and 3 are all between 2.34×10⁻⁵ and 7.63×10⁻⁵ seconds (23–76 microseconds). Even a single forward pass on a modest image would take substantially longer on any real hardware. The paper does not clarify whether these are per-iteration or total times, nor does it specify the hardware, image resolution, or number of iterations. This undermines the paper's speed claims and casts doubt on the timing methodology.

### Minor

- **Citation inconsistency for SNAdam.** The Related Work (p. 2, line 33) attributes SNAdam to Reddi et al. (2019), stating they "incorporated Nesterov-acceleration technique into Adam, named SNAdam" — but Reddi et al. (2019) proposed AMSGrad, not SNAdam. The experiments and contributions (lines 50, 281) correctly cite SNAdam as Xie et al. (2024).

- **Nomenclature confusion.** The experiments label standard Adam (Kingma & Ba, 2014) as "SAdam" (line 281), while the Related Work (line 13) discusses SAdam as a distinct algorithm by Wang et al. (2019) and Le-Duc et al. (2024).

- **Theory-practice gap in parameter scheduling.** The scheduling intervals (Eqs. 6–8) depend on problem constants (L, τ, V₁, V_T, ρ, M, s) that are generally unknown in practice. Remark 3 partially acknowledges this but does not bridge the gap.

- **No discussion of per-iteration cost.** The two-track framework performs two proximal gradient steps per iteration vs. one in standard methods, but the paper does not discuss this overhead or its practical implications.

### Trivial

None.

## Nice-to-Haves

- Add controlled ablations: single-track + SARAH and single-track + SAGA baselines to isolate the two-track mechanism's contribution.
- Clarify the timing methodology (what "Time(s)" measures, hardware, image resolution, iteration count) and verify physical plausibility.
- Report standard deviations or confidence intervals across multiple trials.
- Add convergence plots (loss vs iteration, loss vs wall-clock time).
- Evaluate on at least one additional dataset beyond LOL.
- Fix the SNAdam attribution in the Related Work and use consistent "SAdam"/"Adam" nomenclature.
- Discuss the per-iteration computational overhead of the two-track framework.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Motivation–experiment disconnect:** The critic argued the paper motivates STNAdam for deep learning but evaluates on a hand-crafted LIE model. Removed because the paper's primary contribution is for composite optimization of the form (1), and the LIE model (14) is a valid instance. The deep learning references in the introduction are general motivation, not the core claim.
- **No comparison against NAdam/Adam⁺:** Removed as scope creep; the paper already compares against 11 baselines.
- **No deep learning benchmark:** Removed as scope creep; the paper's target problem class is composite optimization.
- **Missing related works, formatting nitpicks, grammar issues:** Removed per hard rules (parser artifacts, not verifiable).
- **Generic/speculative criticisms lacking concrete paper anchors:** Removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

The most important single change would be to add STNAdam-SARAH vs single-track-SARAH and STNAdam-SAGA vs single-track-SAGA comparisons. This would directly validate whether the two-track mechanism — rather than the choice of gradient estimator — is responsible for the reported gains. Combined with convergence curves, error bars, and a second dataset, this would address the paper's most critical empirical gaps.

## Score and Decision

**Score: 4**  
**Decision: Reject**

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>