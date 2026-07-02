## Summary

This paper develops a theoretical framework to prove that (non-linear) neural policy ensembles are sub-optimal compared to linear policy ensembles in control settings. The authors provide theoretical results showing that neural ensembles violate stability guarantees even when individual policies are stable, and they empirically validate these claims through comparisons on linear and nonlinear dynamical systems, demonstrating that neural ensembles underperform linear ensembles often by 2 orders of magnitude.

## Strengths

- **Novel theoretical framework**: The paper provides formal definitions (Nonlinearity Measure, Convexity Violations) and proves three main theorems addressing sub-optimality, stability violations, and the disadvantage of non-convex mixing, which is a genuine theoretical contribution to understanding ensemble methods in control.
- **Clear practical implications**: The findings have direct relevance to safety-critical systems, RL-based policy ensembles, and Mixture-of-Experts architectures in agentic AI, making the work broadly impactful beyond pure theory.
- **Thorough empirical validation**: The authors include multiple experiments (linear systems, nonlinear systems, diversity experiments, stability experiments, policy mixing experiments) with statistical significance testing, which strengthens the credibility of the theoretical claims.

## Weaknesses

### Major

- **Limited scope of theoretical results**: Theorem 1 relies on an assumption of a linear system (\(\dot{x} = Ax + Bu\)) while claiming to prove sub-optimality of neural ensembles generally. The theoretical results do not extend to the nonlinear dynamical systems mentioned in the paper's introductory claims. The conditions for Theorem 1 (Diversity, Nonlinearity, Sufficient Complexity) appear to be specific and may not hold broadly.
- **Unconvincing empirical comparisons**: The neural network ensemble is compared against a theoretically optimal LQR ensemble, which is an unfair comparison. The paper does not adequately control for training quality, architecture search, or regularization of the neural networks. The neural ensemble may simply be undertrained rather than fundamentally sub-optimal. Well-tuned neural policies can outperform LQR in many settings, and the paper does not address this.
- **Oversimplification of the claim**: The paper's title and abstract make a sweeping claim that "neural policy ensembles are sub-optimal" in general, but the theoretical proofs only cover specific settings (linear dynamics, specific cost structures). The claim conflates sub-optimality of the specific implementation with fundamental impossibility.

### Minor

- **Missing baselines**: The empirical studies compare neural ensembles only against LQR ensembles and an oracle. There is no comparison against other non-linear policy ensemble methods (e.g., gated mixtures, attention-based mixing, or other RL ensemble methods) that might perform better.
- **Absence of non-linear system theory**: The theoretical analysis is limited to linear-quadratic settings, but the paper claims implications for nonlinear systems. The extension to nonlinear dynamics is asserted rather than proven.

### Trivial

- The figures are adequate but the text descriptions in the captions are verbose and could be more concise.
- Some claims about "2 orders of magnitude" improvement do not appear to be directly supported by the reported numbers in the figures.

## Nice-to-Haves

- A discussion of whether the sub-optimality can be mitigated through specific architectural choices (e.g., residual connections, layer normalization, or ensemble-specific training objectives) would strengthen the work.
- A comparison against learned mixing weights that are constrained to be convex (e.g., softmax over learned parameters) would help isolate whether the issue is the neural network architecture or the non-convex mixing.
- Including experiments on nonlinear dynamical systems with non-quadratic costs would broaden the empirical support.

## Novel Insights

The key insight—that temporal coupling in control settings breaks the variance-reduction benefits of ensemble methods, unlike the classification setting—is genuinely novel and important. The formalization of how nonlinear function approximators can amplify rather than cancel errors through feedback loops provides a useful conceptual framework. However, this insight is primarily demonstrated for linear systems; the generalization to nonlinear systems remains a claim rather than a proven result.

## Suggestions

1. Revise the title and abstract to reflect the specific conditions under which the sub-optimality is proven (linear dynamics, quadratic costs) rather than claiming general sub-optimality of neural policy ensembles.
2. Include experiments where neural network ensembles are trained more carefully, with hyperparameter optimization and regularization, to ensure the comparison is fair and that the observed gap is not an artifact of poor neural network training.
3. Provide at least one experiment on a nonlinear dynamical system to support the claim that the theoretical results extend beyond linear settings.
4. Consider adding a baseline where the neural mixing weights are constrained to be convex (e.g., via softmax) to test whether the issue is non-convexity or neural network architecture.

## Score and Decision

The paper presents a novel theoretical framework with clear proofs for linear systems, supported by empirical evidence. However, the sweeping claims about neural policy ensemble sub-optimality are not fully justified by the limited theoretical scope (linear dynamics, quadratic costs). The empirical comparisons are weakened by not ensuring that neural networks are well-optimized, and the generalization to nonlinear systems is asserted without proof. The paper is borderline because while the core insight is interesting and the theory is sound for specific settings, the contribution is narrower than claimed.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>