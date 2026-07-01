## Summary

Terminal-Bench 2.0 introduces a benchmark of 89 hard, realistic terminal tasks drawn from real professional workflows (COBOL reimplementation, OCaml garbage collector fixes, differential cryptanalysis of FEAL, XSS filter bypass), together with a rigorous two-phase task verification pipeline. The paper evaluates 16 models × 6 agents over 32,155 trials, finding that even frontier models resolve fewer than 65% of tasks, and provides trajectory-level and command-level error analyses to diagnose failure patterns. The benchmark itself is the main contribution, and it fills a genuine gap.

## Strengths

1. **Genuinely realistic, economically valuable task set.** Tasks are drawn from real professional workflows (COBOL reimplementation, OCaml GC fixing, FEAL cryptanalysis, XSS filter bypass) rather than synthetic toy problems. The paper's emphasis on tasks that "professionals are paid to do" (Section 1) is substantive and evidenced by the concrete task descriptions throughout.

2. **Rigorous task verification pipeline.** The two-phase audit process (Figure 3) — automated CI, LLM checks, expert human review, post-merge trajectory auditing, adversarial exploit detection — is substantially more thorough than most benchmark papers. Three hours of combined reviewer attention per task, across three reviewers, represents a genuine investment in quality control that addresses the known failure modes of agent benchmarks (specificity, solvability, integrity).

3. **Broad and systematic evaluation.** 16 models × 6 agents × 89 tasks × ≥5 runs = 32,155 trials is a serious evaluation effort. The cost-performance Pareto analysis (Figure 5) adds practical value beyond a simple leaderboard.

4. **Two-level error analysis.** The combination of trajectory-level (MAST-derived) and command-level error analysis provides actionable diagnostics. The finding that "command not found" accounts for 24.1% of command failures (Figure 8) is a concrete, fixable problem. The observation that open-weight models show a more balanced error profile while closed models are dominated by execution errors (Figure 7) is non-obvious and useful.

5. **Human-predicted vs. empirical difficulty comparison (Section 4.2).** The finding that 93.3% of human-rated hard tasks are also empirically hard, while 54.5% of human-rated medium tasks are empirically hard, quantifies where human intuition overestimates model capability — a useful calibration result.

## Weaknesses

### Fatal
None.

### Major

1. **Agent-model confounding in the headline rankings.** The paper's primary result (Figure 1) reports each model's score using a *different* agent scaffold, chosen "to maximize performance" (Figure 1 caption). GPT-5.2 runs on Codex CLI (its native, heavily engineered scaffold), while Claude Opus 4.5 runs on Terminus 2 (a deliberately simple scaffold with "a single tool, a headless terminal," Section 3.1). The paper acknowledges this confound (Section 3.1: "agent and model performance are hard to decouple") but never resolves it in the reported rankings. The paper's own data show Gemini 2.5 Pro improves 17% when switching from OpenHands to Terminus 2, demonstrating that scaffold choice substantially affects scores. Without a controlled comparison (e.g., all top models on a constant scaffold, reported alongside the best-agent results), the reader cannot determine whether the Figure 1 ordering reflects model capability, scaffold quality, or both. The paper claims "model selection is usually more important than agent scaffold," but this conclusion is drawn from a single comparison point (Gemini 2.5 Pro) and does not justify reporting confounded rankings as the headline result.

### Minor

1. **Contamination risk weakly mitigated.** The paper acknowledges (Section 5) that agents have internet access and the benchmark (including oracle solutions) is on a public GitHub repository. The only protection is a canary string in each file. The counterargument — "we have not observed this behavior in tens of thousands of agent trajectories" — is weak because an agent that finds the solution, internalizes it internally, and then solves the task "naturally" would be indistinguishable from genuine success. This is honestly discussed, and the paper mentions a private test set as future work, but the mitigation does not match the severity of the concern for a benchmark whose purpose is to measure whether models can solve hard tasks.

2. **Llama 4 Maverick listed but absent from reported results.** Section 3.3 lists Llama 4 Maverick among evaluated open-weight models, but it does not appear in Figure 1 or any other results table in the main text. If it was evaluated but scored below a display cutoff, this should be stated; if it was not evaluated with any functional agent scaffold, the model list is inaccurate. This needs clarification.

