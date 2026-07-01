Now I have sufficient calibration data. Let me finalize the review with a calibrated score.

## Calibration Summary

**Round 1 — Bracketing:**

My initial bracket is score 3.5–5.5 (borderline reject to borderline accept). The paper introduces a novel prompting method (TMK) adapted from cognitive science and shows striking results on Random Blocksworld (o1: 31.5% → 97.3%). However, evaluation is limited to one domain and one model family, no variance estimates are reported, and the paper makes strong mechanistic claims without evidence.

**Calibration anchors examined:**

| Anchor | Avg Score | Comparison |
|--------|-----------|------------|
| "Planning in Strawberry Fields" (jOuHjFw71C) | 3.00 | Evaluates o1 on PlanBench but introduces no new method. Our paper has more novelty (TMK framework) but similar evaluation breadth. |
| "Exploring and Benchmarking Planning Capabilities" (koza5fePTs) | 2.00 | Broad benchmark with limited novelty. Our paper is more novel. |
| "Do Think Tags Really Help LLMs Plan?" (85Ik12q2hP) | 4.00 | Critical evaluation of ReAct; no new method proposed. Similar quality but our paper has a constructive contribution (TMK method). |
| "Guiding Language Models Reasoning with Planning Tokens" (UJkgGbLfWA) | 5.00 | Novel method (planning tokens), multiple datasets & models, but rejected for limited baselines and narrow scope. Our paper has weaker evaluation scope but a more striking result. |
| "Improving Planning with LLMs: A Modular Agentic Architecture" (iNcEChuYXD) | 4.50 | Novel agentic architecture but rejected — evaluation scope issues. Similar quality tier to our paper. |
| "Tree-Planner" (Glcsog6zOe) | 5.25 | New method, multiple domains, accepted. Our paper has weaker evaluation breadth. |
| "LLMs Can Plan Only If We Tell Them" (K3KrOsR6y9) | 6.40 | New prompting method (AoT+), Blocksworld+Logistics, multiple model families, accepted with SOTA results. Our paper's evaluation is narrower. |
| "Take a Step Back" (3bq3jsvcQ1) | 8.00 | Strong prompting paper with multi-domain evaluation. Our paper is substantially weaker. |

**Narrowed score:** 4.0. This paper introduces a novel method and has striking results, placing it above papers scoring 2.0–3.0 (which lack methodological novelty). However, the limited evaluation scope (single domain, one model family), missing variance estimates, and disconnect between mechanistic claims and evidence prevent it from reaching the 5.25–6.40 tier of accepted papers with comprehensive evaluation.

---

## Summary

This paper introduces Task-Method-Knowledge (TMK) prompting, a structured knowledge representation framework borrowed from cognitive science, for improving LLM performance on planning tasks. The authors evaluate TMK on the PlanBench Blocksworld benchmark (Classic, Mystery, Random variants) using OpenAI models (GPT-4, GPT-4o, o1-mini, o1, GPT-5) and compare against plain-text baselines from the PlanBench leaderboard. The most striking result is o1 going from 31.5% to 97.3% on Random Blocksworld with TMK prompting, including a performance inversion where opaque symbolic tasks become easier than semantically meaningful ones.

## Strengths

1. **A striking empirical finding on the hardest variant.** The o1 model's jump from 31.5% to 97.3% on Random Blocksworld (Table 2) is a notable result — a transformation from near-failure to near-perfection on a task designed to strip away semantic priors. This finding is genuinely attention-worthy.

2. **The performance inversion is a novel diagnostic observation.** The pattern that plain-text o1 performs better on Mystery (74.3%) than Random (31.5%), but TMK flips this (Random 97.3% vs Mystery 83.3%), provides evidence that TMK changes *how* the model approaches the task, not just what facts it receives. This is the paper's most compelling piece of evidence.

3. **Principled engagement with prior prompting criticisms.** Section 2.1 seriously engages with known limitations of CoT, CoS, and ReACT — specifically the concern that reported gains may come from instance-specific N-shot pattern matching rather than genuine reasoning. The paper uses a non-matching one-shot example and requires full plan verification, addressing these criticisms.

## Weaknesses

### Fatal
None.

### Major

1. **Mechanistic claims outrun the evidence.** The paper presents a strong mechanistic interpretation — that TMK "steers reasoning models away from their default linguistic modes to engage formal, code-execution pathways" (abstract) and "confirms that TMK acts as a symbolic scaffold" (conclusion) — without any experiment that tests this mechanism. No analysis of model internals, no probing of attention patterns, no comparison of token distributions, no ablation that varies syntactic form while holding semantic content constant. The performance inversion is *consistent with* the code-execution hypothesis, but it is also consistent with simpler alternatives (e.g., better-organized task decomposition, explicit pre/post-condition specifications reducing search space). The paper simultaneously admits "the cause of that increase is left to future work" (line 304), which contradicts the confident framing in the abstract and conclusion. This overclaiming undermines the paper's credibility.

