## Summary

This paper introduces BIRD-INTERACT, a benchmark for multi-turn interactive text-to-SQL evaluation. It addresses two real limitations of existing benchmarks: reliance on static conversation transcripts (which cannot reward or penalize a model's own interaction strategy) and a narrow SELECT-only scope that ignores DML/DDL operations. The benchmark provides a function-driven user simulator (two-stage AMB/LOC/UNA action classifier), two evaluation settings (protocol-guided *c*-Interact and agentic *a*-Interact), and 900 tasks covering the full CRUD spectrum. Experiments with 7 frontier LLMs show success rates below 17% on the full set, and a memory grafting experiment isolates communication skill from SQL generation skill.

## Strengths

1. **Problem diagnosis is precise and well-supported (Section 1, lines 26–28).** The paper identifies two concrete deficiencies in prior multi-turn text-to-SQL benchmarks — static conversation transcripts and SELECT-only scope — and the benchmark design follows directly from addressing them. This is not a straw-man critique.

2. **The function-driven user simulator is a principled solution to a known problem (Section 3.3, lines 80–84; Figure 6).** The two-stage approach that maps system queries to a constrained action set (`AMB`, `LOC`, `UNA`) before generating responses cleanly avoids ground-truth leakage and task deviation. Validation on USERSIM-GUARD shows a reduction in failure rate on unanswerable questions from 67.4% (baseline) to 2.7% — compelling evidence that the simulator solves the problem it was designed for.

3. **The memory grafting experiment cleanly isolates a specific capability bottleneck (Section 5.2, Figure 5).** Providing GPT-5 with interaction histories from Qwen-3-Coder and O3-Mini raises its success rate from ~13.8% to 18.8–20.5%, surpassing the donors' own performance (18.5%). This is a genuinely informative diagnostic that separates communication strategy from SQL generation ability.

4. **Human alignment validation is meaningful (Section 6, Table 3).** The 0.84 Pearson correlation (p=0.02) between the function-driven simulator and human judges, versus 0.61 (p=0.14) for the baseline, provides real evidence that the automated evaluation aligns with human judgments.

## Weaknesses

### Fatal
None.

### Major

1. **The "ITS Law" framing and the "monotonically" claim are not supported by the presented evidence.** The introduction (line 36) states that performance "improves monotonically with additional interaction opportunities across multiple models," and Section 5.2 (line 207) defines an "ITS Law." However:
   - Figure 4's own caption states: *"In c-Interact mode, performance generally increases with patience, while in a-Interact mode, it remains relatively flat or slightly decreases."* The pattern does not hold in a-Interact — the primary setting for agentic behavior.
   - Only Claude-3.7-Sonnet is described as exhibiting "clear scaling behavior" (line 203); the other models show weaker or inconsistent trends.
   - Results are from single runs with no variance estimates (line 163), so it is unclear whether observed increases in c-Interact are statistically distinguishable from noise.
   
   The observed pattern is still interesting (suggesting that *how* the interaction budget is structured matters enormously), but calling it a "law" and claiming it holds "across multiple models" in both settings overstates the evidence. The paper should either present more systematic evidence or replace the "law" framing with a precise, setting-specific description.

### Minor

2. **Budget formulas encode information about the number of ambiguities (Section 4, lines 125, 133).** The budget for both evaluation settings is a function of `m_amb` (the annotated number of ambiguities per task). Since systems are "informed of the remaining budget" (line 109), and the patience parameter λ_pat is a known global constant, a model can infer the exact number of ambiguities that need resolution. In real human-AI interaction, neither party knows this count. Furthermore, because the budget scales exactly with task complexity, it simulates a user whose patience perfectly matches each task — not a user with a fixed, realistic patience threshold. The paper does not acknowledge or discuss this limitation.

3. **Single-run evaluation with no variance reporting (Section 5, line 163).** The paper states "conducting single runs due to cost." Many reported differences between models are 1–5% (e.g., GPT-5 vs. Claude-Sonnet-3.7 in c-Interact DM: 25.40% vs. 33.86%). Without multiple runs or any variance estimate, the reader cannot assess whether these differences are meaningful. This is a common constraint in API-based research, but it should be transparently discussed as a limitation rather than simply stated.

4. **No summary comparison with prior benchmarks in the main text (Section 3.4, line 103).** The paper states that "Appendix E" contains a comprehensive comparison showing BIRD-INTERACT is "among the most open, challenging, and long-horizon interactive benchmarks," but the main text provides no summary table comparing key dimensions (number of tasks, interaction length, CRUD coverage, ambiguity types) with COSQL, SParC, LEARN-TO-CLARIFY, or MINT. A brief comparison table in the main body would make the contribution self-contained.

5. **Single debugging opportunity design choice is not motivated (Section 4.1, line 113).** The *c*-Interact setting gives models exactly one debugging attempt per sub-task. The paper explains what this choice is but not why one attempt was chosen over zero or multiple. Since this design decision shapes the difficulty and character of the setting, the rationale should be stated.

6. **Follow-up sub-task difficulty claim is confounded by sequential evaluation (Section 5.1, line 171).** The paper states that "follow-up sub-tasks are noticeably more challenging" but does not note that success on sub-task 2 is conditional on success on sub-task 1 (failure on sub-task 1 terminates the session). This confound is inherent to the design but should be acknowledged when interpreting the "more challenging" claim.

7. **No discussion of whether injected ambiguities resemble natural ones (Section 3.2, lines 62–72).** Ambiguities are systematically injected into originally clear tasks. The paper does not discuss whether the resulting distribution of interaction difficulty, clarification patterns, or failure modes resembles naturally-occurring ambiguous scenarios. A brief limitations paragraph acknowledging the synthetic nature would improve the paper.

8. **State dependency could use a concrete example (Section 3.2, lines 74–76).** The paper introduces "state dependency" between sub-tasks as a novel feature but only states that models must reason over "modified database states or newly created objects." A concrete example (e.g., "after INSERT creates a new row in table X, sub-task 2 queries that row") would clarify this for readers.

### Trivial

9. **Reward weighting placement.** The reward structure weighting (70% priority sub-task, 30% follow-up) is mentioned only in the results discussion (line 173) rather than in the metrics subsection (Section 2, lines 46). Moving it to the metrics definition would improve clarity.

## Nice-to-Haves

- **Controlled experiment with task-independent budget.** Running a subset of tasks with a fixed (ambiguity-count-independent) budget would test whether the budget-ambiguity coupling materially affects results, and would clarify the benchmark's sensitivity to this design choice.
- **Variance estimates for a subset.** Even 3 runs on the LITE set (300 tasks) would give a rough sense of stochasticity and strengthen the empirical claims.
- **Benchmarking a specialized interactive text-to-SQL agent** (e.g., MAC-SQL or DAIL-SQL adapted to this setting) would provide a more informative performance bound and help the community understand whether existing agentic methods transfer to this task.

## Removed Points

- The reviewer's claim that the abstract states the monotonic ITS claim: the actual claim is at line 36 (introduction), not the abstract. The criticism itself (that the claim is unsupported) remains valid and is retained as a Major weakness.
- The reviewer's point about not being able to verify Appendix E: per the meta-review guidelines, appendix content is stripped by the parser and exists in the original submission. The retained Minor weakness (point 4) is about the *main text* lacking a summary table, which is a presentation issue.
- The reviewer's suggestion that the action distribution favoring trial-and-error "could partly reflect an optimal strategy under budget constraints" is an interesting analytical point but is speculative and does not identify a concrete flaw in the paper's methodology. It is not retained as a weakness.
- Dropped generic strengths (e.g., "the problem is important," "timely topic") that lack specific evidence from the paper's content.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Remove or substantially qualify the "ITS Law" framing.** Replace line 207's "Law" with a precise description: e.g., "In the *c*-Interact setting, several models show a positive trend with increased patience (single-run, no variance estimates), while no consistent pattern is observed in *a*-Interact." Drop the "monotonically" claim from line 36.

2. **Add a limitations paragraph** that discusses: (a) the budget-ambiguity coupling and its implications for realism, (b) the single-run nature of the experiments and what conclusions can or cannot be drawn, (c) the synthetic nature of ambiguity injection, and (d) the conditional confound in follow-up sub-task difficulty.

3. **Add a concise comparison table** in the main text (Section 3.4) summarizing how BIRD-INTERACT compares to COSQL, SParC, LEARN-TO-CLARIFY, and MINT on key dimensions (task count, interaction length, CRUD support, ambiguity types, state dependency).

4. **Move the reward weighting** (70/30 split) from the results discussion (line 173) into the metrics definition (Section 2).

## Score and Decision

The benchmark infrastructure — the function-driven user simulator, the two evaluation settings, the ambiguity injection methodology, the validation experiments — is well-designed and constitutes a genuine contribution to the community. The memory grafting experiment is insightful, and the human alignment study provides meaningful validation. These strengths are substantial.

The primary weakness is the overclaiming around the "ITS Law" and "monotonically" framing, which is not supported by the evidence and would be misleading if published as-is. The remaining issues (budget-ambiguity coupling, single-run variance, missing comparison table) are addressable. None of the weaknesses are fatal — the benchmark itself is built on solid methodological foundations.

With the proposed revisions — particularly removing the "law" terminology and adding a candid limitations discussion — the paper would make a strong contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>