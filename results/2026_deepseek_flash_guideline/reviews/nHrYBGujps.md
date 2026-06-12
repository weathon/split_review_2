## Summary
BIRD-INTERACT is a benchmark for evaluating LLMs on multi-turn interactive text-to-SQL tasks. It contributes: (1) a function-driven user simulator that mitigates ground-truth leakage, validated to reduce improper feedback from 67.4% to 2.7%; (2) 900 tasks covering the full CRUD spectrum with injected ambiguities and state-dependent follow-up sub-tasks; and (3) two evaluation settings (c-Interact for conversational protocol, a-Interact for agentic autonomy). Evaluations of 7 frontier LLMs show even GPT-5 achieves only 8.67% success in c-Interact and 17% in a-Interact, establishing a clear gap in interactive text-to-SQL capability.

## Strengths
1. **Function-driven user simulator with strong empirical validation**: Section 3.3 introduces a two-stage approach (action classification → constrained response generation) that demonstrably reduces ground-truth leakage. Section 6 shows baseline simulators fail on UNA questions up to 67.4% of the time, reduced to 2.7% by the proposed approach (Figure 6). Human alignment (Table 3) shows 0.84 Pearson correlation (p=0.02) vs. 0.61 (p=0.14) for baselines — a concrete, statistically significant improvement over prior LLM-based simulators.

2. **State-dependent follow-up sub-tasks that impose measurable additional difficulty**: Section 3.2 introduces state dependency between sub-tasks, where later sub-tasks require reasoning over modified database states from earlier queries. Table 2 confirms this empirically: follow-up sub-task SR is substantially lower than priority SR across all models (e.g., GPT-5 a-Interact: 29.17% priority → 17.00% follow-up; Gemini-2.5-Pro c-Interact: 25.00% → 16.33%), showing the benchmark captures a dimension prior static benchmarks do not.

3. **Memory grafting experiment provides diagnostic signal**: Section 5.2/Figure 5 shows GPT-5's SR rises from 13.8% to 18.8–20.5% when provided with interaction histories from better-performing models. This provides evidence that interaction quality is a separable bottleneck from SQL generation capability — a level of analysis absent from prior benchmarks that only report aggregate scores.

4. **High annotation quality with quantitative evidence**: Inter-annotator agreement of 93.33% (LITE) and 93.50% (FULL) (Table 1) signals that the ambiguity injection and follow-up annotations are reproducible rather than idiosyncratic.

5. **Full CRUD coverage with stratified BI/DM analysis**: The benchmark covers the full CRUD spectrum and partitions tasks into BI and DM types. Table 2 reveals consistent patterns (DM tasks easier than BI across all models), providing richer signal than SELECT-only benchmarks.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
1. **Memory grafting interpretation has confounds**: The experiment provides GPT-5 with full successful interaction trajectories from other models. GPT-5 may be benefiting from these as additional in-context examples that effectively disambiguate task structure, rather than specifically having its "communication deficit" supplemented. The conclusion that GPT-5's SQL generation is robust but communication is deficient is plausible but not uniquely supported by this experimental design. A cleaner comparison would control for information content (e.g., providing GPT-5 with its own interaction history vs. another model's). This does not undermine the benchmark's core contribution but weakens a secondary behavioral claim.

2. **Single-run evaluations without variance estimates**: The paper conducts single runs at temperature=0 citing cost (Section 5). While temperature=0 reduces variance, it does not eliminate it — especially for reasoning models (O3-Mini, DeepSeek-Chat-V3.1) that use internal randomness. Without confidence intervals or a small-scale multi-run study, it is difficult to assess whether reported differences between models (e.g., GPT-5 at 14.50% vs. Qwen-3-Coder at 22.00% in c-Interact priority) are statistically significant or within noise. Given that absolute success rates are low (single digits to mid-twenties), this is a meaningful concern for inter-model comparisons.

3. **No ceiling analysis**: The paper does not analyze what proportion of tasks are solvable under ideal conditions. The "idealized performance" in Figure 4 is defined as single-turn unambiguous performance, not the maximum achievable in the interactive setting. Understanding whether some tasks are inherently unsolvable even with perfect interaction would help the community calibrate expectations and prioritize efforts.

4. **ITS Law defined but not demonstrated**: Section 5.2 defines an "ITS Law" stating that a model can match idealized single-turn performance given enough interactive turns. However, none of the models in Figure 4 actually reach the idealized performance line. The law is stated as a formal claim but no empirical evidence supports it — this should either be removed or reframed as a conjecture/hypothesis.

### Trivial
- The budget formula (τ_clar = m_amb + λ_pat) implicitly reveals information about task difficulty: more budget signals more annotated ambiguities, which a sophisticated system could exploit as an indirect signal.

