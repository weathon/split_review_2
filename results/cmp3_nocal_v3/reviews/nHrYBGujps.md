## Summary

This paper introduces BIRD-INTERACT, a benchmark for evaluating text-to-SQL systems in dynamic, multi-turn interaction settings. It contributes a function-driven user simulator that maps system queries to constrained actions (AMB/LOC/UNA) to avoid ground-truth leakage, two evaluation settings (protocol-guided c-Interact and autonomous a-Interact), and a 900-task suite spanning CRUD operations. Empirical results show that even GPT-5 completes at most 17% of tasks end-to-end, and reveal that model rankings reverse across interaction paradigms.

---

## Strengths

- **The gap is real and well-motivated.** Section 1 precisely identifies two concrete failures of existing multi-turn benchmarks: (a) they use static conversation transcripts rather than dynamic interaction, and (b) they restrict to SELECT-only queries. The diagnosis that "every LLM is evaluated against the same predetermined dialogue trajectory" points to a genuine limitation that the benchmark directly addresses.

- **The function-driven user simulator is a substantive methodological contribution.** The two-stage approach (semantic parsing into AMB/LOC/UNA actions, then generating responses from ground-truth SQL with clarification source) tackles the known ground-truth leakage and task-deviation problems with LLM-based simulators. The validation is compelling—reducing UNA failure rates from 67.4% to 2.7% on USERSIM-GUARD (Figure 6), and achieving a Pearson correlation of 0.84 with human evaluators vs. 0.61 for baselines (Table 3, p=0.02). This is likely the most reusable component of the paper.

- **The dual evaluation settings are well-designed and produce non-trivial findings.** The distinction between c-Interact (protocol-guided) and a-Interact (agentic) maps to genuinely different deployment scenarios, and the results verify that model rankings differ across settings—GPT-5 performs worst in c-Interact (14.50% SR) but best in a-Interact (29.17% SR). This demonstrates the two settings measure different capabilities.

- **Several empirical findings are concrete and potentially influential.** That GPT-5 underperforms in the more structured c-Interact setting despite excelling in single-turn benchmarks, that the memory grafting experiment isolates a communication deficit from a generation deficit, and that models favor costly trial-and-error over systematic exploration—these are falsifiable observations that can drive future research on interaction strategy.

---

## Weaknesses

### Fatal

None.

### Major

- **Single-run evaluation without variance reporting limits the reliability of model comparisons.** The paper states (line 163): "All models use temperature=0 and top_p=1, with default reasoning settings, conducting single runs due to cost." For a benchmark whose empirical contribution includes ranking models across settings, this is a significant limitation. With absolute success rates mostly between 8% and 30% on a 600-task suite, small absolute differences separate adjacent models (e.g., c-Interact follow-ups: Claude-Sonnet-3.7 at 8.33% vs. Deepseek-Chat-V3.1 at 8.50%—a difference of one task outcome). While temperature=0 reduces stochasticity, it does not eliminate all sources of variance (API-level non-determinism, floating-point ordering, etc.), and the absence of any repeated trials or confidence intervals makes it impossible to assess whether reported differences are systematic or noise. The paper would be substantially stronger if it ran each model at least 3 times on the LITE set (300 tasks, ~$90/model at reported costs) and reported mean/variance, or if it explicitly refrained from fine-grained ordinal claims.

- **State dependency is foregrounded as a key contribution but is not evidenced in the main paper.** Section 3.2 states (line 76): "A key contribution of our benchmark is the introduction of state dependency between sub-tasks… System models must reason over modified database states or the newly created objects (e.g. tables) from preceding queries to write SQLs for follow-up sub-tasks." This is a genuinely novel property that distinguishes BIRD-INTERACT from prior multi-turn benchmarks. However, the main paper provides no statistics on what fraction of tasks have this property, no worked example showing non-trivial state dependency, and no analysis of whether model failures on follow-up tasks correlate with state dependency. Table 1 does not include a "state-dependent tasks" row. Given that this is claimed as a key contribution, the evidence in the main text is too thin.

- **Follow-up sub-task difficulty is attributed primarily to context length while other confounding factors are not disentangled.** The paper notes (line 171) that follow-up sub-tasks "are noticeably more challenging, likely because the longer, concatenated context in these turns remains a bottleneck." But follow-up sub-tasks differ from priority sub-tasks in at least three conflated ways: (a) longer context from prior interaction, (b) potential state dependency from the priority sub-task's SQL execution, and (c) partial consumption of the interaction budget. Without controlled experiments (e.g., resetting context between sub-tasks, or controlling for state dependency), it is unclear which factor drives the difficulty drop.

### Minor

