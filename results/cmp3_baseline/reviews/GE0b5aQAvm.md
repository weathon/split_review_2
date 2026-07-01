## Summary
This paper argues that ensembles of nonlinear (neural network) policies are inherently suboptimal compared to ensembles of linear policies for control tasks.  The authors present theoretical results (suboptimality gap, stability violation, suboptimality of nonlinear mixing) for linear-quadratic settings and provide empirical comparisons on controlled linear and nonlinear dynamical systems.  The central claim is that neural policy ensembles suffer from temporal error amplification and function-space geometry issues that linear ensembles avoid.

## Strengths
- The paper attempts to formalize an important distinction between ensemble classifiers and ensemble policies, highlighting the role of temporal coupling in the latter.
- The theoretical analysis is structured around clear definitions (nonlinearity measure, CLF conditions) and aims to prove specific statements about suboptimality and stability.
- The empirical study covers multiple scenarios (linear systems, nonlinear systems, different mixing strategies) and reports large performance gaps.

## Weaknesses
### Major
1. **Unfair comparison in experiments.**  The main empirical claim that neural ensembles underperform linear ensembles by orders of magnitude is undermined because the linear ensembles are composed of *optimal* LQR controllers, while the neural ensembles are trained via gradient descent.  The observed gap could easily reflect suboptimal training or insufficient capacity of the neural policies rather than a fundamental property of neural *ensembles*.  A fair comparison would require both ensembles to be learned from data under identical optimization conditions, or both to be optimal given their policy classes.

2. **Limited scope of theoretical results.**  The theorems (1, 2, 3) are proved only for linear dynamical systems with quadratic costs (LQR setting).  Yet the paper’s title and abstract make broad claims about neural policy ensembles in general, including RL and MoE settings where optimal policies are often highly nonlinear.  The theory does not address whether the suboptimality persists when the optimal policy itself is nonlinear, which severely limits the paper’s claimed generality.

3. **Insufficient empirical detail for reproducibility.**  The paper does not specify neural network architectures, optimization hyperparameters, training lengths, or the exact procedure for tuning the neural ensembles.  Figures are low-resolution and captions are incomplete (e.g., “vadDerPol” appears as a domain name).  The appendix (containing proofs and experimental details) is referenced but not provided, making it impossible to verify the theoretical or empirical claims.

4. **Stability result is not novel for the claimed context.**  Theorem 2 shows that fast switching between stable subsystems can cause instability—a well-known phenomenon in switched linear systems and control theory.  The result is presented as a specific failure of neural ensembles, but the same instability would occur for linear ensembles if the weights vary sufficiently fast.  The paper does not demonstrate that the instability is inherently tied to nonlinearity.

### Minor
- The paper uses “neural policy ensemble” to mean a convex combination of neural network policies, but many practical ensembles use gating networks or MoE architectures with more complex mixing.  The analysis of “neural mixing” in Section 3.3 only considers non-convex weight combinations, not the actual mechanism of neural mixing.
- The empirical results for policy mixing (Figure 5) show that on Soft_Pendulum the neural non-convex mixer has a *higher* mean episode count than the linear convex mixer, but the paper focuses on cost increase.  The interpretation is ambiguous and the reported relative losses appear inconsistent with the bar plots (e.g., the Neural Non-Convex bar is taller than Linear Convex, yet relative loss is 464%).
- The paper does not discuss how the neural policies are trained to be stable or what guarantees they have; the stability experiment assumes each individual neural policy is stable, but no training method is provided to ensure this.

### Trivial
- Several typos in figure captions and variable names (e.g., “vadDerPol”, “Mid\_Nonlinear\_Oscillator”).
- Figures are referenced but their content is not well explained in the main text.

## Nice-to-Haves
- A detailed description of the neural network training procedure, including architecture, optimizer, and hyperparameter search.
- A controlled experiment where both linear and neural ensembles are learned from the same data using comparable optimization, with results showing whether neural ensembles still underperform.
- Discussion of when neural ensembles *can* outperform linear ensembles (e.g., when the optimal policy is nonlinear), and whether the theoretical suboptimality bound can be negative (i.e., neural can be better) under certain conditions.
- A clearer explanation of why the stability result is specific to neural ensembles and does not also apply to linear ensembles with time-varying weights.

## Novel Insights
None beyond the paper’s own contributions.  The observation that nonlinearity can break averaging benefits in control settings is not new, and the theoretical results are extensions of known LQR and switched-systems facts to the context of ensemble policies.  The paper does not provide a deeper understanding of when or why neural ensembles might still be beneficial despite these issues.

## Suggestions
- Revise the title and claims to reflect the actual scope: “Neural Policy Ensembles are Sub-Optimal for Linear Quadratic Control” would be more accurate.
- Redesign the experiments to ensure fair comparison: train both linear and neural ensembles from scratch using the same amount of data and optimization budget, and evaluate on the same metrics.
- Provide a proof outline or key lemmas in the main text instead of relying entirely on an inaccessible appendix.
- Include a discussion of related work on nonlinear control and neural control that has successfully used neural policies, and explain why the findings here do not contradict those results.
- Improve figure quality and caption clarity; fix typographical errors.

## Score and Decision
MY FINAL SCORE: <score>3</score>  
MY FINAL DECISION: <decision>Reject</decision>