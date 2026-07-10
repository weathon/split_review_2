Now I have all the information I need. Let me write the final review.

## Summary

BIRD-INTERACT introduces a benchmark for evaluating LLMs in dynamic, multi-turn text-to-SQL interactions, addressing a genuine gap in existing benchmarks that rely on static conversation transcripts. The paper's core contributions are: (1) a function-driven user simulator that avoids ground-truth leakage issues plaguing LLM-based simulators, (2) two evaluation settings (c-Interact for structured conversation, a-Interact for autonomous agentic planning), and (3) 900 CRUD tasks with 11,796 interactions spanning BI and DM operations. The benchmark reveals that even GPT-5 achieves only 8.67% success in c-Interact and 17.00% in a-Interact, demonstrating substantial room for improvement.

## Strengths

- **The function-driven user simulator is a principled technical contribution.** The two-stage mechanism (semantic parsing to AMB/LOC/UNA actions, then controlled response generation) directly addresses known problems with LLM-as-simulator approaches. The USERSIM-GUARD evaluation (Figure 6) shows the function-driven approach reduces UNA failure rates from 67.4% to 2.7%, a dramatic improvement. The human alignment study (Table 3) showing 0.84 Pearson correlation (p=0.02) vs. 0.61 (p=0.14) for the baseline further supports the simulator's validity (Section 3.3, Section 6).

- **The benchmark fills a real gap.** Existing multi-turn text-to-SQL benchmarks (COSQL, SParC) rely on static conversation transcripts shared across all models, making them unable to measure a model's ability to *drive* an interaction productively. BIRD-INTERACT's dynamic interaction framework is a meaningful step beyond this (Section 1).

- **CRUD coverage is a meaningful expansion.** Existing benchmarks are overwhelmingly SELECT-only. By including INSERT, UPDATE, DELETE, and DDL operations, BIRD-INTERACT covers a broader range of real database work. The BI vs. DM distinction in Table 2 reveals interesting differential performance invisible to single-turn SELECT-only benchmarks.

- **Two evaluation settings with budget constraints are well-designed.** c-Interact and a-Interact probe different axes of capability (structured conversation following vs. autonomous planning). The finding that GPT-5 is worst at c-Interact (14.50%) but best at a-Interact (29.17%) is non-obvious and genuinely informative (Section 5.1).

- **Scale and annotation quality are strong.** 600/300 tasks with 11,796 total interactions, inter-annotator agreement of 93.3–93.5%, and 12 expert annotators (Table 1, Section 3.4).

## Weaknesses

### Major

- **The "ITS Law" claim is unsupported by the evidence.** The paper defines an "ITS Law" (Section 5.2) — that a model satisfies this law if, given enough turns, it can match or surpass idealized single-turn performance. The evidence is limited to Figure 4, which shows data for only 4 models on BIRD-INTERACT-LITE, and the text states that only Claude-3.7-Sonnet "exhibits clear scaling behavior." Calling this a "law" based on one model's behavior on one dataset split is overclaiming. The comparison against "idealized single-turn performance" is also apples-to-oranges: single-turn tasks are unambiguous (all context provided), while interactive tasks start ambiguous, so "matching" the single-turn baseline is an expected ceiling, not a discovery. This should be tempered to an observation or trend.

- **The memory grafting experiment (Section 5.2) does not cleanly isolate communication ability from SQL generation.** GPT-5 improves when given interaction histories from Qwen-3-Coder or O3-Mini, but the "without memory grafting" condition requires GPT-5 to both navigate interaction *and* generate SQL, while the "with memory grafting" condition hands it a clean, already-resolved history. The improvement could simply reflect that generating SQL from a clean history is easier — not necessarily that GPT-5 has a specific communication deficit. A cleaner test would isolate the communication variable (e.g., by giving GPT-5 the same interaction budget with a better prompting strategy). As designed, the experiment mainly confirms that GPT-5's SQL module is decent, which is already known from single-turn benchmarks.

- **Single-run evaluation with no variance reporting is a gap for a benchmark with path-dependent interaction trajectories** (Section 5, line 163). While temperature=0 makes individual LLM calls deterministic, the *interaction trajectory* itself is path-dependent: the model's action at turn t determines what information is available at turn t+1. Without repeated runs or confidence intervals, it is impossible to distinguish genuine performance differences from stochastic path variation. Given the already-low success rates (8.67–29.17%), variance could easily change model rankings. Even cost-prohibitive full reruns could be mitigated by reporting on a subset (e.g., 3 runs on BIRD-INTERACT-LITE for 2–3 models).

### Minor

