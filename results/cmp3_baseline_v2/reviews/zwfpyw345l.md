## Summary

The paper proposes a hierarchical attention model for code embeddings used as state representations in reinforcement learning. The model combines token-level, function-level, and module-level attention with graph-structured dependencies (AST and code dependency graph). The authors evaluate on three code-related RL tasks (code completion, program repair, algorithmic problem solving) and report improvements over several baselines.

## Strengths

- The idea of multi-level hierarchical attention for code is conceptually reasonable and addresses a genuine need in code representation learning.
- The ablation study (Table 2) provides some evidence that each component contributes to overall performance.
- The paper attempts to integrate both sequential and graph-based attention mechanisms, which is a plausible direction.

## Weaknesses

### Fatal

1. **Insufficient clarity and rigor in method description.** The equations (1)–(8) are presented without proper explanation of notation, dimensions, or how they interact. The integration of transformer and GAT layers is described only at a high level; critical details (e.g., how token-level representations are aggregated into function-level, how the CLS token is trained, how the CDG is constructed) are missing. The paper does not provide enough information to reproduce the method.

2. **Inadequate experimental validation.** The RL tasks are not fully specified: the MDP formulation, action space, reward function, and environment dynamics are not described. The baselines are weak—no comparison to state-of-the-art code models such as GraphCodeBERT, CodeT5, or PLBART. Results are reported without error bars, confidence intervals, or statistical significance tests (the paper mentions paired t-tests but does not report p-values or standard deviations). The sample efficiency claim is not supported by quantitative analysis.

3. **Suspicious or incorrect references.** The paper cites “Gomez et al., 2025” (a future year), “Cui, 2024” for the APPS benchmark (which is actually from Hendrycks et al., 2021), and several other references that appear fabricated or irrelevant. This undermines the credibility of the paper.

4. **Lack of reproducibility.** No code, data splits, or hyperparameter details are provided. The training protocol (warm-up with demonstration trajectories) is mentioned but the source of demonstrations is not specified. The paper cannot be independently verified.

### Major

- The paper does not adequately discuss or compare with existing hierarchical code representation methods (e.g., SG-Trans, Tree-structured transformers, Hoppity). The claim that prior work does not optimize for RL objectives is weak—many works fine-tune code representations for downstream tasks.
- The evaluation metrics are poorly defined (e.g., “CodeBLEU score (?)” with a question mark). The code quality metrics (compilation success, test pass rate) are not clearly tied to the RL reward.
- The scalability analysis (Figure 3) is vague: “Baseline 1” and “Baseline 2” are not identified, and the prediction error metric is not defined.
- The paper admits using an LLM to polish writing, but the overall quality remains poor, with many unclear sentences and logical gaps.

### Minor

- The paper contains numerous grammatical errors and awkward phrasing (e.g., “hierarchical cherry-picking of the code embedding system” in the conclusion).
- Figure 1 is referenced but not explained in sufficient detail; the flow of information is unclear.
- The related work section is disjointed and does not clearly position the contribution.

### Trivial

- Some equations have formatting issues (e.g., missing parentheses, inconsistent notation).

## Nice-to-Haves

- A clear diagram showing how the three attention levels interact with the RL policy and value network.
- An analysis of computational cost (FLOPs, memory) compared to baselines.
- A discussion of why the proposed method outperforms CodeBERT despite CodeBERT being pre-trained on a large corpus.

## Novel Insights

None beyond the paper’s own contributions. The paper does not provide any theoretical analysis or surprising empirical findings that would fundamentally change understanding of code representation or RL.

## Suggestions

1. Provide a complete and precise description of the hierarchical attention mechanism, including all equations with clear notation and dimensions.
2. Fully specify the RL environment for each task: state space, action space, reward function, episode length, and termination conditions.
3. Compare against stronger baselines (e.g., GraphCodeBERT, CodeT5, TreeGAT) and report results with standard deviations over multiple seeds.
4. Release code and data splits to ensure reproducibility.
5. Remove or correct suspicious references; ensure all citations are accurate and relevant.
6. Improve the writing for clarity and correctness.

## Score and Decision

**Score:** 3

**Decision:** Reject

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>