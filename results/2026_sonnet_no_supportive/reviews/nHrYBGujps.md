Now let me draft the review and then calibrate.## Summary
BIRD-INTERACT is a benchmark for evaluating LLMs in dynamic, multi-turn text-to-SQL tasks. It extends LIVESQLBENCH with ambiguity injection, CRUD-complete follow-up sub-tasks with state dependency, and a two-stage function-driven user simulator that constrains action selection to prevent ground-truth leakage. Two evaluation modes are proposed: c-Interact (conversational, protocol-guided) and a-Interact (agentic). Evaluated across 7 frontier models on 600 full-set tasks, the best models achieve only 17–29% success rate, with empirical analysis including Interaction Test-Time Scaling (ITS) and a memory grafting experiment to diagnose interaction bottlenecks.

## Strengths
- **Function-driven simulator with demonstrated robustness (Figure 6, Section 6):** The two-stage design (semantic parsing to one of AMB/LOC/UNA, then controlled generation) reduces UNA failure rates from up to 67.4% (baseline simulators) to 2.7%. This is a qualitative robustness improvement directly relevant to benchmark validity, not a marginal one.
- **Human-alignment validation (Table 3):** The paper goes beyond intrinsic simulator evaluation to report Pearson correlations with human-user success rates across 7 models on 100 tasks. The function-driven approach achieves r=0.84 (p=0.02) vs. r=0.61 (p=0.14, not statistically significant) for the baseline — a higher bar than most benchmark papers attempt.
- **Memory grafting diagnostic (Figure 5):** Providing GPT-5 with interaction histories from O3-Mini or Qwen-3-Coder (which outperform GPT-5 in c-Interact) yields SR improvements of 6.7–20.5% relative, isolating interaction strategy as the bottleneck rather than SQL generation ability. GPT-5 using O3-Mini's history (20.5%) even exceeds O3-Mini's own SR (18.5%), revealing a clean decomposition of interaction skill vs. generation capability.
- **CRUD coverage and state-dependency (Sections 3.1–3.2):** Explicit inclusion of DML/DDL operations and state-dependent follow-up sub-tasks (where sub-task 2 depends on DB state modified by sub-task 1) meaningfully distinguishes BIRD-INTERACT from SELECT-only predecessors and is implemented with a principled 5-category taxonomy.
- **Benchmark difficulty and scale (Table 2):** Success rates of 8–29% across GPT-5, Claude-Sonnet-4, and Gemini-2.5-Pro on 600 tasks (up to 11,796 total interactions) demonstrate the benchmark is not saturated and leaves substantial room for progress.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- **Statistical fragility of the human-alignment correlation (Table 3):** The correlation is computed over 7 system models (one data point per model). At n=7, a 95% confidence interval around r=0.84 stretches from roughly 0.25 to 0.98 — extremely wide. The paper presents this as strong evidence of alignment without acknowledging this limitation. Clarifying whether correlation is at the model level (n=7) or task level (n=100), and reporting a confidence interval, is necessary for readers to calibrate trust in this result.
- **a-Interact non-scaling finding underanalyzed (Figure 4, bottom row):** The c-Interact rows show monotonic improvement with increasing user patience (ITS Law). The a-Interact rows are flat or slightly decreasing. The paper briefly attributes this to trial-and-error bias (Section 5.2) and defers a free-mode experiment to Future Work (Section 8), but does not check whether agents are exhausting their budgets unproductively vs. failing due to poor early decisions. The ITS claim ("validates the importance of effective interaction") is only cleanly supported for c-Interact; the divergence with a-Interact should be treated as a primary finding rather than a secondary observation.
- **Single-run evaluation without variance estimates (Section 5):** At 8.67% SR on 600 tasks, the 95% CI is approximately ±2.3 percentage points; at 300 tasks (LITE), it widens further. Differences between closely ranked models (e.g., GPT-5 at 14.50% vs. DeepSeek at 18.50% priority SR in c-Interact) may not be statistically distinguishable. No standard errors or significance tests are reported for any model comparison.

### Trivial
- The LOC() action (handling clarifications outside pre-annotated ambiguities via AST-based retrieval) is described in one sentence in the main text and deferred entirely to Appendix N. Given that LOC() determines how flexibly the simulator handles unanticipated but legitimate questions, a brief characterization in the main text would improve transparency.

