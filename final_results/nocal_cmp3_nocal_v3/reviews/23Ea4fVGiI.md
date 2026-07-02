Now I have all the information needed to produce the consolidated review.

## Summary

This paper evaluates whether prompting with the Task-Method-Knowledge (TMK) framework — a structured knowledge representation from cognitive science that decomposes procedural knowledge into Tasks, Methods, and Knowledge — improves LLM performance on planning tasks. Evaluated on PlanBench's Blocksworld domain (Classic, Mystery, and Random variants), the paper reports that TMK-structured prompts increase planning accuracy across multiple models, with the headline result being o1's Random Blocksworld accuracy rising from 31.5% to 97.3%. The paper also documents a performance inversion: under TMK, o1 performs better on the opaque Random domain than on the semantically misleading Mystery domain, which the authors interpret as evidence that TMK shifts models from linguistic approximation toward code-execution reasoning pathways.

## Strengths

1. **The o1 Random Blocksworld result is empirically striking.** A jump from 31.5% to 97.3% (Table 2) on a standard planning benchmark is a large effect that goes well beyond typical incremental improvements reported in the prompting literature. This finding is the paper's strongest contribution.

2. **The performance inversion pattern (Random > Mystery under TMK for o1) is genuinely interesting and non-obvious.** The paper correctly notes that if TMK simply added useful context, one would expect uniform gains across domains; the inversion suggests something more specific is occurring, whether or not one accepts the paper's mechanistic interpretation.

3. **The paper engages honestly with prior criticisms of prompting-based planning work** (Stechly et al., 2024; Bhambri et al., 2025). The evaluation design — one-shot with a non-matching example, full plan verification, comparison against the better of zero-shot and one-shot — shows awareness of the pattern-matching critique that has undercut earlier claims of planning ability.

4. **The single-domain scope is acknowledged as a limitation** (Section 5.3). The paper does not claim cross-domain generalizability beyond Blocksworld.

## Weaknesses

### Fatal
None. The core empirical finding (TMK improves planning accuracy, especially for o1 Random) is likely real and survives scrutiny even if the attribution and mechanistic interpretation are contested.

### Major

1. **The comparison between TMK and plain text is confounded on multiple dimensions simultaneously, making it impossible to attribute improvements to the TMK framework specifically.**

   The TMK prompt (Section 3.1, Fig. 1) differs from the plain-text PlanBench baseline in at least three ways at once: (a) *information content* — the TMK prompt includes explicit preconditions ("Given: On(block, table), IsClear(block), HandEmpty()"), post-conditions, parameter specifications, and causal links between goals and methods, which the standard PlanBench plain-text prompt does not include; (b) *format* — TMK uses JSON with nested hierarchy, while the baseline is plain English prose; (c) *shot count* — TMK is one-shot while the baseline is zero-shot for the published leaderboard results and one-shot for the authors' own runs, though the paper argues the one-shot example is random and zero-shot outperforms one-shot for plain text.

   The paper addresses point (c) in some detail (Section 3.2), but points (a) and (b) are not controlled for. A necessary control — a prompt containing the same action descriptions (same preconditions, same effects, same parameters) organized as flat JSON, detailed plain English, or any non-TMK structure — is absent. Without this, any improvement could come from the *additional domain knowledge* in the prompt or its *structured format* rather than from the TMK framework's specific teleological decomposition.

2. **The central mechanistic claim — that TMK acts as a "symbolic steering mechanism" shifting models from "linguistic approximation" to "formal code-execution pathways" — is not supported by the evidence presented.**

   The Abstract states that TMK "steers reasoning models away from their default linguistic modes to engage formal, code-execution pathways" as a finding. The experimental evidence, however, consists entirely of accuracy numbers (Table 2) and the performance inversion pattern. These are consistent with the steering hypothesis but are also consistent with simpler alternatives that the paper does not rule out: (a) the TMK prompt provides more useful domain knowledge (explicit preconditions and effects) that helps planning regardless of modality shifts; (b) the JSON structure improves output format compliance, reducing formatting errors the paper itself notes are common (lines 189–191); (c) the one-shot example demonstrates the required output format. The paper's discussion (Section 5.2.1) qualifies these claims with phrases like "it is feasible" and "we hypothesize," but the Abstract and introduction present the mechanism as an established finding. As the Conclusion itself concedes, "the cause of that increase is left to future work" (line 304).

3. **No direct comparison with alternative prompting methods (CoT, ReACT, CoS) on the same experimental setup.**

   Section 2.1 critiques Chain-of-Thought, ReACT, and Chain-of-Symbols at length for their limitations in planning, but the paper never benchmarks TMK against any of these methods under controlled conditions. The "SoTA" claim (Section 2, line 33) refers to the PlanBench public leaderboard, not to a direct comparison with other prompting techniques on matched models and data. Without such a comparison, the paper cannot support claims that TMK outperforms prior prompting approaches for planning.

4. **The extraction function modification for Random Blocksworld creates an asymmetric evaluation for GPT-4 and GPT-4o.**

   The paper modified the PlanBench extraction function for Random Blocksworld to handle stochastic formatting artifacts (lines 183–191). This modified extraction was used for TMK results and for the authors' own plain-text runs on newer models (o1, o1-mini, GPT-5). However, the plain-text baselines for GPT-4 and GPT-4o are taken from the public leaderboard (Table 2 footnote: "Results extracted from Valmeekam (2023)"), which presumably used the original, stricter extraction. This means the small improvements for GPT-4 Random (0% → 4.17%) and GPT-4o Random (0.83% → 4.83%) could be partially or entirely artifacts of the more lenient extraction. (The large o1 Random improvement, 31.5% → 97.3%, is not affected because both plain-text and TMK runs for o1 were conducted by the authors using the same extraction.)

