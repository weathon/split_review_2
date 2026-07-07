Now I have enough calibration data. Let me write the final consolidated review.

---

## Summary

BIRD-INTERACT is a benchmark for evaluating LLMs on multi-turn, interactive text-to-SQL tasks. It converts single-turn tasks from LIVESQLBENCH into interactive scenarios via systematic ambiguity injection and follow-up sub-tasks, proposes a two-stage function-driven user simulator to avoid ground-truth leakage, and evaluates models under two settings: a protocol-guided conversational mode (c-Interact) and an open-ended agentic mode (a-Interact). The benchmark comprises 600 (full) / 300 (lite) tasks covering the full CRUD spectrum. Experiments on 7 frontier LLMs show that even the best models succeed on fewer than 30% of tasks, with interesting cross-modal reversals (e.g., GPT-5 is worst in c-Interact but best in a-Interact). The user simulator is validated through a static test set (USERSIM-GUARD) and a human alignment study.

## Strengths

- **The function-driven user simulator (Section 3.3) is a genuine and well-validated methodological advance for interactive evaluation.** The two-stage architecture — a semantic parser that maps system questions to three predefined actions (AMB, LOC, UNA) followed by constrained response generation from ground-truth SQL — directly addresses ground-truth leakage and task deviation in prior LLM-based simulators. The USERSIM-GUARD evaluation (Figure 6) is convincing: UNA-category failure rates drop from up to 67.4% to as low as 2.7%. The human alignment study (Table 3) shows significantly better correlation with real human users (Pearson 0.84 vs. 0.61, p=0.02 vs. p=0.14). This contribution stands as the paper's strongest technical result and has independent value beyond the benchmark itself.

- **The two evaluation settings (c-Interact and a-Interact) are well-motivated and produce non-trivial findings.** The distinction between a protocol-guided conversational mode and an open-ended agentic mode captures two genuinely different real-world deployment scenarios. The results justify this design: GPT-5 is the worst model in c-Interact (14.50% SR) but the best in a-Interact (29.17% SR), while Gemini-2.5-Pro shows the opposite pattern. These cross-modal reversals demonstrate that the benchmark measures something beyond single-turn SQL competence and reveal that interactive capability is partially orthogonal to SQL generation skill.

- **The validation infrastructure is unusually thorough for a benchmark paper.** The USERSIM-GUARD static test set (2,100 questions with expert-labeled reference actions), the human alignment correlation study (100 tasks × human experts), and the high inter-annotator agreement (93.33–93.50%) on task annotations all provide concrete evidence about the reliability of the evaluation instrument. Many benchmark papers provide substantially less validation of this kind.

## Weaknesses

### Major

- **The "ITS Law" claim (Section 5.2) is not supported by the paper's own data.** The paper defines an "ITS Law" as: "A model satisfies this law if, given enough interactive turns, its performance can match or even surpass that of the idealized single-turn task" (line 207–208). The evidence is Figure 4, which shows that only Claude-3.7-Sonnet exhibits a clear upward trend in c-Interact; O3-Mini, GPT-4o, and Qwen-3 show much flatter or flat curves. In a-Interact mode, performance decreases or stays flat with increasing patience for most models — a fact the paper's own Figure 4 caption confirms ("in a-Interact mode, it remains relatively flat or slightly decreases"). Calling this a "law" is premature and overstates what the data supports. This is the most significant framing issue in the paper and should be corrected to a measured observation (e.g., "scaling trend observed for some models in c-Interact").

- **The claim that BIRD-INTERACT is more challenging or realistic than existing benchmarks lacks direct comparative evidence in the main text.** The paper argues that existing multi-turn benchmarks (COSQL, SParC, etc.) rely on static conversation histories and SELECT-only tasks, but no controlled experiment is presented showing how the same models perform on those benchmarks under comparable conditions. The claim that BIRD-INTERACT is "more challenging" rests entirely on absolute low success rates (e.g., GPT-5 at 8.67% in c-Interact), which could partly reflect task-specific design choices (ambiguity injection methodology, database schemas, budget constraints) rather than interaction complexity per se. While Appendix E is referenced, the main paper's case is incomplete without this comparative validation.

