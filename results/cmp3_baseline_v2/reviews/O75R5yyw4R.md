## Summary

The paper proposes **IterRef**, a test-time scaling method for discrete diffusion models that uses Multiple-Try Metropolis (MTM) with noising-denoising transitions to iteratively refine intermediate states toward a reward-aligned distribution. The method is theoretically grounded (convergence guarantee under a reversibility assumption) and empirically evaluated across text (MDLM, LLaDA-8B) and image (MaskGIT) domains, consistently outperforming baselines such as FK Steering, SVDD, and Best-of-N under equal compute budgets.

## Strengths

- **Novel and principled approach**: IterRef is the first method to apply Multiple-Try Metropolis with a noising-denoising kernel for iterative refinement in discrete diffusion. The design of the transition kernel and balancing function is well-motivated and leads to a simple acceptance rule (Eq. 3) that depends only on reward differences.
- **Strong empirical results**: Across four language tasks and one image task, IterRef consistently achieves higher reward than all baselines, often with large margins (e.g., 8× faster on Toxicity with LLaDA-8B, Table 1 shows clear gains on MaskGIT). The scaling plots (Figure 2) demonstrate that IterRef benefits from additional compute more effectively than prior methods.
- **Insightful analysis**: The study of effective timesteps (Table 2) reveals that later denoising stages are more important for discrete diffusion, contrasting with continuous diffusion where early steps dominate. The comparison of iterations \(k\) vs. particles \(N\) (Table 3) shows that iterative refinement is more beneficial than simply increasing the number of candidates, supporting the core design choice.
- **Theoretical foundation**: Proposition 1 provides a convergence guarantee to the optimal intermediate distribution under the MTM framework, and the derivations of importance weights and acceptance rate are clearly presented.

## Weaknesses

### Fatal
None.

### Major
- **Reversibility assumption for convergence guarantee**: Proposition 1 assumes that \(q\) and \(p_\theta\) form a reversible Markov kernel. In practice, the learned reverse process \(p_\theta\) is not guaranteed to be reversible with respect to the forward noising process \(q\). The paper does not discuss whether this assumption holds for trained discrete diffusion models or how violations might affect the theoretical guarantee. This weakens the claimed theoretical justification.
- **Compute fairness and NFE metric**: The paper uses NFE (number of function evaluations) as the unified compute metric, counting both generative model calls and reward model calls equally. However, IterRef requires additional reward model evaluations per refinement step (N per iteration), while baselines like BoN may have different ratios. The paper acknowledges this issue (Section 3.3) but still reports only NFE in the main results. For smaller models like MDLM where reward model cost is comparable, this could bias comparisons. Separate reporting of generative and reward model calls would strengthen the evaluation.
- **Missing comparisons with recent strong baselines**: The related work mentions DSearch (Li et al., 2025), DTS (Jain et al., 2025), and PG-DLM (Dang et al., 2025), but these are not included in the experimental comparison. Given that these methods also address inference-time alignment for discrete diffusion, their absence limits the completeness of the empirical evaluation.

### Minor
- **Ambiguous claim about improvement magnitude**: The paper states "up to a 2× improvement on Toxicity reward with LLaDA-8B under the equal compute" (Section 1), but Figure 2(b) shows IterRef achieving ~0.95 vs. FK ~0.85 at NFE=32, which is roughly a 12% relative improvement. The "2×" likely refers to compute efficiency (8× faster) rather than reward magnitude, but the phrasing is unclear.
- **Limited discussion of limitations**: The paper does not discuss potential failure cases, sensitivity to hyperparameters (\(k\), \(N\), \(\alpha\), effective timestep set), or scenarios where IterRef might underperform. Including such discussion would improve the paper's completeness.
- **Algorithm description clarity**: Algorithm 2 uses notation \(x_t'^{\text{cand}}\) in line 9 that is not defined; it should be \(x_t'\). The pseudocode could be more precise.

### Trivial
None.

## Nice-to-Haves

- Provide separate plots for generative model calls and reward model calls to fully justify the NFE-based comparison.
- Include a sensitivity analysis for the temperature parameter \(\alpha\) and the effective timestep set \(\mathcal{U}\).
- Add a discussion on the practical validity of the reversibility assumption and how the method behaves when it is violated.

## Novel Insights

Beyond the paper's own contributions, the finding that later denoising stages are more critical for reward-guided refinement in discrete diffusion (Table 2) is a genuinely novel insight that contrasts with the common wisdom from continuous diffusion. This suggests that the dynamics of discrete diffusion differ fundamentally from continuous diffusion, and that test-time scaling strategies should focus on the later, more deterministic stages. The observation that increasing iterations \(k\) is more effective than increasing particles \(N\) (Table 3) further supports the value of iterative refinement over simple resampling.

## Suggestions

- Clarify the reversibility assumption and either provide empirical evidence that it approximately holds for the models used, or discuss how the method remains effective even when the assumption is violated.
- Include comparisons with DSearch and DTS to strengthen the empirical evaluation.
- Report compute costs separately for generative model and reward model calls, or justify why NFE is a fair metric for all methods.
- Add a limitations section discussing hyperparameter sensitivity and potential failure modes.

## Score and Decision

The paper presents a novel, theoretically motivated, and empirically strong method for test-time scaling in discrete diffusion. The weaknesses (reversibility assumption, compute fairness, missing baselines) are significant but not fatal, and the empirical results convincingly demonstrate the method's effectiveness across multiple domains. The paper makes a clear contribution to the field.

**Score**: 8

**Decision**: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>