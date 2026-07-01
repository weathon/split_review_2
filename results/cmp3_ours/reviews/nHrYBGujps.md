Here is my final consolidated review.

---

## Summary

This paper introduces BIRD-INTERACT, a benchmark for evaluating text-to-SQL systems through dynamic, multi-turn interactions rather than static conversation transcripts. It converts 600/300 (FULL/LITE) single-turn tasks from LIVESQLBENCH into interactive scenarios via injected ambiguities, a function-driven user simulator (two-stage AMB/LOC/UNA classification), and follow-up sub-tasks with state dependencies. Two evaluation settings are supported: c-Interact (protocol-guided conversation) and a-Interact (autonomous agent exploration). Experiments on 7 frontier LLMs show very low end-to-end success rates (best ~17%), and a human correlation study validates the simulator with r=0.84 (p=0.02). The core contribution is a benchmark that fills a genuine gap in interactive text-to-SQL evaluation.

## Strengths

1. **The function-driven user simulator is a genuine methodological contribution.** The two-stage approach (classifying queries into AMB/LOC/UNA actions via symbolic mapping before generating responses) addresses ground-truth leakage that plagues LLM-based simulators. Section 6 provides strong evidence: baseline simulators fail on Unanswerable (UNA) questions up to 67.4% of the time, whereas the function-driven approach reduces this to 2.7% (Figure 6).

2. **The gap the benchmark targets is real and well-motivated.** The observation that existing multi-turn text-to-SQL benchmarks (COSQL, SParC, etc.) use static, pre-recorded conversation histories is correct. BIRD-INTERACT forces models to generate their own clarifications and recover from their own errors — a genuinely different evaluation paradigm.

3. **The two evaluation settings are thoughtfully differentiated.** The distinction between c-Interact (protocol-guided) and a-Interact (agentic) is not cosmetic — Table 2 shows GPT-5 is the worst model in c-Interact but the best in a-Interact, revealing qualitative capability differences that a single setting would not surface.

4. **CRUD coverage expands task scope meaningfully.** Including INSERT/UPDATE/DELETE and DDL operations with state-dependent follow-ups creates dependencies between sub-tasks that cannot exist in read-only settings. This is genuinely novel among interactive text-to-SQL benchmarks.

5. **The memory grafting experiment (Figure 5) is well-designed.** Giving GPT-5 the interaction histories from better-performing models and measuring the resulting improvement cleanly separates SQL generation ability from interactive communication ability.

6. **The human correlation study (Table 3) is strong validation.** A Pearson correlation of 0.84 (p=0.02) between simulator-based and human-based success rates across 100 tasks is convincing evidence for simulator fidelity.

## Weaknesses

### Fatal
None.

### Major

1. **The "ITS Law" is over-claimed.** The paper defines "Interaction Test-time Scaling (ITS) Law" (line 207) as follows: "A model satisfies this law if, given enough interactive turns, its performance can match or even surpass that of the idealized single-turn task." The abstract claims "performance improves monotonically with additional interaction opportunities across multiple models." However, Figure 4 shows only Claude-3.7-Sonnet exhibiting clear upward scaling in c-Interact, while other models (especially in a-Interact) show flat or decreasing performance. A single-model observation does not warrant the label "law." This framing should be downgraded to an observation.

### Minor

2. **Single-run evaluation limits the reliability of comparative claims.** Section 5 states that all experiments are "single runs due to cost" with temperature=0. While temperature=0 reduces variance, LLM outputs — especially for action selection in a-Interact and clarification dialogue — remain non-deterministic due to sampling, system prompts, and API-level variability. Several model differences in Table 2 are small (e.g., Gemini-2.5-Pro at 16.33% vs O3-Mini at 15.83% in c-Interact Follow-ups). Without error bars or multiple runs, it is impossible to tell whether these differences are meaningful or within noise. The benchmark itself remains the primary contribution, so this weakens the empirical conclusions but not the benchmark's value.

3. **The memory grafting experiment does not state whether it uses LITE or FULL.** Figure 5 shows GPT-5 "without" memory grafting at 13.8%, while Table 2 (FULL, c-Interact Priority) reports GPT-5 at 14.50%. The discrepancy suggests Figure 5 uses LITE, but neither the caption nor the text clarifies this. Figure 4 (ITS) explicitly states "BIRD-INTERACT-LITE"; the memory grafting section should do the same for consistency and reproducibility.

4. **The comparison between c-Interact and a-Interact results is partially confounded by differing budget structures.** In c-Interact: τ_clar = m_amb + λ_pat (budget on clarification turns). In a-Interact: B = 6 + 2·m_amb + 2·λ_pat (budget on all actions, with doubled multipliers). The paper concludes that "Interaction Mode Emerged as the Decisive Factor" (Section 5.1), but the budget differential means a-Interact tasks have systematically more resources. This does not invalidate the finding, but the conclusion should acknowledge the budget confound.

5. **The ambiguity injection methodology is not validated for naturalness.** The paper injects three types of ambiguity (superficial, knowledge, environmental) but does not evaluate whether these injected ambiguities resemble naturally-occurring interaction patterns. The human correlation study (Table 3) validates the simulator's responses, not whether the injected ambiguities themselves are representative of real-world ambiguity. The high inter-annotator agreement (93.5%) measures annotation consistency, not naturalness.

