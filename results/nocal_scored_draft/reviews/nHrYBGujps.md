## Summary

BIRD-INTERACT addresses a real gap in text-to-SQL evaluation: existing multi-turn benchmarks use static conversation transcripts where every model sees the same predetermined dialogue history, which cannot reward intelligent questioning strategies or penalize poor ones. The paper introduces a dynamic interaction benchmark built on LIVESQLBENCH, featuring (1) a function-driven user simulator that avoids ground-truth leakage, (2) dual evaluation settings (c-Interact for structured conversation and a-Interact for autonomous agentic planning), and (3) 900 tasks covering the full CRUD spectrum. The most striking result is that GPT-5 is the worst model in c-Interact (14.50%) but the best in a-Interact (29.17%), demonstrating that interaction paradigm matters as much as SQL ability.

## Strengths

- **The function-driven user simulator is a concrete technical contribution with strong validation.** The two-stage design — mapping model requests to {AMB, LOC, UNA} before generating responses — is a principled solution to the ground-truth leakage problem that plagues prior LLM-based simulators. The USERSIM-GUARD evaluation (Figure 6, Table 3) shows the function-driven variant reduces leakage failures to 2.7% (vs. 67.4% for baselines), and the human-alignment correlation of 0.84 (p=0.02) validates that it reflects actual human behavior.

- **The two evaluation settings reveal complementary and non-trivial information.** The finding that GPT-5 is the *worst* model in c-Interact (14.50% SR) but the *best* in a-Interact (29.17% SR) is a genuinely interesting result that justifies the dual-setting design. It shows that interaction paradigm matters as much as raw SQL ability and that different models have different aptitudes for different modes.

- **The main results are sobering and honest** — the best model achieves only 25.52% normalized reward. This establishes convincingly that the problem is not solved and points toward strategic interaction skills as the missing capability.

- **The benchmark scope is broader than prior work**, covering DML/DDL operations (INSERT, UPDATE, DELETE, ALTER TABLE) alongside SELECT queries, expanding beyond the read-only scope of benchmarks like Spider and CoSQL.

## Weaknesses

### Fatal

None.

### Major

- **Single-run evaluation with no variance reporting (Section 5, line 163).** All models are evaluated once (temperature=0, 600 tasks each). Even with greedy decoding, the multi-turn interaction involves non-deterministic elements (simulator responses, model reasoning traces). Without standard errors, bootstrap intervals, or even a small repeatability study on the 300-task LITE subset, every comparative claim in Table 2 lacks a reliability estimate. For a benchmark paper whose primary output is model rankings, this makes it impossible to assess whether observed differences (e.g., GPT-5 at 14.50% vs. Deepseek-Chat-V3.1 at 18.50%) are meaningful or within noise. The paper would substantially benefit from at minimum a 3-run repeatability study on a subset.

- **The "ITS Law" claim (Section 5.2, line 207) is not supported by the evidence.** The proposed "law" states that given enough interactive turns, a model's performance can match or surpass its idealized single-turn performance. However, Figure 4 shows this pattern clearly only in c-Interact mode (where performance generally increases with patience). In a-Interact mode, the paper's own caption notes that curves "remain relatively flat or slightly decreases." Elevating what is at best a setting-specific empirical observation to a "law" is an overclaim. Renaming this to "Interaction Test-time Scaling" as an observed phenomenon would be more appropriate.

### Minor

- **The memory grafting experiment (Section 5.2, lines 191-197) has a confound that weakens its interpretive precision.** GPT-5 is given ambiguity-resolution histories from Qwen-3-Coder and O3-mini. Since those histories contain the *correctly resolved answers*, GPT-5's SQL improvement could simply reflect receiving better information, not specifically being freed from a "communication ability" deficit. The experiment remains valuable as evidence that interaction quality matters, but it does not cleanly isolate communication ability as the specific bottleneck.

- **Missing database diversity information.** Table 1 reports "# Distinct Test Cases" (191 for FULL) but not "# Distinct Databases," which is a standard statistic for text-to-SQL benchmarks and relevant for assessing cross-domain generalization claims.

- **No failure mode analysis.** The paper reports success rates but does not break down error distributions (e.g., did the model fail to ask for clarification, ask but receive the wrong information, or ask correctly but generate wrong SQL?). A failure-mode breakdown would substantially increase the benchmark's diagnostic value.

- **The state dependency claim (line 76) is stated but not validated.** The paper says follow-up sub-tasks require reasoning over modified database states, but there is no experiment (e.g., an ablation that resets the database between sub-tasks) confirming that models actually need state tracking rather than simply handling a new question in context.

- **The choice of exactly two sub-tasks per task (n=2, line 46) is declared without justification.** With only one follow-up, the benchmark tests exactly one level of state dependency. This is acknowledged in Future Work but should be discussed as a limitation earlier in the paper.

- **The LLM used as the semantic parser in Stage 1 of the function-driven simulator (Section 3.3) is not disclosed.** Its accuracy directly bounds the simulator's reliability and should be reported.

### Trivial

None.

## Nice-to-Haves

- Report idealized single-turn ("Idealized Performance") numbers as absolute values alongside Table 2, so readers can precisely quantify the added difficulty from interaction.
- Include a failure-mode taxonomy (clarification failures vs. SQL generation failures vs. action-space navigation failures).
- Run the state-dependency ablation to validate that models actually need to track modified database states.

## Removed Points

- **Criticism about LIVESQLBENCH being an "unpublished foundation":** REMOVED per policy — the paper cites BIRD-Team (2025); all cited references are assumed to exist as of the review date.
- **Criticism about ecological validity of injected ambiguities:** REMOVED as speculative — no evidence that injected ambiguities are less representative than naturally occurring ones.
- **Criticism that the paper "speculates" about training data differences causing model ranking reversals:** REMOVED — the paper explicitly says "we hypothesize" (line 187), properly flagging this as conjecture.
- **Generic strength about "the problem being important":** REMOVED as not specific to this paper's contribution.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add variance reporting — even a small repeatability study (3 runs on the LITE subset for 2–3 models) would substantially increase the paper's credibility.
2. Report the absolute single-turn "Idealized Performance" numbers in a main-paper table for direct comparison with interactive results.
3. Reframe the memory grafting experiment to avoid claiming it isolates "communication ability" — present it as a cleaner demonstration that interaction history quality matters.
4. Rename "ITS Law" to "Interaction Test-time Scaling" as an empirical observation rather than a law.

## Score and Decision

This is a solid benchmark paper with well-validated core contributions (the function-driven simulator, the dual evaluation settings) and genuinely informative empirical findings (the model-ranking reversal between c-Interact and a-Interact). The weaknesses are addressable: the "ITS Law" overclaim can be tempered by changing terminology, and the single-run variance concern can be partially addressed with a small repeatability study. The core benchmark and simulator are valuable contributions that the community is likely to adopt.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>