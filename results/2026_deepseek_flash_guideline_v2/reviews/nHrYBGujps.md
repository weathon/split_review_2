Now let me finalize my review with the complete analysis.

## Summary

BIRD-INTERACT is a benchmark for evaluating LLMs on dynamic, multi-turn text-to-SQL tasks. It converts LIVESQLBENCH's single-turn tasks into interactive scenarios with injected ambiguities and follow-up sub-tasks (900 total: 600 full + 300 lite). The key contributions are: (1) a function-driven user simulator designed to prevent ground-truth leakage that plagues LLM-based simulators; (2) two evaluation settings — c-Interact (conversational protocol) and a-Interact (agentic, budget-constrained); (3) a task suite covering the full CRUD spectrum with state-dependent follow-up sub-tasks. Evaluations of 7 frontier LLMs show very low success rates (best: GPT-5 at 29.17% SR in a-Interact, Gemini-2.5-Pro at 25.00% in c-Interact). A memory grafting experiment suggests that communication skill — not just SQL generation ability — is a bottleneck.

## Strengths

- **Quantitatively validated function-driven user simulator.** Section 6 provides strong evidence that the simulator addresses ground-truth leakage. On USERSIM-GUARD (2,100 labeled questions), the function-driven approach reduces the UNA (unanswerable) failure rate from up to 67.4% (baseline) to as low as 2.7% (Figure 6). The human alignment study (Table 3) yields Pearson r = 0.84 (p = 0.02) with human expert behavior — concrete validation that many benchmark papers lack.

- **Two evaluation settings that reveal non-obvious failure modes.** Table 2 shows GPT-5 is the *worst* model in c-Interact (14.50% SR) but the *best* in a-Interact (29.17% SR) — a reversal from single-turn rankings. Action distribution analysis (Section 5.2) shows submit+ask actions comprise 60.87% of all actions, revealing a bias toward costly trial-and-error over strategic exploration. The benchmark surfaces behavioral distinctions that prior static benchmarks could not capture.

- **State dependency between sub-tasks.** Follow-up sub-tasks (Section 3.2) require reasoning over database states modified by preceding queries (e.g., newly created tables from DDL). The paper explicitly distinguishes this from prior datasets (CoSQL, SParC, etc.) that lack this property — a concrete design difference rather than generic scope enlargement.

- **Knowledge chain breaking as a novel ambiguity type.** Section 3.2 describes a DAG-structured Hierarchical Knowledge Base where intermediate nodes are masked (e.g., "AVS" in the "urgent care → AVS → IF/CPI" chain), requiring multi-hop reasoning and user clarification to reconstruct. This goes beyond surface-level paraphrasing ambiguity.

- **Full CRUD coverage.** Table 1 reports 190/600 data management tasks (INSERT, UPDATE, DELETE, DDL) alongside 410 business-intelligence SELECT tasks, expanding meaningfully beyond the SELECT-only scope of prior multi-turn text-to-SQL benchmarks.

## Weaknesses

### Fatal
None.

### Major

- **The user simulator's reliance on the ground-truth SQL creates unresolved ambiguity about what the benchmark measures.** The two-stage simulator (Section 3.3, line 84) uses the annotated GT SQL as a source for generating responses for both `AMB()` and `LOC()` actions. For `LOC()` specifically, the simulator "uses an AST-based retrieval step to locate the relevant SQL fragment" from the GT SQL. The core question is: does the `LOC()` response provide natural-language information (reasonable) or literal SQL content (problematic leakage)? The paper states the second stage "generates a final response based on the chosen action and the annotated GT SQL with clarification source," but the main text does not clarify whether these responses are natural-language paraphrases or SQL disclosures. If they are SQL content, then the benchmark may partially reward systems for extracting SQL-relevant information from an oracle rather than for genuine interactive problem-solving. The human alignment study (r = 0.84) provides partial reassurance that the simulator behaves realistically, but it does not directly test for this oracle-exploitation channel. **Why this is Major (not Fatal):** the simulator's `AMB()` action is well-scoped to pre-annotated ambiguities, and the `UNA()` action explicitly prevents inappropriate queries. The concern applies primarily to the `LOC()` action (unanticipated but reasonable queries), and even there the paper has designed controls. A main-text clarification of what `LOC()` responses actually contain would substantially resolve this issue.

- **The memory grafting experiment does not cleanly isolate the role of communication strategy from SQL content in context.** In Section 5.2, GPT-5 is provided with "ambiguity resolution histories" from Qwen-3-Coder and O3-Mini. The paper concludes that GPT-5's improvement (from 13.8% to 20.5%) is due to learning better communication schemas. However, the paper does not specify whether these histories include the SQL queries the source models attempted (including potentially correct SQLs and execution feedback). If they do, then GPT-5's improvement could partially reflect having better SQL in its context window rather than learning better clarification strategies. Additionally, the "without memory grafting" baseline (13.8%) does not clearly correspond to any single entry in Table 2 (GPT-5 c-Interact: 8.67% overall SR, 14.50% priority SR), and the paper does not specify which task subset or evaluation conditions this experiment uses, making precise interpretation difficult.

### Minor

- **Single-run evaluation without variance estimation.** Section 5 (line 163) states "conducting single runs due to cost." While temperature=0 is a standard mitigation and many benchmark papers operate similarly, several pairwise comparisons in Table 2 involve differences of <1% (e.g., O3-Mini at 24.00% vs. Gemini-2.5-Pro at 25.00% for c-Interact priority SR). The qualitative claims about model ordering (e.g., "GPT-5 performs poorly in c-Interact") are robust, but fine-grained comparative claims lack statistical support.

