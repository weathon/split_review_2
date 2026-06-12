## Summary

This paper introduces the Agent GPA (Goal-Plan-Action) framework, a structured evaluation paradigm for LLM agents that decomposes agent behavior into goal setting, planning, and action execution. The framework includes five core metrics (Goal Fulfillment, Logical Consistency, Execution Efficiency, Plan Quality, Plan Adherence) plus two tool-specific metrics, each implemented as a dedicated LLM judge. Experimental validation on TRAIL/GAIA and an internal production data agent dataset shows the framework captures 95% of annotated errors with 86% localization accuracy, substantially outperforming the TRAIL baseline.

## Strengths

- **Well-motivated decomposition with practical value.** The goal-plan-action decomposition is intuitive and maps naturally to how agents operate. By decomposing evaluation into specialized judges rather than relying on a monolithic evaluator, the paper addresses a real weakness of existing agent evaluation methods. The ability to localize errors to specific operational dimensions (plan quality vs. tool calling vs. logical consistency) provides actionable debugging signals that are more useful than binary pass/fail outcomes.

- **Strong experimental comparison against established baseline.** The comparison against the TRAIL LLM judge is well-designed and shows dramatic improvements: 95% vs. ~54% error coverage, and 86% vs. 49% localization on the test set. The per-impact-level breakdown (Table 2, 5) demonstrates that the improvement is especially pronounced for medium and high-impact errors, which are the most operationally relevant.

- **Thorough consistency and reliability analysis.** The paper goes beyond accuracy metrics to examine inter-rater reliability via Krippendorff's α (all above 0.7 except PQ at 0.628) and semantic consistency of judge rationales via cosine similarity. This analysis is important for establishing trustworthiness of LLM-as-judge evaluations and is more rigorous than what most comparable papers provide.

- **GEPA-based automated optimization demonstrates scalability.** The use of automated prompt optimization to replace manual prompt engineering, with results showing GEPA matches or exceeds manually crafted prompts (Table 8), is a valuable practical contribution for deploying the framework at scale.

## Weaknesses

### Fatal
None.

### Major

- **Small dataset sizes limit the strength of quantitative claims.** The TRAIL/GAIA dataset contains only 117 total traces (58 dev + 59 test), and the internal dataset has just 17 traces. With such small sample sizes, per-judge precision/recall estimates (Table 3, 6) have wide confidence intervals, and differences between judges may not be statistically reliable. This is especially concerning for PQ, which has only 14 errors in the test set—performance metrics on such a small class are not very informative. The paper would benefit from reporting confidence intervals or performing statistical significance tests.

- **The "error coverage" metric is partially conflated with category breadth.** The claim that the framework "captures all 570 errors" on TRAIL/GAIA is partly a consequence of how broadly the five-plus-two categories are defined. When human annotators manually map each error to one or more GPA dimensions post-hoc, the framework is guaranteed to cover everything by construction. The more meaningful test is whether the *LLM judges themselves* catch the errors, which the paper does measure (95% recall), but the distinction between framework coverage and judge coverage could be clearer. The 95% figure still leaves 14 uncaught test-set errors unexamined—what characterizes these?

- **Significant precision problems for Plan Quality and Plan Adherence.** PQ has F1 of 0.49 on the test set, and PA has F1 of 0.66. While the paper notes PQ has very few positive examples making evaluation difficult, these are precisely the judges that would be most novel (evaluating the quality of an agent's plan in a reference-free manner). If these judges produce high false-positive rates, their utility for automated debugging is limited. The paper acknowledges this but does not offer a clear path forward.

### Minor

- **The 3-point bucketing for human alignment inflates accuracy.** The paper defines a 4-point scale (0-3) but then buckets into 3 categories (0, {1,2}, 3) for accuracy reporting, noting that off-by-one accuracy was already high. This collapsing obscures meaningful distinctions—distinguishing "partially correct with minor issues" (1) from "partially correct with major issues" (2) is precisely where nuanced evaluation should be most valuable. The high Acc-OB1 scores combined with lower Acc-3pt scores for some judges (e.g., EE at 35.6% on test) suggest the judges struggle with the intermediate gradations.

- **The internal dataset results (Section 4.2) are preliminary.** With only 17 traces and only two judges evaluated, this section provides limited evidence of generalizability. The claim that "the analysis enabled us to recommend several targeted improvements" is interesting but unverifiable without more detail.

- **Trace preprocessing could introduce artifacts.** The preprocessing step strips duplicated messages and truncates long traces to fit context windows. This manipulation could remove or alter information that affects judge performance, and the paper does not quantify the extent of information loss or its impact on evaluation accuracy.

## Nice-to-Haves

- Ablation study showing how each judge contributes to the aggregate performance (e.g., if you remove the best-performing judge, how much does coverage drop?)
- Analysis of the 14 uncaught test errors—what failure mode do they represent that the judges miss?
- Comparison with non-LLM-based automated evaluation methods to better contextualize the value of LLM judges

## Novel Insights

The paper's most interesting empirical finding is that decomposing agent evaluation into specialized LLM judges with targeted prompts substantially outperforms monolithic judges, even when the underlying model is the same. The TRAIL baseline and the GPA judges both use LLMs, yet the GPA approach achieves 95% vs. 54% error coverage. This strongly suggests that evaluation prompt design and task decomposition are as important as model capability for agent assessment. The observation that high-impact errors are easier to detect across all methods, while low-impact errors remain challenging, also provides useful guidance for future evaluation system design.

## Suggestions

- Expand the analysis to include more diverse agent architectures and benchmarks beyond GAIA and SWE-bench to strengthen generalizability claims.
- Provide explicit confidence intervals or bootstrapped error bars on all per-judge metrics given the small dataset sizes.
- Investigate and characterize the errors that the GPA judges fail to catch—understanding these blind spots would strengthen the framework.

## Score and Decision

The paper presents a practical and well-structured framework for agent evaluation that addresses a genuine need in the community. The experimental validation, while limited in dataset size, demonstrates clear improvements over the existing baseline, and the consistency analysis adds credibility. The main concerns are the small datasets, underperformance of key judges (PQ, PA), and the partially circular nature of the coverage claims. These are significant but not fatal issues. The paper represents a useful contribution that will be valuable for practitioners building and debugging agent systems.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>