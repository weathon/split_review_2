## Summary
This paper proposes RLIE, a framework that integrates LLM-based rule generation with probabilistic modeling (logistic regression) to learn a set of weighted natural-language rules. The method includes iterative refinement driven by prediction errors and evaluates two classes of inference strategies: direct logistic-regression prediction versus injecting rules and weights back into the LLM. Experiments on six text classification datasets show that the linear combiner alone often outperforms LLM-augmented inference, and RLIE achieves competitive or superior results compared to baselines.

## Strengths
- **Clear motivation and architecture.** The paper identifies a genuine gap (lack of probabilistic rule combination in LLM-based rule learning) and proposes a well-structured four-stage pipeline that separates semantic generation (LLM) from global probabilistic weighting (logistic regression).
- **Informative negative result.** The hierarchical evaluation (E1–E4) reveals that injecting rules, weights, and even the linear model’s prediction back into the LLM frequently degrades performance. This finding is non-trivial and provides practical guidance for neuro-symbolic system design.
- **Broad empirical comparison.** The paper compares RLIE against several strong baselines (Zero-shot, IO Refinement, HypoGeniC, LoRA) across six diverse datasets, reporting both accuracy and macro-F1.

## Weaknesses
### Fatal
- **Critical inconsistency in model specification.** Section 4.3 states *“All experiments involving LLMs utilized gpt-4o-mini”*, yet Table 1 lists RLIE results obtained with *Qwen3-Next-80B*, *Qwen3-235B*, and *DeepSeek-V3* as backbones. The paper never explains which LLM actually drove rule generation, rule judgment, and inference within RLIE. This inconsistency invalidates the reproducibility of the reported numbers and makes the comparison to baselines (which used DeepSeek-V3) unreliable.

### Major
- **Unfair backbone comparison.** The LoRA baseline uses a small model (Qwen3-8B) while RLIE is evaluated on models up to 235B parameters. Even among non-LoRA baselines, all use DeepSeek-V3 whereas RLIE’s best results also come from DeepSeek-V3, but the paper mixes backbones without controlling for model size or capacity.
- **Small dataset splits.** Each dataset uses only 200 training, 200 validation, and 300 test samples. With such small splits, the reported results may have high variance and limited generalizability; the paper does not justify why these sizes were chosen or provide statistical significance tests beyond mean and std.

### Minor
- **Limited ablation.** The framework has several hyperparameters (rule capacity H=10, number of hard examples k=20, coverage threshold γ=0.2, number of iterations) but no ablation study examines their impact. The iterative refinement process is described but not empirically characterized (e.g., how often does it converge, how many rules are retained after pruning?).
- **Narrow scope of baselines.** The paper does not compare against classical rule learning methods (e.g., RIPPER, decision lists) even on the same datasets, which would help position the value of the natural-language rule paradigm.
- **Overstated claim of “first”.** The claim that this is the first combination of LLMs with probabilistic rule learning is too strong given prior work on combining neural networks with symbolic reasoning (e.g., Markov Logic Networks, neuro-symbolic rule induction).

### Trivial
- **Figure 1 artifact.** The red arrow labeled “Update” from the Evaluation stage back to Rule Generation is inconsistent with the text, which describes evaluation as a final step after learning.

## Nice-to-Haves
- Ablation on rule set size and iteration count to demonstrate sensitivity.
- A comparison with a classical rule ensemble (e.g., RuleFit) after encoding text via sentence embeddings.
- Analysis of the computational cost (number of LLM calls per dataset).

## Novel Insights
The paper empirically shows that while LLMs are effective at generating and interpreting individual rules, they struggle to integrate probabilistic weights and multiple rule judgments during inference. The logistic regression combiner, though simple, consistently outperforms LLM-augmented strategies. This suggests a design principle for neuro-symbolic systems: confine LLMs to local semantic judgment and leave global aggregation to transparent probabilistic models.

## Suggestions
1. **Clarify the backbone inconsistency.** Specify exactly which LLM was used for each component of RLIE (rule generation, rule judgment, inference) and ensure consistency with the “gpt-4o-mini” statement, or correct the statement.
2. **Run a controlled comparison.** Use the same LLM backbone (e.g., DeepSeek-V3) for all methods, including RLIE, and either match LoRA’s size or explain the discrepancy.
3. **Expand dataset sizes** or provide a power analysis to justify the current splits; include confidence intervals with bootstrapping.
4. **Add ablation studies** on critical hyperparameters (H, k, γ) and report the number of iterations needed for convergence.

## Score and Decision
MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>