### Minor

- **The 2-sub-task structure (n=2, line 46) limits the scope of what the benchmark measures.** While the average ~13 interactions per task (Table 1) involves many clarification turns, these are turns within only two sub-tasks — not extended sequences of dependent sub-tasks. Real-world database work often involves many more iterative cycles of query, revision, and follow-up. The paper's framing as capturing "the complete interactive problem-solving process" (line 26) overstates what 2 sub-tasks can represent. The paper is transparent about n=2, but the scope is narrower than the most ambitious framing suggests. This does not invalidate the contribution, but the claims about "full-spectrum" interaction should be calibrated.

- **The memory grafting experiment (Section 5.2) has a confound that limits its interpretability.** Giving GPT-5 interaction histories from higher-performing models (Qwen-3-Coder, O3-mini) improves GPT-5's SQL generation, but this does not cleanly isolate whether GPT-5's weakness is specifically in communication strategy versus planning versus question-asking ability. The improvement could partly reflect better SQL generation conditions from clearer context rather than purely a communication-to-generation decoupling. The conclusion that GPT-5 "possesses robust SQL generation capabilities" but needs "a more effective communication schema" is reasonable as a hypothesis but only partially supported by this experiment.

- **The benchmark's ambiguity-injection methodology (Section 3.2) produces a bounded ambiguity space that is narrower than "dynamic interactions" implies.** Each ambiguity is paired with a specific SQL snippet from the ground-truth query as a clarification source (line 72), meaning the user simulator's responses are tightly coupled to the correct answer. This is a reasonable design choice for controlled evaluation, but the benchmark tests whether a system can identify which pre-annotated ambiguity to resolve, not whether it can handle genuinely open-ended clarifications where the answer space is unbounded. The paper would benefit from explicitly acknowledging this scope limitation rather than framing the benchmark as capturing fully open-ended interaction.

### Trivial

None.

## Nice-to-Haves

- A controlled comparison experiment on at least one existing multi-turn benchmark (e.g., COSQL or SParC) using the same models would directly validate the claim of greater difficulty.
- Showing at least one representative failure trace (a qualitative example of where and why a model fails) would make the benchmark's diagnostic value more concrete.
- An ablation that more cleanly separates communication skill from planning skill in the memory grafting experiment would strengthen the analysis.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Criticism that the paper's characterization of existing benchmarks as relying on "static conversation transcripts" is unfair.** This is a subjective framing preference; the paper's characterization is not unreasonable and does not misrepresent those benchmarks.
- **Criticism that baseline simulator designs are unspecified in the main text.** The paper references Appendix O for these details. The appendix was stripped by the parser, but the paper appropriately defers design details to the appendix.
- **Request for Normalized Reward metric details and action cost values in main text.** These implementation details are appropriately deferred to appendices; the essential weighting structure (70% priority, 30% follow-up) is stated in the main text (line 173).
- **Question about the factor of 2 in the a-Interact budget formula.** This is a design clarification, not a weakness. The paper references Appendix J.
- **Request for error analysis or qualitative examples.** This is a nice-to-have, not a core weakness.
- **The "ambiguity injection narrows the benchmark" concern.** This was moved to Minor with reduced severity since the paper is transparent about the design choice.

## Novel Insights

Beyond the paper's own contributions, the clearest insight emerging from the reviews is that the dramatic cross-modal model-rank reversals (GPT-5: worst in c-Interact, best in a-Interact; Gemini-2.5-Pro: the reverse) suggest that interactive capability in structured vs. open-ended modes is largely orthogonal to single-turn SQL competence. The memory grafting experiment provides suggestive evidence for decoupling communication from generation, though the confound limits strong conclusions. These observations point toward a richer, multi-dimensional model evaluation landscape than single-turn benchmarks capture.