- **The ambiguity injection process creates a constrained evaluation space whose limitations are unacknowledged.** The paper's methodology (Section 3.2) injects three types of ambiguity that are "unsolvable without clarification yet fully reconstructable once clarifications are provided." This requires systems to navigate pre-annotated ambiguity points. A system that asks reasonable but unanticipated questions may not receive useful feedback via the `LOC()` path. The paper does not discuss whether these injected ambiguities correspond to natural user ambiguity patterns or how the controlled injection might limit generalizability.

- **Only 2 sub-tasks per task.** The paper describes the benchmark as capturing "long-horizon" interaction, but each task has exactly 2 sub-tasks. The average of ~13 interactions per task (Table 1) comes largely from clarification turns within each sub-task, not from extended multi-step problem solving. The paper does not discuss whether 2 sub-tasks are sufficient to differentiate models on sustained interaction capability.

### Trivial

- The "without memory grafting" baseline in Figure 5 (13.8%) does not precisely match any number in Table 2 (GPT-5 c-Interact: 8.67% overall, 14.50% priority SR). The evaluation conditions or subset should be clarified.

## Nice-to-Haves

- An ablation of the `LOC()` action specifying whether responses are natural-language paraphrases or literal SQL fragments would directly address the oracle-exploitation concern.
- The memory grafting experiment could be strengthened by a control condition where SQL attempts are stripped from the grafted histories, isolating the effect of clarification strategy alone.
- A "free-mode" (budget-unconstrained) comparison alongside the stress-mode a-Interact results would help distinguish whether the trial-and-error bias is inherent or an artifact of budget pressure.
- More details on test case construction (number per task, edge-case coverage, functional equivalence verification) would strengthen reproducibility.

## Removed Points

These points from the inputs were removed with brief justification:

- **Harsh Critic: "The ambiguity injection is artificial and the task scope is inherited"** — Demoted from potential structural concern to Minor and reframed. Controlled benchmarks inherently involve artificial construction; LIVESQLBENCH is the acknowledged foundation. The valid sub-concern (unacknowledged limitations) is retained in Minor.
- **Harsh Critic: "The budget formula conflates task difficulty with resources"** — Removed as speculative; the formula appears reasonable for the stated purpose.
- **Harsh Critic: "The ITS analysis lacks quantitative trend analysis"** — Removed as a scope-creep preference; the qualitative ITS analysis is appropriate for the paper's scope.
- **Harsh Critic: Section-by-section notes on novelty overstatement** — Removed; the paper is appropriately situated in context and the critique is generic.
- **Strength Finder: "Memory grafting experiment is the single most important piece of evidence"** — The assertion is too strong given the verified confound. The finding is still interesting but tempered in the retained Strengths.
- **Strength Finder: Generic/scoping strengths** — Several strength entries (e.g., "this paper addressed an important problem") removed as generic, not anchored to specific paper content.

## Novel Insights

The merge reveals a tension not surfaced by either reviewer alone: the paper's two most compelling pieces of evidence (the memory grafting experiment and the human alignment study) sit in tension with each other. The memory grafting experiment is the paper's best causal demonstration that interaction skill matters separately from SQL ability — but it has a confound (potential SQL content in the history). The human alignment study (r=0.84) is the best evidence that the simulator produces realistic behavior — but it validates the overall simulator, not the specific claim that `LOC()` responses are free from oracle-exploitation. These two pieces of evidence would jointly be much stronger if: (1) the human alignment study were broken down by action type (AMB vs. LOC vs. UNA), and (2) the memory grafting experiment specified exactly what was in the histories. Together, the reviews suggest a paper that is well-designed but needs clearer exposition on two specific points to fully earn its interpretive claims.

## Suggestions

1. Clarify in the main text (Section 3.3) what the `LOC()` action's responses actually contain — if they are natural-language paraphrases derived from SQL fragments, state this explicitly; if they are literal SQL disclosures, acknowledge the validity concern and discuss how the human alignment study addresses it.
2. For the memory grafting experiment, specify what information is in the grafted histories (clarification dialogue only, or also SQL attempts). Add a controlled condition where SQL attempts are stripped from the grafted history.
3. Add a brief limitations paragraph discussing the artificial nature of the injected ambiguities, the 2 sub-task structure, and the trade-offs in the controlled evaluation design.
4. Clarify which task subset (FULL or LITE) and which evaluation conditions the memory grafting experiment uses, to reconcile the baseline numbers.
5. Add confidence intervals from multiple runs on a small subset (e.g., 50 LITE tasks with 3 runs each) to establish typical variance levels.

## Score and Decision

**Calibration note:** The calibration corpus was inaccessible at the time of review, so direct anchor-based score calibration was not possible. Scores are assigned based on the paper's merits relative to ICLR standards for benchmark papers.

This paper makes a genuine and well-validated contribution to interactive text-to-SQL evaluation. The function-driven user simulator is clearly better than baselines (validated both objectively and via human alignment). The two evaluation settings surface genuinely novel behavioral findings (GPT-5 reversal). The benchmark scale (900 tasks), CRUD coverage, and state dependency are meaningful extensions over prior work. The two major weaknesses — the need to clarify what `LOC()` responses actually contain, and the memory grafting confound — are real but addressable; they do not invalidate the core contribution. With the suggested clarifications and controls, this would be a strong paper.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>