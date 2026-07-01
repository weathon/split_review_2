Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper tests whether the Task-Method-Knowledge (TMK) framework—a structured knowledge representation format from cognitive science—can improve LLM performance on planning tasks. On PlanBench Blocksworld, TMK-structured prompts yield substantial gains, most strikingly for o1 on Random Blocksworld (31.5% → 97.3%). The paper also observes a "performance inversion" where o1 performs better on opaque symbolic tasks than on semantically-loaded ones under TMK.

## Strengths

- **The o1 Random Blocksworld result is genuinely striking and warrants attention.** The jump from 31.5% to 97.3% on the hardest variant (random, opaque tokens) using only a prompt change is a practically meaningful improvement (Table 2, lines 249-251). If validated through controlled comparisons, this would be a noteworthy finding.

- **The performance inversion observation is the most interesting finding in the paper.** The fact that TMK causes o1 to perform better on Random (97.33%) than Mystery (83.3%)—reversing the typical relationship where Mystery outperforms Random—is non-obvious and provides concrete evidence that TMK is doing something qualitatively different from simply adding more context (Section 4.2, lines 205-209).

- **The paper acknowledges key limitations**, noting it only tests Blocksworld and calls for broader evaluation, and leaves the cause of improvement to future work (Section 5.3, line 294; Section 6, line 304).

## Weaknesses

### Major

1. **Uncontrolled comparison prevents attributing improvements specifically to TMK.** The TMK condition differs from the baseline along multiple uncontrolled dimensions simultaneously:

   - **Zero-shot vs. one-shot (lines 177-181):** The TMK results use one-shot prompts while the leaderboard baselines are zero-shot. The authors argue this is inconsequential based on general trends observed elsewhere, but do not demonstrate it for the specific models and TMK format tested here. A one-shot example provides format scaffolding—showing the model how to structure its output—that could inflate scores independent of TMK's domain knowledge.

   - **Format confound:** The TMK prompt uses JSON with explicit hierarchical structure, while the baseline uses plain text. The paper's own hypothesis about "code-execution pathways" (Section 5.2.1) implies the JSON format itself may trigger different internal processing modes, making it impossible to tell whether observed gains come from the TMK structure specifically or from any structured, code-like format.

   - **Structural knowledge confound:** The TMK prompt contains the Blocksworld domain model in an explicit decomposed form (preconditions, effects, descriptions, inputs, outputs; Figure 1). A controlled comparison using the same domain knowledge in a flat, non-TMK structured format (e.g., clean PDDL text or plain JSON without the TMK hierarchy) is needed to isolate whether the specific TMK hierarchy matters or simply having well-structured domain knowledge suffices.

   Without a controlled baseline that holds shot-count, format-type, and knowledge-content fixed, the paper cannot attribute the observed improvements specifically to the TMK framework.

2. **The enhanced extraction function may inflate TMK scores relative to baseline.** The paper describes a modified extraction function (lines 189-191) that is more lenient—accepting symbols, words like "object" instead of block names, and extra words in plan steps. The baseline scores from the public leaderboard were computed with different extraction criteria. The paper acknowledges the extraction was changed and argues it is consistent with ICAPS practices (line 191), but does not quantify the effect of this change on comparability. The striking o1 Random improvement could be partially affected by this asymmetry.

3. **The central mechanism claim (code-steering) is presented as a finding but is not tested.** The abstract presents "steering reasoning models away from their default linguistic modes to engage formal, code-execution pathways" (lines 9-10) as a finding. The introduction frames it similarly (lines 22-23). However, the evidence is entirely correlational—TMK improves performance and performance inversions are observed. No analysis of hidden states, attention patterns, or reasoning traces is provided. Section 5.2.1 is explicitly speculative ("It is feasible that…", "We theorize…", "It is reasonable to deduce…"). The performance inversion is consistent with the code-steering hypothesis, but also with several other explanations (e.g., Mystery's semantically-loaded words conflict with TMK's structure creating interference absent in Random). The paper would be stronger if it clearly labeled this as an untested hypothesis rather than an empirical finding.

4. **Results lack statistical precision.** Accuracy is reported as point estimates with no standard errors, confidence intervals, or statistical tests (Table 2). The dataset size (number of problems per variant) is not stated anywhere in the paper. Small improvements—e.g., GPT4 Mystery 0% → 3.8%, GPT4o Random 0.83% → 4.83%—could easily be within the noise of a few random successes. The paper calls improvements "significant" (Table 2 caption) without any statistical basis.