## Suggestions

1. **Reframe the "ITS Law"** as an observed scaling trend for certain models in the c-Interact setting. Use measured language such as "interaction test-time scaling pattern" rather than "law." Explicitly note where the data does not support the scaling claim (a-Interact mode, several models).

2. **Add a controlled comparison experiment** on at least one existing multi-turn benchmark (COSQL or SParC) with the same model set. Show that BIRD-INTERACT produces different model rankings or that the gap between single-turn and multi-turn performance is larger than on existing benchmarks. This would convert the "more challenging" claim from a circumstantial assertion to a demonstrated property.

3. **Explicitly bound the benchmark's scope** in the introduction and conclusion: BIRD-INTERACT tests interaction within a pre-specified, annotated ambiguity space using controlled simulators. This is a feature (controllable, reproducible evaluation) not a bug, but the current framing as "complete interactive problem-solving process" oversells the degree of open-endedness relative to what the benchmark actually measures.

4. **Add at least one qualitative failure trace** (e.g., a model that fails because it asks the wrong clarification question) to make the benchmark's diagnostic value concrete for readers.

5. **Include a brief statement about the user simulator's LLM configuration** (temperature, etc.) in the main text rather than only in the appendix, since this affects the reproducibility of evaluations.

## Score and Decision

**Round 1 bracket:** I estimate this paper sits between 5.5 and 7.0.

**Calibration anchors retrieved (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| XmProj9cPs.md (Spider 2.0) | 8.00 | R1 | Yes | Stronger paper — virtually no negatives; enterprise-scale benchmark with broader scope |
| GGlpykXDCa.md (MMQA) | 8.00 | R1 | Yes | Stronger — cleaner multi-table QA benchmark with comprehensive evaluation |
| roNSXZpUDN.md (τ-bench) | 6.50 | R1/R2 | Yes | Similar quality — both are interactive benchmarks with user simulators; τ-bench has stronger negatives (-7.17 overclaiming, -5.16 user sim concerns) than this paper |
| jp3gWrMuIZ.md (MINT) | 6.75 | R2 | Yes | Similar quality — both benchmark multi-turn interaction; MINT has more severe negatives (-7.26 biased task selection, -6.63 unjustified claims) |
| CvGqMD5OtX.md (CHASE-SQL) | 6.25 | R1 | No | Method paper, not directly comparable |
| 6guG2OlXsr.md (MTU-Bench) | 5.75 | R2 | No | Tool-use benchmark with narrower scope |

**Weighted-item comparison:** My draft's strongest negative is the ITS Law overclaim (-5.20). This is milder than τ-bench's overclaiming criticism (-7.17) and MINT's biased-task-set criticism (-7.26). My strongest positives (+5.47, +5.55) are comparable to τ-bench's (+6.26) and MINT's (+5.72). The shared heavy-weight positive across all accepted anchors is a novel, well-validated benchmark that fills a real gap — this paper has that. The missing heavy-weight positive relative to Spider 2.0 and MMQA is the absence of a clean comparison showing the benchmark is distinctively harder than prior work. Placing this paper below τ-bench and MINT would be too harsh given that its user simulator is actually a validated strength (not a criticized weakness like τ-bench's). Placing it at Spider 2.0's level (8.0) would be too generous given the ITS Law overclaim and missing comparative evidence. The 6.0–7.0 range aligns with the calibration anchors.

**Final score: 6.5** — A solid benchmark paper with a genuinely useful technical contribution (the function-driven user simulator) and interesting empirical findings. The ITS Law overclaim and lack of direct comparative validation against existing benchmarks are fixable issues that do not undermine the core contribution. With recalibrated claims and additional comparative analysis, the paper would fully earn its place in this range.

**MY FINAL SCORE:** <score>6.5</score>
**MY FINAL DECISION:** <decision>Accept</decision>