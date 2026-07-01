Now let me read the remaining sections to get full context on the discussion and limitations:Now I have a comprehensive understanding of the paper. Let me draft my review.Now let me run Round 1 calibration — bracketing pass:Let me read the most relevant anchor papers to calibrate the score:Now I have enough calibration data. Let me form my initial bracket and finalize the review.

**Round 1 Bracket Analysis:**

- **Strong reject anchors (< 1.5):** Papers with fundamental issues (jailbreaking paper, survey paper, etc.) — the TMK paper is far better than these. It has real experiments with real results.

- **Reject band (1.5–3.5):** "Planning in Strawberry Fields" (3.0) — evaluated o1 on PlanBench with LRM-Modulo, criticized for limited novelty. "Exploring and Benchmarking Planning Capabilities" (2.0) — just packaging existing benchmarks. TMK paper is stronger than both: it introduces a novel prompting approach and has a striking empirical result (31.5% → 97.3%).

- **Borderline reject band (3.5–5.5):** "Do Think Tags Really Help LLMs Plan?" (4.0) — critical evaluation of ReAct with similar scope issues. "ChinaTravel" (5.0) — planning benchmark. TMK paper is comparable to the ReAct evaluation paper in rigor.

- **Borderline accept band (5.5–7.5):** "LLMs Can Plan Only If We Tell Them" (6.4) — has ablations, multiple domains, multiple models. TMK paper is clearly weaker: no ablations, single domain, single model family, overclaimed mechanism.

**Initial bracket: 3.5 – 5.0.** The TMK paper has a stronger empirical result than the 3.0 "Strawberry Fields" paper but much weaker experimental design than the 6.4 "AoT+" paper.

Now let me write the final review:

---

## Summary
This paper proposes prompting LLMs with domain knowledge structured using the TMK (Task-Method-Knowledge) framework—a cognitive science representation that hierarchically decomposes goals, methods, and domain ontology—and evaluates it on the PlanBench Blocksworld benchmark across five OpenAI models. The headline result is a dramatic improvement for the o1 model on Random Blocksworld (31.5% → 97.3%), accompanied by a "performance inversion" where o1 performs better on opaque tokens (Random) than misleading ones (Mystery) under TMK prompting. The authors hypothesize that TMK steers reasoning models from linguistic to symbolic/code-like processing modes.

## Strengths
- **Striking o1/Random result with formal verification.** The improvement from 31.5% to 97.3% on Random Blocksworld (Table 2) is large and unambiguous. Critically, this uses PlanBench's formal plan validation via classical planning tools (Section 2.2, referencing VAL and Fast Downward), ensuring that "close enough" plans do not inflate accuracy. This is the paper's strongest contribution.

- **Performance inversion is a genuinely interesting empirical observation.** Under TMK, o1 scores 97.3% on Random (opaque tokens) vs. 83.3% on Mystery (misleading tokens), reversing the plain-text pattern where Mystery (74.3%) > Random (31.5%) (Table 2, Section 4.2). This reversal is a concrete, falsifiable data point that merits further investigation regardless of the mechanistic interpretation.

- **Sound engagement with criticisms of prompting research.** The paper directly addresses Stechly et al. (2024) and Bhambri et al. (2025)'s criticisms about pattern matching and example similarity (Section 5.1). The experimental design avoids N-shot pattern matching concerns: the one-shot example is "random and not tailored to the problem at hand" (Section 3.2, point 3), and the entire plan trace must be correct.

## Weaknesses

### Fatal
None.

### Major
1. **No ablation separating TMK's structural/teleological properties from its information content.** The TMK prompt encodes explicit preconditions, effects, and process descriptions in a structured JSON format (Figure 1: e.g., `Requires: On(block, table), IsClear(block), HandEmpty()`, `Provides: Holding(block)`). This is essentially a PDDL-like domain specification rendered in JSON. The paper's central claim is that TMK's unique properties—hierarchical decomposition, teleological reasoning, the "why" of actions—drive the improvement (Sections 5.2.1–5.2.2). However, no experiment tests whether a flat JSON with the same preconditions/effects, structured plain text with equivalent information, or partial TMK without teleological links would achieve comparable results. Without this ablation, the paper cannot distinguish "TMK's cognitive architecture matters" from "giving the model formal action rules in any structured format helps." This is the paper's most critical gap because it undermines the interpretation of every result.

