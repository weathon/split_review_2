Now I have enough calibration data. Let me synthesize the final review.

## Summary

This paper proposes using the Task-Method-Knowledge (TMK) framework — a knowledge representation formalism from cognitive science that captures teleological, hierarchical, and causal structure — as a prompting strategy to improve LLM performance on PlanBench Blocksworld planning tasks. Compared against plain-text baselines from the public PlanBench leaderboard, the authors report accuracy improvements across several OpenAI models, most strikingly on o1 Random Blocksworld (31.5% → 97.3%). The paper also observes a "performance inversion" under TMK prompting where o1 performs better on opaque symbolic tasks (Random) than on semantically meaningful ones (Mystery), which the authors interpret as evidence that TMK steers models toward symbolic/code-execution reasoning pathways.

## Strengths

- **Well-motivated, principled intervention.** The paper grounds its approach in the TMK framework from cognitive science and AI (Murdock & Goel, 2008), rather than ad-hoc prompt engineering. TMK's explicit representation of preconditions, effects, teleological "why," and hierarchical decomposition is a conceptually coherent match for planning tasks. This is a genuine departure from the CoT/ReACT paradigm.
- **Striking headline result.** The o1 Random Blocksworld improvement (31.5% → 97.3%) is large and practically meaningful. Even accounting for experimental design concerns, a delta of this magnitude is unlikely to disappear under tighter controls.
- **Engages honestly with prior criticisms.** The paper explicitly addresses the pattern-matching concern raised by Stechly et al. (2024) and Bhambri et al. (2025), uses whole-plan evaluation (not just final-state matching), and acknowledges that the one-shot example is generic/random. This awareness is a genuine improvement over many prompting papers.
- **Interesting empirical fingerprint.** The performance inversion (plain text: Mystery > Random; TMK: Random > Mystery for o1) is an intriguing pattern that, if robust, suggests the prompting method qualitatively changes how the model processes the task.

## Weaknesses

### Major

- **Asymmetrical central comparison.** The core empirical claim rests on comparing TMK (one-shot, with a structured JSON domain definition) against plain text (best of sampled zero-shot and one-shot). This conflates two variables: the structured TMK representation and the presence of a one-shot example. The paper's defense (Section 3.2) — that one-shot plain text is often worse than zero-shot — is supported only by sample testing in an external OSF link, not by in-paper data. Even if true, it does not address the core concern: the TMK condition differs from the baseline in both structure and example presence. The minimal control that would allow attribution to TMK specifically is **plain-text domain description + the same one-shot example**, which is absent from the main paper. The large o1 Random improvement is unlikely to vanish, but for smaller gains (e.g., GPT4 Classic: 34.6% → 39.7%), interpretability is compromised.

- **Custom extraction function not validated against VAL.** The paper introduces a custom extraction function (Section 3.2) that normalizes outputs by stripping symbols and handling word substitutions, but does not empirically verify that this function yields the same correctness judgments as the original PlanBench validator (VAL). Without running VAL on TMK outputs, scores could be inflated relative to the leaderboard baselines. The authors argue consistency with ICAPS conventions, but this should be validated, not argued.

### Minor

- **No ablation isolating TMK's specific features.** The paper claims TMK's teleological structure is uniquely beneficial (Section 2.3), but never tests whether simpler structured representations — a PDDL domain description, a non-TMK JSON encoding of pre/post conditions, or even a well-structured paragraph — produce similar gains. This limits what can be concluded about TMK specifically versus structured domain knowledge in general.

- **No variance or statistical reporting.** Results in Table 2 are point estimates with no indication of number of runs, standard deviations, or confidence intervals. While the o1 Random delta (65.8pp) is large enough to likely be robust, smaller improvements are uninterpretable without error information. Multiple trials are standard practice for stochastic LLM evaluations.

