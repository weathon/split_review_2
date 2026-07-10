I've verified the key claims against the paper. Now I'll produce the final consolidated review.

---

## Summary

BIRD-INTERACT addresses a genuine gap in text-to-SQL evaluation by introducing a benchmark for dynamic, multi-turn interaction. Its core contributions are: (1) a function-driven user simulator that avoids ground-truth leakage, (2) two evaluation settings (c-Interact for protocol-guided conversation and a-Interact for agentic exploration), and (3) a task suite covering the full CRUD spectrum with 600 tasks involving injected ambiguities and follow-up sub-tasks. The benchmark reveals that even GPT-5 achieves only 8.67–17.00% success, demonstrating substantial headroom for future work.

## Strengths

- **Addresses a genuine limitation of static multi-turn benchmarks.** Correctly identifies that existing datasets (COSQL, SParC, etc.) present every model with the same static conversation transcript regardless of what clarification questions that model would actually ask (Section 1, paragraph 3). This is a well-motivated problem.

- **Function-driven user simulator with strong ground-truth leakage prevention.** The two-stage design (semantic parser → AMB/LOC/UNA action → controlled response) is a practical engineering contribution. The USERSIM-GUARD evaluation (Figure 6) shows conventional simulators fail to reject unanswerable questions up to 67.4% of the time, while this approach reduces failures to 2.7%.

- **Human-alignment evidence for the simulator.** Table 3 shows the function-driven simulator achieves Pearson r=0.84 (p=0.02) with human users versus 0.61 (p=0.14) for the baseline, providing direct evidence that the simulator produces model rankings that match human interaction patterns.

- **Genuinely challenging benchmark.** Even GPT-5 achieves only 8.67% (c-Interact) and 17.00% (a-Interact) on the full set, leaving substantial headroom for future work (Table 2). The hard benchmark is a desirable property.

- **Full CRUD coverage.** Including DML and DDL operations alongside SELECT queries meaningfully expands beyond existing text-to-SQL benchmarks (Section 1, Table 1).

## Weaknesses

### Major

- **Memory grafting experiment conflates communication strategy and SQL content (Section 5.2, Figure 5).** The experiment provides GPT-5 with ambiguity-resolution histories from Qwen-3-Coder and O3-Mini, then concludes GPT-5 has "robust SQL generation capabilities" but "deficient communication." However, these histories contain both the interaction dialogue and the resulting SQL solutions (or strong hints about them), so the design cannot separate the benefit of better interaction strategy from that of SQL content leakage. Additionally, the baseline comparison is unclear: GPT-5's "without memory grafting" baseline of 13.8% does not match its reported 14.50% Priority Question SR in Table 2, and the experimental conditions (which subset?) are not specified. The causal claim about communication deficiency is not supported by this experimental design.

- **The "ITS Law" claim overreaches the evidence (Section 5.2, Figure 4).** The paper defines an "ITS Law" as: "A model satisfies this law if, given enough interactive turns, its performance can match or even surpass that of the idealized single-turn task." No model is shown to actually cross that threshold, and the data only spans four patience levels (0, 3, 5, 7) on four models. Calling this a "law" is overwrought for the empirical trend shown — the data is better characterized as "some models benefit from more turns, especially in c-Interact mode." For a benchmark paper that sets evaluation standards, this overclaiming weakens credibility.

### Minor

- **Single-run evaluation (Section 5).** The paper states "conducting single runs due to cost." With success rates as low as 8–25% and stochastic model behavior (LLM-based reasoning steps), single runs provide no variance estimates. It is impossible to assess whether the reported differences between models (e.g., 22.00% vs. 22.33% SR) are reliable. At minimum, 3 trials on the 300-task LITE set would provide error bars.

- **GPT-4o appears in Figure 4 but not in Table 2.** The ITS experiment (Figure 4) evaluates GPT-4o alongside three other models on the LITE set, but the main results (Table 2) do not include GPT-4o at all. The paper does not explain this inconsistency, raising questions about whether different conditions or model selections were used across experiments.

