## Summary

This paper introduces MISINFOTASK, a 108-task benchmark dataset for studying misinformation injection in multi-agent systems, and ARGUS, a two-stage training-free defense framework. ARGUS first adaptively localizes misinformation-propagating communication channels using topological importance and semantic relevance signals, then deploys a goal-aware corrective agent that uses chain-of-thought reasoning to detect and rectify misinformation across multiple rounds.

## Strengths

- **Well-motivated problem framing (Section 1, Figure 1).** The paper draws a clear and practical distinction between overtly malicious/jailbreak content and covert misinformation (semantically benign but factually incorrect). This distinction is meaningful for MAS security because the latter is harder to detect with conventional methods yet equally harmful.
- **Principled two-stage architecture (Sections 4.1–4.2).** The separation into Adaptive Localization (spatial: which channels to monitor, combining edge betweenness centrality, semantic relevance to inferred goals, and channel frequency) and Goal-aware Rectification (temporal: multi-round analysis via CoT-based detection and correction) is well-motivated and technically sound.
- **Comprehensive ablation study (Tables 2–3).** The ablation removes each of the three localization components (topology, relevance, frequency) and each of the three rectification components (dynamic localization, CoT revision, multi-turn correction), providing clear evidence that each component contributes to overall performance.
- **Dataset fills a genuine gap.** MISINFOTASK targets a specific gap — the lack of benchmarks designed for misinformation (as opposed to malicious/jailbreak content) in MAS. The inclusion of task descriptions, misinformation goals, supporting/refuting arguments, and ground-truth reference solutions for each sample is a well-structured data design.

## Weaknesses

### Fatal
None.

### Major

1. **Unvalidated evaluation metrics undermine quantitative claims.** The headline claims (28.17% MT reduction, 10.33% TSR improvement) rest entirely on MT and TSR scores computed by an LLM judge (GPT-4o) measuring "semantic consistency" between system outputs and reference answers. **No human evaluation is conducted** to validate that the LLM judge's scores correlate with human judgments of factual correctness or task completion. This is especially critical for a paper about misinformation, where ground truth matters. The same model family (GPT-4o) is used both as the judge and as a core LLM in the system being evaluated, introducing potential evaluation contamination. Additionally, the TSR metric depends on a threshold θ_m (Equation 1) whose value is **never specified or justified** anywhere in the visible text.

2. **No variance or statistical significance for main results.** Table 1 reports point estimates with subscripts indicating differences from the attack-only baseline (an unexplained notation), but **no standard deviations or confidence intervals** are provided. The Figure 2 caption mentions "three independent experimental trials," yet these trials are never aggregated into variance estimates in the main results. Without variance, the reader cannot assess whether reported improvements (e.g., ARGUS's 84.33% TSR vs. Self-Check's 82.60% TSR for DeepSeek-V3 — a 1.73 pp gap) are statistically meaningful.

