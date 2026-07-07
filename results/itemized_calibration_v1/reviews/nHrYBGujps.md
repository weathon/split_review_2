## Summary

BIRD-INTERACT is a benchmark paper introducing a new evaluation suite for multi-turn, interactive text-to-SQL. Built on LIVESQLBENCH, it provides 900 tasks with injected ambiguities, a function-driven user simulator designed to avoid ground-truth leakage, two evaluation settings (c-Interact for protocol-guided and a-Interact for open-ended agentic interaction), and CRUD operations extending beyond SELECT-only. Evaluations of 7 frontier LLMs show very low success rates (best ~25% normalized reward), demonstrating the benchmark's difficulty and the gap between current SQL generation and interactive capability.

## Strengths

- **The gap is real and well-motivated.** Existing multi-turn benchmarks (CoSQL, SParC) provide static transcripts — predetermined dialogue histories identical for every model — which cannot reward intelligent interaction strategies or penalize conversational failures. The paper correctly identifies this blind spot.

- **Function-driven user simulator is a concrete technical contribution.** The two-stage approach — a semantic parser mapping model queries to AMB/LOC/UNA actions before response generation — is a principled solution to ground-truth leakage in simulator-based evaluation. USERSIM-GUARD evaluation (Figure 6) shows baseline LLM simulators fail to reject inappropriate queries up to 67.4% of the time, while the function-driven version reduces this to 2.7%. Human alignment (Table 3) shows improved correlation with human evaluators (r=0.84 vs. 0.61).

- **CRUD expansion is valuable and under-explored.** Including INSERT, UPDATE, DELETE, and DDL operations extends text-to-SQL evaluation beyond the narrow SELECT-only scope of other benchmarks. The BI vs. DM breakdown in Table 2 provides useful information about where different models struggle.

- **Action distribution analysis** (Section 5.2) surfaces an interesting behavioral observation: models disproportionately use *submit* and *ask* (60.87% of actions) over knowledge/schema retrieval, providing the kind of insight a benchmark should enable.

## Weaknesses

### Fatal
None.

### Major

1. **Ambiguity injection methodology has unaddressed construct validity concerns.** The paper states that ambiguities are *injected* into otherwise well-specified single-turn queries from LIVESQLBENCH. Three types are described: surface-level ambiguity in user language, knowledge ambiguity where HKB entries are removed/masked, and environmental ambiguities. The "knowledge chain breaking" (masking intermediate nodes in the HKB so the model must ask the user to fill them in) is particularly artificial. Real-world ambiguities typically arise from underspecification in user goals, domain-specific jargon, or mismatched expectations — properties not obviously approximated by removing entries from a knowledge base. Models evaluated on this benchmark could learn patterns specific to the injection methodology (e.g., "when there is a gap in the knowledge DAG, ask the user about it") rather than developing generalizable interactive skills. The paper provides no evidence that injected ambiguities resemble naturally-occurring ones, which is a structural concern for a benchmark whose value proposition is realism.

2. **The "dynamic interaction" framing overstates what c-Interact delivers.** The paper's central critique of existing benchmarks is their reliance on "static conversation transcripts." However, in c-Interact, the interaction is tightly bounded by pre-annotated ambiguity points. The budget is `τ_clar = m_amb + λ_pat`, where `m_amb` is the *number of annotated ambiguities*. The user simulator can meaningfully respond to queries about these pre-specified ambiguities (via AMB()), handle reasonable-but-unannotated clarifications (via LOC()), or reject inappropriate queries (via UNA()). A model that asks an equally reasonable clarification question not in the annotation set receives a LOC() or UNA() response and burns budget without making progress. This means c-Interact partially measures alignment with annotators' expectations about *which* ambiguities matter, not open-ended interactive capability. While the paper acknowledges the protocol-guided nature, the contrast with "static transcripts" is sharper than the evidence sustains.

### Minor

3. **The "ITS Law" is asserted from insufficient evidence.** The paper defines an "ITS Law" — a model with enough interactive turns can match or surpass idealized single-turn performance — and illustrates it primarily with one model (Claude-3.7-Sonnet) in Figure 4. The abstract claims "performance improves monotonically with additional interaction opportunities across multiple models," but other models in the figure do not clearly show this pattern; some appear flat or decreasing. Generalizing an observation into a "law" on this evidence is not justified.

