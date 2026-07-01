## Summary

This paper introduces Terminal-Bench, a benchmark for evaluating AI agents on hard, realistic command-line interface tasks. The benchmark comprises 89 tasks in containerized environments spanning software engineering, security, data science, and other domains, each with an instruction, a Docker image, tests, and a human-written reference solution. The authors evaluate 16 frontier models across multiple agent scaffolds (Claude Code, Codex CLI, Gemini CLI, OpenHands, Mini-SWE-Agent, and their own Terminus 2), conducting over 32,000 trials, and find that the best-performing system (GPT-5.2 with Codex CLI) achieves only ~63% resolution. The paper also provides trajectory-level and command-level error analyses to characterize failure modes and inform future improvements.

## Strengths

- **Rigorous task verification pipeline.** Each task undergoes a multi-stage audit: automated CI checks (oracle solution must pass, dummy agent must fail), LLM-based review, adversarial exploit detection, and manual review by at least three experienced human auditors, totaling approximately three hours of reviewer attention per task. This sets a high standard for dataset quality that many existing benchmarks lack.
- **Diverse and realistic task collection.** The 89 tasks are crowd-sourced from 93 contributors and span 16 categories, including non-engineering domains like video processing and personal assistance. Time estimates from task authors (Table 1) show that many tasks would take a junior engineer 1–24 hours, supporting the claim of non-trivial difficulty.
- **Comprehensive evaluation across models and agents.** The authors run 32,155 trials across 16 frontier models and 6 agent scaffolds, with each task attempted at least 5 times per model-agent combination. This provides a reliable empirical picture, and the inclusion of both closed-source and open-weight models adds breadth.
- **Detailed error analysis with validated methodology.** The trajectory-level analysis uses a taxonomy adapted from MAST, with human annotators achieving 93% Cohen's κ on a calibration set. The command-level analysis labels 3,800 failures against a taxonomy with 82% human-LLM agreement. These analyses yield actionable insights (e.g., "command not found" accounts for 24.1% of command failures; open-weight models show more balanced error patterns across execution, coherence, and verification categories).
- **Public release of dataset and evaluation harness** with canary strings to aid decontamination, and integration with the Harbor framework for reproducibility.

## Weaknesses

### Fatal
None identified. The paper's core claims—that Terminal-Bench contains hard, realistic tasks and that frontier models score below 65%—are supported by the presented evidence.

### Major

1. **Confounding of model and agent scaffold.** The paper chooses the agent scaffold that maximizes performance for each model, but this makes it impossible to attribute performance differences to model capability versus scaffold quality. For example, GPT-5.2 uses Codex CLI while Gemini 3 Pro uses Terminus 2—both are state-of-the-art, but the comparison conflates model and infrastructure. The authors acknowledge this challenge (Section 3.1) but the evaluation design does not isolate model effects, weakening conclusions about model rankings.

2. **LLM-as-judge circularity in error analysis.** The trajectory-level error analysis uses GPT-5 (high-reasoning mode) as the primary judge to classify failures, yet GPT-5 is itself one of the evaluated models. While validated against human annotations (90% agreement), the risk of systematic bias in favor of or against models from the same family is non-trivial. The command-level analysis uses the same GPT-5 model (92.4% agreement with humans, 82% for taxonomy categorization) and faces a similar concern. Using a model from outside the evaluated pool would have been preferable.

3. **Limited number of tasks (89) for a benchmark.** While the tasks are diverse and complex, 89 tasks provide limited statistical power for fine-grained comparisons, especially when broken down by category (many categories have 1–4 tasks). The error bars in Figure 1 are correspondingly wide for some models. A larger set would improve the reliability of per-category conclusions.

### Minor

1. **Internet access introduces uncontrolled variance.** Allowing agents to install packages and query the web means results may not be perfectly reproducible over time (package versions, API availability, web content changes). The authors acknowledge this limitation but do not quantify its impact on result variance.

2. **Uneven category distribution.** Software Engineering accounts for 26 of 89 tasks (~29%), while multiple categories have only 1–2 tasks (e.g., Video Processing, Data Querying). This limits the benchmark's ability to draw meaningful conclusions in under-represented domains.

3. **Cost Pareto analysis (Figure 5) is informative but brittle.** API pricing changes frequently, so the cost-performance frontier is likely to shift. The analysis is useful as a snapshot but should be interpreted with caution for future comparisons.

### Trivial

- The abstract and text state that frontier models score "less than 65%", but the top result (GPT-5.2, Codex CLI) is shown as ~63% in one place and ~65% in Figure 1. The error bar likely covers 65%, making the phrasing slightly imprecise but technically correct for the reported ~63% average.
- The paper references "Terminal-Bench 2.0" but does not explain what version 1.0 was or how the current version differs, which may confuse readers.

## Nice-to-Haves

- An ablation comparing the same model across different agent scaffolds would help decouple model capability from scaffold effects, strengthening the conclusion that "model selection is usually more important than agent scaffold."
- A human baseline (e.g., expert human performance on a subset of tasks) would calibrate the benchmark's difficulty against human ability and strengthen the claim that tasks are "realistic" for skilled professionals.
- Analysis of the  tasks that *no* model could solve (briefly mentioned in Section 4) could illuminate whether the bottleneck is reasoning, tool use, or task design issues.

## Novel Insights

The paper's most novel contribution is the combination of a rigorous, multi-stage human verification process with a task set that demonstrably saturates frontier models (best score ~63%). The finding that different model families exhibit distinct failure-mode signatures (execution-dominated for frontier closed models, more balanced for open-weight models, as shown in Figure 7) is a useful diagnostic for guiding targeted improvements. The command-level error taxonomy, particularly that "command not found" errors account for nearly a quarter of all command failures, is a concrete and actionable insight for improving agent robustness in open-ended terminal environments.

## Suggestions

- Consider publishing results from running a *single* model across multiple scaffolds (e.g., using one model with Terminus 2, Claude Code, and Codex CLI) to provide a cleaner decomposition of model vs. scaffold effects.
- Provide a human-expert baseline on a stratified sample of tasks to anchor the difficulty claims.
- Extend the benchmark over time with a private held-out set to future-proof against data contamination, as the authors suggest in the limitations section.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>