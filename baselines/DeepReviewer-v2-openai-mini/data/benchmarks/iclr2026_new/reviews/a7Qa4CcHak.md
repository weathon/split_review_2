## Summary
# Final Review Report

## Summary

This paper presents Terminal-Bench 2.0, a benchmark for evaluating AI agents on hard, realistic command-line tasks. The benchmark consists of 89 tasks across 16 categories (Software Engineering, System Administration, Security, Scientific Computing, etc.), each implemented as a containerized environment with a human-written instruction, outcome-based tests, and a reference solution. Tasks were crowd-sourced from 93 contributors (229 submissions) and filtered through a rigorous multi-stage verification process involving automated checks, LLM-assisted auditing, adversarial exploit detection, and manual review by three experienced reviewers totaling ~3 person-hours per task.

The authors evaluate 16 frontier LLMs across 6 agent scaffolds (Claude Code, Codex CLI, Gemini CLI, OpenHands, Mini-SWE-Agent, and their own Terminus 2), running 32,155 trials in total. The key empirical finding is that the best-performing system (GPT-5.2 via Codex CLI) achieves only 63% resolution, and smaller models fall to 12–15%. The paper provides two complementary error analyses: trajectory-level (categorizing failures into Execution, Coherence, and Verification classes) and command-level (finding that 24.1% of command failures are "command not found" errors).

**Strengths:** The benchmark addresses a genuine gap — measuring agents on economically valuable, long-horizon terminal work. The verification pipeline is exceptionally thorough. The evaluation scale (32,155 trials) and error analysis methodology are impressive contributions. The cost-performance Pareto analysis and human-vs-model difficulty correlation provide actionable insights.

**Weaknesses:** (1) Model-scaffold coupling makes clean cross-model comparisons difficult. (2) The Related Work section lists benchmarks but does not provide a structured comparative positioning. (3) The conclusion undersells the paper's empirical findings. (4) The empirical difficulty definition uses arbitrary thresholds without sensitivity analysis. (5) Several methodological details in the error analysis (sampling strategy, taxonomy pruning, LLM-judge agreement) need clarification. (6) Limitations omit discussion of cost comparability, benchmark ceiling effects, and English-only task language.

**Novelty:** External literature verification is deferred due to retrieval unavailability in this run. Based on manuscript content alone, the main novel contributions are the Terminal-Bench framework and dataset, the large-scale evaluation with 16 models, and the dual error analysis methodology. The novelty relative to existing benchmarks (SWE-Bench, WebArena, OSWorld, τ-Bench, etc.) is the combination of real terminal environments, diverse expert-curated tasks, and outcome-driven evaluation, but a systematic literature comparison is needed to confirm positioning.

**Score: 7/10** (strong empirical contribution and rigorous verification methodology; weaknesses in comparative positioning, methodological transparency, and conclusion synthesis are fixable in revision)

## Strengths
**1. Addresses a genuine and timely evaluation gap.** The paper identifies that existing agent benchmarks either test narrow skills (code generation, shell translation) or use synthetic/simulated environments, and fills this gap with realistic, outcome-driven terminal tasks. The focus on economically valuable workflows (software engineering, system administration, security, scientific computing) is well-motivated and practically important.

**2. Exceptionally rigorous verification pipeline.** The multi-stage task verification process (Figure 3) — automated CI checks, LLM-assisted review, expert human review, post-merge trajectory analysis, adversarial exploit auditing, and final auditor sign-off — sets a high standard for benchmark construction. The reported ~3 person-hours of reviewer attention per task demonstrates substantial community investment.

**3. Large-scale, systematic evaluation.** Running 32,155 trials across 16 models and 6 agent scaffolds at 5+ repetitions each provides statistically meaningful coverage. The evaluation includes both closed-source frontier models (GPT-5.2, Claude Opus 4.5, Gemini 3 Pro) and open-weight models (Qwen Coder, Kimi K2, GLM 4.6), enabling broad landscape analysis.

**4. Actionable error analysis.** The dual error analysis — trajectory-level (Execution/Coherence/Verification taxonomy derived from MAST) and command-level (taxonomy with 24.1% "command not found" as top failure mode) — provides concrete, actionable insights for agent and model developers. The use of Docent + LLM-as-judge + human validation is a methodological contribution in itself for scalable error annotation.

