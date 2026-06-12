Now I have all the information I need. Let me write the final review.

---

## Summary

This paper introduces Ambig-SWE, a benchmark for evaluating LLM agents' ability to handle underspecified software engineering instructions. Built by synthetically underspecifying 500 issues from SWE-Bench Verified via GPT-4o, it evaluates six models (Claude Sonnet 4, Sonnet 3.5, Haiku 3.5, Qwen 3 Coder, Deepseek-v2, Llama 3.1 70B) across three settings (Full, Hidden, Interaction) and decomposes agent behavior into three measurable subtasks: detection of missing information, quality of clarification questions, and integration of obtained information for task completion.

## Strengths

- **Clean three-setting evaluation framework with statistical rigor.** The Full/Hidden/Interaction experimental design isolates the causal effect of underspecification and interaction. Wilcoxon signed-rank tests confirm significant differences between Hidden and Interaction settings for all six models (Table 4 in §3.1). This goes beyond simply reporting pass rates to enable controlled causal measurement of interaction's impact.

- **Granular decomposition into measurable subtasks.** Rather than a single pass/fail metric, the paper designs distinct experiments for detection (§4, randomized Full/Hidden presentation across three prompt conditions), question quality (§5, complementary cosine-distance and LLM-as-judge metrics), and task completion (§3). This enables targeted diagnosis of *where* models fail, not just *that* they fail.

- **Non-obvious empirical findings backed by trajectory analysis.** Qwen 3 Coder's performance *worsens* when given navigational file-location information (Table 1, §3.3), traced via trajectory analysis to rigid protocol-following where it re-explores the codebase despite already having the answer. Qwen completely fails to interact under any prompt condition (100% FNR, Table 2) despite matching Sonnet 4 on standard SWE-Bench. These findings go beyond surface-level model comparison to reveal concrete behavioral failure modes.

- **Complementary metrics reveal that integration matters more than extraction.** Claude Sonnet 3.5 and Haiku extract nearly identical information (0.136 vs 0.135 cosine distance) yet achieve vastly different task performance (39.6% vs 26.8%), while Qwen extracts the most (0.179) but with 50% more questions for comparable resolve rates. This disconnection between extraction and integration is a substantive design insight visible only through the dual-metric approach.

- **Transparent characterization of synthetic vs. natural underspecification.** The distributional difference analysis (§2.1) comparing generated issues against naturally underspecified SWE-Bench examples provides methodological transparency that most benchmark papers omit, helping calibrate how to interpret results.

## Weaknesses

### Fatal
None

### Major

- **Unequal experimental conditions across models complicate cross-model comparisons.** Claude Sonnet 4 and Qwen 3 Coder are allocated up to 100 interaction turns while all other models are restricted to 30 (§3.1, line 106), and Claude Sonnet 4 is evaluated on only 100/500 instances in the Hidden setting (footnote 4). The paper justifies this by citing "greater reasoning and planning capacity," but this creates a confound: performance advantages may partly reflect more exploration budget rather than better reasoning. Cross-model comparisons in §3.2 — central to the paper's analysis — become harder to interpret when resource budgets differ substantially. The 100/500 subset for Sonnet 4 in Hidden further limits comparability of gap recovery rates across models.

- **Ecological validity of synthetic underspecification is asserted but not validated.** The paper's own distributional analysis (§2.1) reveals that synthetic issues differ systematically from naturally underspecified ones — they lack code snippets, error messages, and file/line references more aggressively. The authors argue these differences "may not directly impact agent performance" (line 66), but this is asserted rather than demonstrated. No validation experiment assesses whether model rankings or trends transfer to real underspecification. The justification that natural underspecified issues lack paired ground truth is methodologically sound, but even a small-scale validation on a sample of naturally underspecified instances would substantially strengthen the claims about real-world applicability.

### Minor

- **The "74%" claim in the abstract is imprecise.** The abstract states interaction boosts performance "up to 74% over the non-interactive settings." The relative improvement (Interaction−Hidden)/Hidden ranges from 18% (Qwen) to 100% (Haiku). The gap recovery rate (Interaction−Hidden)/(Full−Hidden) ranges from 34% (Llama) to ~76% (Sonnet 4). The "74%" approximates Sonnet 4's gap recovery but is not clearly identified as such, and could be confused with a relative improvement figure. This should be clarified with the specific metric.

- **Detection experiment (RQ2) analysis complicated by prompt sensitivity.** Different models peak at different prompt conditions (Sonnet 3.5 at Moderate, Sonnet 4 at Strong, Deepseek at Neutral). Cross-model comparison at any single prompt setting is unfair, and comparing each model at its "best" prompt introduces selection bias. The paper acknowledges this variability but doesn't fully address the fairness concern in the cross-model analysis.

### Trivial
None

