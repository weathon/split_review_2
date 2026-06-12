## Summary

The paper proposes **IterRef**, a test-time scaling method for discrete diffusion models. IterRef applies Multiple-Try Metropolis (MTM) at selected denoising steps, using a noising-denoising transition kernel to iteratively refine intermediate states toward a reward-aligned target distribution. The method is accompanied by a convergence guarantee, practical computational optimisations (pool reuse, selective timestep application), and extensive experiments across language (MDLM, LLaDA-8B) and image (MaskGIT) domains with multiple reward functions, consistently outperforming prior guidance methods.

## Strengths

- **Novel and principled method**: IterRef is the first to adapt Multiple-Try Metropolis for test-time scaling in discrete diffusion. The use of a carefully designed kernel and balancing function yields a tractable acceptance ratio (Equation 3) while preserving theoretical convergence guarantees (Proposition 1). The approach directly addresses the irreversibility problem of tokens in discrete diffusion by allowing in-place refinement.

- **Theoretical grounding**: The paper provides a convergence proof showing that IterRef sampling converges to the optimal reward-aligned distribution under the assumption of a reversible Markov kernel. This formal foundation is rare among test-time scaling methods for discrete diffusion and strengthens confidence in the method.

- **Strong and consistent empirical results**: Across four language tasks and two backbones (MDLM, LLaDA-8B), IterRef consistently outperforms four strong baselines (BoN, FK, SoP, SVDD) at nearly every compute budget. Gains are especially pronounced at low compute budgets (e.g., 8× faster on Toxicity with LLaDA-8B at low NFE). The method also transfers effectively to image generation (MaskGIT + CLIPScore), achieving the best quantitative results and visually improved samples.

- **Insightful analysis**:
  - Demonstrates that increasing the number of iterations \(k\) is more effective than increasing the number of particles \(N\) (Table 3), supporting the core thesis of iterative refinement.
  - Reveals that later denoising timesteps (closer to \(t=0\)) are more influential for reward-guided refinement in discrete diffusion—a noteworthy contrast to continuous diffusion where early steps dominate (Table 2).
  - Scaling analysis (Figure 4) shows consistent improvements with both \(k\) and \(N\), with larger gains from iterating.

- **Practical design**: The authors incorporate efficient implementation tricks (balancing function that eliminates auxiliary resampling, pool reuse upon rejection, selective timestep application) that make IterRef computationally viable compared to particle-based methods.

## Weaknesses

### Fatal
None.

### Major
- **Strong assumption for convergence guarantee**: Proposition 1 assumes that the noising kernel \(q\) and the denoising kernel \(p_\theta\) together form a reversible Markov kernel. In practice, the learned denoiser \(p_\theta\) is an approximation that may not satisfy this property. While such assumptions are common in MCMC analyses, the paper does not discuss how severely a violation would affect convergence, nor does it provide empirical diagnostics (e.g., trace plots, autocorrelation, or checks of detailed balance). This gap weakens the practical applicability of the theoretical guarantee.

### Minor
- **Acceptance ratio derivation is dense and somewhat opaque**: The key simplification leading to Equation 3 (importance weights \(w_n = 1/N\) and acceptance probability \(\beta = \min(1, \exp((r(x_t')-r(x_t))/\alpha)\)) depends on a non-obvious choice of balancing function (Equation 2). The derivation is relegated to Appendix D.2, and the main text offers no intuition or sanity check. A more intuitive explanation or a simple worked example would help readers trust the result.

- **Effective timestep experiment budget is unclear**: The description "We fix the total computational budget by allocating \(4T\) NFEs at each selected step" is confusing. If IterRef is applied only at a single step, does the total NFE equal \(4T\)? If applied evenly across all \(T\) steps, does each step receive \(4T/T = 4\) NFEs? The table labels (e.g., \(0.1T\), Evenly) do not make the total cost comparable across columns, making it difficult to interpret the relative effectiveness of different application strategies.

- **Limited discussion of reward model approximation**: The intermediate reward \(r(x_t)\) is approximated by evaluating the reward on the denoiser’s predicted \(x_0\). This approximation is used in both baseline methods and IterRef. The paper does not analyse how approximation errors propagate across iterative refinement steps, nor does it justify that the MTM framework remains robust under such approximations.

- **Overclaim on "8× faster"**: The main text and Figure 1(b) highlight "8× faster" on LLaDA-8B with safety reward. While indeed at low NFE IterRef reaches higher reward than baselines, the "8×" factor is based on a single comparison point (IterRef at NFE=4 vs FK at NFE=32 achieving roughly the same reward). This framing is dramatic but somewhat cherry-picked; the advantage is smaller at higher compute budgets. The claim should be contextualised.

### Trivial
- None.

## Nice-to-Haves

- Wall-clock time analysis comparing IterRef with baselines would be valuable, especially since the paper notes that reward-model vs. generative-model cost ratios differ across backbones. (This may already appear in Appendix C.4, which was removed.)
- Ablation on the assumption of reversible kernel, e.g., by measuring how well detailed balance is satisfied empirically during refinement.
- Analysis of how many MTM iterations are needed in practice to approach stationarity for typical discrete diffusion models.

## Novel Insights

Beyond the paper’s own contributions, a genuinely novel insight is the _inversion_ of the typical diffusion-guidance locus: whereas continuous diffusion models concentrate most content decisions in early denoising steps, IterRef reveals that discrete diffusion (with absorbing-state masks) benefits most from reward-guided refinement at _later_ steps (closer to \(t=0\)). This suggests that the token-fixing problem in discrete diffusion may be partially circumvented by re-noising and re-denoising near the end of the trajectory—a qualitatively different dynamic from continuous diffusion. The observation that iterative depth (\(k\)) matters more than particle count (\(N\)) further reinforces that in-place correction, rather than parallel search, is the more effective scaling strategy for this setting.

## Suggestions

1. Provide a cleaner explanation of the acceptance ratio simplification (Equation 2 → Equation 3) in the main text, perhaps with a compact derivation or an intuitive sketch.
2. Clarify the total NFE budget in the effective-timestep experiment (Table 2). State explicitly how many total NFEs are used for each condition and what “Evenly” means in terms of per-step NFE.
3. Discuss the reversibility assumption: acknowledge its strength, and consider including a small empirical validation (e.g., comparing the forward and reverse KL of the proposal distribution) to show that the assumption is reasonably satisfied.
4. Tone down the “8× faster” claim or provide a more balanced quantitative summary (e.g., average speedup across multiple reward thresholds).
5. (Optional) Report ImageReward scores (mentioned in §4.3) to strengthen the qualitative claims.

## Score and Decision

I assess that the paper makes a significant, well-grounded contribution to an important problem (test-time scaling for discrete diffusion). The method is novel, theoretically motivated, and supported by strong empirical results across diverse settings. The weaknesses are not fatal and can be addressed via clarification and minor supplementary analysis. The paper meets the bar for acceptance at a top venue like ICLR.

MY FINAL SCORE: <score>8.0</score>  
MY FINAL DECISION: <decision>Accept</decision>