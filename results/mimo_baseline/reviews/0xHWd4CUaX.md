## Summary

This paper proposes a framework for automated code refactoring that combines contrastive pre-training of code graph embeddings with reinforcement learning. The approach uses syntax-preserving augmentations to learn structural code representations, then integrates these embeddings with traditional code quality metrics in a composite reward function for a graph attention-based RL policy. Experiments on Java and Python datasets show improvements over rule-based, learning-based, and RL baselines across syntactic improvement, semantic preservation, and generalization metrics.

## Strengths

- **Reasonable architectural design:** The combination of contrastive pre-training on code graphs with RL fine-tuning is a sensible approach to reduce dependence on handcrafted reward functions, and the modular three-phase pipeline (pre-train → RL fine-tune → inference) is clean.
- **Ablation study provides component attribution:** Table 2 shows that contrastive pre-training contributes the largest gains (−7.5% SI when removed), followed by semantic tests (−8.6% SP), offering useful insight into the system's design choices.
- **Cross-language evaluation:** Testing a Java-trained model on Python and C++ without fine-tuning (Table 3) is a worthwhile experiment for assessing representation quality, even if the comparison conditions are limited.

## Weaknesses

### Fatal

None.

### Major

- **Critical missing RL environment specification:** The paper never concretely defines the action space (what refactoring actions the agent can take), state transition dynamics, or how the environment provides states and rewards at each timestep. For an RL paper, these are foundational details—without them, the results cannot be understood, reproduced, or evaluated. Section 4.6 mentions PPO and 1M environment steps, but the MDP formulation (S, A, P, R, γ) introduced in Section 3.1 is never instantiated for the refactoring domain.

- **Unfair cross-language comparison (Table 3):** The generalization experiment compares the proposed method only against rule-based tools (PyLint, Cppcheck) rather than the learning-based and RL baselines from Table 1. This inflates the perceived advantage—learning-based methods like GraphRL or NeuroRefactor may also generalize across languages. The claim of "out-performing language-specific rule-based tools" is trivially expected for a learned method.

- **No statistical significance or error bars:** All results in Tables 1–3 and Figure 1 are reported as single point estimates. Given the relatively close margins between some baselines (e.g., NeuroRefactor: 79.4% SI vs. Ours: 83.7% SI), it is unclear whether differences are statistically significant. Standard practice requires reporting confidence intervals or conducting significance tests, especially for stochastic RL methods.

### Minor

- **Questionable scalability of semantic preservation (Section 4.5):** The method claims to use "symbolic execution" for generating test cases, described as "lightweight." In practice, symbolic execution is notoriously expensive and does not scale to large codebases or complex data structures. This contradicts the scalability claims in Section 6.3 and undermines the practicality of the semantic preservation mechanism.

- **Figure 3 interpretation is unclear:** The stacked area chart shows "proportion" of reward components summing to 1.0, but Equation 5 defines the reward as a sum, not a normalized mixture. The figure appears to show relative magnitudes after some unexplained normalization, making its interpretation ambiguous. The claim that "traditional metrics guide initial improvements" while "embedding dynamics become increasingly important" is interesting but not supported by the formal reward specification.

- **Reward component design needs more justification:** The use of tanh(β·Δh_t) as a reward signal (Equation 5) encourages large embedding-space movements, but it is unclear why this correlates with refactoring quality. Figure 2 shows a positive correlation (r=0.72), but this is an observational analysis, not a causal argument—large embedding changes could also correspond to undesirable code mutations.

- **Contrastive augmentation semantics:** "Subtree masking" (randomly removing AST subtrees while maintaining program validity) is non-trivial—determining which subtrees can be removed while preserving validity requires sophisticated static analysis that is not described.

## Nice-to-Haves

- A concrete specification of the action space (e.g., extract method, inline variable, move method) and how many actions are available per state would substantially strengthen the paper.
- Comparison of cross-language generalization against the learning-based baselines, not just rule-based tools.
- Discussion of how the method handles multi-file or project-level refactoring scenarios.

## Novel Insights

The paper's most interesting empirical observation is the shift in reward component dominance over refactoring stages (Figure 3, if taken at face value): early-stage refactoring is driven by coarse code quality metrics while later stages rely more on embedding-space guidance. This suggests a natural curriculum-like property where learned representations capture fine-grained optimization patterns that traditional metrics miss. However, this observation is not formally analyzed or leveraged in the training procedure (e.g., through scheduled reward weighting), which would have been a compelling methodological contribution.

## Suggestions

- Add a complete MDP specification: enumerate the refactoring action set, describe state representation construction, and detail how transitions are simulated.
- Report confidence intervals (e.g., over 5+ random seeds) for all experimental results.
- Add learning-based baselines to the cross-language experiment in Table 3.
- Clarify or remove the stacked area chart (Figure 3) unless the normalization procedure and its relationship to the actual reward (Equation 5) are explicitly explained.
- Provide concrete evidence that the symbolic execution-based semantic preservation scales (e.g., runtime measurements, or replace with a lighter-weight equivalence check).

## Score and Decision

The paper presents an interesting direction combining contrastive pre-training with RL for code refactoring, but the evaluation has significant gaps: the RL environment is underspecified, comparisons lack statistical rigor, and the cross-language evaluation uses unfairly weak baselines. These issues prevent confident assessment of whether the method's improvements are genuine and reproducible.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>