3. **Empirical difficulty labels are scaffold-specific but presented as task properties.** Section 4.2 defines empirical difficulty based on Terminus 2's pass rate, meaning the "hard"/"medium"/"easy" labels reflect difficulty under a constrained single-tool agent. A model running on Codex CLI or Claude Code might find a "hard" (Terminus-2) task easy. The paper should explicitly scope these difficulty labels to the Terminus 2 scaffold in the main exposition rather than presenting them as task-inherent properties in Figure 6.

4. **Scoring rule not explicitly stated.** The paper uses "resolution rate" throughout but never states whether a task counts as resolved only when *all* tests pass, or whether partial credit is given. Figure 2's example shows "1 passed, 2 failed" but does not clarify how this trial would be counted toward the resolution rate. This is a standard detail that should be explicit.

5. **GPT-5 vs. GPT-5.2 relationship unclear.** Section 3.3 lists "GPT-5.2 (Int, 2026)" but Figure 1 includes both "GPT-5.2 (Codex CLI)" and "GPT-5 (Codex CLI)" as separate entries without explanation. Since 5.2 outperforms 5, the relationship (reasoning budget? capability tier? different model?) needs clarification in Section 3.3.

6. **Cross-reference error in Section 2.1.** The text cites "Section 3.4" for Terminus 2's description as a neutral testbed, but Section 3.4 describes Harbor, not Terminus 2. The correct reference is Section 3.1.

7. **Empirical difficulty model set underspecified.** Section 4.2 says the difficulty metric uses Terminus 2's pass rate "across the frontier models in Section 3.3," but not all Section 3.3 models were tested with Terminus 2. The exact set of models used should be specified.

### Trivial

1. **"Terminal-Bench 2.0" naming unexplained.** The dataset is called "2.0" but there is no reference to a Terminal-Bench 1.0 anywhere in the paper. This appears to be the first release, so the version numbering is confusing.

## Nice-to-Haves

- Run a controlled scaffold comparison: all top models on Terminus 2 (constant scaffold), and a subset of top models cross-evaluated on alternative scaffolds (e.g., Claude Opus 4.5 on Codex CLI, GPT-5.2 on Claude Code). This would decouple model capability from scaffold quality and substantially strengthen the empirical contribution.
- Summarize the adversarial exploit audit results (Appendix C.4) in the main paper rather than deferring entirely to the appendix.
- Report temperature settings and decoding parameters for reproducibility.

## Removed Points

These points from the input review were removed with justification:

- **Missing URL in Section 3.4** ("The Harbor configuration files ... are available at" followed by nothing): Formatting artifact from PDF extraction; the original submission does not have this issue.
- **$1B revenue claim being "unusually high"**: The critic stated this was not a review criterion; it is an observation, not a weakness.
- **"Terminus 2 is too constrained to serve as a neutral testbed" (framed as structural flaw)**: Overstated. The paper's premise is terminal-based tasks, and Terminus 2 aligns with that premise. The paper also evaluates other agents (Codex CLI, Claude Code, etc.) with results in Appendix B. The legitimate concern (that difficulty labels are scaffold-specific) is preserved as Minor weakness #3 above.
- **Temperature / hyperparameters not mentioned**: Per filtering rules, undisclosed hyperparameters are a reproducibility nitpick, not a substantive weakness. Moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the headline confound.** Add a figure or table showing all top models evaluated on Terminus 2 (constant scaffold) alongside the current best-agent-per-model results, so readers can separate model capability from scaffold quality.
2. **Clarify Llama 4 Maverick's status.** Either remove it from the model list or explain why its results are absent from the main figures.
3. **State the scoring rule explicitly.** Clarify whether "resolution rate" counts only tasks where all tests pass, and whether partial credit is ever assigned.
4. **Fix the cross-reference** in Section 2.1 (Section 3.4 → Section 3.1).
5. **Specify the model set** used for the empirical difficulty calculation in Section 4.2.
6. **Disambiguate GPT-5 and GPT-5.2** in Section 3.3.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>