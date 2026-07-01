## Summary

This paper proposes an RL-based automated code refactoring framework that combines contrastive pre-training of code graph embeddings with a composite reward function and a graph attention policy network. The key idea is to learn refactoring-aware code representations via self-supervised contrastive objectives on syntactically-augmented code graphs, thereby reducing reliance on handcrafted reward functions. Experiments are conducted on Java, Python, and C++ codebases against rule-based and learning-based baselines.

## Strengths

1. **Well-motivated problem.** The paper correctly identifies that handcrafted reward functions are a weakness of existing RL-based code refactoring approaches, and that learning refactoring-aware representations from unlabeled code could reduce this dependency. This is a genuine and timely problem.

2. **Clean modular architecture.** The three-part design — contrastive encoder, composite reward, graph attention policy — is presented in a way that makes the method easy to understand. The system operates in three distinct phases (pre-training, RL fine-tuning, inference) that are clearly separated.

3. **Ablation study included.** Table 2 provides component-level analysis that lets the reader see the effect of removing each piece (contrastive pre-training, embedding rewards, semantic tests, guided exploration), even though the interpretation is limited by missing variance estimates.

## Weaknesses

### Fatal

None.

### Major

1. **No measure of variance for any experimental result.** Every result in Tables 1, 2, and 3 is reported as a single number with no standard deviations, confidence intervals, or multiple seeds. PPO-based RL is notoriously sensitive to seed variation and environment stochasticity. Without variance estimates the reader cannot assess whether the reported differences (e.g., Ours 83.7% SI vs. NeuroRefactor 79.4%; ablation drops of 7.5% SI from removing contrastive pre-training) are meaningful or within the noise of a single run. This is a significant evidential gap for an RL paper.

2. **Learning-based baselines missing from the cross-language evaluation.** Table 3 compares only against PyLint (Python) and Cppcheck (C++) — static analysis tools with no learning component. Learning-based methods (Code2Seq, Graph2Edit, GraphRL, NeuroRefactor) that were included in the main Java evaluation are absent here. The method actually underperforms on SP (88.9 vs. PyLint's 90.4 for Python; 91.2 vs. Cppcheck's 93.1 for C++). Without learning-based comparators, it is impossible to assess whether the cross-language generalization claim holds relative to other learned approaches.

3. **Questionable baseline selection and no adaptation described.** Code2Seq is a sequence-to-sequence model designed for code summarization and method naming, not refactoring. Graph2Edit generates vulnerable code via program transformations, not refactoring. The paper lists these as "learning-based" baselines (lines 183–184) but provides no description of how they are adapted for the refactoring task. Including baselines whose original objectives are unrelated to refactoring, without describing task-specific modifications, weakens the comparison.

4. **BigCloneBench adaptation is unspecified.** The paper states that BigCloneBench (6 million Java fragments, designed for clone detection) is used "for cross-project evaluation" (line 173), but does not explain how this clone-detection dataset is adapted for a refactoring evaluation — what labels are used, what the evaluation protocol is, or how the results are factored into the aggregate numbers in Table 1. This is a significant gap in experimental reporting.

### Minor

1. **Partial overlap between training reward and evaluation metrics.** Two of the five evaluation metrics have some overlap with reward components. SP (test case pass rate) is closely related to the δ_t penalty term in the reward. SI (reduction in code smells) relates to the "style violations" component of q_t in the reward, though SI is a separately computed aggregate and the reward weighs multiple quality dimensions. This overlap is common in applied ML (models are evaluated on objectives correlated with their training signal) and is not as severe as "three of five metrics" — Δh_t is a validation signal, not an evaluation metric, and ED, MG, and GS are independent of the reward. Nevertheless, the SP overlap in particular means the gap over baselines (93.8 vs. 91.2 SP) should be interpreted with caution.

2. **Figure 1 caption overstates final performance.** The caption claims "higher final performance," but both the proposed method and GraphRL converge to approximately the same final reward (~0.85); the main difference is convergence speed (15k vs. 25k episodes). The paper should frame the advantage as sample efficiency rather than final quality.

3. **No computational cost data.** Pre-training uses 8×V100 GPUs and RL uses a single GPU, but wall-clock times, number of environment steps per dataset, and inference latency are not reported. Without this, the practical feasibility of the approach is unclear.

4. **Semantic equivalence checker failure cases not discussed.** Section 4.5 describes symbolic execution (Cadar & Sen, 2013) for generating test cases to verify semantic preservation. Symbolic execution can fail on code with loops, recursion, or external calls. The paper does not report the success rate of the checker or how failures are handled during training.

### Trivial

- **Writing quality.** The paper acknowledges using LLM polishing (Section 8), but the prose remains awkward in many places (e.g., "objecting to code quality," "something that necessarily requires the existing RL approaches to accomplish and that most often do last year"). This reduces clarity but does not affect the technical content.

## Nice-to-Haves

- **Hyperparameter sensitivity analysis.** The reward weights (w_q, α, β, γ) and exploration parameters are reported but not varied. A brief sensitivity study for the key parameters (especially α, β, γ) would increase confidence that the reported configuration is not cherry-picked.
- **Controlled baseline with standard contrastive pre-training.** Adding an ablation that pre-trains the encoder using a standard contrastive objective on code (without the refactoring-specific augmentations) would isolate whether the *specific* contrastive pre-training matters, or whether any pre-trained code representation would work.
- **Deeper analysis of the embedding-guided exploration strategy.** The ablation shows a large drop when replacing it with random exploration (83.7 → 74.8 SI), but there is no discussion of why this component has such a large effect or how it interacts with the other reward components.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *"Three of the five evaluation metrics are directly or indirectly optimized during training."* — Factually incorrect: Δh_t is not one of the five evaluation metrics listed in the paper (SI, SP, ED, MG, GS). The valid concern about SI and SP overlap is kept as a Minor weakness above.
- *"The correlation between Δh_t and SI is circular."* — The reviewer claims the correlation would arise even with meaningless embeddings because the agent is rewarded for Δh_t. This misunderstands the setting: the correlation is between a training signal (Δh_t) and an *independent* evaluation metric (SI). If embeddings were random noise, there would be no reason for Δh_t to correlate with SI. The concern about a potential confound (both Δh_t and SI correlating with "amount of change") is noted but does not constitute circularity.
- *"The method is more directly optimizing the evaluation metrics than any baseline."* — Rule-based baselines like PMD and Checkstyle are explicitly designed to detect/reduce code smells, so they are directly optimizing related objectives. The asymmetry claim is unsupported.

## Novel Insights

None beyond the paper's own contributions. The harsh review identifies a genuine evidential gap (no variance reporting) and a set of under-specified experimental details (BigCloneBench adaptation, baseline adaptation, cross-language missing comparators), but the core methodological concerns about metric overlap are less severe than initially framed.

## Suggestions

1. Report all results with means and standard deviations over at least 5 random seeds, which is standard practice for RL evaluations.
2. Clarify how BigCloneBench is adapted for refactoring evaluation (task formulation, labels, protocol).
3. Describe how Code2Seq and Graph2Edit are adapted for the refactoring task, or replace them with more appropriate baselines.
4. Include learning-based baselines in the cross-language evaluation (Table 3) to support the generalization claim.
5. Report the success rate and failure handling of the symbolic-execution-based equivalence checker.

## Score and Decision

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>