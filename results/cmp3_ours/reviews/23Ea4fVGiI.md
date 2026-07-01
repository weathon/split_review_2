Now I have a well-calibrated picture. Let me write the final review.

## Summary

This paper proposes using the Task-Method-Knowledge (TMK) framework — originally from cognitive science — as a JSON-structured prompt for LLMs on planning tasks. It evaluates TMK on the PlanBench Blocksworld benchmark (Classic, Mystery, Random variants) across five models (GPT-4, GPT-4o, o1-mini, o1, GPT-5) against plain-text leaderboard baselines. The headline finding is o1 improving from 31.5% to 97.3% on Random Blocksworld under TMK, accompanied by a "performance inversion" where Random accuracy exceeds Mystery accuracy — a reversal of the normal difficulty ordering.

## Strengths

- **Novel use of a cognitive-science knowledge representation for LLM prompting.** The TMK framework (Task, Method, Knowledge) with its explicit teleological decomposition is a genuinely different approach from CoT, ReACT, or other existing prompting techniques. The paper provides a concrete JSON serialization, a clear three-layer hierarchy, and a reproducible procedure for converting domain knowledge into the TMK format.

- **The "performance inversion" is a striking empirical observation.** The finding that o1 under TMK scores 97.3% on Random Blocksworld versus 83.3% on Mystery Blocksworld — reversing the normal ordering where Mystery is easier due to semantic cues — is non-obvious and narratively coherent with the steering hypothesis. This result alone is worth further investigation.

- **The experimental design addresses known criticisms of prior planning prompting work.** The paper uses a non-matching one-shot example (avoiding the near-identical example criticism of ReACT), performs full plan validation (not just final-state matching), and compares against the better of zero-shot and one-shot plain text baselines. These methodological choices are well-motivated and appropriate.

- **Transparent about limitations.** The paper acknowledges that "the cause of that increase is left to future work" (Section 6) and discusses the speculative nature of the mechanism explanation.

## Weaknesses

### Major

- **The extraction pipeline for Random Blocksworld differs between the TMK and plain-text conditions, creating an invalid apples-to-oranges comparison.** The paper states (Section 3.2) that the Valmeekam (2023) extraction code "required update" for Random Blocksworld and that the authors "added new code ... to the extraction criteria which was applied for random blocksworld data set." The enhanced function tolerates extra symbols, words, and paraphrased action names. The plain-text baselines in Table 2 are taken from the Valmeekam (2023) leaderboard, which used the original (stricter) extraction. Because one condition was evaluated under a more permissive extraction pipeline, the accuracy differences conflate genuine planning improvement with differential formatting tolerance. This directly affects the paper's headline Random Blocksworld results, including the o1 31.5% → 97.3% finding. The paper's defense — that these are "stochastic errors" that "do not take away from the ability to assess if language models can plan" — misses the issue: even if the tolerance is reasonable in isolation, it cannot be applied to one condition and not the other without breaking comparability.

- **No ablation distinguishes TMK-specific effects from generic structured-domain-knowledge effects.** The comparison is TMK (JSON-structured with task-method-knowledge decomposition) versus plain text (natural language). A necessary control would be the same domain knowledge in JSON but without the TMK decomposition (e.g., flat operator definitions in JSON, or a PDDL description in JSON). Without this, the improvement could come from: putting domain knowledge in a structured format (any JSON works), providing a complete formal specification (PDDL would do this), the specific TMK decomposition, or simply having more text describing the domain. The paper's central claim is about TMK as a framework, but the experimental design cannot separate these competing explanations.

- **No statistical uncertainty or test-set size reported.** Table 2 reports single accuracy numbers per condition. The paper never states how many problems constitute each Blocksworld subdomain. The original PlanBench test set has 200 problems per variant, but the paper does not confirm this. Without confidence intervals or even a sample size, the reader cannot assess whether differences of a few percentage points (e.g., GPT-4o Classic: 35.5% → 45.3%; GPT-5 Classic: 99.3% → 99.7%) represent real effects or noise. While the headline o1 Random result is clearly not noise, the lack of basic reporting undermines the paper's overall empirical rigor.