2. **"Symbolic steering" hypothesis overclaimed as validated.** The abstract states TMK "functions not merely as context, but also as a mechanism that steers reasoning models away from their default linguistic modes to engage formal, code-execution pathways." Section 5.2.1 calls the performance inversion "empirical validation of this steering effect," and the conclusion states "This confirms that TMK acts as a symbolic scaffold." However, a simpler alternative explanation exists: once explicit formal rules are provided, tasks with opaque tokens (Random) produce less interference than tasks with semantically misleading tokens (Mystery)—straightforward interference theory, not evidence of a "reasoning modality" shift. The paper itself acknowledges this should be "tested in models that have transparent reasoning tokens as part of future work" (Section 5.2.1), which directly contradicts the confidence expressed in the abstract and conclusion. The gap between hedged hypothesis in the body and confirmed finding in the abstract/conclusion is a substantive overclaim.

3. **No statistical analysis on single-run results.** All results in Table 2 are single-run accuracy numbers with no confidence intervals, variance estimates, or significance tests. LLM outputs are stochastic (acknowledged in Section 3.2 when discussing extraction artifacts). For smaller improvements—GPT-4 Classic: 34.6% → 39.7%; GPT-4o Random: 0.83% → 4.83%—these could plausibly be within noise. The Table 2 caption labels bold values as "significantly improved" without defining "significant" or performing any statistical test.

### Minor
1. **Modified extraction code may asymmetrically favor TMK results.** Section 3.2 describes modifications to PlanBench's extraction code for Random Blocksworld, noting the original code "required update... to be comparable with the ground truth." Since the plain-text baselines come from the PlanBench leaderboard (which likely uses the original extraction code), and TMK results use the modified code, there is a potential asymmetry specifically in Random Blocksworld—where the largest gains are claimed. The paper should explicitly confirm the extraction was applied symmetrically or that the leaderboard results were recomputed.

2. **Scope overclaim in the title.** "Knowledge Model Prompting Increases LLM Performance on Planning Tasks" implies generalizability across domains and model families, but the evidence covers only Blocksworld (one domain) with only OpenAI models. The paper acknowledges this in Section 5.3 but the title and abstract project broader scope.

3. **TMK differences across variants are not detailed.** Section 3.1.4 notes "there are also differences in TMK in classic blocksworld, mystery blocksworld, and random blocksworld" but defers to an external OSF link rather than describing them in the body. The reader cannot assess whether these differences introduce additional confounds.

### Trivial
None.

## Nice-to-Haves
- Testing with non-OpenAI model families (Claude, Gemini, Llama) to establish generalizability across architectures.
- A second planning domain (e.g., Logistics from PlanBench) would strengthen the "planning tasks" claim.
- Examining reasoning traces or surface-level outputs for evidence of code-like processing patterns, which would provide *some* evidence for the steering hypothesis.
- Comparing TMK against other structured knowledge representations (BDI, HTN) as the paper itself suggests as future work (Section 6).

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **Criticism about one-shot vs. zero-shot comparison fairness**: The paper provides three arguments (Section 3.2) that substantially address this concern: (1) the original PlanBench paper used one-shot while the leaderboard is zero-shot, (2) zero-shot outperforms one-shot for plain text, meaning the comparison against zero-shot is conservative, and (3) the one-shot example is random and not tailored. While a direct one-shot plain-text comparison would be ideal, the paper's defense is reasonable enough to move this out of the main weaknesses. Retained as a minor note under Minor #1 (extraction code) context.

- **Cognitive scaffolding discussion lacks experimental grounding (Section 5.2.2)**: The reviewer noted this as speculative. However, it is explicitly presented as a secondary hypothesis and discussion point, not as a validated claim. Removing as it is appropriately scoped as speculation.

## Novel Insights
The performance inversion phenomenon—where structured domain knowledge causes a reasoning model to perform *better* on fully opaque tokens than on semantically misleading ones—is a genuinely novel empirical observation. This challenges the default assumption that semantic overlap always helps and suggests that under the right conditions, prior semantic knowledge becomes interference rather than aid. While the mechanistic interpretation (steering toward "code-execution pathways") remains unvalidated, the raw empirical pattern is noteworthy and could motivate interesting follow-up work on the interaction between structured prompts, token semantics, and model inference strategies.

