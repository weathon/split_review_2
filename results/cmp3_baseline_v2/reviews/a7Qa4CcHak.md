## Summary

Terminal-Bench is a new evaluation framework and curated dataset of 89 hard, realistic command-line interface tasks that require long-horizon autonomous agent behavior. The paper introduces a rigorous multi-stage verification pipeline with manual review, automated checks, and adversarial exploit detection, then evaluates 16 frontier models across multiple agent scaffolds, finding that the best model achieves only ~65% resolution. The authors also provide trajectory-level and command-level error taxonomies to guide future development.

## Strengths

- **Geniunely hard, economically valuable tasks.** The benchmark focuses on the kind of high-skill work professionals are paid to do—reimplementing COBOL programs in Python, performing differential cryptanalysis, implementing physics-based renderers—and shows meaningful headroom for frontier models. This distinguishes Terminal-Bench from benchmarks that saturate quickly or measure toy problems.
- **Rigorous, multi-stage verification process.** Each task undergoes automated CI checks, LLM-assisted review, expert human review, post-merge adversarial exploit auditing, and manual trajectory inspection by multiple auditors (~3 reviewer-hours per task). This is a much higher verification standard than most agent benchmarks, and the authors transparently acknowledge remaining risks.
- **Open-source release with decontamination measures.** The dataset and Harbor evaluation harness are publicly released, and each file contains a Big-Bench canary string to aid training corpus decontamination. This supports reproducibility and community use.
- **Useful error analysis.** The taxonomy of failures at both the trajectory level (execution, coherence, verification) and command level (invocation, REPL, runtime, app failure, filesystem) provides actionable insights for improving both models and agent scaffolds. The human-LLM agreement validation (93% Cohen's κ on calibration set) strengthens confidence in the analysis.
- **Systematic evaluation across models and agents.** 32,155 trials across 16 models and multiple scaffolds yields statistically meaningful comparisons. The inclusion of a neutral scaffold (Terminus 2) helps disentangle model vs. agent effects, and the cost-performance Pareto analysis is practically useful.

## Weaknesses

### Major

- **Limited dataset size.** 89 tasks is small for a benchmark intended to measure progress of frontier models. With many categories having only 1-4 tasks (Video Processing, Data Querying, Personal Assistant), per-category conclusions are statistically unreliable. Confidence intervals in Figure 1 reflect this uncertainty. A larger task count would substantially strengthen the benchmark.
- **Crowd-sourced difficulty estimates are subjective.** The human-predicted difficulty labels (medium/hard) come from task authors, and while there is overall correlation with empirical difficulty (r=0.436), the paper reports that 54.5% of human-"medium" tasks are empirically hard. This suggests the difficulty labeling is noisy and may not reliably stratify tasks for future analysis.
- **Potential for benchmark overfitting is acknowledged but not addressed.** The authors note that models could train on the public dataset and that preventing intentional contamination is "outside the scope of this paper." For a benchmark whose main value is measuring frontier capability progress, the lack of a private held-out test set is a meaningful limitation that weakens longitudinal conclusions.

### Minor

- **Category imbalance limits diagnostic power.** Software Engineering comprises 26/89 tasks (~29%) while 8 categories have ≤2 tasks each. This makes the benchmark better suited for aggregate scores than for diagnosing specific capability gaps.
- **Terminus 2 scaffold may disadvantage some models.** The paper's neutral scaffold uses only a headless terminal with Bash commands, but some models may have been optimized for tool-calling interfaces. The authors acknowledge this but could more explicitly quantify how scaffold choice affects rankings (beyond the one Gemini-2.5-Pro example).
- **LLM-as-judge for command-level error analysis has limitations.** While agreement with human annotators (82-92.4%) is reported, systematic biases in the judge model (GPT-5) could propagate into the failure taxonomy. The paper does not analyze what kinds of errors the LLM judge systematically misclassifies.

### Trivial

- The paper claims "less than 65%" while the top model achieves ~65% (within error bars). The framing is slightly imprecise but not misleading.

## Nice-to-Haves

- Include a private test set in future work (as the authors suggest).
- Stratify results by task category even for aggregate scores to understand where different models excel.
- Analyze the variance of model performance across multiple runs per task to identify tasks that are particularly noise-sensitive.

## Novel Insights

The finding that human-predicted and empirical difficulty diverge primarily on "medium" tasks (54.5% of human-medium tasks are empirically hard) suggests that current models struggle with tasks requiring creative or adversarial reasoning even when humans perceive them as moderate difficulty. The command-level failure analysis—showing that "command not found" errors account for 24.1% of all failures—reveals a surprisingly mundane bottleneck: frontier models still fail at basic environment awareness and tool invocation. This insight is more concrete than typical "reasoning failure" taxonomies and directly points to practical improvements (better environment state tracking, more robust command construction).

## Suggestions

- Expand the benchmark to at least 200+ tasks to improve statistical reliability, especially for sub-category analysis.
- Develop a private test set (e.g., using held-out tasks with restricted access) to enable reliable tracking of progress over time and detect benchmark overfitting.
- Include standard deviations or per-task pass rates in addition to aggregate means to give a richer picture of model reliability.

## Score and Decision

**Score: 7.5** — The paper presents a carefully constructed, hard, and realistic benchmark with a verification standard that exceeds most existing agent benchmarks. The evaluation is thorough, the error analysis is actionable, and the open-source release is a genuine service to the community. The primary limitations are dataset size and the lack of a private test set, which constrain the benchmark's long-term utility for measuring frontier progress. Despite these concerns, the contribution is strong and well-executed.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>