## Summary

The paper proposes using the Task-Method-Knowledge (TMK) framework, originally from cognitive science, as a structured prompting strategy to improve LLM performance on planning tasks. On PlanBench Blocksworld variants, replacing the standard domain description with a TMK-structured JSON prompt yields accuracy improvements across several OpenAI models, most notably raising o1 on Random Blocksworld from 31.5% to 97.3%. The authors argue that TMK acts as a symbolic steering mechanism that shifts models from linguistic approximation to formal, code-like reasoning.

## Strengths

- Novel interdisciplinary application: importing a knowledge representation framework from cognitive science and education into LLM prompting for planning is a creative and underexplored direction.
- The experimental setup uses the well-established PlanBench benchmark, which provides formal validation of plan correctness, addressing criticisms of earlier prompting work.
- The performance gains are substantial and clearly documented, particularly the o1 improvement on Random Blocksworld, which suggests a genuine effect worth investigating.
- The discussion of potential mechanisms (code-execution steering, cognitive scaffolding) offers testable hypotheses and connects to recent work on textual vs. code-based reasoning.

## Weaknesses

### Fatal
- **The contribution cannot be attributed to TMK specifically.** The baseline is a plain-text domain description, while the treatment is a JSON-formatted TMK structure. The comparison does not control for structure format: any well-structured, symbolic domain description (e.g., PDDL, a simple JSON of actions/predicates) might yield similar gains. Without ablations (TMK vs. non-TMK JSON, TMK vs. other hierarchical frameworks as prompts, TMK vs. a flat list of actions in JSON), the claimed mechanism is unsubstantiated. The core conclusion that TMK *as a framework* drives improvement is not supported.

### Major
- **No statistical rigor.** Accuracy values are reported as single numbers with no confidence intervals, standard errors, or multiple runs. Given the stochastic nature of LLMs, the reliability of these results is unclear.
- **Modified evaluation procedure.** The authors changed the extraction criteria (handling symbols, words, word order) compared to the official PlanBench evaluation. The impact on comparability with the leaderboard and the potential for false positives is not validated. The paper says the changes "prevent these from getting evaluated as incorrect," but this could also accept formally incorrect plans that happen to match after extraction.
- **Overclaimed "performance inversion."** The claim that TMK inverts the difficulty order (Random easier than Mystery) is based on a single model (o1) for a single variant. GPT-5 does not show inversion (Mystery 98.3 vs. Random 99.0), and o1-mini shows degradation on Mystery. The evidence does not support a general phenomenon.

### Minor
- **Single model family.** Only OpenAI models are tested; generalizability to other LLM families (e.g., Llama, Claude, Gemini) is unknown.
- **No comparison to other prompting techniques.** The paper only compares TMK to plain text, not to Chain-of-Thought, ReACT, or other structured prompting methods. The value relative to existing approaches is unclear.
- **Speculative mechanism.** The claim that TMK shifts reasoning to "code-execution pathways" is interesting but unsupported by any analysis of model internals, attention patterns, or reasoning traces. The discussion is plausible but not empirically backed.

### Trivial
- Some redundancy in the discussion sections could be trimmed.

## Nice-to-Haves

- Perform controlled experiments that isolate the effect of TMK structure: compare TMK-JSON to a non-hierarchical JSON dictionary of actions, to a PDDL domain description, and to a flat list of action signatures.
- Report results over multiple runs (e.g., 3-5) with confidence intervals or standard deviations.
- Validate the modified extraction against the official PlanBench validator on a held-out set of model outputs to ensure no false positives.
- Include a comparison with CoT or ReACT baselines under the same one-shot setting.
- Analyze model output lengths or errors to understand where TMK helps or hurts.

## Novel Insights

None beyond the paper's own contributions; the core idea (structured knowledge representation as prompt) is potentially valuable but the current experiments do not clearly isolate its effect.

## Suggestions

- Add ablation experiments: (1) TMK-JSON vs. plain-text JSON (same actions listed as key-value pairs), (2) TMK vs. a PDDL-style domain description, (3) TMK vs. a flat list of action definitions in natural language. This would separate the effect of "structured symbolic format" from "TMK-specific hierarchical/telological structure."
- Report multiple independent runs for each condition and provide confidence intervals.
- Clarify the exact differences between the TMK prompt and the baseline plain-text prompt (preferably include both in the appendix for inspection).

## Score and Decision

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>