- **Pre-annotated ambiguity space limits the "dynamic" claim.** The benchmark's interaction space is determined by pre-annotated ambiguities paired with clarification sources from ground-truth SQL. The user simulator can only respond through AMB() queries that map onto these annotations. This creates a curated interaction space rather than truly free-form underspecification. The paper acknowledges the need for controllability ("To make annotation and evaluation controllable") but uses broader language ("restores this missing realism") that is not fully supported by this design. For a benchmark, controlled evaluation is acceptable — but the claims should be calibrated accordingly.

### Trivial

None.

## Nice-to-Haves

- Add variance estimates (at minimum 3 trials on the LITE set).
- Reformulate the memory grafting experiment to isolate the communication channel (e.g., provide clarification dialogue without the resulting SQL).
- Replace the "ITS Law" framing with a more measured empirical characterization.
- Clarify the relationship with LIVESQLBENCH: quantify what is inherited vs. new, and describe annotation effort in person-hours.
- Correct the "900 tasks" claim: there are 600 unique tasks, with LITE as a subset; stating "900" cumulatively is misleading.
- Specify what LLM powers the semantic parsing stage of the user simulator during benchmark evaluation (not just during USERSIM-GUARD validation).

## Removed Points

These points from the input review are flagged to be removed; treat them with caution.

- **Weakness about the correlation analysis sample underspecification.** The critic questioned whether Pearson r is computed over 7 or 700 data points, and called p-values "marginal." However, r=0.84 with n=7 yields t≈3.48, p≈0.018 — this is consistent with the reported p=0.02 and is a valid result. The baseline's p=0.14 and p=0.21 are non-significant, which supports rather than undermines the paper's claim that the function-driven approach is better.

- **Weakness about 900 vs. 600 tasks.** This is factually correct (the paper inflates task count) but belongs as a presentation fix in Suggestions, not a standalone weakness, since the actual benchmark has 600 unique tasks which is still substantial.

