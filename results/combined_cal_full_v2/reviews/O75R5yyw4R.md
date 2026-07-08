Now let me finalize the review with score and decision.

## Summary

This paper introduces IterRef, a test-time scaling method for discrete diffusion models that uses Multiple-Try Metropolis (MTM) with noising-denoising transitions to iteratively refine intermediate states toward higher reward. The core idea — correcting misaligned tokens through an MCMC loop that noises then denoises — is conceptually clean and addresses a genuine limitation of existing single-pass guidance methods. The method is evaluated across text (MDLM, LLaDA-8B) and image (MaskGIT) domains with multiple reward functions, consistently outperforming baselines (BoN, FK, SVDD, SoP) at most compute budgets.

## Strengths

- **Well-motivated and principled method design.** The paper identifies a genuine problem in discrete diffusion (token discretization prevents gradient-based guidance) and proposes an MCMC-based refinement loop using noising-denoising transitions. The connection to Multiple-Try Metropolis (MTM) is apt, and the balancing function (Eq. 2) that simplifies the acceptance probability to `min(1, exp((r(x_t') - r(x_t))/α))` is elegant. This is not a trivial adaptation of an existing method.

- **Consistent and broad empirical results.** The method is evaluated across two modalities (text and image), three backbones (MDLM, LLaDA-8B, MaskGIT), and multiple reward functions (CoLA, Toxicity, Sentiment, Perplexity, CLIPScore). IterRef outperforms baselines at most compute budgets in virtually every setting. Table 1 (MaskGIT with CLIPScore) shows large and consistent improvement over FK and BoN across all NFE budgets.

- **Informative analysis of refinement dynamics.** Section 4.4 provides genuinely useful insights: (a) later-stage refinement is more effective than early-stage (contrasting with continuous diffusion where early steps dominate), and (b) increasing iterations k matters more than increasing particles N. These findings are non-obvious and practically useful.

- **Practical efficiency design.** The paper acknowledges computational cost and proposes concrete mitigations: the balancing function eliminates the need for explicit backward-proposal resampling, rejected-proposal pool reuse avoids regenerating candidates, and selective application via the effective timestep set U allows targeted computation.

## Weaknesses

### Fatal
None.

### Major

- **Convergence guarantee relies on an unverified reversibility assumption, and the theoretical claim is overstated.** Proposition 1 assumes q and p_θ form a reversible Markov kernel — an assumption not verified for any of the absorbing-state (masked) diffusion models used in experiments (MDLM, LLaDA, MaskGIT), where the forward process adds masks and the reverse removes them (an asymmetric structure that makes reversibility questionable). The abstract claims "proving convergence to the reward-aligned distribution" without qualifying this assumption. While the method may work well in practice, the advertised theoretical support is weaker than stated.

- **No statistical uncertainty reported.** All results are point estimates with no error bars, standard deviations, or confidence intervals. With 15 prompts × 20 samples = 300 generations per condition for the language experiments, variability across prompts could be substantial. Without uncertainty measures, it is difficult to assess whether IterRef's advantages over baselines at equivalent compute budgets are statistically significant. This affects the credibility of precise quantitative claims such as "8× faster" and "2× improvement."

### Minor

- **NFE aggregation may obscure cost structure differences.** The paper aggregates generative-model calls and reward-model evaluations into a single NFE metric while acknowledging (lines 174) that their cost ratio varies by model scale and that "aggregating these into a single NFE value may obscure meaningful differences." IterRef requires N reward-model evaluations per refinement step. Wall-clock analysis is deferred to an appendix (not visible here), so the main NFE-based comparisons are hard to interpret fairly.

- **No sensitivity analysis for hyperparameter α.** The method's temperature parameter α controls the reward KL strength, yet the paper does not report how α was chosen or how results vary with it. This affects reproducibility.

- **Intermediate reward approximation not analyzed.** The paper notes that intermediate rewards r(x_t) can be approximated by evaluating the reward function on the model's x_0 prediction (line 117). This is a non-trivial approximation that introduces error into the MTM target distribution, but its impact on the convergence guarantee is not discussed.

- **Effective timestep comparison (Table 2) is ambiguously described.** The paper states it "fix[es] the total computational budget by allocating 4T NFEs at each selected step" but does not clarify how the budget is controlled across the single-step conditions (0.9T, …, 0.1T) versus the "Evenly" condition, making it unclear whether "Evenly" is genuinely more effective or simply uses more total compute.