- **Overclaiming the "steering mechanism" interpretation.** The abstract frames TMK as "a mechanism that steers reasoning models away from their default linguistic modes to engage formal, code-execution pathways" — but the paper provides no evidence about internal model processing pathways, only output accuracy. The performance inversion is consistent with this hypothesis but does not uniquely support it; simpler explanations (better task decomposition, reduced ambiguity) also predict the pattern.

### Trivial

- None.

## Nice-to-Haves

- Compare TMK against alternative structured representations (PDDL, non-TMK JSON, CoT) to isolate whether TMK's specific structure drives gains.
- Validate TMK outputs with VAL and report agreement rates.
- Apply TMK to additional PlanBench domains (e.g., Logistics) to test generalizability beyond Blocksworld.

## Removed Points

* "No analysis of model internals, attention patterns, or reasoning traces" — scope creep; the paper never claims to provide mechanistic interpretability.
* "Code/data should be accessible to reviewers" — OSF links for double-blind submissions are standard practice.
* "Missing related works" — cannot be verified from available information.
* Generic speculation about confounders without concrete evidence — removed per filtering rules.

## Novel Insights

The key insight from the harsh critic is that the paper's central experimental comparison is structurally asymmetrical: TMK (one-shot, with structured domain definition) vs. plain text (best of zero-shot and one-shot, without structured domain definition). This is not a minor nitpick — it is a design gap that prevents clean attribution of the reported gains to TMK structure specifically. The critic's proposed minimal control (plain-text + same one-shot example as TMK) is precise and actionable. Beyond this, the remaining observations (extraction validation, ablation needs, variance reporting) are standard methodological concerns consistent with the paper's own framing.

## Suggestions

1. **Highest priority:** Add a plain-text + one-shot example baseline (same generic example, same models, same extraction) to Table 2. This is the minimal experimental control needed to support the claim that TMK structure — rather than the mere presence of a domain definition plus an example — drives improvements.
2. Validate TMK outputs with VAL and report the agreement rate between the custom extraction and VAL.
3. Report number of runs and variance (standard deviation or confidence intervals) for at least the key results.
4. Include an ablation comparing TMK against a PDDL or non-TMK structured JSON to test whether TMK's specific features matter.

## Score and Decision

**Initial bracket (Round 1):** The paper sits between the 3–4 range papers (pure evaluation, limited novelty) and the 5.25–6.40 range papers (accepted method papers). The strongest anchor is "LLMs Can Plan Only If We Tell Them" (6.40, Accept) — a paper with a similar profile (prompting method + planning benchmarks) but stronger experimental controls and more comprehensive evaluation. The weakest relevant anchor is "Exploring and Benchmarking Planning Capabilities" (2.00, Reject), which was rejected for lacking novelty. Our paper's negatives are less severe than that paper, and its positives (novel method, striking o1 result) are stronger.

**Final calibration:** Our draft's weighted positives (+5.36 for the o1 result, +3.73 for engaging with criticisms, +3.69 for motivation) are comparable to the 6.40 anchor's positives (+5.63, +5.06, +4.30) but lower in magnitude. Our weighted negatives (-3.61, -3.47, -3.44, -3.32, -2.50) are less severe than the 6.40 anchor's worst negatives (-5.86, -5.13) but more numerous. Compared to the 5.25 anchor (Tree-Planner, Accept), our negatives are shallower (-3.61 vs. -10.14) and our positives are somewhat weaker (+5.36 vs. +6.54). Compared to the 4.00 anchor (ReAct critique, Reject), our paper is stronger because it proposes a method rather than only critiquing one. The paper has real contributions and a striking result, but the experimental design gap (asymmetrical comparison) prevents clean attribution of the core claim.

**Score: 5.0** — This reflects a paper with genuine conceptual novelty and a striking result that needs tighter experimental controls to fully support its claims. The core idea is worth preserving, but the evidence as presented does not cleanly separate the effect of TMK structure from the effect of having a structured domain definition plus a one-shot example.

**Decision: Borderline Reject** — The paper should not be accepted in its current form without the minimal experimental control (plain-text + same one-shot) being added and the extraction function being validated. With these additions, the paper could make a solid case.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>