- **Weakness about LIVESQLBENCH relationship being underspecified.** The paper does state it builds on LIVESQLBENCH and says "our primary contribution is to convert this static benchmark into a dynamic, interactive setting." The issue is one of quantification (what's new vs. inherited) rather than omission — moved to Suggestions.

- **The original "ambiguity injection limits realism" framed as a Critical Issue.** The paper explicitly acknowledges this is for controllability, and it is a standard trade-off in benchmarks. Rephrased as a Minor weakness with calibrated language.

## Novel Insights

The observation that LLMs over-favor direct trial-and-error execution (submit → error feedback) over systematic knowledge retrieval (Section 5.2, Action Distribution Patterns) is a genuinely non-obvious finding that emerges from the benchmark's dual-setting design and warrants further investigation. The finding that different models show opposite strengths in c-Interact vs. a-Interact (GPT-5 worst in c-Interact, best in a-Interact) is also interesting and suggests that interaction mode compatibility is a real factor.

## Suggestions

1. **Fix the memory grafting experiment.** Provide GPT-5 with interaction histories that contain only the clarification dialogue but withhold the resulting SQL. This would isolate whether the improvement comes from better communication strategy or SQL content leakage. If infeasible, acknowledge the confound explicitly.

2. **Replace the "ITS Law" with an honest empirical trend.** Present the patience-vs-performance data as "some models benefit from more interaction turns, especially in c-Interact mode; others plateau." This is more accurate and more interesting.

3. **Add variance estimates on the LITE set.** Three repetitions would cost ~3× the LITE evaluation cost but would provide crucial error bars for the community to trust the rankings.

4. **Clarify task counting.** State clearly that there are 600 unique tasks, with LITE being a 300-task subset, rather than implying 900 independent tasks.

5. **Explain the GPT-4o inconsistency.** Either add GPT-4o to Table 2 or clarify why it was included in Figure 4 but not the main results.

---

## Calibration Report

**Round 1 brackets (all anchors with avg human scores):**

| Score Band | Anchor | Avg Score | Relevance | Itemized? |
|---|---|---|---|---|
| <1.5 | 5kMwiMnUip.md (jailbreaking) | 1.40 | Low | No |
| <1.5 | P49gSPmrvN.md (discourse vis.) | 1.00 | Low | No |
| <1.5 | 8QTpYC4smR.md (LLM survey) | 1.00 | Low | No |
| 1.5–3.5 | ReKWjKvkJE.md (struct-guided SQL) | 3.40 | Medium | No |
| 1.5–3.5 | lMW9d1AqC9.md (sign-to-SQL) | 1.67 | Low | No |
| 1.5–3.5 | BltaWJZMeR.md (DataSciBench) | 3.20 | High | Yes |
| 3.5–5.5 | NmILZXKcOi.md (DB-GPT-Hub) | 3.75 | Medium | No |
| 3.5–5.5 | 7ZeoPg3eTA.md (TrustSQL) | 4.00 | High | Yes |
| 3.5–5.5 | NfUHBaZdLw.md (EvoSchema) | 4.25 | Medium | No |
| 5.5–7.5 | CvGqMD5OtX.md (CHASE-SQL) | 6.25 | Medium | Yes |
| 5.5–7.5 | BAglD6NGy0.md (ROUTE) | 6.25 | Medium | No |
| 5.5–7.5 | RaSLSUCKz0.md (SQL-GEN) | 5.67 | Low | No |
| 7.5–8.5 | XmProj9cPs.md (Spider 2.0) | 8.00 | High | Yes |
| 7.5–8.5 | GGlpykXDCa.md (MMQA) | 8.00 | Low | No |
| 7.5–8.5 | jOmk0uS1hl.md (train-on-test-task) | 8.00 | Low | No |

**Round 2 — refinement inside (5.5, 7.5):**

| Anchor | Avg Score | Relevance | Itemized? |
|---|---|---|---|
| roNSXZpUDN.md (τ-bench) | 6.50 | High | Yes |
| 5LXcoDtNyq.md (HoloBench) | 6.25 | Medium | Yes |
| WYdpjwKQma.md (LAIA-SQL) | 5.00 | Low | No |
| iSTMsye6SD.md (KIR benchmark) | 5.25 | Low | No |

**Round 1 bracket:** The paper sits between 3.5 and 7.5. It is clearly stronger than DataSciBench (3.20) and TrustSQL (4.00) — both of which had fundamental pipeline validity issues or limited domain coverage that BIRD-INTERACT avoids. It is weaker than Spider 2.0 (8.00), which had nearly flawless reviews and a larger paradigm shift. Initial bracket: **5.5–7.0**.

**Round 2 narrowing:** Comparing against τ-bench (6.50) — the most comparable interactive benchmark — BIRD-INTERACT has similarly high-strength favorability ratings (9–13) on its core contributions. However, τ-bench's weaknesses are about inherent simulation limitations (favorability ~4.5), while BIRD-INTERACT's most damaging weakness items (the memory grafting confound at favorability 2.72, the single-run evaluation at -1.50, and the ITS Law overclaim at -0.25) are experimental design issues that reflect more directly on the paper's own claims. HoloBench (6.25) has weaknesses as low as -2.46 favorability but also has fewer high-favorability strengths. On balance, BIRD-INTERACT is below τ-bench but roughly on par with or slightly above HoloBench.

**Final score: 6.0.** The paper has strong, well-evidenced contributions (simulator design, human alignment, benchmark difficulty) that the community would find valuable. However, two overclaims (ITS Law, memory grafting interpretation) and the single-run evaluation prevent it from reaching the 6.5+ tier. These issues are fixable in revision — variance estimates, experimental redesign, and claim calibration would substantially strengthen the paper.

---

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>