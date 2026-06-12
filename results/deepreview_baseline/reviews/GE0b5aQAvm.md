## Summary

This paper claims to prove that neural network policy ensembles are fundamentally sub-optimal compared to linear policy ensembles in control settings. The authors develop a theoretical framework analyzing sub-optimality, stability violations, and non-convex mixing penalties, and provide empirical validation on linear and nonlinear dynamical systems. The paper argues that nonlinear function approximators are inherently unsuitable for ensemble control methods, with implications for RL, MoE, and agentic AI.

## Strengths

- The paper tackles an important and timely question about the fundamental limitations of neural policy ensembles, which has broad implications across RL, control, and LLM applications.
- The theoretical framework attempts to formalize intuitive differences between ensemble classifiers and ensemble policies, particularly around temporal coupling and error amplification.
- The empirical study covers multiple aspects (performance, stability, diversity, mixing) across different dynamical systems, providing a reasonably comprehensive evaluation.

## Weaknesses

### Fatal

1. **The core theoretical claims are not properly proven.** Theorem 1 states that under certain conditions, the neural ensemble is sub-optimal compared to the linear ensemble, but the conditions themselves (diversity, nonlinearity, sufficient complexity) are defined in terms of the neural policies' deviation from linearity. This is essentially assuming what needs to be proven—if neural policies are sufficiently nonlinear and diverse, they perform worse than linear ones. The theorem does not establish that neural ensembles are *inherently* sub-optimal; it only shows that under specific conditions favoring linearity, linear ensembles perform better. The proof is not provided in the main text, and the conditions are so restrictive (e.g., requiring L_f * κ_0 * δ > ρ) that they may not hold for well-designed neural ensembles.

2. **Theorem 2 (stability violation) has a critical logical flaw.** The theorem states that if ensemble weights vary with rate β > (min_i α_i)/(2 max_i ||V_i||_∞), then the ensemble can be unstable. However, this is a statement about *time-varying* convex combinations of stable systems, not about neural nonlinearity. The same instability would occur for time-varying linear ensembles with the same weight variation rate. The theorem does not establish any unique instability property of neural ensembles—it conflates temporal variation of weights with nonlinearity of the constituent policies. This fundamentally undermines the paper's central claim about neural-specific sub-optimality.

3. **The empirical validation does not support the theoretical claims.** The experiments compare neural ensembles against LQR ensembles, but the neural networks are trained with gradient descent while LQR controllers are computed analytically via Riccati equations. This is an unfair comparison—the LQR solution is globally optimal for linear systems with quadratic costs, while the neural network is trained with a local optimization method. The observed performance gap could be entirely due to optimization difficulty rather than any fundamental property of neural ensembles. A proper test would compare neural ensembles against neural networks trained to approximate the optimal linear solution, or compare both methods under identical training conditions.

### Major

4. **The paper's title and abstract make sweeping claims that are not supported by the actual results.** The claim that "neural policy ensembles are sub-optimal" is presented as a universal statement, but the theoretical results only apply under specific conditions (linear systems, quadratic costs, particular diversity/nonlinearity thresholds). The paper does not address nonlinear systems where neural policies might have an advantage, nor does it consider the many successful applications of neural policy ensembles in the literature.

5. **The experimental methodology has serious issues.** The neural ensemble uses learned weights via Bayesian updates, while the linear ensemble uses fixed weights. The neural network architecture, training procedure, and hyperparameter tuning are not described in sufficient detail. The "2 orders of magnitude" claim in the abstract is not supported by the actual results (Figure 1 shows costs of 432 vs 234, which is less than 2x, not 100x). The statistical significance claims (p < 10^-5) are stated without proper justification of the test used.

6. **The paper misrepresents the relationship to existing work.** The claim that "classical adaptive control theory... doesn't extend to neural networks" ignores a large body of work on neural adaptive control, Lyapunov-based neural control, and learning-based control with stability guarantees. The paper does not engage with the substantial literature on neural network controllers that do provide stability and optimality guarantees under appropriate conditions.

### Minor

7. **The definition of the nonlinearity measure (Definition 10) is problematic.** It measures deviation from linearity but is normalized by ||x - y||, which means it can be arbitrarily large or small depending on the domain scaling. The condition κ_0 > 0 is essentially always true for any nonlinear function, making the theorem's conditions almost tautological.

8. **The empirical results for policy mixing (Figure 5) are confusing and partially contradictory.** For the Soft Pendulum system, the neural non-convex mixing actually performs *better* than linear convex mixing (higher mean episode count), which contradicts the paper's claims. The authors acknowledge this but dismiss it as "variability" without proper analysis.

### Trivial

9. The paper uses "vadDerPol" in the text (Section 5.1) which appears to be a typo for "van der Pol."

## Nice-to-Haves

- A comparison of neural ensembles against neural networks trained to approximate the optimal linear solution would help isolate whether the issue is nonlinearity or optimization.
- Analysis of whether the sub-optimality gap decreases with more sophisticated neural network training (e.g., using RL rather than supervised learning) would strengthen the claims.
- Discussion of known successful neural ensemble methods (e.g., in robotics, game playing) and how they relate to the theoretical framework would improve contextualization.

## Novel Insights

None beyond the paper's own contributions. The paper's core insight—that temporal coupling in dynamical systems breaks the variance-reduction benefits of ensemble averaging—is not new and has been discussed in the adaptive control and reinforcement learning literature. The specific theoretical framework and empirical comparisons are the paper's claimed contributions, but the fatal flaws in the theoretical proofs and experimental methodology prevent any genuinely novel insight from emerging.

## Suggestions

1. Reconsider the theoretical framework: the current theorems essentially assume the conclusion. A proper proof would need to show that neural ensembles are sub-optimal *without* assuming conditions that directly imply linearity is better.
2. Fix the stability theorem: either show that the instability is unique to neural (nonlinear) ensembles, or acknowledge that the same issue affects time-varying linear ensembles.
3. Redesign the experiments to provide a fair comparison: train both linear and neural controllers using the same optimization procedure, or compare neural ensembles against neural networks that approximate the optimal solution.
4. Tone down the claims: the paper would be more credible as a study of specific limitations under particular conditions rather than a universal statement about neural ensemble sub-optimality.

## Score and Decision

The paper addresses an important question and has an ambitious scope, but the theoretical results are not properly established (the theorems either assume their conclusions or conflate different issues), and the empirical methodology does not support the strong claims made. The fatal flaws in the core theoretical arguments and the unfair experimental comparisons invalidate the paper's main contributions. The paper would need substantial revision to address these issues.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>