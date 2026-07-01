## Summary

This paper introduces TMK (Task-Method-Knowledge) prompting, a structured JSON-formatted prompt encoding hierarchical domain knowledge (tasks, methods, and teleological "why" links), and evaluates it on PlanBench Blocksworld variants (Classic, Mystery, Random) against plain-text baselines. The main result is a striking gain on o1 Random Blocksworld (31.5% → 97.33%), alongside the observation that TMK reverses the usual difficulty ordering (Random becomes easier than Mystery).

## Strengths

- **Genuinely large empirical effect on one critical condition.** The o1 model on Random Blocksworld jumps from 31.5% to 97.33% — a 65.8 percentage point improvement (Table 2, o1 Random row). This is far larger than typical prompting gains and warrants attention.

- **Rigorous evaluation metric.** The paper uses PlanBench's full-plan validation (every step must be correct, verified by an external planner), avoiding the partial-matching pitfalls common in prompting research (Section 2.2, lines 51–52).

- **Performance-inversion pattern is empirically interesting and more robust than the critic suggests.** Under TMK, the standard ordering (Mystery > Random) flips for o1, o1-mini, *and* GPT-5 — all three reasoning models show Random surpassing Mystery (Table 2). This consistency across models strengthens the case that something systematic is happening, even if the mechanism remains unclear.

## Weaknesses

### Fatal
None.

### Major

- **No experimental comparison against existing prompting methods for planning.** The paper discusses CoT and ReACT limitations at length (Section 2.1) but never tests whether TMK outperforms them under the same conditions. The entire evaluation is TMK vs. "plain text" (the PlanBench leaderboard). While the paper's scope includes this comparison, the extended discussion of CoT/ReACT creates an expectation that is unmet, and a reader cannot tell whether TMK adds value beyond existing structured prompting techniques. This is the single most important experiment missing from the paper.

- **The central mechanistic claim (code-execution steering) overstates the evidence.** The abstract states that TMK "steers reasoning models away from their default linguistic modes to engage formal, code-execution pathways." The evidence offered is (a) TMK's structural similarity to code and (b) the performance inversion pattern. Neither directly demonstrates a shift in internal reasoning modality. The paper itself later acknowledges "the cause of that increase is left to future work" (line 304), which undercuts the strong causal framing. The mechanistic claim should be softened to a hypothesis requiring further investigation.

- **No ablation study decomposing the TMK intervention.** The TMK prompt bundles hierarchical task decomposition, pre/post conditions, teleological links, JSON formatting, and a one-shot example. Without ablations, it is impossible to attribute the gains to TMK's specific architecture versus any structured representation (e.g., flat JSON with the same information, or bullet-pointed pre/post conditions).

### Minor

- **The one-shot vs. zero-shot confound is acknowledged but not fully resolved in-paper.** TMK uses one-shot prompting and is compared against "best of sampled Zero & One shot" plain text. The paper argues zero-shot plain text is stronger (Section 3.2), but the key evidence for this claim is relegated to an external OSF repository. The paper would be stronger by including those numbers directly.

- **Single-domain evaluation.** All results are from Blocksworld variants. The paper acknowledges this limitation (Section 5.3), but the title and abstract claim generality to "planning tasks." Testing on at least one additional domain (Logistics, or a domain with more complex dynamics) would substantiate the generality claim.

### Trivial
None.

## Nice-to-Haves

- A CoT baseline and a flat-structured-prompt baseline (e.g., the same domain information in non-hierarchical JSON) would cleanly isolate whether TMK's hierarchical + teleological structure drives the gains, or whether any structured formatting helps.
- Reporting confidence intervals or run variance would improve reproducibility assessment.
- Prompt examples should be central in the main paper, not deferred to appendix/external links, given this is a prompting-method paper.

## Removed Points

- **Claim that o1-mini "does not show the inversion."** Factually incorrect — Table 2 shows o1-mini plain text: Mystery 19.1% > Random 9.33%; TMK: Mystery 16.83% < Random 27.0%. The relative ordering *does* invert. Removed.
- **Claim that GPT-5 "does not invert (Mystery stays higher than Random)."** Factually incorrect — Table 2 shows GPT-5 TMK: Random 99.0% > Mystery 98.3%. The ordering inverts. Removed.
- **Claim that three models showing three different patterns weakens the inversion evidence.** Factually incorrect — all three reasoning models show the inversion pattern. Removed.
- **Several generic or speculative criticisms** (e.g., "the paper would be stronger if TMK were tested on o1preview," "evaluation code modifications not quantified") — these are untethered to specific paper content or request non-standard analyses. Removed.
- **Criticism about "no code or prompt examples in the main paper"** — the parser strips appendices; these exist in the original submission. Removed per hard rule.
- **Criticism about missing related works** — removed per hard rule (cannot verify from external sources).
- **Formatting nitpicks and reproduction complaints about external evidence** — removed per hard rules.

## Novel Insights

The meta-reviewer notes that the critic's strongest claim (that only o1 shows performance inversion, weakening the steering hypothesis) is falsified by the paper's own Table 2 — all three reasoning models (o1, o1-mini, GPT-5) exhibit the inversion pattern where Random Blocksworld surpasses Mystery under TMK. This *strengthens* the empirical regularity, even as it does not resolve what causes it. The consistency of the inversion across models is a genuinely interesting finding that deserves more emphasis than the paper gives it, and more analysis than the critic acknowledged.

## Suggestions

1. Add CoT and a flat-structured (non-hierarchical) baseline to isolate what TMK's specific architecture contributes.
2. Soften the causal mechanistic claim throughout — frame the code-execution steering as a testable hypothesis, not a concluded finding. The striking empirical result stands on its own.
3. Include the one-shot plain-text numbers (currently in external repository) directly in the paper to resolve the confound concern.
4. Add ablations stripping TMK down to sub-components (e.g., pre/post conditions only, or hierarchical decomposition without teleology).
5. Test on at least one additional PlanBench domain (Logistics) to begin establishing generality.

## Score and Decision

This paper reports an empirical result that is genuinely striking on one condition (o1 × Random Blocksworld), uses rigorous full-plan validation, and uncovers a consistent performance-inversion pattern across multiple reasoning models. However, it lacks experimental comparison against existing prompting methods (CoT, ReACT), offers no ablation isolating TMK's active ingredients, and makes an unsupported mechanistic claim about code-execution steering. The paper presents an interesting phenomenon that merits follow-up, but in its current form the contribution is insufficiently supported relative to its broader claims.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>