3. **Limited baselines and modest advantages.** Only two baselines are compared: Self-Check and G-Safeguard. Missing baselines include: (a) a retrieval-augmented fact-checker agent, (b) multi-agent debate/consensus (Chern et al., 2024 — cited in the paper's own related work but not compared against), and (c) simple instruction hardening. ARGUS's advantage over Self-Check is small in several settings (~1.7–2.6 pp TSR improvement for DeepSeek-V3 and Gemini-2.0-flash), which — combined with the absence of variance — makes it unclear whether these differences are meaningful.

4. **Inconsistent quantitative claim in the abstract.** The abstract (line 24) states ARGUS achieves "reducing misinformation toxicity by approximately 38.24% across various core LLMs." This figure does not match any clear calculation from the results in Section 5.2 and Table 1, where per-attack-type reductions are 28.18%, 20.38%, and 35.95% (averaging to 28.17%, the other number in the abstract). The provenance of the 38.24% figure is unclear and should be explained or corrected.

### Minor

5. **Goal identification accuracy is overstated.** The paper says the corrective agent identifies misleading goals with "high accuracy" (Section 5.2), but Figure 4 shows accuracy ranging from ~0.50 to ~0.80. For Tool Injection, several categories show accuracy around 0.50 — essentially random for a binary classification framing. Since the adaptive re-localization depends on these inferred goals to compute semantic relevance scores, moderate accuracy directly limits the localization mechanism's effectiveness.

6. **Conceptual tension between the definition of misinformation and the defense mechanism.** The paper defines misinformation as "content that contradicts the factual knowledge implicitly stored in the parameters of an LLM" (Section 2.3). The defense relies on the same mechanism — using the LLM's parametric knowledge via "Internal Knowledge Resonance" to detect discrepancies. The paper does not address why the same LLM can reliably detect misinformation in *other agents' outputs* (as the corrective agent) when it was susceptible to that same misinformation in its own processing. This may be addressable (detection is easier than generation; the corrective agent uses a different prompt), but the paper provides no analysis or evidence on this point.

7. **The subscript notation in Table 1 is unexplained.** The subscripts (e.g., 4.54<sub>0.40</sub>) are differences from the attack-only baseline, but the caption does not state this. This is non-standard and makes the table difficult to interpret.

8. **No analysis of ARGUS's computational overhead.** The paper acknowledges efficiency/cost as a limitation (Section 7) but provides no quantitative data. Given that ARGUS runs a corrective agent analyzing every message on monitored channels across multiple rounds, reporting token counts, latency, or cost per task would help readers assess the practical trade-off.

9. **Modest dataset size with evaluation contamination risk.** MISINFOTASK contains 108 tasks generated by an LLM and evaluated by an LLM judge (GPT-4o). Since the judge is similar to the generation model, scores may reflect stylistic pattern-matching rather than genuine task success. With 108 tasks across 4 LLMs × 3 attack types × multiple conditions, the effective sample size per cell is small, and no statistical tests are reported.

### Trivial
None.

## Nice-to-Haves
- Expanding the threat model beyond single-agent compromise to multi-agent coordinated attacks would be a more stringent test of robustness.
- Quantitative analysis of how ARGUS's effectiveness varies across topological structures, beyond the qualitative summary in Section 5.4.
- Testing whether a different (more capable or retrieval-augmented) model for the corrective agent improves goal-identification accuracy.

## Removed Points
These points from the input review were filtered out with brief justification:
- **"Circular dependency is a fatal structural flaw"** — Overstated. Detection (analyzing others' outputs) and generation (producing one's own) are cognitively distinct tasks that can have different susceptibility profiles. The concern is valid but not fatal; demoted to Minor (point 6).
- **"Criticism about the attack-only TSR reduction (20.04%) being insufficiently contextualized"** — The abstract references this number in context and it is consistent with the results. Not a meaningful weakness.
- **"Dataset size is insufficient as a standalone criticism"** — 108 tasks is modest but not unusually small for a specialized benchmark. Rephrased as a minor point about per-cell sample size and contamination risk.
- **"MT metric ambiguity as a structural flaw"** — While MT measures similarity to the misinformation goal, the paper explicitly defines it as quantifying "the extent of misinformation assimilation" (Section 3.2). The interpretability concern is better captured by the need for human evaluation (point 1) than as a separate structural issue.

## Novel Insights
The reviewer's most penetrating observation is that three weaknesses compound each other: (a) unvalidated LLM-judge metrics, (b) absence of variance reporting, and (c) modest margins over Self-Check in several settings. Even if each individually were minor, together they prevent the reader from trusting that ARGUS's reported advantages are real rather than artifacts of the evaluation pipeline. Conversely, the ablation study (Tables 2–3) partially compensates: the clear degradation when each component is removed provides internal evidence that the design choices matter, even if the absolute numbers need validation.

## Suggestions
- **Validate the evaluation pipeline with human judges.** Have annotators rate a stratified sample of 50–100 system outputs on factual correctness and task completion, and report correlation with the LLM judge's scores.
- **Report standard deviations or confidence intervals** for the three experimental trials mentioned in the Figure 2 caption, and add statistical significance tests for key ARGUS-vs-baseline comparisons.
- **Add at least one stronger baseline** — a retrieval-augmented fact-checker agent or a multi-agent consensus mechanism — to contextualize ARGUS's performance.
- **Explain or correct the 38.24% figure** in the introduction/abstract so it can be verified against the results.
- **Report the θ_m threshold value** used for TSR computation.
- **Acknowledge and quantify ARGUS's overhead** (extra LLM calls, latency, cost) to help practitioners assess the trade-off.

## Score and Decision
The paper targets a meaningful and understudied problem, and the proposed framework is principled and well-constructed. However, the evaluation has significant weaknesses — an unvalidated LLM judge as the sole metric, no variance reporting, limited baselines, and an internally inconsistent quantitative claim in the abstract — that prevent the quantitative claims from being trusted at their face value. The paper would benefit substantially from human validation of the metrics, proper statistical reporting, and at least one additional strong baseline. In its current form, the evidence is insufficient to fully support the headline claims.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>