### Minor

1. **No measures of variance or statistical significance are reported.** Table 2 shows single accuracy numbers without confidence intervals, standard deviations, or multiple trials. For the headline o1 Random result (31.5% → 97.3%), the effect size is large enough that this is not a fatal concern. But for smaller improvements (GPT-4 Classic: 34.6% → 39.7%; GPT-5 Classic: 99.3% → 99.7%; GPT-5 Mystery: 98.1% → 98.3%), single-point estimates without variance cannot be interpreted as meaningful.

2. **The cognitive scaffolding discussion (Section 5.2.2) is interesting background but has no connection to the experimental results.** The paper discusses Bloom's taxonomy, the worked example effect, and the claim that "TMK prompting may encourage LLMs to produce more procedural reasoning explanations," but it only measures plan *correctness*, not the procedural quality of explanations. This section is speculative framing, not an evidence-supported finding.

3. **The o1-mini degradation in Mystery (19.1% → 16.83%) is noted but not explored.** The paper attributes this to "semantic overload" or "capacity limitations" without any supporting analysis (e.g., of whether the model generates invalid plans or fails to follow the TMK structure). This is a missed opportunity to better understand the boundary conditions of TMK's effectiveness.

### Trivial
None.

## Nice-to-Haves

- **Ablation controlling for information content:** A "flat JSON" condition containing the same action descriptions (preconditions, effects, parameters) as the TMK prompt but without the Task/Method/Knowledge hierarchical decomposition, and a "detailed plain text" condition with the same information in English prose, would allow attribution of gains to the TMK framework specifically rather than to the presence of more detailed action knowledge or to structured format in general.
- **Direct comparison with Chain-of-Thought** on the same models and Blocksworld setup would support the paper's critiques in Section 2.1 and strengthen the "surpassing SoTA" claim.
- **Multiple trials with variance reporting** for conditions with smaller effect sizes (GPT-4 Classic, GPT-5 Classic/Mystery) would clarify whether those improvements are meaningful.
- **Analysis of o1-mini's outputs under TMK for Mystery vs. Random** could shed light on why this model shows degradation in Mystery while improving in Random.

## Removed Points

- The critic's claim in Issue 1(c) that the one-shot example confounds the comparison is partially addressed by the paper's argument (Section 3.2, points 2–3) that zero-shot outperforms one-shot for plain text and that the example is random and not tailored. The paper's argument here is reasonable even if not fully dispositive. This sub-point is subsumed under the broader information-content and format confounds.
- The critic's "worked example hypothesis" sub-point in Issue 2 restates the one-shot concern and is similarly addressed by the paper's Section 3.2 defense. Removed as redundant.
- General concerns about "the paper would be strengthened by reframing" are speculative framing suggestions, not weaknesses. Moved to Nice-to-Haves implicitly.
- The comment that "Section 5.3 (Limitations) does not discuss the extraction function modification, the lack of ablations..." is valid as a minor omission but is covered by other weaknesses; it has been absorbed into Major Issue 4 and Nice-to-Haves rather than listed separately.

## Novel Insights

The key insight that emerges from the reviews — beyond the paper's own contributions — is a precise framing of the empirical finding's value and limits. The o1 Random improvement and the performance inversion are genuinely interesting and likely robust observations. However, they currently function as existence proofs (TMK-structured prompts produce large accuracy gains in this specific setting) rather than as evidence for any particular mechanism. The most productive path forward would be to frame the paper as an empirical discovery ("TMK prompts produce large and surprising accuracy patterns on Blocksworld") and reserve mechanism claims for follow-up work with proper ablations. The inversion pattern itself — Random suddenly becoming easier than Mystery — is the paper's most valuable observation and deserves focused follow-up even if the mechanistic interpretation proves wrong.

## Suggestions

1. **Run a "flat JSON" ablation** that provides the same action descriptions (preconditions, effects, parameters) as the TMK prompt but without the Task/Method/Knowledge hierarchy. If TMK outperforms flat JSON, the case for the TMK framework's specific structure is strengthened substantially.
2. **Tone down the Abstract's mechanistic claims.** Replace "steers reasoning models away from their default linguistic modes to engage formal, code-execution pathways" with a description of the empirical findings and note that the mechanism is a hypothesis for future investigation.
3. **Benchmark at least one alternative prompting method** (e.g., Chain-of-Thought) on the same Blocksworld setup, or explicitly state that the paper's contribution is the empirical finding and not a claim of superiority over other prompting techniques.
4. **Clarify in the paper which conditions used the modified extraction function** and whether any historical baselines were affected, to eliminate the asymmetric extraction concern.
5. **Report multiple trials** (at least 3) with standard deviations, or note that single runs are the norm in PlanBench literature and flag the small improvements as not interpretable.

## Score and Decision

This paper has a genuinely interesting empirical finding — TMK-structured prompts produce a dramatic accuracy improvement for o1 on Random Blocksworld (31.5% → 97.3%) and a surprising performance inversion — and the paper engages honestly with prior criticisms. However, the evaluation has significant confounds that prevent attribution of the improvement to the TMK framework specifically: the TMK prompt differs from the plain-text baseline in information content and format simultaneously, no ablation controls for this, the mechanistic claims in the Abstract are unsupported by the evidence, and no comparison with alternative prompting methods is provided. The paper would need substantial revision (ablation controls, toned-down claims, comparison with other prompting methods) to meet the standards for acceptance. The core empirical observation is worth pursuing, but the current presentation oversells what the evidence supports.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>