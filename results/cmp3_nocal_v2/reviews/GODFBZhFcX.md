## Summary

This paper presents PCE (Planner-Composer-Evaluator), a framework that extracts implicit assumptions from LLM reasoning traces, structures them into a decision tree, and scores each root-to-leaf path by likelihood × gain − cost to guide action selection in decentralized, partially observable multi-agent embodied settings. The central idea is that LLM planners already generate uncertainty-relevant assumptions in their reasoning traces, but handle them fragmentedly; PCE aggregates and evaluates these assumptions explicitly, reducing reliance on communication. Experiments across two benchmarks (C-WAH, TDW-MAT), three LLM backbones (GPT-4o mini, Gemma3:4B, GPT-OSS:20B), and four communication-centric baselines consistently show PCE achieving higher task success and efficiency.

## Strengths

1. **Well-motivated and empirically grounded insight.** The paper identifies a genuinely useful observation — that LLM reasoning traces already contain implicit assumptions about uncertainty, but these are invoked locally and never systematically aggregated. This is supported with concrete examples (Figure 2a) and shifts the framing from "communicate to reduce uncertainty" to "structure the assumptions you already have."

2. **Clean and principled method design.** The Planner-Composer-Evaluator pipeline follows a logical flow: extract assumptions (Planner), structure them into a decision tree (Composer), then score each path via likelihood × gain − cost (Evaluator, Eq. 1–3). The scoring function is simple, interpretable, and the overall architecture is a coherent design choice rather than a patch.

3. **Extensive empirical scope.** The evaluation covers two benchmarks (C-WAH, TDW-MAT), three diverse LLM backbones spanning commercial and open-source models (GPT-4o mini, Gemma3:4B, GPT-OSS:20B), four strong communication-centric baselines (CoELA, REVECA, CaPo, CoTS), component ablations (Table 3), scaling analyses (Figure 3), and a user study. Across all 6 primary comparisons (3 backbones × 2 benchmarks), PCE achieves the best task-performance result.

4. **Scaling analysis is informative.** Figure 3 shows that a "Planner only" variant (no uncertainty structuring) produces nearly flat improvement as model capacity increases from 4B→12B→27B or reasoning depth increases from Low→Medium→High, while PCE is consistently better. This cleanly supports the claim that scaling alone does not resolve the core problem and that PCE's benefits are additive to scaling.

## Weaknesses

### Fatal
None.

### Major

1. **No variance reporting or statistical significance measures in the main experiments.** Tables 1 and 2 report point estimates only, on benchmarks with as few as 10 episodes (C-WAH) and 24 episodes (TDW-MAT). There are no standard deviations, confidence intervals, per-episode breakdowns, or multiple-seed runs reported anywhere in the main paper. While the consistency of PCE's advantage across all 6 × 3 = 18 condition×metric combinations is encouraging, individual margins (e.g., PCE 42.76 vs. REVECA 46.80 steps on C-WAH with GPT-4o mini — a ~4-step difference on a 10-episode benchmark) could plausibly be within the noise floor. This substantially weakens the reader's ability to assess statistical reliability of the claimed improvements. The paper would be significantly strengthened by reporting variance or per-episode results.

### Minor

2. **"Comparable token usage" claim is overstated for TDW-MAT.** The abstract and conclusion both state PCE achieves "comparable token usage." On C-WAH this is reasonable (PCE is generally in the middle of the pack). However, on TDW-MAT (Table 2), PCE's token consumption is substantially higher than the most efficient baseline (CoELA) across all three backbones: 75% higher for GPT-4o mini, 42% higher for GPT-OSS:20B, and 88% higher for Gemma3:4B. The Introduction (line 29) makes an even stronger claim that PCE "outperforms... in... token usage," which is not supported on TDW-MAT. PCE is more efficient than CaPo and CoTS, but the claim should be recalibrated to reflect variance across baselines.

