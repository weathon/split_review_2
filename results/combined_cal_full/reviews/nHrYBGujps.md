Now I have all the calibration data I need. Let me compile the final review.

## Summary
This paper introduces BIRD-INTERACT, a benchmark for evaluating LLMs on interactive, multi-turn text-to-SQL tasks. It addresses two limitations of existing benchmarks: (1) they use static conversation transcripts that cannot reward/punish models for their interaction strategies, and (2) they are overwhelmingly SELECT-only. BIRD-INTERACT provides 900 tasks with full CRUD coverage, a function-driven user simulator that avoids ground-truth leakage, and two evaluation settings (c-Interact for protocol-guided conversation, a-Interact for autonomous agentic planning). Experiments show that state-of-the-art models like GPT-5 achieve only 8.67% success in c-Interact and 17.00% in a-Interact.

## Strengths

**1. Genuine, well-motivated gap.** The paper clearly articulates how existing multi-turn benchmarks (COSQL, SPaRC, LEARN-TO-CLARIFY) rely on static transcripts and are SELECT-only, and BIRD-INTERACT directly addresses both shortcomings with dynamic interaction histories and full-CRUD task coverage.

**2. Function-driven user simulator is a real technical contribution.** The two-stage approach (parse to AMB/LOC/UNA actions, then generate controlled responses from ground-truth SQL snippets) provides a principled solution to ground-truth leakage and task drift. The USERSIM-GUARD evaluation (Figure 6) shows failure rates drop from 67.4% to 2.7%, and the human alignment study (Table 3: 0.84 vs 0.61 Pearson correlation for GPT-4o) confirms more realistic behavior than conventional LLM-as-user-simulator approaches.

**3. Memory grafting experiment is analytically crisp.** Giving GPT-5 interaction histories from better-interacting models (Qwen-3-Coder, O3-mini) and showing its SQL generation improves from 13.8% to 18.8–20.5% cleanly separates interaction skill from SQL generation competence. This analysis goes beyond leaderboard numbers to provide mechanistic insight.

**4. The benchmark is genuinely hard.** GPT-5 at 8.67% (c-Interact) and 17.00% (a-Interact) leaves meaningful room for progress. The BI vs. DM breakdown (Table 2) reveals non-trivial structure, consistent with the paper's explanation that DM tasks follow more standardized patterns.

**5. Rigorous annotation process.** Twelve expert annotators with multi-stage selection, inter-annotator agreement of 93.33–93.50%, and quality control ensuring ambiguous queries are "unsolvable without clarification yet fully reconstructable once clarifications are provided."

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

**1. The "ITS Law" framing overstates the evidence.** The paper defines ITS Law as "A model satisfies this law if, given enough interactive turns, its performance can match or even surpass that of the idealized single-turn task" — but in all experiments, models plateau well below the idealized single-turn line (Figure 4). The empirical finding that some models improve with more turns in c-Interact is interesting, but naming it a "law" and grounding it primarily on Claude-3.7-Sonnet's isolated scaling behavior is not supported by the broader pattern. This should be reframed as a limited empirical observation.

**2. The paper does not include an explicit statement that its benchmark artifacts will be publicly released.** For a benchmark paper, the absence of a release commitment for the annotations, simulator code, evaluation framework, and USERSIM-GUARD dataset is a notable gap. While the paper builds on the open-source LIVESQLBENCH and describes construction methodology in detail, the central contribution cannot be used by the community without a clear release commitment. This is fixable and should be addressed in the final version.

**3. Single-run evaluation without variance reporting.** The paper acknowledges single runs due to cost (Section 5, temperature=0). While deterministic decoding makes c-Interact fairly stable, the a-Interact setting involves autonomous action selection where trajectories can diverge stochastically. Without multiple trials or variance estimates, comparative claims (e.g., GPT-5 being "worst" in c-Interact at 14.50% vs. Claude-Sonnet-4 at 22.33%) cannot be fully assessed for reliability.

**4. The ambiguity space is inherently closed-world.** The simulator's AMB action only responds to pre-annotated ambiguities. While LOC() provides some flexibility via AST retrieval for unanticipated questions, the benchmark primarily measures performance against a fixed set of known ambiguities that annotators chose to inject. This bounds the kinds of "interaction strategy" the benchmark can measure and is not sufficiently discussed as a limitation.

### Trivial
None.

## Nice-to-Haves

