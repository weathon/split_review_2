## Summary

This paper proposes Autoformalizer with Tool Feedback (ATF), a framework that improves autoformalization of mathematical statements into Lean 4 by integrating two tools during generation: a Lean 4 compiler for syntax checking and a multi-LLM ensemble for semantic consistency validation. The model is trained through a three-phase pipeline (cold-start, expert iteration, DPO) to learn iterative refinement based on tool feedback, achieving substantial improvements over existing formalizers across three benchmarks, with particularly large gains on out-of-distribution data.

## Strengths

- **Well-motivated problem with clear practical impact.** The paper convincingly identifies two key failure modes in existing autoformalizers—syntactic invalidity and semantic inconsistency—and designs targeted tools for each. The motivating examples in Figure 1 effectively illustrate subtle failure cases (e.g., ∃ vs ∀, modulo 100 vs 12).

- **Strong and comprehensive experimental results.** ATF-32B outperforms all baselines across all three benchmarks on both syntax and consistency metrics. The improvements are especially striking on CombiBench (out-of-distribution): 29.13% absolute improvement in Pass@1 consistency over Goedel-V2-Formalizer-32B. The human evaluation on 300 instances (100 per benchmark, 3 annotators each) validates the automatic consistency check tool, with a Pearson correlation of 0.746.

- **Thorough ablation study.** Table 4 systematically isolates the contribution of each component (syntax check, consistency check, cold-start, expert iteration, DPO), clearly demonstrating that tool feedback is essential and that each training phase provides cumulative gains. The no-tools baseline drops to 23.69% on CombiBench consistency vs. 65.38% with full ATF.

- **Insightful analysis of inference scaling.** Figure 4 demonstrates that ATF continues to benefit from additional revision attempts and parallel sampling beyond training constraints, suggesting the model has learned generalizable revision strategies rather than memorized patterns.

- **Practical engineering contributions.** The grouped Lean 4 execution method (Figure 3) for efficient batch compilation and the multi-LLM ensemble voting for reducing false positive rate in consistency checking (FPR from ~9% to ~6%) are useful practical contributions.

- **Valuable open-source resource.** The Numina-ATF dataset of 750K synthetic formal statements is a significant contribution to the ATP community.

## Weaknesses

### Fatal
None.

### Major

- **Fairness of inference-time comparison.** ATF uses up to 4 revision attempts with tool calls during inference, while it is unclear whether baselines like Goedel-V2-Formalizer-32B (which also uses "self-correction" per its title) employ comparable iterative refinement. The authors claim output lengths are "roughly equivalent," but the computational cost per query differs significantly due to multiple tool calls (compiler invocations, LLM ensemble queries). A wall-clock time or FLOPs comparison would strengthen the fairness argument. Without this, the Pass@1 comparison may conflate method quality with inference budget.

- **Noisy consistency training signal.** The consistency check tool has a ~6% false positive rate (Table 1), meaning ~6% of semantically inconsistent statements are labeled as consistent during training. While the authors validate with human evaluation post-hoc, the impact of this label noise on the training process itself is not analyzed. How many training trajectories are potentially corrupted by false consistency labels?

### Minor

- **Consistency benchmark construction bias.** The negative examples for the consistency check benchmark are generated exclusively by Gemini-2.5-Pro, which may not represent the full distribution of semantic errors the formalizer produces. The benchmark's ability to evaluate the tool's effectiveness on ATF's own error distribution (which may differ from Gemini-generated perturbations) is not validated.

- **Limited analysis of persistent failure modes.** The paper shows strong aggregate metrics but provides little analysis of what types of problems or errors ATF still fails on. Figure 5c shows consistency check success rate declining from 69.5% to 8.8% across attempts, but the paper doesn't characterize what makes later attempts fail—whether the model exhausts its knowledge, hits fundamental limitations, or gets stuck in loops.

- **Distillation details sparse.** ATF-8B-Distilled is mentioned as trained "using the same data," but the distillation procedure (e.g., is it trained on ATF-32B trajectories, or independently?) is not clearly described in the main text.

### Trivial
None.

## Nice-to-Haves

- A comparison of inference latency/cost between ATF and baselines to contextualize the performance gains.
- Error-type analysis (e.g., categorizing remaining failures by type) to guide future work.
- Analysis of how the consistency check tool's FPR affects training trajectory quality.

## Novel Insights

The paper's most interesting finding is the inference-time scaling behavior: the model generalizes revision strategies beyond its training regime (trained with <8 revisions, continues improving up to 14), and the combination of revision scaling with parallel sampling can push success rates toward 100% even on challenging out-of-distribution data. This suggests that tool-augmented autoformalization has a fundamentally different scaling profile than single-pass methods, where the bottleneck shifts from model capability to search budget. The declining consistency check success rate across attempts (69.5% → 8.8%) also provides a useful signal about the diminishing returns of iterative refinement.

## Suggestions

- Add a table or figure comparing wall-clock inference time and/or computational cost across methods to contextualize the performance gains.
- Include a brief error taxonomy for ATF's remaining failures on CombiBench to help the community understand what remains unsolved.
- Clarify the ATF-8B-Distilled training procedure—whether it involves distillation from ATF-32B trajectories or independent training.

## Score and Decision

This is a solid applied paper that addresses an important problem (autoformalization for ATP) with a well-designed methodology, strong experimental results validated by human evaluation, and meaningful practical contributions (open-source dataset, engineering insights). The improvements are substantial and consistent, particularly on out-of-distribution data. The main concerns are around inference-time comparison fairness and noisy training labels, but these do not invalidate the core contribution. The paper advances the state of the art in autoformalization in a meaningful way.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: Accept