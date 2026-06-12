Now I have all the calibration information I need. Let me produce the final consolidated review.

## Summary

BIRD-INTERACT is a benchmark for evaluating LLMs on multi-turn, interactive text-to-SQL tasks. It converts static single-turn queries from LIVESQLBENCH into interactive scenarios through: (1) ambiguity injection and follow-up sub-task annotation, (2) a function-driven user simulator that maps system queries to controlled actions (AMB/LOC/UNA) before generating responses, and (3) two evaluation settings (c-Interact: protocol-guided; a-Interact: agentic). The benchmark includes 900 tasks (600 full + 300 lite) covering full CRUD operations. Results show GPT-5 achieves only 8.67% success in c-Interact and 17% in a-Interact, confirming the benchmark is challenging with substantial headroom.

## Strengths

1. **Well-motivated gap with concrete design response.** The paper correctly identifies two real limitations of existing multi-turn text-to-SQL benchmarks (static conversation transcripts, SELECT-only scope) and designs a benchmark that directly addresses both through dynamic interaction and CRUD coverage (Sections 1, 3.2).

2. **Function-driven user simulator is a genuine methodological contribution.** The two-stage approach (semantic parser → {AMB, LOC, UNA} actions → controlled response generation) demonstrably reduces unanswerable-question leakage from up to 67.4% (baseline LLM simulators) to 2.7% (Figure 6). This is a principled solution to a known problem in interactive evaluation.

3. **Human alignment validation strengthens the case.** The function-driven simulator achieves Pearson r = 0.84 (p = 0.02) with human user success rates on the same tasks, vs. 0.61 (p = 0.14) for the baseline (Table 3). This provides meaningful evidence that the simulator reflects actual human-AI interaction patterns.

4. **Memory grafting experiment yields a non-obvious finding.** Showing that GPT-5's poor c-Interact performance is rescued by grafting interaction histories from Qwen-3-Coder or O3-Mini (Figure 5) cleanly separates SQL generation capability from communication strategy, pointing to a specific bottleneck future work can target.

5. **The benchmark is genuinely hard.** Top models achieve <25% normalized reward and <17% end-to-end success. The inter-annotator agreement of 93.5% (Table 1) supports annotation quality. The dual evaluation settings (c-Interact/a-Interact) and state-dependent follow-ups are genuine extensions beyond existing benchmarks.

## Weaknesses

### Fatal
None.

### Major

1. **The simulator's responses are anchored to ground-truth SQL, raising a construct validity question that the paper does not adequately address.** The paper states (Section 3.2, line 72) that each ambiguity is "paired with a corresponding SQL snippet from the ground-truth query as a clarification source," and (Section 3.3) the simulator generates responses "based on the chosen action and the annotated GT SQL with clarification source." Both AMB() and LOC() actions retrieve information from the ground-truth SQL. This means the evaluation pipeline channels GT-SQL-derived information into the system's context through the clarification response. The system must still figure out *what* to ask — but it does not need to reason from domain knowledge or database contents alone; it needs to ask questions whose answers have been prepackaged from the target SQL. This does *not* invalidate the benchmark (the core task of identifying and resolving ambiguities remains), but the paper's claim that the benchmark evaluates "strategic interaction capabilities" needs qualification: the benchmark more precisely evaluates a system's ability to discover which prepackaged GT-SQL-derived clarifications to trigger. The paper should either provide evidence that this pipeline does not substantially inflate measured performance (e.g., by replacing the SQL-snippet source with natural-language descriptions and comparing results) or reframe the benchmark's claims more precisely. The paper partially preempts this concern by acknowledging uncontrolled GT leakage in prior simulators (Section 3.3), but the controlled approach still channels GT information — it constrains *how*, not *whether*.

2. **All evaluations are single runs with no measure of variance.** Section 5 states "conducting single runs due to cost." For a benchmark whose central empirical contribution is ranking models (Table 2) and drawing qualitative conclusions (e.g., GPT-5 is worst in c-Interact at 14.50% but best in a-Interact at 29.17%), single runs are inadequate. Differences between adjacent models are often small — Claude-Sonnet-3.7 at 8.33% vs. Deepseek-Chat-V3.1 at 8.50% in c-Interact follow-ups — and without variance estimates there is no way to know whether these reflect signal or noise. The LITE set exists and the authors explicitly note it enables "faster development"; running at least 3 trials on the LITE set would provide much-needed confidence intervals for model comparisons.

### Minor

1. **Ambiguities are synthetically injected rather than drawn from natural interaction data.** The method of taking clear single-turn queries and injecting intent-level vagueness, knowledge removals, and knowledge chain masking (Section 3.2) is methodologically reasonable for a controlled benchmark. However, whether these injected ambiguities resemble those that arise naturally in real database interactions is unclear. The human alignment study (Table 3) validates the simulator against human behavior on the *same* tasks, but does not validate whether the tasks themselves generalize to natural ambiguity. This should be discussed as a limitation.

2. **The ITS analysis claim is overstated.** The paper asserts an "ITS Law" — that with enough turns, performance can match or surpass the idealized single-turn task (Section 5.2). From Figure 4, the patterns across models are mixed: some models' a-Interact performance is flat or decreasing with more patience. A single observation that Claude-3.7-Sonnet "exhibits clear scaling behavior" does not constitute a law. The claim should be softened or supported with stronger evidence.

### Trivial
None.

