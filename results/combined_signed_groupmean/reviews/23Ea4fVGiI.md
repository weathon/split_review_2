Now I have sufficient calibration data. Let me compile the final review.

All anchors retrieved across rounds:

1. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/koza5fePTs.md` (avg 2.00) - Round 1, itemized. Benchmark paper on LLM planning; weaker method novelty than this paper, similar evaluation rigor concerns.
2. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/cWrqs2lwCJ.md` (avg 3.00) - Round 1, itemized. Backward planning paper; mixed reviews, evaluation concerns but proposes a novel algorithm.
3. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/jOuHjFw71C.md` (avg 3.00) - Round 1, itemized. o1 evaluation on PlanBench; limited to benchmarking, no new method.
4. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/BW8O4wHgbo.md` (avg 3.00) - Round 1. Multi-agent path finding with LLMs; focused on negative results.
5. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/sdpVfWOUQA.md` (avg 3.00) - Round 1. MCTS planning framework; better evaluation but less conceptual novelty.
6. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/DZBFchnM3b.md` (avg 3.67) - Round 1. Search problems benchmark; different framing.
7. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/UiLtbLsiPU.md` (avg 4.50) - Round 1. Embodied task planning benchmark; limited relevance.
8. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/OPdmIxdkPb.md` (avg 4.75) - Round 2, itemized. Query-efficient planning; clean evaluation, some novelty concerns.
9. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Glcsog6zOe.md` (avg 5.25) - Round 2. Tree-Planner; better evaluation and ablation design.
10. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/SkETBJRKH7.md` (avg 5.25) - Round 2, itemized. PFC-inspired architecture; limited scope but clean evaluation.
11. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/85Ik12q2hP.md` (avg 4.00) - Round 2, itemized. Critical ReAct evaluation; strong methodology, limited novelty.
12. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/iNcEChuYXD.md` (avg 4.50) - Round 2. Modular agentic architecture; broader scope.
13. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/CfdPELywGN.md` (avg 5.20) - Round 2. Cognitive maps for path planning; similar inspiration source.
14. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/rpbzBXdo4x.md` (avg 5.00) - Round 2. CoT performance reduction; limited relevance.
15. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/GO4Sd6LUuY.md` (avg 4.25) - Round 2. EC-Agent; different problem domain.
16. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/K3KrOsR6y9.md` (avg 6.40) - Round 1, itemized. AoT+ prompting; strong clean evaluation and results, clearly above this paper.
17. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/P8FS9byr1c.md` (avg 3.75) - Round 2. Plan retrieval framework; limited domain overlap.

**Round 1 bracket**: Between 3.0 and 5.0, with the paper sitting closer to 3.0 than 5.0.

**Narrowing**: Comparing itemized impact scores, my draft's decisive weakness pulls (-10.00 for overclaimed mechanism, -9.91 for shot-count) match the severity profile of papers scoring ~3.0 (like jOuHjFw71C). Unlike papers at 4.0+ (like 85Ik12q2hP at 4.0, which had clean evaluation methodology), this paper has structural confounds in its central comparison. My draft's strongest strength (+9.89 for the o1 improvement) is tempered by the fact that the result itself is contested by the evaluation confounds.

**Final score**: 3.0

---

## Summary

This paper proposes applying the TMK (Task-Method-Knowledge) framework from cognitive science as a structured prompting technique to improve LLM performance on PlanBench Blocksworld planning tasks. The authors evaluate TMK across several models (GPT-4, GPT-4o, o1-mini, o1, GPT-5) and report striking results, including a 65.8pp gain for o1 on Random Blocksworld (31.5% → 97.3%). They also present a "performance inversion" observation and advance a mechanistic hypothesis about TMK steering models toward code-execution pathways.

## Strengths

- **Dramatic reported improvement for o1 on Random Blocksworld (31.5% → 97.3%).** If this result holds under properly controlled conditions, a 65.8 percentage point gain on a benchmark that has resisted substantial improvement through prior prompting methods would be a meaningful contribution. **[impact=+9.89]**
- **The "performance inversion" observation is a clever analytical lens.** The fact that o1 performs worse on Random than Mystery under plain text, but the reverse under TMK, provides internal evidence that TMK is doing something qualitatively different from simply providing more context. **[impact=+7.24]**
- **The paper correctly identifies and avoids some known experimental pitfalls.** It uses PlanBench's formal plan verification (every step must be correct), provides a non-tailored one-shot example that does not match the problem, and engages critically with the literature on prompting-for-planning failures (Stechly et al., Bhambri et al.). **[impact=+8.81]**

## Weaknesses

### Fatal
None.

### Major

- **Shot-count mismatch confound.** TMK uses one-shot prompting while the primary baselines from the public PlanBench leaderboard are zero-shot. The paper acknowledges this (Section 3.2) and argues it is conservative because zero-shot outperforms one-shot for plain text, but the actual one-shot plain-text numbers are not reported in the main table or text. The claim that zero-shot > one-shot uniformly for Blocksworld planning is asserted without direct evidence in the main paper. A fair comparison requires one-shot plain-text baselines run under identical conditions.

- **Differential extraction function.** The TMK results on Random Blocksworld use an enhanced extraction function (lines 183-191) that is more permissive of formatting variations (extra words, symbols). The plain-text baselines from the public leaderboard use standard PlanBench extraction. The paper acknowledges these artifacts are "common in random blocksworld" (line 191) and "rare in classic blocksworld." Since the enhanced extraction is applied only to TMK results, some of the reported improvement — especially the large o1 Random gain (31.5% → 97.3%) — could be an artifact of differential evaluation leniency, not genuine planning improvement. The same extraction function must be applied uniformly to both conditions.

- **No ablation or control for information content.** The TMK prompt replaces the "domain portion" of the PlanBench prompt with a JSON structure that explicitly includes preconditions, effects, descriptions, inputs, outputs, and relational knowledge. The natural-language PlanBench prompt likely does not contain all this information with the same explicitness. The improvement could therefore reflect providing **more complete domain information** rather than the TMK structure per se. A minimal control — providing the same information in natural language prose — is needed to attribute gains to TMK's specific structure rather than to the additional content it happens to encode.

- **Overclaimed mechanistic narrative.** The abstract and conclusion state that TMK "steers reasoning models away from their default linguistic modes to engage formal, code-execution pathways" as an empirical finding. However, the paper provides no mechanistic evidence (no analysis of model internals, no probing experiments, no ablation isolating the mechanism). The "performance inversion" is consistent with this hypothesis but also with multiple alternatives: richer domain knowledge, reduced ambiguity through explicit pre/post conditions, triggering JSON-completion priors, or simply longer/more detailed prompts. The paper's own logical argument — "If TMK were simply providing additional context, we would expect uniform gains across domains" (line 282) — is not sound, since additional context can certainly have non-uniform effects depending on how it resolves ambiguity in different domains. The claim should be presented as a hypothesis, not a demonstrated finding.

### Minor

- **No statistical rigor.** All results are reported as single-point accuracies with no confidence intervals, error bars, or variance measures. Test set sizes are not stated. For smaller improvements (e.g., GPT-5 Mystery: 98.1 → 98.3; GPT4o Classic: +9.8pp), readers cannot assess whether differences are meaningful or noise. While single-run evaluation is common on PlanBench, providing basic confidence intervals would substantially strengthen the empirical contribution.

- **The o1-mini anomaly is unexplained.** The regression on Mystery (19.1 → 16.83) is noted but the explanation ("capacity limitations in resolving semantic interference") is speculative. Without further analysis or additional model sizes, this remains an unexplained outlier that complicates the narrative.

### Trivial
None.

## Nice-to-Haves
- Comparison with other structured prompting baselines (e.g., a simple JSON-formatted domain description without the full TMK hierarchy) would strengthen the claim that TMK's specific structure matters.
- Testing on additional PlanBench domains (Logistics) or other planning benchmarks would help assess generalizability.

## Removed Points
These points are flagged to be removed, treat them with caution.

- **HTN/BDI comparison criticism**: Removed because the paper explicitly states that comparing to HTN/BDI is future work (line 304: "For future work, we hope to... evaluate how well TMK performs when compared to other knowledge models such as BDI and HTNs"). The paper distinguishes TMK conceptually but does not claim empirical superiority.
- **Missing related works**: Removed per instructions — external sources cannot confirm their existence.
- **Formatting/style nitpicks**: Removed per instructions.
- **Reproducibility nitpicks about undisclosed hyperparameters**: Removed per instructions.
- **Speculation about "not yet released" models or datasets**: Removed per instructions.

## Novel Insights
None beyond the paper's own contributions. The reviews do not surface genuinely novel observations about the paper that the paper itself does not already contain or imply.

## Suggestions

1. **Run plain-text one-shot baselines** for every model/domain combination in Table 2, using the **same extraction function** as the TMK condition. This single change would resolve both the shot-count and extraction confounds simultaneously.
2. **Add an information-matched control**: Provide the same domain knowledge (preconditions, effects, action descriptions) that the TMK JSON encodes, but in natural language prose. If TMK still outperforms this matched control, you have evidence that structure matters beyond content.
3. **Temper the mechanistic claims**. Replace "steers reasoning models away from their default linguistic modes to engage formal, code-execution pathways" with language indicating this is a hypothesis consistent with the data, not a demonstrated mechanism.
4. **Report test set sizes** and provide confidence intervals (bootstrapped or exact binomial) to allow readers to assess whether reported differences are meaningful.
5. **Compare against at least one structured-prompting baseline**, such as a simple JSON-formatted domain description without the full TMK hierarchy.

## Score and Decision

**Round 1 bracket**: Between 3.0 and 5.0, with the paper sitting closer to 3.0 than 5.0.

**Narrowing**: Comparing itemized impact scores, the decisive weakness pulls (-10.00 for overclaimed mechanism, -9.91 for shot-count mismatch) match the severity profile of papers scoring ~3.0 (e.g., `jOuHjFw71C` at 3.00 for o1 PlanBench evaluation). Unlike papers at 4.0+ (e.g., `85Ik12q2hP` at 4.00, which had clean evaluation methodology despite limited novelty), this paper has structural evaluation confounds in its central comparison. The strongest strength (+9.89 for the o1 improvement) is substantially tempered by the fact that the result itself is contested by differential extraction and shot-count confounds. The paper's novel conceptual contribution (applying TMK from cognitive science) is genuine, but the evaluation does not currently support the claimed findings.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>