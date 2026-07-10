Now let me finalize the review.

## Summary

This paper introduces IterRef, a test-time scaling method for discrete diffusion models that uses Multiple-Try Metropolis (MTM) with noising-denoising transitions to iteratively refine intermediate states toward reward-aligned distributions. The method is theoretically grounded (convergence to a target distribution via MTM) and empirically evaluated across text (MDLM, LLaDA-8B) and image (MaskGIT) domains, consistently outperforming prior reward-guided generation methods (FK, SVDD, SoP, BoN) under comparable compute budgets.

## Strengths

- **Novel and principled approach.** The paper identifies a genuine limitation of existing reward-guided discrete diffusion methods — intermediate states cannot be corrected once generated — and proposes a principled MCMC-based solution by applying Multiple-Try Metropolis with noising-denoising transitions. This is conceptually distinct from trajectory-search (FK, SVDD) and particle-filter (SMC) methods. *(impact: +9.7)*

- **Appropriate theoretical framing with concrete design choices.** The transition kernel (Eq. 2) and balancing function are specifically designed so the acceptance probability simplifies to a tractable form (Eq. 3), preserving detailed balance while enabling practical computation. Proposition 1 provides a convergence guarantee for the idealized procedure. *(impact: +8.7)*

- **Strong and consistent empirical results across modalities.** IterRef consistently outperforms four baselines on four text tasks with two diffusion LM backbones (MDLM, LLaDA-8B, Figure 2) and on image generation with MaskGIT (Table 1). The gains are not marginal — on Toxicity with MDLM, IterRef at 4T NFEs matches FK at 32T NFEs. *(impact: +9.6)*

- **Informative analysis in Section 4.4.** The findings that (a) refinement is more effective at later denoising stages (Table 2) and (b) increasing iterations *k* helps more than increasing particles *N* at fixed compute (Table 3) provide actionable insights about discrete diffusion dynamics that go beyond the method itself. *(impact: +8.6 / +8.1)*

## Weaknesses

### Fatal
None.

### Major

- **Gap between theoretical guarantee and practical approximation.** The paper acknowledges (line 117) that intermediate rewards *r*(*xₜ*) are approximated by evaluating the reward function on a single point estimate (the model's prediction of *x₀*), whereas the true intermediate reward (line 61) is defined as an expectation over all possible *x₀* completions. Proposition 1's convergence guarantee applies to MTM targeting the true *p*(*xₜ*), but the actual algorithm uses an approximation whose divergence from the true target is unanalyzed. The paper does not discuss conditions under which this approximation is accurate. *(impact: -3.4)*

### Minor

- **Proposition 1's reversibility assumption is unexamined.** The proposition assumes that *q* (forward corruption) and *p*⍬ (learned reverse) jointly form a reversible Markov kernel. This is a strong assumption in discrete diffusion with absorbing-state masking — *q* and *p*⍬ are not jointly constructed to satisfy detailed balance. The paper does not justify when or why this would hold, nor does it discuss implications if it fails. *(impact: -3.6)*

- **No limitations section.** The conclusion (Section 6) does not discuss limitations. The method depends on reward models that score partially-noised intermediate states, which is a non-trivial requirement, and there is no discussion of potential failure modes (reward hacking, diversity degradation, sensitivity to α). *(impact: -2.8)*

- **Over-claiming on "8x faster."** The 8× result (line 200) is specifically for Toxicity with MDLM (IterRef at 4T NFEs matches FK at 32T NFEs). Gains on other tasks and backbones are more modest (e.g., CoLA with LLaDA-8B where BoN sometimes wins). Presenting "8x faster" prominently in Figure 1 without calibrating it as a best case is misleading. *(impact: -2.4)*

- **Undefined baselines in Section 4.5 case study.** The detoxification experiment (Figure 5) compares against baselines labeled SLP, SR, SVTOD, but these are not defined anywhere in the main text, making the comparison unverifiable. *(impact: -1.3)*

- **Ambiguous compute budget in Table 2.** The paper says "We fix the total computational budget by allocating 4T NFEs at each selected step" (line 261) but the table caption says "under the same total cost" for the Evenly column. It is unclear whether Evenly receives 4T NFEs per timestep (vastly more total compute) or the same total 4T spread across all timesteps. *(impact: -0.1)*

- **Computational cost ambiguity.** The paper does not specify the value of *s* (the noise level in the transition kernel) or the resulting (*s*−*t*) cost per proposal. The paper references Appendix C.4 for wall-clock analysis, but the main text should state the value of *s* used. *(impact: -0.3)*

### Trivial
None.

## Nice-to-Haves

- An ablation reporting the empirical acceptance rate of the MTM proposal step would clarify how much the Metropolis correction contributes.
- Sensitivity analysis for α (KL regularization strength) would help practitioners choose this parameter.
- Variance/error bars across seeds for the main results would increase confidence, though single-run evaluation is common practice for large-scale diffusion benchmarks.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Baseline fairness concern (SoP/SVDD from continuous diffusion):** The critic questioned SoP and SVDD as baselines since they were designed for continuous diffusion. However, IterRef also convincingly outperforms FK Steering, which IS designed for discrete diffusion. SoP/SVDD are supplementary comparisons; the core result against FK already demonstrates the method's advantage. Removed as a weak criticism. *(dismissed)*
- **Pool reuse / backward proposal step:** The critic questioned whether Algorithm 2's line 8 (backward proposals) is executed in practice. The paper explicitly explains (line 164) that the balancing function eliminates this step in the practical implementation. Algorithm 2 presents the full theoretical pseudocode, while the optimization is described in the text. Removed as a misunderstanding. *(dismissed)*
- **Figure 1(b) baseline inconsistency:** The critic noted that Figure 1(b) uses labels IS, SMC, PK while the main experiments use BoN, FK, SVDD, SoP. Figure 1 is a conceptual overview using generic labels; the specific instantiations appear in the main experiments. Removed as a minor presentation concern. *(weakened/dismissed)*
- **Ethics statement inconsistency:** Concern about toxicity-increasing experiments not shown in the main text. These may be in the stripped appendix. Removed as speculative. *(dismissed)*

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Address the intermediate reward approximation gap: add a small-scale experiment or discussion quantifying how well the point-estimate approximation of *r*(*xₜ*) correlates with a Monte Carlo estimate of the true expected reward.
2. Specify the value of *s* (noise level) used in all experiments and report (*s*−*t*) explicitly so readers can assess the per-proposal cost.
3. Discuss or empirically verify the reversibility assumption (q and p_θ jointly forming a reversible kernel) underlying Proposition 1.
4. Add a limitations section covering: dependence on reward models that score partially-noised states, the approximation gap, sensitivity to α, and potential diversity degradation from aggressive refinement.
5. Calibrate the "8x faster" framing to reflect the range of observed gains.
6. Define all baselines (SLP, SR, SVTOD) in Section 4.5 and clarify the compute budget for Evenly vs. single-step in Table 2.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>