## Suggestions
1. **Run ablation experiments** to isolate TMK's structural contribution: (a) flat JSON with identical preconditions/effects, (b) structured plain text with the same information, (c) partial TMK without teleological links (removing the Mechanism field). This is the single highest-leverage improvement.
2. **Moderate claims in abstract/conclusion** to match the evidence—present the steering hypothesis as a hypothesis, not a confirmation. The body's appropriate hedging should be carried to the abstract.
3. **Report variance across multiple runs** (3–5 minimum) to establish robustness, particularly for smaller effects.
4. **Describe TMK variant differences in the body** rather than deferring entirely to an external link.
5. **Explicitly confirm extraction code symmetry** between TMK and baseline results for Random Blocksworld.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to TMK paper |
|-------|------|-----------|-------|------------------------|
| NEMESIS Jailbreaking | 5kMwiMnUip | 1.40 | R1 | Fundamentally weaker — no real experiments, no contribution |
| Advancing Cross-Lingual Capabilities | gwZ90hFSL2 | 1.00 | R1 | Not comparable — pseudoscientific claims |
| Systematic Review of LLMs | 8QTpYC4smR | 1.00 | R1 | Survey paper with no novelty; TMK paper much stronger |
| KL Divergence GFlowNets | Uj0h13lVrR | 1.00 | R1 | Not topically related |
| Exploring and Benchmarking Planning | koza5fePTs | 2.00 | R1 | Similar domain but weaker — no novel technique, packaging existing benchmarks; TMK paper has a novel approach and striking result |
| Structure-Rich Text Benchmark | ly10tMV6cD | 3.25 | R1 | Loosely related; TMK paper has a clearer contribution |
| Planning in Strawberry Fields (o1/PlanBench) | jOuHjFw71C | 3.00 | R1 | Very topically related — also evaluates o1 on PlanBench. Criticized for limited novelty (just evaluating new models). TMK paper is stronger: introduces a novel prompting technique with a striking empirical result |
| Harnessing Wikipedia Graph | Avg6hmtgHE | 3.40 | R1 | Different topic |
| Navigating the Labyrinth | DZBFchnM3b | 3.67 | R1 | Related (LLM reasoning benchmark); TMK paper has comparable experimental rigor |
| Do Think Tags Really Help LLMs Plan? | 85Ik12q2hP | 4.00 | R1 | Very relevant — critical evaluation of ReAct prompting, similar scope limitations. TMK paper has a stronger positive finding but comparable experimental rigor |
| ChinaTravel | 9dfRC2dq0R | 5.00 | R1 | Planning benchmark with more comprehensive evaluation; TMK paper has a more interesting finding but thinner evidence |
| Assessing Knowledge-intensive Reasoning | iSTMsye6SD | 5.25 | R1 | Different focus; more comprehensive evaluation design |
| ActionReasoningBench | NUD03NBDOE | 6.75 | R1 | More comprehensive benchmark (8 domains, 6 dimensions); TMK paper is narrower and less rigorous |
| LLMs Can Plan Only If We Tell Them | K3KrOsR6y9 | 6.40 | R1 | Very relevant — also prompting for Blocksworld planning. Significantly stronger: has ablations (AoT vs AoT+), tests multiple domains, multiple models. TMK paper lacks all of these |
| Robotouille | OhUoTMxFIH | 5.67 | R1 | Different planning focus |
| Factual Knowledge of LLMs | 9OevMUdods | 6.75 | R1 | Different topic |

**Round 1 bracket: 3.5 – 5.0.** The TMK paper is clearly above the 3.0 "Strawberry Fields" anchor (which was criticized for having no novel technique) but clearly below the 6.4 "AoT+" anchor (which had ablations, multiple domains, multiple models).

**Narrowing within the bracket:** The TMK paper's striking empirical result (31.5% → 97.3%) and the performance inversion observation lift it above the 4.0 "Do Think Tags Really Help?" anchor, which was a purely critical evaluation without a positive contribution. However, the TMK paper's lack of ablation, overclaimed mechanism, no statistical analysis, and single domain/model family prevent it from reaching the 5.0+ range where papers begin to demonstrate the rigor needed for acceptance. The paper presents a genuinely useful empirical finding that is undercut by interpretive overclaiming and insufficient controls.

**Final score: 4.0** — Borderline reject. The paper demonstrates an interesting empirical phenomenon (TMK-structured prompts dramatically improve o1 planning on obfuscated Blocksworld) but the gap between claims and evidence is too large for acceptance. The central thesis about TMK's unique structural properties being the active ingredient is untested by any ablation. The "symbolic steering" mechanism is presented as validated in the abstract/conclusion but remains an untested hypothesis. With ablation experiments, statistical analysis, and more appropriately scoped claims, this could become a compelling paper.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>