### Minor

- **The "code-execution steering" mechanism is asserted but not directly evidenced.** The paper claims (Abstract, Section 5.2.1) that TMK "steers reasoning models away from their default linguistic modes to engage formal, code-execution pathways." The primary evidence is the performance inversion itself, which is consistent with multiple explanations (better domain knowledge, longer prompt, JSON structure, the longer prompt giving the model more compute). The paper does not test whether the model actually enters a "code-execution" mode — e.g., by analyzing intermediate tokens, comparing TMK-JSON to a non-JSON structured representation, or examining whether outputs contain code-like reasoning. The cognitive scaffolding discussion (Section 5.2.2) is entirely speculative with no empirical analysis of outputs. The paper would be stronger if the claims were limited to what the evidence supports: TMK improves planning accuracy, and the mechanism is an open question.

- **No experimental comparison against CoT or ReACT.** The paper extensively critiques CoT and ReACT (Section 2.1) but does not compare TMK against them experimentally. This limits the paper's ability to claim TMK "surpasses state-of-the-art performance" (Related Work). Even a non-exhaustive comparison on a subset of conditions would contextualize the results.

- **Performance inversion is demonstrated for only 2 of 5 models.** As the paper acknowledges, GPT-4 and GPT-4o have near-zero plain-text Random scores ("nothing to invert"), and o1-mini does not show the inversion. The inversion claim is supported by exactly two models (o1 and GPT-5). This limits generality and should be stated more carefully.

- **The o1-mini Mystery regression (19.1% → 16.83%) is acknowledged but not investigated.** For a paper claiming TMK improves planning, a condition where TMK *hurts* performance deserves analysis beyond vague references to "capacity limitations" and "semantic overload."

### Trivial

- Table 2 includes o1-preview alongside o1 with a note that it has been "deprecated and replaced by o1." The o1-preview plain-text Random score (37.3%) is actually higher than the o1 Random score (31.5%), which the paper does not discuss. Moving o1-preview to a separate footnote or row would improve clarity.

## Nice-to-Haves

- Re-evaluate plain-text baselines through the same (modified) extraction pipeline to resolve the comparability issue.
- Add a non-TMK structured control condition (e.g., flat JSON operator definitions without the task-method-knowledge decomposition).
- Report problem counts and binomial confidence intervals for each condition.
- Qualitatively analyze model outputs under TMK vs. plain text to examine whether TMK produces measurably different reasoning patterns (e.g., code-like intermediate tokens).
- Compare against at least one alternative prompting method (CoT, ReACT) on the same models and conditions.

## Removed Points

- **Various section-by-section notes about the speculative nature of cognitive scaffolding discussions.** These are observations about the paper's style of argumentation, not specific weaknesses. The core concern (insufficient evidence for mechanism) is already captured in the Minor weakness above.

- **Concerns about statistical reporting that merely restate the absence of a test-set size.** Merged into the single Major weakness about missing uncertainty and test-set size.

- **Criticisms about missing related work and missing appendix content.** Removed per instructions (parser strips appendices; missing related work cannot be verified without external sources).

- **Formatting and style nitpicks (typos, figure quality, whitespace issues).** These are parser artifacts, not author errors.

- **The criticism about o1-preview Random (37.3%) > o1 Random (31.5%) undermining the narrative.** This is a reasonable observation but is a data point the paper could discuss, not a weakness. Kept as part of the Trivial note about Table 2 clarity.

- **The strength "well-motivated framing of the problem."** This is generic praise that any paper could receive. Keeping it would conflict with the paper's actual weaknesses; removed per instructions.

## Novel Insights

