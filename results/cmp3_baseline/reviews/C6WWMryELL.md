## Summary

This paper identifies and systematically studies output length volatility in LLM long-form generation—the inconsistency in length and content across multiple generations for the same prompt. The authors introduce VOLTBench, a heterogeneous-task benchmark covering unstructured and structured tasks across languages and instruction complexities, with special emphasis on volatility metrics. Through attention trace analysis, they identify internal patterns (Attention Collapse, Attention Instability) that precede output instability. They propose SELB (Structural Enforcement via Logits Boosting), a training-free decoding strategy that boosts tokens for structural transitions and suppresses known failure modes (early termination, filler phrases). Experiments show SELB improves mean output length by 148% and reduces length volatility by 69% compared to baselines.

## Strengths

- **Important and underexplored problem.** Output volatility across multiple generations is a practical reliability concern that most prior work overlooks, focusing instead on single-generation quality. The paper makes a strong case for why this matters.
- **Comprehensive benchmark design.** VOLTBench covers multiple dimensions (language, instruction complexity, output format) and includes both unstructured and structured tasks, enabling systematic evaluation. The chapter-based format allows scaling up to 100k words, exposing failure modes not visible in shorter tasks.
- **Novel probing methodology.** The attention trace analysis provides interpretable evidence linking internal attention dynamics to observable failures, yielding the identified patterns (Attention Collapse, Attentive Instability) that are plausible and actionable.
- **Lightweight mitigation.** SELB operates at decoding time, requires no training or fine-tuning, and is conceptually simple. The results show substantial improvements in length adherence and volatility reduction on the evaluated tasks.
- **Clear three-stage structure.** The paper is well organized and easy to follow.

## Weaknesses

### Major

1. **SELB is heavily hand-crafted and task-specific.** The method relies on explicit structural anchors (section headers, chapter titles) and manually defined sets of banned tokens. While an extension to free-form generation is described in the appendix, the main paper's results are confined to chapter-based generation. The generalizability to arbitrary long-form tasks without explicit section boundaries is not convincingly demonstrated.
2. **Insufficient rigor in volatility evaluation.** Volatility metrics are computed from only 5 generations per instruction. No confidence intervals, bootstrap estimates, or discussion of sampling error are provided. Given that volatility is the paper's central metric, this is a significant concern—particularly for models with high variance, where 5 samples may give unreliable estimates.
3. **Uncontrolled attribution of improvements.** The claimed "148% improvement in mean output length" and "69% reduction in length volatility" are presented without clear baselines. In Section 6.3, the method is applied to an unspecified base model (presumably Qwen2.5-7B, based on context), but the comparison table (Table 2) mixes different model families. A direct, controlled comparison of the base model with and without SELB on the same tasks is missing; instead, the main comparison is against LongWriter-8B, a different model with different training. It is unclear how much of the improvement is due to SELB versus model choice.
4. **Missing ablation and sensitivity analysis.** SELB has several hyperparameters: boosting constant β, maximum section length τ_max, set of banned tokens, EOS suppression rule. No ablation study isolates the contribution of each component. Sensitivity to hyperparameters (especially τ_max and β) is not explored, raising concerns about reproducibility and robustness.
5. **Attention trace analysis is qualitative.** The paper identifies two patterns from visual inspection of two model runs. No quantitative correlation between attention metrics and volatility is established across models, tasks, or multiple seeds. The causal claim ("output volatility is closely linked to… internal attention dynamics") is suggestive but not rigorously supported.

### Minor

1. **Limited model scope in experiments.** The evaluation focuses on models in the 1.5B–8B range plus three API models. This constrains the generality of the findings, especially for larger open-source models (e.g., 70B+) that may behave differently.
2. **Comparison with existing mitigation is weak.** The only training-free baselines are simple decoding strategies (repetition penalty, entropy stopping, length constraint). There is no comparison to more sophisticated lightweight methods like dynamic temperature, contrastive decoding, or prompt-based approaches (e.g., "ensure you output exactly K sections" with repetition).
3. **Some claims about "first" are overstated.** Prior benchmarks (e.g., LIFEBench, LongGenBench) have evaluated length adherence variability, though not with volatility as the primary metric. The paper's novelty is more in degree and systematicity than absolute firstness.

### Trivial

- None significant.

## Nice-to-Haves

- Evaluate on more diverse and larger models (e.g., 70B-scale) to test generality.
- Provide uncertainty estimates (e.g., bootstrap confidence intervals) for volatility metrics.
- Compare SELB against a simple prompting baseline that explicitly instructs the model to produce exactly K sections of a given length.
- Analyze computational overhead of SELB compared to vanilla decoding.

## Novel Insights

The paper's key insight—that attention dynamics can serve as an early indicator of output instability in long-form generation—is genuinely novel and useful. The identification of "attention summits" (periodic peaks in constraint attention) as necessary for maintaining task coherence, and the distinct failure signatures of collapse versus instability, provide a concrete lens for understanding why models fail in long contexts. This could inspire future work on dynamic attention steering or early-termination detectors.

## Suggestions

1. Perform a controlled experiment comparing a single base model with and without SELB on the same set of tasks, reporting LSD, LVC, MLA for each configuration. Include ablation runs that disable structural enforcement and failure prevention separately.
2. Run all volatility benchmarks with at least 10–20 generations per instruction to improve estimate reliability; report standard errors or confidence intervals.
3. Provide a sensitivity analysis for key hyperparameters (β, τ_max) on at least one task and model.
4. Include a simple prompt-based baseline (e.g., "Write exactly 100 sections, each between 150–200 words") for comparison.
5. Quantitatively link attention patterns to volatility, e.g., by computing the correlation between the variance of constraint attention across steps and the output length variance across runs.

## Score and Decision

**Score**: 4  
**Decision**: Reject  

The paper addresses a timely and practically important problem with a thoughtful three-stage approach. The benchmark and probing analyses are valuable contributions. However, the mitigation method (SELB) has significant limitations in generality and insufficient experimental rigor. The claimed improvements are not convincingly attributed to the method due to uncontrolled comparisons, and the lack of ablation/hyperparameter analysis makes it difficult to assess robustness. These weaknesses prevent the paper from meeting the acceptance bar.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>