- **Choice of noise level s > t not specified.** The transition kernel K(x_t, x_t') requires choosing how far forward to noise before denoising back. The paper does not explain how s is determined, which affects the exploration-exploitation tradeoff.

- **Asymptotic guarantee with small practical k.** The convergence guarantee is asymptotic (k → ∞), but practical usage is k = 1–16. The paper provides no mixing diagnostics (acceptance rates, effective sample sizes, trace plots) to assess chain convergence with these values.

### Trivial

- Algorithm 2 line 9 refers to `x_t'^{cand}` which is not defined in the pseudocode.

## Nice-to-Haves

- A dedicated limitations section discussing the reversibility assumption, intermediate vs. final output convergence gap, sensitivity to hyperparameters, and conditions where IterRef does not help (e.g., CoLA with LLaDA-8B where BoN outperforms IterRef).
- Sensitivity analysis for α and the noise level s.
- Mixing diagnostics (acceptance rates, trace plots) to support the asymptotic convergence claim with finite k.

## Removed Points

These points from the input review were removed after cross-checking against the paper:

1. **"Nearly zero cost" claim about noising process** — The paper correctly states the noising process (random remasking) is cheap; this does not claim the whole refinement loop is cheap. The critic misread this. Removed.

2. **Pool reuse breaks MTM framework** — The paper correctly notes pool reuse happens only upon rejection (when state x_t is unchanged), so the pool drawn from K(x_t, ·) remains valid. Removed.

3. **w_n = N^{-1} typo** — N^{-1} = 1/N, not a typo. Removed.

4. **Missing PG-DLM and DTS baselines** — The paper already includes 4 baselines (BoN, SoP, SVDD, FK) and discusses PG-DLM/DTS in Related Work. Scope creep. Removed.

5. **Introduction overstates about uncorrectable tokens** — The paper describes a general challenge of discrete diffusion and acknowledges re-masking solutions (Wang et al., 2025) in Related Work. Removed.

6. **Guarantee about intermediate vs. final outputs gap** — Partially valid but the gap is narrow since optimal intermediate distributions propagate to final outputs through the Markov chain. The paper targets intermediate distributions explicitly. Overblown. Removed.

## Novel Insights

None beyond the paper's own contributions. The review process confirms the paper's main narrative: IterRef is a clever adaptation of MTM to discrete diffusion with a noising-denoising kernel, and its empirical results are broad and consistent. The main insights from the review relate to calibration of the theoretical claims and the need for statistical rigor.

## Suggestions

- Qualify the theoretical claim in the abstract and introduction to reflect that convergence requires the reversibility assumption, and discuss whether this assumption holds for masked diffusion models.
- Add error bars (bootstrap confidence intervals or standard errors across prompts) to all quantitative results.
- Report wall-clock time in the main paper (not just the appendix) and discuss the cost ratio between reward and generative models explicitly.
- Add a sensitivity study for α and clarify how the noise level s is selected.
- Clarify the budget control in the effective timestep experiment (Table 2).

## Score and Decision

**Calibration details:** I retrieved anchor papers across score bands using topical similarity queries. The most relevant anchors are:
- *Steering Masked Discrete Diffusion Models via DDPP* (6.25) — shares the task of steering masked discrete diffusion; our paper has stronger strength weights (9.65–11.04 vs 8.81–9.50) and comparable weakness weights.
- *Unlocking Guidance for Discrete State-Space Diffusion and Flow Models* (6.50) — addresses guidance in discrete state-spaces; our paper has comparable strength weights and less severe weakness weights (no item as negative as its -5.27).
- *Derivative-Free Guidance (SVDD)* (3.80) — addresses a similar problem but had fundamental issues with unfair α settings and biased value function estimates; our paper does not share these issues.
- *Think Twice Before You Act (DPMC)* (4.75) — applies MCMC to diffusion but for inverse problems; our paper has stronger strengths and more consistent empirical breadth.

**Bracket reasoning (Round 1):** The paper clearly clears the 1.5–3.5 reject range and the 3.5–5.5 weak reject range, as it has a strong method contribution and broad positive results. Its strengths place it in the 5.5–7.5 range. Within this range, the most topically similar anchors (DDPP at 6.25, Unlocking Guidance at 6.50) share similar patterns of strengths and addressable weaknesses.

**Narrowing (Round 2):** Comparing weighted items: our paper's four strengths (9.65, 11.04, 10.61, 10.13) are comparable to DDPP's top strengths (9.50, 9.16, 8.81) and Unlocking Guidance's (10.73, 9.18). Our highest-weighted weaknesses (5.99, 5.57) are lower than DDPP's highest (7.59). The two major concerns (reversibility assumption at 0.21, missing error bars at 2.41) carry relatively low negative weight, suggesting they are addressable rather than fatal. The paper's contributions are real and the method is sound.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>