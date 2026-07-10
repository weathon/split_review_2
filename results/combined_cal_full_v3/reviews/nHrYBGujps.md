Here is the final consolidated review:

---

## Summary

This paper introduces BIRD-INTERACT, a benchmark for evaluating LLMs on interactive, multi-turn text-to-SQL tasks. It builds on LIVESQLBENCH by injecting ambiguities into single-turn queries, generating follow-up sub-tasks, and providing a function-driven user simulator that avoids ground-truth leakage. The benchmark supports two evaluation settings (conversational c-Interact and agentic a-Interact), covers the full CRUD spectrum, and includes 900 tasks. Experiments on 7 frontier models show very low success rates (e.g., GPT-5 at 8.67% in c-Interact and 17.00% in a-Interact), demonstrating that current models' strong single-turn SQL performance does not transfer to interactive settings.

## Strengths

- **Function-driven user simulator (Section 3.3).** The two-stage pipeline—mapping system queries to constrained symbolic actions (AMB, LOC, UNA) before generating responses—addresses the known problems of ground-truth leakage and task drift in LLM-based simulators. Validation on USERSIM-GUARD (Figure 6) shows failure rates on unanswerable questions dropping from up to 67.4% to 2.7%, a concrete and measurable improvement.

- **Human-alignment study (Table 3).** The function-driven simulator achieves a Pearson correlation of 0.84 (p=0.02) with human success rates across 100 tasks, compared to 0.61 (p=0.14) for the baseline—the baseline correlation is not statistically significant while the function-driven version is. This provides genuine evidence that the simulator approximates real user behavior.

- **Core empirical finding (Table 2).** GPT-5 completes only 8.67% of tasks in c-Interact and 17.00% in a-Interact. This striking result demonstrates that strong single-turn SQL performance does not transfer to interactive settings, precisely the kind of finding a benchmark should surface to motivate further research.

- **Two complementary evaluation settings (c-Interact / a-Interact).** The distinction between protocol-guided conversation and autonomous agent interaction captures qualitatively different failure modes. The observation that models have different relative strengths across modes (e.g., GPT-5 worst in c-Interact, best in a-Interact) would not emerge from a single setting.

- **Full CRUD coverage.** Including INSERT/UPDATE/DELETE/DDL operations (190 DM tasks in the FULL set, Table 1) moves beyond the SELECT-only scope of prior benchmarks and addresses a genuine gap in evaluation coverage.

## Weaknesses

### Fatal
None.

### Major

- **Single-run evaluations with no variance reporting (line 163: 'conducting single runs due to cost').** No standard deviations, confidence intervals, or statistical tests are reported for any model comparison. With success rates in the 8–29% range, absolute differences of a few percentage points between models (e.g., GPT-5 at 14.50% vs. Deepseek-Chat-V3.1 at 18.50% in c-Interact Priority) may not be reliable. While the benchmark itself is the primary contribution and model evaluations are illustrative, this limits the strength of comparative claims between models.

- **The ambiguity injection methodology is synthetic, but the paper frames the benchmark as restoring 'realism' without acknowledging this limitation (abstract line 9; Section 3.2).** The benchmark is constructed by taking clear single-turn tasks and deliberately breaking them via injected ambiguities with known clarification sources and predetermined reconstruction paths (lines 62–72). This tests a model's ability to resolve *designed, annotated types of ambiguity*, which is not the same as handling *naturally occurring ambiguity* where clarification paths are unknown and not governed by annotation. Controlled injection is a defensible methodological choice for avoiding confounds, but the paper overstates what the construction supports.

- **The 'ITS Law' (line 207) is not supported by the evidence presented.** The paper defines this as a general principle that 'given enough interactive turns, its performance can match or even surpass that of the idealized single-turn task.' However, only one model (Claude-3.7-Sonnet) is described as showing 'clear scaling behavior' (line 203), and this is observed only in the c-Interact setting—the Figure 4 caption itself states that a-Interact performance 'remains relatively flat or slightly decreases.' Calling a single observation from one model in one setting a 'law' is a significant overstatement.

### Minor

- **The memory grafting experiment (Section 5.2, Figure 5) shows that GPT-5 benefits from good interaction histories produced by other models, but the interpretation that this specifically diagnoses a 'communication deficit' in GPT-5 is indirect.** The experiment demonstrates that GPT-5 can leverage pre-cleaned histories, not necessarily that its SQL generation is robust or that its communication is specifically deficient. A more direct test would compare SQL accuracy on ambiguity-free queries across models.

- **No error analysis or categorization of failures.** Given the very low success rates (most models <25%), understanding whether failures stem from (a) inability to ask the right clarification questions, (b) inability to interpret simulator responses, (c) inability to generate correct SQL after clarification, or (d) context-length issues would significantly increase the benchmark's utility for guiding future method development.