**5. Interesting human-model difficulty comparison.** The correlation analysis (r=0.436, p<0.001) between human-predicted and empirical difficulty, especially the finding that 54.5% of human-medium tasks are empirically hard for models, provides insight into systematic capability gaps where human intuition outperforms current models.

**6. Open infrastructure.** The Harbor evaluation framework, task format, and experimental configuration are released openly, enabling community contributions and reproducible evaluations. The canary string inclusion aids training corpus decontamination.

**7. Well-scoped limitations discussion.** The Limitations section honestly addresses contamination risk, internet dependency, and task quality tradeoffs, demonstrating awareness of benchmark validity threats.

## Weaknesses
**W1. Model-scaffold coupling undermines clean comparisons (Major).** The paper evaluates models using different agents (Terminus 2 for most, Codex CLI for GPT models, Claude Code for Anthropic models, etc.), so it is impossible to disentangle model capability from scaffold effectiveness. The paper acknowledges this challenge but does not fully resolve it. The top result (GPT-5.2 via Codex CLI, 63%) and second-best (Claude Opus 4.5 via Terminus 2, 58%) use different scaffolds, and the paper's own data shows scaffold effects of up to 17% (Gemini 2.5 Pro: Terminus 2 vs. OpenHands). A cleaner design would have run all models on at least one shared scaffold (e.g., all 14 Terminus-2-compatible models) and reported those rankings alongside the scaffold-maximized results. *Reference: Page 5 - Section 3.1; Page 6 - Section 4 Results.*

**W2. Related Work lacks structured comparative positioning (Major).** The Related Work section (Section 6) lists benchmark families (SWE-Bench, WebArena, τ-Bench, etc.) with one-sentence descriptions but does not provide a systematic comparison against Terminal-Bench on key axes (task source, environment type, outcome-driven vs. process-driven, verification rigor, task count, domain diversity, cost analysis, long-horizon capability). Without this structured positioning, the paper's novelty claim — "distinct in its emphasis on diverse, long-horizon tasks collected from experts, conducted inside a real terminal shell" — is asserted rather than demonstrated. A comparative table would substantially strengthen the contribution framing. *Reference: Page 9 - Section 6 Related Work.*

**W3. Empirical difficulty definition lacks sensitivity analysis (Major).** The "empirical difficulty" thresholds (Easy: ≥66.7%, Hard: <33.3%) are presented without justification or sensitivity analysis. The paper should demonstrate that the main conclusions (e.g., 93.3% of human-hard tasks are also empirically hard) hold under alternative thresholds (e.g., 70/30, 60/40). Additionally, the definition uses Terminus 2 pass rates, which may reflect scaffold-specific biases rather than genuine task difficulty. *Reference: Page 6-7 - Section 4.2.*

**W4. Conclusion undersells empirical findings (Major).** The conclusion re-states the framework and dataset but does not synthesize the paper's rich empirical findings into actionable guidance. Key messages — "command not found" being the most common failure (24.1%), execution errors dominating frontier model failures, 22% of tasks unsolved by any model — are left for readers to extract. The final paragraph's focus on urging dataset curators to invest in manual verification, while appropriate, does not reflect the paper's primary contributions as an evaluation and analysis paper. *Reference: Page 9 - Section 7 Conclusion.*

**W5. Error analysis methodology needs clarification (Moderate).** Several methodological details require elaboration: (a) The trajectory-level sampling strategy ("two failed trials per model") is undefined for models with fewer than two failures; (b) The MAST sub-categories that were "dropped" are not enumerated, making the taxonomy's completeness unverifiable; (c) The Figure 7 failure percentages sum to >100% per model but this is not explicitly stated in the caption; (d) The LLM-as-judge (82.0% agreement) used for command-level categorization introduces a non-trivial misclassification floor (~680 potentially mislabeled instances out of 3,800) without robustness checks. *Reference: Page 7-8 - Sections 4.3, 4.4.*

**W6. Time limit specification and enforcement unclear (Moderate).** The task formulation mentions a "time limit" but the paper never specifies how limits were set (based on expert or junior estimates?), whether they were enforced in evaluation, or how violations were handled. This is critical for reproducibility: an agent that spends 3 hours on a task designed for 1 hour may have an unfair advantage or disadvantage depending on the limit. *Reference: Page 1 - Section 2.1 Task Formulation.*