### Minor

1. **The performance inversion has plausible alternative explanations that are not explored.** The inversion (Section 4.2, lines 205-209) could arise from (a) the Mystery domain's semantically-loaded words ("Attack", "Feast") conflicting with TMK's structured descriptions, creating interference that the Random domain's opaque tokens do not; (b) the one-shot example providing a format template that is easier to follow with arbitrary tokens; or (c) the JSON structure reducing ambiguity in Random while Mystery's misleading semantics still leak through despite the structure. The paper adopts the code-steering explanation without ruling out these alternatives.

2. **The o1-mini degradation on Mystery (19.1% → 16.83%) and limited improvement on Classic (56.7% → 57%) are mentioned but not deeply analyzed.** Given that these negative/flat results contrast with the paper's emphasis on TMK's benefits, they deserve more investigation than the brief "semantic overload" or "capacity limitations" hypothesis (Section 4.2, line 211; Section 6, line 302).

### Trivial

None.

## Nice-to-Haves

- Run the plain-text baseline under identical one-shot conditions with the same extraction function to enable a controlled comparison.
- Add a structural ablation: reformat the same domain knowledge as flat structured specification (e.g., PDDL text or plain JSON without TMK hierarchy) to test whether the TMK hierarchy specifically matters.
- Add an ablation of the one-shot example (zero-shot TMK) to isolate the contribution of the example vs. the structure.
- Report cost or inference time, since TMK prompts are substantially longer.
- Report N, standard errors, or confidence intervals.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"The TMK prompt contains more complete domain knowledge than the baseline"** – The paper states it "replaces the domain portion of the PlanBench prompt" (line 169), implying both conditions encode domain knowledge but in different formats. The critic's assertion of greater completeness is speculative.
- **"Plain-text baseline 'presumably' contains less structured description"** – Speculative, as the paper does not provide the baseline prompt verbatim but states it replaces the same domain portion.
- **"The worked example effect analogy is strained"** – This is an editorial opinion about Section 5.2.2 rather than a verifiable weakness of the paper's claims or results.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Run the plain-text baseline under identical conditions (same models, one-shot, same extraction function) as the TMK condition. This single change would address the most damaging confound.
2. Add a structural control: reformat the same domain knowledge as a flat structured specification (e.g., clean PDDL text, or a plain JSON listing of actions/conditions without TMK hierarchy). If TMK outperforms this, the hierarchy matters; if not, the improvement is just "structured knowledge helps."
3. Report N, standard errors, or confidence intervals for all accuracy figures.
4. Explicitly confirm whether the extraction criteria for TMK outputs and baseline outputs are identical; if they differ, quantify the effect of the difference.
5. Clearly separate the mechanism hypothesis (code-steering) from the empirical results throughout the paper, including the abstract.

## Score and Decision

**Bracket (Round 1):** After calibration against anchor papers, the plausible range is 3.5–5.5. The paper is stronger than pure evaluation papers (e.g., "Planning in Strawberry Fields" at 3.0) because it proposes a novel framework and has striking empirical observations. It is weaker than papers with careful controlled experiments (e.g., "LLMs Can Plan Only If We Tell Them" at 6.4) because of uncontrolled confounds in the comparison.

**Calibration anchors consulted:**
- "Exploring and Benchmarking Planning Capabilities of LLMs" (2.00) – pure benchmark + evaluation, less novel than this paper.
- "Planning in Strawberry Fields" (3.00) – evaluation-only paper on similar models/benchmarks, less novel content.
- "Do Think Tags Really Help LLMs Plan?" (4.00) – critical analysis of prompting, stronger controlled evaluation but less positive findings.
- "Tree-Planner" (5.25) – proposed method with evaluation on single environment, similar scope but stronger baselines.
- "A Prefrontal Cortex-inspired Architecture for Planning in LLMs" (5.25) – cognitive-science-inspired method, similar single-domain limitation and baseline concerns.
- "LLMs Can Plan Only If We Tell Them" (6.40) – stronger evaluation with ablations and controlled comparisons across multiple benchmarks.

**Final determination:** The paper has a genuinely interesting core finding and a novel framework, but the experimental design does not permit clean attribution of improvements to TMK specifically. The mechanism claims outrun the evidence. The contribution is promising but not yet established. A careful revision addressing the confounds and toning down claims could lift this significantly.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>