- **The paper reports only aggregate success rates without a breakdown of failure types.** For a benchmark intended as a diagnostic tool, characterizing whether failures stem from ambiguity detection failure, resolution failure, follow-up failure, or debugging failure would be far more informative. A failure-type taxonomy would substantially increase the benchmark's utility.

## Nice-to-Haves

- **Ablation of simulator components.** The paper does not ablate the function-driven simulator's components (e.g., removing AST-based retrieval for LOC, using a smaller LLM for the semantic parser stage). This would help the community understand which design choices matter most.

- **State dependency analysis.** The paper claims state dependency between sub-tasks as a contribution (Section 3.2) but does not analyze whether follow-up sub-task failures correlate with initial sub-task success or failure.

- **Confidence intervals for the human alignment study** (Table 3). The 0.84 vs. 0.61 comparison on 100 tasks is suggestive but would benefit from interval estimates.

## Removed Points

These points from the input review are removed per filtering rules:

1. **"LIVESQLBENCH accessibility / availability"** — REMOVED (hard rule: do not question existence/availability of cited resources).
2. **"Paper overstates distinction from prior work (COSQL/SParC allow dynamic interaction)"** — REMOVED (factually incorrect: the paper correctly notes these benchmarks use static conversation transcripts).
3. **"Evaluation framework validity concern (simulator knows answer key, budget calibrated to annotations)"** — REMOVED (the paper explicitly addresses this with the LOC action via AST-based retrieval for off-script questions and the tunable λ_pat parameter; the impact scoring model rated this concern at -0.07, indicating it is not a meaningful weakness given the paper's design).
4. **"Cost multipliers deferred to Appendix J"** — REMOVED (standard practice; not a weakness).
5. **"λ_pat justification not given"** — REMOVED (minor; the parameter is clearly defined).
6. **"No evidence for GPT-5 training data hypothesis"** — REMOVED (the paper says "we hypothesize," not "we conclude"; this is appropriate speculative framing).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Tone down the "ITS Law" framing to "ITS observation" or "ITS trend" given the limited evidence (one model, one setting, one split).
2. Add a controlled experiment that provides models with perfect clarifications (bypassing interaction) to isolate whether the bottleneck is SQL generation or interaction quality — this would directly validate what the benchmark measures.
3. Report variance: even 3 runs on BIRD-INTERACT-LITE for 2–3 models would substantially strengthen confidence in model rankings.
4. Add a failure-type breakdown (detection vs. resolution vs. follow-up vs. debugging) to make the benchmark more diagnostically useful.

## Score and Decision

**Calibration summary:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| Spider 2.0 | XmProj9cPs.md | 8.00 | 1 | Yes | Higher-quality benchmark with cleaner claims. BIRD-INTERACT has comparable scale but weaker analytical rigor. |
| MINT | jp3gWrMuIZ.md | 6.75 | 2 | Yes | Similar multi-turn interaction benchmark. BIRD-INTERACT has comparable core contributions but more overclaiming. |
| τ-bench | roNSXZpUDN.md | 6.50 | 2 | Yes | Tool-agent-user interaction benchmark. BIRD-INTERACT is comparable. |
| HoloBench | 5LXcoDtNyq.md | 6.25 | 2 | Yes | Lower anchor. BIRD-INTERACT has stronger core contributions (function-driven simulator, larger scale). |
| TrustSQL | 7ZeoPg3eTA.md | 4.00 | 1 | Yes | Weaker benchmark. BIRD-INTERACT is clearly stronger. |
| DB-GPT-Hub | NmILZXKcOi.md | 3.75 | 1 | Yes | Much weaker. BIRD-INTERACT clearly outranks it. |

Round 1 bracket: 5.5–7.5. Round 2 narrows to 5.5–6.5 based on comparison with MINT (6.75) and HoloBench (6.25). Impact-score comparison: BIRD-INTERACT shares MINT's high-magnitude strengths (principled benchmark design, comprehensive evaluation) but carries additional high-magnitude weaknesses (ITS Law overclaim at -10.00, single-run at -9.89, memory grafting at -9.81) that MINT does not have to the same degree. These pull it below MINT (6.75) but still well above HoloBench (6.25) whose weaknesses (corpus quality, RAG comparison flaws) are more fundamental.

**Final score: 6.0 — Borderline Accept.** The benchmark itself is a solid, needed contribution with a well-designed user simulator and strong validation. However, the paper overclaims on the ITS Law and the memory grafting experiment does not cleanly support its stated conclusion, while the single-run evaluation without variance reporting limits confidence in model rankings. These issues are addressable and do not invalidate the core benchmark contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>