## Nice-to-Haves
- Run experiments where the clarification source for a given ambiguity is a natural-language description rather than a SQL snippet, to quantify the information-leakage concern.
- Report action distributions broken down by model and task type (currently only an aggregate 60.87% submit/ask figure is reported).
- Analyze the cost-performance tradeoff systematically (cost data appears in Table 2 but is not interpreted).

## Removed Points
*These points were flagged to be removed; treat them with caution.*
- **"Relationship between LIVESQLBENCH and BIRD-INTERACT is underspecified"** — The paper clearly states (Section 3.1) that BIRD-INTERACT is built on LIVESQLBENCH and converts static tasks to interactive ones. The relationship is adequately specified.
- **"Cost analysis underanalyzed"** — This is a nice-to-have, not a core weakness. Cost data is presented; deeper analysis would strengthen but is not expected for a benchmark paper.
- **"No discussion of stochasticity/seed-sensitivity"** — Generic concern applicable to any LLM evaluation; the paper acknowledges single runs due to cost.
- **Various formatting and reproducibility nitpicks** — Parser artifacts or issues common to all LLM evaluation papers.

## Novel Insights

The harsh critic's most penetrating observation — that the simulator's reliance on GT-SQL clarification sources creates a confound — is real and verifiable from the paper's own exposition (Section 3.2–3.3). However, the critic overstates its severity: this is a construct validity *precision* issue, not a fatal flaw. In real-world clarification, the human user *does* know the answer and provides it — the skill being tested is asking the right question. The concern is whether the *form* of the response (SQL-derived fragments rather than natural language) makes the subsequent SQL construction unrealistically easy. This can be addressed with an ablation. The single-run criticism is accurate and well-targeted, though it is common practice in the field. The critic's other observations (ecological validity of injected ambiguities, overstated ITS claim) are legitimate but secondary.

## Suggestions
1. **Address the GT-SQL-to-simulator pipeline directly in the paper** — either provide evidence (e.g., an ablation replacing SQL-snippet clarification sources with NL descriptions) that the information flow does not inflate performance, or reframe the benchmark's claims to precisely describe what is measured.
2. **Run at least 3 trials on the LITE set** to provide variance estimates for the key model comparisons in Table 2 (LITE results).
3. **Tone down the "ITS Law" claim** or support it with statistical evidence across all tested models.
4. **Discuss synthetic vs. natural ambiguity as an acknowledged limitation** rather than equating the two.

## Score and Decision

**Calibration Report:**

The following anchor papers from the human-review corpus were used for score calibration.

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| Spider 2.0 | 8.00 | R1 | Enterprise text-to-SQL benchmark; real-world databases, multi-dialect; no construct validity concerns. Clearly stronger than BIRD-INTERACT. |
| HoloBench | 6.25 | R1 | Benchmark for holistic reasoning with LCLMs; accepted with minor weakness about scale (90 Qs). Slightly stronger than BIRD-INTERACT. |
| CHASE-SQL | 6.25 | R2 | Text-to-SQL method paper; different genre but same area. Comparable in quality to BIRD-INTERACT. |
| ROUTE | 6.25 | R2 | Text-to-SQL method paper. Comparable. |
| SQL-GEN | 5.67 | R2 | SQL dialect adaptation method; rejected. Different type of contribution. |
| SQL-GEN | 5.67 | R1 | Same as above. |
| DialSim | 5.00 | R2 | Dialogue simulator benchmark; had data leakage concerns. Weaker than BIRD-INTERACT. |
| LAIA-SQL | 5.00 | R2 | Text-to-SQL method; mixed reviews. |
| EvoSchema | 4.25 | R1 | Text-to-SQL robustness benchmark; limited dataset scope, rejected. Weaker than BIRD-INTERACT. |
| TrustSQL | 4.00 | R1 | Text-to-SQL reliability benchmark; re-annotated existing data, rejected. Weaker than BIRD-INTERACT. |
| DB-GPT-Hub | 3.75 | R1 | Text-to-SQL fine-tuning benchmark; baseline-only focus, rejected. Weaker than BIRD-INTERACT. |
| DataSciBench | 3.20 | R1 | Data science agent benchmark; questionable authenticity, rejected. Weaker than BIRD-INTERACT. |

**Round 1 bracket:** After reviewing the paper and initial calibration, the narrowest plausible range was [5.0, 6.5]. BIRD-INTERACT is clearly stronger than the rejected benchmarks in the 3.2–5.0 range (DataSciBench, DB-GPT-Hub, TrustSQL, EvoSchema, DialSim) which had more fundamental flaws. It is clearly weaker than Spider 2.0 (8.0) which has no comparable construct validity concerns. It sits slightly below HoloBench (6.25) which was accepted with only a minor scale concern.

**Round 2 narrowing:** Targeted search in the 4.5–6.5 range confirmed that accepted papers at the high end (CHASE-SQL, ROUTE at 6.25) are method papers with less scrutiny on benchmark construct validity, while rejected papers at the low end (DialSim 5.0, LAIA-SQL 5.0) have more severe problems. BIRD-INTERACT's genuine contribution and solid simulator validation place it above DialSim, but the GT-SQL pipeline concern and single-run limitation prevent it from reaching the HoloBench level.

**Final score: 5.5** — This paper makes a real contribution (the function-driven simulator, dual evaluation settings, challenging task suite, and interesting analyses) but has two notable weaknesses: (1) the clarification pipeline's reliance on ground-truth SQL fragments is underscrutinized, creating construct validity uncertainty, and (2) single-run evaluations undermine the reliability of model rankings. Both are addressable. The paper should be accepted with the expectation that the authors will address these issues in the final version.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>