## Nice-to-Haves
- Analysis of how cost correlates with performance across models (Table 2 reports cost but does not analyze this relationship).
- Discussion of how often the LOC() mechanism is triggered during actual evaluation, and whether the AST-based retrieval handles the range of reasonable unanticipated questions.
- Free-mode experiments (without budget constraints) to observe natural interaction strategies, which the paper already identifies as future work.

## Removed Points
The following points from the inputs were evaluated and removed:
- **Criticism about ambiguity injection limiting open-ended interaction**: The critic notes the benchmark measures resolution of a known ambiguity set. This is a generic property of any closed-world benchmark with ground-truth annotations — not a specific flaw of this paper. The paper explicitly acknowledges this via the LOC() mechanism for handling reasonable unanticipated questions.
- **Criticism about a-Interact being described as "harder" while results show otherwise**: The paper does not claim a-Interact is harder; it describes it as "more open-ended and agentic." The critic inferred a tension not present in the paper's text.
- **Criticism about Normalized Reward weighting lacking justification in main text**: The 70%/30% weighting is stated in Section 5.1, with details deferred to the appendix — standard practice.
- **Generic formatting nitpicks, missing related work concerns, and speculation about unreleased artifacts**: Removed per filtering rules (parser artifacts; papers cited in the submission are assumed to exist).

## Novel Insights
The reviews surface a useful reframing: the function-driven user simulator is the paper's most technically novel and best-validated contribution. The harsh critic correctly notes that positioning this more centrally would strengthen the paper's narrative, while the benchmark construction (ambiguity injection, follow-up tasks) is thorough but follows established practices. The memory grafting experiment is interesting diagnostically but its headline interpretation needs qualification — a nuance the strength finder's framing glosses over.

## Suggestions
1. Add a small-scale multi-run study (e.g., 5 runs on 50 representative tasks) to provide variance estimates, even if limited to a subset of models.
2. Clarify the interpretation of the memory grafting experiment — acknowledge the in-context learning confound and discuss what additional controls would strengthen the conclusion.
3. Provide a ceiling analysis (what proportion of tasks are solvable given perfect communication + perfect SQL?) to help the community understand the benchmark's upper bound.
4. Either remove the formal "ITS Law" definition or explicitly state that it is a conjecture/hypothesis not yet empirically supported.

## Score and Decision
**Calibration anchors (Round 1 — single query used across all bands, 4 hits per band):**

| Band | Path | Avg Score | Comparison |
|------|------|-----------|------------|
| < 1.5 | 5kMwiMnUip (jailbreaking), P49gSPmrvN (discourse), 8QTpYC4smR (survey), nSDOkm0SKo (finance) | 1.0–1.4 | Not comparable |
| 1.5–3.5 | ReKWjKvkJE (SQL method), Avg6hmtgHE (QA), wwO8qS9tQl (ALMANACS benchmark), lMW9d1AqC9 (sign-to-SQL) | 1.67–3.40 | Not comparable |
| 3.5–5.5 | W1x77vRucB (DialSim dialogue simulator) | 5.00 | Similar type, weaker quality (data leakage concerns). **BIRD-INTERACT is stronger.** |
| 3.5–5.5 | NmILZXKcOi (DB-GPT-Hub, 3.75), 7ZeoPg3eTA (TrustSQL, 4.00), NfUHBaZdLw (EvoSchema, 4.25) | 3.75–4.25 | Similar domain but weaker methodology. **BIRD-INTERACT is stronger.** |
| **5.5–7.5** | **roNSXZpUDN (τ-bench, 6.50)** | **6.50** | **Most directly comparable — both benchmark+simulator for agent-user interaction. BIRD-INTERACT has stronger simulator validation (dedicated USERSIM-GUARD dataset, human alignment study, p=0.02).** |
| 5.5–7.5 | CvGqMD5OtX (CHASE-SQL, 6.25), BAglD6NGy0 (ROUTE, 6.25), RaSLSUCKz0 (SQL-GEN, 5.67) | 5.67–6.25 | Method papers, not directly comparable |
| 7.5–8.5 | **XmProj9cPs (Spider 2.0, 8.00)** | **8.00** | Gold-standard benchmark with established lineage. **BIRD-INTERACT is below this tier** (narrower scope, newer lineage). |
| 7.5–8.5 | GGlpykXDCa (MMQA), SQrHpTllXa (CABINET), 7gUrYE50Rb (EQA-MX) | 8.00 | Different domains |

**Round-1 bracket:** 5.5–7.5. **Final score 6.5** — calibrated against τ-bench (6.50) which is the most similar anchor. BIRD-INTERACT has stronger simulator validation than τ-bench but does not reach the tier of Spider 2.0 (8.00, established lineage, broader scope). The weaknesses are real but minor, and the core contributions (benchmark + simulator) are solid.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>