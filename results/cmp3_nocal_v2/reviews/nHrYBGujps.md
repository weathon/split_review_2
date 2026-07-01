## Summary

This paper introduces BIRD-INTERACT, a benchmark for evaluating text-to-SQL systems in a multi-turn interactive setting. It builds on LIVESQLBENCH by injecting ambiguities into tasks, adding follow-up sub-tasks with state dependency, and providing a function-driven user simulator with controlled response actions (AMB/LOC/UNA). Two evaluation settings are proposed: *c*-Interact (protocol-guided conversation) and *a*-Interact (agentic tool-use with budget constraints). The benchmark comprises 600 tasks (FULL) and 300 tasks (LITE). Experiments with 7 frontier LLMs show the benchmark is challenging (best model achieves ~17% end-to-end success on FULL), reveal non-obvious cross-setting performance dissociations (e.g., GPT-5 worst at c-Interact but best at a-Interact), and provide Interaction Test-Time Scaling analysis.

## Strengths

1. **Well-motivated gap identification.** Section 1 precisely identifies two shortcomings of existing text-to-SQL benchmarks: reliance on static conversation transcripts that every model sees identically, and a narrow SELECT-only scope that excludes DML/DDL operations. The paper provides concrete examples (Figure 1) of ambiguity resolution, error recovery, and evolving goals that current benchmarks cannot capture.

2. **Principled function-driven user simulator with strong validation.** The two-stage approach (classify into AMB/LOC/UNA → generate controlled response) is a methodological improvement over naive LLM-as-user simulators. The USERSIM-GUARD evaluation (Figure 6) provides concrete evidence: baseline simulators fail on 40–67% of Unanswerable questions, while the function-driven approach reduces this to 2.7–10%. This is a genuine reliability gain, not a marginal one.

3. **Human alignment study (Table 3) sets a good standard for benchmark papers.** The simulator's task-level rankings correlate with human users at r=0.84 (p=0.02) for GPT-4o with function calling, versus r=0.61 (p=0.14) without. This directly addresses the concern that an automated simulator might rank models differently than real users would, and this kind of validation is exactly what a benchmark paper should provide.

4. **Cross-setting dissociations demonstrate the benchmark measures something new.** GPT-5 is worst among frontier models at c-Interact (14.50% priority SR) but best at a-Interact (29.17% priority SR). This kind of pattern would not emerge from single-turn or single-paradigm evaluation, validating that the benchmark captures different dimensions of model capability.

5. **Interaction Test-Time Scaling analysis yields actionable insights.** Figure 4 shows that some models (Claude-3.7-Sonnet) improve monotonically with more interaction turns while others plateau. The "ITS Law" framing—whether a model can match its idealized single-turn performance given enough turns—provides a concrete behavioral criterion for evaluation beyond raw accuracy.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **The high-level framing overstates the openness of the interaction.** The abstract and introduction describe "dynamic interactions" and a "complete interactive problem-solving process," but the actual interaction space is substantially constrained: ambiguities are pre-annotated with corresponding SQL snippets (Section 3.2), the simulator's meaningful responses are limited to three action classes (AMB/LOC/UNA, Section 3.3), and each task has exactly two pre-sequenced sub-tasks. The paper is transparent about these design choices, but the consistent use of "dynamic" and "autonomous" framing risks leading readers to expect more open-ended dialogue than the benchmark actually tests. The benchmark is best understood as a *structured, controlled interaction test*—valuable in its own right, but the framing should be calibrated accordingly.

2. **The memory grafting experiment (Section 5.2) is over-interpreted.** The experiment provides GPT-5 with ambiguity-resolution histories from Qwen-3-Coder and O3-mini and shows improved performance (from 13.8% to 18.8%/20.5%). The paper concludes that "GPT-5 possesses robust SQL generation capabilities" and a "more effective communication schema is required." However, the grafted condition gives GPT-5 several simultaneous advantages: no budget cost for acquiring information, guaranteed correct clarification, and elimination of the planning burden. A controlled experiment equating the budget available for SQL generation between conditions would be needed to isolate "communication ability" as the specific bottleneck. The experiment supports the weaker claim (GPT-5 can write SQL when given ideal information at no cost) but not the stronger claim (communication is the specific deficit).

