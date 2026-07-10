Now I have all the data I need. Let me write the final consolidated review.

**Calibration Summary:**

| Anchor | Path | Score | Round | Itemized | Comparison |
|--------|------|-------|-------|----------|------------|
| Exploring & Benchmarking Planning Capabilities | koza5fePTs.md | 2.00 | R1 | Yes | Lower novelty; our paper has genuine novel contribution |
| Planning in Strawberry Fields (o1 eval) | jOuHjFw71C.md | 3.00 | R1 | Yes | No new method; our paper has novel TMK framework |
| Do Think Tags Really Help LLMs Plan? | 85Ik12q2hP.md | 4.00 | R2 | Yes | Stronger systematic analysis but no novel solution; our paper has novel idea but weaker controls |
| Tree-Planner | Glcsog6zOe.md | 5.25 | R2 | Yes | Better evaluation rigor, ablation studies; our paper has more novel framing but weaker controls |
| LLMs Can Plan Only If We Tell Them (AoT+) | K3KrOsR6y9.md | 6.40 | R1 | Yes | Much stronger evaluation with comprehensive ablations; our paper's evaluation less rigorous |
| Take a Step Back | 3bq3jsvcQ1.md | 8.00 | R1 | Yes | Excellent evaluation across many domains; much stronger overall |

**Initial bracket:** Between 4.0 and 6.0 (stronger than 3.0 anchors with no novel method, weaker than 6.4 anchor with comprehensive evaluation).

**Narrowing:** The paper's strength (novel TMK framing, striking o1 Random result) places it above purely evaluative papers at 3.0. But the evaluation gaps (shot-count confound, no structured control, extraction concerns, no variance) reduce rigor below papers at 5.25+ which typically include ablations and controls. The closest anchor is the "Do Think Tags" paper (4.00) which similarly has a valid contribution but significant evaluation limitations, though our paper's novel positive contribution (not just critique) pushes it slightly higher.

**Final score: 4.5** — The paper has a genuinely novel framing and striking results, but the evaluation has three significant gaps (shot-count confound, missing control for structured format, extraction function asymmetry) that prevent the core claims from being fully accepted on current evidence.

Now the final review:

## Summary
This paper proposes TMK (Task-Method-Knowledge), a prompting framework borrowed from cognitive science, to improve LLM planning on PlanBench Blocksworld variants. It evaluates TMK one-shot against plain-text baselines from the public leaderboard, reporting impressive gains including o1 Random Blocksworld going from 31.5% to 97.3%. The paper also observes a "performance inversion" (Random > Mystery under TMK for o1) and offers mechanistic hypotheses about symbolic steering.

## Strengths
- **Novel and well-motivated framing.** Borrowing TMK from cognitive science (Murdock & Goel, 2008; Dass et al., 2025) is genuinely different from the usual CoT/ReACT prompting literature. Section 2.3 and Figure 1 concretely illustrate why TMK's explicit representation of goals, mechanisms, and teleology could address known LLM planning failures.
- **The o1 Random Blocksworld result is striking.** Going from 31.5% → 97.3% (a 65.8 percentage point gain) on the hardest, most symbolic variant is impressive. The performance inversion (Random > Mystery under TMK for o1) is a genuinely interesting empirical pattern.
- **The paper addresses known criticisms of prior prompting work.** Section 5.1 explicitly tackles pattern matching concerns, evaluation of full plans, and domain generality, showing methodological awareness.

## Weaknesses

### Major
1. **Shot-count confound between TMK and baseline.** The paper compares TMK one-shot against plain-text values that, for older models from the leaderboard, are zero-shot. While the table header says "best of sampled Zero & One shot" and the paper argues conservatism (zero-shot is harder, so any improvement is meaningful), the actual one-shot plain-text numbers for the specific models and problem sets are not presented in the paper — they are deferred to an external OSF link as "sample testing." This means some fraction of the observed gain could be attributable to having a one-shot example rather than to TMK's specific properties. (Section 3.2, lines 177-181; Table 2.)