3. **Undiscussed circularity risk in the scoring mechanism.** The Evaluator uses the same LLM to estimate scenario likelihood (ℒ), conditional gain (𝒢), and execution cost (𝒞). These scores then determine action selection, which feeds back into future observations. If the LLM systematically overestimates the likelihood of assumptions it generated itself, or underestimates costs of its own proposed actions, the scoring becomes self-reinforcing rather than corrective. The paper mentions "human-expert correlation studies" (Appendix A.10, A.11) but the main text offers no discussion of how self-scoring biases are mitigated or why this concern is not expected to significantly affect results.

4. **User study is small and lacks statistical rigor.** The user study (Section 5.3) has 12 participants with no mention of counterbalancing, randomization, or blinding. The Likert-scale results (Figure 4) are presented without error bars or significance tests. The claim that "PCE scored highest across all questions" is descriptive of the observed means but should be treated as suggestive pilot evidence rather than a quantitative finding. The qualitative interview feedback is helpful context but does not constitute a controlled evaluation.

5. **Composer reliability is not analyzed.** The tree construction process (Section 4.3) relies on an LLM-based "local ranking policy" to select which assumption to branch on and to generate new assumptions. The paper does not report how often the Composer produces coherent trees, how frequently contradictory or redundant branches arise, or what the failure modes are. (The ablation in Table 3 shows that removing the Composer degrades performance, but this does not characterize the quality of trees produced by the intact system.)

### Trivial
None that survive filtering (see Removed Points).

## Nice-to-Haves

- Reporting per-episode results or variance estimates would directly address the main evidential concern. This is the single highest-leverage improvement.
- A brief hyperparameter sensitivity discussion for α, β, λ, D in the main text (currently deferred to Appendix A.5) would help readers understand robustness to these choices.
- The token-usage comparison in the ablation (Table 3: "w/o Composer" has lower Usages than PCE while "w/o Planner" has much higher Usages) is interesting but not discussed; unpacking why the Planner is the main token-cost driver would aid understanding.

## Removed Points

- "Figure 4 caption has a garbled repetition of 'PCE (blue)' twice, suggesting figure encoding issues" — Removed as a formatting/parser artifact, not an author error.
- "C-WAH's 10 episodes is a small benchmark" — Removed because the paper inherits this benchmark from prior work, acknowledges it, and also evaluates on TDW-MAT (24 episodes). The point is already subsumed under the variance-reporting weakness.
- Generic concerns about "missing related work" — Not included per instruction (cannot verify from external sources).
- Speculative worry about "how often does the Composer generate incoherent trees" being framed as a fatal flaw — Demoted to Minor weakness #5 with concrete grounding in the paper's text (Section 4.3's underspecification).

## Novel Insights

None beyond the paper's own contributions. The harsh reviewer's observations are useful calibrations of evidential strength (variance reporting, token-usage framing) but do not constitute novel technical insights about the method.

## Suggestions

1. **Report variance.** Add standard deviations, per-episode breakdowns, or confidence intervals to Tables 1 and 2. If running multiple seeds is feasible, do so; otherwise, provide per-episode tables so readers can assess the spread.
2. **Recalibrate token-usage claims.** Replace "comparable token usage" with more precise language acknowledging that PCE's token consumption varies across baselines — it is substantially lower than CaPo/CoTS on TDW-MAT but higher than CoELA.
3. **Discuss the self-scoring concern.** Add a paragraph (or ideally a small calibration experiment) addressing whether the LLM's self-estimates of likelihood, gain, and cost are systematically biased, and why the approach remains sound.
4. **Characterize Composer output quality.** Report a sample of trees generated by the Composer with a brief qualitative analysis, or a simple metric (e.g., fraction of trees with a valid path to the selected action).
5. **Strengthen user study reporting.** Add error bars to Figure 4, state whether conditions were counterbalanced, and hedge the claims appropriately.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>