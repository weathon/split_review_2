Now I will produce the final consolidated review.

## Summary

This paper tackles noisy correspondence (NC) in multi-view clustering. It identifies two types of NC — category-level mismatch and sample-level mismatch — and proposes CorreGen, a generative framework that formulates cross-view correspondence learning as maximum likelihood estimation solved via EM. In the E-step, a GMM-guided optimal transport formulation estimates soft correspondences; in the M-step, the encoder is updated to maximize expected log-likelihood. The paper proves that InfoNCE is a special case under degenerate assumptions and reports strong empirical results on four datasets.

## Strengths

- **Principled two-type formalization of NC (Def. 1–2).** The paper clearly distinguishes category-level mismatch (same-class pairs treated as negatives) from sample-level mismatch (misaligned or missing pairs). This conceptual decomposition is useful beyond the specific method and provides a clearer language for describing NC in MVC.

- **Generative reframing is a meaningful departure from the discriminative paradigm.** Shifting from contrastive objectives to a maximum-likelihood formulation over latent correspondences (Eqs. 2–8) is well-motivated and non-obvious. The result that InfoNCE emerges as a special case (Proposition 2) strengthens the theoretical connection and positions the method as a principled generalization.

- **Consistent improvements on UMPC-Food101 (Table 1).** UMPC-Food101 is a challenging real-world dataset with genuinely noisy web-crawled image–recipe pairs. At 0% MR, CorreGen achieves 49.77 ACC vs. 36.20 for DIVIDE and 33.10 for CANDY — substantial gaps that suggest the method is doing something useful on real noisy data.

- **Posterior visualization (Fig. 3).** The qualitative evidence that estimated posterior distributions evolve toward block-diagonal (class-level) structure over training provides a sanity check that the E-step is learning meaningful correspondences.

## Weaknesses

### Fatal
None.

### Major

- **GMM-guided marginal formula (Eqs. 13–14) does not guarantee valid OT marginals, and the paper provides no mechanism ensuring cross-view mass matching.** The OT problem (Eq. 11) requires $\mathbf{P}\mathbf{1}_N = \mathbf{p}^{(v_1)}$ and $\mathbf{P}^\top\mathbf{1}_N = \mathbf{p}^{(v_2)}$, which is feasible only if $\sum_i p_i^{(v_1)} = \sum_j p_j^{(v_2)}$. The GMM is fitted independently per view on embeddings from different modalities. The formula $p(\mathbf{x}_i^{(v)}; \theta^{(t)}) = \frac{m^{d_i}-1}{m-1} \cdot \frac{N_c}{N}$ is not derived from any probabilistic model, and there is no discussion of normalizing the result to sum to a consistent constant across views. Since the marginals are used as constraints for the Sinkhorn algorithm, a mismatch in total mass makes the problem infeasible. Even if the implementation handles this via ad-hoc normalization, the paper neither states this nor justifies it. This is a gap in the method as presented.

- **The evaluation design conflates "general clustering improvement" with "noise robustness."** CorreGen is built on top of DIVIDE. At 0% MR (no artificial sample-level noise), CorreGen already substantially outperforms DIVIDE on *every* dataset — including Scene15 (50.25 vs. 44.57 ACC) and Caltech101 (68.52 vs. 62.20 ACC), which are clean benchmarks. On UMPC-Food101 the gap is even larger (49.77 vs. 36.20). Since the method improves clustering even without artificial noise, the reported gains under noisy settings cannot be cleanly attributed to the NC-handling mechanism. The improvement could come from the GMM-guided OT, the generative objective itself, or simply from additional modeling capacity. The paper needs an ablation that isolates the NC-robustness effect — e.g., comparing the *performance drop* from clean to noisy data for CorreGen vs. DIVIDE, rather than only reporting raw absolute numbers.

- **The $\rho$ parameter for the virtual sample is not specified.** The virtual sample mechanism (Sec. 3.2.1) introduces $\rho$ as "the potential noise ratio, which corresponds to the marginal probability mass of the virtual sample." The paper does not state how $\rho$ is set — whether it is a fixed hyperparameter, estimated from data, or tuned per dataset. Since the noise level in real-world data is unknown and the method's sensitivity to $\rho$ is not discussed (the paper cites an appendix that is not available in the reviewed version), the practical applicability of the method is unclear on this point alone.

### Minor

- **The claim of "consistently achieves the best performance" (Sec. 4.2) has unacknowledged counterexamples.** At 80% MR on Scene15 (Table 1), CANDY achieves 42.27 ACC vs. CorreGen's 40.96. At MR 0.2 / CR 0.5 on Caltech101 (Table 2), CANDY achieves 62.57 ACC vs. CorreGen's 61.19. The paper does not discuss these cases. The claim should be qualified to acknowledge settings where CorreGen is not the top performer on every metric.

