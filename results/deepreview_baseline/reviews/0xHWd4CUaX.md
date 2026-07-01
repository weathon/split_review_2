## Summary

The paper proposes a reinforcement learning (RL) framework for automated code refactoring that uses contrastive pre-training on code graphs to learn representations of code quality. These learned embeddings are combined with traditional code metrics in a composite reward function, and a graph attention policy network operates on the joint representation space. The method is evaluated on three refactoring datasets and compared against rule-based, learning-based, and RL-based baselines, showing improvements across several metrics.

## Strengths

- **Relevant and timely problem**: Automated code refactoring is an important area in software engineering, and the use of self-supervised learning to reduce reliance on handcrafted rewards is a sensible direction.
- **Modular framework design**: The separation into contrastive pre-training, composite reward, and graph attention policy allows for potential component swaps and future extensions.
- **Ablation and cross-language experiments**: The ablation study (Table 2) isolates the contribution of each component, and the cross-language generalization experiment (Table 3) provides evidence of transferability beyond the training language.

## Weaknesses

### Major

1. **Poor clarity and insufficient technical detail**: The writing is often unclear and contains garbled sentences (e.g., abstract: “something that necessarily requires the existing RL approaches to accomplish and that most often do last year because of the handcrafted nature of their metrics”). Key technical components are described at a high level without enough precision to reproduce the method. For example:
   - The action space of the RL agent is never explicitly defined (what refactoring operations are available? how are they parameterized?).
   - The contrastive augmentations (subtree masking, edge rewiring, identifier shuffling) are mentioned but not specified in a way that guarantees program validity.
   - The policy network (Equation 7) computes attention weights, but how these weights translate into concrete refactoring actions is unclear.
   - The exploration strategy (Equation 6) is introduced but not evaluated in the ablation study, leaving its contribution unverified.

2. **Weak experimental validation and baseline selection**: The baselines include several methods that are either obscure, not peer-reviewed, or potentially outdated (e.g., RLRefactor, GraphRL, NeuroRefactor). The paper does not provide sufficient details about these baselines (e.g., hyperparameters, training setup) to ensure a fair comparison. The reported improvements over the strongest baseline (NeuroRefactor) are modest (SI: +4.3%, SP: +3.3%, MG: +3.3%, GS: +5.2%) and no statistical significance or variance is reported. The cross-language comparison only pits the method against rule-based tools (PyLint, Cppcheck), not against other learning-based approaches that could transfer across languages.

3. **Unclear justification for the embedding dynamics reward**: The composite reward includes a term based on the magnitude of latent space movement (Δh_t). The paper states this “means that the gradients propagate in a stable way during RL training” but does not explain why moving in embedding space is a meaningful signal for refactoring quality. The ablation study shows that removing this term hurts performance, but the mechanism remains opaque.

4. **Missing MDP formulation**: The paper does not formally define the Markov Decision Process for the refactoring task. The state space, action space, transition dynamics, and reward function are not fully specified, which is a critical omission for an RL paper.

### Minor

- The semantic preservation component (Section 4.5) relies on symbolic execution to generate test cases, which is computationally expensive and may not scale to large codebases. The paper does not discuss the cost or limitations of this component.
- The paper claims “enormous improvement” in the conclusion, but the experimental results show only incremental gains.
- The references include several entries with future years (2025) that appear to be technical reports from non-peer-reviewed sources, raising concerns about the reliability of the baselines.

### Trivial

- The paper states “We use LLM polish writing based on our original paper” in Section 8, which is acceptable but the writing still has significant clarity issues.

## Nice-to-Haves

- A formal definition of the MDP (states, actions, transitions) would greatly improve reproducibility.
- Comparison with more recent pre-trained code models (e.g., CodeBERT, GraphCodeBERT) fine-tuned for refactoring would strengthen the experimental evaluation.
- An analysis of the computational cost of the symbolic execution component and its impact on scalability.

## Novel Insights

None beyond the paper’s own contributions. The idea of using contrastive learning to learn refactoring-aware embeddings is novel, but the paper does not provide deeper theoretical or empirical insights into why this works or under what conditions it fails.

## Suggestions

- Rewrite the paper with clear, precise language. Define all components of the RL framework (state, action, transition, reward) explicitly.
- Provide more details on the contrastive augmentations and how program validity is maintained.
- Include statistical significance tests (e.g., confidence intervals) for the main results.
- Compare against stronger, well-established baselines (e.g., fine-tuned CodeBERT, GraphCodeBERT) and include learning-based cross-language transfer methods.
- Evaluate the contribution of the exploration strategy (Equation 6) in the ablation study.
- Discuss the limitations of the symbolic execution component and potential alternatives.

## Score and Decision

**Score**: 3  
**Decision**: Reject

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>