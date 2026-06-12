## Summary
This paper introduces Dig-DEC, a new model-free decision-estimation coefficient that removes the optimism principle from prior work and drives exploration purely through information gain. The authors show that Dig-DEC is always no larger than optimistic DEC and can be much smaller in special cases. The removal of optimism allows the framework to handle adversarial environments without explicit reward estimators, yielding the first model-free regret bounds for hybrid MDPs with bandit feedback under linear reward and several general transition structures. The paper also improves online function estimation procedures, achieving better regret rates than prior work in both average and squared estimation error settings.

## Strengths
- **Novel theoretical framework**: The introduction of Dig-DEC that removes optimism and relies purely on information gain is a conceptually clean and principled advance. The framework unifies and generalizes prior AIR-based approaches while simplifying the analysis.
- **Significant technical contributions**: The paper resolves the main open problem from [LWZ25] by establishing the first model-free regret bounds for hybrid MDPs with bandit feedback. The improvements in online function estimation (from T^{3/4} to T^{3/5} and from T^{5/6} to sqrt{T}) are substantial and technically non-trivial.
- **Broad applicability**: The framework handles multiple canonical settings (bilinear classes, Bellman-Eluder dimension, coverability) in both stochastic and hybrid environments, demonstrating its generality. The ability to match optimism-based approaches in Bellman-complete MDPs for the first time is a notable achievement.
- **Rigorous theoretical development**: The paper provides careful definitions, clear assumptions, and a well-structured analysis. The connection to mirror descent and the flexible divergence framework are elegant contributions.

## Weaknesses

### Major
- **Assumption 3 is restrictive**: The requirement that transitions inducing the same value function under a given policy must be grouped together, while reasonable, does not capture all learnable hybrid MDPs. The authors acknowledge this limitation (e.g., low-rank MDPs with unknown reward features), but this significantly narrows the scope of the claimed "first model-free bounds for hybrid MDPs." The paper would benefit from a clearer discussion of which practically relevant MDP classes satisfy this assumption and which do not.
- **Computational tractability is not addressed**: The paper explicitly states that "model-free" does not imply computational efficiency, but the algorithms require solving minimax optimization problems over potentially large spaces (Δ(Π) and Δ(Ψ)). For any non-trivial MDP, these spaces are enormous, and the paper provides no discussion of how these optimization problems could be solved efficiently or approximated. This is a significant gap between theory and practice.
- **The toy example (Theorem 14) is a 3-armed bandit**: While the example demonstrates a separation between Dig-DEC and optimistic DEC, bandits are a very special case of the DMSO framework. The claim that "the improvement can be arbitrarily large" is supported only by this simple example. It would be more convincing to show a non-trivial MDP instance where the improvement is substantial.

### Minor
- **The paper is dense and notation-heavy**: While this is common in theoretical work, the exposition could benefit from more intuitive explanations of key concepts (e.g., the role of each term in the divergence measure, the intuition behind the two-timescale procedure). The current presentation may limit accessibility.
- **The comparison with prior work in the main text is somewhat limited**: The key comparison with optimistic DEC is given in Theorem 13, but the bound includes an additive η term, and the relationship between the two measures could be discussed more thoroughly. The tables in the appendix are helpful but the main text could provide more interpretation.

### Trivial
- The abstract mentions "T^{3/2}/T^{5/8}" which appears to be a typo (likely T^{3/4}/T^{5/6} based on the introduction).

## Nice-to-Haves
- A discussion of computational approaches or approximations for the minimax optimization in Algorithm 1 would greatly enhance practical relevance.
- An explicit example of a non-trivial MDP where Dig-DEC strictly improves over optimistic DEC (beyond the bandit case) would strengthen the paper's claims.
- A more detailed comparison with the concurrent work [CR25] mentioned in the preliminaries would help position the contribution.

## Novel Insights
The key insight is that optimism is not necessary for model-free exploration in the DEC framework; information gain alone, properly structured through a carefully designed divergence measure, suffices. The decomposition of the KL term into regularization and information gain components provides a clean explanation of why Dig-DEC can match or improve upon optimistic DEC. The connection to mirror descent analysis, which allows flexible divergence choices beyond KL, is a methodological contribution that may enable future work to design problem-specific divergences. The improvement in online function estimation through unbiased estimators (splitting samples) and refined two-timescale procedures are technically interesting and may have independent applications.

## Suggestions
- Add a discussion of computational considerations for Algorithm 1, even if only to acknowledge the challenge and suggest potential approximation strategies (e.g., using online convex optimization or sampling-based methods).
- Provide at least one non-bandit MDP example where Dig-DEC strictly improves over optimistic DEC, or clarify why such examples are difficult to construct.
- Consider adding a "roadmap" section early in the paper to help readers navigate the dense notation and multiple settings.

## Score and Decision
The paper makes significant theoretical contributions to the DEC framework and resolves an open problem in hybrid MDPs. The technical improvements in regret bounds are substantial and the framework is elegant and general. However, the restrictive assumptions (particularly Assumption 3) and the lack of computational considerations temper the practical impact. The paper is clearly a strong theoretical contribution appropriate for ICLR.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>