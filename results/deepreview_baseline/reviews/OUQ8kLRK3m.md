## Summary

This paper introduces DRE-Bench, a dynamic reasoning evaluation benchmark for assessing the fluid intelligence of large language models. DRE-Bench organizes 36 abstract reasoning tasks into a four-level cognitive hierarchy (Attribute, Spatial, Sequential, Conceptual) grounded in psychology, and uses a code-based generator-solver pipeline to produce multiple dynamic variants per task with varying complexity. Evaluations of 11 state-of-the-art LLMs reveal that while models perform reasonably on low-level tasks, their accuracy drops sharply on high-level abstract reasoning, and they exhibit poor generalization and instability as task complexity increases—indicating that current LLMs fall short of genuine fluid intelligence.

## Strengths

- **Clear motivation and well-motivated design.** The paper identifies concrete limitations of existing fluid intelligence benchmarks (lack of cognitive hierarchy, static datasets, scalability issues) and proposes DRE-Bench to address all three, with each design choice explicitly justified.
- **Systematic and interpretable hierarchical framework.** The four cognitive levels (Attribute, Spatial, Sequential, Conceptual) are derived from established psychology literature (Primi 2001), enabling fine-grained, interpretable evaluation of which aspects of reasoning LLMs master or fail at.
- **Scalable and verifiable data generation pipeline.** The human-agent collaboration using code-based generators and solvers allows dynamic generation of many task variants with different complexity levels, and the verification process helps ensure correctness—a significant improvement over manual annotation.
- **Comprehensive evaluation and insightful findings.** The paper evaluates a broad range of general and reasoning LLMs, reports performance across all four levels, analyzes dynamic trends with complexity, and includes ablation studies on in-context learning, visual information, and inference time. Findings such as the asymmetry in spatial orientation (better vertical than horizontal) and the failure of inference-time scaling on high-level tasks are novel and informative.
- **Human study that validates the cognitive hierarchy.** Human performance also declines across levels, confirming the hierarchy's validity, and humans outperform LLMs, reinforcing the claim that current models lack human-like fluid intelligence.

## Weaknesses

### Fatal
None.

### Major
- **Human study accuracy numbers appear implausibly high on Level-4 tasks.** For example, human accuracy on "Mechanics" (Reflection) is reported as 76.16% and "Thermal" (Expansion) as 16.16%. Given the abstract nature and that the paper states these tasks require understanding of physical concepts, these numbers require strong justification. The methodology details (sample size per task, presentation format, participant instructions) are only in the appendix and not sufficiently validated in the main text. If the human numbers are unreliable, the claim that the hierarchy reflects human cognitive difficulty is weakened.
- **The claim of "100% reliability" for code-verifiable data generation is overstated.** The verification uses a set of parameter configurations and manual inspection; this does not guarantee correctness for all possible inputs, especially edge cases or bugs in the generated code.
- **Lack of statistical rigor in experimental results.** All results are averages over three trials with no confidence intervals, standard deviations, or statistical significance tests reported. Given the variability across models and tasks, this omission makes it difficult to assess the reliability of performance differences and trends.
- **The analysis of in-context learning impact is weak.** The improvement from increasing training samples is marginal (e.g., Level-3 from ~38% to ~42%) and inconsistent. The claim that "increasing the number of in-context samples helps models better capture underlying rules" is not strongly supported by the presented data.

### Minor
- **Accuracy is the only primary metric.** Grid-based reasoning tasks could benefit from partial-credit metrics (e.g., grid size precision, matching percentage), which are mentioned in the appendix but not featured in the main results. Including them would provide a more complete picture.
- **The spatial orientation asymmetry observation is intriguing but under-analyzed.** The paper reports that models perform better on vertical than horizontal movements, and better on horizontal than vertical symmetry, but offers no explanation or further investigation (e.g., is this consistent across all models? Does it correlate with training data biases?).
- **Table 1 appears to have a typo: "o3-mini" appears twice with different numbers** (rows 7 and 8), which may confuse readers and suggests a duplicate or mislabeling.

### Trivial
None.

## Nice-to-Haves

- Include confidence intervals or standard errors for all reported accuracies, especially for the main Table 1 and Figure 4.
- Present the auxiliary metrics (grid size precision, matching percentage) in the main paper alongside accuracy to offer a more nuanced evaluation.
- Provide a deeper analysis of the spatial orientation asymmetry, e.g., comparing models with different training data or probing whether the effect is consistent across complexity levels.
- Discuss potential limitations of the code-verifiable generation more explicitly (e.g., possible bugs, blind spots in verification).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Clarify and expand the human study methodology: report the number of samples per participant, whether grids were visualized, and ensure accuracy numbers are reliable and representative. If the human results are not robust, consider presenting them as preliminary or removing the strong conclusions drawn from them.
- Tone down the "100% reliability" claim; replace with "high correctness verified on a held-out set of parameter configurations" or similar wording.
- Add error bars or standard deviations to Table 1 and key figures. Even basic standard errors across three trials would improve interpretability.
- Provide a more nuanced discussion of the in-context learning results, acknowledging the modest and inconsistent improvements rather than overstating the effect.

## Score and Decision

**Score:** 6  
**Decision:** Accept  

The paper presents a well-motivated, systematically designed benchmark that addresses important gaps in evaluating LLM fluid intelligence. The hierarchical cognitive framework, dynamic generation pipeline, and comprehensive evaluations are valuable contributions. The major concerns about the human study's credibility and the lack of statistical rigor are significant but do not invalidate the core contributions; they can be addressed through clarification and revision. Overall, the paper provides sufficient value to the community to merit acceptance.

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>