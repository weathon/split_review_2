## Summary
This paper introduces Dig-DEC, a new model-free decision-estimation coefficient that replaces the optimism principle of prior work with pure information-gain-driven exploration. Dig-DEC is always no larger than optimistic DEC and can be strictly smaller. The authors apply their framework to hybrid MDPs (stochastic transitions, adversarial rewards) and obtain the first model-free regret bounds with bandit feedback, resolving an open problem from LWZ25. They also improve the online function estimation procedures, achieving better regret rates for both average and squared estimation error settings.

## Strengths
- **Conceptual novelty**: Removing optimism from the DEC framework and driving exploration purely via information gain is a principled contribution. The resulting Dig-DEC is provably no larger than optimistic DEC and can be arbitrarily smaller in constructed examples (Theorem 14).
- **Resolves an open problem**: The paper provides the first model-free regret bounds for hybrid MDPs with bandit feedback under linear rewards and several general transition structures, directly addressing a gap left by LWZ25.
- **Improved regret rates**: The refined online estimation procedures yield concrete improvements—e.g., from \(T^{3/4}\) to \(T^{3/5}\) in the on-policy average estimation case and from \(T^{5/6}\) to \(\sqrt{T}\) in the Bellman-complete squared error case.
- **Unifying framework**: The general Algorithm 1 with divergence \(D\) recovers previous AIR/XZ23 and LWZ25 results cleanly, demonstrating flexibility beyond the KL-based posterior update.

## Weaknesses
### Fatal
None.

### Major
- **Inconsistent exponent claims**: The abstract states an improvement from \(T^{5/6}\) to \(T^{7/8}\) for the off-policy average estimation error. \(T^{7/8}\) is a worse rate than \(T^{5/6}\), contradicting the claimed improvement. Moreover, the concrete bounds in Table 1 (e.g., \(T^{2/3}\)) do not align with the abstract’s \(T^{3/5}\) and \(T^{7/8}\). This inconsistency undermines the clarity of the paper’s results and must be corrected.
- **Limited evaluation of assumptions**: Assumptions 3 and 4 (unique reward-to-value mapping, known linear reward features) restrict the generality of the hybrid-setting results. The paper acknowledges that some important cases (e.g., unknown reward features in low-rank MDPs) remain out of reach, but the discussion of how broad the remaining coverage is could be more thorough.

### Minor
- **Not truly “model-free” in the computational sense**: The paper clarifies that “model-free” only refers to regret bounds independent of \(|\mathcal{M}|\); the learner still has access to the full model class and may face computational challenges. This is consistent with prior work but could be misleading without the explicit caveat.
- **Suboptimal rates in some hybrid subcases**: The hybrid regret bounds (Table 2) include exponents like \(T^{3/2}\) and \(T^{13/8}\), which are far from the \(\sqrt{T}\) rates achievable in the stochastic setting or in certain full-information hybrid algorithms. The paper does not discuss whether these rates are optimal or improvable.

### Trivial
- Some notation (e.g., the bold subscript in \(\nu_\phi(\cdot|\pi,o)\)) is explained in a footnote but could be made clearer in the main text.

## Nice-to-Haves
- Provide lower bounds or optimality discussions for the hybrid setting to contextualize the achieved rates.
- Extend the hybrid results to settings with unknown reward features (as done by LMWZ24) or relax Assumption 3.

## Novel Insights
The paper’s key insight is that optimism—a common heuristic for exploration—can be entirely replaced by an information-gain penalty (KL divergence) within the DEC framework, while still recovering or improving prior bounds. This removal of optimism is crucial for handling adversarial rewards without explicit reward estimators, because the reward can be absorbed into the value function estimation via the divergence term. The connection between regularization and information gain (the two components of the KL term) offers a new perspective on why model-free exploration works.

## Suggestions
- Correct the exponent inconsistencies in the abstract and ensure alignment with the bounds reported in the main tables.
- Add a brief discussion on the computational tractability of the minimax optimization in Algorithm 1.

## Score and Decision
I view this as a strong theoretical paper with a novel concept and significant applications. Despite the clarity issues in the abstract, the core contributions are sound and advance the state of the art. I recommend acceptance.

MY FINAL SCORE: <score>6.5</score>  
MY FINAL DECISION: <decision>Accept</decision>