Beyond the paper's own contributions, the most useful insight from the review process is that the **extraction methodology comparison issue** is more central than the paper acknowledges. The paper's most striking finding (o1 Random: 31.5% → 97.3%) rests on a comparison where the two conditions were evaluated under different extraction criteria. This is a well-known failure mode in benchmarking (differential evaluation pipelines breaking comparability), and resolving it through re-evaluation of baselines would either confirm a strong result (if the gap persists) or substantially weaken the paper's claims (if the gap shrinks). The performance inversion observation — while interesting — should be treated as preliminary until this methodological issue is resolved, and the paper's strong mechanistic claims (code-execution steering) should be decoupled from the accuracy results until a proper ablation study disentangles TMK-specific effects from generic structured-format effects.

## Suggestions

1. **Re-evaluate all plain-text baselines through the same extraction pipeline used for TMK results.** This is the single highest-leverage fix and would resolve the most serious validity concern.
2. **Add a non-TMK structured control** — the minimal ablation is the same domain knowledge in JSON format but without the task-method-knowledge decomposition. This would establish whether the improvement comes from TMK specifically or from structured JSON generally.
3. **Report the number of test problems per condition and add binomial confidence intervals.** This is basic experimental hygiene.
4. **Tone down the mechanistic claims** (code-execution steering, symbolic scaffold) to match what the evidence supports. Frame these as hypotheses or post-hoc observations rather than demonstrated mechanisms. The paper would be stronger if it said "TMK improves planning accuracy" without asserting an unvalidated mechanism.
5. **Add at least one comparison against CoT or ReACT** on a subset of models/conditions to contextualize the results.

## Score and Decision

**Round 1 bracket:** 3.5 – 5.0. The paper has a novel idea and an interesting empirical observation, placing it above purely benchmarking papers (scores 2–3) but below papers with clean ablations and proper statistical reporting (scores 6+).

**Anchors consulted across all rounds:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `Planning in Strawberry Fields` (jOuHjFw71C) | 3.00 | 1 | Same domain (PlanBench + o1), less novelty (just benchmarking), scored 3 |
| `Exploring and Benchmarking Planning` (koza5fePTs) | 2.00 | 1 | Benchmarking paper with limited novelty, scored 2 |
| `Do Think Tags Really Help` (85Ik12q2hP) | 4.00 | 2 | Critical evaluation of prompting, rigorous but narrow, scored 4 |
| `Prefrontal Cortex-inspired` (SkETBJRKH7) | 5.25 | 2 | Cognitive-inspired architecture, clean evaluation but small tasks, scored 5.25 |
| `Modular Agentic Architecture` (iNcEChuYXD) | 4.50 | 2 | Cognitive-inspired modular approach, similar ambition level, scored 4.5 |
| `LLMs Can Plan Only If We Tell Them` (K3KrOsR6y9) | 6.40 | 1 | Clean methodology, proper ablations, SOTA claims on Blocksworld, scored 6.4 |
| `ActionReasoningBench` (NUD03NBDOE) | 6.75 | 1 | New benchmark with rigorous evaluation, scored 6.75 |

**Narrowing to final score:** The paper has more novelty than the 3.00 papers (which largely benchmarked existing models) but has a significant methodological flaw (extraction incomparability) that the 4.00–6.40 papers do not share. The PFCI paper (5.25) had clean ablations and proper evaluation but was still rejected for limited tasks. Our paper has weaker methodology than all papers at 4.5+, placing it at the lower end of the borderline range. Score 4.0 reflects a paper with a genuinely novel contribution and interesting findings, but whose central quantitative claims rest on an invalid comparison that needs to be resolved before acceptance.

**Final calibration:** The paper's contribution exceeds the 2–3 range (pure benchmarking), but the extraction methodology issue and missing ablations prevent it from reaching the 4.5–6 range (competitive but flawed). Score 4.0 is appropriate for a borderline paper with a promising idea and weak execution on evaluation.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>