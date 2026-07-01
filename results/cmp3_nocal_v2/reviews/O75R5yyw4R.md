## Summary

This paper proposes IterRef, a test-time scaling method for discrete diffusion models that uses Multiple-Try Metropolis (MTM) to iteratively refine intermediate sampling states via reward-guided noising-denoising transitions. The method is grounded in an MTM framework with a derived acceptance ratio, and is evaluated across language (MDLM, LLaDA-8B) and image (MaskGIT) domains with multiple reward functions. The core idea—applying MCMC refinement at intermediate timesteps rather than searching over trajectories—is well-motivated and produces consistently strong empirical results.

## Strengths

1. **Well-motivated problem framing and principled method design.** The paper correctly identifies a genuine gap: test-time scaling for discrete diffusion faces unique obstacles (no gradient-based guidance, irreversible token fixation) that prior work on continuous diffusion does not address. The connection to Multiple-Try Metropolis is non-trivial—the paper tailors both the transition kernel and the balancing function (Eq. 2) to the reward-alignment objective, then verifies that the acceptance ratio collapses to a simple, computable form (Eq. 3). This gives the method a theoretical anchor that most test-time scaling papers lack.

2. **Consistent empirical advantage across diverse settings.** The results in Figure 2 show IterRef consistently outperforming baselines across four language tasks with two backbones (MDLM, LLaDA-8B). On MDLM, IterRef with 2T NFE outperforms all baselines at 32T NFE on three of four tasks. The MaskGIT results (Table 1) extend this pattern to image generation. The ablations (Tables 2–3, Figure 4) provide useful insights into design choices.

3. **Informative ablations that go beyond "our method works."** The timestep selection study (Table 2), the k-vs-N tradeoff (Table 3), and the safety case study (Section 4.5) each isolate a specific design choice. The finding that later denoising stages benefit more from refinement (differing from continuous diffusion patterns) is a genuinely interesting empirical observation.

## Weaknesses

### Fatal

None.

### Major

1. **No uncertainty quantification for any reported result.** All experimental results are reported as point estimates with no error bars, confidence intervals, or variance measures—not in Figure 2, Table 1, Tables 2–3, or Figure 5. The language evaluation uses 15 prompts × 20 samples = 300 generations per condition. Given the stochasticity of discrete diffusion sampling and sensitivity of reward-model evaluation to prompt choice, the absence of variance reporting makes it difficult to assess whether reported gaps (e.g., the 1-point CLIPScore gap at NFE=16 in Table 1) are statistically meaningful. This is the single most consequential missing element for the empirical claims.

2. **Unanalyzed approximation in the core method.** The MTM theory assumes exact evaluation of the intermediate reward r(x_t) = α log E_{x₀∼p_θ(·|x_t)}[exp(r(x₀)/α)]. In practice (line 117), the paper replaces this with a point estimate r(x̂₀), where x̂₀ is the diffusion model's single prediction of x₀ given x_t. This is a hard approximation, especially at highly masked states. The acceptance ratio β = min(1, exp((r(x_t')−r(x_t))/α)) directly depends on these values. While the approximation is shared with prior work (Li et al., 2024; Singhal et al., 2025), the paper's theoretical convergence claim depends on exact r(x_t), and the effect of this approximation on the MCMC acceptance decisions is never analyzed or acknowledged as a limitation.

### Minor

3. **Tension between Algorithm 2 and the text about the resampling step.** Section 3.3 (line 164) states that "the acceptance rate can be evaluated without the need for resampled proposals x_t''" and that "the practical implementation eliminates the resampling step." However, Algorithm 2 (Line 8) explicitly includes proposing N−1 auxiliary samples from K(x_t', ·). If the implementation truly skips this step, the algorithm as presented is misleading; if it does not, the paragraph is inaccurate. This needs clarification.

4. **Compute-efficiency claims are reported at a single operating point without full contextualization.** The "8× faster" claim (Abstract, Figure 1 caption, Section 4.2) is based on one comparison: IterRef (MDLM, Toxicity, 4T NFE) matching FK (MDLM, Toxicity, 32T NFE). The paper's own complexity analysis (Section 3.3) notes that NFE aggregations conflate generative-model and reward-model calls, but this caveat is not incorporated into the headline "8× faster" framing.

5. **No ablation or reporting of α (KL regularization strength).** The hyperparameter α controls the reward-KL tradeoff and appears throughout the theoretical development (Eq. 1–3, the acceptance ratio, and the intermediate reward definition). Its value is never reported for any experiment, and no study examines its effect on results. This is a critical hyperparameter that could substantially change which states are accepted during refinement.

### Trivial

6. **Imprecise framing of token fixation.** The claim that "incorrectly generated tokens cannot be corrected in subsequent denoising steps, since tokens are fixed once generated" (line 15) is stated as a universal property of discrete diffusion but is specific to *absorbing-state* formulations. Other discrete diffusion formulations (e.g., uniform transition) do allow correction. Since the paper only evaluates absorbing-state models, this does not affect the empirical results but is worth clarifying.

## Nice-to-Haves

- **A sensitivity study of α** would strengthen the empirical characterization of the method. This hyperparameter directly controls the acceptance ratio and the target distribution's reward-KL tradeoff.
- **Human evaluation or analysis of reward-model reliability** as a proxy for human preferences would strengthen the claims about generation quality. The paper briefly mentions ImageReward scores (Appendix C.1), but a more systematic discussion would be valuable.
- The timestep ablation (Table 2) compares "Evenly" vs. single-step application under a fixed total budget, which confounds budget concentration with timestep importance. Disentangling these would strengthen the conclusion about later-stage effectiveness.

## Novel Insights

The key non-obvious finding from this paper is that iterative refinement (more MCMC steps k) consistently outperforms parallel exploration (more particles N) at the same compute budget for discrete diffusion test-time scaling. This provides evidence that the bottleneck in guided discrete diffusion sampling is not insufficient trajectory coverage but insufficient correction of the current state's distribution—a qualitative distinction from how test-time scaling is typically understood in continuous diffusion. The finding that later denoising stages benefit more from refinement (Table 2) further challenges the intuition transplanted from continuous diffusion that early stages dominate.

## Suggestions

1. Add error bars (or at minimum, per-condition standard deviations) to all main and ablation figures/tables. If 3 seeds are available, show min/max or standard deviations; otherwise report bootstrap confidence intervals from the 300 generations per condition.
2. Acknowledge the r(x̂₀) approximation explicitly as a limitation of the current analysis, and either provide an empirical study of its impact (e.g., how the acceptance ratio distribution changes when using r(x̂₀) vs. a Monte Carlo estimate of r(x_t)), or argue why the simplification is benign through diagnostic statistics.
3. Reconcile the text in Section 3.3 with Algorithm 2—either remove the claim about eliminating the resampling step, or update the pseudocode to match what is actually implemented.
4. Report the α values used in all experiments and, ideally, provide an ablation showing sensitivity to this parameter.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>