- **Context length as a confound is not analyzed** despite the paper noting that follow-up sub-tasks are harder 'likely because the longer, concatenated context in these turns remains a bottleneck' (line 171). No breakdown of whether degradation correlates with interaction length or context window size is provided, leaving this important observation unsubstantiated.

### Trivial
None.

## Nice-to-Haves

- Report variance on the LITE set: running 2–3 models (one closed-source, one open-source) with multiple seeds on BIRD-INTERACT-LITE to calibrate reader expectations about noise levels in the FULL-set results.
- Add a paragraph in Section 3.2 or a limitations subsection acknowledging the distinction between *controllable evaluation* (what injected ambiguities provide) and *naturalistic simulation*, clarifying what the current construction does and does not capture.
- Replace "ITS Law" with "observed scaling trend" or "interaction benefit pattern" and report which models exhibit the pattern across both settings.

## Removed Points

- *Criticism about the "designed personally" phrase (line 187):* Removed as a typographic nitpick per hard rules.
- *Criticism about reliance on appendix details (AST retrieval in Appendix N, prompts in Appendix R):* Removed per hard rules—appendix content is removed by the parser and exists in the original submission.
- *Criticism about the framing of static conversation transcripts being "slightly overbroad":* This is a subjective observation about nuance in presentation, not a concrete weakness.
- *Note about the discrepancy between Figure 5's 13.8% and Table 2's 14.50%:* The difference (0.7 percentage points) is within expected noise for single-run evaluations and does not materially affect any conclusion.

## Novel Insights

The most insightful observation from the review process is that the paper's three main concerns (single-run variance, synthetic ambiguity framing, and ITS Law overclaim) all relate to the calibration between what the paper claims and what the evidence supports. The core benchmark contribution—the function-driven simulator, the interactive evaluation framework, the CRUD coverage—is solid and well-validated. The paper would be strongest if it leaned into its genuine strengths (which are considerable) rather than overclaiming on the "realism" framing or elevating a suggestive observation to a "law."

## Suggestions

1. Report at least 2–3 runs on the LITE set for a subset of models (e.g., one open-source and one closed-source) to calibrate readers' expectations about noise levels in the FULL-set results.
2. Add a limitations paragraph in Section 3.2 discussing what injected ambiguities do and do not capture about natural ambiguity, and distinguish between *controllable evaluation* and *naturalistic simulation*.
3. Replace "ITS Law" with "observed scaling trend" or "interaction benefit pattern" and report which models exhibit the pattern across both settings.

---

**Calibration Report.** Anchors retrieved across rounds:

| Path | Avg Score | Round | Itemized? | Comparison to this paper |
|------|-----------|-------|-----------|-------------------------|
| Spider 2.0 (XmProj9cPs) | 8.00 | R1 | Yes | Higher-quality text-to-SQL benchmark with real enterprise data; fewer methodological concerns. This paper below it. |
| τ-bench (roNSXZpUDN) | 6.50 | R1 | Yes | Similar interactive user-simulator benchmark; comparable score range. This paper has stronger simulator validation but additional framing concerns. |
| MINT (jp3gWrMuIZ) | 6.75 | R1 | Yes | Multi-turn interaction benchmark; comparable in scope and weakness severity. This paper's weaknesses are slightly less severe than MINT's most negative items. |
| WildBench (MKEHCx25xp) | 7.33 | R1 | Yes | LLM benchmark from real user data; different domain so less directly comparable. |
| HoloBench (5LXcoDtNyq) | 6.25 | R2 | Yes | Database reasoning benchmark; its weaknesses (favorability 0.15–2.70) were more severe than this paper's, supporting placement above it. |
| CHASE-SQL (CvGqMD5OtX) | 6.25 | R2 | No | Text-to-SQL method paper, less comparable. |
| DB-GPT-Hub (NmILZXKcOi) | 3.75 | R1 | No | Text-to-SQL benchmark/toolkit with lower scores; not directly comparable. |

**Bracketing: R1 bracket estimated at [5.5, 7.5]** based on comparison with τ-bench (6.50) and MINT (6.75) as closest methodological neighbors. **Narrowing (R2):** Comparison against HoloBench (6.25, with weakness favorabilities as low as -2.18 and 0.15) confirmed this paper's weaknesses are less severe, while comparison with Spider 2.0 (8.00) confirmed this paper's weaknesses are more significant. Final score of **6.5** reflects a paper with genuinely strong contributions (function-driven simulator with human validation, CRUD coverage, striking empirical findings) but held back from the 7+ range by overclaiming (ITS Law, realism framing) and single-run evaluations.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>