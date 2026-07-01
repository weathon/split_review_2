## Summary

This paper introduces IterRef, a test-time scaling method for discrete diffusion models that performs reward-guided iterative refinement via a Multiple-Try Metropolis (MTM) framework. The core idea is to use noising-denoising transitions at intermediate sampling steps to progressively correct misaligned tokens, with a theoretical guarantee of convergence to the reward-aligned distribution. Experiments on language (MDLM, LLaDA-8B) and image (MaskGIT) generation tasks show consistent improvements over prior baselines, often achieving large gains at low compute budgets (e.g., up to 8× faster scaling).

## Strengths

- **Addresses an important and underexplored problem.** Test-time scaling for discrete diffusion is far less studied than for autoregressive or continuous diffusion models, and the paper convincingly identifies the unique challenges (no gradients, irreversible tokens).
- **Principled methodology with theoretical support.** The use of Multiple-Try Metropolis with a carefully chosen transition kernel and balancing function yields a clean acceptance ratio (Eq. 3) and a formal convergence guarantee (Proposition 1). This gives the method a strong foundation beyond heuristics.
- **Strong and consistent empirical results.** IterRef outperforms all baselines (BoN, FK, SVDD, SoP) across four language tasks and two backbones, and on MaskGIT image generation. The improvements are especially pronounced at low NFE budgets, which is practically relevant.
- **Informative ablations and analysis.** The study of scaling with \(k\) vs. \(N\), effective timesteps, and the safety case study provide useful insights into when and why IterRef works. The finding that later denoising stages are more critical (unlike continuous diffusion) is particularly interesting.

## Weaknesses

### Major

- **The reversibility assumption for the convergence proof is questionable.** Proposition 1 assumes that \(q\) and \(p_\theta\) form a reversible Markov kernel. In practice, the true forward process \(q\) and the learned reverse \(p_\theta\) are not generally reversible; the paper does not justify this assumption or discuss how it can be satisfied. While the empirical results suggest the method works even when this assumption is violated, the theoretical claim is weakened.

### Minor

- **Inconsistency between the claimed simplification and Algorithm 2.** The text states that through the choice of balancing function, the resampling step (backward proposals) can be eliminated in practice. However, Algorithm 2 still includes steps 8–9 that generate \(N-1\) auxiliary samples. This discrepancy makes it unclear what the actual implementation does and how the reported NFEs are computed.
- **The “8× faster” claim is not precisely defined.** The label in Figure 1(b) and the text refer to “8× faster” but the metric used (e.g., NFE to reach a given reward) is not specified. The figure shows IterRef reaching a reward of ~0.95 at NFE=32 while FK reaches ~0.85, but a direct speedup factor requires a specific target reward threshold.
- **Lack of statistical significance reporting.** All results are reported as single numbers without error bars or standard deviations. Given the stochastic nature of the sampling process, this makes it difficult to gauge the variability and reliability of the improvements.

### Trivial

- Missing parenthesis in Equation 3: \(\exp((r(x_t') - r(x_t)/\alpha))\) should be \(\exp((r(x_t') - r(x_t))/\alpha)\).  
- The notation \(\mathcal{U}\) as “effective timestep set” is introduced but its definition is slightly vague (e.g., why “effective” rather than simply “selected”).

## Nice-to-Haves

- A more detailed comparison with the recent works PG-DLM (Dang et al., 2025) and DSearch (Li et al., 2025) mentioned in the related work section would strengthen the positioning of IterRef.
- An analysis of wall-clock time (beyond NFE) for the main experimental setups would better illustrate practical efficiency, especially given the separate calls to the generative model and reward model.

## Novel Insights

Beyond the method itself, the paper provides an interesting observation that for discrete diffusion, refinement at later denoising stages is more effective than at early stages, in contrast to continuous diffusion where most content is determined early. This suggests that the error-correction dynamics differ fundamentally between discrete and continuous state spaces. The ablation showing that increasing the number of iterations \(k\) is more beneficial than increasing the number of particles \(N\) also highlights the value of iterative refinement over simple resampling.

## Suggestions

1. Clarify the actual implementation with respect to the backward proposal resampling: does the released code eliminate Steps 8–9 as claimed, or is Algorithm 2 the full procedure? This affects both the correctness of the MTM derivation and the NFE accounting.
2. Add error bars or confidence intervals to the main plots (Figures 2 and 5) to give readers a better sense of the result stability.
3. Relax or discuss the reversibility assumption in Proposition 1. If it cannot be justified, rephrase the theoretical claim as a heuristic guarantee or provide empirical evidence that the chain still converges approximately.
4. Specify the exact reward threshold used for the “8× faster” claim or rephrase to avoid ambiguity.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>