- **No variance information reported despite five runs.** The paper reports results as "the mean of five individual runs with different random seeds" (Table 1 caption) but provides no standard deviations, confidence intervals, or significance tests. Given that some improvements are modest (e.g., Caltech101 0% MR: 68.52 vs. 67.64 — less than 1 ACC point), the lack of variance information makes it impossible to assess which differences are meaningful.

- **The transition from Eq. (2) to Eq. (3) glosses over a modeling choice.** Eq. (2) marginalizes over each view independently. The paper states this is "reformulated" as Eq. (3), which sums over view pairs of log Σ_j p(x_i^(v1), x_j^(v2)). While the connection follows from marginalization (p(x_i) = Σ_j p(x_i, x_j)), the step from per-view to cross-view aggregation changes the objective and deserves a clearer justification than the paper provides.

- **The momentum update mentioned for GMM stabilization is underspecified.** The paper states "apply a momentum update to stabilize training" (Sec. 3.2.1) but does not explain whether this is momentum on GMM parameters, on the marginal estimates, or on some other quantity. Without this detail, the training dynamics are ambiguous.

### Trivial
- In Table 1, SURE on LandUse21 at 0% MR shows ACC=29.29 alongside ARI=65.64. While theoretically possible (pure but poorly matched clusters), this is unusual enough that the authors should verify the numbers.

## Nice-to-Haves

- **Evaluation of category-level mismatch handling.** The paper motivates category-level mismatch as a core contribution but tests only sample-level MR/CR in the main experiments. An explicit evaluation (e.g., synthetic manipulation of class-level correspondence structures) would strengthen the empirical support.
- **Discussion of computational cost.** The OT problem is solved per batch; a brief analysis of training time vs. baselines would help assess practicality.
- **Clarify what "10% accuracy improvements" in the abstract refers to** (absolute percentage points vs. relative improvement) for precision.

## Removed Points

These points from the input review are removed with brief justification:

- **"Eq. (3) is a different objective, not a reformulation of Eq. (2)"** — This is technically overstated. Since p(x_i^(v1)) = Σ_j p(x_i^(v1), x_j^(v2)) by marginalization, Eq. (3) is V times Eq. (2) up to a constant. The transition could be clearer, but it is not incorrect.
- **"Computational cost is not discussed"** (as a weakness) — The paper states OT is solved "within batches of 512" (Sec. 4.1), which addresses the scalability concern. Deferred to nice-to-have.
- **"Category-level mismatch is never directly tested"** — The paper explicitly notes this is "an intrinsic challenge" and evaluates it indirectly via posterior visualization (Fig. 3), which is a reasonable approach.
- **Missing related works** — Cannot verify; removed per policy.
- **Parser-stripped appendix content concerns** — Per policy, appendix content exists in the original submission but is removed by the parser.
- **Formatting/style nitpicks and typographical issues** — These are parser artifacts, not author errors.
- **Reproducibility nitpicks about trivial implementation details** — Removed per policy.

## Novel Insights

The most incisive observation from the review process is that the GMM-guided marginal formula (Eqs. 13–14) is presented as a probability estimate but lacks the normalization guarantees that would make it a valid marginal constraint for optimal transport. This is not standard in most OT-based MVC methods, which typically use simpler (normalized) marginals. If the paper normalizes in implementation, this should be stated; if not, the OT problem is technically infeasible. This observation reveals a gap between the mathematical formalism and the practical implementation that should be addressed regardless of the final acceptance decision.

## Suggestions

1. Clarify the GMM marginal estimation: either (a) add explicit normalization to ensure $\sum_i p_i^{(v_1)} = \sum_j p_j^{(v_2)} = 1 - \rho$, (b) derive the formula from first principles, or (c) clearly state what normalization is applied in practice.
2. Add a controlled comparison that isolates NC-robustness: report the *performance drop* (clean → noisy) for both CorreGen and DIVIDE, rather than only raw absolute numbers.
3. Specify how $\rho$ is set — fixed hyperparameter, tuned per dataset, or estimated — and discuss sensitivity.
4. Add standard deviations to all tables.
5. Qualify the "consistently achieves the best performance" claim to acknowledge counterexamples.
6. Clarify what "momentum update" refers to for the GMM.

## Score and Decision

The paper addresses a real problem with a conceptually clean approach and obtains strong results on the most challenging dataset. However, the methodological gap in the marginal estimation, the confounded evaluation design, and the unspecified $\rho$ parameter are significant issues that prevent full confidence in the claims as presented. These are fixable, but the current version does not adequately support its central thesis that the method is specifically effective for handling noisy correspondence.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>