- The paper would be strengthened by showing that BIRD-INTERACT rankings differ meaningfully from those on static-transcript benchmarks (e.g., COSQL, SParC). Currently, it shows scores are low — but low scores alone don't validate the benchmark as measuring something new. A comparison showing models ranked similarly on single-turn BIRD but differently on BIRD-INTERACT would substantiate the claim that dynamic interaction changes our conclusions.
- A clearer characterization of what each evaluation setting specifically measures (e.g., c-Interact primarily tests clarification ability under a fixed protocol; a-Interact tests planning and resource allocation) would help the community interpret results from each setting.

## Removed Points

- **Weakness about user simulator "closed world" (overstated version):** The original review claimed that models asking "smart but unanticipated" clarification questions would be rebuffed. However, the paper explicitly includes a LOC() action that handles "reasonable clarification requests that fall outside our pre-annotated ambiguities" via AST-based retrieval. The paper partially addresses this; the remaining reasonable concern is kept as Minor weakness #4 above.
- **Question about Table 1's "191 Distinct Test Cases":** The reviewer asked whether 191 test cases for 600 tasks (1,200 sub-tasks) is low. This is a clarification question, not a weakness — tasks on the same database can share test cases.
- **Strength dropped (generic):** "The paper addressed an important problem" — too generic to retain.
- **Speculative claims removed:** Claims about missing appendices or references (parser artifacts, not paper issues). Claims about "at time of writing" regarding model availability — the paper cites these models, so they exist.

## Novel Insights
None beyond the paper's own contributions. The reviews provide useful framing corrections and suggest helpful extensions (comparison to static benchmarks, characterizing settings more precisely), but do not surface analytical patterns the paper itself missed.

## Suggestions

1. Add a clear release commitment statement for benchmark artifacts (annotations, simulator code, evaluation framework, USERSIM-GUARD) in the final version.
2. Reframe "ITS Law" as "Interaction Test-Time Scaling behavior" — a descriptive empirical observation — rather than a "law," since no model in the experiments satisfies the defined condition.
3. Provide bootstrap variance estimates or at minimum discuss which comparative claims are robust to stochasticity in a-Interact action trajectories.
4. Explicitly discuss the closed-world nature of the pre-annotated ambiguity space as a limitation, and clarify what kinds of interaction strategy the benchmark can and cannot measure.

## Anchors

All anchors retrieved across rounds, with comparison:

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| roNSXZpUDN.md (τ-bench) | 6.50 | R1 | Yes | Tool-agent-user interaction benchmark. BIRD-INTERACT has much milder weaknesses (no -7+ weight items) and stronger simulator validation. |
| XmProj9cPs.md (Spider 2.0) | 8.00 | R1 | Yes | Enterprise text-to-SQL benchmark with established brand. Benefits from explicit public release. BIRD-INTERACT has similarly mild weaknesses but lacks release commitment. |
| NmILZXKcOi.md (DB-GPT-Hub) | 3.75 | R1 | Yes | Text-to-SQL benchmark for fine-tuning. BIRD-INTERACT is substantially stronger in novelty, validation, and analytical depth. |
| 5LXcoDtNyq.md (HoloBench) | 6.25 | R1 | Yes | Long-context benchmark based on text-to-SQL. Has heavy weaknesses (-7.18) about flawed RAG comparison and limited diversity. BIRD-INTERACT is stronger. |
| jp3gWrMuIZ.md (MINT) | 6.75 | R2 | Yes | Multi-turn interaction with tools/feedback benchmark. Has heavy weaknesses (-7.26) about limited scope (Python-only) and setup. BIRD-INTERACT is more comprehensive and has stronger validation. |
| MKEHCx25xp.md (WildBench) | 7.33 | R2 | Yes | Real-user-query benchmark with strong evaluation metrics. Has very heavy novelty weaknesses (-8.13, -9.05). BIRD-INTERACT is similar in quality with more novel contributions. |

## Score and Decision

**Round 1 bracket:** Between 6.5 and 8.0 (above τ-bench at 6.50 and MINT at 6.75, comparable to WildBench at 7.33, below Spider 2.0 at 8.00).

**Weights comparison:** BIRD-INTERACT's strongest positive weights (up to +6.03 for the user simulator contribution) match or exceed the strongest anchors' best items. Its weaknesses are all mild (-1.69 to +0.22), placing it well above MINT (which has -7.26 weight items) and τ-bench (which has -7.17 weight items), comparable to WildBench despite WildBench's +4.20–4.57 strengths vs. its -8.13 to -9.05 weaknesses. The main factor preventing an 8.0 score is the missing release commitment for benchmark artifacts — a gap addressed by Spider 2.0 and other top benchmarks.

**Final score:** 7.0 — a clear accept with minor issues to address.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>