2. **No control for structured format vs. TMK-specific content.** The TMK prompt uses JSON with explicit fields; the baseline is plain text. This design cannot distinguish whether gains come from (a) TMK's causal/telological structure, (b) any structured hierarchical format (e.g., a non-TMK JSON schema), or (c) simply providing more domain knowledge. A minimal control condition is absent. (Section 3.2; Table 2.)

3. **Modified extraction function for Random Blocksworld creates uncertainty about fair comparison.** The paper states (lines 183-191) that extraction criteria were updated for Random Blocksworld, adding tolerance for symbols, extra words, and formatting artifacts. It is not explicitly stated whether the same enhanced extraction was applied to the plain-text baseline numbers from the leaderboard. If the leaderboard used stricter extraction, TMK outputs could benefit from a more lenient evaluation, invalidating the comparison. (Section 3.2, lines 183-191.)

### Minor
4. **No variance or statistical significance reported.** Results are presented as point estimates with no error bars, confidence intervals, or number of runs per condition. For stochastic LLM outputs, this omission prevents assessing whether gains are reliable. (Table 2; Section 4.)

5. **Mechanistic claims in the abstract go beyond what the evidence supports.** The abstract states TMK "steers reasoning models away from their default linguistic modes to engage formal, code-execution pathways," but the paper provides no causal evidence about internal processing. This is a reasonable hypothesis (discussed as such in Section 5.2.1) but is presented too definitively in the abstract.

6. **Gap between related-work critique and evaluation scope.** Section 2.1 critiques CoT, CoS, and ReACT at length but the evaluation only compares TMK against plain text, not against any of these methods. This weakens the positioning of TMK as an alternative to these techniques.

### Trivial
None.

## Nice-to-Haves
- Presenting one-shot plain-text numbers for all models would resolve the main confound.
- Adding one structured control (same domain knowledge in a non-TMK JSON schema or well-formatted YAML) would strengthen attribution to TMK-specific structure.
- Reporting plain-text numbers re-evaluated with the same modified extraction function would eliminate evaluation-artifact concerns.
- Reporting variance (number of runs, confidence intervals) across conditions.

## Removed Points
- "The prompt formatting is not in the paper / reliance on external repository" — removed per instructions (appendix stripped by parser, exists in original).
- "No comparison against any existing prompting technique (CoT, ReACT, CoS)" — downgraded from Major to Minor; the paper scopes itself around the PlanBench baseline, which is a reasonable design choice, but the related work creates an expectation that is not met.
- "The performance inversion claim is only for o1, not general" — this is accurate reporting by the paper, not a weakness; the paper correctly identifies which models do and don't show the pattern.
- "Section 5.2.2 connection to Bloom's taxonomy is post-hoc rationalization" — this is standard discussion/conjecture in a "Discussion" section; not a weakness.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Run plain-text one-shot for all models and present those numbers alongside TMK one-shot in the main paper (not just in an external OSF link).
2. Add at least one structured control condition (e.g., same domain knowledge in plain-text bullet points or a non-TMK JSON schema) to isolate whether TMK-specific structure drives gains.
3. Clarify whether the same extraction function was applied to all conditions, or re-run plain-text baselines with the modified extractor.
4. Tone down mechanistic claims in the abstract to match the evidence presented.
5. Report variance (number of runs, confidence intervals) across conditions.

## Score and Decision
The paper introduces a genuinely novel framing (TMK from cognitive science) and reports striking results (o1 Random: 31.5% → 97.3%). However, the evaluation has three significant methodological gaps — the shot-count confound between TMK (one-shot) and baseline (primarily zero-shot), the absence of a structured-format control to isolate TMK-specific effects, and uncertainty about whether the modified extraction function was applied uniformly. These gaps prevent the paper's core claims from being accepted on the current evidence.

**Score: 4.5 — Borderline Reject.** The contribution is potentially real and the idea is interesting, but the evaluation needs major strengthening before the claims are supported.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>