**W7. Task category sparsity limits fine-grained analysis (Minor).** Of 16 task categories, 8 have fewer than 5 tasks each. Categories with 1 task each (Personal Assistant, Video Processing, Optimization, Data Querying) cannot support meaningful category-level conclusions. Additionally, category labels were self-assigned by authors without a standardized rubric, raising consistency concerns. *Reference: Page 4 - Section 2.4 Composition, Figure 4.*

**W8. Missing limitations: cost comparability, ceiling effects, language bias (Minor).** The Limitations section is transparent about contamination and internet dependency but omits: (a) API costs in Figure 5 are provider-specific and not transferable; (b) the benchmark may approach saturation within 1-2 model generations (best model at 63%); (c) all tasks use English-language tooling, limiting global generalizability. *Reference: Page 9 - Section 5 Limitations.*

**W9. Abstract and Introduction could better differentiate the gap (Minor).** The abstract's gap statement is generic ("Current benchmarks either do not measure real-world tasks, or are not sufficiently difficult"), and the introduction lacks a clear paragraph positioning the terminal as the specific missing evaluation environment before discussing agent popularity. The first intro paragraph mentions general AI progress without connecting to terminal-specific needs. *Reference: Page 0-1 - Abstract and Section 1 Introduction.*

**W10. Revenue claim lacks verifiable citation (Minor).** The claim that "Claude Code drives $1B in run-rate revenue" is striking but cites only "(Anthropic, 2025)" — an internal company source without public verification. For peer-reviewed publication, this should be clearly marked as self-reported. *Reference: Page 1 - Section 1, paragraph 2.*

**W11. Outcome-driven testing: edge cases and test completeness verification (Verification-needed).** The paper states tests verify properties of the "final container state" through unit tests. However, it does not discuss false positives/negatives in tests: if an agent solves a task in an unexpected but correct way that the tests do not recognize, is it marked as a failure? Conversely, can tests pass while the task is genuinely unsolved (test incompleteness)? The verification process partially addresses this (specificity criterion), but the risk of test incompleteness is not quantified. *Reference: Page 1-3 - Sections 2.1, 2.3.*

**W12. Small model annotation and scaling law analysis is premature (Verification-needed).** The correlation between model size/API cost and performance is presented in Figure 5 but without controlling for agent scaffold, reasoning effort, or training data freshness. The claim "model selection is usually more important than agent scaffold" is supported by only one data point (Gemini 2.5 Pro: 17% scaffold effect). More systematic ablation (varying scaffold while fixing model, and vice versa) is needed to support this claim reliably. *Reference: Page 6 - Section 4, paragraph 1.*

## Score
**Final Score: 7/10**

**Rationale:** The paper makes a strong empirical contribution by introducing a timely, well-verified benchmark for terminal-based agent evaluation and conducting an impressively large-scale study (32,155 trials across 16 models). The verification pipeline and error analysis methodology are standout features that advance benchmark construction practice. However, the score is limited by four key factors:

1. **Novelty verification is deferred** due to external literature retrieval being unavailable in this run. A full assessment of the benchmark's positioning relative to existing work (SWE-Bench, WebArena, OSWorld, τ-Bench, etc.) requires systematic comparison that could not be completed here.

2. **Model-scaffold coupling** prevents clean interpretation of the model rankings — the top result uses a different agent than the second-best, and scaffold effects of up to 17% are documented but not fully controlled.

3. **Several methodological details** (difficulty threshold selection, error analysis sampling strategy, taxonomy pruning rationale, LLM-judge agreement impact) need clarification to meet the transparency standards expected for a benchmark paper.

4. **Narrative framing could be significantly strengthened** — the conclusion undersells the empirical findings, the Related Work lacks structured comparison, and the abstract's gap statement is generic.

These weaknesses are fixable in revision. The core contributions (the framework, dataset, evaluation, and error taxonomies) are solid and reproducible. With stronger comparative positioning, methodological clarifications, and a more impactful conclusion, this paper would merit a score of 8/10.

**Scoring breakdown (10-point scale):**
- Research value and significance: 8/10 (addresses a clear gap, economically motivated)
- Methodological soundness and reproducibility: 7/10 (strong verification but scaffold confound and missing details)
- Novelty and positioning: 6/10 (deferred external verification; related work needs structured comparison)
- Experimental rigor and evidence depth: 8/10 (large scale, multi-perspective error analysis, cost analysis)
- Clarity and presentation: 6/10 (well-structured but conclusion, abstract, and related work need revision)
- Actionability of findings: 8/10 (error taxonomies directly inform agent development priorities)