4. **Memory Grafting experiment has unaddressed confounds.** The experiment shows GPT-5's performance improves (13.8% → 18.8–20.5%) when given interaction histories from better-performing models (Qwen-3-Coder, O3-mini). The paper concludes GPT-5's weakness is in communication rather than SQL generation. However, the grafted history contains not only ambiguity resolutions but also the SQL solutions (or strong hints) produced by the source models. GPT-5 may benefit from seeing better SQL, not just better interaction patterns. A cleaner control would compare GPT-5 with its *own* interaction history or graft only the clarification dialogue without solutions.

5. **Single-run evaluation with no uncertainty quantification.** The paper states "conducting single runs due to cost" with temperature=0. Even with deterministic decoding, frontier model APIs exhibit some non-determinism. With 600 tasks and success rates of 8–25%, the raw counts are modest — GPT-5's 8.67% SR in c-Interact represents ~52 solved tasks out of 600; a binomial 95% CI spans roughly 6.4% to 10.9%. Several reported differences between models (e.g., GPT-5's 29.17% vs. Claude-Sonnet-4's 27.83% in a-Interact) fall within plausible noise ranges. Bootstrapping over tasks would help distinguish signal from noise.

6. **USERSIM-GUARD evaluation is not connected to main benchmark outcomes.** The simulator analysis (Section 6) convincingly demonstrates that the function-driven simulator is more controllable than baselines. However, the paper does not report whether model rankings or conclusions change when using a baseline simulator instead. Without this comparison, the analysis shows controllability but does not validate that the main benchmark results depend on the improved simulator.

7. **Inter-agreement score is unspecified.** Table 1 reports "Inter-Agreement | 93.33 | 93.50" without clarifying the metric — is this percentage agreement, Cohen's kappa, or something else? Agreement on what (ambiguity annotation, SQL correctness, task labels)? This makes it difficult to assess annotation quality from the main text.

8. **Follow-up sub-task SR is mechanically confounded.** Because follow-up sub-tasks can only be attempted after the primary sub-task succeeds (Section 4.1 states "failure in the initial priority sub-task immediately terminates the entire session"), lower follow-up SR partly reflects the sequential structure. Reporting conditional SR (follow-up success given primary success) would isolate whether follow-ups are genuinely harder or just penalized by the dependency.

### Trivial
None.

## Nice-to-Haves
- A small human study characterizing how injected ambiguities compare with naturally-occurring ones would directly address the construct validity concern.
- A comparison run (on a subset) with a baseline non-function-driven simulator to demonstrate that model rankings depend on simulator choice.
- Qualitative case studies showing representative successes and failures would ground the analysis and increase practical value.

## Removed Points
These points from the input review were removed after verification:

1. **"No code or data release commitment stated in the paper"** — Removed per hard rule: criticisms questioning the existence/release status of a cited resource are disallowed. The paper cites LIVESQLBENCH as open-source infrastructure.
2. **Pure formatting/style nitpicks** — Removed per hard rules (parser artifacts, not author errors).
3. **Criticisms about missing appendix content** (e.g., "important details deferred to appendices") — Removed per hard rule: the parser strips appendices from all papers; they exist in the original submission.
4. **The characterization that Memory Grafting "tells us nothing" and "any model would improve"** — Weakened to Minor. The experiment does provide meaningful directional evidence (GPT-5 + O3-mini history at 20.5% beats O3-mini alone at 18.5%), and the source model controls partially address this concern. The remaining confound is noted in Minor weakness #4.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add bootstrapped confidence intervals or error bars to Table 2.
2. Report conditional follow-up SR (given primary sub-task success) to disentangle mechanical confounds.
3. Clarify the inter-agreement metric in Table 1 (metric type and annotation target).
4. Temper claims: rename "ITS Law" to "ITS Observation" or "ITS Pattern"; soften the "dynamic interaction" framing for c-Interact.
5. Add a comparison run with a baseline (non-function-driven) simulator on a subset to validate the simulator's impact on conclusions.
6. Consider a small human study comparing injected vs. naturally-occurring ambiguities to address construct validity.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>