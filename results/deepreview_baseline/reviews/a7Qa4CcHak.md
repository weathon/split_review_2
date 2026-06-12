## Summary

Terminal-Bench 2.0 is a benchmark of 89 challenging, realistic command-line interface tasks designed to evaluate AI agents on long-horizon, economically valuable work. The tasks span software engineering, system administration, security, scientific computing, and other domains, each with containerized environments, human-written solutions, and comprehensive tests. The authors evaluate 16 frontier models across multiple agent scaffolds, finding that the best system (GPT-5.2 with Codex CLI) achieves only ~65% resolution, with most models scoring substantially lower, and provide detailed error taxonomies to guide future improvements.

## Strengths

- **High-quality, rigorously verified benchmark**: The three-phase verification process (automated checks, expert human review, post-merge auditing with adversarial exploit detection) is exceptionally thorough, with approximately three person-hours of review per task. This sets a new standard for benchmark quality in the agent evaluation community.

- **Realistic and economically valuable tasks**: Unlike synthetic benchmarks, Terminal-Bench tasks are drawn from real workflows (e.g., reimplementing COBOL programs, fixing the OCaml garbage collector, differential cryptanalysis) that represent actual high-skill professional work. The task difficulty estimates (Table 1) confirm these are genuinely hard, long-horizon problems.

- **Comprehensive and fair evaluation**: The authors evaluate 16 models across multiple agent scaffolds with 32,155 total trials, use a neutral testbed (Terminus 2) to decouple model and agent effects, and provide both trajectory-level and command-level error analysis. The Pareto frontier analysis (Figure 5) and difficulty correlation analysis (Figure 6) add practical value.

- **Actionable error taxonomy**: The two-level error analysis (trajectory-level using MAST-derived categories and command-level with detailed failure modes) provides concrete guidance for improving both models and agents. The finding that "command not found" errors account for 24.1% of command failures is a specific, fixable issue.

## Weaknesses

### Fatal
None.

### Major

- **Limited task count (89) and potential for overfitting**: With only 89 tasks, the benchmark may not provide sufficient statistical power to distinguish between models, especially given the 95% confidence intervals shown in Figure 1. The gap between GPT-5.2 (~65%) and Claude Opus 4.5 (~58%) may not be significant. More importantly, 89 tasks is small enough that model developers could potentially overfit to the specific tasks, especially given the public release of the dataset.

- **Crowd-sourced task quality variance**: While the verification process is rigorous, the tasks were contributed by 93 different contributors with varying expertise. The "expert time estimates" in Table 1 show that 48.6% of tasks take experts less than 1 hour, suggesting many tasks may not be genuinely "hard" for humans. The authors' own analysis shows 16.4% of human-rated "medium" tasks are empirically "easy" for models, raising questions about the benchmark's overall difficulty calibration.

- **Internet access introduces reproducibility concerns**: The authors acknowledge that agents can access the internet, which introduces external dependencies (APIs, package versions, web content). This is a significant methodological concern for a benchmark claiming to measure reproducible progress. Two runs of the same model on the same task could yield different results due to external factors, and results may not be reproducible even months later.

### Minor

- **The Terminus 2 scaffold is underspecified**: While the authors describe Terminus 2 as having "a single tool, a headless terminal," the paper provides minimal details about its implementation (e.g., how it handles long-running commands, error recovery, context window management). Given that Terminus 2 is used as the primary evaluation scaffold for comparing models, more implementation details are needed for reproducibility.

- **Error analysis sample size is limited**: The trajectory-level error analysis samples only two failed trials per model per task, and the command-level analysis samples 3,800 failures across all models and tasks. With 89 tasks and 16 models, this means the command-level analysis covers roughly 2-3 failures per model-task combination, which may not be representative.

- **The "canary string" approach to contamination is weak**: The authors rely on a Big-Bench canary string to prevent training data contamination, but this is easily bypassed and does not address intentional contamination by model developers. Given the benchmark's public release and the commercial incentives to perform well on it, this is a growing concern that the paper acknowledges but does not adequately address.

### Trivial
None.

## Nice-to-Haves

- A private test set (even 10-20 tasks) would significantly strengthen the benchmark's resistance to overfitting and contamination.
- Per-task difficulty metrics (e.g., average tokens used, time taken, number of commands issued) would help users understand what makes tasks hard.
- Analysis of which specific tasks are solved by which models would be more informative than aggregate scores alone.

## Novel Insights

The paper's most novel insight is the systematic finding that "command not found" errors account for nearly a quarter of all command failures across models, suggesting that current agents have a fundamental weakness in understanding their environment's capabilities. This is a qualitatively different failure mode from the reasoning errors typically studied in LLM research, and it points to a concrete engineering target: agents need better environment awareness and tool discovery mechanisms. The finding that execution errors dominate for frontier models while open-weight models show more balanced failure patterns (Figure 7) is also valuable, suggesting that different model families may benefit from different improvement strategies.

## Suggestions

- Consider releasing a held-out subset of tasks (e.g., 20 tasks) that are never publicly released, to enable robust detection of overfitting and contamination in future evaluations.
- Provide more detailed specifications for the Terminus 2 scaffold, including prompt templates, context management strategy, and error handling logic, to enable independent reproduction of results.
- Report per-task resolution rates for all models to enable finer-grained analysis of which capabilities are lacking.

## Score and Decision

This is a well-executed benchmark paper that makes a genuine contribution to the agent evaluation community. The verification process is exemplary, the task diversity is impressive, and the error analysis provides actionable insights. The main concerns are the small task count (89) and the reproducibility issues introduced by internet access, but these are acknowledged limitations rather than fatal flaws. The paper is clearly written, the experiments are thorough, and the results are informative. I recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>