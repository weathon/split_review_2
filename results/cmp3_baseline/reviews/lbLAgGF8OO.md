## Summary

This paper introduces Dig-DEC, a new model-free decision-estimation coefficient that removes the optimism principle used in prior work and drives exploration purely through information gain (KL divergence and an additional divergence term). The authors show that Dig-DEC is always no larger than optimistic DEC and can be much smaller in some cases. They apply their framework to hybrid MDPs (stochastic transitions, adversarial rewards) with bandit feedback, obtaining the first model-free regret bounds for hybrid bilinear classes and Bellman-complete coverable MDPs under linear reward. Additionally, they improve online function estimation procedures, achieving better regret rates in both average and squared error settings.

## Strengths

- **Novel theoretical framework**: The paper introduces a principled way to remove optimism from the DEC framework, replacing it with information-gain terms. This is a conceptually clean approach that unifies and extends previous DEC-based methods.
- **First model-free bounds for hybrid MDPs with bandit feedback**: The paper resolves an open problem from [LWZ25] by providing the first model-free regret bounds in this setting, which is a significant contribution.
- **Improved regret rates**: The refined online estimation procedures yield better T-dependence in several settings (e.g., √T for Bellman-complete MDPs, matching optimism-based approaches).
- **Elegant analysis**: The use of Bregman divergence and mirror descent to handle general divergence measures is technically sound and provides flexibility for future extensions.

## Weaknesses

### Fatal
- **Critical inconsistency in reported regret bounds**: The abstract claims improvements from T^{3/4} to T^{3/5} (on-policy) and T^{5/6} to T^{7/8} (off-policy), while the introduction claims improvements from T^{3/2}/T^{5/8} to T^{3/2}/T^{5/6}, and the main results tables (e.g., Table 1) show T^{2/3} rates. These numbers are mutually incompatible and make it impossible to determine the actual claimed improvements. This inconsistency undermines the credibility of the paper's core claims.

### Major
- **No discussion of computational tractability**: Algorithm 1 requires solving a minimax optimization over distributions (Δ(Π) and Δ(Ψ)), which is likely computationally intractable for large policy or model classes. The paper does not address this practical limitation, which is a significant concern for the applicability of the framework.
- **Strong assumptions limit generality**: Assumption 3 (unique reward-to-value mapping given φ) and Assumption 4 (linear reward with known features) are quite restrictive. While the paper acknowledges some limitations, the scope of the results is narrower than the title and abstract suggest.

### Minor
- **Comparisons relegated to appendix**: The detailed comparison tables with prior work are in the appendix, making it hard for readers to assess the improvements without flipping back and forth.
- **Toy example is too simple**: Theorem 14 uses a 3-armed bandit to demonstrate improvement over optimistic DEC. While illustrative, a more complex MDP example would be more convincing.

### Trivial
- None.

## Nice-to-Haves

- A discussion of how the minimax optimization in Algorithm 1 could be approximated or solved efficiently for specific function classes.
- Empirical validation on small MDPs to demonstrate that the theoretical improvements translate to practice.

## Novel Insights

The paper's key insight is that optimism is not necessary for model-free DEC; information gain alone (via KL regularization and an additional divergence) can achieve comparable or better complexity bounds while also enabling extension to adversarial settings. The use of Bregman divergence to unify the analysis of different divergence measures is a nice technical contribution that may facilitate future work.

## Suggestions

- Resolve the inconsistency in the reported regret bounds across the abstract, introduction, and tables. Ensure all numbers are consistent and clearly explained.
- Add a discussion of computational complexity and potential relaxations of the minimax step.
- Move the comparison tables from the appendix to the main text to improve readability.

## Score and Decision

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>