2. **No variance estimates or replication information.** Every accuracy in Table 2 is reported as a single number with no confidence intervals, standard deviations, or indication of how many runs were performed. LLM outputs are stochastic — a single run per condition is unreliable, especially for models where temperature settings are not reported. The precision of "97.33%" and "16.83%" is misleading without variance estimates. Without this information, the reader cannot distinguish meaningful improvements from sampling noise, particularly for smaller gains (e.g., GPT4 Classic: 34.6% → 39.7% with no variance estimate).

### Minor

1. **Comparison confound: TMK one-shot vs. plain text zero-shot.** The paper compares TMK (one-shot) against plain text (best of sampled zero-shot and one-shot, where zero-shot is the stronger baseline). While the paper argues this comparison is conservative (Section 3.2), the absence of a TMK zero-shot condition means improvement could partly reflect format scaffolding from the one-shot example rather than TMK content per se. The paper partially addresses this (arguing zero-shot plain text is a stronger baseline, and the one-shot example is random), but a TMK zero-shot condition would be needed for a fully controlled attribution.

2. **Enhanced extraction function not fully specified.** The paper mentions an "enhanced extraction function" (lines 187–191) that handles stochastic variations in model outputs (symbols, word choices). The description is insufficient for a reader to assess whether this could inflate scores by accepting plans that are not strictly correct, or to reproduce the evaluation.

3. **Single domain, single model family.** The experiments cover only Blocksworld (one of several PlanBench domains) and only OpenAI models. The paper acknowledges this limitation (Section 5.3), but the contribution's generality is untested — the most striking result (performance inversion) has only been observed in one model (o1), and GPT-5 starts at 92.5% on Random, leaving little room for TMK to show its distinctive effect.

4. **Decoding parameters not reported.** Temperature, top-p, max tokens, and other sampling parameters are not provided, limiting reproducibility.

### Trivial
- Table 2 uses bold for "significant improvements" but does not explain how significance is determined (no statistical tests reported).

## Nice-to-Haves
- Running TMK in zero-shot as a control would strengthen attribution of gains to TMK content versus format scaffolding.
- Providing an ablation that gives the same domain information in plain prose would disentangle TMK structure from information quantity.
- Reporting accuracy over multiple runs (3–5) with variance estimates would help distinguish signal from noise.
- The o1-mini degradation on Mystery (19.1% → 16.83%) is a notable exception that the main story does not fully explain; investigating this could strengthen the analysis.

## Removed Points
- **"The one-shot/zero-shot comparison is uncontrolled (structural/fatal)"** — Downgraded to Minor. The paper provides a reasoned defense (Section 3.2) that zero-shot plain text is a stronger baseline than one-shot plain text, making the comparison conservative. The weakness is retained (as Minor) but not at the structural level the harsh critic suggested.
- **"Section 2.1 claim about the leaderboard is not quite right"** — This is a minor interpretive point that does not affect the paper's core contribution.
- **"Section 5.2.2 cognitive scaffolding does not contribute evidence"** — The paper frames this section as hypothesis/speculation in the Discussion, not as experimental evidence.
- **"o1preview has no TMK column"** — The paper already notes with an asterisk that these results are from the leaderboard ("o1Preview has been deprecated and replaced by o1. Results extracted from Valmeekam (2023)").

## Novel Insights
The most interesting observation from the review process is the tension between the paper's two strongest assets: the performance inversion pattern (Mystery vs. Random difficulty reversal under TMK) is genuinely suggestive of a modality shift in the model's reasoning approach, yet the paper lacks the experimental design to pin down what causes this shift. This is precisely the kind of finding that could motivate substantial follow-up work, but the current paper would be stronger if it treated the mechanism as speculation and focused on the empirical discovery.

## Suggestions
1. Add a zero-shot TMK condition and a one-shot plain-text condition (with a random example) to fully control the comparison and isolate the effect of TMK structure.
2. Report accuracy over at least 3–5 runs with standard deviations or confidence intervals.
3. Tone down the mechanistic claims ("code-execution pathway steering") to match the evidence. Frame the code-execution hypothesis as speculation for future work, consistent with the line 304 admission that "the cause of that increase is left to future work."
4. Report decoding parameters (temperature, top-p, max tokens).
5. Provide a more detailed description of the enhanced extraction function, ideally with concrete examples of what it normalizes.
6. Add results from at least one additional PlanBench domain (e.g., Logistics) and/or one open-source model to demonstrate generality.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>