3. **GT SQL leakage characterization is incomplete.** The simulator generates responses based on "the annotated GT SQL with clarification source" (Section 3.3). The USERSIM-GUARD evaluation validates *action classification* accuracy but does not analyze whether the *generated response content* contains systematically more information than a human would naturally provide (e.g., naming exact column names and thresholds instead of giving vaguer cues). The human alignment study (Table 3) partially addresses this by showing rank-order correlation, but rank correlation can be high even if the simulator systematically provides more (or less) information, as long as relative task difficulty is preserved.

4. **Single-turn baselines are missing from the main results table.** Figure 4 includes "Idealized Performance" (ambiguity-free single-turn accuracy) for 4 models on the LITE set, but Table 2 (BIRD-INTERACT-FULL, all 7 models) does not report single-turn baselines. Since the paper argues that the interactive setting reveals deficits that single-turn evaluation misses, including these baselines for all models on the FULL set would strengthen this argument and allow readers to assess the interaction gap directly.

5. **The simulator backbone for the main evaluation (Table 2) is not specified.** The USERSIM-GUARD evaluation and human alignment study identify the backbone models (GPT-4o, Gemini-2.0-Flash, and an "AMG" variant), but the main experimental results do not state which LLM powers the user simulator during those evaluations. This matters because the quality of the simulator's responses affects the conclusions drawn about the evaluated models.

6. **The "Inter-Agreement" metric (Table 1) is not defined.** The table reports values of 93.33 and 93.50, but the paper does not specify whether this is percentage agreement, Cohen's kappa, or another metric, or over what units it is computed (e.g., agreement on which ambiguities to inject vs. agreement on specific SQL clarification sources).

### Trivial
None.

## Nice-to-Haves

- **Budget parameter justification.** The default values (λ\_pat = 3, B\_base = 6) are stated without explanation of whether they were derived from pilot experiments or theoretical reasoning. A brief justification would help readers understand the design rationale.

- **State dependency validation.** The paper claims that follow-up sub-tasks require reasoning over modified database state from the preceding sub-task (Section 3.2). An ablation showing that models perform worse on the follow-up without access to the first sub-task's output would directly validate this design feature.

- **Single-run limitation acknowledgment.** The paper acknowledges single runs due to cost (Section 5). While temperature=0 makes this defensible for most models, a brief discussion of potential variance for reasoning models with stochastic decoding would be helpful.

- **Response content analysis.** A human-in-the-loop comparison of simulator vs. human responses along dimensions like specificity (number of columns/values named) would directly address the leakage concern in Weakness 3.

## Removed Points

*These points were flagged for removal from the input review; they are listed here for optional reference but should not be treated as active weaknesses.*

- A claim that the inter-annotator agreement being "suspiciously high" might indicate the task was too constrained. This is speculation without evidence, and the paper describes a rigorous multi-stage annotation process (Appendix C). Removed per the rule against speculative concerns.
- A claim that "virtually all existing systems are evaluated only in single-turn settings" in the Related Work is inaccurate. This was the harsh reviewer's comment, not a weakness of the paper. Removed as not a weakness.
- Various presentation/polish suggestions (e.g., "the paper would benefit from more precise language") that are formatting/preference comments. Removed per the rule against pure presentation nitpicks.
- The comment that "the explanation for DM being easier than BI is asserted without evidence." The paper provides a brief explanation ("DM operations follow standardized, predictable patterns") that is a reasonable observation, not a core claim requiring extensive evidence. Weakened; moved here as insubstantial.
- Concerns about the appendix being missing or details deferred to appendix (e.g., "full details in Appendix 12 and 13"). The parser strips appendices from all papers; these sections exist in the original submission. Removed per hard rule.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Calibrate the framing.** Replace "dynamic interaction" with "controlled interaction" or "structured multi-turn interaction" in high-level descriptions. The constraints (pre-annotated ambiguities, 2 sub-tasks, budget limits) are design virtues, not things to hedge about—being precise about what the benchmark measures would strengthen it.

2. **Add single-turn baselines to Table 2.** Report the ambiguity-free single-turn success rate for each model on the same BIRD-INTERACT-FULL tasks. This directly supports the paper's central argument that interaction reveals deficits that single-turn evaluation misses.

3. **Specify the simulator backbone for the main evaluation.** State which LLM powers the user simulator in the Table 2 experiments, and briefly note how results might vary with different backbones.

4. **Reframe the memory grafting conclusion.** Replace "GPT-5's deficit is in communication ability" with "GPT-5's SQL generation is competitive when given the right information at no interaction cost; the bottleneck is in the *interaction process* itself (information acquisition, planning, or budget management)."

5. **Define the inter-annotator agreement metric** in the Table 1 caption.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>