## Nice-to-Haves
- A brief discussion of training interventions suggested by the findings — the conclusion mentions training but remains vague, while the empirical observations (rigid protocol-following, poor detection, exploration-first as best practice) point toward concrete fine-tuning directions.
- A brief summary of average information loss between full and underspecified issues in the main text, rather than deferring all quantitative characterization to Appendix §A.2.3.
- Equalized turn budgets across models or, if budgets must differ, additional metrics (e.g., resolve rate vs. turns used) to disentangle budget effects from capability differences.

## Removed Points
These points are flagged to be removed, treat them with caution.
- **Formatting/style nitpicks** — parser artifacts, not author errors.
- **Missing appendix content** — stripped by parser; exists in original submission.
- **Criticisms about model/tool/benchmark existence** — per hard rules, all cited entities are assumed to exist and be released.

## Novel Insights
The paper's most genuinely novel observation is that the three components of handling underspecified instructions — detection, question quality, and information integration — are largely independent capabilities. Qwen extracts the most information but integrates poorly (worsens with navigational info); Sonnet 4 achieves comparable extraction with fewer questions via exploration-first strategies; Haiku and Sonnet 3.5 extract identically but differ in integration. This decomposition provides actionable diagnostic insight that aggregate benchmarks cannot: it tells researchers *where* to focus improvements. The rigid protocol-following behavior of Qwen 3 Coder — a model that matches Sonnet 4 on standard SWE-Bench yet completely fails to interact — is a striking finding with implications for how we train agentic models, suggesting that current training paradigms optimize task completion without promoting adaptive integration of interactive feedback.

## Suggestions
- Add a small validation experiment comparing model rankings on naturally underspecified SWE-Bench examples vs. synthetic ones.
- Clarify the "74%" figure in the abstract by specifying it as the gap recovery rate for Sonnet 4.
- Equalize turn budgets or report resolve-rate-vs-turns curves to disentangle budget from capability effects.

## Reporting: Calibration Anchors

**Round 1 — Bracketing:**

| Anchor Paper | Avg Human Score | Round | Comparison |
|---|---|---|---|
| NEMESIS Jailbreaking LLMs | 1.40 | R1 | Unrelated; rejected survey on jailbreaking. Much weaker. |
| Systematic Review of LLMs | 1.00 | R1 | Weak survey. Much weaker. |
| DataSciBench | 3.20 | R1 | LLM agent benchmark for data science, rejected. Weaker contribution and analysis. |
| SOP-Agent | 3.00 | R1 | Agent framework, rejected. Less rigorous evaluation. |
| SWE-Bench+ | 3.75 | R1 | SWE-Bench enhancement, rejected. Limited contribution — only filters data. Ambig-SWE is substantially stronger. |
| Codev-Bench | 4.25 | R1 | Code completion benchmark, rejected. Narrower scope, weaker analysis. |
| TDD Benchmark | 4.00 | R1 | Test-driven development benchmark, rejected. Simpler evaluation. |
| FEABench | 4.50 | R1 | Physics reasoning benchmark, rejected. Less relevant topically. |
| ML-Bench | 5.75 | R1 | Repo-level ML benchmark, rejected. Ambig-SWE has broader model evaluation, cleaner design, deeper insights. |
| SWE-bench original | 6.25 | R1 | Foundational benchmark, accepted. Ambig-SWE extends it meaningfully. |
| AgentBench | 6.20 | R1 | General agent benchmark, accepted. Less focused on underspecification. |
| ScienceAgentBench | 6.00 | R1 | Scientific agent evaluation, accepted. Less relevant. |
| RefactorBench | 6.50 | R1 | Code agent evaluation, accepted. Ambig-SWE evaluates more models with cleaner experimental design. |
| τ-bench | 6.50 | R1 | Tool-agent-user interaction, accepted. Topically aligned — also simulates user interaction. Comparable quality. |
| Commit0 | 6.67 | R1 | Library generation benchmark, accepted. Ambig-SWE has more thorough analysis and actionable insights. |
| Active Task Disambiguation | 7.33 | R1 | Disambiguation via clarifying questions, accepted. Most topically relevant. Proposes a novel method; Ambig-SWE is purely evaluation but on more realistic tasks with 6 models. |
| Spider 2.0 | 8.00 | R1 | Enterprise text-to-SQL, accepted. Higher quality but different domain. |
| BigCodeBench | 9.00 | R1 | Code generation benchmark, accepted. Stronger contribution across board. |

**Round 1 bracket:** Between 6.0 and 7.0. Ambig-SWE is clearly above ML-Bench (5.75) and comparable to SWE-bench (6.25), τ-bench (6.50), and RefactorBench (6.50). It sits somewhat below Active Task Disambiguation (7.33) which contributed a novel method rather than purely an evaluation.

**Final calibration:** The paper's clean experimental design, breadth of model evaluation (6 models with statistical tests), genuinely non-obvious findings, and careful decomposition into measurable subtasks place it solidly among accepted benchmark papers in the 6.5 range. The two major weaknesses (unequal turn budgets, unvalidated ecological validity) are real but acknowledged, and don't undermine the core contribution of the framework and insights.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>