6. **Action distribution analysis is descriptive rather than analytical.** Section 5.2 reports that "submit" and "ask" comprise 60.87% of all actions but does not break this down by model or correlate action patterns with success rates. This limits the insightfulness of an otherwise interesting finding.

### Trivial

7. **The default reward weights (70% priority / 30% follow-up) are stated in Section 5.1 but not introduced in Section 2 (Metrics) where Normalized Reward is defined.** Moving this information earlier would improve clarity.

## Nice-to-Haves
- Adding variance estimates (even 2–3 runs on LITE) would strengthen the empirical conclusions.
- A control condition in the memory grafting experiment (giving GPT-5 deliberately suboptimal interaction histories) would confirm that improvement is specific to good interaction histories.
- Analyzing what types of clarification questions, exploration patterns, and error-recovery strategies correlate with success would deepen the paper's contribution beyond descriptive action statistics.

## Removed Points
These points from the input review were removed with justification:

1. **"Normalized Reward is deferred to Appendix F; main text does not provide enough detail"** — REMOVED because Section 5.1 (line 173) explicitly states "the reward structure allocating 70% to the primary sub-task and 30% to follow-up sub-tasks." The critic's claim that weights are only in the appendix is incorrect.

2. **"The 'multi-turn' framing is over-stated"** — REMOVED because the paper clearly states n=2 sub-tasks per task and average ~13 turns per task. The 11,796 figure is transparently described as interactions across all 600 tasks. "Multi-turn" is accurate given the ~13-turn average; "long-horizon" appears once (Section 3.4) and is used comparatively against existing static benchmarks.

3. **"Full CRUD spectrum is slightly misleading"** — REMOVED because "full CRUD spectrum" means coverage of all operation types, not equal distribution. The benchmark includes INSERT/UPDATE/DELETE/DDL (190/600 DM tasks), constituting genuine CRUD coverage.

4. **"The abstract's 8.67% matches Follow-ups column, not Priority column"** — REMOVED because this is the paper's intended design: the Follow-ups column represents end-to-end task completion (since the second sub-task requires completing the first). The abstract and Table 2 are consistent.

5. **Budget formula justification nitpicks (why B_base=6, why multiply m_amb by 2)** — REMOVED as a granular design detail that does not affect the core contribution.

## Novel Insights
None beyond the paper's own contributions. The review does not surface any genuinely novel insight that the paper itself does not already articulate.

## Suggestions
1. Downgrade the "ITS Law" language to an observation about Claude-3.7-Sonnet's scaling behavior.
2. Explicitly state whether the memory grafting experiment uses LITE or FULL in the caption and body text.
3. Acknowledge the budget differential as a confound when comparing c-Interact vs a-Interact results.
4. Add variance estimates on at least the LITE subset in a revision or extended version.

## Score and Decision

**Calibration Anchors (retrieved from human-review corpus):**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| τ-bench (roNSXZpUDN) | 6.50 | R1 | Tool-agent-user interaction benchmark. BIRD-INTERACT has stronger simulator validation (human correlation r=0.84) |
| ToolDial (J1J5eGJsKZ) | 6.67 | R1 | Multi-turn dialogue for tool-augmented LMs. Comparable genre; BIRD-INTERACT more rigorous simulator design |
| DataSciBench (BltaWJZMeR) | 3.20 | R1 | LLM data science benchmark. Less relevant; BIRD-INTERACT has stronger contribution |
| TrustSQL (7ZeoPg3eTA) | 4.00 | R1 | Text-to-SQL reliability benchmark. Less relevant to interaction dynamics |
| DB-GPT-Hub (NmILZXKcOi) | 3.75 | R1 | Text-to-SQL benchmark. Less relevant |
| WildBench (MKEHCx25xp) | 7.33 | R2 | LLM evaluation with real user queries. Comparable contribution significance |
| SPA-Bench (OZbFRNhpwr) | 7.33 | R2 | Smartphone agent benchmark. Comparable scope and strength |
| HAZARD (n6mLhaBahJ) | 6.75 | R2 | Embodied decision-making benchmark. Similar genre as interactive evaluation |
| Spider 2.0 (XmProj9cPs) | 8.00 | R2 | Enterprise text-to-SQL. Stronger in real-world data provenance but different focus |
| VoxDialogue (vbmSSIhKAM) | 6.60 | R2 | Spoken dialogue benchmark. Similar evaluation scope |

**Round 1 Bracket:** [6.5, 7.5]  
**Narrowing:** BIRD-INTERACT is stronger than τ-bench (6.50) — whose main weakness was insufficient user simulator validation — because it provides a principled function-driven simulator with human correlation (r=0.84). It is comparable to SPA-Bench (7.33) and WildBench (7.33) in contribution significance. It is not at the Spider 2.0 (8.00) level, where unanimous 8s reflect a benchmark with real enterprise data and near-flawless execution. The weaknesses identified (ITS Law over-claim, single-run evaluation, LITE/FULL confusion) are real but addressable, and none threaten the core contribution.

**Final Score:** 7.0  
**Final Decision:** Accept

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>