## Nice-to-Haves
- Connect the action distribution analysis (60.87% concentration on *submit* and *ask*, Section 5.2) directly to the a-Interact non-scaling finding — e.g., show that models with more budget simply use additional budget for *submit* (trial-and-error) rather than *knowledge retrieval*, quantifying how much of the gap is attributable to this. This would unify the ITS Law and action distribution findings into a coherent narrative.
- Briefly summarize in the main text what makes O3-Mini/Qwen-3-Coder interaction histories better than GPT-5's (currently deferred to Appendix P), since this makes the memory grafting finding actionable.
- A simple check (what fraction of a-Interact episodes exhaust their budget) would clarify whether agents fail due to hard budget constraint or due to poor early-turn decisions.

## Removed Points
*These points are flagged as removed — treat them with caution.*

- **BI vs. DM confound:** The harsh critic suggested the BI/DM performance gap may be due to SQL length differences (Table 1: 361 tokens/SQL for LITE vs. 252 for FULL) rather than domain difficulty. While plausible, the paper's explanation (BI requires complex business-logic reasoning) is an equally reasonable hypothesis. This is not a verifiable flaw but a confounding variable. Removed as a weakness; noted as a potential caveat.
- **USERSIM-GUARD judge circularity:** The critic raised concerns about using Qwen3-235B-A22B as the sole LLM judge for USERSIM-GUARD. However, the dataset is labeled by human experts and the judge evaluates simulator accuracy against those labels — the circularity concern is limited. Removed as a standalone weakness.

## Novel Insights
The memory grafting experiment elegantly decomposes interaction skill from SQL generation capability: GPT-5 grafted with O3-Mini's interaction history outperforms O3-Mini itself, suggesting that these capabilities are partially separable in frontier LLMs and that interaction strategy — not core generation — is currently the bottleneck for c-Interact. The divergence between c-Interact (ITS holds: more budget monotonically helps) and a-Interact (ITS fails: more budget does not help or slightly hurts) is a genuinely actionable insight: agentic models, when given more budget, appear to waste it on trial-and-error rather than converting it into information gain, pointing to a specific training gap in budget-aware planning.

## Suggestions
- Report whether Table 3's Pearson correlation is at the model level (n=7) or task level (n=100), and add a 95% confidence interval. This is a small addition that substantially changes interpretation.
- In Section 5.2, add a budget-exhaustion analysis for a-Interact: what fraction of episodes exhaust the full budget, and what action types dominate in those exhausted episodes? Connect this to the action distribution finding.
- Report standard errors or confidence intervals for key model-level comparisons in Table 2, particularly for models within a few percentage points of each other.

## Score and Decision

**Calibration anchors retrieved:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| Spider 2.0 (XmProj9cPs) | 8.00 | R1 | Text-to-SQL enterprise benchmark; landmark scope but single-turn; BIRD-INTERACT adds the interactive/dynamic dimension |
| MMQA (GGlpykXDCa) | 8.00 | R1 | Multi-table QA benchmark; solid but less technically novel than BIRD-INTERACT's simulator design |
| AndroidWorld (il5yUQsrjC) | 7.00 | R2 | Dynamic agent benchmark; comparable in scope and rigor |
| τ-bench (roNSXZpUDN) | 6.50 | R1 | Tool-agent-user interaction benchmark, the closest analog; BIRD-INTERACT has stronger simulator validation and domain specificity |
| MINT (jp3gWrMuIZ) | 6.75 | R2 | Multi-turn interaction benchmark (cited in paper); BIRD-INTERACT addresses documented MINT failures (ground-truth leakage) with principled fix and human alignment validation |
| CHASE-SQL (CvGqMD5OtX) | 6.25 | R1 | Text-to-SQL method paper, not benchmark |
| ROUTE (BAglD6NGy0) | 6.25 | R1 | Text-to-SQL fine-tuning paper, not benchmark |

**Round 1 bracket:** 6.5–8.0. The paper is clearly above τ-bench (6.5) and MINT (6.75) in technical depth (function-driven simulator with quantified robustness, human-alignment validation, memory grafting analysis). It is below or at Spider 2.0 (8.0) — Spider 2.0 is a landmark enterprise benchmark with broader scope; BIRD-INTERACT is narrower but adds the interactive dimension which Spider 2.0 lacks.

**Round 2 narrowing:** AndroidWorld (7.0) is a good comparator: solid benchmark with dynamic construction, executable rewards, real-world grounding. BIRD-INTERACT matches this level of rigor and adds stronger analytical contributions (memory grafting, ITS). The minor weaknesses (undisclosed n in Table 3, single-run evaluation, underanalyzed a-Interact non-scaling) do not undermine core contributions.

**Final score: 7.0** — a solid, well-executed benchmark paper with genuine technical contributions (function-driven simulator, human-alignment validation, CRUD coverage, memory grafting diagnostic) and minor evidential/presentational gaps that should be addressed in revision.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>