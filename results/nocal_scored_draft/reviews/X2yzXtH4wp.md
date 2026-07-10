Now let me write the final consolidated review.

## Summary

This paper introduces Ambig-SWE, an underspecified variant of SWE-Bench Verified, and evaluates LLM agents across three diagnostic capacities: (i) detecting underspecificity, (ii) asking targeted clarification questions, and (iii) leveraging interaction to complete the task. The key contributions are the Ambig-SWE benchmark with paired ground-truth specifications, a structured three-capacity evaluation framework, and empirical findings showing that interaction helps all models (up to meaningful performance recovery) but most models struggle to detect underspecificity, and strategies vary substantially (e.g., exploration-first vs. ask-first). Qwen 3 Coder's complete non-interactivity (100% FNR) across all conditions is a particularly striking result.

## Strengths

- **Useful three-capacity decomposition (detection, questioning, integration).** This framework moves beyond a single "did the agent succeed?" metric and enables targeted diagnostic evaluation of where different models fail. Sections 3–5 each cleanly operationalize one capacity with distinct, sensible experimental designs.
- **Thoughtful dataset construction with paired ground truth.** Creating Ambig-SWE from SWE-Bench Verified by synthetically generating underspecified variants alongside their fully-specified originals enables causal attribution of performance differences to resolution of underspecification. The distributional analysis comparing synthetic to real underspecified issues (lines 64–66) is transparent about what is gained and lost.
- **Several genuinely striking and non-obvious empirical findings.** (a) Claude Sonnet 4 achieves 89% detection accuracy under strong encouragement while most models hover near chance (Table 2). (b) The qualitative finding (Figure 4, §5.3) that Claude models adopt an exploration-first strategy (examine the codebase, then ask only what cannot be discovered) while other models ask immediately about code-recoverable details is insightful and actionable.
- **Clean experimental controls.** The user proxy design (§2.2) limits responses to information explicitly present in the issue, and the three-level prompting scheme (Neutral/Moderate/Strong) for the detection experiment is well-justified and well-designed.

## Weaknesses

### Fatal
None.

### Major

- **Asymmetric interaction-turn limits confound model comparisons in the main Interaction experiment (Section 3.1, lines 106–107).** Claude Sonnet 4 and Qwen 3 Coder receive up to 100 interaction turns while all other models are capped at 30. The paper justifies this as accounting for "greater reasoning and planning capacity," but this is circular — the models hypothesized to be stronger are given a structural advantage in the very setting (Interaction) where performance is measured. Without a sensitivity analysis (e.g., capping all models at 30 turns or giving all models 100 turns), the reported performance gaps between model tiers in the Interaction setting cannot be cleanly attributed to capability versus allocated resources. This weakens the reliability of the quantitative comparisons in Figure 3.

### Minor

- **The headline "up to 74%" figure is ambiguously defined and not clearly traceable to the data (abstract, line 9; §1, line 37).** The maximum relative improvement (Hidden → Interaction) across models is 100% (Claude Haiku). The maximum gap recovery, (Interaction−Hidden)/(Full−Hidden), is 76.4% (Claude Sonnet 4). Neither cleanly matches 74%, and no calculation or definition accompanies the claim. A reader cannot reproduce this number from the data in Figure 3.

- **The user proxy is an idealized oracle, and the paper does not bound how much this affects the headline result.** The proxy receives the full issue specification and responds helpfully to all reasonable queries. The paper acknowledges this in §7 (line 281) but treats it as a minor scope constraint. In practice, this choice directly determines the magnitude of the headline finding that interaction improves performance — a less cooperative proxy would likely yield a smaller benefit. A simple sensitivity analysis (e.g., a proxy that answers only 50% of queries or gives partial answers) would substantially strengthen the conclusions.

- **Claude Sonnet 4's Hidden-setting resolve rate (40.0%) is estimated from only 100/500 instances (footnote 4, line 131).** This smaller sample is directly compared against other models' estimates from the full 500-instance set. If those 100 instances were easier or harder than the full set, the calculated interaction benefit and gap recovery for Claude Sonnet 4 could shift. The paper asserts statistical significance (Table 4), but the primary comparison data is not shown in the main paper.

- **The claim that prior work addresses "only a single detail" while this work targets "multiple, interdependent gaps" (lines 31–32, 275) is asserted without evidence.** The synthetic underspecified issues are created by removing details from fully-specified issues — it is not demonstrated that the resulting gaps are genuinely interdependent (rather than simply multiple independent details removed). This overclaim should be either substantiated or removed.

### Trivial
None.

## Nice-to-Haves

- Run a sensitivity analysis with a less-cooperative user proxy (e.g., answering only a random subset of queries, giving only partial answers) to bound how much the oracle assumption affects the headline interaction benefit.
- Run the Interaction setting with uniform turn limits across all models (either 30 for all or 100 for all) to disentangle capability from allocated resources.
- Quantify the exploration-first strategy (e.g., average number of file reads before the first question) to strengthen the qualitative finding in §5.3.
- Include GPT-4o as an evaluated agent for calibration, since it serves as both the issue generator and the user proxy.

## Removed Points

These points from the input are flagged to be removed; treat with caution:

- **Criticism that "there does not seem to be a direct correlation" is an overstatement** — Removed because the paper's claim is about *relative* performance (gap recovery), where Claude Haiku indeed achieves similar performance to Claude Sonnet 3.5 despite inferior coding ability. The claim is defensible from the presented data.
- **Cosine distance metric conflates information gain with other textual differences** — Removed because the paper acknowledges this limitation in §7 (line 281).
- **Gripes about the paper not including GPT-4o as an agent** — Moved to Nice-to-Haves.
- **Complaint about no error analysis of failed interaction trajectories** — Moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Clarify the definition of the "74%" figure in the abstract and introduction, and ensure it is traceable to a specific model and calculation.
- Address the turn-limit asymmetry either through an ablation or by adopting uniform limits; acknowledge this as an explicit bound on the cross-model comparisons.
- Add sensitivity analysis around the cooperativeness of the user proxy to bound the headline interaction benefit.

## Score and Decision

This paper makes a clear contribution: a well-designed benchmark, a useful diagnostic framework, and several genuinely informative findings about how current LLM agents handle underspecification. The weaknesses are real but addressable — the asymmetric turn limits are the most significant concern, but they affect precise cross-model ranking more than the paper's core qualitative conclusions. On balance, the paper brings sufficient value to the community and merits acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>