- **The memory grafting experiment would benefit from a reverse control.** The experiment (Section 5.2) shows GPT-5 improves when given interaction histories from Qwen-3-Coder or O3-Mini, supporting the conclusion that GPT-5 has a communication deficit. However, the reverse condition (feeding GPT-5's history to Qwen-3-Coder or O3-Mini) is not run. Without this control, the experiment is consistent with the stated interpretation but does not rule out the alternative that GPT-5 simply produces *less informative* histories (a subtly different deficit about what questions to ask rather than about understanding responses). Adding the reverse condition would sharpen the conclusion.

- **The paper does not discuss failure modes of the user simulator.** The USERSIM-GUARD evaluation (Figure 6) shows the simulator achieves ~90%+ accuracy on AMB and LOC, meaning it fails 5-10% of the time. When it misclassifies an AMB as UNA (or vice versa), what happens to the evaluation of the downstream task? A brief discussion of failure modes and their impact on measured success rates would strengthen confidence in the benchmark.

- **The abstract could more clearly distinguish end-to-end task completion from priority sub-task success.** The abstract states GPT-5 "completes only 8.67% of tasks" in c-Interact. This is correct (Follow Ups SR = 8.67% in Table 2), but a reader could infer this refers to priority tasks (14.50%). A parenthetical clarification ("end-to-end completion of both sub-tasks") would prevent confusion.

- **The budget formula for c-Interact (τ_clar = m_amb + λ_pat) does not explicitly state whether the single debugging re-submission consumes from the clarification budget.** The paper notes debugging incurs a "reward penalty" (line 123) but does not clarify whether it also reduces the available clarification turns. If debugging is outside the budget, the constraint primarily governs clarification, not total interaction. This should be made explicit.

### Trivial

None.

---

## Nice-to-Haves

- Run multiple trials (at least 3) on the LITE set and report mean/variance, or explicitly qualify that fine-grained model comparisons may not be statistically reliable.
- Add an "information-seeking agent" baseline that systematically asks about all ambiguities before generating SQL, establishing a "diligent interaction" upper bound.
- Report per-task success rates across models to identify which tasks are most/least discriminative, helping future users select informative subsets.

---

## Removed Points

These points were raised in the original review but are removed for the following reasons:

- **c-Interact protocol prompting is underspecified**: The paper references Appendix R for detailed prompts; the appendix is stripped by the parser and exists in the original submission. The main-text description (lines 111-128) provides adequate high-level specification for a benchmark paper.
- **Quality control for ambiguity injection needs more detail**: Referenced to Appendix H, which is stripped. Exists in the original submission.
- **ITS Law discussion is too brief**: Subjective judgment about depth of analysis; the paper presents the empirical finding and Figure 4, which is sufficient for a first characterization.
- **Table 2 cost comparison confusion**: The paper clearly states "Avg. Cost is the cost for one task on average in USD. Our user simulator has an avg. cost of 0.03 USD." The note merely informs the reader of the simulator's cost component; it does not confuse per-row comparisons.
- **Related Work nuance about COSQL**: Subjective opinion about positioning nuance; not a substantive weakness.
- **Per-task variance not reported / information-seeking agent baseline not included**: These are suggestions for extension, not weaknesses; moved to Nice-to-Haves.
- **Budget/debugging overlap**: Partially answerable from the paper text (debugging incurs reward penalty, budget constrains clarification turns), already retained as a Minor point above for the remaining ambiguity.

---

## Novel Insights

The harsh review's analysis sharpens two insights that go beyond the paper's own contributions. First, the single-run critique identifies that the benchmark's most headline-worthy findings (model ranking reversals across c-Interact vs. a-Interact) are presented without any variance characterization, making it impossible to separate signal from measurement noise—a concern that applies even to temperature=0 evaluations in practice. Second, the observation that the state dependency contribution is claimed but unquantified in the main text is a specific, actionable weakness: the paper would be materially stronger if it simply reported what fraction of its 600 tasks actually require reasoning over modified database states, and whether this correlates with model failure on follow-up tasks.

---

## Suggestions

1. Run at least 3 trials on the LITE set (300 tasks) and report mean success rates with variance—this is the single highest-leverage improvement for the paper's reliability as a benchmark.
2. Add a row to Table 1 (or a new table) reporting how many tasks have genuine state dependency, and separate follow-up success rates by whether the follow-up depends on prior state or not.
3. Add the reverse memory grafting control (feed GPT-5's history to Qwen-3-Coder/O3-Mini) to sharpen the communication-deficit interpretation.
4. Clarify in Section 4.1 whether the debugging re-submission consumes from the clarification budget or is outside it.
5. Add a brief paragraph discussing user simulator failure modes and their downstream impact on task evaluation.

---

**MY FINAL SCORE:** <score>6.0</score>
**MY FINAL DECISION:** <decision>Accept</decision>