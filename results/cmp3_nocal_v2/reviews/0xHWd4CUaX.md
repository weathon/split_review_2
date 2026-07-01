## Summary

This paper proposes integrating contrastive pre-training of code graph embeddings with reinforcement learning for automated code refactoring. The method uses a syntax-guided contrastive encoder to learn structural representations of code, a composite reward function combining traditional metrics with embedding dynamics and semantic preservation checks, and a graph attention policy network trained with PPO. Experiments on refactoring benchmarks show improvements over rule-based, learning-based, and RL-based baselines.

## Strengths

- **Ablation study (Table 2).** The paper systematically removes four components (contrastive pre-training, embedding rewards, semantic tests, random exploration) and reports their effect on three metrics. Each component contributes non-trivially, providing the clearest evidence for the method's design choices.
- **Correlation analysis between embedding dynamics and SI (Figure 2).** The reported Pearson's r=0.72 provides some empirical support linking latent-space movement to code quality improvement, going beyond raw benchmark reporting.

## Weaknesses

### Fatal

1. **The RL MDP is never defined.** The paper claims to formulate code refactoring as an MDP (Section 3.1) but never specifies: (a) what the actions are — the action space is described only as "possible refactorings" with zero enumeration of specific transformations (e.g., extract method, rename variable); (b) how the code transitions between states after an action is taken; (c) how the attention weights from the policy network (Equation 7) map to concrete code transformations. The policy network produces attention weights over graph nodes, but the mechanism by which these select a refactoring action is never explained. Without the MDP definition, the method is non-reproducible and the experimental results cannot be properly interpreted. (Verified from Sections 3.1, 4.4, and the absence of any action specification anywhere in the paper.)

### Major

1. **No statistical significance or variance reported.** All results in Tables 1, 2, and 3 are point estimates with no standard deviations, confidence intervals, or significance tests. In an RL setting where training is notoriously high-variance, the reader cannot determine whether the reported improvements over baselines (e.g., SI 79.4→83.7, SP 90.5→93.8) are meaningful or within noise. The ablation study (Table 2) suffers from the same issue. (Verified from all tables in the paper.)

2. **Central claim about reducing expert demonstrations is never tested.** The paper repeatedly asserts that a key advantage is reducing reliance on expert demonstrations (Sections 1, 4, 7), yet no experiment directly tests this. There is no controlled comparison between the proposed method with and without expert demonstrations. The baselines that use expert demonstrations (GraphRL, NeuroRefactor) are entirely different systems, not controlled variants of the same framework. This central motivational claim is asserted but unsubstantiated. (Verified from lines 21, 91, 328 — claims present, no corresponding experiment.)

3. **Citation mismatch for a key baseline.** GraphRL is described as "GNN policy with expert demonstrations" (Section 5.1, line 203) but the cited reference (Darvari et al., 2024) is titled "Graph reinforcement learning for combinatorial optimization: A survey and unifying perspective" — a survey paper with no apparent connection to GNN-based code refactoring with expert demonstrations. This undermines confidence in how baselines are characterized. (Verified from line 203 vs. lines 347-349.)

### Minor

1. **Cross-language evaluation is not truly zero-shot and comparison is limited.** The paper states the model is "trained over a Java language codebase (CodeSearchNet)" (line 266), but CodeSearchNet contains 2 million functions across 6 programming languages including Python (line 175). The model thus saw Python data during pre-training, undermining the claim of zero-shot transfer. Additionally, comparison on Python and C++ is only against rule-based tools (PyLint, Cppcheck), not against any learning-based baselines, making the comparison less informative. (Verified from lines 175, 266, and Table 3.)

2. **BigCloneBench usage is unexplained.** BigCloneBench is a clone detection benchmark listed among evaluation datasets (line 173), but the paper never explains how a clone detection dataset is used to evaluate refactoring quality. The GS metric ("Generalization Score") is described as "performance on unseen project types (cross-validation)" but no details connect this to the dataset or explain how refactoring metrics are computed on it. (Verified from lines 173-174 and lines 217-218.)

3. **Symbolic execution overhead is not discussed.** The semantic preservation mechanism uses symbolic execution for test case generation (Section 4.5), which is computationally expensive and prone to path explosion. With 1M environment steps reported in training, the feasibility and cost of this component are never addressed. (Verified from Section 4.5 and line 226.)

4. **The embedding dynamics reward term has a conceptually problematic sign.** The term `α tanh(β Δh_t)` positively rewards the magnitude of embedding space movement (`Δh_t = ||h_t - h_{t-1}||₂`), which incentivizes large changes rather than directly incentivizing quality improvement. While Figure 2 shows a correlation between Δh and SI, the reward directly optimizes Δh rather than quality. The semantic preservation penalty partially constrains this, but the reward structure remains an indirect proxy. (Verified from Equation 5 and surrounding text in Section 4.2.)

### Trivial

- None.

## Nice-to-Haves

- A hyperparameter sensitivity analysis for the reward weights (w_q, α, β, γ) and temperature τ would strengthen confidence in the method's robustness.
- The paper would benefit from explicitly listing the set of atomic refactoring actions and how they are parameterized.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Grammar/writing quality and typos ("lemon deep learning", broken abstract sentence, etc.):** Removed per the hard rule against formatting/writing nitpicks.
- **Missing references from bibliography:** The parser stripped the remainder of the reference list (noted at line 386). Removed per the hard rule about parser-stripped content.
- **No public code/data release mentioned:** Removed per the hard rule about release-status criticism.
- **LLM use disclosure (Section 8):** Removed per the hard rule against writing/formatting criticisms.
- **Cross-language experiment listed as a strength:** Removed because it conflicts with a verified weakness (non-zero-shot, limited comparison). Per the rules, the weakness wins.

## Novel Insights

None beyond the paper's own contributions. The review surface reveals that the paper's evaluation is structurally incomplete (undefined MDP) and lacks basic statistical rigor, making it impossible to assess the validity of the claimed results. The contrastive pre-training component and the ablation study show promise, but the fundamental underspecification of the RL framework prevents meaningful evaluation.

## Suggestions

1. **Define the MDP completely.** Specify the atomic refactoring actions (discrete list), how the code transitions between states, how the policy network's attention weights select specific actions, and how invalid/partial states are handled. Without this, the method is not reproducible.
2. **Report variance across multiple seeds.** Run all experiments with at least 5 independent seeds and report means with standard deviations. This is standard practice for RL papers.
3. **Test the expert-demonstration reduction claim directly.** Construct a controlled experiment comparing the proposed method against a version augmented with expert demonstrations (e.g., behavioral cloning pre-training or reward shaping from expert traces).
4. **Clarify the cross-language evaluation.** Specify which subset of CodeSearchNet is used for pre-training, and add learning-based baselines on Python and C++ for fair comparison.
5. **Explain how each dataset (especially BigCloneBench) is used to compute each metric.**

## Score and Decision

The paper proposes a sensible combination of contrastive pre-training and RL for code refactoring, and the ablation study provides some evidence that each component contributes. However, the paper has a fatal flaw: **the RL MDP is never defined** — the action space, state transitions, and policy-to-action mapping are all unspecified. Without this, the method is not reproducible and the experimental results cannot be properly interpreted. Combined with the lack of statistical rigor, an untested central claim (about reducing expert demonstrations), and citation issues, the paper cannot be accepted in its current form.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>